#!/usr/bin/env python3
"""
Man-Tui Sora async video CLI.

Supports:
- create: submit a Sora video task via application/json
- status: query task status, optionally wait until terminal state
- download: fetch final MP4 from watermark_free_url/video_url after querying status
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
import time
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, Optional, Tuple
from urllib.parse import urlsplit, urlunsplit

import requests

try:
    from dotenv import load_dotenv

    try:
        load_dotenv()
    except Exception:
        load_dotenv(dotenv_path=str(Path.cwd() / ".env"))
except ImportError:
    print(
        "❌ 缺少依赖，请先执行: "
        "pip install -r .agents/skills/api/man-tui/video/sora/requirements.txt"
    )
    sys.exit(1)


DEFAULT_MODEL = "sora-2"
DEFAULT_BASE_URL = "https://api.man-tui.com"
DEFAULT_SECONDS = 10
DEFAULT_SIZE = "720x1280"
DEFAULT_GROUP = "default"
DEFAULT_GROUP_TRANSPORT = "off"
DEFAULT_GROUP_HEADER = "X-Group"
DEFAULT_TIMEOUT = 180
DEFAULT_POLL_INTERVAL = 10
DEFAULT_WAIT_TIMEOUT = 1800
DEFAULT_OUTPUT_ROOT = Path("output/影片")

SECONDS_CHOICES = {10, 15}
SIZE_CHOICES = {"720x1280", "1280x720"}
TASK_KIND_CHOICES = {"project", "test", "temp"}
GROUP_TRANSPORT_CHOICES = {"off", "header", "body", "both"}
TERMINAL_STATUSES = {"completed", "failed", "error", "cancelled", "canceled"}


def _now_stamp() -> str:
    return datetime.now().strftime("%Y%m%d_%H%M%S")


def _safe_name(text: str, max_len: int = 64) -> str:
    text = re.sub(r"\s+", "_", text.strip())
    text = re.sub(r"[^0-9A-Za-z_\u4e00-\u9fff-]+", "", text)
    return text[:max_len] or "task"


def _redact_text(value: Any) -> Any:
    if value is None:
        return None
    text = str(value)
    text = re.sub(r"Bearer\s+[A-Za-z0-9._-]+", "Bearer <redacted>", text, flags=re.IGNORECASE)
    text = re.sub(r"sk-[A-Za-z0-9]+", "sk-<redacted>", text)
    text = re.sub(r"(api[_-]?key=)[^&\\s]+", r"\1<redacted>", text, flags=re.IGNORECASE)
    text = re.sub(r"(key=)[^&\\s]+", r"\1<redacted>", text, flags=re.IGNORECASE)
    return text


def _redact_url(url: str) -> str:
    split = urlsplit(url)
    if not split.query:
        return url
    pairs = []
    for chunk in split.query.split("&"):
        if "=" not in chunk:
            pairs.append(chunk)
            continue
        key, value = chunk.split("=", 1)
        lowered = key.lower()
        if lowered.startswith("x-amz-") or lowered in {
            "key",
            "api_key",
            "token",
            "sig",
            "signature",
            "expires",
            "x-oss-signature",
        }:
            pairs.append(f"{key}=<redacted>")
        else:
            pairs.append(f"{key}={value}")
    return urlunsplit((split.scheme, split.netloc, split.path, "&".join(pairs), split.fragment))


def _redact_obj(obj: Any) -> Any:
    if isinstance(obj, dict):
        redacted: Dict[str, Any] = {}
        for key, value in obj.items():
            if str(key).lower() in {"authorization", "api_key", "x-api-key"}:
                redacted[key] = "<redacted>"
            else:
                redacted[key] = _redact_obj(value)
        return redacted
    if isinstance(obj, list):
        return [_redact_obj(item) for item in obj]
    if isinstance(obj, str):
        if obj.startswith("http://") or obj.startswith("https://"):
            return _redact_text(_redact_url(obj))
        return _redact_text(obj)
    return obj


def _load_api_key(explicit: Optional[str]) -> str:
    key = explicit or os.getenv("MAN_TUI_API_KEY")
    if not key:
        raise RuntimeError("缺少 API Key，请在根目录 .env 中配置 MAN_TUI_API_KEY 或显式传 --api-key")
    return key


def _load_base_url(explicit: Optional[str]) -> str:
    base = explicit or os.getenv("MAN_TUI_API_BASE_URL") or DEFAULT_BASE_URL
    return base.rstrip("/")


def _project_name(task_kind: str, project_name: Optional[str]) -> str:
    if project_name:
        return project_name
    if task_kind == "test":
        return "测试"
    if task_kind == "temp":
        return "临时"
    return "未命名项目"


def _resolve_output_dir(
    output_dir: Optional[str],
    project_name: Optional[str],
    task_kind: str,
) -> Path:
    if output_dir:
        return Path(output_dir)
    resolved_project = _project_name(task_kind, project_name)
    return DEFAULT_OUTPUT_ROOT / resolved_project / "5-API" / "video" / "man-tui" / "sora"


def _ensure_parent(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)


def _default_report_path(command: str, output_dir: Path) -> Path:
    output_dir.mkdir(parents=True, exist_ok=True)
    return output_dir / f"man_tui_sora_{command}_report_{_now_stamp()}.json"


def _write_json(path: Path, payload: Dict[str, Any]) -> None:
    _ensure_parent(path)
    path.write_text(
        json.dumps(_redact_obj(payload), ensure_ascii=False, indent=2),
        encoding="utf-8",
    )


def _headers(
    api_key: str,
    group: Optional[str] = None,
    group_transport: str = "off",
    group_header: str = DEFAULT_GROUP_HEADER,
    include_json_content_type: bool = False,
) -> Dict[str, str]:
    headers = {
        "Authorization": f"Bearer {api_key}",
    }
    if include_json_content_type:
        headers["Content-Type"] = "application/json"
    if group and group_transport in {"header", "both"}:
        headers[group_header] = group
    return headers


def _normalize_seconds(value: int) -> int:
    if value not in SECONDS_CHOICES:
        raise ValueError(f"seconds 非法，允许值: {sorted(SECONDS_CHOICES)}")
    return value


def _normalize_size(value: str) -> str:
    value = value.strip()
    if value not in SIZE_CHOICES:
        raise ValueError(f"size 非法，允许值: {sorted(SIZE_CHOICES)}")
    return value


def _normalize_task_kind(value: str) -> str:
    value = value.strip().lower()
    if value not in TASK_KIND_CHOICES:
        raise ValueError(f"task_kind 非法，允许值: {sorted(TASK_KIND_CHOICES)}")
    return value


def _normalize_group_transport(value: str) -> str:
    value = value.strip().lower()
    if value not in GROUP_TRANSPORT_CHOICES:
        raise ValueError(f"group_transport 非法，允许值: {sorted(GROUP_TRANSPORT_CHOICES)}")
    return value


def _normalize_group_header(value: str) -> str:
    candidate = value.strip()
    if not candidate or ":" in candidate or "\n" in candidate or "\r" in candidate:
        raise ValueError("group_header 非法，必须是非空且不包含换行或冒号的 header 名")
    return candidate


def _resolve_group_settings(args: argparse.Namespace) -> Tuple[str, str, str]:
    group = (getattr(args, "group", None) or os.getenv("MAN_TUI_API_GROUP") or DEFAULT_GROUP).strip()
    group_transport = _normalize_group_transport(
        getattr(args, "group_transport", None)
        or os.getenv("MAN_TUI_API_GROUP_TRANSPORT")
        or DEFAULT_GROUP_TRANSPORT
    )
    group_header = _normalize_group_header(
        getattr(args, "group_header", None)
        or os.getenv("MAN_TUI_API_GROUP_HEADER")
        or DEFAULT_GROUP_HEADER
    )
    if group_transport != "off" and not group:
        raise ValueError("启用 group 路由时，group 不能为空")
    return group, group_transport, group_header


def _normalize_reference_url(value: Optional[str]) -> Optional[str]:
    if not value:
        return None
    candidate = value.strip()
    if not re.match(r"^https?://", candidate, flags=re.IGNORECASE):
        raise ValueError("input_reference 必须是公网可访问的 http/https URL，不支持本地路径")
    return candidate


def _create_request_summary(args: argparse.Namespace, output_dir: Path) -> Dict[str, Any]:
    return {
        "model": args.model,
        "prompt": args.prompt,
        "seconds": args.seconds,
        "size": args.size,
        "input_reference": args.input_reference,
        "group": getattr(args, "group", None),
        "group_transport": getattr(args, "group_transport", None),
        "group_header": getattr(args, "group_header", None),
        "wait": args.wait,
        "poll_interval": args.poll_interval,
        "wait_timeout": args.wait_timeout,
        "download_on_complete": args.download_on_complete,
        "output_dir": str(output_dir),
        "task_kind": args.task_kind,
        "project_name": args.project_name,
    }


def _terminal_status(status: Optional[str]) -> bool:
    if not status:
        return False
    return status.lower() in TERMINAL_STATUSES


def _build_output_path(
    task_id: str,
    output: Optional[str],
    output_dir: Path,
) -> Path:
    if output:
        return Path(output)
    output_dir.mkdir(parents=True, exist_ok=True)
    return output_dir / f"{_safe_name(task_id)}.mp4"


def _extract_download_url(payload: Dict[str, Any]) -> Optional[str]:
    candidates = []
    for key in ("watermark_free_url", "video_url"):
        value = payload.get(key)
        if isinstance(value, str) and value.strip():
            candidates.append(value.strip())

    result = payload.get("result")
    if isinstance(result, dict):
        for key in ("watermark_free_url", "video_url", "share_url"):
            value = result.get(key)
            if isinstance(value, str) and value.strip():
                candidates.append(value.strip())

    for candidate in candidates:
        if re.match(r"^https?://", candidate, flags=re.IGNORECASE):
            return candidate
    return None


def _status_downloadable(payload: Dict[str, Any]) -> Tuple[bool, Optional[str]]:
    status = str(payload.get("status") or "").lower()
    if status != "completed":
        return False, "任务尚未 completed，不能下载"
    if payload.get("content_violation") is True:
        return False, "任务命中 content_violation，视频不可下载"
    url = _extract_download_url(payload)
    if not url:
        return False, "完成态响应中缺少可用下载 URL"
    return True, None


def create_task(
    base_url: str,
    api_key: str,
    args: argparse.Namespace,
    output_dir: Path,
) -> Dict[str, Any]:
    request_summary = _create_request_summary(args, output_dir)
    body = {
        "prompt": args.prompt,
        "model": args.model,
        "seconds": str(_normalize_seconds(args.seconds)),
        "size": _normalize_size(args.size),
    }
    if args.group and args.group_transport in {"body", "both"}:
        body["group"] = args.group
    reference_url = _normalize_reference_url(args.input_reference)
    if reference_url:
        body["input_reference"] = reference_url
        request_summary["input_reference"] = reference_url

    if args.print_request or args.dry_run:
        print(json.dumps(_redact_obj({"request_summary": request_summary, "json_body": body}), ensure_ascii=False, indent=2))
    if args.dry_run:
        return {
            "ok": True,
            "dry_run": True,
            "command": "create",
            "request_summary": request_summary,
            "json_body": body,
        }

    url = f"{base_url}/v1/videos"
    try:
        response = requests.post(
            url,
            headers=_headers(
                api_key,
                group=args.group,
                group_transport=args.group_transport,
                group_header=args.group_header,
                include_json_content_type=True,
            ),
            json=body,
            timeout=args.timeout,
        )
        response.raise_for_status()
        body_json = response.json()
        return {
            "ok": True,
            "dry_run": False,
            "command": "create",
            "request_summary": request_summary,
            "response": body_json,
        }
    except requests.HTTPError as exc:
        body_text = exc.response.text if exc.response is not None else None
        raise RuntimeError(f"HTTP {exc.response.status_code if exc.response else 'ERR'}: {body_text}") from exc


def fetch_status(
    base_url: str,
    api_key: str,
    task_id: str,
    timeout: int,
    group: Optional[str] = None,
    group_transport: str = "off",
    group_header: str = DEFAULT_GROUP_HEADER,
) -> Dict[str, Any]:
    url = f"{base_url}/v1/videos/{task_id}"
    response = requests.get(
        url,
        headers=_headers(
            api_key,
            group=group,
            group_transport=group_transport,
            group_header=group_header,
            include_json_content_type=False,
        ),
        timeout=timeout,
    )
    try:
        response.raise_for_status()
    except requests.HTTPError as exc:
        body_text = exc.response.text if exc.response is not None else None
        raise RuntimeError(f"HTTP {exc.response.status_code if exc.response else 'ERR'}: {body_text}") from exc
    return response.json()


def wait_for_task(
    base_url: str,
    api_key: str,
    task_id: str,
    poll_interval: int,
    wait_timeout: int,
    timeout: int,
    group: Optional[str] = None,
    group_transport: str = "off",
    group_header: str = DEFAULT_GROUP_HEADER,
) -> Dict[str, Any]:
    start = time.time()
    history = []
    last_payload: Dict[str, Any] | None = None

    while True:
        payload = fetch_status(
            base_url,
            api_key,
            task_id,
            timeout=timeout,
            group=group,
            group_transport=group_transport,
            group_header=group_header,
        )
        last_payload = payload
        history.append(
            {
                "status": payload.get("status"),
                "progress": payload.get("progress"),
                "content_violation": payload.get("content_violation"),
                "polled_at": datetime.now().isoformat(),
            }
        )
        status = str(payload.get("status") or "").lower()
        if _terminal_status(status):
            downloadable, reason = _status_downloadable(payload)
            return {
                "ok": downloadable,
                "timed_out": False,
                "task_id": task_id,
                "response": payload,
                "history": history,
                "error": None if downloadable else reason,
            }
        if time.time() - start >= wait_timeout:
            return {
                "ok": False,
                "timed_out": True,
                "task_id": task_id,
                "response": last_payload,
                "history": history,
                "error": f"等待超时：{wait_timeout}s 内未进入终态",
            }
        time.sleep(max(1, poll_interval))


def download_from_url(
    file_url: str,
    output_path: Path,
    timeout: int,
) -> Dict[str, Any]:
    _ensure_parent(output_path)
    with requests.get(
        file_url,
        timeout=timeout,
        stream=True,
        allow_redirects=True,
    ) as response:
        try:
            response.raise_for_status()
        except requests.HTTPError as exc:
            body_text = exc.response.text if exc.response is not None else None
            raise RuntimeError(f"HTTP {exc.response.status_code if exc.response else 'ERR'}: {body_text}") from exc

        with output_path.open("wb") as handle:
            for chunk in response.iter_content(chunk_size=1024 * 1024):
                if chunk:
                    handle.write(chunk)

        return {
            "ok": True,
            "saved_file": str(output_path),
            "final_url": response.url,
            "status_code": response.status_code,
            "content_type": response.headers.get("Content-Type"),
        }


def download_by_task(
    base_url: str,
    api_key: str,
    task_id: str,
    output_path: Path,
    timeout: int,
    group: Optional[str] = None,
    group_transport: str = "off",
    group_header: str = DEFAULT_GROUP_HEADER,
) -> Dict[str, Any]:
    payload = fetch_status(
        base_url,
        api_key,
        task_id,
        timeout=timeout,
        group=group,
        group_transport=group_transport,
        group_header=group_header,
    )
    downloadable, reason = _status_downloadable(payload)
    if not downloadable:
        raise RuntimeError(reason)
    download_url = _extract_download_url(payload)
    if not download_url:
        raise RuntimeError("缺少可用下载 URL")
    result = {
        "ok": True,
        "task_id": task_id,
        "status_response": payload,
        "download_source_url": download_url,
    }
    result["download_result"] = download_from_url(download_url, output_path, timeout=timeout)
    return result


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Man-Tui Sora async video CLI")
    subparsers = parser.add_subparsers(dest="command", required=True)

    create = subparsers.add_parser("create", help="提交视频生成任务")
    create.add_argument("--prompt", required=True, help="视频提示词")
    create.add_argument("--model", default=DEFAULT_MODEL, help="模型名")
    create.add_argument("--seconds", type=int, default=DEFAULT_SECONDS, help="视频时长")
    create.add_argument("--size", default=DEFAULT_SIZE, help="输出尺寸")
    create.add_argument("--input-reference", help="图生视频参考图 URL")
    create.add_argument("--api-key", help="显式 API Key")
    create.add_argument("--api-base-url", help="显式 API 基础地址")
    create.add_argument("--group", help="请求分组，默认读取 MAN_TUI_API_GROUP，回退 default")
    create.add_argument("--group-transport", help="group 注入方式：off / header / body / both")
    create.add_argument("--group-header", help="当 group 走 header 时使用的 header 名，默认 X-Group")
    create.add_argument("--project-name", help="项目名，用于默认输出目录")
    create.add_argument("--task-kind", default="test", help="project / test / temp")
    create.add_argument("--output-dir", help="输出目录")
    create.add_argument("--report-json", help="报告 JSON 路径")
    create.add_argument("--timeout", type=int, default=DEFAULT_TIMEOUT, help="HTTP timeout 秒数")
    create.add_argument("--wait", action="store_true", help="提交后轮询到终态")
    create.add_argument("--poll-interval", type=int, default=DEFAULT_POLL_INTERVAL, help="轮询间隔秒数")
    create.add_argument("--wait-timeout", type=int, default=DEFAULT_WAIT_TIMEOUT, help="等待超时秒数")
    create.add_argument("--download-on-complete", action="store_true", help="等待成功后自动下载视频")
    create.add_argument("--output", help="自动下载时的视频输出路径")
    create.add_argument("--dry-run", action="store_true", help="只打印请求摘要，不发请求")
    create.add_argument("--print-request", action="store_true", help="打印请求摘要")

    status = subparsers.add_parser("status", help="查询任务状态")
    status.add_argument("task_id", help="任务 ID")
    status.add_argument("--api-key", help="显式 API Key")
    status.add_argument("--api-base-url", help="显式 API 基础地址")
    status.add_argument("--group", help="请求分组，默认读取 MAN_TUI_API_GROUP，回退 default")
    status.add_argument("--group-transport", help="group 注入方式：off / header / body / both")
    status.add_argument("--group-header", help="当 group 走 header 时使用的 header 名，默认 X-Group")
    status.add_argument("--timeout", type=int, default=DEFAULT_TIMEOUT, help="HTTP timeout 秒数")
    status.add_argument("--wait", action="store_true", help="轮询到终态")
    status.add_argument("--poll-interval", type=int, default=DEFAULT_POLL_INTERVAL, help="轮询间隔秒数")
    status.add_argument("--wait-timeout", type=int, default=DEFAULT_WAIT_TIMEOUT, help="等待超时秒数")
    status.add_argument("--download-on-complete", action="store_true", help="完成后自动下载")
    status.add_argument("--project-name", help="项目名，用于默认输出目录")
    status.add_argument("--task-kind", default="test", help="project / test / temp")
    status.add_argument("--output-dir", help="输出目录")
    status.add_argument("--output", help="自动下载时的视频输出路径")
    status.add_argument("--report-json", help="报告 JSON 路径")

    download = subparsers.add_parser("download", help="下载生成后的视频")
    download.add_argument("task_id", help="任务 ID")
    download.add_argument("--api-key", help="显式 API Key")
    download.add_argument("--api-base-url", help="显式 API 基础地址")
    download.add_argument("--group", help="请求分组，默认读取 MAN_TUI_API_GROUP，回退 default")
    download.add_argument("--group-transport", help="group 注入方式：off / header / body / both")
    download.add_argument("--group-header", help="当 group 走 header 时使用的 header 名，默认 X-Group")
    download.add_argument("--timeout", type=int, default=DEFAULT_TIMEOUT, help="HTTP timeout 秒数")
    download.add_argument("--project-name", help="项目名，用于默认输出目录")
    download.add_argument("--task-kind", default="test", help="project / test / temp")
    download.add_argument("--output-dir", help="输出目录")
    download.add_argument("--output", help="输出视频路径")
    download.add_argument("--report-json", help="报告 JSON 路径")

    return parser


def _validate_common(args: argparse.Namespace) -> Tuple[str, str, str, Path]:
    task_kind = _normalize_task_kind(getattr(args, "task_kind", "test"))
    api_key = _load_api_key(getattr(args, "api_key", None))
    base_url = _load_base_url(getattr(args, "api_base_url", None))
    output_dir = _resolve_output_dir(getattr(args, "output_dir", None), getattr(args, "project_name", None), task_kind)
    group, group_transport, group_header = _resolve_group_settings(args)
    args.group = group
    args.group_transport = group_transport
    args.group_header = group_header
    return task_kind, api_key, base_url, output_dir


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()

    try:
        if args.command == "create":
            task_kind, api_key, base_url, output_dir = _validate_common(args)
            args.task_kind = task_kind
            result = create_task(base_url, api_key, args, output_dir)
            if args.dry_run:
                report_path = Path(args.report_json) if args.report_json else _default_report_path("create", output_dir)
                _write_json(report_path, result)
                print(f"✅ dry-run 完成: {report_path}")
                return 0

            response = result.get("response") or {}
            task_id = response.get("task_id") or response.get("id")
            if not task_id:
                raise RuntimeError("创建成功但响应中缺少 task_id")

            if args.wait:
                wait_result = wait_for_task(
                    base_url,
                    api_key,
                    task_id=task_id,
                    poll_interval=args.poll_interval,
                    wait_timeout=args.wait_timeout,
                    timeout=args.timeout,
                    group=args.group,
                    group_transport=args.group_transport,
                    group_header=args.group_header,
                )
                result["wait_result"] = wait_result

                if args.download_on_complete and wait_result.get("ok"):
                    output_path = _build_output_path(task_id, args.output, output_dir)
                    download_url = _extract_download_url(wait_result.get("response") or {})
                    if not download_url:
                        raise RuntimeError("等待完成后缺少可用下载 URL")
                    result["download_result"] = download_from_url(
                        download_url,
                        output_path=output_path,
                        timeout=args.timeout,
                    )

            report_path = Path(args.report_json) if args.report_json else _default_report_path("create", output_dir)
            _write_json(report_path, result)
            print(json.dumps(_redact_obj(result), ensure_ascii=False, indent=2))
            print(f"📄 report: {report_path}")
            overall_ok = bool(result.get("ok"))
            if args.wait:
                overall_ok = overall_ok and bool((result.get("wait_result") or {}).get("ok"))
            if args.download_on_complete:
                overall_ok = overall_ok and bool((result.get("download_result") or {}).get("ok"))
            return 0 if overall_ok else 1

        if args.command == "status":
            task_kind, api_key, base_url, output_dir = _validate_common(args)
            args.task_kind = task_kind
            if args.wait:
                result = wait_for_task(
                    base_url,
                    api_key,
                    task_id=args.task_id,
                    poll_interval=args.poll_interval,
                    wait_timeout=args.wait_timeout,
                    timeout=args.timeout,
                    group=args.group,
                    group_transport=args.group_transport,
                    group_header=args.group_header,
                )
                result["command"] = "status"
            else:
                payload = fetch_status(
                    base_url,
                    api_key,
                    args.task_id,
                    timeout=args.timeout,
                    group=args.group,
                    group_transport=args.group_transport,
                    group_header=args.group_header,
                )
                result = {
                    "ok": True,
                    "command": "status",
                    "task_id": args.task_id,
                    "response": payload,
                }

            if args.download_on_complete:
                response = result.get("response") or {}
                downloadable, reason = _status_downloadable(response)
                if not downloadable:
                    raise RuntimeError(reason)
                output_path = _build_output_path(args.task_id, args.output, output_dir)
                download_url = _extract_download_url(response)
                if not download_url:
                    raise RuntimeError("状态完成但缺少可用下载 URL")
                result["download_result"] = download_from_url(
                    download_url,
                    output_path=output_path,
                    timeout=args.timeout,
                )

            report_path = Path(args.report_json) if args.report_json else _default_report_path("status", output_dir)
            _write_json(report_path, result)
            print(json.dumps(_redact_obj(result), ensure_ascii=False, indent=2))
            print(f"📄 report: {report_path}")
            return 0 if result.get("ok", True) else 1

        if args.command == "download":
            task_kind, api_key, base_url, output_dir = _validate_common(args)
            args.task_kind = task_kind
            output_path = _build_output_path(args.task_id, args.output, output_dir)
            result = {
                "ok": True,
                "command": "download",
                "task_id": args.task_id,
                "request_summary": {
                    "output": str(output_path),
                    "output_dir": str(output_dir),
                },
            }
            download_result = download_by_task(
                base_url,
                api_key,
                task_id=args.task_id,
                output_path=output_path,
                timeout=args.timeout,
                group=args.group,
                group_transport=args.group_transport,
                group_header=args.group_header,
            )
            result.update(download_result)
            report_path = Path(args.report_json) if args.report_json else _default_report_path("download", output_dir)
            _write_json(report_path, result)
            print(json.dumps(_redact_obj(result), ensure_ascii=False, indent=2))
            print(f"📄 report: {report_path}")
            return 0

        raise RuntimeError(f"未知命令: {args.command}")

    except Exception as exc:
        error_payload = {
            "ok": False,
            "command": getattr(args, "command", None),
            "error": _redact_text(exc),
        }
        print(json.dumps(_redact_obj(error_payload), ensure_ascii=False, indent=2), file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
