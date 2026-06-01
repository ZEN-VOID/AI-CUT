#!/usr/bin/env python3
"""Mechanical checks for 3-motion enrichment outputs."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path


FORBIDDEN_TERMS = ("分镜N", "机位", "景别", "运镜", "图像 prompt", "视频请求")


def validate(path: Path) -> tuple[bool, list[str]]:
    findings: list[str] = []
    text = path.read_text(encoding="utf-8")

    if "stage: 3-运动" not in text and "# 3-运动" not in text:
        findings.append("[ERROR] missing stage marker `3-运动`")
    if "运动强化：" not in text:
        findings.append("[ERROR] missing `运动强化：` entries")
    if "motion_state_ledger" not in text and "Motion State Ledger" not in text and "运动状态" not in text:
        findings.append("[WARN] missing visible motion_state_ledger evidence")
    if "group_reference_profile" not in text and "Group Reference Profile" not in text and "组级参照" not in text:
        findings.append("[WARN] missing visible group_reference_profile evidence")

    for term in FORBIDDEN_TERMS:
        if term in text:
            findings.append(f"[WARN] possible downstream overreach term: {term}")

    return not any(item.startswith("[ERROR]") for item in findings), findings


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate 3-运动 enrichment markup.")
    parser.add_argument("episode_file", help="Path to a 3-运动 Markdown output")
    args = parser.parse_args()

    path = Path(args.episode_file)
    if not path.is_file():
        print(f"[ERROR] file not found: {path}")
        return 2

    ok, findings = validate(path)
    for item in findings or ["[OK] mechanical checks passed"]:
        print(item)
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
