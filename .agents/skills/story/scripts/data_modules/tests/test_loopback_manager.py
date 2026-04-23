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
    (project_root / "2-Planning").mkdir(parents=True, exist_ok=True)
    (project_root / "2-Planning" / "第2卷").mkdir(parents=True, exist_ok=True)
    (project_root / "2-Planning" / "整体规划.md").write_text(
        "书名：凡人资本论\n\n整体故事大纲：\n\n卷划分：\n\n整体节奏曲线：\n\n```mermaid\nflowchart TD\nA-->B\n```\n\n规避：\n",
        encoding="utf-8",
    )
    (project_root / "2-Planning" / "第2卷" / "卷规划.md").write_text(
        "卷标题：第二卷\n\n本卷故事大纲：\n\n章划分：\n\n本卷节奏曲线：\n\n```mermaid\nflowchart TD\nA-->B\n```\n\n本卷登场人物：\n\n本卷主要场景：\n\n本卷关键道具：\n\n本卷任务线\n- 主线：\n- 支线：\n\n卷末达成：\n\n规避：\n",
        encoding="utf-8",
    )
    (project_root / "2-Planning" / "第2卷" / "第12章.md").write_text(
        "章标题：第十二章\n\n本章故事概要：\n\n本章冲突：\n\n本章节奏曲线：\n- `selected_pack`：动静结合\n- `selected_mode`：势能式\n\n七步职责映射：\n- 入场：税线压迫先显影\n- 推动：林辰决定先看而不动\n- 转折：阿真被逼跪雨中\n- 发展：林辰试图压住怒意\n- 升级：税吏继续羞辱众人\n- 高潮：林辰第一次准备拔剑\n- 尾钩：真正代价被推到下一章\n\n规划义务：\n- `entry_promise`：开场先给压迫感与假安稳同时存在。\n- `conflict_axis`：林辰想忍，但税线恶压逼他表态，失败代价是心气与局面同时失守。\n- `micro_payoff`：林辰第一次真正做出要不要拔剑的决定。\n- `exit_hook`：拔剑冲动与更大代价被推向下一章。\n\n义务段位：\n- 必须兑现：前段压迫显影，中段矛盾升级，章末决意外露。\n- 可延后兑现：真正出手与后续代价。\n\n建议写法：\n- 开场处理：先给雨夜压迫，再落到人物观察。\n- 中段处理：让忍耐和怒意来回拉扯。\n- 章末处理：用未真正出手前的一步把压力送出。\n\n```mermaid\nflowchart TD\nA-->B\n```\n\n本章登场人物：\n\n本章主要场景：\n\n本章关键道具：\n\n本章任务线\n- 主线：\n- 支线：\n\n章末达成：\n\n本章线索：\n\n本章伏笔\n- 铺设：\n- 兑现：\n\n规避：\n",
        encoding="utf-8",
    )


def _build_project_with_slice(project_root: Path) -> None:
    _write_json(
        project_root / "2-Planning" / "全息地图.json",
        {
            "schema_version": "story2026/holomap/v1",
            "content": {
                "holomap": {
                    "episode_sequence_axis": [
                        {
                            "episode_ref": "第012章",
                            "slice_ref": "slice-011-020",
                            "chapter_board_ref": "ep-012",
                        }
                    ],
                    "episode_slice_manifest": [
                        {
                            "slice_id": "slice-011-020",
                            "file_ref": "卷分片/第2卷.json",
                        }
                    ],
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
                        "episode_status_index": [],
                        "slice_status_index": [],
                    },
                }
            },
        },
    )
    _write_json(
        project_root / "2-Planning" / "卷分片" / "第2卷.json",
        {
            "schema_version": "story2026/holomap-slice/v1",
            "content": {
                "holomap_slice": {
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


def _build_nested_cards_project(project_root: Path) -> None:
    _build_project(project_root)
    _write_json(
        project_root / "1-Cards" / "2-角色卡" / "主要角色" / "林辰.json",
        {
            "content": {
                "card_schema": {
                    "character_card": {
                        "core": {"identity": {"name": "林辰"}},
                        "current_state": {"realm": "炼气", "stance": "中立"},
                        "history": [],
                    }
                }
            }
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
            "3-Drafting/第2卷/第12章.md",
        ],
    )

    with pytest.raises(SystemExit) as exc:
        module.main()

    assert int(exc.value.code or 0) == 1
    assert not (project_root / "5-Loopback" / "第2卷.loopback.json").exists()


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
            "handoff_targets": ["review/", "5-Loopback"],
            "validation_ref": "4-Validation/第12章.validation.json",
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
            "3-Drafting/第2卷/第12章.md",
        ],
    )

    with pytest.raises(SystemExit) as exc:
        module.main()

    assert int(exc.value.code or 0) == 1
    assert not (project_root / "5-Loopback" / "第2卷.loopback.json").exists()


def test_loopback_manager_blocks_empty_actualization_delta(tmp_path, monkeypatch):
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
            "validation_ref": "4-Validation/第12章.validation.json",
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
            "3-Drafting/第2卷/第12章.md",
        ],
    )

    with pytest.raises(SystemExit) as exc:
        module.main()

    assert int(exc.value.code or 0) == 1
    assert not (project_root / "5-Loopback" / "第2卷.loopback.json").exists()


