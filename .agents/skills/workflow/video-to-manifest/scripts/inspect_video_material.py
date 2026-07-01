#!/usr/bin/env python3
"""Create mechanical evidence for workflow video manifest authoring."""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import re
import shutil
import subprocess
from datetime import datetime
from pathlib import Path
from typing import Any

try:
    import yaml
except Exception:  # pragma: no cover - handled at runtime
    yaml = None


VIDEO_EXTENSIONS = {".mp4", ".mov", ".mkv", ".webm", ".m4v"}
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


def run_command(args: list[str]) -> subprocess.CompletedProcess[str]:
    return subprocess.run(args, text=True, capture_output=True, check=False)


def require_binary(name: str) -> None:
    if shutil.which(name) is None:
        raise SystemExit(f"missing required binary: {name}")


def discover_videos(target: Path, recursive: bool) -> list[Path]:
    if target.is_file():
        if target.suffix.lower() not in VIDEO_EXTENSIONS:
            raise SystemExit(f"not a supported video file: {target}")
        return [target]
    if not target.is_dir():
        raise SystemExit(f"target does not exist: {target}")
    pattern = "**/*" if recursive else "*"
    videos = [
        path
        for path in target.glob(pattern)
        if path.is_file() and path.suffix.lower() in VIDEO_EXTENSIONS
    ]
    return sorted(videos)


def parse_rate(value: str | None) -> str | None:
    if not value or value == "0/0":
        return None
    return value


def category_hint_from_path(path: Path) -> str | None:
    for part in path.parts:
        if part in DIRECTORY_CATEGORY_HINTS:
            return DIRECTORY_CATEGORY_HINTS[part]
    return None


def material_branch_profile_from_path(path: Path) -> dict[str, Any]:
    profile: dict[str, Any] = {}
    matched_parts: list[str] = []
    parts = path.parts
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
    strong_category = category_hint_from_path(path)
    if strong_category:
        profile["category_hint"] = strong_category
        profile["category_confidence"] = "strong"
    return profile


def evidence_path_slug(relative_path: Path) -> str:
    raw = "/".join(relative_path.parts) or relative_path.name
    safe = re.sub(r"[^A-Za-z0-9._-]+", "-", raw).strip("-._")
    safe = safe[:80] or "video"
    digest = hashlib.sha1(raw.encode("utf-8")).hexdigest()[:10]
    return f"{safe}-{digest}"


def ffprobe(path: Path) -> dict[str, Any]:
    result = run_command(
        [
            "ffprobe",
            "-v",
            "error",
            "-print_format",
            "json",
            "-show_format",
            "-show_streams",
            str(path),
        ]
    )
    if result.returncode != 0:
        raise RuntimeError(result.stderr.strip() or f"ffprobe failed: {path}")
    data = json.loads(result.stdout)
    video_stream = next((s for s in data.get("streams", []) if s.get("codec_type") == "video"), {})
    audio_streams = [s for s in data.get("streams", []) if s.get("codec_type") == "audio"]
    duration = data.get("format", {}).get("duration") or video_stream.get("duration")
    media = {
        "duration_sec": round(float(duration), 3) if duration is not None else None,
        "fps": parse_rate(video_stream.get("avg_frame_rate") or video_stream.get("r_frame_rate")),
        "resolution": (
            f"{video_stream.get('width')}x{video_stream.get('height')}"
            if video_stream.get("width") and video_stream.get("height")
            else None
        ),
        "codec": video_stream.get("codec_name"),
        "has_audio": bool(audio_streams),
    }
    return {"raw": data, "media": media}


def timestamp_label(seconds: float) -> str:
    return f"{seconds:08.3f}".replace(".", "_")


def format_timestamp(seconds: float) -> str:
    minutes, secs = divmod(max(0.0, seconds), 60)
    hours, minutes = divmod(int(minutes), 60)
    if hours:
        return f"{hours:02d}:{minutes:02d}:{secs:06.3f}"
    return f"{minutes:02d}:{secs:06.3f}"


