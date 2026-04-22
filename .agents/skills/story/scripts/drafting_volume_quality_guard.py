#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
drafting_volume_quality_guard.py - pre-validation quality gate for story2026 drafting

用途：
- 在卷级 `candidate_volume_draft` 之后、进入 `4-Validation` 之前，阻止“工序完整但整体写平”的卷继续下游
- 统一消费 `第V卷.写作日志.yaml -> quality_gate_snapshot`
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any, Optional

try:
    import yaml
except ImportError:  # pragma: no cover
    yaml = None

from project_locator import resolve_project_root
from runtime_compat import enable_windows_utf8_stdio, normalize_windows_path


READY_VERDICT = "ready_for_validation"
BLOCK_VERDICT = "rework_required_before_validation"
REQUIRED_AXES = (
    "anti_formula_progression",
    "relationship_friction",
    "spatial_separation",
    "antagonist_face",
    "volume_closure",
)


def _resolve_project_root(raw: Optional[str]) -> Path:
    if raw:
        return resolve_project_root(str(Path(normalize_windows_path(raw)).resolve()))
    return resolve_project_root()


def _load_yaml(path: Path) -> dict[str, Any]:
    if yaml is None:
        raise RuntimeError("PyYAML is required for drafting_volume_quality_guard.py")
    if not path.is_file():
        return {}
    payload = yaml.safe_load(path.read_text(encoding="utf-8"))
    return payload if isinstance(payload, dict) else {}


def _resolve_write_log_path(project_root: Path, volume_num: int, explicit_path: Optional[str]) -> Path:
    if explicit_path:
        return Path(normalize_windows_path(explicit_path)).resolve()
    if volume_num <= 0:
        raise ValueError("volume_num must be positive when --write-log is omitted")
    return project_root / "3-Drafting" / f"第{volume_num}卷.写作日志.yaml"


def _normalized_list(value: Any) -> list[str]:
    if not isinstance(value, list):
        return []
    out: list[str] = []
    for item in value:
        text = str(item or "").strip()
        if text:
            out.append(text)
    return out


def _extract_snapshot(write_log_payload: dict[str, Any]) -> tuple[dict[str, Any], str]:
    snapshot = write_log_payload.get("quality_gate_snapshot")
    if isinstance(snapshot, dict):
        return snapshot, "quality_gate_snapshot"
    legacy = write_log_payload.get("post_review_summary")
    if isinstance(legacy, dict):
        return legacy, "post_review_summary"
    return {}, ""


