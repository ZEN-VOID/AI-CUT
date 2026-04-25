#!/usr/bin/env python3
"""Render canonical `执行报告.md` for `1-Planning/3-分组`.

This renderer is the report writeback adapter:
- reuse existing human-authored fields such as `source_span` / `judgement_basis`
- fill authoritative quantized fields from `grouping_quantizer.py`
- normalize the report layout to `templates/grouping-report.template.md`
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path
from typing import Any

from grouping_quantizer import build_quantization_result, parse_frontmatter, parse_group_sections

SCRIPT_DIR = Path(__file__).resolve().parent
SKILL_ROOT = SCRIPT_DIR.parent
REPORT_TEMPLATE = SKILL_ROOT / "templates" / "grouping-report.template.md"

GROUP_BLOCK_RE = re.compile(
    r"^###\s*【(?P<group_id>\d+-\d+-\d+)】(?:\s+(?P<title>.+))?\s*$"
    r"(?P<body>.*?)(?=^###\s*【|^##\s*handoff\s+摘要|\Z)",
    re.M | re.S,
)
HANDOFF_BLOCK_RE = re.compile(r"^##\s*handoff\s+摘要\s*$.*\Z", re.M | re.S)
REPORT_VALUE_RE = re.compile(r"^(?P<field>[^:\n]+):\s*`?(?P<value>.+?)`?\s*$", re.M)
EPISODE_BLOCK_RE = re.compile(r"^##\s*第(?P<episode>\d+)集\s*$.*?(?=^##\s*第\d+集\s*$|\Z)", re.M | re.S)
REPORT_TITLE = "# 1-Planning 3-分组执行报告"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="按 canonical 模板重写 3-分组 `执行报告.md`。")
    parser.add_argument("--input", required=True, help="输入 grouped script 文件路径（第N集.md）")
    parser.add_argument("--report", help="执行报告路径；默认读取同目录 `执行报告.md`")
    parser.add_argument("--dry-run", action="store_true", help="仅预览，不写文件")
    return parser.parse_args()


def ensure_template_exists() -> None:
    if not REPORT_TEMPLATE.exists():
        raise FileNotFoundError(f"缺少执行报告模板：{REPORT_TEMPLATE}")


def extract_report_value(block: str, field_name: str) -> str | None:
    match = re.search(rf"^{re.escape(field_name)}:\s*`?(.+?)`?\s*$", block, re.M)
    if not match:
        return None
    return match.group(1).strip()


def parse_existing_group_blocks(report_text: str) -> dict[str, dict[str, str]]:
    result: dict[str, dict[str, str]] = {}
    for match in GROUP_BLOCK_RE.finditer(report_text):
        group_id = match.group("group_id")
        title = (match.group("title") or "").strip()
        body = match.group("body")
        values: dict[str, str] = {}
        for value_match in REPORT_VALUE_RE.finditer(body):
            values[value_match.group("field").strip()] = value_match.group("value").strip()
        if title:
            values["_report_title"] = title
        result[group_id] = values
    return result


def parse_handoff_values(report_text: str) -> dict[str, Any]:
    match = HANDOFF_BLOCK_RE.search(report_text)
    if not match:
        return {}
    block = match.group(0)
    values: dict[str, Any] = {}
    upstream_paths_match = re.search(r"^upstream_paths:\s*$\n(?P<items>(?:- .*\n?)*)", block, re.M)
    if upstream_paths_match:
        items = [
            line.strip()[2:].strip().strip("`")
            for line in upstream_paths_match.group("items").splitlines()
            if line.strip().startswith("- ")
        ]
        values["upstream_paths"] = items
    for value_match in REPORT_VALUE_RE.finditer(block):
        values[value_match.group("field").strip()] = value_match.group("value").strip()
    return values


def default_window_status(group_metric: dict[str, Any]) -> str:
    effective_chars = int(group_metric["effective_text_chars"])
    if effective_chars < int(group_metric["warn_low"]):
        return "pass_low_anchor"
    if effective_chars > int(group_metric["warn_high"]):
        return "pass_high_preserve"
    return "pass"


def default_judgement_basis(window_status: str) -> str:
    if window_status == "pass_low_anchor":
        return "低于 warn_low；已触发并组检查，需补充独立信息落点、锁定依据或不可并原因。"
    if window_status == "pass_high_preserve":
        return "高于 warn_high，但未超 hard_text_window；已触发拆分检查，需补充不可拆、连续峰值或保留依据。"
    return "位于 warn_window 内。"


def default_source_span(group_id: str) -> str:
    return f"<待补 source_span for {group_id}>"


def resolve_handoff_value(existing_handoff: dict[str, Any], field_name: str, fallback: str) -> str:
    value = existing_handoff.get(field_name)
    if isinstance(value, str) and value.strip():
        return value.strip()
    return fallback


def resolve_upstream_paths(grouped_script_path: Path, frontmatter: dict[str, str], existing_handoff: dict[str, Any]) -> list[str]:
    existing_paths = existing_handoff.get("upstream_paths")
    if isinstance(existing_paths, list) and existing_paths:
        return [str(item) for item in existing_paths]

    project_root = grouped_script_path.parents[2]
    candidate_paths = [
        frontmatter.get("上游主稿", ""),
        str(project_root / "1-Planning" / "episode-split-plan.json"),
        str(project_root / "0-Init" / "north_star.yaml"),
        str(project_root / "0-Init" / "init_handoff.yaml"),
    ]
    return [path for path in candidate_paths if path]


def render_group_block(
    *,
    title: str,
    group_metric: dict[str, Any],
    existing_values: dict[str, str],
) -> str:
    source_span = existing_values.get("source_span") or group_metric.get("source_span") or default_source_span(group_metric["group_id"])
    window_status = existing_values.get("window_status") or default_window_status(group_metric)
    judgement_basis = existing_values.get("judgement_basis") or default_judgement_basis(window_status)
    lines = [
        f"### 【{group_metric['group_id']}】 {title}".rstrip(),
        f"source_span: `{source_span}`",
        f"estimated_duration_seconds: `{group_metric['resolved_duration_seconds']}秒`",
        f"effective_text_chars: `{group_metric['effective_text_chars']}`",
        f"window_status: `{window_status}`",
        f"judgement_basis: `{judgement_basis}`",
        f"quantization_trace: `{group_metric['quantization_trace']}`",
    ]
    return "\n".join(lines)


def render_handoff_block(
    *,
    grouped_script_path: Path,
    frontmatter: dict[str, str],
    episode_label: str,
    group_metrics: list[dict[str, Any]],
    existing_handoff: dict[str, Any],
) -> str:
    group_order = " -> ".join(group["group_id"] for group in group_metrics)
    group_count = len(group_metrics)
    project_root = grouped_script_path.parents[2]
    default_handoff_summary = f"{episode_label}已形成 {group_count} 组 grouped script，并按模板回写执行报告。"
    upstream_paths = resolve_upstream_paths(grouped_script_path, frontmatter, existing_handoff)
    duration_policy = resolve_handoff_value(
        existing_handoff,
        "duration_policy",
        frontmatter.get("duration_policy", "默认15秒；若无显式上游时长证据则不偏离"),
    )
    pace_tier = resolve_handoff_value(
        existing_handoff,
        "pace_tier",
        frontmatter.get("pace_tier", "中节奏"),
    )
    handoff_summary = resolve_handoff_value(
        existing_handoff,
        "handoff_summary",
        default_handoff_summary,
    )
    bootstrap_output = resolve_handoff_value(
        existing_handoff,
        "bootstrap_output",
        str(project_root / "2-Global" / "导演意图.md"),
    )
    lines = [
        "## handoff 摘要",
        "",
        f"episode_id: `{episode_label}`",
        f"group_count: `{group_count}`",
        f"group_order: `{group_order}`",
        f"locked_anchor_ids: `{existing_handoff.get('locked_anchor_ids', '[]')}`",
        f"duration_policy: `{duration_policy}`",
        f"pace_tier: `{pace_tier}`",
        f"handoff_summary: `{handoff_summary}`",
        f"bootstrap_output: `{bootstrap_output}`",
        "upstream_paths:",
    ]
    lines.extend(f"- `{path}`" for path in upstream_paths)
    return "\n".join(lines)


def render_report(grouped_script_path: Path, report_path: Path) -> str:
    ensure_template_exists()
    text = grouped_script_path.read_text(encoding="utf-8")
    frontmatter, body = parse_frontmatter(text)
    group_sections = parse_group_sections(body)
    metrics_payload = build_quantization_result(grouped_script_path, report_path if report_path.exists() else None)
    metric_by_group = {item["group_id"]: item for item in metrics_payload["groups"]}

    existing_report_text = report_path.read_text(encoding="utf-8") if report_path.exists() else ""
    existing_blocks = parse_existing_group_blocks(existing_report_text)
    existing_handoff = parse_handoff_values(existing_report_text)
    episode_label = frontmatter.get("集数", grouped_script_path.stem)

    blocks = [REPORT_TITLE, "", f"## {episode_label}", ""]
    for section in group_sections:
        group_metric = metric_by_group[section.group_id]
        title = section.title or existing_blocks.get(section.group_id, {}).get("_report_title", "")
        blocks.append(
            render_group_block(
                title=title,
                group_metric=group_metric,
                existing_values=existing_blocks.get(section.group_id, {}),
            )
        )
        blocks.append("")

    blocks.append(
        render_handoff_block(
            grouped_script_path=grouped_script_path,
            frontmatter=frontmatter,
            episode_label=episode_label,
            group_metrics=metrics_payload["groups"],
            existing_handoff=existing_handoff,
        )
    )
    blocks.append("")
    return "\n".join(blocks)


def merge_episode_report(existing_report_text: str, rendered_episode_report: str, episode_label: str) -> str:
    current_match = re.search(rf"^##\s*{re.escape(episode_label)}\s*$.*\Z", rendered_episode_report, re.M | re.S)
    if current_match is None:
        return rendered_episode_report
    current_block = current_match.group(0).strip()

    blocks: dict[int, str] = {}
    for match in EPISODE_BLOCK_RE.finditer(existing_report_text):
        episode_no = int(match.group("episode"))
        if f"第{episode_no}集" != episode_label:
            blocks[episode_no] = match.group(0).strip()

    episode_no_match = re.search(r"第(\d+)集", episode_label)
    if episode_no_match is None:
        return rendered_episode_report
    blocks[int(episode_no_match.group(1))] = current_block

    merged_blocks = [blocks[key] for key in sorted(blocks)]
    return REPORT_TITLE + "\n\n" + "\n\n".join(merged_blocks).rstrip() + "\n"


def main() -> int:
    args = parse_args()
    grouped_script_path = Path(args.input)
    report_path = Path(args.report) if args.report else grouped_script_path.parent / "执行报告.md"
    try:
        rendered = render_report(grouped_script_path, report_path)
        frontmatter, _body = parse_frontmatter(grouped_script_path.read_text(encoding="utf-8"))
        episode_label = frontmatter.get("集数", grouped_script_path.stem)
        if report_path.exists():
            rendered = merge_episode_report(report_path.read_text(encoding="utf-8"), rendered, episode_label)
    except Exception as exc:  # noqa: BLE001
        print(str(exc), file=sys.stderr)
        return 1

    if args.dry_run:
        print(rendered)
        return 0

    report_path.write_text(rendered, encoding="utf-8")
    print(f"已按模板回写执行报告: {report_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
