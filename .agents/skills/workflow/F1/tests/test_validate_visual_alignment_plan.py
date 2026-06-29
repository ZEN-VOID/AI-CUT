from __future__ import annotations

import importlib.util
import json
from pathlib import Path


SCRIPT_PATH = Path(__file__).resolve().parents[1] / "scripts" / "validate_visual_alignment_plan.py"
SPEC = importlib.util.spec_from_file_location("validate_visual_alignment_plan", SCRIPT_PATH)
assert SPEC and SPEC.loader
validator = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(validator)


def write_plan(tmp_path: Path, title_card: dict) -> Path:
    path = tmp_path / "visual_alignment_plan.json"
    path.write_text(json.dumps({"title_cards": [title_card]}, ensure_ascii=False), encoding="utf-8")
    return path


def write_plan_cards(tmp_path: Path, title_cards: list[dict]) -> Path:
    path = tmp_path / "visual_alignment_plan.json"
    path.write_text(json.dumps({"title_cards": title_cards}, ensure_ascii=False), encoding="utf-8")
    return path


def base_pip_density_policy(count: int = 1) -> dict:
    return {
        "density_mode": "high",
        "target_count": count,
        "actual_count": count,
        "triggerable_cue_count": max(count, 1),
        "default_group_size": 3 if count >= 3 else count,
        "group_layout_policy": "multi-window PiP triggers default to an aligned three-up row",
        "content_relevance_policy": "each inset must cite the current narration cue text it supports",
        "duration_policy": "video PiP holds at least 4s; static image PiP holds at least 3s",
        "min_video_duration_sec": 4,
        "min_image_duration_sec": 3,
        "cadence_sec": "one evidence-backed PiP every 6-10s in proof/result spans",
        "density_basis": "reference clip uses frequent PiP proof windows and the script has matching preview cues",
        "overuse_guardrail": "do not overlap hard subtitles, title cards, faces, key UI, or primary action",
    }


def write_pip_plan(tmp_path: Path, pip_item: dict | list[dict], include_density_policy: bool = True) -> Path:
    path = tmp_path / "visual_alignment_plan.json"
    pip_items = pip_item if isinstance(pip_item, list) else [pip_item]
    data = {"picture_in_picture": pip_items}
    if include_density_policy:
        data["pip_density_policy"] = base_pip_density_policy(len(pip_items))
    path.write_text(json.dumps(data, ensure_ascii=False), encoding="utf-8")
    return path


def write_dialogue_alignment(tmp_path: Path, cues: list[dict] | None = None) -> Path:
    path = tmp_path / "dialogue_alignment.json"
    path.write_text(
        json.dumps(
            {
                "cues": cues
                or [
                    {
                        "index": 1,
                        "text": "前置铺垫",
                        "audio_span": {"start": 0.0, "end": 2.0},
                        "verdict": "pass",
                    },
                    {
                        "index": 2,
                        "text": "转入演示",
                        "audio_span": {"start": 2.0, "end": 5.0},
                        "verdict": "pass",
                    },
                    {
                        "index": 3,
                        "text": "现在只需要把小说原文上传",
                        "audio_span": {"start": 5.0, "end": 8.0},
                        "verdict": "pass",
                    }
                ]
            },
            ensure_ascii=False,
        ),
        encoding="utf-8",
    )
    return path


def base_transition_density_policy(count: int = 1) -> dict:
    return {
        "density_mode": "reference_high_frequency",
        "target_count": count,
        "actual_count": count,
        "candidate_boundary_count": max(count, 1),
        "target_interval_sec": "reference analysis found an average visual cut interval near 1.6s",
        "density_basis": "reference clip uses frequent hard cuts, flash resets, and content-category switches",
        "overuse_guardrail": "avoid transition effects over hard subtitles, title-card text, and already busy PiP moments",
        "effect_palette": [
            "beat_punch_cut",
            "whip_motion_bridge",
            "result_flash_reveal",
            "tool_glitch_snap",
        ],
        "richness_policy": "vary effect families, direction, intensity, and parameters across nearby stitching points",
    }


