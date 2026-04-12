#!/usr/bin/env python3
"""Compute quantized grouping metrics for `1-Planning/3-分组`.

This script is the stage-local calculation truth for:
- resolved group duration
- text window thresholds
- effective_text_chars
- mixed-source / storyboard-source recompute
"""

from __future__ import annotations

import argparse
import ast
import json
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import yaml

PACE_COEFFICIENT = {
    "慢节奏": 0.7,
    "中节奏": 1.0,
    "快节奏": 1.3,
}

ACTION_VISUAL_COEFFICIENT = {
    "慢节奏": 0.7,
    "中节奏": 0.5,
    "快节奏": 0.3,
}

GROUP_HEADER_RE = re.compile(r"^##\s*【(?P<group_id>\d+-\d+-\d+)】(?:\s+(?P<title>.+))?$")
SCENE_HEADER_RE = re.compile(r"^###\s*场景(?P<label>[^：:]+)\s*[：:]\s*(?P<title>.+?)\s*$")
VOICE_TEXT_RE = re.compile(r"^(对白|独白|内心独白|旁白)(?:（.*?）|\(.*?\))?\s*[：:]\s*(.*)$")
VOICE_VISUAL_RE = re.compile(r"^(对白画面|独白画面|内心独白画面|旁白画面)\s*[：:]\s*(.*)$")
ACTION_VISUAL_RE = re.compile(r"^动作画面\s*[：:]\s*(.*)$")
SHOT_RANGE_RE = re.compile(r"镜\s*(?P<start>\d+)(?:\s*-\s*(?P<end>\d+))?")
SHOT_HEADER_RE = re.compile(
    r"(?m)^(?:#{1,6}\s*)?(?:镜头?|分镜|镜)\s*(?P<num>\d+)\s*[：:].*$"
)


class QuantizationError(RuntimeError):
    """Raised when the grouped-script quantization contract is broken."""


@dataclass
class GroupSection:
    group_id: str
    title: str
    body: str


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="计算 1-Planning/3-分组 的量化字段。")
    parser.add_argument("--input", required=True, help="输入 grouped script 文件路径（第N集.md）")
    parser.add_argument("--report", help="执行报告路径；默认读取同目录 `执行报告.md`")
    parser.add_argument("--json", action="store_true", help="输出 JSON")
    return parser.parse_args()


def parse_frontmatter(text: str) -> tuple[dict[str, str], str]:
    if not text.startswith("---\n"):
        raise QuantizationError("文件必须以 frontmatter 开头。")
    try:
        _, rest = text.split("---\n", 1)
        block, body = rest.split("\n---\n", 1)
    except ValueError as exc:
        raise QuantizationError("frontmatter 结束分隔符缺失。") from exc

    data: dict[str, str] = {}
    for raw_line in block.splitlines():
        line = raw_line.strip()
        if not line or ":" not in line:
            continue
        key, value = line.split(":", 1)
        data[key.strip()] = value.strip()
    return data, body


def parse_literal(value: str) -> Any:
    value = value.strip()
    if not value:
        return value
    for loader in (json.loads, ast.literal_eval):
        try:
            return loader(value)
        except Exception:
            continue
    return value


def parse_seconds(value: Any, *, field_name: str) -> int:
    if isinstance(value, (int, float)):
        return int(value)
    if not isinstance(value, str):
        raise QuantizationError(f"`{field_name}` 无法解析为秒数：{value!r}")
    match = re.search(r"(\d+)", value)
    if not match:
        raise QuantizationError(f"`{field_name}` 必须包含秒数：{value}")
    return int(match.group(1))


def count_visible_chars(text: str) -> int:
    stripped = re.sub(r"\s+", "", text)
    return len(stripped)


def compute_window(duration_seconds: int, pace_tier: str) -> dict[str, int]:
    if pace_tier not in PACE_COEFFICIENT:
        raise QuantizationError(f"未知 pace_tier: {pace_tier}")
    base = round(duration_seconds * 10 * PACE_COEFFICIENT[pace_tier])
    warn_low = round(base * 0.8)
    warn_high = round(base * 1.0)
    hard = round(base * 1.1)
    return {
        "base_text_window": base,
        "warn_low": warn_low,
        "warn_high": warn_high,
        "hard_text_window": hard,
    }


def parse_group_sections(body: str) -> list[GroupSection]:
    lines = body.splitlines()
    groups: list[tuple[str, str, int, int]] = []
    for index, raw_line in enumerate(lines):
        match = GROUP_HEADER_RE.match(raw_line.strip())
        if match:
            groups.append(
                (
                    match.group("group_id"),
                    (match.group("title") or "").strip(),
                    index,
                    -1,
                )
            )

    if not groups:
        raise QuantizationError("未发现任何分镜组标题。")

    finalized: list[GroupSection] = []
    for position, (group_id, title, start, _end) in enumerate(groups):
        end = groups[position + 1][2] if position + 1 < len(groups) else len(lines)
        section_lines = lines[start + 1 : end]
        finalized.append(GroupSection(group_id=group_id, title=title, body="\n".join(section_lines).strip()))
    return finalized


