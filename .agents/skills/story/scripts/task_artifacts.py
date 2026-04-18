#!/usr/bin/env python3
"""Shadow governance task artifact helpers for story2026 runs."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path
from typing import Any, Optional

from security_utils import atomic_write_json, create_secure_directory


TASK_DIR_REL = Path(".webnovel") / "tasks"

TASK_FILES = {
    "mandate_ref": "mandate.yaml",
    "mission_brief_ref": "mission_brief.yaml",
    "route_plan_ref": "route_plan.yaml",
    "preflight_verdict_ref": "preflight_verdict.yaml",
    "artifact_manifest_ref": "artifact_manifest.json",
    "validation_report_ref": "validation_report.md",
    "learning_record_ref": "learning_record.md",
    "root_cause_trace_ref": "root_cause_trace.md",
}


def now_iso() -> str:
    return datetime.now().isoformat()


def story_task_dir(project_root: Path, run_id: str) -> Path:
    return project_root / TASK_DIR_REL / run_id


def story_task_refs(project_root: Path, run_id: str) -> dict[str, str]:
    task_dir = story_task_dir(project_root, run_id)
    return {
        "task_dir_ref": str(task_dir.relative_to(project_root)),
        **{
            key: str((task_dir / filename).relative_to(project_root))
            for key, filename in TASK_FILES.items()
        },
    }


def _write_yaml_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def _write_markdown(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content.rstrip() + "\n", encoding="utf-8")


def _load_json(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))


def _seed_artifact_manifest(*, task_id: str, refs: dict[str, str], status: str, generated_at: str) -> dict[str, Any]:
    return {
        "task_id": task_id,
        "status": status,
        "generated_at": generated_at,
        "updated_at": generated_at,
        "artifacts": refs,
        "step_artifacts": {},
    }


def bootstrap_story_task_artifacts(
    *,
    project_root: Path,
    run_id: str,
    command: str,
    stage_id: str,
    stage_label: str,
    args: dict[str, Any],
    route_steps: list[tuple[str, str, str]],
) -> dict[str, str]:
    task_dir = story_task_dir(project_root, run_id)
    create_secure_directory(str(task_dir))
    generated_at = now_iso()
    refs = story_task_refs(project_root, run_id)
    chapter_num = args.get("chapter_num")

    mandate_path = project_root / refs["mandate_ref"]
    if not mandate_path.exists():
        _write_yaml_json(
            mandate_path,
            {
                "task_id": run_id,
                "task_type": "story2026-stage-run",
                "objective": f"以 shadow governance 模式执行 {command}",
                "requested_by": "story2026/workflow_manager.py",
                "command": command,
                "stage_id": stage_id,
                "stage_label": stage_label,
                "risk_level": "high" if command in {"story-init", "story-write", "story-validate", "story-review"} else "medium",
                "generated_at": generated_at,
                "source_refs": [
                    "AGENTS.md",
                    ".codex/schemas/mandate.schema.json",
                    ".codex/registry/routes.yaml",
                ],
            },
        )

    mission_path = project_root / refs["mission_brief_ref"]
    if not mission_path.exists():
        summary = f"{command} run {run_id} 将继续沿用现有 .webnovel 状态主链，并额外写三省工件增强证据层。"
        if chapter_num is not None:
            summary = f"{summary} 当前章节: {chapter_num}。"
        _write_yaml_json(
            mission_path,
            {
                "task_id": run_id,
                "command": command,
                "stage_id": stage_id,
                "stage_label": stage_label,
                "generated_at": generated_at,
                "summary": summary,
                "args": args,
                "success_criteria": [
                    "旧 .webnovel 状态文件继续可读",
                    "本次 run 生成三省 shadow 工件",
                    "任务完成后 artifact manifest 与 validation report 可追溯",
                ],
                "acceptance_checks": [
                    "workflow_state.json / execution_state.json 仍保持兼容",
                    "任务目录至少包含 mandate / mission_brief / preflight / artifact_manifest",
                    "任务完成后生成 validation_report.md 与 learning_record.md",
                ],
                "source_refs": [
                    ".codex/schemas/mission-brief.schema.json",
                    ".codex/runbooks/preflight.md",
                    ".codex/runbooks/closure.md",
                ],
            },
        )

    route_path = project_root / refs["route_plan_ref"]
    if not route_path.exists():
        _write_yaml_json(
            route_path,
            {
                "task_id": run_id,
                "generated_at": generated_at,
                "planning_office": "planning-office",
                "execution_office": "execution-office",
                "review_office": "review-office",
                "steps": [
                    {
                        "step_id": step_id,
                        "step_name": step_name,
                        "owner": owner,
                        "parallelizable": False,
                    }
                    for step_id, step_name, owner in route_steps
                ],
            },
        )

    preflight_path = project_root / refs["preflight_verdict_ref"]
    if not preflight_path.exists():
        _write_yaml_json(
            preflight_path,
            {
                "task_id": run_id,
                "generated_at": generated_at,
                "status": "shadow-pass",
                "mode": "shadow",
                "can_execute": True,
                "reviewer": "review-office",
                "checks": [
                    {
                        "name": "legacy_state_chain_preserved",
                        "status": "pass",
                        "detail": "workflow_state.json / execution_state.json / task_log.jsonl 继续作为旧主链保留。",
                    },
                    {
                        "name": "shadow_artifacts_enabled",
                        "status": "pass",
                        "detail": "本次 run 将旁路写入三省工件，不替代旧状态真源。",
                    },
                ],
                "notes": [
                    "第一阶段只做 shadow 接入。",
                    "任何失败闭环仍需回写 root_cause_trace.md。",
                ],
            },
        )

    manifest_path = project_root / refs["artifact_manifest_ref"]
    if not manifest_path.exists():
        atomic_write_json(
            manifest_path,
            _seed_artifact_manifest(task_id=run_id, refs=refs, status="running", generated_at=generated_at),
            use_lock=True,
            backup=False,
        )

    return refs


def record_story_step_artifacts(
    *,
    project_root: Path,
    run_id: str,
    step_id: str,
    step_name: str,
    artifacts: Optional[dict[str, Any]],
) -> None:
    refs = story_task_refs(project_root, run_id)
    manifest_path = project_root / refs["artifact_manifest_ref"]
    manifest = _load_json(manifest_path) or _seed_artifact_manifest(
        task_id=run_id,
        refs=refs,
        status="running",
        generated_at=now_iso(),
    )
    manifest["updated_at"] = now_iso()
    manifest["step_artifacts"][step_id] = {
        "step_name": step_name,
        "artifacts": artifacts or {},
        "updated_at": manifest["updated_at"],
    }
    atomic_write_json(manifest_path, manifest, use_lock=True, backup=False)


def finalize_story_task_artifacts(
    *,
    project_root: Path,
    run_id: str,
    command: str,
    status: str,
    completed_steps: list[dict[str, Any]],
    failed_steps: list[dict[str, Any]],
    final_artifacts: Optional[dict[str, Any]] = None,
    failure_reason: str = "",
) -> dict[str, str]:
    refs = story_task_refs(project_root, run_id)
    now = now_iso()

    manifest_path = project_root / refs["artifact_manifest_ref"]
    manifest = _load_json(manifest_path) or _seed_artifact_manifest(
        task_id=run_id,
        refs=refs,
        status=status,
        generated_at=now,
    )
    manifest["status"] = status
    manifest["updated_at"] = now
    if final_artifacts:
        manifest["artifacts"]["final_artifacts"] = final_artifacts
    manifest["artifacts"]["completed_steps"] = [row.get("id") for row in completed_steps]
    manifest["artifacts"]["failed_steps"] = [row.get("id") for row in failed_steps]
    atomic_write_json(manifest_path, manifest, use_lock=True, backup=False)

    validation_path = project_root / refs["validation_report_ref"]
    overall_status = "shadow-pass" if status == "completed" else "fail" if status == "failed" else "shadow-pass"
    findings = []
    if failure_reason:
        findings.append(f"失败原因: {failure_reason}")
    findings.append(f"completed_steps={len(completed_steps)}")
    findings.append(f"failed_steps={len(failed_steps)}")
    validation_md = "\n".join(
        [
            "# Validation Report",
            "",
            f"- task_id: `{run_id}`",
            f"- command: `{command}`",
            f"- overall_status: `{overall_status}`",
            f"- generated_at: `{now}`",
            "",
            "## Summary",
            "",
            "本次任务以 shadow governance 模式回填了治理工件。",
            "",
            "## Findings",
            "",
            *[f"- {item}" for item in findings],
        ]
    )
    _write_markdown(validation_path, validation_md)

    learning_path = project_root / refs["learning_record_ref"]
    heuristic = (
        "复杂任务第一阶段优先旁路写治理工件，先保留旧状态真源，再逐步切换主链消费。"
        if status == "completed"
        else "失败任务必须把 root cause、即时修复和制度预防写成可追溯工件。"
    )
    learning_md = "\n".join(
        [
            "# Learning Record",
            "",
            f"- task_id: `{run_id}`",
            f"- outcome_type: `{'success' if status == 'completed' else 'failure'}`",
            f"- generated_at: `{now}`",
            f"- promotion_scope: `story2026/runtime-governance`",
            "",
            "## Summary",
            "",
            heuristic,
        ]
    )
    _write_markdown(learning_path, learning_md)

    if status == "failed":
        root_cause_path = project_root / refs["root_cause_trace_ref"]
        trace_md = "\n".join(
            [
                "# Root Cause Trace",
                "",
                f"- task_id: `{run_id}`",
                f"- generated_at: `{now}`",
                "",
                "## Layered Trace",
                "",
                f"- Symptom: `{command}` run failed",
                f"- Direct Technical Cause: {failure_reason or 'manual_fail'}",
                "- Rule Source: `.agents/skills/story/scripts/workflow_manager.py`",
                "- Meta Rule Source: `AGENTS.md` root-cause governance + `.codex/runbooks/closure.md`",
                "",
                "## Closure Triad",
                "",
                "- Immediate fix: 保留旧状态链并写出 failure evidence。",
                "- Systemic prevention fix: 将失败闭环沉到共享任务工件，不再只留在会话上下文。",
            ]
        )
        _write_markdown(root_cause_path, trace_md)

    return refs