def write_transition_plan(
    tmp_path: Path, transition_item: dict | list[dict], include_density_policy: bool = True
) -> Path:
    path = tmp_path / "visual_alignment_plan.json"
    transition_items = transition_item if isinstance(transition_item, list) else [transition_item]
    data = {"visual_transitions": transition_items}
    if include_density_policy:
        data["transition_density_policy"] = base_transition_density_policy(len(transition_items))
    path.write_text(json.dumps(data, ensure_ascii=False), encoding="utf-8")
    return path


def base_title_card() -> dict:
    return {
        "id": "tc-001",
        "trigger_source": "manual",
        "card_type": "emphasis_overlay",
        "text_policy": "verbatim_script",
        "text_determination": {"basis": "user selected hook phrase"},
        "card_text": "成本膝盖斩",
        "source_text": "成本膝盖斩",
        "supporting_sources": ["script cue 1"],
        "cue_indices": [1],
        "script_span": [0.0, 2.0],
        "audio_span": [0.0, 2.0],
        "visual_span": [0.0, 2.0],
        "presentation_timing": {"in": 0.0, "hold": 1.6, "out": 2.0},
        "layout": {
            "layout_zone": "hero_emphasis_band",
            "anchor": "center",
            "x_pct": 0.5,
            "y_pct": 0.43,
            "width_pct": 0.76,
            "height_pct": 0.18,
            "safe_margin_bottom_to_subtitle_px": 150,
            "collision_avoidance": "clear of subtitles and primary subject",
        },
        "safe_zone": {"subtitle_clearance_px": 150},
        "style_ref": "hero-big-text",
        "effect_style": {
            "font_size_min": 90,
            "text_effect": "heavy outline + glow + soft shadow",
            "entrance_effect": "kinetic_pop+light_sweep_reveal",
            "entrance_effect_reason": "matches hook impact and moving background",
            "entrance_effect_selection": {
                "cue_role": "hook_keyword",
                "semantic_energy": "high",
                "visual_motion": "slow aerial push",
                "candidate_effects": ["kinetic_pop", "zoom_blur_in", "light_sweep_reveal"],
                "selection_reason": "short punch phrase needs immediate impact without hiding the moving background",
                "diversity_check": "first hero title-card in this local window",
            },
        },
        "duration_policy": "short_emphasis",
        "subtitle_text": "成本膝盖斩",
        "subtitle_display_policy": "subtitle_visible",
        "layer_order": "before_hard_subtitles",
        "selection_reason": "manual hook emphasis",
        "verdict": "pass",
    }


def add_render_evidence(item: dict, marker: str, runtime_effect: str) -> dict:
    item["render_evidence"] = {
        "runtime_effect": runtime_effect,
        "render_layer": "overlay_before_hard_subtitles",
        "filter_evidence": marker,
    }
    return item


def base_picture_in_picture() -> dict:
    return {
        "id": "pip-001",
        "trigger_source": "reference_style",
        "pip_type": "hero_pip_preview",
        "pip_role": "preview",
        "cue_indices": [3],
        "script_span": [5.0, 8.0],
        "audio_span": [5.0, 8.0],
        "visual_span": [5.0, 8.0],
        "base_layer_ref": "mc-tool-003",
        "overlay_source": {
            "source_file": "素材/视频/影像内容/result.mp4",
            "segment_id": "result-shot-01",
        },
        "content_evidence": "script cue says to preview the generated result while the tool screen remains visible",
        "layout": {
            "layout_zone": "hero_preview_band",
            "anchor": "center",
            "x_pct": 0.52,
            "y_pct": 0.42,
            "width_pct": 0.48,
            "height_pct": 0.42,
            "subtitle_clearance_px": 150,
            "collision_avoidance": "does not cover bottom subtitles or the active generate button",
        },
        "safe_zone": {"subtitle_clearance_px": 150},
        "style": {
            "border": "thin white",
            "shadow": "soft",
            "visual_priority": "secondary proof window below main tool action",
        },
        "motion": {
            "entrance_effect": "scale_pop",
            "entrance_effect_reason": "result preview appears on the proof beat without hiding the tool context",
        },
        "placement_decision": "seeded safe-zone choice keeps the result near the tool context while clearing subtitles",
        "position_strategy": {
            "mode": "weighted_safe_random",
            "candidate_zones": ["hero_preview_band", "upper_right", "mid_left"],
            "selected_zone": "hero_preview_band",
            "randomization_seed": "project-cue-3",
            "selection_reason": "hero preview is weighted higher for result proof cues",
            "collision_checks": ["bottom subtitles clear", "generate button clear", "face clear"],
        },
        "layer_order": "before_hard_subtitles",
        "selection_reason": "reference style uses a result preview inset over the tool interface",
        "verdict": "pass",
    }


