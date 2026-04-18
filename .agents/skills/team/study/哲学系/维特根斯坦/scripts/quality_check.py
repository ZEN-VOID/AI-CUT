#!/usr/bin/env python3
"""
检查生成的 SKILL.md 是否满足最小结构质量门槛。

用法:
    python3 quality_check.py <SKILL.md路径>
"""

import re
import sys
from pathlib import Path


def check_mental_models(content: str) -> tuple[bool, str]:
    models = re.findall(r"^###\s+(?:模型|Model|心智模型)\s*\d", content, re.MULTILINE)
    count = len(models)
    if count == 0:
        return False, "未检测到心智模型 section"
    passed = 3 <= count <= 7
    return passed, f"{count} 个心智模型 {'✅' if passed else '❌ (应为 3-7 个)'}"


def check_limitations(content: str) -> tuple[bool, str]:
    passed = bool(re.search(r"局限|失效|不适用|盲区|limitation", content, re.IGNORECASE))
    return passed, "有局限性标注 ✅" if passed else "❌ 未找到局限性描述"


def check_expression_dna(content: str) -> tuple[bool, str]:
    if not re.search(r"表达 DNA|Expression DNA|表达风格", content, re.IGNORECASE):
        return False, "❌ 未找到表达 DNA section"
    markers = len(re.findall(r"句式|词汇|语气|幽默|节奏|输出要求", content))
    passed = markers >= 3
    return passed, f"表达 DNA 特征: {markers} 项 {'✅' if passed else '❌ (应≥3项)'}"


def check_honest_boundary(content: str) -> tuple[bool, str]:
    match = re.search(r"(?:##\s+.*诚实边界)(.*?)(?=\n##\s|\Z)", content, re.DOTALL)
    if not match:
        return False, "❌ 未找到诚实边界 section"
    count = len(re.findall(r"^[-*]\s+", match.group(1), re.MULTILINE))
    passed = count >= 3
    return passed, f"诚实边界: {count} 条 {'✅' if passed else '❌ (应≥3条)'}"


def check_tensions(content: str) -> tuple[bool, str]:
    passed = len(re.findall(r"张力|矛盾|一方面.*另一方面|既.*又", content, re.IGNORECASE)) >= 2
    return passed, "内在张力 ✅" if passed else "❌ 内在张力不足"


def check_primary_sources(content: str) -> tuple[bool, str]:
    match = re.search(r"(?:##\s+.*调研来源)(.*?)(?=\n##\s|\Z)", content, re.DOTALL)
    if not match:
        return True, "未找到调研来源 section（跳过）"
    section = match.group(1)
    primary = len(re.findall(r"一手|原文|原始|讲稿|手稿|文本", section, re.IGNORECASE))
    secondary = len(re.findall(r"二手|评论|研究|百科|导论", section, re.IGNORECASE))
    total = primary + secondary
    if total == 0:
        return True, "未标记来源类型（跳过）"
    ratio = primary / total
    passed = ratio > 0.5
    return passed, f"一手来源占比: {primary}/{total} ({ratio:.0%}) {'✅' if passed else '❌ (应>50%)'}"


def main() -> None:
    if len(sys.argv) < 2:
        print("用法: python3 quality_check.py <SKILL.md路径>")
        sys.exit(1)

    path = Path(sys.argv[1])
    if not path.exists():
        print(f"❌ 文件不存在: {path}")
        sys.exit(1)

    content = path.read_text(encoding="utf-8")
    checks = [
        ("心智模型数量", check_mental_models),
        ("模型局限性", check_limitations),
        ("表达 DNA", check_expression_dna),
        ("诚实边界", check_honest_boundary),
        ("内在张力", check_tensions),
        ("一手来源占比", check_primary_sources),
    ]

    print(f"质量检查: {path.name}")
    print("=" * 50)

    passed_count = 0
    for name, fn in checks:
        passed, detail = fn(content)
        print(f"{name:<12} {'✅ PASS' if passed else '❌ FAIL'}  {detail}")
        if passed:
            passed_count += 1

    print("=" * 50)
    print(f"结果: {passed_count}/{len(checks)} 通过")
    sys.exit(0 if passed_count == len(checks) else 1)


if __name__ == "__main__":
    main()
