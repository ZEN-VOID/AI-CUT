#!/usr/bin/env python3
"""Validate the markdown output contract for 3-Detail/2-镜花."""

from __future__ import annotations

import argparse
import re
from pathlib import Path


GROUP_HEADER_RE = re.compile(r"^##\s+(.+)$", re.MULTILINE)
SHOT_MARKER_RE = re.compile(r"\[分镜\d+[^\]]*\]")


def visible_char_count(text: str) -> int:
    text = re.sub(r"^#+.*$", "", text, flags=re.MULTILINE)
    text = re.sub(r"\s+", "", text)
    return len(text)


def split_groups(text: str) -> list[tuple[str, str]]:
    matches = list(GROUP_HEADER_RE.finditer(text))
    groups: list[tuple[str, str]] = []
    for index, match in enumerate(matches):
        start = match.end()
        end = matches[index + 1].start() if index + 1 < len(matches) else len(text)
        groups.append((match.group(1).strip(), text[start:end]))
    return groups


def extract_section(body: str, section_name: str) -> str | None:
    pattern = re.compile(
        rf"^###\s+{re.escape(section_name)}\s*$\n(.*?)(?=^###\s+|\Z)",
        re.MULTILINE | re.DOTALL,
    )
    match = pattern.search(body)
    return match.group(1).strip() if match else None


def validate_file(path: Path, max_chars: int) -> list[str]:
    text = path.read_text(encoding="utf-8")
    errors: list[str] = []
    groups = split_groups(text)

    if not groups:
        return ["未找到任何 `## 分镜组标题` 组块。"]

    for header, body in groups:
        if "### 锚点" in body or "### 镜花" in body or "水月承接：" in body:
            errors.append(f"{header}: 不应外露 `锚点/镜花/水月承接` 区块。")
        if "### " not in body:
            errors.append(f"{header}: 缺少场景级标题字段。")
        if not SHOT_MARKER_RE.search(body):
            errors.append(f"{header}: 缺少 `[分镜N ...]` 标记。")

        count = visible_char_count(body)
        if count > max_chars:
            errors.append(f"{header}: visible chars = {count}，超过上限 {max_chars}。")

    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate 2-镜花 markdown output.")
    parser.add_argument("path", type=Path, help="Path to `projects/aigc/<项目名>/3-Detail/2-镜花/第N集.md`")
    parser.add_argument("--max-chars", type=int, default=1800, help="Per-group visible char limit.")
    args = parser.parse_args()

    if not args.path.exists():
        print(f"文件不存在: {args.path}")
        return 1

    errors = validate_file(args.path, args.max_chars)
    if errors:
        print("校验失败:")
        for error in errors:
            print(f"- {error}")
        return 1

    print("校验通过。")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
