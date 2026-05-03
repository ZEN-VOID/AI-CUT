#!/usr/bin/env python3
"""Mechanically validate AIGC storyboard group Markdown files.

This script is intentionally read-only. It checks structure, rough word
limits, group IDs, required labels, YAML stats, and paired bridge shots. It
does not generate grouping decisions or creative text.
"""

from __future__ import annotations

import argparse
import re
import sys
from dataclasses import dataclass
from pathlib import Path

try:
    import yaml
except ImportError:  # pragma: no cover - repo environments usually include yaml
    yaml = None


GROUP_HEADING_RE = re.compile(r"^##\s+(\d+)-(\d+)-(\d+)\s*$", re.MULTILINE)
FENCED_YAML_RE = re.compile(r"```yaml\n(.*?)\n```", re.DOTALL)
EPISODE_RE = re.compile(r"第(\d+)集")
SCENE_HEADING_RE = re.compile(r"^###\s+场景(\d+)[：:]", re.MULTILINE)
STATS_COUNT_RE = re.compile(r"(\d+)")
OLD_VISIBLE_STYLE_LABELS = ("[全局风格]", "[类型元素]", "[画面风格]")
STYLE_LINE_COUNT = 3
GLOBAL_STYLE_REQUIRED_PREFIX = "视频生成的画面风格，光影和氛围与场景参照图保持一致。不生成文字字幕和BGM，仅生成物理互动音效与环境和氛围音效。"
ENTRY_LABEL = "入场画面："
EXIT_LABEL = "出场画面："
REQUIRED_YAML_KEYS = ("字数统计", "角色", "场景", "道具")
COUNT_TOLERANCE = 30
TARGET_CHAR_COUNT = 1680
HARD_CHAR_COUNT = 1980
MIN_REVIEW_CHAR_COUNT = 850


@dataclass
class GroupBlock:
    group_id: str
    episode: int
    scene: int
    index: int
    body: str
    line_number: int


@dataclass
class ValidationResult:
    errors: list[str]
    warnings: list[str]


def display_path(path: Path) -> str:
    try:
        return str(path.relative_to(Path.cwd()))
    except ValueError:
        return str(path)


def discover_files(path: Path) -> list[Path]:
    if path.is_file():
        return [path]
    return sorted(path.glob("第*集.md"))


def split_groups(text: str) -> list[GroupBlock]:
    matches = list(GROUP_HEADING_RE.finditer(text))
    groups: list[GroupBlock] = []
    for idx, match in enumerate(matches):
        start = match.start()
        end = matches[idx + 1].start() if idx + 1 < len(matches) else len(text)
        line_number = text[:start].count("\n") + 1
        episode, scene, group_index = map(int, match.groups())
        groups.append(
            GroupBlock(
                group_id=f"{episode}-{scene}-{group_index}",
                episode=episode,
                scene=scene,
                index=group_index,
                body=text[start:end].strip(),
                line_number=line_number,
            )
        )
    return groups


def strip_yaml_blocks(text: str) -> str:
    return FENCED_YAML_RE.sub("", text)


def estimate_chars(text: str) -> int:
    return len(re.findall(r"[\w\u4e00-\u9fff]|[^\s]", text, flags=re.UNICODE))


def extract_scene_numbers(body: str) -> list[int]:
    return [int(match.group(1)) for match in SCENE_HEADING_RE.finditer(body)]


def extract_label_content(body: str, label: str) -> str:
    lines = body.splitlines()
    for index, line in enumerate(lines):
        if line.strip() != label:
            continue
        collected: list[str] = []
        for candidate in lines[index + 1 :]:
            if not candidate.strip():
                if collected:
                    break
                continue
            if candidate.startswith("```yaml") or candidate.startswith("## "):
                break
            collected.append(candidate.strip())
        return "\n".join(collected).strip()
    return ""


