#!/usr/bin/env python3
"""Mechanical checks for 4-摄影 integrated storyboard-picture markup.

The script validates the new canonical output shape:

    角色动作：
    [0-2秒] ...
    [2-3秒] ...

It checks coverage, continuous time ranges, coarse segment-count
distribution, non-visual source preservation, frontmatter presence,
duration range hints, psychological/cognitive-reaction visual coverage,
abstract term detection, and empty block detection.
It does not generate storyboard prose or decide creative beats.
"""

from __future__ import annotations

import argparse
import re
from pathlib import Path


VISUAL_LABEL_RE = re.compile(
    r"^(?!分镜画面)(?!分镜明细)"
    r"([^：\n]*(画面|动作|表演|心理反应|心理变化|情绪反应|思考反应|角色思考|认知变化|意识变化|内心反应|内心活动|描写|特写|显影|角色造型|场面调度|转场)[^：\n]*)："
)
STORYBOARD_FIELD = "分镜画面："
LEGACY_DETAIL_FIELD = "分镜明细："
TIME_RANGE_RE = re.compile(r"^\[(\d+(?:\.\d+)?)-(\d+(?:\.\d+)?)秒\]\s*(.+)")
LEGACY_SHOT_RE = re.compile(r"^分镜\d+（约.+?秒）[:：]")
TWO_SEGMENT_WARNING_THRESHOLD = 0.8
MIN_BLOCKS_FOR_DISTRIBUTION_WARNING = 10

FRONTMATTER_REQUIRED_FIELDS = [
    "stage: 4-摄影",
    "output_path:",
    "duration_policy:",
]

ABSTRACT_TERMS_RE = re.compile(
    r"(?:象征|隐喻|寓意|暗示了|表现了|体现了|导演意图|世界观|命运|心理状态|孤独感|压迫感)"
)

BODY_MARKER = "【剧本正文】"
EPSILON = 1e-6


def parse_frontmatter(lines: list[str]) -> tuple[dict[str, str], list[str]]:
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
        findings.append(f"[ERROR] Frontmatter missing required field: {field}")

    if (
        "source_motion_path" not in frontmatter
        and "source_writing_directing_path" not in frontmatter
        and "fallback_source_writing_directing_path" not in frontmatter
    ):
        findings.append(
            "[ERROR] Frontmatter missing source field: source_motion_path or source_writing_directing_path"
        )
    return findings


def body_lines(lines: list[str]) -> list[str]:
    try:
        body_start = lines.index(BODY_MARKER)
    except ValueError:
        return []
    return lines[body_start:]


def normalized_source_non_visual_lines(lines: list[str]) -> list[str]:
    result: list[str] = []
    for line in body_lines(lines):
        if not line.strip():
            continue
        if VISUAL_LABEL_RE.match(line):
            continue
        result.append(line.rstrip())
    return result


def normalized_output_non_storyboard_lines(lines: list[str]) -> list[str]:
    result: list[str] = []
    body = body_lines(lines)
    index = 0
    while index < len(body):
        line = body[index]
        stripped = line.strip()
        if stripped == STORYBOARD_FIELD:
            index += 1
            while index < len(body):
                current = body[index].strip()
                if not current or TIME_RANGE_RE.match(current):
                    index += 1
                    continue
                break
            continue
        if VISUAL_LABEL_RE.match(stripped):
            index += 1
            while index < len(body):
                current = body[index].strip()
                if not current or TIME_RANGE_RE.match(current):
                    index += 1
                    continue
                break
            continue
        if stripped and stripped != LEGACY_DETAIL_FIELD:
            result.append(line.rstrip())
        index += 1
    return result


def count_source_visual_units(lines: list[str]) -> int:
    return sum(1 for line in body_lines(lines) if VISUAL_LABEL_RE.match(line))


