#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import sys
from pathlib import Path


def test_extract_state_summary_accepts_dominant_key(tmp_path):
    scripts_dir = Path(__file__).resolve().parents[2]
    if str(scripts_dir) not in sys.path:
        sys.path.insert(0, str(scripts_dir))

    from extract_chapter_context import extract_state_summary

    state = {
        "progress": {"current_chapter": 12, "total_words": 12345},
        "protagonist_state": {
            "power": {"realm": "筑基", "layer": 2},
            "location": "宗门",
            "golden_finger": {"name": "系统", "level": 1},
        },
        "strand_tracker": {
            "history": [
                {"chapter": 10, "dominant": "quest"},
                {"chapter": 11, "dominant": "fire"},
            ]
        },
    }

    (tmp_path / "STATE.json").write_text(json.dumps(state, ensure_ascii=False), encoding="utf-8")

    text = extract_state_summary(tmp_path)
    assert "Ch10:quest" in text
    assert "Ch11:fire" in text


def test_extract_chapter_outline_supports_hyphen_filename(tmp_path):
    scripts_dir = Path(__file__).resolve().parents[2]
    if str(scripts_dir) not in sys.path:
        sys.path.insert(0, str(scripts_dir))

    from extract_chapter_context import extract_chapter_outline

    (tmp_path / "STATE.json").write_text("{}", encoding="utf-8")
    outline_dir = tmp_path / "2-Planning" / "legacy"
    outline_dir.mkdir(parents=True, exist_ok=True)
    (outline_dir / "第1卷-详细大纲.md").write_text("### 第1章：测试标题\n测试大纲", encoding="utf-8")

    outline = extract_chapter_outline(tmp_path, 1)
    assert "### 第1章：测试标题" in outline
    assert "测试大纲" in outline


def test_extract_chapter_outline_prefers_holomap_over_legacy_outline(tmp_path):
    scripts_dir = Path(__file__).resolve().parents[2]
    if str(scripts_dir) not in sys.path:
        sys.path.insert(0, str(scripts_dir))

    from extract_chapter_context import extract_chapter_outline

    planning_dir = tmp_path / "2-Planning"
    planning_dir.mkdir(parents=True, exist_ok=True)
    holomap = {
        "schema_version": "story2026/holomap/v1",
        "content": {
            "holomap": {
                "chapter_boards": [
                    {
                        "chapter": 1,
                        "title": "地图标题",
                        "summary": "地图摘要",
                        "events": ["地图事件A"],
                        "conflicts": [{"title": "地图冲突", "status": "进行中"}],
                    }
                ]
            }
        },
    }
    (planning_dir / "全息地图.json").write_text(json.dumps(holomap, ensure_ascii=False), encoding="utf-8")

    outline_dir = tmp_path / "2-Planning" / "legacy"
    outline_dir.mkdir(parents=True, exist_ok=True)
    (outline_dir / "第1卷-详细大纲.md").write_text("### 第1章：旧大纲标题\n旧大纲内容", encoding="utf-8")

    outline = extract_chapter_outline(tmp_path, 1)
    assert "### 第1章：地图标题" in outline
    assert "地图摘要" in outline
    assert "地图事件A" in outline
    assert "旧大纲内容" not in outline


def test_extract_chapter_outline_prefers_state_volume_mapping(tmp_path):
    scripts_dir = Path(__file__).resolve().parents[2]
    if str(scripts_dir) not in sys.path:
        sys.path.insert(0, str(scripts_dir))

    from extract_chapter_context import extract_chapter_outline

    state = {
        "progress": {
            "volumes_planned": [
                {"volume": 1, "chapters_range": "1-10"},
                {"volume": 2, "chapters_range": "11-20"},
            ]
        }
    }
    (tmp_path / "STATE.json").write_text(json.dumps(state, ensure_ascii=False), encoding="utf-8")

    outline_dir = tmp_path / "2-Planning" / "legacy"
    outline_dir.mkdir(parents=True, exist_ok=True)
    (outline_dir / "第2卷-详细大纲.md").write_text("### 第12章：V2标题\nV2大纲", encoding="utf-8")

    outline = extract_chapter_outline(tmp_path, 12)
    assert "### 第12章：V2标题" in outline
    assert "V2大纲" in outline


