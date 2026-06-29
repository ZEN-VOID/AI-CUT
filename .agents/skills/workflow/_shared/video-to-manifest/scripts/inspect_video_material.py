#!/usr/bin/env python3
"""Create mechanical evidence for workflow video manifest authoring."""

from __future__ import annotations

import argparse
import json
import math
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
    frames_dir: Path,
) -> list[dict[str, Any]]:
    slices = []
    for index, (start, end) in enumerate(slice_ranges(duration, threshold_sec, max_slice_sec), 1):
        slice_id = f"{video_id}-a{index:02d}"
        frames = []
        for ts in sample_timestamps_in_range(start, end, slice_sample_count):
            frame_path = frames_dir / video.stem / "analysis_slices" / f"a{index:02d}" / f"{timestamp_label(ts)}.jpg"
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
    return slices


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
        "purpose": "为 F1/F2 等视频工作流提供可用于选材、截段、拼接、字幕避让、asset evidence 或 EDL/storyboard 前置证据的结构化素材索引。",
        "consumer_contract": {
            "primary_consumers": ["F1", "F2"],
            "read_phase": "N1-INTAKE",
            "apply_phase": "N5-VISUAL-PLAN",
            "verify_phase": "N7-VERIFY",
            "authority": "素材事实索引与选材辅助层。",
            "not_authority": [
                "不得替代 ffprobe、抽帧验证、用户文案真源、旁白主时钟、F1 最终 EDL 裁决或 F2 asset_evidence/storyboard 裁决。",
                "不得仅凭本 YAML 判定字幕不遮挡，必须在 final 或预览帧中验证。",
            ],
            "fallback": "若 YAML 缺失、解析失败、文件不存在、时长差异超过 0.25 秒或抽帧与描述冲突，下游 workflow 回退到 ffprobe + 抽帧人工观察或 F2 asset_evidence 重建，并在报告记录 manifest_mismatch。",
        },
        "field_model": {
            "video_level_required": [
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
    output_json = Path(args.output_json).expanduser().resolve() if args.output_json else work_dir / "material-evidence.json"

    videos = discover_videos(target, recursive=not args.no_recursive)
    if not videos:
        raise SystemExit(f"no supported videos found: {target}")

    evidence_videos: list[dict[str, Any]] = []
    errors: list[dict[str, str]] = []
    for video_index, video in enumerate(videos, 1):
        rel = video.relative_to(base_dir) if video.is_relative_to(base_dir) else video.name
        evidence_video_id = f"video-{video_index:02d}"
        item: dict[str, Any] = {
            "evidence_id": evidence_video_id,
            "file": str(rel),
            "absolute_path": str(video),
        }
        item["directory_category_hint"] = category_hint_from_path(Path(str(rel))) or category_hint_from_path(video)
        try:
            probe = ffprobe(video)
            item["media"] = probe["media"]
            ffprobe_path = work_dir / "ffprobe" / f"{video.stem}.json"
            ffprobe_path.parent.mkdir(parents=True, exist_ok=True)
            ffprobe_path.write_text(json.dumps(probe["raw"], ensure_ascii=False, indent=2), encoding="utf-8")
            item["ffprobe_json"] = str(ffprobe_path)
            frames = []
            for ts in sample_timestamps(probe["media"].get("duration_sec"), args.sample_count):
                frame_path = frames_dir / video.stem / f"{timestamp_label(ts)}.jpg"
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
                frames_dir=frames_dir,
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
            "scope": "analysis evidence only; original videos are not moved or overwritten",
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