def validate_source_preservation(
    output_lines: list[str], source_path: Path
) -> tuple[bool, list[str], int | None]:
    findings: list[str] = []
    if not source_path.is_file():
        return False, [f"[ERROR] Source performance file not found: {source_path}"], None

    source_lines = source_path.read_text(encoding="utf-8").splitlines()
    source_non_visual = normalized_source_non_visual_lines(source_lines)
    output_non_storyboard = normalized_output_non_storyboard_lines(output_lines)
    source_visual_count = count_source_visual_units(source_lines)

    if source_non_visual == output_non_storyboard:
        return True, ["[OK] Non-visual source preservation check passed."], source_visual_count

    first_diff = 0
    max_common = min(len(source_non_visual), len(output_non_storyboard))
    while (
        first_diff < max_common
        and source_non_visual[first_diff] == output_non_storyboard[first_diff]
    ):
        first_diff += 1

    findings.append(
        "[ERROR] Non-visual source preservation check failed after removing visual-field storyboard time ranges."
    )
    findings.append(
        f"[INFO] source_non_visual_lines={len(source_non_visual)} "
        f"output_non_storyboard_lines={len(output_non_storyboard)}"
    )
    if first_diff < len(source_non_visual):
        findings.append(
            f"[INFO] first_source_mismatch_line={first_diff + 1}: "
            f"{source_non_visual[first_diff][:100]}"
        )
    if first_diff < len(output_non_storyboard):
        findings.append(
            f"[INFO] first_output_mismatch_line={first_diff + 1}: "
            f"{output_non_storyboard[first_diff][:100]}"
        )
    return False, findings, source_visual_count


