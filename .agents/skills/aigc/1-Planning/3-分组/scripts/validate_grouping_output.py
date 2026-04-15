#!/usr/bin/env python3
"""Validate grouped-script outputs for `1-Planning/3-分组`."""

from __future__ import annotations

import argparse
import ast
import json
import re
import sys
from pathlib import Path

from grouping_quantizer import (
    TAIL_HOOK_COMMENT_PREFIX,
    TAIL_HOOK_LABEL,
    QuantizationError,
    build_quantization_result,
    parse_frontmatter,
    parse_group_sections,
    strip_tail_hook_block,
)

EPISODE_FILE_RE = re.compile(r"^第(?P<episode>\d+)集\.md$")
GROUP_HEADER_RE = re.compile(r"^##\s*【(?P<group_id>\d+-\d+-\d+)】(?:\s+(?P<title>.+))?$")
SCENE_HEADER_RE = re.compile(r"^###\s*场景(?P<label>[^：:]+)\s*[：:]\s*(?P<title>.+?)\s*$")
SOURCE_PATH_RE = re.compile(r"^projects/.+/1-Planning/2-格式/第\d+集\.md$")
REPORT_PATH_RE = re.compile(r"^projects/.+/1-Planning/3-分组/执行报告\.md$")
TAIL_HOOK_HEADING_RE = re.compile(rf"^####\s*{re.escape(TAIL_HOOK_LABEL)}(?:（(?P<meta>.*)）)?\s*$")
TAIL_HOOK_COMMENT_RE = re.compile(
    rf"^<!--\s*{re.escape(TAIL_HOOK_COMMENT_PREFIX)}\s*from=(?P<group_id>\d+-\d+-\d+)"
    rf"(?:\s*;\s*quantize=(?P<quantize>[a-z-]+))?\s*-->$"
)

REQUIRED_FRONTMATTER = (
    "项目名",
    "集数",
    "上游主稿",
    "bootstrap_output",
    "scene_unit_count",
    "duration_policy",
    "pace_tier",
    "base_text_window",
    "warn_window",
    "hard_text_window",
    "默认组时长",
    "分镜组时长映射",
    "时长偏离证据",
    "group_count",
    "report_ref",
    "generated_at",
)

FAIL_WINDOW_STATUS_TOKENS = {
    "warn-low",
    "warn_high",
    "warn-high",
    "warn_low",
    "error",
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="校验 1-Planning/3-分组 grouped script 输出契约。")
    parser.add_argument("--input", required=True, help="输入文件或目录（第N集.md 或 3-分组 目录）")
    parser.add_argument("--include-pattern", default="第*集.md", help="目录模式匹配（默认: 第*集.md）")
    return parser.parse_args()


def fail(message: str) -> int:
    print(message, file=sys.stderr)
    return 1


def collect_files(input_path: Path, include_pattern: str) -> list[Path]:
    if not input_path.exists():
        raise FileNotFoundError(f"输入路径不存在: {input_path}")
    if input_path.is_file():
        return [input_path]
    files = sorted(path for path in input_path.glob(include_pattern) if path.is_file())
    if files:
        return files
    return sorted(path for path in input_path.glob("*.md") if path.is_file())


def parse_literal(value: str) -> object:
    value = value.strip()
    if not value:
        return value
    try:
        return json.loads(value)
    except Exception:
        pass
    try:
        return ast.literal_eval(value)
    except Exception:
        return value


def parse_group_headers(body: str) -> list[tuple[str, int, str]]:
    groups: list[tuple[str, int, str]] = []
    for line_no, raw_line in enumerate(body.splitlines(), start=1):
        match = GROUP_HEADER_RE.match(raw_line.strip())
        if match:
            groups.append((match.group("group_id"), line_no, (match.group("title") or "").strip()))
    return groups


