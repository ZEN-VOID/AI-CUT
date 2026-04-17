#!/usr/bin/env python3
"""
AnyFast Sora 2 video generation CLI.

Supports:
- submit: create a video generation task
- status: poll/query an existing task
- download: fetch content JSON and optionally download the MP4
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
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional
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
DEFAULT_MODEL = "official-sora-2-pro"
DEFAULT_SECONDS = "4"
DEFAULT_SIZE = "720x1280"
DEFAULT_PROJECT_NAME = "测试"
DEFAULT_TIMEOUT = 180
DEFAULT_POLL_INTERVAL = 10
DEFAULT_MAX_WAIT_SECONDS = 900
ALLOWED_SECONDS = {"4", "8", "12"}
ALLOWED_SIZES = {"720x1280", "1280x720", "1024x1792", "1792x1024"}
MODEL_LADDER = [
    "official-sora-2-pro",
    "sora-2-pro",
    "official-sora-2",
    "sora-2",
]
MODEL_EQUIVALENTS = {
    "official-sora-2-pro": ["sora-2-pro"],
    "sora-2-pro": ["official-sora-2-pro"],
    "official-sora-2": ["sora-2"],
    "sora-2": ["official-sora-2"],
}


def _now_stamp() -> str:
    return datetime.now().strftime("%Y%m%d_%H%M%S")


def _safe_name(text: str, max_len: int = 64) -> str:
    normalized = re.sub(r"\s+", "_", text.strip())
    normalized = re.sub(r"[^0-9A-Za-z_\u4e00-\u9fff-]+", "", normalized)
    return (normalized or "sora_video")[:max_len]


def _env_api_key() -> Optional[str]:
    return (
        os.getenv("SORA_API_KEY")
        or os.getenv("ANYFAST_VIDEO_API_KEY")
        or os.getenv("ANYFAST_API_KEY")
    )


def _env_base_url() -> str:
    return (
        os.getenv("SORA_API_BASE_URL")
        or os.getenv("ANYFAST_API_BASE_URL")
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


def _guess_mime_type(name: str, fallback: str = "image/png") -> str:
    mime_type, _ = mimetypes.guess_type(name)
    return mime_type or fallback


def _is_remote_url(value: str) -> bool:
    parsed = urlparse(value)
    return parsed.scheme in {"http", "https"} and bool(parsed.netloc)


def _is_data_url(value: str) -> bool:
    return value.startswith("data:image/")


@dataclass
class ImageInput:
    source: str
    input_type: str
    mime_type: str
    data: bytes
    filename: str

    def to_summary(self) -> Dict[str, Any]:
        return {
            "source": self.source,
            "input_type": self.input_type,
            "mime_type": self.mime_type,
            "bytes": len(self.data),
            "filename": self.filename,
        }


def _read_data_url(value: str) -> ImageInput:
    match = re.match(r"^data:(image/[^;]+);base64,(.+)$", value, re.DOTALL)
    if not match:
        raise ValueError("data URL 格式不合法，需形如 data:image/png;base64,...")
    mime_type = match.group(1)
    b64_data = match.group(2)
    try:
        raw = base64.b64decode(b64_data)
    except Exception as exc:
        raise ValueError("data URL 中的 base64 内容无法解码") from exc
    extension = mimetypes.guess_extension(mime_type) or ".png"
    return ImageInput(
        source=value[:64] + "...",
        input_type="data_url",
        mime_type=mime_type,
        data=raw,
        filename=f"input_reference{extension}",
    )


def _read_remote_url(value: str, timeout: int) -> ImageInput:
    response = requests.get(value, timeout=timeout)
    response.raise_for_status()
    mime_type = response.headers.get("Content-Type", "").split(";", 1)[0].strip() or _guess_mime_type(value)
    filename = Path(urlparse(value).path).name or "input_reference"
    if "." not in filename:
        extension = mimetypes.guess_extension(mime_type) or ".png"
        filename = f"{filename}{extension}"
    return ImageInput(
        source=value,
        input_type="remote_url",
        mime_type=mime_type,
        data=response.content,
        filename=filename,
    )


def _read_local_file(value: str) -> ImageInput:
    path = Path(value).expanduser()
    if not path.is_file():
        raise FileNotFoundError(f"本地图片不存在: {value}")
    return ImageInput(
        source=str(path),
        input_type="local_file",
        mime_type=_guess_mime_type(path.name),
        data=path.read_bytes(),
        filename=path.name,
    )


def _read_image_source(value: str, timeout: int) -> ImageInput:
    if _is_data_url(value):
        return _read_data_url(value)
    if _is_remote_url(value):
        return _read_remote_url(value, timeout=timeout)
    return _read_local_file(value)


def _default_output_dir(project_name: str) -> Path:
    project = project_name.strip() or DEFAULT_PROJECT_NAME
    return Path("output") / "影片" / project / "5-API" / "video" / "sora"


def _normalize_submit_response(body: Dict[str, Any], attempted_models: List[str]) -> Dict[str, Any]:
    return {
        "id": body.get("id"),
        "object": body.get("object"),
        "model": body.get("model"),
        "status": body.get("status"),
        "progress": body.get("progress"),
        "created_at": body.get("created_at"),
        "seconds": body.get("seconds"),
        "size": body.get("size"),
        "attempted_models": attempted_models,
    }


def _normalize_status_response(body: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "id": body.get("id"),
        "object": body.get("object"),
        "model": body.get("model"),
        "status": body.get("status"),
        "progress": body.get("progress"),
        "prompt": body.get("prompt"),
        "seconds": body.get("seconds"),
        "size": body.get("size"),
        "created_at": body.get("created_at"),
        "completed_at": body.get("completed_at"),
        "expires_at": body.get("expires_at"),
        "error": body.get("error"),
        "remixed_from_video_id": body.get("remixed_from_video_id"),
    }


def _normalize_download_response(body: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "id": body.get("id"),
        "object": body.get("object"),
        "model": body.get("model"),
        "status": body.get("status"),
        "progress": body.get("progress"),
        "video_url": body.get("video_url") or body.get("url"),
        "url": body.get("url"),
        "seconds": body.get("seconds"),
        "size": body.get("size"),
        "created_at": body.get("created_at"),
    }


def _write_json(path: Path, data: Dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def _make_report_path(output_dir: Path, prefix: str, command: str, explicit: Optional[str]) -> Path:
    if explicit:
        return Path(explicit)
    stem = _safe_name(prefix or "sora")
    return output_dir / f"{stem}_{command}_report_{_now_stamp()}.json"


def _build_model_candidates(model: str, allow_alias_fallback: bool, *, model_was_explicit: bool) -> List[str]:
    if model_was_explicit:
        candidates = [model]
        if allow_alias_fallback:
            candidates.extend(MODEL_EQUIVALENTS.get(model, []))
    else:
        candidates = list(MODEL_LADDER)
        if model and model not in candidates:
            candidates.insert(0, model)
        if not allow_alias_fallback:
            candidates = [candidates[0]]
    deduped: List[str] = []
    for item in candidates:
        if item not in deduped:
            deduped.append(item)
    return deduped


def _build_attempt_diagnostic(errors: List[Dict[str, Any]]) -> Optional[str]:
    texts: List[str] = []
    for item in errors:
        body = item.get("body")
        if isinstance(body, dict):
            if isinstance(body.get("error"), dict):
                message = body["error"].get("message")
                if message:
                    texts.append(str(message))
            message = body.get("message")
            if message:
                texts.append(str(message))
            code = body.get("code")
            if code:
                texts.append(str(code))
    merged = " | ".join(texts)
    if not merged:
        return None
    if "额度已用尽" in merged or "quota not enough" in merged or "insufficient_user_quota" in merged:
        return "API Key 或账户额度不足；优先检查 SORA/ANYFAST 令牌余额，再决定是否切换到有额度的 key。"
    if "under group auto (distributor)" in merged and "model_not_found" in merged:
        return "当前账户分组未开通 Sora 通道；如果官方端点与加速端点都报同样错误，就不要继续试模型别名，应改查账户分组或渠道开通状态。"
    if "model_not_found" in merged or "No available channel for model" in merged:
        return "当前网关没有可用的该模型通道；检查模型名是否需要改成网关支持的别名，或确认该组已开通 Sora 通道。"
    return None


def _session_headers(api_key: str) -> Dict[str, str]:
    return {
        "Authorization": _normalize_auth_header(api_key),
        "Accept": "application/json",
    }


def _request_summary(
    *,
    method: str,
    url: str,
    headers: Dict[str, str],
    data: Optional[Dict[str, Any]] = None,
    files: Optional[List[Dict[str, Any]]] = None,
) -> Dict[str, Any]:
    sanitized_headers = {k: (_redact_auth_header(v) if k.lower() == "authorization" else v) for k, v in headers.items()}
    return {
        "method": method,
        "url": url,
        "headers": sanitized_headers,
        "data": data,
        "files": files,
    }


def submit_video(
    *,
    prompt: str,
    model: str,
    seconds: str,
    size: str,
    image: Optional[str],
    remix_video_id: Optional[str],
    api_key: str,
    base_url: str,
    timeout: int,
    dry_run: bool,
    print_payload: bool,
    allow_alias_fallback: bool,
    model_was_explicit: bool,
) -> Dict[str, Any]:
    if seconds not in ALLOWED_SECONDS:
        raise ValueError(f"seconds 不合法: {seconds}")
    if size not in ALLOWED_SIZES:
        raise ValueError(f"size 不合法: {size}")
    if not prompt.strip():
        raise ValueError("prompt 不能为空")

    image_input = _read_image_source(image, timeout=timeout) if image else None
    headers = _session_headers(api_key)
    url = f"{base_url.rstrip('/')}/v1/videos"
    model_candidates = _build_model_candidates(
        model,
        allow_alias_fallback,
        model_was_explicit=model_was_explicit,
    )
    request_data = {
        "prompt": prompt,
        "seconds": seconds,
        "size": size,
    }
    if remix_video_id:
        request_data["remix_video_id"] = remix_video_id

    request_summary = _request_summary(
        method="POST",
        url=url,
        headers=headers,
        data={
            "requested_model": model,
            "model_was_explicit": model_was_explicit,
            "model_candidates": model_candidates,
            **request_data,
        },
        files=[image_input.to_summary()] if image_input else None,
    )
    if print_payload or dry_run:
        print(json.dumps(request_summary, ensure_ascii=False, indent=2))
    if dry_run:
        return {
            "ok": True,
            "request_summary": request_summary,
            "normalized_submit": None,
            "raw_response": None,
            "attempted_models": model_candidates,
            "diagnostic_hint": "dry-run 未实际提交任务",
        }

    errors: List[Dict[str, Any]] = []
    for candidate_model in model_candidates:
        data = {"model": candidate_model, **request_data}
        files = None
        if image_input:
            files = {
                "input_reference": (
                    image_input.filename,
                    image_input.data,
                    image_input.mime_type,
                )
            }
        response = requests.post(
            url,
            headers={"Authorization": headers["Authorization"]},
            data=data,
            files=files,
            timeout=timeout,
        )
        try:
            body = response.json()
        except ValueError:
            body = {"non_json_response": response.text}

        if response.ok:
            return {
                "ok": True,
                "request_summary": request_summary,
                "normalized_submit": _normalize_submit_response(body, model_candidates),
                "raw_response": body,
                "attempted_models": model_candidates,
            }

        errors.append(
            {
                "model": candidate_model,
                "status_code": response.status_code,
                "body": body,
            }
        )

    return {
        "ok": False,
        "request_summary": request_summary,
        "normalized_submit": None,
        "raw_response": {"attempt_errors": errors},
        "attempted_models": model_candidates,
        "error": "创建任务失败",
        "diagnostic_hint": _build_attempt_diagnostic(errors),
    }


def query_status(*, video_id: str, api_key: str, base_url: str, timeout: int) -> Dict[str, Any]:
    headers = _session_headers(api_key)
    url = f"{base_url.rstrip('/')}/v1/videos/{video_id}"
    response = requests.get(url, headers=headers, timeout=timeout)
    try:
        body = response.json()
    except ValueError:
        body = {"non_json_response": response.text}
    return {
        "ok": response.ok,
        "request_summary": _request_summary(method="GET", url=url, headers=headers),
        "normalized_status": _normalize_status_response(body) if response.ok else None,
        "raw_response": body,
        "status_code": response.status_code,
        "error": None if response.ok else "查询任务失败",
    }


def poll_until_complete(
    *,
    video_id: str,
    api_key: str,
    base_url: str,
    timeout: int,
    poll_interval: int,
    max_wait_seconds: int,
) -> Dict[str, Any]:
    started = time.time()
    history: List[Dict[str, Any]] = []
    while True:
        status_result = query_status(video_id=video_id, api_key=api_key, base_url=base_url, timeout=timeout)
        history.append(status_result.get("normalized_status") or status_result.get("raw_response"))
        if not status_result["ok"]:
            status_result["history"] = history
            return status_result

        normalized = status_result["normalized_status"] or {}
        status = normalized.get("status")
        if status == "completed":
            status_result["history"] = history
            return status_result
        if status == "failed":
            status_result["history"] = history
            status_result["error"] = normalized.get("error") or "任务状态为 failed"
            status_result["ok"] = False
            return status_result
        if time.time() - started >= max_wait_seconds:
            status_result["history"] = history
            status_result["ok"] = False
            status_result["error"] = f"轮询超时，已等待 {max_wait_seconds} 秒"
            return status_result
        time.sleep(poll_interval)


def download_video_result(
    *,
    video_id: str,
    api_key: str,
    base_url: str,
    timeout: int,
    output_dir: Path,
    filename_prefix: str,
    save_video: bool,
) -> Dict[str, Any]:
    headers = _session_headers(api_key)
    url = f"{base_url.rstrip('/')}/v1/videos/{video_id}/content"
    response = requests.get(url, headers=headers, timeout=timeout)
    try:
        body = response.json()
    except ValueError:
        body = {"non_json_response": response.text}

    result: Dict[str, Any] = {
        "ok": response.ok,
        "request_summary": _request_summary(method="GET", url=url, headers=headers),
        "normalized_download": _normalize_download_response(body) if response.ok else None,
        "raw_response": body,
        "status_code": response.status_code,
        "saved_file": None,
        "error": None if response.ok else "下载信息查询失败",
    }
    if not response.ok:
        return result

    video_url = result["normalized_download"].get("video_url")
    if not video_url:
        result["ok"] = False
        result["error"] = "下载接口未返回 video_url/url"
        return result

    if not save_video:
        return result

    output_dir.mkdir(parents=True, exist_ok=True)
    target = output_dir / f"{_safe_name(filename_prefix or 'sora')}_{video_id}.mp4"
    video_response = requests.get(video_url, timeout=timeout, stream=True)
    if not video_response.ok:
        result["ok"] = False
        result["error"] = f"二次下载 MP4 失败: HTTP {video_response.status_code}"
        return result
    with target.open("wb") as handle:
        for chunk in video_response.iter_content(chunk_size=1024 * 512):
            if chunk:
                handle.write(chunk)
    result["saved_file"] = str(target)
    return result


def build_parser() -> argparse.ArgumentParser:
    common_parser = argparse.ArgumentParser(add_help=False)
    common_parser.add_argument("--api-key", help="API Key，不传则读取 .env")
    common_parser.add_argument("--base-url", default=_env_base_url(), help="API 基础 URL")
    common_parser.add_argument("--timeout", type=int, default=DEFAULT_TIMEOUT, help="HTTP 超时秒数")
    common_parser.add_argument("--project-name", default=DEFAULT_PROJECT_NAME, help="项目名，用于默认输出目录")
    common_parser.add_argument("--output-dir", help="覆盖默认输出目录")
    common_parser.add_argument("--filename-prefix", default="sora", help="报告/视频文件名前缀")
    common_parser.add_argument("--report-json", help="显式指定报告 JSON 路径")

    parser = argparse.ArgumentParser(
        description="Submit and manage AnyFast Sora 2 video tasks",
        parents=[common_parser],
    )

    subparsers = parser.add_subparsers(dest="command", required=True)

    submit_parser = subparsers.add_parser("submit", help="创建视频任务", parents=[common_parser])
    submit_parser.add_argument("--prompt", required=True, help="视频提示词")
    submit_parser.add_argument(
        "--model",
        help=f"模型 ID；不传时默认按最高档位候选链尝试（当前为 {DEFAULT_MODEL}）",
    )
    submit_parser.add_argument("--image", help="单张参考图，支持本地/远程/data URL")
    submit_parser.add_argument("--remix-video-id", help="已完成视频 ID")
    submit_parser.add_argument("--seconds", default=DEFAULT_SECONDS, choices=sorted(ALLOWED_SECONDS), help="4 / 8 / 12")
    submit_parser.add_argument("--size", default=DEFAULT_SIZE, choices=sorted(ALLOWED_SIZES), help="输出分辨率")
    submit_parser.add_argument("--dry-run", action="store_true", help="仅打印请求摘要，不实际提交")
    submit_parser.add_argument("--print-payload", action="store_true", help="打印最终请求摘要")
    submit_parser.add_argument("--no-model-alias-fallback", action="store_true", help="禁用 official-* 模型别名回退")

    status_parser = subparsers.add_parser("status", help="查询任务状态", parents=[common_parser])
    status_parser.add_argument("--video-id", required=True, help="视频任务 ID")

    download_parser = subparsers.add_parser("download", help="下载视频结果", parents=[common_parser])
    download_parser.add_argument("--video-id", required=True, help="视频任务 ID")
    download_parser.add_argument("--no-save-video", action="store_true", help="只查询 video_url，不下载 MP4")

    run_parser = subparsers.add_parser("run", help="创建 + 轮询 + 下载", parents=[common_parser])
    run_parser.add_argument("--prompt", required=True, help="视频提示词")
    run_parser.add_argument(
        "--model",
        help=f"模型 ID；不传时默认按最高档位候选链尝试（当前为 {DEFAULT_MODEL}）",
    )
    run_parser.add_argument("--image", help="单张参考图，支持本地/远程/data URL")
    run_parser.add_argument("--remix-video-id", help="已完成视频 ID")
    run_parser.add_argument("--seconds", default=DEFAULT_SECONDS, choices=sorted(ALLOWED_SECONDS), help="4 / 8 / 12")
    run_parser.add_argument("--size", default=DEFAULT_SIZE, choices=sorted(ALLOWED_SIZES), help="输出分辨率")
    run_parser.add_argument("--poll-interval", type=int, default=DEFAULT_POLL_INTERVAL, help="轮询间隔秒数")
    run_parser.add_argument("--max-wait-seconds", type=int, default=DEFAULT_MAX_WAIT_SECONDS, help="最大等待秒数")
    run_parser.add_argument("--dry-run", action="store_true", help="仅打印请求摘要，不实际提交")
    run_parser.add_argument("--print-payload", action="store_true", help="打印最终请求摘要")
    run_parser.add_argument("--no-model-alias-fallback", action="store_true", help="禁用 official-* 模型别名回退")
    run_parser.add_argument("--no-save-video", action="store_true", help="只保留 video_url，不下载 MP4")

    return parser


def _resolve_api_key(explicit: Optional[str]) -> str:
    value = explicit or _env_api_key()
    if not value:
        raise ValueError("缺少 API Key，请在 .env 中配置 SORA_API_KEY / ANYFAST_VIDEO_API_KEY / ANYFAST_API_KEY")
    return value


def _resolve_requested_model(explicit: Optional[str]) -> tuple[str, bool]:
    if explicit and explicit.strip():
        return explicit.strip(), True
    return DEFAULT_MODEL, False


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()

    try:
        api_key = _resolve_api_key(args.api_key)
        requested_model, model_was_explicit = _resolve_requested_model(getattr(args, "model", None))
        output_dir = Path(args.output_dir) if args.output_dir else _default_output_dir(args.project_name)

        if args.command == "submit":
            result = submit_video(
                prompt=args.prompt,
                model=requested_model,
                seconds=args.seconds,
                size=args.size,
                image=args.image,
                remix_video_id=args.remix_video_id,
                api_key=api_key,
                base_url=args.base_url,
                timeout=args.timeout,
                dry_run=args.dry_run,
                print_payload=args.print_payload,
                allow_alias_fallback=not args.no_model_alias_fallback,
                model_was_explicit=model_was_explicit,
            )

        elif args.command == "status":
            result = query_status(
                video_id=args.video_id,
                api_key=api_key,
                base_url=args.base_url,
                timeout=args.timeout,
            )

        elif args.command == "download":
            result = download_video_result(
                video_id=args.video_id,
                api_key=api_key,
                base_url=args.base_url,
                timeout=args.timeout,
                output_dir=output_dir,
                filename_prefix=args.filename_prefix,
                save_video=not args.no_save_video,
            )

        elif args.command == "run":
            submit_result = submit_video(
                prompt=args.prompt,
                model=requested_model,
                seconds=args.seconds,
                size=args.size,
                image=args.image,
                remix_video_id=args.remix_video_id,
                api_key=api_key,
                base_url=args.base_url,
                timeout=args.timeout,
                dry_run=args.dry_run,
                print_payload=args.print_payload,
                allow_alias_fallback=not args.no_model_alias_fallback,
                model_was_explicit=model_was_explicit,
            )
            if not submit_result.get("ok"):
                result = {
                    "ok": False,
                    "command": "run",
                    "submit": submit_result,
                    "error": submit_result.get("error") or "创建任务失败",
                }
            elif args.dry_run:
                result = {
                    "ok": True,
                    "command": "run",
                    "submit": submit_result,
                    "diagnostic_hint": "dry-run 未实际进入轮询和下载阶段",
                }
            else:
                video_id = submit_result["normalized_submit"]["id"]
                status_result = poll_until_complete(
                    video_id=video_id,
                    api_key=api_key,
                    base_url=args.base_url,
                    timeout=args.timeout,
                    poll_interval=args.poll_interval,
                    max_wait_seconds=args.max_wait_seconds,
                )
                if not status_result.get("ok"):
                    result = {
                        "ok": False,
                        "command": "run",
                        "submit": submit_result,
                        "status": status_result,
                        "error": status_result.get("error") or "轮询失败",
                    }
                else:
                    download_result = download_video_result(
                        video_id=video_id,
                        api_key=api_key,
                        base_url=args.base_url,
                        timeout=args.timeout,
                        output_dir=output_dir,
                        filename_prefix=args.filename_prefix,
                        save_video=not args.no_save_video,
                    )
                    result = {
                        "ok": download_result.get("ok", False),
                        "command": "run",
                        "submit": submit_result,
                        "status": status_result,
                        "download": download_result,
                        "saved_file": download_result.get("saved_file"),
                        "error": download_result.get("error"),
                    }
        else:
            raise ValueError(f"不支持的命令: {args.command}")

        if "command" not in result:
            result["command"] = args.command
        report_path = _make_report_path(output_dir, args.filename_prefix, args.command, args.report_json)
        _write_json(report_path, result)
        result["report_json"] = str(report_path)
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 0 if result.get("ok") else 1

    except Exception as exc:
        fallback_output_dir = Path(args.output_dir) if getattr(args, "output_dir", None) else _default_output_dir(
            getattr(args, "project_name", DEFAULT_PROJECT_NAME)
        )
        error_result = {
            "ok": False,
            "command": getattr(args, "command", "unknown"),
            "error": str(exc),
        }
        report_path = _make_report_path(
            fallback_output_dir,
            getattr(args, "filename_prefix", "sora"),
            getattr(args, "command", "error"),
            getattr(args, "report_json", None),
        )
        _write_json(report_path, error_result)
        error_result["report_json"] = str(report_path)
        print(json.dumps(error_result, ensure_ascii=False, indent=2))
        return 1


if __name__ == "__main__":
    sys.exit(main())
