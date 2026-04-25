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

VOICE_TEXT_COEFFICIENT = 1.2
TAIL_HOOK_LABEL = "尾钩借焰"
TAIL_HOOK_COMMENT_PREFIX = "tail-hook:"

GROUP_HEADER_RE = re.compile(r"^##\s*【(?P<group_id>\d+-\d+-\d+)】(?:\s+(?P<title>.+))?$")
SCENE_HEADER_RE = re.compile(r"^###\s*场景(?P<label>[^：:]+)\s*[：:]\s*(?P<title>.+?)\s*$")
VOICE_TEXT_RE = re.compile(r"^(对白|独白|内心独白|旁白)(?:（.*?）|\(.*?\))?\s*[：:]\s*(.*)$")
VOICE_VISUAL_RE = re.compile(r"^(对白画面|独白画面|内心独白画面|旁白画面)\s*[：:]\s*(.*)$")
VISUAL_FIELD_RE = re.compile(
    r"^(动作画面|角色动作|环境描写|音效|音效画面|转场|角色造型|道具特写|表情特写|特写画面|"
    r"群像画面|系统画面|规则显影|现实灾难画面|表演提示|心理反应|镜头语言预设)\s*[：:]\s*(.*)$"
)
TAIL_HOOK_HEADING_RE = re.compile(rf"^####\s*{re.escape(TAIL_HOOK_LABEL)}(?:（.*）)?\s*$")
TAIL_HOOK_COMMENT_RE = re.compile(
    rf"^<!--\s*{re.escape(TAIL_HOOK_COMMENT_PREFIX)}\s*from=(?P<group_id>\d+-\d+-\d+)"
    rf"(?:\s*;\s*quantize=(?P<quantize>[a-z-]+))?\s*-->$"
)
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


def format_factor(value: float) -> str:
    if float(value).is_integer():
        return str(int(value))
    return f"{value:.2f}".rstrip("0").rstrip(".")


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


def split_tail_hook_block(text: str) -> tuple[str, str | None]:
    lines = text.splitlines()
    for index, raw_line in enumerate(lines):
        stripped = raw_line.strip()
        comment_match = TAIL_HOOK_COMMENT_RE.match(stripped)
        if comment_match:
            return (
                "\n".join(lines[:index]).rstrip(),
                "\n".join(lines[index + 1 :]).strip(),
            )
        if TAIL_HOOK_HEADING_RE.match(stripped):
            return (
                "\n".join(lines[:index]).rstrip(),
                "\n".join(lines[index + 1 :]).strip(),
            )
    return text.rstrip(), None


def strip_tail_hook_block(text: str) -> str:
    canonical_text, _tail_hook = split_tail_hook_block(text)
    return canonical_text


def field_weighted_chars(text: str, pace_tier: str) -> tuple[int, bool, dict[str, dict[str, Any]]]:
    total = 0
    matched_field = False
    action_coef = ACTION_VISUAL_COEFFICIENT[pace_tier]
    breakdown = {
        "voice_text": {
            "raw_chars": 0,
            "weighted_chars": 0,
            "line_count": 0,
            "coefficient": VOICE_TEXT_COEFFICIENT,
        },
        "voice_visual": {
            "raw_chars": 0,
            "weighted_chars": 0,
            "line_count": 0,
            "coefficient": 0.0,
        },
        "visual_field": {
            "raw_chars": 0,
            "weighted_chars": 0,
            "line_count": 0,
            "coefficient": action_coef,
        },
        "fallback_visual": {
            "raw_chars": 0,
            "weighted_chars": 0,
            "line_count": 0,
            "coefficient": action_coef,
        },
    }
    for raw_line in text.splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#"):
            continue
        if SCENE_HEADER_RE.match(line):
            continue
        voice_text = VOICE_TEXT_RE.match(line)
        if voice_text:
            raw_chars = count_visible_chars(voice_text.group(2))
            weighted_chars = round(raw_chars * VOICE_TEXT_COEFFICIENT)
            total += weighted_chars
            matched_field = True
            breakdown["voice_text"]["raw_chars"] += raw_chars
            breakdown["voice_text"]["weighted_chars"] += weighted_chars
            breakdown["voice_text"]["line_count"] += 1
            continue
        voice_visual = VOICE_VISUAL_RE.match(line)
        if voice_visual:
            matched_field = True
            breakdown["voice_visual"]["raw_chars"] += count_visible_chars(voice_visual.group(2))
            breakdown["voice_visual"]["line_count"] += 1
            continue
        visual_field = VISUAL_FIELD_RE.match(line)
        if visual_field:
            raw_chars = count_visible_chars(visual_field.group(2))
            weighted_chars = round(raw_chars * action_coef)
            total += weighted_chars
            matched_field = True
            breakdown["visual_field"]["raw_chars"] += raw_chars
            breakdown["visual_field"]["weighted_chars"] += weighted_chars
            breakdown["visual_field"]["line_count"] += 1
            continue
        raw_chars = count_visible_chars(line)
        weighted_chars = round(raw_chars * action_coef)
        total += weighted_chars
        breakdown["fallback_visual"]["raw_chars"] += raw_chars
        breakdown["fallback_visual"]["weighted_chars"] += weighted_chars
        breakdown["fallback_visual"]["line_count"] += 1
    return total, matched_field, breakdown


