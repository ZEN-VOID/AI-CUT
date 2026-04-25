#!/usr/bin/env python3
"""Validate group-level director intent density for AIGC 2-Global outputs."""

from __future__ import annotations

import argparse
import json
from difflib import SequenceMatcher
from pathlib import Path
from typing import Any


REQUIRED_MARKERS = ("观看策略", "执行抓手", "禁用")
MIN_CHARS = 36
MAX_SIMILARITY_TO_SCRIPT = 0.62


def normalize_text(value: Any) -> str:
    return " ".join(str(value or "").split())


def iter_groups(data: dict[str, Any]) -> list[dict[str, Any]]:
    groups = data.get("groups")
    if isinstance(groups, list):
        return [group for group in groups if isinstance(group, dict)]
    final_output = data.get("final_output")
    if isinstance(final_output, list):
        return [group for group in final_output if isinstance(group, dict)]
    return []


def group_id(group: dict[str, Any], index: int) -> str:
    return normalize_text(group.get("分镜组ID") or group.get("group_id") or f"group[{index}]")


def global_block(group: dict[str, Any]) -> dict[str, Any]:
    block = group.get("global")
    if isinstance(block, dict):
        return block
    group_design = group.get("组间设计")
    if isinstance(group_design, dict):
        return group_design
    return {}


def validate_group(group: dict[str, Any], index: int) -> list[str]:
    block = global_block(group)
    intent = normalize_text(block.get("导演意图"))
    script = normalize_text(block.get("剧本正文"))
    gid = group_id(group, index)
    errors: list[str] = []

    if not intent:
        return [f"{gid}: missing global.导演意图"]
    if len(intent) < MIN_CHARS:
        errors.append(f"{gid}: 导演意图 too short ({len(intent)} chars)")

    missing = [marker for marker in REQUIRED_MARKERS if marker not in intent]
    if missing:
        errors.append(f"{gid}: 导演意图 missing markers: {', '.join(missing)}")

    if script:
        compact_intent = intent.replace(" ", "")
        compact_script = script.replace(" ", "")
        if compact_intent and compact_intent in compact_script:
            errors.append(f"{gid}: 导演意图 appears copied from 剧本正文")
        similarity = SequenceMatcher(None, intent[:180], script[:360]).ratio()
        if similarity >= MAX_SIMILARITY_TO_SCRIPT:
            errors.append(f"{gid}: 导演意图 too similar to 剧本正文 ({similarity:.2f})")

    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("json_path", type=Path)
    args = parser.parse_args()

    data = json.loads(args.json_path.read_text(encoding="utf-8"))
    groups = iter_groups(data)
    if not groups:
        print(f"FAIL {args.json_path}: no groups found")
        return 1

    errors: list[str] = []
    for index, group in enumerate(groups, start=1):
        errors.extend(validate_group(group, index))

    if errors:
        print(f"FAIL {args.json_path}")
        for error in errors:
            print(f"- {error}")
        return 1

    print(f"PASS {args.json_path}: {len(groups)} director intents validated")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