def aligned_picture_in_picture_group() -> list[dict]:
    slots = [
        ("aligned_top_left", 0.07, 1),
        ("aligned_top_center", 0.38, 2),
        ("aligned_top_right", 0.69, 3),
    ]
    items = []
    for zone, x_pct, slot in slots:
        item = base_picture_in_picture()
        item["id"] = f"pip-00{slot}"
        item["cluster_id"] = "pip_cluster_01"
        item["cue_text"] = "现在只需要把小说原文上传"
        item["content_evidence"] = (
            "cue 3: 现在只需要把小说原文上传；"
            f"第 {slot}/3 个画框展示上传小说动作、工具界面或结果证据。"
        )
        item["simultaneous_group_size"] = 3
        item["layout"] = {
            "layout_zone": zone,
            "anchor": "top_left",
            "x_pct": x_pct,
            "y_pct": 0.10,
            "width_pct": 0.24,
            "height_pct": 0.22,
            "subtitle_clearance_px": 260,
            "collision_avoidance": "aligned top row clears title cards, bottom subtitles, and primary action",
        }
        item["layout_group"] = {
            "group_id": "pip_cluster_01",
            "layout_mode": "aligned_three_up_row",
            "alignment_axis": "row",
            "group_size": 3,
            "slot": slot,
            "slot_count": 3,
        }
        item["position_strategy"] = {
            "mode": "manual_safe_choice",
            "candidate_zones": ["aligned_top_left", "aligned_top_center", "aligned_top_right"],
            "selected_zone": zone,
            "randomization_seed": "project-cue-3-aligned-row",
            "selection_reason": "three related proof windows are locked into a tidy row for this trigger",
            "collision_checks": ["bottom subtitles clear", "title-card band clear", "main subject clear"],
        }
        item["position_selection_reason"] = "aligned three-up group keeps simultaneous PiP windows orderly"
        items.append(item)
    return items


def base_visual_transition() -> dict:
    return {
        "id": "tr-001",
        "trigger_source": "reference_style",
        "transition_type": "whip_pan_blur",
        "transition_role": "category_bridge",
        "cue_indices": [4],
        "script_span": [10.0, 10.24],
        "audio_span": [10.0, 10.24],
        "visual_span": [10.0, 10.24],
        "duration_sec": 0.24,
        "from_material_composition_id": "mc-tool-004",
        "to_material_composition_id": "mc-result-005",
        "selection_reason": "reference clip uses rapid tool-to-result switches; this boundary bridges UI context to result reveal",
        "rhythm_sync": {
            "sync_point": "cue stress at 10.12s",
            "reference_evidence": "high-frequency reference cut cluster mapped to result reveal boundary",
        },
        "effect_style": {
            "effect_family": "motion_bridge",
            "style_preset": "whip_motion_bridge",
            "motion": "horizontal blur with 8-frame settle",
            "parameters": {
                "direction": "left_to_right",
                "motion_blur_px": 24,
                "settle_frames": 8,
                "easing": "easeOutCubic",
            },
            "intensity": "strong",
            "variant_seed": "tr-001-tool-to-result",
            "variation_reason": "nearby reveals should switch to flash, zoom, or glitch families instead of repeating whip motion",
            "readability_reason": "movement stays in main visual layer and clears bottom subtitles",
        },
        "safe_zone": {
            "subtitle_clearance_px": 140,
            "collision_avoidance": "transition occurs before hard subtitles and does not smear bottom subtitle area",
        },
        "layer_order": "within_main_visual",
        "verdict": "pass",
    }


