#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
story2026 validated actualization manager.

只负责 `5-Loopback` 的 PASS-only 回写闭环：
- 生成 loopback artifact
- 回写 Cards.current_state/history
- 回写 story_map.actualization
- 刷新下一轮 projection / runtime markers
"""

from __future__ import annotations

import argparse
import copy
import json
from pathlib import Path
from typing import Any, Dict, Iterable, List

from planning_paths import canonical_planning_artifact_relpath, resolve_planning_artifact_path
from project_locator import resolve_project_root, resolve_state_file
from runtime_compat import enable_windows_utf8_stdio
from security_utils import atomic_write_json, create_secure_directory, sanitize_filename


def _scripts_dir() -> Path:
    return Path(__file__).resolve().parent


def _story2026_root() -> Path:
    return _scripts_dir().parent


def _template_path() -> Path:
    return _story2026_root() / "5-Loopback" / "templates" / "loopback.json"


def _load_json_file(path: Path) -> Dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def _load_json_arg(raw: str) -> Dict[str, Any]:
    if raw.startswith("@"):
        return _load_json_file(Path(raw[1:]))
    return json.loads(raw)


def _deep_merge(base: Dict[str, Any], patch: Dict[str, Any]) -> Dict[str, Any]:
    merged = copy.deepcopy(base)
    for key, value in patch.items():
        if isinstance(value, dict) and isinstance(merged.get(key), dict):
            merged[key] = _deep_merge(merged[key], value)
        else:
            merged[key] = copy.deepcopy(value)
    return merged


def _project_name(project_root: Path, state: Dict[str, Any]) -> str:
    project_info = state.get("project_info", {}) if isinstance(state.get("project_info"), dict) else {}
    raw_name = (
        project_info.get("title")
        or project_info.get("name")
        or project_info.get("project_name")
        or project_root.name
    )
    return sanitize_filename(str(raw_name), max_length=80)


def _relpath(path: Path, project_root: Path) -> str:
    try:
        return str(path.relative_to(project_root))
    except ValueError:
        return str(path)


def _build_artifact_path(project_root: Path, state: Dict[str, Any], episode: int) -> Path:
    output_dir = project_root / "Loopback"
    create_secure_directory(str(output_dir))
    return output_dir / f"第{episode}集.loopback.json"


def _load_template() -> Dict[str, Any]:
    path = _template_path()
    if not path.is_file():
        raise FileNotFoundError(f"缺少 loopback 模板: {path}")
    return _load_json_file(path)


def _normalize_delta_payload(
    validation_payload: Dict[str, Any],
    explicit_delta: Dict[str, Any] | None,
) -> Dict[str, List[Dict[str, Any]]]:
    if explicit_delta is not None:
        source = explicit_delta
    else:
        source = (
            validation_payload.get("loopback_delta")
            if isinstance(validation_payload.get("loopback_delta"), dict)
            else validation_payload
        )

    return {
        "card_deltas": list(source.get("card_deltas") or []),
        "map_deltas": list(source.get("map_deltas") or []),
        "projection_refresh": list(source.get("projection_refresh") or []),
        "evidence_refs": list(source.get("evidence_refs") or []),
    }


def _map_bucket_key(bucket: str) -> str:
    mapping = {
        "episode_nodes": "episode_ref",
        "clue_points": "clue_ref",
        "foreshadow_points": "foreshadow_ref",
        "promise_threads": "thread_ref",
        "suspense_threads": "thread_ref",
        "tasklines": "taskline_ref",
        "threads": "thread_ref",
    }
    if bucket not in mapping:
        raise ValueError(f"不支持的 map bucket: {bucket}")
    return mapping[bucket]


def _default_projection_path(target_type: str) -> list[str]:
    mapping = {
        "writer_projection": ["setting_route_packet", "writer_context_projection", "memory_projection"],
        "planning_projection": ["planning_projection"],
        "query_projection": ["query_projection"],
        "carryover_context": ["carryover_context"],
    }
    if target_type not in mapping:
        raise ValueError(f"不支持的 projection target_type: {target_type}")
    return list(mapping[target_type])


def _set_nested_value(payload: Dict[str, Any], path: Iterable[str], value: Any) -> None:
    parts = [part for part in path if part]
    if not parts:
        raise ValueError("nested path 不能为空")

    current = payload
    for part in parts[:-1]:
        next_value = current.get(part)
        if not isinstance(next_value, dict):
            next_value = {}
            current[part] = next_value
        current = next_value
    current[parts[-1]] = copy.deepcopy(value)


def _apply_projection_refresh(
    state: Dict[str, Any],
    projection_refresh: List[Dict[str, Any]],
) -> List[str]:
    refreshed_refs: List[str] = []
    for item in projection_refresh:
        if not isinstance(item, dict):
            continue

        target_type = str(item.get("target_type") or "").strip()
        payload = copy.deepcopy(item.get("payload") or {})
        target_ref = str(item.get("target_ref") or "").strip()

        if target_type == "runtime_marker":
            state.setdefault("runtime_markers", {})
            if not isinstance(state["runtime_markers"], dict):
                state["runtime_markers"] = {}
            marker_name = target_ref or "loopback"
            state["runtime_markers"][marker_name] = payload
            refreshed_refs.append(f"runtime_markers.{marker_name}")
            continue

        nested_path = _default_projection_path(target_type)
        _set_nested_value(state, nested_path, payload)
        refreshed_refs.append(".".join(nested_path))

    return refreshed_refs


def _apply_map_deltas(holomap: Dict[str, Any], map_deltas: List[Dict[str, Any]]) -> List[str]:
    holomap_root = holomap.setdefault("content", {}).setdefault("holomap", {})
    actualization = holomap_root.setdefault(
        "actualization",
        {
            "write_policy": "actualization-only",
            "episode_nodes": [],
            "clue_points": [],
            "foreshadow_points": [],
            "promise_threads": [],
            "suspense_threads": [],
            "tasklines": [],
            "threads": [],
        },
    )

    written_refs: List[str] = []
    for item in map_deltas:
        if not isinstance(item, dict):
            continue

        bucket = str(item.get("target_bucket") or "").strip()
        key_name = _map_bucket_key(bucket)
        patch = copy.deepcopy(item.get("actualization_patch") or {})
        target_ref = str(item.get("target_ref") or "").strip()
        match_value = str(patch.get(key_name) or target_ref or "").strip()
        if not match_value:
            raise ValueError(f"{bucket} 缺少 target_ref/{key_name}")

        entries = actualization.setdefault(bucket, [])
        if not isinstance(entries, list):
            raise ValueError(f"actualization.{bucket} 必须是数组")

        match = None
        for row in entries:
            if isinstance(row, dict) and str(row.get(key_name) or "").strip() == match_value:
                match = row
                break

        if match is None:
            new_entry = copy.deepcopy(patch)
            new_entry.setdefault(key_name, match_value)
            entries.append(new_entry)
        else:
            match.update(patch)

        written_refs.append(f"{bucket}:{target_ref or match_value}")

    return written_refs


def _apply_card_deltas(
    project_root: Path,
    artifact_ref: str,
    validation_ref: str,
    card_deltas: List[Dict[str, Any]],
) -> List[str]:
    written_refs: List[str] = []
    for item in card_deltas:
        if not isinstance(item, dict):
            continue

        target_ref = str(item.get("target_ref") or "").strip()
        if not target_ref:
            raise ValueError("card_delta.target_ref 不能为空")

        target_path = (project_root / target_ref).resolve()
        if not target_path.is_file():
            raise FileNotFoundError(f"Card 文件不存在: {target_path}")

        payload = _load_json_file(target_path)
        if not isinstance(payload, dict):
            raise ValueError(f"Card JSON 非对象: {target_path}")

        payload.setdefault("current_state", {})
        payload.setdefault("history", [])

        current_patch = item.get("current_state_patch") or {}
        if isinstance(current_patch, dict):
            payload["current_state"] = _deep_merge(payload["current_state"], current_patch)

        history_append = copy.deepcopy(item.get("history_append") or {})
        if history_append:
            history_append.setdefault("validation_ref", validation_ref)
            history_append["loopback_ref"] = artifact_ref
            payload["history"].append(history_append)

        atomic_write_json(target_path, payload, use_lock=True, backup=True)
        written_refs.append(target_ref)

    return written_refs


def _derive_actual_outcome_summary(map_deltas: List[Dict[str, Any]]) -> str:
    for item in map_deltas:
        if not isinstance(item, dict):
            continue
        patch = item.get("actualization_patch") or {}
        summary = str(patch.get("actual_outcome_summary") or "").strip()
        if summary:
            return summary
    return ""


def _build_artifact(
    template: Dict[str, Any],
    *,
    project_root: Path,
    state: Dict[str, Any],
    episode: int,
    manuscript_ref: str,
    validation_ref: str,
    draft_packet_ref: str,
    story_map_ref: str,
    delta_payload: Dict[str, List[Dict[str, Any]]],
    artifact_ref: str,
) -> Dict[str, Any]:
    artifact = copy.deepcopy(template)
    meta = artifact.setdefault("meta", {})
    meta["project_name"] = _project_name(project_root, state)
    meta["episode_ref"] = f"第{episode}集"
    meta["created_at"] = ""
    meta["loopback_ref"] = artifact_ref

    inputs = artifact.setdefault("inputs", {})
    inputs["project_root"] = str(project_root)
    inputs["manuscript_ref"] = manuscript_ref
    inputs["validation_ref"] = validation_ref
    inputs["draft_packet_ref"] = draft_packet_ref
    inputs["story_map_ref"] = story_map_ref
    inputs["validation_status"] = "PASS"

    content = artifact.setdefault("content", {})
    loopback_delta = content.setdefault("loopback_delta", {})
    loopback_delta["card_deltas"] = copy.deepcopy(delta_payload["card_deltas"])
    loopback_delta["map_deltas"] = copy.deepcopy(delta_payload["map_deltas"])
    loopback_delta["projection_refresh"] = copy.deepcopy(delta_payload["projection_refresh"])
    loopback_delta["evidence_refs"] = copy.deepcopy(delta_payload["evidence_refs"])
    writeback_summary = content.setdefault("writeback_summary", {})
    writeback_summary.setdefault("written_card_refs", [])
    writeback_summary.setdefault("written_map_refs", [])
    writeback_summary.setdefault("refreshed_projection_refs", [])

    gate_summary = artifact.setdefault("gate_summary", {})
    gate_summary["status"] = "PASS"
    gate_summary["validation_gate"] = "PASS-only"
    gate_summary.setdefault("fail_codes", [])
    gate_summary.setdefault("repair_entry", "")

    execution_notes = artifact.setdefault("execution_notes", {})
    execution_notes["actual_outcome_summary"] = _derive_actual_outcome_summary(delta_payload["map_deltas"])
    execution_notes.setdefault("risk_notes", "")

    return artifact


def actualize(args: argparse.Namespace) -> int:
    project_root = resolve_project_root(str(args.project_root))
    state_path = resolve_state_file(explicit_project_root=str(project_root))
    requested_story_map_rel = str(args.story_map_ref or "").strip()
    story_map_rel = requested_story_map_rel or canonical_planning_artifact_relpath("holomap")
    if requested_story_map_rel:
        story_map_path = project_root / requested_story_map_rel
    else:
        story_map_path = resolve_planning_artifact_path(project_root, "holomap")

    if not state_path.is_file():
        raise SystemExit(f"缺少 STATE.json: {state_path}")
    if not story_map_path.is_file():
        raise SystemExit(f"缺少 story_map: {story_map_path}")

    state = _load_json_file(state_path)
    validation_payload = _load_json_arg(args.validation_data)
    validation_status = str(validation_payload.get("validation_status") or "").strip()
    if validation_status != "PASS":
        print(
            json.dumps(
                {
                    "ok": False,
                    "error": "validation_status_must_be_pass",
                    "validation_status": validation_status or "missing",
                },
                ensure_ascii=False,
                indent=2,
            )
        )
        return 1

    delta_payload = _normalize_delta_payload(
        validation_payload,
        _load_json_arg(args.loopback_delta) if args.loopback_delta else None,
    )
    artifact_path = _build_artifact_path(project_root, state, args.episode)
    artifact_ref = _relpath(artifact_path, project_root)
    validation_ref = str(
        args.validation_ref
        or validation_payload.get("validation_ref")
        or validation_payload.get("report_file")
        or ""
    ).strip()

    artifact = _build_artifact(
        _load_template(),
        project_root=project_root,
        state=state,
        episode=args.episode,
        manuscript_ref=args.manuscript_ref,
        validation_ref=validation_ref,
        draft_packet_ref=str(args.draft_packet_ref or ""),
        story_map_ref=story_map_rel,
        delta_payload=delta_payload,
        artifact_ref=artifact_ref,
    )

    written_card_refs = _apply_card_deltas(
        project_root,
        artifact_ref,
        validation_ref,
        delta_payload["card_deltas"],
    )

    holomap = _load_json_file(story_map_path)
    written_map_refs = _apply_map_deltas(holomap, delta_payload["map_deltas"])
    atomic_write_json(story_map_path, holomap, use_lock=True, backup=True)

    refreshed_projection_refs = _apply_projection_refresh(state, delta_payload["projection_refresh"])
    atomic_write_json(state_path, state, use_lock=True, backup=True)

    artifact["content"]["writeback_summary"]["written_card_refs"] = written_card_refs
    artifact["content"]["writeback_summary"]["written_map_refs"] = written_map_refs
    artifact["content"]["writeback_summary"]["refreshed_projection_refs"] = refreshed_projection_refs
    atomic_write_json(artifact_path, artifact, use_lock=True, backup=False)

    print(
        json.dumps(
            {
                "ok": True,
                "loopback_ref": artifact_ref,
                "episode_ref": f"第{args.episode}集",
                "validation_ref": validation_ref,
                "validation_status": "PASS",
                "card_deltas": delta_payload["card_deltas"],
                "map_deltas": delta_payload["map_deltas"],
                "projection_refresh": delta_payload["projection_refresh"],
                "evidence_refs": delta_payload["evidence_refs"],
                "written_card_refs": written_card_refs,
                "written_map_refs": written_map_refs,
                "refreshed_projection_refs": refreshed_projection_refs,
            },
            ensure_ascii=False,
            indent=2,
        )
    )
    return 0


def main() -> None:
    parser = argparse.ArgumentParser(description="story2026 loopback actualization manager")
    parser.add_argument("--project-root", required=True, help="书项目根目录或工作区根目录")
    sub = parser.add_subparsers(dest="command", required=True)

    p_actualize = sub.add_parser("actualize", help="执行 PASS-only loopback actualization")
    p_actualize.add_argument("--episode", type=int, required=True, help="目标 episode/chapter 编号")
    p_actualize.add_argument("--validation-data", required=True, help="验证聚合结果 JSON 或 @文件路径")
    p_actualize.add_argument("--manuscript-ref", required=True, help="正文稿件路径（相对 project_root）")
    p_actualize.add_argument("--validation-ref", help="验证报告路径（相对 project_root）")
    p_actualize.add_argument("--draft-packet-ref", help="可选 draft packet 引用")
    p_actualize.add_argument("--story-map-ref", default=canonical_planning_artifact_relpath("holomap"), help="story_map 相对路径")
    p_actualize.add_argument("--loopback-delta", help="可选 loopback delta JSON 或 @文件路径")
    p_actualize.set_defaults(func=actualize)

    args = parser.parse_args()
    raise SystemExit(int(args.func(args) or 0))


if __name__ == "__main__":
    enable_windows_utf8_stdio(skip_in_pytest=True)
    main()
