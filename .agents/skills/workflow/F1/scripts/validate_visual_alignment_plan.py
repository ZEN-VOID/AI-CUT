#!/usr/bin/env python3
"""Validate F1 material-composition, tool-screen, PiP, and title-card plans."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def load_text(path: Path | None) -> str | None:
    if path is None:
        return None
    return path.read_text(encoding="utf-8")


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
VALID_TRANSITION_DENSITY_MODES = {"sparse", "normal", "high", "manual", "reference_high_frequency"}
VALID_TRANSITION_TRIGGER_SOURCES = {
    "manual",
    "reference_style",
    "semantic_phase_change",
    "material_category_switch",
    "beat_sync",
    "result_reveal",
    "tool_context_switch",
    "action_continuity",
    "fallback_smoothing",
}
VALID_TRANSITION_TYPES = {
    "hard_cut_on_beat",
    "match_cut",
    "motion_match_cut",
    "whip_pan_blur",
    "zoom_push",
    "zoom_pull",
    "speed_ramp_cut",
    "slide_wipe",
    "mask_wipe",
    "luma_wipe",
    "flash_cut",
    "white_flash",
    "black_flash",
    "glitch_snap",
    "light_sweep",
    "parallax_push",
    "radial_blur_zoom",
    "split_slide",
    "ripple_warp",
    "film_burn",
    "particle_wipe",
    "ink_wipe",
    "datamosh_snap",
    "rgb_split_glitch",
    "soft_crossfade",
}
VALID_TRANSITION_EFFECT_FAMILIES = {
    "rhythm_cut",
    "motion_bridge",
    "zoom_depth",
    "wipe_mask",
    "light_flash",
    "digital_glitch",
    "speed_time",
    "parallax_depth",
    "soft_fallback",
}
VALID_TRANSITION_STYLE_PRESETS = {
    "beat_punch_cut",
    "rhythm_hard_reset",
    "tool_glitch_snap",
    "result_flash_reveal",
    "black_reset_pulse",
    "whip_motion_bridge",
    "zoom_depth_push",
    "zoom_depth_pull",
    "mask_ui_wipe",
    "luma_magic_wipe",
    "speed_ramp_impact",
    "parallax_slide_depth",
    "comparison_slide_switch",
    "film_burn_reveal",
    "particle_wipe_reveal",
    "soft_context_blend",
}
VALID_TRANSITION_INTENSITIES = {"subtle", "medium", "strong", "impact"}
VALID_TRANSITION_ROLES = {
    "pace_boost",
    "category_bridge",
    "tool_to_result",
    "result_reveal",
    "scene_reset",
    "continuity_smoothing",
    "hook_punch",
    "tail_hook",
    "comparison_shift",
}
VALID_TRANSITION_LAYER_ORDERS = {"within_main_visual", "before_overlays", "before_hard_subtitles"}
VALID_PIP_TYPES = {
    "hero_pip_preview",
    "corner_pip",
    "tool_detail_zoom",
    "before_after_comparison",
    "result_preview",
    "reference_style_echo",
    "process_context",
}
VALID_PIP_TRIGGER_SOURCES = {"manual", "reference_style", "auto_visual_proof", "comparison_need", "fallback_context"}
VALID_PIP_ROLES = {"preview", "proof", "comparison", "detail_zoom", "context", "continuity_bridge"}
VALID_PIP_DENSITY_MODES = {"sparse", "normal", "high", "manual", "reference_high_frequency"}
VALID_PIP_POSITION_MODES = {
    "weighted_safe_random",
    "seeded_safe_random",
    "rotating_safe_zone",
    "reference_style_weighted",
    "manual_safe_choice",
    "source_tethered",
}
VALID_PIP_LAYOUT_ZONES = {
    "hero_preview_band",
    "upper_right",
    "upper_left",
    "mid_right",
    "mid_left",
    "aligned_top_left",
    "aligned_top_center",
    "aligned_top_right",
    "aligned_lower_left",
    "aligned_lower_center",
    "aligned_lower_right",
    "corner_pip",
    "lower_right_safe",
    "lower_left_safe",
    "local_zoom",
    "comparison_pair",
    "custom",
}
VALID_PIP_LAYER_ORDERS = {"before_hard_subtitles", "above_main_visual_below_subtitles"}
VALID_PIP_ENTRANCE_EFFECTS = {
    "cut_in",
    "slide_in",
    "slide_in_left",
    "slide_in_right",
    "scale_pop",
    "soft_zoom_in",
    "snap_zoom",
    "wipe_in",
    "mask_reveal",
    "glow_pop",
}
PIP_IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp", ".gif", ".bmp", ".tif", ".tiff", ".heic", ".avif"}
PIP_VIDEO_EXTENSIONS = {".mp4", ".mov", ".m4v", ".webm", ".mkv", ".avi"}
PIP_HOLD_REASON_FIELDS = (
    "duration_policy",
    "minimum_duration_policy",
    "hold_duration_policy",
    "duration_extension_reason",
    "hold_reason",
)
HERO_TITLE_CARD_TYPES = {"emphasis_overlay", "section_card"}
HERO_LAYOUT_ZONES = {"hero_emphasis_band", "main_visual_emphasis_band", "upper_middle_hero"}
TOP_BANNER_LAYOUT_ZONES = {"top_banner", "top_center", "upper_banner", "safe_top", "top_safe", "red_box_top_banner"}
LOCAL_LAYOUT_ZONES = {"local_callout", "tool_safe_callout", "full_frame", "custom"}
VALID_TITLE_LAYOUT_ZONES = HERO_LAYOUT_ZONES | TOP_BANNER_LAYOUT_ZONES | LOCAL_LAYOUT_ZONES
VALID_TITLE_ENTRANCE_EFFECTS = {
    "kinetic_pop",
    "zoom_blur_in",
    "light_sweep_reveal",
    "wipe_stretch_in",
    "slam_bounce",
    "glitch_snap",
    "parallax_push_in",
    "typewriter_snap",
    "shimmer_scale_in",
}
MIN_HERO_FONT_SIZE_720P = 90
MIN_HERO_WIDTH_PCT = 0.55
MIN_HERO_HEIGHT_PCT = 0.10
MIN_SUBTITLE_CLEARANCE_PX = 120
MIN_PIP_SUBTITLE_CLEARANCE_PX = 100
MIN_PIP_WIDTH_PCT = 0.14
MAX_PIP_WIDTH_PCT = 0.65
HERO_Y_RANGE = (0.30, 0.58)
MIN_TRANSITION_DURATION_SEC = 0.03
MAX_TRANSITION_DURATION_SEC = 0.8


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


def value_texts(value: object) -> list[str]:
    if isinstance(value, str):
        text = value.strip()
        return [text] if text else []
    if isinstance(value, (int, float)):
        return [str(value)]
    if isinstance(value, list):
        texts: list[str] = []
        for entry in value:
            texts.extend(value_texts(entry))
        return texts
    if isinstance(value, dict):
        texts = []
        for entry in value.values():
            texts.extend(value_texts(entry))
        return texts
    return []


def first_text(item: dict, fields: tuple[str, ...]) -> str:
    for field in fields:
        value = item.get(field)
        if str(value or "").strip():
            return str(value).strip()
    return ""


def parse_number(value: object) -> float | None:
    if isinstance(value, (int, float)):
        return float(value)
    if isinstance(value, str):
        match = re.search(r"-?\d+(?:\.\d+)?", value)
        if match:
            return float(match.group(0))
    return None


def parse_pct(value: object) -> float | None:
    number = parse_number(value)
    if number is None:
        return None
    if isinstance(value, str) and "%" in value:
        return number / 100.0
    if number > 1.0:
        return number / 100.0
    return number


def read_number(item: dict, fields: tuple[str, ...]) -> float | None:
    for field in fields:
        value = item.get(field)
        number = parse_number(value)
        if number is not None:
            return number
    return None


def read_pct(item: dict, fields: tuple[str, ...]) -> float | None:
    for field in fields:
        value = item.get(field)
        pct = parse_pct(value)
        if pct is not None:
            return pct
    return None


def pip_media_type(item: dict) -> str | None:
    for field in ("pip_media_type", "overlay_media_type", "source_media_type", "media_type", "asset_type"):
        value = str(item.get(field) or "").strip().lower()
        if not value:
            continue
        if any(token in value for token in ("image", "picture", "photo", "static", "still")):
            return "image"
        if any(token in value for token in ("video", "clip", "movie", "motion")):
            return "video"

    source_values: list[str] = []
    overlay_source = item.get("overlay_source")
    if isinstance(overlay_source, str):
        source_values.append(overlay_source)
    elif isinstance(overlay_source, dict):
        for field in ("source_file", "file", "path", "video_file", "image_file", "asset_file"):
            value = overlay_source.get(field)
            if str(value or "").strip():
                source_values.append(str(value))
    for field in ("source_file", "overlay_file", "image_file", "video_file", "asset_file"):
        value = item.get(field)
        if str(value or "").strip():
            source_values.append(str(value))

    for value in source_values:
        suffix = Path(value).suffix.lower()
        if suffix in PIP_IMAGE_EXTENSIONS:
            return "image"
        if suffix in PIP_VIDEO_EXTENSIONS:
            return "video"
    return None


def normalize_evidence_text(value: object) -> str:
    text = "".join(value_texts(value)).lower()
    return re.sub(r"[\s，。！？、；：,.!?;:'\"“”‘’（）()\[\]{}《》<>|/\\+-]+", "", text)


def has_any_reason(item: dict, layout: dict, fields: tuple[str, ...]) -> bool:
    for source in (item, layout):
        for field in fields:
            value = source.get(field)
            if isinstance(value, (dict, list)) and value:
                return True
            if str(value or "").strip():
                return True
    return False


def entrance_effect_is_allowed(value: str) -> bool:
    if not value:
        return False
    normalized = value.strip()
    if normalized.startswith("custom:"):
        return True
    tokens = [token for token in re.split(r"[\s,+/|]+", normalized) if token]
    return any(token in VALID_TITLE_ENTRANCE_EFFECTS for token in tokens)


def pip_entrance_effect_is_allowed(value: str) -> bool:
    if not value:
        return False
    normalized = value.strip()
    if normalized.startswith("custom:"):
        return True
    tokens = [token for token in re.split(r"[\s,+/|]+", normalized) if token]
    return any(token in VALID_PIP_ENTRANCE_EFFECTS for token in tokens)


def primary_entrance_effect(value: str) -> str:
    if not value:
        return ""
    normalized = value.strip()
    if normalized.startswith("custom:"):
        return normalized
    tokens = [token for token in re.split(r"[\s,+/|]+", normalized) if token]
    for token in tokens:
        if token in VALID_TITLE_ENTRANCE_EFFECTS:
            return token
    return tokens[0] if tokens else ""


def check_render_evidence(
    item: dict,
    errors: list[str],
    prefix: str,
    render_command_text: str | None,
    required_fields: tuple[str, ...],
) -> None:
    evidence = item.get("render_evidence") or item.get("runtime_render_evidence")
    if not isinstance(evidence, dict):
        errors.append(f"{prefix}: missing render_evidence for render-command parity")
        return
    for field in required_fields:
        if not value_texts(evidence.get(field)):
            errors.append(f"{prefix}.render_evidence: missing {field}")
    markers = (
        value_texts(evidence.get("filter_evidence"))
        + value_texts(evidence.get("filter_marker"))
        + value_texts(evidence.get("command_token"))
        + value_texts(evidence.get("overlay_filter_ref"))
    )
    if not markers:
        errors.append(f"{prefix}.render_evidence: missing filter_evidence/filter_marker/command_token")
    elif render_command_text is not None:
        missing = [marker for marker in markers if marker not in render_command_text]
        if missing:
            errors.append(
                f"{prefix}.render_evidence: render command missing evidence marker(s): {', '.join(missing)}"
            )


def check_title_effect_style(
    item: dict,
    errors: list[str],
    prefix: str,
    expected_title_font_size: float | None = None,
) -> None:
    effect_style = item.get("effect_style")
    if not isinstance(effect_style, dict):
        errors.append(f"{prefix}: effect_style must be an object")
        return
    size_fields = ("font_size_min", "font_size", "size", "size_policy", "scale", "text_size")
    effect_fields = ("text_effect", "effect", "animation", "motion_effect", "entrance_effect", "exit_effect")
    entrance_fields = ("entrance_effect", "entry_effect", "in_effect")
    entrance_reason_fields = (
        "entrance_effect_reason",
        "entrance_fit_reason",
        "entrance_policy",
        "entrance_rhythm_reason",
    )
    if not any(str(effect_style.get(field, "")).strip() for field in size_fields):
        errors.append(f"{prefix}: effect_style missing size/font-size policy")
    if not any(str(effect_style.get(field, "")).strip() for field in effect_fields):
        errors.append(f"{prefix}: effect_style missing text effect or animation policy")
    if not any(str(effect_style.get(field, "")).strip() for field in entrance_fields):
        errors.append(f"{prefix}: effect_style missing entrance_effect")
    else:
        entrance_effect = first_text(effect_style, entrance_fields)
        if item.get("card_type") in HERO_TITLE_CARD_TYPES and not entrance_effect_is_allowed(entrance_effect):
            errors.append(
                f"{prefix}: entrance_effect {entrance_effect!r} is not in the governed hero title-card effect set"
            )
    if not any(str(effect_style.get(field, "")).strip() for field in entrance_reason_fields):
        errors.append(f"{prefix}: effect_style missing entrance effect fit reason")
    if item.get("card_type") in HERO_TITLE_CARD_TYPES:
        font_size = read_number(effect_style, ("font_size_min", "font_size", "text_size"))
        if font_size is None:
            errors.append(f"{prefix}: hero title-card effect_style missing numeric font_size_min/font_size")
        elif font_size < MIN_HERO_FONT_SIZE_720P:
            errors.append(
                f"{prefix}: hero title-card font size {font_size:g} is below {MIN_HERO_FONT_SIZE_720P} for 720p"
            )
        if expected_title_font_size is not None:
            numeric_size_fields = ("font_size_min", "font_size", "text_size")
            found_sizes = [
                (field, read_number(effect_style, (field,)))
                for field in numeric_size_fields
                if read_number(effect_style, (field,)) is not None
            ]
            if not found_sizes:
                errors.append(
                    f"{prefix}: hero title-card missing numeric font size for expected {expected_title_font_size:g}"
                )
            else:
                mismatches = [
                    f"{field}={value:g}"
                    for field, value in found_sizes
                    if value is not None and float(value) != float(expected_title_font_size)
                ]
                if mismatches:
                    errors.append(
                        f"{prefix}: hero title-card expected font size {expected_title_font_size:g}; "
                        f"found {', '.join(mismatches)}"
                    )
        selection = effect_style.get("entrance_effect_selection")
        if not isinstance(selection, dict):
            errors.append(f"{prefix}: hero title-card missing effect_style.entrance_effect_selection")
        else:
            require_any_text(selection, ("cue_role", "cue_intent", "semantic_role"), errors, f"{prefix}.entrance_effect_selection")
            require_any_text(
                selection,
                ("semantic_energy", "energy_level", "impact_level"),
                errors,
                f"{prefix}.entrance_effect_selection",
            )
            require_any_text(
                selection,
                ("visual_motion", "background_motion", "shot_motion"),
                errors,
                f"{prefix}.entrance_effect_selection",
            )
            require_any_text(
                selection,
                ("candidate_effects", "ranked_candidates"),
                errors,
                f"{prefix}.entrance_effect_selection",
            )
            require_any_text(
                selection,
                ("selection_reason", "selection_basis", "effect_match_reason"),
                errors,
                f"{prefix}.entrance_effect_selection",
            )
            require_any_text(
                selection,
                ("diversity_check", "previous_effect_check", "repetition_policy"),
                errors,
                f"{prefix}.entrance_effect_selection",
            )


def check_title_layout(item: dict, errors: list[str], prefix: str) -> None:
    layout = item.get("layout")
    if not isinstance(layout, dict):
        errors.append(f"{prefix}: layout must be an object with layout_zone and normalized geometry")
        return
    layout_zone = str(layout.get("layout_zone") or layout.get("zone") or "").strip()
    if not layout_zone:
        errors.append(f"{prefix}: layout missing layout_zone")
        return
    if layout_zone not in VALID_TITLE_LAYOUT_ZONES:
        errors.append(f"{prefix}: unknown layout_zone {layout_zone!r}")
    require_any_text(layout, ("anchor", "position_anchor"), errors, f"{prefix}.layout")
    require_any_text(layout, ("collision_avoidance", "avoidance", "safe_zone_reason"), errors, f"{prefix}.layout")

    card_type = item.get("card_type")
    if card_type not in HERO_TITLE_CARD_TYPES:
        return

    if layout_zone in TOP_BANNER_LAYOUT_ZONES:
        if not has_any_reason(
            item,
            layout,
            ("layout_fallback_reason", "fallback_reason", "collision_reason", "user_position_reason"),
        ):
            errors.append(f"{prefix}: top-banner layout requires layout_fallback_reason or collision evidence")
        return
    if layout_zone not in HERO_LAYOUT_ZONES:
        if not has_any_reason(item, layout, ("layout_fallback_reason", "fallback_reason", "collision_reason")):
            errors.append(f"{prefix}: hero title-card must default to hero_emphasis_band or document fallback reason")
        return

    x_pct = read_pct(layout, ("x_pct", "center_x_pct", "cx_pct"))
    y_pct = read_pct(layout, ("y_pct", "center_y_pct", "cy_pct"))
    width_pct = read_pct(layout, ("width_pct", "w_pct"))
    height_pct = read_pct(layout, ("height_pct", "h_pct"))
    for field_name, value in (
        ("x_pct", x_pct),
        ("y_pct", y_pct),
        ("width_pct", width_pct),
        ("height_pct", height_pct),
    ):
        if value is None:
            errors.append(f"{prefix}: hero_emphasis_band layout missing {field_name}")
    if y_pct is not None and not (HERO_Y_RANGE[0] <= y_pct <= HERO_Y_RANGE[1]):
        errors.append(f"{prefix}: hero_emphasis_band y_pct {y_pct:.2f} outside {HERO_Y_RANGE[0]}-{HERO_Y_RANGE[1]}")
    if width_pct is not None and width_pct < MIN_HERO_WIDTH_PCT:
        errors.append(f"{prefix}: hero_emphasis_band width_pct {width_pct:.2f} below {MIN_HERO_WIDTH_PCT}")
    if height_pct is not None and height_pct < MIN_HERO_HEIGHT_PCT:
        errors.append(f"{prefix}: hero_emphasis_band height_pct {height_pct:.2f} below {MIN_HERO_HEIGHT_PCT}")

    safe_zone = item.get("safe_zone")
    if not isinstance(safe_zone, dict):
        safe_zone = {}
    clearance = read_number(
        {**safe_zone, **layout},
        ("safe_margin_bottom_to_subtitle_px", "subtitle_clearance_px", "bottom_subtitle_clearance_px"),
    )
    if clearance is None:
        errors.append(f"{prefix}: hero_emphasis_band missing subtitle clearance in layout/safe_zone")
    elif clearance < MIN_SUBTITLE_CLEARANCE_PX:
        errors.append(f"{prefix}: subtitle clearance {clearance:g}px below {MIN_SUBTITLE_CLEARANCE_PX}px")


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


def check_pip_visual_audio_timing(
    item: dict,
    audio_span: tuple[float, float] | None,
    visual_span: tuple[float, float] | None,
    max_delta: float,
    errors: list[str],
    prefix: str,
) -> None:
    if audio_span is None or visual_span is None:
        return
    if has_any_reason(item, item, PIP_HOLD_REASON_FIELDS):
        overlaps_audio = visual_span[0] <= audio_span[1] and visual_span[1] >= audio_span[0]
        if not overlaps_audio:
            errors.append(f"{prefix}: PiP hold span must overlap the referenced narration audio_span")
        if visual_span[0] > audio_span[0] + max_delta:
            errors.append(f"{prefix}: PiP hold visual start begins after the narration cue by more than {max_delta}s")
        return
    check_visual_audio_delta(audio_span, visual_span, max_delta, errors, prefix)


def check_pip_duration_policy(
    data: dict,
    pip_items: list[dict],
    errors: list[str],
    min_video_duration: float | None,
    min_image_duration: float | None,
    require_duration_policy: bool,
) -> None:
    if not pip_items:
        return
    if min_video_duration is None and min_image_duration is None and not require_duration_policy:
        return
    policy = (
        data.get("pip_density_policy")
        or data.get("picture_in_picture_density")
        or data.get("picture_in_picture_density_policy")
    )
    if not isinstance(policy, dict):
        errors.append("missing pip_density_policy for PiP duration policy")
        return
    if require_duration_policy:
        require_any_text(
            policy,
            ("duration_policy", "hold_duration_policy", "minimum_duration_policy", "media_duration_policy"),
            errors,
            "pip_density_policy",
        )
    if min_video_duration is not None:
        declared = read_number(
            policy,
            ("min_video_duration_sec", "minimum_video_duration_sec", "video_min_duration_sec", "min_video_hold_sec"),
        )
        if declared is None:
            errors.append("pip_density_policy: missing min_video_duration_sec")
        elif declared + 0.001 < min_video_duration:
            errors.append(
                f"pip_density_policy: min_video_duration_sec {declared:g}s is below required {min_video_duration:g}s"
            )
    if min_image_duration is not None:
        declared = read_number(
            policy,
            ("min_image_duration_sec", "minimum_image_duration_sec", "image_min_duration_sec", "min_image_hold_sec"),
        )
        if declared is None:
            errors.append("pip_density_policy: missing min_image_duration_sec")
        elif declared + 0.001 < min_image_duration:
            errors.append(
                f"pip_density_policy: min_image_duration_sec {declared:g}s is below required {min_image_duration:g}s"
            )


def check_pip_duration(
    item: dict,
    visual_span: tuple[float, float] | None,
    errors: list[str],
    prefix: str,
    min_video_duration: float | None,
    min_image_duration: float | None,
    require_duration_policy: bool,
) -> None:
    if visual_span is None:
        return
    if min_video_duration is None and min_image_duration is None and not require_duration_policy:
        return
    media_type = pip_media_type(item)
    if media_type is None:
        errors.append(f"{prefix}: missing or uninferable pip_media_type for duration validation")
        return
    if require_duration_policy:
        require_any_text(item, PIP_HOLD_REASON_FIELDS, errors, prefix)
    duration = visual_span[1] - visual_span[0]
    if media_type == "video" and min_video_duration is not None and duration + 0.001 < min_video_duration:
        errors.append(
            f"{prefix}: video PiP visual duration {duration:.3f}s is below required {min_video_duration:g}s"
        )
    if media_type == "image" and min_image_duration is not None and duration + 0.001 < min_image_duration:
        errors.append(
            f"{prefix}: image PiP visual duration {duration:.3f}s is below required {min_image_duration:g}s"
        )


def check_transition_density_policy(
    data: dict, transition_items: list[dict], errors: list[str], require_transitions: bool
) -> None:
    if not transition_items and not require_transitions:
        return
    policy = data.get("transition_density_policy") or data.get("visual_transition_density_policy")
    if not isinstance(policy, dict):
        errors.append("missing transition_density_policy for visual transition planning")
        return
    density_mode = str(policy.get("density_mode") or policy.get("mode") or "").strip()
    if density_mode not in VALID_TRANSITION_DENSITY_MODES:
        errors.append(f"transition_density_policy: invalid density_mode {density_mode!r}")
    require_any_text(
        policy,
        ("density_basis", "reference_observation", "transition_rule_summary", "selection_basis"),
        errors,
        "transition_density_policy",
    )
    require_any_text(
        policy,
        ("overuse_guardrail", "anti_overuse_policy", "subtitle_guardrail", "viewer_comfort_guardrail"),
        errors,
        "transition_density_policy",
    )
    require_any_text(
        policy,
        ("effect_palette", "transition_effect_palette", "style_palette", "effect_family_mix"),
        errors,
        "transition_density_policy",
    )
    require_any_text(
        policy,
        ("richness_policy", "effect_richness_policy", "variation_policy", "style_variation_policy"),
        errors,
        "transition_density_policy",
    )
    target_count = read_number(policy, ("target_count", "target_transition_count", "planned_count"))
    if target_count is None:
        errors.append("transition_density_policy: missing target_count")
    elif len(transition_items) < int(target_count):
        errors.append(
            f"transition_density_policy: target_count {int(target_count)} exceeds visual_transitions count {len(transition_items)}"
        )
    actual_count = read_number(policy, ("actual_count", "actual_transition_count", "planned_transition_count"))
    if actual_count is not None and int(actual_count) != len(transition_items):
        errors.append(
            f"transition_density_policy: actual_count {int(actual_count)} does not match visual_transitions count {len(transition_items)}"
        )
    boundary_count = read_number(policy, ("candidate_boundary_count", "triggerable_boundary_count", "candidate_count"))
    if boundary_count is None:
        errors.append("transition_density_policy: missing candidate_boundary_count/triggerable_boundary_count")
    elif target_count is not None and target_count > boundary_count:
        errors.append(
            f"transition_density_policy: target_count {int(target_count)} exceeds candidate boundary count {int(boundary_count)}"
        )
    if density_mode in {"high", "reference_high_frequency"}:
        require_any_text(
            policy,
            ("target_interval_sec", "cadence_sec", "target_cut_interval_sec", "scene_change_reference"),
            errors,
            "transition_density_policy",
        )


def transition_type_is_allowed(value: str) -> bool:
    if not value:
        return False
    normalized = value.strip()
    if normalized.startswith("custom:"):
        return True
    return normalized in VALID_TRANSITION_TYPES


def transition_effect_family_is_allowed(value: str) -> bool:
    if not value:
        return False
    normalized = value.strip()
    if normalized.startswith("custom:"):
        return True
    return normalized in VALID_TRANSITION_EFFECT_FAMILIES


def transition_style_preset_is_allowed(value: str) -> bool:
    if not value:
        return False
    normalized = value.strip()
    if normalized.startswith("custom:"):
        return True
    return normalized in VALID_TRANSITION_STYLE_PRESETS


def transition_intensity_is_allowed(value: str) -> bool:
    if not value:
        return False
    normalized = value.strip()
    if normalized.startswith("custom:"):
        return True
    return normalized in VALID_TRANSITION_INTENSITIES


def transition_effect_profile(item: dict) -> dict:
    for field in ("effect_profile", "effect_style", "transition_effect", "style_profile"):
        value = item.get(field)
        if isinstance(value, dict):
            return value
    return {}


def check_transition_item(
    item: dict, errors: list[str], prefix: str, max_cue: int | None, max_delta: float
) -> None:
    require_text(item, "id", errors, prefix)
    require_cue_indices(item, errors, prefix, max_cue)
    audio_span = require_span(item, "audio_span", errors, prefix)
    visual_span = require_span(item, "visual_span", errors, prefix)
    require_span(item, "script_span", errors, prefix)
    trigger_source = item.get("trigger_source")
    if trigger_source not in VALID_TRANSITION_TRIGGER_SOURCES:
        errors.append(f"{prefix}: invalid trigger_source {trigger_source!r}")
    transition_type = str(item.get("transition_type") or "").strip()
    if not transition_type_is_allowed(transition_type):
        errors.append(f"{prefix}: transition_type {transition_type!r} is not governed")
    transition_role = item.get("transition_role")
    if transition_role not in VALID_TRANSITION_ROLES:
        errors.append(f"{prefix}: invalid transition_role {transition_role!r}")
    require_any_text(item, ("from_material_composition_id", "from_visual_ref", "from_ref"), errors, prefix)
    require_any_text(item, ("to_material_composition_id", "to_visual_ref", "to_ref"), errors, prefix)
    require_any_text(item, ("selection_reason", "transition_reason"), errors, prefix)
    require_any_text(
        item,
        ("rhythm_sync", "beat_sync", "reference_rhythm_evidence", "sync_evidence"),
        errors,
        prefix,
    )
    require_any_text(item, ("motion", "effect_style", "transition_style", "implementation"), errors, prefix)
    effect_profile = transition_effect_profile(item)
    if not effect_profile:
        errors.append(f"{prefix}: transition effect profile must be a non-empty object")
    else:
        effect_family = first_text(effect_profile, ("effect_family", "transition_effect_family", "family"))
        if not effect_family:
            errors.append(f"{prefix}: missing effect_family in transition effect profile")
        elif not transition_effect_family_is_allowed(effect_family):
            errors.append(f"{prefix}: effect_family {effect_family!r} is not governed")
        style_preset = first_text(effect_profile, ("style_preset", "transition_style_preset", "preset"))
        if not style_preset:
            errors.append(f"{prefix}: missing style_preset in transition effect profile")
        elif not transition_style_preset_is_allowed(style_preset):
            errors.append(f"{prefix}: style_preset {style_preset!r} is not governed")
        intensity = first_text(effect_profile, ("intensity", "effect_intensity", "energy_level"))
        if not intensity:
            errors.append(f"{prefix}: missing intensity in transition effect profile")
        elif not transition_intensity_is_allowed(intensity):
            errors.append(f"{prefix}: intensity {intensity!r} is not governed")
        require_any_text(
            effect_profile,
            ("parameters", "effect_parameters", "parameter_profile", "variant_parameters"),
            errors,
            prefix,
        )
        require_any_text(
            effect_profile,
            ("variation_reason", "variant_seed", "style_variation", "preset_selection_reason"),
            errors,
            prefix,
        )
    require_any_text(
        item,
        ("safe_zone", "subtitle_policy", "collision_avoidance", "viewer_comfort"),
        errors,
        prefix,
    )
    layer_order = item.get("layer_order")
    if layer_order not in VALID_TRANSITION_LAYER_ORDERS:
        errors.append(f"{prefix}: invalid layer_order {layer_order!r}")
    duration = read_number(item, ("duration_sec", "transition_duration_sec", "duration"))
    if duration is None:
        if visual_span is not None:
            duration = visual_span[1] - visual_span[0]
        else:
            errors.append(f"{prefix}: missing duration_sec")
    if duration is not None and not (MIN_TRANSITION_DURATION_SEC <= duration <= MAX_TRANSITION_DURATION_SEC):
        errors.append(
            f"{prefix}: transition duration {duration:g}s outside {MIN_TRANSITION_DURATION_SEC}-{MAX_TRANSITION_DURATION_SEC}s"
        )
    if transition_type == "soft_crossfade":
        require_any_text(
            item,
            ("crossfade_reason", "slow_transition_reason", "mood_bridge_reason"),
            errors,
            prefix,
        )
    if item.get("verdict") != "pass":
        errors.append(f"{prefix}: verdict is {item.get('verdict')!r}")
    check_visual_audio_delta(audio_span, visual_span, max_delta, errors, prefix)


def check_transition_diversity(transition_items: list[dict], errors: list[str]) -> None:
    previous: tuple[int, str] | None = None
    previous_family: tuple[int, str] | None = None
    recent: list[tuple[int, str, dict]] = []
    recent_families: list[tuple[int, str, dict, dict]] = []
    for index, item in enumerate(transition_items, 1):
        if not isinstance(item, dict):
            continue
        transition_type = str(item.get("transition_type") or "").strip()
        if not transition_type:
            continue
        effect_profile = transition_effect_profile(item)
        effect_family = first_text(effect_profile, ("effect_family", "transition_effect_family", "family"))
        has_repeat_reason = has_any_reason(
            item,
            item,
            ("repeat_transition_reason", "same_transition_reason", "continuity_reason", "brand_rhythm_reason"),
        )
        if previous and transition_type == previous[1] and not has_repeat_reason:
            errors.append(
                f"visual_transitions[{index}]: repeats transition_type {transition_type!r} from visual_transitions[{previous[0]}] without repeat_transition_reason"
            )
        recent.append((index, transition_type, item))
        if len(recent) >= 3:
            window = recent[-3:]
            types = [window_type for _, window_type, _ in window]
            window_has_reason = any(
                has_any_reason(
                    window_item,
                    window_item,
                    (
                        "repeat_transition_reason",
                        "same_transition_reason",
                        "continuity_reason",
                        "brand_rhythm_reason",
                    ),
                )
                for _, _, window_item in window
            )
            if len(set(types)) == 1 and not window_has_reason:
                window_indices = ", ".join(str(window_index) for window_index, _, _ in window)
                errors.append(
                    f"visual_transitions[{index}]: transition window [{window_indices}] uses only {transition_type!r}; add transition diversity or repeat_transition_reason"
                )
        previous = (index, transition_type)
        if effect_family:
            has_family_repeat_reason = has_any_reason(
                item,
                effect_profile,
                (
                    "repeat_effect_family_reason",
                    "same_family_reason",
                    "family_continuity_reason",
                    "style_rhythm_reason",
                    "brand_rhythm_reason",
                ),
            )
            if previous_family and effect_family == previous_family[1] and not has_family_repeat_reason:
                errors.append(
                    f"visual_transitions[{index}]: repeats effect_family {effect_family!r} from visual_transitions[{previous_family[0]}] without repeat_effect_family_reason"
                )
            recent_families.append((index, effect_family, item, effect_profile))
            if len(recent_families) >= 3:
                family_window = recent_families[-3:]
                families = [window_family for _, window_family, _, _ in family_window]
                family_window_has_reason = any(
                    has_any_reason(
                        window_item,
                        window_profile,
                        (
                            "repeat_effect_family_reason",
                            "same_family_reason",
                            "family_continuity_reason",
                            "style_rhythm_reason",
                            "brand_rhythm_reason",
                        ),
                    )
                    for _, _, window_item, window_profile in family_window
                )
                if len(set(families)) == 1 and not family_window_has_reason:
                    window_indices = ", ".join(str(window_index) for window_index, _, _, _ in family_window)
                    errors.append(
                        f"visual_transitions[{index}]: effect-family window [{window_indices}] uses only {effect_family!r}; add effect-family diversity or repeat_effect_family_reason"
                    )
            previous_family = (index, effect_family)


def check_pip_density_policy(data: dict, pip_items: list[dict], errors: list[str], require_pip: bool) -> None:
    if not pip_items and not require_pip:
        return
    policy = (
        data.get("pip_density_policy")
        or data.get("picture_in_picture_density")
        or data.get("picture_in_picture_density_policy")
    )
    if not isinstance(policy, dict):
        errors.append("missing pip_density_policy for picture_in_picture planning")
        return
    density_mode = str(policy.get("density_mode") or policy.get("mode") or "").strip()
    if density_mode not in VALID_PIP_DENSITY_MODES:
        errors.append(f"pip_density_policy: invalid density_mode {density_mode!r}")
    require_any_text(
        policy,
        ("density_basis", "trigger_rule_summary", "coverage_reason", "selection_basis"),
        errors,
        "pip_density_policy",
    )
    require_any_text(
        policy,
        ("overuse_guardrail", "conflict_guardrail", "anti_overuse_policy"),
        errors,
        "pip_density_policy",
    )
    target_count = read_number(policy, ("target_count", "target_pip_count", "planned_count"))
    if target_count is None:
        errors.append("pip_density_policy: missing target_count")
    elif len(pip_items) < int(target_count):
        errors.append(
            f"pip_density_policy: target_count {int(target_count)} exceeds picture_in_picture count {len(pip_items)}"
        )
    triggerable_count = read_number(policy, ("triggerable_cue_count", "candidate_count", "trigger_candidate_count"))
    if triggerable_count is None:
        errors.append("pip_density_policy: missing triggerable_cue_count/candidate_count")
    elif target_count is not None and target_count > triggerable_count:
        errors.append(
            f"pip_density_policy: target_count {int(target_count)} exceeds triggerable cue count {int(triggerable_count)}"
        )
    actual_count = read_number(policy, ("actual_count", "actual_pip_count", "planned_pip_count"))
    if actual_count is not None and int(actual_count) != len(pip_items):
        errors.append(
            f"pip_density_policy: actual_count {int(actual_count)} does not match picture_in_picture count {len(pip_items)}"
        )
    if density_mode in {"high", "reference_high_frequency"}:
        require_any_text(
            policy,
            ("cadence_sec", "target_gap_sec", "target_screen_time_ratio", "density_window"),
            errors,
            "pip_density_policy",
        )


def pip_group_key(item: dict, index: int) -> str:
    layout = item.get("layout") if isinstance(item.get("layout"), dict) else {}
    layout_group = item.get("layout_group")
    if not isinstance(layout_group, dict):
        layout_group = layout.get("layout_group") if isinstance(layout.get("layout_group"), dict) else {}
    key = (
        item.get("cluster_id")
        or item.get("trigger_group")
        or item.get("layout_group_id")
        or layout_group.get("group_id")
        or layout.get("layout_group_id")
    )
    return str(key).strip() if str(key or "").strip() else f"__single_pip_{index}"


def layout_group_dict(item: dict) -> dict:
    layout = item.get("layout") if isinstance(item.get("layout"), dict) else {}
    layout_group = item.get("layout_group")
    if isinstance(layout_group, dict):
        return layout_group
    layout_group = layout.get("layout_group")
    return layout_group if isinstance(layout_group, dict) else {}


def dialogue_cue_texts(path: Path | None) -> dict[int, str]:
    if path is None:
        return {}
    data = load_json(path)
    cues = data.get("cues")
    if not isinstance(cues, list):
        raise ValueError("dialogue alignment JSON missing cues")
    cue_texts: dict[int, str] = {}
    for cue in cues:
        if not isinstance(cue, dict):
            continue
        index = cue.get("index")
        text = str(cue.get("text") or "").strip()
        if isinstance(index, int) and text:
            cue_texts[index] = text
    return cue_texts


def check_pip_group_contract(
    data: dict,
    pip_items: list[dict],
    errors: list[str],
    expected_group_size: int | None,
    require_aligned_groups: bool,
    require_cue_text_evidence: bool,
    cue_texts: dict[int, str],
) -> None:
    if expected_group_size is None and not require_aligned_groups and not require_cue_text_evidence:
        return
    if require_cue_text_evidence and not cue_texts:
        errors.append("require_pip_cue_text_evidence needs --dialogue-alignment cue text evidence")

    policy = (
        data.get("pip_density_policy")
        or data.get("picture_in_picture_density")
        or data.get("picture_in_picture_density_policy")
        or {}
    )
    if expected_group_size is not None:
        declared_size = read_number(
            policy,
            (
                "default_group_size",
                "default_frames_per_trigger",
                "frames_per_trigger_default",
                "simultaneous_group_size",
            ),
        )
        if declared_size is None:
            errors.append(
                "pip_density_policy: missing default_group_size/default_frames_per_trigger for grouped PiP"
            )
        elif int(declared_size) != expected_group_size:
            errors.append(
                f"pip_density_policy: default PiP group size {int(declared_size)} does not match expected {expected_group_size}"
            )
        require_any_text(
            policy,
            ("group_layout_policy", "multi_frame_policy", "aligned_group_policy"),
            errors,
            "pip_density_policy",
        )
        require_any_text(
            policy,
            ("content_relevance_policy", "cue_relation_policy", "source_match_policy"),
            errors,
            "pip_density_policy",
        )

    groups: dict[str, list[tuple[int, dict]]] = {}
    for index, item in enumerate(pip_items, 1):
        if isinstance(item, dict):
            groups.setdefault(pip_group_key(item, index), []).append((index, item))

    expected_slots = set(range(1, expected_group_size + 1)) if expected_group_size is not None else set()
    for group_id, entries in groups.items():
        if expected_group_size is not None and len(entries) != expected_group_size:
            errors.append(
                f"picture_in_picture group {group_id!r}: has {len(entries)} item(s); expected {expected_group_size}"
            )

        slots: list[int] = []
        x_slots: list[tuple[int, float]] = []
        y_values: list[float] = []
        height_values: list[float] = []
        for index, item in entries:
            prefix = f"picture_in_picture[{index}]"
            if expected_group_size is not None:
                item_group_size = read_number(item, ("simultaneous_group_size", "group_size"))
                if item_group_size is not None and int(item_group_size) != expected_group_size:
                    errors.append(
                        f"{prefix}: simultaneous_group_size {int(item_group_size)} does not match expected {expected_group_size}"
                    )
            layout = item.get("layout") if isinstance(item.get("layout"), dict) else {}
            group = layout_group_dict(item)
            if require_aligned_groups:
                if not group:
                    errors.append(f"{prefix}: missing layout_group for aligned grouped PiP")
                else:
                    require_any_text(group, ("layout_mode", "alignment_mode", "mode"), errors, f"{prefix}.layout_group")
                    require_any_text(group, ("alignment_axis", "row_axis", "grid_axis"), errors, f"{prefix}.layout_group")
                    group_size = read_number(group, ("group_size", "slot_count"))
                    if expected_group_size is not None and group_size is not None and int(group_size) != expected_group_size:
                        errors.append(
                            f"{prefix}.layout_group: group_size {int(group_size)} does not match expected {expected_group_size}"
                        )
                    slot = read_number(group, ("slot", "group_slot", "slot_index"))
                    if slot is None:
                        errors.append(f"{prefix}.layout_group: missing slot/group_slot")
                    else:
                        slots.append(int(slot))
                        x_pct = read_pct(layout, ("x_pct", "center_x_pct", "cx_pct"))
                        if x_pct is not None:
                            x_slots.append((int(slot), x_pct))
                y_pct = read_pct(layout, ("y_pct", "center_y_pct", "cy_pct"))
                height_pct = read_pct(layout, ("height_pct", "h_pct"))
                if y_pct is not None:
                    y_values.append(y_pct)
                if height_pct is not None:
                    height_values.append(height_pct)

            if require_cue_text_evidence and cue_texts:
                indices = item.get("cue_indices") if isinstance(item.get("cue_indices"), list) else []
                blob = normalize_evidence_text(
                    [
                        item.get("cue_text"),
                        item.get("current_narration"),
                        item.get("related_script_text"),
                        item.get("content_evidence"),
                        item.get("match_evidence"),
                        item.get("selection_reason"),
                        item.get("cluster_trigger_reason"),
                    ]
                )
                for cue_index in indices:
                    cue_text = cue_texts.get(cue_index)
                    if cue_text and normalize_evidence_text(cue_text) not in blob:
                        errors.append(
                            f"{prefix}: cue text evidence missing current narration for cue {cue_index}: {cue_text}"
                        )

        if require_aligned_groups and expected_group_size is not None and set(slots) != expected_slots:
            errors.append(
                f"picture_in_picture group {group_id!r}: aligned group slots {sorted(slots)} do not match expected {sorted(expected_slots)}"
            )
        if require_aligned_groups and y_values and max(y_values) - min(y_values) > 0.04:
            errors.append(f"picture_in_picture group {group_id!r}: y positions are not aligned in one row")
        if require_aligned_groups and height_values and max(height_values) - min(height_values) > 0.03:
            errors.append(f"picture_in_picture group {group_id!r}: frame heights are not aligned")
        if require_aligned_groups and len(x_slots) >= 2:
            sorted_x = [x for _, x in sorted(x_slots)]
            if any(right <= left for left, right in zip(sorted_x, sorted_x[1:])):
                errors.append(f"picture_in_picture group {group_id!r}: slot x positions are not left-to-right")


def check_pip_position_strategy(item: dict, layout_zone: str, errors: list[str], prefix: str) -> None:
    strategy = item.get("position_strategy") or item.get("position_randomization") or item.get("layout_randomization")
    if not isinstance(strategy, dict):
        errors.append(f"{prefix}: missing position_strategy for controlled random placement")
        return
    mode = str(strategy.get("mode") or strategy.get("position_mode") or "").strip()
    if mode not in VALID_PIP_POSITION_MODES:
        errors.append(f"{prefix}: invalid position_strategy mode {mode!r}")
    selected_zone = str(strategy.get("selected_zone") or strategy.get("selected_layout_zone") or "").strip()
    if selected_zone and layout_zone and selected_zone != layout_zone:
        errors.append(
            f"{prefix}: position_strategy selected_zone {selected_zone!r} does not match layout_zone {layout_zone!r}"
        )
    candidates = (
        strategy.get("candidate_zones")
        or strategy.get("safe_zone_candidates")
        or strategy.get("weighted_candidates")
        or []
    )
    if isinstance(candidates, list):
        candidate_count = len(candidates)
    else:
        candidate_count = 0
    if mode not in {"manual_safe_choice", "source_tethered"} and candidate_count < 2:
        errors.append(f"{prefix}: position_strategy needs at least two safe candidate zones for random placement")
    if mode in {"manual_safe_choice", "source_tethered"} and candidate_count < 1:
        errors.append(f"{prefix}: position_strategy needs at least one safe candidate zone")
    require_any_text(
        strategy,
        ("randomization_seed", "selection_seed", "randomization_basis", "seed_basis"),
        errors,
        f"{prefix}.position_strategy",
    )
    require_any_text(
        strategy,
        ("selection_reason", "position_selection_reason", "placement_reason"),
        errors,
        f"{prefix}.position_strategy",
    )
    require_any_text(
        strategy,
        ("collision_checks", "safe_zone_checks", "rejected_zones", "avoidance_checks"),
        errors,
        f"{prefix}.position_strategy",
    )


def check_pip_layout(item: dict, errors: list[str], prefix: str) -> str:
    layout = item.get("layout")
    if not isinstance(layout, dict):
        errors.append(f"{prefix}: layout must be an object")
        return ""
    layout_zone = str(layout.get("layout_zone") or layout.get("zone") or "").strip()
    if layout_zone not in VALID_PIP_LAYOUT_ZONES:
        errors.append(f"{prefix}: invalid picture-in-picture layout_zone {layout_zone!r}")
    require_any_text(layout, ("anchor", "position_anchor"), errors, f"{prefix}.layout")
    require_any_text(layout, ("collision_avoidance", "safe_zone_reason", "key_ui_avoidance"), errors, f"{prefix}.layout")
    for field in ("x_pct", "y_pct", "width_pct", "height_pct"):
        value = read_pct(layout, (field,))
        if value is None:
            errors.append(f"{prefix}: picture-in-picture layout missing {field}")
        elif not 0.0 <= value <= 1.0:
            errors.append(f"{prefix}: picture-in-picture {field} {value:.2f} outside 0-1")
    width_pct = read_pct(layout, ("width_pct", "w_pct"))
    if width_pct is not None and not (MIN_PIP_WIDTH_PCT <= width_pct <= MAX_PIP_WIDTH_PCT):
        errors.append(
            f"{prefix}: picture-in-picture width_pct {width_pct:.2f} outside {MIN_PIP_WIDTH_PCT}-{MAX_PIP_WIDTH_PCT}"
        )
    if layout_zone == "corner_pip" and width_pct is not None and width_pct > 0.38:
        errors.append(f"{prefix}: corner picture-in-picture width_pct {width_pct:.2f} exceeds 0.38")

    safe_zone = item.get("safe_zone")
    if not isinstance(safe_zone, dict):
        safe_zone = {}
    clearance = read_number(
        {**safe_zone, **layout},
        ("subtitle_clearance_px", "safe_margin_bottom_to_subtitle_px", "bottom_subtitle_clearance_px"),
    )
    if clearance is None:
        errors.append(f"{prefix}: picture-in-picture missing subtitle clearance")
    elif clearance < MIN_PIP_SUBTITLE_CLEARANCE_PX:
        errors.append(
            f"{prefix}: picture-in-picture subtitle clearance {clearance:g}px below {MIN_PIP_SUBTITLE_CLEARANCE_PX}px"
        )
    if item.get("covers_subtitles") is True or layout.get("covers_subtitles") is True:
        errors.append(f"{prefix}: picture-in-picture must not cover hard subtitles")
    if item.get("covers_key_ui") is True and not str(layout.get("collision_avoidance", "")).strip():
        errors.append(f"{prefix}: picture-in-picture covers key UI without collision_avoidance")
    return layout_zone


def check_pip_presentation(item: dict, errors: list[str], prefix: str) -> None:
    presentation = item.get("presentation") or item.get("style") or item.get("presentation_style")
    if not isinstance(presentation, dict):
        errors.append(f"{prefix}: picture-in-picture missing presentation/style object")
    else:
        require_any_text(
            presentation,
            ("border", "backplate", "shadow", "mask", "shape", "outline", "crop_style"),
            errors,
            f"{prefix}.presentation",
        )
        require_any_text(
            presentation,
            ("visual_priority", "readability_reason", "style_reason", "contrast_reason"),
            errors,
            f"{prefix}.presentation",
        )

    motion = item.get("motion") or item.get("animation") or item.get("entrance_motion")
    if not isinstance(motion, dict):
        errors.append(f"{prefix}: picture-in-picture missing motion object")
    else:
        require_any_text(motion, ("entrance_effect", "entry_effect", "in_effect"), errors, f"{prefix}.motion")
        entrance_effect = first_text(motion, ("entrance_effect", "entry_effect", "in_effect"))
        if entrance_effect and not pip_entrance_effect_is_allowed(entrance_effect):
            errors.append(f"{prefix}: picture-in-picture entrance_effect {entrance_effect!r} is not governed")
        require_any_text(
            motion,
            ("entrance_effect_reason", "entrance_fit_reason", "motion_reason", "timing_reason"),
            errors,
            f"{prefix}.motion",
        )

    require_any_text(
        item,
        ("placement_decision", "layout_decision", "position_selection_reason", "placement_reason"),
        errors,
        prefix,
    )


def check_picture_in_picture(
    item: dict,
    errors: list[str],
    prefix: str,
    max_cue: int | None,
    max_delta: float,
    min_pip_video_duration: float | None,
    min_pip_image_duration: float | None,
    require_pip_duration_policy: bool,
) -> None:
    require_text(item, "id", errors, prefix)
    require_cue_indices(item, errors, prefix, max_cue)
    audio_span = require_span(item, "audio_span", errors, prefix)
    visual_span = require_span(item, "visual_span", errors, prefix)
    require_span(item, "script_span", errors, prefix)
    trigger_source = item.get("trigger_source")
    if trigger_source not in VALID_PIP_TRIGGER_SOURCES:
        errors.append(f"{prefix}: invalid trigger_source {trigger_source!r}")
    pip_type = item.get("pip_type")
    if pip_type not in VALID_PIP_TYPES:
        errors.append(f"{prefix}: invalid pip_type {pip_type!r}")
    pip_role = item.get("pip_role")
    if pip_role not in VALID_PIP_ROLES:
        errors.append(f"{prefix}: invalid pip_role {pip_role!r}")
    require_any_text(
        item,
        ("overlay_source", "source_file", "segment_id", "image_id", "source_region"),
        errors,
        prefix,
    )
    require_any_text(item, ("content_evidence", "match_evidence", "comparison_evidence"), errors, prefix)
    require_text(item, "selection_reason", errors, prefix)
    require_any_text(item, ("base_layer_ref", "material_composition_id"), errors, prefix)
    check_pip_presentation(item, errors, prefix)
    layer_order = item.get("layer_order")
    if layer_order not in VALID_PIP_LAYER_ORDERS:
        errors.append(f"{prefix}: layer_order must be before_hard_subtitles or above_main_visual_below_subtitles")
    if pip_type == "before_after_comparison":
        require_any_text(item, ("comparison_items", "comparison_pair", "before_after_sources"), errors, prefix)
    layout_zone = check_pip_layout(item, errors, prefix)
    check_pip_position_strategy(item, layout_zone, errors, prefix)
    check_pip_duration(
        item,
        visual_span,
        errors,
        prefix,
        min_pip_video_duration,
        min_pip_image_duration,
        require_pip_duration_policy,
    )
    if item.get("verdict") != "pass":
        errors.append(f"{prefix}: verdict is {item.get('verdict')!r}")
    check_pip_visual_audio_timing(item, audio_span, visual_span, max_delta, errors, prefix)


def check_pip_position_diversity(pip_items: list[dict], errors: list[str]) -> None:
    previous_zone: tuple[int, str] | None = None
    recent_zones: list[tuple[int, str, dict]] = []
    for index, item in enumerate(pip_items, 1):
        layout = item.get("layout") if isinstance(item, dict) else {}
        strategy = (
            item.get("position_strategy")
            or item.get("position_randomization")
            or item.get("layout_randomization")
            if isinstance(item, dict)
            else {}
        )
        layout_dict = layout if isinstance(layout, dict) else {}
        strategy_dict = strategy if isinstance(strategy, dict) else {}
        zone = str(layout_dict.get("layout_zone") or layout_dict.get("zone") or "").strip()
        if not zone:
            continue
        has_repeat_reason = has_any_reason(
            item,
            strategy_dict,
            ("repeat_position_reason", "same_zone_reason", "position_lock_reason", "source_tether_reason"),
        )
        if previous_zone and zone == previous_zone[1] and not has_repeat_reason:
            errors.append(
                f"picture_in_picture[{index}]: repeats layout_zone {zone!r} from picture_in_picture[{previous_zone[0]}] without repeat_position_reason"
            )
        recent_zones.append((index, zone, strategy_dict))
        if len(recent_zones) >= 3:
            window = recent_zones[-3:]
            zones = [window_zone for _, window_zone, _ in window]
            window_has_reason = any(
                has_any_reason(
                    pip_items[window_index - 1],
                    window_strategy,
                    ("repeat_position_reason", "same_zone_reason", "position_lock_reason", "source_tether_reason"),
                )
                for window_index, _, window_strategy in window
            )
            if len(set(zones)) == 1 and not window_has_reason:
                window_indices = ", ".join(str(window_index) for window_index, _, _ in window)
                errors.append(
                    f"picture_in_picture[{index}]: position window [{window_indices}] uses only {zone!r}; add safe-zone variation or repeat_position_reason"
                )
        previous_zone = (index, zone)


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
    render_command: Path | None = None,
    require_tool_screen: bool = False,
    require_title_card: bool = False,
    require_pip: bool = False,
    require_transitions: bool = False,
    require_material_composition: bool = False,
    require_render_parity: bool = False,
    expected_title_font_size: float | None = None,
    require_render_title_font_size: bool = False,
    expected_pip_group_size: int | None = None,
    require_pip_aligned_groups: bool = False,
    require_pip_cue_text_evidence: bool = False,
    min_pip_video_duration: float | None = None,
    min_pip_image_duration: float | None = None,
    require_pip_duration_policy: bool = False,
    max_delta: float = 0.75,
) -> dict:
    data = load_json(path)
    errors: list[str] = []
    max_cue = dialogue_cue_count(dialogue_alignment)
    cue_texts = dialogue_cue_texts(dialogue_alignment) if require_pip_cue_text_evidence else {}
    render_command_text = load_text(render_command)

    if not isinstance(data, dict):
        return {"path": str(path), "ok": False, "errors": ["plan must be a JSON object"]}
    if require_render_parity and render_command_text is None:
        errors.append("require_render_parity needs --render-command evidence")
    if require_render_title_font_size:
        if render_command_text is None:
            errors.append("require_render_title_font_size needs --render-command evidence")
        elif expected_title_font_size is None:
            errors.append("require_render_title_font_size needs --expected-title-font-size")
        else:
            title_font_sizes = re.findall(
                r"(?<![A-Za-z_])fontsize\s*=\s*([0-9]+(?:\.[0-9]+)?)",
                render_command_text,
            )
            if not title_font_sizes:
                errors.append("render_command: missing title drawtext fontsize projection")
            else:
                mismatches = [
                    value for value in title_font_sizes if float(value) != float(expected_title_font_size)
                ]
                if mismatches:
                    errors.append(
                        "render_command: title drawtext fontsize mismatch; "
                        f"expected {expected_title_font_size:g}, found {', '.join(mismatches)}"
                    )

    tool_items = data.get("tool_screen_alignment", [])
    title_items = data.get("title_cards", [])
    pip_items = data.get("picture_in_picture", [])
    transition_items = data.get("visual_transitions", data.get("transitions", []))
    composition_items = data.get("material_composition", [])

    if require_tool_screen and not tool_items:
        errors.append("missing required tool_screen_alignment entries")
    if require_title_card and not title_items:
        errors.append("missing required title_cards entries")
    if require_pip and not pip_items:
        errors.append("missing required picture_in_picture entries")
    if require_transitions and not transition_items:
        errors.append("missing required visual_transitions entries")
    if require_material_composition and not composition_items:
        errors.append("missing required material_composition entries")
    if not isinstance(tool_items, list):
        errors.append("tool_screen_alignment must be a list")
        tool_items = []
    if not isinstance(title_items, list):
        errors.append("title_cards must be a list")
        title_items = []
    if not isinstance(pip_items, list):
        errors.append("picture_in_picture must be a list")
        pip_items = []
    if not isinstance(transition_items, list):
        errors.append("visual_transitions must be a list")
        transition_items = []
    if not isinstance(composition_items, list):
        errors.append("material_composition must be a list")
        composition_items = []

    check_pip_density_policy(data, pip_items, errors, require_pip)
    check_pip_duration_policy(
        data,
        pip_items,
        errors,
        min_pip_video_duration,
        min_pip_image_duration,
        require_pip_duration_policy,
    )
    check_pip_group_contract(
        data,
        pip_items,
        errors,
        expected_pip_group_size,
        require_pip_aligned_groups,
        require_pip_cue_text_evidence,
        cue_texts,
    )
    check_transition_density_policy(data, transition_items, errors, require_transitions)

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

    for index, item in enumerate(pip_items, 1):
        prefix = f"picture_in_picture[{index}]"
        if not isinstance(item, dict):
            errors.append(f"{prefix}: not an object")
            continue
        check_picture_in_picture(
            item,
            errors,
            prefix,
            max_cue,
            max_delta,
            min_pip_video_duration,
            min_pip_image_duration,
            require_pip_duration_policy,
        )
        if require_render_parity:
            check_render_evidence(
                item,
                errors,
                prefix,
                render_command_text,
                ("runtime_effect", "render_layer", "filter_evidence"),
            )
    check_pip_position_diversity(pip_items, errors)

    for index, item in enumerate(transition_items, 1):
        prefix = f"visual_transitions[{index}]"
        if not isinstance(item, dict):
            errors.append(f"{prefix}: not an object")
            continue
        check_transition_item(item, errors, prefix, max_cue, max_delta)
    check_transition_diversity(transition_items, errors)

    previous_hero_effect: tuple[int, str] | None = None
    recent_hero_effects: list[tuple[int, str]] = []
    for index, item in enumerate(title_items, 1):
        prefix = f"title_cards[{index}]"
        if not isinstance(item, dict):
            errors.append(f"{prefix}: not an object")
            continue
        require_text(item, "id", errors, prefix)
        require_text(item, "card_text", errors, prefix)
        require_text(item, "source_text", errors, prefix)
        require_any_text(item, ("text_determination",), errors, prefix)
        require_any_text(item, ("supporting_sources",), errors, prefix)
        require_any_text(item, ("presentation_timing",), errors, prefix)
        require_any_text(item, ("effect_style",), errors, prefix)
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
        check_title_effect_style(item, errors, prefix, expected_title_font_size=expected_title_font_size)
        check_title_layout(item, errors, prefix)
        if card_type in HERO_TITLE_CARD_TYPES:
            effect_style = item.get("effect_style")
            if isinstance(effect_style, dict):
                effect = primary_entrance_effect(first_text(effect_style, ("entrance_effect", "entry_effect", "in_effect")))
                selection = effect_style.get("entrance_effect_selection")
                selection_dict = selection if isinstance(selection, dict) else {}
                has_repeat_reason = has_any_reason(
                    item,
                    selection_dict,
                    ("repetition_reason", "repeat_reason", "same_effect_reason", "continuity_reason"),
                )
                if previous_hero_effect and effect and effect == previous_hero_effect[1] and not has_repeat_reason:
                    errors.append(
                        f"{prefix}: repeats entrance_effect {effect!r} from title_cards[{previous_hero_effect[0]}] without repetition_reason"
                    )
                recent_hero_effects.append((index, effect))
                if len(recent_hero_effects) >= 3:
                    window = recent_hero_effects[-3:]
                    effects = [window_effect for _, window_effect in window if window_effect]
                    if len(effects) == 3 and len(set(effects)) == 1 and not has_repeat_reason:
                        window_indices = ", ".join(str(window_index) for window_index, _ in window)
                        errors.append(
                            f"{prefix}: title-card effect window [{window_indices}] uses only {effect!r}; add diversity or repetition_reason"
                        )
                if effect:
                    previous_hero_effect = (index, effect)
        for field in ("subtitle_text", "safe_zone", "style_ref", "selection_reason"):
            require_text(item, field, errors, prefix)
        if item.get("verdict") != "pass":
            errors.append(f"{prefix}: verdict is {item.get('verdict')!r}")
        check_visual_audio_delta(audio_span, visual_span, max_delta, errors, prefix)
        if require_render_parity:
            check_render_evidence(
                item,
                errors,
                prefix,
                render_command_text,
                ("runtime_effect", "render_layer", "filter_evidence"),
            )

    return {
        "path": str(path),
        "dialogue_alignment": str(dialogue_alignment) if dialogue_alignment else None,
        "render_command": str(render_command) if render_command else None,
        "render_parity_required": require_render_parity,
        "expected_title_font_size": expected_title_font_size,
        "render_title_font_size_required": require_render_title_font_size,
        "expected_pip_group_size": expected_pip_group_size,
        "pip_aligned_groups_required": require_pip_aligned_groups,
        "pip_cue_text_evidence_required": require_pip_cue_text_evidence,
        "min_pip_video_duration": min_pip_video_duration,
        "min_pip_image_duration": min_pip_image_duration,
        "pip_duration_policy_required": require_pip_duration_policy,
        "ok": not errors,
        "material_composition_count": len(composition_items),
        "tool_screen_count": len(tool_items),
        "picture_in_picture_count": len(pip_items),
        "visual_transition_count": len(transition_items),
        "title_card_count": len(title_items),
        "errors": errors,
    }


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("plan", type=Path)
    parser.add_argument("--dialogue-alignment", type=Path)
    parser.add_argument("--render-command", type=Path)
    parser.add_argument("--require-tool-screen", action="store_true")
    parser.add_argument("--require-title-card", action="store_true")
    parser.add_argument("--require-pip", action="store_true")
    parser.add_argument("--require-transitions", action="store_true")
    parser.add_argument("--require-material-composition", action="store_true")
    parser.add_argument("--require-render-parity", action="store_true")
    parser.add_argument("--expected-title-font-size", type=float)
    parser.add_argument("--require-render-title-font-size", action="store_true")
    parser.add_argument("--expected-pip-group-size", type=int)
    parser.add_argument("--require-pip-aligned-groups", action="store_true")
    parser.add_argument("--require-pip-cue-text-evidence", action="store_true")
    parser.add_argument("--min-pip-video-duration", type=float)
    parser.add_argument("--min-pip-image-duration", type=float)
    parser.add_argument("--require-pip-duration-policy", action="store_true")
    parser.add_argument("--max-delta", type=float, default=0.75)
    args = parser.parse_args(argv[1:])

    try:
        report = validate(
            args.plan,
            dialogue_alignment=args.dialogue_alignment,
            render_command=args.render_command,
            require_tool_screen=args.require_tool_screen,
            require_title_card=args.require_title_card,
            require_pip=args.require_pip,
            require_transitions=args.require_transitions,
            require_material_composition=args.require_material_composition,
            require_render_parity=args.require_render_parity,
            expected_title_font_size=args.expected_title_font_size,
            require_render_title_font_size=args.require_render_title_font_size,
            expected_pip_group_size=args.expected_pip_group_size,
            require_pip_aligned_groups=args.require_pip_aligned_groups,
            require_pip_cue_text_evidence=args.require_pip_cue_text_evidence,
            min_pip_video_duration=args.min_pip_video_duration,
            min_pip_image_duration=args.min_pip_image_duration,
            require_pip_duration_policy=args.require_pip_duration_policy,
            max_delta=args.max_delta,
        )
    except Exception as exc:  # pragma: no cover - CLI guard
        report = {"path": str(args.plan), "ok": False, "errors": [str(exc)]}
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0 if report["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