def test_hero_emphasis_band_title_card_passes(tmp_path: Path) -> None:
    path = write_plan(tmp_path, base_title_card())

    report = validator.validate(path, require_title_card=True)

    assert report["ok"], report["errors"]


def test_title_card_render_parity_requires_filter_evidence(tmp_path: Path) -> None:
    path = write_plan(tmp_path, base_title_card())
    render_command = tmp_path / "render_command.txt"
    render_command.write_text("ffmpeg -filter_complex drawtext=fontsize=96", encoding="utf-8")

    report = validator.validate(
        path,
        render_command=render_command,
        require_title_card=True,
        require_render_parity=True,
    )

    assert not report["ok"]
    assert "missing render_evidence" in "\n".join(report["errors"])


def test_title_card_render_parity_passes_with_matching_marker(tmp_path: Path) -> None:
    marker = "title_runtime_effect=tc-001"
    path = write_plan(tmp_path, add_render_evidence(base_title_card(), marker, "kinetic_pop"))
    render_command = tmp_path / "render_command.txt"
    render_command.write_text(f"ffmpeg -filter_complex drawtext@{marker}:fontsize=96", encoding="utf-8")

    report = validator.validate(
        path,
        render_command=render_command,
        require_title_card=True,
        require_render_parity=True,
    )

    assert report["ok"], report["errors"]


def test_expected_title_font_size_and_render_command_projection_passes(tmp_path: Path) -> None:
    marker = "title_runtime_effect=tc-001"
    title_card = base_title_card()
    title_card["effect_style"]["font_size"] = 90
    path = write_plan(tmp_path, add_render_evidence(title_card, marker, "kinetic_pop"))
    render_command = tmp_path / "render_command.txt"
    render_command.write_text(
        f"ffmpeg -filter_complex drawtext@{marker}:text='成本膝盖斩':fontsize=90 "
        "-metadata f1_render_evidence=subtitle_fontsize=30|title_fontsize=90",
        encoding="utf-8",
    )

    report = validator.validate(
        path,
        render_command=render_command,
        require_title_card=True,
        require_render_parity=True,
        expected_title_font_size=90,
        require_render_title_font_size=True,
    )

    assert report["ok"], report["errors"]


def test_title_render_font_size_mismatch_fails(tmp_path: Path) -> None:
    marker = "title_runtime_effect=tc-001"
    title_card = base_title_card()
    title_card["effect_style"]["font_size"] = 96
    path = write_plan(tmp_path, add_render_evidence(title_card, marker, "kinetic_pop"))
    render_command = tmp_path / "render_command.txt"
    render_command.write_text(
        f"ffmpeg -filter_complex drawtext@{marker}:text='成本膝盖斩':fontsize=104",
        encoding="utf-8",
    )

    report = validator.validate(
        path,
        render_command=render_command,
        require_title_card=True,
        require_render_parity=True,
        expected_title_font_size=90,
        require_render_title_font_size=True,
    )

    assert not report["ok"]
    errors = "\n".join(report["errors"])
    assert "hero title-card expected font size 90" in errors
    assert "title drawtext fontsize mismatch" in errors


