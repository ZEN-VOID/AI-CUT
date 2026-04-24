#!/usr/bin/env python3
"""Extract the canonical AIGC global style prefix from `全局风格.md`."""

from __future__ import annotations

import argparse
import re
from pathlib import Path


GLOBAL_STYLE_RE = re.compile(r"^\s*[-*]\s*全局风格[:：]\s*(?P<value>.+?)\s*$", re.MULTILINE)
NONCANONICAL_GLOBAL_STYLE_RE = re.compile(
    r"^\s*全局风格[:：]\s*(?P<value>.+?)\s*$",
    re.MULTILINE,
)


def compact_inline(text: str, limit: int | None = None) -> str:
    clean = re.sub(r"\s+", " ", str(text or "")).strip()
    if limit and len(clean) > limit:
        return clean[: limit - 3].rstrip() + "..."
    return clean


def extract_global_style_prefix(text: str, *, limit: int | None = None) -> str:
    """Return only the canonical `- 全局风格：...` value from global style markdown."""
    matches = [match.group("value").strip() for match in GLOBAL_STYLE_RE.finditer(text or "")]
    if matches:
        return compact_inline(matches[-1], limit)
    return ""


def find_noncanonical_global_style_fields(text: str) -> list[str]:
    """Return noncanonical style-field values that look repairable."""
    return [match.group("value").strip() for match in NONCANONICAL_GLOBAL_STYLE_RE.finditer(text or "")]


def extract_global_style_prefix_from_path(path: Path | None, *, limit: int | None = None) -> str:
    if path is None or not path.exists():
        return ""
    return extract_global_style_prefix(path.read_text(encoding="utf-8"), limit=limit)


def main() -> int:
    parser = argparse.ArgumentParser(description="Extract canonical `- 全局风格：...` prefix.")
    parser.add_argument("path", help="全局风格.md path")
    parser.add_argument("--limit", type=int, default=None)
    args = parser.parse_args()
    path = Path(args.path)
    prefix = extract_global_style_prefix_from_path(path, limit=args.limit)
    if not prefix:
        text = path.read_text(encoding="utf-8") if path.exists() else ""
        noncanonical = find_noncanonical_global_style_fields(text)
        if noncanonical:
            parser.exit(
                1,
                "未找到 canonical `- 全局风格：` 字段；检测到非规范 `全局风格:` 裸行，"
                "请将其移动到 `## JSON 直接提取字段` 下并改为列表项 `- 全局风格：...`\n",
            )
        parser.exit(1, "未找到 `- 全局风格：` 字段\n")
    print(prefix)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