def sample_timestamps(duration: float | None, sample_count: int) -> list[float]:
    if not duration or duration <= 0:
        return [0.5]
    count = max(3, sample_count)
    if duration >= 30:
        count = max(count, min(12, math.ceil(duration / 10)))
    count = min(count, 12)
    if duration <= 1:
        return [0.0]
    start = min(0.5, max(0.0, duration / 4))
    end = max(start, duration - min(0.5, duration / 4))
    if count == 1:
        return [start]
    return [round(start + (end - start) * i / (count - 1), 3) for i in range(count)]


def slice_ranges(duration: float | None, threshold_sec: float, max_slice_sec: float) -> list[tuple[float, float]]:
    if not duration or duration <= threshold_sec or max_slice_sec <= 0:
        return []
    ranges: list[tuple[float, float]] = []
    cursor = 0.0
    while cursor < duration:
        end = min(duration, cursor + max_slice_sec)
        ranges.append((round(cursor, 3), round(end, 3)))
        cursor = end
    return ranges


def sample_timestamps_in_range(start: float, end: float, sample_count: int) -> list[float]:
    duration = max(0.0, end - start)
    if duration <= 0:
        return [start]
    count = max(2, sample_count)
    if duration <= 1:
        return [round(start, 3)]
    inner_start = start + min(0.5, duration / 4)
    inner_end = end - min(0.5, duration / 4)
    if count == 1:
        return [round(inner_start, 3)]
    return [round(inner_start + (inner_end - inner_start) * i / (count - 1), 3) for i in range(count)]


def extract_frame(video: Path, timestamp: float, output: Path) -> dict[str, Any]:
    output.parent.mkdir(parents=True, exist_ok=True)
    result = run_command(
        [
            "ffmpeg",
            "-hide_banner",
            "-loglevel",
            "error",
            "-ss",
            f"{timestamp:.3f}",
            "-i",
            str(video),
            "-frames:v",
            "1",
            "-q:v",
            "2",
            "-y",
            str(output),
        ]
    )
    return {
        "timestamp_sec": timestamp,
        "path": str(output),
        "ok": result.returncode == 0 and output.exists(),
        "error": result.stderr.strip() if result.returncode != 0 else "",
    }


def build_analysis_slices(
    video: Path,
    video_id: str,
    file_value: str,
    duration: float | None,
    threshold_sec: float,
    max_slice_sec: float,
    slice_sample_count: int,
    frame_root: Path,
    base_dir: Path,
    clips_dir: Path | None,
) -> list[dict[str, Any]]:
    slices = []
    for index, (start, end) in enumerate(slice_ranges(duration, threshold_sec, max_slice_sec), 1):
        slice_id = f"{video_id}-a{index:02d}"
        frames = []
        for ts in sample_timestamps_in_range(start, end, slice_sample_count):
            frame_path = frame_root / "analysis_slices" / f"a{index:02d}" / f"{timestamp_label(ts)}.jpg"
            frames.append(extract_frame(video, ts, frame_path))
        slices.append(
            {
                "slice_id": slice_id,
                "source_file": file_value,
                "start": format_timestamp(start),
                "end": format_timestamp(end),
                "duration_sec": round(end - start, 3),
                "sample_frames": [frame["path"] for frame in frames if frame.get("ok")],
                "observation_status": "needs_llm_semantic_completion",
            }
        )
        if clips_dir is not None:
            clip_path = clips_dir / video_id / f"{slice_id}.mp4"
            clip = write_analysis_clip(video, start, min(end - start, max_slice_sec), clip_path)
            if clip.get("ok"):
                slices[-1]["proxy_clip"] = str(clip_path.relative_to(base_dir))
                slices[-1]["proxy_clip_role"] = "physical_analysis_slice_under_60s"
                slices[-1]["proxy_clip_duration_sec"] = clip.get("duration_sec")
            else:
                slices[-1]["proxy_clip_error"] = clip.get("error")
    return slices


def probe_duration(path: Path) -> float | None:
    result = run_command(
        [
            "ffprobe",
            "-v",
            "error",
            "-show_entries",
            "format=duration",
            "-of",
            "default=noprint_wrappers=1:nokey=1",
            str(path),
        ]
    )
    if result.returncode != 0:
        return None
    try:
        return float(result.stdout.strip())
    except ValueError:
        return None


