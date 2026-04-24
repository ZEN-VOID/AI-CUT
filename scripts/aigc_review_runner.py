#!/usr/bin/env python3
"""Governed runner for `aigc/review`.

This runner upgrades `aigc/review` from a seeded aggregate packet generator to
an executable review bus with:

- shared `review_fact_pack` writeback
- automatic `code-reviewer` provider dispatch
- dimension-level packet/report generation
- aggregate gate + repair plan generation
- optional `governance-state.yaml` review bridge synchronization
"""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
import time
from copy import deepcopy
from pathlib import Path
from typing import Any

import yaml


ROOT = Path(".agents/skills/aigc/review")
REGISTRY = ROOT / "_shared" / "review-dimension-registry.yaml"
AGGREGATE_TEMPLATE = ROOT / "_shared" / "review-aggregate.template.json"
REPORT_TEMPLATE = ROOT / "_shared" / "review-dimension-report.template.md"
EXECUTION_PROVIDER_CONFIG = ROOT / "_shared" / "execution-provider.yaml"

STAGE_ACCEPTANCE_PASS_TARGETS = {
    "1-Planning": ["2-Global"],
    "2-Global": ["3-Detail"],
    "3-Detail": ["4-Design", "5-Image", "6-Video"],
    "4-Design": ["5-Image"],
    "5-Image": ["6-Video"],
    "6-Video": ["release"],
}

SOURCE_LAYER_OWNERS = {
    "0-Init",
    "1-Planning",
    "2-Global",
    "3-Detail",
    "root-aigc",
    "project-runtime",
}

SEVERITY_ORDER = {
    "critical": 4,
    "high": 3,
    "medium": 2,
    "low": 1,
}


def _default_codex_home() -> Path:
    configured = os.environ.get("CODEX_HOME")
    if configured:
        return Path(configured).expanduser()
    return Path.home() / ".codex"


def load_execution_provider() -> dict[str, Any]:
    defaults = {
        "provider_id": "code-reviewer",
        "skill_relative_to_codex_home": "skills/meta/构建/架构/code-reviewer/SKILL.md",
        "checker_script_relative_to_codex_home": "skills/meta/构建/架构/code-reviewer/scripts/code_quality_checker.py",
        "reporter_script_relative_to_codex_home": "skills/meta/构建/架构/code-reviewer/scripts/review_report_generator.py",
        "artifact_dir_name": ".code-reviewer",
        "timeout_seconds": 60.0,
    }
    loaded: dict[str, Any] = {}
    if EXECUTION_PROVIDER_CONFIG.is_file():
        payload = yaml.safe_load(EXECUTION_PROVIDER_CONFIG.read_text(encoding="utf-8")) or {}
        if isinstance(payload, dict):
            loaded = payload
    config = {**defaults, **loaded}
    codex_home = _default_codex_home()
    return {
        **config,
        "codex_home": codex_home,
        "skill_path": codex_home / str(config["skill_relative_to_codex_home"]),
        "checker_script_path": codex_home / str(config["checker_script_relative_to_codex_home"]),
        "reporter_script_path": codex_home / str(config["reporter_script_relative_to_codex_home"]),
        "timeout_seconds": float(config.get("timeout_seconds") or defaults["timeout_seconds"]),
    }


EXECUTION_PROVIDER = load_execution_provider()
CODE_REVIEWER_PROVIDER_NAME = str(EXECUTION_PROVIDER["provider_id"])
CODE_REVIEWER_CHECKER = Path(EXECUTION_PROVIDER["checker_script_path"])
CODE_REVIEWER_REPORTER = Path(EXECUTION_PROVIDER["reporter_script_path"])
CODE_REVIEWER_TIMEOUT_SECONDS = float(EXECUTION_PROVIDER["timeout_seconds"])