def validate_quality_snapshot(
    snapshot: dict[str, Any],
    *,
    snapshot_key: str = "quality_gate_snapshot",
    chapter_refs: Optional[list[str]] = None,
) -> dict[str, Any]:
    refs = chapter_refs or []
    issues: list[dict[str, str]] = []
    if not snapshot:
        return {
            "status": "block",
            "reason": "missing_quality_gate_snapshot",
            "issues": [{"code": "missing_quality_gate_snapshot", "message": "missing quality_gate_snapshot in write log"}],
            "metrics": {"required_axes": len(REQUIRED_AXES), "passed_axes": 0},
            "snapshot_key": snapshot_key,
        }

    review_mode = str(snapshot.get("review_mode") or "").strip()
    reviewed_at = str(snapshot.get("reviewed_at") or "").strip()
    reviewer_source = str(snapshot.get("reviewer_source") or "").strip()
    verdict = str(snapshot.get("verdict") or "").strip()
    next_action = str(snapshot.get("next_action") or "").strip()
    checkpoint_stage = str(snapshot.get("checkpoint_stage") or "pre_validation").strip()
    reviewers = _normalized_list(snapshot.get("reviewers"))
    representative_refs = _normalized_list(snapshot.get("representative_chapter_refs"))
    primary_issues = _normalized_list(snapshot.get("primary_issues"))
    rework_targets = _normalized_list(snapshot.get("priority_rework_targets"))
    raw_axes = snapshot.get("guard_axes")
    axes = raw_axes if isinstance(raw_axes, dict) else {}

    if checkpoint_stage != "pre_validation":
        issues.append(
            {
                "code": "invalid_checkpoint_stage",
                "message": f"checkpoint_stage must be pre_validation, got {checkpoint_stage or '<empty>'}",
            }
        )
    if not review_mode:
        issues.append({"code": "missing_review_mode", "message": "review_mode is required"})
    if not reviewed_at:
        issues.append({"code": "missing_reviewed_at", "message": "reviewed_at is required"})
    if verdict not in {READY_VERDICT, BLOCK_VERDICT}:
        issues.append(
            {
                "code": "invalid_verdict",
                "message": f"verdict must be {READY_VERDICT} or {BLOCK_VERDICT}",
            }
        )
    if reviewer_source != "self-audit" and not reviewers:
        issues.append({"code": "missing_reviewers", "message": "reviewers are required unless reviewer_source == self-audit"})
    if not representative_refs:
        issues.append(
            {
                "code": "missing_representative_chapter_refs",
                "message": "representative_chapter_refs must contain reviewed chapters",
            }
        )
    if refs:
        missing_refs = [item for item in representative_refs if item not in refs]
        if missing_refs:
            issues.append(
                {
                    "code": "representative_refs_out_of_scope",
                    "message": f"representative refs not in current volume chapter_refs: {', '.join(missing_refs)}",
                }
            )

    passed_axes = 0
    missing_axes: list[str] = []
    blocked_axes: list[str] = []
    for axis in REQUIRED_AXES:
        status = str(axes.get(axis) or "").strip()
        if not status:
            missing_axes.append(axis)
            continue
        if status == "pass":
            passed_axes += 1
        else:
            blocked_axes.append(axis)
    if missing_axes:
        issues.append(
            {
                "code": "missing_guard_axes",
                "message": f"missing guard_axes: {', '.join(missing_axes)}",
            }
        )
    if blocked_axes:
        issues.append(
            {
                "code": "blocked_guard_axes",
                "message": f"blocked guard axes: {', '.join(blocked_axes)}",
            }
        )
    if verdict == READY_VERDICT and next_action != "4-Validation":
        issues.append(
            {
                "code": "invalid_next_action_for_ready",
                "message": f"ready verdict requires next_action=4-Validation, got {next_action or '<empty>'}",
            }
        )
    if verdict == BLOCK_VERDICT:
        if next_action != "3-Drafting-rework":
            issues.append(
                {
                    "code": "invalid_next_action_for_block",
                    "message": f"block verdict requires next_action=3-Drafting-rework, got {next_action or '<empty>'}",
                }
            )
        if not primary_issues:
            issues.append(
                {
                    "code": "missing_primary_issues",
                    "message": "primary_issues cannot be empty when verdict requires rework",
                }
            )
        if not rework_targets:
            issues.append(
                {
                    "code": "missing_priority_rework_targets",
                    "message": "priority_rework_targets cannot be empty when verdict requires rework",
                }
            )

    if snapshot_key == "post_review_summary" and verdict == READY_VERDICT and not axes:
        issues.append(
            {
                "code": "legacy_snapshot_missing_guard_axes",
                "message": "legacy post_review_summary cannot directly pass quality gate without guard_axes",
            }
        )

    status = "pass"
    reason = "volume_quality_gate_passed"
    if verdict == BLOCK_VERDICT:
        status = "block"
        reason = "quality_rework_required_before_validation"
    if issues:
        status = "block"
        if reason == "volume_quality_gate_passed":
            reason = "volume_quality_gate_failed"

    return {
        "status": status,
        "reason": reason,
        "snapshot_key": snapshot_key,
        "metrics": {
            "required_axes": len(REQUIRED_AXES),
            "passed_axes": passed_axes,
            "reviewer_count": len(reviewers),
            "representative_chapter_count": len(representative_refs),
        },
        "verdict": verdict,
        "next_action": next_action,
        "blocked_axes": blocked_axes,
        "issues": issues,
        "priority_rework_targets": rework_targets,
        "representative_chapter_refs": representative_refs,
    }


def validate_volume_log(
    write_log_path: Path,
    *,
    volume_num: int = 0,
) -> dict[str, Any]:
    if not write_log_path.is_file():
        return {
            "status": "block",
            "reason": "missing_write_log",
            "issues": [{"code": "missing_write_log", "message": f"missing write log: {write_log_path}"}],
            "metrics": {"required_axes": len(REQUIRED_AXES), "passed_axes": 0},
            "write_log_path": str(write_log_path),
        }
    payload = _load_yaml(write_log_path)
    chapter_refs = _normalized_list(payload.get("chapter_refs"))
    snapshot, snapshot_key = _extract_snapshot(payload)
    if volume_num <= 0:
        volume_num = int(payload.get("volume_num") or 0)
    result = validate_quality_snapshot(snapshot, snapshot_key=snapshot_key or "quality_gate_snapshot", chapter_refs=chapter_refs)
    result["write_log_path"] = str(write_log_path)
    result["volume_num"] = volume_num
    result["chapter_refs"] = chapter_refs
    return result


def validate_project_volume(
    project_root: Path,
    volume_num: int,
    *,
    write_log_path: Optional[Path] = None,
) -> dict[str, Any]:
    resolved = write_log_path or (project_root / "3-Drafting" / f"第{volume_num}卷.写作日志.yaml")
    return validate_volume_log(resolved, volume_num=volume_num)


def main(argv: Optional[list[str]] = None) -> int:
    parser = argparse.ArgumentParser(description="pre-validation volume quality guard")
    parser.add_argument("--project-root", help="project root path")
    parser.add_argument("--volume", type=int, help="volume number")
    parser.add_argument("--write-log", help="explicit write log path")
    args = parser.parse_args(argv)

    project_root = _resolve_project_root(args.project_root)
    write_log_path = _resolve_write_log_path(project_root, int(args.volume or 0), args.write_log)
    result = validate_project_volume(
        project_root,
        int(args.volume or 0) or int(_load_yaml(write_log_path).get("volume_num") or 0),
        write_log_path=write_log_path,
    )
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result.get("status") == "pass" else 2


if __name__ == "__main__":
    enable_windows_utf8_stdio(skip_in_pytest=True)
    raise SystemExit(main())
