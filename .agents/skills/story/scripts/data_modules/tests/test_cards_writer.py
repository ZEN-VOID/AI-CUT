#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import sys
from pathlib import Path


def _load_modules():
    scripts_dir = Path(__file__).resolve().parents[2]
    if str(scripts_dir) not in sys.path:
        sys.path.insert(0, str(scripts_dir))

    import cards_coverage_validator
    import cards_writer

    return cards_writer, cards_coverage_validator


def _write_json(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")


def _make_project_root(tmp_path: Path) -> Path:
    project_root = tmp_path / "book"
    _write_json(
        project_root / ".webnovel" / "state.json",
        {
            "project_info": {
                "title": "测试书",
                "genre": "都市成长",
                "target_chapters": 10,
                "protagonist_structure": "单主角",
                "antagonist_tiers": "对手:赵竞",
            }
        },
    )
    _write_json(
        project_root / "Init" / "north_star_contract.json",
        {
            "project_identity": {
                "title": "测试书",
                "genre": "都市成长",
                "target_chapters": 10,
            },
            "reader_promise": {
                "hard_constraints": [],
                "primary_pleasures": ["现实压力下的成长"],
            },
            "cards": {
                "world_system": {
                    "worldview": {"genre": "都市成长"},
                    "rule_system": [],
                    "section_constraints": [],
                },
                "current_focus": {
                    "enforcement_focus": [],
                },
            },
            "story_kernel": {"core_conflict": "在债务与真相之间求生"},
        },
    )
    _write_json(
        project_root / "Init" / "初始化简报.json",
        {
            "cards_seed": {
                "character_seed": {
                    "protagonist": {"structure": "单主角"},
                    "relationship": {"antagonist_tiers": {"对手": "赵竞"}},
                }
            },
            "planning_seed": {
                "pacing_scale": {"target_chapters": 10, "protagonist_structure": "单主角"},
                "constraint_seed": {"hard_constraints": []},
            },
        },
    )
    return project_root


def _build_payload() -> dict:
    return {
        "mode": "full-build",
        "boundary_notes": ["cards-writer-test"],
        "sections": {
            "characters": {
                "relationship_edges": [
                    {"source": "林舟", "target": "周岚", "type": "ally"},
                    {"source": "林舟", "target": "赵竞", "type": "rival"},
                ],
                "current_focus": {
                    "confirmed_facts": ["主角、对手、支撑角色已确认"],
                    "inferred_defaults": [],
                    "active_pressures": ["债务"],
                },
                "cards": [
                    {
                        "bucket": "protagonists",
                        "file_name": "林舟.json",
                        "card": {
                            "core": {
                                "identity": {"name": "林舟"},
                                "narrative_function": ["承压主角"],
                                "relationship_ports": ["向周岚求援", "与赵竞对抗"],
                                "exclusive_item_hooks": ["旧怀表"],
                            },
                            "current_state": {
                                "status": "active",
                                "active_pressure": ["债务"],
                                "current_relationships": ["周岚", "赵竞"],
                                "current_resources": ["旧怀表"],
                                "timeline_anchor": {"experience_phase": "起步期"},
                            },
                            "experience_timeline": {
                                "time_model": "experience-centric",
                                "current_growth_stage": "被迫上路",
                                "growth_log": ["第一次为保护朋友撒谎"],
                            },
                            "history": [],
                        },
                    },
                    {
                        "bucket": "antagonists",
                        "file_name": "赵竞.json",
                        "card": {
                            "core": {
                                "identity": {"name": "赵竞"},
                                "narrative_function": ["现实对手"],
                                "relationship_ports": ["打压林舟"],
                                "exclusive_item_hooks": [],
                            },
                            "current_state": {
                                "status": "active",
                                "active_pressure": ["催债"],
                                "current_relationships": ["林舟"],
                                "current_resources": ["录音笔"],
                                "timeline_anchor": {"experience_phase": "施压期"},
                            },
                            "experience_timeline": {
                                "time_model": "experience-centric",
                                "current_growth_stage": "逼近真相",
                                "growth_log": ["决定把旧案当作筹码"],
                            },
                            "history": [],
                        },
                    },
                    {
                        "bucket": "supporting",
                        "file_name": "周岚.json",
                        "card": {
                            "core": {
                                "identity": {"name": "周岚"},
                                "narrative_function": ["情报支撑"],
                                "relationship_ports": ["替林舟查档案"],
                                "exclusive_item_hooks": [],
                            },
                            "current_state": {
                                "status": "active",
                                "active_pressure": ["夹在两边"],
                                "current_relationships": ["林舟"],
                                "current_resources": ["档案钥匙"],
                                "timeline_anchor": {"experience_phase": "介入期"},
                            },
                            "experience_timeline": {
                                "time_model": "experience-centric",
                                "current_growth_stage": "开始承担风险",
                                "growth_log": ["第一次替人伪造借阅记录"],
                            },
                            "history": [],
                        },
                    },
                ],
            },
            "scenes": {
                "scene_links": [
                    {"source": "旧公寓", "target": "天桥", "type": "escape"},
                    {"source": "天桥", "target": "档案室", "type": "clue"},
                ],
                "current_focus": {
                    "confirmed_facts": ["都市常驻场景已锁定"],
                    "inferred_defaults": [],
                    "repeat_use_strategy": ["旧公寓与档案室循环加压"],
                },
                "cards": [
                    {
                        "bucket": "indoor",
                        "file_name": "旧公寓.json",
                        "card": {
                            "core": {
                                "identity": {"name": "旧公寓"},
                                "narrative_functions": ["逼出选择"],
                                "rule_and_risk": {
                                    "scene_rules": ["凌晨后不能开灯"],
                                    "hazards": ["房东巡查"],
                                    "costs": ["暴露行踪"],
                                },
                                "compatible_roles": ["林舟"],
                            },
                            "current_state": {
                                "active_mood": ["逼仄"],
                                "repeat_use_status": "active",
                                "current_open_threads": ["房租告急"],
                            },
                            "history": [],
                        },
                        "content_patch": {
                            "current_focus": {
                                "repeat_use_strategy": ["每次返场都抬高债务压力"],
                            }
                        },
                    },
                    {
                        "bucket": "outdoor",
                        "file_name": "天桥.json",
                        "card": {
                            "core": {
                                "identity": {"name": "天桥"},
                                "narrative_functions": ["制造公开碰撞"],
                                "rule_and_risk": {
                                    "scene_rules": ["交易必须在人流最高时完成"],
                                    "hazards": ["被认出"],
                                    "costs": ["留下目击者"],
                                },
                                "compatible_roles": ["林舟", "赵竞"],
                            },
                            "current_state": {
                                "active_mood": ["暴露"],
                                "repeat_use_status": "active",
                                "current_open_threads": ["下一次交锋时间未定"],
                            },
                            "history": [],
                        },
                        "content_patch": {
                            "current_focus": {
                                "repeat_use_strategy": ["每次返场都升级公开风险"],
                            }
                        },
                    },
                    {
                        "bucket": "natural",
                        "file_name": "河堤.json",
                        "card": {
                            "core": {
                                "identity": {"name": "河堤"},
                                "narrative_functions": ["提供喘息和反思"],
                                "rule_and_risk": {
                                    "scene_rules": ["不能久留"],
                                    "hazards": ["被尾随"],
                                    "costs": ["错失时机"],
                                },
                                "compatible_roles": ["林舟", "周岚"],
                            },
                            "current_state": {
                                "active_mood": ["短暂平静"],
                                "repeat_use_status": "standby",
                                "current_open_threads": ["是否要交换真相"],
                            },
                            "history": [],
                        },
                        "content_patch": {
                            "current_focus": {
                                "repeat_use_strategy": ["只在情绪反转点使用"],
                            }
                        },
                    },
                    {
                        "bucket": "surreal",
                        "file_name": "档案室.json",
                        "card": {
                            "core": {
                                "identity": {"name": "档案室"},
                                "narrative_functions": ["承接真相剥离"],
                                "rule_and_risk": {
                                    "scene_rules": ["一次只能带走一份旧档"],
                                    "hazards": ["记录缺页"],
                                    "costs": ["触发旧案回响"],
                                },
                                "compatible_roles": ["林舟", "周岚"],
                            },
                            "current_state": {
                                "active_mood": ["压抑"],
                                "repeat_use_status": "active",
                                "current_open_threads": ["缺失档案的去向"],
                            },
                            "history": [],
                        },
                        "content_patch": {
                            "current_focus": {
                                "repeat_use_strategy": ["每次返场只多揭一层旧案"],
                            }
                        },
                    },
                ],
            },
            "items": {
                "ownership_links": [
                    {"item": "旧怀表", "owner": "林舟"},
                    {"item": "录音笔", "owner": "赵竞"},
                ],
                "exclusive_item_hooks": [
                    {"owner": "林舟", "item": "旧怀表"},
                ],
                "current_focus": {
                    "confirmed_facts": ["关键物链已锁定"],
                    "inferred_defaults": [],
                    "active_items": ["旧怀表", "录音笔"],
                    "locked_items": [],
                },
                "cards": [
                    {
                        "bucket": "weapons_equipment",
                        "file_name": "折叠刀.json",
                        "card": {
                            "core": {
                                "identity": {"name": "折叠刀", "owner_type": "character"},
                                "narrative_functions": ["提升现场危险"],
                                "usage_rules": {
                                    "activation": ["弹开刀刃"],
                                    "costs": ["留下痕迹"],
                                },
                                "exclusive_fit": {
                                    "preferred_owners": ["赵竞"],
                                    "style_match": ["凌厉"],
                                },
                            },
                            "current_state": {
                                "holder": "赵竞",
                                "condition": "完好",
                                "unlock_status": "active",
                                "active_plot_load": ["威胁升级"],
                            },
                            "history": [],
                        },
                    },
                    {
                        "bucket": "clue_items",
                        "file_name": "录音笔.json",
                        "card": {
                            "core": {
                                "identity": {"name": "录音笔", "owner_type": "character"},
                                "narrative_functions": ["固化证词"],
                                "usage_rules": {
                                    "activation": ["按下录音键"],
                                    "costs": ["留下可追踪音轨"],
                                },
                                "exclusive_fit": {
                                    "preferred_owners": ["赵竞"],
                                    "style_match": ["精确"],
                                },
                            },
                            "current_state": {
                                "holder": "赵竞",
                                "condition": "磨损",
                                "unlock_status": "active",
                                "active_plot_load": ["握有旧案录音"],
                            },
                            "history": [],
                        },
                    },
                    {
                        "bucket": "narrative_items",
                        "file_name": "旧怀表.json",
                        "card": {
                            "core": {
                                "identity": {"name": "旧怀表", "owner_type": "character"},
                                "narrative_functions": ["触发主线真相"],
                                "usage_rules": {
                                    "activation": ["逆时针拨动一格"],
                                    "costs": ["短暂记忆错位"],
                                },
                                "exclusive_fit": {
                                    "preferred_owners": ["林舟"],
                                    "style_match": ["克制"],
                                },
                            },
                            "current_state": {
                                "holder": "林舟",
                                "condition": "旧",
                                "unlock_status": "partial",
                                "active_plot_load": ["牵出父亲旧案"],
                            },
                            "history": [],
                        },
                    },
                    {
                        "bucket": "relics",
                        "file_name": "旧借阅证.json",
                        "card": {
                            "core": {
                                "identity": {"name": "旧借阅证", "owner_type": "institution"},
                                "narrative_functions": ["证明旧案关联"],
                                "usage_rules": {
                                    "activation": ["出示编号"],
                                    "costs": ["暴露查询意图"],
                                },
                                "exclusive_fit": {
                                    "preferred_owners": ["周岚"],
                                    "style_match": ["谨慎"],
                                },
                            },
                            "current_state": {
                                "holder": "周岚",
                                "condition": "脆化",
                                "unlock_status": "active",
                                "active_plot_load": ["打开档案室权限"],
                            },
                            "history": [],
                        },
                    },
                    {
                        "bucket": "adornments",
                        "file_name": "工牌.json",
                        "card": {
                            "core": {
                                "identity": {"name": "工牌", "owner_type": "character"},
                                "narrative_functions": ["帮助潜入日常空间"],
                                "usage_rules": {
                                    "activation": ["刷卡通行"],
                                    "costs": ["一旦挂失就失效"],
                                },
                                "exclusive_fit": {
                                    "preferred_owners": ["周岚"],
                                    "style_match": ["低调"],
                                },
                            },
                            "current_state": {
                                "holder": "周岚",
                                "condition": "正常",
                                "unlock_status": "active",
                                "active_plot_load": ["便于出入档案馆"],
                            },
                            "history": [],
                        },
                    },
                ],
            },
        },
    }


def test_cards_writer_writes_trace_fields_and_passes_gate(tmp_path):
    cards_writer, cards_coverage_validator = _load_modules()
    project_root = _make_project_root(tmp_path)

    report = cards_writer.write_cards_payload(project_root, _build_payload(), run_gate=True)

    assert report["ok"] is True
    assert report["mode"] == "full-build"

    protagonist_path = project_root / "Cards" / "2-角色卡" / "主要角色" / "林舟.json"
    protagonist = json.loads(protagonist_path.read_text(encoding="utf-8"))
    assert protagonist["content"]["module_route"] == "story-cards > references/character-card-module/module-spec.md"
    assert protagonist["content"]["loaded_references"] == [
        "references/README.md",
        "references/character-card-module/module-spec.md",
        "templates/character-card.json",
    ]
    assert protagonist["content"]["writeback_plan"]["mode"] == "full-build"
    assert protagonist["content"]["writeback_plan"]["target_paths"] == [
        "Cards/2-角色卡/主要角色/林舟.json",
        "Cards/2-角色卡/角色索引.json",
    ]

    character_index_path = project_root / "Cards" / "2-角色卡" / "角色索引.json"
    character_index = json.loads(character_index_path.read_text(encoding="utf-8"))
    assert character_index["content"]["module_route"] == "story-cards > references/character-card-module/module-spec.md"
    assert character_index["content"]["loaded_references"] == [
        "references/README.md",
        "references/character-card-module/module-spec.md",
        "templates/character-card.json",
    ]
    assert character_index["content"]["writeback_plan"]["target_paths"] == ["Cards/2-角色卡/角色索引.json"]
    assert character_index["gate_summary"]["status"] == "PASS"

    coverage_report = cards_coverage_validator.build_cards_coverage_report(project_root)
    assert coverage_report["ok"] is True
    assert coverage_report["sections"]["characters"]["trace"]["module_route"] == "story-cards > references/character-card-module/module-spec.md"
