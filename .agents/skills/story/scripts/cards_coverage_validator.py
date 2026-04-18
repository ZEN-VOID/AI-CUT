#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Validate whether story2026 1-Cards outputs are broad enough for full-series use.

The validator focuses on two layers:
1. Structural completeness: required buckets and link fields exist.
2. Scale fitness: card density matches the novel span inferred from project metadata.
"""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional
import yaml

from project_locator import resolve_project_root
from runtime_compat import enable_windows_utf8_stdio


STYLE_INDEX_REL = Path("Cards") / "1-风格卡" / "风格索引.json"
CHARACTER_INDEX_REL = Path("Cards") / "2-角色卡" / "角色索引.json"
SCENE_INDEX_REL = Path("Cards") / "3-场景卡" / "场景索引.json"
ITEM_INDEX_REL = Path("Cards") / "4-物品卡" / "物品索引.json"
STATE_REL = Path("STATE.json")
NORTH_STAR_REL = Path("0-Init") / "north_star.yaml"
INIT_HANDOFF_REL = Path("0-Init") / "init_handoff.yaml"

STYLE_BUCKETS = {
    "global_styles": Path("Cards") / "1-风格卡" / "总风格",
}
CHARACTER_BUCKETS = {
    "protagonists": Path("Cards") / "2-角色卡" / "主要角色",
    "antagonists": Path("Cards") / "2-角色卡" / "反派角色",
    "supporting": Path("Cards") / "2-角色卡" / "次要角色",
    "ensemble": Path("Cards") / "2-角色卡" / "群像角色",
}
SCENE_BUCKETS = {
    "indoor": Path("Cards") / "3-场景卡" / "室内",
    "outdoor": Path("Cards") / "3-场景卡" / "室外",
    "natural": Path("Cards") / "3-场景卡" / "自然",
    "surreal": Path("Cards") / "3-场景卡" / "超现实",
}
ITEM_BUCKETS = {
    "weapons_equipment": Path("Cards") / "4-物品卡" / "武器装备",
    "clue_items": Path("Cards") / "4-物品卡" / "线索物品",
    "narrative_items": Path("Cards") / "4-物品卡" / "重要叙事物品",
    "relics": Path("Cards") / "4-物品卡" / "文物",
    "adornments": Path("Cards") / "4-物品卡" / "点缀物",
}

TRACE_SPECS = {
    "style": {
        "source_skill_id": "story-cards-style",
        "source_route": "0-Init > story-cards > 风格卡/SKILL.md",
        "module_route": "story-cards > 风格卡/SKILL.md",
        "loaded_references": [
            "SKILL.md",
            "CONTEXT.md",
            "风格卡/SKILL.md",
            "风格卡/CONTEXT.md",
            "风格卡/templates/style-card.json",
        ],
    },
    "character": {
        "source_skill_id": "story-cards-character",
        "source_route": "0-Init > story-cards > 角色卡/SKILL.md",
        "module_route": "story-cards > 角色卡/SKILL.md",
        "loaded_references": [
            "SKILL.md",
            "CONTEXT.md",
            "角色卡/SKILL.md",
            "角色卡/CONTEXT.md",
            "角色卡/templates/character-card.json",
        ],
    },
    "scene": {
        "source_skill_id": "story-cards-scene",
        "source_route": "0-Init > story-cards > 场景卡/SKILL.md",
        "module_route": "story-cards > 场景卡/SKILL.md",
        "loaded_references": [
            "SKILL.md",
            "CONTEXT.md",
            "场景卡/SKILL.md",
            "场景卡/CONTEXT.md",
            "场景卡/templates/scene-card.json",
        ],
    },
    "item": {
        "source_skill_id": "story-cards-item",
        "source_route": "0-Init > story-cards > 物品卡/SKILL.md",
        "module_route": "story-cards > 物品卡/SKILL.md",
        "loaded_references": [
            "SKILL.md",
            "CONTEXT.md",
            "物品卡/SKILL.md",
            "物品卡/CONTEXT.md",
            "物品卡/templates/item-card.json",
        ],
    },
}


def _load_json(path: Path) -> Optional[Dict[str, Any]]:
    if not path.is_file():
        return None
    if path.suffix in {".yaml", ".yml"}:
        data = yaml.safe_load(path.read_text(encoding="utf-8"))
    else:
        data = json.loads(path.read_text(encoding="utf-8"))
    return data if isinstance(data, dict) else None


def _safe_list(value: Any) -> List[Any]:
    return value if isinstance(value, list) else []


def _safe_dict(value: Any) -> Dict[str, Any]:
    return value if isinstance(value, dict) else {}


def _resolve_ref(project_root: Path, ref: str) -> Path:
    path = Path(ref)
    if path.is_absolute():
        return path
    return project_root / path


def _scan_bucket_files(project_root: Path, bucket_rel: Path) -> List[str]:
    bucket_path = project_root / bucket_rel
    if not bucket_path.is_dir():
        return []
    refs: List[str] = []
    for file_path in sorted(bucket_path.glob("*.json")):
        refs.append(str(file_path.relative_to(project_root)))
    return refs


def _load_bucket_refs(project_root: Path, index_rel: Path, bucket_map: Dict[str, Path]) -> tuple[Dict[str, List[str]], Dict[str, List[str]], Dict[str, Any]]:
    payload = _load_json(project_root / index_rel) or {}
    groups = _safe_dict(_safe_dict(payload.get("content")).get("card_groups"))
    refs_by_bucket: Dict[str, List[str]] = {}
    missing_by_bucket: Dict[str, List[str]] = {}

    for bucket, bucket_rel in bucket_map.items():
        raw_refs = groups.get(bucket)
        refs = [str(item) for item in raw_refs if isinstance(item, str)] if isinstance(raw_refs, list) else _scan_bucket_files(project_root, bucket_rel)
        refs_by_bucket[bucket] = refs
        missing_by_bucket[bucket] = [ref for ref in refs if not _resolve_ref(project_root, ref).is_file()]

    return refs_by_bucket, missing_by_bucket, payload


def _keyword_hit(text: str, keywords: Iterable[str]) -> bool:
    return any(keyword in text for keyword in keywords)


def _count_segments(raw: str) -> int:
    if not raw:
        return 0
    parts = [part.strip() for part in re.split(r"[;；\n]+", raw) if part.strip()]
    return len(parts)


def _project_info(project_root: Path) -> Dict[str, Any]:
    state = _load_json(project_root / STATE_REL) or {}
    return _safe_dict(state.get("project_info"))


def _flatten_text_fragments(value: Any) -> List[str]:
    fragments: List[str] = []
    if isinstance(value, str):
        if value.strip():
            fragments.append(value.strip())
    elif isinstance(value, list):
        for item in value:
            fragments.extend(_flatten_text_fragments(item))
    elif isinstance(value, dict):
        for item in value.values():
            fragments.extend(_flatten_text_fragments(item))
    elif value not in (None, ""):
        fragments.append(str(value))
    return fragments


def _has_material(value: Any) -> bool:
    return bool(_flatten_text_fragments(value))


def _load_upstream_truth(project_root: Path) -> Dict[str, Dict[str, Any]]:
    return {
        "north_star": _load_json(project_root / NORTH_STAR_REL) or {},
        "init_handoff": _load_json(project_root / INIT_HANDOFF_REL) or {},
    }


def _infer_profile(info: Dict[str, Any], upstream_truth: Dict[str, Dict[str, Any]]) -> Dict[str, Any]:
    north_star = _safe_dict(upstream_truth.get("north_star"))
    project_identity = _safe_dict(north_star.get("project_identity"))
    story_kernel = _safe_dict(north_star.get("story_kernel"))
    reader_promise = _safe_dict(north_star.get("reader_promise"))
    cards = _safe_dict(north_star.get("cards"))
    world_system = _safe_dict(cards.get("world_system"))
    worldview = _safe_dict(world_system.get("worldview"))
    current_focus = _safe_dict(cards.get("current_focus"))
    init_handoff = _safe_dict(upstream_truth.get("init_handoff"))
    planning_seed = _safe_dict(init_handoff.get("stage_entry_seeds", {}).get("planning_seed"))
    pacing_scale = _safe_dict(planning_seed.get("pacing_scale"))
    constraint_seed = _safe_dict(planning_seed.get("constraint_seed"))
    cards_seed = _safe_dict(init_handoff.get("stage_entry_seeds", {}).get("cards_seed"))
    character_seed = _safe_dict(cards_seed.get("character_seed"))
    protagonist_seed = _safe_dict(character_seed.get("protagonist"))
    relationship_seed = _safe_dict(character_seed.get("relationship"))

    chapters_raw = (
        info.get("target_chapters")
        or project_identity.get("target_chapters")
        or pacing_scale.get("target_chapters")
    )
    try:
        chapters = int(chapters_raw or 0)
    except (TypeError, ValueError):
        chapters = 0

    protagonist_structure = str(
        info.get("protagonist_structure")
        or pacing_scale.get("protagonist_structure")
        or protagonist_seed.get("structure")
        or ""
    )
    protagonist_min = 1
    if "双主角" in protagonist_structure:
        protagonist_min = 2
    elif "多主角" in protagonist_structure or "群像" in protagonist_structure:
        protagonist_min = 3

    antagonist_tiers_raw = info.get("antagonist_tiers")
    antagonist_tiers = str(antagonist_tiers_raw or "")
    if antagonist_tiers:
        antagonist_min = max(1, min(_count_segments(antagonist_tiers), 5))
    else:
        antagonist_tier_map = _safe_dict(relationship_seed.get("antagonist_tiers"))
        antagonist_min = max(1, min(len(antagonist_tier_map), 5)) if antagonist_tier_map else 1

    if chapters >= 80:
        span = "epic"
        supporting_min = 3
        ensemble_min = 2
        relationship_min = 6
        scene_total_min = 8
        scene_link_min = 4
        item_total_min = 9
        ownership_link_min = 4
    elif chapters >= 20:
        span = "series"
        supporting_min = 2
        ensemble_min = 1
        relationship_min = 4
        scene_total_min = 6
        scene_link_min = 3
        item_total_min = 7
        ownership_link_min = 3
    else:
        span = "compact"
        supporting_min = 1
        ensemble_min = 0
        relationship_min = 2
        scene_total_min = 4
        scene_link_min = 2
        item_total_min = 5
        ownership_link_min = 2

    text_fragments = []
    for value in (
        info,
        project_identity,
        story_kernel,
        reader_promise,
        worldview,
        world_system.get("rule_system"),
        world_system.get("section_constraints"),
        current_focus,
        constraint_seed,
        cards_seed,
    ):
        text_fragments.extend(_flatten_text_fragments(value))
    text_blob = " ".join(text_fragments)

    travel_keywords = ("海", "路", "旅", "港", "岛", "跨海", "江湖", "冒险")
    surreal_keywords = ("怪谈", "诡", "梦", "幻", "异界", "超现实", "规则", "系统", "残意", "神话", "修仙", "异能")
    combat_keywords = ("武侠", "武道", "江湖", "修仙", "高武", "末世", "战", "刀", "剑", "枪", "异能", "机甲", "科技")
    clue_keywords = ("悬疑", "怪谈", "真相", "规则", "调查", "谜", "密", "谍", "线索", "追查")
    hard_rule_keywords = ("规则", "禁忌", "契约", "律令", "必须遵守", "代价", "不可违背", "怪谈")

    natural_min = 1 if chapters >= 20 or _keyword_hit(text_blob, travel_keywords) else 0
    surreal_min = 1 if _keyword_hit(text_blob, surreal_keywords) else 0
    weapons_min = 1 if _keyword_hit(text_blob, combat_keywords) else 0
    clue_min = 1 if _keyword_hit(text_blob, clue_keywords) else 0
    narrative_min = 1 if chapters >= 20 else 0

    rule_signal_count = len(_safe_list(world_system.get("rule_system")))
    rule_signal_count += len(_safe_list(reader_promise.get("hard_constraints")))
    rule_signal_count += len(_safe_list(constraint_seed.get("hard_constraints")))
    rule_signal_count += len(_safe_list(current_focus.get("enforcement_focus")))
    rule_signal_count += len(_safe_list(world_system.get("section_constraints")))
    if _keyword_hit(text_blob, hard_rule_keywords):
        rule_signal_count += 2
    if rule_signal_count >= 5:
        rule_rigidity = "strong"
    elif rule_signal_count >= 2:
        rule_rigidity = "medium"
    else:
        rule_rigidity = "weak"

    if rule_rigidity == "strong":
        surreal_min = max(surreal_min, 1)
        scene_link_min += 1
        item_total_min += 1
        ownership_link_min += 1
    elif rule_rigidity == "medium":
        scene_link_min = max(scene_link_min, 3)

    return {
        "target_chapters": chapters,
        "span": span,
        "rule_rigidity": rule_rigidity,
        "protagonist_min": protagonist_min,
        "antagonist_min": antagonist_min,
        "supporting_min": supporting_min,
        "ensemble_min": ensemble_min,
        "relationship_min": relationship_min,
        "scene_total_min": scene_total_min,
        "scene_link_min": scene_link_min,
        "natural_min": natural_min,
        "surreal_min": surreal_min,
        "item_total_min": item_total_min,
        "ownership_link_min": ownership_link_min,
        "weapons_min": weapons_min,
        "clue_min": clue_min,
        "narrative_min": narrative_min,
        "exclusive_hook_min": protagonist_min,
    }


def _append_issue(target: List[Dict[str, str]], severity: str, code: str, message: str) -> None:
    target.append({"severity": severity, "code": code, "message": message})


def _validate_trace_fields(
    content: Dict[str, Any],
    *,
    expected_trace: Dict[str, Any],
    issues: List[Dict[str, str]],
    route_code: str,
    refs_code: str,
    writeback_code: str,
) -> Dict[str, Any]:
    module_route = content.get("module_route")
    loaded_references = _safe_list(content.get("loaded_references"))
    writeback_plan = _safe_dict(content.get("writeback_plan"))
    target_paths = _safe_list(writeback_plan.get("target_paths"))

    if not isinstance(module_route, str) or not module_route.strip():
        _append_issue(issues, "blocking", route_code, "缺少 `content.module_route`，无法追溯本轮命中的模块路由。")
    elif module_route.strip() != str(expected_trace["module_route"]):
        _append_issue(
            issues,
            "blocking",
            route_code,
            f"`content.module_route` 漂移：当前 `{module_route}`，期望 `{expected_trace['module_route']}`。",
        )
    if not loaded_references or not all(isinstance(item, str) and item.strip() for item in loaded_references):
        _append_issue(issues, "blocking", refs_code, "缺少 `content.loaded_references`，无法追溯实际加载的 references/template。")
    else:
        missing_refs = [item for item in expected_trace["loaded_references"] if item not in loaded_references]
        if missing_refs:
            _append_issue(
                issues,
                "blocking",
                refs_code,
                f"`content.loaded_references` 缺少 child skill trace: {missing_refs}",
            )
    if not isinstance(writeback_plan.get("mode"), str) or not str(writeback_plan.get("mode")).strip():
        _append_issue(issues, "blocking", writeback_code, "缺少 `content.writeback_plan.mode`，无法判断本轮是全量、增量还是修复。")
    elif writeback_plan["mode"] not in {"full-build", "incremental-writeback", "coverage-repair", "source-contract-fix"}:
        _append_issue(issues, "blocking", writeback_code, f"`content.writeback_plan.mode` 非法：{writeback_plan['mode']}")
    if not target_paths or not all(isinstance(item, str) and item.strip() for item in target_paths):
        _append_issue(issues, "blocking", writeback_code, "缺少 `content.writeback_plan.target_paths`，无法追溯正式写回边界。")

    return {
        "module_route": module_route if isinstance(module_route, str) else "",
        "loaded_references": loaded_references,
        "writeback_plan": writeback_plan,
    }


def _load_card_payload(project_root: Path, ref: str) -> Optional[Dict[str, Any]]:
    return _load_json(_resolve_ref(project_root, ref))


def _validate_card_payloads(
    *,
    project_root: Path,
    refs_by_bucket: Dict[str, List[str]],
    issues: List[Dict[str, str]],
    card_kind: str,
) -> None:
    schema_key = f"{card_kind}_card"
    schema_prefix = "story2026/cards/style/v1" if card_kind == "style" else f"story2026/cards/{card_kind}/v2"
    expected_trace = TRACE_SPECS[card_kind]

    for refs in refs_by_bucket.values():
        for ref in refs:
            payload = _load_card_payload(project_root, ref)
            if not isinstance(payload, dict):
                _append_issue(issues, "blocking", f"FAIL-CARDS-{card_kind.upper()}-CARD-SCHEMA", f"{ref} 不是合法 JSON 卡片。")
                continue

            if str(payload.get("schema_version") or "") != schema_prefix:
                _append_issue(issues, "blocking", f"FAIL-CARDS-{card_kind.upper()}-CARD-SCHEMA", f"{ref} 的 schema_version 非法。")
                continue

            meta = _safe_dict(payload.get("meta"))
            content = _safe_dict(payload.get("content"))
            gate_summary = _safe_dict(payload.get("gate_summary"))
            if meta.get("skill_id") != "story-cards":
                _append_issue(issues, "blocking", f"FAIL-CARDS-{card_kind.upper()}-CARD-SCHEMA", f"{ref} 缺少合法 `meta.skill_id`。")
                continue
            if meta.get("source_skill_id") != expected_trace["source_skill_id"]:
                _append_issue(
                    issues,
                    "blocking",
                    f"FAIL-CARDS-{card_kind.upper()}-CARD-TRACE",
                    f"{ref} 的 `meta.source_skill_id` 漂移。",
                )
            if meta.get("source_route") != expected_trace["source_route"]:
                _append_issue(
                    issues,
                    "blocking",
                    f"FAIL-CARDS-{card_kind.upper()}-CARD-TRACE",
                    f"{ref} 的 `meta.source_route` 漂移。",
                )
            if not isinstance(gate_summary.get("status"), str) or not gate_summary.get("status"):
                _append_issue(issues, "blocking", f"FAIL-CARDS-{card_kind.upper()}-CARD-SCHEMA", f"{ref} 缺少 `gate_summary.status`。")
                continue

            _validate_trace_fields(
                content,
                expected_trace=expected_trace,
                issues=issues,
                route_code=f"FAIL-CARDS-{card_kind.upper()}-CARD-ROUTE",
                refs_code=f"FAIL-CARDS-{card_kind.upper()}-CARD-TRACE",
                writeback_code=f"FAIL-CARDS-{card_kind.upper()}-CARD-WRITEBACK",
            )

            card_schema = _safe_dict(content.get("card_schema"))
            card = _safe_dict(card_schema.get(schema_key))
            core = _safe_dict(card.get("core"))
            current_state = _safe_dict(card.get("current_state"))
            history = card.get("history")

            if not card or not core or not current_state or not isinstance(history, list):
                _append_issue(issues, "blocking", f"FAIL-CARDS-{card_kind.upper()}-CARD-SCHEMA", f"{ref} 缺少 `{schema_key}.core/current_state/history`。")
                continue

            if card_kind == "character":
                identity = _safe_dict(core.get("identity"))
                experience_timeline = _safe_dict(card.get("experience_timeline"))
                timeline_anchor = _safe_dict(current_state.get("timeline_anchor"))
                if not _has_material(identity.get("name")):
                    _append_issue(issues, "blocking", "FAIL-CARDS-CHAR-CARD-CONTENT", f"{ref} 缺少角色名。")
                if not _has_material(core.get("narrative_function")):
                    _append_issue(issues, "blocking", "FAIL-CARDS-CHAR-CARD-CONTENT", f"{ref} 缺少叙事功能桶。")
                if not _has_material(core.get("relationship_ports")):
                    _append_issue(issues, "blocking", "FAIL-CARDS-CHAR-CARD-CONTENT", f"{ref} 缺少关系接口。")
                if not _has_material(experience_timeline):
                    _append_issue(issues, "blocking", "FAIL-CARDS-CHAR-CARD-CONTENT", f"{ref} 缺少成长时间线。")
                if not _has_material(timeline_anchor):
                    _append_issue(issues, "blocking", "FAIL-CARDS-CHAR-CARD-CONTENT", f"{ref} 缺少 `current_state.timeline_anchor`。")
            elif card_kind == "scene":
                identity = _safe_dict(core.get("identity"))
                rule_and_risk = _safe_dict(core.get("rule_and_risk"))
                current_focus = _safe_dict(content.get("current_focus"))
                if not _has_material(identity.get("name")):
                    _append_issue(issues, "blocking", "FAIL-CARDS-SCENE-CARD-CONTENT", f"{ref} 缺少场景名。")
                if not _has_material(core.get("narrative_functions")):
                    _append_issue(issues, "blocking", "FAIL-CARDS-SCENE-CARD-CONTENT", f"{ref} 缺少场景叙事功能。")
                if not _has_material(rule_and_risk):
                    _append_issue(issues, "blocking", "FAIL-CARDS-SCENE-CARD-CONTENT", f"{ref} 缺少规则/风险/代价。")
                if not _has_material(core.get("compatible_roles")):
                    _append_issue(issues, "blocking", "FAIL-CARDS-SCENE-CARD-CONTENT", f"{ref} 缺少 `compatible_roles`。")
                if not _has_material(current_focus.get("repeat_use_strategy")):
                    _append_issue(issues, "blocking", "FAIL-CARDS-SCENE-CARD-CONTENT", f"{ref} 缺少 `repeat_use_strategy`。")
            elif card_kind == "item":
                identity = _safe_dict(core.get("identity"))
                usage_rules = _safe_dict(core.get("usage_rules"))
                exclusive_fit = _safe_dict(core.get("exclusive_fit"))
                if not _has_material(identity.get("name")):
                    _append_issue(issues, "blocking", "FAIL-CARDS-ITEM-CARD-CONTENT", f"{ref} 缺少物品名。")
                if not _has_material(core.get("narrative_functions")):
                    _append_issue(issues, "blocking", "FAIL-CARDS-ITEM-CARD-CONTENT", f"{ref} 缺少物品叙事功能。")
                if not _has_material(usage_rules):
                    _append_issue(issues, "blocking", "FAIL-CARDS-ITEM-CARD-CONTENT", f"{ref} 缺少使用规则/代价。")
                if not _has_material(exclusive_fit):
                    _append_issue(issues, "blocking", "FAIL-CARDS-ITEM-CARD-CONTENT", f"{ref} 缺少专属适配。")
                if not _has_material(identity.get("owner_type")) and not _has_material(current_state.get("holder")):
                    _append_issue(issues, "blocking", "FAIL-CARDS-ITEM-CARD-CONTENT", f"{ref} 缺少归属信息。")
            elif card_kind == "style":
                identity = _safe_dict(core.get("identity"))
                reader_promise = _safe_dict(core.get("reader_promise"))
                aesthetic_axes = _safe_dict(core.get("aesthetic_axes"))
                style_system = _safe_dict(core.get("style_system"))
                style_gate = _safe_dict(core.get("style_gate"))
                if not _has_material(identity.get("name")):
                    _append_issue(issues, "blocking", "FAIL-CARDS-STYLE-CARD-CONTENT", f"{ref} 缺少风格卡名。")
                if not _has_material(reader_promise):
                    _append_issue(issues, "blocking", "FAIL-CARDS-STYLE-CARD-CONTENT", f"{ref} 缺少 `reader_promise`。")
                if not _has_material(aesthetic_axes):
                    _append_issue(issues, "blocking", "FAIL-CARDS-STYLE-CARD-CONTENT", f"{ref} 缺少 `aesthetic_axes`。")
                if not _has_material(style_system):
                    _append_issue(issues, "blocking", "FAIL-CARDS-STYLE-CARD-CONTENT", f"{ref} 缺少 `style_system`。")
                if not _has_material(style_gate):
                    _append_issue(issues, "blocking", "FAIL-CARDS-STYLE-CARD-CONTENT", f"{ref} 缺少 `style_gate`。")


def _validate_styles(project_root: Path, upstream_truth: Dict[str, Dict[str, Any]]) -> Dict[str, Any]:
    refs_by_bucket, missing_by_bucket, payload = _load_bucket_refs(project_root, STYLE_INDEX_REL, STYLE_BUCKETS)
    content = _safe_dict(payload.get("content"))
    style_contract_refs = _safe_list(content.get("style_contract_refs"))
    counts = {bucket: len(refs) for bucket, refs in refs_by_bucket.items()}
    total_count = sum(counts.values())
    issues: List[Dict[str, str]] = []
    warnings: List[Dict[str, str]] = []

    north_star = _safe_dict(upstream_truth.get("north_star"))
    reader_promise = _safe_dict(north_star.get("reader_promise"))
    aesthetic_axes = _safe_dict(north_star.get("aesthetic_axes"))
    cards = _safe_dict(north_star.get("cards"))
    style_system = _safe_dict(cards.get("style_system"))

    if total_count < 1:
        _append_issue(issues, "blocking", "FAIL-CARDS-STYLE-TOTAL", "缺少正式风格卡。")
    if not style_contract_refs:
        _append_issue(issues, "blocking", "FAIL-CARDS-STYLE-REFS", "缺少 `style_contract_refs`，下游无法引用风格契约。")
    if not _has_material(reader_promise):
        _append_issue(warnings, "advisory", "WARN-CARDS-STYLE-UPSTREAM-PROMISE", "north_star 缺少 `reader_promise`，风格卡可能失去承诺真源。")
    if not _has_material(aesthetic_axes):
        _append_issue(warnings, "advisory", "WARN-CARDS-STYLE-UPSTREAM-AESTHETIC", "north_star 缺少 `aesthetic_axes`，风格卡可能失去审美轴真源。")
    if not _has_material(style_system):
        _append_issue(warnings, "advisory", "WARN-CARDS-STYLE-UPSTREAM-SYSTEM", "north_star.cards 缺少 `style_system`，风格卡可能失去风格系统真源。")
    trace = _validate_trace_fields(
        content,
        expected_trace=TRACE_SPECS["style"],
        issues=issues,
        route_code="FAIL-CARDS-STYLE-ROUTE",
        refs_code="FAIL-CARDS-STYLE-TRACE",
        writeback_code="FAIL-CARDS-STYLE-WRITEBACK",
    )

    missing_refs = {bucket: refs for bucket, refs in missing_by_bucket.items() if refs}
    if missing_refs:
        _append_issue(issues, "blocking", "FAIL-CARDS-STYLE-MISSING-REFS", f"风格索引存在失效引用：{missing_refs}")
    _validate_card_payloads(project_root=project_root, refs_by_bucket=refs_by_bucket, issues=issues, card_kind="style")

    return {
        "ok": not issues,
        "counts": counts,
        "style_contract_refs": len(style_contract_refs),
        "total_count": total_count,
        "requirements": {
            "total_count": 1,
            "style_contract_refs": 1,
        },
        "blocking_findings": issues,
        "advisory_findings": warnings,
        "trace": trace,
    }


def _validate_characters(project_root: Path, profile: Dict[str, Any]) -> Dict[str, Any]:
    refs_by_bucket, missing_by_bucket, payload = _load_bucket_refs(project_root, CHARACTER_INDEX_REL, CHARACTER_BUCKETS)
    content = _safe_dict(payload.get("content"))
    relationship_edges = _safe_list(content.get("relationship_edges"))
    current_focus = _safe_dict(content.get("current_focus"))

    counts = {bucket: len(refs) for bucket, refs in refs_by_bucket.items()}
    issues: List[Dict[str, str]] = []
    warnings: List[Dict[str, str]] = []

    if counts["protagonists"] < profile["protagonist_min"]:
        _append_issue(issues, "blocking", "FAIL-CARDS-CHAR-PROTAG", f"主角卡数量不足：当前 {counts['protagonists']}，最低应为 {profile['protagonist_min']}。")
    if counts["antagonists"] < profile["antagonist_min"]:
        _append_issue(issues, "blocking", "FAIL-CARDS-CHAR-ANTAG", f"反派卡数量不足：当前 {counts['antagonists']}，最低应为 {profile['antagonist_min']}。")
    if counts["supporting"] < profile["supporting_min"]:
        _append_issue(issues, "blocking", "FAIL-CARDS-CHAR-SUPPORT", f"次要角色数量不足：当前 {counts['supporting']}，最低应为 {profile['supporting_min']}。")
    if counts["ensemble"] < profile["ensemble_min"]:
        _append_issue(warnings, "advisory", "WARN-CARDS-CHAR-ENSEMBLE", f"群像角色偏少：当前 {counts['ensemble']}，建议至少 {profile['ensemble_min']}。")
    if len(relationship_edges) < profile["relationship_min"]:
        _append_issue(issues, "blocking", "FAIL-CARDS-CHAR-REL", f"关系边不足：当前 {len(relationship_edges)}，最低应为 {profile['relationship_min']}。")
    if not _safe_list(current_focus.get("confirmed_facts")):
        _append_issue(issues, "blocking", "FAIL-CARDS-CHAR-FOCUS", "角色索引缺少 `current_focus.confirmed_facts`，无法说明当前生效的人物骨架。")
    trace = _validate_trace_fields(
        content,
        expected_trace=TRACE_SPECS["character"],
        issues=issues,
        route_code="FAIL-CARDS-CHAR-ROUTE",
        refs_code="FAIL-CARDS-CHAR-TRACE",
        writeback_code="FAIL-CARDS-CHAR-WRITEBACK",
    )

    missing_refs = {bucket: refs for bucket, refs in missing_by_bucket.items() if refs}
    if missing_refs:
        _append_issue(issues, "blocking", "FAIL-CARDS-CHAR-REFS", f"角色索引存在失效引用：{missing_refs}")
    _validate_card_payloads(project_root=project_root, refs_by_bucket=refs_by_bucket, issues=issues, card_kind="character")

    return {
        "ok": not issues,
        "counts": counts,
        "relationship_edges": len(relationship_edges),
        "requirements": {
            "protagonists": profile["protagonist_min"],
            "antagonists": profile["antagonist_min"],
            "supporting": profile["supporting_min"],
            "ensemble": profile["ensemble_min"],
            "relationship_edges": profile["relationship_min"],
        },
        "blocking_findings": issues,
        "advisory_findings": warnings,
        "trace": trace,
    }


def _validate_scenes(project_root: Path, profile: Dict[str, Any]) -> Dict[str, Any]:
    refs_by_bucket, missing_by_bucket, payload = _load_bucket_refs(project_root, SCENE_INDEX_REL, SCENE_BUCKETS)
    content = _safe_dict(payload.get("content"))
    scene_links = _safe_list(content.get("scene_links"))

    counts = {bucket: len(refs) for bucket, refs in refs_by_bucket.items()}
    total_count = sum(counts.values())
    issues: List[Dict[str, str]] = []
    warnings: List[Dict[str, str]] = []

    if counts["indoor"] < 1:
        _append_issue(issues, "blocking", "FAIL-CARDS-SCENE-INDOOR", "室内场景为空，缺少常驻社会空间。")
    if counts["outdoor"] < 1:
        _append_issue(issues, "blocking", "FAIL-CARDS-SCENE-OUTDOOR", "室外场景为空，缺少移动与公开冲突空间。")
    if counts["natural"] < profile["natural_min"]:
        target = warnings if profile["natural_min"] == 0 else issues
        severity = "advisory" if profile["natural_min"] == 0 else "blocking"
        code = "WARN-CARDS-SCENE-NATURAL" if profile["natural_min"] == 0 else "FAIL-CARDS-SCENE-NATURAL"
        _append_issue(target, severity, code, f"自然场景偏少：当前 {counts['natural']}，期望 {profile['natural_min']}。")
    if counts["surreal"] < profile["surreal_min"]:
        _append_issue(issues, "blocking", "FAIL-CARDS-SCENE-SURREAL", f"超现实/规则场景偏少：当前 {counts['surreal']}，最低应为 {profile['surreal_min']}。")
    if total_count < profile["scene_total_min"]:
        _append_issue(issues, "blocking", "FAIL-CARDS-SCENE-TOTAL", f"场景总量不足：当前 {total_count}，最低应为 {profile['scene_total_min']}。")
    if len(scene_links) < profile["scene_link_min"]:
        _append_issue(issues, "blocking", "FAIL-CARDS-SCENE-LINKS", f"`scene_links` 数量不足：当前 {len(scene_links)}，最低应为 {profile['scene_link_min']}。")
    trace = _validate_trace_fields(
        content,
        expected_trace=TRACE_SPECS["scene"],
        issues=issues,
        route_code="FAIL-CARDS-SCENE-ROUTE",
        refs_code="FAIL-CARDS-SCENE-TRACE",
        writeback_code="FAIL-CARDS-SCENE-WRITEBACK",
    )

    missing_refs = {bucket: refs for bucket, refs in missing_by_bucket.items() if refs}
    if missing_refs:
        _append_issue(issues, "blocking", "FAIL-CARDS-SCENE-REFS", f"场景索引存在失效引用：{missing_refs}")
    _validate_card_payloads(project_root=project_root, refs_by_bucket=refs_by_bucket, issues=issues, card_kind="scene")

    return {
        "ok": not issues,
        "counts": counts,
        "scene_links": len(scene_links),
        "total_count": total_count,
        "requirements": {
            "indoor": 1,
            "outdoor": 1,
            "natural": profile["natural_min"],
            "surreal": profile["surreal_min"],
            "total_count": profile["scene_total_min"],
            "scene_links": profile["scene_link_min"],
        },
        "blocking_findings": issues,
        "advisory_findings": warnings,
        "trace": trace,
    }


def _validate_items(project_root: Path, profile: Dict[str, Any]) -> Dict[str, Any]:
    refs_by_bucket, missing_by_bucket, payload = _load_bucket_refs(project_root, ITEM_INDEX_REL, ITEM_BUCKETS)
    content = _safe_dict(payload.get("content"))
    ownership_links = _safe_list(content.get("ownership_links"))
    exclusive_item_hooks = _safe_list(content.get("exclusive_item_hooks"))

    counts = {bucket: len(refs) for bucket, refs in refs_by_bucket.items()}
    total_count = sum(counts.values())
    issues: List[Dict[str, str]] = []
    warnings: List[Dict[str, str]] = []

    if counts["weapons_equipment"] < profile["weapons_min"]:
        _append_issue(issues, "blocking", "FAIL-CARDS-ITEM-WEAPONS", f"武器/装备物品不足：当前 {counts['weapons_equipment']}，最低应为 {profile['weapons_min']}。")
    if counts["clue_items"] < profile["clue_min"]:
        target = warnings if profile["clue_min"] == 0 else issues
        severity = "advisory" if profile["clue_min"] == 0 else "blocking"
        code = "WARN-CARDS-ITEM-CLUE" if profile["clue_min"] == 0 else "FAIL-CARDS-ITEM-CLUE"
        _append_issue(target, severity, code, f"线索物偏少：当前 {counts['clue_items']}，期望 {profile['clue_min']}。")
    if counts["narrative_items"] < profile["narrative_min"]:
        target = warnings if profile["narrative_min"] == 0 else issues
        severity = "advisory" if profile["narrative_min"] == 0 else "blocking"
        code = "WARN-CARDS-ITEM-NARRATIVE" if profile["narrative_min"] == 0 else "FAIL-CARDS-ITEM-NARRATIVE"
        _append_issue(target, severity, code, f"重要叙事物偏少：当前 {counts['narrative_items']}，期望 {profile['narrative_min']}。")
    if total_count < profile["item_total_min"]:
        _append_issue(issues, "blocking", "FAIL-CARDS-ITEM-TOTAL", f"物品总量不足：当前 {total_count}，最低应为 {profile['item_total_min']}。")
    if len(ownership_links) < profile["ownership_link_min"]:
        _append_issue(issues, "blocking", "FAIL-CARDS-ITEM-OWNERSHIP", f"`ownership_links` 数量不足：当前 {len(ownership_links)}，最低应为 {profile['ownership_link_min']}。")
    if len(exclusive_item_hooks) < profile["exclusive_hook_min"]:
        _append_issue(issues, "blocking", "FAIL-CARDS-ITEM-HOOKS", f"角色专属物钩子不足：当前 {len(exclusive_item_hooks)}，最低应为 {profile['exclusive_hook_min']}。")
    trace = _validate_trace_fields(
        content,
        expected_trace=TRACE_SPECS["item"],
        issues=issues,
        route_code="FAIL-CARDS-ITEM-ROUTE",
        refs_code="FAIL-CARDS-ITEM-TRACE",
        writeback_code="FAIL-CARDS-ITEM-WRITEBACK",
    )

    missing_refs = {bucket: refs for bucket, refs in missing_by_bucket.items() if refs}
    if missing_refs:
        _append_issue(issues, "blocking", "FAIL-CARDS-ITEM-REFS", f"物品索引存在失效引用：{missing_refs}")
    _validate_card_payloads(project_root=project_root, refs_by_bucket=refs_by_bucket, issues=issues, card_kind="item")

    return {
        "ok": not issues,
        "counts": counts,
        "ownership_links": len(ownership_links),
        "exclusive_item_hooks": len(exclusive_item_hooks),
        "total_count": total_count,
        "requirements": {
            "weapons_equipment": profile["weapons_min"],
            "clue_items": profile["clue_min"],
            "narrative_items": profile["narrative_min"],
            "total_count": profile["item_total_min"],
            "ownership_links": profile["ownership_link_min"],
            "exclusive_item_hooks": profile["exclusive_hook_min"],
        },
        "blocking_findings": issues,
        "advisory_findings": warnings,
        "trace": trace,
    }


def build_cards_coverage_report(project_root: Path) -> Dict[str, Any]:
    info = _project_info(project_root)
    upstream_truth = _load_upstream_truth(project_root)
    profile = _infer_profile(info, upstream_truth)

    sections = {
        "styles": _validate_styles(project_root, upstream_truth),
        "characters": _validate_characters(project_root, profile),
        "scenes": _validate_scenes(project_root, profile),
        "items": _validate_items(project_root, profile),
    }

    blocking_findings: List[Dict[str, str]] = []
    advisory_findings: List[Dict[str, str]] = []
    for section in sections.values():
        blocking_findings.extend(section["blocking_findings"])
        advisory_findings.extend(section["advisory_findings"])

    return {
        "ok": not blocking_findings,
        "project_root": str(project_root),
        "profile": profile,
        "project_info": {
            "title": info.get("title", ""),
            "genre": info.get("genre", ""),
            "target_chapters": info.get("target_chapters", 0),
            "protagonist_structure": info.get("protagonist_structure", ""),
            "antagonist_tiers": info.get("antagonist_tiers", ""),
        },
        "upstream_truth": {
            "north_star_loaded": bool(upstream_truth["north_star"]),
            "init_handoff_loaded": bool(upstream_truth["init_handoff"]),
        },
        "sections": sections,
        "blocking_findings": blocking_findings,
        "advisory_findings": advisory_findings,
    }


def _print_text_report(report: Dict[str, Any]) -> None:
    status = "PASS" if report["ok"] else "FAIL-QUALITY"
    profile = report["profile"]
    print(f"{status} cards coverage: {report['project_root']}")
    print(
        "profile:"
        f" span={profile['span']},"
        f" chapters={profile['target_chapters']},"
        f" protagonists>={profile['protagonist_min']},"
        f" antagonists>={profile['antagonist_min']},"
        f" scenes>={profile['scene_total_min']},"
        f" items>={profile['item_total_min']}"
    )

    for section_name, section in report["sections"].items():
        marker = "OK" if section["ok"] else "FAIL"
        print(f"{marker} {section_name}")
        for finding in section["blocking_findings"]:
            print(f"  - {finding['code']}: {finding['message']}")
        for finding in section["advisory_findings"]:
            print(f"  - {finding['code']}: {finding['message']}")


def parse_args(argv: Optional[List[str]] = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Validate story2026 1-Cards coverage")
    parser.add_argument("--project-root", help="书项目根目录或工作区根目录（可选，默认自动检测）")
    parser.add_argument("--format", choices=["text", "json"], default="text", help="输出格式")
    return parser.parse_args(argv)


def main(argv: Optional[List[str]] = None) -> int:
    args = parse_args(argv)
    project_root = resolve_project_root(args.project_root) if args.project_root else resolve_project_root()
    report = build_cards_coverage_report(project_root)
    if args.format == "json":
        print(json.dumps(report, ensure_ascii=False, indent=2))
    else:
        _print_text_report(report)
    return 0 if report["ok"] else 1


if __name__ == "__main__":
    enable_windows_utf8_stdio(skip_in_pytest=True)
    raise SystemExit(main())