def test_extract_chapter_outline_falls_back_when_state_has_no_match(tmp_path):
    scripts_dir = Path(__file__).resolve().parents[2]
    if str(scripts_dir) not in sys.path:
        sys.path.insert(0, str(scripts_dir))

    from extract_chapter_context import extract_chapter_outline

    state = {"progress": {"volumes_planned": [{"volume": 1, "chapters_range": "1-10"}]}}
    (tmp_path / "STATE.json").write_text(json.dumps(state, ensure_ascii=False), encoding="utf-8")

    outline_dir = tmp_path / "2-Planning" / "legacy"
    outline_dir.mkdir(parents=True, exist_ok=True)
    (outline_dir / "第2卷-详细大纲.md").write_text("### 第60章：V2标题\nV2大纲", encoding="utf-8")

    outline = extract_chapter_outline(tmp_path, 60)
    assert "### 第60章：V2标题" in outline
    assert "V2大纲" in outline


def test_build_chapter_context_payload_includes_contract_sections(tmp_path):
    scripts_dir = Path(__file__).resolve().parents[2]
    if str(scripts_dir) not in sys.path:
        sys.path.insert(0, str(scripts_dir))

    from extract_chapter_context import build_chapter_context_payload
    from data_modules.config import DataModulesConfig
    from data_modules.index_manager import IndexManager, ChapterReadingPowerMeta, ReviewMetrics

    cfg = DataModulesConfig.from_project_root(tmp_path)
    cfg.ensure_dirs()

    state = {
        "project": {"genre": "xuanhuan"},
        "project_info": {"genre": "xuanhuan"},
        "progress": {"current_chapter": 3, "total_words": 9000},
        "protagonist_state": {
            "power": {"realm": "筑基", "layer": 2},
            "location": "宗门",
            "golden_finger": {"name": "系统", "level": 1},
        },
        "strand_tracker": {"history": [{"chapter": 2, "dominant": "quest"}]},
        "chapter_meta": {},
        "disambiguation_warnings": [],
        "disambiguation_pending": [],
    }
    (project_root := tmp_path / "STATE.json").write_text(json.dumps(state, ensure_ascii=False), encoding="utf-8")

    summaries_dir = cfg.webnovel_dir / "summaries"
    summaries_dir.mkdir(parents=True, exist_ok=True)
    (summaries_dir / "ch0002.md").write_text("## 剧情摘要\n上一章总结", encoding="utf-8")

    outline_dir = tmp_path / "2-Planning" / "legacy"
    outline_dir.mkdir(parents=True, exist_ok=True)
    (outline_dir / "第1卷 详细大纲.md").write_text("### 第3章：测试标题\n测试大纲", encoding="utf-8")

    refs_dir = tmp_path / ".agents" / "skills" / "story" / "_shared"
    refs_dir.mkdir(parents=True, exist_ok=True)
    (refs_dir / "genre-profiles.md").write_text("## xuanhuan\n- 升级线清晰", encoding="utf-8")
    (refs_dir / "reading-power-taxonomy.md").write_text("## xuanhuan\n- 悬念钩优先", encoding="utf-8")

    global_card_dir = tmp_path / "1-Cards" / "0-全局卡" / "总设定"
    global_card_dir.mkdir(parents=True, exist_ok=True)
    global_card_ref = "1-Cards/0-全局卡/总设定/世界总卡.json"
    (tmp_path / "1-Cards" / "0-全局卡" / "全局索引.json").write_text(
        json.dumps(
            {
                "content": {
                    "card_groups": {"master_globals": [global_card_ref]},
                    "global_contract_refs": [{"card_id": "世界总卡", "path": global_card_ref}],
                }
            },
            ensure_ascii=False,
            indent=2,
        ),
        encoding="utf-8",
    )
    (tmp_path / global_card_ref).write_text(
        json.dumps(
            {
                "content": {
                    "card_schema": {
                        "global_card": {
                            "core": {
                                "worldview": {"genre": "xuanhuan"},
                                "rule_system": [{"label": "铁律", "value": "越级有代价"}],
                                "golden_finger": {"name": "系统", "limits": ["每日一次"]},
                            }
                        }
                    }
                }
            },
            ensure_ascii=False,
            indent=2,
        ),
        encoding="utf-8",
    )

    protagonist_card_path = tmp_path / "1-Cards" / "2-角色卡" / "主要角色" / "李青.json"
    protagonist_card_path.parent.mkdir(parents=True, exist_ok=True)
    protagonist_card_path.write_text(
        json.dumps(
            {
                "content": {
                    "card_schema": {
                        "character_card": {
                            "card_id": "李青",
                            "core": {
                                "identity": {"name": "李青"},
                                "cast_markers": {"primary_alignment": "protagonist", "is_protagonist": True},
                                "growth_contract": {
                                    "growth_enabled": True,
                                    "growth_role": "protagonist",
                                },
                            },
                            "current_state": {
                                "growth_state": {
                                    "active_arc_phase": "破局前夜",
                                    "latest_growth_episode": "第2集",
                                    "skill": {"stage": "稳固", "focus": "先稳手上余劲"},
                                    "heart": {"stage": "裂开", "recent_shift": "开始怀疑自己赢得是否太快"},
                                    "emotion": {"stage": "松动", "current_tension": "不敢再把同门推远"},
                                }
                            },
                        }
                    }
                }
            },
            ensure_ascii=False,
            indent=2,
        ),
        encoding="utf-8",
    )

    idx = IndexManager(cfg)
    idx.save_chapter_reading_power(
        ChapterReadingPowerMeta(chapter=2, hook_type="悬念钩", hook_strength="strong", coolpoint_patterns=["身份掉马"])
    )
    idx.save_review_metrics(
        ReviewMetrics(start_chapter=1, end_chapter=2, overall_score=71, dimension_scores={"plot": 71})
    )

    payload = build_chapter_context_payload(tmp_path, 3, current_step_id="Step 2")
    assert payload["context_contract_version"] == "v2"
    assert payload.get("context_weight_stage") in {"early", "mid", "late"}
    assert "writing_guidance" in payload
    assert "validation_fact_pack" in payload
    fact_pack = payload["validation_fact_pack"]
    assert {"draft_snapshot", "cards_truth", "planning_truth", "init_truth", "runtime_context"}.issubset(fact_pack.keys())
    assert fact_pack["draft_snapshot"]["manuscript_ref"] == "3-Drafting/第3集.md"
    assert fact_pack["planning_truth"]["promise_slice"]["global_contract_refs"] == [global_card_ref]
    assert fact_pack["cards_truth"]["global_truth_slice"]["global_contract_summary"]["golden_finger"]["name"] == "系统"
    growth_snapshot = fact_pack["cards_truth"]["cards_state_history_slice"]["protagonist_growth_snapshot"]
    assert growth_snapshot["character_name"] == "李青"
    assert growth_snapshot["growth_enabled"] is True
    assert growth_snapshot["latest_growth_episode"] == "第2集"
    assert "开始怀疑自己赢得是否太快" in growth_snapshot["carry_signals"]
    assert fact_pack["runtime_context"]["state_summary"]
    assert isinstance(payload["writing_guidance"].get("guidance_items"), list)
    assert isinstance(payload["writing_guidance"].get("checklist"), list)
    assert isinstance(payload["writing_guidance"].get("checklist_score"), dict)
    assert payload["genre_profile"].get("genre") == "xuanhuan"
    assert "_base" in (payload["type_pack_profile"].get("active_packs") or [])
    assert "rag_assist" in payload
    assert isinstance(payload["rag_assist"], dict)
    assert payload["rag_assist"].get("invoked") is False
    assert payload["current_step_id"] == "Step 2"


