#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import sys
from pathlib import Path

import yaml


def _load_modules():
    scripts_dir = Path(__file__).resolve().parents[2]
    if str(scripts_dir) not in sys.path:
        sys.path.insert(0, str(scripts_dir))

    import cards_coverage_validator
    import cards_writer
    import security_utils

    return cards_writer, cards_coverage_validator, security_utils


def _write_json(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")


def _write_yaml(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(yaml.safe_dump(payload, allow_unicode=True, sort_keys=False), encoding="utf-8")


def _make_project_root(tmp_path: Path) -> Path:
    project_root = tmp_path / "book"
    _write_json(
        project_root / "STATE.json",
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
    _write_yaml(
        project_root / "0-Init" / "north_star.yaml",
        {
            "project_identity": {
                "title": "测试书",
                "genre": "都市成长",
                "target_chapters": 10,
            },
            "type_stack": {
                "method_kernel": "story-core-v1",
                "base": "_base",
                "primary": "网文高冲击",
                "secondary": ["都市复仇"],
                "platform": [],
                "audience": [],
            },
            "reader_promise": {
                "hard_constraints": [],
                "primary_pleasures": ["现实压力下的成长"],
                "anti_trope": "不用说教胜利学",
                "no_fly_zones": ["鸡汤式自白"],
            },
            "aesthetic_axes": {
                "tone": "冷静克制",
                "violence_texture": "现实痛感",
                "mystery_density": "中高",
                "romance_policy": "克制慢热",
            },
            "cards": {
                "style_system": {
                    "text_style": {
                        "tone": "冷静克制",
                        "genre_corridor": "都市成长",
                        "anti_trope": "不用说教胜利学",
                    },
                    "narrative_style": {
                        "opening_hook": "债务与旧案双压",
                        "mystery_density": "中高",
                        "romance_policy": "克制慢热",
                    },
                    "tone_promises": ["现实压力下的成长"],
                    "taboo_styles": ["鸡汤式自白"],
                    "downstream_constraints": [],
                },
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
            "cards_seed": {
                "character_seed": {
                    "protagonist": {"structure": "单主角"},
                    "relationship": {"antagonist_tiers": {"对手": "赵竞"}},
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
                        "protagonist": {"structure": "单主角"},
                        "relationship": {"antagonist_tiers": {"对手": "赵竞"}},
                    }
                },
                "planning_seed": {
                    "pacing_scale": {"target_chapters": 10, "protagonist_structure": "单主角"},
                    "constraint_seed": {"hard_constraints": []},
                },
            }
        },
    )
    return project_root


def _build_payload() -> dict:
    return {
        "mode": "full-build",
        "boundary_notes": ["cards-writer-test"],
        "sections": {
            "globals": {
                "global_contract_refs": [
                    {"card_id": "世界总卡", "path": "1-Cards/0-全局卡/总设定/世界总卡.json"}
                ],
                "current_focus": {
                    "confirmed_facts": ["世界规则与金手指合同已锁定"],
                    "inferred_defaults": [],
                    "active_constraints": ["金手指必须付代价"],
                },
                "cards": [
                    {
                        "bucket": "master_globals",
                        "file_name": "世界总卡.json",
                        "card": {
                            "core": {
                                "identity": {"name": "世界总卡", "scope": "full-series"},
                                "worldview": {
                                    "world_scale": "都市边缘区",
                                    "genre": "都市成长",
                                    "target_reader": "网文读者",
                                    "platform": "连载平台",
                                    "summary": "现实债务压力下存在可追溯但有代价的异常规则。",
                                },
                                "rule_system": [
                                    {"label": "旧案规则", "value": "每次回溯都必须牺牲一段即时记忆"},
                                    {"label": "现实边界", "value": "不能直接改写已公开发生的事件"},
                                ],
                                "era_constraints": {
                                    "era_anchor": "当代都市",
                                    "worldline_mode": "单线现实",
                                    "hard_boundaries": ["智能手机与监控系统普遍存在"],
                                },
                                "culture_and_arts": {
                                    "culture": ["旧城借贷文化", "档案制度与人情社会并存"],
                                    "arts": ["冷白霓虹", "旧纸张与磁带质感"],
                                },
                                "power_or_technology": {
                                    "system_type": ["有限回溯"],
                                    "tech_or_martial": ["监控系统", "旧式录音设备"],
                                    "resources": ["记忆", "时间窗口"],
                                },
                                "golden_finger": {
                                    "name": "旧怀表回溯",
                                    "type": "记忆代价型",
                                    "style": "冷硬工具型",
                                    "core_function": "短时间读取与旧案相关的残留记忆",
                                    "trigger_conditions": ["逆时针拨动怀表一格"],
                                    "costs": ["失去一段当日记忆"],
                                    "limits": ["每天最多一次", "无法读取与自己无关的现场"],
                                    "counterplay": ["对手可通过噪声信息污染记忆残留"],
                                    "growth_path": ["从单点回溯升级为链式回溯"],
                                },
                            },
                            "current_state": {
                                "active_focus": ["旧案回溯规则"],
                                "downstream_targets": ["1-Cards", "2-Planning", "3-Drafting"],
                                "revision_policy": "只有 north_star 的世界设定改动时才重写",
                            },
                            "history": [],
                        },
                    }
                ],
            },
            "styles": {
                "style_contract_refs": [
                    {"card_id": "整书风格卡", "path": "1-Cards/1-风格卡/总风格/整书风格卡.json"}
                ],
                "current_focus": {
                    "confirmed_facts": ["读者承诺与审美轴已锁定"],
                    "inferred_defaults": [],
                    "active_constraints": ["鸡汤式自白禁用"],
                },
                "cards": [
                    {
                        "bucket": "global_styles",
                        "file_name": "整书风格卡.json",
                        "card": {
                            "core": {
                                "identity": {"name": "整书风格卡", "scope": "full-series"},
                                "style_identity": {
                                    "one_line_definition": "冷静克制的现实成长叙事，靠压力、旧案与关系裂缝推着人物前行。",
                                    "overall_tone": {
                                        "base_tone": "冷静克制",
                                        "emotional_temperature": "冷中带灼",
                                        "dark_bright_balance": "七冷三暖",
                                        "tragic_comic_ratio": "八二",
                                        "gravity_level": "中高",
                                    },
                                },
                                "experience_contract": {
                                    "core_pleasures": ["现实压力下的成长"],
                                    "expected_aftertaste": ["压抑后的清醒", "迟到但成立的尊严"],
                                    "anti_trope": ["不用说教胜利学"],
                                    "no_fly_zones": ["鸡汤式自白"],
                                },
                                "narrative_style": {
                                    "pov_mode": "近距离第三人称",
                                    "narrator_distance": "贴身但不自怜",
                                    "chronology_mode": "顺时序推进，关键处短回溯补压",
                                    "information_release_style": "先给压力结果，再逐步揭露旧案因果",
                                    "suspense_method": "债务、旧案、关系三线并压",
                                    "chapter_hook_style": "以现实困局切入",
                                    "chapter_end_style": "留半步真相，不做硬悬浮",
                                    "pacing_profile": "中速推进，关键节点骤然收紧",
                                },
                                "dialogue_style": {
                                    "dialogue_density": "中高",
                                    "speech_rhythm": "短句试探后突然摊牌",
                                    "subtext_level": "高",
                                    "wit_sharpness": "克制锋利",
                                    "register_policy": "都市口语为底，关键对峙时拔高",
                                    "character_voice_separation": ["林舟压句省词", "周岚冷静拆解", "赵竞礼貌压迫"],
                                    "inner_monologue_ratio": "中低",
                                    "forbidden_dialogue_patterns": ["直白讲道理", "鸡汤总结局面"],
                                },
                                "visual_style": {
                                    "image_texture": "冷白霓虹、旧纸张、潮湿墙皮",
                                    "color_palette": ["冷白", "锈黄", "深蓝"],
                                    "light_shadow_tendency": "偏暗，局部硬光切面",
                                    "motion_texture": "缓压突刺",
                                    "spatial_feeling": "逼仄都市夹缝",
                                    "violence_imagery": "现实钝痛，不做热血夸饰",
                                    "romance_imagery": "冷光下的迟疑靠近",
                                    "landmark_images": ["档案馆冷灯", "旧怀表金属反光"],
                                },
                                "prose_style": {
                                    "sentence_length_tendency": "短中句为主",
                                    "paragraph_rhythm": "短段推进，关键段落突然拉长",
                                    "diction_register": "克制现代汉语",
                                    "metaphor_density": "低到中",
                                    "sensory_bias": ["视觉", "触觉"],
                                    "description_density": "中等偏省",
                                    "exposition_policy": "解释服从情境压力，不做讲义化展开",
                                },
                                "scene_style": {
                                    "action_rendering": "动作少而准，重后果",
                                    "emotion_rendering": "情绪不喊口号，靠停顿和错位动作显形",
                                    "atmosphere_rendering": "先空间压迫，再情绪上脸",
                                    "transition_style": "用物件或动作切场",
                                    "set_piece_policy": "大场面服务人物选择，不只拼刺激",
                                },
                                "style_gate": {
                                    "anti_ai_required": True,
                                    "no_poison_required": True,
                                    "style_contract_ref": "1-Cards/1-风格卡/总风格/整书风格卡.json",
                                    "must_keep": ["冷静克制", "现实压迫", "人物尊严感"],
                                    "must_avoid": ["鸡汤式自白", "无代价逆转"],
                                    "drift_signals": ["人物突然大段讲道理", "画面忽然热血漫画化"],
                                    "repair_actions": ["收短句子", "把解释改回动作与场景承压"],
                                }
                            },
                            "current_state": {
                                "active_focus": ["现实压力下的成长"],
                                "downstream_targets": ["Drafting", "Validation"],
                                "revision_policy": "只有 north_star 改动时才重写",
                            },
                            "history": [],
                        },
                    }
                ],
            },
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
                    {"source": "档案室", "target": "河堤", "type": "reveal"},
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
    cards_writer, cards_coverage_validator, _security_utils = _load_modules()
    project_root = _make_project_root(tmp_path)

    report = cards_writer.write_cards_payload(project_root, _build_payload(), run_gate=True)

    assert report["ok"] is True
    assert report["mode"] == "full-build"

    global_path = project_root / "1-Cards" / "0-全局卡" / "总设定" / "世界总卡.json"
    global_card = json.loads(global_path.read_text(encoding="utf-8"))
    assert global_card["meta"]["source_skill_id"] == "story-cards-global"
    assert global_card["meta"]["source_route"] == "0-Init > story-cards > 全局卡/SKILL.md"
    assert global_card["content"]["module_route"] == "story-cards > 全局卡/SKILL.md"
    assert global_card["content"]["loaded_references"] == [
        "SKILL.md",
        "CONTEXT.md",
        "全局卡/SKILL.md",
        "全局卡/CONTEXT.md",
        "全局卡/templates/global-card.json",
        "全局卡/references/golden-finger-templates.md",
    ]

    style_path = project_root / "1-Cards" / "1-风格卡" / "总风格" / "整书风格卡.json"
    style_card = json.loads(style_path.read_text(encoding="utf-8"))
    assert style_card["meta"]["source_skill_id"] == "story-cards-style"
    assert style_card["meta"]["source_route"] == "0-Init > story-cards > 风格卡/SKILL.md"
    assert style_card["content"]["module_route"] == "story-cards > 风格卡/SKILL.md"
    assert style_card["content"]["loaded_references"] == [
        "SKILL.md",
        "CONTEXT.md",
        "风格卡/SKILL.md",
        "风格卡/CONTEXT.md",
        "风格卡/templates/style-card.json",
    ]

    protagonist_path = project_root / "1-Cards" / "2-角色卡" / "主要角色" / "林舟.json"
    protagonist = json.loads(protagonist_path.read_text(encoding="utf-8"))
    assert protagonist["meta"]["source_skill_id"] == "story-cards-character"
    assert protagonist["meta"]["source_route"] == "0-Init > story-cards > 角色卡/SKILL.md"
    assert protagonist["content"]["module_route"] == "story-cards > 角色卡/SKILL.md"
    assert protagonist["content"]["type_stack_ref"]["primary"] == "网文高冲击"
    assert protagonist["content"]["loaded_references"] == [
        "SKILL.md",
        "CONTEXT.md",
        "角色卡/SKILL.md",
        "角色卡/CONTEXT.md",
        "角色卡/templates/character-card.json",
    ]
    assert protagonist["content"]["writeback_plan"]["mode"] == "full-build"
    assert protagonist["content"]["writeback_plan"]["target_paths"] == [
        "1-Cards/2-角色卡/主要角色/林舟.json",
        "1-Cards/2-角色卡/角色索引.json",
    ]
    assert protagonist["content"]["card_schema"]["character_card"]["card_scope"]["scope_type"] == "full-series"
    assert protagonist["content"]["card_schema"]["character_card"]["core"]["cast_markers"] == {
        "primary_alignment": "protagonist",
        "is_protagonist": True,
        "is_antagonist": False,
        "is_supporting": False,
        "is_ensemble": False,
    }

    character_index_path = project_root / "1-Cards" / "2-角色卡" / "角色索引.json"
    character_index = json.loads(character_index_path.read_text(encoding="utf-8"))
    assert character_index["meta"]["source_skill_id"] == "story-cards-character"
    assert character_index["meta"]["source_route"] == "0-Init > story-cards > 角色卡/SKILL.md"
    assert character_index["content"]["module_route"] == "story-cards > 角色卡/SKILL.md"
    assert character_index["content"]["type_stack_ref"]["primary"] == "网文高冲击"
    assert character_index["content"]["loaded_references"] == [
        "SKILL.md",
        "CONTEXT.md",
        "角色卡/SKILL.md",
        "角色卡/CONTEXT.md",
        "角色卡/templates/character-card.json",
    ]
    assert character_index["content"]["writeback_plan"]["target_paths"] == [
        "1-Cards/2-角色卡/角色索引.json",
        "1-Cards/2-角色卡/角色关系图谱.md",
    ]
    assert character_index["content"]["relationship_graph"]["path"] == "1-Cards/2-角色卡/角色关系图谱.md"
    assert character_index["gate_summary"]["status"] == "PASS"

    relationship_graph_path = project_root / "1-Cards" / "2-角色卡" / "角色关系图谱.md"
    relationship_graph = relationship_graph_path.read_text(encoding="utf-8")
    assert "# 角色关系图谱" in relationship_graph
    assert "## 文字说明" in relationship_graph
    assert "```mermaid" in relationship_graph
    assert "[主角] 林舟" in relationship_graph
    assert "[反派] 赵竞" in relationship_graph

    coverage_report = cards_coverage_validator.build_cards_coverage_report(project_root)
    assert coverage_report["ok"] is True
    assert coverage_report["sections"]["globals"]["trace"]["module_route"] == "story-cards > 全局卡/SKILL.md"
    assert coverage_report["sections"]["styles"]["trace"]["module_route"] == "story-cards > 风格卡/SKILL.md"
    assert coverage_report["sections"]["characters"]["trace"]["module_route"] == "story-cards > 角色卡/SKILL.md"


def test_cards_writer_cleans_empty_lock_files_by_default(tmp_path):
    cards_writer, _cards_coverage_validator, security_utils = _load_modules()
    project_root = _make_project_root(tmp_path)

    if not security_utils.HAS_FILELOCK:
        return

    report = cards_writer.write_cards_payload(project_root, _build_payload(), run_gate=False)

    assert report["cleanup_empty_lock_on_release"] is True
    assert list(project_root.rglob("*.lock")) == []


def test_cards_writer_can_keep_empty_lock_files_when_requested(tmp_path):
    cards_writer, _cards_coverage_validator, security_utils = _load_modules()
    project_root = _make_project_root(tmp_path)
    payload = _build_payload()
    payload["cleanup_empty_lock_on_release"] = False

    if not security_utils.HAS_FILELOCK:
        return

    report = cards_writer.write_cards_payload(project_root, payload, run_gate=False)

    lock_files = list(project_root.rglob("*.lock"))
    assert report["cleanup_empty_lock_on_release"] is False
    assert lock_files