CHECKPOINT_REQUIREMENTS = {
    "planning-handoff-ready": {
        "validation_refs": ["1-Planning/validation-report.md"],
        "source_truth_refs": [
            "0-Init/north_star.yaml",
            "0-Init/init_handoff.yaml",
            "1-Planning/",
        ],
        "runtime_artifact_refs": ["1-Planning/"],
        "handoff_candidate_refs": ["2-Global/"],
    },
    "global-seed-ready": {
        "validation_refs": ["2-Global/validation-report.md"],
        "source_truth_refs": [
            "0-Init/north_star.yaml",
            "1-Planning/",
            "2-Global/第N集.json",
        ],
        "runtime_artifact_refs": ["2-Global/第N集.json"],
        "handoff_candidate_refs": ["3-Detail/"],
    },
    "detail-episode-ready": {
        "validation_refs": ["3-Detail/validation-report.md"],
        "source_truth_refs": [
            "1-Planning/",
            "2-Global/第N集.json",
            "3-Detail/{scope_ref}.json",
        ],
        "runtime_artifact_refs": ["3-Detail/{scope_ref}.json"],
        "handoff_candidate_refs": ["4-Design/", "5-Image/", "6-Video/"],
    },
    "design-list-ready": {
        "validation_refs": ["4-Design/validation-report.md"],
        "source_truth_refs": [
            "3-Detail/{scope_ref}.json",
            "4-Design/",
        ],
        "runtime_artifact_refs": ["4-Design/"],
        "handoff_candidate_refs": ["4-Design/"],
    },
    "design-truth-ready": {
        "validation_refs": ["4-Design/validation-report.md"],
        "source_truth_refs": [
            "3-Detail/{scope_ref}.json",
            "4-Design/",
        ],
        "runtime_artifact_refs": ["4-Design/"],
        "handoff_candidate_refs": ["4-Design/", "5-Image/2-参照引用/"],
    },
    "design-panel-ready": {
        "validation_refs": ["4-Design/validation-report.md"],
        "source_truth_refs": [
            "3-Detail/{scope_ref}.json",
            "4-Design/",
        ],
        "runtime_artifact_refs": ["4-Design/"],
        "handoff_candidate_refs": ["5-Image/"],
    },
    "image-request-ready": {
        "validation_refs": ["5-Image/validation-report.md", "3-Detail/validation-report.md"],
        "source_truth_refs": [
            "3-Detail/{scope_ref}.json",
            "5-Image/1-提示词蒸馏/",
        ],
        "runtime_artifact_refs": ["5-Image/1-提示词蒸馏/"],
        "handoff_candidate_refs": ["5-Image/2-参照引用/"],
    },
    "image-reference-ready": {
        "validation_refs": ["5-Image/validation-report.md"],
        "source_truth_refs": [
            "4-Design/",
            "5-Image/1-提示词蒸馏/",
            "5-Image/2-参照引用/",
        ],
        "runtime_artifact_refs": ["5-Image/2-参照引用/"],
        "handoff_candidate_refs": ["5-Image/3-图像生成/"],
    },
    "image-handoff-ready": {
        "validation_refs": ["5-Image/validation-report.md"],
        "source_truth_refs": [
            "5-Image/2-参照引用/",
            "5-Image/3-图像生成/",
        ],
        "runtime_artifact_refs": ["5-Image/3-图像生成/"],
        "handoff_candidate_refs": ["Assets/", "5-Image/3-图像生成/"],
    },
    "video-request-ready": {
        "validation_refs": ["6-Video/validation-report.md", "3-Detail/validation-report.md"],
        "source_truth_refs": [
            "3-Detail/{scope_ref}.json",
            "6-Video/1-提示词蒸馏/",
        ],
        "runtime_artifact_refs": ["6-Video/1-提示词蒸馏/"],
        "handoff_candidate_refs": ["6-Video/2-参照引用/"],
    },
    "video-reference-ready": {
        "validation_refs": ["6-Video/validation-report.md"],
        "source_truth_refs": [
            "5-Image/",
            "6-Video/1-提示词蒸馏/",
            "6-Video/2-参照引用/",
        ],
        "runtime_artifact_refs": ["6-Video/2-参照引用/"],
        "handoff_candidate_refs": ["6-Video/3-视频生成/"],
    },
    "video-handoff-ready": {
        "validation_refs": ["6-Video/validation-report.md"],
        "source_truth_refs": [
            "6-Video/2-参照引用/",
            "6-Video/3-视频生成/",
        ],
        "runtime_artifact_refs": ["6-Video/3-视频生成/"],
        "handoff_candidate_refs": ["Assets/", "6-Video/3-视频生成/"],
    },
    "package-release-ready": {
        "validation_refs": [
            "1-Planning/validation-report.md",
            "2-Global/validation-report.md",
            "3-Detail/validation-report.md",
            "4-Design/validation-report.md",
            "5-Image/validation-report.md",
            "6-Video/validation-report.md",
        ],
        "source_truth_refs": [
            "0-Init/north_star.yaml",
            "1-Planning/",
            "2-Global/第N集.json",
            "3-Detail/",
            "4-Design/",
            "5-Image/",
            "6-Video/",
        ],
        "runtime_artifact_refs": [
            "1-Planning/",
            "2-Global/",
            "3-Detail/",
            "4-Design/",
            "5-Image/",
            "6-Video/",
        ],
        "handoff_candidate_refs": ["Assets/", "validation-report.md"],
    },
}

STAGE_REQUIREMENTS = {
    "1-Planning": CHECKPOINT_REQUIREMENTS["planning-handoff-ready"],
    "2-Global": CHECKPOINT_REQUIREMENTS["global-seed-ready"],
    "3-Detail": CHECKPOINT_REQUIREMENTS["detail-episode-ready"],
    "4-Design": {
        "validation_refs": ["4-Design/validation-report.md"],
        "source_truth_refs": ["3-Detail/{scope_ref}.json", "4-Design/"],
        "runtime_artifact_refs": ["4-Design/"],
        "handoff_candidate_refs": ["5-Image/", "6-Video/"],
    },
    "5-Image": {
        "validation_refs": ["5-Image/validation-report.md"],
        "source_truth_refs": ["4-Design/", "5-Image/"],
        "runtime_artifact_refs": ["5-Image/"],
        "handoff_candidate_refs": ["6-Video/", "Assets/"],
    },
    "6-Video": {
        "validation_refs": ["6-Video/validation-report.md"],
        "source_truth_refs": ["5-Image/", "6-Video/"],
        "runtime_artifact_refs": ["6-Video/"],
        "handoff_candidate_refs": ["Assets/", "validation-report.md"],
    },
}

DIMENSION_EXPECTATIONS = {
    "planning-seed-validator": {
        "source_prefixes": ["0-Init/", "1-Planning/", "2-Global/", "3-Detail/"],
        "validation_prefixes": ["1-Planning/", "2-Global/", "3-Detail/"],
    },
    "detail-execution-validator": {
        "source_prefixes": ["2-Global/", "3-Detail/"],
        "runtime_prefixes": ["3-Detail/"],
        "validation_prefixes": ["3-Detail/"],
    },
    "design-alignment-validator": {
        "source_prefixes": ["3-Detail/", "4-Design/"],
        "runtime_prefixes": ["4-Design/"],
        "validation_prefixes": ["4-Design/"],
    },
    "image-delivery-validator": {
        "source_prefixes": ["3-Detail/", "4-Design/", "5-Image/"],
        "runtime_prefixes": ["5-Image/"],
        "validation_prefixes": ["5-Image/"],
    },
    "video-delivery-validator": {
        "source_prefixes": ["3-Detail/", "4-Design/", "5-Image/", "6-Video/"],
        "runtime_prefixes": ["6-Video/"],
        "validation_prefixes": ["6-Video/"],
    },
    "governance-closure-validator": {
        "use_fact_pack_validation_refs": True,
        "runtime_refs": ["STATE.json", "team.yaml"],
    },
}


def load_yaml(path: Path) -> dict[str, Any]:
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    return data if isinstance(data, dict) else {}


def load_json(path: Path) -> dict[str, Any]:
    data = json.loads(path.read_text(encoding="utf-8"))
    return data if isinstance(data, dict) else {}


def load_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def sanitize_scope_ref(scope_ref: str) -> str:
    return scope_ref.replace("/", "_").replace("\\", "_").strip()


def checkpoint_spec(registry: dict[str, Any], checkpoint_id: str) -> dict[str, Any]:
    for item in registry.get("checkpoints", []) or []:
        if isinstance(item, dict) and item.get("id") == checkpoint_id:
            return item
    raise KeyError(f"unknown checkpoint_id: {checkpoint_id}")