def parse_scene_headers(body: str) -> list[tuple[int, int, str]]:
    scenes: list[tuple[int, int, str]] = []
    for line_no, raw_line in enumerate(body.splitlines(), start=1):
        match = SCENE_HEADER_RE.match(raw_line.strip())
        if match:
            scene_no = int(match.group("label"))
            scenes.append((line_no, scene_no, match.group("title").strip()))
    return scenes


def resolve_declared_path(declared_path: str, grouped_script_path: Path) -> Path:
    path = Path(declared_path)
    if path.is_absolute() or path.exists():
        return path

    resolved_grouped_path = grouped_script_path.resolve()
    parts = resolved_grouped_path.parts
    if "projects" not in parts:
        return path
    repo_root = Path(*parts[: parts.index("projects")])
    return repo_root / path


def parse_upstream_scene_headers(upstream_path: Path) -> tuple[list[tuple[int, str]], str | None]:
    if not upstream_path.exists():
        return [], f"frontmatter `上游主稿` 指向的文件不存在：{upstream_path}"

    upstream_text = upstream_path.read_text(encoding="utf-8")
    _frontmatter, body = parse_frontmatter(upstream_text)
    scenes: list[tuple[int, str]] = []
    seen_scene_numbers: set[int] = set()
    for raw_line in body.splitlines():
        match = SCENE_HEADER_RE.match(raw_line.strip())
        if not match:
            continue
        scene_no = int(match.group("label"))
        if scene_no in seen_scene_numbers:
            return [], f"上游主稿存在重复场景编号：场景{scene_no}"
        seen_scene_numbers.add(scene_no)
        scenes.append((scene_no, match.group("title").strip()))

    if not scenes:
        return [], f"上游主稿未发现任何 `### 场景N：...` 标题：{upstream_path}"
    return scenes, None


def validate_scene_headers_against_upstream(
    output_scenes: list[tuple[int, int, str]],
    upstream_scenes: list[tuple[int, str]],
    upstream_path: Path,
) -> str | None:
    upstream_by_no = dict(upstream_scenes)
    seen_scene_numbers: set[int] = set()

    for line_no, scene_no, title in output_scenes:
        expected_title = upstream_by_no.get(scene_no)
        if expected_title is None:
            return f"第 {line_no} 行 `场景{scene_no}` 不存在于上游主稿：{upstream_path}"
        if title != expected_title:
            return (
                f"第 {line_no} 行 `场景{scene_no}` 标题必须逐字沿用上游："
                f"`{expected_title}`，实际为 `{title}`。"
            )
        seen_scene_numbers.add(scene_no)

    missing_scene_numbers = [scene_no for scene_no, _title in upstream_scenes if scene_no not in seen_scene_numbers]
    if missing_scene_numbers:
        missing = "、".join(f"场景{scene_no}" for scene_no in missing_scene_numbers)
        return f"grouped script 缺少上游场景单位：{missing}"
    return None


def parse_int_field(frontmatter: dict[str, str], key: str) -> int:
    try:
        return int(frontmatter[key])
    except Exception as exc:  # noqa: BLE001
        raise ValueError(f"frontmatter `{key}` 必须是整数。") from exc


def extract_report_block(report_text: str, group_id: str) -> str | None:
    pattern = re.compile(
        rf"^###\s*【{re.escape(group_id)}】.*?(?=^###\s*【|\Z)",
        re.M | re.S,
    )
    match = pattern.search(report_text)
    if not match:
        return None
    return match.group(0)


def extract_report_value(block: str, field_name: str) -> str | None:
    match = re.search(rf"{re.escape(field_name)}:\s*`?(.+?)`?\s*$", block, re.M)
    if not match:
        return None
    return match.group(1).strip()