def test_top_banner_small_fade_title_card_fails(tmp_path: Path) -> None:
    title_card = base_title_card()
    title_card["layout"] = {
        "layout_zone": "top_banner",
        "anchor": "top_center",
        "x_pct": 0.5,
        "y_pct": 0.18,
        "width_pct": 0.36,
        "height_pct": 0.10,
        "safe_margin_bottom_to_subtitle_px": 260,
        "collision_avoidance": "none",
    }
    title_card["effect_style"] = {
        "font_size_min": 56,
        "text_effect": "black box",
        "entrance_effect": "fade_in",
        "entrance_effect_reason": "generic fade",
        "entrance_effect_selection": {
            "cue_role": "hook_keyword",
            "semantic_energy": "high",
            "visual_motion": "slow aerial push",
            "candidate_effects": ["fade_in"],
            "selection_reason": "generic",
            "diversity_check": "not checked",
        },
    }
    path = write_plan(tmp_path, title_card)

    report = validator.validate(path, require_title_card=True)

    assert not report["ok"]
    errors = "\n".join(report["errors"])
    assert "top-banner layout requires" in errors
    assert "font size 56 is below 90" in errors
    assert "entrance_effect 'fade_in'" in errors


def test_adjacent_repeated_hero_entrance_effect_requires_reason(tmp_path: Path) -> None:
    first = base_title_card()
    second = base_title_card()
    second["id"] = "tc-002"
    second["cue_indices"] = [2]
    second["script_span"] = [2.0, 4.0]
    second["audio_span"] = [2.0, 4.0]
    second["visual_span"] = [2.0, 4.0]
    second["card_text"] = "一键起飞"
    second["source_text"] = "一键起飞"
    path = write_plan_cards(tmp_path, [first, second])

    report = validator.validate(path, require_title_card=True)

    assert not report["ok"]
    assert "repeats entrance_effect 'kinetic_pop'" in "\n".join(report["errors"])


def test_picture_in_picture_overlay_passes(tmp_path: Path) -> None:
    path = write_pip_plan(tmp_path, base_picture_in_picture())

    report = validator.validate(path, require_pip=True)

    assert report["ok"], report["errors"]
    assert report["picture_in_picture_count"] == 1


def test_video_picture_in_picture_min_duration_passes(tmp_path: Path) -> None:
    pip_item = base_picture_in_picture()
    pip_item["pip_media_type"] = "video"
    pip_item["visual_span"] = [5.0, 9.0]
    pip_item["duration_policy"] = "video PiP hold extended to meet the 4s minimum"
    path = write_pip_plan(tmp_path, pip_item)

    report = validator.validate(
        path,
        require_pip=True,
        min_pip_video_duration=4,
        min_pip_image_duration=3,
        require_pip_duration_policy=True,
    )

    assert report["ok"], report["errors"]


def test_short_video_picture_in_picture_min_duration_fails(tmp_path: Path) -> None:
    pip_item = base_picture_in_picture()
    pip_item["pip_media_type"] = "video"
    pip_item["visual_span"] = [5.0, 8.2]
    pip_item["duration_policy"] = "video PiP hold claims to meet the 4s minimum"
    path = write_pip_plan(tmp_path, pip_item)

    report = validator.validate(
        path,
        require_pip=True,
        min_pip_video_duration=4,
        min_pip_image_duration=3,
        require_pip_duration_policy=True,
    )

    assert not report["ok"]
    assert "video PiP visual duration" in "\n".join(report["errors"])


def test_image_picture_in_picture_min_duration_passes(tmp_path: Path) -> None:
    pip_item = base_picture_in_picture()
    pip_item["pip_media_type"] = "image"
    pip_item["visual_span"] = [5.0, 8.0]
    pip_item["duration_policy"] = "image PiP hold meets the 3s minimum"
    pip_item["overlay_source"]["source_file"] = "素材/图片/result.png"
    path = write_pip_plan(tmp_path, pip_item)

    report = validator.validate(
        path,
        require_pip=True,
        min_pip_video_duration=4,
        min_pip_image_duration=3,
        require_pip_duration_policy=True,
    )

    assert report["ok"], report["errors"]