def planning_estimate_chars(text: str) -> tuple[int, dict[str, int]]:
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
    total = visible_total + scene_units * 6 + turning_points * 2
    return total, {
        "visible_total": visible_total,
        "scene_units": scene_units,
        "turning_points": turning_points,
    }


def compute_body_chars(text: str, pace_tier: str) -> tuple[int, str, dict[str, Any]]:
    weighted, matched_field, field_breakdown = field_weighted_chars(text, pace_tier)
    if matched_field:
        return weighted, "field_weighted", {
            "trace_type": "field_weighted",
            "source_scope": "group_section",
            "breakdown": field_breakdown,
        }
    estimated_total, planning_breakdown = planning_estimate_chars(text)
    return estimated_total, "planning_estimate_visible_chars", {
        "trace_type": "planning_estimate",
        "source_scope": "group_section",
        "breakdown": planning_breakdown,
    }


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
        raise QuantizationError("分组文件路径必须位于 `projects/aigc/<项目名>/...` 下。")
    projects_index = parts.index("projects")
    try:
        if projects_index + 2 < len(parts) and parts[projects_index + 1] == "aigc":
            return Path(*parts[: projects_index + 3])
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
) -> tuple[int, str, dict[str, Any]]:
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
    weighted, matched_field, field_breakdown = field_weighted_chars(joined, pace_tier)
    if matched_field:
        return weighted, "story_source_recomputed_field_weighted", {
            "trace_type": "field_weighted",
            "source_scope": "story_source",
            "shot_range": {
                "start": shot_range[0],
                "end": shot_range[1],
            },
            "breakdown": field_breakdown,
        }
    estimated_total, planning_breakdown = planning_estimate_chars(joined)
    return estimated_total, "story_source_recomputed_visible_chars", {
        "trace_type": "planning_estimate",
        "source_scope": "story_source",
        "shot_range": {
            "start": shot_range[0],
            "end": shot_range[1],
        },
        "breakdown": planning_breakdown,
    }


def compute_effective_chars(
    section: GroupSection,
    pace_tier: str,
    report_block: str | None,
    source_type: str | None,
    story_source_text: str | None,
) -> tuple[int, str, dict[str, Any]]:
    source_span = extract_report_field(report_block or "", "source_span")
    shot_range = parse_shot_range(source_span)
    if (
        source_type in {"storyboard_script", "hybrid_story_text"}
        and shot_range
        and story_source_text is not None
    ):
        return recompute_from_story_source(story_source_text, shot_range, pace_tier)

    counted_chars, mode, detail = compute_body_chars(section.body, pace_tier)
    if mode == "field_weighted":
        return counted_chars, "group_section_field_weighted", detail
    return counted_chars, mode, detail


def format_shot_range(shot_range: dict[str, int] | None) -> str | None:
    if not shot_range:
        return None
    start = shot_range["start"]
    end = shot_range["end"]
    if start == end:
        return f"镜{start}"
    return f"镜{start}-{end}"


