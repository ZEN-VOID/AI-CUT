#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import logging
import sys
from pathlib import Path
from types import SimpleNamespace


def _load_module():
    scripts_dir = Path(__file__).resolve().parents[2]
    if str(scripts_dir) not in sys.path:
        sys.path.insert(0, str(scripts_dir))
    import workflow_manager

    return workflow_manager


def _seed_project_root(project_root: Path) -> None:
    (project_root / ".webnovel").mkdir(parents=True, exist_ok=True)
    (project_root / "STATE.json").write_text("{}", encoding="utf-8")


def _write_project_state(project_root: Path, payload: dict) -> None:
    (project_root / "STATE.json").write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")


def _seed_manuscript(project_root: Path, chapter_num: int, text: str) -> None:
    drafting_dir = project_root / "3-Drafting"
    drafting_dir.mkdir(parents=True, exist_ok=True)
    (drafting_dir / f"第{chapter_num}集.md").write_text(text, encoding="utf-8")


def _pass_all_active_inline_validators(module) -> None:
    state = module.load_state()
    task = state.get("current_task") or {}
    batch = ((task.get("inline_validation") or {}) if isinstance(task, dict) else {}).get("active_batch")
    assert batch is not None
    step_id = batch["step_id"]
    for validator in batch.get("validators", []):
        module.record_inline_validation(
            step_id,
            validator["role_id"],
            json.dumps(
                {
                    "validation_context": "drafting_inline",
                    "pass": True,
                    "issues": [],
                    "summary": "ok",
                },
                ensure_ascii=False,
            ),
        )


def test_workflow_lifecycle_and_trace(tmp_path, monkeypatch):
    module = _load_module()
    monkeypatch.setattr(module, "find_project_root", lambda: tmp_path)
    _seed_project_root(tmp_path)

    module.start_task("story-plan", {"chapter_num": 7})
    module.start_step("Step 1", "Context")
    module.complete_step("Step 1", json.dumps({"state_json_modified": True}, ensure_ascii=False))
    module.complete_task(json.dumps({"review_completed": True}, ensure_ascii=False))

    state = module.load_state()
    execution_state = module.load_execution_state()
    assert state["current_task"] is None
    assert state["history"][-1]["status"] == module.TASK_STATUS_COMPLETED
    assert state["last_stable_state"]["artifacts"]["review_completed"] is True
    run_id = execution_state["runs"][-1]["run_id"]
    assert state["last_stable_state"]["governance_refs"]["mission_brief_ref"] == (
        f"STATE.json#workflow_runtime.governance_index.{run_id}.mission_brief"
    )
    assert execution_state["active_run_id"] is None
    assert execution_state["runs"][-1]["status"] == module.TASK_STATUS_COMPLETED
    assert execution_state["stage_progress"]["2-planning"]["status"] == module.TASK_STATUS_COMPLETED
    assert execution_state["runs"][-1]["governance_refs"]["validation_report_ref"] == (
        f"STATE.json#workflow_runtime.governance_index.{run_id}.validation_report"
    )

    task_log_path = module.get_task_log_path()
    assert task_log_path.exists()
    project_state = json.loads(task_log_path.read_text(encoding="utf-8"))
    task_log_events = [
        row["event"]
        for row in project_state["workflow_runtime"]["task_log"]
        if isinstance(row, dict) and row.get("event")
    ]
    assert "task_started" in task_log_events
    assert "task_completed" in task_log_events

    trace_path = module.get_call_trace_path()
    assert trace_path.exists()
    lines = trace_path.read_text(encoding="utf-8").strip().splitlines()
    events = [json.loads(line)["event"] for line in lines if line.strip()]
    assert "task_started" in events
    assert "step_started" in events
    assert "step_completed" in events
    assert "task_completed" in events

    governance_bundle = execution_state["governance_index"][run_id]
    assert governance_bundle["mandate"]["task_id"] == run_id
    assert governance_bundle["mission_brief"]["task_id"] == run_id
    assert governance_bundle["route_plan"]["task_id"] == run_id
    assert governance_bundle["preflight_verdict"]["task_id"] == run_id
    assert governance_bundle["artifact_manifest"]["status"] == module.TASK_STATUS_COMPLETED
    assert governance_bundle["validation_report"] == f"story-plan 已完成，run_id={run_id}"
    assert governance_bundle["learning_record"] == "completed"