def stage_spec(registry: dict[str, Any], stage: str) -> dict[str, Any]:
    for item in registry.get("stage_acceptance", []) or []:
        if isinstance(item, dict) and item.get("stage") == stage:
            return item
    raise KeyError(f"unknown stage for stage_acceptance: {stage}")


def role_specs_by_ids(registry: dict[str, Any], role_ids: list[str]) -> list[dict[str, Any]]:
    dimensions = [item for item in registry.get("dimensions", []) or [] if isinstance(item, dict)]
    indexed = {str(item.get("role_id") or ""): item for item in dimensions}
    return [indexed[role_id] for role_id in role_ids if role_id in indexed]


def safe_dict(value: Any) -> dict[str, Any]:
    return value if isinstance(value, dict) else {}


def safe_list(value: Any) -> list[Any]:
    return value if isinstance(value, list) else []


def severity_counts(issues: list[dict[str, Any]]) -> dict[str, int]:
    counts = {"critical": 0, "high": 0, "medium": 0, "low": 0}
    for issue in issues:
        severity = str(issue.get("severity") or "").strip().lower()
        if severity in counts:
            counts[severity] += 1
    return counts


def merge_severity_counts(items: list[dict[str, int]]) -> dict[str, int]:
    merged = {"critical": 0, "high": 0, "medium": 0, "low": 0}
    for item in items:
        for key in merged:
            merged[key] += int(safe_dict(item).get(key) or 0)
    return merged


def has_blocking_issue(issues: list[dict[str, Any]]) -> bool:
    return any(str(item.get("severity") or "").strip().lower() in {"critical", "high"} for item in issues)


def clamp_score(value: float) -> float:
    return round(max(0.0, min(100.0, value)), 2)


def utc_now() -> str:
    return time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())


def relref(path: Path, project_root: Path) -> str:
    try:
        return str(path.relative_to(project_root))
    except ValueError:
        return str(path)


def default_output_path(project_root: Path, mode: str, scope_ref: str, checkpoint_id: str, stage: str) -> Path:
    safe_scope = sanitize_scope_ref(scope_ref)
    if mode == "checkpoint_inline":
        return project_root / "review" / "checkpoints" / checkpoint_id / f"{safe_scope}.review.json"
    if mode == "stage_acceptance":
        return project_root / "review" / "stages" / stage / f"{safe_scope}.review.json"
    return project_root / "review" / "releases" / f"{safe_scope}.review.json"


def fact_pack_path(output_path: Path) -> Path:
    return output_path.with_name(f"{output_path.stem}.fact-pack.json")


def repair_plan_path(output_path: Path) -> Path:
    return output_path.with_name(f"{output_path.stem}.repair.json")


def review_report_path(output_path: Path) -> Path:
    return output_path.with_name(f"{output_path.stem}.review.md")


def code_reviewer_dir(output_path: Path) -> Path:
    artifact_dir_name = str(EXECUTION_PROVIDER.get("artifact_dir_name") or ".code-reviewer")
    directory = output_path.parent / artifact_dir_name / output_path.stem
    directory.mkdir(parents=True, exist_ok=True)
    return directory


def substitute_scope_refs(refs: list[str], scope_ref: str) -> list[str]:
    return [item.replace("{scope_ref}", scope_ref) for item in refs]


def build_requirement_spec(mode: str, checkpoint_id: str, stage: str) -> dict[str, list[str]]:
    if mode == "checkpoint_inline":
        return deepcopy(CHECKPOINT_REQUIREMENTS.get(checkpoint_id, {}))
    if mode == "stage_acceptance":
        return deepcopy(STAGE_REQUIREMENTS.get(stage, {}))
    return deepcopy(CHECKPOINT_REQUIREMENTS["package-release-ready"])


def materialize_requirements(
    project_root: Path,
    requirement_spec: dict[str, list[str]],
    scope_ref: str,
) -> dict[str, list[dict[str, Any]]]:
    out: dict[str, list[dict[str, Any]]] = {}
    for key in ("validation_refs", "source_truth_refs", "runtime_artifact_refs", "handoff_candidate_refs"):
        entries = []
        for rel in substitute_scope_refs(requirement_spec.get(key, []), scope_ref):
            path = project_root / rel
            entries.append(
                {
                    "ref": rel,
                    "exists": path.exists(),
                    "is_file": path.is_file(),
                    "is_dir": path.is_dir(),
                }
            )
        out[key] = entries
    return out


def required_missing_refs(pack: dict[str, Any]) -> list[str]:
    missing: list[str] = []
    for key in ("validation_refs", "source_truth_refs", "runtime_artifact_refs"):
        for item in pack.get(key, []) or []:
            packet = safe_dict(item)
            if packet and not packet.get("exists"):
                missing.append(str(packet.get("ref") or ""))
    return [item for item in missing if item]


def build_fact_pack(
    *,
    project_root: Path,
    mode: str,
    checkpoint_id: str,
    stage: str,
    scope_ref: str,
    output_path: Path,
) -> dict[str, Any]:
    requirement_spec = build_requirement_spec(mode, checkpoint_id, stage)
    refs = materialize_requirements(project_root, requirement_spec, scope_ref)
    team_yaml = project_root / "team.yaml"
    state_json = project_root / "STATE.json"
    governance_state = project_root / "governance-state.yaml"
    pack = {
        "project_root": str(project_root),
        "review_mode": mode,
        "checkpoint_id": checkpoint_id,
        "stage": stage,
        "scope_ref": scope_ref,
        "team_yaml_ref": "team.yaml" if team_yaml.exists() else "",
        "state_ref": "STATE.json" if state_json.exists() else "",
        "governance_state_ref": "governance-state.yaml" if governance_state.exists() else "",
        "validation_refs": refs["validation_refs"],
        "source_truth_refs": refs["source_truth_refs"],
        "runtime_artifact_refs": refs["runtime_artifact_refs"],
        "handoff_candidate_refs": refs["handoff_candidate_refs"],
        "required_slice_status": {
            "validation_refs": all(item.get("exists") for item in refs["validation_refs"]),
            "source_truth_refs": all(item.get("exists") for item in refs["source_truth_refs"]),
            "runtime_artifact_refs": all(item.get("exists") for item in refs["runtime_artifact_refs"]),
        },
        "missing_required_refs": required_missing_refs(refs),
        "aggregate_review_ref": relref(output_path, project_root),
        "generated_at": utc_now(),
    }
    pack["evidence_refs"] = [
        packet["ref"]
        for key in ("validation_refs", "source_truth_refs", "runtime_artifact_refs", "handoff_candidate_refs")
        for packet in pack.get(key, [])
        if safe_dict(packet).get("exists")
    ]
    return pack


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def load_optional_json(path: Path) -> dict[str, Any]:
    if not path.is_file():
        return {}
    try:
        return load_json(path)
    except Exception:
        return {}


