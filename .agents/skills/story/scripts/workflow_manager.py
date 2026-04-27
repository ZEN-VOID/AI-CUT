#!/usr/bin/env python3
"""
Workflow state manager
- Track story2026 stage execution status
- Detect interruption points
- Provide recovery options
- Emit call traces and task logs for observability
"""

from __future__ import annotations

import json
import logging
import os
import re
import shutil
import subprocess
import sys
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, Optional

from chapter_paths import default_chapter_draft_path, drafting_root_md_path, find_chapter_file
from drafting_manuscript_guard import validate_project_chapter
from drafting_volume_quality_guard import validate_volume_log
from planning_paths import planned_chapter_numbers_for_volume
from project_locator import resolve_project_root, resolve_state_file
from runtime_compat import enable_windows_utf8_stdio, normalize_windows_path
from security_utils import atomic_write_json, create_secure_directory

try:
    import yaml
except ImportError:  # pragma: no cover
    yaml = None


logger = logging.getLogger(__name__)


if sys.platform == "win32" and __name__ == "__main__" and not os.environ.get("PYTEST_CURRENT_TEST"):
    enable_windows_utf8_stdio(skip_in_pytest=True)


TASK_STATUS_RUNNING = "running"
TASK_STATUS_COMPLETED = "completed"
TASK_STATUS_FAILED = "failed"
TASK_STATUS_CLEARED = "cleared"

STEP_STATUS_STARTED = "started"
STEP_STATUS_RUNNING = "running"
STEP_STATUS_COMPLETED = "completed"
STEP_STATUS_FAILED = "failed"

INLINE_VALIDATION_STATUS_PENDING = "pending"
INLINE_VALIDATION_STATUS_PASSED = "passed"
INLINE_VALIDATION_STATUS_FAILED = "failed"
INLINE_VALIDATION_STATUS_BLOCKED = "blocked"
INLINE_VALIDATION_STATUS_NOT_RUN = "not_run"

CANDIDATE_FINAL_STATUS_NOT_READY = "not_ready"
CANDIDATE_FINAL_STATUS_READY = "candidate_final_draft"
CANDIDATE_FINAL_STATUS_VALIDATED = "validated_final_draft"
CANDIDATE_FINAL_STATUS_BLOCKED = "blocked"


COMMAND_ALIASES: dict[str, str] = {
    "webnovel-init": "story-init",
    "story-init": "story-init",
    "story2026-cards": "story-cards",
    "story-cards": "story-cards",
    "webnovel-plan": "story-plan",
    "story-plan": "story-plan",
    "webnovel-write": "story-write",
    "story-write": "story-write",
    "webnovel-validate": "story-validate",
    "story2026-validation": "story-validate",
    "story-validate": "story-validate",
    "webnovel-review": "story-review",
    "story-review": "story-review",
    "webnovel-loopback": "story-context-return",
    "story2026-loopback": "story-context-return",
    "story-loopback": "story-context-return",
    "story-context-return": "story-context-return",
    "webnovel-query": "story-query",
    "story-query": "story-query",
    "webnovel-resume": "story-resume",
    "story-resume": "story-resume",
}


def _normalized_tokens(raw: Any) -> set[str]:
    if not isinstance(raw, list):
        return set()
    return {str(item or "").strip().rstrip("/").replace("\\", "/").lower() for item in raw if str(item or "").strip()}


def _context_return_gate_ready(validation_payload: dict[str, Any]) -> bool:
    if str(validation_payload.get("validation_status") or "").strip() != "PASS":
        return False
    if str(validation_payload.get("routing_decision") or "").strip() != "handoff_to_review_and_context_return":
        return False
    targets = _normalized_tokens(validation_payload.get("handoff_targets"))
    if not (targets & {"review", "story-review"}) or not (targets & {"context-return", "story-context-return"}):
        return False
    stage = str(validation_payload.get("accepted_manuscript_stage") or "").strip()
    refs = validation_payload.get("accepted_manuscript_refs")
    if not isinstance(refs, list) or not refs:
        return False
    if stage == "4-润色":
        return True
    if stage == "3-初稿":
        return bool(validation_payload.get("skip_polish_accepted")) or str(validation_payload.get("polish_status") or "") == "skipped"
    return False


def normalize_command_name(command: Optional[str]) -> str:
    raw = str(command or "").strip()
    if not raw:
        return ""
    return COMMAND_ALIASES.get(raw, raw)


COMMAND_SPECS: dict[str, dict[str, Any]] = {
    "story-init": {
        "stage_id": "0-init",
        "stage_label": "初始化",
        "steps": [
            ("Step 1", "锁定 team代入模式与组队子路径", "story-init-skill"),
            ("Step 2", "预建项目骨架与运行时入口", "init-project"),
            ("Step 3", "完成自动/自定义组队路由", "story-init-skill"),
            ("Step 4", "先写 team.yaml 并锁团队真源", "story-init-skill"),
            ("Step 5", "执行 planning 固定题包直答", "story-init-skill"),
            ("Step 6", "综合写回 0-初始化 三件套与 STATE.json", "story-init-skill"),
            ("Step 7", "做 sufficiency audit 与 closure", "story-init-skill"),
        ],
    },
    "story-cards": {
        "stage_id": "1-cards",
        "stage_label": "卡片层",
        "steps": [
            ("Step 1", "路由与输入校验", "story-cards"),
            ("Step 2", "生成/修复类型卡", "story-cards"),
            ("Step 3", "生成/修复风格卡", "story-cards"),
            ("Step 4", "生成/修复角色卡", "story-cards"),
            ("Step 5", "生成/修复场景卡", "story-cards"),
            ("Step 6", "生成/修复物品卡", "story-cards"),
            ("Step 7", "shared writeback 与 coverage gate", "cards-coverage-validator"),
        ],
    },
    "story-plan": {
        "stage_id": "2-planning",
        "stage_label": "规划层",
        "steps": [
            ("Step 1", "部级规划（1-部级）", "story-plan"),
            ("Step 2", "卷级规划（2-卷级）", "story-plan"),
            ("Step 3", "章级规划（3-章级）", "story-plan"),
            ("Step 4", "父层结构校验与收束", "story-plan"),
        ],
    },
    "story-write": {
        "stage_id": "3-drafting",
        "stage_label": "起草层",
        "steps": [
            ("Step 1", "单章叙事起盘", "drafting-episode-kickoff"),
            ("Step 2", "节奏优化", "drafting-pacing"),
            ("Step 3", "场景和氛围渲染", "drafting-scene-atmosphere"),
            ("Step 4", "角色形象刻画", "drafting-character-rendering"),
            ("Step 5", "对白优化", "drafting-dialogue-optimization"),
            ("Step 6", "心理活动描写", "drafting-inner-life"),
            ("Step 7", "追读力强化", "drafting-reading-power"),
            ("Step 8", "润色", "drafting-polish"),
        ],
    },
    "story-validate": {
        "stage_id": "4-review",
        "stage_label": "审计层",
        "steps": [
            ("Step 1", "加载审计规范与事实包", "context-agent"),
            ("Step 2", "后台分发 code-reviewer 审计", "validation-team"),
            ("Step 3", "聚合 findings 与修复分流", "validation-aggregator"),
            ("Step 4", "路由交接", "validation-router"),
        ],
    },
    "story-review": {
        "stage_id": "review",
        "stage_label": "审查层",
        "steps": [
            ("Step 1", "确认 review 输出", "story-review-skill"),
            ("Step 2", "加载参考与项目状态", "story-review-skill"),
            ("Step 3", "汇总评估结果", "story-review-skill"),
            ("Step 4", "生成审查报告", "story-review-skill"),
            ("Step 5", "保存审查指标", "story-review-skill"),
            ("Step 6", "写回审查记录", "story-review-skill"),
            ("Step 7", "关键问题升级/分流", "story-review-skill"),
            ("Step 8", "收尾", "story-review-skill"),
        ],
    },
    "story-context-return": {
        "stage_id": "context-return",
        "stage_label": "上下文回流层",
        "steps": [
            ("Step 1", "锁 validation/handoff gate 并提纯 delta", "context-return-manager"),
            ("Step 2", "执行 validated truth writeback", "context-return-manager"),
            ("Step 3", "刷新 projection、项目 CONTEXT 与 runtime marker", "context-return-manager"),
            ("Step 4", "收束 PASS-only context-return artifact 与 closure", "context-return-manager"),
        ],
    },
    "story-query": {
        "stage_id": "query",
        "stage_label": "查询层",
        "steps": [
            ("Step 1", "解析问题与 truth-role", "story-query"),
            ("Step 2", "定位真源", "story-query"),
            ("Step 3", "装配证据与回答", "story-query"),
        ],
    },
    "story-resume": {
        "stage_id": "resume",
        "stage_label": "恢复层",
        "steps": [
            ("Step 1", "预检与 project root 解析", "story-resume"),
            ("Step 2", "检测中断状态", "story-resume"),
            ("Step 3", "归一化恢复选项", "story-resume"),
            ("Step 4", "执行恢复/清理/交接", "story-resume"),
        ],
    },
}

CHAPTERS_PER_VOLUME = 10
VALIDATION_REF_RE = re.compile(r"第(\d+)集\.validation\.json$")
CONTEXT_RETURN_REF_RE = re.compile(r"第(\d+)集\.context-return\.json$")
REVIEW_REPORT_RE = re.compile(r"第(\d+)-(\d+)章审查报告\.md$")
VALIDATION_VOLUME_REF_RE = re.compile(r"第(\d+)卷\.validation\.json$")
CONTEXT_RETURN_VOLUME_REF_RE = re.compile(r"第(\d+)卷\.context-return\.json$")
REVIEW_REPORT_VOLUME_RE = re.compile(r"第(\d+)卷审查报告\.md$")
WRITE_LOG_VOLUME_RE = re.compile(r"第(\d+)卷\.写作日志\.yaml$")


def now_iso() -> str:
    return datetime.now().isoformat()


def _safe_int(value: Any, default: int = 0) -> int:
    try:
        return int(value)
    except Exception:
        return default


def find_project_root(override: Optional[Path] = None) -> Path:
    if override is not None:
        return resolve_project_root(str(override))
    return resolve_project_root()


_cli_project_root: Optional[Path] = None


def _get_active_project_root() -> Path:
    if _cli_project_root is not None:
        return find_project_root(_cli_project_root)
    return find_project_root()


def _project_state_path() -> Path:
    return resolve_state_file(explicit_project_root=str(_get_active_project_root()))


