#!/usr/bin/env python3
"""Validate `1-水月` markdown landing structure and per-group character budget."""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

GROUP_HEADING_RE = re.compile(r"^##\s*【[^】]+】", re.MULTILINE)


def split_group_sections(text: str) -> list[tuple[str, str]]:
    """Return `(heading, body)` tuples for each group section."""
    matches = list(GROUP_HEADING_RE.finditer(text))
    sections: list[tuple[str, str]] = []
    for index, match in enumerate(matches):
        start = match.start()
        end = matches[index + 1].start() if index + 1 < len(matches) else len(text)
        block = text[start:end].strip()
        lines = block.splitlines()
        heading = lines[0].strip() if lines else ""
        body = "\n".join(lines[1:]).strip()
        sections.append((heading, body))
    return sections


def visible_chars(text: str) -> int:
    """Count visible characters by removing all whitespace."""
    return len(re.sub(r"\s+", "", text))


def validate(text: str, max_chars: int) -> list[str]:
    errors: list[str] = []
    sections = split_group_sections(text)
    if not sections:
        return ["未找到 `## 【分镜组ID】 组标题` 段落。"]

    for heading, body in sections:
        if "锚点：" in body or "扩写：" in body:
            errors.append(f"{heading} 不应外露 `锚点：/扩写：` 字段。")
        if "### " not in body:
            errors.append(f"{heading} 缺少场景级标题字段。")
        count = visible_chars(body)
        if count > max_chars:
            errors.append(f"{heading} 可见字符数 {count} 超过上限 {max_chars}。")
    return errors


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Validate `3-Detail/1-水月/第N集.md` structure and per-group character budget."
    )
    parser.add_argument("path", type=Path, help="Target markdown file path.")
    parser.add_argument(
        "--max-chars",
        type=int,
        default=1000,
        help="Maximum visible characters allowed per group block. Default: 1000.",
    )
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    text = args.path.read_text(encoding="utf-8")
    errors = validate(text, args.max_chars)
    if errors:
        for error in errors:
            print(f"FAIL: {error}")
        return 1
    print("PASS: 水月输出结构与字数预算通过。")
    return 0


if __name__ == "__main__":
    sys.exit(main())
