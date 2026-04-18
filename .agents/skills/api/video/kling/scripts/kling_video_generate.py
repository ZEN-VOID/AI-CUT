#!/usr/bin/env python3
"""
FineAPI Kling image-to-video CLI.

Confirmed contract on 2026-04-17:
- Create job: POST /kling/v1/videos/image2video
- Query job: GET /kling/v1/videos/image2video/{task_id}
- Final asset comes from query result task_result URLs; no separate download endpoint is assumed.
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

VIDEO_SKILL_ROOT = Path(__file__).resolve().parents[2]
if str(VIDEO_SKILL_ROOT) not in sys.path:
    sys.path.insert(0, str(VIDEO_SKILL_ROOT))

from shared.default_model_policy import select_highest_model


ALLOWED_MODELS = {
    "kling-v1",
    "kling-v1-5",
    "kling-v1-6",
    "kling-v2-master",
    "kling-v2-1",
    "kling-v2-1-master",
    "kling-v2-5-turbo",
    "kling-v2-6",
    "kling-v3",
}
ALLOWED_MODES = {"std", "pro"}
ALLOWED_DURATIONS = {str(i) for i in range(3, 16)}
ALLOWED_SOUND = {"on", "off"}
ALLOWED_SHOT_TYPES = {"customize", "intelligence"}
CFG_SCALE_SUPPORTED_PREFIXES = ("kling-v1",)


def _model_sort_key(model: str) -> Tuple[int, int, int, str]:
    match = re.fullmatch(r"kling-v(?P<major>\d+)(?:-(?P<minor>\d+))?(?:-(?P<variant>[A-Za-z0-9-]+))?", model)
    if not match:
        return (-1, -1, -1, model)

    major = int(match.group("major"))
    minor = int(match.group("minor") or 0)
    variant = (match.group("variant") or "").lower()
    variant_rank = {
        "": 3,
        "master": 2,
        "turbo": 1,
    }.get(variant, 0)
    return (major, minor, variant_rank, model)


def _model_is_at_least(model: str, minimum: str) -> bool:
    return _model_sort_key(model) >= _model_sort_key(minimum)


DEFAULT_MODEL = select_highest_model(ALLOWED_MODELS, sort_key=_model_sort_key)
SOUND_MIN_MODEL = "kling-v2-6"
SOUND_SUPPORTED_MODELS = {model for model in ALLOWED_MODELS if _model_is_at_least(model, SOUND_MIN_MODEL)}
DEFAULT_MODE = "std"
DEFAULT_DURATION = "5"
DEFAULT_SOUND = "off"
DEFAULT_PROJECT_NAME = "测试"
DEFAULT_TIMEOUT = 180
DEFAULT_POLL_INTERVAL = 10
DEFAULT_MAX_WAIT_SECONDS = 900
DRY_RUN_API_KEY_PLACEHOLDER = "__KLING_DRY_RUN_NO_KEY__"
DRY_RUN_BASE_URL_PLACEHOLDER = "https://dry-run.invalid"


def _now_stamp() -> str:
    return datetime.now().strftime("%Y%m%d_%H%M%S")


def _safe_name(text: str, max_len: int = 64) -> str:
    normalized = re.sub(r"\s+", "_", text.strip())
    normalized = re.sub(r"[^0-9A-Za-z_\u4e00-\u9fff-]+", "", normalized)
    return (normalized or "kling_video")[:max_len]


def _env_api_key() -> Optional[str]:
    return (
        os.getenv("ANYFAST_VIDEO_API_KEY")
        or os.getenv("KLING_API_KEY")
        or os.getenv("FINEAPI_KLING_API_KEY")
        or os.getenv("ANYFAST_API_KEY")
        or os.getenv("FINEAPI_API_KEY")
    )


def _env_base_url() -> Optional[str]:
    return (
        os.getenv("ANYFAST_API_BASE_URL")
        or os.getenv("KLING_API_BASE_URL")
        or os.getenv("FINEAPI_KLING_API_BASE_URL")
        or os.getenv("FINEAPI_API_BASE_URL")
    )


def _resolve_api_key(explicit: Optional[str], *, allow_missing: bool = False) -> str:
    value = explicit or _env_api_key()
    if not value:
        if allow_missing:
            return DRY_RUN_API_KEY_PLACEHOLDER
        raise ValueError(
            "缺少 API Key，请配置 ANYFAST_VIDEO_API_KEY / KLING_API_KEY / FINEAPI_KLING_API_KEY / "
            "ANYFAST_API_KEY / FINEAPI_API_KEY 或显式传 --api-key"
        )
    return value


def _resolve_base_url(explicit: Optional[str], *, allow_missing: bool = False) -> str:
    value = explicit or _env_base_url()
    if not value:
        if allow_missing:
            return DRY_RUN_BASE_URL_PLACEHOLDER
        raise ValueError(
            "缺少 Base URL，请配置 ANYFAST_API_BASE_URL / KLING_API_BASE_URL / "
            "FINEAPI_KLING_API_BASE_URL / FINEAPI_API_BASE_URL 或显式传 --base-url"
        )
    return value.rstrip("/")


def _normalize_auth_header(api_key: str) -> str:
    token = api_key.strip()
    if token.lower().startswith("bearer "):
        return token
    return f"Bearer {token}"


def _redact_auth_header(value: str) -> str:
    return "Bearer ***" if value else value


def _is_remote_url(value: str) -> bool:
    parsed = urlparse(value)
    return parsed.scheme in {"http", "https"} and bool(parsed.netloc)


def _is_data_url(value: str) -> bool:
    return value.startswith("data:")


def _guess_mime_type(path: str, fallback: str = "image/png") -> str:
    mime_type, _ = mimetypes.guess_type(path)
    return mime_type or fallback


def _load_bytes_from_path(path_str: str) -> Tuple[bytes, str]:
    path = Path(path_str).expanduser()
    if not path.is_file():
        raise FileNotFoundError(f"本地文件不存在: {path_str}")
    return path.read_bytes(), _guess_mime_type(path.name)


def _strip_data_url(value: str) -> str:
    if not _is_data_url(value):
        return value
    prefix, _, payload = value.partition(",")
    if "base64" not in prefix or not payload:
        raise ValueError("data URL 必须是 base64 形式")
    return payload


def _looks_like_base64(value: str) -> bool:
    candidate = re.sub(r"\s+", "", value)
    if len(candidate) < 32 or len(candidate) % 4 != 0:
        return False
    return bool(re.fullmatch(r"[A-Za-z0-9+/=]+", candidate))


def _normalize_media_value(value: Optional[str]) -> Optional[str]:
    if value is None:
        return None
    text = value.strip()
    if not text:
        return None
    if _is_remote_url(text):
        return text
    if _is_data_url(text):
        return _strip_data_url(text)
    if Path(text).expanduser().is_file():
        raw, _ = _load_bytes_from_path(text)
        return base64.b64encode(raw).decode("utf-8")
    if _looks_like_base64(text):
        return re.sub(r"\s+", "", text)
    # Guard against leaking nonexistent local paths into the JSON payload.
    if any(token in text for token in ("/", "\\", "~")) or Path(text).suffix.lower() in {".png", ".jpg", ".jpeg", ".webp"}:
        raise FileNotFoundError(f"本地媒体文件不存在，且输入也不是可识别的 URL / Base64: {text}")
    return text


def _load_json_input(value: Optional[str], *, field_name: str) -> Any:
    if value is None:
        return None
    stripped = value.strip()
    if not stripped:
        return None
    path = Path(stripped).expanduser()
    if path.is_file():
        return json.loads(path.read_text(encoding="utf-8"))
    try:
        return json.loads(stripped)
    except json.JSONDecodeError as exc:
        raise ValueError(f"{field_name} 需要是 JSON 文件路径或 JSON 字符串") from exc


def _normalize_dynamic_masks(data: Any) -> Any:
    if data is None:
        return None
    if not isinstance(data, list):
        raise ValueError("dynamic_masks 必须是数组")
    normalized = []
    for item in data:
        if not isinstance(item, dict):
            raise ValueError("dynamic_masks 的每个元素都必须是对象")
        current = dict(item)
        current["mask"] = _normalize_media_value(current.get("mask"))
        trajectories = current.get("trajectories")
        if not isinstance(trajectories, list) or not trajectories:
            raise ValueError("dynamic_masks 的每个元素都必须包含非空 trajectories 数组")
        normalized.append(current)
    return normalized


def _ensure_object_list(data: Any, *, field_name: str, max_items: int, required_key: str) -> Any:
    if data is None:
        return None
    if not isinstance(data, list):
        raise ValueError(f"{field_name} 必须是数组")
    if len(data) > max_items:
        raise ValueError(f"{field_name} 最多允许 {max_items} 项")
    normalized = []
    for item in data:
        if not isinstance(item, dict):
            raise ValueError(f"{field_name} 的每个元素都必须是对象")
        if item.get(required_key) in (None, ""):
            raise ValueError(f"{field_name} 的每个元素都必须包含 {required_key}")
        normalized.append(dict(item))
    return normalized


def _validate_multi_prompt(data: Any, *, total_duration: str) -> Any:
    if data is None:
        return None
    if not isinstance(data, list):
        raise ValueError("multi_prompt 必须是数组")
    if not 1 <= len(data) <= 6:
        raise ValueError("multi_prompt 项数必须在 1 到 6 之间")
    max_duration = int(total_duration)
    normalized = []
    for item in data:
        if not isinstance(item, dict):
            raise ValueError("multi_prompt 的每个元素都必须是对象")
        index = item.get("index")
        prompt = item.get("prompt")
        duration = str(item.get("duration", "")).strip()
        if not isinstance(index, int):
            raise ValueError("multi_prompt.index 必须是整数")
        if not isinstance(prompt, str) or not prompt.strip():
            raise ValueError("multi_prompt.prompt 必须是非空字符串")
        if len(prompt) > 512:
            raise ValueError("multi_prompt.prompt 长度不能超过 512 字符")
        if not duration.isdigit():
            raise ValueError("multi_prompt.duration 必须是数字字符串")
        duration_int = int(duration)
        if duration_int < 1 or duration_int > max_duration:
            raise ValueError("multi_prompt.duration 必须在 1 到总时长之间")
        normalized.append({"index": index, "prompt": prompt, "duration": duration})
    return normalized


def _default_output_dir(project_name: str) -> Path:
    project = project_name.strip() or DEFAULT_PROJECT_NAME
    return Path("output") / "影片" / project / "5-API" / "video" / "kling"


def _write_json(path: Path, data: Dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def _make_report_path(output_dir: Path, prefix: str, command: str, explicit: Optional[str]) -> Path:
    if explicit:
        return Path(explicit)
    stem = _safe_name(prefix or "kling")
    return output_dir / f"{stem}_{command}_report_{_now_stamp()}.json"


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


def _unwrap_body(body: Any) -> Any:
    if isinstance(body, dict) and isinstance(body.get("data"), dict):
        return body["data"]
    return body


def _response_ok(response: requests.Response, body: Any) -> bool:
    if not response.ok:
        return False
    if isinstance(body, dict) and "code" in body:
        return body.get("code") == 0
    return True


def _normalize_submit(body: Dict[str, Any]) -> Dict[str, Any]:
    core = _unwrap_body(body)
    if not isinstance(core, dict):
        return {}
    return {
        "id": core.get("id") or core.get("task_id"),
        "task_id": core.get("task_id") or core.get("id"),
        "object": core.get("object"),
        "model": core.get("model"),
        "status": core.get("status") or core.get("task_status"),
        "progress": core.get("progress"),
        "created_at": core.get("created_at"),
        "message": body.get("message") if isinstance(body, dict) else None,
    }


def _normalize_status(body: Dict[str, Any]) -> Dict[str, Any]:
    core = _unwrap_body(body)
    if not isinstance(core, dict):
        return {}
    return {
        "task_id": core.get("task_id") or core.get("id"),
        "task_status": core.get("task_status") or core.get("status"),
        "task_status_msg": core.get("task_status_msg") or core.get("status_msg"),
        "created_at": core.get("created_at"),
        "updated_at": core.get("updated_at"),
        "task_result": core.get("task_result"),
        "message": body.get("message") if isinstance(body, dict) else None,
        "request_id": body.get("request_id") if isinstance(body, dict) else None,
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


def _build_diagnostic_hint(response_body: Optional[Dict[str, Any]] = None) -> Optional[str]:
    messages = [
        f"优先检查页面真源、默认模型是否已自动落到当前最高版本（当前 {DEFAULT_MODEL}），以及 image/image_tail 输入是否已归一化。"
    ]
    if response_body:
        _, merged = _collect_error_strings(response_body)
        lowered = merged.lower()
        if "额度" in merged or "quota" in lowered or "remainquota" in lowered:
            messages.append("当前更像额度或配额问题；优先检查 `.env` 中的 `ANYFAST_VIDEO_API_KEY` 是否仍有余额。")
        if "unauthorized" in lowered or "令牌" in merged or "token" in lowered:
            messages.append("当前更像鉴权问题；优先检查 Bearer Token 与 AnyFast 网关是否匹配。")
    return " ".join(messages)


def _extract_asset_url(body: Dict[str, Any]) -> Tuple[Optional[str], List[str]]:
    tried = []
    core = _unwrap_body(body)
    if not isinstance(core, dict):
        return None, tried
    task_result = core.get("task_result")
    if not isinstance(task_result, dict):
        tried.append("data.task_result")
        return None, tried

    candidate_paths = [
        ("task_result.videos[0].url", task_result.get("videos")),
        ("task_result.video.url", task_result.get("video")),
        ("task_result.assets[0].url", task_result.get("assets")),
        ("task_result.images[0].url", task_result.get("images")),
        ("task_result.video_url", task_result.get("video_url")),
        ("task_result.url", task_result.get("url")),
    ]
    for label, value in candidate_paths:
        tried.append(label)
        if isinstance(value, list) and value:
            first = value[0]
            if isinstance(first, dict) and first.get("url"):
                return str(first["url"]), tried
        elif isinstance(value, dict) and value.get("url"):
            return str(value["url"]), tried
        elif isinstance(value, str) and value:
            return value, tried
    return None, tried


def _build_payload(args: argparse.Namespace) -> Dict[str, Any]:
    image = _normalize_media_value(args.image)
    image_tail = _normalize_media_value(args.image_tail)
    static_mask = _normalize_media_value(args.static_mask) if args.static_mask else None
    if not image and not image_tail:
        raise ValueError("image 与 image_tail 至少二选一")
    if args.model not in ALLOWED_MODELS:
        raise ValueError(f"model_name 不合法: {args.model}")
    if args.mode not in ALLOWED_MODES:
        raise ValueError(f"mode 不合法: {args.mode}")
    if args.duration not in ALLOWED_DURATIONS:
        raise ValueError(f"duration 不合法: {args.duration}")
    if args.sound not in ALLOWED_SOUND:
        raise ValueError(f"sound 不合法: {args.sound}")
    if args.sound == "on" and args.model not in SOUND_SUPPORTED_MODELS:
        allowed_sound_models = " / ".join(sorted(SOUND_SUPPORTED_MODELS, key=_model_sort_key))
        raise ValueError(f"sound=on 仅支持 {SOUND_MIN_MODEL} 及后续模型；当前本地允许 {allowed_sound_models}")
    if args.cfg_scale is not None and not (0 <= args.cfg_scale <= 1):
        raise ValueError("cfg_scale 取值范围必须在 0 到 1 之间")
    if args.cfg_scale is not None and not args.model.startswith(CFG_SCALE_SUPPORTED_PREFIXES):
        raise ValueError("cfg_scale 仅支持 kling-v1.x 模型")
    if args.shot_type and args.shot_type not in ALLOWED_SHOT_TYPES:
        raise ValueError(f"shot_type 不合法: {args.shot_type}")

    multi_prompt = _validate_multi_prompt(
        _load_json_input(args.multi_prompt_json, field_name="multi_prompt"),
        total_duration=args.duration,
    )
    dynamic_masks = _normalize_dynamic_masks(_load_json_input(args.dynamic_masks_json, field_name="dynamic_masks"))
    camera_control = _load_json_input(args.camera_control_json, field_name="camera_control")
    element_list = _ensure_object_list(
        _load_json_input(args.element_list_json, field_name="element_list"),
        field_name="element_list",
        max_items=3,
        required_key="element_id",
    )
    voice_list = _ensure_object_list(
        _load_json_input(args.voice_list_json, field_name="voice_list"),
        field_name="voice_list",
        max_items=2,
        required_key="voice_id",
    )

    control_groups = sum(
        1
        for enabled in (
            bool(image_tail),
            bool(static_mask or dynamic_masks),
            camera_control is not None,
        )
        if enabled
    )
    if control_groups > 1:
        raise ValueError("image_tail、dynamic_masks/static_mask、camera_control 三组控制参数互斥")
    if static_mask and dynamic_masks:
        raise ValueError("static_mask 与 dynamic_masks 不能同时传入")

    prompt = (args.prompt or "").strip()
    if len(prompt) > 2500:
        raise ValueError("prompt 长度不能超过 2500 字符")
    if args.negative_prompt and len(args.negative_prompt) > 2500:
        raise ValueError("negative_prompt 长度不能超过 2500 字符")
    if not args.multi_shot:
        if not prompt:
            raise ValueError("multi_shot=false 时 prompt 必填")
    else:
        if not args.shot_type:
            raise ValueError("multi_shot=true 时 shot_type 必填")
        if args.shot_type == "customize" and not multi_prompt:
            raise ValueError("shot_type=customize 时 multi_prompt 必填")
        if args.shot_type == "intelligence" and not prompt:
            raise ValueError("shot_type=intelligence 时 prompt 必填")

    if element_list and voice_list:
        raise ValueError("element_list 与 voice_list 互斥，不能同时传入")

    payload: Dict[str, Any] = {
        "model_name": args.model,
        "mode": args.mode,
        "duration": args.duration,
        "sound": args.sound,
        "multi_shot": args.multi_shot,
    }
    if image:
        payload["image"] = image
    if image_tail:
        payload["image_tail"] = image_tail
    if prompt:
        payload["prompt"] = prompt
    if args.negative_prompt:
        payload["negative_prompt"] = args.negative_prompt
    if args.cfg_scale is not None:
        payload["cfg_scale"] = args.cfg_scale
    if args.shot_type:
        payload["shot_type"] = args.shot_type
    if multi_prompt is not None:
        payload["multi_prompt"] = multi_prompt
    if static_mask:
        payload["static_mask"] = static_mask
    if dynamic_masks is not None:
        payload["dynamic_masks"] = dynamic_masks
    if camera_control is not None:
        payload["camera_control"] = camera_control
    if element_list is not None:
        payload["element_list"] = element_list
    if voice_list is not None:
        payload["voice_list"] = voice_list
    if args.watermark_enabled is not None:
        payload["watermark_info"] = {"enabled": args.watermark_enabled}
    if args.callback_url:
        payload["callback_url"] = args.callback_url
    if args.external_task_id:
        payload["external_task_id"] = args.external_task_id
    return payload


def _payload_preview(payload: Dict[str, Any]) -> Dict[str, Any]:
    preview = dict(payload)
    for key in ("image", "image_tail", "static_mask"):
        value = preview.get(key)
        if isinstance(value, str) and value and not _is_remote_url(value):
            preview[key] = {"type": "base64", "length": len(value)}
    if isinstance(preview.get("dynamic_masks"), list):
        masks = []
        for item in preview["dynamic_masks"]:
            current = dict(item)
            mask = current.get("mask")
            if isinstance(mask, str) and mask and not _is_remote_url(mask):
                current["mask"] = {"type": "base64", "length": len(mask)}
            masks.append(current)
        preview["dynamic_masks"] = masks
    return preview


def _dry_run_diagnostic(api_key: str, base_url: str) -> str:
    notes = [
        "当前 dry-run 仅验证 JSON 请求体、默认值和高级字段约束。",
        "Kling 真源页面固定为 422568253e0 / 403045624e0 / 403045626e0。",
        f"本技能默认模型按任务要求自动选择当前允许列表中的最高版本，当前为 {DEFAULT_MODEL}；这不同于 FineAPI 页面写的 kling-v1。",
    ]
    if api_key == DRY_RUN_API_KEY_PLACEHOLDER:
        notes.append("未提供 API Key，dry-run 使用占位符")
    if base_url == DRY_RUN_BASE_URL_PLACEHOLDER:
        notes.append("未提供 Base URL，dry-run 使用占位符")
    return " ".join(notes)


def submit_video(*, args: argparse.Namespace, api_key: str, base_url: str) -> Dict[str, Any]:
    payload = _build_payload(args)
    headers = _session_headers(api_key)
    url = f"{base_url}/kling/v1/videos/image2video"
    request_summary = _request_summary("POST", url, headers, data=_payload_preview(payload))
    if args.print_payload or args.dry_run:
        print(json.dumps(request_summary, ensure_ascii=False, indent=2))
    if args.dry_run:
        return {
            "ok": True,
            "request_summary": request_summary,
            "normalized_submit": None,
            "raw_response": None,
            "diagnostic_hint": _dry_run_diagnostic(api_key, base_url),
        }

    response = requests.post(url, headers=headers, json=payload, timeout=args.timeout)
    try:
        body = response.json()
    except ValueError:
        body = {"non_json_response": response.text}

    ok = _response_ok(response, body)
    return {
        "ok": ok,
        "request_summary": request_summary,
        "normalized_submit": _normalize_submit(body) if ok and isinstance(body, dict) else None,
        "raw_response": body,
        "status_code": response.status_code,
        "error": None if ok else "创建任务失败",
        "diagnostic_hint": None if ok else _build_diagnostic_hint(body if isinstance(body, dict) else None),
    }


def query_status(*, task_id: str, api_key: str, base_url: str, timeout: int) -> Dict[str, Any]:
    headers = _session_headers(api_key)
    url = f"{base_url}/kling/v1/videos/image2video/{task_id}"
    response = requests.get(url, headers=headers, timeout=timeout)
    try:
        body = response.json()
    except ValueError:
        body = {"non_json_response": response.text}
    ok = _response_ok(response, body)
    normalized = _normalize_status(body) if ok and isinstance(body, dict) else None
    asset_url, asset_paths = _extract_asset_url(body) if isinstance(body, dict) else (None, [])
    return {
        "ok": ok,
        "request_summary": _request_summary("GET", url, headers),
        "normalized_status": normalized,
        "asset_url": asset_url,
        "asset_url_paths_tried": asset_paths,
        "raw_response": body,
        "status_code": response.status_code,
        "error": None if ok else "查询任务失败",
    }


def poll_until_complete(*, task_id: str, api_key: str, base_url: str, timeout: int, poll_interval: int, max_wait_seconds: int) -> Dict[str, Any]:
    started = time.time()
    history: List[Any] = []
    while True:
        result = query_status(task_id=task_id, api_key=api_key, base_url=base_url, timeout=timeout)
        history.append(result.get("normalized_status") or result.get("raw_response"))
        if not result["ok"]:
            result["history"] = history
            return result
        normalized = result.get("normalized_status") or {}
        task_status = str(normalized.get("task_status") or "").lower()
        if task_status in {"succeed", "succeeded", "success", "completed"}:
            result["history"] = history
            return result
        if task_status in {"failed", "error", "cancelled", "canceled"}:
            result["history"] = history
            result["ok"] = False
            result["error"] = "任务状态为 failed/error/cancelled"
            return result
        if time.time() - started >= max_wait_seconds:
            result["history"] = history
            result["ok"] = False
            result["error"] = f"轮询超时，已等待 {max_wait_seconds} 秒"
            return result
        time.sleep(poll_interval)


def download_from_status(*, task_id: str, api_key: str, base_url: str, timeout: int, output_dir: Path, filename_prefix: str, save_video: bool) -> Dict[str, Any]:
    status_result = query_status(task_id=task_id, api_key=api_key, base_url=base_url, timeout=timeout)
    result = {
        "ok": status_result.get("ok", False),
        "request_summary": status_result.get("request_summary"),
        "normalized_status": status_result.get("normalized_status"),
        "asset_url": status_result.get("asset_url"),
        "asset_url_paths_tried": status_result.get("asset_url_paths_tried"),
        "raw_response": status_result.get("raw_response"),
        "saved_file": None,
        "error": status_result.get("error"),
    }
    if not result["ok"]:
        return result
    asset_url = result["asset_url"]
    if not asset_url:
        result["ok"] = False
        result["error"] = "查询结果未提取到可下载的媒体 URL"
        return result
    if not save_video:
        return result

    output_dir.mkdir(parents=True, exist_ok=True)
    parsed = urlparse(asset_url)
    suffix = Path(parsed.path).suffix or ".mp4"
    target = output_dir / f"{_safe_name(filename_prefix or 'kling')}_{task_id}{suffix}"
    response = requests.get(asset_url, timeout=timeout, stream=True)
    if not response.ok:
        result["ok"] = False
        result["error"] = f"下载媒体文件失败: HTTP {response.status_code}"
        return result
    with target.open("wb") as handle:
        for chunk in response.iter_content(chunk_size=1024 * 512):
            if chunk:
                handle.write(chunk)
    result["saved_file"] = str(target)
    return result


def build_parser() -> argparse.ArgumentParser:
    common = argparse.ArgumentParser(add_help=False)
    common.add_argument("--api-key", help="API Key，不传则读取 .env")
    common.add_argument("--base-url", default=_env_base_url(), help="API Base URL，不传则读取 .env")
    common.add_argument("--timeout", type=int, default=DEFAULT_TIMEOUT, help="HTTP 超时秒数")
    common.add_argument("--project-name", default=DEFAULT_PROJECT_NAME, help="项目名，用于默认输出目录")
    common.add_argument("--output-dir", help="覆盖默认输出目录")
    common.add_argument("--filename-prefix", default="kling", help="报告/视频文件名前缀")
    common.add_argument("--report-json", help="显式指定报告 JSON 路径")

    parser = argparse.ArgumentParser(description="Submit and manage FineAPI Kling image2video tasks", parents=[common])
    sub = parser.add_subparsers(dest="command", required=True)

    def add_create_arguments(target: argparse.ArgumentParser) -> None:
        target.add_argument("--prompt", help="视频提示词；单镜头模式必填")
        target.add_argument("--image", help="首帧参考图，支持本地/远程/data URL/裸 Base64")
        target.add_argument("--image-tail", help="尾帧参考图，支持本地/远程/data URL/裸 Base64")
        target.add_argument("--model", default=DEFAULT_MODEL, choices=sorted(ALLOWED_MODELS))
        target.add_argument("--mode", default=DEFAULT_MODE, choices=sorted(ALLOWED_MODES))
        target.add_argument("--duration", default=DEFAULT_DURATION, choices=sorted(ALLOWED_DURATIONS))
        target.add_argument("--negative-prompt", help="负向提示词")
        target.add_argument("--cfg-scale", type=float, help="0-1，仅 kling-v1.x 稳定支持")
        target.add_argument("--sound", default=DEFAULT_SOUND, choices=sorted(ALLOWED_SOUND))
        target.add_argument("--multi-shot", action="store_true", help="开启多镜头模式")
        target.add_argument("--shot-type", choices=sorted(ALLOWED_SHOT_TYPES))
        target.add_argument("--multi-prompt-json", help="multi_prompt 的 JSON 文件路径或 JSON 字符串")
        target.add_argument("--static-mask", help="静态蒙版，支持本地/远程/data URL/裸 Base64")
        target.add_argument("--dynamic-masks-json", help="dynamic_masks 的 JSON 文件路径或 JSON 字符串")
        target.add_argument("--camera-control-json", help="camera_control 的 JSON 文件路径或 JSON 字符串")
        target.add_argument("--element-list-json", help="element_list 的 JSON 文件路径或 JSON 字符串")
        target.add_argument("--voice-list-json", help="voice_list 的 JSON 文件路径或 JSON 字符串")
        target.add_argument("--watermark-enabled", type=lambda x: str(x).lower() == "true", help="true/false；显式传入时写入 watermark_info.enabled")
        target.add_argument("--callback-url", help="回调地址")
        target.add_argument("--external-task-id", help="自定义任务 ID")
        target.add_argument("--dry-run", action="store_true")
        target.add_argument("--print-payload", action="store_true")

    submit_parser = sub.add_parser("submit", aliases=["create"], help="创建图生视频任务", parents=[common])
    add_create_arguments(submit_parser)

    status_parser = sub.add_parser("status", help="查询图生视频任务状态", parents=[common])
    status_parser.add_argument("--task-id", required=True)

    download_parser = sub.add_parser("download", help="按任务 ID 下载最终视频", parents=[common])
    download_parser.add_argument("--task-id", required=True)
    download_parser.add_argument("--no-save-video", action="store_true")

    run_parser = sub.add_parser("run", help="创建 + 轮询 + 下载", parents=[common])
    add_create_arguments(run_parser)
    run_parser.add_argument("--poll-interval", type=int, default=DEFAULT_POLL_INTERVAL)
    run_parser.add_argument("--max-wait-seconds", type=int, default=DEFAULT_MAX_WAIT_SECONDS)
    run_parser.add_argument("--no-save-video", action="store_true")

    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()

    try:
        allow_missing_env = bool(getattr(args, "dry_run", False) and args.command in {"submit", "run"})
        api_key = _resolve_api_key(getattr(args, "api_key", None), allow_missing=allow_missing_env)
        base_url = _resolve_base_url(getattr(args, "base_url", None), allow_missing=allow_missing_env)
        output_dir = Path(args.output_dir) if getattr(args, "output_dir", None) else _default_output_dir(args.project_name)

        if args.command in {"submit", "create"}:
            result = submit_video(args=args, api_key=api_key, base_url=base_url)
        elif args.command == "status":
            result = query_status(task_id=args.task_id, api_key=api_key, base_url=base_url, timeout=args.timeout)
        elif args.command == "download":
            result = download_from_status(
                task_id=args.task_id,
                api_key=api_key,
                base_url=base_url,
                timeout=args.timeout,
                output_dir=output_dir,
                filename_prefix=args.filename_prefix,
                save_video=not args.no_save_video,
            )
        elif args.command == "run":
            submit_result = submit_video(args=args, api_key=api_key, base_url=base_url)
            if not submit_result.get("ok"):
                result = {"ok": False, "command": "run", "submit": submit_result, "error": submit_result.get("error") or "创建任务失败"}
            elif args.dry_run:
                result = {"ok": True, "command": "run", "submit": submit_result, "diagnostic_hint": "dry-run 未实际进入轮询和下载阶段"}
            else:
                submit_normalized = submit_result.get("normalized_submit") or {}
                task_id = submit_normalized.get("task_id") or submit_normalized.get("id")
                if not task_id:
                    result = {
                        "ok": False,
                        "command": "run",
                        "submit": submit_result,
                        "error": "创建响应未提取到 task_id",
                    }
                else:
                    status_result = poll_until_complete(
                        task_id=task_id,
                        api_key=api_key,
                        base_url=base_url,
                        timeout=args.timeout,
                        poll_interval=args.poll_interval,
                        max_wait_seconds=args.max_wait_seconds,
                    )
                    if not status_result.get("ok"):
                        result = {"ok": False, "command": "run", "submit": submit_result, "status": status_result, "error": status_result.get("error") or "轮询失败"}
                    else:
                        download_result = download_from_status(
                            task_id=task_id,
                            api_key=api_key,
                            base_url=base_url,
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
                            "asset_url": download_result.get("asset_url"),
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
        fallback_output_dir = Path(getattr(args, "output_dir", "")) if getattr(args, "output_dir", None) else _default_output_dir(getattr(args, "project_name", DEFAULT_PROJECT_NAME))
        error_result = {"ok": False, "command": getattr(args, "command", "unknown"), "error": str(exc)}
        report_path = _make_report_path(
            fallback_output_dir,
            getattr(args, "filename_prefix", "kling"),
            getattr(args, "command", "error"),
            getattr(args, "report_json", None),
        )
        _write_json(report_path, error_result)
        error_result["report_json"] = str(report_path)
        print(json.dumps(error_result, ensure_ascii=False, indent=2))
        return 1


if __name__ == "__main__":
    sys.exit(main())
