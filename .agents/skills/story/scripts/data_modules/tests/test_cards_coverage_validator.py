#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import sys
from pathlib import Path

import yaml


def _load_module():
    scripts_dir = Path(__file__).resolve().parents[2]
    if str(scripts_dir) not in sys.path:
        sys.path.insert(0, str(scripts_dir))
    import cards_coverage_validator

    return cards_coverage_validator


def _write_json(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")


def _write_yaml(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(yaml.safe_dump(payload, allow_unicode=True, sort_keys=False), encoding="utf-8")


def _touch_card(project_root: Path, rel_path: str) -> None:
    path = project_root / rel_path
    name = Path(rel_path).stem
    if "1-风格卡" in rel_path:
        payload = {
            "schema_version": "story2026/cards/style/v1",
            "meta": {
                "skill_id": "story-cards",
                "source_skill_id": "story-cards-style",
                "source_route": "0-Init > story-cards > 风格卡/SKILL.md",
            },
            "content": {
                **_trace_payload("story-cards > 风格卡/SKILL.md", "Cards/1-风格卡"),
                "card_schema": {
                    "style_card": {
                        "card_id": name,
                        "card_type": "style",
                        "group": "global_style",
                        "core": {
                            "identity": {"name": name, "scope": "full-series"},
                            "reader_promise": {
                                "primary_pleasures": ["规则压迫"],
                                "anti_trope": "不用爽文碾压",
                                "hard_constraints": ["必须守规则"],
                                "no_fly_zones": ["鸡汤式总结"],
                            },
                            "aesthetic_axes": {
                                "tone": "冷峻",
                                "violence_texture": "粗砺",
                                "mystery_density": "高",
                                "romance_policy": "克制",
                            },
                            "style_system": {
                                "text_style": {"tone": "冷峻", "genre_corridor": "规则怪谈", "anti_trope": "不用爽文碾压"},
                                "narrative_style": {"opening_hook": "规则先压人", "mystery_density": "高", "romance_policy": "克制"},
                                "tone_promises": ["规则压迫"],
                                "taboo_styles": ["鸡汤式总结"],
                                "downstream_constraints": ["必须守规则"],
                            },
                            "style_gate": {
                                "anti_ai_required": True,
                                "no_poison_required": True,
                                "style_contract_ref": f"Cards/1-风格卡/总风格/{name}.json",
                            },
                        },
                        "current_state": {
                            "active_focus": ["规则压迫"],
                            "downstream_targets": ["Drafting", "Validation"],
                            "revision_policy": "north_star 变动才刷新",
                        },
                        "history": [],
                    }
                },
                "style_contract_refs": [
                    {"card_id": name, "path": f"Cards/1-风格卡/总风格/{name}.json"}
                ],
                "current_focus": {"confirmed_facts": [name]},
            },
            "gate_summary": {"status": "PASS", "fail_codes": [], "repair_entry": ""},
        }
    elif "2-角色卡" in rel_path:
        payload = {
            "schema_version": "story2026/cards/character/v2",
            "meta": {
                "skill_id": "story-cards",
                "source_skill_id": "story-cards-character",
                "source_route": "0-Init > story-cards > 角色卡/SKILL.md",
            },
            "content": {
                **_trace_payload("story-cards > 角色卡/SKILL.md", "Cards/2-角色卡"),
                "card_schema": {
                    "character_card": {
                        "card_id": name,
                        "card_type": "character",
                        "group": "protagonist",
                        "core": {
                            "identity": {"name": name},
                            "narrative_function": ["承载主线压力"],
                            "relationship_ports": ["同盟"],
                            "exclusive_item_hooks": ["角色专属物"],
                        },
                        "current_state": {
                            "status": "active",
                            "timeline_anchor": {"experience_phase": "起势期"},
                        },
                        "experience_timeline": {
                            "time_model": "experience-centric",
                            "current_growth_stage": "初期",
                            "growth_log": ["第一次失手"],
                        },
                        "history": [],
                    }
                },
                "current_focus": {"confirmed_facts": [name]},
            },
            "gate_summary": {"status": "PASS", "fail_codes": [], "repair_entry": ""},
        }
    elif "3-场景卡" in rel_path:
        payload = {
            "schema_version": "story2026/cards/scene/v2",
            "meta": {
                "skill_id": "story-cards",
                "source_skill_id": "story-cards-scene",
                "source_route": "0-Init > story-cards > 场景卡/SKILL.md",
            },
            "content": {
                **_trace_payload("story-cards > 场景卡/SKILL.md", "Cards/3-场景卡"),
                "card_schema": {
                    "scene_card": {
                        "card_id": name,
                        "card_type": "scene",
                        "group": "indoor",
                        "core": {
                            "identity": {"name": name},
                            "narrative_functions": ["承接冲突"],
                            "rule_and_risk": {"scene_rules": ["必须留下痕迹"], "hazards": ["误判"], "costs": ["暴露"]},
                            "compatible_roles": ["主角"],
                        },
                        "current_state": {"active_mood": ["压迫"]},
                        "history": [],
                    }
                },
                "current_focus": {"repeat_use_strategy": ["多次返场"]},
            },
            "gate_summary": {"status": "PASS", "fail_codes": [], "repair_entry": ""},
        }
    else:
        payload = {
            "schema_version": "story2026/cards/item/v2",
            "meta": {
                "skill_id": "story-cards",
                "source_skill_id": "story-cards-item",
                "source_route": "0-Init > story-cards > 物品卡/SKILL.md",
            },
            "content": {
                **_trace_payload("story-cards > 物品卡/SKILL.md", "Cards/4-物品卡"),
                "card_schema": {
                    "item_card": {
                        "card_id": name,
                        "card_type": "item",
                        "group": "weapons_equipment",
                        "core": {
                            "identity": {"name": name, "owner_type": "character"},
                            "narrative_functions": ["推动剧情"],
                            "usage_rules": {"activation": ["持有即可"], "costs": ["失控风险"]},
                            "exclusive_fit": {"preferred_owners": ["主角"], "style_match": ["冷硬"]},
                        },
                        "current_state": {"holder": "甲"},
                        "history": [],
                    }
                }
            },
            "gate_summary": {"status": "PASS", "fail_codes": [], "repair_entry": ""},
        }
    _write_json(path, payload)


def _trace_payload(module_route: str, target_path: str) -> dict:
    template_name = {
        "story-cards > 风格卡/SKILL.md": "风格卡/templates/style-card.json",
        "story-cards > 角色卡/SKILL.md": "角色卡/templates/character-card.json",
        "story-cards > 场景卡/SKILL.md": "场景卡/templates/scene-card.json",
        "story-cards > 物品卡/SKILL.md": "物品卡/templates/item-card.json",
    }[module_route]
    child_path = module_route.split(" > ")[-1]
    child_dir = str(Path(child_path).parent)
    return {
        "module_route": module_route,
        "loaded_references": [
            "SKILL.md",
            "CONTEXT.md",
            child_path,
            f"{child_dir}/CONTEXT.md",
            template_name,
        ],
        "writeback_plan": {
            "mode": "full-build",
            "target_paths": [target_path],
            "upstream_patch_required": False,
            "boundary_notes": ["tests"],
        },
    }


def _make_project_root(tmp_path: Path) -> Path:
    project_root = tmp_path / "book"
    _write_json(
        project_root / "STATE.json",
        {
            "project_info": {
                "title": "测试书",
                "genre": "武侠+规则怪谈",
                "target_chapters": 30,
                "protagonist_structure": "双主角",
                "antagonist_tiers": "小反派:甲;中反派:乙;大反派:丙",
                "core_selling_points": "海路追杀、规则空间、残意真相",
                "world_scale": "跨海江湖与港町",
                "power_system_type": "中原武学与异域武道对撞",
            }
        },
    )
    return project_root


def _write_upstream_truth(project_root: Path, *, genre: str = "规则怪谈", target_chapters: int = 30, hard_constraints=None) -> None:
    if hard_constraints is None:
        hard_constraints = ["必须遵守旧港规则", "每次破局都要付出代价"]
    _write_yaml(
        project_root / "0-Init" / "north_star.yaml",
        {
            "project_identity": {
                "genre": genre,
                "target_chapters": target_chapters,
            },
            "reader_promise": {
                "hard_constraints": hard_constraints,
                "primary_pleasures": ["规则压迫"],
                "anti_trope": "不用爽文碾压",
                "no_fly_zones": ["鸡汤式总结"],
            },
            "aesthetic_axes": {
                "tone": "冷峻",
                "violence_texture": "粗砺",
                "mystery_density": "高",
                "romance_policy": "克制",
            },
            "cards": {
                "style_system": {
                    "text_style": {"tone": "冷峻", "genre_corridor": genre, "anti_trope": "不用爽文碾压"},
                    "narrative_style": {"opening_hook": "规则先压人", "mystery_density": "高", "romance_policy": "克制"},
                    "tone_promises": ["规则压迫"],
                    "taboo_styles": ["鸡汤式总结"],
                    "downstream_constraints": hard_constraints,
                },
                "world_system": {
                    "worldview": {"genre": genre},
                    "rule_system": [{"label": "旧港规则", "value": "夜里不能直呼真名"}],
                    "section_constraints": ["必须守规则"],
                },
                "current_focus": {
                    "enforcement_focus": ["规则优先"],
                },
            },
            "story_kernel": {"core_conflict": "在规则内求生"},
            "cards_seed": {
                "character_seed": {
                    "protagonist": {"structure": "双主角"},
                    "relationship": {"antagonist_tiers": {"小反派": "甲", "大反派": "乙"}},
                }
            },
        },
    )
    _write_yaml(
        project_root / "0-Init" / "init_handoff.yaml",
        {
            "stage_entry_seeds": {
                "cards_seed": {
                    "character_seed": {
                        "protagonist": {"structure": "双主角"},
                        "relationship": {"antagonist_tiers": {"小反派": "甲", "大反派": "乙"}},
                    }
                },
                "planning_seed": {
                    "pacing_scale": {"target_chapters": target_chapters, "protagonist_structure": "双主角"},
                    "constraint_seed": {"hard_constraints": hard_constraints},
                },
            }
        },
    )


def test_cards_coverage_report_passes_for_series_scale_project(tmp_path):
    module = _load_module()
    project_root = _make_project_root(tmp_path)
    _write_upstream_truth(project_root)

    for rel_path in (
        "Cards/1-风格卡/总风格/整书风格卡.json",
        "Cards/2-角色卡/主要角色/甲.json",
        "Cards/2-角色卡/主要角色/乙.json",
        "Cards/2-角色卡/反派角色/丙.json",
        "Cards/2-角色卡/反派角色/丁.json",
        "Cards/2-角色卡/反派角色/戊.json",
        "Cards/2-角色卡/次要角色/己.json",
        "Cards/2-角色卡/次要角色/庚.json",
        "Cards/2-角色卡/群像角色/辛.json",
        "Cards/3-场景卡/室内/酒肆.json",
        "Cards/3-场景卡/室外/港町.json",
        "Cards/3-场景卡/自然/海岛.json",
        "Cards/3-场景卡/自然/断崖.json",
        "Cards/3-场景卡/超现实/镜庭.json",
        "Cards/3-场景卡/超现实/残意海.json",
        "Cards/4-物品卡/武器装备/佩剑.json",
        "Cards/4-物品卡/武器装备/短刀.json",
        "Cards/4-物品卡/线索物品/密账.json",
        "Cards/4-物品卡/线索物品/海图.json",
        "Cards/4-物品卡/重要叙事物品/残篇.json",
        "Cards/4-物品卡/重要叙事物品/铃牌.json",
        "Cards/4-物品卡/文物/旧袍.json",
        "Cards/4-物品卡/点缀物/酒壶.json",
    ):
        _touch_card(project_root, rel_path)

    _write_json(
        project_root / "Cards" / "1-风格卡" / "风格索引.json",
        {
            "content": {
                **_trace_payload(
                    "story-cards > 风格卡/SKILL.md",
                    "Cards/1-风格卡",
                ),
                "card_groups": {
                    "global_styles": ["Cards/1-风格卡/总风格/整书风格卡.json"],
                },
                "style_contract_refs": [
                    {"card_id": "整书风格卡", "path": "Cards/1-风格卡/总风格/整书风格卡.json"}
                ],
                "current_focus": {"confirmed_facts": ["整书风格契约已锁定"]},
            }
        },
    )
    _write_json(
        project_root / "Cards" / "2-角色卡" / "角色索引.json",
        {
            "content": {
                **_trace_payload(
                    "story-cards > 角色卡/SKILL.md",
                    "Cards/2-角色卡",
                ),
                "card_groups": {
                    "protagonists": [
                        "Cards/2-角色卡/主要角色/甲.json",
                        "Cards/2-角色卡/主要角色/乙.json",
                    ],
                    "antagonists": [
                        "Cards/2-角色卡/反派角色/丙.json",
                        "Cards/2-角色卡/反派角色/丁.json",
                        "Cards/2-角色卡/反派角色/戊.json",
                    ],
                    "supporting": [
                        "Cards/2-角色卡/次要角色/己.json",
                        "Cards/2-角色卡/次要角色/庚.json",
                    ],
                    "ensemble": ["Cards/2-角色卡/群像角色/辛.json"],
                },
                "relationship_edges": [{"ok": 1}, {"ok": 2}, {"ok": 3}, {"ok": 4}],
                "current_focus": {"confirmed_facts": ["双主角成立"]},
            }
        },
    )
    _write_json(
        project_root / "Cards" / "3-场景卡" / "场景索引.json",
        {
            "content": {
                **_trace_payload(
                    "story-cards > 场景卡/SKILL.md",
                    "Cards/3-场景卡",
                ),
                "card_groups": {
                    "indoor": ["Cards/3-场景卡/室内/酒肆.json"],
                    "outdoor": ["Cards/3-场景卡/室外/港町.json"],
                    "natural": [
                        "Cards/3-场景卡/自然/海岛.json",
                        "Cards/3-场景卡/自然/断崖.json",
                    ],
                    "surreal": [
                        "Cards/3-场景卡/超现实/镜庭.json",
                        "Cards/3-场景卡/超现实/残意海.json",
                    ],
                },
                "scene_links": [{"ok": 1}, {"ok": 2}, {"ok": 3}, {"ok": 4}],
            }
        },
    )
    _write_json(
        project_root / "Cards" / "4-物品卡" / "物品索引.json",
        {
            "content": {
                **_trace_payload(
                    "story-cards > 物品卡/SKILL.md",
                    "Cards/4-物品卡",
                ),
                "card_groups": {
                    "weapons_equipment": [
                        "Cards/4-物品卡/武器装备/佩剑.json",
                        "Cards/4-物品卡/武器装备/短刀.json",
                    ],
                    "clue_items": [
                        "Cards/4-物品卡/线索物品/密账.json",
                        "Cards/4-物品卡/线索物品/海图.json",
                    ],
                    "narrative_items": [
                        "Cards/4-物品卡/重要叙事物品/残篇.json",
                        "Cards/4-物品卡/重要叙事物品/铃牌.json",
                    ],
                    "relics": ["Cards/4-物品卡/文物/旧袍.json"],
                    "adornments": ["Cards/4-物品卡/点缀物/酒壶.json"],
                },
                "ownership_links": [{"ok": 1}, {"ok": 2}, {"ok": 3}, {"ok": 4}],
                "exclusive_item_hooks": [{"owner": "甲"}, {"owner": "乙"}],
            }
        },
    )

    report = module.build_cards_coverage_report(project_root)

    assert report["ok"] is True
    assert report["sections"]["styles"]["total_count"] == 1
    assert report["sections"]["characters"]["counts"]["protagonists"] == 2
    assert report["sections"]["scenes"]["total_count"] == 6
    assert report["sections"]["items"]["total_count"] == 8
    assert report["sections"]["characters"]["trace"]["module_route"] == "story-cards > 角色卡/SKILL.md"


def test_cards_coverage_report_fails_when_series_cards_are_too_thin(tmp_path):
    module = _load_module()
    project_root = _make_project_root(tmp_path)
    _write_upstream_truth(project_root)

    for rel_path in (
        "Cards/1-风格卡/总风格/整书风格卡.json",
        "Cards/2-角色卡/主要角色/甲.json",
        "Cards/2-角色卡/反派角色/丙.json",
        "Cards/3-场景卡/室内/酒肆.json",
        "Cards/4-物品卡/武器装备/佩剑.json",
    ):
        _touch_card(project_root, rel_path)

    _write_json(
        project_root / "Cards" / "1-风格卡" / "风格索引.json",
        {
            "content": {
                **_trace_payload(
                    "story-cards > 风格卡/SKILL.md",
                    "Cards/1-风格卡",
                ),
                "card_groups": {
                    "global_styles": ["Cards/1-风格卡/总风格/整书风格卡.json"],
                },
                "style_contract_refs": [
                    {"card_id": "整书风格卡", "path": "Cards/1-风格卡/总风格/整书风格卡.json"}
                ],
                "current_focus": {"confirmed_facts": ["风格契约已锁定"]},
            }
        },
    )
    _write_json(
        project_root / "Cards" / "2-角色卡" / "角色索引.json",
        {
            "content": {
                **_trace_payload(
                    "story-cards > 角色卡/SKILL.md",
                    "Cards/2-角色卡",
                ),
                "card_groups": {
                    "protagonists": ["Cards/2-角色卡/主要角色/甲.json"],
                    "antagonists": ["Cards/2-角色卡/反派角色/丙.json"],
                    "supporting": [],
                    "ensemble": [],
                },
                "relationship_edges": [{"ok": 1}],
                "current_focus": {"confirmed_facts": ["过薄"]},
            }
        },
    )
    _write_json(
        project_root / "Cards" / "3-场景卡" / "场景索引.json",
        {
            "content": {
                **_trace_payload(
                    "story-cards > 场景卡/SKILL.md",
                    "Cards/3-场景卡",
                ),
                "card_groups": {
                    "indoor": ["Cards/3-场景卡/室内/酒肆.json"],
                    "outdoor": [],
                    "natural": [],
                    "surreal": [],
                },
                "scene_links": [{"ok": 1}],
            }
        },
    )
    _write_json(
        project_root / "Cards" / "4-物品卡" / "物品索引.json",
        {
            "content": {
                **_trace_payload(
                    "story-cards > 物品卡/SKILL.md",
                    "Cards/4-物品卡",
                ),
                "card_groups": {
                    "weapons_equipment": ["Cards/4-物品卡/武器装备/佩剑.json"],
                    "clue_items": [],
                    "narrative_items": [],
                    "relics": [],
                    "adornments": [],
                },
                "ownership_links": [{"ok": 1}],
                "exclusive_item_hooks": [],
            }
        },
    )

    report = module.build_cards_coverage_report(project_root)

    assert report["ok"] is False
    codes = {item["code"] for item in report["blocking_findings"]}
    assert "FAIL-CARDS-CHAR-PROTAG" in codes
    assert "FAIL-CARDS-CHAR-ANTAG" in codes
    assert "FAIL-CARDS-SCENE-OUTDOOR" in codes
    assert "FAIL-CARDS-ITEM-HOOKS" in codes


def test_cards_coverage_report_fails_when_trace_fields_are_missing(tmp_path):
    module = _load_module()
    project_root = _make_project_root(tmp_path)
    _write_upstream_truth(project_root)

    for rel_path in (
        "Cards/1-风格卡/总风格/整书风格卡.json",
        "Cards/2-角色卡/主要角色/甲.json",
        "Cards/2-角色卡/主要角色/乙.json",
        "Cards/2-角色卡/反派角色/丙.json",
        "Cards/2-角色卡/反派角色/丁.json",
        "Cards/2-角色卡/反派角色/戊.json",
        "Cards/2-角色卡/次要角色/己.json",
        "Cards/2-角色卡/次要角色/庚.json",
        "Cards/2-角色卡/群像角色/辛.json",
        "Cards/3-场景卡/室内/酒肆.json",
        "Cards/3-场景卡/室外/港町.json",
        "Cards/3-场景卡/自然/海岛.json",
        "Cards/3-场景卡/自然/断崖.json",
        "Cards/3-场景卡/超现实/镜庭.json",
        "Cards/3-场景卡/超现实/残意海.json",
        "Cards/4-物品卡/武器装备/佩剑.json",
        "Cards/4-物品卡/武器装备/短刀.json",
        "Cards/4-物品卡/线索物品/密账.json",
        "Cards/4-物品卡/线索物品/海图.json",
        "Cards/4-物品卡/重要叙事物品/残篇.json",
        "Cards/4-物品卡/重要叙事物品/铃牌.json",
        "Cards/4-物品卡/文物/旧袍.json",
        "Cards/4-物品卡/点缀物/酒壶.json",
    ):
        _touch_card(project_root, rel_path)

    _write_json(
        project_root / "Cards" / "1-风格卡" / "风格索引.json",
        {
            "content": {
                "card_groups": {
                    "global_styles": ["Cards/1-风格卡/总风格/整书风格卡.json"],
                },
                "style_contract_refs": [{"card_id": "整书风格卡", "path": "Cards/1-风格卡/总风格/整书风格卡.json"}],
                "current_focus": {"confirmed_facts": ["风格契约已锁定"]},
            }
        },
    )
    _write_json(
        project_root / "Cards" / "2-角色卡" / "角色索引.json",
        {
            "content": {
                "card_groups": {
                    "protagonists": [
                        "Cards/2-角色卡/主要角色/甲.json",
                        "Cards/2-角色卡/主要角色/乙.json",
                    ],
                    "antagonists": [
                        "Cards/2-角色卡/反派角色/丙.json",
                        "Cards/2-角色卡/反派角色/丁.json",
                        "Cards/2-角色卡/反派角色/戊.json",
                    ],
                    "supporting": [
                        "Cards/2-角色卡/次要角色/己.json",
                        "Cards/2-角色卡/次要角色/庚.json",
                    ],
                    "ensemble": ["Cards/2-角色卡/群像角色/辛.json"],
                },
                "relationship_edges": [{"ok": 1}, {"ok": 2}, {"ok": 3}, {"ok": 4}],
                "current_focus": {"confirmed_facts": ["双主角成立"]},
            }
        },
    )
    _write_json(
        project_root / "Cards" / "3-场景卡" / "场景索引.json",
        {
            "content": {
                "card_groups": {
                    "indoor": ["Cards/3-场景卡/室内/酒肆.json"],
                    "outdoor": ["Cards/3-场景卡/室外/港町.json"],
                    "natural": [
                        "Cards/3-场景卡/自然/海岛.json",
                        "Cards/3-场景卡/自然/断崖.json",
                    ],
                    "surreal": [
                        "Cards/3-场景卡/超现实/镜庭.json",
                        "Cards/3-场景卡/超现实/残意海.json",
                    ],
                },
                "scene_links": [{"ok": 1}, {"ok": 2}, {"ok": 3}],
            }
        },
    )
    _write_json(
        project_root / "Cards" / "4-物品卡" / "物品索引.json",
        {
            "content": {
                "card_groups": {
                    "weapons_equipment": [
                        "Cards/4-物品卡/武器装备/佩剑.json",
                        "Cards/4-物品卡/武器装备/短刀.json",
                    ],
                    "clue_items": [
                        "Cards/4-物品卡/线索物品/密账.json",
                        "Cards/4-物品卡/线索物品/海图.json",
                    ],
                    "narrative_items": [
                        "Cards/4-物品卡/重要叙事物品/残篇.json",
                        "Cards/4-物品卡/重要叙事物品/铃牌.json",
                    ],
                    "relics": ["Cards/4-物品卡/文物/旧袍.json"],
                    "adornments": ["Cards/4-物品卡/点缀物/酒壶.json"],
                },
                "ownership_links": [{"ok": 1}, {"ok": 2}, {"ok": 3}],
                "exclusive_item_hooks": [{"owner": "甲"}, {"owner": "乙"}],
            }
        },
    )

    report = module.build_cards_coverage_report(project_root)

    assert report["ok"] is False
    codes = {item["code"] for item in report["blocking_findings"]}
    assert "FAIL-CARDS-STYLE-ROUTE" in codes
    assert "FAIL-CARDS-STYLE-TRACE" in codes
    assert "FAIL-CARDS-STYLE-WRITEBACK" in codes
    assert "FAIL-CARDS-CHAR-ROUTE" in codes
    assert "FAIL-CARDS-CHAR-TRACE" in codes
    assert "FAIL-CARDS-CHAR-WRITEBACK" in codes
    assert "FAIL-CARDS-SCENE-ROUTE" in codes
    assert "FAIL-CARDS-ITEM-WRITEBACK" in codes


def test_cards_coverage_report_fails_when_card_files_are_shell_payloads(tmp_path):
    module = _load_module()
    project_root = _make_project_root(tmp_path)
    _write_upstream_truth(project_root)

    for rel_path in (
        "Cards/1-风格卡/总风格/整书风格卡.json",
        "Cards/2-角色卡/主要角色/甲.json",
        "Cards/2-角色卡/主要角色/乙.json",
        "Cards/2-角色卡/反派角色/丙.json",
        "Cards/2-角色卡/反派角色/丁.json",
        "Cards/2-角色卡/反派角色/戊.json",
        "Cards/2-角色卡/次要角色/己.json",
        "Cards/2-角色卡/次要角色/庚.json",
        "Cards/2-角色卡/群像角色/辛.json",
        "Cards/3-场景卡/室内/酒肆.json",
        "Cards/3-场景卡/室外/港町.json",
        "Cards/3-场景卡/自然/海岛.json",
        "Cards/3-场景卡/自然/断崖.json",
        "Cards/3-场景卡/超现实/镜庭.json",
        "Cards/3-场景卡/超现实/残意海.json",
        "Cards/4-物品卡/武器装备/佩剑.json",
        "Cards/4-物品卡/武器装备/短刀.json",
        "Cards/4-物品卡/线索物品/密账.json",
        "Cards/4-物品卡/线索物品/海图.json",
        "Cards/4-物品卡/重要叙事物品/残篇.json",
        "Cards/4-物品卡/重要叙事物品/铃牌.json",
        "Cards/4-物品卡/文物/旧袍.json",
        "Cards/4-物品卡/点缀物/酒壶.json",
    ):
        _write_json(project_root / rel_path, {"ok": True})

    _write_json(
        project_root / "Cards" / "1-风格卡" / "风格索引.json",
        {
            "content": {
                **_trace_payload(
                    "story-cards > 风格卡/SKILL.md",
                    "Cards/1-风格卡",
                ),
                "card_groups": {
                    "global_styles": ["Cards/1-风格卡/总风格/整书风格卡.json"],
                },
                "style_contract_refs": [{"card_id": "整书风格卡", "path": "Cards/1-风格卡/总风格/整书风格卡.json"}],
                "current_focus": {"confirmed_facts": ["风格契约已锁定"]},
            }
        },
    )
    _write_json(
        project_root / "Cards" / "2-角色卡" / "角色索引.json",
        {
            "content": {
                **_trace_payload(
                    "story-cards > 角色卡/SKILL.md",
                    "Cards/2-角色卡",
                ),
                "card_groups": {
                    "protagonists": [
                        "Cards/2-角色卡/主要角色/甲.json",
                        "Cards/2-角色卡/主要角色/乙.json",
                    ],
                    "antagonists": [
                        "Cards/2-角色卡/反派角色/丙.json",
                        "Cards/2-角色卡/反派角色/丁.json",
                        "Cards/2-角色卡/反派角色/戊.json",
                    ],
                    "supporting": [
                        "Cards/2-角色卡/次要角色/己.json",
                        "Cards/2-角色卡/次要角色/庚.json",
                    ],
                    "ensemble": ["Cards/2-角色卡/群像角色/辛.json"],
                },
                "relationship_edges": [{"ok": 1}, {"ok": 2}, {"ok": 3}, {"ok": 4}],
                "current_focus": {"confirmed_facts": ["双主角成立"]},
            }
        },
    )
    _write_json(
        project_root / "Cards" / "3-场景卡" / "场景索引.json",
        {
            "content": {
                **_trace_payload(
                    "story-cards > 场景卡/SKILL.md",
                    "Cards/3-场景卡",
                ),
                "card_groups": {
                    "indoor": ["Cards/3-场景卡/室内/酒肆.json"],
                    "outdoor": ["Cards/3-场景卡/室外/港町.json"],
                    "natural": [
                        "Cards/3-场景卡/自然/海岛.json",
                        "Cards/3-场景卡/自然/断崖.json",
                    ],
                    "surreal": [
                        "Cards/3-场景卡/超现实/镜庭.json",
                        "Cards/3-场景卡/超现实/残意海.json",
                    ],
                },
                "scene_links": [{"ok": 1}, {"ok": 2}, {"ok": 3}, {"ok": 4}],
            }
        },
    )
    _write_json(
        project_root / "Cards" / "4-物品卡" / "物品索引.json",
        {
            "content": {
                **_trace_payload(
                    "story-cards > 物品卡/SKILL.md",
                    "Cards/4-物品卡",
                ),
                "card_groups": {
                    "weapons_equipment": [
                        "Cards/4-物品卡/武器装备/佩剑.json",
                        "Cards/4-物品卡/武器装备/短刀.json",
                    ],
                    "clue_items": [
                        "Cards/4-物品卡/线索物品/密账.json",
                        "Cards/4-物品卡/线索物品/海图.json",
                    ],
                    "narrative_items": [
                        "Cards/4-物品卡/重要叙事物品/残篇.json",
                        "Cards/4-物品卡/重要叙事物品/铃牌.json",
                    ],
                    "relics": ["Cards/4-物品卡/文物/旧袍.json"],
                    "adornments": ["Cards/4-物品卡/点缀物/酒壶.json"],
                },
                "ownership_links": [{"ok": 1}, {"ok": 2}, {"ok": 3}, {"ok": 4}],
                "exclusive_item_hooks": [{"owner": "甲"}, {"owner": "乙"}],
            }
        },
    )

    report = module.build_cards_coverage_report(project_root)

    assert report["ok"] is False
    codes = {item["code"] for item in report["blocking_findings"]}
    assert "FAIL-CARDS-STYLE-CARD-SCHEMA" in codes or "FAIL-CARDS-STYLE-CARD-TRACE" in codes
    assert "FAIL-CARDS-CHARACTER-CARD-SCHEMA" in codes or "FAIL-CARDS-CHAR-CARD-SCHEMA" in codes
    assert "FAIL-CARDS-SCENE-CARD-SCHEMA" in codes
    assert "FAIL-CARDS-ITEM-CARD-SCHEMA" in codes


def test_cards_coverage_report_uses_north_star_truth_for_rule_rigidity(tmp_path):
    module = _load_module()
    project_root = _make_project_root(tmp_path)
    _write_json(
        project_root / "STATE.json",
        {
            "project_info": {
                "title": "测试书",
                "genre": "现实题材",
                "target_chapters": 12,
                "protagonist_structure": "双主角",
                "antagonist_tiers": "",
                "core_selling_points": "港区生存",
                "world_scale": "港区",
                "power_system_type": "",
            }
        },
    )
    _write_upstream_truth(project_root, genre="现实题材", target_chapters=12, hard_constraints=["夜里不能说真名", "每次破局都要付出代价", "港区规则不可违背"])

    for rel_path in (
        "Cards/1-风格卡/总风格/整书风格卡.json",
        "Cards/2-角色卡/主要角色/甲.json",
        "Cards/2-角色卡/主要角色/乙.json",
        "Cards/2-角色卡/反派角色/丙.json",
        "Cards/2-角色卡/次要角色/己.json",
        "Cards/3-场景卡/室内/酒肆.json",
        "Cards/3-场景卡/室外/港町.json",
        "Cards/3-场景卡/自然/海岛.json",
        "Cards/4-物品卡/武器装备/佩剑.json",
        "Cards/4-物品卡/线索物品/密账.json",
        "Cards/4-物品卡/重要叙事物品/残篇.json",
        "Cards/4-物品卡/文物/旧袍.json",
        "Cards/4-物品卡/点缀物/酒壶.json",
    ):
        _touch_card(project_root, rel_path)

    _write_json(
        project_root / "Cards" / "1-风格卡" / "风格索引.json",
        {
            "content": {
                **_trace_payload("story-cards > 风格卡/SKILL.md", "Cards/1-风格卡"),
                "card_groups": {
                    "global_styles": ["Cards/1-风格卡/总风格/整书风格卡.json"],
                },
                "style_contract_refs": [{"card_id": "整书风格卡", "path": "Cards/1-风格卡/总风格/整书风格卡.json"}],
                "current_focus": {"confirmed_facts": ["现实题材风格契约"]},
            }
        },
    )
    _write_json(
        project_root / "Cards" / "2-角色卡" / "角色索引.json",
        {
            "content": {
                **_trace_payload("story-cards > 角色卡/SKILL.md", "Cards/2-角色卡"),
                "card_groups": {
                    "protagonists": [
                        "Cards/2-角色卡/主要角色/甲.json",
                        "Cards/2-角色卡/主要角色/乙.json",
                    ],
                    "antagonists": ["Cards/2-角色卡/反派角色/丙.json"],
                    "supporting": ["Cards/2-角色卡/次要角色/己.json"],
                    "ensemble": [],
                },
                "relationship_edges": [{"ok": 1}, {"ok": 2}],
                "current_focus": {"confirmed_facts": ["现实题材"]},
            }
        },
    )
    _write_json(
        project_root / "Cards" / "3-场景卡" / "场景索引.json",
        {
            "content": {
                **_trace_payload("story-cards > 场景卡/SKILL.md", "Cards/3-场景卡"),
                "card_groups": {
                    "indoor": ["Cards/3-场景卡/室内/酒肆.json"],
                    "outdoor": ["Cards/3-场景卡/室外/港町.json"],
                    "natural": ["Cards/3-场景卡/自然/海岛.json"],
                    "surreal": [],
                },
                "scene_links": [{"ok": 1}, {"ok": 2}],
            }
        },
    )
    _write_json(
        project_root / "Cards" / "4-物品卡" / "物品索引.json",
        {
            "content": {
                **_trace_payload("story-cards > 物品卡/SKILL.md", "Cards/4-物品卡"),
                "card_groups": {
                    "weapons_equipment": ["Cards/4-物品卡/武器装备/佩剑.json"],
                    "clue_items": ["Cards/4-物品卡/线索物品/密账.json"],
                    "narrative_items": ["Cards/4-物品卡/重要叙事物品/残篇.json"],
                    "relics": ["Cards/4-物品卡/文物/旧袍.json"],
                    "adornments": ["Cards/4-物品卡/点缀物/酒壶.json"],
                },
                "ownership_links": [{"ok": 1}, {"ok": 2}],
                "exclusive_item_hooks": [{"owner": "甲"}, {"owner": "乙"}],
            }
        },
    )

    report = module.build_cards_coverage_report(project_root)

    assert report["upstream_truth"]["north_star_loaded"] is True
    assert report["upstream_truth"]["init_handoff_loaded"] is True
    assert report["profile"]["rule_rigidity"] == "strong"
    assert report["sections"]["styles"]["ok"] is True
    codes = {item["code"] for item in report["blocking_findings"]}
    assert "FAIL-CARDS-SCENE-SURREAL" in codes
