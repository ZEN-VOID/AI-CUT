#!/usr/bin/env python3
"""Validate comic episode poster design JSON."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any


EPISODE_LABEL_RE = re.compile(r"^第\d+集$")
ALLOWED_ASPECTS = {"3:4", "9:16", "2:3"}
MIN_PROMPT_LENGTH = 24


def load_json(path: Path) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        raise SystemExit(f"[FAIL] file not found: {path}")
    except json.JSONDecodeError as exc:
        raise SystemExit(f"[FAIL] invalid json: {exc}")


def expect(condition: bool, message: str, errors: list[str]) -> None:
    if not condition:
        errors.append(message)


def validate(data: dict[str, Any]) -> list[str]:
    errors: list[str] = []

    expect(data.get("schema_version") == "comic_episode_poster_design.v1", "schema_version must be comic_episode_poster_design.v1", errors)

    episode = data.get("episode", {})
    expect(isinstance(episode.get("number"), int) and episode["number"] >= 1, "episode.number must be an integer >= 1", errors)
    expect(isinstance(episode.get("display_text"), str) and EPISODE_LABEL_RE.match(episode["display_text"]) is not None, "episode.display_text must match 第N集", errors)

    upstream_context = data.get("upstream_context", {})
    loaded_artifacts = upstream_context.get("loaded_artifacts", [])
    expect(isinstance(loaded_artifacts, list) and len(loaded_artifacts) >= 2, "upstream_context.loaded_artifacts must contain at least 2 upstream artifacts", errors)
    loaded_roles = {item.get("role") for item in loaded_artifacts if isinstance(item, dict)}
    expect("bridge_pack" in loaded_roles, "upstream_context.loaded_artifacts must include bridge_pack", errors)
    expect("nine_blade_json" in loaded_roles, "upstream_context.loaded_artifacts must include nine_blade_json", errors)

    style_inheritance = upstream_context.get("style_inheritance", {})
    expect(bool(style_inheritance.get("character_stage_anchor")), "upstream_context.style_inheritance.character_stage_anchor is required", errors)
    expect(bool(style_inheritance.get("scene_continuity_anchor")), "upstream_context.style_inheritance.scene_continuity_anchor is required", errors)
    expect(bool(style_inheritance.get("style_anchor")), "upstream_context.style_inheritance.style_anchor is required", errors)

    highlight_discovery = upstream_context.get("highlight_discovery", {})
    candidate_highlights = highlight_discovery.get("candidate_highlights", [])
    expect(isinstance(candidate_highlights, list) and len(candidate_highlights) >= 3, "upstream_context.highlight_discovery.candidate_highlights must contain at least 3 candidates", errors)
    expect(bool(highlight_discovery.get("selected_highlight")), "upstream_context.highlight_discovery.selected_highlight is required", errors)
    expect(bool(highlight_discovery.get("selection_reason")), "upstream_context.highlight_discovery.selection_reason is required", errors)

    thinking = data.get("thinking_process", {})
    expect(isinstance(thinking, dict) and bool(thinking), "thinking_process must be a non-empty object", errors)
    expect(bool(thinking.get("highlight_selection_reason")), "thinking_process.highlight_selection_reason is required", errors)
    expect(bool(thinking.get("style_consistency_reason")), "thinking_process.style_consistency_reason is required", errors)

    creative = data.get("creative_direction", {})
    expect(bool(creative.get("creative_core")), "creative_direction.creative_core is required", errors)
    expect(bool(creative.get("representative_scene")), "creative_direction.representative_scene is required", errors)
    expect(bool(creative.get("hook_meaning")), "creative_direction.hook_meaning is required", errors)

    subject_lock = data.get("subject_lock", {})
    primary_subjects = subject_lock.get("primary_subjects", [])
    expect(subject_lock.get("only_current_episode_characters") is True, "subject_lock.only_current_episode_characters must be true", errors)
    expect(isinstance(primary_subjects, list) and len(primary_subjects) >= 1, "subject_lock.primary_subjects must contain at least 1 subject", errors)

    composition = data.get("composition", {})
    expect(composition.get("aspect_ratio") in ALLOWED_ASPECTS, "composition.aspect_ratio must be one of 3:4, 9:16, 2:3", errors)
    expect(bool(composition.get("foreground")), "composition.foreground is required", errors)
    expect(bool(composition.get("subjects")), "composition.subjects is required", errors)
    expect(bool(composition.get("background")), "composition.background is required", errors)

    text_system = data.get("text_system", {})
    episode_label = text_system.get("episode_label", {})
    hook_title = text_system.get("hook_title", {})
    expect(text_system.get("horizontal_alignment") == "center", "text_system.horizontal_alignment must be center", errors)
    expect(text_system.get("vertical_alignment") == "center", "text_system.vertical_alignment must be center", errors)
    expect(episode_label.get("text") == episode.get("display_text"), "text_system.episode_label.text must equal episode.display_text", errors)
    episode_label_position = episode_label.get("position", {})
    hook_title_position = hook_title.get("position", {})
    expect(
        isinstance(episode_label_position, dict)
        and episode_label_position.get("horizontal") == "center"
        and episode_label_position.get("vertical") == "center",
        "text_system.episode_label.position must be horizontally and vertically centered",
        errors,
    )
    expect(
        isinstance(hook_title_position, dict)
        and hook_title_position.get("horizontal") == "center"
        and hook_title_position.get("vertical") == "center",
        "text_system.hook_title.position must be horizontally and vertically centered",
        errors,
    )
    expect(hook_title.get("language") in {"zh-CN", "zh"}, "text_system.hook_title.language should default to Chinese", errors)
    expect(bool(hook_title.get("text")), "text_system.hook_title.text is required", errors)
    if isinstance(hook_title.get("text"), str) and isinstance(episode_label.get("text"), str):
        expect(hook_title["text"] != episode_label["text"], "hook_title.text must differ from episode label", errors)

    atmosphere = data.get("atmosphere_color", {})
    expect(bool(atmosphere.get("mood")), "atmosphere_color.mood is required", errors)
    expect(isinstance(atmosphere.get("dominant_colors"), list) and len(atmosphere["dominant_colors"]) >= 1, "atmosphere_color.dominant_colors must contain at least 1 color", errors)
    expect(isinstance(atmosphere.get("accent_colors"), list) and len(atmosphere["accent_colors"]) >= 1, "atmosphere_color.accent_colors must contain at least 1 color", errors)
    expect(bool(atmosphere.get("lighting_strategy")), "atmosphere_color.lighting_strategy is required", errors)

    prompt_package = data.get("prompt_package", {})
    positive_prompt = str(prompt_package.get("positive_prompt", "")).strip()
    expect(bool(positive_prompt), "prompt_package.positive_prompt is required", errors)
    expect(
        len(positive_prompt) >= MIN_PROMPT_LENGTH,
        f"prompt_package.positive_prompt must be at least {MIN_PROMPT_LENGTH} characters to remain directly usable for downstream generation",
        errors,
    )

    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate comic episode poster design JSON.")
    parser.add_argument("json_path", help="Path to comic episode poster design JSON")
    args = parser.parse_args()

    data = load_json(Path(args.json_path))
    if not isinstance(data, dict):
        print("[FAIL] root must be a JSON object")
        return 1

    errors = validate(data)
    if errors:
        print("[FAIL] validation errors:")
        for error in errors:
            print(f"- {error}")
        return 1

    print("[PASS] comic episode poster design json is valid")
    return 0


if __name__ == "__main__":
    sys.exit(main())
