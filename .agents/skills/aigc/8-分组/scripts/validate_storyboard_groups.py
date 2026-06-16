#!/usr/bin/env python3
"""Mechanically validate AIGC storyboard group Markdown files.

This script is intentionally read-only. It checks structure, rough word
limits, storyboard block durations, group IDs, global style fields,
group-baseline time ranges, deprecated connector blocks,
deprecated supplemental-first-frame/hulong-frame fields, deprecated
position-detail fields, and YAML stats. It does not generate grouping decisions
or creative text.
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
SCENE_TITLE_LINE_RE = re.compile(r"^场景(\d+)[：:].+")
STATS_COUNT_RE = re.compile(r"(\d+)")
LEGACY_SHOT_DURATION_RE = re.compile(r"分镜\d+（约((?:0\.5)|(?:[1-9]\d?(?:\.\d+)?))秒）")
SHOT_LINE_DURATION_RE = re.compile(
    r"分镜\d+（((?:0)|(?:[1-9]\d?)(?:\.\d+)?)-((?:0)|(?:[1-9]\d?)(?:\.\d+)?)秒）[：:]"
)
BRACKET_DURATION_RE = re.compile(
    r"\[((?:0)|(?:[1-9]\d?)(?:\.\d+)?)-((?:0)|(?:[1-9]\d?)(?:\.\d+)?)秒\]"
)
FIELD_LABEL_RE = re.compile(r"^[^\s\[]+[：:]")
VISUAL_FIELD_LABEL_RE = re.compile(
    r"^(?!分镜画面[：:]?$)(?!画面构图[：:]?$)(?!全局风格[：:]?$)"
    r"[^：:\n]*(画面|动作|表演|心理反应|心理变化|情绪反应|思考反应|角色思考|认知变化|意识变化|内心反应|内心活动|描写|特写|显影|角色造型|场面调度|转场)[^：:\n]*[：:]$"
)

GLOBAL_STYLE_LABEL = "全局风格："
VISUAL_STYLE_LABEL = "画面风格："
GLOBAL_STYLE_REQUIRED_PREFIX = "视频生成的画面风格，光影和氛围与场景参照图保持一致。需要生成现场物理互动音效、氛围感音效、环境声、自然现象声、动作声，不要生成任何字幕，不要生成背景音乐。"
MAX_GLOBAL_STYLE_PROJECTION_CHARS = 300
STYLE_LINE_COUNT = 1
OLD_VISIBLE_STYLE_LABELS = ("[全局风格]", "[类型元素]")

STORYBOARD_PICTURE_LABEL = "分镜画面："
DEPRECATED_POSITION_DETAIL_LABELS = (
    "画面构图：",
    "左侧：",
    "中间：",
    "右侧：",
    "前景：",
    "中景：",
    "背景：",
)
PROHIBITED_GROUP_SUBJECT_LABEL_RE = re.compile(r"^(角色|场景|道具|主体信息)[：:]", re.MULTILINE)
DEPRECATED_GROUP_LABELS = (
    "入场镜头：",
    "出场画面：",
    "画面属性：",
    "增补首帧：",
    "回龙帧：",
    "入场画面：",
    *DEPRECATED_POSITION_DETAIL_LABELS,
)

CONNECTOR_SCENE_ARROW = "➡️"
DEPRECATED_CONNECTOR_LABELS = DEPRECATED_GROUP_LABELS + (
    "连接类型：",
    "连接方法：",
    "时长：",
    "变化过程：",
    "主体运动：",
    "运镜设计：",
    "透视适应：",
    "避免元素：",
    "起点尾帧：",
    "目标首帧：",
    "分镜ID：",
    "连接件提示：",
)
REQUIRED_YAML_KEYS = ("字数统计", "时长估算", "角色", "场景", "道具")
YAML_SUBJECT_KEYS = {
    "角色": ("characters", "CHR-"),
    "场景": ("scenes", "SCN-"),
    "道具": ("props", "PRP-"),
}
COUNT_TOLERANCE = 30
DURATION_TOLERANCE = 0.05
TARGET_CHAR_COUNT = 1680
MIN_REVIEW_CHAR_COUNT = 850
MIN_REVIEW_SECONDS = 10.0
MAX_REVIEW_SECONDS = 14.5
HALF_SECOND_TOLERANCE = 0.01


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


@dataclass
class SubjectRegistry:
    by_domain: dict[str, dict[str, str]]

    @classmethod
    def empty(cls) -> "SubjectRegistry":
        return cls(by_domain={domain: {} for domain in YAML_SUBJECT_KEYS})

    def canonical_name(self, yaml_key: str, subject_id: str) -> str | None:
        return self.by_domain.get(yaml_key, {}).get(subject_id)


def display_path(path: Path) -> str:
    try:
        return str(path.relative_to(Path.cwd()))
    except ValueError:
        return str(path)


def load_subject_registry(path: Path | None, errors: list[str]) -> SubjectRegistry | None:
    if path is None:
        return None
    if yaml is None:
        errors.append("--subject-registry-yaml requires PyYAML to parse the registry")
        return SubjectRegistry.empty()
    if not path.exists():
        errors.append(f"subject registry not found: {display_path(path)}")
        return SubjectRegistry.empty()
    try:
        data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    except Exception as exc:  # noqa: BLE001
        errors.append(f"invalid subject registry yaml {display_path(path)}: {exc}")
        return SubjectRegistry.empty()

    subjects = data.get("subjects") or {}
    registry = SubjectRegistry.empty()
    for yaml_key, (registry_key, expected_prefix) in YAML_SUBJECT_KEYS.items():
        entries = subjects.get(registry_key) or []
        if not isinstance(entries, list):
            errors.append(f"subject registry subjects.{registry_key} must be a list")
            continue
        for index, entry in enumerate(entries, start=1):
            if not isinstance(entry, dict):
                errors.append(f"subject registry subjects.{registry_key}[{index}] must be a mapping")
                continue
            subject_id = str(entry.get("id") or "").strip()
            canonical_name = str(entry.get("canonical_name") or "").strip()
            if not subject_id or not canonical_name:
                errors.append(
                    f"subject registry subjects.{registry_key}[{index}] must contain id and canonical_name"
                )
                continue
            if not subject_id.startswith(expected_prefix):
                errors.append(
                    f"subject registry id {subject_id} in subjects.{registry_key}[{index}] must start with {expected_prefix}"
                )
            registry.by_domain[yaml_key][subject_id] = canonical_name
    return registry


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
    for match in matches:
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


def estimate_duration_seconds(text: str) -> float:
    ranges = list(SHOT_LINE_DURATION_RE.finditer(text)) + list(BRACKET_DURATION_RE.finditer(text))
    if not ranges:
        return 0.0
    return max(float(match.group(2)) for match in ranges)


def ends_on_half_second(value: float) -> bool:
    return abs((value % 1.0) - 0.5) <= HALF_SECOND_TOLERANCE


def validate_group_baseline_ranges(prefix: str, text: str, errors: list[str]) -> None:
    ranges = [
        (float(match.group(1)), float(match.group(2)), match.group(0))
        for match in sorted(
            list(SHOT_LINE_DURATION_RE.finditer(text)) + list(BRACKET_DURATION_RE.finditer(text)),
            key=lambda item: item.start(),
        )
    ]
    if not ranges:
        return
    first_start = ranges[0][0]
    if abs(first_start) > 0.01:
        errors.append(
            f"{prefix} first storyboard time range must start at current group baseline 0s, got {ranges[0][2]}"
        )
    previous_end = 0.0
    for start, end, raw_range in ranges:
        if end <= start:
            errors.append(f"{prefix} invalid non-positive storyboard time range {raw_range}")
        if abs(start - previous_end) > 0.01:
            errors.append(
                f"{prefix} storyboard time ranges must be continuous in current group baseline; {raw_range} must start at previous end {previous_end:g}s"
            )
        previous_end = end


def extract_scene_numbers(body: str) -> list[int]:
    return [int(match.group(1)) for match in SCENE_HEADING_RE.finditer(body)]


def extract_leading_scene_title(body: str) -> str:
    for line in body.splitlines()[1:]:
        stripped = line.strip()
        if stripped:
            return stripped
    return ""


def extract_scene_title_numbers(line: str) -> list[int]:
    return [int(match) for match in re.findall(r"场景(\d+)[：:]", line)]


def is_scene_title_line(line: str) -> bool:
    if CONNECTOR_SCENE_ARROW in line:
        return all(SCENE_TITLE_LINE_RE.match(part.strip()) for part in line.split(CONNECTOR_SCENE_ARROW))
    return SCENE_TITLE_LINE_RE.match(line.strip()) is not None


def nonempty_lines_after_heading(body: str) -> list[tuple[int, str]]:
    return [
        (index, line.strip())
        for index, line in enumerate(body.splitlines()[1:], start=1)
        if line.strip()
    ]


def find_prefixed_label_index(body: str, label: str) -> int | None:
    for index, line in enumerate(body.splitlines()):
        stripped = line.strip()
        if stripped == label or stripped.startswith(label):
            return index
    return None


def find_first_time_range_index(body: str) -> int | None:
    for index, line in enumerate(body.splitlines()):
        if SHOT_LINE_DURATION_RE.search(line) or BRACKET_DURATION_RE.search(line):
            return index
    return None


def find_first_visual_field_index(body: str) -> int | None:
    for index, line in enumerate(body.splitlines()):
        if VISUAL_FIELD_LABEL_RE.match(line.strip()):
            return index
    return None


def find_exact_label_index(body: str, label: str) -> int | None:
    for index, line in enumerate(body.splitlines()):
        if line.strip() == label:
            return index
    return None


def first_fenced_yaml_line_index(body: str) -> int | None:
    for index, line in enumerate(body.splitlines()):
        if line.startswith("```yaml"):
            return index
    return None


def extract_prefixed_label_content(
    body: str,
    label: str,
    stop_labels: tuple[str, ...] = (),
) -> str:
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
                    or VISUAL_FIELD_LABEL_RE.match(candidate_stripped)
                    or SHOT_LINE_DURATION_RE.search(candidate_stripped)
                    or BRACKET_DURATION_RE.search(candidate_stripped)
                    or any(candidate_stripped.startswith(stop_label) for stop_label in stop_labels)
                ):
                    break
                collected.append(candidate_stripped)
            return "\n".join(collected).strip()
        if stripped.startswith(label):
            return stripped[len(label) :].strip()
    return ""


def extract_global_style_lines(body: str) -> list[str]:
    lines = body.splitlines()
    global_index = find_exact_label_index(body, GLOBAL_STYLE_LABEL)
    if global_index is None:
        return []
    style_lines: list[str] = []
    for line in lines[global_index + 1 :]:
        stripped = line.strip()
        if not stripped:
            continue
        if (
            stripped.startswith(VISUAL_STYLE_LABEL)
            or stripped.startswith(STORYBOARD_PICTURE_LABEL)
            or FIELD_LABEL_RE.match(stripped)
            or VISUAL_FIELD_LABEL_RE.match(stripped)
            or SHOT_LINE_DURATION_RE.search(stripped)
            or BRACKET_DURATION_RE.search(stripped)
            or stripped.startswith("## ")
            or stripped.startswith("```yaml")
        ):
            break
        style_lines.append(stripped)
    return style_lines


def style_line_indices(body: str) -> list[int]:
    lines = body.splitlines()
    global_index = find_exact_label_index(body, GLOBAL_STYLE_LABEL)
    if global_index is None:
        return []
    indices: list[int] = []
    for index, line in enumerate(lines[global_index + 1 :], start=global_index + 1):
        stripped = line.strip()
        if stripped:
            indices.append(index)
        if len(indices) == STYLE_LINE_COUNT:
            break
    return indices


def validate_global_style(prefix: str, body: str, errors: list[str]) -> None:
    style_lines = extract_global_style_lines(body)
    if len(style_lines) != STYLE_LINE_COUNT:
        errors.append(
            f"{prefix} {GLOBAL_STYLE_LABEL} must contain {STYLE_LINE_COUNT} non-empty style lines"
        )
        return
    if not style_lines[0].startswith(GLOBAL_STYLE_REQUIRED_PREFIX):
        errors.append(
            f"{prefix} global style line must start with fixed prefix: {GLOBAL_STYLE_REQUIRED_PREFIX}"
        )
    else:
        projected_style = style_lines[0][len(GLOBAL_STYLE_REQUIRED_PREFIX) :].strip()
        projected_style_chars = estimate_chars(projected_style)
        if not projected_style:
            errors.append(f"{prefix} empty global style projection after fixed prefix")
        elif projected_style_chars > MAX_GLOBAL_STYLE_PROJECTION_CHARS:
            errors.append(
                f"{prefix} global style projection {projected_style_chars} chars exceeds {MAX_GLOBAL_STYLE_PROJECTION_CHARS}; extract only current evidence-relevant style"
            )
    style_header = "\n".join(style_lines)
    for label in OLD_VISIBLE_STYLE_LABELS:
        if label in style_header:
            errors.append(f"{prefix} style header exposes old visible label {label}")
    if "（" in style_header or "）" in style_header:
        errors.append(f"{prefix} style header must not wrap north_star fields in Chinese parentheses")


def connector_sequence(groups: list[GroupBlock]) -> list[tuple[str, str]]:
    return [(groups[idx].group_id, groups[idx + 1].group_id) for idx in range(len(groups) - 1)]


def strip_group_non_body_sections(body: str) -> str:
    lines = body.splitlines()
    content_lines: list[str] = []
    skip_global_style_lines = 0
    for line in lines:
        stripped = line.strip()
        if stripped.startswith("## "):
            continue
        if stripped.startswith("```yaml"):
            break
        if stripped.startswith(GLOBAL_STYLE_LABEL):
            skip_global_style_lines = STYLE_LINE_COUNT
            continue
        if skip_global_style_lines:
            if stripped:
                skip_global_style_lines -= 1
            continue
        content_lines.append(line)
    return "\n".join(content_lines).strip()


def validate_yaml_stats(
    block: GroupBlock,
    char_count: int,
    duration_seconds: float,
    errors: list[str],
    warnings: list[str],
    subject_registry: SubjectRegistry | None = None,
) -> None:
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
    duration_value = data.get("时长估算")
    duration_match = re.search(r"(\d+(?:\.\d+)?)", str(duration_value or ""))
    if not duration_match:
        errors.append(f"line {block.line_number}: {block.group_id} yaml 时长估算 must contain a number")
    else:
        declared_duration = float(duration_match.group(1))
        if not ends_on_half_second(declared_duration):
            errors.append(
                f"line {block.line_number}: {block.group_id} yaml 时长估算 {declared_duration:g}s must end on .5s"
            )
        if abs(declared_duration - duration_seconds) > DURATION_TOLERANCE:
            errors.append(
                f"line {block.line_number}: {block.group_id} yaml 时长估算 {declared_duration:g} differs from estimated {duration_seconds:g} by more than {DURATION_TOLERANCE:g}"
            )
    for key in ("角色", "场景", "道具"):
        if key in data and not isinstance(data[key], list):
            errors.append(f"line {block.line_number}: {block.group_id} yaml {key} must be a list")
    if subject_registry is not None:
        validate_yaml_subject_registry_alignment(block, data, subject_registry, errors, warnings)
    props = data.get("道具")
    if isinstance(props, list):
        normalized_props: dict[str, str] = {}
        duplicates: list[str] = []
        for prop in props:
            normalized = normalize_yaml_subject_entry(prop)
            if not normalized:
                continue
            if normalized in normalized_props:
                duplicates.append(normalized)
            else:
                normalized_props[normalized] = normalized
        if duplicates:
            unique_duplicates = sorted(set(duplicates))
            warnings.append(
                f"line {block.line_number}: {block.group_id} yaml 道具 contains exact duplicate names {unique_duplicates}; statistics review should merge repeated props and check same-object aliases"
            )


def normalize_yaml_subject_entry(entry: object) -> str:
    if isinstance(entry, dict):
        subject_id = str(entry.get("id") or "").strip()
        subject_name = str(entry.get("name") or entry.get("canonical_name") or "").strip()
        if subject_id and subject_name:
            return f"{subject_id}:{subject_name}"
        return subject_id or subject_name
    return str(entry).strip()


def validate_yaml_subject_registry_alignment(
    block: GroupBlock,
    data: dict[str, object],
    subject_registry: SubjectRegistry,
    errors: list[str],
    warnings: list[str],
) -> None:
    for yaml_key, (_registry_key, expected_prefix) in YAML_SUBJECT_KEYS.items():
        values = data.get(yaml_key)
        if values is None:
            continue
        if not isinstance(values, list):
            continue
        for index, value in enumerate(values, start=1):
            if not isinstance(value, dict):
                errors.append(
                    f"line {block.line_number}: {block.group_id} yaml {yaml_key}[{index}] must be a mapping with id/name when --subject-registry-yaml is used"
                )
                continue
            subject_id = str(value.get("id") or "").strip()
            subject_name = str(value.get("name") or value.get("canonical_name") or "").strip()
            if not subject_id or not subject_name:
                errors.append(
                    f"line {block.line_number}: {block.group_id} yaml {yaml_key}[{index}] must contain id and name"
                )
                continue
            if not subject_id.startswith(expected_prefix):
                errors.append(
                    f"line {block.line_number}: {block.group_id} yaml {yaml_key}[{index}] id {subject_id} must start with {expected_prefix}"
                )
            canonical_name = subject_registry.canonical_name(yaml_key, subject_id)
            if canonical_name is None:
                errors.append(
                    f"line {block.line_number}: {block.group_id} yaml {yaml_key}[{index}] id {subject_id} is not registered in subject registry"
                )
                continue
            if subject_name != canonical_name:
                errors.append(
                    f"line {block.line_number}: {block.group_id} yaml {yaml_key}[{index}] name {subject_name!r} does not match registry canonical_name {canonical_name!r}"
                )


def validate_connectors(
    path: Path,
    text: str,
    groups: list[GroupBlock],
    connectors: list[ConnectorBlock],
    errors: list[str],
) -> None:
    for connector in connectors:
        prefix = f"{display_path(path)}:{connector.line_number}: connector {connector.connector_id}"
        errors.append(f"{prefix} inter-group connector blocks are deprecated; remove ## A~B connector design sections")


def validate_file(path: Path, subject_registry: SubjectRegistry | None = None) -> ValidationResult:
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

    if LEGACY_CONNECTOR_HEADING_RE.search(text):
        errors.append(f"{display_path(path)}: legacy connector sections are deprecated; remove 组间连接件 blocks")

    previous_by_scene: dict[int, int] = {}

    for group_index, group in enumerate(groups):
        prefix = f"{display_path(path)}:{group.line_number}: {group.group_id}"
        if expected_episode is not None and group.episode != expected_episode:
            errors.append(f"{prefix} episode segment does not match 第{expected_episode}集")

        for label in DEPRECATED_GROUP_LABELS:
            if label in group.body:
                errors.append(f"{prefix} must not use deprecated group label {label}")
        if STORYBOARD_PICTURE_LABEL in group.body:
            errors.append(
                f"{prefix} must inherit original visual field titles from 7-摄影 and must not introduce standalone {STORYBOARD_PICTURE_LABEL}"
            )

        leading_scene_title = extract_leading_scene_title(group.body)
        leading_scene_numbers = extract_scene_title_numbers(leading_scene_title)
        leading_lines = nonempty_lines_after_heading(group.body)
        if not leading_scene_title or not is_scene_title_line(leading_scene_title):
            errors.append(f"{prefix} must start with a scene title line before {GLOBAL_STYLE_LABEL}")
        elif CONNECTOR_SCENE_ARROW in leading_scene_title:
            errors.append(f"{prefix} group scene title must contain exactly one scene title, not a transition")
        elif leading_scene_numbers[:1] != [group.scene]:
            errors.append(f"{prefix} scene title must start with 场景{group.scene}")
        if len(leading_lines) < 2 or leading_lines[1][1] != GLOBAL_STYLE_LABEL:
            errors.append(
                f"{prefix} must include standalone {GLOBAL_STYLE_LABEL} immediately after the scene title line"
            )
        validate_global_style(prefix, group.body, errors)

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

        yaml_index = first_fenced_yaml_line_index(group.body)
        head_without_yaml = group.body
        if yaml_index is not None:
            head_without_yaml = "\n".join(group.body.splitlines()[:yaml_index])
        prohibited_labels = PROHIBITED_GROUP_SUBJECT_LABEL_RE.findall(head_without_yaml)
        if prohibited_labels:
            errors.append(
                f"{prefix} group head must integrate subject info into prose fields, not use structured labels {sorted(set(prohibited_labels))}"
            )

        countable_text = strip_group_non_body_sections(group.body)
        char_count = estimate_chars(countable_text)
        legacy_duration_matches = list(LEGACY_SHOT_DURATION_RE.finditer(countable_text))
        if legacy_duration_matches:
            errors.append(
                f"{prefix} contains legacy 分镜N（约X秒） durations; return to source owner and migrate to explicit 分镜N（N-N秒） or [N-N秒] time ranges"
            )
        duration_seconds = estimate_duration_seconds(countable_text)
        validate_group_baseline_ranges(prefix, countable_text, errors)
        if duration_seconds == 0:
            warnings.append(
                f"{prefix} contains no 分镜N（N-N秒） or [N-N秒] time ranges; semantic review should restore canonical timing or declare source_override/direct_screenplay timecode planning"
            )
        else:
            if duration_seconds < MIN_REVIEW_SECONDS:
                warnings.append(
                    f"{prefix} estimated group duration {duration_seconds:g}s is below review floor {MIN_REVIEW_SECONDS:g}s; semantic review must justify a short-scene exception or rebalance complete atomic units"
                )
            if not ends_on_half_second(duration_seconds):
                errors.append(
                    f"{prefix} estimated group duration {duration_seconds:g}s must end on .5s; if the natural sum does not end on .5s, add 0.5s to the final group end time"
                )
            if duration_seconds > MAX_REVIEW_SECONDS:
                errors.append(
                    f"{prefix} estimated group duration {duration_seconds:g}s exceeds hard max {MAX_REVIEW_SECONDS:g}s; split/rebalance complete atomic units or return to source owner to repair an overlong atomic unit"
                )
        if char_count > TARGET_CHAR_COUNT:
            warnings.append(
                f"{prefix} estimated scene-title-plus-body char count {char_count} exceeds review target {TARGET_CHAR_COUNT}; semantic review must justify keeping this dense group, but char count is not a hard failure"
            )
        if char_count < MIN_REVIEW_CHAR_COUNT:
            warnings.append(
                f"{prefix} estimated scene-title-plus-body char count {char_count} is below review floor {MIN_REVIEW_CHAR_COUNT}; semantic review must justify a short-scene exception or rebalance complete atomic units"
            )

        validate_yaml_stats(group, char_count, duration_seconds, errors, warnings, subject_registry)

    validate_connectors(path, text, groups, connectors, errors)

    return ValidationResult(errors=errors, warnings=warnings)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("path", help="A storyboard group Markdown file or directory")
    parser.add_argument(
        "--subject-registry-yaml",
        help="Optional projects/aigc/<项目名>/3-主体/subject-registry.yaml used to validate YAML role/scene/prop id/name alignment",
    )
    args = parser.parse_args()

    target = Path(args.path)
    setup_errors: list[str] = []
    subject_registry = load_subject_registry(
        Path(args.subject_registry_yaml) if args.subject_registry_yaml else None,
        setup_errors,
    )
    files = discover_files(target)
    if not files:
        print(f"No files found: {display_path(target)}")
        return 1

    errors: list[str] = setup_errors
    warnings: list[str] = []
    for file_path in files:
        result = validate_file(file_path, subject_registry)
        errors.extend(result.errors)
        warnings.extend(result.warnings)

    print("AIGC storyboard group validation")
    print(f"target: {display_path(target)}")
    if args.subject_registry_yaml:
        print(f"subject_registry: {display_path(Path(args.subject_registry_yaml))}")
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