def test_start_task_reentry_increments_retry(tmp_path, monkeypatch):
    module = _load_module()
    monkeypatch.setattr(module, "find_project_root", lambda: tmp_path)
    _seed_project_root(tmp_path)

    module.start_task("story-write", {"chapter_num": 8})
    module.start_task("story-write", {"chapter_num": 8})

    state = module.load_state()
    task = state["current_task"]
    assert task is not None
    assert task["status"] == module.TASK_STATUS_RUNNING
    assert int(task.get("retry_count", 0)) >= 1


def test_legacy_command_aliases_are_normalized(tmp_path, monkeypatch):
    module = _load_module()
    monkeypatch.setattr(module, "find_project_root", lambda: tmp_path)
    _seed_project_root(tmp_path)

    module.start_task("webnovel-write", {"chapter_num": 6})

    state = module.load_state()
    execution_state = module.load_execution_state()
    assert state["current_task"]["command"] == "story-write"
    assert execution_state["runs"][-1]["command"] == "story-write"
    assert module.expected_step_owner("webnovel-write", "Step 1") == "drafting-episode-kickoff"


def test_complete_step_rejects_mismatch_step_id(tmp_path, monkeypatch):
    module = _load_module()
    monkeypatch.setattr(module, "find_project_root", lambda: tmp_path)
    _seed_project_root(tmp_path)

    module.start_task("story-write", {"chapter_num": 9})
    module.start_step("Step 1", "Context")
    module.complete_step("Step 1")
    _pass_all_active_inline_validators(module)
    module.start_step("Step 2", "Pacing")
    module.complete_step("Step 3")

    state = module.load_state()
    current_step = state["current_task"]["current_step"]
    assert current_step is not None
    assert current_step["id"] == "Step 2"
    assert current_step["status"] == module.STEP_STATUS_RUNNING


def test_story_write_step_completion_triggers_inline_validation_batch(tmp_path, monkeypatch):
    module = _load_module()
    monkeypatch.setattr(module, "find_project_root", lambda: tmp_path)
    _seed_project_root(tmp_path)

    module.start_task("story-write", {"chapter_num": 14})
    module.start_step("Step 1", "Context")
    module.complete_step("Step 1")

    state = module.load_state()
    task = state["current_task"]
    inline_state = task["inline_validation"]
    active_batch = inline_state["active_batch"]

    assert active_batch is not None
    assert active_batch["step_id"] == "Step 1"
    assert active_batch["status"] == module.INLINE_VALIDATION_STATUS_PENDING
    assert {item["role_id"] for item in active_batch["validators"]} == {
        "structure-validator",
        "continuity-validator",
        "logic-validator",
        "timeline-validator",
    }


def test_story_write_complete_step_auto_runs_inline_validation_when_manuscript_exists(tmp_path, monkeypatch):
    module = _load_module()
    monkeypatch.setattr(module, "find_project_root", lambda: tmp_path)
    _seed_project_root(tmp_path)
    _seed_manuscript(
        tmp_path,
        19,
        "清晨，李青还站在山门前。长老拦住他，问他为何执意下山。李青没有解释太多，只说自己要把昨夜留下的线索查清。",
    )

    module.start_task("story-write", {"chapter_num": 19})
    module.start_step("Step 1", "单集叙事起盘")
    module.complete_step("Step 1")

    state = module.load_state()
    inline_state = state["current_task"]["inline_validation"]
    assert inline_state["active_batch"] is None
    assert inline_state["history"]
    assert inline_state["latest_summary"]["reason"] == "auto_runner_recorded"


