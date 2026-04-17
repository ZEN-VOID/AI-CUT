#!/usr/bin/env python3
"""
Seedance video generation CLI.

Supports:
- submit/create: create a Seedance task via POST /v1/video/generations
- status: query a task via GET /v1/video/generations/{id}
- download: fetch task status and download the resolved video URL
- run: submit + poll + download in one flow
"""

from __future__ import annotations

import argparse
import base64
import json
import mimetypes
import os
import re
import sys
import time
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional, Sequence, Tuple
from urllib.parse import urlparse

import requests

try:
    from dotenv import load_dotenv

    try:
        load_dotenv()
    except Exception:
        load_dotenv(dotenv_path=str(Path.cwd() / ".env"))
except ImportError:
    print("❌ 缺少依赖: pip install requests python-dotenv")
    sys.exit(1)


DEFAULT_BASE_URL = "https://fw2afus.ent.acc.kurtisasia.com"
# `seedance` / `seedance-fast` are AnyFast rolling aliases for the latest
# quality-first and speed-first Seedance 2.0 endpoints.
DEFAULT_MODEL = "seedance"
DEFAULT_MODE = "auto"
DEFAULT_PROJECT_NAME = "测试"
DEFAULT_RESOLUTION = "720p"
DEFAULT_RATIO = "adaptive"
DEFAULT_DURATION = 5
DEFAULT_TIMEOUT = 180
DEFAULT_POLL_INTERVAL = 10
DEFAULT_MAX_WAIT_SECONDS = 900
ALLOWED_MODELS = {"seedance", "seedance-fast"}
ALLOWED_MODES = {"auto", "text", "first-frame", "first-last", "multimodal"}
ALLOWED_RESOLUTIONS = {"480p", "720p"}
ALLOWED_RATIOS = {"16:9", "4:3", "1:1", "3:4", "9:16", "21:9", "adaptive"}
TERMINAL_SUCCESS_STATES = {"success", "succeeded", "completed"}
TERMINAL_FAILURE_STATES = {"failed", "error", "cancelled", "canceled"}
IN_PROGRESS_STATES = {"queued", "running", "processing", "pending", "submitted", "in_progress", "in-progress"}


def _now_stamp() -> str:
    return datetime.now().strftime("%Y%m%d_%H%M%S")


def _safe_name(text: str, max_len: int = 64) -> str:
    normalized = re.sub(r"\s+", "_", text.strip())
    normalized = re.sub(r"[^0-9A-Za-z_\u4e00-\u9fff-]+", "", normalized)
    return (normalized or "seedance_video")[:max_len]


def _env_api_key() -> Optional[str]:
    return (
        os.getenv("ANYFAST_VIDEO_API_KEY")
        or os.getenv("SEEDANCE_API_KEY")
        or os.getenv("ANYFAST_API_KEY")
        or os.getenv("FINEAPI_API_KEY")
    )


def _env_base_url() -> str:
    return (
        os.getenv("SEEDANCE_API_BASE_URL")
        or os.getenv("ANYFAST_API_BASE_URL")
        or os.getenv("FINEAPI_API_BASE_URL")
        or DEFAULT_BASE_URL
    )


def _normalize_auth_header(api_key: str) -> str:
    token = api_key.strip()
    if token.lower().startswith("bearer "):
        return token
    return f"Bearer {token}"


def _redact_auth_header(value: str) -> str:
    if not value:
        return value
    return "Bearer ***"


def _session_headers(api_key: str) -> Dict[str, str]:
    return {
        "Authorization": _normalize_auth_header(api_key),
        "Accept": "application/json",
        "Content-Type": "application/json",
    }