def test_short_image_picture_in_picture_min_duration_fails(tmp_path: Path) -> None:
    pip_item = base_picture_in_picture()
    pip_item["pip_media_type"] = "image"
    pip_item["visual_span"] = [5.0, 7.5]
    pip_item["duration_policy"] = "image PiP hold claims to meet the 3s minimum"
    pip_item["overlay_source"]["source_file"] = "素材/图片/result.png"
    path = write_pip_plan(tmp_path, pip_item)

    report = validator.validate(
        path,
        require_pip=True,
        min_pip_video_duration=4,
        min_pip_image_duration=3,
        require_pip_duration_policy=True,
    )

    assert not report["ok"]
    assert "image PiP visual duration" in "\n".join(report["errors"])


def test_aligned_three_up_picture_in_picture_group_passes(tmp_path: Path) -> None:
    path = write_pip_plan(tmp_path, aligned_picture_in_picture_group())
    dialogue_alignment = write_dialogue_alignment(tmp_path)

    report = validator.validate(
        path,
        dialogue_alignment=dialogue_alignment,
        require_pip=True,
        expected_pip_group_size=3,
        require_pip_aligned_groups=True,
        require_pip_cue_text_evidence=True,
    )

    assert report["ok"], report["errors"]
    assert report["picture_in_picture_count"] == 3


def test_expected_picture_in_picture_group_size_fails_on_two_windows(tmp_path: Path) -> None:
    path = write_pip_plan(tmp_path, aligned_picture_in_picture_group()[:2])

    report = validator.validate(
        path,
        require_pip=True,
        expected_pip_group_size=3,
        require_pip_aligned_groups=True,
    )

    errors = "\n".join(report["errors"])
    assert not report["ok"]
    assert "expected 3" in errors


def test_picture_in_picture_cue_text_evidence_required(tmp_path: Path) -> None:
    items = aligned_picture_in_picture_group()
    del items[0]["cue_text"]
    items[0]["content_evidence"] = "generic tool proof window without the current narration"
    path = write_pip_plan(tmp_path, items)
    dialogue_alignment = write_dialogue_alignment(tmp_path)

    report = validator.validate(
        path,
        dialogue_alignment=dialogue_alignment,
        require_pip=True,
        expected_pip_group_size=3,
        require_pip_aligned_groups=True,
        require_pip_cue_text_evidence=True,
    )

    assert not report["ok"]
    assert "cue text evidence missing current narration" in "\n".join(report["errors"])


def test_picture_in_picture_render_parity_checks_command_marker(tmp_path: Path) -> None:
    pip_item = add_render_evidence(base_picture_in_picture(), "pip_runtime_effect=pip-001", "scale_pop")
    path = write_pip_plan(tmp_path, pip_item)
    render_command = tmp_path / "render_command.txt"
    render_command.write_text("ffmpeg -filter_complex overlay=x=10:y=10", encoding="utf-8")

    report = validator.validate(
        path,
        render_command=render_command,
        require_pip=True,
        require_render_parity=True,
    )

    assert not report["ok"]
    assert "render command missing evidence marker" in "\n".join(report["errors"])


def test_picture_in_picture_missing_source_and_subtitle_clearance_fails(tmp_path: Path) -> None:
    pip_item = base_picture_in_picture()
    del pip_item["overlay_source"]
    pip_item["covers_subtitles"] = True
    pip_item["layout"]["width_pct"] = 0.78
    pip_item["layout"]["subtitle_clearance_px"] = 40
    pip_item["layer_order"] = "after_hard_subtitles"
    path = write_pip_plan(tmp_path, pip_item)

    report = validator.validate(path, require_pip=True)

    assert not report["ok"]
    errors = "\n".join(report["errors"])
    assert "overlay_source" in errors
    assert "subtitle clearance" in errors
    assert "must not cover hard subtitles" in errors
    assert "layer_order" in errors


def test_picture_in_picture_missing_density_and_position_strategy_fails(tmp_path: Path) -> None:
    pip_item = base_picture_in_picture()
    del pip_item["position_strategy"]
    path = write_pip_plan(tmp_path, pip_item, include_density_policy=False)

    report = validator.validate(path, require_pip=True)

    assert not report["ok"]
    errors = "\n".join(report["errors"])
    assert "missing pip_density_policy" in errors
    assert "missing position_strategy" in errors


