#!/usr/bin/env python3
"""Unified CLI for Vidu enterprise video APIs."""

from __future__ import annotations

import argparse
import base64
import datetime as dt
import hashlib
import hmac
import json
import mimetypes
import os
import socket
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[5]
DEFAULT_BASE_URL = "https://api.vidu.cn"
DEFAULT_OUTPUT_ROOT = REPO_ROOT / "output" / "影片"
DEFAULT_TIMEOUT = 180
TERMINAL_STATES = {"success", "failed"}

CREATE_ENDPOINTS = {
    "reference2video": "/ent/v2/reference2video",
    "text2video": "/ent/v2/text2video",
    "img2video": "/ent/v2/img2video",
    "start-end2video": "/ent/v2/start-end2video",
    "multiframe": "/ent/v2/multiframe",
    "template": "/ent/v2/template",
    "template-story": "/ent/v2/template-story",
}


class CliError(RuntimeError):
    """User-facing CLI error."""


def load_dotenv(path: Path) -> dict[str, str]:
    values: dict[str, str] = {}
    if not path.exists():
        return values
    for raw_line in path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        key = key.strip()
        value = value.strip().strip("'").strip('"')
        values[key] = value
    return values


def env_value(key: str, dotenv: dict[str, str]) -> str | None:
    return os.environ.get(key) or dotenv.get(key)


def ensure_api_key(args: argparse.Namespace, dotenv: dict[str, str]) -> str:
    key = args.api_key or env_value("VIDU_API_KEY", dotenv)
    if not key:
        raise CliError(
            "缺少 Vidu API Key。请在根目录 .env 中设置 `VIDU_API_KEY`，或显式传入 `--api-key`。"
        )
    return key


def resolve_base_url(args: argparse.Namespace, dotenv: dict[str, str]) -> str:
    value = args.base_url or env_value("VIDU_API_BASE_URL", dotenv) or DEFAULT_BASE_URL
    return value.rstrip("/")


def resolve_project_name(project_name: str | None, task_kind: str) -> str:
    if project_name:
        return project_name
    if task_kind == "test":
        return "测试"
    if task_kind == "temp":
        return "临时"
    return "未命名项目"


def default_output_dir(args: argparse.Namespace) -> Path:
    if getattr(args, "output_dir", None):
        return Path(args.output_dir).expanduser().resolve()
    project_name = resolve_project_name(getattr(args, "project_name", None), getattr(args, "task_kind", "project"))
    return DEFAULT_OUTPUT_ROOT / project_name / "5-API" / "video" / "vidu"


def mkdir(path: Path) -> Path:
    path.mkdir(parents=True, exist_ok=True)
    return path


def utc_stamp() -> str:
    return dt.datetime.now(dt.timezone.utc).strftime("%Y%m%dT%H%M%SZ")


def read_json(path: Path) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise CliError(f"JSON 文件不存在：{path}") from exc
    except json.JSONDecodeError as exc:
        raise CliError(f"JSON 文件解析失败：{path} -> {exc}") from exc


def guess_mime(path: Path, media_kind: str) -> str:
    guessed, _ = mimetypes.guess_type(str(path))
    if guessed and not guessed.startswith(f"{media_kind}/"):
        raise CliError(f"本地文件 `{path}` 不是合法的 {media_kind} 媒体类型：{guessed}")
    if guessed:
        return guessed
    if media_kind == "video":
        return "video/mp4"
    return "image/png"


def path_to_data_url(path: Path, media_kind: str) -> str:
    mime = guess_mime(path, media_kind)
    payload = base64.b64encode(path.read_bytes()).decode("ascii")
    return f"data:{mime};base64,{payload}"


def normalize_media_value(value: Any, media_kind: str) -> Any:
    if not isinstance(value, str):
        return value
    if value.startswith(("http://", "https://", "data:")):
        return value
    candidate = Path(value).expanduser()
    if candidate.exists():
        return path_to_data_url(candidate, media_kind)
    return value


