#!/usr/bin/env python3
"""Validate a workflow 视频说明.yaml manifest."""

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
TOP_LEVEL_RECOMMENDED = [
    "material_pool_profile",
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
RECOMMENDED_DIVERSITY_FIELDS = [
    "semantic_vector",
    "trigger_profile",
    "visual_signature",
    "variation_profile",
]
BRANCH_VIDEO_FIELDS = [
    "material_branch",
    "branch_path",
    "workflow_role_hint",
    "layer_affinity",
]
BRANCH_SEGMENT_FIELDS = [
    "segment_role_fit",
    "content_subtype_fit",
    "selection_constraints",
]
GENERIC_TAGS = {
    "工具",
    "展示",
    "剧情",
    "素材",
    "画面",
    "视频",
    "内容",
    "操作",
    "场景",
}
LONG_VIDEO_THRESHOLD_SEC = 60.0
MAX_ANALYSIS_SLICE_SEC = 60.0

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
MATERIAL_BRANCH_HINTS = {
    "操作展示": {
        "material_branch": "legacy_operation_demo",
        "workflow_role_hint": "process_proof",
        "layer_affinity": ["background_video", "semantic_pip"],
        "content_subtype_hint": "operation_demo",
        "category_hint": "operation_demo",
        "category_confidence": "strong",
    },
    "工具使用": {
        "material_branch": "legacy_tool_display",
        "workflow_role_hint": "tool_proof",
        "layer_affinity": ["semantic_pip", "background_video"],
        "content_subtype_hint": "tool_display",
        "category_hint": "tool_display",
        "category_confidence": "strong",
    },
    "影像内容": {
        "material_branch": "legacy_aigc_content",
        "workflow_role_hint": "content_body",
        "layer_affinity": ["background_video"],
        "content_subtype_hint": "aigc_content",
        "category_hint": "aigc_content",
        "category_confidence": "strong",
    },
    "开头素材": {
        "material_branch": "opening_hook",
        "workflow_role_hint": "hook_opening",
        "layer_affinity": ["background_video", "hook_visual"],
        "content_subtype_hint": "high_energy_opening",
        "category_hint": "aigc_content",
        "category_confidence": "weak",
    },
    "收益素材": {
        "material_branch": "revenue_proof",
        "workflow_role_hint": "proof_point",
        "layer_affinity": ["semantic_pip", "background_video", "editorial_overlay"],
        "content_subtype_hint": "revenue_evidence",
        "category_hint": None,
        "category_confidence": "none",
    },
    "收益视频": {
        "material_branch": "revenue_proof",
        "workflow_role_hint": "proof_point",
        "layer_affinity": ["semantic_pip", "background_video"],
        "content_subtype_hint": "revenue_video",
        "category_hint": None,
        "category_confidence": "none",
    },
    "工作流素材": {
        "material_branch": "workflow_demo",
        "workflow_role_hint": "process_proof",
        "layer_affinity": ["semantic_pip", "background_video"],
        "content_subtype_hint": "workflow_process",
        "category_hint": "operation_demo",
        "category_confidence": "weak",
    },
    "工作流实拍": {
        "material_branch": "workflow_demo",
        "workflow_role_hint": "process_proof",
        "layer_affinity": ["background_video", "semantic_pip"],
        "content_subtype_hint": "workflow_real_shot",
        "category_hint": "operation_demo",
        "category_confidence": "weak",
    },
    "工作流网上素材": {
        "material_branch": "workflow_demo",
        "workflow_role_hint": "tool_proof",
        "layer_affinity": ["semantic_pip", "background_video"],
        "content_subtype_hint": "workflow_reference",
        "category_hint": "tool_display",
        "category_confidence": "weak",
    },
    "引流素材": {
        "material_branch": "private_traffic_cta",
        "workflow_role_hint": "private_traffic_cta",
        "layer_affinity": ["semantic_pip", "editorial_overlay", "background_video"],
        "content_subtype_hint": "cta_material",
        "category_hint": None,
        "category_confidence": "none",
    },
    "提示词方向": {
        "material_branch": "prompt_cta",
        "workflow_role_hint": "private_traffic_cta",
        "layer_affinity": ["editorial_overlay", "semantic_pip"],
        "content_subtype_hint": "prompt_offer",
        "category_hint": None,
        "category_confidence": "none",
    },
    "课程方向": {
        "material_branch": "course_cta",
        "workflow_role_hint": "private_traffic_cta",
        "layer_affinity": ["editorial_overlay", "semantic_pip"],
        "content_subtype_hint": "course_offer",
        "category_hint": None,
        "category_confidence": "none",
    },
    "漫剧素材": {
        "material_branch": "comic_drama",
        "workflow_role_hint": "content_body",
        "layer_affinity": ["background_video"],
        "content_subtype_hint": "comic_drama",
        "category_hint": "aigc_content",
        "category_confidence": "weak",
    },
    "纯漫剧素材": {
        "material_branch": "pure_comic_drama",
        "workflow_role_hint": "content_body",
        "layer_affinity": ["background_video"],
        "content_subtype_hint": "pure_comic_drama",
        "category_hint": "aigc_content",
        "category_confidence": "strong",
    },
    "漫剧账号录屏": {
        "material_branch": "comic_account_recording",
        "workflow_role_hint": "proof_point",
        "layer_affinity": ["semantic_pip", "background_video"],
        "content_subtype_hint": "account_recording",
        "category_hint": "tool_display",
        "category_confidence": "weak",
    },
    "大字报": {
        "material_branch": "editorial_overlay",
        "workflow_role_hint": "editorial_emphasis",
        "layer_affinity": ["editorial_overlay"],
        "content_subtype_hint": "big_text_card",
        "category_hint": None,
        "category_confidence": "none",
    },
    "转场素材": {
        "material_branch": "transition",
        "workflow_role_hint": "transition",
        "layer_affinity": ["transition"],
        "content_subtype_hint": "transition_effect",
        "category_hint": "aigc_content",
        "category_confidence": "weak",
    },
    "核心关键词": {
        "material_branch": "keyword_trigger",
        "workflow_role_hint": "keyword_anchor",
        "layer_affinity": ["editorial_overlay", "semantic_pip"],
        "content_subtype_hint": "keyword_trigger",
        "category_hint": None,
        "category_confidence": "none",
    },
    "资产图": {
        "material_branch": "asset_image_reference",
        "workflow_role_hint": "semantic_pip",
        "layer_affinity": ["semantic_pip"],
        "content_subtype_hint": "asset_reference",
        "category_hint": "reference_only",
        "category_confidence": "weak",
    },
}
STRICT_CONSUMERS = {"workflow-batch", "workflow-social-ad"}


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


def material_branch_profile_from_path(file_value: str) -> dict[str, Any]:
    profile: dict[str, Any] = {}
    matched_parts: list[str] = []
    parts = Path(file_value).parts
    for part in parts:
        branch_hint = MATERIAL_BRANCH_HINTS.get(part)
        if branch_hint:
            profile.update(branch_hint)
            matched_parts.append(part)
    if "引流素材" in parts and "工具" in parts:
        profile.update(
            {
                "material_branch": "tool_cta",
                "workflow_role_hint": "private_traffic_cta",
                "layer_affinity": ["semantic_pip", "editorial_overlay"],
                "content_subtype_hint": "tool_cta",
                "category_hint": "tool_display",
                "category_confidence": "weak",
            }
        )
        matched_parts.append("工具")
    if not profile:
        return {}
    profile["branch_path"] = "/".join(matched_parts)
    profile["branch_source"] = matched_parts[-1]
    strong_category = category_hint_from_path(file_value)
    if strong_category:
        profile["category_hint"] = strong_category
        profile["category_confidence"] = "strong"
    return profile


def has_category_mismatch_note(video: dict[str, Any]) -> bool:
    evidence = video.get("evidence") if isinstance(video.get("evidence"), dict) else {}
    note_fields = [
        video.get("category_mismatch_reason"),
        video.get("classification_notes"),
        evidence.get("category_mismatch_reason"),
        evidence.get("classification_notes"),
    ]
    return any(bool(value) for value in note_fields)


def has_branch_mismatch_note(video: dict[str, Any]) -> bool:
    evidence = video.get("evidence") if isinstance(video.get("evidence"), dict) else {}
    note_fields = [
        video.get("branch_mismatch_reason"),
        video.get("classification_notes"),
        evidence.get("branch_mismatch_reason"),
        evidence.get("classification_notes"),
    ]
    return any(bool(value) for value in note_fields)


def effective_semantic_tags(value: Any) -> list[str]:
    if not isinstance(value, list):
        return []
    tags = []
    for tag in value:
        text = str(tag).strip()
        if text and text != "needs_llm" and text not in GENERIC_TAGS:
            tags.append(text)
    return sorted(set(tags))


def has_mapping_value(value: Any) -> bool:
    return isinstance(value, dict) and any(item not in (None, "", [], "needs_llm") for item in value.values())


def has_list_value(value: Any) -> bool:
    return isinstance(value, list) and any(item not in (None, "", [], "needs_llm") for item in value)


def has_structured_value(value: Any) -> bool:
    if isinstance(value, dict):
        return has_mapping_value(value)
    if isinstance(value, list):
        return has_list_value(value)
    return value not in (None, "", "needs_llm")


def add_quality_issue(errors: list[str], warnings: list[str], message: str, fatal: bool) -> None:
    if fatal:
        errors.append(message)
    else:
        warnings.append(message)


def validate_manifest(
    manifest_path: Path,
    base_dir_override: Path | None,
    tolerance_sec: float,
    skip_media_check: bool,
    consumer_profile: str,
) -> dict[str, Any]:
    errors: list[str] = []
    warnings: list[str] = []
    strict_consumer = consumer_profile in STRICT_CONSUMERS

    data = yaml.safe_load(manifest_path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        return {"status": "fail", "errors": ["manifest root must be a mapping"], "warnings": warnings}

    add_missing(errors, data, TOP_LEVEL_REQUIRED, "manifest")
    for key in TOP_LEVEL_RECOMMENDED:
        if key not in data or data.get(key) in (None, "", []):
            warnings.append(f"manifest.{key} recommended for branch-aware projects/素材 material pools")
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
        branch_profile = material_branch_profile_from_path(file_value)
        if branch_profile:
            expected_branch = branch_profile.get("material_branch")
            actual_branch = video.get("material_branch")
            for field in BRANCH_VIDEO_FIELDS:
                if field == "layer_affinity":
                    present = has_list_value(video.get(field))
                else:
                    present = has_structured_value(video.get(field))
                if not present:
                    add_quality_issue(
                        errors,
                        warnings,
                        f"{prefix}.{field} recommended for branch-aware material pool path {branch_profile.get('branch_path')!r}",
                        fatal=strict_consumer,
                    )
            if actual_branch and actual_branch != expected_branch and not has_branch_mismatch_note(video):
                add_quality_issue(
                    errors,
                    warnings,
                    f"{prefix}.material_branch {actual_branch!r} conflicts with path hint {expected_branch!r}; "
                    "add branch_mismatch_reason or correct the branch",
                    fatal=strict_consumer,
                )
            expected_role = branch_profile.get("workflow_role_hint")
            actual_role = video.get("workflow_role_hint")
            if actual_role and expected_role and actual_role != expected_role and not has_branch_mismatch_note(video):
                warnings.append(
                    f"{prefix}.workflow_role_hint {actual_role!r} differs from path hint {expected_role!r}; "
                    "keep only with visual or user-hint evidence"
                )
            branch_category_hint = branch_profile.get("category_hint")
            if (
                branch_category_hint
                and branch_profile.get("category_confidence") == "strong"
                and category != branch_category_hint
                and not has_category_mismatch_note(video)
            ):
                add_quality_issue(
                    errors,
                    warnings,
                    f"{prefix}.category {category!r} conflicts with strong material branch category hint "
                    f"{branch_category_hint!r}",
                    fatal=strict_consumer,
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

        video_duration = media.get("duration_sec") if isinstance(media.get("duration_sec"), (int, float)) else None
        analysis_slices = video.get("analysis_slices")
        if video_duration is not None and float(video_duration) > LONG_VIDEO_THRESHOLD_SEC:
            if not isinstance(analysis_slices, list) or not analysis_slices:
                add_quality_issue(
                    errors,
                    warnings,
                    f"{prefix}.analysis_slices recommended for videos longer than {LONG_VIDEO_THRESHOLD_SEC:.0f}s",
                    fatal=strict_consumer,
                )
            else:
                for slice_index, analysis_slice in enumerate(analysis_slices):
                    slice_prefix = f"{prefix}.analysis_slices[{slice_index}]"
                    if not isinstance(analysis_slice, dict):
                        warnings.append(f"{slice_prefix} should be a mapping")
                        continue
                    for key in ["slice_id", "source_file", "start", "end", "duration_sec", "sample_frames"]:
                        if key not in analysis_slice or analysis_slice.get(key) in (None, "", []):
                            warnings.append(f"{slice_prefix}.{key} recommended")
                    try:
                        slice_start = parse_time(analysis_slice.get("start"))
                        slice_end = parse_time(analysis_slice.get("end"))
                        slice_duration = float(analysis_slice.get("duration_sec"))
                        if slice_end <= slice_start:
                            warnings.append(f"{slice_prefix}.end should be greater than start")
                        if slice_duration > MAX_ANALYSIS_SLICE_SEC + tolerance_sec:
                            warnings.append(
                                f"{slice_prefix}.duration_sec exceeds {MAX_ANALYSIS_SLICE_SEC:.0f}s"
                            )
                    except Exception as exc:  # noqa: BLE001
                        warnings.append(f"{slice_prefix}.time invalid: {exc}")

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
                if declared > LONG_VIDEO_THRESHOLD_SEC:
                    warnings.append(f"{seg_prefix}.duration_sec exceeds {LONG_VIDEO_THRESHOLD_SEC:.0f}s")
                if video_duration is not None and end > float(video_duration) + tolerance_sec:
                    errors.append(f"{seg_prefix}.end exceeds video duration")
            except Exception as exc:  # noqa: BLE001
                errors.append(f"{seg_prefix}.time invalid: {exc}")
            effective_tags = effective_semantic_tags(segment.get("semantic_tags"))
            if len(effective_tags) < 3:
                add_quality_issue(
                    errors,
                    warnings,
                    f"{seg_prefix}.semantic_tags should include at least 3 non-generic tags",
                    fatal=strict_consumer,
                )
            for field in RECOMMENDED_DIVERSITY_FIELDS:
                if not has_mapping_value(segment.get(field)):
                    add_quality_issue(
                        errors,
                        warnings,
                        f"{seg_prefix}.{field} recommended for workflow batch diversity",
                        fatal=strict_consumer,
                    )
            if branch_profile:
                for field in BRANCH_SEGMENT_FIELDS:
                    if not has_structured_value(segment.get(field)):
                        add_quality_issue(
                            errors,
                            warnings,
                            f"{seg_prefix}.{field} recommended for branch-aware workflow matching",
                            fatal=strict_consumer,
                        )
                role_fit = segment.get("segment_role_fit")
                expected_role = branch_profile.get("workflow_role_hint")
                if isinstance(role_fit, list) and expected_role and expected_role not in role_fit:
                    warnings.append(
                        f"{seg_prefix}.segment_role_fit does not include path role hint {expected_role!r}"
                    )
            if video_duration is not None and float(video_duration) > LONG_VIDEO_THRESHOLD_SEC:
                if not segment.get("analysis_slice_id"):
                    add_quality_issue(
                        errors,
                        warnings,
                        f"{seg_prefix}.analysis_slice_id recommended for long-source videos",
                        fatal=strict_consumer,
                    )
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
        "consumer_profile": consumer_profile,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("manifest", help="Path to 视频说明.yaml")
    parser.add_argument("--base-dir", help="Override manifest base_dir")
    parser.add_argument("--tolerance-sec", type=float, default=0.25)
    parser.add_argument("--skip-media-check", action="store_true", help="Validate schema without checking video files.")
    parser.add_argument(
        "--consumer",
        choices=["generic", "workflow", "workflow-batch", "workflow-social-ad"],
        default="workflow",
        help="Downstream consumer profile. Batch/social-ad modes promote branch and diversity gaps to fatal errors.",
    )
    parser.add_argument("--strict", action="store_true", help="Treat warnings as failure.")
    parser.add_argument("--report", help="Write JSON validation report.")
    args = parser.parse_args()

    manifest_path = Path(args.manifest).expanduser().resolve()
    base_dir = Path(args.base_dir).expanduser().resolve() if args.base_dir else None
    result = validate_manifest(manifest_path, base_dir, args.tolerance_sec, args.skip_media_check, args.consumer)
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
