#!/usr/bin/env python3
"""Validate the minimum structure of Story2026 planning story_map output."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


REQUIRED_HOLOMAP_KEYS = [
    "story_promise",
    "genre_corridor",
    "story_spine",
    "timeline_axis",
    "space_axis",
    "episode_sequence_axis",
    "volume_boards",
    "chapter_boards",
    "conflict_threads",
    "mission_threads",
    "clue_threads",
    "foreshadow_threads",
    "cross_thread_indexes",
    "actualization",
    "state_transitions",
    "navigation_rules",
]


def _load_json(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as f:
        data = json.load(f)
    if not isinstance(data, dict):
        raise SystemExit(f"顶层必须是 object: {path}")
    return data


def _validate(path: Path, strict: bool) -> list[str]:
    data = _load_json(path)
    errors: list[str] = []

    if data.get("schema_version") != "story2026/story-map/v3":
        errors.append("schema_version 必须为 story2026/story-map/v3")

    meta = data.get("meta")
    if not isinstance(meta, dict):
        errors.append("缺少 meta object")
    else:
        if meta.get("skill_id") != "story-plan":
            errors.append("meta.skill_id 必须为 story-plan")

    holomap = data.get("content", {}).get("holomap")
    if not isinstance(holomap, dict):
        errors.append("缺少 content.holomap object")
        return errors

    for key in REQUIRED_HOLOMAP_KEYS:
        if key not in holomap:
            errors.append(f"content.holomap 缺少 {key}")

    chapter_boards = holomap.get("chapter_boards", [])
    if not isinstance(chapter_boards, list) or not chapter_boards:
        errors.append("chapter_boards 必须为非空数组")
    elif strict:
        first = chapter_boards[0]
        if not isinstance(first, dict):
            errors.append("chapter_boards[] 必须是 object")
        else:
            bundled = first.get("bundled_elements", {})
            for key in ("events", "conflicts", "missions", "clues", "foreshadows"):
                if key not in bundled:
                    errors.append(f"chapter_boards[].bundled_elements 缺少 {key}")

    if strict and not holomap.get("cross_thread_indexes"):
        errors.append("strict 模式要求 cross_thread_indexes 非空")

    return errors


def main() -> None:
    parser = argparse.ArgumentParser(description="Validate Story2026 story_map output")
    parser.add_argument("path", help="Path to 2-Planning/全息地图.json")
    parser.add_argument("--strict", action="store_true", help="Require non-empty thread indexes")
    args = parser.parse_args()

    target_path = Path(args.path).resolve()
    errors = _validate(target_path, strict=args.strict)
    if errors:
        for err in errors:
            print(f"FAIL: {err}")
        raise SystemExit(1)

    print("PASS: story_map output structure is valid")


if __name__ == "__main__":
    main()
