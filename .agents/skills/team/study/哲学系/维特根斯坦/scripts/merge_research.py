#!/usr/bin/env python3
"""
合并 6 个调研文件，生成 Phase 1.5 调研摘要表格。

用法:
    python3 merge_research.py <skill目录路径>
"""

import re
import sys
from pathlib import Path

AGENTS = {
    "01-writings": "著作",
    "02-conversations": "对话",
    "03-expression-dna": "表达",
    "04-external-views": "他者",
    "05-decisions": "决策",
    "06-timeline": "时间线",
}


def count_sources(content: str) -> dict[str, int]:
    urls = re.findall(r"https?://[^\s\)]+", content)
    primary = len(
        re.findall(r"一手|primary|原文|原始|讲稿|手稿|书信|文本", content, re.IGNORECASE)
    )
    secondary = len(
        re.findall(r"二手|secondary|评论|研究|分析|百科|导论", content, re.IGNORECASE)
    )
    return {
        "unique_urls": len(set(urls)),
        "primary_markers": primary,
        "secondary_markers": secondary,
    }


def extract_key_findings(content: str, max_items: int = 3) -> list[str]:
    headings = re.findall(r"^##\s+(.+)$", content, re.MULTILINE)
    if headings:
        return headings[:max_items]
    lines = [line.strip() for line in content.splitlines() if line.strip() and not line.startswith("#")]
    return [line[:48] + "..." if len(line) > 48 else line for line in lines[:max_items]]


def find_contradictions(files: dict[str, str]) -> list[str]:
    contradictions: list[str] = []
    for name, content in files.items():
        matches = re.findall(r"(?:矛盾|张力|争议|分歧).{0,90}", content)
        for match in matches:
            contradictions.append(f"{AGENTS.get(name, name)}: {match[:70]}")
    return contradictions[:5]


def main() -> None:
    if len(sys.argv) < 2:
        print("用法: python3 merge_research.py <skill目录路径>")
        sys.exit(1)

    skill_dir = Path(sys.argv[1])
    research_dir = skill_dir / "references" / "research"
    if not research_dir.exists():
        print(f"❌ 目录不存在: {research_dir}")
        sys.exit(1)

    files: dict[str, str] = {}
    rows: list[str] = []
    missing: list[str] = []
    total_sources = 0
    total_primary = 0
    total_secondary = 0

    for key, label in AGENTS.items():
        path = research_dir / f"{key}.md"
        if not path.exists():
            missing.append(label)
            rows.append(f"│ {label:<12} │ {'❌ 缺失':<8} │ {'—':<24} │")
            continue

        content = path.read_text(encoding="utf-8")
        files[key] = content
        stats = count_sources(content)
        findings = extract_key_findings(content)

        total_sources += stats["unique_urls"]
        total_primary += stats["primary_markers"]
        total_secondary += stats["secondary_markers"]

        findings_str = ", ".join(findings) if findings else "—"
        if len(findings_str) > 40:
            findings_str = findings_str[:37] + "..."
        rows.append(f"│ {label:<12} │ {stats['unique_urls']:<8} │ {findings_str:<24} │")

    contradictions = find_contradictions(files)
    primary_ratio = (
        f"{total_primary}/{total_primary + total_secondary}"
        if (total_primary + total_secondary) > 0
        else "未标记"
    )

    print("┌──────────────┬──────────┬──────────────────────────┐")
    print("│ Agent        │ 来源数量  │ 关键发现                  │")
    print("├──────────────┼──────────┼──────────────────────────┤")
    for row in rows:
        print(row)
    print("├──────────────┼──────────┼──────────────────────────┤")
    print(f"│ 总来源数      │ {total_sources:<8} │ 一手占比: {primary_ratio:<15} │")
    if contradictions:
        print(f"│ 矛盾点        │ {len(contradictions)}处      │ {contradictions[0][:24]:<24} │")
    else:
        print(f"│ 矛盾点        │ 0处      │ {'—':<24} │")
    if missing:
        print(f"│ 信息不足维度   │ {len(missing)}个      │ {', '.join(missing):<24} │")
    else:
        print(f"│ 信息不足维度   │ 无       │ {'—':<24} │")
    print("└──────────────┴──────────┴──────────────────────────┘")

    if total_sources < 10:
        print("\n⚠️ 总来源数 <10，建议补充调研或在诚实边界中标注不足。")
    if missing:
        print(f"\n⚠️ 缺失维度: {', '.join(missing)}")


if __name__ == "__main__":
    main()