def test_story_write_next_step_blocked_until_inline_validation_finishes(tmp_path, monkeypatch):
    module = _load_module()
    monkeypatch.setattr(module, "find_project_root", lambda: tmp_path)
    _seed_project_root(tmp_path)

    module.start_task("story-write", {"chapter_num": 15})
    module.start_step("Step 1", "Context")
    module.complete_step("Step 1")
    module.start_step("Step 2", "Pacing")

    state = module.load_state()
    assert state["current_task"]["current_step"] is None
    assert state["current_task"]["inline_validation"]["active_batch"] is not None


def test_story_write_passed_inline_validation_allows_next_step(tmp_path, monkeypatch):
    module = _load_module()
    monkeypatch.setattr(module, "find_project_root", lambda: tmp_path)
    _seed_project_root(tmp_path)

    module.start_task("story-write", {"chapter_num": 16})
    module.start_step("Step 1", "Context")
    module.complete_step("Step 1")
    _pass_all_active_inline_validators(module)
    module.start_step("Step 2", "Pacing")

    state = module.load_state()
    assert state["current_task"]["current_step"]["id"] == "Step 2"
    assert state["current_task"]["inline_validation"]["active_batch"] is None
    assert state["current_task"]["inline_validation"]["blocking_gate"] is None


def test_story_write_failed_inline_validation_requires_rewind(tmp_path, monkeypatch):
    module = _load_module()
    monkeypatch.setattr(module, "find_project_root", lambda: tmp_path)
    _seed_project_root(tmp_path)

    module.start_task("story-write", {"chapter_num": 17})
    module.start_step("Step 1", "单集叙事起盘")
    module.complete_step("Step 1")
    _pass_all_active_inline_validators(module)
    module.start_step("Step 2", "节奏优化")
    module.complete_step("Step 2")
    _pass_all_active_inline_validators(module)
    module.start_step("Step 3", "场景和氛围渲染")
    module.complete_step("Step 3")
    module.start_step("Step 4", "角色形象刻画")
    module.complete_step("Step 4")

    state = module.load_state()
    batch = state["current_task"]["inline_validation"]["active_batch"]
    assert batch is not None

    for validator in batch["validators"]:
        payload = {
            "validation_context": "drafting_inline",
            "pass": validator["role_id"] != "logic-validator",
            "issues": [],
            "summary": "ok",
        }
        if validator["role_id"] == "logic-validator":
            payload["issues"] = [
                {
                    "id": "LG-017-001",
                    "severity": "high",
                    "rework_target_step": "1-单集叙事起盘",
                    "source_layer_owner": "3-Drafting",
                }
            ]
        module.record_inline_validation("Step 4", validator["role_id"], json.dumps(payload, ensure_ascii=False))

    module.start_step("Step 5", "对白个性化")
    state = module.load_state()
    assert state["current_task"]["current_step"] is None
    gate = state["current_task"]["inline_validation"]["blocking_gate"]
    assert gate["allowed_rework_step_id"] == "Step 1"

    module.start_step("Step 1", "单集叙事起盘")
    state = module.load_state()
    assert state["current_task"]["current_step"]["id"] == "Step 1"
    assert state["current_task"]["inline_validation"]["blocking_gate"] is None


def test_story_write_complete_task_requires_candidate_final_draft(tmp_path, monkeypatch):
    module = _load_module()
    monkeypatch.setattr(module, "find_project_root", lambda: tmp_path)
    _seed_project_root(tmp_path)

    module.start_task("story-write", {"chapter_num": 18})
    module.start_step("Step 1", "单集叙事起盘")
    module.complete_step("Step 1")
    _pass_all_active_inline_validators(module)
    module.complete_task(json.dumps({"review_completed": True}, ensure_ascii=False))

    state = module.load_state()
    assert state["current_task"] is not None
    assert state["current_task"]["status"] == module.TASK_STATUS_RUNNING


