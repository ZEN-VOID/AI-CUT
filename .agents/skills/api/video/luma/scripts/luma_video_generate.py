#!/usr/bin/env python3
"""
FineAPI-compatible Luma video generation CLI.

Supports:
- submit: create a generation via POST /luma/generations
- status: query a generation object via configurable path template
- download: fetch generation status and download the resolved video URL
- run: submit + poll + download in one flow
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


DEFAULT_RESOLUTION = "720p"
DEFAULT_DURATION = "5s"
DEFAULT_PROJECT_NAME = "测试"
DEFAULT_TIMEOUT = 180
DEFAULT_POLL_INTERVAL = 10
DEFAULT_MAX_WAIT_SECONDS = 900
DEFAULT_STATUS_PATH_TEMPLATE = "/luma/generations/{id}"
ALLOWED_RESOLUTIONS = {"720p", "1080p"}
ALLOWED_DURATIONS = {"5s"}
TERMINAL_SUCCESS_STATES = {"completed", "succeeded", "success"}
TERMINAL_FAILURE_STATES = {"failed", "error", "canceled", "cancelled"}
KNOWN_MODELS = {
    "ray-v1",
    "ray-v2",
    "ray-1.6",
    "ray1.6",
    "ray-2",
    "ray2",
}
MODEL_ALIAS_MAP = {
    "ray-2": ["ray-v2", "ray2"],
    "ray-v1": ["ray-1.6", "ray1.6"],
    "ray-v2": ["ray-2", "ray2"],
    "ray-1.6": ["ray-v1"],
}


def _now_stamp() -> str:
    return datetime.now().strftime("%Y%m%d_%H%M%S")


def _safe_name(text: str, max_len: int = 64) -> str:
    normalized = re.sub(r"\s+", "_", text.strip())
    normalized = re.sub(r"[^0-9A-Za-z_\u4e00-\u9fff-]+", "", normalized)
    return (normalized or "luma_video")[:max_len]


def _version_key_from_model(model: str) -> tuple[int, ...]:
    match = re.search(r"(\d+(?:\.\d+)*)", model)
    if not match:
        return (0,)
    return tuple(int(part) for part in match.group(1).split("."))


def _select_latest_known_model() -> str:
    latest_version = max((_version_key_from_model(model) for model in KNOWN_MODELS), default=(0,))
    same_version = [model for model in KNOWN_MODELS if _version_key_from_model(model) == latest_version]
    for preferred in ("ray-2", "ray-v2", "ray2"):
        if preferred in same_version:
            return preferred
    return sorted(same_version)[0]


DEFAULT_MODEL = _select_latest_known_model()


def _env_api_key() -> Optional[str]:
    return (
        os.getenv("LUMA_API_KEY")
        or os.getenv("FINEAPI_API_KEY")
        or os.getenv("ANYFAST_VIDEO_API_KEY")
        or os.getenv("ANYFAST_API_KEY")
    )


def _env_base_url() -> Optional[str]:
    return os.getenv("LUMA_API_BASE_URL") or os.getenv("FINEAPI_API_BASE_URL")


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
    return Path("output") / "影片" / project / "5-API" / "video" / "luma"


def _write_json(path: Path, data: Dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def _make_report_path(output_dir: Path, prefix: str, command: str, explicit: Optional[str]) -> Path:
    if explicit:
        return Path(explicit)
    stem = _safe_name(prefix or "luma")
    return output_dir / f"{stem}_{command}_report_{_now_stamp()}.json"


def _build_model_candidates(model: str, allow_alias_fallback: bool) -> List[str]:
    candidates = [model]
    if allow_alias_fallback:
        candidates.extend(MODEL_ALIAS_MAP.get(model, []))
    deduped: List[str] = []
    for item in candidates:
        if item not in deduped:
            deduped.append(item)
    return deduped


def _collect_text_leaves(value: Any) -> List[str]:
    texts: List[str] = []
    if isinstance(value, str):
        stripped = value.strip()
        if stripped:
            texts.append(stripped)
    elif isinstance(value, dict):
        for nested in value.values():
            texts.extend(_collect_text_leaves(nested))
    elif isinstance(value, list):
        for nested in value:
            texts.extend(_collect_text_leaves(nested))
    return texts


def _build_attempt_diagnostic(errors: List[Dict[str, Any]], resolution: str) -> Optional[str]:
    messages: List[str] = []
    if resolution == "1080p":
        messages.append("当前默认仍优先信任 720p；若 1080p 失败，请先回退到 720p 验证。")
    merged_text: List[str] = []
    for item in errors:
        body = item.get("body")
        merged_text.extend(_collect_text_leaves(body))
    merged = " | ".join(merged_text)
    merged_lower = merged.lower()
    html_shell = "<!doctype html>" in merged_lower or "response_validation_error" in merged_lower or "前端 html" in merged
    if html_shell:
        messages.append("当前更像 API 路由未开或 Base URL 错位；网关返回了前端 HTML，而不是 generation JSON。")
    else:
        if "quota" in merged_lower or "余额" in merged or "额度已用尽" in merged:
            messages.append("当前更像配额或余额问题；优先检查当前 Bearer Token 对应账户余额。")
        if "unauthorized" in merged_lower or "authorization failed" in merged_lower or "invalid token" in merged_lower:
            messages.append("当前更像鉴权问题；优先检查 .env 中的 LUMA/FINEAPI/ANYFAST token。")
        if "model" in merged_lower and ("not found" in merged_lower or "invalid" in merged_lower):
            messages.append(f"当前更像模型名漂移；可尝试 `{DEFAULT_MODEL}` 与其等价别名之间切换。")
    if not messages:
        return None
    return " ".join(messages)


def _normalize_state(value: Any) -> str:
    if not isinstance(value, str):
        return ""
    return value.strip().lower()


def _session_headers(api_key: str) -> Dict[str, str]:
    return {
        "Authorization": _normalize_auth_header(api_key),
        "Accept": "application/json",
        "Content-Type": "application/json",
    }


def _request_summary(method: str, url: str, headers: Dict[str, str], data: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
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


def _normalize_submit_response(body: Dict[str, Any], attempted_models: List[str]) -> Dict[str, Any]:
    return {
        "id": body.get("id"),
        "prompt": body.get("prompt"),
        "state": body.get("state"),
        "queue_state": body.get("queue_state"),
        "created_at": body.get("created_at"),
        "batch_id": body.get("batch_id"),
        "video": body.get("video"),
        "video_raw": body.get("video_raw"),
        "thumbnail": body.get("thumbnail"),
        "last_frame": body.get("last_frame"),
        "estimate_wait_seconds": body.get("estimate_wait_seconds"),
        "attempted_models": attempted_models,
    }


def _normalize_status_response(body: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "id": body.get("id"),
        "prompt": body.get("prompt"),
        "state": body.get("state"),
        "queue_state": body.get("queue_state"),
        "created_at": body.get("created_at"),
        "batch_id": body.get("batch_id"),
        "video": body.get("video"),
        "video_raw": body.get("video_raw"),
        "thumbnail": body.get("thumbnail"),
        "last_frame": body.get("last_frame"),
        "estimate_wait_seconds": body.get("estimate_wait_seconds"),
        "failure_reason": body.get("failure_reason"),
        "assets": body.get("assets"),
    }


def _looks_like_generation_payload(body: Dict[str, Any]) -> bool:
    expected_keys = {
        "id",
        "state",
        "queue_state",
        "created_at",
        "video",
        "video_raw",
        "thumbnail",
        "last_frame",
        "assets",
    }
    return any(key in body for key in expected_keys)


def _extract_video_url(body: Dict[str, Any]) -> Optional[str]:
    for key in ("video", "video_raw"):
        value = body.get(key)
        if isinstance(value, str) and value.strip():
            return value.strip()
        if isinstance(value, dict):
            for nested in ("url", "src", "video_url"):
                nested_value = value.get(nested)
                if isinstance(nested_value, str) and nested_value.strip():
                    return nested_value.strip()
    assets = body.get("assets")
    if isinstance(assets, dict):
        video_asset = assets.get("video")
        if isinstance(video_asset, str) and video_asset.strip():
            return video_asset.strip()
        if isinstance(video_asset, dict):
            for nested in ("url", "src", "video_url"):
                nested_value = video_asset.get(nested)
                if isinstance(nested_value, str) and nested_value.strip():
                    return nested_value.strip()
    return None


def _build_create_payload(
    *,
    prompt: str,
    model_name: str,
    resolution: str,
    duration: str,
    expand_prompt: Optional[bool],
    loop: Optional[bool],
    image_url: Optional[str],
    image_end_url: Optional[str],
    notify_hook: Optional[str],
) -> Dict[str, Any]:
    payload: Dict[str, Any] = {
        "user_prompt": prompt,
        "model_name": model_name,
        "resolution": resolution,
        "duration": duration,
    }
    if expand_prompt is not None:
        payload["expand_prompt"] = expand_prompt
    if loop is not None:
        payload["loop"] = loop
    if image_url:
        payload["image_url"] = image_url
    if image_end_url:
        payload["image_end_url"] = image_end_url
    if notify_hook:
        payload["notify_hook"] = notify_hook
    return payload


def submit_generation(
    *,
    prompt: str,
    model: str,
    resolution: str,
    duration: str,
    expand_prompt: Optional[bool],
    loop: Optional[bool],
    image_url: Optional[str],
    image_end_url: Optional[str],
    notify_hook: Optional[str],
    api_key: str,
    base_url: str,
    timeout: int,
    dry_run: bool,
    print_payload: bool,
    allow_alias_fallback: bool,
) -> Dict[str, Any]:
    if not prompt.strip():
        raise ValueError("prompt 不能为空")
    if resolution not in ALLOWED_RESOLUTIONS:
        raise ValueError(f"resolution 不合法: {resolution}")
    if duration not in ALLOWED_DURATIONS:
        raise ValueError(f"duration 不合法: {duration}；当前只支持 5s")
    if image_url and not _is_remote_url(image_url):
        raise ValueError("image_url 仅接受公网 http/https URL")
    if image_end_url and not _is_remote_url(image_end_url):
        raise ValueError("image_end_url 仅接受公网 http/https URL")
    if notify_hook and not _is_remote_url(notify_hook):
        raise ValueError("notify_hook 仅接受公网 http/https URL")

    headers = _session_headers(api_key)
    url = f"{base_url.rstrip('/')}/luma/generations"
    model_candidates = _build_model_candidates(model, allow_alias_fallback)
    request_payload = _build_create_payload(
        prompt=prompt,
        model_name=model_candidates[0],
        resolution=resolution,
        duration=duration,
        expand_prompt=expand_prompt,
        loop=loop,
        image_url=image_url,
        image_end_url=image_end_url,
        notify_hook=notify_hook,
    )
    request_summary = _request_summary(
        "POST",
        url,
        headers,
        {
            **request_payload,
            "model_candidates": model_candidates,
        },
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
        payload = _build_create_payload(
            prompt=prompt,
            model_name=candidate_model,
            resolution=resolution,
            duration=duration,
            expand_prompt=expand_prompt,
            loop=loop,
            image_url=image_url,
            image_end_url=image_end_url,
            notify_hook=notify_hook,
        )
        response = requests.post(url, headers=headers, json=payload, timeout=timeout)
        try:
            body = response.json()
        except ValueError:
            body = {"non_json_response": response.text}
        if response.ok and _looks_like_generation_payload(body):
            return {
                "ok": True,
                "request_summary": request_summary,
                "normalized_submit": _normalize_submit_response(body, model_candidates),
                "raw_response": body,
                "attempted_models": model_candidates,
            }
        if response.ok:
            body = {
                **body,
                "response_validation_error": "HTTP 200 但返回体不是 generation JSON；疑似路由未开、Base URL 错位或网关返回前端 HTML。",
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
        "diagnostic_hint": _build_attempt_diagnostic(errors, resolution),
    }


def query_generation(
    *,
    generation_id: str,
    api_key: str,
    base_url: str,
    timeout: int,
    status_path_template: str,
) -> Dict[str, Any]:
    if "{id}" not in status_path_template:
        raise ValueError("status_path_template 必须包含 {id}")
    headers = _session_headers(api_key)
    relative = status_path_template.format(id=generation_id)
    url = f"{base_url.rstrip('/')}/{relative.lstrip('/')}"
    response = requests.get(url, headers=headers, timeout=timeout)
    try:
        body = response.json()
    except ValueError:
        body = {"non_json_response": response.text}

    diagnostic_hint = None
    if not response.ok and response.status_code in {404, 405}:
        diagnostic_hint = (
            "当前更像查询路径未被该网关镜像；创建接口已确认，但需显式覆盖 --status-path-template "
            "或先停在 submit receipt。"
        )
    elif response.ok and not _looks_like_generation_payload(body):
        diagnostic_hint = "HTTP 200 但返回体不是 generation JSON；疑似查询路由未开、Base URL 错位或网关返回前端 HTML。"

    return {
        "ok": response.ok and _looks_like_generation_payload(body),
        "request_summary": _request_summary("GET", url, headers),
        "normalized_status": _normalize_status_response(body) if response.ok and _looks_like_generation_payload(body) else None,
        "raw_response": body,
        "status_code": response.status_code,
        "error": None if response.ok and _looks_like_generation_payload(body) else "查询任务失败",
        "diagnostic_hint": diagnostic_hint,
    }


def poll_until_terminal(
    *,
    generation_id: str,
    api_key: str,
    base_url: str,
    timeout: int,
    poll_interval: int,
    max_wait_seconds: int,
    status_path_template: str,
    emit_progress: bool = False,
) -> Dict[str, Any]:
    started = time.time()
    history: List[Dict[str, Any]] = []
    while True:
        status_result = query_generation(
            generation_id=generation_id,
            api_key=api_key,
            base_url=base_url,
            timeout=timeout,
            status_path_template=status_path_template,
        )
        history.append(status_result.get("normalized_status") or status_result.get("raw_response"))
        if not status_result["ok"]:
            status_result["history"] = history
            return status_result

        normalized = status_result["normalized_status"] or {}
        state = _normalize_state(normalized.get("state"))
        if emit_progress:
            elapsed = int(time.time() - started)
            print(
                f"[luma] generation={generation_id} state={state or 'unknown'} elapsed={elapsed}s",
                file=sys.stderr,
                flush=True,
            )
        if state in TERMINAL_SUCCESS_STATES:
            status_result["history"] = history
            return status_result
        if state in TERMINAL_FAILURE_STATES:
            status_result["history"] = history
            status_result["ok"] = False
            status_result["error"] = normalized.get("failure_reason") or "任务状态为失败"
            return status_result
        if time.time() - started >= max_wait_seconds:
            status_result["history"] = history
            status_result["ok"] = False
            status_result["error"] = f"轮询超时，已等待 {max_wait_seconds} 秒"
            return status_result
        time.sleep(poll_interval)


def download_generation_video(
    *,
    generation_id: str,
    api_key: str,
    base_url: str,
    timeout: int,
    output_dir: Path,
    filename_prefix: str,
    status_path_template: str,
    save_video: bool,
) -> Dict[str, Any]:
    status_result = query_generation(
        generation_id=generation_id,
        api_key=api_key,
        base_url=base_url,
        timeout=timeout,
        status_path_template=status_path_template,
    )
    result: Dict[str, Any] = {
        "ok": status_result.get("ok", False),
        "request_summary": status_result.get("request_summary"),
        "normalized_download": None,
        "raw_response": status_result.get("raw_response"),
        "saved_file": None,
        "error": status_result.get("error"),
        "diagnostic_hint": status_result.get("diagnostic_hint"),
    }
    if not status_result.get("ok"):
        return result

    body = status_result.get("raw_response") or {}
    if not isinstance(body, dict):
        result["ok"] = False
        result["error"] = "查询返回不是 JSON object，无法抽取视频地址"
        return result

    video_url = _extract_video_url(body)
    result["normalized_download"] = {
        "id": body.get("id"),
        "state": body.get("state"),
        "video_url": video_url,
        "thumbnail": body.get("thumbnail"),
        "last_frame": body.get("last_frame"),
    }
    if not video_url:
        result["ok"] = False
        result["error"] = "generation 对象中未找到可下载视频地址"
        return result
    if not save_video:
        return result

    output_dir.mkdir(parents=True, exist_ok=True)
    target = output_dir / f"{_safe_name(filename_prefix or 'luma')}_{generation_id}.mp4"
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
    common_parser.add_argument("--filename-prefix", default="luma", help="报告/视频文件名前缀")
    common_parser.add_argument("--report-json", help="显式指定报告 JSON 路径")
    common_parser.add_argument(
        "--status-path-template",
        default=DEFAULT_STATUS_PATH_TEMPLATE,
        help="查询路径模板，必须包含 {id}",
    )

    parser = argparse.ArgumentParser(
        description="Submit and manage FineAPI-compatible Luma generation tasks",
        parents=[common_parser],
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    submit_parser = subparsers.add_parser("submit", help="创建视频任务", parents=[common_parser])
    submit_parser.add_argument("--prompt", required=True, help="视频提示词")
    submit_parser.add_argument(
        "--model",
        default=DEFAULT_MODEL,
        help=f"模型 ID；默认自动选择当前已登记 Ray 系列最高版本（当前为 {DEFAULT_MODEL}）",
    )
    submit_parser.add_argument(
        "--resolution",
        default=DEFAULT_RESOLUTION,
        choices=sorted(ALLOWED_RESOLUTIONS),
        help="输出分辨率",
    )
    submit_parser.add_argument(
        "--duration",
        default=DEFAULT_DURATION,
        choices=sorted(ALLOWED_DURATIONS),
        help="当前只支持 5s",
    )
    submit_parser.add_argument("--expand-prompt", action=argparse.BooleanOptionalAction, default=None, help="提示词扩写开关")
    submit_parser.add_argument("--loop", action=argparse.BooleanOptionalAction, default=None, help="循环视频开关")
    submit_parser.add_argument("--image-url", help="起始关键帧图片 URL")
    submit_parser.add_argument("--image-end-url", help="结束关键帧图片 URL")
    submit_parser.add_argument("--notify-hook", help="处理完成后的 webhook URL")
    submit_parser.add_argument("--dry-run", action="store_true", help="仅打印请求摘要，不实际提交")
    submit_parser.add_argument("--print-payload", action="store_true", help="打印最终请求摘要")
    submit_parser.add_argument("--no-model-alias-fallback", action="store_true", help="禁用 ray-* 模型别名回退")

    status_parser = subparsers.add_parser("status", help="查询任务状态", parents=[common_parser])
    status_parser.add_argument("--generation-id", required=True, help="generation ID")

    download_parser = subparsers.add_parser("download", help="下载视频结果", parents=[common_parser])
    download_parser.add_argument("--generation-id", required=True, help="generation ID")
    download_parser.add_argument("--no-save-video", action="store_true", help="只查询视频地址，不下载 MP4")

    run_parser = subparsers.add_parser("run", help="创建 + 轮询 + 下载", parents=[common_parser])
    run_parser.add_argument("--prompt", required=True, help="视频提示词")
    run_parser.add_argument(
        "--model",
        default=DEFAULT_MODEL,
        help=f"模型 ID；默认自动选择当前已登记 Ray 系列最高版本（当前为 {DEFAULT_MODEL}）",
    )
    run_parser.add_argument(
        "--resolution",
        default=DEFAULT_RESOLUTION,
        choices=sorted(ALLOWED_RESOLUTIONS),
        help="输出分辨率",
    )
    run_parser.add_argument(
        "--duration",
        default=DEFAULT_DURATION,
        choices=sorted(ALLOWED_DURATIONS),
        help="当前只支持 5s",
    )
    run_parser.add_argument("--expand-prompt", action=argparse.BooleanOptionalAction, default=None, help="提示词扩写开关")
    run_parser.add_argument("--loop", action=argparse.BooleanOptionalAction, default=None, help="循环视频开关")
    run_parser.add_argument("--image-url", help="起始关键帧图片 URL")
    run_parser.add_argument("--image-end-url", help="结束关键帧图片 URL")
    run_parser.add_argument("--notify-hook", help="处理完成后的 webhook URL")
    run_parser.add_argument("--poll-interval", type=int, default=DEFAULT_POLL_INTERVAL, help="轮询间隔秒数")
    run_parser.add_argument("--max-wait-seconds", type=int, default=DEFAULT_MAX_WAIT_SECONDS, help="最大等待秒数")
    run_parser.add_argument("--dry-run", action="store_true", help="仅打印请求摘要，不实际提交")
    run_parser.add_argument("--print-payload", action="store_true", help="打印最终请求摘要")
    run_parser.add_argument("--no-model-alias-fallback", action="store_true", help="禁用 ray-* 模型别名回退")
    run_parser.add_argument("--no-save-video", action="store_true", help="只保留 video_url，不下载 MP4")

    return parser


def _resolve_api_key(explicit: Optional[str]) -> str:
    value = explicit or _env_api_key()
    if not value:
        raise ValueError(
            "缺少 API Key，请在 .env 中配置 LUMA_API_KEY / FINEAPI_API_KEY / ANYFAST_VIDEO_API_KEY / ANYFAST_API_KEY"
        )
    return value


def _resolve_base_url(explicit: Optional[str]) -> str:
    value = explicit or _env_base_url()
    if not value:
        generic_anyfast = os.getenv("ANYFAST_API_BASE_URL")
        if generic_anyfast:
            raise ValueError(
                "缺少 Luma 专用 Base URL。当前仅检测到 ANYFAST_API_BASE_URL，但真实探测表明该通用网关对 "
                "/luma/generations 会返回前端 HTML；请显式配置 LUMA_API_BASE_URL / FINEAPI_API_BASE_URL 或传 --base-url"
            )
        raise ValueError(
            "缺少 API Base URL，请在 .env 中配置 LUMA_API_BASE_URL / FINEAPI_API_BASE_URL 或显式传 --base-url"
        )
    return value


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()

    try:
        api_key = _resolve_api_key(args.api_key)
        base_url = _resolve_base_url(args.base_url)
        output_dir = Path(args.output_dir) if args.output_dir else _default_output_dir(args.project_name)

        if args.command == "submit":
            result = submit_generation(
                prompt=args.prompt,
                model=args.model,
                resolution=args.resolution,
                duration=args.duration,
                expand_prompt=args.expand_prompt,
                loop=args.loop,
                image_url=args.image_url,
                image_end_url=args.image_end_url,
                notify_hook=args.notify_hook,
                api_key=api_key,
                base_url=base_url,
                timeout=args.timeout,
                dry_run=args.dry_run,
                print_payload=args.print_payload,
                allow_alias_fallback=not args.no_model_alias_fallback,
            )

        elif args.command == "status":
            result = query_generation(
                generation_id=args.generation_id,
                api_key=api_key,
                base_url=base_url,
                timeout=args.timeout,
                status_path_template=args.status_path_template,
            )

        elif args.command == "download":
            result = download_generation_video(
                generation_id=args.generation_id,
                api_key=api_key,
                base_url=base_url,
                timeout=args.timeout,
                output_dir=output_dir,
                filename_prefix=args.filename_prefix,
                status_path_template=args.status_path_template,
                save_video=not args.no_save_video,
            )

        elif args.command == "run":
            submit_result = submit_generation(
                prompt=args.prompt,
                model=args.model,
                resolution=args.resolution,
                duration=args.duration,
                expand_prompt=args.expand_prompt,
                loop=args.loop,
                image_url=args.image_url,
                image_end_url=args.image_end_url,
                notify_hook=args.notify_hook,
                api_key=api_key,
                base_url=base_url,
                timeout=args.timeout,
                dry_run=args.dry_run,
                print_payload=args.print_payload,
                allow_alias_fallback=not args.no_model_alias_fallback,
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
                generation_id = submit_result["normalized_submit"]["id"]
                print(
                    f"[luma] submitted generation={generation_id} model={submit_result['normalized_submit'].get('attempted_models', [args.model])[0]}",
                    file=sys.stderr,
                    flush=True,
                )
                status_result = poll_until_terminal(
                    generation_id=generation_id,
                    api_key=api_key,
                    base_url=base_url,
                    timeout=args.timeout,
                    poll_interval=args.poll_interval,
                    max_wait_seconds=args.max_wait_seconds,
                    status_path_template=args.status_path_template,
                    emit_progress=True,
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
                    download_result = download_generation_video(
                        generation_id=generation_id,
                        api_key=api_key,
                        base_url=base_url,
                        timeout=args.timeout,
                        output_dir=output_dir,
                        filename_prefix=args.filename_prefix,
                        status_path_template=args.status_path_template,
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
            getattr(args, "filename_prefix", "luma"),
            getattr(args, "command", "error"),
            getattr(args, "report_json", None),
        )
        _write_json(report_path, error_result)
        error_result["report_json"] = str(report_path)
        print(json.dumps(error_result, ensure_ascii=False, indent=2))
        return 1


if __name__ == "__main__":
    sys.exit(main())
