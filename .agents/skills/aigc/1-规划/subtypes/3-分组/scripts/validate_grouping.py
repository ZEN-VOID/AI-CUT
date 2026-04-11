#!/usr/bin/env python3
"""Validate aigc planning grouping markdown outputs."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path


EPISODE_FILE_RE = re.compile(r"^第0*(?P<ep>\d+)集\.md$")
FORBIDDEN_GROUP_FILE_RE = re.compile(r"^第0*(?P<group>\d+)组\.md$")
GROUP_HEADING_RE = re.compile(r"^##\s+(G\d+)\b")

GROUP_PLAN_REQUIRED = [
    "# 分组总览",
    "## 分组目标",
    "## 主路由决议",
    "## 量化摘要",
    "## 集级总览表",
]
GROUP_PLAN_TABLE_HEADER = "| episode | route | duration_policy | pace_tier | episode_load_score | recommended_group_band | group_count | grouping_focus | downstream_entry | dependency_note |"

REPORT_REQUIRED = [
    "# 分组执行报告",
    "## 输入清单",
    "## 路由决议",
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
ALLOWED_ROUTES = {"preset", "structure", "load"}
ALLOWED_PACE_TIERS = {"慢节奏", "中节奏", "快节奏"}
ALLOWED_WINDOW_STATUS = {"ok", "warn-low", "warn-high", "error"}
ALLOWED_PRESET_MODES = {"standard", "preserve_and_extend", "preserve_only"}
ALLOWED_PRESET_POLICIES = {"inherit", "split-soft-lock", "reference-only", "none"}
DURATION_TEXT_RE = re.compile(r"^(?P<seconds>\d+)秒$")


def fail(message: str) -> int:
    print(message, file=sys.stderr)
    return 1


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


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
        "route",
        "source_span",
        "group_count",
        "scene_unit_count",
        "duration_policy",
        "默认组时长",
        "分镜组时长映射",
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

    if frontmatter["route"] not in ALLOWED_ROUTES:
        errors.append(f"{path}: `route` 必须是 {sorted(ALLOWED_ROUTES)} 之一。")

    if not frontmatter["group_count"].isdigit() or int(frontmatter["group_count"]) <= 0:
        errors.append(f"{path}: `group_count` 必须是正整数。")
        return
    group_count = int(frontmatter["group_count"])

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
    for row in plan_rows:
        group_id = row["group_id"]
        seen_group_ids.add(group_id)
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
    if not group_plan.exists():
        errors.append(f"{input_path}: 缺少 `group-plan.md`。")
    else:
        validate_group_plan(group_plan, errors)

    if not report.exists():
        errors.append(f"{input_path}: 缺少 `执行报告.md`。")
    else:
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