def field_weighted_chars(text: str, pace_tier: str) -> tuple[int, bool]:
    total = 0
    matched_field = False
    action_coef = ACTION_VISUAL_COEFFICIENT[pace_tier]
    for raw_line in text.splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#"):
            continue
        if SCENE_HEADER_RE.match(line):
            continue
        voice_text = VOICE_TEXT_RE.match(line)
        if voice_text:
            total += count_visible_chars(voice_text.group(2))
            matched_field = True
            continue
        voice_visual = VOICE_VISUAL_RE.match(line)
        if voice_visual:
            matched_field = True
            continue
        action_visual = ACTION_VISUAL_RE.match(line)
        if action_visual:
            total += round(count_visible_chars(action_visual.group(1)) * action_coef)
            matched_field = True
            continue
        total += round(count_visible_chars(line) * action_coef)
    return total, matched_field


def planning_estimate_chars(text: str) -> int:
    visible_total = 0
    scene_units = 0
    turning_points = 0
    for raw_line in text.splitlines():
        line = raw_line.strip()
        if not line:
            continue
        if line.startswith("#"):
            if SCENE_HEADER_RE.match(line):
                scene_units += 1
            continue
        visible_total += count_visible_chars(line)
        if re.search(r"[。！？!?；;]", line):
            turning_points += 1
    return visible_total + scene_units * 6 + turning_points * 2


def parse_report_block(report_text: str, group_id: str) -> str | None:
    pattern = re.compile(
        rf"^###\s*【{re.escape(group_id)}】.*?(?=^###\s*【|\Z)",
        re.M | re.S,
    )
    match = pattern.search(report_text)
    if not match:
        return None
    return match.group(0)


def extract_report_field(block: str, field_name: str) -> str | None:
    match = re.search(rf"{re.escape(field_name)}:\s*`?(.+?)`?\s*$", block, re.M)
    if not match:
        return None
    return match.group(1).strip()


def locate_project_root(grouped_script_path: Path) -> Path:
    parts = grouped_script_path.parts
    if "projects" not in parts:
        raise QuantizationError("分组文件路径必须位于 `projects/<项目名>/...` 下。")
    projects_index = parts.index("projects")
    try:
        return Path(*parts[: projects_index + 2])
    except Exception as exc:
        raise QuantizationError(f"无法从路径解析项目根：{grouped_script_path}") from exc


def load_story_manifest(project_root: Path) -> dict[str, Any]:
    manifest_path = project_root / "0-Init" / "story-source-manifest.yaml"
    if not manifest_path.exists():
        return {}
    return yaml.safe_load(manifest_path.read_text(encoding="utf-8")) or {}


def resolve_story_source(project_root: Path, manifest: dict[str, Any]) -> tuple[str | None, Path | None]:
    primary = manifest.get("primary_story_source") or {}
    source_type = primary.get("source_type")
    relative_path = primary.get("path")
    if not relative_path:
        return source_type, None
    return source_type, project_root / relative_path


def parse_shot_range(source_span: str | None) -> tuple[int, int] | None:
    if not source_span:
        return None
    match = SHOT_RANGE_RE.search(source_span)
    if not match:
        return None
    start = int(match.group("start"))
    end = int(match.group("end") or start)
    if end < start:
        raise QuantizationError(f"`source_span` 的镜号范围非法：{source_span}")
    return start, end


def split_story_source_by_shot(text: str) -> dict[int, str]:
    headers = list(SHOT_HEADER_RE.finditer(text))
    if not headers:
        return {}
    result: dict[int, str] = {}
    for index, match in enumerate(headers):
        shot_no = int(match.group("num"))
        start = match.start()
        end = headers[index + 1].start() if index + 1 < len(headers) else len(text)
        result[shot_no] = text[start:end].strip()
    return result


def recompute_from_story_source(
    source_text: str,
    shot_range: tuple[int, int],
    pace_tier: str,
) -> tuple[int, str]:
    shot_map = split_story_source_by_shot(source_text)
    if not shot_map:
        raise QuantizationError("故事主源存在，但无法解析镜号标题。")
    chunks: list[str] = []
    for shot_no in range(shot_range[0], shot_range[1] + 1):
        chunk = shot_map.get(shot_no)
        if chunk is None:
            raise QuantizationError(f"故事主源缺少镜号 `{shot_no}`。")
        chunks.append(chunk)
    joined = "\n".join(chunks)
    weighted, matched_field = field_weighted_chars(joined, pace_tier)
    if matched_field:
        return weighted, "story_source_recomputed_field_weighted"
    return planning_estimate_chars(joined), "story_source_recomputed_visible_chars"


