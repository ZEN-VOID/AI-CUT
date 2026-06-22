#!/usr/bin/env python3
"""Validate F1 material-composition, tool-screen, and title-card plans."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def span_values(value: object) -> tuple[float, float] | None:
    if isinstance(value, list) and len(value) == 2:
        return float(value[0]), float(value[1])
    if isinstance(value, dict) and "start" in value and "end" in value:
        return float(value["start"]), float(value["end"])
    return None


def require_text(item: dict, field: str, errors: list[str], prefix: str) -> None:
    if not str(item.get(field, "")).strip():
        errors.append(f"{prefix}: missing {field}")


def require_span(item: dict, field: str, errors: list[str], prefix: str) -> tuple[float, float] | None:
    span = span_values(item.get(field))
    if span is None:
        errors.append(f"{prefix}: missing {field}")
        return None
    start, end = span
    if end <= start:
        errors.append(f"{prefix}: non-positive {field}")
    return span


def require_cue_indices(item: dict, errors: list[str], prefix: str, max_cue: int | None) -> None:
    indices = item.get("cue_indices")
    if not isinstance(indices, list) or not indices:
        errors.append(f"{prefix}: missing cue_indices")
        return
    for cue_index in indices:
        if not isinstance(cue_index, int) or cue_index <= 0:
            errors.append(f"{prefix}: invalid cue index {cue_index!r}")
        elif max_cue is not None and cue_index > max_cue:
            errors.append(f"{prefix}: cue index {cue_index} exceeds dialogue cue count {max_cue}")


VALID_COMPOSITION_CATEGORIES = {"operation_demo", "tool_display", "aigc_content", "fallback_card"}
VALID_TITLE_CARD_TYPES = {"emphasis_overlay", "section_card", "full_frame_card", "callout_label"}
VALID_TITLE_TRIGGER_SOURCES = {"manual", "auto_emphasis", "fallback_explainer"}
VALID_TITLE_TEXT_POLICIES = {
    "verbatim_script",
    "compressed_from_script",
    "user_supplied",
    "fallback_explainer",
}
VALID_TITLE_DURATION_POLICIES = {"cue_bound", "short_emphasis", "section_hold", "fallback_hold"}
VALID_TITLE_DISPLAY_POLICIES = {"subtitle_visible", "poster_replaces_subtitle"}


def require_any_text(item: dict, fields: tuple[str, ...], errors: list[str], prefix: str) -> None:
    for field in fields:
        value = item.get(field)
        if isinstance(value, dict) and value:
            return
        if isinstance(value, list) and value:
            return
        if str(value or "").strip():
            return
    errors.append(f"{prefix}: missing one of {', '.join(fields)}")


def check_visual_audio_delta(
    audio_span: tuple[float, float] | None,
    visual_span: tuple[float, float] | None,
    max_delta: float,
    errors: list[str],
    prefix: str,
) -> None:
    if audio_span is None or visual_span is None:
        return
    if abs(audio_span[0] - visual_span[0]) > max_delta:
        errors.append(f"{prefix}: visual/audio start delta exceeds {max_delta}s")
    if abs(audio_span[1] - visual_span[1]) > max_delta:
        errors.append(f"{prefix}: visual/audio end delta exceeds {max_delta}s")


def dialogue_cue_count(path: Path | None) -> int | None:
    if path is None:
        return None
    data = load_json(path)
    cues = data.get("cues")
    if not isinstance(cues, list):
        raise ValueError("dialogue alignment JSON missing cues")
    return len(cues)


def validate(
    path: Path,
    dialogue_alignment: Path | None = None,
    require_tool_screen: bool = False,
    require_title_card: bool = False,
    require_material_composition: bool = False,
    max_delta: float = 0.75,
) -> dict:
    data = load_json(path)
    errors: list[str] = []
    max_cue = dialogue_cue_count(dialogue_alignment)

    if not isinstance(data, dict):
        return {"path": str(path), "ok": False, "errors": ["plan must be a JSON object"]}

    tool_items = data.get("tool_screen_alignment", [])
    title_items = data.get("title_cards", [])
    composition_items = data.get("material_composition", [])

    if require_tool_screen and not tool_items:
        errors.append("missing required tool_screen_alignment entries")
    if require_title_card and not title_items:
        errors.append("missing required title_cards entries")
    if require_material_composition and not composition_items:
        errors.append("missing required material_composition entries")
    if not isinstance(tool_items, list):
        errors.append("tool_screen_alignment must be a list")
        tool_items = []
    if not isinstance(title_items, list):
        errors.append("title_cards must be a list")
        title_items = []
    if not isinstance(composition_items, list):
        errors.append("material_composition must be a list")
        composition_items = []

    last_audio_end: float | None = None
    for index, item in enumerate(composition_items, 1):
        prefix = f"material_composition[{index}]"
        if not isinstance(item, dict):
            errors.append(f"{prefix}: not an object")
            continue
        require_text(item, "id", errors, prefix)
        require_cue_indices(item, errors, prefix, max_cue)
        audio_span = require_span(item, "audio_span", errors, prefix)
        visual_span = require_span(item, "visual_span", errors, prefix)
        require_span(item, "script_span", errors, prefix)
        category = item.get("primary_category")
        if category not in VALID_COMPOSITION_CATEGORIES:
            errors.append(f"{prefix}: invalid primary_category {category!r}")
        require_text(item, "visual_role", errors, prefix)
        require_text(item, "selection_reason", errors, prefix)
        require_text(item, "transition_policy", errors, prefix)
        if category == "fallback_card":
            require_text(item, "fallback_reason", errors, prefix)
        elif not str(item.get("source_file", "")).strip() and not str(item.get("segment_id", "")).strip():
            errors.append(f"{prefix}: missing source_file or segment_id")
        if category == "operation_demo":
            require_any_text(item, ("operation_state", "action_phase", "step_label", "category_evidence"), errors, prefix)
        elif category == "tool_display":
            require_any_text(item, ("screen_state", "tool_state", "category_evidence"), errors, prefix)
        elif category == "aigc_content":
            require_any_text(item, ("semantic_match", "visual_rhythm_reason", "category_evidence"), errors, prefix)
        if item.get("verdict") != "pass":
            errors.append(f"{prefix}: verdict is {item.get('verdict')!r}")
        check_visual_audio_delta(audio_span, visual_span, max_delta, errors, prefix)
        if audio_span is not None:
            if last_audio_end is not None and audio_span[0] < last_audio_end - 0.001:
                errors.append(f"{prefix}: audio_span overlaps previous material_composition entry")
            last_audio_end = audio_span[1]

    for index, item in enumerate(tool_items, 1):
        prefix = f"tool_screen_alignment[{index}]"
        if not isinstance(item, dict):
            errors.append(f"{prefix}: not an object")
            continue
        require_text(item, "id", errors, prefix)
        require_cue_indices(item, errors, prefix, max_cue)
        audio_span = require_span(item, "audio_span", errors, prefix)
        visual_span = require_span(item, "visual_span", errors, prefix)
        require_span(item, "script_span", errors, prefix)
        if not str(item.get("source_file", "")).strip() and not str(item.get("segment_id", "")).strip():
            errors.append(f"{prefix}: missing source_file or segment_id")
        for field in ("screen_state", "spoken_topic", "match_evidence"):
            require_text(item, field, errors, prefix)
        if item.get("verdict") != "pass":
            errors.append(f"{prefix}: verdict is {item.get('verdict')!r}")
        check_visual_audio_delta(audio_span, visual_span, max_delta, errors, prefix)

    for index, item in enumerate(title_items, 1):
        prefix = f"title_cards[{index}]"
        if not isinstance(item, dict):
            errors.append(f"{prefix}: not an object")
            continue
        require_text(item, "id", errors, prefix)
        require_text(item, "card_text", errors, prefix)
        require_text(item, "source_text", errors, prefix)
        require_cue_indices(item, errors, prefix, max_cue)
        audio_span = require_span(item, "audio_span", errors, prefix)
        visual_span = require_span(item, "visual_span", errors, prefix)
        require_span(item, "script_span", errors, prefix)
        trigger_source = item.get("trigger_source")
        if trigger_source not in VALID_TITLE_TRIGGER_SOURCES:
            errors.append(f"{prefix}: invalid trigger_source {trigger_source!r}")
        card_type = item.get("card_type")
        if card_type not in VALID_TITLE_CARD_TYPES:
            errors.append(f"{prefix}: invalid card_type {card_type!r}")
        text_policy = item.get("text_policy")
        if text_policy not in VALID_TITLE_TEXT_POLICIES:
            errors.append(f"{prefix}: invalid text_policy {text_policy!r}")
        elif text_policy == "compressed_from_script":
            require_text(item, "compression_reason", errors, prefix)
        duration_policy = item.get("duration_policy")
        if duration_policy not in VALID_TITLE_DURATION_POLICIES:
            errors.append(f"{prefix}: invalid duration_policy {duration_policy!r}")
        layer_order = item.get("layer_order")
        if layer_order != "before_hard_subtitles":
            errors.append(f"{prefix}: layer_order must be before_hard_subtitles")
        display_policy = item.get("subtitle_display_policy")
        if display_policy not in VALID_TITLE_DISPLAY_POLICIES:
            errors.append(f"{prefix}: invalid subtitle_display_policy")
        if display_policy == "poster_replaces_subtitle":
            require_text(item, "replacement_reason", errors, prefix)
        if trigger_source == "fallback_explainer" or text_policy == "fallback_explainer":
            require_text(item, "fallback_reason", errors, prefix)
        if card_type == "full_frame_card":
            require_text(item, "background_policy", errors, prefix)
        for field in ("subtitle_text", "layout", "safe_zone", "style_ref", "selection_reason"):
            require_text(item, field, errors, prefix)
        if item.get("verdict") != "pass":
            errors.append(f"{prefix}: verdict is {item.get('verdict')!r}")
        check_visual_audio_delta(audio_span, visual_span, max_delta, errors, prefix)

    return {
        "path": str(path),
        "dialogue_alignment": str(dialogue_alignment) if dialogue_alignment else None,
        "ok": not errors,
        "material_composition_count": len(composition_items),
        "tool_screen_count": len(tool_items),
        "title_card_count": len(title_items),
        "errors": errors,
    }


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("plan", type=Path)
    parser.add_argument("--dialogue-alignment", type=Path)
    parser.add_argument("--require-tool-screen", action="store_true")
    parser.add_argument("--require-title-card", action="store_true")
    parser.add_argument("--require-material-composition", action="store_true")
    parser.add_argument("--max-delta", type=float, default=0.75)
    args = parser.parse_args(argv[1:])

    try:
        report = validate(
            args.plan,
            dialogue_alignment=args.dialogue_alignment,
            require_tool_screen=args.require_tool_screen,
            require_title_card=args.require_title_card,
            require_material_composition=args.require_material_composition,
            max_delta=args.max_delta,
        )
    except Exception as exc:  # pragma: no cover - CLI guard
        report = {"path": str(args.plan), "ok": False, "errors": [str(exc)]}
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0 if report["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