def extract_prefixed_label_content(body: str, label: str) -> str:
    lines = body.splitlines()
    for index, line in enumerate(lines):
        stripped = line.strip()
        if stripped == label:
            collected: list[str] = []
            for candidate in lines[index + 1 :]:
                candidate_stripped = candidate.strip()
                if not candidate_stripped:
                    if collected:
                        break
                    continue
                if (
                    candidate.startswith("```yaml")
                    or candidate.startswith("#")
                    or candidate.startswith("## ")
                    or candidate_stripped in {ENTRY_LABEL, EXIT_LABEL}
                ):
                    break
                collected.append(candidate_stripped)
            return "\n".join(collected).strip()
        if stripped.startswith(label):
            return stripped[len(label) :].strip()
    return ""


def extract_style_lines(body: str) -> list[str]:
    lines = body.splitlines()
    style_lines: list[str] = []
    # Skip the group heading and collect the first non-empty north_star lines.
    for line in lines[1:]:
        stripped = line.strip()
        if stripped:
            style_lines.append(stripped)
        if len(style_lines) == STYLE_LINE_COUNT:
            break
    return style_lines


def find_prefixed_label_index(body: str, label: str) -> int | None:
    for index, line in enumerate(body.splitlines()):
        stripped = line.strip()
        if stripped == label or stripped.startswith(label):
            return index
    return None


def style_line_indices(body: str) -> list[int]:
    lines = body.splitlines()
    indices: list[int] = []
    for index, line in enumerate(lines[1:], start=1):
        if line.strip():
            indices.append(index)
        if len(indices) == STYLE_LINE_COUNT:
            break
    return indices


def has_label(body: str, label: str) -> bool:
    return any(line.strip() == label for line in body.splitlines())


def validate_yaml_stats(block: GroupBlock, char_count: int, errors: list[str]) -> None:
    yaml_blocks = FENCED_YAML_RE.findall(block.body)
    if not yaml_blocks:
        errors.append(f"line {block.line_number}: {block.group_id} missing fenced yaml stats")
        return
    stats_text = yaml_blocks[-1]
    if yaml is None:
        for key in REQUIRED_YAML_KEYS:
            if re.search(rf"^\s*{re.escape(key)}\s*:", stats_text, re.MULTILINE) is None:
                errors.append(f"line {block.line_number}: {block.group_id} yaml missing {key}")
        return
    try:
        data = yaml.safe_load(stats_text) or {}
    except Exception as exc:  # noqa: BLE001
        errors.append(f"line {block.line_number}: {block.group_id} invalid yaml stats: {exc}")
        return
    for key in REQUIRED_YAML_KEYS:
        if key not in data:
            errors.append(f"line {block.line_number}: {block.group_id} yaml missing {key}")
    count_value = data.get("字数统计")
    count_match = STATS_COUNT_RE.search(str(count_value or ""))
    if not count_match:
        errors.append(f"line {block.line_number}: {block.group_id} yaml 字数统计 must contain a number")
    else:
        declared_count = int(count_match.group(1))
        if abs(declared_count - char_count) > COUNT_TOLERANCE:
            errors.append(
                f"line {block.line_number}: {block.group_id} yaml 字数统计 {declared_count} differs from estimated {char_count} by more than {COUNT_TOLERANCE}"
            )
    for key in ("角色", "场景", "道具"):
        if key in data and not isinstance(data[key], list):
            errors.append(f"line {block.line_number}: {block.group_id} yaml {key} must be a list")


