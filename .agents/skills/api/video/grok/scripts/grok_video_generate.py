#!/usr/bin/env python3
"""
FineAPI Grok Video 3 creation CLI.

Current scope:
- submit/create: create a video task via POST /v1/video/create

The currently confirmed source material covers the create endpoint only.
Status polling and result download must not be invented until their docs are available.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
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


# Highest provider-verified working default as of 2026-04-17 live submit.
DEFAULT_MODEL = "grok-video-3"
DEFAULT_ASPECT_RATIO = "3:2"
DEFAULT_SIZE = "720P"
DEFAULT_PROJECT_NAME = "测试"
DEFAULT_TIMEOUT = 180
ALLOWED_ASPECT_RATIOS = {"2:3", "3:2", "1:1"}
ALLOWED_SIZES = {"720P", "1080P"}


def _now_stamp() -> str:
    return datetime.now().strftime("%Y%m%d_%H%M%S")


def _safe_name(text: str, max_len: int = 64) -> str:
    normalized = re.sub(r"\s+", "_", text.strip())
    normalized = re.sub(r"[^0-9A-Za-z_\u4e00-\u9fff-]+", "", normalized)
    return (normalized or "grok_video")[:max_len]


def _env_api_key() -> Optional[str]:
    return (
        os.getenv("ANYFAST_VIDEO_API_KEY")
        or os.getenv("GROK_VIDEO_API_KEY")
        or os.getenv("ANYFAST_API_KEY")
        or os.getenv("FINEAPI_GROK_API_KEY")
        or os.getenv("FINEAPI_API_KEY")
    )


def _env_base_url() -> Optional[str]:
    return (
        os.getenv("ANYFAST_API_BASE_URL")
        or os.getenv("GROK_VIDEO_API_BASE_URL")
        or os.getenv("FINEAPI_GROK_API_BASE_URL")
        or os.getenv("FINEAPI_API_BASE_URL")
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


def _is_remote_url(value: str) -> bool:
    parsed = urlparse(value)
    return parsed.scheme in {"http", "https"} and bool(parsed.netloc)


def _default_output_dir(project_name: str) -> Path:
    project = project_name.strip() or DEFAULT_PROJECT_NAME
    return Path("output") / "影片" / project / "5-API" / "video" / "grok"


def _write_json(path: Path, data: Dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def _make_report_path(output_dir: Path, prefix: str, command: str, explicit: Optional[str]) -> Path:
    if explicit:
        return Path(explicit)
    stem = _safe_name(prefix or "grok")
    return output_dir / f"{stem}_{command}_report_{_now_stamp()}.json"


def _session_headers(api_key: Optional[str]) -> Dict[str, str]:
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
    }
    if api_key:
        headers["Authorization"] = _normalize_auth_header(api_key)
    return headers


def _request_summary(*, method: str, url: str, headers: Dict[str, str], data: Dict[str, Any]) -> Dict[str, Any]:
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


def _normalize_submit_response(body: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "id": body.get("id"),
        "status": body.get("status"),
        "status_update_time": body.get("status_update_time"),
    }


def _collect_error_strings(response_body: Dict[str, Any]) -> tuple[str, str]:
    text_parts: List[str] = []
    error_code = ""

    nested_error = response_body.get("error")
    if isinstance(nested_error, dict):
        code = nested_error.get("code")
        if isinstance(code, str) and code.strip():
            error_code = code.strip()
            text_parts.append(error_code)
        for key in ("message", "type", "detail", "msg"):
            value = nested_error.get(key)
            if isinstance(value, str) and value.strip():
                text_parts.append(value.strip())

    for key in ("message", "error", "detail", "msg"):
        value = response_body.get(key)
        if isinstance(value, str) and value.strip():
            text_parts.append(value.strip())

    return error_code, " | ".join(text_parts)


def _build_diagnostic_hint(
    *, model: str, size: str, response_body: Optional[Dict[str, Any]] = None
) -> Optional[str]:
    messages: List[str] = []
    if size == "1080P":
        messages.append("文档截图写有 1080P，但同页同时注明“暂只支持 720P”；若失败请先回退到 720P。")
    if response_body:
        error_code, merged = _collect_error_strings(response_body)
        lowered = merged.lower()
        if error_code == "model_not_found" or ("model" in lowered and "not found" in lowered):
            if model == DEFAULT_MODEL:
                messages.append(f"当前默认模型 {DEFAULT_MODEL} 仍是本环境最高已验证可用版本；更高候选模型暂不可用。")
            else:
                messages.append(f"当前模型 {model} 暂无可用渠道；请先回退到 {DEFAULT_MODEL}。")
        if "quota" in merged.lower() or "余额" in merged or "额度" in merged:
            messages.append("当前更像额度或配额问题；优先检查 FineAPI/Grok 通道余额。")
        if "unauthorized" in lowered or "token" in lowered:
            messages.append("当前更像鉴权问题；优先检查 Bearer Token 是否正确。")
    if not messages:
        return None
    return " ".join(messages)


def submit_video(
    *,
    prompt: str,
    model: str,
    aspect_ratio: str,
    size: str,
    images: List[str],
    api_key: Optional[str],
    base_url: str,
    timeout: int,
    dry_run: bool,
    print_payload: bool,
) -> Dict[str, Any]:
    if not prompt.strip():
        raise ValueError("prompt 不能为空")
    if aspect_ratio not in ALLOWED_ASPECT_RATIOS:
        raise ValueError(f"aspect_ratio 不合法: {aspect_ratio}")
    if size not in ALLOWED_SIZES:
        raise ValueError(f"size 不合法: {size}")
    if not images:
        raise ValueError("至少需要一张图片链接，请通过 --image 传入")

    invalid_images = [item for item in images if not _is_remote_url(item)]
    if invalid_images:
        raise ValueError(
            "images 仅接受公网 http/https 链接，以下输入不合法: " + ", ".join(invalid_images)
        )

    if not dry_run and not api_key:
        raise ValueError(
            "缺少 API Key，请在 .env 中配置 GROK_VIDEO_API_KEY / ANYFAST_VIDEO_API_KEY / "
            "FINEAPI_GROK_API_KEY / ANYFAST_API_KEY / FINEAPI_API_KEY"
        )

    headers = _session_headers(api_key)
    url = f"{base_url.rstrip('/')}/v1/video/create"
    payload = {
        "model": model,
        "prompt": prompt,
        "aspect_ratio": aspect_ratio,
        "size": size,
        "images": images,
    }
    request_summary = _request_summary(method="POST", url=url, headers=headers, data=payload)
    if print_payload or dry_run:
        print(json.dumps(request_summary, ensure_ascii=False, indent=2))
    if dry_run:
        return {
            "ok": True,
            "request_summary": request_summary,
            "normalized_submit": None,
            "raw_response": None,
            "diagnostic_hint": _build_diagnostic_hint(model=model, size=size),
        }

    response = requests.post(url, headers=headers, json=payload, timeout=timeout)
    try:
        body = response.json()
    except ValueError:
        body = {"non_json_response": response.text}

    return {
        "ok": response.ok,
        "request_summary": request_summary,
        "normalized_submit": _normalize_submit_response(body) if response.ok else None,
        "raw_response": body,
        "status_code": response.status_code,
        "error": None if response.ok else "创建任务失败",
        "diagnostic_hint": _build_diagnostic_hint(
            model=model,
            size=size,
            response_body=body if isinstance(body, dict) else None,
        ),
    }


def build_parser() -> argparse.ArgumentParser:
    common_parser = argparse.ArgumentParser(add_help=False)
    common_parser.add_argument("--api-key", help="API Key，不传则读取 .env")
    common_parser.add_argument("--base-url", default=_env_base_url(), help="API 基础 URL；当前必须显式配置")
    common_parser.add_argument("--timeout", type=int, default=DEFAULT_TIMEOUT, help="HTTP 超时秒数")
    common_parser.add_argument("--project-name", default=DEFAULT_PROJECT_NAME, help="项目名，用于默认输出目录")
    common_parser.add_argument("--output-dir", help="覆盖默认输出目录")
    common_parser.add_argument("--filename-prefix", default="grok", help="报告文件名前缀")
    common_parser.add_argument("--report-json", help="显式指定报告 JSON 路径")

    parser = argparse.ArgumentParser(
        description="Submit FineAPI Grok Video 3 create tasks",
        parents=[common_parser],
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    submit_parser = subparsers.add_parser(
        "submit",
        aliases=["create"],
        help="创建视频任务",
        parents=[common_parser],
    )
    submit_parser.add_argument("--prompt", required=True, help="视频提示词")
    submit_parser.add_argument("--model", default=DEFAULT_MODEL, help="模型 ID")
    submit_parser.add_argument(
        "--aspect-ratio",
        default=DEFAULT_ASPECT_RATIO,
        choices=sorted(ALLOWED_ASPECT_RATIOS),
        help="2:3 / 3:2 / 1:1",
    )
    submit_parser.add_argument(
        "--size",
        default=DEFAULT_SIZE,
        choices=sorted(ALLOWED_SIZES),
        help="720P / 1080P（当前优先推荐 720P）",
    )
    submit_parser.add_argument(
        "--image",
        dest="images",
        action="append",
        required=True,
        help="公网图片链接，可重复传参",
    )
    submit_parser.add_argument("--dry-run", action="store_true", help="仅打印请求摘要，不实际提交")
    submit_parser.add_argument("--print-payload", action="store_true", help="打印最终请求摘要")

    return parser


def _resolve_api_key(explicit: Optional[str], *, required: bool = True) -> str:
    value = explicit or _env_api_key()
    if not value and required:
        raise ValueError(
            "缺少 API Key，请在 .env 中配置 GROK_VIDEO_API_KEY / ANYFAST_VIDEO_API_KEY / "
            "FINEAPI_GROK_API_KEY / ANYFAST_API_KEY / FINEAPI_API_KEY"
        )
    return value or ""


def _resolve_base_url(explicit: Optional[str]) -> str:
    value = explicit or _env_base_url()
    if not value:
        raise ValueError(
            "缺少 API Base URL，请通过 --base-url 或 .env 中的 GROK_VIDEO_API_BASE_URL / "
            "ANYFAST_API_BASE_URL / FINEAPI_GROK_API_BASE_URL / FINEAPI_API_BASE_URL 提供。"
        )
    return value.rstrip("/")


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()

    try:
        api_key = _resolve_api_key(args.api_key, required=not getattr(args, "dry_run", False))
        base_url = _resolve_base_url(args.base_url)
        output_dir = Path(args.output_dir) if args.output_dir else _default_output_dir(args.project_name)

        if args.command in {"submit", "create"}:
            result = submit_video(
                prompt=args.prompt,
                model=args.model,
                aspect_ratio=args.aspect_ratio,
                size=args.size,
                images=args.images,
                api_key=api_key,
                base_url=base_url,
                timeout=args.timeout,
                dry_run=args.dry_run,
                print_payload=args.print_payload,
            )
        else:
            raise ValueError(f"不支持的命令: {args.command}")

        result["command"] = args.command
        report_path = _make_report_path(output_dir, args.filename_prefix, args.command, args.report_json)
        result["report_json"] = str(report_path)
        _write_json(report_path, result)
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
            getattr(args, "filename_prefix", "grok"),
            getattr(args, "command", "error"),
            getattr(args, "report_json", None),
        )
        _write_json(report_path, error_result)
        error_result["report_json"] = str(report_path)
        print(json.dumps(error_result, ensure_ascii=False, indent=2))
        return 1


if __name__ == "__main__":
    sys.exit(main())
