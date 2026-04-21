#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Normalize legacy nine_blade prompt payloads for current downstream contracts."""

from __future__ import annotations

from copy import deepcopy
from typing import Any

from data_modules.comic_type_pack_resolver import TypePackResolver, _build_genre_alias_map, _keyword_hits


CANONICAL_STAGES = (
    "script_adaptation",
    "nine_blade_prompting",
    "image_generation",
    "animation_generation",
    "episode_poster",
)


def _safe_dict(value: Any) -> dict[str, Any]:
    return value if isinstance(value, dict) else {}


def _safe_list(value: Any) -> list[Any]:
    return value if isinstance(value, list) else []


def _append_dedup(base: list[Any], extra: list[Any]) -> list[Any]:
    out = list(base)
    seen = {str(item) for item in out}
    for item in extra:
        key = str(item)
        if key in seen:
            continue
        out.append(item)
        seen.add(key)
    return out


def _deep_merge(base: dict[str, Any], extra: dict[str, Any]) -> dict[str, Any]:
    result = deepcopy(base)
    for key, value in extra.items():
        if key not in result:
            result[key] = deepcopy(value)
            continue
        current = result[key]
        if isinstance(current, dict) and isinstance(value, dict):
            result[key] = _deep_merge(current, value)
        elif isinstance(current, list) and isinstance(value, list):
            result[key] = _append_dedup(current, value)
        else:
            result[key] = deepcopy(value)
    return result


def _compact_text(value: Any) -> str:
    if value in (None, "", [], {}):
        return ""
    if isinstance(value, str):
        return " ".join(value.split()).strip()
    return str(value).strip()


def _flatten_structure_lines(
    value: Any,
    *,
    prefix: str = "",
    max_lines: int = 24,
    max_depth: int = 4,
) -> list[str]:
    lines: list[str] = []

    def walk(node: Any, current_prefix: str, depth: int) -> None:
        if len(lines) >= max_lines or depth > max_depth:
            return
        if isinstance(node, dict):
            for key, child in node.items():
                next_prefix = f"{current_prefix}.{key}" if current_prefix else str(key)
                walk(child, next_prefix, depth + 1)
                if len(lines) >= max_lines:
                    return
            return
        if isinstance(node, list):
            compact_items = [_compact_text(item) for item in node]
            compact_items = [item for item in compact_items if item]
            if compact_items:
                label = current_prefix or "items"
                lines.append(f"{label}: {', '.join(compact_items[:8])}")
            return
        compact = _compact_text(node)
        if compact:
            label = current_prefix or "value"
            lines.append(f"{label}: {compact}")

    walk(value, prefix, 0)
    return lines[:max_lines]


def _projection_summary(stage_projection: dict[str, Any]) -> dict[str, str]:
    summary: dict[str, str] = {}
    for stage_name in CANONICAL_STAGES:
        projection = _safe_dict(stage_projection.get(stage_name))
        text = ", ".join(str(item) for item in _safe_list(projection.get("focus")) if str(item).strip())
        if not text:
            text = ", ".join(str(item) for item in _safe_list(projection.get("layout_bias")) if str(item).strip())
        if not text:
            text = ", ".join(str(item) for item in _safe_list(projection.get("render_bias")) if str(item).strip())
        if not text:
            text = ", ".join(str(item) for item in _safe_list(projection.get("motion_bias")) if str(item).strip())
        if not text:
            text = ", ".join(str(item) for item in _safe_list(projection.get("poster_bias")) if str(item).strip())
        summary[stage_name] = text
    return summary


def _explicit_stack(data: dict[str, Any]) -> dict[str, Any]:
    type_stack_ref = _safe_dict(data.get("type_stack_ref"))
    type_pack_context = _safe_dict(data.get("type_pack_context"))
    alias_map = _build_genre_alias_map()
    secondary = []
    for item in _safe_list(type_stack_ref.get("secondary") or type_pack_context.get("secondary")):
        label = str(item).strip()
        if not label:
            continue
        mapped = alias_map.get(label.lower())
        if mapped:
            secondary.append(mapped)
            continue
        keyword_hits = _keyword_hits(label, alias_map)
        if keyword_hits:
            secondary.extend(keyword_hits)
            continue
        secondary.append(label)
    explicit = {
        "method_kernel": type_stack_ref.get("method_kernel") or type_pack_context.get("method_kernel"),
        "base": type_stack_ref.get("base") or type_pack_context.get("base"),
        "primary": type_stack_ref.get("primary") or type_pack_context.get("primary"),
        "secondary": secondary,
        "platform": type_stack_ref.get("platform") or type_pack_context.get("platform"),
        "audience": type_stack_ref.get("audience") or type_pack_context.get("audience"),
    }
    return {key: value for key, value in explicit.items() if value not in (None, "", [], {})}


def normalize_nine_blade_prompt_data(data: dict[str, Any]) -> dict[str, Any]:
    """Fill newer type-pack fields for older prompt payloads without mutating source truth."""

    normalized = deepcopy(data)
    explicit_stack = _explicit_stack(normalized)
    if not explicit_stack:
        return normalized

    resolved_profile = TypePackResolver().resolve(explicit_stack)
    if not isinstance(resolved_profile, dict) or not resolved_profile:
        return normalized

    existing_stack = _safe_dict(normalized.get("type_stack_ref"))
    normalized["type_stack_ref"] = _deep_merge(
        {
            "method_kernel": resolved_profile.get("method_kernel"),
            "base": resolved_profile.get("base"),
            "primary": resolved_profile.get("primary"),
            "secondary": resolved_profile.get("secondary"),
            "platform": resolved_profile.get("platform"),
            "audience": resolved_profile.get("audience"),
            "active_packs": resolved_profile.get("active_packs"),
        },
        existing_stack,
    )

    merged_context = _deep_merge(resolved_profile, _safe_dict(normalized.get("type_pack_context")))
    control_surface = _safe_dict(merged_context.get("control_surface"))
    if control_surface and not _safe_list(merged_context.get("control_surface_digest")):
        merged_context["control_surface_digest"] = _flatten_structure_lines(
            control_surface,
            prefix="control_surface",
            max_lines=28,
        )

    stage_projection = _safe_dict(merged_context.get("stage_projection"))
    if not stage_projection:
        stage_projection = {stage_name: {} for stage_name in CANONICAL_STAGES}
        merged_context["stage_projection"] = stage_projection
    else:
        for stage_name in CANONICAL_STAGES:
            stage_projection.setdefault(stage_name, {})

    projection_summary = _safe_dict(merged_context.get("projection_summary"))
    if not projection_summary:
        merged_context["projection_summary"] = _projection_summary(stage_projection)
    else:
        for stage_name, summary in _projection_summary(stage_projection).items():
            projection_summary.setdefault(stage_name, summary)
        merged_context["projection_summary"] = projection_summary

    normalized["type_pack_context"] = merged_context
    return normalized