def validate_file(path: Path) -> ValidationResult:
    errors: list[str] = []
    warnings: list[str] = []
    text = path.read_text(encoding="utf-8")
    groups = split_groups(text)

    if not groups:
        return ValidationResult(
            errors=[f"{display_path(path)}: no storyboard group headings like '## 1-1-1' found"],
            warnings=[],
        )

    episode_match = EPISODE_RE.search(path.name) or EPISODE_RE.search(text[:500])
    expected_episode = int(episode_match.group(1)) if episode_match else None

    previous_by_scene: dict[int, int] = {}
    previous_exit: str | None = None
    previous_id: str | None = None

    for group in groups:
        prefix = f"{display_path(path)}:{group.line_number}: {group.group_id}"
        if expected_episode is not None and group.episode != expected_episode:
            errors.append(f"{prefix} episode segment does not match 第{expected_episode}集")

        scene_numbers = extract_scene_numbers(group.body)
        unique_scene_numbers = sorted(set(scene_numbers))
        if len(unique_scene_numbers) > 1:
            errors.append(f"{prefix} contains multiple scene headings: {unique_scene_numbers}")
        elif unique_scene_numbers and unique_scene_numbers[0] != group.scene:
            errors.append(
                f"{prefix} scene segment does not match body scene {unique_scene_numbers[0]}"
            )

        expected_index = previous_by_scene.get(group.scene, 0) + 1
        if group.index != expected_index:
            errors.append(f"{prefix} expected scene-local group index {expected_index}")
        previous_by_scene[group.scene] = group.index

        style_lines = extract_style_lines(group.body)
        if len(style_lines) < STYLE_LINE_COUNT:
            errors.append(f"{prefix} style header must contain {STYLE_LINE_COUNT} plain north_star lines")
        elif not style_lines[0].startswith(GLOBAL_STYLE_REQUIRED_PREFIX):
            errors.append(
                f"{prefix} global style line must start with fixed prefix: {GLOBAL_STYLE_REQUIRED_PREFIX}"
            )
        style_header = "\n".join(style_lines[:STYLE_LINE_COUNT])
        for label in OLD_VISIBLE_STYLE_LABELS:
            if label in style_header:
                errors.append(f"{prefix} style header exposes old visible label {label}")
        if "（" in style_header or "）" in style_header:
            errors.append(f"{prefix} style header must not wrap north_star fields in Chinese parentheses")
        if EXIT_LABEL not in group.body:
            errors.append(f"{prefix} missing label {EXIT_LABEL}")

        countable_text = strip_yaml_blocks(group.body)
        char_count = estimate_chars(countable_text)
        if char_count > HARD_CHAR_COUNT:
            errors.append(
                f"{prefix} estimated non-yaml char count {char_count} exceeds hard limit {HARD_CHAR_COUNT}"
            )
        elif char_count > TARGET_CHAR_COUNT:
            warnings.append(
                f"{prefix} estimated non-yaml char count {char_count} exceeds target {TARGET_CHAR_COUNT}; semantic review must justify keeping this dense group instead of splitting complete atomic units"
            )
        if char_count < MIN_REVIEW_CHAR_COUNT:
            warnings.append(
                f"{prefix} estimated non-yaml char count {char_count} is below review floor {MIN_REVIEW_CHAR_COUNT}; semantic review must justify a short-scene exception or rebalance complete atomic units"
            )

        validate_yaml_stats(group, char_count, errors)

        entry = extract_label_content(group.body, ENTRY_LABEL)
        exit_ = extract_label_content(group.body, EXIT_LABEL)
        if previous_exit is None:
            if has_label(group.body, ENTRY_LABEL):
                errors.append(f"{prefix} first group must omit entry shot label")
        elif entry != previous_exit:
            errors.append(
                f"{prefix} entry shot does not match previous group {previous_id} exit shot"
            )
        if not exit_:
            errors.append(f"{prefix} empty exit shot")
        previous_exit = exit_
        previous_id = group.group_id

    return ValidationResult(errors=errors, warnings=warnings)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("path", help="A storyboard group Markdown file or directory")
    args = parser.parse_args()

    target = Path(args.path)
    files = discover_files(target)
    if not files:
        print(f"No files found: {display_path(target)}")
        return 1

    errors: list[str] = []
    warnings: list[str] = []
    for file_path in files:
        result = validate_file(file_path)
        errors.extend(result.errors)
        warnings.extend(result.warnings)

    print("AIGC storyboard group validation")
    print(f"target: {display_path(target)}")
    print(f"files_checked: {len(files)}")
    print(f"errors: {len(errors)}")
    print(f"warnings: {len(warnings)}")
    if warnings:
        print()
        for warning in warnings:
            print(f"- warning: {warning}")
    if errors:
        print()
        for error in errors:
            print(f"- {error}")
        return 1
    print("[OK] storyboard group structure passed mechanical checks")
    return 0


if __name__ == "__main__":
    sys.exit(main())
