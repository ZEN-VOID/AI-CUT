#!/usr/bin/env python3
"""Validate mechanical structure of a 4-表演 episode script.

This script is intentionally narrow. It checks common mechanical risks only;
it does not prove performance craft quality or replace LLM/human review.
"""

from __future__ import annotations

import argparse
import re
from pathlib import Path


SUBJECTIVE_ACTION_WORDS = ("试图", "想要", "打算", "意图", "为了掩饰", "准备借此")
CAMERA_OVERREACH_WORDS = ("机位", "景别", "镜头运动", "推镜", "摇镜", "分镜编号", "分镜明细预设")
PLACEHOLDER_PATTERNS = (
    "本场按上游",
    "说话者的视线",
    "不新增事件结果",
    "引号内不加入动作",
    "<项目名>",
)
DIALOGUE_HEADING_RE = re.compile(r"^对白（([^）]+)）[:：]", re.MULTILINE)
VAGUE_DIALOGUE_STATES = ("平静", "紧张", "生气", "愤怒", "难过", "开心", "害怕", "复杂")


def collect_findings(text: str) -> list[str]:
    findings: list[str] = []

    if "【剧本正文】" not in text:
        findings.append("missing required section: 【剧本正文】")

    for word in SUBJECTIVE_ACTION_WORDS:
        if word in text:
            findings.append(f"subjective action wording found: {word}")

    for word in CAMERA_OVERREACH_WORDS:
        if word in text:
            findings.append(f"cinematography overreach wording found: {word}")

    for pattern in PLACEHOLDER_PATTERNS:
        if pattern in text:
            findings.append(f"placeholder or rule leak found: {pattern}")

    if re.search(r"^###\s*场景.+\n(?:.|\n){0,500}(?:表演提示|场面调度)[:：]", text, re.MULTILINE):
        findings.append("possible scene-end performance/blocking summary block found")

    for match in DIALOGUE_HEADING_RE.finditer(text):
        heading = match.group(1).strip()
        if "，" not in heading and "," not in heading:
            findings.append(f"dialogue heading missing tone/state segment: 对白（{heading}）")
            continue

        state = re.split(r"[，,]", heading, maxsplit=1)[1].strip()
        if not state:
            findings.append(f"dialogue heading has empty tone/state segment: 对白（{heading}）")
        elif state in VAGUE_DIALOGUE_STATES:
            findings.append(f"dialogue heading has vague tone/state segment: 对白（{heading}）")

    return findings


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("episode_script", help="Path to projects/aigc/<项目名>/4-表演/第N集.md")
    args = parser.parse_args()

    path = Path(args.episode_script)
    text = path.read_text(encoding="utf-8")
    findings = collect_findings(text)

    if findings:
        print("FAIL")
        for item in findings:
            print(f"- {item}")
        return 1

    print("OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
