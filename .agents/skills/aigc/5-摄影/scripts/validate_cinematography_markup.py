#!/usr/bin/env python3
"""Mechanical checks for 5-摄影 cinematography markup.

This script validates coverage, explicit duration markers, numbering,
coarse shot-count distribution signals, source-text preservation,
frontmatter presence, short-drama AIGC duration range hints, abstract term
detection, and empty block detection. It does not generate shot details or
decide creative beats.
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
    "stage: 5-摄影",
    "source_performance_path:",
    "output_path:",
    "duration_policy:",
]

ABSTRACT_TERMS_RE = re.compile(
    r"(?:象征|隐喻|寓意|暗示了|表现了|体现了|导演意图|世界观|命运|心理状态|孤独感|压迫感)"
)

BODY_MARKER = "【剧本正文】"


def parse_frontmatter(lines: list[str]) -> tuple[dict[str, str], list[str]]:
    """Extract simple key-value frontmatter fields."""
    findings: list[str] = []
    data: dict[str, str] = {}
    if not lines or lines[0].strip() != "---":
        findings.append("[ERROR] Missing frontmatter opening '---'.")
        return data, findings

    close_index = -1
    for i in range(1, len(lines)):
        if lines[i].strip() == "---":
            close_index = i
            break

    if close_index == -1:
        findings.append("[ERROR] Frontmatter not closed with '---'.")
        return data, findings

    for raw_line in lines[1:close_index]:
        if ":" not in raw_line:
            continue
        key, value = raw_line.split(":", 1)
        data[key.strip()] = value.strip().strip("\"'")
    return data, findings


def validate_frontmatter(lines: list[str]) -> list[str]:
    """Check that required frontmatter fields are present."""
    findings: list[str] = []
    frontmatter, fm_findings = parse_frontmatter(lines)
    findings.extend(fm_findings)
    if fm_findings:
        return findings

    close_index = next(i for i in range(1, len(lines)) if lines[i].strip() == "---")
    frontmatter_text = "\n".join(lines[1:close_index])
    for field in FRONTMATTER_REQUIRED_FIELDS:
        if field.endswith(":"):
            field_name = field.rstrip(":")
            if field_name in frontmatter:
                continue
        elif field in frontmatter_text:
            continue
        else:
            findings.append(f"[ERROR] Frontmatter missing required field: {field}")

    return findings


def body_lines(lines: list[str]) -> list[str]:
    """Return lines after the canonical screenplay body marker."""
    try:
        body_start = lines.index(BODY_MARKER)
    except ValueError:
        return []
    return lines[body_start:]


def normalized_source_lines(lines: list[str]) -> list[str]:
    """Normalize source body lines for preservation comparison."""
    return [line.rstrip() for line in body_lines(lines) if line.strip()]


def normalized_output_source_lines(lines: list[str]) -> list[str]:
    """Remove injected 分镜明细 blocks and normalize remaining source body lines."""
    result: list[str] = []
    body = body_lines(lines)
    index = 0
    while index < len(body):
        line = body[index]
        if line.strip() == "分镜明细：":
            index += 1
            while index < len(body):
                candidate = body[index]
                if not candidate.strip() or candidate.startswith("分镜"):
                    index += 1
                    continue
                break
            continue
        if line.strip():
            result.append(line.rstrip())
        index += 1
    return result


def validate_source_preservation(
    output_lines: list[str], source_path: Path
) -> tuple[bool, list[str]]:
    """Ensure output preserves the source performance body after removing injections."""
    findings: list[str] = []
    if not source_path.is_file():
        return False, [f"[ERROR] Source performance file not found: {source_path}"]

    source_lines = source_path.read_text(encoding="utf-8").splitlines()
    source_body = normalized_source_lines(source_lines)
    output_body = normalized_output_source_lines(output_lines)

    if source_body == output_body:
        return True, ["[OK] Source body preservation check passed."]

    first_diff = 0
    max_common = min(len(source_body), len(output_body))
    while first_diff < max_common and source_body[first_diff] == output_body[first_diff]:
        first_diff += 1

    findings.append(
        "[ERROR] Source body preservation check failed after removing 分镜明细 blocks."
    )
    findings.append(
        f"[INFO] source_body_lines={len(source_body)} output_body_lines={len(output_body)}"
    )
    if first_diff < len(source_body):
        findings.append(
            f"[INFO] first_source_mismatch_line={first_diff + 1}: "
            f"{source_body[first_diff][:100]}"
        )
    if first_diff < len(output_body):
        findings.append(
            f"[INFO] first_output_mismatch_line={first_diff + 1}: "
            f"{output_body[first_diff][:100]}"
        )
    return False, findings


def validate(
    path: Path,
    *,
    strict_shot_distribution: bool = False,
    source_performance_path: Path | None = None,
    skip_source_preservation: bool = False,
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

    # --- Source preservation check ---
    if not skip_source_preservation:
        frontmatter, _ = parse_frontmatter(lines)
        resolved_source = source_performance_path
        if resolved_source is None and frontmatter.get("source_performance_path"):
            resolved_source = Path(frontmatter["source_performance_path"])
        if resolved_source is not None:
            if not resolved_source.is_absolute():
                resolved_source = Path.cwd() / resolved_source
            source_ok, source_findings = validate_source_preservation(lines, resolved_source)
            findings.extend(source_findings)
            if not source_ok:
                ok = False
        else:
            findings.append(
                "[WARN] Source preservation check skipped; no source_performance_path found."
            )

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
    parser = argparse.ArgumentParser(description="Validate 5-摄影 markup.")
    parser.add_argument("episode_file", help="Path to projects/aigc/<项目名>/5-摄影/第N集.md")
    parser.add_argument(
        "--strict-shot-distribution",
        action="store_true",
        help="Treat highly concentrated 2-shot distribution as an error instead of a warning.",
    )
    parser.add_argument(
        "--source-performance-path",
        help="Override source performance file path for source body preservation check.",
    )
    parser.add_argument(
        "--skip-source-preservation",
        action="store_true",
        help="Skip source body preservation check.",
    )
    args = parser.parse_args()
    path = Path(args.episode_file)
    if not path.is_file():
        print(f"[ERROR] Not a file: {path}")
        return 1
    source_path = Path(args.source_performance_path) if args.source_performance_path else None
    ok, findings = validate(
        path,
        strict_shot_distribution=args.strict_shot_distribution,
        source_performance_path=source_path,
        skip_source_preservation=args.skip_source_preservation,
    )
    for finding in findings:
        print(finding)
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
