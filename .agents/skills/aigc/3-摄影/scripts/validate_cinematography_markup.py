#!/usr/bin/env python3
"""Mechanical checks for 3-摄影 cinematography markup.

This script validates coverage and numbering only. It does not generate
cinematography language or decide creative beats.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path


VISUAL_LABEL_RE = re.compile(r"^(?!镜头语言)([^：\n]*(画面|动作|表演|描写|特写|显影)[^：\n]*)：")
SHOT_RE = re.compile(r"^分镜(\d+):")


def validate(path: Path) -> tuple[bool, list[str]]:
    lines = path.read_text(encoding="utf-8").splitlines()
    findings: list[str] = []
    ok = True
    visual_count = 0
    language_count = 0

    index = 0
    while index < len(lines):
        line = lines[index]
        if not VISUAL_LABEL_RE.match(line):
            index += 1
            continue

        visual_count += 1
        next_index = index + 1
        while next_index < len(lines) and lines[next_index] == "":
            next_index += 1

        if next_index >= len(lines) or lines[next_index].strip() != "镜头语言：":
            findings.append(f"[ERROR] Missing 镜头语言 after line {index + 1}: {line[:80]}")
            ok = False
            index += 1
            continue

        language_count += 1
        shot_numbers: list[int] = []
        cursor = next_index + 1
        while cursor < len(lines):
            current = lines[cursor]
            if current == "":
                cursor += 1
                continue
            if current.startswith("分镜"):
                match = SHOT_RE.match(current)
                if not match:
                    findings.append(f"[ERROR] Invalid shot marker at line {cursor + 1}: {current[:80]}")
                    ok = False
                    break
                shot_numbers.append(int(match.group(1)))
                cursor += 1
                continue
            break

        expected = list(range(1, len(shot_numbers) + 1))
        if not shot_numbers:
            findings.append(f"[ERROR] No 分镜N entries after line {next_index + 1}")
            ok = False
        elif shot_numbers != expected:
            findings.append(
                f"[ERROR] Non-continuous shot numbers after line {next_index + 1}: {shot_numbers}"
            )
            ok = False
        index = max(cursor, index + 1)

    findings.append(f"[INFO] visual_units={visual_count} lens_language_blocks={language_count}")
    if ok:
        findings.append("[OK] Cinematography markup is mechanically valid.")
    return ok, findings


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate 3-摄影 markup.")
    parser.add_argument("episode_file", help="Path to projects/aigc/<项目名>/3-摄影/第N集.md")
    args = parser.parse_args()
    path = Path(args.episode_file)
    if not path.is_file():
        print(f"[ERROR] Not a file: {path}")
        return 1
    ok, findings = validate(path)
    for finding in findings:
        print(finding)
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
