#!/usr/bin/env python3
"""Validate an F1 视频说明.yaml manifest."""

from __future__ import annotations

import argparse
import json
import shutil
import subprocess
from pathlib import Path
from typing import Any

import yaml


TOP_LEVEL_REQUIRED = [
    "schema_version",
    "manifest_id",
    "manifest_name",
    "base_dir",
    "purpose",
    "consumer_contract",
    "field_model",
    "global_editing_policy",
    "videos",
]

VIDEO_REQUIRED = [
    "id",
    "file",
    "category",
    "role",
    "media",
    "content_profile",
    "selection_profile",
    "splicing_profile",
    "subtitle_safe_zone",
    "segments",
]

MEDIA_REQUIRED = ["duration_sec", "fps", "resolution", "codec", "has_audio"]
CONTENT_REQUIRED = [
    "visual_summary",
    "visual_density",
    "motion_level",
]
SELECTION_REQUIRED = ["best_for", "avoid_for", "keyword_triggers"]
SPLICING_REQUIRED = ["preferred_clip_sec", "entry_affordance", "exit_affordance"]
SAFE_ZONE_REQUIRED = ["risk_level", "recommended_f1_position"]
SEGMENT_REQUIRED = [
    "segment_id",
    "start",
    "end",
    "duration_sec",
    "visual_content",
    "semantic_tags",
    "shot_type",
    "motion",
    "action_intensity",
    "text_overlay",
    "best_for",
    "avoid_for",
    "splice_notes",
]

VALID_CATEGORIES = {
    "operation_demo",
    "tool_display",
    "aigc_content",
    "reference_only",
    "other",
    "needs_llm",
}

DIRECTORY_CATEGORY_HINTS = {
    "操作展示": "operation_demo",
    "工具使用": "tool_display",
    "影像内容": "aigc_content",
}


def parse_time(value: Any) -> float:
    if isinstance(value, (int, float)):
        return float(value)
    text = str(value).strip()
    parts = text.split(":")
    try:
        if len(parts) == 1:
            return float(parts[0])
        if len(parts) == 2:
            minutes, seconds = parts
            return int(minutes) * 60 + float(seconds)
        if len(parts) == 3:
            hours, minutes, seconds = parts
            return int(hours) * 3600 + int(minutes) * 60 + float(seconds)
    except ValueError as exc:
        raise ValueError(f"invalid timestamp: {value}") from exc
    raise ValueError(f"invalid timestamp: {value}")


def add_missing(errors: list[str], obj: dict[str, Any], keys: list[str], prefix: str) -> None:
    for key in keys:
        if key not in obj or obj.get(key) in (None, ""):
            errors.append(f"{prefix}.{key} missing")


def ffprobe_duration(path: Path) -> float | None:
    if shutil.which("ffprobe") is None:
        return None
    result = subprocess.run(
        [
            "ffprobe",
            "-v",
            "error",
            "-show_entries",
            "format=duration",
            "-of",
            "default=noprint_wrappers=1:nokey=1",
            str(path),
        ],
        text=True,
        capture_output=True,
        check=False,
    )
    if result.returncode != 0:
        return None
    try:
        return float(result.stdout.strip())
    except ValueError:
        return None


def category_hint_from_path(file_value: str) -> str | None:
    parts = Path(file_value).parts
    for part in parts:
        if part in DIRECTORY_CATEGORY_HINTS:
            return DIRECTORY_CATEGORY_HINTS[part]
    return None


def has_category_mismatch_note(video: dict[str, Any]) -> bool:
    evidence = video.get("evidence") if isinstance(video.get("evidence"), dict) else {}
    note_fields = [
        video.get("category_mismatch_reason"),
        video.get("classification_notes"),
        evidence.get("category_mismatch_reason"),
        evidence.get("classification_notes"),
    ]
    return any(bool(value) for value in note_fields)


