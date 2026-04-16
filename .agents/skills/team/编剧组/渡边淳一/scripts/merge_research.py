#!/usr/bin/env python3
"""Generate a compact Phase 1.5 research review table for a Nuwa skill."""

from __future__ import annotations

import re
import sys
from pathlib import Path


RESEARCH_FILES = [
    ("01-writings.md", "著作"),
    ("02-conversations.md", "对话"),
    ("03-expression-dna.md", "表达"),
    ("04-external-views.md", "他者"),
    ("05-decisions.md", "决策"),
    ("06-timeline.md", "时间线"),
]


def count_unique_urls(text: str) -> int:
    """Return unique URL count in a markdown file."""
    urls = re.findall(r"https?://[^\s)]+", text)
    return len(set(urls))


def extract_findings(text: str, limit: int = 2) -> str:
    """Extract short finding labels from headings."""
    headings = [
        h.strip()
        for h in re.findall(r"^##\s+(.+)$", text, flags=re.MULTILINE)
        if "Sources" not in h
    ]
    if not headings:
        bold = re.findall(r"\*\*(.+?)\*\*", text)
        headings = [b.strip() for b in bold]
    summary = "、".join(headings[:limit]) if headings else "-"
    return summary[:36] + ("..." if len(summary) > 36 else "")


def main() -> int:
    if len(sys.argv) != 2:
        print("Usage: python3 merge_research.py <skill_dir>")
        return 2

    skill_dir = Path(sys.argv[1])
    research_dir = skill_dir / "references" / "research"
    if not research_dir.is_dir():
        print(f"Missing research dir: {research_dir}")
        return 1

    print("| Agent | 来源数量 | 关键发现 |")
    print("|---|---:|---|")
    missing: list[str] = []
    total_sources = 0

    for filename, label in RESEARCH_FILES:
        path = research_dir / filename
        if not path.exists():
            missing.append(label)
            print(f"| {label} | 0 | MISSING |")
            continue
        text = path.read_text(encoding="utf-8")
        source_count = count_unique_urls(text)
        total_sources += source_count
        print(f"| {label} | {source_count} | {extract_findings(text)} |")

    print(f"| 总计 | {total_sources} | 缺失维度：{', '.join(missing) if missing else '无'} |")
    return 1 if missing else 0


if __name__ == "__main__":
    raise SystemExit(main())