def _run_json_tool(
    *,
    script_path: Path,
    target_path: Path,
    output_path: Path,
    log_path: Path,
) -> dict[str, Any]:
    payload: dict[str, Any] = {
        "script": str(script_path),
        "target": str(target_path),
        "output_ref": str(output_path),
        "log_ref": str(log_path),
        "mode": "subprocess_waited",
    }
    if not script_path.is_file():
        payload["status"] = "missing-script"
        return payload

    with log_path.open("w", encoding="utf-8") as log_file:
        try:
            completed = subprocess.run(
                [
                    sys.executable,
                    str(script_path),
                    str(target_path),
                    "--json",
                    "--output",
                    str(output_path),
                ],
                stdout=log_file,
                stderr=subprocess.STDOUT,
                timeout=CODE_REVIEWER_TIMEOUT_SECONDS,
                check=False,
            )
        except subprocess.TimeoutExpired:
            payload["status"] = "timeout"
            return payload

    payload["status"] = "completed" if completed.returncode == 0 else "failed"
    payload["returncode"] = completed.returncode
    payload["output_exists"] = output_path.is_file()
    return payload


def run_code_reviewer(
    *,
    fact_pack_file: Path,
    output_path: Path,
    project_root: Path,
) -> dict[str, Any]:
    output_dir = code_reviewer_dir(output_path)
    checker_json = output_dir / "code_quality.json"
    checker_log = output_dir / "code_quality.log"
    report_json = output_dir / "review_report.json"
    report_log = output_dir / "review_report.log"

    checker_job = _run_json_tool(
        script_path=CODE_REVIEWER_CHECKER,
        target_path=fact_pack_file,
        output_path=checker_json,
        log_path=checker_log,
    )
    reporter_job = _run_json_tool(
        script_path=CODE_REVIEWER_REPORTER,
        target_path=fact_pack_file,
        output_path=report_json,
        log_path=report_log,
    )

    checker_payload = load_optional_json(checker_json)
    reporter_payload = load_optional_json(report_json)
    findings: list[dict[str, Any]] = []
    for packet in (checker_payload, reporter_payload):
        for item in packet.get("findings", []) or []:
            if isinstance(item, dict):
                findings.append(item)

    provider_status = "completed"
    if any(job.get("status") in {"failed", "timeout", "missing-script"} for job in (checker_job, reporter_job)):
        provider_status = "degraded"

    return {
        "provider": CODE_REVIEWER_PROVIDER_NAME,
        "status": provider_status,
        "provider_skill_ref": str(EXECUTION_PROVIDER.get("skill_relative_to_codex_home") or ""),
        "target_ref": relref(fact_pack_file, project_root),
        "artifact_dir_ref": relref(output_dir, project_root),
        "jobs": [checker_job, reporter_job],
        "checker_result": checker_payload,
        "report_result": reporter_payload,
        "findings": findings,
        "executed_at": utc_now(),
    }


def issue_packet(
    *,
    role_id: str,
    issue_type: str,
    severity: str,
    checkpoint_id: str,
    stage: str,
    scope_ref: str,
    location: str,
    description: str,
    suggestion: str,
    rework_target: str,
    source_layer_owner: str,
    index: int,
    can_override: bool = False,
) -> dict[str, Any]:
    return {
        "id": f"{role_id}-{index:02d}",
        "type": issue_type,
        "severity": severity,
        "stage": stage,
        "checkpoint_id": checkpoint_id,
        "scope_ref": scope_ref,
        "location": location,
        "description": description,
        "suggestion": suggestion,
        "can_override": can_override,
        "rework_target": rework_target,
        "source_layer_owner": source_layer_owner,
    }


def _collect_fact_pack_refs(
    fact_pack: dict[str, Any],
    bucket: str,
    prefixes: list[str],
) -> list[str]:
    refs: list[str] = []
    for item in fact_pack.get(bucket, []) or []:
        ref = str(safe_dict(item).get("ref") or "")
        if not ref:
            continue
        if any(ref.startswith(prefix) for prefix in prefixes):
            refs.append(ref)
    return refs


def expected_dimension_refs(role_id: str, fact_pack: dict[str, Any]) -> dict[str, list[str]]:
    spec = deepcopy(DIMENSION_EXPECTATIONS.get(role_id, {}))
    refs: dict[str, list[str]] = {
        "validation_refs": [],
        "source_truth_refs": [],
        "runtime_artifact_refs": [],
    }
    if spec.get("use_fact_pack_validation_refs"):
        refs["validation_refs"] = [
            str(safe_dict(item).get("ref") or "")
            for item in fact_pack.get("validation_refs", []) or []
            if str(safe_dict(item).get("ref") or "")
        ]
    else:
        refs["validation_refs"] = _collect_fact_pack_refs(
            fact_pack,
            "validation_refs",
            list(spec.get("validation_prefixes", []) or []),
        )

    refs["source_truth_refs"] = _collect_fact_pack_refs(
        fact_pack,
        "source_truth_refs",
        list(spec.get("source_prefixes", []) or []),
    )
    refs["runtime_artifact_refs"] = _collect_fact_pack_refs(
        fact_pack,
        "runtime_artifact_refs",
        list(spec.get("runtime_prefixes", []) or []),
    )
    refs["runtime_artifact_refs"].extend(list(spec.get("runtime_refs", []) or []))
    return refs


