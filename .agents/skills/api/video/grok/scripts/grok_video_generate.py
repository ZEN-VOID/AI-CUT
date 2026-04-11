#!/usr/bin/env python3
"""
GROK video generation submit CLI.

Current contract:
- Submit GROK video jobs in JSON or multipart mode
- Read local files, remote URLs, and data URLs as image inputs
- Normalize task_id/id response fields
- Persist a submission report

Current limit:
- PRP does not provide a query/download endpoint, so this script only submits jobs.
"""

from __future__ import annotations

import argparse
import base64
import json
import mimetypes
import os
import re
import sys
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple
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


DEFAULT_BASE_URL = "https://api.ai666.net"
DEFAULT_MODEL = "grok-video-3"
DEFAULT_ASPECT_RATIO = "16:9"
DEFAULT_SIZE = "720P"
DEFAULT_SECONDS = 10
DEFAULT_TIMEOUT = 180
ALLOWED_RATIOS = {"16:9", "9:16", "2:3", "3:2", "1:1"}
ALLOWED_SIZES = {"720P", "1080P"}
ALLOWED_SECONDS = {6, 10, 15}


def _now_stamp() -> str:
    return datetime.now().strftime("%Y%m%d_%H%M%S")


def _safe_name(text: str, max_len: int = 48) -> str:
    normalized = re.sub(r"\s+", "_", text.strip())
    normalized = re.sub(r"[^0-9A-Za-z_\u4e00-\u9fff-]+", "", normalized)
    return (normalized or "grok_video")[:max_len]


def _env_api_key() -> Optional[str]:
    return (
        os.getenv("GROK_API_KEY")
        or os.getenv("AI666_API_KEY")
        or os.getenv("OPENAI_API_KEY")
    )


def _env_base_url() -> str:
    return (
        os.getenv("GROK_API_BASE_URL")
        or os.getenv("AI666_API_BASE_URL")
        or DEFAULT_BASE_URL
    )


def _normalize_auth_header(api_key: str) -> str:
    token = api_key.strip()
    if token.lower().startswith("bearer "):
        return token
    return f"Bearer {token}"


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

    def to_summary(self) -> Dict[str, Any]:
        return {
            "source": self.source,
            "input_type": self.input_type,
            "mime_type": self.mime_type,
            "bytes": len(self.data),
        }


def _read_data_url(value: str) -> ImageInput:
    match = re.match(r"^data:(image/[^;]+);base64,(.+)$", value, re.DOTALL)
    if not match:
        raise ValueError("data URL 格式不合法，需形如 data:image/png;base64,...")
    mime_type = match.group(1)
    b64_data = match.group(2)
    try:
        raw = base64.b64decode(b64_data)
    except Exception as exc:  # pragma: no cover - defensive
        raise ValueError("data URL 中的 base64 内容无法解码") from exc
    return ImageInput(source=value[:64] + "...", input_type="data_url", mime_type=mime_type, data=raw)


def _read_remote_url(value: str, timeout: int) -> ImageInput:
    response = requests.get(value, timeout=timeout)
    response.raise_for_status()
    mime_type = response.headers.get("Content-Type", "").split(";", 1)[0].strip() or _guess_mime_type(value)
    return ImageInput(source=value, input_type="remote_url", mime_type=mime_type, data=response.content)


def _read_local_file(value: str) -> ImageInput:
    path = Path(value).expanduser()
    if not path.is_file():
        raise FileNotFoundError(f"本地图片不存在: {value}")
    return ImageInput(
        source=str(path),
        input_type="local_file",
        mime_type=_guess_mime_type(path.name),
        data=path.read_bytes(),
    )


def _read_image_source(value: str, timeout: int) -> ImageInput:
    if _is_data_url(value):
        return _read_data_url(value)
    if _is_remote_url(value):
        return _read_remote_url(value, timeout=timeout)
    return _read_local_file(value)


def _to_data_url(image: ImageInput) -> str:
    payload = base64.b64encode(image.data).decode("ascii")
    return f"data:{image.mime_type};base64,{payload}"


def _normalize_submission(body: Dict[str, Any]) -> Dict[str, Any]:
    task_id = body.get("task_id") or body.get("id")
    return {
        "task_id": task_id,
        "status": body.get("status"),
        "status_update_time": body.get("status_update_time"),
        "created_at": body.get("created_at"),
    }