def normalize_reference_payload(payload: dict[str, Any]) -> dict[str, Any]:
    subjects = payload.get("subjects")
    if not isinstance(subjects, list):
        return payload
    normalized_subjects: list[dict[str, Any]] = []
    for subject in subjects:
        if not isinstance(subject, dict):
            normalized_subjects.append(subject)
            continue
        current = dict(subject)
        if isinstance(current.get("images"), list):
            current["images"] = [normalize_media_value(item, "image") for item in current["images"]]
        if isinstance(current.get("videos"), list):
            current["videos"] = [normalize_media_value(item, "video") for item in current["videos"]]
        normalized_subjects.append(current)
    payload["subjects"] = normalized_subjects
    return payload


def normalize_payload_media(mode: str, payload: dict[str, Any]) -> dict[str, Any]:
    normalized = json.loads(json.dumps(payload))
    if mode in {"img2video", "start-end2video", "template", "template-story"} and isinstance(normalized.get("images"), list):
        normalized["images"] = [normalize_media_value(item, "image") for item in normalized["images"]]
    if mode == "multiframe":
        if "start_image" in normalized:
            normalized["start_image"] = normalize_media_value(normalized["start_image"], "image")
        if isinstance(normalized.get("image_settings"), list):
            updated: list[dict[str, Any]] = []
            for item in normalized["image_settings"]:
                if not isinstance(item, dict):
                    updated.append(item)
                    continue
                current = dict(item)
                if "key_image" in current:
                    current["key_image"] = normalize_media_value(current["key_image"], "image")
                updated.append(current)
            normalized["image_settings"] = updated
    if mode == "reference2video":
        normalized = normalize_reference_payload(normalized)
    return normalized


def merge_set(payload: dict[str, Any], key: str, value: Any) -> None:
    if value is not None:
        payload[key] = value


def build_create_payload(args: argparse.Namespace) -> dict[str, Any]:
    payload: dict[str, Any] = {}
    if args.input_json:
        payload = read_json(Path(args.input_json))
        if not isinstance(payload, dict):
            raise CliError("--input-json 必须指向 JSON object。")

    if args.subject_json_file:
        payload["subjects"] = [read_json(Path(item)) for item in args.subject_json_file]
    if args.image_setting_json_file:
        payload["image_settings"] = [read_json(Path(item)) for item in args.image_setting_json_file]

    merge_set(payload, "model", args.model)
    merge_set(payload, "style", args.style)
    merge_set(payload, "prompt", args.prompt)
    merge_set(payload, "duration", args.duration)
    merge_set(payload, "aspect_ratio", args.aspect_ratio)
    merge_set(payload, "resolution", args.resolution)
    merge_set(payload, "seed", args.seed)
    merge_set(payload, "payload", args.payload)
    merge_set(payload, "callback_url", args.callback_url)
    merge_set(payload, "voice_id", args.voice_id)
    merge_set(payload, "audio_type", args.audio_type)
    merge_set(payload, "server_id", args.server_id)
    merge_set(payload, "movement_amplitude", args.movement_amplitude)
    merge_set(payload, "wm_position", args.wm_position)
    merge_set(payload, "wm_url", args.wm_url)
    merge_set(payload, "meta_data", args.meta_data)
    merge_set(payload, "template", args.template_name)
    merge_set(payload, "story", args.story_name)

    if args.image:
        payload["images"] = args.image
    if args.start_image:
        payload["start_image"] = args.start_image

    if args.audio:
        payload["audio"] = True
    if args.auto_subjects:
        payload["auto_subjects"] = True
    if args.off_peak:
        payload["off_peak"] = True
    if args.watermark:
        payload["watermark"] = True

    return normalize_payload_media(args.mode, payload)


