#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
extract_chapter_context.py - extract chapter writing context

Features:
- chapter planning snippet (chapter-plan-first, holomap compatibility fallback)
- previous chapter summaries (prefers .webnovel/summaries)
- compact state summary
- ContextManager contract sections (reader_signal / genre_profile / writing_guidance)
"""

from __future__ import annotations

import argparse
import asyncio
import json
import re
import sys
from pathlib import Path
from typing import Any, Dict, List

from chapter_outline_loader import load_chapter_outline, load_holomap_chapter_context
from planning_paths import (
    canonical_book_plan_path,
    canonical_book_plan_relpath,
    canonical_chapter_plan_path,
    canonical_chapter_plan_relpath,
    canonical_volume_plan_path,
    canonical_volume_plan_relpath,
    planning_volume_num_for_chapter,
)

from runtime_compat import enable_windows_utf8_stdio

try:
    import yaml
except ImportError:  # pragma: no cover
    yaml = None

try:
    from chapter_paths import drafting_root_md_path, find_chapter_file
except ImportError:  # pragma: no cover
    from scripts.chapter_paths import drafting_root_md_path, find_chapter_file


def _ensure_scripts_path():
    scripts_dir = Path(__file__).resolve().parent
    if str(scripts_dir) not in sys.path:
        sys.path.insert(0, str(scripts_dir))


_RAG_TRIGGER_KEYWORDS = (
    "关系",
    "恩怨",
    "冲突",
    "敌对",
    "同盟",
    "师徒",
    "身份",
    "线索",
    "伏笔",
    "回收",
    "地点",
    "势力",
    "真相",
    "来历",
)


def find_project_root(start_path: Path | None = None) -> Path:
    """解析真实书项目根（包含 `STATE.json` 的目录）。"""
    from project_locator import resolve_project_root

    if start_path is None:
        return resolve_project_root()
    return resolve_project_root(str(start_path))


def extract_chapter_outline(project_root: Path, chapter_num: int) -> str:
    """Extract chapter planning segment, preferring canonical chapter plans over compatibility carriers."""
    return load_chapter_outline(project_root, chapter_num, max_chars=1500)


def _load_summary_file(project_root: Path, chapter_num: int) -> str:
    """Load summary section from `.webnovel/summaries/chNNNN.md`."""
    summary_path = project_root / ".webnovel" / "summaries" / f"ch{chapter_num:04d}.md"
    if not summary_path.exists():
        return ""

    text = summary_path.read_text(encoding="utf-8")
    summary_match = re.search(r"##\s*剧情摘要\s*\r?\n(.+?)(?=\r?\n##|$)", text, re.DOTALL)
    if summary_match:
        return summary_match.group(1).strip()
    return ""


def extract_chapter_summary(project_root: Path, chapter_num: int) -> str:
    """Extract chapter summary, fallback to chapter body head."""
    summary = _load_summary_file(project_root, chapter_num)
    if summary:
        return summary

    chapter_file = find_chapter_file(project_root, chapter_num)
    if not chapter_file or not chapter_file.exists():
        return f"⚠️ 第{chapter_num}章文件不存在"

    content = chapter_file.read_text(encoding="utf-8")

    summary_match = re.search(r"##\s*本章摘要\s*\r?\n(.+?)(?=\r?\n##|$)", content, re.DOTALL)
    if summary_match:
        return summary_match.group(1).strip()

    stats_match = re.search(r"##\s*本章统计\s*\r?\n(.+?)(?=\r?\n##|$)", content, re.DOTALL)
    if stats_match:
        return f"[无摘要，仅统计]\n{stats_match.group(1).strip()}"

    lines = content.split("\n")
    text_lines = [line for line in lines if not line.startswith("#") and line.strip()]
    text = "\n".join(text_lines)[:500]
    return f"[自动截取前500字]\n{text}..."


def extract_state_summary(project_root: Path) -> str:
    """Extract key fields from `STATE.json`."""
    from project_locator import resolve_state_file

    state_file = resolve_state_file(explicit_project_root=str(project_root))
    if not state_file.exists():
        return "⚠️ STATE.json 不存在"

    state = json.loads(state_file.read_text(encoding="utf-8"))
    summary_parts: List[str] = []

    if "progress" in state:
        progress = state["progress"]
        summary_parts.append(
            f"**进度**: 第{progress.get('current_chapter', '?')}章 / {progress.get('total_words', '?')}字"
        )

    if "protagonist_state" in state:
        ps = state["protagonist_state"]
        power = ps.get("power", {})
        summary_parts.append(f"**主角实力**: {power.get('realm', '?')} {power.get('layer', '?')}层")
        summary_parts.append(f"**当前位置**: {ps.get('location', '?')}")
        golden_finger = ps.get("golden_finger", {})
        summary_parts.append(
            f"**金手指**: {golden_finger.get('name', '?')} Lv.{golden_finger.get('level', '?')}"
        )

    if "strand_tracker" in state:
        tracker = state["strand_tracker"]
        history = tracker.get("history", [])[-5:]
        if history:
            items: List[str] = []
            for row in history:
                if not isinstance(row, dict):
                    continue
                chapter = row.get("chapter", "?")
                strand = row.get("strand") or row.get("dominant") or "unknown"
                items.append(f"Ch{chapter}:{strand}")
            if items:
                summary_parts.append(f"**近5章Strand**: {', '.join(items)}")

    plot_threads = state.get("plot_threads", {}) if isinstance(state.get("plot_threads"), dict) else {}
    foreshadowing = plot_threads.get("foreshadowing", [])
    if isinstance(foreshadowing, list) and foreshadowing:
        active = [row for row in foreshadowing if row.get("status") in {"active", "未回收"}]
        urgent = [row for row in active if row.get("urgency", 0) > 50]
        if urgent:
            urgent_list = [
                f"{row.get('content', '?')[:30]}... (紧急度:{row.get('urgency')})"
                for row in urgent[:3]
            ]
            summary_parts.append(f"**紧急伏笔**: {'; '.join(urgent_list)}")

    return "\n".join(summary_parts)


def _normalize_outline_text(outline: str) -> str:
    text = str(outline or "")
    if not text or text.startswith("⚠️"):
        return ""
    text = re.sub(r"^#+\s*", "", text, flags=re.MULTILINE)
    text = re.sub(r"\s+", " ", text).strip()
    return text


def _build_rag_query(outline: str, chapter_num: int, min_chars: int, max_chars: int) -> str:
    plain = _normalize_outline_text(outline)
    if not plain or len(plain) < min_chars:
        return ""

    if not any(keyword in plain for keyword in _RAG_TRIGGER_KEYWORDS):
        return ""

    if "关系" in plain or "师徒" in plain or "敌对" in plain or "同盟" in plain:
        topic = "人物关系与动机"
    elif "地点" in plain or "势力" in plain:
        topic = "地点势力与场景约束"
    elif "伏笔" in plain or "线索" in plain or "回收" in plain:
        topic = "伏笔与线索"
    else:
        topic = "剧情关键线索"

    clean_max = max(40, int(max_chars))
    return f"第{chapter_num}章 {topic}：{plain[:clean_max]}"


def _load_protagonist_growth_snapshot(project_root: Path) -> Dict[str, Any]:
    protagonist_dir = project_root / "1-Cards" / "2-角色卡" / "主要角色"
    if not protagonist_dir.is_dir():
        return {}

    for path in sorted(protagonist_dir.glob("*.json")):
        try:
            payload = json.loads(path.read_text(encoding="utf-8"))
        except Exception:
            continue

        card = (
            ((payload.get("content") or {}).get("card_schema") or {}).get("character_card")
            if isinstance(payload, dict)
            else None
        )
        if not isinstance(card, dict):
            continue

        core = card.get("core") or {}
        current_state = card.get("current_state") or {}
        growth_contract = core.get("growth_contract") or {}
        growth_state = current_state.get("growth_state") or {}
        cast_markers = core.get("cast_markers") or {}
        if growth_contract.get("growth_enabled") is not True and cast_markers.get("is_protagonist") is not True:
            continue

        identity = core.get("identity") or {}
        skill = growth_state.get("skill") or {}
        heart = growth_state.get("heart") or {}
        emotion = growth_state.get("emotion") or {}
        carry_signals: List[str] = []
        for value in (
            skill.get("focus"),
            skill.get("recent_gain"),
            skill.get("current_tension"),
            heart.get("recent_shift"),
            heart.get("current_tension"),
            emotion.get("recent_shift"),
            emotion.get("current_tension"),
        ):
            text = str(value or "").strip()
            if text and text not in carry_signals:
                carry_signals.append(text)

        return {
            "character_name": str(identity.get("name") or card.get("card_id") or path.stem),
            "growth_enabled": bool(growth_contract.get("growth_enabled")),
            "growth_role": str(growth_contract.get("growth_role") or ""),
            "active_arc_phase": str(growth_state.get("active_arc_phase") or ""),
            "latest_growth_episode": str(growth_state.get("latest_growth_episode") or ""),
            "skill_stage": str((skill or {}).get("stage") or ""),
            "heart_stage": str((heart or {}).get("stage") or ""),
            "emotion_stage": str((emotion or {}).get("stage") or ""),
            "carry_signals": carry_signals,
        }
    return {}


def _load_story_source_manifest_summary(project_root: Path) -> Dict[str, Any]:
    manifest_path = project_root / "0-Init" / "story-source-manifest.yaml"
    if not manifest_path.is_file() or yaml is None:
        return {}

    try:
        payload = yaml.safe_load(manifest_path.read_text(encoding="utf-8"))
    except Exception:
        return {}
    if not isinstance(payload, dict):
        return {}

    primary = payload.get("primary_story_source") if isinstance(payload.get("primary_story_source"), dict) else {}
    auxiliary = payload.get("auxiliary_sources") if isinstance(payload.get("auxiliary_sources"), list) else []
    briefs = payload.get("development_briefs") if isinstance(payload.get("development_briefs"), list) else []

    drafting_titles: List[str] = []
    coverage_notes: List[str] = []
    source_refs: List[str] = []
    for item in auxiliary:
        if not isinstance(item, dict):
            continue
        title = str(item.get("title") or "").strip()
        authoritative_for = {str(v).strip() for v in (item.get("authoritative_for") or []) if str(v).strip()}
        paths = [str(v).strip() for v in (item.get("paths") or []) if str(v).strip()]
        coverage = str(item.get("coverage_scope") or "").strip()
        if title and ("3-Drafting" in authoritative_for or item.get("source_type") in {"style_card", "character_bundle"}):
            drafting_titles.append(title)
        if coverage and coverage not in coverage_notes:
            coverage_notes.append(coverage)
        for path in paths:
            if path and path not in source_refs:
                source_refs.append(path)

    brief_titles: List[str] = []
    for item in briefs:
        if not isinstance(item, dict):
            continue
        title = str(item.get("title") or "").strip()
        if title:
            brief_titles.append(title)
        for path in (item.get("source_refs") or []):
            ref = str(path).strip()
            if ref and ref not in source_refs:
                source_refs.append(ref)

    return {
        "manifest_ref": "0-Init/story-source-manifest.yaml",
        "primary_story_source_status": str(primary.get("status") or "").strip(),
        "primary_coverage_scope": str(primary.get("coverage_scope") or "").strip(),
        "drafting_auxiliary_titles": drafting_titles[:6],
        "coverage_notes": coverage_notes[:8],
        "development_brief_titles": brief_titles[:6],
        "legacy_source_refs": source_refs[:12],
        "sequel_mode": bool(auxiliary or briefs),
    }


def _load_json_object(path: Path) -> Dict[str, Any]:
    if not path.is_file():
        return {}
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return {}
    return payload if isinstance(payload, dict) else {}


def _extract_holomap_slice_root(payload: Dict[str, Any]) -> Dict[str, Any]:
    content = payload.get("content")
    if isinstance(content, dict):
        holomap_slice = content.get("holomap_slice")
        if isinstance(holomap_slice, dict):
            return holomap_slice
    holomap_slice = payload.get("holomap_slice")
    return holomap_slice if isinstance(holomap_slice, dict) else {}


def _safe_dict(value: Any) -> Dict[str, Any]:
    return value if isinstance(value, dict) else {}


def _safe_list(value: Any) -> List[Any]:
    return value if isinstance(value, list) else []


def _extract_chapter_num(value: Any) -> int | None:
    if isinstance(value, int):
        return value if value > 0 else None
    text = str(value or "").strip()
    if not text:
        return None
    match = re.search(r"(\d+)", text)
    if not match:
        return None
    parsed = int(match.group(1))
    return parsed if parsed > 0 else None


def _select_episode_rhythm_role(
    roles: Any,
    *,
    chapter_num: int,
    episode_ref: str,
) -> Dict[str, Any]:
    best_match: Dict[str, Any] = {}
    for item in _safe_list(roles):
        role = _safe_dict(item)
        if not role:
            continue
        selector = str(
            role.get("episode_selector")
            or role.get("episode_ref")
            or role.get("chapter_ref")
            or role.get("chapter_selector")
            or ""
        ).strip()
        if selector == episode_ref:
            return role
        if selector and _extract_chapter_num(selector) == chapter_num:
            best_match = role
    if best_match:
        return best_match
    if len(_safe_list(roles)) == 1:
        return _safe_dict(_safe_list(roles)[0])
    return {}


def _load_episode_rhythm_handoff(project_root: Path, planning_ctx: Dict[str, Any], chapter_num: int) -> Dict[str, Any]:
    episode_ref = f"第{chapter_num}集"
    board = _safe_dict(planning_ctx.get("chapter_board"))
    slice_path_raw = str(planning_ctx.get("slice_path") or "").strip()
    slice_root = _extract_holomap_slice_root(_load_json_object(Path(slice_path_raw))) if slice_path_raw else {}

    framework = _safe_dict(slice_root.get("episode_rhythm_framework")) or _safe_dict(board.get("episode_rhythm_framework"))
    role = _select_episode_rhythm_role(
        slice_root.get("episode_rhythm_roles"),
        chapter_num=chapter_num,
        episode_ref=episode_ref,
    ) or _safe_dict(board.get("episode_rhythm_role"))
    slice_style_contract = _safe_dict(slice_root.get("slice_style_contract"))

    if not framework and not role and not slice_style_contract:
        return {}

    entry_promise = str(role.get("entry_promise") or slice_style_contract.get("entry_promise") or "").strip()
    exit_hook = str(role.get("exit_hook") or slice_style_contract.get("exit_hook") or "").strip()

    return {
        "episode_ref": episode_ref,
        "framework_ref": str(planning_ctx.get("slice_ref") or "").strip(),
        "framework_path": slice_path_raw,
        "framework": framework,
        "role": role,
        "selected_pack_id": str(role.get("selected_pack_id") or framework.get("default_pack_id") or "").strip(),
        "selected_pack_label": str(role.get("selected_pack_label") or framework.get("default_pack_label") or "").strip(),
        "selected_mode_id": str(role.get("selected_mode_id") or "").strip(),
        "selected_mode_label": str(role.get("selected_mode_label") or "").strip(),
        "yin_yang_polarity": str(role.get("yin_yang_polarity") or "").strip(),
        "polarity_sequence_note": str(role.get("polarity_sequence_note") or "").strip(),
        "why_this_pack": str(role.get("why_this_pack") or "").strip(),
        "entry_promise": entry_promise,
        "exit_hook": exit_hook,
        "base_spine_projection": [item for item in _safe_list(role.get("base_spine_projection")) if isinstance(item, dict)],
    }


def _split_planning_obligation_fragments(value: Any) -> List[str]:
    fragments: List[str] = []
    if isinstance(value, list):
        for item in value:
            fragments.extend(_split_planning_obligation_fragments(item))
        return fragments

    text = str(value or "").strip()
    if not text:
        return fragments

    normalized = text
    for token in (
        "而是",
        "代价是",
        "由此",
        "却先",
        "却看见",
        "却",
        "只想",
        "第一次",
        "切回",
    ):
        normalized = normalized.replace(token, f"|{token}")

    for chunk in re.split(r"[|，,；;。]+", normalized):
        item = chunk.strip("“”\"' \t\r\n")
        if len(item) >= 4 and item not in fragments:
            fragments.append(item)
    if not fragments and len(text) >= 4:
        fragments.append(text)
    return fragments


def _split_story_beats(value: Any) -> List[str]:
    text = str(value or "").strip()
    if not text:
        return []

    normalized = text
    for token in ("；", ";", "再一刀反切到", "画面猛然反切到", "却很快", "随后", "最后", "接着"):
        normalized = normalized.replace(token, "|")

    beats: List[str] = []
    for chunk in normalized.split("|"):
        item = chunk.strip("“”\"' \t\r\n，,。")
        if len(item) < 6:
            continue
        if item not in beats:
            beats.append(item)
    return beats


def _is_reflective_fragment(fragment: str) -> bool:
    text = str(fragment or "").strip()
    return any(marker in text for marker in ("不是单一", "意味着", "核心仍是", "真正看到", "风险如果太弱"))


def _is_actionable_planning_fragment(fragment: str) -> bool:
    text = str(fragment or "").strip()
    if len(text) < 4:
        return False

    # Planning thread ids like `event-001` / `conf-001` are routing tokens, not prose obligations.
    if re.fullmatch(r"(?:event|conf|mission|clue|foe|edge)-\d+", text):
        return False

    meta_markers = (
        "第一卷",
        "第二卷",
        "第三卷",
        "第四卷",
        "第五卷",
        "第六卷",
        "时间压力",
        "由此落锁",
        "本章承担",
        "本章关键角色",
    )
    if any(marker in text for marker in meta_markers):
        return False

    return True


def _search_with_rag(
    project_root: Path,
    chapter_num: int,
    query: str,
    top_k: int,
) -> Dict[str, Any]:
    _ensure_scripts_path()
    from data_modules.config import DataModulesConfig
    from data_modules.rag_adapter import RAGAdapter

    config = DataModulesConfig.from_project_root(project_root)
    adapter = RAGAdapter(config)
    intent_payload = adapter.query_router.route_intent(query)
    center_entities = list(intent_payload.get("entities") or [])

    results = []
    mode = "auto"
    fallback_reason = ""
    has_embed_key = bool(str(getattr(config, "embed_api_key", "") or "").strip())
    if has_embed_key:
        try:
            results = asyncio.run(
                adapter.search(
                    query=query,
                    top_k=top_k,
                    strategy="auto",
                    chapter=chapter_num,
                    center_entities=center_entities,
                )
            )
        except Exception as exc:
            fallback_reason = f"auto_failed:{exc.__class__.__name__}"
            mode = "bm25_fallback"
            results = adapter.bm25_search(query=query, top_k=top_k, chapter=chapter_num)
    else:
        mode = "bm25_fallback"
        fallback_reason = "missing_embed_api_key"
        results = adapter.bm25_search(query=query, top_k=top_k, chapter=chapter_num)

    hits: List[Dict[str, Any]] = []
    for row in results:
        content = re.sub(r"\s+", " ", str(getattr(row, "content", "") or "")).strip()
        hits.append(
            {
                "chunk_id": str(getattr(row, "chunk_id", "") or ""),
                "chapter": int(getattr(row, "chapter", 0) or 0),
                "scene_index": int(getattr(row, "scene_index", 0) or 0),
                "score": round(float(getattr(row, "score", 0.0) or 0.0), 6),
                "source": str(getattr(row, "source", "") or mode),
                "source_file": str(getattr(row, "source_file", "") or ""),
                "content": content[:180],
            }
        )

    return {
        "invoked": True,
        "query": query,
        "mode": mode,
        "reason": fallback_reason or ("ok" if hits else "no_hit"),
        "intent": intent_payload.get("intent"),
        "needs_graph": bool(intent_payload.get("needs_graph")),
        "center_entities": center_entities,
        "hits": hits,
    }


def _load_rag_assist(project_root: Path, chapter_num: int, outline: str) -> Dict[str, Any]:
    _ensure_scripts_path()
    from data_modules.config import DataModulesConfig

    config = DataModulesConfig.from_project_root(project_root)
    enabled = bool(getattr(config, "context_rag_assist_enabled", True))
    top_k = max(1, int(getattr(config, "context_rag_assist_top_k", 4)))
    min_chars = max(20, int(getattr(config, "context_rag_assist_min_outline_chars", 40)))
    max_chars = max(40, int(getattr(config, "context_rag_assist_max_query_chars", 120)))
    base_payload = {"enabled": enabled, "invoked": False, "reason": "", "query": "", "hits": []}

    if not enabled:
        base_payload["reason"] = "disabled_by_config"
        return base_payload

    query = _build_rag_query(outline, chapter_num=chapter_num, min_chars=min_chars, max_chars=max_chars)
    if not query:
        base_payload["reason"] = "outline_not_actionable"
        return base_payload

    vector_db = config.vector_db
    if not vector_db.exists() or vector_db.stat().st_size <= 0:
        base_payload["reason"] = "vector_db_missing_or_empty"
        return base_payload

    try:
        rag_payload = _search_with_rag(project_root=project_root, chapter_num=chapter_num, query=query, top_k=top_k)
        rag_payload["enabled"] = True
        return rag_payload
    except Exception as exc:
        base_payload["reason"] = f"rag_error:{exc.__class__.__name__}"
        return base_payload


def _load_contract_context(project_root: Path, chapter_num: int, current_step_id: str | None = None) -> Dict[str, Any]:
    """Build context via ContextManager and return selected sections."""
    _ensure_scripts_path()
    from data_modules.config import DataModulesConfig
    from data_modules.context_manager import ContextManager

    config = DataModulesConfig.from_project_root(project_root)
    manager = ContextManager(config)
    payload = manager.build_context(
        chapter=chapter_num,
        template="plot",
        use_snapshot=True,
        save_snapshot=True,
        max_chars=8000,
        current_step_id=current_step_id,
    )

    sections = payload.get("sections", {})
    core = (sections.get("core") or {}).get("content", {})
    global_ctx = (sections.get("global") or {}).get("content", {})
    story_skeleton = (sections.get("story_skeleton") or {}).get("content", {})
    writing_guidance = (sections.get("writing_guidance") or {}).get("content", {})
    planning_ctx = load_holomap_chapter_context(project_root, chapter_num)
    episode_rhythm_handoff = _load_episode_rhythm_handoff(project_root, planning_ctx, chapter_num)
    active_foreshadowing = core.get("active_foreshadowing") or []
    story_skeleton_items = story_skeleton if isinstance(story_skeleton, list) else []
    story_skeleton_first = story_skeleton_items[0] if story_skeleton_items and isinstance(story_skeleton_items[0], dict) else {}
    promise_slice = {
        "genre": ((sections.get("genre_profile") or {}).get("content", {}) or {}).get("genre", ""),
        "style_contract_ref": global_ctx.get("style_contract_ref", ""),
        "global_contract_refs": global_ctx.get("global_contract_refs", []),
        "project_preferences": (sections.get("preferences") or {}).get("content", {}) or {},
    }
    volume_num = planning_volume_num_for_chapter(chapter_num, project_root=project_root)
    book_plan_ref = canonical_book_plan_relpath() if canonical_book_plan_path(project_root).is_file() else ""
    volume_plan_ref = canonical_volume_plan_relpath(volume_num) if canonical_volume_plan_path(project_root, volume_num).is_file() else ""
    chapter_plan_ref = (
        canonical_chapter_plan_relpath(chapter_num, volume_num, project_root=project_root)
        if canonical_chapter_plan_path(project_root, chapter_num, volume_num).is_file()
        else ""
    )
    chapter_board = {
        "outline": story_skeleton_first.get("summary", "") if isinstance(story_skeleton_first, dict) else "",
        "chapter_goals": story_skeleton_first.get("chapter_goals", []) if isinstance(story_skeleton_first, dict) else [],
        "must_happen": story_skeleton_first.get("must_happen", []) if isinstance(story_skeleton_first, dict) else [],
        "cannot_change": story_skeleton_first.get("cannot_change", []) if isinstance(story_skeleton_first, dict) else [],
        "story_skeleton_samples": story_skeleton_items,
    }
    slice_board = planning_ctx.get("chapter_board") if isinstance(planning_ctx.get("chapter_board"), dict) else {}
    if slice_board:
        bundled = slice_board.get("bundled_elements") if isinstance(slice_board.get("bundled_elements"), dict) else {}
        planned_state = slice_board.get("planned_state") if isinstance(slice_board.get("planned_state"), dict) else {}
        action_plan = planned_state.get("action_beat_plan") if isinstance(planned_state.get("action_beat_plan"), dict) else {}
        style_execution = planned_state.get("style_execution") if isinstance(planned_state.get("style_execution"), dict) else {}
        emotion_execution = planned_state.get("emotion_execution") if isinstance(planned_state.get("emotion_execution"), dict) else {}
        emotion_beat = planned_state.get("emotion_beat") if isinstance(planned_state.get("emotion_beat"), dict) else {}
        chapter_goal = str(slice_board.get("chapter_goal") or "").strip()
        must_happen = []
        for item in bundled.get("events", []) if isinstance(bundled.get("events"), list) else []:
            for fragment in _split_planning_obligation_fragments(item):
                if _is_actionable_planning_fragment(fragment) and fragment not in must_happen:
                    must_happen.append(fragment)
        for key in ("turning_point", "relationship_change", "injury_or_cost"):
            text = str(action_plan.get(key) or "").strip()
            for fragment in _split_planning_obligation_fragments(text):
                if _is_actionable_planning_fragment(fragment) and fragment not in must_happen:
                    must_happen.append(fragment)

        chapter_goal_fragments = [
            fragment
            for fragment in _split_planning_obligation_fragments(chapter_goal)
            if _is_actionable_planning_fragment(fragment)
        ]
        beat_checkpoints = [
            fragment
            for fragment in _split_story_beats(chapter_goal)
            if fragment and not _is_reflective_fragment(fragment)
        ]
        terminal_beat = beat_checkpoints[-1] if beat_checkpoints else ""

        chapter_board = {
            "outline": str(slice_board.get("chapter_title") or chapter_goal or chapter_board.get("outline") or "").strip(),
            "chapter_goals": chapter_goal_fragments or chapter_board.get("chapter_goals", []),
            "must_happen": must_happen or chapter_board.get("must_happen", []),
            "cannot_change": chapter_board.get("cannot_change", []),
            "story_skeleton_samples": [slice_board],
            "node_id": str(slice_board.get("node_id") or "").strip(),
            "episode_ref": str(slice_board.get("episode_ref") or "").strip(),
            "chapter_title": str(slice_board.get("chapter_title") or "").strip(),
            "bundled_elements": bundled,
            "planned_state": planned_state,
            "action_beat_plan": action_plan,
            "style_execution": style_execution,
            "emotion_execution": emotion_execution,
            "emotion_beat": emotion_beat,
            "beat_checkpoints": beat_checkpoints,
            "terminal_beat": terminal_beat,
            "anti_drift": list(style_execution.get("anti_drift") or []),
            "planning_slice_ref": str(planning_ctx.get("slice_ref") or "").strip(),
            "planning_slice_path": str(planning_ctx.get("slice_path") or "").strip(),
        }
    if episode_rhythm_handoff:
        chapter_board["episode_rhythm_handoff"] = episode_rhythm_handoff
        chapter_board["selected_mode_id"] = episode_rhythm_handoff.get("selected_mode_id", "")
        chapter_board["selected_mode_label"] = episode_rhythm_handoff.get("selected_mode_label", "")
        chapter_board["entry_promise"] = episode_rhythm_handoff.get("entry_promise", "")
        chapter_board["exit_hook"] = episode_rhythm_handoff.get("exit_hook", "")
        chapter_board["base_spine_projection"] = episode_rhythm_handoff.get("base_spine_projection", [])

    def _collect_task_texts(*values: object) -> list[str]:
        items: list[str] = []
        for value in values:
            if isinstance(value, str):
                text = value.strip()
                if text:
                    items.append(text)
            elif isinstance(value, list):
                for item in value:
                    if isinstance(item, str) and item.strip():
                        items.append(item.strip())
        unique: list[str] = []
        seen: set[str] = set()
        for item in items:
            if item not in seen:
                unique.append(item)
                seen.add(item)
        return unique

    planning_task_lineage = planning_ctx.get("task_lineage") if isinstance(planning_ctx.get("task_lineage"), dict) else {}
    planning_task_convergence = (
        planning_ctx.get("task_convergence") if isinstance(planning_ctx.get("task_convergence"), dict) else {}
    )
    chapter_task_relation = {
        "上承卷级任务": str(
            slice_board.get("upstream_volume_task")
            or planning_task_lineage.get("upstream_volume_task")
            or planning_task_lineage.get("upstream_task")
            or ""
        ).strip(),
        "主线": _collect_task_texts(
            slice_board.get("main_task"),
            planning_task_lineage.get("main_task"),
            chapter_board.get("outline"),
        )[:1],
        "支线": _collect_task_texts(
            slice_board.get("branch_tasks"),
            slice_board.get("tasks"),
            planning_task_lineage.get("branch_tasks"),
        ),
        "汇聚动作": str(
            slice_board.get("merge_action")
            or planning_task_convergence.get("merge_action")
            or chapter_board.get("terminal_beat")
            or _safe_dict(chapter_board.get("episode_rhythm_handoff")).get("exit_hook")
            or ""
        ).strip(),
        "未汇聚任务去向": str(
            slice_board.get("open_branch_route")
            or planning_task_convergence.get("open_branch_route")
            or ""
        ).strip(),
    }
    volume_task_relation = {
        "上承部级主任务": str(
            planning_ctx.get("upstream_book_task")
            or planning_task_lineage.get("upstream_book_task")
            or ""
        ).strip(),
        "主线": _collect_task_texts(
            planning_ctx.get("main_task"),
            planning_task_lineage.get("main_task"),
            _safe_dict(planning_ctx.get("story_spine")).get("headline"),
        )[:1],
        "支线": _collect_task_texts(
            planning_ctx.get("branch_tasks"),
            planning_ctx.get("tasks"),
            planning_task_lineage.get("branch_tasks"),
        ),
        "汇聚回主线": str(
            planning_ctx.get("merge_back_to_main")
            or planning_task_convergence.get("merge_back_to_main")
            or ""
        ).strip(),
    }
    cards_state_history_slice = {
        "recent_entities": core.get("recent_entities", []),
        "current_location": core.get("location", ""),
        "recent_state_changes": core.get("recent_state_changes", []),
        "protagonist_growth_snapshot": _load_protagonist_growth_snapshot(project_root),
    }
    foreshadow_silence_slice = {
        "has_active_foreshadowing": bool(active_foreshadowing),
        "active_foreshadowing": active_foreshadowing,
        "silence_windows": story_skeleton_first.get("silence_windows", []) if isinstance(story_skeleton_first, dict) else [],
        "payoff_windows": story_skeleton_first.get("payoff_windows", []) if isinstance(story_skeleton_first, dict) else [],
    }
    slice_foreshadow = planning_ctx.get("foreshadow_silence_slice")
    if isinstance(slice_foreshadow, dict) and slice_foreshadow:
        foreshadow_silence_slice = slice_foreshadow
    style_gate = {
        "anti_ai_required": True,
        "no_poison_required": True,
        "checklist": writing_guidance.get("checklist", []),
        "guidance_items": writing_guidance.get("guidance_items", []),
    }
    sequel_continuity = _load_story_source_manifest_summary(project_root)
    global_truth_slice = {
        "global_contract_index_ref": global_ctx.get("global_contract_index_ref", ""),
        "global_contract_refs": global_ctx.get("global_contract_refs", []),
        "global_card_count": global_ctx.get("global_card_count", 0),
        "global_contract_summary": global_ctx.get("global_contract_summary", {}),
    }
    chapter_planning_packet = {
        "chapter_ref": f"第{chapter_num}章",
        "chapter_title": str(chapter_board.get("chapter_title") or chapter_board.get("outline") or "").strip(),
        "story_overview": str(chapter_board.get("outline") or "").strip(),
        "chapter_goals": chapter_board.get("chapter_goals", []),
        "must_happen": chapter_board.get("must_happen", []),
        "cannot_change": chapter_board.get("cannot_change", []),
        "beat_checkpoints": chapter_board.get("beat_checkpoints", []),
        "terminal_beat": chapter_board.get("terminal_beat", ""),
        "bundled_elements": chapter_board.get("bundled_elements", {}),
        "planned_state": chapter_board.get("planned_state", {}),
        "action_beat_plan": chapter_board.get("action_beat_plan", {}),
        "style_execution": chapter_board.get("style_execution", {}),
        "emotion_execution": chapter_board.get("emotion_execution", {}),
        "emotion_beat": chapter_board.get("emotion_beat", {}),
        "anti_drift": chapter_board.get("anti_drift", []),
        "episode_rhythm_handoff": chapter_board.get("episode_rhythm_handoff", {}),
        "task_relation": chapter_task_relation,
    }
    chapter_planning_packet.update({key: value for key, value in chapter_task_relation.items() if value})
    volume_planning_summary = {
        "volume_ref": f"第{volume_num}卷",
        "book_plan_ref": book_plan_ref,
        "volume_plan_ref": volume_plan_ref,
        "story_spine": planning_ctx.get("story_spine") if isinstance(planning_ctx.get("story_spine"), dict) else {},
        "thread_window_slice": planning_ctx.get("thread_window_slice")
        if isinstance(planning_ctx.get("thread_window_slice"), dict)
        else {},
        "task_relation": volume_task_relation,
    }
    volume_planning_summary.update({key: value for key, value in volume_task_relation.items() if value})
    return {
        "context_contract_version": (payload.get("meta") or {}).get("context_contract_version"),
        "context_weight_stage": (payload.get("meta") or {}).get("context_weight_stage"),
        "current_step_id": str((payload.get("meta") or {}).get("current_step_id") or current_step_id or ""),
        "reader_signal": (sections.get("reader_signal") or {}).get("content", {}),
        "genre_profile": (sections.get("genre_profile") or {}).get("content", {}),
        "writing_guidance": writing_guidance,
        "validation_fact_pack": {
            "draft_snapshot": {
                "chapter": chapter_num,
                "current_step_id": str((payload.get("meta") or {}).get("current_step_id") or current_step_id or ""),
            },
            "cards_truth": {
                "cards_state_history_slice": cards_state_history_slice,
                "global_truth_slice": global_truth_slice,
            },
            "planning_truth": {
                "book_plan_ref": book_plan_ref,
                "volume_plan_ref": volume_plan_ref,
                "chapter_plan_refs": [chapter_plan_ref] if chapter_plan_ref else [],
                "volume_planning_summary": volume_planning_summary,
                "chapter_planning_packets": [chapter_planning_packet],
                "chapter_planning_packet": chapter_planning_packet,
                "promise_slice": promise_slice,
                "chapter_board": chapter_board,
                "episode_rhythm_handoff": episode_rhythm_handoff,
                "story_spine": planning_ctx.get("story_spine") if isinstance(planning_ctx.get("story_spine"), dict) else {},
                "thread_window_slice": planning_ctx.get("thread_window_slice")
                if isinstance(planning_ctx.get("thread_window_slice"), dict)
                else {},
                "foreshadow_silence_slice": foreshadow_silence_slice,
            },
            "init_truth": {
                "project_preferences": (sections.get("preferences") or {}).get("content", {}) or {},
                "genre_profile": (sections.get("genre_profile") or {}).get("content", {}) or {},
                "style_contract_ref": global_ctx.get("style_contract_ref", ""),
                "global_contract_refs": global_ctx.get("global_contract_refs", []),
            },
            "runtime_context": {
                "style_gate": style_gate,
                "reader_signal": (sections.get("reader_signal") or {}).get("content", {}) or {},
                "writing_guidance": writing_guidance,
                "sequel_continuity": sequel_continuity,
            },
        },
    }


def build_chapter_context_payload(
    project_root: Path,
    chapter_num: int,
    current_step_id: str | None = None,
) -> Dict[str, Any]:
    """Assemble full chapter context payload for text/json output."""
    outline = extract_chapter_outline(project_root, chapter_num)

    prev_summaries = []
    for prev_ch in range(max(1, chapter_num - 2), chapter_num):
        summary = extract_chapter_summary(project_root, prev_ch)
        prev_summaries.append(f"### 第{prev_ch}章摘要\n{summary}")

    state_summary = extract_state_summary(project_root)
    contract_context = _load_contract_context(project_root, chapter_num, current_step_id=current_step_id)
    rag_assist = _load_rag_assist(project_root, chapter_num, outline)

    validation_fact_pack = contract_context.get("validation_fact_pack", {})
    if isinstance(validation_fact_pack, dict):
        draft_snapshot = validation_fact_pack.get("draft_snapshot")
        if isinstance(draft_snapshot, dict):
            manuscript_ref = str(drafting_root_md_path(project_root, chapter_num).relative_to(project_root))
            draft_snapshot.setdefault("manuscript_ref", manuscript_ref)
            if chapter_num > 1:
                previous_ref = str(drafting_root_md_path(project_root, chapter_num - 1).relative_to(project_root))
                draft_snapshot.setdefault("previous_chapter_ref", previous_ref)
            draft_snapshot.setdefault("outline_excerpt", str(outline or "")[:240])

        runtime_context = validation_fact_pack.get("runtime_context")
        if isinstance(runtime_context, dict):
            runtime_context.setdefault("state_summary", state_summary)
            runtime_context.setdefault("previous_summaries", prev_summaries)

    payload = {
        "chapter": chapter_num,
        "outline": outline,
        "previous_summaries": prev_summaries,
        "state_summary": state_summary,
        "context_contract_version": contract_context.get("context_contract_version"),
        "context_weight_stage": contract_context.get("context_weight_stage"),
        "current_step_id": contract_context.get("current_step_id", str(current_step_id or "")),
        "reader_signal": contract_context.get("reader_signal", {}),
        "genre_profile": contract_context.get("genre_profile", {}),
        "writing_guidance": contract_context.get("writing_guidance", {}),
        "validation_fact_pack": validation_fact_pack,
        "rag_assist": rag_assist,
    }
    return payload


def _render_text(payload: Dict[str, Any]) -> str:
    chapter_num = payload.get("chapter")
    lines: List[str] = []

    lines.append(f"# 第 {chapter_num} 章创作上下文")
    lines.append("")

    lines.append("## 本章规划节点")
    lines.append("")
    lines.append(str(payload.get("outline", "")))
    lines.append("")
    lines.append("---")
    lines.append("")

    lines.append("## 前文摘要")
    lines.append("")
    for item in payload.get("previous_summaries", []):
        lines.append(item)
        lines.append("")

    lines.append("---")
    lines.append("")
    lines.append("## 当前状态")
    lines.append("")
    lines.append(str(payload.get("state_summary", "")))
    lines.append("")

    current_step_id = str(payload.get("current_step_id") or "").strip()
    if current_step_id:
        lines.append("## 当前工序")
        lines.append("")
        lines.append(f"- drafting_step: {current_step_id}")
        lines.append("")

    contract_version = payload.get("context_contract_version")
    if contract_version:
        lines.append(f"## Contract ({contract_version})")
        lines.append("")
        stage = payload.get("context_weight_stage")
        if stage:
            lines.append(f"- 上下文阶段权重: {stage}")
            lines.append("")

    writing_guidance = payload.get("writing_guidance") or {}
    guidance_items = writing_guidance.get("guidance_items") or []
    checklist = writing_guidance.get("checklist") or []
    checklist_score = writing_guidance.get("checklist_score") or {}
    methodology = writing_guidance.get("methodology") or {}
    if guidance_items or checklist:
        lines.append("## 写作执行建议")
        lines.append("")
        for idx, item in enumerate(guidance_items, start=1):
            lines.append(f"{idx}. {item}")

        if checklist:
            total_weight = 0.0
            required_count = 0
            for row in checklist:
                if isinstance(row, dict):
                    try:
                        total_weight += float(row.get("weight") or 0)
                    except (TypeError, ValueError):
                        pass
                    if row.get("required"):
                        required_count += 1

            lines.append("")
            lines.append("### 执行检查清单（可评分）")
            lines.append("")
            lines.append(f"- 项目数: {len(checklist)}")
            lines.append(f"- 总权重: {total_weight:.2f}")
            lines.append(f"- 必做项: {required_count}")
            lines.append("")

            for idx, row in enumerate(checklist, start=1):
                if not isinstance(row, dict):
                    lines.append(f"{idx}. {row}")
                    continue
                label = str(row.get("label") or "").strip() or "未命名项"
                weight = row.get("weight")
                required_tag = "必做" if row.get("required") else "可选"
                verify_hint = str(row.get("verify_hint") or "").strip()
                lines.append(f"{idx}. [{required_tag}][w={weight}] {label}")
                if verify_hint:
                    lines.append(f"   - 验收: {verify_hint}")

        if checklist_score:
            lines.append("")
            lines.append("### 执行评分")
            lines.append("")
            lines.append(f"- 评分: {checklist_score.get('score')}")
            lines.append(f"- 完成率: {checklist_score.get('completion_rate')}")
            lines.append(f"- 必做完成率: {checklist_score.get('required_completion_rate')}")

        lines.append("")

    if isinstance(methodology, dict) and methodology.get("enabled"):
        lines.append("## 长篇方法论策略")
        lines.append("")
        lines.append(f"- 框架: {methodology.get('framework')}")
        methodology_scope = methodology.get("genre_profile_key") or methodology.get("pilot") or "general"
        lines.append(f"- 适用题材: {methodology_scope}")
        lines.append(f"- 章节阶段: {methodology.get('chapter_stage')}")
        observability = methodology.get("observability") or {}
        if observability:
            lines.append(
                "- 指标: "
                f"next_reason={observability.get('next_reason_clarity')}, "
                f"anchor={observability.get('anchor_effectiveness')}, "
                f"rhythm={observability.get('rhythm_naturalness')}"
            )
        signals = methodology.get("signals") or {}
        risk_flags = list(signals.get("risk_flags") or [])
        if risk_flags:
            lines.append(f"- 风险标记: {', '.join(str(flag) for flag in risk_flags)}")
        lines.append("")

    reader_signal = payload.get("reader_signal") or {}
    review_trend = reader_signal.get("review_trend") or {}
    if review_trend:
        overall_avg = review_trend.get("overall_avg")
        lines.append("## 追读信号")
        lines.append("")
        lines.append(f"- 最近审查均分: {overall_avg}")
        low_ranges = reader_signal.get("low_score_ranges") or []
        if low_ranges:
            lines.append(f"- 低分区间数: {len(low_ranges)}")
        lines.append("")

    genre_profile = payload.get("genre_profile") or {}
    if genre_profile.get("genre"):
        lines.append("## 题材锚定")
        lines.append("")
        lines.append(f"- 题材: {genre_profile.get('genre')}")
        genres = genre_profile.get("genres") or []
        if len(genres) > 1:
            lines.append(f"- 复合题材: {' + '.join(str(token) for token in genres)}")
            composite_hints = genre_profile.get("composite_hints") or []
            for row in composite_hints[:2]:
                lines.append(f"- {row}")
        refs = genre_profile.get("reference_hints") or []
        for row in refs[:3]:
            lines.append(f"- {row}")
        lines.append("")

    rag_assist = payload.get("rag_assist") or {}
    hits = rag_assist.get("hits") or []
    if rag_assist.get("invoked") and hits:
        lines.append("## RAG 检索线索")
        lines.append("")
        lines.append(f"- 模式: {rag_assist.get('mode')}")
        lines.append(f"- 意图: {rag_assist.get('intent')}")
        lines.append(f"- 查询: {rag_assist.get('query')}")
        lines.append("")
        for idx, row in enumerate(hits[:5], start=1):
            chapter = row.get("chapter", "?")
            scene_index = row.get("scene_index", "?")
            score = row.get("score", 0)
            source = row.get("source", "unknown")
            content = row.get("content", "")
            lines.append(f"{idx}. [Ch{chapter}-S{scene_index}][{source}][score={score}] {content}")
        lines.append("")

    return "\n".join(lines).rstrip() + "\n"


def main():
    parser = argparse.ArgumentParser(description="提取章节创作所需的精简上下文")
    parser.add_argument("--chapter", type=int, required=True, help="目标章节号")
    parser.add_argument("--project-root", type=str, help="项目根目录")
    parser.add_argument("--format", choices=["text", "json"], default="text", help="输出格式")
    parser.add_argument("--step-id", type=str, help="当前 drafting step_id，可选")

    args = parser.parse_args()

    try:
        project_root = (
            find_project_root(Path(args.project_root))
            if args.project_root
            else find_project_root()
        )
        payload = build_chapter_context_payload(project_root, args.chapter, current_step_id=args.step_id)

        if args.format == "json":
            print(json.dumps(payload, ensure_ascii=False, indent=2))
        else:
            print(_render_text(payload), end="")

    except Exception as exc:
        print(f"❌ 错误: {exc}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    if sys.platform == "win32":
        enable_windows_utf8_stdio()
    main()