def _default_output_dir(project_name: str) -> Path:
    project = project_name.strip() or "测试"
    return Path("output") / "影片" / project / "5-API" / "video" / "grok"


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Submit GROK video generation tasks")
    parser.add_argument("--prompt", required=True, help="视频提示词")
    parser.add_argument("--model", default=DEFAULT_MODEL, help="模型 ID")
    parser.add_argument("--api-key", help="API Key，不传则读取 .env")
    parser.add_argument("--base-url", default=_env_base_url(), help="API 基础 URL")
    parser.add_argument(
        "--request-mode",
        choices=["auto", "json", "multipart"],
        default="auto",
        help="auto 默认优先 JSON；multipart 仅用于严格跟随 OpenAPI 文字版接口",
    )
    parser.add_argument("--image", action="append", default=[], help="图片输入，可重复传入；支持本地/远程/data URL")
    parser.add_argument("--aspect-ratio", default=DEFAULT_ASPECT_RATIO, help="16:9 / 9:16 / 2:3 / 3:2 / 1:1")
    parser.add_argument("--size", default=DEFAULT_SIZE, help="720P / 1080P")
    parser.add_argument("--seconds", type=int, default=DEFAULT_SECONDS, help="6 / 10 / 15")
    parser.add_argument("--project-name", default="测试", help="项目名，用于默认输出目录")
    parser.add_argument("--output-dir", help="覆盖默认输出目录")
    parser.add_argument("--filename-prefix", default="grok_video", help="报告文件名前缀")
    parser.add_argument("--report-json", help="显式指定报告 JSON 路径")
    parser.add_argument("--timeout", type=int, default=DEFAULT_TIMEOUT, help="HTTP 超时秒数")
    parser.add_argument("--dry-run", action="store_true", help="仅打印请求摘要，不实际提交")
    parser.add_argument("--print-payload", action="store_true", help="打印最终请求摘要")
    return parser


def _validate_args(args: argparse.Namespace) -> None:
    if args.aspect_ratio not in ALLOWED_RATIOS:
        raise ValueError(f"aspect-ratio 不合法: {args.aspect_ratio}")
    if args.size not in ALLOWED_SIZES:
        raise ValueError(f"size 不合法: {args.size}")
    if args.seconds not in ALLOWED_SECONDS:
        raise ValueError(f"seconds 不合法: {args.seconds}")


def _resolve_request_mode(request_mode: str, image_count: int) -> str:
    if request_mode == "auto":
        return "json"
    if request_mode == "multipart" and image_count > 1:
        raise ValueError("multipart 模式只支持单张参考图，请改用 json 模式")
    return request_mode


def _build_request_spec(
    *,
    base_url: str,
    mode: str,
    model: str,
    prompt: str,
    aspect_ratio: str,
    size: str,
    seconds: int,
    images: List[ImageInput],
) -> Dict[str, Any]:
    normalized_base = base_url.rstrip("/")
    if mode == "json":
        payload: Dict[str, Any] = {
            "model": model,
            "prompt": prompt,
            "images": [_to_data_url(image) for image in images],
            "aspect_ratio": aspect_ratio,
            "size": size,
            "duration": seconds,
        }
        return {
            "mode": "json",
            "method": "POST",
            "url": f"{normalized_base}/v1/video/create",
            "headers": {"Content-Type": "application/json"},
            "json": payload,
            "files": None,
            "data": None,
        }

    data = {
        "model": model,
        "prompt": prompt,
        "aspect_ratio": aspect_ratio,
        "size": size,
        "seconds": str(seconds),
    }
    files = None
    if images:
        image = images[0]
        extension = mimetypes.guess_extension(image.mime_type) or ".png"
        files = {
            "input_reference": (
                f"reference{extension}",
                image.data,
                image.mime_type,
            )
        }
    return {
        "mode": "multipart",
        "method": "POST",
        "url": f"{normalized_base}/v1/videos",
        "headers": {},
        "json": None,
        "files": files,
        "data": data,
    }


def _request_summary(spec: Dict[str, Any], images: List[ImageInput]) -> Dict[str, Any]:
    summary = {
        "mode": spec["mode"],
        "url": spec["url"],
        "headers": spec["headers"],
        "image_count": len(images),
        "image_inputs": [image.to_summary() for image in images],
    }
    if spec["mode"] == "json":
        payload = dict(spec["json"] or {})
        payload["images"] = [f"<data-url:{i + 1}>" for i, _ in enumerate(images)]
        summary["payload"] = payload
    else:
        summary["form"] = spec["data"]
        summary["files"] = [image.to_summary() for image in images[:1]]
    return summary