def validate_create_payload(mode: str, payload: dict[str, Any]) -> None:
    required_by_mode = {
        "reference2video": ("model", "subjects", "prompt"),
        "text2video": ("model", "prompt"),
        "img2video": ("model", "images"),
        "start-end2video": ("model", "images"),
        "multiframe": ("model", "start_image", "image_settings"),
        "template": ("template", "images"),
        "template-story": ("story", "images"),
    }
    for key in required_by_mode[mode]:
        if key not in payload or payload[key] in (None, "", []):
            raise CliError(f"{mode} 缺少必需字段：{key}")

    if mode == "start-end2video":
        images = payload.get("images")
        if not isinstance(images, list) or len(images) != 2:
            raise CliError("start-end2video 要求 `images` 恰好包含 2 张图。")
    if mode == "multiframe":
        frames = payload.get("image_settings")
        if not isinstance(frames, list) or not (2 <= len(frames) <= 9):
            raise CliError("multiframe 要求 `image_settings` 数量在 2 到 9 之间。")


def redact_query(url: str) -> str:
    parsed = urllib.parse.urlsplit(url)
    if not parsed.scheme:
        return url
    return urllib.parse.urlunsplit((parsed.scheme, parsed.netloc, parsed.path, "<redacted>" if parsed.query else "", ""))


def sanitize(value: Any, api_key: str | None = None) -> Any:
    if isinstance(value, dict):
        return {key: sanitize(val, api_key) for key, val in value.items()}
    if isinstance(value, list):
        return [sanitize(item, api_key) for item in value]
    if isinstance(value, str):
        result = value
        if api_key:
            result = result.replace(api_key, "<redacted>")
        if result.startswith("data:"):
            prefix, _, payload = result.partition(",")
            mime = prefix.split(";")[0].replace("data:", "") or "application/octet-stream"
            return f"<data-url:{mime};bytes≈{len(payload)}>"
        if result.startswith(("http://", "https://")):
            return redact_query(result)
        return result
    return value


def request_json(
    method: str,
    url: str,
    api_key: str,
    payload: dict[str, Any] | None = None,
    timeout: int = DEFAULT_TIMEOUT,
) -> tuple[int, Any]:
    data = None
    headers = {
        "Authorization": f"Token {api_key}",
        "Content-Type": "application/json",
        "Accept": "application/json",
    }
    if payload is not None:
        data = json.dumps(payload, ensure_ascii=False).encode("utf-8")

    request = urllib.request.Request(url=url, data=data, headers=headers, method=method.upper())
    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:
            raw = response.read()
            if not raw:
                return response.getcode(), {}
            return response.getcode(), json.loads(raw.decode("utf-8"))
    except urllib.error.HTTPError as exc:
        body = exc.read().decode("utf-8", errors="replace")
        try:
            parsed = json.loads(body)
        except json.JSONDecodeError:
            parsed = {"error": body}
        return exc.code, parsed
    except (urllib.error.URLError, TimeoutError, socket.timeout) as exc:
        raise CliError(f"网络请求失败：{exc}") from exc


def download_file(url: str, destination: Path, timeout: int = DEFAULT_TIMEOUT) -> None:
    destination.parent.mkdir(parents=True, exist_ok=True)
    request = urllib.request.Request(url=url, method="GET")
    with urllib.request.urlopen(request, timeout=timeout) as response:
        destination.write_bytes(response.read())


def make_report_path(args: argparse.Namespace, slug: str, output_dir: Path) -> Path:
    if getattr(args, "report_json", None):
        return Path(args.report_json).expanduser().resolve()
    return output_dir / f"{slug}.json"