def validate_tail_hook_contract(body: str) -> str | None:
    sections = parse_group_sections(body)
    for index, section in enumerate(sections):
        lines = section.body.splitlines()
        hook_indexes = [
            line_index
            for line_index, raw_line in enumerate(lines)
            if TAIL_HOOK_HEADING_RE.match(raw_line.strip()) or TAIL_HOOK_COMMENT_RE.match(raw_line.strip())
        ]
        if not hook_indexes:
            continue
        if len(hook_indexes) > 1:
            return f"`{section.group_id}` 只能出现一个 `{TAIL_HOOK_LABEL}` 区块。"
        if index == len(sections) - 1:
            return f"末组 `{section.group_id}` 不得追加 `{TAIL_HOOK_LABEL}`。"
        hook_index = hook_indexes[0]
        if not any(raw_line.strip() for raw_line in lines[hook_index + 1 :]):
            return f"`{section.group_id}` 的 `{TAIL_HOOK_LABEL}` 区块不能为空。"
        if strip_tail_hook_block(section.body) != "\n".join(lines[:hook_index]).rstrip():
            return f"`{section.group_id}` 的 `{TAIL_HOOK_LABEL}` 必须位于组尾，且其后只允许保留借入段落。"
        expected_next_group_id = sections[index + 1].group_id
        marker_line = lines[hook_index].strip()
        comment_match = TAIL_HOOK_COMMENT_RE.match(marker_line)
        if comment_match:
            referenced_group_id = comment_match.group("group_id")
            quantize_mode = comment_match.group("quantize")
            if quantize_mode not in (None, "include", "ignore"):
                return f"`{section.group_id}` 的 `{TAIL_HOOK_LABEL}` 注释包含未知 quantize 模式：{quantize_mode}"
        else:
            heading_match = TAIL_HOOK_HEADING_RE.match(marker_line)
            meta = heading_match.group("meta") if heading_match else ""
            referenced_group_id = expected_next_group_id if expected_next_group_id in (meta or "") else ""
        if referenced_group_id != expected_next_group_id:
            return f"`{section.group_id}` 的 `{TAIL_HOOK_LABEL}` 标记必须显式回指下一组 `{expected_next_group_id}`。"
    return None