def test_workflow_step_owner_and_order_violation_trace(tmp_path, monkeypatch):
    module = _load_module()
    monkeypatch.setattr(module, "find_project_root", lambda: tmp_path)
    _seed_project_root(tmp_path)

    assert module.expected_step_owner("story-write", "Step 1") == "drafting-episode-kickoff"
    assert module.expected_step_owner("story-write", "Step 6") == "drafting-inner-life"
    assert module.expected_step_owner("story-write", "Step 7") == "drafting-reading-power"
    assert module.expected_step_owner("story-write", "Step 8") == "drafting-polish"

    module.start_task("story-write", {"chapter_num": 12})
    module.start_step("Step 3", "Review")

    state = module.load_state()
    assert state["current_task"]["current_step"] is None

    trace_path = module.get_call_trace_path()
    lines = [json.loads(line) for line in trace_path.read_text(encoding="utf-8").splitlines() if line.strip()]
    events = [row.get("event") for row in lines]
    assert "step_order_violation" in events

    step_started = [row for row in lines if row.get("event") == "step_started"]
    assert not step_started


def test_workflow_rejects_unknown_step_id(tmp_path, monkeypatch):
    module = _load_module()
    monkeypatch.setattr(module, "find_project_root", lambda: tmp_path)
    _seed_project_root(tmp_path)

    module.start_task("story-write", {"chapter_num": 13})
    module.start_step("Step X", "Bogus")

    state = module.load_state()
    assert state["current_task"]["current_step"] is None

    trace_path = module.get_call_trace_path()
    lines = [json.loads(line) for line in trace_path.read_text(encoding="utf-8").splitlines() if line.strip()]
    rejected = [row for row in lines if row.get("event") == "step_start_rejected"]
    assert rejected
    assert rejected[-1].get("payload", {}).get("reason") == "unknown_step_id"


def test_safe_append_call_trace_logs_failure(monkeypatch, caplog):
    module = _load_module()

    def _raise_trace_error(event, payload=None):
        raise RuntimeError("trace failure")

    monkeypatch.setattr(module, "append_call_trace", _raise_trace_error)

    with caplog.at_level(logging.WARNING):
        module.safe_append_call_trace("unit_test_event", {"ok": True})

    message_text = "\n".join(record.getMessage() for record in caplog.records)
    assert "failed to append call trace" in message_text
    assert "unit_test_event" in message_text


def test_get_workflow_paths_support_zero_arg_find_project_root(tmp_path, monkeypatch):
    module = _load_module()
    monkeypatch.setattr(module, "_cli_project_root", None)
    monkeypatch.setattr(module, "find_project_root", lambda: tmp_path)
    _seed_project_root(tmp_path)

    assert module.get_workflow_state_path() == tmp_path / "STATE.json"
    assert module.get_execution_state_path() == tmp_path / "STATE.json"
    assert module.get_task_log_path() == tmp_path / "STATE.json"
    assert module.get_call_trace_path() == tmp_path / ".webnovel" / "observability" / "call_trace.jsonl"


def test_workflow_reentry_does_not_duplicate_history(tmp_path, monkeypatch):
    module = _load_module()
    monkeypatch.setattr(module, "find_project_root", lambda: tmp_path)
    _seed_project_root(tmp_path)

    module.start_task("story-write", {"chapter_num": 20})
    module.start_task("story-write", {"chapter_num": 20})
    module.start_task("story-write", {"chapter_num": 20})

    state = module.load_state()
    assert isinstance(state.get("history"), list)
    assert len(state.get("history")) == 0

    task = state.get("current_task") or {}
    assert int(task.get("retry_count", 0)) >= 2