def test_picture_in_picture_repeated_position_requires_reason(tmp_path: Path) -> None:
    first = base_picture_in_picture()
    second = base_picture_in_picture()
    second["id"] = "pip-002"
    second["cue_indices"] = [4]
    second["script_span"] = [8.2, 11.0]
    second["audio_span"] = [8.2, 11.0]
    second["visual_span"] = [8.2, 11.0]
    second["position_strategy"]["randomization_seed"] = "project-cue-4"
    path = write_pip_plan(tmp_path, [first, second])

    report = validator.validate(path, require_pip=True)

    assert not report["ok"]
    assert "repeats layout_zone 'hero_preview_band'" in "\n".join(report["errors"])


def test_visual_transition_plan_passes(tmp_path: Path) -> None:
    path = write_transition_plan(tmp_path, base_visual_transition())

    report = validator.validate(path, require_transitions=True)

    assert report["ok"], report["errors"]
    assert report["visual_transition_count"] == 1


def test_visual_transition_missing_density_and_evidence_fails(tmp_path: Path) -> None:
    transition = base_visual_transition()
    del transition["rhythm_sync"]
    del transition["safe_zone"]
    transition["transition_type"] = "generic_crossfade"
    transition["layer_order"] = "after_hard_subtitles"
    path = write_transition_plan(tmp_path, transition, include_density_policy=False)

    report = validator.validate(path, require_transitions=True)

    assert not report["ok"]
    errors = "\n".join(report["errors"])
    assert "missing transition_density_policy" in errors
    assert "transition_type 'generic_crossfade' is not governed" in errors
    assert "missing one of rhythm_sync" in errors
    assert "invalid layer_order" in errors


def test_visual_transition_missing_effect_richness_fails(tmp_path: Path) -> None:
    transition = base_visual_transition()
    transition["effect_style"] = {
        "motion": "generic blur",
        "readability_reason": "claims to clear subtitles",
    }
    path = write_transition_plan(tmp_path, transition)

    report = validator.validate(path, require_transitions=True)

    assert not report["ok"]
    errors = "\n".join(report["errors"])
    assert "missing effect_family" in errors
    assert "missing style_preset" in errors
    assert "missing intensity" in errors
    assert "missing one of parameters" in errors


def test_visual_transition_repeated_type_requires_reason(tmp_path: Path) -> None:
    first = base_visual_transition()
    second = base_visual_transition()
    second["id"] = "tr-002"
    second["cue_indices"] = [5]
    second["script_span"] = [12.0, 12.22]
    second["audio_span"] = [12.0, 12.22]
    second["visual_span"] = [12.0, 12.22]
    second["from_material_composition_id"] = "mc-result-005"
    second["to_material_composition_id"] = "mc-aigc-006"
    path = write_transition_plan(tmp_path, [first, second])

    report = validator.validate(path, require_transitions=True)

    assert not report["ok"]
    assert "repeats transition_type 'whip_pan_blur'" in "\n".join(report["errors"])


def test_visual_transition_repeated_effect_family_requires_reason(tmp_path: Path) -> None:
    first = base_visual_transition()
    second = base_visual_transition()
    second["id"] = "tr-002"
    second["transition_type"] = "match_cut"
    second["cue_indices"] = [5]
    second["script_span"] = [12.0, 12.18]
    second["audio_span"] = [12.0, 12.18]
    second["visual_span"] = [12.0, 12.18]
    second["duration_sec"] = 0.18
    second["from_material_composition_id"] = "mc-result-005"
    second["to_material_composition_id"] = "mc-aigc-006"
    second["effect_style"]["style_preset"] = "beat_punch_cut"
    second["effect_style"]["variation_reason"] = "same motion family is intentionally omitted to exercise validation"
    path = write_transition_plan(tmp_path, [first, second])

    report = validator.validate(path, require_transitions=True)

    assert not report["ok"]
    assert "repeats effect_family 'motion_bridge'" in "\n".join(report["errors"])