def pack_ref_lookup(fact_pack: dict[str, Any]) -> dict[str, dict[str, Any]]:
    lookup: dict[str, dict[str, Any]] = {}
    for key in ("validation_refs", "source_truth_refs", "runtime_artifact_refs", "handoff_candidate_refs"):
        for item in fact_pack.get(key, []) or []:
            packet = safe_dict(item)
            ref = str(packet.get("ref") or "")
            if ref:
                lookup[ref] = packet
    for key in ("team_yaml_ref", "state_ref", "governance_state_ref"):
        ref = str(fact_pack.get(key) or "")
        if not ref:
            continue
        lookup[ref] = {
            "ref": ref,
            "exists": True,
            "is_file": True,
            "is_dir": False,
        }
    return lookup


def external_findings_to_issues(
    *,
    role_id: str,
    dimension: str,
    findings: list[dict[str, Any]],
    checkpoint_id: str,
    stage: str,
    scope_ref: str,
    default_rework_target: str,
) -> list[dict[str, Any]]:
    issues: list[dict[str, Any]] = []
    for index, item in enumerate(findings, start=1):
        severity = str(item.get("severity") or item.get("priority") or "medium").strip().lower()
        if severity not in SEVERITY_ORDER:
            severity = "medium"
        issues.append(
            issue_packet(
                role_id=role_id,
                issue_type="external_review",
                severity=severity,
                checkpoint_id=checkpoint_id,
                stage=stage,
                scope_ref=scope_ref,
                location=str(item.get("location") or item.get("file") or dimension),
                description=str(item.get("description") or item.get("title") or f"{CODE_REVIEWER_PROVIDER_NAME} 返回了需要人工确认的 findings"),
                suggestion=str(item.get("suggestion") or item.get("recommendation") or "回到最早受影响的返工入口修复后重跑 review"),
                rework_target=default_rework_target,
                source_layer_owner=stage if stage and stage != "package" else "root-aigc",
                index=index,
                can_override=severity == "low",
            )
        )
    return issues


def filter_external_findings(role_id: str, findings: list[dict[str, Any]]) -> list[dict[str, Any]]:
    matched: list[dict[str, Any]] = []
    for item in findings:
        packet = safe_dict(item)
        finding_role = str(packet.get("role_id") or packet.get("dimension_role_id") or "").strip()
        finding_dimension = str(packet.get("dimension") or "").strip()
        if finding_role and finding_role == role_id:
            matched.append(packet)
            continue
        if finding_dimension and finding_dimension == role_id:
            matched.append(packet)
            continue
        if not finding_role and not finding_dimension and role_id == "governance-closure-validator":
            matched.append(packet)
    return matched


def run_dimension_review(
    *,
    spec: dict[str, Any],
    fact_pack: dict[str, Any],
    external_review: dict[str, Any],
    output_path: Path,
    project_root: Path,
    report_template: str,
) -> dict[str, Any]:
    role_id = str(spec.get("role_id") or "")
    dimension = str(spec.get("dimension") or role_id)
    checkpoint_id = str(fact_pack.get("checkpoint_id") or "")
    stage = str(fact_pack.get("stage") or "")
    scope_ref = str(fact_pack.get("scope_ref") or "")
    lookup = pack_ref_lookup(fact_pack)
    expected = expected_dimension_refs(role_id, fact_pack)
    issues: list[dict[str, Any]] = []

    for bucket, refs in expected.items():
        for ref in refs:
            packet = safe_dict(lookup.get(ref))
            if packet.get("exists"):
                continue
            rework_targets = safe_list(spec.get("default_rework_targets"))
            rework_target = str(rework_targets[0] if rework_targets else stage or role_id)
            owner_candidates = safe_list(spec.get("upstream_source_owners"))
            source_owner = str(owner_candidates[0] if owner_candidates else stage or "root-aigc")
            issue_type = f"missing_{bucket[:-1]}" if bucket.endswith("s") else f"missing_{bucket}"
            severity = "high" if bucket in {"source_truth_refs", "runtime_artifact_refs"} else "medium"
            issues.append(
                issue_packet(
                    role_id=role_id,
                    issue_type=issue_type,
                    severity=severity,
                    checkpoint_id=checkpoint_id,
                    stage=stage,
                    scope_ref=scope_ref,
                    location=ref,
                    description=f"{dimension} 需要的证据缺失：`{ref}`。",
                    suggestion=f"先补齐 `{ref}` 或修复其上游 writeback，再重跑当前 review checkpoint。",
                    rework_target=rework_target,
                    source_layer_owner=source_owner,
                    index=len(issues) + 1,
                    can_override=False,
                )
            )

    findings = filter_external_findings(role_id, safe_list(external_review.get("findings")))
    default_rework_targets = safe_list(spec.get("default_rework_targets"))
    default_rework_target = str(default_rework_targets[0] if default_rework_targets else stage or role_id)
    external_issues = external_findings_to_issues(
        role_id=role_id,
        dimension=dimension,
        findings=findings,
        checkpoint_id=checkpoint_id,
        stage=stage,
        scope_ref=scope_ref,
        default_rework_target=default_rework_target,
    )
    issues.extend(external_issues)

    counts = severity_counts(issues)
    score = clamp_score(100 - counts["critical"] * 40 - counts["high"] * 22 - counts["medium"] * 10 - counts["low"] * 4)
    passed = not has_blocking_issue(issues)
    blocking_scope = "stage" if has_blocking_issue(issues) else "local"
    report_ref = output_path.parent / str(spec.get("report_filename") or f"{dimension}.md")
    source_trace = list(spec.get("upstream_source_owners") or [])

    summary = (
        f"{dimension} 当前通过，review fact pack 与 provider findings 未发现阻断项。"
        if passed and not issues
        else f"{dimension} 存在 {len(issues)} 个需要回退处理的问题。"
    )

    packet = {
        "role_id": role_id,
        "dimension": dimension,
        "review_mode": str(fact_pack.get("review_mode") or ""),
        "checkpoint_id": checkpoint_id,
        "stage": stage,
        "scope_ref": scope_ref,
        "pass": passed,
        "score": score,
        "summary": summary,
        "issues": issues,
        "severity_counts": counts,
        "critical_issues": [item for item in issues if str(item.get("severity")) == "critical"],
        "metrics": {
            "missing_required_refs": len([item for item in issues if str(item.get("type") or "").startswith("missing_")]),
            "external_findings": len(external_issues),
            "provider_status": str(external_review.get("status") or "unknown"),
        },
        "default_rework_targets": default_rework_targets,
        "source_trace": source_trace,
        "report_ref": relref(report_ref, project_root),
        "blocking_scope": blocking_scope,
    }

    recommended_action = (
        "允许继续当前 handoff。"
        if passed
        else f"优先回退到 {', '.join(default_rework_targets) if default_rework_targets else stage}。"
    )
    issues_md = "- 无结构化 issues。" if not issues else "\n".join(
        f"- `{item['id']}` [{item['severity']}] {item['location']} :: {item['description']}"
        for item in issues
    )
    metrics_md = json.dumps(packet["metrics"], ensure_ascii=False, indent=2)
    source_trace_md = json.dumps(source_trace, ensure_ascii=False, indent=2)
    rendered_report = (
        report_template
        .replace("{{dimension}}", dimension)
        .replace("{{review_mode}}", packet["review_mode"])
        .replace("{{checkpoint_id}}", checkpoint_id)
        .replace("{{stage}}", stage)
        .replace("{{scope_ref}}", scope_ref)
        .replace("{{summary}}", summary)
        .replace("{{issues}}", issues_md)
        .replace("{{metrics}}", metrics_md)
        .replace("{{source_trace}}", source_trace_md)
        .replace("{{recommended_action}}", recommended_action)
    )
    report_ref.write_text(rendered_report + ("\n" if not rendered_report.endswith("\n") else ""), encoding="utf-8")
    return {
        "dimension_packet": packet,
        "dimension_report_ref": packet["report_ref"],
    }