def validate_file(path: Path) -> tuple[bool, str]:
    text = path.read_text(encoding="utf-8")
    try:
        frontmatter, body = parse_frontmatter(text)
    except Exception as exc:  # noqa: BLE001
        return False, str(exc)

    for key in REQUIRED_FRONTMATTER:
        if key not in frontmatter or not frontmatter[key]:
            return False, f"frontmatter 缺失字段 `{key}`。"

    file_match = EPISODE_FILE_RE.match(path.name)
    if not file_match:
        return False, f"文件名必须是 `第N集.md`：{path.name}"

    episode_number = int(file_match.group("episode"))
    episode_label = f"第{episode_number}集"
    if frontmatter["集数"] != episode_label:
        return False, f"frontmatter `集数` 与文件名不一致：{frontmatter['集数']} vs {path.name}"
    if not SOURCE_PATH_RE.match(frontmatter["上游主稿"]):
        return False, "frontmatter `上游主稿` 必须指向 `projects/aigc/<项目名>/1-Planning/2-格式/第N集.md`。"
    if not REPORT_PATH_RE.match(frontmatter["report_ref"]):
        return False, "frontmatter `report_ref` 必须指向 `projects/aigc/<项目名>/1-Planning/3-分组/执行报告.md`。"

    duration_mapping = parse_literal(frontmatter["分镜组时长映射"])
    duration_evidence = parse_literal(frontmatter["时长偏离证据"])
    if not isinstance(duration_mapping, dict):
        return False, "frontmatter `分镜组时长映射` 必须是对象字面量。"
    if duration_mapping and (not isinstance(duration_evidence, list) or not duration_evidence):
        return False, "frontmatter `分镜组时长映射` 非空时，`时长偏离证据` 也必须非空。"

    if "【分组正文】" not in body:
        return False, "缺少 `【分组正文】` 区块。"

    groups = parse_group_headers(body)
    if not groups:
        return False, "未发现任何三段式分镜组标题 `## 【x-x-x】`。"

    tail_hook_error = validate_tail_hook_contract(body)
    if tail_hook_error:
        return False, tail_hook_error
    scenes = parse_scene_headers(body)
    if not scenes:
        return False, "未发现任何 `### 场景N：...` 标题。"

    upstream_path = resolve_declared_path(frontmatter["上游主稿"], path)
    upstream_scenes, upstream_scene_error = parse_upstream_scene_headers(upstream_path)
    if upstream_scene_error:
        return False, upstream_scene_error
    scene_truth_error = validate_scene_headers_against_upstream(scenes, upstream_scenes, upstream_path)
    if scene_truth_error:
        return False, scene_truth_error

    expected_group_count = parse_int_field(frontmatter, "group_count")
    if expected_group_count != len(groups):
        return False, f"`group_count` 应为 {len(groups)}，实际为 {frontmatter['group_count']}。"
    expected_scene_count = parse_int_field(frontmatter, "scene_unit_count")
    unique_scene_count = len({scene_no for _line_no, scene_no, _title in scenes})
    if expected_scene_count != unique_scene_count:
        return False, f"`scene_unit_count` 应为 {unique_scene_count}，实际为 {frontmatter['scene_unit_count']}。"

    seen_group_ids: set[str] = set()
    scene_group_ordinals: dict[int, int] = {}
    current_scene_index = 0
    previous_scene_no = 0

    for group_id, line_no, _title in groups:
        parts = [int(part) for part in group_id.split("-")]
        if len(parts) != 3:
            return False, f"{group_id} 不是合法三段式分镜组ID。"
        if parts[0] != episode_number:
            return False, f"{group_id} 的第一段必须等于当前集号 {episode_number}。"
        if group_id in seen_group_ids:
            return False, f"分镜组锚点重复：{group_id}"
        seen_group_ids.add(group_id)

        next_scene_no: int | None = None
        while current_scene_index < len(scenes):
            scene_line_no, scene_no, _scene_title = scenes[current_scene_index]
            if scene_line_no > line_no:
                next_scene_no = scene_no
                break
            current_scene_index += 1
        if next_scene_no is None:
            return False, f"{group_id} 后面没有承接任何场景标题。"
        if next_scene_no < previous_scene_no:
            return False, f"{group_id} 之后的场景顺序倒退。"
        if parts[1] != next_scene_no:
            return False, f"{group_id} 的第二段应等于该组起始场景号 {next_scene_no}。"
        expected_group_ordinal = scene_group_ordinals.get(next_scene_no, 0) + 1
        if parts[2] != expected_group_ordinal:
            return False, f"{group_id} 的第三段应等于场景 {next_scene_no} 内第 {expected_group_ordinal} 组。"
        scene_group_ordinals[next_scene_no] = expected_group_ordinal
        previous_scene_no = next_scene_no

    report_path = path.parent / "执行报告.md"
    if not report_path.exists():
        return False, f"缺少总执行报告：{report_path}"
    report_text = report_path.read_text(encoding="utf-8")
    if f"## {episode_label}" not in report_text:
        return False, f"执行报告缺少当前集区块：`## {episode_label}`。"

    try:
        metrics = build_quantization_result(path, report_path)
    except (QuantizationError, ValueError) as exc:
        return False, f"量化脚本执行失败：{exc}"

    if parse_int_field(frontmatter, "base_text_window") != metrics["base_text_window"]:
        return False, "frontmatter `base_text_window` 与 quantizer 计算结果不一致。"
    expected_warn_window = f"{metrics['warn_low']}-{metrics['warn_high']}"
    if frontmatter["warn_window"] != expected_warn_window:
        return False, "frontmatter `warn_window` 与 quantizer 计算结果不一致。"
    if parse_int_field(frontmatter, "hard_text_window") != metrics["hard_text_window"]:
        return False, "frontmatter `hard_text_window` 与 quantizer 计算结果不一致。"

    metric_by_group = {item["group_id"]: item for item in metrics["groups"]}
    for group_id, _line_no, _title in groups:
        block = extract_report_block(report_text, group_id)
        if block is None:
            return False, f"执行报告未登记分镜组ID：{group_id}"
        for field in (
            "estimated_duration_seconds",
            "effective_text_chars",
            "window_status",
            "judgement_basis",
        ):
            if f"{field}:" not in block:
                return False, f"执行报告缺少 `{group_id}` 的 `{field}`。"

        status_value = extract_report_value(block, "window_status")
        if status_value is None:
            return False, f"执行报告未能解析 `{group_id}` 的 `window_status`。"
        if status_value in FAIL_WINDOW_STATUS_TOKENS:
            return False, f"`window_status` 不得直接落盘候选态：{status_value}"

        group_metric = metric_by_group[group_id]
        estimated_value = extract_report_value(block, "estimated_duration_seconds")
        if estimated_value is None or int(re.search(r"\d+", estimated_value).group(0)) != group_metric["resolved_duration_seconds"]:
            return False, f"`{group_id}` 的 `estimated_duration_seconds` 与 duration mapping 不一致。"

        effective_value = extract_report_value(block, "effective_text_chars")
        if effective_value is None:
            return False, f"执行报告未能解析 `{group_id}` 的 `effective_text_chars`。"
        reported_chars = int(re.search(r"\d+", effective_value).group(0))
        expected_chars = int(group_metric["effective_text_chars"])
        calculation_mode = group_metric["calculation_mode"]
        if calculation_mode.startswith("story_source_recomputed") or calculation_mode == "group_section_field_weighted":
            tolerance = 2
            if abs(reported_chars - expected_chars) > tolerance:
                return False, (
                    f"`{group_id}` 的 `effective_text_chars` 应为 {expected_chars}，"
                    f"实际为 {reported_chars}（容差 {tolerance}）。"
                )
        else:
            tolerance = max(25, round(expected_chars * 0.35))
            if abs(reported_chars - expected_chars) > tolerance:
                return False, (
                    f"`{group_id}` 的 `effective_text_chars` 偏离 quantizer 估算过大："
                    f"{reported_chars} vs {expected_chars}（容差 {tolerance}）。"
                )

        judgement_basis = extract_report_value(block, "judgement_basis") or ""
        if expected_chars > int(group_metric["hard_text_window"]):
            return False, (
                f"`{group_id}` 的 `effective_text_chars` 超过 hard_text_window："
                f"{expected_chars} > {group_metric['hard_text_window']}。"
            )
        if expected_chars < int(group_metric["warn_low"]) and not re.search(
            r"warn_low|低于|过轻|并组|不可并|明确信息落点|独立信息落点|尾组|锁定|固定镜数|分镜ID|分镜组ID|下游|2-Global|3-Detail|beat",
            judgement_basis,
        ):
            return False, (
                f"`{group_id}` 低于 warn_low 时，`judgement_basis` 必须说明并组检查、独立信息落点或锁定分镜依据。"
            )
        if int(group_metric["warn_high"]) < expected_chars <= int(group_metric["hard_text_window"]) and not re.search(
            r"warn_high|未超|不超|hard_text_window|不可拆|连续峰值|保留",
            judgement_basis,
        ):
            return False, (
                f"`{group_id}` 高于 warn_high 时，`judgement_basis` 必须说明拆分检查或保留依据。"
            )

    return True, f"{path.name} 校验通过：grouped script、三段式组ID与量化报告一致。"


def main() -> int:
    args = parse_args()
    try:
        files = collect_files(Path(args.input), args.include_pattern)
    except Exception as exc:  # noqa: BLE001
        return fail(str(exc))

    if not files:
        return fail("未找到可校验的 markdown 文件。")

    for path in files:
        ok, message = validate_file(path)
        if not ok:
            return fail(f"{path}: {message}")
        print(message)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