def _request_summary(*, method: str, url: str, headers: Dict[str, str], data: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    sanitized_headers = {
        key: (_redact_auth_header(value) if key.lower() == "authorization" else value)
        for key, value in headers.items()
    }
    return {
        "method": method,
        "url": url,
        "headers": sanitized_headers,
        "data": data,
    }


def _parse_bool_optional(raw: Optional[str]) -> Optional[bool]:
    if raw is None:
        return None
    value = raw.strip().lower()
    if value in {"true", "1", "yes", "y", "on"}:
        return True
    if value in {"false", "0", "no", "n", "off"}:
        return False
    raise ValueError(f"布尔参数不合法: {raw}")


def _is_http_url(value: str) -> bool:
    parsed = urlparse(value)
    return parsed.scheme in {"http", "https"} and bool(parsed.netloc)


def _is_data_url(value: str) -> bool:
    return value.startswith("data:")


def _is_asset_ref(value: str) -> bool:
    return value.startswith("asset://")


def _guess_mime(path: Path, fallback: str) -> str:
    guessed, _ = mimetypes.guess_type(str(path))
    if guessed:
        return guessed
    return fallback


def _encode_local_file_as_data_url(path: Path, fallback_mime: str) -> str:
    mime = _guess_mime(path, fallback_mime)
    payload = base64.b64encode(path.read_bytes()).decode("ascii")
    return f"data:{mime};base64,{payload}"


def _normalize_image_input(value: str) -> str:
    raw = value.strip()
    if _is_http_url(raw) or _is_data_url(raw) or _is_asset_ref(raw):
        return raw
    path = Path(raw).expanduser()
    if not path.exists():
        raise ValueError(f"image-url 既不是合法 URL/Data URL/asset 引用，也不是存在的本地文件: {value}")
    return _encode_local_file_as_data_url(path, "image/png")


def _normalize_audio_input(value: str) -> str:
    raw = value.strip()
    if _is_http_url(raw) or _is_data_url(raw) or _is_asset_ref(raw):
        return raw
    path = Path(raw).expanduser()
    if not path.exists():
        raise ValueError(f"audio-url 既不是合法 URL/Data URL/asset 引用，也不是存在的本地文件: {value}")
    return _encode_local_file_as_data_url(path, "audio/mpeg")


def _normalize_video_input(value: str) -> str:
    raw = value.strip()
    if _is_http_url(raw) or _is_asset_ref(raw):
        return raw
    path = Path(raw).expanduser()
    if path.exists():
        raise ValueError(f"video-url 当前仅支持公网 URL 或 asset:// 引用，不支持本地视频路径: {value}")
    raise ValueError(f"video-url 不是合法 URL 或 asset 引用: {value}")


def _default_output_dir(project_name: str) -> Path:
    project = project_name.strip() or DEFAULT_PROJECT_NAME
    return Path("output") / "影片" / project / "5-API" / "video" / "seedance"


def _write_json(path: Path, data: Dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def _make_report_path(output_dir: Path, prefix: str, command: str, explicit: Optional[str]) -> Path:
    if explicit:
        return Path(explicit)
    stem = _safe_name(prefix or "seedance")
    return output_dir / f"{stem}_{command}_report_{_now_stamp()}.json"


def _infer_mode(explicit_mode: str, image_count: int, video_count: int, audio_count: int) -> str:
    if explicit_mode != DEFAULT_MODE:
        return explicit_mode
    if video_count or audio_count:
        return "multimodal"
    if image_count == 0:
        return "text"
    if image_count == 1:
        return "first-frame"
    if image_count == 2:
        return "first-last"
    return "multimodal"


def _validate_duration(value: int) -> int:
    if value == -1:
        return value
    if 4 <= value <= 15:
        return value
    raise ValueError(f"duration 仅允许 4-15 的整数或 -1: {value}")


def _build_validation_notes(
    *,
    model: str,
    mode: str,
    has_video: bool,
    has_audio: bool,
    web_search: bool,
) -> List[str]:
    notes: List[str] = []
    if model == "seedance-fast":
        notes.append("`seedance-fast` 是当前最新速度优先别名；若追求最高质量，优先使用默认模型 `seedance`。")
    if mode == "multimodal" and not has_video and not has_audio:
        notes.append("当前 multimodal 场景仅使用参考图；若希望严格首尾帧一致，优先改用 `first-last`。")
    return notes


def _build_content(
    *,
    prompt: Optional[str],
    mode: str,
    images: Sequence[str],
    videos: Sequence[str],
    audios: Sequence[str],
) -> List[Dict[str, Any]]:
    content: List[Dict[str, Any]] = []
    if prompt:
        content.append({"type": "text", "text": prompt})

    if mode == "text":
        if images or videos or audios:
            raise ValueError("mode=text 时不得传入 image/video/audio")
        if not prompt:
            raise ValueError("文本生视频至少需要 prompt")
        return content

    if mode == "first-frame":
        if len(images) != 1 or videos or audios:
            raise ValueError("mode=first-frame 只允许 1 张图片，且不得带视频/音频")
        content.append(
            {
                "type": "image_url",
                "image_url": {"url": images[0]},
                "role": "first_frame",
            }
        )
        return content

    if mode == "first-last":
        if len(images) != 2 or videos or audios:
            raise ValueError("mode=first-last 必须恰好 2 张图片，且不得带视频/音频")
        content.extend(
            [
                {
                    "type": "image_url",
                    "image_url": {"url": images[0]},
                    "role": "first_frame",
                },
                {
                    "type": "image_url",
                    "image_url": {"url": images[1]},
                    "role": "last_frame",
                },
            ]
        )
        return content

    if mode != "multimodal":
        raise ValueError(f"不支持的 mode: {mode}")

    if len(images) > 9:
        raise ValueError("multimodal 场景图片最多 9 张")
    if len(videos) > 3:
        raise ValueError("multimodal 场景视频最多 3 个")
    if len(audios) > 3:
        raise ValueError("multimodal 场景音频最多 3 个")
    if not images and not videos:
        raise ValueError("multimodal 场景至少需要 1 张图片或 1 个视频")
    if audios and not (images or videos):
        raise ValueError("audio-url 不能单独输入，至少需伴随图片或视频")

    for item in images:
        content.append(
            {
                "type": "image_url",
                "image_url": {"url": item},
                "role": "reference_image",
            }
        )
    for item in videos:
        content.append(
            {
                "type": "video_url",
                "video_url": {"url": item},
                "role": "reference_video",
            }
        )
    for item in audios:
        content.append(
            {
                "type": "audio_url",
                "audio_url": {"url": item},
                "role": "reference_audio",
            }
        )
    return content


def _build_payload(
    *,
    model: str,
    prompt: Optional[str],
    mode: str,
    images: Sequence[str],
    videos: Sequence[str],
    audios: Sequence[str],
    generate_audio: bool,
    resolution: str,
    ratio: str,
    duration: int,
    web_search: bool,
    watermark: Optional[bool],
) -> Tuple[Dict[str, Any], List[str]]:
    if model not in ALLOWED_MODELS:
        raise ValueError(f"model 不合法: {model}")
    if mode not in ALLOWED_MODES:
        raise ValueError(f"mode 不合法: {mode}")
    if resolution not in ALLOWED_RESOLUTIONS:
        raise ValueError(f"resolution 不合法: {resolution}")
    if ratio not in ALLOWED_RATIOS:
        raise ValueError(f"ratio 不合法: {ratio}")
    duration = _validate_duration(duration)
    if web_search and (images or videos or audios):
        raise ValueError("web_search 仅支持文本生视频，不能和 image/video/audio 混用")

    content = _build_content(prompt=prompt, mode=mode, images=images, videos=videos, audios=audios)
    payload: Dict[str, Any] = {
        "model": model,
        "content": content,
        "generate_audio": generate_audio,
        "resolution": resolution,
        "ratio": ratio,
        "duration": duration,
    }
    if web_search:
        payload["tools"] = [{"type": "web_search"}]
    if watermark is not None:
        payload["watermark"] = watermark

    notes = _build_validation_notes(
        model=model,
        mode=mode,
        has_video=bool(videos),
        has_audio=bool(audios),
        web_search=web_search,
    )
    return payload, notes


def _normalize_submit_response(body: Dict[str, Any], validation_notes: List[str]) -> Dict[str, Any]:
    return {
        "id": body.get("id") or body.get("task_id"),
        "task_id": body.get("task_id") or body.get("id"),
        "object": body.get("object"),
        "model": body.get("model"),
        "status": body.get("status"),
        "progress": body.get("progress"),
        "created_at": body.get("created_at"),
        "validation_notes": validation_notes,
    }


def _normalize_state(value: Any) -> str:
    if not isinstance(value, str):
        return ""
    return value.strip().lower()


def _normalize_status_response(body: Dict[str, Any]) -> Dict[str, Any]:
    outer = body.get("data") if isinstance(body.get("data"), dict) else {}
    inner = outer.get("data") if isinstance(outer.get("data"), dict) else {}
    normalized_status = _normalize_state(outer.get("status")) or _normalize_state(inner.get("status"))
    return {
        "task_id": outer.get("task_id") or inner.get("id"),
        "action": outer.get("action"),
        "status_outer": outer.get("status"),
        "status_inner": inner.get("status"),
        "normalized_status": normalized_status,
        "fail_reason": outer.get("fail_reason"),
        "progress": outer.get("progress"),
        "submit_time": outer.get("submit_time"),
        "start_time": outer.get("start_time"),
        "finish_time": outer.get("finish_time"),
        "model": inner.get("model"),
        "resolution": inner.get("resolution"),
        "ratio": inner.get("ratio"),
        "duration": inner.get("duration"),
        "generate_audio": inner.get("generate_audio"),
        "usage": inner.get("usage"),
        "inner_data": inner,
    }


def _extract_video_url(body: Dict[str, Any]) -> Tuple[Optional[str], List[str]]:
    tried: List[str] = []
    outer = body.get("data") if isinstance(body.get("data"), dict) else {}
    inner = outer.get("data") if isinstance(outer.get("data"), dict) else {}
    content = inner.get("content") if isinstance(inner.get("content"), dict) else {}

    candidate = content.get("video_url")
    tried.append("data.data.content.video_url")
    if isinstance(candidate, str) and candidate.strip():
        return candidate.strip(), tried

    last_try = outer.get("fail_reason")
    tried.append("data.fail_reason")
    if isinstance(last_try, str) and last_try.strip().startswith(("http://", "https://")):
        return last_try.strip(), tried

    for key in ("video_url", "url"):
        tried.append(f"data.data.{key}")
        value = inner.get(key)
        if isinstance(value, str) and value.strip():
            return value.strip(), tried

    return None, tried


def _extract_last_frame_url(body: Dict[str, Any]) -> Optional[str]:
    outer = body.get("data") if isinstance(body.get("data"), dict) else {}
    inner = outer.get("data") if isinstance(outer.get("data"), dict) else {}
    content = inner.get("content") if isinstance(inner.get("content"), dict) else {}
    for key in ("last_frame", "last_frame_url", "tail_frame_url"):
        value = content.get(key)
        if isinstance(value, str) and value.strip():
            return value.strip()
        value = inner.get(key)
        if isinstance(value, str) and value.strip():
            return value.strip()
    return None


def _download_file(url: str, target_path: Path, timeout: int) -> Path:
    target_path.parent.mkdir(parents=True, exist_ok=True)
    response = requests.get(url, timeout=timeout, stream=True)
    response.raise_for_status()
    with target_path.open("wb") as handle:
        for chunk in response.iter_content(chunk_size=1024 * 64):
            if chunk:
                handle.write(chunk)
    return target_path


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Seedance video generation CLI")
    subparsers = parser.add_subparsers(dest="command", required=True)

    def add_shared(subparser: argparse.ArgumentParser) -> None:
        subparser.add_argument("--api-key")
        subparser.add_argument("--base-url")
        subparser.add_argument("--timeout", type=int, default=DEFAULT_TIMEOUT)
        subparser.add_argument("--project-name", default=DEFAULT_PROJECT_NAME)
        subparser.add_argument("--output-dir")
        subparser.add_argument("--filename-prefix", default="seedance")
        subparser.add_argument("--report-json")

    submit_parser = subparsers.add_parser("submit", help="Create a Seedance generation task")
    add_shared(submit_parser)
    submit_parser.add_argument("--model", default=DEFAULT_MODEL, choices=sorted(ALLOWED_MODELS))
    submit_parser.add_argument("--mode", default=DEFAULT_MODE, choices=sorted(ALLOWED_MODES))
    submit_parser.add_argument("--prompt")
    submit_parser.add_argument("--image-url", action="append", default=[])
    submit_parser.add_argument("--video-url", action="append", default=[])
    submit_parser.add_argument("--audio-url", action="append", default=[])
    submit_parser.add_argument("--resolution", default=DEFAULT_RESOLUTION, choices=sorted(ALLOWED_RESOLUTIONS))
    submit_parser.add_argument("--ratio", default=DEFAULT_RATIO, choices=sorted(ALLOWED_RATIOS))
    submit_parser.add_argument("--duration", type=int, default=DEFAULT_DURATION)
    submit_parser.add_argument("--web-search", action="store_true")
    submit_parser.add_argument("--generate-audio", dest="generate_audio", action="store_true", default=True)
    submit_parser.add_argument("--no-generate-audio", dest="generate_audio", action="store_false")
    submit_parser.add_argument("--watermark")
    submit_parser.add_argument("--dry-run", action="store_true")
    submit_parser.add_argument("--print-payload", action="store_true")

    status_parser = subparsers.add_parser("status", help="Query Seedance generation status")
    add_shared(status_parser)
    status_parser.add_argument("--generation-id", required=True)

    download_parser = subparsers.add_parser("download", help="Download resolved Seedance video")
    add_shared(download_parser)
    download_parser.add_argument("--generation-id", required=True)
    download_parser.add_argument("--download-last-frame", action="store_true")

    run_parser = subparsers.add_parser("run", help="Submit, poll, and download Seedance video")
    add_shared(run_parser)
    run_parser.add_argument("--model", default=DEFAULT_MODEL, choices=sorted(ALLOWED_MODELS))
    run_parser.add_argument("--mode", default=DEFAULT_MODE, choices=sorted(ALLOWED_MODES))
    run_parser.add_argument("--prompt")
    run_parser.add_argument("--image-url", action="append", default=[])
    run_parser.add_argument("--video-url", action="append", default=[])
    run_parser.add_argument("--audio-url", action="append", default=[])
    run_parser.add_argument("--resolution", default=DEFAULT_RESOLUTION, choices=sorted(ALLOWED_RESOLUTIONS))
    run_parser.add_argument("--ratio", default=DEFAULT_RATIO, choices=sorted(ALLOWED_RATIOS))
    run_parser.add_argument("--duration", type=int, default=DEFAULT_DURATION)
    run_parser.add_argument("--web-search", action="store_true")
    run_parser.add_argument("--generate-audio", dest="generate_audio", action="store_true", default=True)
    run_parser.add_argument("--no-generate-audio", dest="generate_audio", action="store_false")
    run_parser.add_argument("--watermark")
    run_parser.add_argument("--poll-interval", type=int, default=DEFAULT_POLL_INTERVAL)
    run_parser.add_argument("--max-wait-seconds", type=int, default=DEFAULT_MAX_WAIT_SECONDS)
    run_parser.add_argument("--download-last-frame", action="store_true")
    run_parser.add_argument("--dry-run", action="store_true")
    run_parser.add_argument("--print-payload", action="store_true")

    return parser


def _resolve_common_paths(args: argparse.Namespace) -> Tuple[str, str, Path, Path]:
    api_key = args.api_key or _env_api_key()
    if not api_key:
        raise ValueError("缺少 API Key。请在 .env 中设置 ANYFAST_VIDEO_API_KEY，或显式传 --api-key")
    base_url = (args.base_url or _env_base_url()).rstrip("/")
    output_dir = Path(args.output_dir) if args.output_dir else _default_output_dir(args.project_name)
    report_path = _make_report_path(output_dir, args.filename_prefix, args.command, args.report_json)
    return api_key, base_url, output_dir, report_path


def _normalize_submit_inputs(args: argparse.Namespace) -> Tuple[str, List[str], List[str], List[str]]:
    images = [_normalize_image_input(item) for item in args.image_url]
    videos = [_normalize_video_input(item) for item in args.video_url]
    audios = [_normalize_audio_input(item) for item in args.audio_url]
    mode = _infer_mode(args.mode, len(images), len(videos), len(audios))
    return mode, images, videos, audios


def _submit(args: argparse.Namespace) -> Dict[str, Any]:
    api_key, base_url, output_dir, report_path = _resolve_common_paths(args)
    mode, images, videos, audios = _normalize_submit_inputs(args)
    headers = _session_headers(api_key)
    watermark = _parse_bool_optional(args.watermark)
    payload, validation_notes = _build_payload(
        model=args.model,
        prompt=args.prompt,
        mode=mode,
        images=images,
        videos=videos,
        audios=audios,
        generate_audio=args.generate_audio,
        resolution=args.resolution,
        ratio=args.ratio,
        duration=args.duration,
        web_search=args.web_search,
        watermark=watermark,
    )
    url = f"{base_url}/v1/video/generations"
    summary = _request_summary(method="POST", url=url, headers=headers, data=payload)

    report: Dict[str, Any] = {
        "command": "submit",
        "mode": mode,
        "validation_notes": validation_notes,
        "request_summary": summary,
        "output_dir": str(output_dir),
    }
    if args.dry_run:
        report["dry_run"] = True
        _write_json(report_path, report)
        if args.print_payload:
            print(json.dumps(report, ensure_ascii=False, indent=2))
        return report

    response = requests.post(url, headers=headers, json=payload, timeout=args.timeout)
    response.raise_for_status()
    body = response.json()
    report["response_body"] = body
    report["normalized_response"] = _normalize_submit_response(body, validation_notes)
    _write_json(report_path, report)
    print(json.dumps(report["normalized_response"], ensure_ascii=False, indent=2))
    return report


def _query_status(*, api_key: str, base_url: str, generation_id: str, timeout: int) -> Dict[str, Any]:
    headers = _session_headers(api_key)
    url = f"{base_url}/v1/video/generations/{generation_id}"
    response = requests.get(url, headers=headers, timeout=timeout)
    response.raise_for_status()
    body = response.json()
    return {
        "request_summary": _request_summary(method="GET", url=url, headers=headers),
        "response_body": body,
        "normalized_response": _normalize_status_response(body),
    }


def _status(args: argparse.Namespace) -> Dict[str, Any]:
    api_key, base_url, output_dir, report_path = _resolve_common_paths(args)
    report = {
        "command": "status",
        "generation_id": args.generation_id,
        "output_dir": str(output_dir),
    }
    queried = _query_status(api_key=api_key, base_url=base_url, generation_id=args.generation_id, timeout=args.timeout)
    report.update(queried)
    _write_json(report_path, report)
    print(json.dumps(report["normalized_response"], ensure_ascii=False, indent=2))
    return report


def _download(args: argparse.Namespace) -> Dict[str, Any]:
    api_key, base_url, output_dir, report_path = _resolve_common_paths(args)
    report: Dict[str, Any] = {
        "command": "download",
        "generation_id": args.generation_id,
        "output_dir": str(output_dir),
    }
    queried = _query_status(api_key=api_key, base_url=base_url, generation_id=args.generation_id, timeout=args.timeout)
    report.update(queried)
    body = queried["response_body"]
    normalized = queried["normalized_response"]
    video_url, tried = _extract_video_url(body)
    last_frame_url = _extract_last_frame_url(body)
    report["video_url_paths_tried"] = tried
    report["video_url"] = video_url
    report["last_frame_url"] = last_frame_url
    if not video_url:
        raise ValueError("未能从查询结果中解析到 video_url")

    task_id = normalized.get("task_id") or args.generation_id
    stem = _safe_name(f"{args.filename_prefix}_{task_id}")
    video_path = output_dir / f"{stem}.mp4"
    _download_file(video_url, video_path, args.timeout)
    report["downloaded_video_path"] = str(video_path)

    if args.download_last_frame and last_frame_url:
        last_frame_path = output_dir / f"{stem}_last_frame.png"
        _download_file(last_frame_url, last_frame_path, args.timeout)
        report["downloaded_last_frame_path"] = str(last_frame_path)

    _write_json(report_path, report)
    print(json.dumps({"task_id": task_id, "video_path": str(video_path)}, ensure_ascii=False, indent=2))
    return report


def _run(args: argparse.Namespace) -> Dict[str, Any]:
    submit_report = _submit(args)
    if args.dry_run:
        return submit_report

    normalized_submit = submit_report.get("normalized_response", {})
    generation_id = normalized_submit.get("task_id") or normalized_submit.get("id")
    if not generation_id:
        raise ValueError("创建成功后未拿到 generation id/task_id")

    api_key, base_url, output_dir, report_path = _resolve_common_paths(args)
    start = time.time()
    latest_status: Optional[Dict[str, Any]] = None
    while True:
        latest_status = _query_status(api_key=api_key, base_url=base_url, generation_id=generation_id, timeout=args.timeout)
        normalized = latest_status["normalized_response"]
        state = normalized.get("normalized_status", "")
        if state in TERMINAL_SUCCESS_STATES:
            break
        if state in TERMINAL_FAILURE_STATES:
            raise ValueError(f"任务失败: {json.dumps(normalized, ensure_ascii=False)}")
        if state and state not in IN_PROGRESS_STATES:
            # 保守处理未知状态：继续轮询，直到超时。
            pass
        if time.time() - start > args.max_wait_seconds:
            raise TimeoutError(f"轮询超时，最后状态: {json.dumps(normalized, ensure_ascii=False)}")
        time.sleep(args.poll_interval)

    download_args = argparse.Namespace(**vars(args))
    download_args.command = "download"
    download_args.generation_id = generation_id
    download_report = _download(download_args)
    run_report = {
        "command": "run",
        "generation_id": generation_id,
        "submit_report": submit_report.get("normalized_response"),
        "final_status": latest_status["normalized_response"] if latest_status else None,
        "download_result": {
            "video_url": download_report.get("video_url"),
            "downloaded_video_path": download_report.get("downloaded_video_path"),
            "downloaded_last_frame_path": download_report.get("downloaded_last_frame_path"),
        },
        "output_dir": str(output_dir),
    }
    _write_json(report_path, run_report)
    print(json.dumps(run_report, ensure_ascii=False, indent=2))
    return run_report


def main() -> int:
    parser = _build_parser()
    args = parser.parse_args()
    try:
        if args.command == "submit":
            _submit(args)
        elif args.command == "status":
            _status(args)
        elif args.command == "download":
            _download(args)
        elif args.command == "run":
            _run(args)
        else:
            parser.error(f"未知命令: {args.command}")
    except requests.HTTPError as exc:
        print(f"❌ HTTP 错误: {exc}", file=sys.stderr)
        if exc.response is not None:
            try:
                print(json.dumps(exc.response.json(), ensure_ascii=False, indent=2), file=sys.stderr)
            except Exception:
                print(exc.response.text, file=sys.stderr)
        return 1
    except Exception as exc:
        print(f"❌ {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