def write_analysis_clip(video: Path, start: float, duration: float, output: Path) -> dict[str, Any]:
    output.parent.mkdir(parents=True, exist_ok=True)
    duration = min(duration, 60.0)
    copy_cmd = [
        "ffmpeg",
        "-hide_banner",
        "-loglevel",
        "error",
        "-y",
        "-ss",
        f"{start:.3f}",
        "-t",
        f"{duration:.3f}",
        "-i",
        str(video),
        "-map",
        "0",
        "-c",
        "copy",
        "-avoid_negative_ts",
        "make_zero",
        str(output),
    ]
    result = run_command(copy_cmd)
    actual_duration = probe_duration(output) if result.returncode == 0 and output.exists() else None
    if result.returncode == 0 and output.exists() and output.stat().st_size > 0 and (
        actual_duration is None or actual_duration <= 60.25
    ):
        return {"ok": True, "path": str(output), "duration_sec": round(actual_duration, 3) if actual_duration else None}

    # Stream-copy cuts can exceed the requested duration when keyframes are sparse.
    # Re-encode only those slices so physical proxy clips stay under the 60s contract.
    tmp_output = output.with_suffix(".tmp.mp4")
    encode_cmd = [
        "ffmpeg",
        "-hide_banner",
        "-loglevel",
        "error",
        "-y",
        "-ss",
        f"{start:.3f}",
        "-t",
        f"{min(duration, 59.9):.3f}",
        "-i",
        str(video),
        "-map",
        "0",
        "-c:v",
        "libx264",
        "-preset",
        "ultrafast",
        "-crf",
        "28",
        "-c:a",
        "aac",
        "-b:a",
        "96k",
        "-movflags",
        "+faststart",
        str(tmp_output),
    ]
    encoded = run_command(encode_cmd)
    if encoded.returncode == 0 and tmp_output.exists() and tmp_output.stat().st_size > 0:
        tmp_output.replace(output)
        actual_duration = probe_duration(output)
        return {"ok": True, "path": str(output), "duration_sec": round(actual_duration, 3) if actual_duration else None}
    if tmp_output.exists():
        tmp_output.unlink()
    return {
        "ok": False,
        "path": str(output),
        "error": (encoded.stderr or result.stderr or "analysis clip generation failed").strip(),
    }


