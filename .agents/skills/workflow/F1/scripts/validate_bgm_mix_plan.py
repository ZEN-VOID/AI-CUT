#!/usr/bin/env python3
"""Validate F1 background-music mix plans."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any


MAX_SYNC_DELTA_SEC = 0.35
MAX_BGM_VOLUME_DB = -6.0
MIN_COVERAGE_RATIO = 0.92


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def require_text(item: dict, field: str, errors: list[str], prefix: str) -> None:
    if not str(item.get(field, "")).strip():
        errors.append(f"{prefix}: missing {field}")


def require_any_text(item: dict, fields: tuple[str, ...], errors: list[str], prefix: str) -> None:
    for field in fields:
        value = item.get(field)
        if isinstance(value, dict) and value:
            return
        if isinstance(value, list) and value:
            return
        if str(value or "").strip():
            return
    errors.append(f"{prefix}: missing one of {', '.join(fields)}")


def read_number(item: dict, fields: tuple[str, ...]) -> float | None:
    for field in fields:
        value = item.get(field)
        if isinstance(value, (int, float)):
            return float(value)
        if isinstance(value, str):
            text = value.strip()
            for suffix in ("dB", "DB", "db", "s", "sec", "秒"):
                if text.endswith(suffix):
                    text = text[: -len(suffix)].strip()
                    break
            try:
                return float(text)
            except ValueError:
                continue
    return None


def require_positive_number(item: dict, fields: tuple[str, ...], errors: list[str], prefix: str) -> float | None:
    value = read_number(item, fields)
    if value is None:
        errors.append(f"{prefix}: missing one of {', '.join(fields)}")
        return None
    if value <= 0:
        errors.append(f"{prefix}: non-positive {fields[0]}")
    return value


def span_from_fields(item: dict, start_fields: tuple[str, ...], end_fields: tuple[str, ...]) -> tuple[float, float] | None:
    start = read_number(item, start_fields)
    end = read_number(item, end_fields)
    if start is None or end is None:
        return None
    return start, end


def check_rhythm_match(segment: dict, errors: list[str], prefix: str) -> None:
    rhythm_match = segment.get("rhythm_match")
    if not isinstance(rhythm_match, dict):
        errors.append(f"{prefix}: rhythm_match must be an object")
        return
    require_any_text(
        rhythm_match,
        ("visual_cut_sync", "beat_sync", "energy_match", "sync_evidence"),
        errors,
        f"{prefix}.rhythm_match",
    )
    max_delta = read_number(rhythm_match, ("max_sync_delta_sec", "max_delta_sec", "cut_beat_delta_sec"))
    if max_delta is None:
        errors.append(f"{prefix}.rhythm_match: missing max_sync_delta_sec")
    elif max_delta > MAX_SYNC_DELTA_SEC:
        errors.append(
            f"{prefix}.rhythm_match: max_sync_delta_sec {max_delta:g}s exceeds {MAX_SYNC_DELTA_SEC:g}s"
        )


def check_mix_policy(plan: dict, errors: list[str], prefix: str) -> None:
    if plan.get("voiceover_priority") is not True:
        errors.append(f"{prefix}: voiceover_priority must be true")
    mix_policy = plan.get("mix_policy")
    if not isinstance(mix_policy, dict):
        errors.append(f"{prefix}: mix_policy must be an object")
        return
    require_any_text(mix_policy, ("ducking", "sidechain_ducking", "voiceover_ducking"), errors, f"{prefix}.mix_policy")
    volume_db = read_number(mix_policy, ("bed_volume_db", "volume_db", "target_gain_db"))
    if volume_db is None:
        errors.append(f"{prefix}.mix_policy: missing bed_volume_db/volume_db/target_gain_db")
    elif volume_db > MAX_BGM_VOLUME_DB:
        errors.append(f"{prefix}.mix_policy: BGM volume {volume_db:g}dB is louder than {MAX_BGM_VOLUME_DB:g}dB")
    require_any_text(mix_policy, ("loudness_target", "target_lufs", "peak_limit_db"), errors, f"{prefix}.mix_policy")


def validate(path: Path, require_bgm: bool = False) -> dict:
    data = load_json(path)
    errors: list[str] = []

    if not isinstance(data, dict):
        return {"path": str(path), "ok": False, "errors": ["plan must be a JSON object"]}

    plan = data.get("background_music", data)
    if require_bgm and not plan:
        errors.append("missing required background_music plan")
    if not isinstance(plan, dict):
        errors.append("background_music plan must be an object")
        plan = {}

    enabled = plan.get("enabled", True)
    if enabled is False:
        if require_bgm:
            errors.append("background_music is disabled but --require-bgm was used")
        return {"path": str(path), "ok": not errors, "background_music_enabled": False, "errors": errors}

    prefix = "background_music"
    require_text(plan, "source_file", errors, prefix)
    require_any_text(plan, ("source_probe", "source_duration_sec", "media"), errors, prefix)
    if plan.get("source_has_audio") is False:
        errors.append(f"{prefix}: source_has_audio must not be false")
    final_duration = require_positive_number(
        plan,
        ("final_duration_sec", "output_duration_sec", "target_duration_sec"),
        errors,
        prefix,
    )
    check_mix_policy(plan, errors, prefix)

    segments = plan.get("segments")
    if not isinstance(segments, list) or not segments:
        errors.append(f"{prefix}: segments must be a non-empty list")
        segments = []

    last_target_end: float | None = None
    covered_duration = 0.0
    for index, segment in enumerate(segments, 1):
        segment_prefix = f"{prefix}.segments[{index}]"
        if not isinstance(segment, dict):
            errors.append(f"{segment_prefix}: not an object")
            continue
        require_text(segment, "id", errors, segment_prefix)
        source_span = span_from_fields(
            segment,
            ("source_start", "source_start_sec"),
            ("source_end", "source_end_sec"),
        )
        target_span = span_from_fields(
            segment,
            ("target_start", "target_start_sec"),
            ("target_end", "target_end_sec"),
        )
        if source_span is None:
            errors.append(f"{segment_prefix}: missing source_start/source_end")
        elif source_span[1] <= source_span[0]:
            errors.append(f"{segment_prefix}: non-positive source span")
        if target_span is None:
            errors.append(f"{segment_prefix}: missing target_start/target_end")
        else:
            if target_span[1] <= target_span[0]:
                errors.append(f"{segment_prefix}: non-positive target span")
            else:
                covered_duration += target_span[1] - target_span[0]
            if final_duration is not None and target_span[1] > final_duration + 0.25:
                errors.append(f"{segment_prefix}: target_end exceeds final duration")
            if last_target_end is not None and target_span[0] < last_target_end - 0.05:
                errors.append(f"{segment_prefix}: target span overlaps previous BGM segment")
            last_target_end = target_span[1]
        require_text(segment, "selection_reason", errors, segment_prefix)
        require_any_text(segment, ("visual_sync_points", "sync_points", "cut_points"), errors, segment_prefix)
        require_any_text(segment, ("fade_in_sec", "fade_in", "transition_in"), errors, segment_prefix)
        require_any_text(segment, ("fade_out_sec", "fade_out", "transition_out"), errors, segment_prefix)
        require_any_text(segment, ("loop_policy", "extend_policy", "repeat_policy"), errors, segment_prefix)
        require_any_text(segment, ("ducking", "ducking_policy", "sidechain"), errors, segment_prefix)
        check_rhythm_match(segment, errors, segment_prefix)
        volume_db = read_number(segment, ("volume_db", "gain_db", "bed_volume_db"))
        if volume_db is not None and volume_db > MAX_BGM_VOLUME_DB:
            errors.append(f"{segment_prefix}: BGM segment volume {volume_db:g}dB is louder than {MAX_BGM_VOLUME_DB:g}dB")
        if segment.get("verdict") != "pass":
            errors.append(f"{segment_prefix}: verdict is {segment.get('verdict')!r}")

    if final_duration is not None and segments:
        coverage_policy = str(plan.get("coverage_policy", "")).strip()
        if covered_duration < final_duration * MIN_COVERAGE_RATIO and coverage_policy != "intentional_gaps":
            errors.append(
                f"{prefix}: BGM target coverage {covered_duration:.2f}s is below "
                f"{MIN_COVERAGE_RATIO:.0%} of final duration {final_duration:.2f}s"
            )

    return {
        "path": str(path),
        "ok": not errors,
        "background_music_enabled": enabled is not False,
        "segment_count": len(segments),
        "errors": errors,
    }


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("plan", type=Path)
    parser.add_argument("--require-bgm", action="store_true")
    args = parser.parse_args(argv[1:])

    try:
        report = validate(args.plan, require_bgm=args.require_bgm)
    except Exception as exc:  # pragma: no cover - CLI guard
        report = {"path": str(args.plan), "ok": False, "errors": [str(exc)]}
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0 if report["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
