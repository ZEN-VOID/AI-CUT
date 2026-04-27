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


def _write_text(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def _write_character_graph(project_root: Path, node_names: list[str], edge_count: int) -> None:
    labels = "\n".join(
        f'    n_{index}["{name}"]' for index, name in enumerate(node_names, start=1)
    ) or "    EMPTY[暂无角色数据]"
    edges = []
    for index in range(max(edge_count, 0)):
        left = f"n_{(index % max(len(node_names), 1)) + 1}"
        right = f"n_{((index + 1) % max(len(node_names), 1)) + 1}"
        edges.append(f"    {left} -->|关联| {right}")
    body = "\n".join(edges)
    _write_text(
        project_root / "1-设定" / "2-角色卡" / "角色关系图谱.md",
        "\n".join(
            [
                "# 角色关系图谱",
                "",
                "## 文字说明",
                "- 作用域：全书级角色卡网络，不退化为单章出场名单。",
                f"- 角色总数：{len(node_names)}",
                f"- 关系边数：{edge_count}",
                "",
                "## Mermaid",
                "```mermaid",
                "graph LR",
                labels,
                body,
                "```",
                "",
            ]
        ),
    )


def _touch_card(project_root: Path, rel_path: str) -> None:
    path = project_root / rel_path
    name = Path(rel_path).stem
    if "0-全局卡" in rel_path:
        payload = {
            "schema_version": "story2026/cards/global/v1",
            "meta": {
                "skill_id": "story-cards",
                "source_skill_id": "story-cards-global",
                "source_route": "0-初始化 > story-cards > 全局卡/SKILL.md",
            },
            "content": {
                **_trace_payload("story-cards > 全局卡/SKILL.md", "1-设定/0-全局卡"),
                "card_schema": {
                    "global_card": {
                        "card_id": name,
                        "card_type": "global",
                        "group": "master_global",
                        "core": {
                            "identity": {"name": name, "scope": "full-series"},
                            "worldview": {
                                "world_scale": "跨海江湖与港町",
                                "genre": "武侠+规则怪谈",
                                "target_reader": "网文读者",
                                "platform": "连载平台",
                                "summary": "规则会反噬，武学与异域武道并存。",
                            },
                            "rule_system": [
                                {"label": "旧港规则", "value": "夜里不能直呼真名"},
                                {"label": "武学代价", "value": "越级催动会伤身"},
                            ],
                            "era_constraints": {
                                "era_anchor": "架空近代港町",
                                "worldline_mode": "单线",
                                "hard_boundaries": ["航路贸易仍是主要物流方式"],
                            },
                            "culture_and_arts": {
                                "culture": ["码头行会", "江湖旧礼"],
                                "arts": ["戏台唱段", "海港灯彩"],
                            },
                            "faction_topology": {
                                "tiers": ["海关总署", "码头行会", "走私帮派"],
                                "rule_holders": ["海关总署", "码头行会"],
                                "resource_controllers": ["航路情报", "港口税线"],
                                "relation_patterns": ["明面合作", "暗地互相掣肘"],
                                "protagonist_entry_path": "主角先被码头行会雇佣，再被走私帮派盯上。",
                                "escalation_logic": ["从码头争夺升级为航路控制权争夺"],
                            },
                            "power_or_technology": {
                                "system_type": ["中原武学", "异域武道"],
                                "tech_or_martial": ["刀术", "火器", "航海术"],
                                "resources": ["门派传承", "航路情报"],
                            },
                            "golden_finger": {
                                "name": "残意回响",
                                "type": "规则代价型",
                                "style": "半明牌",
                                "core_function": "读取旧港残留意志",
                                "trigger_conditions": ["进入规则节点"],
                                "costs": ["损耗当日记忆"],
                                "limits": ["一天一次"],
                                "counterplay": ["可被规则噪声污染"],
                                "growth_path": ["从单点读取升级为链式追踪"],
                                "design_template_ref": "全局卡/references/golden-finger-templates.md",
                            },
                        },
                        "current_state": {
                            "active_focus": ["旧港规则"],
                            "downstream_targets": ["Planning", "Drafting", "Validation"],
                            "revision_policy": "north_star 改动才刷新",
                        },
                        "history": [],
                    }
                },
                "global_contract_refs": [
                    {"card_id": name, "path": f"1-设定/0-全局卡/总设定/{name}.json"}
                ],
                "current_focus": {"confirmed_facts": [name]},
            },
            "gate_summary": {"status": "PASS", "fail_codes": [], "repair_entry": ""},
        }
    elif "1-风格卡" in rel_path:
        payload = {
            "schema_version": "story2026/cards/style/v1",
            "meta": {
                "skill_id": "story-cards",
                "source_skill_id": "story-cards-style",
                "source_route": "0-初始化 > story-cards > 风格卡/SKILL.md",
            },
            "content": {
                **_trace_payload("story-cards > 风格卡/SKILL.md", "1-设定/1-风格卡"),
                "card_schema": {
                    "style_card": {
                        "card_id": name,
                        "card_type": "style",
                        "group": "global_style",
                        "core": {
                            "identity": {"name": name, "scope": "full-series"},
                            "style_identity": {
                                "one_line_definition": "冷峻规则压迫型悬疑，靠规则与人心双重收束推进。",
                                "overall_tone": {
                                    "base_tone": "冷峻",
                                    "emotional_temperature": "冷中带刺",
                                    "dark_bright_balance": "八冷二亮",
                                    "tragic_comic_ratio": "九一",
                                    "gravity_level": "高",
                                },
                            },
                            "experience_contract": {
                                "core_pleasures": ["规则压迫"],
                                "expected_aftertaste": ["后怕", "清醒"],
                                "anti_trope": ["不用爽文碾压"],
                                "no_fly_zones": ["鸡汤式总结"],
                            },
                            "narrative_style": {
                                "pov_mode": "近距离第三人称",
                                "narrator_distance": "贴身压迫",
                                "chronology_mode": "顺时序",
                                "information_release_style": "先给规训，再给解释",
                                "suspense_method": "规则倒计时 + 人心试探",
                                "chapter_hook_style": "开场即碰红线",
                                "chapter_end_style": "留规则缺口",
                                "pacing_profile": "快起手，中段挤压，尾段急收",
                            },
                            "dialogue_style": {
                                "dialogue_density": "中",
                                "speech_rhythm": "短句对顶",
                                "subtext_level": "高",
                                "wit_sharpness": "冷硬",
                                "register_policy": "规则话术与日常口语混用",
                                "character_voice_separation": ["守规者平直", "破规者绕行"],
                                "inner_monologue_ratio": "低",
                                "forbidden_dialogue_patterns": ["大段讲义"],
                            },
                            "visual_style": {
                                "image_texture": "潮湿、锈蚀、旧港硬边",
                                "color_palette": ["灰蓝", "铁锈红"],
                                "light_shadow_tendency": "暗面吞光",
                                "motion_texture": "慢压骤断",
                                "spatial_feeling": "低顶逼仄",
                                "violence_imagery": "粗砺留痕",
                                "romance_imagery": "克制回避",
                                "landmark_images": ["港口雾灯", "潮湿台阶"],
                            },
                            "prose_style": {
                                "sentence_length_tendency": "短句为主",
                                "paragraph_rhythm": "短段逼近",
                                "diction_register": "冷硬克制",
                                "metaphor_density": "低",
                                "sensory_bias": ["视觉", "听觉"],
                                "description_density": "中低",
                                "exposition_policy": "只解释当下必须知道的规则",
                            },
                            "scene_style": {
                                "action_rendering": "动作服从规则成本",
                                "emotion_rendering": "情绪藏在失误和停顿里",
                                "atmosphere_rendering": "规则先压场，再压人",
                                "transition_style": "用规则提示物切场",
                                "set_piece_policy": "场面必须带来规则代价",
                            },
                            "style_gate": {
                                "anti_ai_required": True,
                                "no_poison_required": True,
                                "style_contract_ref": f"1-设定/1-风格卡/总风格/{name}.json",
                                "must_keep": ["规则压迫", "冷峻节奏"],
                                "must_avoid": ["鸡汤式总结"],
                                "drift_signals": ["人物突然热血宣讲"],
                                "repair_actions": ["收缩对白", "让规则代价重新上场"],
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
                    {"card_id": name, "path": f"1-设定/1-风格卡/总风格/{name}.json"}
                ],
                "current_focus": {"confirmed_facts": [name]},
            },
            "gate_summary": {"status": "PASS", "fail_codes": [], "repair_entry": ""},
        }
    elif "2-角色卡" in rel_path:
        group = "protagonist"
        if "反派角色" in rel_path:
            group = "antagonist"
        elif "次要角色" in rel_path:
            group = "supporting"
        elif "群像角色" in rel_path:
            group = "ensemble"
        payload = {
            "schema_version": "story2026/cards/character/v2",
            "meta": {
                "skill_id": "story-cards",
                "source_skill_id": "story-cards-character",
                "source_route": "0-初始化 > story-cards > 角色卡/SKILL.md",
            },
            "content": {
                **_trace_payload("story-cards > 角色卡/SKILL.md", "1-设定/2-角色卡"),
                "card_schema": {
                    "character_card": {
                        "card_id": name,
                        "card_type": "character",
                        "group": group,
                        "card_scope": {
                            "scope_type": "full-series",
                            "episode_span": "all-planned-episodes",
                            "refresh_policy": "incremental-writeback extends but never narrows scope",
                        },
                        "core": {
                            "identity": {"name": name},
                            "cast_markers": {
                                "primary_alignment": group,
                                "is_protagonist": group == "protagonist",
                                "is_antagonist": group == "antagonist",
                                "is_supporting": group == "supporting",
                                "is_ensemble": group == "ensemble",
                            },
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
                "source_route": "0-初始化 > story-cards > 场景卡/SKILL.md",
            },
            "content": {
                **_trace_payload("story-cards > 场景卡/SKILL.md", "1-设定/3-场景卡"),
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
                "source_route": "0-初始化 > story-cards > 物品卡/SKILL.md",
            },
            "content": {
                **_trace_payload("story-cards > 物品卡/SKILL.md", "1-设定/4-物品卡"),
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
        "story-cards > 全局卡/SKILL.md": "全局卡/templates/global-card.json",
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
        ]
        + (["全局卡/references/golden-finger-templates.md"] if module_route == "story-cards > 全局卡/SKILL.md" else []),
        "writeback_plan": {
            "mode": "full-build",
            "target_paths": [target_path],
            "upstream_patch_required": False,
            "boundary_notes": ["tests"],
        },
    }


def _write_global_fixture(project_root: Path) -> None:
    _touch_card(project_root, "1-设定/0-全局卡/总设定/世界总卡.json")
    _write_json(
        project_root / "1-设定" / "0-全局卡" / "全局索引.json",
        {
            "content": {
                **_trace_payload("story-cards > 全局卡/SKILL.md", "1-设定/0-全局卡"),
                "card_groups": {
                    "master_globals": ["1-设定/0-全局卡/总设定/世界总卡.json"],
                },
                "global_contract_refs": [
                    {"card_id": "世界总卡", "path": "1-设定/0-全局卡/总设定/世界总卡.json"}
                ],
                "current_focus": {"confirmed_facts": ["世界总设定已锁定"]},
            }
        },
    )


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
        project_root / "0-初始化" / "north_star.yaml",
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
        project_root / "0-初始化" / "init_handoff.yaml",
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
    _write_global_fixture(project_root)

    for rel_path in (
        "1-设定/1-风格卡/总风格/整书风格卡.json",
        "1-设定/2-角色卡/主要角色/甲.json",
        "1-设定/2-角色卡/主要角色/乙.json",
        "1-设定/2-角色卡/反派角色/丙.json",
        "1-设定/2-角色卡/反派角色/丁.json",
        "1-设定/2-角色卡/反派角色/戊.json",
        "1-设定/2-角色卡/次要角色/己.json",
        "1-设定/2-角色卡/次要角色/庚.json",
        "1-设定/2-角色卡/群像角色/辛.json",
        "1-设定/3-场景卡/室内/酒肆.json",
        "1-设定/3-场景卡/室外/港町.json",
        "1-设定/3-场景卡/自然/海岛.json",
        "1-设定/3-场景卡/自然/断崖.json",
        "1-设定/3-场景卡/超现实/镜庭.json",
        "1-设定/3-场景卡/超现实/残意海.json",
        "1-设定/4-物品卡/武器装备/佩剑.json",
        "1-设定/4-物品卡/武器装备/短刀.json",
        "1-设定/4-物品卡/线索物品/密账.json",
        "1-设定/4-物品卡/线索物品/海图.json",
        "1-设定/4-物品卡/重要叙事物品/残篇.json",
        "1-设定/4-物品卡/重要叙事物品/铃牌.json",
        "1-设定/4-物品卡/文物/旧袍.json",
        "1-设定/4-物品卡/点缀物/酒壶.json",
    ):
        _touch_card(project_root, rel_path)

    _write_json(
        project_root / "1-设定" / "1-风格卡" / "风格索引.json",
        {
            "content": {
                **_trace_payload(
                    "story-cards > 风格卡/SKILL.md",
                    "1-设定/1-风格卡",
                ),
                "card_groups": {
                    "global_styles": ["1-设定/1-风格卡/总风格/整书风格卡.json"],
                },
                "style_contract_refs": [
                    {"card_id": "整书风格卡", "path": "1-设定/1-风格卡/总风格/整书风格卡.json"}
                ],
                "current_focus": {"confirmed_facts": ["整书风格契约已锁定"]},
            }
        },
    )
    _write_json(
        project_root / "1-设定" / "2-角色卡" / "角色索引.json",
        {
            "content": {
                **_trace_payload(
                    "story-cards > 角色卡/SKILL.md",
                    "1-设定/2-角色卡",
                ),
                "card_groups": {
                    "protagonists": [
                        "1-设定/2-角色卡/主要角色/甲.json",
                        "1-设定/2-角色卡/主要角色/乙.json",
                    ],
                    "antagonists": [
                        "1-设定/2-角色卡/反派角色/丙.json",
                        "1-设定/2-角色卡/反派角色/丁.json",
                        "1-设定/2-角色卡/反派角色/戊.json",
                    ],
                    "supporting": [
                        "1-设定/2-角色卡/次要角色/己.json",
                        "1-设定/2-角色卡/次要角色/庚.json",
                    ],
                    "ensemble": ["1-设定/2-角色卡/群像角色/辛.json"],
                },
                "relationship_edges": [{"ok": 1}, {"ok": 2}, {"ok": 3}, {"ok": 4}],
                "relationship_graph": {
                    "path": "1-设定/2-角色卡/角色关系图谱.md",
                    "format": "markdown+mermaid",
                    "scope": "full-series",
                },
                "current_focus": {"confirmed_facts": ["双主角成立"]},
            }
        },
    )
    _write_character_graph(project_root, ["甲", "乙", "丙", "丁", "戊", "己", "庚", "辛"], 4)
    _write_json(
        project_root / "1-设定" / "3-场景卡" / "场景索引.json",
        {
            "content": {
                **_trace_payload(
                    "story-cards > 场景卡/SKILL.md",
                    "1-设定/3-场景卡",
                ),
                "card_groups": {
                    "indoor": ["1-设定/3-场景卡/室内/酒肆.json"],
                    "outdoor": ["1-设定/3-场景卡/室外/港町.json"],
                    "natural": [
                        "1-设定/3-场景卡/自然/海岛.json",
                        "1-设定/3-场景卡/自然/断崖.json",
                    ],
                    "surreal": [
                        "1-设定/3-场景卡/超现实/镜庭.json",
                        "1-设定/3-场景卡/超现实/残意海.json",
                    ],
                },
                "scene_links": [{"ok": 1}, {"ok": 2}, {"ok": 3}, {"ok": 4}, {"ok": 5}],
            }
        },
    )
    _write_json(
        project_root / "1-设定" / "4-物品卡" / "物品索引.json",
        {
            "content": {
                **_trace_payload(
                    "story-cards > 物品卡/SKILL.md",
                    "1-设定/4-物品卡",
                ),
                "card_groups": {
                    "weapons_equipment": [
                        "1-设定/4-物品卡/武器装备/佩剑.json",
                        "1-设定/4-物品卡/武器装备/短刀.json",
                    ],
                    "clue_items": [
                        "1-设定/4-物品卡/线索物品/密账.json",
                        "1-设定/4-物品卡/线索物品/海图.json",
                    ],
                    "narrative_items": [
                        "1-设定/4-物品卡/重要叙事物品/残篇.json",
                        "1-设定/4-物品卡/重要叙事物品/铃牌.json",
                    ],
                    "relics": ["1-设定/4-物品卡/文物/旧袍.json"],
                    "adornments": ["1-设定/4-物品卡/点缀物/酒壶.json"],
                },
                "ownership_links": [{"ok": 1}, {"ok": 2}, {"ok": 3}, {"ok": 4}],
                "exclusive_item_hooks": [{"owner": "甲"}, {"owner": "乙"}],
            }
        },
    )

    report = module.build_cards_coverage_report(project_root)

    assert report["ok"] is True
    assert "globals" not in report["sections"]
    assert "styles" not in report["sections"]
    assert "types" not in report["sections"]
    assert report["sections"]["characters"]["counts"]["protagonists"] == 2
    assert report["sections"]["scenes"]["total_count"] == 6
    assert report["sections"]["items"]["total_count"] == 8
    assert report["sections"]["characters"]["trace"]["module_route"] == "story-cards > 角色卡/SKILL.md"


def test_cards_coverage_report_fails_when_series_cards_are_too_thin(tmp_path):
    module = _load_module()
    project_root = _make_project_root(tmp_path)
    _write_upstream_truth(project_root)
    _write_global_fixture(project_root)

    for rel_path in (
        "1-设定/1-风格卡/总风格/整书风格卡.json",
        "1-设定/2-角色卡/主要角色/甲.json",
        "1-设定/2-角色卡/反派角色/丙.json",
        "1-设定/3-场景卡/室内/酒肆.json",
        "1-设定/4-物品卡/武器装备/佩剑.json",
    ):
        _touch_card(project_root, rel_path)

    _write_json(
        project_root / "1-设定" / "1-风格卡" / "风格索引.json",
        {
            "content": {
                **_trace_payload(
                    "story-cards > 风格卡/SKILL.md",
                    "1-设定/1-风格卡",
                ),
                "card_groups": {
                    "global_styles": ["1-设定/1-风格卡/总风格/整书风格卡.json"],
                },
                "style_contract_refs": [
                    {"card_id": "整书风格卡", "path": "1-设定/1-风格卡/总风格/整书风格卡.json"}
                ],
                "current_focus": {"confirmed_facts": ["风格契约已锁定"]},
            }
        },
    )
    _write_json(
        project_root / "1-设定" / "2-角色卡" / "角色索引.json",
        {
            "content": {
                **_trace_payload(
                    "story-cards > 角色卡/SKILL.md",
                    "1-设定/2-角色卡",
                ),
                "card_groups": {
                    "protagonists": ["1-设定/2-角色卡/主要角色/甲.json"],
                    "antagonists": ["1-设定/2-角色卡/反派角色/丙.json"],
                    "supporting": [],
                    "ensemble": [],
                },
                "relationship_edges": [{"ok": 1}],
                "relationship_graph": {
                    "path": "1-设定/2-角色卡/角色关系图谱.md",
                    "format": "markdown+mermaid",
                    "scope": "full-series",
                },
                "current_focus": {"confirmed_facts": ["过薄"]},
            }
        },
    )
    _write_character_graph(project_root, ["甲", "丙"], 1)
    _write_json(
        project_root / "1-设定" / "3-场景卡" / "场景索引.json",
        {
            "content": {
                **_trace_payload(
                    "story-cards > 场景卡/SKILL.md",
                    "1-设定/3-场景卡",
                ),
                "card_groups": {
                    "indoor": ["1-设定/3-场景卡/室内/酒肆.json"],
                    "outdoor": [],
                    "natural": [],
                    "surreal": [],
                },
                "scene_links": [{"ok": 1}],
            }
        },
    )
    _write_json(
        project_root / "1-设定" / "4-物品卡" / "物品索引.json",
        {
            "content": {
                **_trace_payload(
                    "story-cards > 物品卡/SKILL.md",
                    "1-设定/4-物品卡",
                ),
                "card_groups": {
                    "weapons_equipment": ["1-设定/4-物品卡/武器装备/佩剑.json"],
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
    _write_global_fixture(project_root)

    for rel_path in (
        "1-设定/1-风格卡/总风格/整书风格卡.json",
        "1-设定/2-角色卡/主要角色/甲.json",
        "1-设定/2-角色卡/主要角色/乙.json",
        "1-设定/2-角色卡/反派角色/丙.json",
        "1-设定/2-角色卡/反派角色/丁.json",
        "1-设定/2-角色卡/反派角色/戊.json",
        "1-设定/2-角色卡/次要角色/己.json",
        "1-设定/2-角色卡/次要角色/庚.json",
        "1-设定/2-角色卡/群像角色/辛.json",
        "1-设定/3-场景卡/室内/酒肆.json",
        "1-设定/3-场景卡/室外/港町.json",
        "1-设定/3-场景卡/自然/海岛.json",
        "1-设定/3-场景卡/自然/断崖.json",
        "1-设定/3-场景卡/超现实/镜庭.json",
        "1-设定/3-场景卡/超现实/残意海.json",
        "1-设定/4-物品卡/武器装备/佩剑.json",
        "1-设定/4-物品卡/武器装备/短刀.json",
        "1-设定/4-物品卡/线索物品/密账.json",
        "1-设定/4-物品卡/线索物品/海图.json",
        "1-设定/4-物品卡/重要叙事物品/残篇.json",
        "1-设定/4-物品卡/重要叙事物品/铃牌.json",
        "1-设定/4-物品卡/文物/旧袍.json",
        "1-设定/4-物品卡/点缀物/酒壶.json",
    ):
        _touch_card(project_root, rel_path)

    _write_json(
        project_root / "1-设定" / "1-风格卡" / "风格索引.json",
        {
            "content": {
                "card_groups": {
                    "global_styles": ["1-设定/1-风格卡/总风格/整书风格卡.json"],
                },
                "style_contract_refs": [{"card_id": "整书风格卡", "path": "1-设定/1-风格卡/总风格/整书风格卡.json"}],
                "current_focus": {"confirmed_facts": ["风格契约已锁定"]},
            }
        },
    )
    _write_json(
        project_root / "1-设定" / "2-角色卡" / "角色索引.json",
        {
            "content": {
                "card_groups": {
                    "protagonists": [
                        "1-设定/2-角色卡/主要角色/甲.json",
                        "1-设定/2-角色卡/主要角色/乙.json",
                    ],
                    "antagonists": [
                        "1-设定/2-角色卡/反派角色/丙.json",
                        "1-设定/2-角色卡/反派角色/丁.json",
                        "1-设定/2-角色卡/反派角色/戊.json",
                    ],
                    "supporting": [
                        "1-设定/2-角色卡/次要角色/己.json",
                        "1-设定/2-角色卡/次要角色/庚.json",
                    ],
                    "ensemble": ["1-设定/2-角色卡/群像角色/辛.json"],
                },
                "relationship_edges": [{"ok": 1}, {"ok": 2}, {"ok": 3}, {"ok": 4}],
                "relationship_graph": {
                    "path": "1-设定/2-角色卡/角色关系图谱.md",
                    "format": "markdown+mermaid",
                    "scope": "full-series",
                },
                "current_focus": {"confirmed_facts": ["双主角成立"]},
            }
        },
    )
    _write_character_graph(project_root, ["甲", "乙", "丙", "丁", "戊", "己", "庚", "辛"], 4)
    _write_json(
        project_root / "1-设定" / "3-场景卡" / "场景索引.json",
        {
            "content": {
                "card_groups": {
                    "indoor": ["1-设定/3-场景卡/室内/酒肆.json"],
                    "outdoor": ["1-设定/3-场景卡/室外/港町.json"],
                    "natural": [
                        "1-设定/3-场景卡/自然/海岛.json",
                        "1-设定/3-场景卡/自然/断崖.json",
                    ],
                    "surreal": [
                        "1-设定/3-场景卡/超现实/镜庭.json",
                        "1-设定/3-场景卡/超现实/残意海.json",
                    ],
                },
                "scene_links": [{"ok": 1}, {"ok": 2}, {"ok": 3}],
            }
        },
    )
    _write_json(
        project_root / "1-设定" / "4-物品卡" / "物品索引.json",
        {
            "content": {
                "card_groups": {
                    "weapons_equipment": [
                        "1-设定/4-物品卡/武器装备/佩剑.json",
                        "1-设定/4-物品卡/武器装备/短刀.json",
                    ],
                    "clue_items": [
                        "1-设定/4-物品卡/线索物品/密账.json",
                        "1-设定/4-物品卡/线索物品/海图.json",
                    ],
                    "narrative_items": [
                        "1-设定/4-物品卡/重要叙事物品/残篇.json",
                        "1-设定/4-物品卡/重要叙事物品/铃牌.json",
                    ],
                    "relics": ["1-设定/4-物品卡/文物/旧袍.json"],
                    "adornments": ["1-设定/4-物品卡/点缀物/酒壶.json"],
                },
                "ownership_links": [{"ok": 1}, {"ok": 2}, {"ok": 3}],
                "exclusive_item_hooks": [{"owner": "甲"}, {"owner": "乙"}],
            }
        },
    )

    report = module.build_cards_coverage_report(project_root)

    assert report["ok"] is False
    codes = {item["code"] for item in report["blocking_findings"]}
    assert "FAIL-CARDS-CHAR-ROUTE" in codes
    assert "FAIL-CARDS-CHAR-TRACE" in codes
    assert "FAIL-CARDS-CHAR-WRITEBACK" in codes
    assert "FAIL-CARDS-SCENE-ROUTE" in codes
    assert "FAIL-CARDS-ITEM-WRITEBACK" in codes


def test_cards_coverage_report_fails_when_card_files_are_shell_payloads(tmp_path):
    module = _load_module()
    project_root = _make_project_root(tmp_path)
    _write_upstream_truth(project_root)
    _write_json(project_root / "1-设定" / "0-全局卡" / "总设定" / "世界总卡.json", {"ok": True})
    _write_json(
        project_root / "1-设定" / "0-全局卡" / "全局索引.json",
        {
            "content": {
                **_trace_payload("story-cards > 全局卡/SKILL.md", "1-设定/0-全局卡"),
                "card_groups": {
                    "master_globals": ["1-设定/0-全局卡/总设定/世界总卡.json"],
                },
                "global_contract_refs": [{"card_id": "世界总卡", "path": "1-设定/0-全局卡/总设定/世界总卡.json"}],
                "current_focus": {"confirmed_facts": ["世界总设定已锁定"]},
            }
        },
    )

    for rel_path in (
        "1-设定/1-风格卡/总风格/整书风格卡.json",
        "1-设定/2-角色卡/主要角色/甲.json",
        "1-设定/2-角色卡/主要角色/乙.json",
        "1-设定/2-角色卡/反派角色/丙.json",
        "1-设定/2-角色卡/反派角色/丁.json",
        "1-设定/2-角色卡/反派角色/戊.json",
        "1-设定/2-角色卡/次要角色/己.json",
        "1-设定/2-角色卡/次要角色/庚.json",
        "1-设定/2-角色卡/群像角色/辛.json",
        "1-设定/3-场景卡/室内/酒肆.json",
        "1-设定/3-场景卡/室外/港町.json",
        "1-设定/3-场景卡/自然/海岛.json",
        "1-设定/3-场景卡/自然/断崖.json",
        "1-设定/3-场景卡/超现实/镜庭.json",
        "1-设定/3-场景卡/超现实/残意海.json",
        "1-设定/4-物品卡/武器装备/佩剑.json",
        "1-设定/4-物品卡/武器装备/短刀.json",
        "1-设定/4-物品卡/线索物品/密账.json",
        "1-设定/4-物品卡/线索物品/海图.json",
        "1-设定/4-物品卡/重要叙事物品/残篇.json",
        "1-设定/4-物品卡/重要叙事物品/铃牌.json",
        "1-设定/4-物品卡/文物/旧袍.json",
        "1-设定/4-物品卡/点缀物/酒壶.json",
    ):
        _write_json(project_root / rel_path, {"ok": True})

    _write_json(
        project_root / "1-设定" / "1-风格卡" / "风格索引.json",
        {
            "content": {
                **_trace_payload(
                    "story-cards > 风格卡/SKILL.md",
                    "1-设定/1-风格卡",
                ),
                "card_groups": {
                    "global_styles": ["1-设定/1-风格卡/总风格/整书风格卡.json"],
                },
                "style_contract_refs": [{"card_id": "整书风格卡", "path": "1-设定/1-风格卡/总风格/整书风格卡.json"}],
                "current_focus": {"confirmed_facts": ["风格契约已锁定"]},
            }
        },
    )
    _write_json(
        project_root / "1-设定" / "2-角色卡" / "角色索引.json",
        {
            "content": {
                **_trace_payload(
                    "story-cards > 角色卡/SKILL.md",
                    "1-设定/2-角色卡",
                ),
                "card_groups": {
                    "protagonists": [
                        "1-设定/2-角色卡/主要角色/甲.json",
                        "1-设定/2-角色卡/主要角色/乙.json",
                    ],
                    "antagonists": [
                        "1-设定/2-角色卡/反派角色/丙.json",
                        "1-设定/2-角色卡/反派角色/丁.json",
                        "1-设定/2-角色卡/反派角色/戊.json",
                    ],
                    "supporting": [
                        "1-设定/2-角色卡/次要角色/己.json",
                        "1-设定/2-角色卡/次要角色/庚.json",
                    ],
                    "ensemble": ["1-设定/2-角色卡/群像角色/辛.json"],
                },
                "relationship_edges": [{"ok": 1}, {"ok": 2}, {"ok": 3}, {"ok": 4}],
                "relationship_graph": {
                    "path": "1-设定/2-角色卡/角色关系图谱.md",
                    "format": "markdown+mermaid",
                    "scope": "full-series",
                },
                "current_focus": {"confirmed_facts": ["双主角成立"]},
            }
        },
    )
    _write_character_graph(project_root, ["甲", "乙", "丙", "丁", "戊", "己", "庚", "辛"], 4)
    _write_json(
        project_root / "1-设定" / "3-场景卡" / "场景索引.json",
        {
            "content": {
                **_trace_payload(
                    "story-cards > 场景卡/SKILL.md",
                    "1-设定/3-场景卡",
                ),
                "card_groups": {
                    "indoor": ["1-设定/3-场景卡/室内/酒肆.json"],
                    "outdoor": ["1-设定/3-场景卡/室外/港町.json"],
                    "natural": [
                        "1-设定/3-场景卡/自然/海岛.json",
                        "1-设定/3-场景卡/自然/断崖.json",
                    ],
                    "surreal": [
                        "1-设定/3-场景卡/超现实/镜庭.json",
                        "1-设定/3-场景卡/超现实/残意海.json",
                    ],
                },
                "scene_links": [{"ok": 1}, {"ok": 2}, {"ok": 3}, {"ok": 4}],
            }
        },
    )
    _write_json(
        project_root / "1-设定" / "4-物品卡" / "物品索引.json",
        {
            "content": {
                **_trace_payload(
                    "story-cards > 物品卡/SKILL.md",
                    "1-设定/4-物品卡",
                ),
                "card_groups": {
                    "weapons_equipment": [
                        "1-设定/4-物品卡/武器装备/佩剑.json",
                        "1-设定/4-物品卡/武器装备/短刀.json",
                    ],
                    "clue_items": [
                        "1-设定/4-物品卡/线索物品/密账.json",
                        "1-设定/4-物品卡/线索物品/海图.json",
                    ],
                    "narrative_items": [
                        "1-设定/4-物品卡/重要叙事物品/残篇.json",
                        "1-设定/4-物品卡/重要叙事物品/铃牌.json",
                    ],
                    "relics": ["1-设定/4-物品卡/文物/旧袍.json"],
                    "adornments": ["1-设定/4-物品卡/点缀物/酒壶.json"],
                },
                "ownership_links": [{"ok": 1}, {"ok": 2}, {"ok": 3}, {"ok": 4}],
                "exclusive_item_hooks": [{"owner": "甲"}, {"owner": "乙"}],
            }
        },
    )

    report = module.build_cards_coverage_report(project_root)

    assert report["ok"] is False
    codes = {item["code"] for item in report["blocking_findings"]}
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
    _write_global_fixture(project_root)

    for rel_path in (
        "1-设定/1-风格卡/总风格/整书风格卡.json",
        "1-设定/2-角色卡/主要角色/甲.json",
        "1-设定/2-角色卡/主要角色/乙.json",
        "1-设定/2-角色卡/反派角色/丙.json",
        "1-设定/2-角色卡/次要角色/己.json",
        "1-设定/3-场景卡/室内/酒肆.json",
        "1-设定/3-场景卡/室外/港町.json",
        "1-设定/3-场景卡/自然/海岛.json",
        "1-设定/4-物品卡/武器装备/佩剑.json",
        "1-设定/4-物品卡/线索物品/密账.json",
        "1-设定/4-物品卡/重要叙事物品/残篇.json",
        "1-设定/4-物品卡/文物/旧袍.json",
        "1-设定/4-物品卡/点缀物/酒壶.json",
    ):
        _touch_card(project_root, rel_path)

    _write_json(
        project_root / "1-设定" / "1-风格卡" / "风格索引.json",
        {
            "content": {
                **_trace_payload("story-cards > 风格卡/SKILL.md", "1-设定/1-风格卡"),
                "card_groups": {
                    "global_styles": ["1-设定/1-风格卡/总风格/整书风格卡.json"],
                },
                "style_contract_refs": [{"card_id": "整书风格卡", "path": "1-设定/1-风格卡/总风格/整书风格卡.json"}],
                "current_focus": {"confirmed_facts": ["现实题材风格契约"]},
            }
        },
    )
    _write_json(
        project_root / "1-设定" / "2-角色卡" / "角色索引.json",
        {
            "content": {
                **_trace_payload("story-cards > 角色卡/SKILL.md", "1-设定/2-角色卡"),
                "card_groups": {
                    "protagonists": [
                        "1-设定/2-角色卡/主要角色/甲.json",
                        "1-设定/2-角色卡/主要角色/乙.json",
                    ],
                    "antagonists": ["1-设定/2-角色卡/反派角色/丙.json"],
                    "supporting": ["1-设定/2-角色卡/次要角色/己.json"],
                    "ensemble": [],
                },
                "relationship_edges": [{"ok": 1}, {"ok": 2}],
                "relationship_graph": {
                    "path": "1-设定/2-角色卡/角色关系图谱.md",
                    "format": "markdown+mermaid",
                    "scope": "full-series",
                },
                "current_focus": {"confirmed_facts": ["现实题材"]},
            }
        },
    )
    _write_character_graph(project_root, ["甲", "乙", "丙", "己"], 2)
    _write_json(
        project_root / "1-设定" / "3-场景卡" / "场景索引.json",
        {
            "content": {
                **_trace_payload("story-cards > 场景卡/SKILL.md", "1-设定/3-场景卡"),
                "card_groups": {
                    "indoor": ["1-设定/3-场景卡/室内/酒肆.json"],
                    "outdoor": ["1-设定/3-场景卡/室外/港町.json"],
                    "natural": ["1-设定/3-场景卡/自然/海岛.json"],
                    "surreal": [],
                },
                "scene_links": [{"ok": 1}, {"ok": 2}],
            }
        },
    )
    _write_json(
        project_root / "1-设定" / "4-物品卡" / "物品索引.json",
        {
            "content": {
                **_trace_payload("story-cards > 物品卡/SKILL.md", "1-设定/4-物品卡"),
                "card_groups": {
                    "weapons_equipment": ["1-设定/4-物品卡/武器装备/佩剑.json"],
                    "clue_items": ["1-设定/4-物品卡/线索物品/密账.json"],
                    "narrative_items": ["1-设定/4-物品卡/重要叙事物品/残篇.json"],
                    "relics": ["1-设定/4-物品卡/文物/旧袍.json"],
                    "adornments": ["1-设定/4-物品卡/点缀物/酒壶.json"],
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
    assert "globals" not in report["sections"]
    assert "styles" not in report["sections"]
    assert "types" not in report["sections"]
    codes = {item["code"] for item in report["blocking_findings"]}
    assert "FAIL-CARDS-SCENE-SURREAL" in codes