def aggregate_rework_targets(issues: list[dict[str, Any]], routing_decision: str) -> list[dict[str, Any]]:
    groups: dict[str, list[str]] = {}
    for issue in issues:
        key = ""
        if routing_decision == "back_to_source_contract":
            key = str(issue.get("source_layer_owner") or "").strip()
        else:
            key = str(issue.get("rework_target") or "").strip()
        if not key:
            continue
        groups.setdefault(key, []).append(str(issue.get("id") or ""))

    targets: list[dict[str, Any]] = []
    for target_ref, issue_ids in groups.items():
        if not issue_ids:
            continue
        reason = (
            "上游真源存在缺口或冲突，需先修 source contract。"
            if routing_decision == "back_to_source_contract"
            else "当前目标是最早受影响的返工入口。"
        )
        targets.append(
            {
                "target_ref": target_ref,
                "issue_ids": issue_ids,
                "reason": reason,
            }
        )
    return targets


def aggregate_handoff_targets(
    *,
    registry: dict[str, Any],
    mode: str,
    checkpoint_id: str,
    stage: str,
) -> list[str]:
    if mode == "checkpoint_inline":
        return list(checkpoint_spec(registry, checkpoint_id).get("default_handoff_on_pass", []) or [])
    if mode == "stage_acceptance":
        return list(STAGE_ACCEPTANCE_PASS_TARGETS.get(stage, []))
    return list(checkpoint_spec(registry, "package-release-ready").get("default_handoff_on_pass", []) or [])


def decide_routing(
    *,
    issues: list[dict[str, Any]],
    mode: str,
    checkpoint_id: str,
    stage: str,
    provider_status: str,
) -> tuple[str, str, list[str]]:
    upstream_owners = {
        str(issue.get("source_layer_owner") or "").strip()
        for issue in issues
        if str(issue.get("source_layer_owner") or "").strip() in SOURCE_LAYER_OWNERS
    }
    if provider_status == "degraded":
        return "FAIL-RUNTIME", "hold_for_human_review", []
    if upstream_owners:
        return "FAIL-COVENANT", "back_to_source_contract", []
    if has_blocking_issue(issues):
        if checkpoint_id in {"image-handoff-ready", "video-handoff-ready"}:
            return "FAIL-BLOCKING", "block_provider_handoff", []
        return "FAIL-BLOCKING", "back_to_stage_contract", []
    if issues:
        return "PASS-WITH-WARNINGS", "handoff_next_stage", []
    if mode == "package_release":
        return "PASS", "handoff_next_stage", ["release"]
    return "PASS", "handoff_next_stage", []


def build_repair_plan(
    *,
    packet: dict[str, Any],
    output_path: Path,
    project_root: Path,
) -> dict[str, Any]:
    review_status = str(packet.get("review_status") or "")
    routing_decision = str(packet.get("routing_decision") or "")
    rework_targets = safe_list(packet.get("rework_targets"))
    handoff_targets = safe_list(packet.get("handoff_targets"))
    if review_status == "PASS":
        status = "not_required"
        recommended_entry_stage = ""
        recommended_entry_path = ""
    elif review_status == "PASS-WITH-WARNINGS":
        status = "advisory"
        first_target = safe_dict(rework_targets[0]) if rework_targets else {}
        recommended_entry_stage = str(first_target.get("target_ref") or "")
        recommended_entry_path = recommended_entry_stage
    else:
        status = "required"
        first_target = safe_dict(rework_targets[0]) if rework_targets else {}
        recommended_entry_stage = str(first_target.get("target_ref") or "")
        recommended_entry_path = recommended_entry_stage

    payload = {
        "review_ref": relref(output_path, project_root),
        "repair_status": status,
        "review_status": review_status,
        "routing_decision": routing_decision,
        "recommended_entry_stage": recommended_entry_stage,
        "recommended_entry_path": recommended_entry_path,
        "handoff_targets": handoff_targets,
        "rework_targets": rework_targets,
        "required_repairs": [
            {
                "target_ref": safe_dict(item).get("target_ref", ""),
                "issue_ids": safe_dict(item).get("issue_ids", []),
                "reason": safe_dict(item).get("reason", ""),
            }
            for item in rework_targets
        ],
        "generated_at": utc_now(),
    }
    return payload