def validate(
    path: Path,
    *,
    strict_segment_distribution: bool = False,
    source_writing_directing_path: Path | None = None,
    skip_source_preservation: bool = False,
) -> tuple[bool, list[str]]:
    lines = path.read_text(encoding="utf-8").splitlines()
    findings: list[str] = []
    ok = True
    storyboard_count = 0
    segment_count_distribution: dict[int, int] = {}
    source_visual_count: int | None = None

    fm_findings = validate_frontmatter(lines)
    for finding in fm_findings:
        findings.append(finding)
        if "[ERROR]" in finding:
            ok = False

    if not skip_source_preservation:
        frontmatter, _ = parse_frontmatter(lines)
        resolved_source = source_writing_directing_path
        if resolved_source is None and frontmatter.get("source_motion_path"):
            resolved_source = Path(frontmatter["source_motion_path"])
        if resolved_source is None and frontmatter.get("source_writing_directing_path"):
            resolved_source = Path(frontmatter["source_writing_directing_path"])
        if resolved_source is None and frontmatter.get("fallback_source_writing_directing_path"):
            resolved_source = Path(frontmatter["fallback_source_writing_directing_path"])
        if resolved_source is not None:
            if not resolved_source.is_absolute():
                resolved_source = Path.cwd() / resolved_source
            source_ok, source_findings, source_visual_count = validate_source_preservation(
                lines, resolved_source
            )
            findings.extend(source_findings)
            if not source_ok:
                ok = False
        else:
            findings.append(
                "[WARN] Source preservation check skipped; no source_motion_path or source_writing_directing_path found."
            )

    index = 0
    while index < len(lines):
        stripped = lines[index].strip()
        if stripped == LEGACY_DETAIL_FIELD or LEGACY_SHOT_RE.match(stripped):
            findings.append(
                f"[ERROR] Legacy shot-detail markup at line {index + 1}; expected original visual field title with [N-N秒] ranges."
            )
            ok = False
            index += 1
            continue
        if stripped == STORYBOARD_FIELD:
            findings.append(
                f"[ERROR] Standalone 分镜画面 field at line {index + 1}; expected the original visual field title to carry [N-N秒] ranges."
            )
            ok = False
            index += 1
            continue
        if not VISUAL_LABEL_RE.match(stripped):
            index += 1
            continue

        storyboard_count += 1
        if "：" in stripped and stripped.split("：", 1)[1].strip():
            findings.append(
                f"[ERROR] Visual field line {index + 1} must keep only the original title; put storyboard prose in [N-N秒] lines below."
            )
            ok = False
        cursor = index + 1
        ranges: list[tuple[float, float]] = []
        while cursor < len(lines):
            current = lines[cursor].strip()
            if not current:
                cursor += 1
                continue
            match = TIME_RANGE_RE.match(current)
            if not match:
                break

            start = float(match.group(1))
            end = float(match.group(2))
            content = match.group(3)
            if end <= start:
                findings.append(
                    f"[ERROR] Invalid non-increasing time range at line {cursor + 1}: {current[:80]}"
                )
                ok = False
            if not ranges and abs(start) > EPSILON:
                findings.append(
                    f"[ERROR] First time range after line {index + 1} must start at 0秒."
                )
                ok = False
            if ranges and abs(start - ranges[-1][1]) > EPSILON:
                findings.append(
                    f"[ERROR] Non-continuous time range at line {cursor + 1}; "
                    f"expected start {ranges[-1][1]:g}秒, got {start:g}秒."
                )
                ok = False

            duration = end - start
            if duration < 1.0:
                findings.append(
                    f"[WARN] Duration {duration:g}s at line {cursor + 1}; verify deliberate flash-cut or instant reaction."
                )
            elif duration > 5.0:
                findings.append(
                    f"[WARN] Duration {duration:g}s at line {cursor + 1}; verify strong exception with dialogue, long blocking, or major cognitive peak."
                )
            elif duration > 3.0:
                findings.append(
                    f"[WARN] Duration {duration:g}s at line {cursor + 1}; verify short-drama AIGC necessity."
                )

            term_match = ABSTRACT_TERMS_RE.search(content)
            if term_match:
                findings.append(
                    f"[WARN] Abstract term \"{term_match.group()}\" at line {cursor + 1}; "
                    "verify translated to visible camera/visual language."
                )

            ranges.append((start, end))
            cursor += 1

        if not ranges:
            findings.append(
                f"[ERROR] Empty visual field storyboard block at line {index + 1} (no [起始秒-结束秒] entries)."
            )
            ok = False
        else:
            segment_count_distribution[len(ranges)] = (
                segment_count_distribution.get(len(ranges), 0) + 1
            )
        index = max(cursor, index + 1)

    if source_visual_count is not None and source_visual_count != storyboard_count:
        findings.append(
            f"[ERROR] Source visual unit count ({source_visual_count}) does not match output visual field storyboard blocks ({storyboard_count})."
        )
        ok = False

    findings.append(f"[INFO] visual_field_storyboard_blocks={storyboard_count}")
    if segment_count_distribution:
        distribution_text = ", ".join(
            f"{segment_count}:{count}"
            for segment_count, count in sorted(segment_count_distribution.items())
        )
        findings.append(f"[INFO] segment_count_distribution={distribution_text}")

        two_segment_blocks = segment_count_distribution.get(2, 0)
        total_blocks = sum(segment_count_distribution.values())
        two_segment_ratio = two_segment_blocks / total_blocks if total_blocks else 0
        if (
            total_blocks >= MIN_BLOCKS_FOR_DISTRIBUTION_WARNING
            and two_segment_ratio >= TWO_SEGMENT_WARNING_THRESHOLD
        ):
            severity = "ERROR" if strict_segment_distribution else "WARN"
            findings.append(
                f"[{severity}] Two-segment blocks are highly concentrated "
                f"({two_segment_blocks}/{total_blocks}, {two_segment_ratio:.1%}). "
                "Review beat_map/rhythm_profile/sequence_density_curve/shot_count_decision."
            )
            if strict_segment_distribution:
                ok = False

    if ok:
        findings.append("[OK] Cinematography visual-field storyboard markup is mechanically valid.")
    return ok, findings


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate 4-摄影 integrated storyboard-picture markup.")
    parser.add_argument("episode_file", help="Path to projects/aigc/<项目名>/4-摄影/第N集.md")
    parser.add_argument(
        "--strict-shot-distribution",
        "--strict-segment-distribution",
        dest="strict_segment_distribution",
        action="store_true",
        help="Treat highly concentrated 2-segment distribution as an error instead of a warning.",
    )
    parser.add_argument("--source-performance-path", help="Legacy alias for source body preservation check.")
    parser.add_argument("--source-motion-path", help="Override source motion-enrichment file path.")
    parser.add_argument("--source-writing-directing-path", help="Override source writing-directing file path.")
    parser.add_argument("--skip-source-preservation", action="store_true")
    args = parser.parse_args()

    path = Path(args.episode_file)
    if not path.is_file():
        print(f"[ERROR] Not a file: {path}")
        return 1

    source_override = (
        args.source_motion_path
        or args.source_writing_directing_path
        or args.source_performance_path
    )
    source_path = Path(source_override) if source_override else None
    ok, findings = validate(
        path,
        strict_segment_distribution=args.strict_segment_distribution,
        source_writing_directing_path=source_path,
        skip_source_preservation=args.skip_source_preservation,
    )
    for finding in findings:
        print(finding)
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