def test_cleanup_artifacts_requires_confirm(tmp_path, monkeypatch):
    module = _load_module()
    monkeypatch.setattr(module, "find_project_root", lambda: tmp_path)
    _seed_project_root(tmp_path)

    draft_path = module.drafting_root_md_path(tmp_path, 7)
    draft_path.parent.mkdir(parents=True, exist_ok=True)
    draft_path.write_text("draft", encoding="utf-8")

    git_called = {"count": 0}

    def _fake_run(*args, **kwargs):
        git_called["count"] += 1
        return SimpleNamespace(returncode=0, stderr="", stdout="")

    monkeypatch.setattr(module.subprocess, "run", _fake_run)

    preview = module.cleanup_artifacts(7, confirm=False)

    assert draft_path.exists()
    assert git_called["count"] == 0
    assert any(item.startswith("[预览]") for item in preview)


def test_cleanup_artifacts_confirm_deletes_with_backup(tmp_path, monkeypatch):
    module = _load_module()
    monkeypatch.setattr(module, "find_project_root", lambda: tmp_path)
    _seed_project_root(tmp_path)

    draft_path = module.drafting_root_md_path(tmp_path, 8)
    draft_path.parent.mkdir(parents=True, exist_ok=True)
    draft_path.write_text("draft", encoding="utf-8")

    git_called = {"count": 0, "cmd": None}

    def _fake_run(cmd, **kwargs):
        git_called["count"] += 1
        git_called["cmd"] = cmd
        return SimpleNamespace(returncode=0, stderr="", stdout="")

    monkeypatch.setattr(module.subprocess, "run", _fake_run)

    cleaned = module.cleanup_artifacts(8, confirm=True)

    assert not draft_path.exists()
    assert git_called["count"] == 1
    assert git_called["cmd"] == ["git", "reset", "HEAD", "."]
    assert any("Git 暂存区已清理" in item for item in cleaned)

    backup_dir = tmp_path / ".webnovel" / "recovery_backups"
    backups = list(backup_dir.glob("ch0008-*"))
    assert backups


def test_analyze_recovery_options_midpass_avoids_destructive_git_reset(tmp_path, monkeypatch):
    module = _load_module()
    monkeypatch.setattr(module, "find_project_root", lambda: tmp_path)
    _seed_project_root(tmp_path)

    draft_path = module.drafting_root_md_path(tmp_path, 11)
    draft_path.parent.mkdir(parents=True, exist_ok=True)
    draft_path.write_text("draft", encoding="utf-8")

    interrupt_info = {
        "command": "story-write",
        "args": {"chapter_num": 11},
        "current_step": {"id": "Step 5"},
    }

    options = module.analyze_recovery_options(interrupt_info)

    action_text = "\n".join(action for option in options for action in option.get("actions", []))
    assert "reset --hard" not in action_text
    assert "3-Drafting/第11集.md" in action_text
    assert any(option.get("label") == "保留半成品做人工检查" for option in options)


def test_analyze_recovery_options_polish_step_keeps_new_drafting_target(tmp_path, monkeypatch):
    module = _load_module()
    monkeypatch.setattr(module, "find_project_root", lambda: tmp_path)
    _seed_project_root(tmp_path)

    draft_path = module.drafting_root_md_path(tmp_path, 12)
    draft_path.parent.mkdir(parents=True, exist_ok=True)
    draft_path.write_text("draft", encoding="utf-8")

    interrupt_info = {
        "command": "story-write",
        "args": {"chapter_num": 12},
        "current_step": {"id": "Step 8"},
    }

    options = module.analyze_recovery_options(interrupt_info)

    action_text = "\n".join(action for option in options for action in option.get("actions", []))
    assert "3-Drafting/第12集.md" in action_text
    assert "backup_manager.py" not in action_text
    assert any(option.get("label") == "继续 润色" for option in options)


