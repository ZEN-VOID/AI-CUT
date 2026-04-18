#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import sys
from pathlib import Path

import pytest


def _ensure_scripts_on_path() -> None:
    scripts_dir = Path(__file__).resolve().parents[2]
    if str(scripts_dir) not in sys.path:
        sys.path.insert(0, str(scripts_dir))


def _load_loopback_module():
    _ensure_scripts_on_path()
    import loopback_manager as loopback_module

    return loopback_module


def _write_json(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")


def _build_project(project_root: Path) -> None:
    _write_json(
        project_root / "STATE.json",
        {
            "project_info": {"title": "凡人资本论"},
            "progress": {"current_chapter": 12, "total_words": 32000},
            "review_checkpoints": [],
        },
    )
    _write_json(
        project_root / "2-Planning" / "全息地图.json",
        {
            "schema_version": "story2026/holomap/v1",
            "content": {
                "holomap": {
                    "chapter_boards": [],
                    "actualization": {
                        "write_policy": "actualization-only",
                        "episode_nodes": [],
                        "clue_points": [],
                        "foreshadow_points": [],
                        "promise_threads": [],
                        "suspense_threads": [],
                        "tasklines": [],
                        "threads": [],
                    },
                }
            },
        },
    )
    _write_json(
        project_root / "1-Cards" / "2-角色卡" / "主要角色" / "林辰.json",
        {
            "core": {"name": "林辰"},
            "current_state": {"realm": "炼气", "stance": "中立"},
            "history": [],
        },
    )


def test_loopback_manager_blocks_non_pass_validation(tmp_path, monkeypatch):
    module = _load_loopback_module()
    project_root = (tmp_path / "book").resolve()
    _build_project(project_root)

    validation_path = project_root / ".webnovel" / "tmp" / "validation.json"
    _write_json(
        validation_path,
        {
            "validation_status": "FAIL-QUALITY",
            "routing_decision": "back_to_drafting_nodes",
            "handoff_targets": ["review/"],
            "card_deltas": [],
            "map_deltas": [],
            "projection_refresh": [],
            "evidence_refs": [],
        },
    )

    monkeypatch.setattr(
        sys,
        "argv",
        [
            "loopback_manager",
            "--project-root",
            str(project_root),
            "actualize",
            "--episode",
            "12",
            "--validation-data",
            f"@{validation_path}",
            "--manuscript-ref",
            "3-Drafting/第12集.md",
        ],
    )

    with pytest.raises(SystemExit) as exc:
        module.main()

    assert int(exc.value.code or 0) == 1
    assert not (project_root / "5-Loopback" / "第12集.loopback.json").exists()


def test_loopback_manager_blocks_pass_without_loopback_handoff(tmp_path, monkeypatch):
    module = _load_loopback_module()
    project_root = (tmp_path / "book").resolve()
    _build_project(project_root)

    validation_path = project_root / ".webnovel" / "tmp" / "validation.json"
    _write_json(
        validation_path,
        {
            "validation_status": "PASS",
            "routing_decision": "handoff_to_review_only",
            "handoff_targets": ["review/"],
            "validation_ref": "4-Validation/第12集.validation.json",
            "card_deltas": [],
            "map_deltas": [],
            "projection_refresh": [],
            "evidence_refs": [],
        },
    )

    monkeypatch.setattr(
        sys,
        "argv",
        [
            "loopback_manager",
            "--project-root",
            str(project_root),
            "actualize",
            "--episode",
            "12",
            "--validation-data",
            f"@{validation_path}",
            "--manuscript-ref",
            "3-Drafting/第12集.md",
        ],
    )

    with pytest.raises(SystemExit) as exc:
        module.main()

    assert int(exc.value.code or 0) == 1
    assert not (project_root / "5-Loopback" / "第12集.loopback.json").exists()


def test_loopback_manager_writes_artifact_and_applies_writebacks(tmp_path, monkeypatch):
    module = _load_loopback_module()
    project_root = (tmp_path / "book").resolve()
    _build_project(project_root)

    validation_path = project_root / ".webnovel" / "tmp" / "validation.json"
    _write_json(
        validation_path,
        {
            "validation_status": "PASS",
            "routing_decision": "handoff_to_review_and_loopback",
            "handoff_targets": ["review/", "5-Loopback"],
            "validation_ref": "4-Validation/第12集.validation.json",
            "governance_refs": {
                "validation_report_ref": "STATE.json#workflow_runtime.governance_index.run-12.validation_report",
                "artifact_manifest_ref": "STATE.json#workflow_runtime.governance_index.run-12.artifact_manifest",
                "mission_brief_ref": "STATE.json#workflow_runtime.governance_index.run-12.mission_brief",
            },
            "card_deltas": [
                {
                    "target_ref": "1-Cards/2-角色卡/主要角色/林辰.json",
                    "target_type": "character_card",
                    "current_state_patch": {
                        "realm": "筑基",
                        "stance": "结盟",
                    },
                    "history_append": {
                        "episode_ref": "第12集",
                        "validation_ref": "4-Validation/第12集.validation.json",
                        "changed_fields": ["realm", "stance"],
                        "change_summary": "林辰完成突破并转向结盟。",
                        "impact_scope": "cross-episode",
                        "evidence_refs": ["3-Drafting/第12集.md"],
                        "timestamp": "2026-04-06T10:00:00",
                    },
                }
            ],
            "map_deltas": [
                {
                    "target_bucket": "episode_nodes",
                    "target_ref": "episode-12",
                    "actualization_patch": {
                        "node_id": "node-12",
                        "episode_ref": "第12集",
                        "execution_status": "completed",
                        "validated_at": "2026-04-06T10:00:00",
                        "manuscript_ref": "3-Drafting/第12集.md",
                        "validation_ref": "4-Validation/第12集.validation.json",
                        "actual_outcome_summary": "本集完成破境并公开立场。",
                        "carry_forward_refs": ["1-Cards/2-角色卡/主要角色/林辰.json"],
                    },
                }
            ],
            "projection_refresh": [
                {
                    "target_type": "writer_projection",
                    "payload": {"focus": ["突破后余波", "宗门立场"]},
                },
                {
                    "target_type": "carryover_context",
                    "payload": {"next_episode": "第13集", "open_threads": ["宗门震荡"]},
                },
                {
                    "target_type": "runtime_marker",
                    "target_ref": "loopback",
                    "payload": {"last_actualized_episode": "第12集", "dirty": False},
                },
            ],
            "evidence_refs": [
                {"ref_type": "manuscript", "ref_path": "3-Drafting/第12集.md", "note": "正文真源"},
                {
                    "ref_type": "validation_packet",
                    "ref_path": "4-Validation/第12集.validation.json",
                    "note": "验证报告",
                },
            ],
        },
    )

    monkeypatch.setattr(
        sys,
        "argv",
        [
            "loopback_manager",
            "--project-root",
            str(project_root),
            "actualize",
            "--episode",
            "12",
            "--validation-data",
            f"@{validation_path}",
            "--manuscript-ref",
            "3-Drafting/第12集.md",
        ],
    )

    with pytest.raises(SystemExit) as exc:
        module.main()

    assert int(exc.value.code or 0) == 0

    artifact_path = project_root / "5-Loopback" / "第12集.loopback.json"
    assert artifact_path.is_file()

    artifact = json.loads(artifact_path.read_text(encoding="utf-8"))
    assert artifact["inputs"]["validation_status"] == "PASS"
    assert artifact["inputs"]["routing_decision"] == "handoff_to_review_and_loopback"
    assert artifact["inputs"]["handoff_targets"] == ["review/", "5-Loopback"]
    assert artifact["content"]["writeback_summary"]["written_card_refs"] == ["1-Cards/2-角色卡/主要角色/林辰.json"]
    assert artifact["content"]["writeback_summary"]["written_map_refs"] == ["episode_nodes:episode-12"]
    assert artifact["execution_notes"]["governance_refs"]["mission_brief_ref"] == (
        "STATE.json#workflow_runtime.governance_index.run-12.mission_brief"
    )

    card = json.loads((project_root / "1-Cards" / "2-角色卡" / "主要角色" / "林辰.json").read_text(encoding="utf-8"))
    assert card["current_state"]["realm"] == "筑基"
    assert card["current_state"]["stance"] == "结盟"
    assert card["history"][-1]["episode_ref"] == "第12集"
    assert card["history"][-1]["loopback_ref"] == "5-Loopback/第12集.loopback.json"

    holomap = json.loads(
        (project_root / "2-Planning" / "全息地图.json").read_text(encoding="utf-8")
    )
    actual_nodes = holomap["content"]["holomap"]["actualization"]["episode_nodes"]
    assert actual_nodes[0]["episode_ref"] == "第12集"
    assert actual_nodes[0]["execution_status"] == "completed"

    state = json.loads((project_root / "STATE.json").read_text(encoding="utf-8"))
    assert state["setting_route_packet"]["writer_context_projection"]["memory_projection"]["focus"] == [
        "突破后余波",
        "宗门立场",
    ]
    assert state["carryover_context"]["next_episode"] == "第13集"
    assert state["runtime_markers"]["loopback"]["last_actualized_episode"] == "第12集"