def write_report(args: argparse.Namespace, slug: str, report: dict[str, Any], output_dir: Path, api_key: str | None = None) -> Path:
    mkdir(output_dir)
    report_path = make_report_path(args, slug, output_dir)
    report_path.write_text(
        json.dumps(sanitize(report, api_key), ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    return report_path


def write_create_failure_report(
    args: argparse.Namespace,
    api_key: str,
    base_url: str,
    endpoint: str,
    payload: dict[str, Any],
    output_dir: Path,
    *,
    status_code: int | None = None,
    error_body: Any = None,
    error_message: str | None = None,
) -> Path:
    timestamp = dt.datetime.now(dt.timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    report: dict[str, Any] = {
        "command": "create",
        "mode": args.mode,
        "base_url": base_url,
        "endpoint": endpoint,
        "request_body": payload,
        "status": "create_failed",
    }
    if status_code is not None:
        report["http_status"] = status_code
    if error_body is not None:
        report["error_response"] = error_body
    if error_message is not None:
        report["error"] = error_message
    return write_report(args, f"create-{args.mode}-failed-{timestamp}", report, output_dir, api_key)


def resolve_creation_url(task_result: dict[str, Any], creation_index: int, watermarked: bool) -> tuple[str, dict[str, Any]]:
    creations = task_result.get("creations")
    if not isinstance(creations, list) or not creations:
        raise CliError("任务已完成，但查询结果里没有 `creations`。")
    if creation_index < 0 or creation_index >= len(creations):
        raise CliError(f"creation_index 越界：{creation_index}，当前只有 {len(creations)} 个生成物。")
    creation = creations[creation_index]
    if not isinstance(creation, dict):
        raise CliError("生成物结构异常，不是 object。")
    key = "watermarked_url" if watermarked else "url"
    url = creation.get(key) or creation.get("url") or creation.get("watermarked_url")
    if not url:
        raise CliError("查询结果缺少可下载生成物链接。")
    return str(url), creation


def output_video_path(args: argparse.Namespace, task_id: str, creation: dict[str, Any], output_dir: Path) -> Path:
    if getattr(args, "output", None):
        return Path(args.output).expanduser().resolve()
    creation_id = creation.get("id", "creation")
    return output_dir / f"{task_id}-{creation_id}.mp4"


def poll_task_until_terminal(
    args: argparse.Namespace,
    api_key: str,
    base_url: str,
    task_id: str,
) -> dict[str, Any]:
    poll_interval = max(args.poll_interval, 1)
    deadline = time.time() + args.wait_timeout
    last_body: dict[str, Any] | None = None
    while time.time() <= deadline:
        _, body = request_json("GET", f"{base_url}/ent/v2/tasks/{task_id}/creations", api_key)
        if isinstance(body, dict):
            last_body = body
            state = body.get("state")
            if state in TERMINAL_STATES:
                return body
        time.sleep(poll_interval)
    if last_body is None:
        raise CliError("轮询超时，且未拿到任何任务查询结果。")
    last_body["_timeout"] = True
    return last_body


def handle_create(args: argparse.Namespace, dotenv: dict[str, str]) -> int:
    api_key = ensure_api_key(args, dotenv)
    base_url = resolve_base_url(args, dotenv)
    output_dir = mkdir(default_output_dir(args))
    payload = build_create_payload(args)
    validate_create_payload(args.mode, payload)
    endpoint = CREATE_ENDPOINTS[args.mode]

    if args.print_request or args.dry_run:
        request_preview = {
            "method": "POST",
            "url": f"{base_url}{endpoint}",
            "headers": {
                "Authorization": "Token <redacted>",
                "Content-Type": "application/json",
            },
            "payload": sanitize(payload, api_key),
        }
        print(json.dumps(request_preview, ensure_ascii=False, indent=2))
        if args.dry_run:
            return 0

    status_code, body = request_json("POST", f"{base_url}{endpoint}", api_key, payload=payload)
    if status_code >= 400:
        report_path = write_create_failure_report(
            args,
            api_key,
            base_url,
            endpoint,
            payload,
            output_dir,
            status_code=status_code,
            error_body=body,
        )
        raise CliError(
            f"创建任务失败（HTTP {status_code}）：{json.dumps(sanitize(body, api_key), ensure_ascii=False)}；"
            f"报告已写入 {report_path}"
        )
    if not isinstance(body, dict):
        report_path = write_create_failure_report(
            args,
            api_key,
            base_url,
            endpoint,
            payload,
            output_dir,
            error_message="创建任务响应不是 JSON object。",
            error_body=body,
        )
        raise CliError(f"创建任务响应不是 JSON object。报告已写入 {report_path}")

    task_id = str(body.get("id") or body.get("task_id") or "")
    if not task_id:
        report_path = write_create_failure_report(
            args,
            api_key,
            base_url,
            endpoint,
            payload,
            output_dir,
            error_message="创建任务成功，但响应里缺少 `id/task_id`。",
            error_body=body,
        )
        raise CliError(f"创建任务成功，但响应里缺少 `id/task_id`。报告已写入 {report_path}")

    report: dict[str, Any] = {
        "command": "create",
        "mode": args.mode,
        "base_url": base_url,
        "endpoint": endpoint,
        "request_body": payload,
        "response": body,
        "task_id": task_id,
    }

    wait_status = "not_requested"
    if args.wait:
        try:
            task_result = poll_task_until_terminal(args, api_key, base_url, task_id)
            report["task_result"] = task_result
            wait_status = "terminal" if task_result.get("state") in TERMINAL_STATES else "timeout"
            if task_result.get("state") == "success" and args.download_on_complete:
                url, creation = resolve_creation_url(task_result, args.creation_index, args.download_watermarked)
                destination = output_video_path(args, task_id, creation, output_dir)
                download_file(url, destination)
                report["download"] = {
                    "selected_url": url,
                    "selected_url_kind": "watermarked_url" if args.download_watermarked else "url",
                    "saved_file": str(destination),
                }
        except CliError as exc:
            wait_status = "poll_error"
            report["task_result"] = {
                "state": "poll_error",
                "error": str(exc),
            }

    report_path = write_report(args, f"create-{args.mode}-{task_id}", report, output_dir, api_key)
    print(
        json.dumps(
            {"task_id": task_id, "wait_status": wait_status, "report_json": str(report_path)},
            ensure_ascii=False,
        )
    )
    return 0


def handle_task(args: argparse.Namespace, dotenv: dict[str, str]) -> int:
    api_key = ensure_api_key(args, dotenv)
    base_url = resolve_base_url(args, dotenv)
    output_dir = mkdir(default_output_dir(args))
    task_id = args.task_id

    wait_status = "not_requested"
    if args.wait:
        try:
            body = poll_task_until_terminal(args, api_key, base_url, task_id)
            wait_status = "terminal" if body.get("state") in TERMINAL_STATES else "timeout"
        except CliError as exc:
            body = {"state": "poll_error", "error": str(exc), "id": task_id}
            wait_status = "poll_error"
    else:
        status_code, body = request_json("GET", f"{base_url}/ent/v2/tasks/{task_id}/creations", api_key)
        if status_code >= 400:
            raise CliError(f"任务查询失败（HTTP {status_code}）：{json.dumps(sanitize(body, api_key), ensure_ascii=False)}")

    if not isinstance(body, dict):
        raise CliError("任务查询响应不是 JSON object。")

    report: dict[str, Any] = {
        "command": "task",
        "task_id": task_id,
        "base_url": base_url,
        "response": body,
    }

    if body.get("state") == "success" and args.download_on_complete:
        url, creation = resolve_creation_url(body, args.creation_index, args.download_watermarked)
        destination = output_video_path(args, task_id, creation, output_dir)
        download_file(url, destination)
        report["download"] = {
            "selected_url": url,
            "selected_url_kind": "watermarked_url" if args.download_watermarked else "url",
            "saved_file": str(destination),
        }

    report_path = write_report(args, f"task-{task_id}", report, output_dir, api_key)
    print(
        json.dumps(
            {
                "task_id": task_id,
                "state": body.get("state"),
                "wait_status": wait_status,
                "report_json": str(report_path),
            },
            ensure_ascii=False,
        )
    )
    return 0


def build_list_query(args: argparse.Namespace) -> str:
    query: list[tuple[str, Any]] = []
    if args.created_from:
        query.append(("created_at.from", args.created_from))
    if args.created_to:
        query.append(("created_at.to", args.created_to))
    for item in args.task_id_filter:
        query.append(("task_ids", item))
    for item in args.template_filter:
        query.append(("templates", item))
    for item in args.model_version:
        query.append(("model_versions", item))
    for item in args.resolution_filter:
        query.append(("resolutions", item))
    for item in args.state:
        query.append(("states", item))
    if args.page is not None:
        query.append(("paper.page", args.page))
    if args.pagesz is not None:
        query.append(("paper.pagesz", args.pagesz))
    if args.page_token:
        query.append(("pager.page_token", args.page_token))
    return urllib.parse.urlencode(query, doseq=True)


def handle_list(args: argparse.Namespace, dotenv: dict[str, str]) -> int:
    api_key = ensure_api_key(args, dotenv)
    base_url = resolve_base_url(args, dotenv)
    output_dir = mkdir(default_output_dir(args))
    query = build_list_query(args)
    url = f"{base_url}/ent/v2/tasks"
    if query:
        url = f"{url}?{query}"
    status_code, body = request_json("GET", url, api_key)
    if status_code >= 400:
        raise CliError(f"任务列表查询失败（HTTP {status_code}）：{json.dumps(sanitize(body, api_key), ensure_ascii=False)}")
    report = {
        "command": "list",
        "base_url": base_url,
        "query": urllib.parse.parse_qs(query),
        "response": body,
    }
    report_path = write_report(args, f"list-{utc_stamp()}", report, output_dir, api_key)
    print(json.dumps({"report_json": str(report_path)}, ensure_ascii=False))
    return 0


def handle_cancel(args: argparse.Namespace, dotenv: dict[str, str]) -> int:
    api_key = ensure_api_key(args, dotenv)
    base_url = resolve_base_url(args, dotenv)
    output_dir = mkdir(default_output_dir(args))
    url = f"{base_url}/ent/v2/tasks/{args.task_id}/cancel"
    status_code, body = request_json("POST", url, api_key, payload={})
    if status_code >= 400:
        raise CliError(f"取消任务失败（HTTP {status_code}）：{json.dumps(sanitize(body, api_key), ensure_ascii=False)}")
    report = {
        "command": "cancel",
        "task_id": args.task_id,
        "base_url": base_url,
        "response": body,
    }
    report_path = write_report(args, f"cancel-{args.task_id}", report, output_dir, api_key)
    print(json.dumps({"task_id": args.task_id, "report_json": str(report_path)}, ensure_ascii=False))
    return 0


def handle_credits(args: argparse.Namespace, dotenv: dict[str, str]) -> int:
    api_key = ensure_api_key(args, dotenv)
    base_url = resolve_base_url(args, dotenv)
    output_dir = mkdir(default_output_dir(args))
    query = urllib.parse.urlencode({"show_detail": str(bool(args.show_detail)).lower()})
    status_code, body = request_json("GET", f"{base_url}/ent/v2/credits?{query}", api_key)
    if status_code >= 400:
        raise CliError(f"积分查询失败（HTTP {status_code}）：{json.dumps(sanitize(body, api_key), ensure_ascii=False)}")
    report = {
        "command": "credits",
        "base_url": base_url,
        "query": {"show_detail": bool(args.show_detail)},
        "response": body,
    }
    report_path = write_report(args, f"credits-{utc_stamp()}", report, output_dir, api_key)
    print(json.dumps({"report_json": str(report_path)}, ensure_ascii=False))
    return 0


def parse_header_kv(items: list[str]) -> dict[str, str]:
    headers: dict[str, str] = {}
    for item in items:
        if "=" not in item:
            raise CliError(f"--header 需要使用 KEY=VALUE 格式：{item}")
        key, value = item.split("=", 1)
        headers[key] = value
    return headers


def compute_callback_signature(
    secret_key: str,
    http_method: str,
    callback_url: str,
    date_value: str,
    headers: dict[str, str],
    signed_headers: list[str],
) -> tuple[str, str]:
    parsed = urllib.parse.urlparse(callback_url)
    uri = parsed.path or "/"
    query = parsed.query or ""
    signing_string = f"{http_method.upper()}\n{uri}\n{query}\nvidu\n{date_value}\n"
    for header in signed_headers:
        if header not in headers:
            raise CliError(f"签名头缺失：{header}")
        signing_string += f"{header}:{headers[header]}\n"
    digest = hmac.new(secret_key.encode("utf-8"), signing_string.encode("utf-8"), hashlib.sha256).digest()
    signature = base64.b64encode(digest).decode("utf-8")
    return signing_string, signature


def handle_verify_callback(args: argparse.Namespace, dotenv: dict[str, str]) -> int:
    api_key = ensure_api_key(args, dotenv)
    output_dir = mkdir(default_output_dir(args))
    secret_key = args.secret_key or api_key
    headers = parse_header_kv(args.header)
    date_value = args.date or headers.get("Date")
    if not date_value:
        raise CliError("回调验签需要 `--date` 或 `--header 'Date=...'`。")
    signed_headers = args.signed_header[:]
    if not signed_headers and "X-HMAC-SIGNED-HEADERS" in headers:
        signed_headers = [item for item in headers["X-HMAC-SIGNED-HEADERS"].split(";") if item]
    if not signed_headers:
        raise CliError("回调验签需要 `--signed-header`，或在 header 中提供 `X-HMAC-SIGNED-HEADERS`。")

    signing_string, signature = compute_callback_signature(
        secret_key=secret_key,
        http_method=args.http_method,
        callback_url=args.callback_url,
        date_value=date_value,
        headers=headers,
        signed_headers=signed_headers,
    )
    matched = None
    if args.expected_signature:
        matched = signature == args.expected_signature
    report = {
        "command": "verify-callback",
        "callback_url": args.callback_url,
        "http_method": args.http_method.upper(),
        "signed_headers": signed_headers,
        "headers": headers,
        "signing_string": signing_string,
        "computed_signature": signature,
        "expected_signature": args.expected_signature,
        "matched": matched,
    }
    report_path = write_report(args, f"callback-signature-{utc_stamp()}", report, output_dir, api_key)
    print(json.dumps({"matched": matched, "report_json": str(report_path)}, ensure_ascii=False))
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Unified CLI for Vidu enterprise video APIs")
    parser.add_argument("--api-key")
    parser.add_argument("--base-url")

    subparsers = parser.add_subparsers(dest="command", required=True)

    create = subparsers.add_parser("create", help="Create a Vidu video task")
    create.add_argument("--mode", choices=sorted(CREATE_ENDPOINTS), required=True)
    create.add_argument("--input-json")
    create.add_argument("--subject-json-file", action="append", default=[])
    create.add_argument("--image-setting-json-file", action="append", default=[])
    create.add_argument("--model")
    create.add_argument("--style")
    create.add_argument("--prompt")
    create.add_argument("--duration", type=int)
    create.add_argument("--aspect-ratio")
    create.add_argument("--resolution")
    create.add_argument("--seed", type=int)
    create.add_argument("--payload")
    create.add_argument("--callback-url")
    create.add_argument("--voice-id")
    create.add_argument("--audio-type")
    create.add_argument("--server-id")
    create.add_argument("--movement-amplitude")
    create.add_argument("--wm-position", type=int)
    create.add_argument("--wm-url")
    create.add_argument("--meta-data")
    create.add_argument("--template-name")
    create.add_argument("--story-name")
    create.add_argument("--image", action="append", default=[])
    create.add_argument("--start-image")
    create.add_argument("--audio", action="store_true")
    create.add_argument("--auto-subjects", action="store_true")
    create.add_argument("--off-peak", action="store_true")
    create.add_argument("--watermark", action="store_true")
    create.add_argument("--project-name")
    create.add_argument("--task-kind", choices=("project", "test", "temp"), default="project")
    create.add_argument("--output-dir")
    create.add_argument("--report-json")
    create.add_argument("--wait", action="store_true")
    create.add_argument("--poll-interval", type=int, default=10)
    create.add_argument("--wait-timeout", type=int, default=600)
    create.add_argument("--download-on-complete", action="store_true")
    create.add_argument("--download-watermarked", action="store_true")
    create.add_argument("--creation-index", type=int, default=0)
    create.add_argument("--output")
    create.add_argument("--print-request", action="store_true")
    create.add_argument("--dry-run", action="store_true")

    task = subparsers.add_parser("task", help="Query one Vidu task")
    task.add_argument("--task-id", required=True)
    task.add_argument("--project-name")
    task.add_argument("--task-kind", choices=("project", "test", "temp"), default="project")
    task.add_argument("--output-dir")
    task.add_argument("--report-json")
    task.add_argument("--wait", action="store_true")
    task.add_argument("--poll-interval", type=int, default=10)
    task.add_argument("--wait-timeout", type=int, default=600)
    task.add_argument("--download-on-complete", action="store_true")
    task.add_argument("--download-watermarked", action="store_true")
    task.add_argument("--creation-index", type=int, default=0)
    task.add_argument("--output")

    list_parser = subparsers.add_parser("list", help="List Vidu tasks")
    list_parser.add_argument("--created-from")
    list_parser.add_argument("--created-to")
    list_parser.add_argument("--task-id-filter", action="append", default=[])
    list_parser.add_argument("--template-filter", action="append", default=[])
    list_parser.add_argument("--model-version", action="append", default=[])
    list_parser.add_argument("--resolution-filter", action="append", default=[])
    list_parser.add_argument("--state", action="append", default=[])
    list_parser.add_argument("--page", type=int)
    list_parser.add_argument("--pagesz", type=int)
    list_parser.add_argument("--page-token")
    list_parser.add_argument("--project-name")
    list_parser.add_argument("--task-kind", choices=("project", "test", "temp"), default="project")
    list_parser.add_argument("--output-dir")
    list_parser.add_argument("--report-json")

    cancel = subparsers.add_parser("cancel", help="Cancel one Vidu task")
    cancel.add_argument("--task-id", required=True)
    cancel.add_argument("--project-name")
    cancel.add_argument("--task-kind", choices=("project", "test", "temp"), default="project")
    cancel.add_argument("--output-dir")
    cancel.add_argument("--report-json")

    credits = subparsers.add_parser("credits", help="Query Vidu credits")
    credits.add_argument("--show-detail", action="store_true")
    credits.add_argument("--project-name")
    credits.add_argument("--task-kind", choices=("project", "test", "temp"), default="project")
    credits.add_argument("--output-dir")
    credits.add_argument("--report-json")

    callback = subparsers.add_parser("verify-callback", help="Generate or verify Vidu callback signature")
    callback.add_argument("--callback-url", required=True)
    callback.add_argument("--http-method", default="POST")
    callback.add_argument("--date")
    callback.add_argument("--header", action="append", default=[])
    callback.add_argument("--signed-header", action="append", default=[])
    callback.add_argument("--secret-key")
    callback.add_argument("--expected-signature")
    callback.add_argument("--project-name")
    callback.add_argument("--task-kind", choices=("project", "test", "temp"), default="project")
    callback.add_argument("--output-dir")
    callback.add_argument("--report-json")

    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    dotenv = load_dotenv(REPO_ROOT / ".env")
    handlers = {
        "create": handle_create,
        "task": handle_task,
        "list": handle_list,
        "cancel": handle_cancel,
        "credits": handle_credits,
        "verify-callback": handle_verify_callback,
    }
    try:
        return handlers[args.command](args, dotenv)
    except CliError as exc:
        print(str(exc), file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