def _submit(spec: Dict[str, Any], auth_header: str, timeout: int) -> Dict[str, Any]:
    headers = dict(spec["headers"])
    headers["Authorization"] = auth_header
    response = requests.request(
        spec["method"],
        spec["url"],
        headers=headers,
        json=spec["json"],
        data=spec["data"],
        files=spec["files"],
        timeout=timeout,
    )
    response.raise_for_status()
    try:
        return response.json()
    except json.JSONDecodeError as exc:
        raise RuntimeError("服务端未返回合法 JSON") from exc


def _write_report(report_path: Path, report: Dict[str, Any]) -> None:
    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")


def _normalize_error(exc: Exception, endpoint: Optional[str] = None) -> str:
    base = str(exc)
    if isinstance(exc, requests.exceptions.SSLError):
        return (
            f"连接 {endpoint or '目标端点'} 时 TLS 握手失败（SSL EOF）。"
            " 这通常表示上游 https 端点当前不可用或网关配置异常，而不是请求 payload 本身有误。"
        )
    if isinstance(exc, requests.exceptions.ConnectionError):
        return (
            f"连接 {endpoint or '目标端点'} 时连接被对端直接关闭。"
            " 这通常表示上游服务未正常响应（例如空回复、网关断开），而不是本地参数校验失败。"
        )
    if isinstance(exc, requests.exceptions.Timeout):
        return f"请求 {endpoint or '目标端点'} 超时，上游服务可能拥堵或不可达。"
    return base


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    endpoint_for_error: Optional[str] = None

    try:
        _validate_args(args)
        resolved_mode = _resolve_request_mode(args.request_mode, len(args.image))
        images = [_read_image_source(item, timeout=args.timeout) for item in args.image]
        if resolved_mode == "multipart" and len(images) > 1:
            raise ValueError("multipart 模式只支持单张图片")

        spec = _build_request_spec(
            base_url=args.base_url,
            mode=resolved_mode,
            model=args.model,
            prompt=args.prompt,
            aspect_ratio=args.aspect_ratio,
            size=args.size,
            seconds=args.seconds,
            images=images,
        )
        summary = _request_summary(spec, images)
        endpoint_for_error = spec["url"]

        output_dir = Path(args.output_dir) if args.output_dir else _default_output_dir(args.project_name)
        report_path = Path(args.report_json) if args.report_json else output_dir / f"{args.filename_prefix}_{_now_stamp()}.json"

        if args.print_payload or args.dry_run:
            print(json.dumps(summary, ensure_ascii=False, indent=2))
        if args.dry_run:
            report = {
                "ok": True,
                "dry_run": True,
                "request_mode": resolved_mode,
                "endpoint": spec["url"],
                "request_summary": summary,
                "image_inputs": [image.to_summary() for image in images],
                "normalized_submission": None,
                "raw_response": None,
                "error": None,
            }
            _write_report(report_path, report)
            print(f"✅ Dry run 完成，报告已写入: {report_path}")
            return 0

        api_key = args.api_key or _env_api_key()
        if not api_key:
            raise ValueError("缺少 API Key，请设置 GROK_API_KEY / AI666_API_KEY / OPENAI_API_KEY 或传 --api-key")

        response_body = _submit(spec, _normalize_auth_header(api_key), args.timeout)
        normalized = _normalize_submission(response_body)
        report = {
            "ok": True,
            "dry_run": False,
            "request_mode": resolved_mode,
            "endpoint": spec["url"],
            "request_summary": summary,
            "image_inputs": [image.to_summary() for image in images],
            "normalized_submission": normalized,
            "raw_response": response_body,
            "error": None,
        }
        _write_report(report_path, report)
        print(json.dumps({"report_json": str(report_path), "normalized_submission": normalized}, ensure_ascii=False, indent=2))
        return 2 if normalized.get("status") == "failed" else 0
    except Exception as exc:
        output_dir = Path(args.output_dir) if getattr(args, "output_dir", None) else _default_output_dir(getattr(args, "project_name", "测试"))
        report_path = Path(args.report_json) if getattr(args, "report_json", None) else output_dir / f"{getattr(args, 'filename_prefix', 'grok_video')}_{_now_stamp()}.json"
        error_message = _normalize_error(exc, endpoint=endpoint_for_error)
        report = {
            "ok": False,
            "dry_run": bool(getattr(args, "dry_run", False)),
            "request_mode": getattr(args, "request_mode", "unknown"),
            "endpoint": endpoint_for_error,
            "request_summary": None,
            "image_inputs": [{"source": value} for value in getattr(args, "image", [])],
            "normalized_submission": None,
            "raw_response": None,
            "error": error_message,
        }
        _write_report(report_path, report)
        print(f"❌ {error_message}")
        print(f"📝 错误报告已写入: {report_path}")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
