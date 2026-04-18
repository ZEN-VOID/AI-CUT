#!/usr/bin/env python3
"""
FineAPI Runway image-to-video CLI.

Supports:
- submit: create a new task
- status: query a task via the Runway task model
- download: download the completed video
- run: submit + poll + download
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
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional
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

VIDEO_SKILL_ROOT = Path(__file__).resolve().parents[2]
if str(VIDEO_SKILL_ROOT) not in sys.path:
    sys.path.insert(0, str(VIDEO_SKILL_ROOT))

from shared.default_model_policy import select_highest_model


DEFAULT_DURATION = 5
DEFAULT_PROJECT_NAME = "测试"
DEFAULT_TIMEOUT = 180
DEFAULT_POLL_INTERVAL = 5
DEFAULT_MAX_WAIT_SECONDS = 900
SUBMIT_PATH = "/runwayml/v1/image_to_video"
TASK_PATH_TEMPLATE = "/runwayml/v1/tasks/{task_id}"
ALLOWED_DURATIONS = {5, 10}
KNOWN_MODELS = {
    "gen4_turbo",
    "gen3a_turbo",
    "gen4.5",
    "veo3.1",
    "veo3.1_fast",
    "veo3",
}
KNOWN_RATIOS = {
    "1280:768",
    "768:1280",
    "1280:720",
    "1584:672",
    "1104:832",
    "720:1280",
    "832:1104",
    "672:1584",
    "960:960",
    "848:480",
    "480:848",
}
OFFICIAL_RATIO_HINTS = {
    "gen3a_turbo": {"1280:768", "768:1280"},
    "gen4_turbo": {"1280:720", "1584:672", "1104:832", "720:1280", "832:1104", "960:960"},
    "gen4.5": {"1280:720", "1584:672", "1104:832", "720:1280", "832:1104", "672:1584", "960:960"},
}
DEFAULT_RATIO_BY_MODEL = {
    "gen3a_turbo": "1280:768",
    "gen4_turbo": "1280:720",
    "gen4.5": "1280:720",
}
SUCCESS_STATES = {"SUCCEEDED", "succeeded", "completed", "COMPLETED", "success", "SUCCESS"}
FAIL_STATES = {
    "FAILED",
    "failed",
    "CANCELED",
    "canceled",
    "cancelled",
    "ABORTED",
    "aborted",
    "error",
    "ERROR",
}
RUNNING_STATES = {
    "PENDING",
    "pending",
    "RUNNING",
    "running",
    "THROTTLED",
    "throttled",
    "queued",
    "processing",
    "in_progress",
    "IN_PROGRESS",
}


def _model_sort_key(model: str) -> tuple[int, int, int, int, str]:
    """Pick the highest known model version, preferring non-fast variants at the same version."""
    match = re.fullmatch(
        r"(?P<family>[A-Za-z]+)(?P<major>\d+)(?:\.(?P<minor>\d+))?(?:[_-](?P<variant>[A-Za-z0-9._-]+))?",
        model,
    )
    if not match:
        return (-1, -1, -1, -1, model)

    family = (match.group("family") or "").lower()
    family_rank = {
        "gen": 3,
        "veo": 2,
        "act": 1,
    }.get(family, 0)
    major = int(match.group("major") or 0)
    minor = int(match.group("minor") or 0)
    variant = (match.group("variant") or "").lower()
    variant_rank = {
        "": 3,
        "turbo": 2,
        "fast": 1,
    }.get(variant, 0)
    return (family_rank, major, minor, variant_rank, model)


def _default_ratio_for_model(model: str) -> str:
    return DEFAULT_RATIO_BY_MODEL.get(model, "1280:720")


DEFAULT_MODEL = select_highest_model(KNOWN_MODELS, sort_key=_model_sort_key)
DEFAULT_RATIO = _default_ratio_for_model(DEFAULT_MODEL)


def _now_stamp() -> str:
    return datetime.now().strftime("%Y%m%d_%H%M%S")


def _safe_name(text: str, max_len: int = 64) -> str:
    normalized = re.sub(r"\s+", "_", text.strip())
    normalized = re.sub(r"[^0-9A-Za-z_\u4e00-\u9fff-]+", "", normalized)
    return (normalized or "runway_video")[:max_len]


def _env_api_key() -> Optional[str]:
    return (
        os.getenv("ANYFAST_VIDEO_API_KEY")
        or os.getenv("RUNWAY_API_KEY")
        or os.getenv("ANYFAST_API_KEY")
        or os.getenv("FINEAPI_API_KEY")
    )


def _env_base_url() -> str:
    return os.getenv("RUNWAY_API_BASE_URL") or os.getenv("FINEAPI_API_BASE_URL") or ""


def _normalize_auth_header(api_key: str) -> str:
    token = api_key.strip()
    if token.lower().startswith("bearer "):
        return token
    return f"Bearer {token}"


def _redact_auth_header(value: str) -> str:
    if not value:
        return value
    return "Bearer ***"


def _resolve_base_url(explicit: Optional[str], *, allow_unverified: bool = False) -> str:
    value = explicit or _env_base_url()
    if value:
        return value.rstrip("/")

    generic_anyfast = os.getenv("ANYFAST_API_BASE_URL")
    if generic_anyfast:
        if allow_unverified:
            return generic_anyfast.rstrip("/")
        raise ValueError(
            "缺少 Runway 专用 Base URL。当前仅检测到 ANYFAST_API_BASE_URL，但 2026-04-17 真实探测表明该通用网关对 "
            "/runwayml/v1/image_to_video 会返回前端 HTML；请显式配置 RUNWAY_API_BASE_URL / FINEAPI_API_BASE_URL 或传 --base-url"
        )
    raise ValueError(
        "缺少 API Base URL，请在 .env 中配置 RUNWAY_API_BASE_URL / FINEAPI_API_BASE_URL 或显式传 --base-url"
    )


def _guess_mime_type(filename: str, fallback: str = "image/png") -> str:
    mime_type, _ = mimetypes.guess_type(filename)
    return mime_type or fallback


def _is_https_url(value: str) -> bool:
    parsed = urlparse(value)
    return parsed.scheme == "https" and bool(parsed.netloc)


def _is_data_url(value: str) -> bool:
    return value.startswith("data:image/")


def _local_file_to_data_uri(path_value: str) -> str:
    path = Path(path_value).expanduser()
    if not path.is_file():
        raise FileNotFoundError(f"本地图片不存在: {path_value}")
    mime_type = _guess_mime_type(path.name)
    encoded = base64.b64encode(path.read_bytes()).decode("ascii")
    return f"data:{mime_type};base64,{encoded}"


def _normalize_prompt_image(image_value: str) -> str:
    if _is_https_url(image_value):
        return image_value
    if _is_data_url(image_value):
        return image_value
    parsed = urlparse(image_value)
    if parsed.scheme and parsed.scheme != "https":
        raise ValueError("promptImage 仅接受 HTTPS URL、Data URI 或本地文件路径")
    return _local_file_to_data_uri(image_value)


def _default_output_dir(project_name: str) -> Path:
    project = project_name.strip() or DEFAULT_PROJECT_NAME
    return Path("output") / "影片" / project / "5-API" / "video" / "runway"


def _write_json(path: Path, data: Dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def _make_report_path(output_dir: Path, prefix: str, command: str, explicit: Optional[str]) -> Path:
    if explicit:
        return Path(explicit)
    stem = _safe_name(prefix or "runway")
    return output_dir / f"{stem}_{command}_report_{_now_stamp()}.json"


def _build_validation_notes(model: str, ratio: str) -> List[str]:
    notes: List[str] = []
    if model not in KNOWN_MODELS:
        notes.append(
            f"模型 `{model}` 不在当前已确认集合中；若代理网关拒绝，请先回退到当前默认最高版本 `{DEFAULT_MODEL}`。"
        )
    if ratio not in KNOWN_RATIOS:
        notes.append(f"ratio `{ratio}` 不在当前已知集合中；若代理网关拒绝，请按官方文档比例重试。")

    official = OFFICIAL_RATIO_HINTS.get(model)
    if official and ratio not in official:
        notes.append(
            f"模型 `{model}` 与 ratio `{ratio}` 组合和官方 Runway ratio 文档不一致；"
            "当前允许提交以兼容 FineAPI 示例，但若网关报错应先改用官方推荐比例。"
        )
    if model == "gen4_turbo" and ratio == "1280:768":
        notes.append(
            "FineAPI 用户示例使用 `gen4_turbo + 1280:768`，但官方 Runway ratio 文档把 `1280:768` 归到 `gen3a_turbo`；"
            "已保留兼容，不做本地硬拒。"
        )
    return notes


def _request_summary(
    *,
    method: str,
    url: str,
    headers: Dict[str, str],
    json_body: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    sanitized_headers = {
        key: (_redact_auth_header(value) if key.lower() == "authorization" else value)
        for key, value in headers.items()
    }
    return {
        "method": method,
        "url": url,
        "headers": sanitized_headers,
        "json": json_body,
    }


def _response_preview(text: str, limit: int = 240) -> str:
    compact = re.sub(r"\s+", " ", text).strip()
    return compact[:limit]


def _looks_like_html(text: str) -> bool:
    lowered = text.lower()
    return "<!doctype html" in lowered or "<html" in lowered


def _parse_json_response(response: requests.Response, *, stage: str) -> Dict[str, Any]:
    content_type = response.headers.get("Content-Type", "")
    text = response.text
    try:
        body = response.json()
    except Exception:
        body = None

    if isinstance(body, dict):
        return body

    diagnostic_hint = None
    if _looks_like_html(text):
        diagnostic_hint = (
            "响应是前端 HTML 页面，不是 Runway API JSON；优先检查 Base URL 是否误指向通用 AnyFast 控制台域名。"
        )

    raise RuntimeError(
        json.dumps(
            {
                "stage": stage,
                "status_code": response.status_code,
                "content_type": content_type,
                "body_preview": _response_preview(text),
                "diagnostic_hint": diagnostic_hint
                or "响应不是可解析的 JSON；优先检查 Base URL、网关路由与上游代理是否真的开放该 Runway 端点。",
            },
            ensure_ascii=False,
        )
    )
    return {
        "method": method,
        "url": url,
        "headers": sanitized_headers,
        "json": json_body,
    }


def _normalize_status_text(value: Any) -> Optional[str]:
    if value is None:
        return None
    return str(value)


def _coerce_string(value: Any) -> Optional[str]:
    if value is None:
        return None
    if isinstance(value, str):
        return value
    return str(value)


def _looks_like_video_url(value: str) -> bool:
    if not value.startswith("http"):
        return False
    lowered = value.lower()
    return ".mp4" in lowered or ".mov" in lowered or "_jwt=" in lowered or "video" in lowered


def _collect_urls(value: Any, out: List[str]) -> None:
    if isinstance(value, str):
        if _looks_like_video_url(value) and value not in out:
            out.append(value)
        return
    if isinstance(value, list):
        for item in value:
            _collect_urls(item, out)
        return
    if isinstance(value, dict):
        for key, item in value.items():
            if key in {"output", "video", "video_raw", "videoRaw", "video_url", "url", "task_result", "result"}:
                _collect_urls(item, out)


def _extract_output_urls(body: Dict[str, Any]) -> List[str]:
    urls: List[str] = []
    _collect_urls(body, urls)
    return urls


def _normalize_submit_response(body: Dict[str, Any], validation_notes: List[str]) -> Dict[str, Any]:
    output_urls = _extract_output_urls(body)
    return {
        "id": body.get("id"),
        "prompt": body.get("prompt"),
        "state": body.get("state") or body.get("status"),
        "queue_state": body.get("queue_state"),
        "created_at": body.get("created_at") or body.get("createdAt"),
        "batch_id": body.get("batch_id"),
        "video": body.get("video"),
        "video_raw": body.get("video_raw") or body.get("videoRaw"),
        "thumbnail": body.get("thumbnail"),
        "last_frame": body.get("last_frame") or body.get("lastFrame"),
        "estimate_wait_seconds": body.get("estimate_wait_seconds"),
        "output_urls": output_urls,
        "validation_notes": validation_notes,
    }


def _normalize_status_response(body: Dict[str, Any]) -> Dict[str, Any]:
    output_urls = _extract_output_urls(body)
    return {
        "id": body.get("id"),
        "status": body.get("status") or body.get("state"),
        "state": body.get("state") or body.get("status"),
        "created_at": body.get("created_at") or body.get("createdAt"),
        "updated_at": body.get("updated_at") or body.get("updatedAt"),
        "output_urls": output_urls,
        "video": body.get("video"),
        "video_raw": body.get("video_raw") or body.get("videoRaw"),
        "error": body.get("error") or body.get("message"),
    }


def _normalize_download_response(status_body: Dict[str, Any], saved_file: Optional[str]) -> Dict[str, Any]:
    output_urls = _extract_output_urls(status_body)
    return {
        "id": status_body.get("id"),
        "status": status_body.get("status") or status_body.get("state"),
        "output_urls": output_urls,
        "saved_file": saved_file,
    }


def _build_diagnostic_hint(status_code: int, body: Any) -> Optional[str]:
    text = json.dumps(body, ensure_ascii=False) if isinstance(body, (dict, list)) else str(body)
    lowered = text.lower()
    if status_code in {401, 403}:
        return "鉴权失败或账户额度不足；优先检查 `.env` 中的 ANYFAST_VIDEO_API_KEY 是否有效。"
    if status_code == 404:
        return "当前网关可能未暴露 `GET /runwayml/v1/tasks/{id}`，或任务 ID 不存在；先核对任务路径推导与任务 ID。"
    if "ratio" in lowered and ("invalid" in lowered or "unsupported" in lowered):
        return "ratio 可能被当前模型或代理网关拒绝；优先改用官方 Runway 文档推荐比例。"
    if "model" in lowered and ("invalid" in lowered or "unsupported" in lowered or "not found" in lowered):
        return f"模型可能未被当前代理网关开放；优先回退到当前默认最高版本 `{DEFAULT_MODEL}`。"
    if "promptimage" in lowered or "data uri" in lowered:
        return "promptImage 格式可能不合法；确认使用 HTTPS URL 或 `data:image/...`。"
    if "<!doctype html" in lowered or "<html" in lowered:
        return "网关返回了前端 HTML，而不是 API JSON；优先检查 Base URL 是否误指向 AnyFast 控制台前端域名。"
    return None


def _session_headers(api_key: str, include_content_type: bool = False) -> Dict[str, str]:
    headers = {
        "Accept": "application/json",
        "Authorization": _normalize_auth_header(api_key),
    }
    if include_content_type:
        headers["Content-Type"] = "application/json"
    return headers


def _require_api_key(api_key: Optional[str], *, allow_placeholder: bool = False) -> str:
    if api_key:
        return api_key
    if allow_placeholder:
        return "DUMMY_TOKEN_FOR_DRY_RUN"
    raise ValueError("缺少 API Key，请在 .env 中配置 ANYFAST_VIDEO_API_KEY / RUNWAY_API_KEY / ANYFAST_API_KEY")


def _ensure_parent(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)


def _save_stream(url: str, destination: Path, timeout: int) -> None:
    _ensure_parent(destination)
    with requests.get(url, stream=True, timeout=timeout) as response:
        response.raise_for_status()
        with destination.open("wb") as file_obj:
            for chunk in response.iter_content(chunk_size=1024 * 128):
                if chunk:
                    file_obj.write(chunk)


def _download_destination(output_dir: Path, prefix: str, task_id: str, url: str) -> Path:
    parsed = urlparse(url)
    ext = Path(parsed.path).suffix or ".mp4"
    filename = f"{_safe_name(prefix or 'runway')}_{_safe_name(task_id, max_len=48)}{ext}"
    return output_dir / filename


def submit_video(
    *,
    prompt: str,
    image: str,
    model: str,
    duration: int,
    ratio: str,
    watermark: Optional[bool],
    seed: Optional[int],
    api_key: str,
    base_url: str,
    timeout: int,
    dry_run: bool,
    print_payload: bool,
) -> Dict[str, Any]:
    normalized_image = _normalize_prompt_image(image)
    validation_notes = _build_validation_notes(model, ratio)
    payload: Dict[str, Any] = {
        "promptImage": normalized_image,
        "model": model,
        "promptText": prompt,
        "duration": duration,
        "ratio": ratio,
    }
    if watermark is not None:
        payload["watermark"] = watermark
    if seed is not None:
        payload["seed"] = seed

    url = base_url.rstrip("/") + SUBMIT_PATH
    headers = _session_headers(api_key, include_content_type=True)
    request_summary = _request_summary(method="POST", url=url, headers=headers, json_body=payload)

    if print_payload:
        print(json.dumps(request_summary, ensure_ascii=False, indent=2))

    if dry_run:
        body = {
            "id": "dry-run-task-id",
            "state": "pending",
            "created_at": datetime.now(timezone.utc).isoformat(),
            "video": None,
            "video_raw": None,
        }
        return {
            "ok": True,
            "request_summary": request_summary,
            "raw_response": body,
            "normalized_submit": _normalize_submit_response(body, validation_notes),
            "validation_notes": validation_notes,
            "diagnostic_hint": "dry-run 未发起真实请求；若要联网执行，请提供有效 API Key 与 Base URL。",
        }

    response = requests.post(url, headers=headers, json=payload, timeout=timeout)
    body = _parse_json_response(response, stage="submit")
    if response.status_code >= 400:
        raise RuntimeError(
            json.dumps(
                {
                    "status_code": response.status_code,
                    "body": body,
                    "diagnostic_hint": _build_diagnostic_hint(response.status_code, body),
                },
                ensure_ascii=False,
            )
        )
    normalized_submit = _normalize_submit_response(body, validation_notes)
    if not normalized_submit.get("id"):
        raise RuntimeError(
            json.dumps(
                {
                    "status_code": response.status_code,
                    "body": body,
                    "diagnostic_hint": "创建响应缺少 task id；不要把无 id 的 200 响应当成成功回执。优先检查网关是否返回了兼容外壳或非标准响应。",
                },
                ensure_ascii=False,
            )
        )
    return {
        "ok": True,
        "request_summary": request_summary,
        "raw_response": body,
        "normalized_submit": normalized_submit,
        "validation_notes": validation_notes,
        "diagnostic_hint": _build_diagnostic_hint(response.status_code, body),
    }


def get_status(
    *,
    task_id: str,
    api_key: str,
    base_url: str,
    timeout: int,
) -> Dict[str, Any]:
    url = base_url.rstrip("/") + TASK_PATH_TEMPLATE.format(task_id=task_id)
    headers = _session_headers(api_key, include_content_type=False)
    request_summary = _request_summary(method="GET", url=url, headers=headers, json_body=None)
    response = requests.get(url, headers=headers, timeout=timeout)
    body = _parse_json_response(response, stage="status")
    if response.status_code >= 400:
        raise RuntimeError(
            json.dumps(
                {
                    "status_code": response.status_code,
                    "body": body,
                    "diagnostic_hint": _build_diagnostic_hint(response.status_code, body),
                },
                ensure_ascii=False,
            )
        )
    normalized_status = _normalize_status_response(body)
    if not (normalized_status.get("id") or normalized_status.get("status") or normalized_status.get("state")):
        raise RuntimeError(
            json.dumps(
                {
                    "status_code": response.status_code,
                    "body": body,
                    "diagnostic_hint": "状态响应缺少任务关键信息；优先检查查询路径推导是否成立，或当前网关是否返回了兼容外壳。",
                },
                ensure_ascii=False,
            )
        )
    return {
        "ok": True,
        "request_summary": request_summary,
        "raw_response": body,
        "normalized_status": normalized_status,
        "diagnostic_hint": _build_diagnostic_hint(response.status_code, body),
    }


def _status_text_from_body(body: Dict[str, Any]) -> Optional[str]:
    return _normalize_status_text(body.get("status") or body.get("state"))


def _is_success_state(status: Optional[str]) -> bool:
    return status in SUCCESS_STATES


def _is_fail_state(status: Optional[str]) -> bool:
    return status in FAIL_STATES


def wait_for_task(
    *,
    task_id: str,
    api_key: str,
    base_url: str,
    timeout: int,
    poll_interval: int,
    max_wait_seconds: int,
) -> Dict[str, Any]:
    started = time.time()
    last_result: Optional[Dict[str, Any]] = None
    while True:
        result = get_status(task_id=task_id, api_key=api_key, base_url=base_url, timeout=timeout)
        last_result = result
        body = result["raw_response"]
        status = _status_text_from_body(body)
        if _is_success_state(status):
            return result
        if _is_fail_state(status):
            raise RuntimeError(
                json.dumps(
                    {
                        "status": status,
                        "body": body,
                        "diagnostic_hint": "任务已进入失败终态；请检查模型、ratio、图片输入与上游审核/额度状态。",
                    },
                    ensure_ascii=False,
                )
            )
        if time.time() - started > max_wait_seconds:
            raise TimeoutError(
                json.dumps(
                    {
                        "status": status,
                        "elapsed_seconds": int(time.time() - started),
                        "body": body,
                        "diagnostic_hint": "等待超时；官方 Runway 任务通常建议至少 5 秒间隔轮询。若状态一直 pending，请检查并发额度或代理路径。",
                    },
                    ensure_ascii=False,
                )
            )
        time.sleep(max(poll_interval, 1))


def download_video(
    *,
    task_id: str,
    api_key: str,
    base_url: str,
    output_dir: Path,
    filename_prefix: str,
    timeout: int,
) -> Dict[str, Any]:
    status_result = get_status(task_id=task_id, api_key=api_key, base_url=base_url, timeout=timeout)
    status_body = status_result["raw_response"]
    output_urls = _extract_output_urls(status_body)
    if not output_urls:
        raise RuntimeError(
            json.dumps(
                {
                    "body": status_body,
                    "diagnostic_hint": "未从任务详情中提取到视频 URL；请检查 `output[] / video / video_raw / video_url` 是否发生字段漂移。",
                },
                ensure_ascii=False,
            )
        )
    chosen_url = output_urls[0]
    destination = _download_destination(output_dir, filename_prefix, task_id, chosen_url)
    _save_stream(chosen_url, destination, timeout=timeout)
    return {
        "ok": True,
        "request_summary": status_result["request_summary"],
        "raw_response": status_body,
        "normalized_download": _normalize_download_response(status_body, str(destination)),
        "saved_file": str(destination),
        "diagnostic_hint": None,
    }


def _common_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument("--api-key")
    parser.add_argument("--base-url")
    parser.add_argument("--project-name", default=DEFAULT_PROJECT_NAME)
    parser.add_argument("--output-dir")
    parser.add_argument("--filename-prefix", default="runway")
    parser.add_argument("--report-json")
    parser.add_argument("--timeout", type=int, default=DEFAULT_TIMEOUT)
    return parser


def _submit_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument("--prompt", required=True)
    parser.add_argument("--image", required=True)
    parser.add_argument("--model", default=DEFAULT_MODEL)
    parser.add_argument("--duration", type=int, default=DEFAULT_DURATION)
    parser.add_argument("--ratio")
    parser.add_argument("--watermark", choices={"true", "false"})
    parser.add_argument("--seed", type=int)
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--print-payload", action="store_true")
    return parser


def _poll_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument("--poll-interval", type=int, default=DEFAULT_POLL_INTERVAL)
    parser.add_argument("--max-wait-seconds", type=int, default=DEFAULT_MAX_WAIT_SECONDS)
    return parser


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="FineAPI Runway image-to-video CLI")
    subparsers = parser.add_subparsers(dest="command", required=True)

    submit_parser = subparsers.add_parser(
        "submit",
        parents=[_common_parser(), _submit_parser()],
        help="创建 Runway 图生视频任务",
    )
    submit_parser.set_defaults(command="submit")

    status_parser = subparsers.add_parser(
        "status",
        parents=[_common_parser()],
        help="查询 Runway 任务状态",
    )
    status_parser.add_argument("--task-id", required=True)
    status_parser.set_defaults(command="status")

    download_parser = subparsers.add_parser(
        "download",
        parents=[_common_parser()],
        help="下载 Runway 成片",
    )
    download_parser.add_argument("--task-id", required=True)
    download_parser.set_defaults(command="download")

    run_parser = subparsers.add_parser(
        "run",
        parents=[_common_parser(), _submit_parser(), _poll_parser()],
        help="创建 + 轮询 + 下载",
    )
    run_parser.set_defaults(command="run")

    return parser


def _bool_from_arg(value: Optional[str]) -> Optional[bool]:
    if value is None:
        return None
    return value == "true"


def _report_base(args: argparse.Namespace, output_dir: Path) -> Dict[str, Any]:
    return {
        "command": args.command,
        "project_name": args.project_name,
        "output_dir": str(output_dir),
    }


def _output_dir_from_args(args: argparse.Namespace) -> Path:
    if args.output_dir:
        return Path(args.output_dir)
    return _default_output_dir(args.project_name)


def _write_report(args: argparse.Namespace, output_dir: Path, payload: Dict[str, Any]) -> Path:
    report_path = _make_report_path(output_dir, args.filename_prefix, args.command, args.report_json)
    _write_json(report_path, payload)
    return report_path


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    output_dir = _output_dir_from_args(args)
    api_key = None
    base_url = ""

    try:
        allow_unverified_base_url = bool(getattr(args, "dry_run", False))
        base_url = _resolve_base_url(args.base_url, allow_unverified=allow_unverified_base_url)
        if args.command == "submit":
            api_key = _require_api_key(args.api_key or _env_api_key(), allow_placeholder=args.dry_run)
            if args.duration not in ALLOWED_DURATIONS:
                raise ValueError(f"duration 仅支持 {sorted(ALLOWED_DURATIONS)}")
            ratio = args.ratio or _default_ratio_for_model(args.model)
            result = submit_video(
                prompt=args.prompt,
                image=args.image,
                model=args.model,
                duration=args.duration,
                ratio=ratio,
                watermark=_bool_from_arg(args.watermark),
                seed=args.seed,
                api_key=api_key,
                base_url=base_url,
                timeout=args.timeout,
                dry_run=args.dry_run,
                print_payload=args.print_payload,
            )
            report = {**_report_base(args, output_dir), **result}
            report_path = _write_report(args, output_dir, report)
            print(json.dumps({"ok": True, "report": str(report_path), "task_id": result["normalized_submit"]["id"]}, ensure_ascii=False))
            return 0

        if args.command == "status":
            api_key = _require_api_key(args.api_key or _env_api_key())
            result = get_status(
                task_id=args.task_id,
                api_key=api_key,
                base_url=base_url,
                timeout=args.timeout,
            )
            report = {**_report_base(args, output_dir), **result}
            report_path = _write_report(args, output_dir, report)
            print(json.dumps({"ok": True, "report": str(report_path), "status": result["normalized_status"]["status"]}, ensure_ascii=False))
            return 0

        if args.command == "download":
            api_key = _require_api_key(args.api_key or _env_api_key())
            result = download_video(
                task_id=args.task_id,
                api_key=api_key,
                base_url=base_url,
                output_dir=output_dir,
                filename_prefix=args.filename_prefix,
                timeout=args.timeout,
            )
            report = {**_report_base(args, output_dir), **result}
            report_path = _write_report(args, output_dir, report)
            print(json.dumps({"ok": True, "report": str(report_path), "saved_file": result["saved_file"]}, ensure_ascii=False))
            return 0

        if args.command == "run":
            api_key = _require_api_key(args.api_key or _env_api_key(), allow_placeholder=args.dry_run)
            if args.duration not in ALLOWED_DURATIONS:
                raise ValueError(f"duration 仅支持 {sorted(ALLOWED_DURATIONS)}")
            ratio = args.ratio or _default_ratio_for_model(args.model)
            submit_result = submit_video(
                prompt=args.prompt,
                image=args.image,
                model=args.model,
                duration=args.duration,
                ratio=ratio,
                watermark=_bool_from_arg(args.watermark),
                seed=args.seed,
                api_key=api_key,
                base_url=base_url,
                timeout=args.timeout,
                dry_run=args.dry_run,
                print_payload=args.print_payload,
            )
            task_id = submit_result["normalized_submit"]["id"]
            if not task_id:
                raise ValueError("创建成功响应缺少 task_id，已停止后续轮询。")
            if args.dry_run:
                report = {
                    **_report_base(args, output_dir),
                    **submit_result,
                    "normalized_status": None,
                    "normalized_download": None,
                    "saved_file": None,
                }
                report_path = _write_report(args, output_dir, report)
                print(json.dumps({"ok": True, "report": str(report_path), "task_id": task_id}, ensure_ascii=False))
                return 0

            status_result = wait_for_task(
                task_id=task_id,
                api_key=api_key,
                base_url=base_url,
                timeout=args.timeout,
                poll_interval=args.poll_interval,
                max_wait_seconds=args.max_wait_seconds,
            )
            download_result = download_video(
                task_id=task_id,
                api_key=api_key,
                base_url=base_url,
                output_dir=output_dir,
                filename_prefix=args.filename_prefix,
                timeout=args.timeout,
            )
            report = {
                **_report_base(args, output_dir),
                "ok": True,
                "request_summary": submit_result.get("request_summary"),
                "normalized_submit": submit_result.get("normalized_submit"),
                "normalized_status": status_result.get("normalized_status"),
                "normalized_download": download_result.get("normalized_download"),
                "saved_file": download_result.get("saved_file"),
                "validation_notes": submit_result.get("validation_notes"),
                "raw_response": {
                    "submit": submit_result.get("raw_response"),
                    "status": status_result.get("raw_response"),
                    "download": download_result.get("raw_response"),
                },
                "error": None,
            }
            report_path = _write_report(args, output_dir, report)
            print(json.dumps({"ok": True, "report": str(report_path), "saved_file": download_result.get("saved_file")}, ensure_ascii=False))
            return 0

        parser.error("未知命令")
        return 2
    except Exception as exc:
        error_text = str(exc)
        try:
            parsed_error = json.loads(error_text)
        except Exception:
            parsed_error = {"message": error_text}
        error_payload = {
            **_report_base(args, output_dir),
            "ok": False,
            "error": parsed_error,
        }
        report_path = _write_report(args, output_dir, error_payload)
        print(json.dumps({"ok": False, "report": str(report_path), "error": parsed_error}, ensure_ascii=False), file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
