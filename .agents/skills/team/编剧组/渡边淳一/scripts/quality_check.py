#!/usr/bin/env python3
"""Run a lightweight quality check for a generated perspective SKILL.md."""

from __future__ import annotations

import re
import sys
from pathlib import Path


def section(text: str, title_fragment: str) -> str:
    """Return markdown section content by title fragment."""
    pattern = rf"^##\s+[^\n]*{re.escape(title_fragment)}[^\n]*$(.*?)(?=^##\s+|\Z)"
    match = re.search(pattern, text, flags=re.MULTILINE | re.DOTALL)
    return match.group(1) if match else ""


def count_model_heads(text: str) -> int:
    """Count model headings under the mental model section."""
    model_section = section(text, "核心心智模型")
    return len(re.findall(r"^###\s+模型\d+", model_section, flags=re.MULTILINE))


def check(name: str, passed: bool, detail: str) -> bool:
    """Print one check row and return pass state."""
    status = "PASS" if passed else "FAIL"
    print(f"{status}: {name} - {detail}")
    return passed


def main() -> int:
    if len(sys.argv) != 2:
        print("Usage: python3 quality_check.py <SKILL.md>")
        return 2

    path = Path(sys.argv[1])
    if not path.exists():
        print(f"Missing file: {path}")
        return 1

    text = path.read_text(encoding="utf-8")
    model_count = count_model_heads(text)
    boundary = section(text, "诚实边界")
    boundary_items = len(re.findall(r"^-\s+", boundary, flags=re.MULTILINE))
    source = section(text, "调研来源")
    checks = [
        check("frontmatter governance tier", "governance_tier: lite" in text, "requires lite tier"),
        check("context loading contract", "Context Loading Contract" in text, "must preload CONTEXT.md"),
        check("mental models", 3 <= model_count <= 7, f"{model_count} models"),
        check("model limitations", text.count("**局限**") >= model_count, "each model should expose limits"),
        check("expression DNA", "## 表达 DNA" in text, "requires voice rules"),
        check("honest boundary", boundary_items >= 3, f"{boundary_items} bullet items"),
        check("root cause contract", "Root-Cause 执行合同" in text, "requires failure trace"),
        check("field mapping", "字段中心映射（Tier-Lite）" in text, "requires tier-lite table"),
        check("source links", source.count("https://") >= 5, "requires research sources"),
    ]
    passed = sum(1 for item in checks if item)
    print(f"Result: {passed}/{len(checks)} passed")
    return 0 if all(checks) else 1


if __name__ == "__main__":
    raise SystemExit(main())
