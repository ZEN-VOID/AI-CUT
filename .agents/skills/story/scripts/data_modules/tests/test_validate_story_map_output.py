#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import sys
from pathlib import Path


def _ensure_scripts_on_path() -> None:
    scripts_dir = Path(__file__).resolve().parents[2]
    planning_scripts_dir = scripts_dir.parent / "2-Planning" / "scripts"
    for path in (scripts_dir, planning_scripts_dir):
        if str(path) not in sys.path:
            sys.path.insert(0, str(path))


def _write_split_story_map(tmp_path: Path, *, thin_contract: bool) -> Path:
    project_root = tmp_path / "story-project"
    planning_dir = project_root / "2-Planning"
    slice_dir = planning_dir / "卷分片"
    slice_dir.mkdir(parents=True, exist_ok=True)

    root_payload = {
        "schema_version": "story2026/story-map/v3",
        "meta": {
            "skill_id": "story-plan",
            "layout_mode": "total-index-plus-deciles",
        },
        "content": {
            "holomap": {
                "story_promise": {},
                "genre_corridor": {},
                "story_spine": {},
                "timeline_axis": [],
                "space_axis": [],
                "episode_sequence_axis": [
                    {
                        "episode_ref": "第1集",
                        "slice_ref": "slice-001-010",
                        "chapter_board_ref": "board-001",
                    }
                ],
                "episode_slice_manifest": [
                    {
                        "slice_id": "slice-001-010",
                        "episode_start": 1,
                        "episode_end": 10,
                        "file_ref": "卷分片/第1卷.json",
                    }
                ],
                "character_roster_projection": [],
                "relationship_graph_projection": {
                    "source_graph_path": "1-Cards/2-角色卡/角色关系图谱.md",
                    "scope": "full-series",
                    "node_refs": [],
                    "edge_projections": [],
                },
                "volume_boards": [
                    {
                        "volume_ref": "第1卷",
                        "chapter_range": "1-10",
                        "core_function": "主角组在异域立足并识别真正敌网。",
                        "volume_promise": "" if thin_contract else "异域压迫、关系绑缚与反击准备同时兑现。",
                        "wave_duty": "" if thin_contract else "promise",
                        "entry_promise": "" if thin_contract else "卷头先给外乡压迫与陌生规训。",
                        "exit_hook": "" if thin_contract else "卷尾把真正敌网与下一步反制欲望送出。",
                        "visual_climate": "" if thin_contract else ["海雾", "冷港", "潮湿木构"],
                        "action_grammar": "" if thin_contract else "以逼仄空间中的突然爆发推进。",
                        "mystery_mode": "" if thin_contract else "低位观察 + 局部揭露",
                        "emotional_temperature": "" if thin_contract else "冷压里带隐燃",
                        "scene_materials": [] if thin_contract else ["盐雾", "木栈桥", "潮湿纸灯"],
                        "performance_axis": "" if thin_contract else "克制试探中逐步结盟",
                        "taboo_writeups": [] if thin_contract else ["不要写成泛泛闯关", "不要写成无差别打斗"],
                    }
                ],
                "conflict_threads": [],
                "mission_threads": [],
                "clue_threads": [],
                "foreshadow_threads": [],
                "cross_thread_indexes": [{"thread_id": "t-1"}],
                "actualization": {},
                "state_transitions": [],
                "navigation_rules": [],
                "chapter_boards": [],
            }
        },
    }

    slice_payload = {
        "schema_version": "story2026/story-map-slice/v1",
        "content": {
            "holomap_slice": {
                "slice_scope": {
                    "slice_id": "slice-001-010",
                    "episode_start": 1,
                    "episode_end": 10,
                },
                "slice_style_contract": {
                    "contract_ref": "volume:第1卷",
                    "volume_ref": "第1卷",
                    "volume_promise": "" if thin_contract else "异域压迫与结盟 promise 同时在线。",
                    "wave_duty": "" if thin_contract else "promise",
                    "entry_promise": "" if thin_contract else "开篇先给陌生规训和压迫气味。",
                    "exit_hook": "" if thin_contract else "尾部把敌网真形推给下一章。",
                    "visual_climate": "" if thin_contract else "海雾冷港",
                    "action_grammar": "" if thin_contract else "短爆发 + 突停留白",
                    "mystery_mode": "" if thin_contract else "局部揭露",
                    "emotional_temperature": "" if thin_contract else "冷压",
                    "scene_materials": [] if thin_contract else ["海雾", "木栈桥"],
                    "performance_axis": "" if thin_contract else "彼此试探中的护短",
                    "taboo_writeups": [] if thin_contract else ["不要写平成通用冒险"],
                },
                "chapter_boards": [
                    {
                        "node_id": "board-001",
                        "episode_ref": "第1集",
                        "timeline_ref": "timeline-001",
                        "primary_space_ref": "space-001",
                        "active_space_refs": ["space-001"],
                        "bundled_elements": {
                            "events": ["主角组抵达港口"],
                            "conflicts": ["港规压迫"],
                            "missions": ["活过第一夜"],
                            "clues": ["账本缺口"],
                            "foreshadows": ["白鹤酒壶旧痕"],
                            "characters": ["令狐冲", "任盈盈"],
                            "scenes": ["海雾港町"],
                            "items": ["白鹤酒壶"],
                            "rule_impacts": ["外乡人触规会被整港盯上"],
                        },
                        "planned_state": {
                            "chapter_promise": "" if thin_contract else "落地即压迫，关系先试探。",
                            "entry_state": {} if thin_contract else {"emotion": "陌生警觉"},
                            "carryover_threads": [] if thin_contract else ["敌网未显", "两人互信未稳"],
                            "expected_exit_delta": {} if thin_contract else {"pressure_up": "地方恶压升级"},
                            "character_focus": {} if thin_contract else {"lead": "令狐冲"},
                            "relationship_focus": {} if thin_contract else {"edge_refs": ["linghu-ren"]},
                        },
                    }
                ],
                "episode_sequence_axis": [
                    {
                        "episode_ref": "第1集",
                        "chapter_board_ref": "board-001",
                        "slice_ref": "slice-001-010",
                    }
                ],
                "cross_chapter_continuity_matrix": [
                    {
                        "from_episode_ref": "第1集",
                        "to_episode_ref": "第2集",
                        "bridge_summary": "" if thin_contract else "从落地压迫接到第一次被迫出手。",
                        "carryover_threads": [] if thin_contract else ["敌网未显", "港规压迫"],
                        "expected_shift": "" if thin_contract else "从观察进入试探性反击。",
                    }
                ],
                "thread_window_slice": {},
                "foreshadow_silence_slice": {},
                "actualization": {},
            }
        },
    }

    root_path = planning_dir / "全息地图.json"
    slice_path = slice_dir / "第1卷.json"
    root_path.write_text(json.dumps(root_payload, ensure_ascii=False), encoding="utf-8")
    slice_path.write_text(json.dumps(slice_payload, ensure_ascii=False), encoding="utf-8")
    return root_path


def test_validate_story_map_output_strict_rejects_thin_volume_contract(tmp_path):
    _ensure_scripts_on_path()
    from validate_story_map_output import _validate

    root_path = _write_split_story_map(tmp_path, thin_contract=True)
    errors = _validate(root_path, strict=True)

    assert any("volume_boards[0].volume_promise 不得为空" in err for err in errors)
    assert any("slice_style_contract.volume_promise 不得为空" in err for err in errors)
    assert any("planned_state.chapter_promise 不得为空" in err for err in errors)
    assert any("cross_chapter_continuity_matrix[0].bridge_summary 不得为空" in err for err in errors)


def test_validate_story_map_output_strict_accepts_thick_volume_contract(tmp_path):
    _ensure_scripts_on_path()
    from validate_story_map_output import _validate

    root_path = _write_split_story_map(tmp_path, thin_contract=False)
    errors = _validate(root_path, strict=True)

    assert errors == []