def build_skeleton(
    base_dir: Path,
    manifest_id: str,
    manifest_name: str,
    videos: list[dict[str, Any]],
) -> dict[str, Any]:
    today = datetime.now().strftime("%Y-%m-%d")
    skeleton_videos = []
    for index, item in enumerate(videos, 1):
        video_id = f"video-{index:02d}"
        skeleton_videos.append(
            {
                "id": video_id,
                "file": item["file"],
                "category": "needs_llm",
                "role": "needs_llm",
                "media": item["media"],
                "material_branch": item.get("material_branch_hint") or "needs_llm",
                "branch_path": item.get("branch_path") or "needs_llm",
                "workflow_role_hint": item.get("workflow_role_hint") or "needs_llm",
                "layer_affinity": item.get("layer_affinity") or [],
                "content_subtype_fit": [item.get("content_subtype_hint")] if item.get("content_subtype_hint") else [],
                "selection_constraints": {
                    "path_hint_only": True,
                    "requires_llm_visual_confirmation": True,
                },
                "content_profile": {
                    "visual_summary": "needs_llm",
                    "setting": [],
                    "main_subjects": [],
                    "color_palette": [],
                    "visual_density": "needs_llm",
                    "motion_level": "needs_llm",
                    "action_intensity": "needs_llm",
                    "text_overlay_density": "needs_llm",
                    "continuity_group": "needs_llm",
                },
                "selection_profile": {
                    "best_for": [],
                    "avoid_for": [],
                    "keyword_triggers": [],
                    "priority": 50,
                    "trigger_profile": {
                        "positive_triggers": [],
                        "negative_triggers": [],
                        "hook_fit": "needs_llm",
                        "proof_fit": "needs_llm",
                        "transition_fit": "needs_llm",
                        "cta_fit": "needs_llm",
                    },
                },
                "splicing_profile": {
                    "preferred_clip_sec": {"min": 2.0, "ideal": 4.0, "max": 7.0},
                    "suggested_cut_style": [],
                    "entry_affordance": "needs_llm",
                    "exit_affordance": "needs_llm",
                    "speed_tolerance": "0.9x-1.1x",
                    "loopability": "needs_llm",
                },
                "reuse_profile": {
                    "distinctiveness": "needs_llm",
                    "similarity_cluster": "needs_llm",
                    "reuse_risk": "needs_llm",
                    "cooldown_after_use": "needs_llm",
                },
                "subtitle_safe_zone": {
                    "risk_level": "needs_llm",
                    "existing_text_positions": [],
                    "recommended_f1_position": "needs_llm",
                    "notes": "needs_llm",
                },
                "evidence": {
                    "ffprobe_json": item.get("ffprobe_json"),
                    "sample_frames": [frame["path"] for frame in item.get("sample_frames", []) if frame.get("ok")],
                    "observation_status": "needs_llm_semantic_completion",
                    "directory_category_hint": item.get("directory_category_hint"),
                    "material_branch_hint": item.get("material_branch_hint"),
                    "branch_path": item.get("branch_path"),
                    "workflow_role_hint": item.get("workflow_role_hint"),
                    "layer_affinity": item.get("layer_affinity"),
                    "content_subtype_hint": item.get("content_subtype_hint"),
                    "classification_boundary": "Path-derived hints only; final category and semantic fields require LLM/operator visual confirmation.",
                },
                "analysis_slices": item.get("analysis_slices", []),
                "segments": [],
            }
        )
    return {
        "schema_version": 2,
        "manifest_id": manifest_id,
        "manifest_name": manifest_name,
        "created_at": today,
        "updated_at": today,
        "base_dir": str(base_dir),
        "purpose": "为 workflow 等视频工作流提供可用于选材、截段、拼接、字幕避让、asset evidence 或 EDL/storyboard 前置证据的结构化素材索引。",
        "consumer_contract": {
            "primary_consumers": ["workflow"],
            "read_phase": "N1-INTAKE",
            "apply_phase": "N5-VISUAL-PLAN",
            "verify_phase": "N7-VERIFY",
            "authority": "素材事实索引与选材辅助层。",
            "not_authority": [
                "不得替代 ffprobe、抽帧验证、用户文案真源、旁白主时钟、workflow EDL 裁决或 workflow asset_evidence/storyboard 裁决。",
                "不得仅凭本 YAML 判定字幕不遮挡，必须在 final 或预览帧中验证。",
            ],
            "fallback": "若 YAML 缺失、解析失败、文件不存在、时长差异超过 0.25 秒或抽帧与描述冲突，下游 workflow 回退到 ffprobe + 抽帧人工观察或 workflow asset_evidence 重建，并在报告记录 manifest_mismatch。",
        },
        "field_model": {
            "video_level_required": [
                "id",
                "file",
                "category",
                "role",
                "material_branch",
                "branch_path",
                "workflow_role_hint",
                "layer_affinity",
                "media",
                "content_profile",
                "selection_profile",
                "splicing_profile",
                "subtitle_safe_zone",
                "segments",
                "analysis_slices",
                "reuse_profile",
            ],
            "segment_level_required": [
                "segment_id",
                "start/end/duration_sec",
                "visual_content",
                "semantic_tags",
                "semantic_vector",
                "trigger_profile",
                "visual_signature",
                "variation_profile",
                "segment_role_fit",
                "content_subtype_fit",
                "selection_constraints",
                "analysis_slice_id",
                "shot_type/motion/action_intensity",
                "text_overlay",
                "best_for/avoid_for",
                "splice_notes",
            ],
        },
        "global_editing_policy": {
            "path_resolution": "videos[].file 均相对 base_dir 解析。",
            "default_audio_policy": "所有视频原音只作参考；下游 final 默认以用户旁白或已锁定主时钟为主音轨。",
            "runtime_validation": [
                "每次执行前重新 ffprobe。",
                "每个入选素材至少抽 1 帧验证画面与 YAML 描述一致。",
                "若使用 subtitle_safe_zone.risk_level 为 high 的素材，必须抽最终字幕帧验证遮挡。",
            ],
            "pre_slice_policy": {
                "enabled": True,
                "threshold_sec": 60,
                "max_analysis_slice_sec": 60,
                "output_scope": "evidence_only",
            },
            "diversity_tag_policy": {
                "min_effective_semantic_tags": 3,
                "recommended_segment_fields": [
                    "semantic_vector",
                    "trigger_profile",
                    "visual_signature",
                    "variation_profile",
                ],
            },
            "default_clip_length_sec": {
                "operation_demo": {"min": 2.5, "ideal": 5.0, "max": 9.0},
                "tool_display": {"min": 2.5, "ideal": 4.0, "max": 7.0},
                "aigc_content": {"min": 2.0, "ideal": 4.5, "max": 8.0},
            },
            "selection_priority": [
                "操作步骤、实操演示、前后对比、流程证明：优先 operation_demo。",
                "AI 工具、提示词、生成流程、剪辑软件、导入导出、资产证明：优先 tool_display。",
                "剧情、打斗、玄幻、角色冲突、爆发、尾钩：优先 aigc_content。",
            ],
        },
        "material_pool_profile": {
            "classification_model": "two_layer_path_hint_plus_visual_confirmation",
            "path_hint_authority": "candidate_pool_only",
            "final_semantic_authority": "LLM/operator visual understanding from per-video evidence",
            "branch_manifest_policy": "projects/素材/ may use branch-level 视频说明.yaml files plus an optional top-level 素材索引.yaml registry.",
        },
        "renames": [],
        "videos": skeleton_videos,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("target", help="Video file or directory to inspect.")
    parser.add_argument("--base-dir", help="Base dir for relative video paths. Defaults to target dir.")
    parser.add_argument("--work-dir", help="Output work directory. Defaults to <base_dir>/video_manifest_work.")
    parser.add_argument("--output-json", help="Evidence JSON path. Defaults to <work_dir>/material-evidence.json.")
    parser.add_argument("--sample-count", type=int, default=5, help="Minimum sample frames per video.")
    parser.add_argument("--pre-slice-threshold-sec", type=float, default=60.0)
    parser.add_argument("--max-analysis-slice-sec", type=float, default=60.0)
    parser.add_argument("--slice-sample-count", type=int, default=3)
    parser.add_argument(
        "--write-analysis-clips",
        action="store_true",
        help="Write physical proxy clips for analysis_slices under <work_dir>/analysis_clips.",
    )
    parser.add_argument("--analysis-clips-dir", help="Output directory for physical analysis proxy clips.")
    parser.add_argument("--no-recursive", action="store_true", help="Do not recursively scan directories.")
    parser.add_argument("--write-skeleton", help="Optional non-final skeleton YAML path.")
    parser.add_argument("--manifest-id", default="video-material-index")
    parser.add_argument("--manifest-name", default="Workflow video material structured selection index")
    args = parser.parse_args()

    require_binary("ffprobe")
    require_binary("ffmpeg")

    target = Path(args.target).expanduser().resolve()
    base_dir = Path(args.base_dir).expanduser().resolve() if args.base_dir else (target.parent if target.is_file() else target)
    work_dir = Path(args.work_dir).expanduser().resolve() if args.work_dir else base_dir / "video_manifest_work"
    frames_dir = work_dir / "frames"
    clips_dir = None
    if args.write_analysis_clips:
        clips_dir = (
            Path(args.analysis_clips_dir).expanduser().resolve()
            if args.analysis_clips_dir
            else work_dir / "analysis_clips"
        )
    output_json = Path(args.output_json).expanduser().resolve() if args.output_json else work_dir / "material-evidence.json"

    videos = discover_videos(target, recursive=not args.no_recursive)
    if not videos:
        raise SystemExit(f"no supported videos found: {target}")

    evidence_videos: list[dict[str, Any]] = []
    errors: list[dict[str, str]] = []
    for video_index, video in enumerate(videos, 1):
        rel = video.relative_to(base_dir) if video.is_relative_to(base_dir) else video.name
        rel_path = Path(str(rel))
        evidence_slug = evidence_path_slug(rel_path)
        frame_root = frames_dir / evidence_slug
        branch_profile = material_branch_profile_from_path(rel_path) or material_branch_profile_from_path(video)
        evidence_video_id = f"video-{video_index:02d}"
        item: dict[str, Any] = {
            "evidence_id": evidence_video_id,
            "file": str(rel),
            "absolute_path": str(video),
            "evidence_slug": evidence_slug,
        }
        category_hint = (
            category_hint_from_path(rel_path)
            or category_hint_from_path(video)
            or branch_profile.get("category_hint")
        )
        item["directory_category_hint"] = category_hint
        item["material_branch_hint"] = branch_profile.get("material_branch")
        item["branch_path"] = branch_profile.get("branch_path")
        item["branch_source"] = branch_profile.get("branch_source")
        item["workflow_role_hint"] = branch_profile.get("workflow_role_hint")
        item["layer_affinity"] = branch_profile.get("layer_affinity", [])
        item["content_subtype_hint"] = branch_profile.get("content_subtype_hint")
        item["category_hint_confidence"] = branch_profile.get("category_confidence", "none")
        item["classification_boundary"] = (
            "Path-derived hints narrow candidate pools only; final category/role/tags require visual evidence."
        )
        try:
            probe = ffprobe(video)
            item["media"] = probe["media"]
            ffprobe_path = work_dir / "ffprobe" / f"{evidence_slug}.json"
            ffprobe_path.parent.mkdir(parents=True, exist_ok=True)
            ffprobe_path.write_text(json.dumps(probe["raw"], ensure_ascii=False, indent=2), encoding="utf-8")
            item["ffprobe_json"] = str(ffprobe_path)
            frames = []
            for ts in sample_timestamps(probe["media"].get("duration_sec"), args.sample_count):
                frame_path = frame_root / f"{timestamp_label(ts)}.jpg"
                frames.append(extract_frame(video, ts, frame_path))
            item["sample_frames"] = frames
            item["analysis_slices"] = build_analysis_slices(
                video=video,
                video_id=evidence_video_id,
                file_value=str(rel),
                duration=probe["media"].get("duration_sec"),
                threshold_sec=args.pre_slice_threshold_sec,
                max_slice_sec=args.max_analysis_slice_sec,
                slice_sample_count=args.slice_sample_count,
                frame_root=frame_root,
                base_dir=base_dir,
                clips_dir=clips_dir,
            )
        except Exception as exc:  # noqa: BLE001
            errors.append({"file": str(rel), "error": str(exc)})
            item["error"] = str(exc)
        evidence_videos.append(item)

    packet = {
        "schema_version": 1,
        "created_at": datetime.now().isoformat(timespec="seconds"),
        "target": str(target),
        "base_dir": str(base_dir),
        "work_dir": str(work_dir),
        "video_count": len(evidence_videos),
        "videos": evidence_videos,
        "errors": errors,
        "pre_slice_policy": {
            "threshold_sec": args.pre_slice_threshold_sec,
            "max_analysis_slice_sec": args.max_analysis_slice_sec,
            "slice_sample_count": args.slice_sample_count,
            "scope": (
                "analysis evidence plus physical proxy clips; original videos are not moved or overwritten"
                if args.write_analysis_clips
                else "analysis evidence only; original videos are not moved or overwritten"
            ),
            "physical_proxy_clips": bool(args.write_analysis_clips),
            "analysis_clips_dir": str(clips_dir) if clips_dir else None,
        },
        "material_pool_hint_policy": {
            "supported_branch_roots": sorted(MATERIAL_BRANCH_HINTS),
            "path_hint_authority": "candidate_pool_only",
            "final_semantic_authority": "LLM/operator visual understanding from per-video evidence",
            "collision_safe_evidence_paths": True,
        },
        "authorship_boundary": "This packet contains mechanical evidence only. LLM/operator must author final semantic manifest fields.",
    }

    output_json.parent.mkdir(parents=True, exist_ok=True)
    output_json.write_text(json.dumps(packet, ensure_ascii=False, indent=2), encoding="utf-8")

    if args.write_skeleton:
        if yaml is None:
            raise SystemExit("PyYAML is required for --write-skeleton")
        skeleton_path = Path(args.write_skeleton).expanduser().resolve()
        skeleton = build_skeleton(base_dir, args.manifest_id, args.manifest_name, evidence_videos)
        skeleton_path.parent.mkdir(parents=True, exist_ok=True)
        skeleton_path.write_text(yaml.safe_dump(skeleton, allow_unicode=True, sort_keys=False), encoding="utf-8")

    print(json.dumps({"status": "ok", "evidence": str(output_json), "errors": errors}, ensure_ascii=False))
    return 0 if not errors else 2


if __name__ == "__main__":
    raise SystemExit(main())