def compute_effective_chars(
    section: GroupSection,
    pace_tier: str,
    report_block: str | None,
    source_type: str | None,
    story_source_text: str | None,
) -> tuple[int, str]:
    source_span = extract_report_field(report_block or "", "source_span")
    shot_range = parse_shot_range(source_span)
    if (
        source_type in {"storyboard_script", "hybrid_story_text"}
        and shot_range
        and story_source_text is not None
    ):
        return recompute_from_story_source(story_source_text, shot_range, pace_tier)

    weighted, matched_field = field_weighted_chars(section.body, pace_tier)
    if matched_field:
        return weighted, "group_section_field_weighted"
    return planning_estimate_chars(section.body), "planning_estimate_visible_chars"


def build_quantization_result(grouped_script_path: Path, report_path: Path | None = None) -> dict[str, Any]:
    text = grouped_script_path.read_text(encoding="utf-8")
    frontmatter, body = parse_frontmatter(text)
    pace_tier = frontmatter.get("pace_tier")
    if not pace_tier:
        raise QuantizationError("frontmatter 缺少 `pace_tier`。")
    default_duration_seconds = parse_seconds(frontmatter.get("默认组时长", "15秒"), field_name="默认组时长")
    episode_window = compute_window(default_duration_seconds, pace_tier)
    duration_mapping = parse_literal(frontmatter.get("分镜组时长映射", "{}"))
    if not isinstance(duration_mapping, dict):
        raise QuantizationError("frontmatter `分镜组时长映射` 必须是对象。")

    groups = parse_group_sections(body)

    if report_path is None:
        report_path = grouped_script_path.parent / "执行报告.md"
    report_text = report_path.read_text(encoding="utf-8") if report_path.exists() else ""

    project_root = locate_project_root(grouped_script_path)
    manifest = load_story_manifest(project_root)
    source_type, story_source_path = resolve_story_source(project_root, manifest)
    story_source_text = None
    if story_source_path and story_source_path.exists():
        story_source_text = story_source_path.read_text(encoding="utf-8")

    group_results: list[dict[str, Any]] = []
    for section in groups:
        report_block = parse_report_block(report_text, section.group_id)
        resolved_duration = default_duration_seconds
        if section.group_id in duration_mapping:
            resolved_duration = parse_seconds(
                duration_mapping[section.group_id],
                field_name=f"分镜组时长映射[{section.group_id}]",
            )
        group_window = compute_window(resolved_duration, pace_tier)
        effective_chars, calculation_mode = compute_effective_chars(
            section,
            pace_tier,
            report_block,
            source_type,
            story_source_text,
        )
        group_results.append(
            {
                "group_id": section.group_id,
                "title": section.title,
                "resolved_duration_seconds": resolved_duration,
                "base_text_window": group_window["base_text_window"],
                "warn_low": group_window["warn_low"],
                "warn_high": group_window["warn_high"],
                "hard_text_window": group_window["hard_text_window"],
                "effective_text_chars": effective_chars,
                "calculation_mode": calculation_mode,
                "source_span": extract_report_field(report_block or "", "source_span"),
            }
        )

    return {
        "input_path": str(grouped_script_path),
        "project_root": str(project_root),
        "source_type": source_type,
        "story_source_path": str(story_source_path) if story_source_path else None,
        "pace_tier": pace_tier,
        "default_duration_seconds": default_duration_seconds,
        **episode_window,
        "groups": group_results,
    }


def main() -> int:
    args = parse_args()
    input_path = Path(args.input)
    report_path = Path(args.report) if args.report else None
    try:
        payload = build_quantization_result(input_path, report_path)
    except Exception as exc:  # noqa: BLE001
        print(str(exc), file=sys.stderr)
        return 1

    if args.json:
        print(json.dumps(payload, ensure_ascii=False, indent=2))
        return 0

    print(f"input: {payload['input_path']}")
    print(f"pace_tier: {payload['pace_tier']}")
    print(
        "episode_window: "
        f"{payload['base_text_window']} / "
        f"{payload['warn_low']}-{payload['warn_high']} / "
        f"{payload['hard_text_window']}"
    )
    for group in payload["groups"]:
        print(
            f"{group['group_id']}: "
            f"{group['resolved_duration_seconds']}s, "
            f"{group['effective_text_chars']} chars, "
            f"{group['calculation_mode']}"
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