def render_effective_chars_trace(total: int, detail: dict[str, Any], mode: str) -> str:
    source_scope = detail.get("source_scope")
    shot_range_label = format_shot_range(detail.get("shot_range"))
    if detail.get("trace_type") == "planning_estimate":
        breakdown = detail["breakdown"]
        prefix = ""
        if source_scope == "story_source" and shot_range_label:
            prefix = f"{shot_range_label}; "
        return (
            f"effective_chars={prefix}"
            f"planning_estimate(visible={breakdown['visible_total']} + "
            f"scene_units({breakdown['scene_units']}*6={breakdown['scene_units'] * 6}) + "
            f"turning_points({breakdown['turning_points']}*2={breakdown['turning_points'] * 2}))"
            f"={total}; mode={mode}"
        )

    breakdown = detail["breakdown"]
    components: list[str] = []
    if breakdown["voice_text"]["line_count"]:
        components.append(
            "voice_text("
            f"sum_round={breakdown['voice_text']['weighted_chars']}; "
            f"raw={breakdown['voice_text']['raw_chars']}; "
            f"coef={format_factor(breakdown['voice_text']['coefficient'])}; "
            f"lines={breakdown['voice_text']['line_count']}"
            ")"
        )
    if breakdown["voice_visual"]["line_count"]:
        components.append(
            "voice_visual("
            f"excluded; raw={breakdown['voice_visual']['raw_chars']}; "
            f"lines={breakdown['voice_visual']['line_count']}"
            ")"
        )
    if breakdown["visual_field"]["line_count"]:
        components.append(
            "visual_field("
            f"sum_round={breakdown['visual_field']['weighted_chars']}; "
            f"raw={breakdown['visual_field']['raw_chars']}; "
            f"coef={format_factor(breakdown['visual_field']['coefficient'])}; "
            f"lines={breakdown['visual_field']['line_count']}"
            ")"
        )
    if breakdown["fallback_visual"]["line_count"]:
        components.append(
            "fallback_visual("
            f"sum_round={breakdown['fallback_visual']['weighted_chars']}; "
            f"raw={breakdown['fallback_visual']['raw_chars']}; "
            f"coef={format_factor(breakdown['fallback_visual']['coefficient'])}; "
            f"lines={breakdown['fallback_visual']['line_count']}"
            ")"
        )
    if not components:
        components.append("no_weighted_components(0)")

    prefix = ""
    if source_scope == "story_source" and shot_range_label:
        prefix = f"{shot_range_label}; "
    return f"effective_chars={prefix}{' + '.join(components)} = {total}; mode={mode}"


def render_quantization_trace(
    *,
    group_id: str,
    default_duration_seconds: int,
    resolved_duration_seconds: int,
    duration_source: str,
    pace_tier: str,
    base_text_window: int,
    warn_low: int,
    warn_high: int,
    hard_text_window: int,
    effective_text_chars: int,
    calculation_mode: str,
    calculation_detail: dict[str, Any],
) -> str:
    duration_label = (
        f"mapping[{group_id}]({resolved_duration_seconds})->{resolved_duration_seconds}"
        if duration_source == "mapping"
        else f"default({default_duration_seconds})->{resolved_duration_seconds}"
    )
    pace_coef = format_factor(PACE_COEFFICIENT[pace_tier])
    duration_trace = f"duration={duration_label}"
    window_trace = (
        "window="
        f"base({resolved_duration_seconds}*10*{pace_coef}={base_text_window}), "
        f"warn_low({base_text_window}*0.8={warn_low}), "
        f"warn_high({base_text_window}*1.0={warn_high}), "
        f"hard({base_text_window}*1.1={hard_text_window})"
    )
    effective_trace = render_effective_chars_trace(
        effective_text_chars,
        calculation_detail,
        calculation_mode,
    )
    return f"{duration_trace}; {window_trace}; {effective_trace}"


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
        duration_source = "default"
        if section.group_id in duration_mapping:
            resolved_duration = parse_seconds(
                duration_mapping[section.group_id],
                field_name=f"分镜组时长映射[{section.group_id}]",
            )
            duration_source = "mapping"
        group_window = compute_window(resolved_duration, pace_tier)
        canonical_body, _tail_hook_body = split_tail_hook_block(section.body)
        effective_chars, calculation_mode, calculation_detail = compute_effective_chars(
            GroupSection(group_id=section.group_id, title=section.title, body=canonical_body),
            pace_tier,
            report_block,
            source_type,
            story_source_text,
        )
        quantization_trace = render_quantization_trace(
            group_id=section.group_id,
            default_duration_seconds=default_duration_seconds,
            resolved_duration_seconds=resolved_duration,
            duration_source=duration_source,
            pace_tier=pace_tier,
            base_text_window=group_window["base_text_window"],
            warn_low=group_window["warn_low"],
            warn_high=group_window["warn_high"],
            hard_text_window=group_window["hard_text_window"],
            effective_text_chars=effective_chars,
            calculation_mode=calculation_mode,
            calculation_detail=calculation_detail,
        )
        group_results.append(
            {
                "group_id": section.group_id,
                "title": section.title,
                "resolved_duration_seconds": resolved_duration,
                "duration_source": duration_source,
                "base_text_window": group_window["base_text_window"],
                "warn_low": group_window["warn_low"],
                "warn_high": group_window["warn_high"],
                "hard_text_window": group_window["hard_text_window"],
                "effective_text_chars": effective_chars,
                "calculation_mode": calculation_mode,
                "calculation_detail": calculation_detail,
                "quantization_trace": quantization_trace,
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
        print(f"  trace: {group['quantization_trace']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