def test_loopback_manager_applies_projection_refresh_modes(tmp_path, monkeypatch):
    module = _load_loopback_module()
    project_root = (tmp_path / "book").resolve()
    _build_project(project_root)

    state_path = project_root / "STATE.json"
    state = json.loads(state_path.read_text(encoding="utf-8"))
    state["setting_route_packet"] = {
        "writer_context_projection": {
            "memory_projection": {
                "existing": ["keep"],
                "nested": {"old": "value"},
            }
        }
    }
    state["carryover_context"] = {"open_threads": ["旧线索"]}
    _write_json(state_path, state)

    validation_path = project_root / ".webnovel" / "tmp" / "validation.json"
    _write_json(
        validation_path,
        {
            "validation_status": "PASS",
            "routing_decision": "handoff_to_review_and_loopback",
            "handoff_targets": ["review/", "5-Loopback"],
            "validation_ref": "4-Validation/第12章.validation.json",
            "card_deltas": [],
            "map_deltas": [],
            "projection_refresh": [
                {
                    "target_type": "writer_projection",
                    "refresh_mode": "merge",
                    "payload": {
                        "nested": {"new": "value"},
                        "new_focus": ["突破后余波"],
                    },
                },
                {
                    "target_type": "carryover_context",
                    "target_ref": "open_threads",
                    "refresh_mode": "append",
                    "payload": ["新支线"],
                },
            ],
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
            "3-Drafting/第2卷/第12章.md",
        ],
    )

    with pytest.raises(SystemExit) as exc:
        module.main()

    assert int(exc.value.code or 0) == 0
    state = json.loads(state_path.read_text(encoding="utf-8"))
    writer_projection = state["setting_route_packet"]["writer_context_projection"]["memory_projection"]
    assert writer_projection["existing"] == ["keep"]
    assert writer_projection["nested"] == {"old": "value", "new": "value"}
    assert writer_projection["new_focus"] == ["突破后余波"]
    assert state["carryover_context"]["open_threads"] == ["旧线索", "新支线"]
    assert state["runtime_markers"]["loopback_state_revision"] == 1


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
            "validation_ref": "4-Validation/第12章.validation.json",
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
                        "growth_state": {
                            "active_arc_phase": "破局初成",
                            "latest_growth_episode": "第12章",
                            "skill": {"stage": "稳固", "recent_gain": "学会在破境后压住手上余劲"},
                        },
                    },
                    "history_append": {
                        "episode_ref": "第12章",
                        "validation_ref": "4-Validation/第12章.validation.json",
                        "changed_fields": ["realm", "stance"],
                        "change_summary": "林辰完成突破并转向结盟。",
                        "impact_scope": "cross-episode",
                        "evidence_refs": ["3-Drafting/第2卷/第12章.md"],
                        "timestamp": "2026-04-06T10:00:00",
                        "growth_delta": {
                            "skill": {"before": "莽冲", "after": "稳固"},
                            "heart": {},
                            "emotion": {},
                        },
                    },
                }
            ],
            "map_deltas": [
                {
                    "target_bucket": "episode_nodes",
                    "target_ref": "episode-12",
                    "actualization_patch": {
                        "node_id": "node-12",
                        "episode_ref": "第12章",
                        "execution_status": "completed",
                        "validated_at": "2026-04-06T10:00:00",
                        "manuscript_ref": "3-Drafting/第2卷/第12章.md",
                        "validation_ref": "4-Validation/第12章.validation.json",
                        "actual_outcome_summary": "本章完成破境并公开立场。",
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
                    "payload": {"next_episode": "第13章", "open_threads": ["宗门震荡"]},
                },
                {
                    "target_type": "runtime_marker",
                    "target_ref": "loopback",
                    "payload": {"last_actualized_episode": "第12章", "dirty": False},
                },
            ],
            "evidence_refs": [
                {"ref_type": "manuscript", "ref_path": "3-Drafting/第2卷/第12章.md", "note": "正文真源"},
                {
                    "ref_type": "validation_packet",
                    "ref_path": "4-Validation/第12章.validation.json",
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
            "3-Drafting/第2卷/第12章.md",
        ],
    )

    with pytest.raises(SystemExit) as exc:
        module.main()

    assert int(exc.value.code or 0) == 0

    artifact_path = project_root / "5-Loopback" / "第2卷.loopback.json"
    assert artifact_path.is_file()

    artifact = json.loads(artifact_path.read_text(encoding="utf-8"))
    assert artifact["inputs"]["validation_status"] == "PASS"
    assert artifact["inputs"]["routing_decision"] == "handoff_to_review_and_loopback"
    assert artifact["inputs"]["handoff_targets"] == ["review/", "5-Loopback"]
    assert artifact["inputs"]["book_plan_ref"] == "2-Planning/整体规划.md"
    assert artifact["inputs"]["volume_plan_ref"] == "2-Planning/第2卷/卷规划.md"
    assert artifact["inputs"]["chapter_plan_refs"] == ["2-Planning/第2卷/第12章.md"]
    assert artifact["content"]["writeback_summary"]["written_card_refs"] == ["1-Cards/2-角色卡/主要角色/林辰.json"]
    assert artifact["content"]["writeback_summary"]["written_planning_actualization_refs"] == [
        "2-Planning/整体规划.actualization.json",
        "2-Planning/第2卷/卷规划.actualization.json",
        "2-Planning/第2卷/第12章.actualization.json",
    ]
    assert artifact["content"]["writeback_summary"]["written_map_refs"] == ["episode_nodes:episode-12"]
    assert artifact["execution_notes"]["governance_refs"]["mission_brief_ref"] == (
        "STATE.json#workflow_runtime.governance_index.run-12.mission_brief"
    )
    assert artifact["execution_notes"]["commit_manifest"]["phase"] == "committed"
    assert artifact["execution_notes"]["commit_manifest"]["next_revisions"]["cards"] == {
        "1-Cards/2-角色卡/主要角色/林辰.json": 1
    }

    card = json.loads((project_root / "1-Cards" / "2-角色卡" / "主要角色" / "林辰.json").read_text(encoding="utf-8"))
    assert card["current_state"]["realm"] == "筑基"
    assert card["current_state"]["stance"] == "结盟"
    assert card["current_state"]["growth_state"]["skill"]["stage"] == "稳固"
    assert card["history"][-1]["episode_ref"] == "第12章"
    assert card["history"][-1]["loopback_ref"] == "5-Loopback/第2卷.loopback.json"
    assert card["history"][-1]["growth_delta"]["skill"]["after"] == "稳固"
    assert card["loopback_revision"] == 1

    holomap = json.loads(
        (project_root / "2-Planning" / "全息地图.json").read_text(encoding="utf-8")
    )
    actual_nodes = holomap["content"]["holomap"]["actualization"]["episode_nodes"]
    assert actual_nodes[0]["episode_ref"] == "第12章"
    assert actual_nodes[0]["execution_status"] == "completed"
    assert holomap["content"]["holomap"]["actualization"]["revision"] == 1

    book_actualization = json.loads(
        (project_root / "2-Planning" / "整体规划.actualization.json").read_text(encoding="utf-8")
    )
    assert book_actualization["volume_status_index"][0]["volume_ref"] == "第2卷"
    assert book_actualization["volume_status_index"][0]["last_actualized_chapter_ref"] == "第12章"

    volume_actualization = json.loads(
        (project_root / "2-Planning" / "第2卷" / "卷规划.actualization.json").read_text(encoding="utf-8")
    )
    assert volume_actualization["volume_ref"] == "第2卷"
    assert volume_actualization["chapter_status_index"][0]["chapter_ref"] == "第12章"

    chapter_actualization = json.loads(
        (project_root / "2-Planning" / "第2卷" / "第12章.actualization.json").read_text(encoding="utf-8")
    )
    assert chapter_actualization["chapter_ref"] == "第12章"
    assert chapter_actualization["status"] == "completed"

    state = json.loads((project_root / "STATE.json").read_text(encoding="utf-8"))
    assert state["setting_route_packet"]["writer_context_projection"]["memory_projection"]["focus"] == [
        "突破后余波",
        "宗门立场",
    ]
    assert state["carryover_context"]["next_episode"] == "第13章"
    assert state["runtime_markers"]["loopback"]["last_actualized_episode"] == "第12章"
    assert state["runtime_markers"]["loopback"]["last_commit_manifest"]["phase"] == "committed"
    assert state["runtime_markers"]["loopback_state_revision"] == 1


def test_loopback_manager_writes_slice_actualization_and_root_indexes(tmp_path, monkeypatch):
    module = _load_loopback_module()
    project_root = (tmp_path / "book").resolve()
    _build_project(project_root)
    _build_project_with_slice(project_root)

    validation_path = project_root / ".webnovel" / "tmp" / "validation.json"
    _write_json(
        validation_path,
        {
            "validation_status": "PASS",
            "routing_decision": "handoff_to_review_and_loopback",
            "handoff_targets": ["review/", "5-Loopback"],
            "validation_ref": "4-Validation/第12章.validation.json",
            "card_deltas": [],
            "map_deltas": [
                {
                    "target_bucket": "episode_nodes",
                    "target_ref": "episode-12",
                    "slice_ref": "slice-011-020",
                    "actualization_patch": {
                        "node_id": "ep-012",
                        "episode_ref": "第012章",
                        "execution_status": "completed",
                        "actual_outcome_summary": "本章完成 validated actualization。",
                    },
                }
            ],
            "projection_refresh": [
                {
                    "target_type": "carryover_context",
                    "payload": {"next_episode": "第013章"},
                }
            ],
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
            "3-Drafting/第2卷/第12章.md",
        ],
    )

    with pytest.raises(SystemExit) as exc:
        module.main()

    assert int(exc.value.code or 0) == 0

    artifact = json.loads((project_root / "5-Loopback" / "第2卷.loopback.json").read_text(encoding="utf-8"))
    assert artifact["inputs"]["story_map_slice_ref"] == "2-Planning/卷分片/第2卷.json"
    assert artifact["inputs"]["volume_plan_ref"] == "2-Planning/第2卷/卷规划.md"
    assert artifact["content"]["writeback_summary"]["written_map_slice_refs"] == ["episode_nodes:episode-12"]
    assert "2-Planning/第2卷/第12章.actualization.json" in artifact["content"]["writeback_summary"]["written_planning_actualization_refs"]
    assert "episode_status_index:第012章" in artifact["content"]["writeback_summary"]["written_map_refs"]
    assert "slice_status_index:slice-011-020" in artifact["content"]["writeback_summary"]["written_map_refs"]

    slice_payload = json.loads(
        (project_root / "2-Planning" / "卷分片" / "第2卷.json").read_text(encoding="utf-8")
    )
    slice_nodes = slice_payload["content"]["holomap_slice"]["actualization"]["episode_nodes"]
    assert slice_nodes[0]["episode_ref"] == "第012章"
    assert slice_payload["content"]["holomap_slice"]["actualization"]["revision"] == 1

    holomap = json.loads((project_root / "2-Planning" / "全息地图.json").read_text(encoding="utf-8"))
    status_index = holomap["content"]["holomap"]["actualization"]["episode_status_index"]
    slice_index = holomap["content"]["holomap"]["actualization"]["slice_status_index"]
    assert status_index[0]["episode_ref"] == "第012章"
    assert status_index[0]["status"] == "completed"
    assert slice_index[0]["slice_id"] == "slice-011-020"
    assert slice_index[0]["status"] == "completed"


def test_loopback_manager_rolls_back_on_commit_failure(tmp_path, monkeypatch):
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
            "validation_ref": "4-Validation/第12章.validation.json",
            "card_deltas": [
                {
                    "target_ref": "1-Cards/2-角色卡/主要角色/林辰.json",
                    "target_type": "character_card",
                    "current_state_patch": {"realm": "筑基"},
                    "history_append": {"episode_ref": "第12章"},
                }
            ],
            "map_deltas": [
                {
                    "target_bucket": "episode_nodes",
                    "target_ref": "episode-12",
                    "actualization_patch": {
                        "episode_ref": "第12章",
                        "execution_status": "completed",
                    },
                }
            ],
            "projection_refresh": [
                {
                    "target_type": "runtime_marker",
                    "target_ref": "loopback",
                    "payload": {"last_actualized_episode": "第12章"},
                }
            ],
            "evidence_refs": [],
        },
    )

    original_atomic_write_json = module.atomic_write_json

    def flaky_atomic_write_json(path, payload, use_lock=True, backup=True):
        path_obj = Path(path)
        if path_obj.name == "第2卷.loopback.json":
            raise OSError("simulated artifact write failure")
        return original_atomic_write_json(path_obj, payload, use_lock=use_lock, backup=backup)

    monkeypatch.setattr(module, "atomic_write_json", flaky_atomic_write_json)
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
            "3-Drafting/第2卷/第12章.md",
        ],
    )

    with pytest.raises(OSError, match="simulated artifact write failure"):
        module.main()

    card = json.loads((project_root / "1-Cards" / "2-角色卡" / "主要角色" / "林辰.json").read_text(encoding="utf-8"))
    assert card["current_state"]["realm"] == "炼气"
    assert card["history"] == []

    holomap = json.loads((project_root / "2-Planning" / "全息地图.json").read_text(encoding="utf-8"))
    assert holomap["content"]["holomap"]["actualization"]["episode_nodes"] == []

    state = json.loads((project_root / "STATE.json").read_text(encoding="utf-8"))
    assert "runtime_markers" not in state
    assert not (project_root / "5-Loopback" / "第2卷.loopback.json").exists()