def test_workflow_supports_non_drafting_stage_runs(tmp_path, monkeypatch):
    module = _load_module()
    monkeypatch.setattr(module, "find_project_root", lambda: tmp_path)
    _seed_project_root(tmp_path)

    module.start_task("story-plan", {"chapter_num": None})
    module.start_step("Step 1", "题材选型")
    module.heartbeat("正在收敛题材走廊", 25)

    state = module.load_state()
    execution_state = module.load_execution_state()
    current_task = state["current_task"]
    assert current_task["command"] == "story-plan"
    assert current_task["current_step"]["progress_note"] == "正在收敛题材走廊"
    assert current_task["current_step"]["progress_percent"] == 25
    assert current_task["governance_refs"]["governance_bundle_ref"].startswith(
        "STATE.json#workflow_runtime.governance_index."
    )
    assert execution_state["stage_progress"]["2-planning"]["status"] == module.TASK_STATUS_RUNNING


def test_failed_task_writes_root_cause_trace(tmp_path, monkeypatch):
    module = _load_module()
    monkeypatch.setattr(module, "find_project_root", lambda: tmp_path)
    _seed_project_root(tmp_path)

    module.start_task("story-write", {"chapter_num": 21})
    module.start_step("Step 1", "Context")
    module.fail_current_task("unit-test-failure")

    state = module.load_state()
    execution_state = module.load_execution_state()
    run_id = execution_state["latest_resume_point"]["run_id"]
    governance_bundle = execution_state["governance_index"][run_id]

    assert state["current_task"]["status"] == module.TASK_STATUS_FAILED
    assert execution_state["runs"][-1]["status"] == module.TASK_STATUS_FAILED
    assert governance_bundle["root_cause_trace"] == "unit-test-failure"
    assert governance_bundle["artifact_manifest"]["status"] == module.TASK_STATUS_FAILED
    assert execution_state["runs"][-1]["command"] == "story-write"


def test_generic_recovery_options_for_non_write_review(tmp_path, monkeypatch):
    module = _load_module()
    monkeypatch.setattr(module, "find_project_root", lambda: tmp_path)
    _seed_project_root(tmp_path)

    interrupt_info = {
        "run_id": "2-planning-run-0001",
        "command": "story-plan",
        "args": {},
        "current_step": {"id": "Step 4"},
    }

    options = module.analyze_recovery_options(interrupt_info)
    labels = [option.get("label") for option in options]
    assert "从当前步骤继续" in labels
    assert "清理中断状态并整段重跑" in labels


def test_detect_interruption_uses_loopback_artifact_fallback(tmp_path, monkeypatch):
    module = _load_module()
    monkeypatch.setattr(module, "find_project_root", lambda: tmp_path)
    _write_project_state(
        tmp_path,
        {
            "carryover_context": {"next_episode": "第11集", "next_volume": "第2卷"},
            "runtime_markers": {"loopback": {"last_actualized_volume": "第1卷"}},
        },
    )

    loopback_dir = tmp_path / "5-Loopback"
    loopback_dir.mkdir(parents=True, exist_ok=True)
    (loopback_dir / "第1卷.loopback.json").write_text(
        json.dumps(
            {
                "meta": {"loopback_ref": "5-Loopback/第1卷.loopback.json", "chapter_refs": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]},
                "inputs": {"validation_ref": "4-Validation/第1卷.validation.json"},
            },
            ensure_ascii=False,
            indent=2,
        ),
        encoding="utf-8",
    )

    interrupt = module.detect_interruption()

    assert interrupt is not None
    assert interrupt["detection_mode"] == "artifact_fallback"
    assert interrupt["command"] == "story-write"
    assert interrupt["args"]["chapter_num"] == 11
    assert interrupt["args"]["volume_num"] == 2
    assert interrupt["resume_reason"] == "loopback_completed_next_volume_ready"

    options = module.analyze_recovery_options(interrupt)
    assert any(option.get("label") == "开始第11集 drafting" for option in options)


