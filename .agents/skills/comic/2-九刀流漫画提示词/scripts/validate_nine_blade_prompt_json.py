#!/usr/bin/env python3
"""Validate nine_blade_comic_prompts.v1 JSON for downstream comic generation."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any


REQUIRED_HARD_CONSTRAINTS = [
    "9 separate",
    "nine-grid",
    "variations of the same scene",
    "multiple comic panels",
]

STYLE_KEYWORDS = [
    "manga",
    "comic",
    "panel",
    "gutter",
    "ink",
    "line art",
    "screentone",
    "sfx",
    "printed",
]

DYNAMIC_LAYOUT_KEYWORDS = [
    "splash",
    "inset",
    "diagonal",
    "split",
    "cascade",
    "impact",
    "cliffhanger",
    "border",
    "zigzag",
    "asymmetric",
    "overlapping",
    "noir",
]

MAIN_CHARACTER_ANCHOR_KEYWORDS = [
    "character locked across all panels",
    "consistent face",
    "consistent costume",
]


def _self_test_data() -> dict[str, Any]:
    pages: list[dict[str, Any]] = []
    layout_ids = [
        "splash-with-insets",
        "asymmetric-investigation-page",
        "diagonal-cut-action",
        "split-diopter-page",
        "vertical-cascade",
        "impact-sfx-page",
        "silent-reaction-grid",
        "border-breaking-cliffhanger",
        "noir-evidence-strip",
    ]
    for page_number in range(1, 10):
        active_character_ids = (
            ["protagonist", "companion"] if page_number in {2, 3, 4, 6} else ["protagonist"]
        )
        prompt_parts = [
            "cinematic comic page, vertical 9:16 aspect ratio",
            f"Page {page_number}",
            "Character locked across all panels: Sun Wukong, a muscular monkey demon with golden fur, consistent face, consistent costume, consistent silhouette",
        ]
        if len(active_character_ids) >= 2:
            prompt_parts.append(
                "Zhu Bajie remains visually consistent and clearly distinguishable with heavy build, round snout, patched vest"
            )
        prompt_parts.extend(
            [
                "scene locked across relevant pages: Thunder Gate Courtyard, black stone gate, lightning totems, consistent architecture and landmark props",
                f"place page number \"{page_number}\" in the bottom-right corner, digits only",
                "keep character and scene consistency across all pages",
                f"unique visible action {page_number}",
            ]
        )
        pages.append(
            {
                "page_number": page_number,
                "page_role": f"story beat {page_number}",
                "source_fragment": f"source fragment {page_number}",
                "active_character_ids": active_character_ids,
                "scene_id": "thunder_gate",
                "layout": {
                    "aspect_ratio": "9:16",
                    "layout_id": layout_ids[page_number - 1],
                    "panel_count": 2,
                    "panel_ratios": ["dominant irregular panel 70%", "supporting inset/reaction panel 30%"],
                },
                "panels": [
                    {
                        "panel_id": f"{page_number}A",
                        "shot": "dramatic comic shot",
                        "action": f"unique visible action {page_number}",
                        "comic_techniques": ["bold gutter"],
                        "text_slots": [
                            {"type": "narration", "text": f"第{page_number}页"}
                        ],
                    },
                    {
                        "panel_id": f"{page_number}B",
                        "shot": "supporting reaction or detail panel",
                        "action": f"supporting visible action {page_number}",
                        "comic_techniques": ["reaction inset"],
                        "text_slots": [],
                    }
                ],
                "page_number_overlay": {
                    "text": str(page_number),
                    "position": "bottom-right",
                    "style_prompt": (
                        f"place page number \"{page_number}\" in the bottom-right corner, "
                        "digits only, small but readable"
                    ),
                },
                "positive_prompt": ", ".join(prompt_parts),
            }
        )
    return {
        "schema_version": "nine_blade_comic_prompts.v1",
        "generation_contract": {
            "provider": "seedream",
            "call_mode": "single_request_sequential",
            "image_count": 9,
            "page_aspect_ratio": "9:16",
            "seedream": {"max_images": 9, "size": "2K", "stream": True},
            "hard_constraints": [
                "Generate exactly 9 separate images/pages.",
                "Do not create a nine-grid collage.",
                "Do not create nine variations of the same scene.",
                "Every page must contain multiple comic panels, never a single full-page illustration.",
                "Keep character and scene consistency across all pages.",
                "Place a small page number in the bottom-right corner of every page, using digits 1-9 only.",
            ],
        },
        "main_character_lock": {
            "character_id": "protagonist",
            "name": "Sun Wukong",
            "anchor_prompt": (
                "Character locked across all panels: Sun Wukong, "
                "a muscular monkey demon with golden fur, a pronounced thunder-god mouth, "
                "sunken eyes with bright golden pupils, wearing a tattered grey-brown Daoist robe, "
                "consistent face, costume, silhouette and color palette in every panel and every page."
            ),
        },
        "scene_continuity_bible": {
            "default_rule": (
                "Keep recurring locations consistent in architecture, landmark props, "
                "lighting mood, and spatial geography across all relevant pages."
            ),
            "scene_locks": [
                {
                    "scene_id": "thunder_gate",
                    "name": "Thunder Gate Courtyard",
                    "anchor_prompt": (
                        "Scene locked across relevant pages: Thunder Gate Courtyard, "
                        "black stone gate, lightning totems, cracked steps, storm-dark sky, "
                        "consistent architecture, landmark props, lighting mood and spatial geography."
                    ),
                }
            ],
        },
        "style_bible": {
            "base_style": "cinematic comic realism",
            "manga_style_keywords": [
                "dynamic manga paneling",
                "dramatic inked line art",
                "high contrast black gutters",
                "oversized SFX",
            ],
        },
        "character_locks": [
            {
                "character_id": "companion",
                "name": "Zhu Bajie",
                "anchor_prompt": (
                    "Character locked across all relevant pages: Zhu Bajie, heavy build, "
                    "round snout, patched vest, clearly distinguishable from Sun Wukong."
                ),
            }
        ],
        "comic_text_system": {"narration": "rectangular caption box"},
        "pages": pages,
        "global_negative_prompt": (
            "collage, nine variations, unreadable Chinese text, watermark"
        ),
    }


def _load_json(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as fh:
        data = json.load(fh)
    if not isinstance(data, dict):
        raise ValueError("root must be a JSON object")
    return data


def _contains(texts: list[str], needle: str) -> bool:
    needle = needle.lower()
    return any(needle in text.lower() for text in texts)


def _has_character_scene_consistency(text: str) -> bool:
    lower = text.lower()
    has_character = "character" in lower
    has_scene = "scene" in lower or "location" in lower
    has_consistency = (
        "consistent" in lower
        or "consistency" in lower
        or "continuity" in lower
    )
    return has_character and has_scene and has_consistency


def _has_main_character_anchor(text: str, character_name: str) -> bool:
    lower = text.lower()
    if character_name.lower() not in lower:
        return False
    return any(keyword in lower for keyword in MAIN_CHARACTER_ANCHOR_KEYWORDS)


def _has_bottom_right_numeric_page_number(text: str, page_number: int) -> bool:
    lower = text.lower()
    has_position = "bottom-right" in lower or "bottom right" in lower
    has_numeric_only = (
        "digits only" in lower
        or "numeric only" in lower
        or "pure digits" in lower
    )
    has_number = f"\"{page_number}\"" in text or f" {page_number} " in f" {text} "
    return has_position and has_numeric_only and has_number


def _mentioned_names(text: str, names: list[str]) -> list[str]:
    lower = text.lower()
    return [name for name in names if name.lower() in lower]


def _stringify(value: Any) -> str:
    if isinstance(value, str):
        return value
    return json.dumps(value, ensure_ascii=False)


def validate(data: dict[str, Any]) -> list[str]:
    errors: list[str] = []

    if data.get("schema_version") != "nine_blade_comic_prompts.v1":
        errors.append("schema_version must be nine_blade_comic_prompts.v1")

    contract = data.get("generation_contract")
    if not isinstance(contract, dict):
        errors.append("generation_contract must be an object")
        contract = {}

    if contract.get("provider") != "seedream":
        errors.append("generation_contract.provider must be seedream")
    if contract.get("call_mode") != "single_request_sequential":
        errors.append("generation_contract.call_mode must be single_request_sequential")
    if contract.get("image_count") != 9:
        errors.append("generation_contract.image_count must be 9")
    if contract.get("page_aspect_ratio") != "9:16":
        errors.append("generation_contract.page_aspect_ratio must be 9:16")

    hard_constraints = contract.get("hard_constraints")
    if not isinstance(hard_constraints, list) or not all(isinstance(x, str) for x in hard_constraints):
        errors.append("generation_contract.hard_constraints must be a string array")
        hard_constraints = []
    for needle in REQUIRED_HARD_CONSTRAINTS:
        if not _contains(hard_constraints, needle):
            errors.append(f"hard_constraints must mention {needle!r}")
    joined_constraints = " ".join(hard_constraints)
    if not _has_character_scene_consistency(joined_constraints):
        errors.append(
            "hard_constraints must explicitly require character and scene consistency"
        )
    if "bottom-right" not in joined_constraints.lower() or "digits 1-9 only" not in joined_constraints.lower():
        errors.append(
            "hard_constraints must require a bottom-right digits-only page number on every page"
        )

    seedream = contract.get("seedream", {})
    if isinstance(seedream, dict) and seedream.get("max_images") not in (None, 9):
        errors.append("generation_contract.seedream.max_images must be 9 when present")

    main_character_lock = data.get("main_character_lock")
    if not isinstance(main_character_lock, dict):
        errors.append("main_character_lock must be an object")
        main_character_lock = {}
    main_character_id = str(main_character_lock.get("character_id", "")).strip()
    main_character_name = str(main_character_lock.get("name", "")).strip()
    main_character_anchor = str(main_character_lock.get("anchor_prompt", "")).strip()
    if not main_character_id:
        errors.append("main_character_lock.character_id must be a non-empty string")
    if not main_character_name:
        errors.append("main_character_lock.name must be a non-empty string")
    if len(main_character_anchor) < 40:
        errors.append("main_character_lock.anchor_prompt must be a detailed anchor string")
    else:
        anchor_lower = main_character_anchor.lower()
        if "character locked across all panels" not in anchor_lower:
            errors.append(
                "main_character_lock.anchor_prompt should include 'Character locked across all panels'"
            )
        if "consistent" not in anchor_lower:
            errors.append(
                "main_character_lock.anchor_prompt should explicitly describe stable appearance semantics"
            )
        if main_character_name and main_character_name.lower() not in anchor_lower:
            errors.append(
                "main_character_lock.anchor_prompt must include main_character_lock.name"
            )

    scene_continuity_bible = data.get("scene_continuity_bible")
    scene_names_by_id: dict[str, str] = {}
    if not isinstance(scene_continuity_bible, dict):
        errors.append("scene_continuity_bible must be an object")
        scene_continuity_bible = {}
    default_rule = str(scene_continuity_bible.get("default_rule", "")).strip()
    if len(default_rule) < 20:
        errors.append("scene_continuity_bible.default_rule must be a descriptive rule")
    scene_locks = scene_continuity_bible.get("scene_locks")
    if not isinstance(scene_locks, list) or not scene_locks:
        errors.append("scene_continuity_bible.scene_locks must be a non-empty array")
        scene_locks = []
    for index, scene_lock in enumerate(scene_locks, start=1):
        if not isinstance(scene_lock, dict):
            errors.append(f"scene_continuity_bible.scene_locks[{index}] must be an object")
            continue
        scene_id = str(scene_lock.get("scene_id", "")).strip()
        scene_name = str(scene_lock.get("name", "")).strip()
        anchor_prompt = str(scene_lock.get("anchor_prompt", "")).strip()
        if not scene_id:
            errors.append(f"scene_continuity_bible.scene_locks[{index}].scene_id must be non-empty")
            continue
        if not scene_name:
            errors.append(f"scene_continuity_bible.scene_locks[{index}].name must be non-empty")
        if len(anchor_prompt) < 40:
            errors.append(
                f"scene_continuity_bible.scene_locks[{index}].anchor_prompt must be detailed"
            )
        scene_names_by_id[scene_id] = scene_name

    character_names_by_id: dict[str, str] = {}
    if main_character_id:
        character_names_by_id[main_character_id] = main_character_name

    character_locks = data.get("character_locks")
    if not isinstance(character_locks, list):
        errors.append("character_locks must be an array")
        character_locks = []
    for index, lock in enumerate(character_locks, start=1):
        if not isinstance(lock, dict):
            errors.append(f"character_locks[{index}] must be an object")
            continue
        character_id = str(lock.get("character_id", "")).strip()
        name = str(lock.get("name", "")).strip()
        anchor_prompt = str(lock.get("anchor_prompt", "")).strip()
        if not character_id:
            errors.append(f"character_locks[{index}].character_id must be non-empty")
            continue
        if not name:
            errors.append(f"character_locks[{index}].name must be non-empty")
        if len(anchor_prompt) < 20:
            errors.append(f"character_locks[{index}].anchor_prompt must be descriptive")
        character_names_by_id[character_id] = name

    style_bible = data.get("style_bible")
    if not isinstance(style_bible, dict):
        errors.append("style_bible must be an object")
        style_bible = {}
    style_text = _stringify(style_bible).lower()
    style_hits = [keyword for keyword in STYLE_KEYWORDS if keyword in style_text]
    if len(style_hits) < 3:
        errors.append(
            "style_bible must include sharper comic style grammar, "
            "for example manga/comic, ink or line art, gutters, panels, screentone, SFX"
        )

    pages = data.get("pages")
    if not isinstance(pages, list):
        errors.append("pages must be an array")
        pages = []
    if len(pages) != 9:
        errors.append("pages must contain exactly 9 page objects")

    seen_page_numbers: set[int] = set()
    layout_ids: list[str] = []
    dynamic_layout_count = 0
    for i, page in enumerate(pages, start=1):
        if not isinstance(page, dict):
            errors.append(f"pages[{i}] must be an object")
            continue
        page_number = page.get("page_number")
        if page_number != i:
            errors.append(f"pages[{i}] page_number must be {i}")
        if isinstance(page_number, int):
            seen_page_numbers.add(page_number)

        layout = page.get("layout")
        if not isinstance(layout, dict):
            errors.append(f"pages[{i}].layout must be an object")
            layout = {}
        layout_id = layout.get("layout_id")
        if isinstance(layout_id, str):
            layout_ids.append(layout_id)
            layout_text = _stringify(layout).lower()
            if any(keyword in layout_text for keyword in DYNAMIC_LAYOUT_KEYWORDS):
                dynamic_layout_count += 1
        if layout.get("aspect_ratio") != "9:16":
            errors.append(f"pages[{i}].layout.aspect_ratio must be 9:16")
        panel_count = layout.get("panel_count")
        panels = page.get("panels")
        if not isinstance(panels, list) or not panels:
            errors.append(f"pages[{i}].panels must be a non-empty array")
            panels = []
        if isinstance(panel_count, int) and panel_count != len(panels):
            errors.append(f"pages[{i}].layout.panel_count must match panels length")
        if isinstance(panel_count, int) and panel_count < 2:
            errors.append(f"pages[{i}].layout.panel_count must be at least 2 for a multi-panel comic page")
        if isinstance(panels, list) and len(panels) < 2:
            errors.append(f"pages[{i}].panels must contain at least 2 panels for a multi-panel comic page")

        active_character_ids = page.get("active_character_ids")
        if not isinstance(active_character_ids, list) or not active_character_ids:
            errors.append(f"pages[{i}].active_character_ids must be a non-empty array")
            active_character_ids = []
        else:
            unknown_character_ids = [
                character_id
                for character_id in active_character_ids
                if character_id not in character_names_by_id
            ]
            if unknown_character_ids:
                errors.append(
                    f"pages[{i}].active_character_ids contains unknown ids: {unknown_character_ids}"
                )

        scene_id = str(page.get("scene_id", "")).strip()
        if not scene_id:
            errors.append(f"pages[{i}].scene_id must be a non-empty string")
        elif scene_id not in scene_names_by_id:
            errors.append(f"pages[{i}].scene_id must reference scene_continuity_bible.scene_locks")

        page_number_overlay = page.get("page_number_overlay")
        if not isinstance(page_number_overlay, dict):
            errors.append(f"pages[{i}].page_number_overlay must be an object")
            page_number_overlay = {}
        else:
            overlay_text = str(page_number_overlay.get("text", "")).strip()
            if overlay_text != str(i):
                errors.append(f"pages[{i}].page_number_overlay.text must equal '{i}'")
            position = str(page_number_overlay.get("position", "")).strip().lower()
            if position != "bottom-right":
                errors.append(f"pages[{i}].page_number_overlay.position must be bottom-right")
            style_prompt = str(page_number_overlay.get("style_prompt", "")).strip()
            if len(style_prompt) < 20:
                errors.append(f"pages[{i}].page_number_overlay.style_prompt must be descriptive")
            elif not _has_bottom_right_numeric_page_number(style_prompt, i):
                errors.append(
                    f"pages[{i}].page_number_overlay.style_prompt must require bottom-right digits-only page number {i}"
                )

        positive_prompt = page.get("positive_prompt")
        if not isinstance(positive_prompt, str) or not positive_prompt.strip():
            errors.append(f"pages[{i}].positive_prompt must be a non-empty string")
        else:
            if "9:16" not in positive_prompt:
                errors.append(f"pages[{i}].positive_prompt must mention 9:16")
            if main_character_name and not _has_main_character_anchor(
                positive_prompt, main_character_name
            ):
                errors.append(
                    f"pages[{i}].positive_prompt must inject the main character anchor with {main_character_name}"
                )
            if not _has_character_scene_consistency(positive_prompt):
                errors.append(
                    f"pages[{i}].positive_prompt must mention character and scene consistency"
                )
            if not _has_bottom_right_numeric_page_number(positive_prompt, i):
                errors.append(
                    f"pages[{i}].positive_prompt must require bottom-right digits-only page number {i}"
                )
            if scene_id in scene_names_by_id:
                scene_name = scene_names_by_id[scene_id]
                if scene_name.lower() not in positive_prompt.lower():
                    errors.append(
                        f"pages[{i}].positive_prompt must mention the active scene lock name {scene_name!r}"
                    )
            if len(active_character_ids) >= 2:
                active_names = [
                    character_names_by_id[character_id]
                    for character_id in active_character_ids
                    if character_id in character_names_by_id
                ]
                mentioned = _mentioned_names(positive_prompt, active_names)
                if len(mentioned) < 2:
                    errors.append(
                        f"pages[{i}].positive_prompt must mention at least two active recurring character names for multi-character pages"
                    )

        for panel in panels:
            if not isinstance(panel, dict):
                errors.append(f"pages[{i}].panels entries must be objects")
                continue
            if not panel.get("panel_id"):
                errors.append(f"pages[{i}] panel missing panel_id")
            if not panel.get("shot"):
                errors.append(f"pages[{i}] panel missing shot")
            if not panel.get("action"):
                errors.append(f"pages[{i}] panel missing action")
            text_slots = panel.get("text_slots", [])
            if not isinstance(text_slots, list):
                errors.append(f"pages[{i}] panel text_slots must be an array")
                continue
            for slot in text_slots:
                if not isinstance(slot, dict):
                    errors.append(f"pages[{i}] text slot must be an object")
                    continue
                if slot.get("type") not in {"dialogue", "narration", "inner_monologue", "sfx"}:
                    errors.append(f"pages[{i}] text slot has invalid type")
                if not isinstance(slot.get("text"), str):
                    errors.append(f"pages[{i}] text slot text must be a string")

    if seen_page_numbers and seen_page_numbers != set(range(1, 10)):
        errors.append("page_number values must be exactly 1..9")

    if len(pages) == 9:
        if len(set(layout_ids)) < 5:
            errors.append("pages[].layout_id must use at least 5 distinct layouts across 9 pages")
        if dynamic_layout_count < 3:
            errors.append(
                "pages[].layout should include at least 3 dynamic classic comic layouts "
                "(splash, inset, diagonal, split, cascade, impact, cliffhanger, border-breaking, zigzag, asymmetric)"
            )

    negative = data.get("global_negative_prompt")
    if not isinstance(negative, str) or not negative.strip():
        errors.append("global_negative_prompt must be a non-empty string")
    else:
        lower_negative = negative.lower()
        for needle in ["collage", "variations", "watermark", "unreadable"]:
            if needle not in lower_negative:
                errors.append(f"global_negative_prompt should mention {needle!r}")

    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate nine_blade_comic_prompts.v1 JSON")
    parser.add_argument("json_path", nargs="?", type=Path)
    parser.add_argument("--self-test", action="store_true", help="Run an in-memory validator self-test")
    args = parser.parse_args()

    if args.self_test:
        errors = validate(_self_test_data())
        if errors:
            print("FAIL")
            for error in errors:
                print(f"- {error}")
            return 1
        print("PASS self-test")
        return 0

    if args.json_path is None:
        parser.error("json_path is required unless --self-test is used")

    try:
        errors = validate(_load_json(args.json_path))
    except Exception as exc:
        print(f"FAIL: {exc}", file=sys.stderr)
        return 2

    if errors:
        print("FAIL")
        for error in errors:
            print(f"- {error}")
        return 1

    print("PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
