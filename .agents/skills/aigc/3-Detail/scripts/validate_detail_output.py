#!/usr/bin/env python3
"""Validate `3-Detail` episode JSON against authoritative density quantization."""

from __future__ import annotations

import argparse
from collections import Counter
import json
import math
import re
import sys
from pathlib import Path

from detail_density_quantizer import DensityQuantizationError, build_quantization_result

EXACT_DUPLICATION_WATCH_FIELDS = (
    "角色背景面",
    "角色站位走位",
    "道具及状态",
    "角色表现",
    "场景氛围",
    "运镜手法",
    "摄影美学",
)
EXACT_DUPLICATION_FIELD_ALIASES = {
    "角色背景面": ("角色背景面", "场景及方位"),
    "角色站位走位": ("角色站位走位", "角色及站位和穿搭"),
}
EXACT_DUPLICATION_MIN_SHOTS = 3
EXACT_DUPLICATION_MAX_RATIO = 0.75
GROUP_COSTUME_SEPARATOR_RE = re.compile(r"[-—:：]")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="校验 `3-Detail` 输出是否符合 authoritative 分镜密度裁决。")
    parser.add_argument("--grouped-script", required=True, help="输入 grouped script 路径（第N集.md）")
    parser.add_argument("--episode-json", required=True, help="输入 `3-Detail/第N集.json` 路径")
    parser.add_argument("--json", action="store_true", help="输出 JSON")
    return parser.parse_args()


def normalize_text(value: object) -> str:
    if not isinstance(value, str):
        return ""
    return " ".join(value.split())


def resolve_watch_field_text(shot: dict[str, object], field: str) -> str:
    for candidate in EXACT_DUPLICATION_FIELD_ALIASES.get(field, (field,)):
        value = shot.get(candidate)
        if isinstance(value, str) and value.strip():
            return value
    return ""


def load_episode_payload(episode_json_path: Path) -> dict[str, object]:
    return json.loads(episode_json_path.read_text(encoding="utf-8"))


def load_episode_groups(payload: dict[str, object]) -> list[dict[str, object]]:
    return payload["final_output"]["main_content"]["分镜组列表"]


def build_exact_duplication_failures(groups: list[dict[str, object]]) -> list[dict[str, object]]:
    failures: list[dict[str, object]] = []
    min_repeat_count = math.ceil(EXACT_DUPLICATION_MIN_SHOTS * EXACT_DUPLICATION_MAX_RATIO)

    for group in groups:
        group_id = group["分镜组ID"]
        shots = group.get("分镜明细", [])
        if len(shots) < EXACT_DUPLICATION_MIN_SHOTS:
            continue

        for field in EXACT_DUPLICATION_WATCH_FIELDS:
            normalized_values: list[tuple[str, str]] = []
            for shot in shots:
                normalized = normalize_text(resolve_watch_field_text(shot, field))
                if not normalized:
                    continue
                normalized_values.append((normalized, shot.get("分镜ID", "")))

            if len(normalized_values) < EXACT_DUPLICATION_MIN_SHOTS:
                continue

            top_value, top_count = Counter(value for value, _ in normalized_values).most_common(1)[0]
            threshold = max(min_repeat_count, math.ceil(len(normalized_values) * EXACT_DUPLICATION_MAX_RATIO))
            if top_count < threshold:
                continue

            repeated_shot_ids = [shot_id for value, shot_id in normalized_values if value == top_value]
            failures.append(
                {
                    "group_id": group_id,
                    "error": "excessive_exact_duplication",
                    "field": field,
                    "repeated_shots": top_count,
                    "shot_count": len(normalized_values),
                    "threshold": threshold,
                    "sample_shot_ids": repeated_shot_ids[:8],
                    "sample_text": top_value[:120],
                }
            )

    return failures


def build_group_costume_failures(groups: list[dict[str, object]]) -> list[dict[str, object]]:
    failures: list[dict[str, object]] = []

    for group in groups:
        group_id = str(group.get("分镜组ID", "")).strip() or "unknown-group"
        shots = group.get("分镜明细", [])
        if not isinstance(shots, list) or not shots:
            continue

        group_design = group.get("组间设计", {})
        if not isinstance(group_design, dict):
            group_design = {}

        costume_summary = normalize_text(group_design.get("出场角色及穿搭"))
        if not costume_summary:
            failures.append(
                {
                    "group_id": group_id,
                    "error": "missing_group_costume_summary",
                    "field": "组间设计.出场角色及穿搭",
                    "shot_count": len(shots),
                }
            )
            continue

        if not GROUP_COSTUME_SEPARATOR_RE.search(costume_summary):
            failures.append(
                {
                    "group_id": group_id,
                    "error": "malformed_group_costume_summary",
                    "field": "组间设计.出场角色及穿搭",
                    "expected_format": "角色名-服装简述；角色名-服装简述",
                    "sample_text": costume_summary[:120],
                }
            )

    return failures


def main() -> int:
    args = parse_args()
    try:
        quantization = build_quantization_result(Path(args.grouped_script))
        payload = load_episode_payload(Path(args.episode_json))
        episode_groups = load_episode_groups(payload)
        actual_groups = {group["分镜组ID"]: len(group["分镜明细"]) for group in episode_groups}
    except (OSError, KeyError, json.JSONDecodeError, DensityQuantizationError) as exc:
        print(str(exc), file=sys.stderr)
        return 1

    failures: list[dict[str, object]] = []
    for group in quantization["groups"]:
        group_id = group["group_id"]
        expected = group["shot_count_decision"]
        actual = actual_groups.get(group_id)
        if actual is None:
            failures.append(
                {
                    "group_id": group_id,
                    "error": "missing_group",
                    "expected_shots": expected,
                }
            )
            continue
        if actual != expected:
            failures.append(
                {
                    "group_id": group_id,
                    "error": "shot_count_mismatch",
                    "expected_shots": expected,
                    "actual_shots": actual,
                    "why_not_fewer": group["why_not_fewer"],
                    "why_not_more": group["why_not_more"],
                }
            )

    extra_groups = sorted(set(actual_groups) - {group["group_id"] for group in quantization["groups"]})
    for group_id in extra_groups:
        failures.append(
            {
                "group_id": group_id,
                "error": "unexpected_group",
                "actual_shots": actual_groups[group_id],
            }
        )

    failures.extend(build_exact_duplication_failures(episode_groups))
    failures.extend(build_group_costume_failures(episode_groups))

    payload = {
        "episode_label": quantization["episode_label"],
        "pace_tier": quantization["pace_tier"],
        "status": "ok" if not failures else "fail",
        "failures": failures,
    }

    if args.json:
        print(json.dumps(payload, ensure_ascii=False, indent=2))
    else:
        print(f"{payload['episode_label']}: {payload['status']} (pace={payload['pace_tier']})")
        for failure in failures:
            print(json.dumps(failure, ensure_ascii=False))

    return 0 if not failures else 1


if __name__ == "__main__":
    raise SystemExit(main())