def test_detect_interruption_uses_validation_review_artifact_fallback(tmp_path, monkeypatch):
    module = _load_module()
    monkeypatch.setattr(module, "find_project_root", lambda: tmp_path)
    _write_project_state(
        tmp_path,
        {
            "review_checkpoints": [
                {
                    "volume": 1,
                    "report": "4-Validation/第1卷审查报告.md",
                }
            ]
        },
    )

    validation_dir = tmp_path / "4-Validation"
    validation_dir.mkdir(parents=True, exist_ok=True)
    (validation_dir / "第1卷.validation.json").write_text(
        json.dumps(
            {
                "volume_ref": "第1卷",
                "chapter_refs": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
                "validation_status": "PASS",
                "routing_decision": "handoff_to_review_and_loopback",
                "handoff_targets": ["review/", "5-Loopback"],
            },
            ensure_ascii=False,
            indent=2,
        ),
        encoding="utf-8",
    )
    (validation_dir / "第1卷审查报告.md").write_text("# report\n", encoding="utf-8")

    interrupt = module.detect_interruption()

    assert interrupt is not None
    assert interrupt["detection_mode"] == "artifact_fallback"
    assert interrupt["command"] == "story-loopback"
    assert interrupt["args"]["volume_num"] == 1
    assert interrupt["resume_reason"] == "validation_pass_review_persisted_loopback_pending"


def test_detect_interruption_uses_writelog_artifact_fallback(tmp_path, monkeypatch):
    module = _load_module()
    monkeypatch.setattr(module, "find_project_root", lambda: tmp_path)
    _seed_project_root(tmp_path)

    drafting_dir = tmp_path / "3-Drafting"
    drafting_dir.mkdir(parents=True, exist_ok=True)
    (drafting_dir / "第1卷.写作日志.yaml").write_text(
        "\n".join(
            [
                "volume_num: 1",
                "chapter_refs:",
                "  - 1",
                "  - 2",
                "  - 3",
                "  - 4",
                "  - 5",
                "  - 6",
                "  - 7",
                "  - 8",
                "  - 9",
                "  - 10",
                "candidate_final_state:",
                "  status: candidate_volume_draft",
                "current_resume_pointer:",
                "  next_step: 4-Validation",
            ]
        )
        + "\n",
        encoding="utf-8",
    )

    interrupt = module.detect_interruption()

    assert interrupt is not None
    assert interrupt["detection_mode"] == "artifact_fallback"
    assert interrupt["command"] == "story-validate"
    assert interrupt["args"]["volume_num"] == 1
    assert interrupt["resume_reason"] == "candidate_volume_draft_waiting_validation"


def test_detect_interruption_prefers_newer_writelog_over_older_loopback(tmp_path, monkeypatch):
    module = _load_module()
    monkeypatch.setattr(module, "find_project_root", lambda: tmp_path)
    _seed_project_root(tmp_path)

    loopback_dir = tmp_path / "5-Loopback"
    loopback_dir.mkdir(parents=True, exist_ok=True)
    (loopback_dir / "第1卷.loopback.json").write_text("{}", encoding="utf-8")

    drafting_dir = tmp_path / "3-Drafting"
    drafting_dir.mkdir(parents=True, exist_ok=True)
    (drafting_dir / "第2卷.写作日志.yaml").write_text(
        "\n".join(
            [
                "volume_num: 2",
                "chapter_refs:",
                "  - 11",
                "  - 12",
                "  - 13",
                "  - 14",
                "  - 15",
                "  - 16",
                "  - 17",
                "  - 18",
                "  - 19",
                "  - 20",
                "candidate_final_state:",
                "  status: candidate_volume_draft",
                "current_resume_pointer:",
                "  next_step: 4-Validation",
            ]
        )
        + "\n",
        encoding="utf-8",
    )

    interrupt = module.detect_interruption()

    assert interrupt is not None
    assert interrupt["detection_mode"] == "artifact_fallback"
    assert interrupt["command"] == "story-validate"
    assert interrupt["args"]["volume_num"] == 2
    assert interrupt["resume_reason"] == "candidate_volume_draft_waiting_validation"
