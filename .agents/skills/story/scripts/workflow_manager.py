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
import shutil
import subprocess
import sys
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, Optional

from chapter_paths import default_chapter_draft_path, drafting_root_md_path, find_chapter_file
from project_locator import resolve_project_root, resolve_state_file
from runtime_compat import enable_windows_utf8_stdio, normalize_windows_path
from security_utils import atomic_write_json, create_secure_directory


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
    "webnovel-loopback": "story-loopback",
    "story2026-loopback": "story-loopback",
    "story-loopback": "story-loopback",
    "webnovel-query": "story-query",
    "story-query": "story-query",
    "webnovel-resume": "story-resume",
    "story-resume": "story-resume",
}


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
            ("Step 1", "选择初始化模式与采集策略", "story-init-skill"),
            ("Step 2", "收集问卷与故事核", "story-init-skill"),
            ("Step 3", "归一化关键字段", "story-init-skill"),
            ("Step 4", "一致性与约束校验", "story-init-skill"),
            ("Step 5", "写入期初文件", "init-project"),
            ("Step 6", "生成初始化简报", "story-init-skill"),
            ("Step 7", "验证项目骨架", "story-init-skill"),
        ],
    },
    "story-cards": {
        "stage_id": "1-cards",
        "stage_label": "卡片层",
        "steps": [
            ("Step 1", "路由与输入校验", "story-cards"),
            ("Step 2", "读取 north star 对象约束", "story-init-skill"),
            ("Step 3", "角色卡（references/character）", "story-cards"),
            ("Step 4", "场景卡（references/scene）", "story-cards"),
            ("Step 5", "物品卡（references/item）", "story-cards"),
            ("Step 6", "覆盖率校验", "cards-coverage-validator"),
        ],
    },
    "story-plan": {
        "stage_id": "2-planning",
        "stage_label": "规划层",
        "steps": [
            ("Step 1", "题材选型（1-题材选型）", "story-plan"),
            ("Step 2", "章节规划（2-章节规划）", "story-plan"),
            ("Step 3", "故事大纲（3-故事大纲）", "story-plan"),
            ("Step 4", "冲突设计（4-冲突设计）", "story-plan"),
            ("Step 5", "任务设计（5-任务设计）", "story-plan"),
            ("Step 6", "线索设计（6-线索设计）", "story-plan"),
            ("Step 7", "伏笔设计（7-伏笔设计）", "story-plan"),
            ("Step 8", "父层收束全息地图（shared root normalize）", "story-plan"),
        ],
    },
    "story-write": {
        "stage_id": "3-drafting",
        "stage_label": "起草层",
        "steps": [
            ("Step 1", "单集叙事起盘", "drafting-episode-kickoff"),
            ("Step 2", "节奏优化", "drafting-pacing"),
            ("Step 3", "场景和氛围渲染", "drafting-scene-atmosphere"),
            ("Step 4", "角色形象刻画", "drafting-character-rendering"),
            ("Step 5", "对白个性化和声口优化", "drafting-dialogue-voice"),
            ("Step 6", "叙事张力强化", "drafting-tension"),
            ("Step 7", "润色", "drafting-polish"),
        ],
    },
    "story-validate": {
        "stage_id": "4-validation",
        "stage_label": "验证层",
        "steps": [
            ("Step 1", "加载事实包", "context-agent"),
            ("Step 2", "分发验证团队", "validation-team"),
            ("Step 3", "聚合结论", "validation-aggregator"),
            ("Step 4", "路由交接", "validation-router"),
        ],
    },
    "story-review": {
        "stage_id": "review",
        "stage_label": "审查层",
        "steps": [
            ("Step 1", "确认 Validation 输出", "story-review-skill"),
            ("Step 2", "加载参考与项目状态", "story-review-skill"),
            ("Step 3", "汇总评估结果", "story-review-skill"),
            ("Step 4", "生成审查报告", "story-review-skill"),
            ("Step 5", "保存审查指标", "story-review-skill"),
            ("Step 6", "写回审查记录", "story-review-skill"),
            ("Step 7", "关键问题升级/分流", "story-review-skill"),
            ("Step 8", "收尾", "story-review-skill"),
        ],
    },
    "story-loopback": {
        "stage_id": "5-loopback",
        "stage_label": "回写层",
        "steps": [
            ("Step 1", "解析 validation 与 delta", "loopback-manager"),
            ("Step 2", "构建对象/规划回写", "loopback-manager"),
            ("Step 3", "刷新 projection 与 runtime marker", "loopback-manager"),
            ("Step 4", "验证 PASS-only writeback", "loopback-manager"),
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


def now_iso() -> str:
    return datetime.now().isoformat()


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


def expected_step_owner(command: str, step_id: str) -> str:
    return _step_owner_map(command).get(step_id, command or "unknown")


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
    return {
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


def _new_run_record(task: Dict[str, Any]) -> Dict[str, Any]:
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

    owner = expected_step_owner(command, step_id)
    _finalize_current_step_as_failed(task, reason="step_replaced_before_completion")

    started_at = now_iso()
    task["current_step"] = {
        "id": step_id,
        "name": step_name,
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
    print(f"✅ {step_id} 完成")


def complete_task(final_artifacts_json=None):
    state = load_state()
    execution_state = load_execution_state()
    task = state.get("current_task")
    if not task:
        print("⚠️ 无活动任务")
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
        return None

    task = state["current_task"]
    if task.get("status") == TASK_STATUS_COMPLETED:
        return None

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
    current_step = interrupt_info["current_step"]
    command = interrupt_info["command"]
    chapter_num = interrupt_info["args"].get("chapter_num", "?")

    if normalize_command_name(command) not in {"story-write", "story-review"}:
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
                "description": "重新起盘当前集，并重新装配 Init/Cards/Planning/上一集终稿上下文",
                "actions": ["清理中断状态", f"执行 /{command} {chapter_num}"],
            }
        ]

    if normalize_command_name(command) == "story-write" and step_id in {"Step 2", "Step 3", "Step 4", "Step 5", "Step 6", "Step 7"}:
        project_root = find_project_root()
        current_target = _primary_drafting_target(project_root, chapter_num)
        chapter_path = (
            str(current_target.relative_to(project_root))
            if current_target is not None
            else f"3-Drafting/第{chapter_num}集.md"
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
                    (f"继续 {next_step}" if next_step else "完成当前集 3-Drafting，并准备交接 4-Validation"),
                ],
            },
            {
                "option": "B",
                "label": "删除当前集正文，从 Step 1 重启",
                "risk": "medium",
                "description": f"清理 {chapter_path}（以及兼容旧路径正文，如存在），重新起盘当前集",
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
    elif args.action == "complete-task":
        complete_task(args.artifacts)
    elif args.action == "fail-task":
        fail_current_task(args.reason)
    elif args.action == "detect":
        interrupt = detect_interruption()
        if interrupt:
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