def test_loopback_manager_writes_nested_card_schema_state(tmp_path, monkeypatch):
    module = _load_loopback_module()
    project_root = (tmp_path / "book").resolve()
    _build_nested_cards_project(project_root)

    validation_path = project_root / ".webnovel" / "tmp" / "validation.json"
    _write_json(
        validation_path,
        {
            "validation_status": "PASS",
            "routing_decision": "handoff_to_review_and_loopback",
            "handoff_targets": ["review/", "5-Loopback"],
            "validation_ref": "4-Validation/第12章.validation.json",
            "card_deltas": [
                {
                    "target_ref": "1-Cards/2-角色卡/主要角色/林辰.json",
                    "target_type": "character_card",
                    "current_state_patch": {
                        "realm": "筑基",
                        "stance": "结盟",
                    },
                    "history_append": {
                        "episode_ref": "第12章",
                        "validation_ref": "4-Validation/第12章.validation.json",
                        "changed_fields": ["realm", "stance"],
                        "change_summary": "林辰完成突破并转向结盟。",
                        "impact_scope": "cross-episode",
                        "evidence_refs": ["3-Drafting/第2卷/第12章.md"],
                        "timestamp": "2026-04-06T10:00:00",
                    },
                }
            ],
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
            "3-Drafting/第2卷/第12章.md",
        ],
    )

    with pytest.raises(SystemExit) as exc:
        module.main()

    assert int(exc.value.code or 0) == 0

    card = json.loads((project_root / "1-Cards" / "2-角色卡" / "主要角色" / "林辰.json").read_text(encoding="utf-8"))
    nested = card["content"]["card_schema"]["character_card"]
    assert nested["current_state"]["realm"] == "筑基"
    assert nested["current_state"]["stance"] == "结盟"
    assert nested["history"][-1]["episode_ref"] == "第12章"
    assert nested["loopback_revision"] == 1
    assert "current_state" not in card
    assert "history" not in card