def sync_governance_state(
    *,
    project_root: Path,
    aggregate_packet: dict[str, Any],
    repair_plan: dict[str, Any],
) -> bool:
    governance_path = project_root / "governance-state.yaml"
    if not governance_path.is_file():
        return False
    data = load_yaml(governance_path)
    review_bridge = safe_dict(data.get("review_bridge"))
    review_bridge["latest_review_status"] = str(aggregate_packet.get("review_status") or "")
    review_bridge["latest_review_ref"] = str(aggregate_packet.get("review_ref") or "")
    review_bridge["latest_review_checkpoint"] = str(aggregate_packet.get("checkpoint_id") or "")
    data["review_bridge"] = review_bridge

    resume_contract = safe_dict(data.get("resume_contract"))
    if str(repair_plan.get("repair_status") or "") == "required":
        resume_contract["recommended_entry_stage"] = str(repair_plan.get("recommended_entry_stage") or "")
        resume_contract["recommended_entry_path"] = str(repair_plan.get("recommended_entry_path") or "")
        resume_contract["required_repairs"] = safe_list(repair_plan.get("required_repairs"))
        resume_contract["rationale"] = (
            f"latest review gate: {aggregate_packet.get('review_status')} -> "
            f"{aggregate_packet.get('routing_decision')}"
        )
    else:
        resume_contract["required_repairs"] = []
        resume_contract["rationale"] = "latest review gate passed; no repair routing required"
    data["resume_contract"] = resume_contract
    data["updated_at"] = utc_now()

    governance_path.write_text(yaml.safe_dump(data, allow_unicode=True, sort_keys=False), encoding="utf-8")
    return True


def write_review_report(
    *,
    project_root: Path,
    output_path: Path,
    packet: dict[str, Any],
    external_review: dict[str, Any],
    fact_pack_file: Path,
    repair_plan_file: Path,
) -> str:
    report_path = review_report_path(output_path)
    lines = [
        f"# AIGC Review Report / {packet.get('scope_ref')}",
        "",
        "## Gate Summary",
        "",
        f"- `review_status`: {packet.get('review_status')}",
        f"- `routing_decision`: {packet.get('routing_decision')}",
        f"- `overall_score`: {packet.get('overall_score')}",
        f"- `handoff_targets`: {json.dumps(packet.get('handoff_targets', []), ensure_ascii=False)}",
        "",
        "## Review Inputs",
        "",
        f"- `review_ref`: {packet.get('review_ref')}",
        f"- `review_fact_pack_ref`: {relref(fact_pack_file, project_root)}",
        f"- `repair_plan_ref`: {relref(repair_plan_file, project_root)}",
        "",
        "## Severity Counts",
        "",
        "```json",
        json.dumps(packet.get("severity_counts", {}), ensure_ascii=False, indent=2),
        "```",
        "",
        "## code-reviewer Dispatch",
        "",
        f"- `provider`: {external_review.get('provider') or CODE_REVIEWER_PROVIDER_NAME}",
        f"- `provider_skill_ref`: {external_review.get('provider_skill_ref') or '-'}",
        f"- `status`: {external_review.get('status') or 'unknown'}",
        f"- `artifact_dir_ref`: {external_review.get('artifact_dir_ref') or '-'}",
        "",
        "## Rework Targets",
        "",
    ]
    rework_targets = safe_list(packet.get("rework_targets"))
    if rework_targets:
        for item in rework_targets:
            lines.append(f"- {json.dumps(item, ensure_ascii=False)}")
    else:
        lines.append("- 当前无结构化返工目标。")

    lines.extend(["", "## Dimension Reports", ""])
    for ref in packet.get("dimension_report_refs", []) or []:
        lines.append(f"- `{ref}`")

    report_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return relref(report_path, project_root)


def build_packet(
    registry: dict[str, Any],
    template: dict[str, Any],
    mode: str,
    scope_ref: str,
    checkpoint_id: str,
    stage: str,
    output_path: Path,
) -> dict[str, Any]:
    packet = deepcopy(template)
    packet["review_mode"] = mode
    packet["checkpoint_id"] = checkpoint_id
    packet["stage"] = stage
    packet["scope_ref"] = scope_ref
    packet["review_ref"] = str(output_path)

    if mode == "checkpoint_inline":
        spec = checkpoint_spec(registry, checkpoint_id)
        role_ids = list(spec.get("mandatory_dimensions", []) or [])
        packet["handoff_targets"] = list(spec.get("default_handoff_on_pass", []) or [])
        packet["thought_process"]["checkpoint_selection"] = str(spec.get("trigger_node") or "")
    elif mode == "stage_acceptance":
        spec = stage_spec(registry, stage)
        role_ids = list(spec.get("mandatory_dimensions", []) or [])
        packet["handoff_targets"] = []
        packet["thought_process"]["checkpoint_selection"] = f"stage_acceptance:{stage}"
    else:
        release_spec = checkpoint_spec(registry, "package-release-ready")
        role_ids = list(release_spec.get("mandatory_dimensions", []) or [])
        packet["handoff_targets"] = list(release_spec.get("default_handoff_on_pass", []) or [])
        packet["thought_process"]["checkpoint_selection"] = "package-release-ready"

    specs = role_specs_by_ids(registry, role_ids)
    packet["selected_agents"] = [str(spec.get("role_id") or "") for spec in specs]
    packet["dimension_packets"] = []
    packet["dimension_report_refs"] = []
    packet["dimension_scores"] = {}
    packet["thought_process"]["mode_decision"] = f"mode={mode}"
    packet["thought_process"]["aggregate_reasoning"] = "aggregate packet will be populated after provider dispatch and dimension review"
    return packet


