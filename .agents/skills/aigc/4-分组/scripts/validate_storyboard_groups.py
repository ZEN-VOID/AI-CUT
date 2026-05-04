#!/usr/bin/env python3
"""Mechanically validate AIGC storyboard group Markdown files.

This script is intentionally read-only. It checks structure, rough word
limits, group IDs, required connector fields, YAML stats, and connector shape. It
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
CONNECTOR_HEADING_RE = re.compile(
    r"^##\s+((\d+-\d+-\d+)~(\d+-\d+-\d+))\s*$",
    re.MULTILINE,
)
LEGACY_CONNECTOR_HEADING_RE = re.compile(r"^##\s+组间连接件：", re.MULTILINE)
FENCED_YAML_RE = re.compile(r"```yaml\n(.*?)\n```", re.DOTALL)
EPISODE_RE = re.compile(r"第(\d+)集")
SCENE_HEADING_RE = re.compile(r"^###\s+场景(\d+)[：:]", re.MULTILINE)
STATS_COUNT_RE = re.compile(r"(\d+)")
OLD_VISIBLE_STYLE_LABELS = ("[全局风格]", "[类型元素]", "[画面风格]")
STYLE_LINE_COUNT = 3
GLOBAL_STYLE_REQUIRED_PREFIX = "视频生成的画面风格，光影和氛围与场景参照图保持一致。不生成文字字幕和BGM，仅生成物理互动音效与环境和氛围音效。"
LEGACY_ENTRY_LABEL = "入场画面："
LEGACY_EXIT_LABEL = "出场画面："
CONNECTOR_REQUIRED_LABELS = (
    "连接类型：",
    "连接方法：",
    "时长：",
    "变化过程：",
    "主体运动：",
    "运镜设计：",
    "透视适应：",
    "避免元素：",
)
CONNECTOR_TYPES = ("同场景连接", "跨场景连接")
ABSTRACT_CONNECTOR_METHODS = ("依赖型", "流动型", "变形型", "复合型", "无连接")
DEPRECATED_CONNECTOR_LABELS = ("起点尾帧：", "目标首帧：", "分镜ID：", "连接件提示：")
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
class ConnectorBlock:
    connector_id: str
    from_group: str
    to_group: str
    body: str
    line_number: int


@dataclass
class SectionBlock:
    kind: str
    identifier: str
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
    section_starts = sorted(
        [match.start() for match in matches]
        + [match.start() for match in CONNECTOR_HEADING_RE.finditer(text)]
    )
    groups: list[GroupBlock] = []
    for match in matches:
        start = match.start()
        next_starts = [position for position in section_starts if position > start]
        end = next_starts[0] if next_starts else len(text)
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


def split_connectors(text: str) -> list[ConnectorBlock]:
    matches = list(CONNECTOR_HEADING_RE.finditer(text))
    boundaries = sorted(
        [(match.start(), "connector", idx) for idx, match in enumerate(matches)]
        + [(match.start(), "group", idx) for idx, match in enumerate(GROUP_HEADING_RE.finditer(text))]
    )
    connectors: list[ConnectorBlock] = []
    for idx, match in enumerate(matches):
        start = match.start()
        next_starts = [position for position, _, _ in boundaries if position > start]
        end = next_starts[0] if next_starts else len(text)
        line_number = text[:start].count("\n") + 1
        connector_id, from_group, to_group = match.groups()
        connectors.append(
            ConnectorBlock(
                connector_id=connector_id,
                from_group=from_group,
                to_group=to_group,
                body=text[start:end].strip(),
                line_number=line_number,
            )
        )
    return connectors


def ordered_sections(text: str) -> list[SectionBlock]:
    matches: list[tuple[int, SectionBlock]] = []
    for match in GROUP_HEADING_RE.finditer(text):
        line_number = text[: match.start()].count("\n") + 1
        episode, scene, group_index = match.groups()
        matches.append(
            (
                match.start(),
                SectionBlock(
                    kind="group",
                    identifier=f"{episode}-{scene}-{group_index}",
                    line_number=line_number,
                ),
            )
        )
    for match in CONNECTOR_HEADING_RE.finditer(text):
        line_number = text[: match.start()].count("\n") + 1
        connector_id = match.group(1)
        matches.append(
            (
                match.start(),
                SectionBlock(
                    kind="connector",
                    identifier=connector_id,
                    line_number=line_number,
                ),
            )
        )
    return [section for _, section in sorted(matches, key=lambda item: item[0])]


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
                    or candidate_stripped in set(CONNECTOR_REQUIRED_LABELS)
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


def extract_content_lines_before_label(body: str, label: str) -> list[str]:
    lines = body.splitlines()
    label_index = find_prefixed_label_index(body, label)
    if label_index is None:
        return []
    return [line.strip() for line in lines[1:label_index] if line.strip()]


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


def connector_sequence(groups: list[GroupBlock]) -> list[tuple[str, str]]:
    return [(groups[idx].group_id, groups[idx + 1].group_id) for idx in range(len(groups) - 1)]


def strip_group_non_body_sections(body: str) -> str:
    lines = body.splitlines()
    content_lines: list[str] = []
    non_empty_seen = 0
    for line in lines:
        stripped = line.strip()
        if stripped.startswith("## "):
            continue
        if non_empty_seen < STYLE_LINE_COUNT:
            if stripped:
                non_empty_seen += 1
            continue
        if stripped.startswith("```yaml"):
            break
        content_lines.append(line)
    return "\n".join(content_lines).strip()


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


def validate_connectors(
    path: Path,
    text: str,
    groups: list[GroupBlock],
    connectors: list[ConnectorBlock],
    errors: list[str],
) -> None:
    expected_pairs = connector_sequence(groups)
    connector_pairs = [(connector.from_group, connector.to_group) for connector in connectors]
    if connector_pairs != expected_pairs:
        errors.append(
            f"{display_path(path)}: connector sequence {connector_pairs} does not match adjacent group sequence {expected_pairs}"
        )
    expected_section_sequence: list[tuple[str, str]] = []
    for idx, group in enumerate(groups):
        expected_section_sequence.append(("group", group.group_id))
        if idx + 1 < len(groups):
            expected_section_sequence.append(
                ("connector", f"{group.group_id}~{groups[idx + 1].group_id}")
            )
    actual_section_sequence = [
        (section.kind, section.identifier) for section in ordered_sections(text)
    ]
    if actual_section_sequence != expected_section_sequence:
        errors.append(
            f"{display_path(path)}: connector sections must be physically placed between adjacent groups; actual {actual_section_sequence} expected {expected_section_sequence}"
        )

    for connector in connectors:
        expected_id = f"{connector.from_group}~{connector.to_group}"
        prefix = f"{display_path(path)}:{connector.line_number}: connector {connector.connector_id}"
        if connector.connector_id != expected_id:
            errors.append(f"{prefix} heading id must equal {expected_id}")
        connector_style_lines = extract_content_lines_before_label(connector.body, "连接类型：")
        if len(connector_style_lines) != STYLE_LINE_COUNT:
            errors.append(
                f"{prefix} connector style header must contain {STYLE_LINE_COUNT} plain north_star lines before 连接类型"
            )
        elif not connector_style_lines[0].startswith(GLOBAL_STYLE_REQUIRED_PREFIX):
            errors.append(
                f"{prefix} global style line must start with fixed prefix: {GLOBAL_STYLE_REQUIRED_PREFIX}"
            )
        connector_style_header = "\n".join(connector_style_lines[:STYLE_LINE_COUNT])
        if any(label in connector_style_header for label in OLD_VISIBLE_STYLE_LABELS):
            errors.append(f"{prefix} connector style header exposes old visible style label")
        if "（" in connector_style_header or "）" in connector_style_header:
            errors.append(f"{prefix} connector style header must not wrap north_star fields in Chinese parentheses")
        for label in CONNECTOR_REQUIRED_LABELS:
            if label not in connector.body:
                errors.append(f"{prefix} missing label {label}")
        connection_type = extract_prefixed_label_content(connector.body, "连接类型：")
        if connection_type and connection_type not in CONNECTOR_TYPES:
            errors.append(
                f"{prefix} 连接类型 must be one of {', '.join(CONNECTOR_TYPES)}"
            )
        connection_method = extract_prefixed_label_content(connector.body, "连接方法：")
        if not connection_method:
            errors.append(f"{prefix} empty 连接方法")
        elif connection_method in ABSTRACT_CONNECTOR_METHODS:
            errors.append(
                f"{prefix} 连接方法 must be a concrete visual method description, not only abstract label {connection_method}"
            )
        if "无连接" in connection_method and "理由" not in connector.body:
            errors.append(f"{prefix} 无连接 must include a reason in 连接方法 or 避免元素")
        duration = extract_prefixed_label_content(connector.body, "时长：")
        if duration and "3-4" not in duration:
            errors.append(f"{prefix} 时长 must declare 3-4秒 by default")
        process = extract_prefixed_label_content(connector.body, "变化过程：")
        if not process:
            errors.append(f"{prefix} empty 变化过程")
        subject_motion = extract_prefixed_label_content(connector.body, "主体运动：")
        if not subject_motion:
            errors.append(f"{prefix} empty 主体运动")
        camera_motion = extract_prefixed_label_content(connector.body, "运镜设计：")
        if not camera_motion:
            errors.append(f"{prefix} empty 运镜设计")
        perspective = extract_prefixed_label_content(connector.body, "透视适应：")
        if not perspective:
            errors.append(f"{prefix} empty 透视适应")
        avoid_elements = extract_prefixed_label_content(connector.body, "避免元素：")
        if not avoid_elements:
            errors.append(f"{prefix} empty 避免元素")
        for label in DEPRECATED_CONNECTOR_LABELS:
            if label in connector.body:
                errors.append(f"{prefix} must not use deprecated connector label {label}")
        if LEGACY_ENTRY_LABEL in connector.body or LEGACY_EXIT_LABEL in connector.body:
            errors.append(f"{prefix} must not use legacy entry/exit labels")


def validate_file(path: Path) -> ValidationResult:
    errors: list[str] = []
    warnings: list[str] = []
    text = path.read_text(encoding="utf-8")
    groups = split_groups(text)
    connectors = split_connectors(text)

    if not groups:
        return ValidationResult(
            errors=[f"{display_path(path)}: no storyboard group headings like '## 1-1-1' found"],
            warnings=[],
        )

    episode_match = EPISODE_RE.search(path.name) or EPISODE_RE.search(text[:500])
    expected_episode = int(episode_match.group(1)) if episode_match else None

    if LEGACY_ENTRY_LABEL in text or LEGACY_EXIT_LABEL in text:
        errors.append(f"{display_path(path)}: legacy entry/exit labels are no longer allowed")
    if LEGACY_CONNECTOR_HEADING_RE.search(text):
        errors.append(f"{display_path(path)}: connector heading must be '## <上一个分镜组ID>~<下一个分镜组ID>' without '组间连接件：' prefix")

    previous_by_scene: dict[int, int] = {}

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

        countable_text = strip_group_non_body_sections(group.body)
        char_count = estimate_chars(countable_text)
        if char_count > HARD_CHAR_COUNT:
            errors.append(
                f"{prefix} estimated pure body char count {char_count} exceeds hard limit {HARD_CHAR_COUNT}"
            )
        elif char_count > TARGET_CHAR_COUNT:
            warnings.append(
                f"{prefix} estimated pure body char count {char_count} exceeds target {TARGET_CHAR_COUNT}; semantic review must justify keeping this dense group instead of splitting complete atomic units"
            )
        if char_count < MIN_REVIEW_CHAR_COUNT:
            warnings.append(
                f"{prefix} estimated pure body char count {char_count} is below review floor {MIN_REVIEW_CHAR_COUNT}; semantic review must justify a short-scene exception or rebalance complete atomic units"
            )

        validate_yaml_stats(group, char_count, errors)

    validate_connectors(path, text, groups, connectors, errors)

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
