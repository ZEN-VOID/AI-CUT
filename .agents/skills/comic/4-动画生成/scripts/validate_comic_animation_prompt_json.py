#!/usr/bin/env python3
"""Validate comic_page_animation_prompts.v1 JSON."""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any


FIXED_PROMPT_PREFIX = (
    "Animate this vertical comic strip into a seamless, continuous cinematic video. "
    "Chronological sequence from right to left, top to bottom panels. "
    "Advanced camera movement transitioning smoothly between scenes. "
    "High-fidelity motion physics, 4K resolution, masterpiece quality."
)


def expect(condition: bool, message: str, errors: list[str]) -> None:
    if not condition:
        errors.append(message)


def _load_json(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as fh:
        data = json.load(fh)
    if not isinstance(data, dict):
        raise ValueError("root must be a JSON object")
    return data


def validate(data: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    expect(
        data.get("schema_version") == "comic_page_animation_prompts.v1",
        "schema_version must be comic_page_animation_prompts.v1",
        errors,
    )
    expect(
        data.get("prompt_prefix") == FIXED_PROMPT_PREFIX,
        "prompt_prefix must equal the fixed animation prefix",
        errors,
    )

    contract = data.get("video_generation_contract", {})
    expect(isinstance(contract, dict), "video_generation_contract must be an object", errors)
    if isinstance(contract, dict):
        expect(contract.get("provider") == "sora", "provider must be sora", errors)
        expect(contract.get("mode") == "image_to_video", "mode must be image_to_video", errors)
        expect(contract.get("aspect_ratio") == "9:16", "aspect_ratio must be 9:16", errors)
        expect(contract.get("seconds") in {4, 8, 12}, "seconds must be one of 4/8/12", errors)
        expect(
            contract.get("size") in {"720x1280", "1280x720", "1024x1792", "1792x1024"},
            "size must be one of the sora supported dimensions",
            errors,
        )

    pages = data.get("pages", [])
    expect(isinstance(pages, list), "pages must be an array", errors)
    expect(len(pages) == 9, "pages must contain exactly 9 items", errors)
    if not isinstance(pages, list):
        return errors

    for expected_page_number, page in enumerate(pages, start=1):
        expect(isinstance(page, dict), f"pages[{expected_page_number - 1}] must be an object", errors)
        if not isinstance(page, dict):
            continue
        page_number = page.get("page_number")
        expect(
            page_number == expected_page_number,
            f"pages[{expected_page_number - 1}].page_number must equal {expected_page_number}",
            errors,
        )
        source_image = str(page.get("source_image", "")).strip()
        expect(bool(source_image), f"pages[{expected_page_number - 1}].source_image is required", errors)
        if source_image:
            expect(
                Path(source_image).exists(),
                f"pages[{expected_page_number - 1}].source_image does not exist: {source_image}",
                errors,
            )

        storyboard_policy = page.get("storyboard_policy", {})
        expect(
            isinstance(storyboard_policy, dict),
            f"pages[{expected_page_number - 1}].storyboard_policy must be an object",
            errors,
        )
        if isinstance(storyboard_policy, dict):
            expect(
                storyboard_policy.get("panel_to_shot") == "one_panel_one_shot_default",
                f"pages[{expected_page_number - 1}].storyboard_policy.panel_to_shot must be one_panel_one_shot_default",
                errors,
            )
            expect(
                storyboard_policy.get("reading_order") == "right_to_left_top_to_bottom",
                f"pages[{expected_page_number - 1}].storyboard_policy.reading_order must be right_to_left_top_to_bottom",
                errors,
            )

        shot_plan = page.get("shot_plan", [])
        expect(
            isinstance(shot_plan, list) and len(shot_plan) >= 1,
            f"pages[{expected_page_number - 1}].shot_plan must contain at least one shot",
            errors,
        )
        if isinstance(shot_plan, list):
            for shot_index, shot in enumerate(shot_plan, start=1):
                expect(
                    isinstance(shot, dict),
                    f"pages[{expected_page_number - 1}].shot_plan[{shot_index - 1}] must be an object",
                    errors,
                )
                if not isinstance(shot, dict):
                    continue
                expect(
                    shot.get("shot_index") == shot_index,
                    f"pages[{expected_page_number - 1}].shot_plan[{shot_index - 1}].shot_index must be {shot_index}",
                    errors,
                )
                for key in ("source_panel_id", "shot", "action", "camera_motion", "subject_motion"):
                    expect(
                        bool(str(shot.get(key, "")).strip()),
                        f"pages[{expected_page_number - 1}].shot_plan[{shot_index - 1}].{key} is required",
                        errors,
                    )

        sora_prompt = str(page.get("sora_prompt", ""))
        expect(
            sora_prompt.startswith(FIXED_PROMPT_PREFIX),
            f"pages[{expected_page_number - 1}].sora_prompt must start with the fixed animation prefix",
            errors,
        )
        for snippet in (
            "Preserve the exact source image composition",
            "one panel becomes one cinematic shot by default",
            "Do not add new panels, characters, props, or story beats",
        ):
            expect(
                snippet in sora_prompt,
                f"pages[{expected_page_number - 1}].sora_prompt missing required snippet: {snippet}",
                errors,
            )

    return errors


def main() -> int:
    if len(sys.argv) != 2:
        print("Usage: validate_comic_animation_prompt_json.py <path>", file=sys.stderr)
        return 2

    path = Path(sys.argv[1]).resolve()
    data = _load_json(path)
    errors = validate(data)
    if errors:
        for item in errors:
            print(f"ERROR: {item}", file=sys.stderr)
        print(f"FAIL: {len(errors)} validation error(s)", file=sys.stderr)
        return 1

    print("PASS")
    return 0


if __name__ == "__main__":
    sys.exit(main())