def main() -> int:
    parser = argparse.ArgumentParser(description="Run `aigc/review` aggregate audit.")
    parser.add_argument("--project-root", required=True, help="Path to `projects/aigc/<项目名>`.")
    parser.add_argument("--mode", choices=("checkpoint_inline", "stage_acceptance", "package_release"), required=True)
    parser.add_argument("--scope-ref", required=True, help="Episode/stage/package scope reference.")
    parser.add_argument("--checkpoint-id", default="", help="Checkpoint id for checkpoint mode.")
    parser.add_argument("--stage", default="", help="Stage name for stage_acceptance.")
    parser.add_argument("--output", default="", help="Optional override output path.")
    parser.add_argument("--print-checkpoints", action="store_true", help="Print known checkpoint ids and exit.")
    args = parser.parse_args()

    registry = load_yaml(REGISTRY)
    if args.print_checkpoints:
        for item in registry.get("checkpoints", []) or []:
            if isinstance(item, dict):
                print(item.get("id", ""))
        return 0

    template = load_json(AGGREGATE_TEMPLATE)
    project_root = Path(args.project_root).resolve()
    checkpoint_id = args.checkpoint_id
    stage = args.stage

    if args.mode == "checkpoint_inline" and not checkpoint_id:
        raise SystemExit("--checkpoint-id is required for checkpoint_inline")
    if args.mode == "checkpoint_inline":
        stage = str(checkpoint_spec(registry, checkpoint_id).get("stage") or "")
    if args.mode == "stage_acceptance" and not stage:
        raise SystemExit("--stage is required for stage_acceptance")
    if args.mode == "package_release":
        checkpoint_id = "package-release-ready"
        stage = "package"

    output_path = Path(args.output).resolve() if args.output else default_output_path(
        project_root, args.mode, args.scope_ref, checkpoint_id, stage
    )
    output_path.parent.mkdir(parents=True, exist_ok=True)

    packet = build_packet(
        registry=registry,
        template=template,
        mode=args.mode,
        scope_ref=args.scope_ref,
        checkpoint_id=checkpoint_id,
        stage=stage,
        output_path=output_path,
    )

    fact_pack = build_fact_pack(
        project_root=project_root,
        mode=args.mode,
        checkpoint_id=checkpoint_id,
        stage=stage,
        scope_ref=args.scope_ref,
        output_path=output_path,
    )
    fact_pack_file = fact_pack_path(output_path)
    write_json(fact_pack_file, fact_pack)

    external_review = run_code_reviewer(
        fact_pack_file=fact_pack_file,
        output_path=output_path,
        project_root=project_root,
    )
    report_template = load_text(REPORT_TEMPLATE)

    dimension_packets: list[dict[str, Any]] = []
    dimension_report_refs: list[str] = []
    dimension_scores: dict[str, float] = {}
    issues: list[dict[str, Any]] = []
    severity_list: list[dict[str, int]] = []
    weighted_score = 0.0
    total_weight = 0.0

    for spec in role_specs_by_ids(registry, list(packet.get("selected_agents") or [])):
        result = run_dimension_review(
            spec=spec,
            fact_pack=fact_pack,
            external_review=external_review,
            output_path=output_path,
            project_root=project_root,
            report_template=report_template,
        )
        dimension_packet = safe_dict(result.get("dimension_packet"))
        dimension_packets.append(dimension_packet)
        dimension_report_ref = str(result.get("dimension_report_ref") or "")
        if dimension_report_ref:
            dimension_report_refs.append(dimension_report_ref)
        dimension_scores[str(dimension_packet.get("role_id") or "")] = float(dimension_packet.get("score") or 0.0)
        issues.extend(safe_list(dimension_packet.get("issues")))
        severity_list.append(safe_dict(dimension_packet.get("severity_counts")))

        spec_weight = 0.0
        if args.mode == "stage_acceptance":
            spec_weight = float(safe_dict(spec.get("stage_acceptance")).get("weight") or 0.0)
        elif args.mode == "package_release":
            spec_weight = float(safe_dict(spec.get("package_release")).get("weight") or 0.0)
        else:
            spec_weight = 1.0
        weighted_score += float(dimension_packet.get("score") or 0.0) * spec_weight
        total_weight += spec_weight

    review_status, routing_decision, handoff_targets = decide_routing(
        issues=issues,
        mode=args.mode,
        checkpoint_id=checkpoint_id,
        stage=stage,
        provider_status=str(external_review.get("status") or "unknown"),
    )
    if review_status == "PASS" and not handoff_targets:
        handoff_targets = aggregate_handoff_targets(
            registry=registry,
            mode=args.mode,
            checkpoint_id=checkpoint_id,
            stage=stage,
        )

    packet["review_ref"] = relref(output_path, project_root)
    packet["dimension_packets"] = dimension_packets
    packet["dimension_report_refs"] = dimension_report_refs
    packet["dimension_scores"] = dimension_scores
    packet["issues"] = issues
    packet["severity_counts"] = merge_severity_counts(severity_list)
    packet["critical_issues"] = [item for item in issues if str(item.get("severity") or "") == "critical"]
    packet["overall_score"] = clamp_score(weighted_score / total_weight) if total_weight else 0.0
    packet["review_status"] = review_status
    packet["routing_decision"] = routing_decision
    packet["handoff_targets"] = handoff_targets
    packet["rework_targets"] = aggregate_rework_targets(issues, routing_decision)
    packet["review_fact_pack_ref"] = relref(fact_pack_file, project_root)
    packet["source_trace"] = [
        {
            "role_id": str(item.get("role_id") or ""),
            "upstream_source_owners": safe_list(item.get("source_trace")),
        }
        for item in dimension_packets
    ]
    packet["evidence_refs"] = list(fact_pack.get("evidence_refs") or [])
    packet["external_review"] = external_review
    packet["thought_process"]["aggregate_reasoning"] = (
        f"provider={external_review.get('status')} issues={len(issues)} routing={routing_decision}"
    )

    repair_plan = build_repair_plan(
        packet=packet,
        output_path=output_path,
        project_root=project_root,
    )
    repair_plan_file = repair_plan_path(output_path)
    write_json(repair_plan_file, repair_plan)
    packet["repair_plan_ref"] = relref(repair_plan_file, project_root)
    packet["governance_state_synced"] = sync_governance_state(
        project_root=project_root,
        aggregate_packet=packet,
        repair_plan=repair_plan,
    )
    packet["review_report_ref"] = write_review_report(
        project_root=project_root,
        output_path=output_path,
        packet=packet,
        external_review=external_review,
        fact_pack_file=fact_pack_file,
        repair_plan_file=repair_plan_file,
    )

    write_json(output_path, packet)
    print(output_path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