def _load_project_state_payload() -> dict[str, Any]:
    state_path = _project_state_path()
    if not state_path.exists():
        return {}
    with open(state_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    return data if isinstance(data, dict) else {}


def _save_project_state_payload(payload: dict[str, Any]) -> None:
    state_path = _project_state_path()
    atomic_write_json(state_path, payload, use_lock=True, backup=False)


def _workflow_runtime_bucket(payload: dict[str, Any]) -> dict[str, Any]:
    bucket = payload.setdefault("workflow_runtime", {})
    if not isinstance(bucket, dict):
        bucket = {}
        payload["workflow_runtime"] = bucket
    return bucket


def get_workflow_state_path() -> Path:
    return _project_state_path()


def get_execution_state_path() -> Path:
    return _project_state_path()


def get_task_log_path() -> Path:
    return _project_state_path()


def get_call_trace_path() -> Path:
    project_root = _get_active_project_root()
    return project_root / ".webnovel" / "observability" / "call_trace.jsonl"


def append_call_trace(event: str, payload: Optional[Dict[str, Any]] = None):
    payload = payload or {}
    trace_path = get_call_trace_path()
    create_secure_directory(str(trace_path.parent))
    row = {"timestamp": now_iso(), "event": event, "payload": payload}
    with open(trace_path, "a", encoding="utf-8") as f:
        f.write(json.dumps(row, ensure_ascii=False) + "\n")


def safe_append_call_trace(event: str, payload: Optional[Dict[str, Any]] = None):
    try:
        append_call_trace(event, payload)
    except Exception as exc:
        logger.warning("failed to append call trace for event '%s': %s", event, exc)


def append_task_log(event: str, payload: Optional[Dict[str, Any]] = None):
    payload = payload or {}
    row = {"timestamp": now_iso(), "event": event, "payload": payload}
    project_state = _load_project_state_payload()
    runtime_bucket = _workflow_runtime_bucket(project_state)
    task_log = runtime_bucket.setdefault("task_log", [])
    if not isinstance(task_log, list):
        task_log = []
        runtime_bucket["task_log"] = task_log
    task_log.append(row)
    _save_project_state_payload(project_state)


def safe_append_task_log(event: str, payload: Optional[Dict[str, Any]] = None):
    try:
        append_task_log(event, payload)
    except Exception as exc:
        logger.warning("failed to append task log for event '%s': %s", event, exc)


def get_command_spec(command: str) -> Optional[dict[str, Any]]:
    return COMMAND_SPECS.get(normalize_command_name(command))


def _normalize_command_payload(payload: Any) -> Any:
    if not isinstance(payload, dict):
        return payload
    command = normalize_command_name(payload.get("command"))
    if command:
        payload["command"] = command
        spec = get_command_spec(command)
        if spec:
            payload["stage_id"] = spec.get("stage_id")
            payload["stage_label"] = spec.get("stage_label")
    return payload


def _build_stage_progress_template() -> dict[str, Any]:
    progress: dict[str, Any] = {}
    seen: set[str] = set()
    for spec in COMMAND_SPECS.values():
        stage_id = str(spec["stage_id"])
        if stage_id in seen:
            continue
        seen.add(stage_id)
        progress[stage_id] = {
            "stage_label": spec["stage_label"],
            "status": "idle",
            "latest_run_id": None,
            "latest_command": None,
            "latest_governance_refs": None,
            "current_step": None,
            "resume_ready": False,
            "last_started_at": None,
            "last_completed_at": None,
            "last_failed_at": None,
            "last_cleared_at": None,
        }
    return progress


def build_initial_workflow_state() -> dict[str, Any]:
    return {
        "schema_version": "2.0",
        "updated_at": now_iso(),
        "current_task": None,
        "last_stable_state": None,
        "history": [],
    }


def build_initial_execution_state() -> dict[str, Any]:
    return {
        "schema_version": "1.1",
        "updated_at": now_iso(),
        "active_run_id": None,
        "run_sequence": 0,
        "latest_resume_point": None,
        "stage_progress": _build_stage_progress_template(),
        "runs": [],
        "artifacts_index": {},
        "governance_index": {},
    }


def _ensure_workflow_state_schema(state: dict[str, Any]) -> dict[str, Any]:
    base = build_initial_workflow_state()
    if not isinstance(state, dict):
        state = {}
    for key, value in base.items():
        state.setdefault(key, value if not isinstance(value, (list, dict)) else json.loads(json.dumps(value)))
    if state.get("current_task"):
        state["current_task"] = _normalize_command_payload(state["current_task"])
        state["current_task"].setdefault("failed_steps", [])
        state["current_task"].setdefault("retry_count", 0)
        state["current_task"].setdefault("run_id", None)
        state["current_task"].setdefault("governance_refs", {})
        state["current_task"] = _ensure_task_runtime_fields(state["current_task"])
    if not isinstance(state.get("history"), list):
        state["history"] = []
    else:
        state["history"] = [_normalize_command_payload(item) for item in state["history"]]
    if isinstance(state.get("last_stable_state"), dict):
        state["last_stable_state"] = _normalize_command_payload(state["last_stable_state"])
        state["last_stable_state"].setdefault("governance_refs", {})
    state["updated_at"] = now_iso()
    return state


def _ensure_execution_state_schema(state: dict[str, Any]) -> dict[str, Any]:
    base = build_initial_execution_state()
    if not isinstance(state, dict):
        state = {}
    for key, value in base.items():
        state.setdefault(key, value if not isinstance(value, (list, dict)) else json.loads(json.dumps(value)))
    stage_progress = state.get("stage_progress")
    if not isinstance(stage_progress, dict):
        stage_progress = {}
        state["stage_progress"] = stage_progress
    for stage_id, snapshot in _build_stage_progress_template().items():
        existing = stage_progress.get(stage_id)
        if not isinstance(existing, dict):
            stage_progress[stage_id] = snapshot
            continue
        for key, value in snapshot.items():
            existing.setdefault(key, value)
    if not isinstance(state.get("runs"), list):
        state["runs"] = []
    else:
        state["runs"] = [_normalize_command_payload(run) for run in state["runs"]]
        for run in state["runs"]:
            if isinstance(run, dict):
                run.setdefault("governance_refs", {})
    if not isinstance(state.get("artifacts_index"), dict):
        state["artifacts_index"] = {}
    if not isinstance(state.get("governance_index"), dict):
        state["governance_index"] = {}
    if isinstance(state.get("latest_resume_point"), dict):
        state["latest_resume_point"] = _normalize_command_payload(state["latest_resume_point"])
    for snapshot in stage_progress.values():
        if isinstance(snapshot, dict):
            if snapshot.get("latest_command"):
                snapshot["latest_command"] = normalize_command_name(snapshot.get("latest_command"))
            snapshot.setdefault("latest_governance_refs", None)
    state["updated_at"] = now_iso()
    return state


def _find_run(execution_state: dict[str, Any], run_id: Optional[str]) -> Optional[dict[str, Any]]:
    if not run_id:
        return None
    for run in execution_state.get("runs", []):
        if run.get("run_id") == run_id:
            return run
    return None


def _next_run_id(execution_state: dict[str, Any], stage_id: str) -> str:
    execution_state["run_sequence"] = int(execution_state.get("run_sequence", 0)) + 1
    return f"{stage_id}-run-{execution_state['run_sequence']:04d}"


def _step_owner_map(command: str) -> dict[str, str]:
    spec = get_command_spec(command) or {}
    return {step_id: owner for step_id, _step_name, owner in spec.get("steps", [])}


def _step_name_map(command: str) -> dict[str, str]:
    spec = get_command_spec(command) or {}
    return {step_id: step_name for step_id, step_name, _owner in spec.get("steps", [])}


def expected_step_name(command: str, step_id: str) -> str:
    return _step_name_map(command).get(step_id, step_id)


def expected_step_owner(command: str, step_id: str) -> str:
    return _step_owner_map(command).get(step_id, command or "unknown")


def _fresh_inline_validation_state() -> dict[str, Any]:
    return {
        "active_batch": None,
        "history": [],
        "blocking_gate": None,
        "latest_summary": {
            "status": INLINE_VALIDATION_STATUS_NOT_RUN,
            "step_id": None,
            "step_name": None,
            "updated_at": None,
        },
        "batch_counter": 0,
    }


def _fresh_candidate_final_state() -> dict[str, Any]:
    return {
        "status": CANDIDATE_FINAL_STATUS_NOT_READY,
        "updated_at": None,
        "source_step_id": None,
        "reason": "validation_not_started",
    }


def _ensure_task_runtime_fields(task: dict[str, Any]) -> dict[str, Any]:
    inline_validation = task.setdefault("inline_validation", _fresh_inline_validation_state())
    if not isinstance(inline_validation, dict):
        inline_validation = _fresh_inline_validation_state()
        task["inline_validation"] = inline_validation
    inline_validation.setdefault("active_batch", None)
    inline_validation.setdefault("history", [])
    inline_validation.setdefault("blocking_gate", None)
    inline_validation.setdefault(
        "latest_summary",
        {
            "status": INLINE_VALIDATION_STATUS_NOT_RUN,
            "step_id": None,
            "step_name": None,
            "updated_at": None,
        },
    )
    inline_validation.setdefault("batch_counter", 0)

    candidate_state = task.setdefault("candidate_final_state", _fresh_candidate_final_state())
    if not isinstance(candidate_state, dict):
        candidate_state = _fresh_candidate_final_state()
        task["candidate_final_state"] = candidate_state
    candidate_state.setdefault("status", CANDIDATE_FINAL_STATUS_NOT_READY)
    candidate_state.setdefault("updated_at", None)
    candidate_state.setdefault("source_step_id", None)
    candidate_state.setdefault("reason", "validation_not_started")
    return task


def _validation_registry_path() -> Path:
    return Path(__file__).resolve().parent.parent / "review" / "_shared" / "validation-dimension-registry.yaml"


def _load_validation_dimension_registry() -> dict[str, Any]:
    if yaml is None:
        raise RuntimeError("PyYAML is required to load validation-dimension-registry.yaml")
    path = _validation_registry_path()
    if not path.is_file():
        raise FileNotFoundError(f"missing validation registry: {path}")
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    return data if isinstance(data, dict) else {}


def _resolve_workflow_step_id(command: str, target: Optional[str]) -> Optional[str]:
    raw = str(target or "").strip()
    if not raw:
        return None
    normalized = re.sub(r"^\d+\s*[-.、]\s*", "", raw)
    spec = get_command_spec(command) or {}
    for step_id, step_name, _owner in spec.get("steps", []):
        if raw == step_id or raw == step_name or normalized == step_name:
            return step_id
    return None


def _inline_dimensions_for_step(command: str, step_id: str) -> list[dict[str, Any]]:
    if normalize_command_name(command) != "story-write":
        return []
    registry = _load_validation_dimension_registry()
    matches: list[dict[str, Any]] = []
    for dimension in registry.get("dimensions", []):
        drafting_inline = dimension.get("drafting_inline") or {}
        if not drafting_inline.get("enabled", False):
            continue
        for checkpoint in drafting_inline.get("checkpoints", []) or []:
            checkpoint_step_id = _resolve_workflow_step_id(command, checkpoint.get("step_id"))
            if checkpoint_step_id == step_id:
                matches.append(
                    {
                        "role_id": str(dimension.get("role_id") or ""),
                        "dimension": str(dimension.get("dimension") or ""),
                        "skill_path": str(dimension.get("skill_path") or ""),
                        "report_filename": str(dimension.get("report_filename") or ""),
                        "fail_action": str(checkpoint.get("fail_action") or ""),
                        "default_rework_targets": list(dimension.get("default_rework_targets") or []),
                        "upstream_source_owners": list(dimension.get("upstream_source_owners") or []),
                    }
                )
                break
    return matches


def _trigger_inline_validation_batch(task: dict[str, Any], completed_step: dict[str, Any]) -> Optional[dict[str, Any]]:
    task = _ensure_task_runtime_fields(task)
    command = str(task.get("command") or "")
    step_id = str(completed_step.get("id") or "")
    validators = _inline_dimensions_for_step(command, step_id)
    inline_state = task["inline_validation"]
    latest_summary = inline_state.setdefault("latest_summary", {})
    latest_summary.update(
        {
            "step_id": step_id,
            "step_name": expected_step_name(command, step_id),
            "updated_at": now_iso(),
        }
    )

    if not validators:
        latest_summary["status"] = INLINE_VALIDATION_STATUS_PASSED
        latest_summary["reason"] = "no_inline_validators"
        inline_state["active_batch"] = None
        inline_state["blocking_gate"] = None
        return None

    inline_state["batch_counter"] = int(inline_state.get("batch_counter", 0)) + 1
    batch_id = f"{task.get('run_id')}:{step_id}:inline:{inline_state['batch_counter']:03d}"
    batch = {
        "batch_id": batch_id,
        "status": INLINE_VALIDATION_STATUS_PENDING,
        "validation_context": "drafting_inline",
        "triggered_at": now_iso(),
        "step_id": step_id,
        "step_name": expected_step_name(command, step_id),
        "validators": [
            {
                "role_id": validator["role_id"],
                "dimension": validator["dimension"],
                "skill_path": validator["skill_path"],
                "report_filename": validator["report_filename"],
                "fail_action": validator["fail_action"],
                "default_rework_targets": list(validator["default_rework_targets"]),
                "upstream_source_owners": list(validator["upstream_source_owners"]),
                "status": INLINE_VALIDATION_STATUS_PENDING,
                "result": None,
                "recorded_at": None,
            }
            for validator in validators
        ],
    }
    inline_state["active_batch"] = batch
    inline_state["blocking_gate"] = {
        "status": INLINE_VALIDATION_STATUS_PENDING,
        "batch_id": batch_id,
        "step_id": step_id,
        "step_name": expected_step_name(command, step_id),
        "reason": "inline_validation_pending",
        "allowed_rework_step_id": None,
        "allowed_rework_step_name": None,
        "source_layer_owners": [],
        "issue_ids": [],
        "updated_at": now_iso(),
    }
    latest_summary["status"] = INLINE_VALIDATION_STATUS_PENDING
    latest_summary["reason"] = "inline_validation_triggered"
    return batch


def _append_inline_validation_history(task: dict[str, Any], batch: dict[str, Any]) -> None:
    task = _ensure_task_runtime_fields(task)
    history = task["inline_validation"].setdefault("history", [])
    history.append(json.loads(json.dumps(batch)))
    if len(history) > 50:
        del history[:-50]


def _step_sequence_index(command: str, step_id: Optional[str]) -> int:
    sequence = get_pending_steps(command)
    if not step_id or step_id not in sequence:
        return -1
    return sequence.index(step_id)


def _aggregate_inline_validation_batch(task: dict[str, Any], batch: dict[str, Any]) -> dict[str, Any]:
    command = str(task.get("command") or "")
    validators = batch.get("validators", [])
    results = [validator.get("result") for validator in validators if isinstance(validator.get("result"), dict)]
    issues: list[dict[str, Any]] = []
    source_layer_owners: set[str] = set()
    target_candidates: list[str] = []
    for result in results:
        for issue in result.get("issues", []) or []:
            if not isinstance(issue, dict):
                continue
            issues.append(issue)
            owner = str(issue.get("source_layer_owner") or "").strip()
            if owner:
                source_layer_owners.add(owner)
            target = _resolve_workflow_step_id(command, issue.get("rework_target_step"))
            if target:
                target_candidates.append(target)

    non_drafting_owners = sorted(owner for owner in source_layer_owners if owner and owner != "3-初稿")
    if non_drafting_owners:
        return {
            "status": INLINE_VALIDATION_STATUS_FAILED,
            "reason": "source_fix_required",
            "allowed_rework_step_id": None,
            "allowed_rework_step_name": None,
            "source_layer_owners": non_drafting_owners,
            "issue_ids": [str(issue.get("id") or "") for issue in issues if issue.get("id")],
            "updated_at": now_iso(),
        }

    if target_candidates:
        earliest = min(target_candidates, key=lambda item: _step_sequence_index(command, item))
    else:
        earliest = batch.get("step_id")

    return {
        "status": INLINE_VALIDATION_STATUS_FAILED,
        "reason": "inline_validation_failed",
        "allowed_rework_step_id": earliest,
        "allowed_rework_step_name": expected_step_name(command, str(earliest or "")),
        "source_layer_owners": [],
        "issue_ids": [str(issue.get("id") or "") for issue in issues if issue.get("id")],
        "updated_at": now_iso(),
    }


def _record_inline_validation_result(task: dict[str, Any], step_id: str, role_id: str, result: dict[str, Any]) -> dict[str, Any]:
    task = _ensure_task_runtime_fields(task)
    inline_state = task["inline_validation"]
    batch = inline_state.get("active_batch")
    if not isinstance(batch, dict):
        raise RuntimeError("no_active_inline_validation_batch")
    if str(batch.get("step_id") or "") != step_id:
        raise RuntimeError("step_id_mismatch_for_inline_validation")

    target: Optional[dict[str, Any]] = None
    for validator in batch.get("validators", []):
        if str(validator.get("role_id") or "") == role_id:
            target = validator
            break
    if target is None:
        raise RuntimeError("unknown_inline_validator")

    target["result"] = result
    target["status"] = INLINE_VALIDATION_STATUS_PASSED if bool(result.get("pass")) else INLINE_VALIDATION_STATUS_FAILED
    target["recorded_at"] = now_iso()

    latest_summary = inline_state.setdefault("latest_summary", {})
    latest_summary.update(
        {
            "step_id": step_id,
            "step_name": batch.get("step_name"),
            "updated_at": now_iso(),
            "last_role_id": role_id,
        }
    )

    if any(str(validator.get("status")) == INLINE_VALIDATION_STATUS_PENDING for validator in batch.get("validators", [])):
        batch["status"] = INLINE_VALIDATION_STATUS_PENDING
        latest_summary["status"] = INLINE_VALIDATION_STATUS_PENDING
        return {
            "batch_status": INLINE_VALIDATION_STATUS_PENDING,
            "remaining": [
                validator.get("role_id")
                for validator in batch.get("validators", [])
                if str(validator.get("status")) == INLINE_VALIDATION_STATUS_PENDING
            ],
        }

    batch["completed_at"] = now_iso()
    all_pass = all(bool((validator.get("result") or {}).get("pass")) for validator in batch.get("validators", []))
    if all_pass:
        batch["status"] = INLINE_VALIDATION_STATUS_PASSED
        inline_state["active_batch"] = None
        inline_state["blocking_gate"] = None
        latest_summary["status"] = INLINE_VALIDATION_STATUS_PASSED
        latest_summary["reason"] = "all_inline_validators_passed"
        _append_inline_validation_history(task, batch)
        if normalize_command_name(task.get("command")) == "story-write" and step_id == "Step 8":
            task["candidate_final_state"] = {
                "status": CANDIDATE_FINAL_STATUS_READY,
                "updated_at": now_iso(),
                "source_step_id": step_id,
                "reason": "step8_inline_validation_passed",
            }
        return {"batch_status": INLINE_VALIDATION_STATUS_PASSED, "remaining": []}

    batch["status"] = INLINE_VALIDATION_STATUS_FAILED
    gate = _aggregate_inline_validation_batch(task, batch)
    gate["batch_id"] = batch.get("batch_id")
    gate["step_id"] = step_id
    gate["step_name"] = batch.get("step_name")
    inline_state["active_batch"] = None
    inline_state["blocking_gate"] = gate
    latest_summary["status"] = INLINE_VALIDATION_STATUS_FAILED
    latest_summary["reason"] = gate.get("reason")
    _append_inline_validation_history(task, batch)
    task["candidate_final_state"] = {
        "status": CANDIDATE_FINAL_STATUS_BLOCKED,
        "updated_at": now_iso(),
        "source_step_id": step_id,
        "reason": str(gate.get("reason") or "inline_validation_failed"),
    }
    return {"batch_status": INLINE_VALIDATION_STATUS_FAILED, "gate": gate}


def _auto_run_inline_validation_batch(task: dict[str, Any]) -> dict[str, Any]:
    task = _ensure_task_runtime_fields(task)
    inline_state = task.get("inline_validation") or {}
    batch = inline_state.get("active_batch")
    if not isinstance(batch, dict):
        return {"status": "noop", "reason": "no_active_batch"}

    chapter_num = _safe_int((task.get("args") or {}).get("chapter_num"), 0)
    if chapter_num <= 0:
        return {"status": "deferred", "reason": "missing_chapter_num"}

    project_root = _get_active_project_root()
    manuscript_path = find_chapter_file(project_root, chapter_num) or drafting_root_md_path(project_root, chapter_num)
    if not manuscript_path.is_file():
        inline_state.setdefault("latest_summary", {})["reason"] = "auto_runner_deferred_missing_manuscript"
        return {
            "status": "deferred",
            "reason": "missing_manuscript",
            "chapter": chapter_num,
            "manuscript_path": str(manuscript_path),
        }

    try:
        from review_runner import run_batch
    except Exception as exc:  # pragma: no cover
        inline_state.setdefault("latest_summary", {})["reason"] = "auto_runner_import_failed"
        return {"status": "deferred", "reason": f"import_error:{exc.__class__.__name__}"}

    role_ids = [str(item.get("role_id") or "") for item in batch.get("validators", []) if str(item.get("role_id") or "").strip()]
    if not role_ids:
        return {"status": "noop", "reason": "empty_batch"}

    try:
        payload = run_batch(
            project_root=project_root,
            chapter_num=chapter_num,
            role_ids=role_ids,
            validation_context=str(batch.get("validation_context") or "drafting_inline"),
            current_step_id=str(batch.get("step_id") or ""),
        )
    except Exception as exc:
        inline_state.setdefault("latest_summary", {})["reason"] = "auto_runner_runtime_failed"
        return {"status": "deferred", "reason": f"runtime_error:{exc.__class__.__name__}"}

    results = payload.get("results", []) if isinstance(payload, dict) else []
    applied = []
    for item in results:
        if not isinstance(item, dict):
            continue
        role_id = str(item.get("role_id") or "")
        result = item.get("result")
        if not role_id or not isinstance(result, dict):
            continue
        summary = _record_inline_validation_result(task, str(batch.get("step_id") or ""), role_id, result)
        applied.append({"role_id": role_id, "batch_status": summary.get("batch_status")})

    inline_state.setdefault("latest_summary", {})["reason"] = "auto_runner_recorded"
    return {"status": "recorded", "results": applied}


def _load_json_arg(raw: str) -> Any:
    text = str(raw or "").strip()
    if not text:
        raise ValueError("missing json arg")
    if text.startswith("@"):
        target = text[1:].strip()
        if not target:
            raise ValueError("invalid json arg path")
        return json.loads(Path(target).read_text(encoding="utf-8"))
    return json.loads(text)


def optional_steps_for_command(command: str, task_args: Optional[Dict[str, Any]] = None) -> set[str]:
    return set()


def get_pending_steps(command: str) -> list[str]:
    spec = get_command_spec(command)
    if not spec:
        return []
    return [step_id for step_id, _step_name, _owner in spec["steps"]]


def step_allowed_before(
    command: str,
    step_id: str,
    completed_steps: list[Dict[str, Any]],
    task_args: Optional[Dict[str, Any]] = None,
) -> bool:
    sequence = get_pending_steps(command)
    if step_id not in sequence:
        return False
    expected_index = sequence.index(step_id)
    completed_ids = [str(item.get("id")) for item in completed_steps]
    required_before = sequence[:expected_index]
    optional_before = optional_steps_for_command(command, task_args)
    return all(prev in completed_ids or prev in optional_before for prev in required_before)


def _new_task(command: str, args: Dict[str, Any], run_id: str) -> Dict[str, Any]:
    started_at = now_iso()
    command = normalize_command_name(command)
    spec = get_command_spec(command) or {}
    task = {
        "run_id": run_id,
        "command": command,
        "stage_id": spec.get("stage_id"),
        "stage_label": spec.get("stage_label"),
        "args": args,
        "started_at": started_at,
        "last_heartbeat": started_at,
        "status": TASK_STATUS_RUNNING,
        "current_step": None,
        "completed_steps": [],
        "failed_steps": [],
        "pending_steps": get_pending_steps(command),
        "retry_count": 0,
        "artifacts": {
            "chapter_file": {},
            "git_status": {},
            "state_json_modified": False,
            "entities_appeared": False,
            "review_completed": False,
        },
        "governance_refs": {},
    }
    return _ensure_task_runtime_fields(task)


def _new_run_record(task: Dict[str, Any]) -> Dict[str, Any]:
    task = _ensure_task_runtime_fields(task)
    return {
        "run_id": task["run_id"],
        "command": task["command"],
        "stage_id": task.get("stage_id"),
        "stage_label": task.get("stage_label"),
        "args": task["args"],
        "status": task["status"],
        "started_at": task["started_at"],
        "last_heartbeat": task["last_heartbeat"],
        "current_step": None,
        "completed_steps": [],
        "failed_steps": [],
        "retry_count": task.get("retry_count", 0),
        "artifacts": dict(task.get("artifacts", {})),
        "governance_refs": dict(task.get("governance_refs", {})),
        "inline_validation": json.loads(json.dumps(task.get("inline_validation", {}))),
        "candidate_final_state": dict(task.get("candidate_final_state", {})),
    }


def _trim_runs(execution_state: dict[str, Any], max_runs: int = 200):
    runs = execution_state.get("runs", [])
    if len(runs) > max_runs:
        execution_state["runs"] = runs[-max_runs:]


def _stage_snapshot(execution_state: dict[str, Any], stage_id: Optional[str]) -> Optional[dict[str, Any]]:
    if not stage_id:
        return None
    return execution_state.setdefault("stage_progress", {}).setdefault(
        stage_id,
        {
            "stage_label": stage_id,
            "status": "idle",
            "latest_run_id": None,
            "latest_command": None,
            "current_step": None,
            "resume_ready": False,
            "last_started_at": None,
            "last_completed_at": None,
            "last_failed_at": None,
            "last_cleared_at": None,
        },
    )


def _update_artifacts_index(execution_state: dict[str, Any], run_id: Optional[str], scope: str, artifacts: Optional[dict[str, Any]]):
    if not run_id or not artifacts:
        return
    bucket = execution_state.setdefault("artifacts_index", {}).setdefault(run_id, {})
    bucket[scope] = artifacts


def _update_latest_resume_point(execution_state: dict[str, Any], task: Optional[dict[str, Any]], reason: str):
    if not task:
        return
    execution_state["latest_resume_point"] = {
        "run_id": task.get("run_id"),
        "command": task.get("command"),
        "stage_id": task.get("stage_id"),
        "current_step": (task.get("current_step") or {}).get("id"),
        "status": task.get("status"),
        "reason": reason,
        "updated_at": now_iso(),
    }


def _sync_run_from_task(execution_state: dict[str, Any], task: dict[str, Any]):
    task = _ensure_task_runtime_fields(task)
    run = _find_run(execution_state, task.get("run_id"))
    if not run:
        run = _new_run_record(task)
        execution_state.setdefault("runs", []).append(run)
    run["status"] = task.get("status")
    run["last_heartbeat"] = task.get("last_heartbeat")
    run["current_step"] = task.get("current_step")
    run["completed_steps"] = list(task.get("completed_steps", []))
    run["failed_steps"] = list(task.get("failed_steps", []))
    run["retry_count"] = int(task.get("retry_count", 0))
    run["artifacts"] = dict(task.get("artifacts", {}))
    run["governance_refs"] = dict(task.get("governance_refs", {}))
    run["inline_validation"] = json.loads(json.dumps(task.get("inline_validation", {})))
    run["candidate_final_state"] = dict(task.get("candidate_final_state", {}))
    if task.get("completed_at"):
        run["completed_at"] = task.get("completed_at")
    if task.get("failed_at"):
        run["failed_at"] = task.get("failed_at")
    if task.get("failure_reason"):
        run["failure_reason"] = task.get("failure_reason")


def _sync_stage_progress(execution_state: dict[str, Any], task: dict[str, Any], *, status: Optional[str] = None):
    snapshot = _stage_snapshot(execution_state, task.get("stage_id"))
    if snapshot is None:
        return
    snapshot["latest_run_id"] = task.get("run_id")
    snapshot["latest_command"] = task.get("command")
    snapshot["latest_governance_refs"] = dict(task.get("governance_refs", {}))
    snapshot["current_step"] = (task.get("current_step") or {}).get("id")
    snapshot["status"] = status or task.get("status") or snapshot.get("status")
    snapshot["last_started_at"] = task.get("started_at") or snapshot.get("last_started_at")
    if snapshot["status"] == TASK_STATUS_COMPLETED:
        snapshot["last_completed_at"] = now_iso()
        snapshot["resume_ready"] = False
        snapshot["current_step"] = None
    elif snapshot["status"] == TASK_STATUS_FAILED:
        snapshot["last_failed_at"] = now_iso()
        snapshot["resume_ready"] = True
    elif snapshot["status"] == TASK_STATUS_CLEARED:
        snapshot["last_cleared_at"] = now_iso()
        snapshot["resume_ready"] = False
        snapshot["current_step"] = None
    else:
        snapshot["resume_ready"] = bool(task.get("current_step"))


def _finalize_current_step_as_failed(task: Dict[str, Any], reason: str):
    current_step = task.get("current_step")
    if not current_step:
        return
    if current_step.get("status") in {STEP_STATUS_COMPLETED, STEP_STATUS_FAILED}:
        return
    current_step = dict(current_step)
    current_step["status"] = STEP_STATUS_FAILED
    current_step["failed_at"] = now_iso()
    current_step["failure_reason"] = reason
    task.setdefault("failed_steps", []).append(current_step)
    task["current_step"] = None


def _mark_task_failed(state: Dict[str, Any], reason: str):
    task = state.get("current_task")
    if not task:
        return
    _finalize_current_step_as_failed(task, reason=reason)
    task["status"] = TASK_STATUS_FAILED
    task["failed_at"] = now_iso()
    task["failure_reason"] = reason


def load_state():
    payload = _load_project_state_payload()
    runtime_bucket = _workflow_runtime_bucket(payload)
    state = runtime_bucket.get("workflow_state", {})
    return _ensure_workflow_state_schema(state)


def save_state(state):
    payload = _load_project_state_payload()
    runtime_bucket = _workflow_runtime_bucket(payload)
    runtime_bucket["workflow_state"] = _ensure_workflow_state_schema(state)
    _save_project_state_payload(payload)


def load_execution_state():
    payload = _load_project_state_payload()
    runtime_bucket = _workflow_runtime_bucket(payload)
    state = runtime_bucket.get("execution_state", {})
    return _ensure_execution_state_schema(state)


def save_execution_state(state):
    payload = _load_project_state_payload()
    runtime_bucket = _workflow_runtime_bucket(payload)
    normalized = _ensure_execution_state_schema(state)
    runtime_bucket["execution_state"] = normalized
    runtime_bucket["governance_index"] = normalized.get("governance_index", {})
    _save_project_state_payload(payload)


def extract_stable_state(task):
    return {
        "run_id": task.get("run_id"),
        "command": task["command"],
        "stage_id": task.get("stage_id"),
        "chapter_num": task["args"].get("chapter_num"),
        "completed_at": task.get("completed_at"),
        "artifacts": task.get("artifacts", {}),
        "governance_refs": task.get("governance_refs", {}),
    }


def _bootstrap_governance_bundle(*, run_id: str, command: str, stage_id: str, stage_label: str, args: Dict[str, Any], route_steps: list[tuple[str, str, str]]) -> tuple[dict[str, str], dict[str, Any]]:
    refs = {
        "governance_bundle_ref": f"STATE.json#workflow_runtime.governance_index.{run_id}",
        "validation_report_ref": f"STATE.json#workflow_runtime.governance_index.{run_id}.validation_report",
        "learning_record_ref": f"STATE.json#workflow_runtime.governance_index.{run_id}.learning_record",
        "artifact_manifest_ref": f"STATE.json#workflow_runtime.governance_index.{run_id}.artifact_manifest",
        "mission_brief_ref": f"STATE.json#workflow_runtime.governance_index.{run_id}.mission_brief",
    }
    bundle = {
        "task_id": run_id,
        "command": command,
        "stage_id": stage_id,
        "stage_label": stage_label,
        "args": args,
        "generated_at": now_iso(),
        "mandate": {
            "task_id": run_id,
            "task_type": "story2026-stage-run",
            "objective": f"以内联 workflow runtime 执行 {command}",
            "command": command,
            "stage_id": stage_id,
            "stage_label": stage_label,
        },
        "mission_brief": {
            "task_id": run_id,
            "summary": f"{command} run {run_id}",
            "args": args,
        },
        "route_plan": {
            "task_id": run_id,
            "steps": [
                {"step_id": step_id, "step_name": step_name, "owner": owner}
                for step_id, step_name, owner in route_steps
            ],
        },
        "preflight_verdict": {
            "task_id": run_id,
            "status": "inline-pass",
            "can_execute": True,
        },
        "artifact_manifest": {
            "task_id": run_id,
            "status": "running",
            "generated_at": now_iso(),
            "updated_at": now_iso(),
            "step_artifacts": {},
        },
        "validation_report": "",
        "learning_record": "",
        "root_cause_trace": "",
        "refs": refs,
    }
    return refs, bundle


def start_task(command, args):
    command = normalize_command_name(command)
    spec = get_command_spec(command)
    if not spec:
        print(f"⚠️ 未注册的 workflow command: {command}")
        return

    state = load_state()
    execution_state = load_execution_state()
    current = state.get("current_task")

    if current and current.get("status") == TASK_STATUS_RUNNING:
        current = _ensure_task_runtime_fields(current)
        if not current.get("governance_refs"):
            refs, bundle = _bootstrap_governance_bundle(
                run_id=str(current.get("run_id")),
                command=str(current.get("command")),
                stage_id=str(current.get("stage_id")),
                stage_label=str(current.get("stage_label")),
                args=dict(current.get("args", {})),
                route_steps=list((get_command_spec(str(current.get("command"))) or {}).get("steps", [])),
            )
            current["governance_refs"] = refs
            execution_state.setdefault("governance_index", {})[str(current.get("run_id"))] = bundle
        current["retry_count"] = int(current.get("retry_count", 0)) + 1
        current["last_heartbeat"] = now_iso()
        state["current_task"] = current
        _sync_run_from_task(execution_state, current)
        _sync_stage_progress(execution_state, current, status=TASK_STATUS_RUNNING)
        execution_state["active_run_id"] = current.get("run_id")
        _update_latest_resume_point(execution_state, current, reason="task_reentered")
        save_state(state)
        save_execution_state(execution_state)
        payload = {
            "command": current.get("command"),
            "stage_id": current.get("stage_id"),
            "run_id": current.get("run_id"),
            "retry_count": current["retry_count"],
        }
        safe_append_call_trace("task_reentered", payload)
        safe_append_task_log("task_reentered", payload)
        print(f"ℹ️ 任务已在运行，执行重入标记: {current.get('command')}")
        return

    run_id = _next_run_id(execution_state, str(spec["stage_id"]))
    task = _new_task(command, args, run_id)
    refs, bundle = _bootstrap_governance_bundle(
        run_id=run_id,
        command=command,
        stage_id=str(spec["stage_id"]),
        stage_label=str(spec["stage_label"]),
        args=args,
        route_steps=list(spec.get("steps", [])),
    )
    task["governance_refs"] = refs
    state["current_task"] = task

    execution_state["active_run_id"] = run_id
    execution_state.setdefault("runs", []).append(_new_run_record(task))
    execution_state.setdefault("governance_index", {})[run_id] = bundle
    _trim_runs(execution_state)
    _sync_stage_progress(execution_state, task, status=TASK_STATUS_RUNNING)
    _update_latest_resume_point(execution_state, task, reason="task_started")

    save_state(state)
    save_execution_state(execution_state)

    payload = {
        "command": command,
        "args": args,
        "run_id": run_id,
        "stage_id": spec["stage_id"],
        "stage_label": spec["stage_label"],
    }
    safe_append_call_trace("task_started", payload)
    safe_append_task_log("task_started", payload)
    print(f"✅ 任务已启动: {command} {json.dumps(args, ensure_ascii=False)}")


def start_step(step_id, step_name, progress_note=None):
    state = load_state()
    execution_state = load_execution_state()
    task = state.get("current_task")
    if not task:
        print("⚠️ 无活动任务，请先使用 start-task")
        return

    task = _ensure_task_runtime_fields(task)
    command = str(task.get("command") or "")
    sequence = get_pending_steps(command)
    if step_id not in sequence:
        payload = {
            "step_id": step_id,
            "command": command,
            "reason": "unknown_step_id",
            "allowed_steps": sequence,
        }
        safe_append_call_trace("step_start_rejected", payload)
        safe_append_task_log("step_start_rejected", payload)
        print(f"⚠️ Step ID 非法: {step_id}")
        return

    if not step_allowed_before(command, step_id, task.get("completed_steps", []), task.get("args", {})):
        required_before = sequence[: sequence.index(step_id)]
        missing_before = [
            prev
            for prev in required_before
            if prev not in {str(item.get('id')) for item in task.get("completed_steps", [])}
            and prev not in optional_steps_for_command(command, task.get("args", {}))
        ]
        payload = {
            "step_id": step_id,
            "command": command,
            "completed_steps": [row.get("id") for row in task.get("completed_steps", [])],
            "missing_steps": missing_before,
        }
        safe_append_call_trace("step_order_violation", payload)
        safe_append_task_log("step_order_violation", payload)
        print(f"⚠️ Step 顺序非法: {step_id}，缺少前置步骤: {', '.join(missing_before)}")
        return

    inline_state = task.get("inline_validation") or {}
    active_batch = inline_state.get("active_batch") if isinstance(inline_state, dict) else None
    if isinstance(active_batch, dict):
        payload = {
            "command": command,
            "requested_step_id": step_id,
            "blocking_step_id": active_batch.get("step_id"),
            "remaining_validators": [
                validator.get("role_id")
                for validator in active_batch.get("validators", [])
                if str(validator.get("status")) == INLINE_VALIDATION_STATUS_PENDING
            ],
        }
        safe_append_call_trace("inline_validation_blocked_start", payload)
        safe_append_task_log("inline_validation_blocked_start", payload)
        print(f"⚠️ 当前 step 后的 inline validation 尚未完成，不能开始 {step_id}")
        return

    blocking_gate = inline_state.get("blocking_gate") if isinstance(inline_state, dict) else None
    if isinstance(blocking_gate, dict):
        source_layer_owners = list(blocking_gate.get("source_layer_owners") or [])
        if source_layer_owners:
            payload = {
                "command": command,
                "requested_step_id": step_id,
                "reason": "source_fix_required",
                "source_layer_owners": source_layer_owners,
                "blocking_step_id": blocking_gate.get("step_id"),
            }
            safe_append_call_trace("inline_validation_source_fix_required", payload)
            safe_append_task_log("inline_validation_source_fix_required", payload)
            print(f"⚠️ 当前 inline validation 指向上游 source fix：{', '.join(source_layer_owners)}，不能继续 drafting")
            return

        allowed_rework_step_id = str(blocking_gate.get("allowed_rework_step_id") or "").strip()
        allowed_index = _step_sequence_index(command, allowed_rework_step_id)
        requested_index = _step_sequence_index(command, step_id)
        if allowed_index >= 0 and requested_index > allowed_index:
            payload = {
                "command": command,
                "requested_step_id": step_id,
                "allowed_rework_step_id": allowed_rework_step_id,
                "reason": "must_rewind_to_earliest_rework_step",
            }
            safe_append_call_trace("inline_validation_rework_rejected", payload)
            safe_append_task_log("inline_validation_rework_rejected", payload)
            print(f"⚠️ 当前必须先回到 {allowed_rework_step_id} 或更早 step，不能直接开始 {step_id}")
            return

        inline_state["blocking_gate"] = None
        inline_state.setdefault("latest_summary", {})["status"] = INLINE_VALIDATION_STATUS_BLOCKED
        inline_state["latest_summary"]["reason"] = "rework_started"
        payload = {
            "command": command,
            "requested_step_id": step_id,
            "cleared_blocking_gate": True,
        }
        safe_append_call_trace("inline_validation_rework_started", payload)
        safe_append_task_log("inline_validation_rework_started", payload)

    owner = expected_step_owner(command, step_id)
    canonical_step_name = expected_step_name(command, step_id)
    _finalize_current_step_as_failed(task, reason="step_replaced_before_completion")

    started_at = now_iso()
    task["current_step"] = {
        "id": step_id,
        "name": step_name,
        "canonical_name": canonical_step_name,
        "status": STEP_STATUS_RUNNING,
        "started_at": started_at,
        "running_at": started_at,
        "attempt": int(task.get("retry_count", 0)) + 1,
        "progress_note": progress_note,
    }
    task["status"] = TASK_STATUS_RUNNING
    task["last_heartbeat"] = now_iso()

    _sync_run_from_task(execution_state, task)
    _sync_stage_progress(execution_state, task, status=TASK_STATUS_RUNNING)
    _update_latest_resume_point(execution_state, task, reason="step_started")
    save_state(state)
    save_execution_state(execution_state)

    payload = {
        "step_id": step_id,
        "step_name": step_name,
        "command": task.get("command"),
        "chapter": task.get("args", {}).get("chapter_num"),
        "run_id": task.get("run_id"),
        "progress_note": progress_note,
        "expected_owner": owner,
    }
    safe_append_call_trace("step_started", payload)
    safe_append_task_log("step_started", payload)
    print(f"▶️ {step_id} 开始: {step_name}")


def heartbeat(progress_note: Optional[str] = None, progress_percent: Optional[int] = None):
    state = load_state()
    execution_state = load_execution_state()
    task = state.get("current_task")
    if not task:
        print("⚠️ 无活动任务")
        return

    task["last_heartbeat"] = now_iso()
    current_step = task.get("current_step") or {}
    if progress_note:
        current_step["progress_note"] = progress_note
    if progress_percent is not None:
        current_step["progress_percent"] = progress_percent
    if current_step:
        task["current_step"] = current_step

    _sync_run_from_task(execution_state, task)
    _sync_stage_progress(execution_state, task, status=TASK_STATUS_RUNNING)
    _update_latest_resume_point(execution_state, task, reason="heartbeat")
    save_state(state)
    save_execution_state(execution_state)

    payload = {
        "command": task.get("command"),
        "run_id": task.get("run_id"),
        "step_id": current_step.get("id"),
        "progress_note": progress_note,
        "progress_percent": progress_percent,
    }
    safe_append_call_trace("task_heartbeat", payload)
    safe_append_task_log("task_heartbeat", payload)
    print("💓 心跳已更新")


def complete_step(step_id, artifacts_json=None):
    state = load_state()
    execution_state = load_execution_state()
    task = state.get("current_task")
    if not task or not task.get("current_step"):
        print("⚠️ 无活动 Step")
        return

    current_step = task["current_step"]
    if current_step.get("id") != step_id:
        payload = {
            "requested_step_id": step_id,
            "active_step_id": current_step.get("id"),
            "command": task.get("command"),
        }
        safe_append_call_trace("step_complete_rejected", payload)
        safe_append_task_log("step_complete_rejected", payload)
        print(f"⚠️ 当前 Step 为 {current_step.get('id')}，与 {step_id} 不一致，拒绝完成")
        return

    task = _ensure_task_runtime_fields(task)
    current_step["status"] = STEP_STATUS_COMPLETED
    current_step["completed_at"] = now_iso()

    step_artifacts = None
    if artifacts_json:
        try:
            step_artifacts = json.loads(artifacts_json)
            current_step["artifacts"] = step_artifacts
            task["artifacts"].update(step_artifacts)
        except json.JSONDecodeError as exc:
            print(f"⚠️ Artifacts JSON 解析失败: {exc}")

    task["completed_steps"].append(current_step)
    task["current_step"] = None
    task["last_heartbeat"] = now_iso()
    run_id = str(task.get("run_id"))
    governance_bundle = execution_state.setdefault("governance_index", {}).setdefault(run_id, {})
    artifact_manifest = governance_bundle.setdefault("artifact_manifest", {"step_artifacts": {}, "updated_at": now_iso()})
    artifact_manifest.setdefault("step_artifacts", {})[step_id] = {
        "step_name": str(current_step.get("name") or step_id),
        "artifacts": step_artifacts or {},
        "updated_at": now_iso(),
    }
    artifact_manifest["updated_at"] = now_iso()

    inline_batch = _trigger_inline_validation_batch(task, current_step)
    auto_run_result = None
    if inline_batch:
        auto_run_result = _auto_run_inline_validation_batch(task)

    _sync_run_from_task(execution_state, task)
    _sync_stage_progress(execution_state, task, status=TASK_STATUS_RUNNING)
    _update_latest_resume_point(execution_state, task, reason="step_completed")
    _update_artifacts_index(execution_state, task.get("run_id"), f"step:{step_id}", step_artifacts)
    save_state(state)
    save_execution_state(execution_state)

    payload = {
        "step_id": step_id,
        "command": task.get("command"),
        "chapter": task.get("args", {}).get("chapter_num"),
        "run_id": task.get("run_id"),
    }
    safe_append_call_trace("step_completed", payload)
    safe_append_task_log("step_completed", payload)
    if inline_batch:
        hook_payload = {
            "command": task.get("command"),
            "run_id": task.get("run_id"),
            "step_id": step_id,
            "batch_id": inline_batch.get("batch_id"),
            "validators": [validator.get("role_id") for validator in inline_batch.get("validators", [])],
        }
        safe_append_call_trace("inline_validation_triggered", hook_payload)
        safe_append_task_log("inline_validation_triggered", hook_payload)
        if isinstance(auto_run_result, dict):
            auto_payload = {
                "command": task.get("command"),
                "run_id": task.get("run_id"),
                "step_id": step_id,
                "batch_id": inline_batch.get("batch_id"),
                **auto_run_result,
            }
            if auto_run_result.get("status") == "recorded":
                safe_append_call_trace("inline_validation_auto_run_recorded", auto_payload)
                safe_append_task_log("inline_validation_auto_run_recorded", auto_payload)
            elif auto_run_result.get("status") == "deferred":
                safe_append_call_trace("inline_validation_auto_run_deferred", auto_payload)
                safe_append_task_log("inline_validation_auto_run_deferred", auto_payload)
    print(f"✅ {step_id} 完成")


def record_inline_validation(step_id: str, role_id: str, result_json: str):
    state = load_state()
    execution_state = load_execution_state()
    task = state.get("current_task")
    if not task:
        print("⚠️ 无活动任务")
        return

    task = _ensure_task_runtime_fields(task)
    try:
        result = _load_json_arg(result_json)
    except Exception as exc:
        print(f"⚠️ inline validation result 解析失败: {exc}")
        return

    if not isinstance(result, dict):
        print("⚠️ inline validation result 必须是 JSON object")
        return

    try:
        summary = _record_inline_validation_result(task, step_id, role_id, result)
    except Exception as exc:
        print(f"⚠️ inline validation 记录失败: {exc}")
        return

    _sync_run_from_task(execution_state, task)
    _sync_stage_progress(execution_state, task, status=TASK_STATUS_RUNNING)
    _update_latest_resume_point(execution_state, task, reason="inline_validation_recorded")
    save_state(state)
    save_execution_state(execution_state)

    payload = {
        "command": task.get("command"),
        "run_id": task.get("run_id"),
        "step_id": step_id,
        "role_id": role_id,
        "batch_status": summary.get("batch_status"),
    }
    safe_append_call_trace("inline_validation_recorded", payload)
    safe_append_task_log("inline_validation_recorded", payload)
    print(f"✅ inline validation 已记录: {role_id} / {summary.get('batch_status')}")


def run_inline_validation_batch():
    state = load_state()
    execution_state = load_execution_state()
    task = state.get("current_task")
    if not task:
        print("⚠️ 无活动任务")
        return

    task = _ensure_task_runtime_fields(task)
    result = _auto_run_inline_validation_batch(task)

    _sync_run_from_task(execution_state, task)
    _sync_stage_progress(execution_state, task, status=TASK_STATUS_RUNNING)
    _update_latest_resume_point(execution_state, task, reason="inline_validation_auto_run")
    save_state(state)
    save_execution_state(execution_state)

    payload = {
        "command": task.get("command"),
        "run_id": task.get("run_id"),
        **(result if isinstance(result, dict) else {}),
    }
    safe_append_call_trace("inline_validation_auto_run_manual", payload)
    safe_append_task_log("inline_validation_auto_run_manual", payload)
    print(json.dumps(result, ensure_ascii=False, indent=2))


def complete_task(final_artifacts_json=None):
    state = load_state()
    execution_state = load_execution_state()
    task = state.get("current_task")
    if not task:
        print("⚠️ 无活动任务")
        return

    task = _ensure_task_runtime_fields(task)
    if normalize_command_name(task.get("command")) == "story-write":
        inline_state = task.get("inline_validation") or {}
        active_batch = inline_state.get("active_batch") if isinstance(inline_state, dict) else None
        blocking_gate = inline_state.get("blocking_gate") if isinstance(inline_state, dict) else None
        candidate_state = task.get("candidate_final_state") or {}
        chapter_num = _safe_int((task.get("args") or {}).get("chapter_num"), 0)
        if active_batch:
            print("⚠️ 当前存在待完成的 inline validation，不能完成 story-write")
            return
        if blocking_gate:
            print("⚠️ 当前存在未解决的 inline validation 失败门，不能完成 story-write")
            return
        if str(candidate_state.get("status") or "") not in {
            CANDIDATE_FINAL_STATUS_READY,
            CANDIDATE_FINAL_STATUS_VALIDATED,
        }:
            print("⚠️ 当前正文尚未达到 candidate_final_draft，不能完成 story-write")
            return
        if chapter_num > 0:
            guard_result = validate_project_chapter(find_project_root(), chapter_num)
            if str(guard_result.get("status") or "") != "pass":
                payload = {
                    "chapter": chapter_num,
                    "reason": str(guard_result.get("reason") or "chapter_complete_manuscript_failed"),
                    "issues": guard_result.get("issues", []),
                    "metrics": guard_result.get("metrics", {}),
                }
                safe_append_call_trace("drafting_manuscript_guard_blocked_complete", payload)
                safe_append_task_log("drafting_manuscript_guard_blocked_complete", payload)
                print("⚠️ 当前正文未通过 chapter-complete manuscript guard，不能完成 story-write")
                return

    _finalize_current_step_as_failed(task, reason="task_completed_with_active_step")
    task["status"] = TASK_STATUS_COMPLETED
    task["completed_at"] = now_iso()

    final_artifacts = None
    if final_artifacts_json:
        try:
            final_artifacts = json.loads(final_artifacts_json)
            task["artifacts"].update(final_artifacts)
        except json.JSONDecodeError as exc:
            print(f"⚠️ Final artifacts JSON 解析失败: {exc}")

    state["last_stable_state"] = extract_stable_state(task)
    state.setdefault("history", []).append(
        {
            "task_id": f"task_{len(state['history']) + 1:03d}",
            "run_id": task.get("run_id"),
            "command": task["command"],
            "stage_id": task.get("stage_id"),
            "chapter": task["args"].get("chapter_num"),
            "status": TASK_STATUS_COMPLETED,
            "completed_at": task["completed_at"],
        }
    )
    state["current_task"] = None
    run_id = str(task.get("run_id"))
    governance_bundle = execution_state.setdefault("governance_index", {}).setdefault(run_id, {})
    governance_bundle["artifact_manifest"] = {
        **governance_bundle.get("artifact_manifest", {}),
        "status": TASK_STATUS_COMPLETED,
        "updated_at": now_iso(),
        "completed_steps": [row.get("id") for row in task.get("completed_steps", [])],
        "failed_steps": [row.get("id") for row in task.get("failed_steps", [])],
        "final_artifacts": final_artifacts or {},
    }
    governance_bundle["validation_report"] = f"{task.get('command')} 已完成，run_id={run_id}"
    governance_bundle["learning_record"] = "completed"
    refs = governance_bundle.get("refs", task.get("governance_refs", {}))
    task["governance_refs"] = refs

    _sync_run_from_task(execution_state, task)
    _sync_stage_progress(execution_state, task, status=TASK_STATUS_COMPLETED)
    _update_artifacts_index(execution_state, task.get("run_id"), "final", final_artifacts)
    execution_state["active_run_id"] = None
    execution_state["latest_resume_point"] = None
    save_state(state)
    save_execution_state(execution_state)

    payload = {
        "command": task.get("command"),
        "chapter": task.get("args", {}).get("chapter_num"),
        "run_id": task.get("run_id"),
        "completed_steps": len(task.get("completed_steps", [])),
        "failed_steps": len(task.get("failed_steps", [])),
    }
    safe_append_call_trace("task_completed", payload)
    safe_append_task_log("task_completed", payload)
    print("🎀 任务完成")


def fail_current_task(reason: str = "manual_fail"):
    state = load_state()
    execution_state = load_execution_state()
    task = state.get("current_task")
    if not task:
        print("⚠️ 无活动任务")
        return

    _mark_task_failed(state, reason=reason)
    task = state.get("current_task")
    if task:
        run_id = str(task.get("run_id"))
        governance_bundle = execution_state.setdefault("governance_index", {}).setdefault(run_id, {})
        governance_bundle["artifact_manifest"] = {
            **governance_bundle.get("artifact_manifest", {}),
            "status": TASK_STATUS_FAILED,
            "updated_at": now_iso(),
            "completed_steps": [row.get("id") for row in task.get("completed_steps", [])],
            "failed_steps": [row.get("id") for row in task.get("failed_steps", [])],
            "failure_reason": reason,
        }
        governance_bundle["root_cause_trace"] = reason
        task["governance_refs"] = governance_bundle.get("refs", task.get("governance_refs", {}))
        _sync_run_from_task(execution_state, task)
        _sync_stage_progress(execution_state, task, status=TASK_STATUS_FAILED)
        _update_latest_resume_point(execution_state, task, reason=reason)
    execution_state["active_run_id"] = None
    save_state(state)
    save_execution_state(execution_state)

    payload = {
        "command": task.get("command") if task else None,
        "chapter": (task or {}).get("args", {}).get("chapter_num"),
        "run_id": (task or {}).get("run_id"),
        "reason": reason,
    }
    safe_append_call_trace("task_failed", payload)
    safe_append_task_log("task_failed", payload)
    print(f"⚠️ 任务已标记失败: {reason}")


def clear_current_task():
    state = load_state()
    execution_state = load_execution_state()
    task = state.get("current_task")
    if not task:
        print("⚠️ 无中断任务")
        return

    payload = {
        "command": task.get("command"),
        "chapter": task.get("args", {}).get("chapter_num"),
        "run_id": task.get("run_id"),
        "status": task.get("status"),
    }
    safe_append_call_trace("task_cleared", payload)
    safe_append_task_log("task_cleared", payload)

    task["status"] = TASK_STATUS_CLEARED
    _sync_run_from_task(execution_state, task)
    _sync_stage_progress(execution_state, task, status=TASK_STATUS_CLEARED)
    _update_latest_resume_point(execution_state, task, reason="task_cleared")
    execution_state["active_run_id"] = None
    state["current_task"] = None
    save_state(state)
    save_execution_state(execution_state)
    print("✅ 中断任务已清除")


def detect_interruption():
    state = load_state()
    if not state or "current_task" not in state or state["current_task"] is None:
        return _detect_artifact_fallback()

    task = state["current_task"]
    if task.get("status") == TASK_STATUS_COMPLETED:
        return _detect_artifact_fallback()

    last_heartbeat = datetime.fromisoformat(task["last_heartbeat"])
    elapsed = (datetime.now() - last_heartbeat).total_seconds()

    interrupt_info = {
        "run_id": task.get("run_id"),
        "command": task["command"],
        "stage_id": task.get("stage_id"),
        "stage_label": task.get("stage_label"),
        "args": task["args"],
        "task_status": task.get("status"),
        "current_step": task.get("current_step"),
        "completed_steps": task.get("completed_steps", []),
        "failed_steps": task.get("failed_steps", []),
        "elapsed_seconds": elapsed,
        "artifacts": task.get("artifacts", {}),
        "started_at": task.get("started_at"),
        "retry_count": int(task.get("retry_count", 0)),
    }

    payload = {
        "command": task.get("command"),
        "chapter": task.get("args", {}).get("chapter_num"),
        "run_id": task.get("run_id"),
        "task_status": task.get("status"),
        "current_step": (task.get("current_step") or {}).get("id"),
        "elapsed_seconds": elapsed,
    }
    safe_append_call_trace("interruption_detected", payload)
    safe_append_task_log("interruption_detected", payload)
    return interrupt_info


def _optional_json(path: Path) -> Optional[dict[str, Any]]:
    if not path.is_file():
        return None
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return None
    return data if isinstance(data, dict) else None


def _optional_yaml(path: Path) -> Optional[dict[str, Any]]:
    if not path.is_file() or yaml is None:
        return None
    try:
        data = yaml.safe_load(path.read_text(encoding="utf-8"))
    except Exception:
        return None
    return data if isinstance(data, dict) else None


def _latest_numbered_file(project_root: Path, relative_dir: str, pattern: re.Pattern[str]) -> tuple[Optional[int], Optional[Path]]:
    folder = project_root / relative_dir
    if not folder.is_dir():
        return None, None

    latest_number: Optional[int] = None
    latest_path: Optional[Path] = None
    for path in folder.iterdir():
        if not path.is_file():
            continue
        match = pattern.fullmatch(path.name)
        if not match:
            continue
        number = _safe_int(match.group(1), 0)
        if number <= 0:
            continue
        if latest_number is None or number > latest_number:
            latest_number = number
            latest_path = path
    return latest_number, latest_path


def _latest_episode_file(project_root: Path, relative_dir: str, pattern: re.Pattern[str]) -> tuple[Optional[int], Optional[Path]]:
    return _latest_numbered_file(project_root, relative_dir, pattern)


def _review_checkpoint_for_episode(project_payload: dict[str, Any], episode: int) -> Optional[dict[str, Any]]:
    checkpoints = project_payload.get("review_checkpoints")
    if not isinstance(checkpoints, list):
        return None

    matched: Optional[dict[str, Any]] = None
    for item in checkpoints:
        if not isinstance(item, dict):
            continue
        chapters = str(item.get("chapters") or "").strip()
        match = re.fullmatch(r"(\d+)-(\d+)", chapters)
        if not match:
            continue
        start = _safe_int(match.group(1), 0)
        end = _safe_int(match.group(2), 0)
        if start == episode and end == episode:
            matched = item
    return matched


def _review_checkpoint_for_volume(project_payload: dict[str, Any], volume: int) -> Optional[dict[str, Any]]:
    checkpoints = project_payload.get("review_checkpoints")
    if not isinstance(checkpoints, list):
        return None

    matched: Optional[dict[str, Any]] = None
    project_root_raw = str(project_payload.get("project_root") or "").strip()
    expected_start = (volume - 1) * CHAPTERS_PER_VOLUME + 1
    expected_end = volume * CHAPTERS_PER_VOLUME
    if project_root_raw:
        try:
            chapter_nums = planned_chapter_numbers_for_volume(Path(project_root_raw), volume)
            if chapter_nums:
                expected_start = min(chapter_nums)
                expected_end = max(chapter_nums)
        except Exception:
            pass

    for item in checkpoints:
        if not isinstance(item, dict):
            continue
        if _safe_int(item.get("volume"), 0) == volume:
            matched = item
            continue
        if str(item.get("volume_ref") or "").strip() == f"第{volume}卷":
            matched = item
            continue
        chapters = str(item.get("chapters") or "").strip()
        match = re.fullmatch(r"(\d+)-(\d+)", chapters)
        if not match:
            continue
        start = _safe_int(match.group(1), 0)
        end = _safe_int(match.group(2), 0)
        if start == expected_start and end == expected_end:
            matched = item
    return matched


def _review_report_for_episode(project_root: Path, episode: int) -> Optional[Path]:
    review_dir = project_root / "review"
    if not review_dir.is_dir():
        return None

    for path in review_dir.glob("第*-*章审查报告.md"):
        match = REVIEW_REPORT_RE.fullmatch(path.name)
        if not match:
            continue
        start = _safe_int(match.group(1), 0)
        end = _safe_int(match.group(2), 0)
        if start == episode and end == episode:
            return path
    return None


def _review_report_for_volume(project_root: Path, volume: int) -> Optional[Path]:
    review_dir = project_root / "review"
    if not review_dir.is_dir():
        return None
    report_path = review_dir / f"第{volume}卷审查报告.md"
    return report_path if report_path.is_file() else None


def _artifact_resume_packet(
    *,
    command: str,
    chapter_num: Optional[int],
    volume_num: Optional[int] = None,
    volume_ref: Optional[str] = None,
    chapter_refs: Optional[list[Any]] = None,
    reason: str,
    summary: str,
    artifact_refs: dict[str, Any],
    evidence_refs: list[str],
) -> dict[str, Any]:
    normalized_command = normalize_command_name(command)
    spec = get_command_spec(normalized_command) or {}
    payload = {
        "detection_mode": "artifact_fallback",
        "run_id": None,
        "command": normalized_command,
        "stage_id": spec.get("stage_id"),
        "stage_label": spec.get("stage_label"),
        "args": {},
        "task_status": "not_tracked",
        "current_step": None,
        "completed_steps": [],
        "failed_steps": [],
        "elapsed_seconds": None,
        "artifacts": artifact_refs,
        "started_at": None,
        "retry_count": 0,
        "resume_reason": reason,
        "summary": summary,
        "evidence_refs": evidence_refs,
    }
    if chapter_num is not None:
        payload["args"]["chapter_num"] = chapter_num
    if volume_num is not None:
        payload["args"]["volume_num"] = volume_num
    if volume_ref:
        payload["args"]["volume_ref"] = volume_ref
    if chapter_refs:
        payload["args"]["chapter_refs"] = chapter_refs
    return payload


def _route_source_fix_command(validation_payload: dict[str, Any]) -> str:
    owners: list[str] = []
    for item in validation_payload.get("source_trace", []) or []:
        if not isinstance(item, dict):
            continue
        for owner in item.get("upstream_source_owners", []) or []:
            owner_text = str(owner or "").strip()
            if owner_text and owner_text not in owners:
                owners.append(owner_text)
    for issue in validation_payload.get("issues", []) or []:
        if not isinstance(issue, dict):
            continue
        owner_text = str(issue.get("source_layer_owner") or "").strip()
        if owner_text and owner_text not in owners:
            owners.append(owner_text)

    if "0-初始化" in owners:
        return "story-init"
    if "1-设定" in owners:
        return "story-cards"
    return "story-plan"


def _detect_artifact_fallback() -> Optional[dict[str, Any]]:
    project_root = _get_active_project_root()
    project_payload = _load_project_state_payload()
    volume_log_num, volume_log_path = _latest_numbered_file(project_root, "3-初稿", WRITE_LOG_VOLUME_RE)
    write_log_path = volume_log_path or (project_root / "3-初稿" / "写作日志.yaml")
    write_log_payload = _optional_yaml(write_log_path) or {}
    write_log_episode: Optional[int] = None
    write_log_packet: Optional[dict[str, Any]] = None
    if write_log_payload:
        volume_num = _safe_int(write_log_payload.get("volume_num"), volume_log_num or 0)
        write_log_chapter_num = _normalize_chapter_num(
            write_log_payload.get("chapter_num") or write_log_payload.get("chapter_num")
        )
        chapter_refs = write_log_payload.get("chapter_refs")
        if not isinstance(chapter_refs, list):
            chapter_refs = []
        candidate_state = write_log_payload.get("candidate_final_state")
        resume_pointer = write_log_payload.get("current_resume_pointer")
        candidate_status = str(candidate_state.get("status") or "").strip() if isinstance(candidate_state, dict) else ""
        next_step = str(resume_pointer.get("next_step") or "").strip() if isinstance(resume_pointer, dict) else ""
        if volume_num > 0 and (
            candidate_status in {CANDIDATE_FINAL_STATUS_READY, "candidate_volume_draft"}
            or next_step == "review"
        ):
            fallback_chapters = planned_chapter_numbers_for_volume(project_root, volume_num)
            quality_guard = validate_volume_log(write_log_path, volume_num=volume_num)
            write_log_episode = max(
                [_normalize_chapter_num(item) or 0 for item in chapter_refs] or fallback_chapters or [volume_num * CHAPTERS_PER_VOLUME]
            )
            if str(quality_guard.get("status") or "") == "pass":
                write_log_packet = _artifact_resume_packet(
                    command="story-validate",
                    chapter_num=None,
                    volume_num=volume_num,
                    volume_ref=f"第{volume_num}卷",
                    chapter_refs=chapter_refs,
                    reason="candidate_volume_draft_waiting_validation",
                    summary=f"未检测到 tracked 中断，但第{volume_num}卷写作日志显示已到 candidate_volume_draft 且 volume quality gate 已通过，下一稳定入口是 review。",
                    artifact_refs={
                        "writing_log_ref": str(write_log_path.relative_to(project_root)),
                        "candidate_final_state": candidate_state if isinstance(candidate_state, dict) else {},
                        "current_resume_pointer": resume_pointer if isinstance(resume_pointer, dict) else {},
                        "quality_gate": quality_guard,
                    },
                    evidence_refs=[str(write_log_path.relative_to(project_root))],
                )
            else:
                rework_targets = quality_guard.get("priority_rework_targets", [])
                target_hint = "；优先返工 " + "、".join(rework_targets) if isinstance(rework_targets, list) and rework_targets else ""
                write_log_packet = _artifact_resume_packet(
                    command="story-write",
                    chapter_num=None,
                    volume_num=volume_num,
                    volume_ref=f"第{volume_num}卷",
                    chapter_refs=chapter_refs,
                    reason="drafting_quality_gate_blocked_validation",
                    summary=f"未检测到 tracked 中断，但第{volume_num}卷写作日志显示 volume quality gate 未通过，下一稳定入口应回到 3-初稿 返工{target_hint}。",
                    artifact_refs={
                        "writing_log_ref": str(write_log_path.relative_to(project_root)),
                        "candidate_final_state": candidate_state if isinstance(candidate_state, dict) else {},
                        "current_resume_pointer": resume_pointer if isinstance(resume_pointer, dict) else {},
                        "quality_gate": quality_guard,
                    },
                    evidence_refs=[str(write_log_path.relative_to(project_root))],
                )
        elif write_log_chapter_num and (
            candidate_status == CANDIDATE_FINAL_STATUS_READY
            or next_step == "review"
        ):
            write_log_episode = write_log_chapter_num
            write_log_packet = _artifact_resume_packet(
                command="story-validate",
                chapter_num=write_log_chapter_num,
                reason="candidate_final_draft_waiting_validation",
                summary=f"未检测到 tracked 中断，但第{write_log_chapter_num}章写作日志显示已到 candidate_final_draft，下一稳定入口是 review。",
                artifact_refs={
                    "writing_log_ref": str(write_log_path.relative_to(project_root)),
                    "candidate_final_state": candidate_state if isinstance(candidate_state, dict) else {},
                    "current_resume_pointer": resume_pointer if isinstance(resume_pointer, dict) else {},
                },
                evidence_refs=[str(write_log_path.relative_to(project_root))],
            )

    context_return_volume, context_return_path = _latest_numbered_file(project_root, "context-return", CONTEXT_RETURN_VOLUME_REF_RE)
    if context_return_volume is not None and context_return_path is not None:
        if write_log_packet is not None and volume_log_num is not None and volume_log_num > context_return_volume:
            safe_append_call_trace("artifact_resume_detected", write_log_packet)
            safe_append_task_log("artifact_resume_detected", write_log_packet)
            return write_log_packet
        context_return_payload = _optional_json(context_return_path) or {}
        chapter_refs = context_return_payload.get("meta", {}).get("chapter_refs")
        if not isinstance(chapter_refs, list):
            chapter_refs = []
        current_volume_chapters = planned_chapter_numbers_for_volume(project_root, context_return_volume)
        next_episode = max(
            [_normalize_chapter_num(item) or 0 for item in chapter_refs]
            or current_volume_chapters
            or [context_return_volume * CHAPTERS_PER_VOLUME]
        ) + 1
        next_volume = context_return_volume + 1
        packet = _artifact_resume_packet(
            command="story-write",
            chapter_num=next_episode,
            volume_num=next_volume,
            volume_ref=f"第{next_volume}卷",
            reason="context_return_completed_next_volume_ready",
            summary=f"未检测到 tracked 中断，但第{context_return_volume}卷已完成上下文回流；下一稳定入口是第{next_volume}卷 drafting。",
            artifact_refs={
                "context_return_ref": str(context_return_path.relative_to(project_root)),
                "validation_ref": str(context_return_payload.get("inputs", {}).get("validation_ref") or ""),
                "carryover_context": project_payload.get("carryover_context", {}),
                "runtime_markers": project_payload.get("runtime_markers", {}),
            },
            evidence_refs=[str(context_return_path.relative_to(project_root))],
        )
        safe_append_call_trace("artifact_resume_detected", packet)
        safe_append_task_log("artifact_resume_detected", packet)
        return packet

    context_return_episode, context_return_path = _latest_episode_file(project_root, "context-return", CONTEXT_RETURN_REF_RE)
    if context_return_episode is not None and context_return_path is not None:
        if write_log_packet is not None and write_log_episode is not None and write_log_episode > context_return_episode:
            safe_append_call_trace("artifact_resume_detected", write_log_packet)
            safe_append_task_log("artifact_resume_detected", write_log_packet)
            return write_log_packet
        context_return_payload = _optional_json(context_return_path) or {}
        next_episode = context_return_episode + 1
        packet = _artifact_resume_packet(
            command="story-write",
            chapter_num=next_episode,
            reason="context_return_completed_next_episode_ready",
            summary=f"未检测到 tracked 中断，但第{context_return_episode}章已完成上下文回流；下一稳定入口是第{next_episode}章 drafting。",
            artifact_refs={
                "context_return_ref": str(context_return_path.relative_to(project_root)),
                "validation_ref": str(context_return_payload.get("inputs", {}).get("validation_ref") or ""),
                "carryover_context": project_payload.get("carryover_context", {}),
                "runtime_markers": project_payload.get("runtime_markers", {}),
            },
            evidence_refs=[str(context_return_path.relative_to(project_root))],
        )
        safe_append_call_trace("artifact_resume_detected", packet)
        safe_append_task_log("artifact_resume_detected", packet)
        return packet

    validation_volume, validation_path = _latest_numbered_file(project_root, "review", VALIDATION_VOLUME_REF_RE)
    if validation_volume is not None and validation_path is not None:
        validation_payload = _optional_json(validation_path) or {}
        validation_status = str(validation_payload.get("validation_status") or "").strip()
        chapter_refs = validation_payload.get("chapter_refs")
        if not isinstance(chapter_refs, list):
            chapter_refs = []
        review_checkpoint = _review_checkpoint_for_volume(project_payload, validation_volume)
        review_report_path = _review_report_for_volume(project_root, validation_volume)
        evidence_refs = [str(validation_path.relative_to(project_root))]
        if review_report_path is not None:
            evidence_refs.append(str(review_report_path.relative_to(project_root)))
        if review_checkpoint:
            evidence_refs.append(f"STATE.json#review_checkpoints[volume={validation_volume}]")

        if validation_status == "PASS":
            if review_report_path is not None or review_checkpoint is not None:
                if _context_return_gate_ready(validation_payload):
                    packet = _artifact_resume_packet(
                        command="story-context-return",
                        chapter_num=None,
                        volume_num=validation_volume,
                        volume_ref=f"第{validation_volume}卷",
                        chapter_refs=chapter_refs,
                        reason="validation_pass_review_persisted_context_return_pending",
                        summary=f"未检测到 tracked 中断，但第{validation_volume}卷已 PASS、review 已落盘且 context-return handoff 合法，下一稳定入口是 context-return。",
                        artifact_refs={
                            "validation_ref": str(validation_path.relative_to(project_root)),
                            "review_report_ref": str(review_report_path.relative_to(project_root)) if review_report_path else "",
                            "review_checkpoint": review_checkpoint or {},
                        },
                        evidence_refs=evidence_refs,
                    )
                else:
                    packet = _artifact_resume_packet(
                        command="story-review",
                        chapter_num=None,
                        volume_num=validation_volume,
                        volume_ref=f"第{validation_volume}卷",
                        chapter_refs=chapter_refs,
                        reason="validation_pass_context_return_gate_not_ready",
                        summary=f"未检测到 tracked 中断，但第{validation_volume}卷 PASS 尚未满足 context-return 的 handoff + accepted manuscript gate，下一稳定入口是 review/润色路由确认。",
                        artifact_refs={
                            "validation_ref": str(validation_path.relative_to(project_root)),
                            "review_report_ref": str(review_report_path.relative_to(project_root)) if review_report_path else "",
                            "review_checkpoint": review_checkpoint or {},
                        },
                        evidence_refs=evidence_refs,
                    )
            else:
                packet = _artifact_resume_packet(
                    command="story-review",
                    chapter_num=None,
                    volume_num=validation_volume,
                    volume_ref=f"第{validation_volume}卷",
                    chapter_refs=chapter_refs,
                    reason="validation_pass_review_pending",
                    summary=f"未检测到 tracked 中断，但第{validation_volume}卷已 PASS 且尚未发现 review 持久化证据，下一稳定入口是 story-validate 后的 review 持久化。",
                    artifact_refs={
                        "validation_ref": str(validation_path.relative_to(project_root)),
                    },
                    evidence_refs=evidence_refs,
                )
            safe_append_call_trace("artifact_resume_detected", packet)
            safe_append_task_log("artifact_resume_detected", packet)
            return packet

        routing_decision = str(validation_payload.get("routing_decision") or "").strip()
        if routing_decision == "back_to_drafting_nodes":
            first_chapter = _normalize_chapter_num(chapter_refs[0]) if chapter_refs else None
            packet = _artifact_resume_packet(
                command="story-write",
                chapter_num=first_chapter,
                volume_num=validation_volume,
                volume_ref=f"第{validation_volume}卷",
                chapter_refs=chapter_refs,
                reason="validation_failed_back_to_drafting",
                summary=f"未检测到 tracked 中断，但第{validation_volume}卷终验未通过；下一稳定入口回到 drafting 修订。",
                artifact_refs={
                    "validation_ref": str(validation_path.relative_to(project_root)),
                    "routing_decision": routing_decision,
                    "rework_targets": validation_payload.get("rework_targets", []),
                },
                evidence_refs=evidence_refs,
            )
            safe_append_call_trace("artifact_resume_detected", packet)
            safe_append_task_log("artifact_resume_detected", packet)
            return packet

        if routing_decision == "back_to_source_contract":
            command = _route_source_fix_command(validation_payload)
            packet = _artifact_resume_packet(
                command=command,
                chapter_num=None,
                volume_num=validation_volume,
                volume_ref=f"第{validation_volume}卷",
                chapter_refs=chapter_refs,
                reason="validation_failed_back_to_source_contract",
                summary=f"未检测到 tracked 中断，但第{validation_volume}卷终验已指向上游 source contract 修复。",
                artifact_refs={
                    "validation_ref": str(validation_path.relative_to(project_root)),
                    "routing_decision": routing_decision,
                    "source_trace": validation_payload.get("source_trace", []),
                    "issues": validation_payload.get("issues", []),
                },
                evidence_refs=evidence_refs,
            )
            safe_append_call_trace("artifact_resume_detected", packet)
            safe_append_task_log("artifact_resume_detected", packet)
            return packet

    validation_episode, validation_path = _latest_episode_file(project_root, "review", VALIDATION_REF_RE)
    if validation_episode is not None and validation_path is not None:
        if write_log_packet is not None and write_log_episode is not None and write_log_episode > validation_episode:
            safe_append_call_trace("artifact_resume_detected", write_log_packet)
            safe_append_task_log("artifact_resume_detected", write_log_packet)
            return write_log_packet
        validation_payload = _optional_json(validation_path) or {}
        validation_status = str(validation_payload.get("validation_status") or "").strip()
        review_checkpoint = _review_checkpoint_for_episode(project_payload, validation_episode)
        review_report_path = _review_report_for_episode(project_root, validation_episode)
        evidence_refs = [str(validation_path.relative_to(project_root))]
        if review_report_path is not None:
            evidence_refs.append(str(review_report_path.relative_to(project_root)))
        if review_checkpoint:
            evidence_refs.append(f"STATE.json#review_checkpoints[{validation_episode}]")

        if validation_status == "PASS":
            if review_report_path is not None or review_checkpoint is not None:
                if _context_return_gate_ready(validation_payload):
                    packet = _artifact_resume_packet(
                        command="story-context-return",
                        chapter_num=validation_episode,
                        reason="validation_pass_review_persisted_context_return_pending",
                        summary=f"未检测到 tracked 中断，但第{validation_episode}集已 PASS、review 已落盘且 context-return handoff 合法，下一稳定入口是 context-return actualization。",
                        artifact_refs={
                            "validation_ref": str(validation_path.relative_to(project_root)),
                            "review_report_ref": str(review_report_path.relative_to(project_root)) if review_report_path else "",
                            "review_checkpoint": review_checkpoint or {},
                        },
                        evidence_refs=evidence_refs,
                    )
                else:
                    packet = _artifact_resume_packet(
                        command="story-review",
                        chapter_num=validation_episode,
                        reason="validation_pass_context_return_gate_not_ready",
                        summary=f"未检测到 tracked 中断，但第{validation_episode}集 PASS 尚未满足 context-return 的 handoff + accepted manuscript gate，下一稳定入口是 review/润色路由确认。",
                        artifact_refs={
                            "validation_ref": str(validation_path.relative_to(project_root)),
                            "review_report_ref": str(review_report_path.relative_to(project_root)) if review_report_path else "",
                            "review_checkpoint": review_checkpoint or {},
                        },
                        evidence_refs=evidence_refs,
                    )
            else:
                packet = _artifact_resume_packet(
                    command="story-review",
                    chapter_num=validation_episode,
                    reason="validation_pass_review_pending",
                    summary=f"未检测到 tracked 中断，但第{validation_episode}集已 PASS 且尚未发现 review 持久化证据，下一稳定入口是 story-validate 后的 review 持久化。",
                    artifact_refs={
                        "validation_ref": str(validation_path.relative_to(project_root)),
                    },
                    evidence_refs=evidence_refs,
                )
            safe_append_call_trace("artifact_resume_detected", packet)
            safe_append_task_log("artifact_resume_detected", packet)
            return packet

        routing_decision = str(validation_payload.get("routing_decision") or "").strip()
        if routing_decision == "back_to_drafting_nodes":
            packet = _artifact_resume_packet(
                command="story-write",
                chapter_num=validation_episode,
                reason="validation_failed_back_to_drafting",
                summary=f"未检测到 tracked 中断，但第{validation_episode}集终验未通过；下一稳定入口回到 drafting 修订。",
                artifact_refs={
                    "validation_ref": str(validation_path.relative_to(project_root)),
                    "routing_decision": routing_decision,
                    "rework_targets": validation_payload.get("rework_targets", []),
                },
                evidence_refs=evidence_refs,
            )
            safe_append_call_trace("artifact_resume_detected", packet)
            safe_append_task_log("artifact_resume_detected", packet)
            return packet

        if routing_decision == "back_to_source_contract":
            command = _route_source_fix_command(validation_payload)
            packet = _artifact_resume_packet(
                command=command,
                chapter_num=validation_episode,
                reason="validation_failed_back_to_source_contract",
                summary=f"未检测到 tracked 中断，但第{validation_episode}集终验指向 source fix；下一稳定入口是 {command}。",
                artifact_refs={
                    "validation_ref": str(validation_path.relative_to(project_root)),
                    "routing_decision": routing_decision,
                    "source_trace": validation_payload.get("source_trace", []),
                },
                evidence_refs=evidence_refs,
            )
            safe_append_call_trace("artifact_resume_detected", packet)
            safe_append_task_log("artifact_resume_detected", packet)
            return packet

    if write_log_packet is not None:
        safe_append_call_trace("artifact_resume_detected", write_log_packet)
        safe_append_task_log("artifact_resume_detected", write_log_packet)
        return write_log_packet

    return None


def _generic_recovery_options(interrupt_info: dict[str, Any]) -> list[dict[str, Any]]:
    command = str(interrupt_info.get("command") or "")
    spec = get_command_spec(command) or {}
    stage_label = spec.get("stage_label", command)
    current_step = interrupt_info.get("current_step") or {}
    step_id = current_step.get("id")
    description = f"继续 {stage_label}"
    if step_id:
        description = f"从 {step_id} 继续 {stage_label}"
    return [
        {
            "option": "A",
            "label": "从当前步骤继续",
            "risk": "low",
            "description": description,
            "actions": [
                f"保留 run_id={interrupt_info.get('run_id') or 'unknown'} 的当前现场",
                "必要时先记录 heartbeat/progress_note",
                f"继续执行 {command}",
            ],
        },
        {
            "option": "B",
            "label": "清理中断状态并整段重跑",
            "risk": "medium",
            "description": f"清理当前 {stage_label} run，再从头重跑该命令",
            "actions": [
                "执行 workflow clear",
                f"重新执行 {command}",
            ],
        },
        {
            "option": "C",
            "label": "保留现场并仅做人工诊断",
            "risk": "low",
            "description": "保留断点、日志与 artifacts，稍后再恢复",
            "actions": [
                "执行 workflow fail-task --reason \"manual_inspection\"",
                "读取 execution_state/task_log 进行诊断",
            ],
        },
    ]


def _normalize_chapter_num(value: Any) -> Optional[int]:
    try:
        chapter_num = int(value)
    except (TypeError, ValueError):
        return None
    return chapter_num if chapter_num > 0 else None


def _drafting_resume_targets(project_root: Path, chapter_num: Any) -> list[Path]:
    normalized = _normalize_chapter_num(chapter_num)
    if normalized is None:
        return []

    targets: list[Path] = []
    canonical = drafting_root_md_path(project_root, normalized)
    targets.append(canonical)

    legacy_draft = default_chapter_draft_path(project_root, normalized)
    if legacy_draft.exists() and legacy_draft not in targets:
        targets.append(legacy_draft)

    published = find_chapter_file(project_root, normalized)
    if published and published not in targets:
        targets.append(published)

    return targets


def _primary_drafting_target(project_root: Path, chapter_num: Any) -> Optional[Path]:
    targets = _drafting_resume_targets(project_root, chapter_num)
    if not targets:
        return None
    for path in targets:
        if path.exists():
            return path
    return targets[0]


def analyze_recovery_options(interrupt_info):
    if str(interrupt_info.get("detection_mode") or "") == "artifact_fallback":
        command = str(interrupt_info.get("command") or "")
        chapter_num = interrupt_info.get("args", {}).get("chapter_num", "?")
        volume_num = interrupt_info.get("args", {}).get("volume_num")
        summary = str(interrupt_info.get("summary") or "")
        artifacts = interrupt_info.get("artifacts") or {}
        volume_label = f"第{volume_num}卷" if volume_num not in (None, "", "?") else "当前卷"
        chapter_label = f"第{chapter_num}章" if chapter_num not in (None, "", "?") else volume_label

        if command == "story-context-return":
            return [
                {
                    "option": "A",
                    "label": "进入 context-return",
                    "risk": "low",
                    "description": summary,
                    "actions": [
                        f"读取 {artifacts.get('validation_ref') or 'review/第V卷.validation.json'}",
                        f"按{volume_label}执行 PASS-only 上下文回流",
                        "回写 Cards.current_state/history、planning actualization sidecars、story_map actualization compat projection、项目 CONTEXT 与 runtime projections",
                    ],
                },
                {
                    "option": "B",
                    "label": "先人工核对 review 证据",
                    "risk": "low",
                    "description": "保留当前现场，先确认审查报告与 checkpoint 后再执行上下文回流。",
                    "actions": [
                        f"查看 {artifacts.get('review_report_ref') or 'review/第V卷审查报告.md'}",
                        "核对 review_checkpoints 与 validation packet 是否一致",
                        "确认后再进入 context-return",
                    ],
                },
            ]

        if command == "story-validate":
            return [
                {
                    "option": "A",
                    "label": "进入 review 终验",
                    "risk": "low",
                    "description": summary,
                    "actions": [
                        f"读取 {artifacts.get('validation_ref') or 'review/第V卷.validation.json'}",
                        "执行后台 code-reviewer 审计并聚合 findings",
                        "根据结果决定交 review、context-return或打回 drafting/source",
                    ],
                },
                {
                    "option": "B",
                    "label": "先核 aggregate JSON",
                    "risk": "low",
                    "description": "先核 aggregate JSON 与 code-reviewer 证据，再决定是否立即继续。",
                    "actions": [
                        "检查 validation_status / routing_decision / handoff_targets",
                        "确认 aggregate 字段完整后再进入 review",
                    ],
                },
            ]

        if command == "story-validate":
            return [
                {
                    "option": "A",
                    "label": "进入 review 终验",
                    "risk": "low",
                    "description": summary,
                    "actions": [
                        f"读取 {artifacts.get('writing_log_ref') or '3-初稿/第V卷.写作日志.yaml'}",
                        f"对{volume_label}执行正式 review 聚合验收",
                        "根据 PASS / FAIL 决定交 review、context-return或打回 drafting/source",
                    ],
                },
                {
                    "option": "B",
                    "label": "先核 candidate_final_draft 现场",
                    "risk": "low",
                    "description": "保留写作终稿与写作日志，人工确认后再进终验。",
                    "actions": [
                        f"查看 {artifacts.get('writing_log_ref') or '3-初稿/第V卷.写作日志.yaml'}",
                        f"查看 {chapter_label}或当前卷候选终稿集合",
                        "确认无额外改动后进入 review",
                    ],
                },
            ]

        if command == "story-write":
            if str(interrupt_info.get("resume_reason") or "") in {
                "context_return_completed_next_episode_ready",
                "context_return_completed_next_volume_ready",
                "loopback_completed_next_episode_ready",
                "loopback_completed_next_volume_ready",
            }:
                return [
                    {
                        "option": "A",
                        "label": f"开始{chapter_label} drafting",
                        "risk": "low",
                        "description": summary,
                        "actions": [
                            "读取 carryover_context / writer_projection / runtime_marker",
                            f"进入{chapter_label} drafting",
                            "承接上一轮 validated threads、clue 状态与卷级 continuity 入口",
                        ],
                    },
                    {
                        "option": "B",
                        "label": "先核 carryover_context",
                        "risk": "low",
                        "description": "先确认下一章开场压力与开放线程，再开始写作。",
                        "actions": [
                            "查看 STATE.json.carryover_context",
                            "确认下一卷/下一章开场压力、开放线程与携带物件",
                        ],
                    },
                ]

            return [
                {
                    "option": "A",
                    "label": f"回到{chapter_label} drafting 修订",
                    "risk": "low",
                    "description": summary,
                    "actions": [
                        f"读取 {artifacts.get('validation_ref') or 'review/第V卷.validation.json'}",
                        "按 rework_targets 回到对应 drafting 节点修稿",
                        "修完后重新进入 review",
                    ],
                },
                {
                    "option": "B",
                    "label": "先核 fail packet",
                    "risk": "low",
                    "description": "先确认 routing 与 fail signal，再决定是否立即重写。",
                    "actions": [
                        "检查 validation issues / rework_targets / source_trace",
                        "确认是正文问题还是 source-contract 问题",
                    ],
                },
            ]

        if command in {"story-plan", "story-cards", "story-init"}:
            return [
                {
                    "option": "A",
                    "label": f"进入 {command}",
                    "risk": "low",
                    "description": summary,
                    "actions": [
                        f"读取 {artifacts.get('validation_ref') or 'review/第V卷.validation.json'}",
                        "按 source_trace 指向的上游真源补修后，再重回 validation",
                    ],
                }
            ]

    current_step = interrupt_info["current_step"]
    command = interrupt_info["command"]
    chapter_num = interrupt_info["args"].get("chapter_num", "?")

    if normalize_command_name(command) not in {"story-write", "story-validate", "story-review"}:
        return _generic_recovery_options(interrupt_info)

    if not current_step:
        return [
            {
                "option": "A",
                "label": "从头开始",
                "risk": "low",
                "description": "重新执行完整流程",
                "actions": ["清理 workflow current_task", f"执行 /{command} {chapter_num}"],
            }
        ]

    step_id = current_step["id"]

    if step_id in {"Step 1", "Step 1.5"}:
        return [
            {
                "option": "A",
                "label": "从 Step 1 重新开始",
                "risk": "low",
                "description": "重新起盘当前章，并重新装配 Init/1-设定/2-卷章/上一章终稿上下文",
                "actions": ["清理中断状态", f"执行 /{command} {chapter_num}"],
            }
        ]

    if normalize_command_name(command) == "story-write" and step_id in {"Step 2", "Step 3", "Step 4", "Step 5", "Step 6", "Step 7", "Step 8"}:
        project_root = find_project_root()
        current_target = _primary_drafting_target(project_root, chapter_num)
        chapter_path = (
            str(current_target.relative_to(project_root))
            if current_target is not None
            else str(drafting_root_md_path(project_root, chapter_num).relative_to(project_root))
        )
        sequence = get_pending_steps(command)
        next_step = None
        if step_id in sequence:
            idx = sequence.index(step_id)
            if idx + 1 < len(sequence):
                next_step = sequence[idx + 1]
        step_name = next((name for sid, name, _owner in (get_command_spec(command) or {}).get("steps", []) if sid == step_id), step_id)

        options = [
            {
                "option": "A",
                "label": f"继续 {step_name}",
                "risk": "low",
                "description": f"保留 {chapter_path}，继续当前工序",
                "actions": [
                    f"打开并继续加工 {chapter_path}",
                    "保存正文与写作日志",
                    (f"继续 {next_step}" if next_step else "完成当前章 3-初稿，并准备交接 review"),
                ],
            },
            {
                "option": "B",
                "label": "删除当前章正文，从 Step 1 重启",
                "risk": "medium",
                "description": f"清理 {chapter_path}（以及兼容旧路径正文，如存在），重新起盘当前章",
                "actions": [
                    f"删除 {chapter_path}（及 legacy 正文，如存在）",
                    "清理 Git 暂存区",
                    "清理中断状态",
                    f"执行 /{command} {chapter_num}",
                ],
            },
        ]
        if current_target and current_target.exists():
            options.append(
                {
                    "option": "C",
                    "label": "保留半成品做人工检查",
                    "risk": "medium",
                    "description": "不自动删除正文文件，只清理 workflow 中断状态，便于人工比对和决定下一步",
                    "actions": [
                        f"保留 {chapter_path}",
                        "如需保留现场，先执行 workflow fail-task 记录失败原因",
                        "清理中断状态或在人工确认后再重新开始",
                    ],
                }
            )
        return options

    if normalize_command_name(command) == "story-validate" and step_id in {"Step 1", "Step 2", "Step 3", "Step 4"}:
        return [
            {
                "option": "A",
                "label": "从当前步骤继续",
                "risk": "low",
                "description": "保持当前 review 输入不变，继续 code-reviewer 审计、聚合和路由。",
                "actions": ["保留当前 review 现场", f"继续 {command}"],
            },
            {
                "option": "B",
                "label": "保留现场并人工核对",
                "risk": "medium",
                "description": "保留 aggregate、报告与审计 sidecar，稍后再继续。",
                "actions": ["记录当前现场", "清理中断状态", "人工决定是否重跑或继续"],
            },
        ]

    if normalize_command_name(command) == "story-review" and step_id in {"Step 1", "Step 2", "Step 3", "Step 4", "Step 5", "Step 6"}:
        return [
            {
                "option": "A",
                "label": "从当前步骤继续",
                "risk": "low",
                "description": "保持当前 review 输入不变，继续后续聚合/报告/落库",
                "actions": ["保留当前 review 现场", f"继续 {command}"],
            },
            {
                "option": "B",
                "label": "保留工作区，退出恢复流程",
                "risk": "medium",
                "description": "清理 workflow 中断状态，但保留报告与现场供人工判断",
                "actions": ["记录当前现场", "清理中断状态", "人工决定是否重跑或继续"],
            },
        ]

    return _generic_recovery_options(interrupt_info)


def _backup_chapter_for_cleanup(project_root: Path, chapter_num: int, chapter_path: Path) -> Path:
    backup_dir = project_root / ".webnovel" / "recovery_backups"
    create_secure_directory(str(backup_dir))
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_name = f"ch{chapter_num:04d}-{chapter_path.name}.{timestamp}.bak"
    backup_path = backup_dir / backup_name
    shutil.copy2(chapter_path, backup_path)
    return backup_path


def cleanup_artifacts(chapter_num, *, confirm: bool = False):
    artifacts_cleaned = []
    planned_actions = []

    project_root = find_project_root()
    cleanup_targets = [path for path in _drafting_resume_targets(project_root, chapter_num) if path.exists()]

    for target in cleanup_targets:
        planned_actions.append(f"删除章节文件: {target.relative_to(project_root)}")
    planned_actions.append("重置 Git 暂存区: git reset HEAD .")

    if not confirm:
        preview_items = [f"[预览] {action}" for action in planned_actions]
        payload = {"chapter": chapter_num, "planned_actions": planned_actions, "confirmed": False}
        safe_append_call_trace("artifacts_cleanup_preview", payload)
        safe_append_task_log("artifacts_cleanup_preview", payload)
        print("⚠️ 检测到高风险清理操作，当前仅预览。若确认执行，请追加 --confirm。")
        return preview_items or ["[预览] 无可清理项"]

    for chapter_path in cleanup_targets:
        try:
            backup_path = _backup_chapter_for_cleanup(project_root, chapter_num, chapter_path)
        except OSError as exc:
            payload = {"chapter": chapter_num, "chapter_file": str(chapter_path), "error": str(exc)}
            safe_append_call_trace("artifacts_cleanup_backup_failed", payload)
            safe_append_task_log("artifacts_cleanup_backup_failed", payload)
            return [f"❌ 章节备份失败，已取消删除: {exc}"]

        chapter_path.unlink()
        artifacts_cleaned.append(str(chapter_path.relative_to(project_root)))
        artifacts_cleaned.append(f"章节备份已保存: {backup_path.relative_to(project_root)}")

    result = subprocess.run(["git", "reset", "HEAD", "."], cwd=project_root, capture_output=True, text=True)
    if result.returncode == 0:
        artifacts_cleaned.append("Git 暂存区已清理（project）")
    else:
        git_error = (result.stderr or "").strip() or "unknown error"
        artifacts_cleaned.append(f"⚠️ Git 暂存区清理失败: {git_error}")

    payload = {
        "chapter": chapter_num,
        "items": artifacts_cleaned,
        "planned_actions": planned_actions,
        "confirmed": True,
        "git_reset_ok": result.returncode == 0,
    }
    safe_append_call_trace("artifacts_cleaned", payload)
    safe_append_task_log("artifacts_cleaned", payload)
    return artifacts_cleaned or ["无可清理项"]


def get_status_snapshot() -> dict[str, Any]:
    state = load_state()
    execution_state = load_execution_state()
    current_task = state.get("current_task")
    snapshot = {
        "current_task": current_task,
        "last_stable_state": state.get("last_stable_state"),
        "latest_resume_point": execution_state.get("latest_resume_point"),
        "active_run_id": execution_state.get("active_run_id"),
        "stage_progress": execution_state.get("stage_progress", {}),
        "recent_runs": execution_state.get("runs", [])[-5:],
        "inline_validation": (current_task or {}).get("inline_validation"),
        "candidate_final_state": (current_task or {}).get("candidate_final_state"),
    }
    return snapshot


def print_status(format_name: str = "text"):
    snapshot = get_status_snapshot()
    if format_name == "json":
        print(json.dumps(snapshot, ensure_ascii=False, indent=2))
        return

    current_task = snapshot.get("current_task")
    if current_task:
        print(f"当前任务: {current_task.get('command')} ({current_task.get('run_id')})")
        print(f"状态: {current_task.get('status')} | 当前步骤: {(current_task.get('current_step') or {}).get('id') or '无'}")
        inline_state = current_task.get("inline_validation") or {}
        active_batch = inline_state.get("active_batch") if isinstance(inline_state, dict) else None
        blocking_gate = inline_state.get("blocking_gate") if isinstance(inline_state, dict) else None
        if active_batch:
            pending = [
                validator.get("role_id")
                for validator in active_batch.get("validators", [])
                if str(validator.get("status")) == INLINE_VALIDATION_STATUS_PENDING
            ]
            print(f"即时审计: pending after {active_batch.get('step_id')} | 待处理={', '.join(pending) or '-'}")
        elif blocking_gate:
            print(
                "即时审计: blocked"
                f" | after={blocking_gate.get('step_id')}"
                f" | rework={blocking_gate.get('allowed_rework_step_id') or 'source-fix'}"
            )
        candidate_state = current_task.get("candidate_final_state") or {}
        if candidate_state:
            print(f"候选终稿状态: {candidate_state.get('status')} | reason={candidate_state.get('reason')}")
    else:
        print("当前任务: 无")

    latest_resume = snapshot.get("latest_resume_point") or {}
    if latest_resume:
        print(
            "最近恢复点: "
            f"{latest_resume.get('command')} / {latest_resume.get('current_step') or '无'} / {latest_resume.get('reason')}"
        )

    print("阶段进度:")
    for stage_id, info in snapshot.get("stage_progress", {}).items():
        print(
            f"- {stage_id}: {info.get('status')} | latest_run={info.get('latest_run_id') or '-'} | "
            f"step={info.get('current_step') or '-'} | resume_ready={info.get('resume_ready')}"
        )


def list_runs(limit: int = 10, format_name: str = "text"):
    execution_state = load_execution_state()
    runs = execution_state.get("runs", [])[-max(1, int(limit)) :]
    if format_name == "json":
        print(json.dumps(runs, ensure_ascii=False, indent=2))
        return

    if not runs:
        print("暂无 run 记录")
        return
    for run in runs:
        print(
            f"{run.get('run_id')} | {run.get('command')} | {run.get('status')} | "
            f"{(run.get('current_step') or {}).get('id') or '-'} | {run.get('started_at')}"
        )


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="工作流状态管理")
    parser.add_argument("--project-root", dest="global_project_root", help="项目根目录（可选，默认自动检测）")
    subparsers = parser.add_subparsers(dest="action", help="操作类型")

    def add_project_root_arg(subparser):
        subparser.add_argument("--project-root", help="项目根目录（可选，默认自动检测）")

    p_start_task = subparsers.add_parser("start-task", help="开始新任务")
    add_project_root_arg(p_start_task)
    p_start_task.add_argument("--command", required=True, help="命令名称")
    p_start_task.add_argument("--chapter", type=int, help="章节号")
    p_start_task.add_argument("--mode", choices=["standard", "fast", "minimal"], help="写作模式（可选）")

    p_start_step = subparsers.add_parser("start-step", help="开始 Step")
    add_project_root_arg(p_start_step)
    p_start_step.add_argument("--step-id", required=True, help="Step ID")
    p_start_step.add_argument("--step-name", required=True, help="Step 名称")
    p_start_step.add_argument("--note", help="进度备注")

    p_heartbeat = subparsers.add_parser("heartbeat", help="刷新任务心跳")
    add_project_root_arg(p_heartbeat)
    p_heartbeat.add_argument("--note", help="进度备注")
    p_heartbeat.add_argument("--progress", type=int, help="进度百分比")

    p_complete_step = subparsers.add_parser("complete-step", help="完成 Step")
    add_project_root_arg(p_complete_step)
    p_complete_step.add_argument("--step-id", required=True, help="Step ID")
    p_complete_step.add_argument("--artifacts", help="Artifacts JSON")

    p_inline_record = subparsers.add_parser("record-inline-validation", help="记录当前 step 的 inline validation 结果")
    add_project_root_arg(p_inline_record)
    p_inline_record.add_argument("--step-id", required=True, help="触发该 hook batch 的 workflow Step ID")
    p_inline_record.add_argument("--role-id", required=True, help="validator role_id")
    p_inline_record.add_argument("--result", required=True, help="validator 结构化结果 JSON 或 @文件路径")

    p_inline_run = subparsers.add_parser("run-inline-validation-batch", help="自动执行当前 active inline validation batch")
    add_project_root_arg(p_inline_run)

    p_complete_task = subparsers.add_parser("complete-task", help="完成任务")
    add_project_root_arg(p_complete_task)
    p_complete_task.add_argument("--artifacts", help="Final artifacts JSON")

    p_fail_task = subparsers.add_parser("fail-task", help="标记任务失败")
    add_project_root_arg(p_fail_task)
    p_fail_task.add_argument("--reason", default="manual_fail", help="失败原因")

    p_detect = subparsers.add_parser("detect", help="检测中断")
    add_project_root_arg(p_detect)

    p_cleanup = subparsers.add_parser("cleanup", help="清理 artifacts")
    add_project_root_arg(p_cleanup)
    p_cleanup.add_argument("--chapter", type=int, required=True, help="章节号")
    p_cleanup.add_argument("--confirm", action="store_true", help="确认执行删除与 Git 重置（高风险）")

    p_clear = subparsers.add_parser("clear", help="清除中断任务")
    add_project_root_arg(p_clear)

    p_status = subparsers.add_parser("status", help="查看 workflow 状态快照")
    add_project_root_arg(p_status)
    p_status.add_argument("--format", choices=["text", "json"], default="text", help="输出格式")

    p_list_runs = subparsers.add_parser("list-runs", help="列出最近 run")
    add_project_root_arg(p_list_runs)
    p_list_runs.add_argument("--limit", type=int, default=10, help="返回最近多少条")
    p_list_runs.add_argument("--format", choices=["text", "json"], default="text", help="输出格式")

    args = parser.parse_args()

    project_root_arg = getattr(args, "project_root", None) or getattr(args, "global_project_root", None)
    if project_root_arg:
        _cli_project_root = normalize_windows_path(project_root_arg)

    if args.action == "start-task":
        task_args = {"chapter_num": args.chapter}
        if getattr(args, "mode", None):
            task_args["mode"] = args.mode
        start_task(args.command, task_args)
    elif args.action == "start-step":
        start_step(args.step_id, args.step_name, args.note)
    elif args.action == "heartbeat":
        heartbeat(args.note, args.progress)
    elif args.action == "complete-step":
        complete_step(args.step_id, args.artifacts)
    elif args.action == "record-inline-validation":
        record_inline_validation(args.step_id, args.role_id, args.result)
    elif args.action == "run-inline-validation-batch":
        run_inline_validation_batch()
    elif args.action == "complete-task":
        complete_task(args.artifacts)
    elif args.action == "fail-task":
        fail_current_task(args.reason)
    elif args.action == "detect":
        interrupt = detect_interruption()
        if interrupt:
            if str(interrupt.get("detection_mode") or "") == "artifact_fallback":
                print("\nℹ️ 未检测到 tracked 中断，但发现可证明的 artifact continuation:")
            else:
                print("\n🔶 检测到中断任务:")
            print(json.dumps(interrupt, ensure_ascii=False, indent=2))
            print("\n📕 恢复选项:")
            options = analyze_recovery_options(interrupt)
            print(json.dumps(options, ensure_ascii=False, indent=2))
        else:
            print("✅ 无中断任务")
    elif args.action == "cleanup":
        cleaned = cleanup_artifacts(args.chapter, confirm=args.confirm)
        if args.confirm:
            print(f"✅ 已清理: {', '.join(cleaned)}")
        else:
            for item in cleaned:
                print(item)
            print("⚠️ 以上为预览，未执行实际清理。")
    elif args.action == "clear":
        clear_current_task()
    elif args.action == "status":
        print_status(args.format)
    elif args.action == "list-runs":
        list_runs(args.limit, args.format)
    else:
        parser.print_help()