def test_loopback_manager_rejects_revision_drift(tmp_path, monkeypatch):
    module = _load_loopback_module()
    project_root = (tmp_path / "book").resolve()
    _build_project(project_root)

    card_path = project_root / "1-Cards" / "2-角色卡" / "主要角色" / "林辰.json"
    card = json.loads(card_path.read_text(encoding="utf-8"))
    card["loopback_revision"] = 3
    _write_json(card_path, card)

    validation_path = project_root / ".webnovel" / "tmp" / "validation.json"
    _write_json(
        validation_path,
        {
            "validation_status": "PASS",
            "routing_decision": "handoff_to_review_and_loopback",
            "handoff_targets": ["review/", "5-Loopback"],
            "validation_ref": "4-Validation/第12章.validation.json",
            "card_deltas": [
                {
                    "target_ref": "1-Cards/2-角色卡/主要角色/林辰.json",
                    "target_type": "character_card",
                    "expected_revision": 2,
                    "current_state_patch": {"realm": "筑基"},
                }
            ],
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
            "3-Drafting/第2卷/第12章.md",
        ],
    )

    with pytest.raises(ValueError, match="revision 已漂移"):
        module.main()


def test_loopback_manager_rejects_non_whitelisted_delta_fields(tmp_path, monkeypatch):
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
            "validation_ref": "4-Validation/第12章.validation.json",
            "card_deltas": [
                {
                    "target_ref": "1-Cards/2-角色卡/主要角色/林辰.json",
                    "target_type": "character_card",
                    "current_state_patch": {
                        "realm": "筑基",
                        "core": {"identity": {"name": "越权"}},
                    },
                }
            ],
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
            "3-Drafting/第2卷/第12章.md",
        ],
    )

    with pytest.raises(ValueError, match="越权字段"):
        module.main()