def test_render_text_contains_writing_guidance_section(tmp_path):
    scripts_dir = Path(__file__).resolve().parents[2]
    if str(scripts_dir) not in sys.path:
        sys.path.insert(0, str(scripts_dir))

    from extract_chapter_context import _render_text

    payload = {
        "chapter": 10,
        "outline": "测试大纲",
        "previous_summaries": ["### 第9章摘要\n上一章"],
        "state_summary": "状态",
        "context_contract_version": "v2",
        "context_weight_stage": "early",
        "current_step_id": "Step 6",
        "reader_signal": {"review_trend": {"overall_avg": 72}, "low_score_ranges": [{"start_chapter": 8, "end_chapter": 9}]},
        "genre_profile": {
            "genre": "xuanhuan",
            "genres": ["xuanhuan", "realistic"],
            "composite_hints": ["以玄幻主线推进，同时保留现实议题表达"],
            "reference_hints": ["升级线清晰"],
        },
        "writing_guidance": {
            "guidance_items": ["先修低分", "钩子差异化"],
            "checklist": [
                {
                    "id": "fix_low_score_range",
                    "label": "修复低分区间问题",
                    "weight": 1.4,
                    "required": True,
                    "source": "reader_signal.low_score_ranges",
                    "verify_hint": "至少完成1处冲突升级",
                }
            ],
            "checklist_score": {
                "score": 81.5,
                "completion_rate": 0.66,
                "required_completion_rate": 0.75,
            },
            "methodology": {
                "enabled": True,
                "framework": "digital-serial-v1",
                "pilot": "xianxia",
                "genre_profile_key": "xianxia",
                "chapter_stage": "confront",
                "observability": {
                    "next_reason_clarity": 78.0,
                    "anchor_effectiveness": 74.0,
                    "rhythm_naturalness": 72.0,
                },
                "signals": {"risk_flags": ["pattern_overuse_watch"]},
            },
        },
    }

    text = _render_text(payload)
    assert "## 本章规划节点" in text
    assert "## 当前工序" in text
    assert "## 写作执行建议" in text
    assert "先修低分" in text
    assert "## Contract (v2)" in text
    assert "- 上下文阶段权重: early" in text
    assert "### 执行检查清单（可评分）" in text
    assert "- 总权重: 1.40" in text
    assert "[必做][w=1.4] 修复低分区间问题" in text
    assert "### 执行评分" in text
    assert "- 评分: 81.5" in text
    assert "- 复合题材: xuanhuan + realistic" in text
    assert "## 长篇方法论策略" in text
    assert "- 适用题材: xianxia" in text
    assert "next_reason=78.0" in text


def test_render_text_contains_rag_assist_section_when_hits_exist(tmp_path):
    scripts_dir = Path(__file__).resolve().parents[2]
    if str(scripts_dir) not in sys.path:
        sys.path.insert(0, str(scripts_dir))

    from extract_chapter_context import _render_text

    payload = {
        "chapter": 12,
        "outline": "测试大纲",
        "previous_summaries": [],
        "state_summary": "状态",
        "context_contract_version": "v2",
        "reader_signal": {},
        "genre_profile": {},
        "writing_guidance": {},
        "rag_assist": {
            "invoked": True,
            "mode": "auto",
            "intent": "relationship",
            "query": "第12章 人物关系与动机：萧炎与药老发生冲突",
            "hits": [
                {
                    "chapter": 9,
                    "scene_index": 2,
                    "source": "graph_hybrid",
                    "score": 0.91,
                    "content": "萧炎与药老在修炼方向上发生分歧。",
                }
            ],
        },
    }

    text = _render_text(payload)
    assert "## RAG 检索线索" in text
    assert "- 模式: auto" in text
    assert "[graph_hybrid]" in text
    assert "萧炎与药老" in text