def validate_manifest(
    manifest_path: Path,
    base_dir_override: Path | None,
    tolerance_sec: float,
    skip_media_check: bool,
) -> dict[str, Any]:
    errors: list[str] = []
    warnings: list[str] = []

    data = yaml.safe_load(manifest_path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        return {"status": "fail", "errors": ["manifest root must be a mapping"], "warnings": warnings}

    add_missing(errors, data, TOP_LEVEL_REQUIRED, "manifest")
    if data.get("schema_version") != 2:
        warnings.append("manifest.schema_version is not 2")

    videos = data.get("videos")
    if not isinstance(videos, list) or not videos:
        errors.append("manifest.videos must be a non-empty list")
        videos = []

    base_value = base_dir_override or Path(str(data.get("base_dir", manifest_path.parent)))
    if not base_value.is_absolute():
        base_dir = (Path.cwd() / base_value).resolve()
    else:
        base_dir = base_value

    seen_ids: set[str] = set()
    seen_segments: set[str] = set()
    for index, video in enumerate(videos):
        prefix = f"videos[{index}]"
        if not isinstance(video, dict):
            errors.append(f"{prefix} must be a mapping")
            continue
        add_missing(errors, video, VIDEO_REQUIRED, prefix)
        video_id = str(video.get("id", ""))
        if video_id in seen_ids:
            errors.append(f"{prefix}.id duplicate: {video_id}")
        seen_ids.add(video_id)

        category = video.get("category")
        if category not in VALID_CATEGORIES:
            warnings.append(f"{prefix}.category unknown: {category}")
        if category == "needs_llm":
            errors.append(f"{prefix}.category still contains needs_llm placeholder")
        file_value = str(video.get("file", ""))
        category_hint = category_hint_from_path(file_value)
        if category_hint and category != category_hint and not has_category_mismatch_note(video):
            warnings.append(
                f"{prefix}.category {category!r} conflicts with directory hint {category_hint!r}; "
                "add category_mismatch_reason or correct the category"
            )

        media = video.get("media") if isinstance(video.get("media"), dict) else {}
        add_missing(errors, media, MEDIA_REQUIRED, f"{prefix}.media")
        content = video.get("content_profile") if isinstance(video.get("content_profile"), dict) else {}
        add_missing(errors, content, CONTENT_REQUIRED, f"{prefix}.content_profile")
        selection = video.get("selection_profile") if isinstance(video.get("selection_profile"), dict) else {}
        add_missing(errors, selection, SELECTION_REQUIRED, f"{prefix}.selection_profile")
        splicing = video.get("splicing_profile") if isinstance(video.get("splicing_profile"), dict) else {}
        add_missing(errors, splicing, SPLICING_REQUIRED, f"{prefix}.splicing_profile")
        safe_zone = video.get("subtitle_safe_zone") if isinstance(video.get("subtitle_safe_zone"), dict) else {}
        add_missing(errors, safe_zone, SAFE_ZONE_REQUIRED, f"{prefix}.subtitle_safe_zone")
        if safe_zone.get("risk_level") == "high" and not safe_zone.get("notes"):
            warnings.append(f"{prefix}.subtitle_safe_zone high risk should include notes")

        video_path = base_dir / file_value if file_value else None
        if not skip_media_check:
            if not video_path or not video_path.exists():
                errors.append(f"{prefix}.file not found: {file_value}")
            else:
                actual_duration = ffprobe_duration(video_path)
                expected = media.get("duration_sec")
                if actual_duration is not None and isinstance(expected, (int, float)):
                    if abs(float(expected) - actual_duration) > tolerance_sec:
                        errors.append(
                            f"{prefix}.media.duration_sec mismatch: manifest={expected}, ffprobe={actual_duration:.3f}"
                        )

        segments = video.get("segments")
        if not isinstance(segments, list) or not segments:
            errors.append(f"{prefix}.segments must be a non-empty list")
            continue
        video_duration = media.get("duration_sec") if isinstance(media.get("duration_sec"), (int, float)) else None
        for seg_index, segment in enumerate(segments):
            seg_prefix = f"{prefix}.segments[{seg_index}]"
            if not isinstance(segment, dict):
                errors.append(f"{seg_prefix} must be a mapping")
                continue
            add_missing(errors, segment, SEGMENT_REQUIRED, seg_prefix)
            segment_id = str(segment.get("segment_id", ""))
            if segment_id in seen_segments:
                errors.append(f"{seg_prefix}.segment_id duplicate: {segment_id}")
            seen_segments.add(segment_id)
            try:
                start = parse_time(segment.get("start"))
                end = parse_time(segment.get("end"))
                declared = float(segment.get("duration_sec"))
                if end <= start:
                    errors.append(f"{seg_prefix}.end must be greater than start")
                if abs((end - start) - declared) > tolerance_sec:
                    errors.append(
                        f"{seg_prefix}.duration_sec mismatch: declared={declared}, range={end - start:.3f}"
                    )
                if video_duration is not None and end > float(video_duration) + tolerance_sec:
                    errors.append(f"{seg_prefix}.end exceeds video duration")
            except Exception as exc:  # noqa: BLE001
                errors.append(f"{seg_prefix}.time invalid: {exc}")
            if category == "tool_display" and not segment.get("tool_state"):
                warnings.append(f"{seg_prefix}.tool_state recommended for tool_display")
            if category == "tool_display" and segment.get("tool_state") == "needs_llm":
                errors.append(f"{seg_prefix}.tool_state still contains needs_llm placeholder")
            if category == "operation_demo" and not segment.get("operation_state"):
                warnings.append(f"{seg_prefix}.operation_state recommended for operation_demo")
            if category == "operation_demo" and segment.get("operation_state") == "needs_llm":
                errors.append(f"{seg_prefix}.operation_state still contains needs_llm placeholder")
            if segment.get("visual_content") == "needs_llm" or segment.get("semantic_tags") == ["needs_llm"]:
                errors.append(f"{seg_prefix} still contains needs_llm placeholders")

    status = "pass" if not errors else "fail"
    return {
        "status": status,
        "fatal_count": len(errors),
        "warning_count": len(warnings),
        "errors": errors,
        "warnings": warnings,
        "manifest": str(manifest_path),
        "base_dir": str(base_dir),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("manifest", help="Path to 视频说明.yaml")
    parser.add_argument("--base-dir", help="Override manifest base_dir")
    parser.add_argument("--tolerance-sec", type=float, default=0.25)
    parser.add_argument("--skip-media-check", action="store_true", help="Validate schema without checking video files.")
    parser.add_argument("--strict", action="store_true", help="Treat warnings as failure.")
    parser.add_argument("--report", help="Write JSON validation report.")
    args = parser.parse_args()

    manifest_path = Path(args.manifest).expanduser().resolve()
    base_dir = Path(args.base_dir).expanduser().resolve() if args.base_dir else None
    result = validate_manifest(manifest_path, base_dir, args.tolerance_sec, args.skip_media_check)
    if args.strict and result["warnings"] and result["status"] == "pass":
        result["status"] = "fail"
        result["errors"].append("strict mode treats warnings as failure")
        result["fatal_count"] = len(result["errors"])

    output = json.dumps(result, ensure_ascii=False, indent=2)
    if args.report:
        report_path = Path(args.report).expanduser().resolve()
        report_path.parent.mkdir(parents=True, exist_ok=True)
        report_path.write_text(output, encoding="utf-8")
    print(output)
    return 0 if result["status"] == "pass" else 1


if __name__ == "__main__":
    raise SystemExit(main())
