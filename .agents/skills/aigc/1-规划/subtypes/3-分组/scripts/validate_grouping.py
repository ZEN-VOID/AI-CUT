#!/usr/bin/env python3
"""Validate aigc planning grouping markdown outputs."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from xml.etree import ElementTree as ET
from zipfile import ZipFile


EPISODE_FILE_RE = re.compile(r"^第0*(?P<ep>\d+)集\.md$")
FORBIDDEN_GROUP_FILE_RE = re.compile(r"^第0*(?P<group>\d+)组\.md$")
GROUP_HEADING_RE = re.compile(r"^##\s+(G\d+)\b")

GROUP_PLAN_REQUIRED = [
    "# 分组总览",
    "## 分组目标",
    "## 边界裁决摘要",
    "## 量化摘要",
    "## 集级总览表",
]
GROUP_PLAN_TABLE_HEADER = "| episode | grouping_method | duration_policy | pace_tier | episode_load_score | recommended_group_band | group_count | grouping_focus | downstream_entry | dependency_note |"

REPORT_REQUIRED = [
    "# 分组执行报告",
    "## 输入清单",
    "## 边界裁决摘要",
    "## 量化摘要",
    "## 集级边界继承检查",
    "## 候选边界",
    "## 集内分组表",
    "## 依赖与并行性检查",
    "## 验收结论与返工项",
]

EPISODE_REQUIRED_SECTIONS = [
    "## 本集分组目标",
    "## 分组计划表",
]
GROUP_TABLE_HEADER = "| group_id | group_name | source_span | structure_anchor | preset_anchor_policy | preset_anchor_ids | estimated_duration_seconds | effective_text_chars | window_status | group_unit_count | group_turning_point_count | group_dependency_count | group_load_score | dependency_note | parallelism | downstream_entry | boundary_reason |"
GROUP_SUBSECTIONS = [
    "### 组目标",
    "### 组内容范围",
    "### 结构锚点",
    "### 外部分镜锚点",
    "### 量化指标",
    "### 交接约束",
    "### 依赖与并行性",
    "### 下游建议",
]
GROUPING_METHOD = "multidimensional_quantized"
ALLOWED_PACE_TIERS = {"慢节奏", "中节奏", "快节奏"}
ALLOWED_WINDOW_STATUS = {"ok", "warn-low", "warn-high", "error"}
ALLOWED_PRESET_MODES = {"standard", "preserve_and_extend", "preserve_only"}
ALLOWED_PRESET_POLICIES = {"inherit", "split-soft-lock", "reference-only", "none"}
DURATION_TEXT_RE = re.compile(r"^(?P<seconds>\d+)秒$")
SHOT_SPAN_RE = re.compile(r"镜\s*(?P<start>\d+)(?:\s*-\s*(?P<end>\d+))?")
SHOT_HEADING_RE = re.compile(r"^(?:####\s*)?镜号?\s*(?P<shot>\d+)\s*$")
PRIMARY_SOURCE_BLOCK_RE = re.compile(r"(?ms)^primary_story_source:\s*\n(?P<body>(?:^[ \t].*\n)+)")
SUPPORTED_SOURCE_BACKED_TYPES = {"storyboard_script", "hybrid_story_text"}
PACE_COEFFICIENTS = {
    "慢节奏": 0.7,
    "中节奏": 1.0,
    "快节奏": 1.3,
}
STORY_META_LABELS = {"场景", "环境", "景别", "音效", "时长"}
STORY_ACTION_LABELS = {"画面", "全景", "中景", "近景", "特写", "正反打", "交叉切", "转场"}


def fail(message: str) -> int:
    print(message, file=sys.stderr)
    return 1


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def read_docx_lines(path: Path) -> list[str]:
    ns = {"w": "http://schemas.openxmlformats.org/wordprocessingml/2006/main"}
    with ZipFile(path) as archive:
        xml = archive.read("word/document.xml")
    root = ET.fromstring(xml)
    lines: list[str] = []
    for para in root.findall(".//w:p", ns):
        texts = [node.text or "" for node in para.findall(".//w:t", ns)]
        line = "".join(texts).strip()
        if line:
            lines.append(line)
    return lines


def read_story_source_lines(path: Path) -> list[str]:
    if path.suffix.lower() == ".docx":
        return read_docx_lines(path)
    return read_text(path).splitlines()


def require_markers(path: Path, text: str, markers: list[str], errors: list[str]) -> None:
    for marker in markers:
        if marker not in text:
            errors.append(f"{path}: 缺少必需区块 `{marker}`。")


def count_table_rows(text: str, header: str) -> int | None:
    lines = text.splitlines()
    for index, line in enumerate(lines):
        if line.strip() != header:
            continue
        if index + 1 >= len(lines) or not lines[index + 1].strip().startswith("| ---"):
            return None
        row_count = 0
        cursor = index + 2
        while cursor < len(lines):
            current = lines[cursor].strip()
            if not current.startswith("|"):
                break
            row_count += 1
            cursor += 1
        return row_count
    return None


def parse_table_rows(text: str, header: str) -> list[dict[str, str]] | None:
    lines = text.splitlines()
    for index, line in enumerate(lines):
        if line.strip() != header:
            continue
        if index + 1 >= len(lines) or not lines[index + 1].strip().startswith("| ---"):
            return None
        columns = [col.strip() for col in header.strip().strip("|").split("|")]
        rows: list[dict[str, str]] = []
        cursor = index + 2
        while cursor < len(lines):
            current = lines[cursor].strip()
            if not current.startswith("|"):
                break
            values = [value.strip() for value in current.strip().strip("|").split("|")]
            if len(values) != len(columns):
                return None
            rows.append(dict(zip(columns, values)))
            cursor += 1
        return rows
    return None


def parse_duration_text(value: str) -> int | None:
    match = DURATION_TEXT_RE.match(value.strip())
    if not match:
        return None
    return int(match.group("seconds"))


def strip_wrapping_quotes(value: str) -> str:
    stripped = value.strip()
    if len(stripped) >= 2 and stripped[0] == stripped[-1] and stripped[0] in {'"', "'"}:
        return stripped[1:-1]
    return stripped


def normalized_char_count(value: str) -> int:
    return len(re.sub(r"\s+", "", value))


def compute_text_windows(duration_seconds: int, pace_tier: str) -> tuple[int, int, int, int]:
    base = round(duration_seconds * 10 * PACE_COEFFICIENTS[pace_tier])
    warn_low = round(base * 0.8)
    warn_high = round(base * 1.0)
    hard = round(base * 1.1)
    return base, warn_low, warn_high, hard


def expected_window_status(effective_text_chars: int, duration_seconds: int, pace_tier: str) -> str:
    _, warn_low, warn_high, hard = compute_text_windows(duration_seconds, pace_tier)
    if effective_text_chars > hard:
        return "error"
    if effective_text_chars > warn_high:
        return "warn-high"
    if effective_text_chars < warn_low:
        return "warn-low"
    return "ok"


def find_project_root(start_path: Path) -> Path | None:
    current = start_path.resolve()
    for candidate in [current, *current.parents]:
        if (candidate / "Init" / "story-source-manifest.yaml").exists():
            return candidate
    return None


def load_primary_story_source(project_root: Path) -> dict[str, str] | None:
    manifest_path = project_root / "Init" / "story-source-manifest.yaml"
    if not manifest_path.exists():
        return None
    text = read_text(manifest_path)
    match = PRIMARY_SOURCE_BLOCK_RE.search(text)
    if not match:
        return None
    body = match.group("body")
    result: dict[str, str] = {}
    for field in ("status", "source_type", "path"):
        field_match = re.search(rf"^\s+{field}:\s*\"?(?P<value>[^\"\n]+)\"?\s*$", body, re.M)
        if field_match:
            result[field] = field_match.group("value").strip()
    if {"status", "source_type", "path"} - set(result):
        return None
    return result


def projected_char_weight(content: str, mode: str, pace_tier: str) -> float:
    if not content or content == "无":
        return 0.0
    chars = normalized_char_count(content)
    if mode == "voice_text":
        return float(chars)
    if mode == "voice_visual":
        return 0.0
    return chars * PACE_COEFFICIENTS[pace_tier]


def split_storyboard_blocks(lines: list[str]) -> list[tuple[int, list[str]]]:
    blocks: list[tuple[int, list[str]]] = []
    current_shot: int | None = None
    current_lines: list[str] = []
    for raw_line in lines:
        line = raw_line.strip()
        match = SHOT_HEADING_RE.match(line)
        if match:
            if current_shot is not None:
                blocks.append((current_shot, current_lines))
            current_shot = int(match.group("shot"))
            current_lines = []
            continue
        if current_shot is not None and line:
            current_lines.append(line)
    if current_shot is not None:
        blocks.append((current_shot, current_lines))
    return blocks


def parse_markdown_storyboard_block(lines: list[str], pace_tier: str) -> int:
    result: dict[int, int] = {}
    total = 0.0
    current_mode = "action_visual"
    for raw_line in lines:
        if not raw_line.strip():
            continue
        stripped = raw_line.strip()
        if not stripped.startswith("- "):
            continue

        indent = len(raw_line) - len(raw_line.lstrip(" "))
        payload = stripped[2:].strip()
        if indent > 0:
            nested_content = payload.split("：", 1)[1].strip() if "：" in payload else payload
            total += projected_char_weight(nested_content, current_mode, pace_tier)
            continue

        label, content = (payload.split("：", 1) + [""])[:2]
        label = label.strip()
        content = content.strip()

        if label in {"台词", "闪回台词", "回到现实台词"}:
            current_mode = "voice_text"
            total += projected_char_weight(content, current_mode, pace_tier)
            continue
        if re.fullmatch(r"(对白|独白|内心独白|旁白)(（.*?）)?", label):
            current_mode = "voice_text"
            total += projected_char_weight(content, current_mode, pace_tier)
            continue
        if label in {"对白画面", "独白画面", "内心独白画面", "旁白画面"}:
            current_mode = "voice_visual"
            total += projected_char_weight(content, current_mode, pace_tier)
            continue

        current_mode = "action_visual"
        total += projected_char_weight(content, current_mode, pace_tier)
    return round(total)


def classify_plain_story_label(label: str) -> str:
    base = re.sub(r"（.*?）", "", label).strip()
    if base in STORY_META_LABELS:
        return "meta"
    if base in STORY_ACTION_LABELS:
        return "action_visual"
    if base in {"对白画面", "独白画面", "内心独白画面", "旁白画面"}:
        return "voice_visual"
    if base in {"对白", "独白", "内心独白", "旁白", "台词"}:
        return "voice_text"
    if re.fullmatch(r".{1,20}", base):
        return "voice_text"
    return "action_visual"


def parse_plain_storyboard_block(lines: list[str], pace_tier: str) -> int:
    text = "\n".join(lines)
    total = 0.0
    segment_matches = list(re.finditer(r"(?P<label>[^：\n]{1,30})：", text))
    if not segment_matches:
        return round(projected_char_weight(text, "action_visual", pace_tier))

    for index, match in enumerate(segment_matches):
        label = match.group("label").strip()
        start = match.end()
        end = segment_matches[index + 1].start() if index + 1 < len(segment_matches) else len(text)
        content = text[start:end].strip(" \n")
        if not content:
            continue
        mode = classify_plain_story_label(label)
        if mode == "meta":
            continue
        total += projected_char_weight(content, mode, pace_tier)
    return round(total)


def parse_storyboard_source_effective_chars(source_path: Path, pace_tier: str) -> dict[int, int]:
    lines = read_story_source_lines(source_path)
    blocks = split_storyboard_blocks(lines)
    result: dict[int, int] = {}
    for shot_id, block_lines in blocks:
        if any(line.strip().startswith("- ") for line in block_lines):
            result[shot_id] = parse_markdown_storyboard_block(block_lines, pace_tier)
        else:
            result[shot_id] = parse_plain_storyboard_block(block_lines, pace_tier)
    return result


def parse_shot_ranges(source_span: str) -> list[tuple[int, int]]:
    ranges: list[tuple[int, int]] = []
    for match in SHOT_SPAN_RE.finditer(source_span):
        start = int(match.group("start"))
        end = int(match.group("end") or start)
        if end < start:
            start, end = end, start
        ranges.append((start, end))
    return ranges


def source_backed_effective_chars(
    source_span: str,
    shot_effective_chars: dict[int, int],
) -> tuple[int | None, str | None]:
    ranges = parse_shot_ranges(source_span)
    if not ranges:
        return None, "source_span 不是可机读的镜号范围"
    total = 0
    for start, end in ranges:
        for shot_id in range(start, end + 1):
            if shot_id not in shot_effective_chars:
                return None, f"故事主源中缺少镜号 {shot_id}"
            total += shot_effective_chars[shot_id]
    return total, None


def parse_frontmatter(path: Path, text: str, errors: list[str]) -> dict[str, str] | None:
    lines = text.splitlines()
    if len(lines) < 3 or lines[0].strip() != "---":
        errors.append(f"{path}: 缺少 YAML frontmatter。")
        return None

    frontmatter: dict[str, str] = {}
    closing_index = None
    for index in range(1, len(lines)):
        if lines[index].strip() == "---":
            closing_index = index
            break
        if ":" not in lines[index]:
            errors.append(f"{path}: frontmatter 行格式非法：{lines[index]!r}")
            continue
        key, value = lines[index].split(":", 1)
        frontmatter[key.strip()] = value.strip()

    if closing_index is None:
        errors.append(f"{path}: frontmatter 未正常闭合。")
        return None
    return frontmatter


def validate_group_plan(path: Path, errors: list[str]) -> None:
    text = read_text(path)
    require_markers(path, text, GROUP_PLAN_REQUIRED, errors)
    row_count = count_table_rows(text, GROUP_PLAN_TABLE_HEADER)
    if row_count is None:
        errors.append(f"{path}: 集级总览表表头或分隔线不符合模板合同。")
    elif row_count < 1:
        errors.append(f"{path}: 集级总览表至少需要一行数据。")


def validate_report(path: Path, errors: list[str]) -> None:
    text = read_text(path)
    require_markers(path, text, REPORT_REQUIRED, errors)
    require_markers(
        path,
        text,
        [
            "- 默认组时长:",
            "- 分镜组时长映射:",
            "- 分镜时间读取链:",
        ],
        errors,
    )
    row_count = count_table_rows(text, "| episode | group_id | group_name | effective_text_chars | window_status | group_load_score | dependency | parallelism | note |")
    if row_count is None:
        errors.append(f"{path}: `集内分组表` 表头或分隔线不符合模板合同。")
    elif row_count < 1:
        errors.append(f"{path}: `集内分组表` 至少需要一行数据。")


def validate_episode(path: Path, errors: list[str]) -> None:
    text = read_text(path)
    frontmatter = parse_frontmatter(path, text, errors)
    if not frontmatter:
        return

    required_keys = {
        "project",
        "episode",
        "grouping_method",
        "source_span",
        "group_count",
        "scene_unit_count",
        "duration_policy",
        "默认组时长",
        "分镜组时长映射",
        "时长偏离证据",
        "外部分镜预设模式",
        "外部分镜锚点登记",
        "pace_tier",
        "base_text_window",
        "warn_window",
        "hard_text_window",
        "structure_unit_count",
        "turning_point_count",
        "hard_dependency_count",
        "episode_load_score",
        "recommended_group_band",
    }
    missing = sorted(required_keys - set(frontmatter))
    if missing:
        errors.append(f"{path}: frontmatter 缺少字段 {', '.join(missing)}。")
        return

    filename_match = EPISODE_FILE_RE.match(path.name)
    if not filename_match:
        errors.append(f"{path}: 文件名必须符合 `第N集.md`。")
        return

    episode_label = f"第{int(filename_match.group('ep'))}集"
    if frontmatter["episode"] != episode_label:
        errors.append(f"{path}: frontmatter `episode` 与文件名不一致。")

    if frontmatter["grouping_method"] != GROUPING_METHOD:
        errors.append(f"{path}: `grouping_method` 必须是 `{GROUPING_METHOD}`。")

    if not frontmatter["group_count"].isdigit() or int(frontmatter["group_count"]) <= 0:
        errors.append(f"{path}: `group_count` 必须是正整数。")
        return
    group_count = int(frontmatter["group_count"])

    source_backed_story: dict[int, int] | None = None
    source_backed_type: str | None = None
    project_root = find_project_root(path.parent)
    if project_root is not None:
        primary_story_source = load_primary_story_source(project_root)
        if (
            primary_story_source
            and primary_story_source.get("status") == "ready"
            and primary_story_source.get("source_type") in SUPPORTED_SOURCE_BACKED_TYPES
        ):
            source_path = project_root / primary_story_source["path"]
            source_backed_type = primary_story_source["source_type"]
            if not source_path.exists():
                errors.append(f"{path}: 主故事源 `{source_path}` 不存在，无法回算 `effective_text_chars`。")
            else:
                source_backed_story = parse_storyboard_source_effective_chars(source_path, frontmatter["pace_tier"])

    for key in (
        "scene_unit_count",
        "base_text_window",
        "hard_text_window",
        "structure_unit_count",
        "turning_point_count",
        "hard_dependency_count",
        "episode_load_score",
    ):
        if not frontmatter[key].isdigit():
            errors.append(f"{path}: `{key}` 必须是非负整数。")

    if not frontmatter["duration_policy"]:
        errors.append(f"{path}: `duration_policy` 不得为空。")

    default_group_duration = parse_duration_text(frontmatter["默认组时长"])
    if default_group_duration is None or default_group_duration <= 0:
        errors.append(f"{path}: `默认组时长` 必须形如 `15秒`，且为正整数秒。")

    raw_duration_map = strip_wrapping_quotes(frontmatter["分镜组时长映射"])
    try:
        duration_overrides = json.loads(raw_duration_map)
    except json.JSONDecodeError as exc:
        errors.append(f"{path}: `分镜组时长映射` 必须是合法 JSON 对象字符串：{exc.msg}。")
        duration_overrides = None

    parsed_duration_overrides: dict[str, int] = {}
    if duration_overrides is not None:
        if not isinstance(duration_overrides, dict):
            errors.append(f"{path}: `分镜组时长映射` 必须解析为 JSON 对象。")
        else:
            for group_id, duration_text in duration_overrides.items():
                if not isinstance(group_id, str) or not group_id.strip():
                    errors.append(f"{path}: `分镜组时长映射` 的组键必须是非空字符串。")
                    continue
                if not isinstance(duration_text, str):
                    errors.append(f"{path}: `分镜组时长映射[{group_id}]` 必须是形如 `10秒` 的字符串。")
                    continue
                parsed_seconds = parse_duration_text(duration_text)
                if parsed_seconds is None or parsed_seconds <= 0:
                    errors.append(f"{path}: `分镜组时长映射[{group_id}]` 必须形如 `10秒`，且为正整数秒。")
                    continue
                if default_group_duration is not None and parsed_seconds == default_group_duration:
                    errors.append(f"{path}: `分镜组时长映射[{group_id}]` 与 `默认组时长` 相同；映射中只应登记偏离默认值的组。")
                    continue
                parsed_duration_overrides[group_id] = parsed_seconds

    raw_duration_evidence = strip_wrapping_quotes(frontmatter["时长偏离证据"])
    try:
        duration_override_evidence = json.loads(raw_duration_evidence)
    except json.JSONDecodeError as exc:
        errors.append(f"{path}: `时长偏离证据` 必须是合法 JSON 数组字符串：{exc.msg}。")
        duration_override_evidence = None
    if duration_override_evidence is not None:
        if not isinstance(duration_override_evidence, list):
            errors.append(f"{path}: `时长偏离证据` 必须解析为 JSON 数组。")
            duration_override_evidence = None
        else:
            for item in duration_override_evidence:
                if not isinstance(item, str) or not item.strip():
                    errors.append(f"{path}: `时长偏离证据` 只能包含非空字符串。")
                    break
    if parsed_duration_overrides and not duration_override_evidence:
        errors.append(f"{path}: 存在 `分镜组时长映射` 偏离，但缺少非空 `时长偏离证据`。")
    if not parsed_duration_overrides and duration_override_evidence:
        errors.append(f"{path}: `分镜组时长映射` 为空时，`时长偏离证据` 也必须为空数组。")

    if frontmatter["pace_tier"] not in ALLOWED_PACE_TIERS:
        errors.append(f"{path}: `pace_tier` 必须是 {sorted(ALLOWED_PACE_TIERS)} 之一。")

    if frontmatter["外部分镜预设模式"] not in ALLOWED_PRESET_MODES:
        errors.append(f"{path}: `外部分镜预设模式` 必须是 {sorted(ALLOWED_PRESET_MODES)} 之一。")

    raw_anchor_registry = strip_wrapping_quotes(frontmatter["外部分镜锚点登记"])
    try:
        anchor_registry = json.loads(raw_anchor_registry)
    except json.JSONDecodeError as exc:
        errors.append(f"{path}: `外部分镜锚点登记` 必须是合法 JSON 数组字符串：{exc.msg}。")
        anchor_registry = None

    known_anchor_ids: set[str] = set()
    if anchor_registry is not None:
        if not isinstance(anchor_registry, list):
            errors.append(f"{path}: `外部分镜锚点登记` 必须解析为 JSON 数组。")
        else:
            for item in anchor_registry:
                if not isinstance(item, dict) or not isinstance(item.get("anchor_id"), str) or not item["anchor_id"].strip():
                    errors.append(f"{path}: `外部分镜锚点登记` 的每一项都必须包含非空 `anchor_id`。")
                    continue
                known_anchor_ids.add(item["anchor_id"].strip())

    if not re.match(r"^\d+-\d+$", frontmatter["warn_window"]):
        errors.append(f"{path}: `warn_window` 必须形如 `120-180`。")

    if not re.match(r"^\d+-\d+$", frontmatter["recommended_group_band"]):
        errors.append(f"{path}: `recommended_group_band` 必须形如 `2-3`。")

    require_markers(path, text, EPISODE_REQUIRED_SECTIONS, errors)
    row_count = count_table_rows(text, GROUP_TABLE_HEADER)
    if row_count is None:
        errors.append(f"{path}: `分组计划表` 表头或分隔线不符合模板合同。")
        return
    if row_count != group_count:
        errors.append(f"{path}: `group_count={group_count}` 与分组计划表行数 `{row_count}` 不一致。")

    plan_rows = parse_table_rows(text, GROUP_TABLE_HEADER)
    if plan_rows is None:
        errors.append(f"{path}: `分组计划表` 数据行解析失败。")
        plan_rows = []

    seen_group_ids = set()
    plan_rows_by_group_id: dict[str, dict[str, str]] = {}
    for row in plan_rows:
        group_id = row["group_id"]
        seen_group_ids.add(group_id)
        plan_rows_by_group_id[group_id] = row
        if row["preset_anchor_policy"] not in ALLOWED_PRESET_POLICIES:
            errors.append(
                f"{path}: `分组计划表` 中 `{group_id}` 的 `preset_anchor_policy` 必须是 {sorted(ALLOWED_PRESET_POLICIES)} 之一。"
            )
        try:
            preset_anchor_ids = json.loads(row["preset_anchor_ids"])
        except json.JSONDecodeError as exc:
            errors.append(f"{path}: `{group_id}` 的 `preset_anchor_ids` 必须是合法 JSON 数组字符串：{exc.msg}。")
            preset_anchor_ids = []
        if not isinstance(preset_anchor_ids, list):
            errors.append(f"{path}: `{group_id}` 的 `preset_anchor_ids` 必须解析为数组。")
            preset_anchor_ids = []
        for anchor_id in preset_anchor_ids:
            if not isinstance(anchor_id, str) or not anchor_id.strip():
                errors.append(f"{path}: `{group_id}` 的 `preset_anchor_ids` 只能包含非空字符串。")
                continue
            if known_anchor_ids and anchor_id not in known_anchor_ids:
                errors.append(f"{path}: `{group_id}` 引用了未登记的锚点 `{anchor_id}`。")
        estimated_duration = row["estimated_duration_seconds"]
        if not estimated_duration.isdigit() or int(estimated_duration) <= 0:
            errors.append(f"{path}: `分组计划表` 中 `{group_id}` 的 `estimated_duration_seconds` 必须是正整数。")
            continue
        effective_text_chars = row["effective_text_chars"]
        if not effective_text_chars.isdigit() or int(effective_text_chars) < 0:
            errors.append(f"{path}: `分组计划表` 中 `{group_id}` 的 `effective_text_chars` 必须是非负整数。")
            continue
        computed_effective: int | None = None
        if source_backed_story is not None:
            computed_effective, source_error = source_backed_effective_chars(row["source_span"], source_backed_story)
            if source_error:
                errors.append(
                    f"{path}: `分组计划表` 中 `{group_id}` 命中 `{source_backed_type}` 主源回算路径，但 {source_error}；"
                    "请把 `source_span` 写成如 `镜1-5` 的可机读范围。"
                )
            elif computed_effective != int(effective_text_chars):
                errors.append(
                    f"{path}: `分组计划表` 中 `{group_id}` 的 `effective_text_chars={effective_text_chars}` "
                    f"与故事主源回算值 `{computed_effective}` 不一致。"
                )
        window_status = row["window_status"]
        if window_status not in ALLOWED_WINDOW_STATUS:
            errors.append(
                f"{path}: `分组计划表` 中 `{group_id}` 的 `window_status` 必须是 {sorted(ALLOWED_WINDOW_STATUS)} 之一。"
            )
        else:
            expected_status = expected_window_status(
                computed_effective if computed_effective is not None else int(effective_text_chars),
                int(estimated_duration),
                frontmatter["pace_tier"],
            )
            if window_status != expected_status:
                _, warn_low, warn_high, hard = compute_text_windows(int(estimated_duration), frontmatter["pace_tier"])
                errors.append(
                    f"{path}: `分组计划表` 中 `{group_id}` 的量化状态不一致："
                    f"`effective_text_chars={effective_text_chars}`、`estimated_duration_seconds={estimated_duration}`、"
                    f"`pace_tier={frontmatter['pace_tier']}` 时应为 `{expected_status}`，当前写为 `{window_status}` "
                    f"（warn={warn_low}-{warn_high}, hard={hard}）。"
                )
            if window_status != "ok":
                errors.append(
                    f"{path}: `分组计划表` 中 `{group_id}` 的 `window_status={window_status}` 未通过严格 gate；"
                    "正式 `第N集.md` 只允许 `ok` 落盘。"
                )
        if default_group_duration is None:
            continue
        resolved_duration = parsed_duration_overrides.get(group_id, default_group_duration)
        if int(estimated_duration) != resolved_duration:
            errors.append(
                f"{path}: `{group_id}` 的 `estimated_duration_seconds={estimated_duration}` 与组时长基线 `{resolved_duration}` 秒不一致。"
            )

    for group_id in sorted(parsed_duration_overrides):
        if group_id not in seen_group_ids:
            errors.append(f"{path}: `分镜组时长映射` 中的 `{group_id}` 未在 `分组计划表` 中出现。")

    lines = text.splitlines()
    group_indices = [index for index, line in enumerate(lines) if GROUP_HEADING_RE.match(line.strip())]
    if len(group_indices) != group_count:
        errors.append(f"{path}: 组级章节数量 `{len(group_indices)}` 与 `group_count={group_count}` 不一致。")
        return

    for idx, start in enumerate(group_indices):
        end = group_indices[idx + 1] if idx + 1 < len(group_indices) else len(lines)
        block = "\n".join(lines[start:end])
        group_match = GROUP_HEADING_RE.match(lines[start].strip())
        block_group_id = group_match.group(1) if group_match else None
        for subsection in GROUP_SUBSECTIONS:
            if subsection not in block:
                errors.append(f"{path}: `{lines[start].strip()}` 缺少必需子区块 `{subsection}`。")
        for required_line in (
            "- estimated_duration_seconds:",
            "- effective_text_chars:",
            "- window_status:",
        ):
            if required_line not in block:
                errors.append(f"{path}: `{lines[start].strip()}` 缺少量化字段 `{required_line}`。")
        status_match = re.search(r"window_status:\s*([A-Za-z-]+)", block)
        if status_match and status_match.group(1) not in ALLOWED_WINDOW_STATUS:
            errors.append(
                f"{path}: `{lines[start].strip()}` 的 `window_status` 必须是 {sorted(ALLOWED_WINDOW_STATUS)} 之一。"
            )
        if not block_group_id or block_group_id not in plan_rows_by_group_id:
            continue
        plan_row = plan_rows_by_group_id[block_group_id]
        duration_match = re.search(r"estimated_duration_seconds:\s*(\d+)", block)
        effective_match = re.search(r"effective_text_chars:\s*(\d+)", block)
        if duration_match and duration_match.group(1) != plan_row["estimated_duration_seconds"]:
            errors.append(
                f"{path}: `{block_group_id}` 组章节中的 `estimated_duration_seconds={duration_match.group(1)}` "
                f"与 `分组计划表` 中的 `{plan_row['estimated_duration_seconds']}` 不一致。"
            )
        if effective_match and effective_match.group(1) != plan_row["effective_text_chars"]:
            errors.append(
                f"{path}: `{block_group_id}` 组章节中的 `effective_text_chars={effective_match.group(1)}` "
                f"与 `分组计划表` 中的 `{plan_row['effective_text_chars']}` 不一致。"
            )
        if status_match and status_match.group(1) != plan_row["window_status"]:
            errors.append(
                f"{path}: `{block_group_id}` 组章节中的 `window_status={status_match.group(1)}` "
                f"与 `分组计划表` 中的 `{plan_row['window_status']}` 不一致。"
            )
        if status_match and status_match.group(1) != "ok":
            errors.append(
                f"{path}: `{block_group_id}` 组章节中的 `window_status={status_match.group(1)}` 未通过严格 gate；"
                "正式 `第N集.md` 只允许 `ok` 落盘。"
            )


def collect_episode_files(input_path: Path) -> list[Path]:
    return sorted(
        path
        for path in input_path.iterdir()
        if path.is_file() and EPISODE_FILE_RE.match(path.name)
    )


def validate_directory(input_path: Path) -> list[str]:
    errors: list[str] = []

    if not input_path.exists():
        return [f"输入路径不存在：{input_path}"]
    if not input_path.is_dir():
        return [f"输入路径必须是目录：{input_path}"]

    forbidden = sorted(
        path for path in input_path.iterdir() if path.is_file() and FORBIDDEN_GROUP_FILE_RE.match(path.name)
    )
    if forbidden:
        errors.append(f"{input_path}: 不允许存在独立组文件：{', '.join(path.name for path in forbidden)}。")

    group_plan = input_path / "group-plan.md"
    report = input_path / "执行报告.md"
    if group_plan.exists():
        validate_group_plan(group_plan, errors)
    if report.exists():
        validate_report(report, errors)

    episode_files = collect_episode_files(input_path)
    if not episode_files:
        errors.append(f"{input_path}: 至少需要一个 `第N集.md`。")
    for episode_file in episode_files:
        validate_episode(episode_file, errors)

    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description="校验 3-分组 输出契约")
    parser.add_argument(
        "--input",
        required=True,
        help="输入目录，通常为 projects/<项目名>/规划/3-分组",
    )
    args = parser.parse_args()

    errors = validate_directory(Path(args.input))
    if errors:
        for error in errors:
            print(f"[FAIL] {error}", file=sys.stderr)
        return 1

    print("3-分组 校验通过：目录结构、模板骨架、集粒度与组级容器均符合合同。")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
