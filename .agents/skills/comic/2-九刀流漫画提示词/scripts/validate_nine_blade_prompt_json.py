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
]

STYLE_KEYWORDS = [
    "manga",
    "comic",
    "panel",
    "gutter",
    "ink",
    "line art",
    "screentone",
    "SFX",
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
        pages.append(
            {
                "page_number": page_number,
                "page_role": f"story beat {page_number}",
                "source_fragment": f"source fragment {page_number}",
                "layout": {
                    "aspect_ratio": "9:16",
                    "layout_id": layout_ids[page_number - 1],
                    "panel_count": 1,
                    "panel_ratios": ["dominant irregular panel with inset/reaction area"],
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
                    }
                ],
                "positive_prompt": (
                    f"cinematic comic page, vertical 9:16 aspect ratio, "
                    f"Page {page_number}, keep character and scene consistency "
                    f"across all pages, unique visible action {page_number}"
                ),
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
                "Keep character and scene consistency across all pages.",
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
        "character_locks": [],
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
    if not _has_character_scene_consistency(" ".join(hard_constraints)):
        errors.append(
            "hard_constraints must explicitly require character and scene consistency"
        )

    seedream = contract.get("seedream", {})
    if isinstance(seedream, dict) and seedream.get("max_images") not in (None, 9):
        errors.append("generation_contract.seedream.max_images must be 9 when present")

    style_bible = data.get("style_bible")
    if not isinstance(style_bible, dict):
        errors.append("style_bible must be an object")
        style_bible = {}
    style_text = _stringify(style_bible).lower()
    style_hits = [keyword for keyword in STYLE_KEYWORDS if keyword.lower() in style_text]
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

        positive_prompt = page.get("positive_prompt")
        if not isinstance(positive_prompt, str) or not positive_prompt.strip():
            errors.append(f"pages[{i}].positive_prompt must be a non-empty string")
        else:
            if "9:16" not in positive_prompt:
                errors.append(f"pages[{i}].positive_prompt must mention 9:16")
            if not _has_character_scene_consistency(positive_prompt):
                errors.append(
                    f"pages[{i}].positive_prompt must mention character and scene consistency"
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
