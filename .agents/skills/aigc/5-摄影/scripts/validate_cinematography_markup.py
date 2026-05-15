#!/usr/bin/env python3
"""Mechanical checks for 3-摄影 cinematography markup.

This script validates coverage, explicit duration markers, numbering,
coarse shot-count distribution signals, frontmatter presence, short-drama
AIGC duration range hints, abstract term detection, and empty block detection. It does not
generate shot details or decide creative beats.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path


VISUAL_LABEL_RE = re.compile(r"^(?!分镜明细)([^：\n]*(画面|动作|表演|描写|特写|显影)[^：\n]*)：")
SHOT_RE = re.compile(r"^分镜(\d+)（约((?:0\.5)|(?:[1-9]\d?(?:\.\d+)?))秒）[:：]")
TWO_SHOT_WARNING_THRESHOLD = 0.8
MIN_BLOCKS_FOR_DISTRIBUTION_WARNING = 10

FRONTMATTER_REQUIRED_FIELDS = [
    "stage: 3-摄影",
    "source_directing_path:",
    "output_path:",
    "duration_policy:",
]

ABSTRACT_TERMS_RE = re.compile(
    r"(?:象征|隐喻|寓意|暗示了|表现了|体现了|导演意图|世界观|命运|心理状态|孤独感|压迫感)"
)


def validate_frontmatter(lines: list[str]) -> list[str]:
    """Check that required frontmatter fields are present."""
    findings: list[str] = []
    if not lines or lines[0].strip() != "---":
        findings.append("[ERROR] Missing frontmatter opening '---'.")
        return findings

    # Find closing ---
    close_index = -1
    for i in range(1, len(lines)):
        if lines[i].strip() == "---":
            close_index = i
            break

    if close_index == -1:
        findings.append("[ERROR] Frontmatter not closed with '---'.")
        return findings

    frontmatter_text = "\n".join(lines[1:close_index])
    for field in FRONTMATTER_REQUIRED_FIELDS:
        if field not in frontmatter_text:
            findings.append(f"[ERROR] Frontmatter missing required field: {field}")

    return findings


def validate(
    path: Path, *, strict_shot_distribution: bool = False
) -> tuple[bool, list[str]]:
    lines = path.read_text(encoding="utf-8").splitlines()
    findings: list[str] = []
    ok = True
    visual_count = 0
    detail_count = 0
    shot_count_distribution: dict[int, int] = {}

    # --- Frontmatter check ---
    fm_findings = validate_frontmatter(lines)
    if fm_findings:
        for f in fm_findings:
            findings.append(f)
            if "[ERROR]" in f:
                ok = False

    # --- Line-by-line scan ---
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

        if next_index >= len(lines) or lines[next_index].strip() != "分镜明细：":
            findings.append(f"[ERROR] Missing 分镜明细 after line {index + 1}: {line[:80]}")
            ok = False
            index += 1
            continue

        detail_count += 1
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
                    findings.append(
                        f"[ERROR] Invalid shot marker at line {cursor + 1}; "
                        f"expected 分镜N（约X秒）: {current[:80]}"
                    )
                    ok = False
                    break
                shot_numbers.append(int(match.group(1)))

                # --- Duration range check ---
                seconds = float(match.group(2))
                if seconds < 1.0:
                    findings.append(
                        f"[WARN] Duration {seconds}s at line {cursor + 1}; "
                        f"verify this is a deliberate flash-cut or instant reaction."
                    )
                elif seconds > 5.0:
                    findings.append(
                        f"[WARN] Duration {seconds}s at line {cursor + 1}; "
                        f"verify this is a strong exception with dialogue, long blocking, or a major cognitive peak."
                    )
                elif seconds > 3.0:
                    findings.append(
                        f"[WARN] Duration {seconds}s at line {cursor + 1}; "
                        f"verify short-drama AIGC necessity (dialogue/readability/performance/blocking/peak evidence)."
                    )

                # --- Abstract term check ---
                shot_content = current
                if ABSTRACT_TERMS_RE.search(shot_content):
                    term_match = ABSTRACT_TERMS_RE.search(shot_content)
                    if term_match:
                        findings.append(
                            f"[WARN] Abstract term \"{term_match.group()}\" at line {cursor + 1} "
                            f"in 分镜明细 block; verify translated to visible camera/visual language."
                        )

                cursor += 1
                continue
            break

        # --- Empty block check ---
        if not shot_numbers and detail_count > 0:
            findings.append(
                f"[ERROR] Empty 分镜明细 block at line {next_index + 1} (no 分镜N entries)."
            )
            ok = False

        expected = list(range(1, len(shot_numbers) + 1))
        if shot_numbers and shot_numbers != expected:
            findings.append(
                f"[ERROR] Non-continuous shot numbers after line {next_index + 1}: {shot_numbers}"
            )
            ok = False
        elif shot_numbers:
            shot_count_distribution[len(shot_numbers)] = (
                shot_count_distribution.get(len(shot_numbers), 0) + 1
            )
        index = max(cursor, index + 1)

    findings.append(f"[INFO] visual_units={visual_count} shot_detail_blocks={detail_count}")
    if shot_count_distribution:
        distribution_text = ", ".join(
            f"{shot_count}:{count}" for shot_count, count in sorted(shot_count_distribution.items())
        )
        findings.append(f"[INFO] shot_count_distribution={distribution_text}")

        two_shot_blocks = shot_count_distribution.get(2, 0)
        total_blocks = sum(shot_count_distribution.values())
        two_shot_ratio = two_shot_blocks / total_blocks if total_blocks else 0
        if (
            total_blocks >= MIN_BLOCKS_FOR_DISTRIBUTION_WARNING
            and two_shot_ratio >= TWO_SHOT_WARNING_THRESHOLD
        ):
            message = (
                "[WARN] Two-shot blocks are highly concentrated "
                f"({two_shot_blocks}/{total_blocks}, {two_shot_ratio:.1%}). "
                "Review beat_map/rhythm_profile/shot_count_decision; 分镜2 must not be a template default."
            )
            findings.append(message)
            if strict_shot_distribution:
                ok = False
    if ok:
        findings.append("[OK] Cinematography markup is mechanically valid.")
    return ok, findings


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate 3-摄影 markup.")
    parser.add_argument("episode_file", help="Path to projects/aigc/<项目名>/3-摄影/第N集.md")
    parser.add_argument(
        "--strict-shot-distribution",
        action="store_true",
        help="Treat highly concentrated 2-shot distribution as an error instead of a warning.",
    )
    args = parser.parse_args()
    path = Path(args.episode_file)
    if not path.is_file():
        print(f"[ERROR] Not a file: {path}")
        return 1
    ok, findings = validate(path, strict_shot_distribution=args.strict_shot_distribution)
    for finding in findings:
        print(finding)
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
