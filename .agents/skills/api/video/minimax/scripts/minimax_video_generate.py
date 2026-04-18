#!/usr/bin/env python3
"""
MiniMax Hailuo video generation create CLI.

Current scope:
- submit/create: create a MiniMax Hailuo task via POST /v1/video/generations

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

VIDEO_SKILL_ROOT = Path(__file__).resolve().parents[2]
if str(VIDEO_SKILL_ROOT) not in sys.path:
    sys.path.insert(0, str(VIDEO_SKILL_ROOT))

from shared.default_model_policy import select_latest_by_version


DEFAULT_BASE_URL = "https://fw2afus.ent.acc.kurtisasia.com"
DEFAULT_PROJECT_NAME = "测试"
DEFAULT_TIMEOUT = 180
KNOWN_MODELS = {
    "Hunyuan",
    "Hailuo-02",
    "Hailuo-2.3",
    "Kling-2.0",
    "Kling-2.1",
    "Kling-2.5",
    "Kling-2.6",
    "Kling-01",
    "Vidu-q2",
    "Vidu-q2-pro",
    "Vidu-q2-turbo",
    "OS-2.0",
    "GV-3.1",
}
ALLOWED_REFERENCE_TYPES = {"asset", "style"}
ALLOWED_RESOLUTIONS = {"720P", "768P", "1080P"}
ALLOWED_ASPECT_RATIOS = {"16:9", "9:16", "1:1", "4:3", "3:4"}
ALLOWED_LOGO_ADD = {0, 1}


def _now_stamp() -> str:
    return datetime.now().strftime("%Y%m%d_%H%M%S")


def _safe_name(text: str, max_len: int = 64) -> str:
    normalized = re.sub(r"\s+", "_", text.strip())
    normalized = re.sub(r"[^0-9A-Za-z_\u4e00-\u9fff-]+", "", normalized)
    return (normalized or "minimax_video")[:max_len]


def _version_key_from_model(model: str) -> tuple[int, ...]:
    match = re.search(r"(\d+(?:\.\d+)*)", model)
    if not match:
        return (0,)
    return tuple(int(part) for part in match.group(1).split("."))


DEFAULT_MODEL = select_latest_by_version(
    KNOWN_MODELS,
    version_key=_version_key_from_model,
    predicate=lambda model: model.startswith("Hailuo"),
    error_message="未找到 Hailuo 系列模型，无法推导默认模型",
)


def _env_api_key() -> Optional[str]:
    return (
        os.getenv("ANYFAST_VIDEO_API_KEY")
        or os.getenv("ANYFAST_API_KEY")
        or os.getenv("FINEAPI_API_KEY")
    )


def _env_base_url() -> str:
    return (
        os.getenv("MINIMAX_API_BASE_URL")
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


def _ensure_http_url(value: str, field_name: str) -> str:
    if not _is_http_url(value):
        raise ValueError(f"{field_name} 仅接受 http/https URL: {value}")
    return value


def _default_output_dir(project_name: str) -> Path:
    project = project_name.strip() or DEFAULT_PROJECT_NAME
    return Path("output") / "影片" / project / "5-API" / "video" / "minimax"


def _write_json(path: Path, data: Dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def _make_report_path(output_dir: Path, prefix: str, command: str, explicit: Optional[str]) -> Path:
    if explicit:
        return Path(explicit)
    stem = _safe_name(prefix or "minimax")
    return output_dir / f"{stem}_{command}_report_{_now_stamp()}.json"


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
        "task_id": body.get("task_id"),
        "model": body.get("model"),
        "status": body.get("status"),
        "created_at": body.get("created_at"),
    }


def _parse_image_info_items(raw_items: List[str], raw_json_items: List[str]) -> List[Dict[str, Any]]:
    items: List[Dict[str, Any]] = []
    for raw in raw_items:
        value = raw.strip()
        if not value:
            continue
        if "|" in value:
            image_url, reference_type = value.split("|", 1)
            image_url = _ensure_http_url(image_url.strip(), "ImageInfos.ImageUrl")
            ref = reference_type.strip()
            if ref not in ALLOWED_REFERENCE_TYPES:
                raise ValueError(f"ReferenceType 不合法: {ref}")
            items.append({"ImageUrl": image_url, "ReferenceType": ref})
        else:
            items.append({"ImageUrl": _ensure_http_url(value, "ImageInfos.ImageUrl")})

    for raw_json in raw_json_items:
        try:
            obj = json.loads(raw_json)
        except json.JSONDecodeError as exc:
            raise ValueError(f"image-info-json 不是合法 JSON: {raw_json}") from exc
        if not isinstance(obj, dict):
            raise ValueError("image-info-json 必须是单个 JSON object")
        image_url = obj.get("ImageUrl") or obj.get("imageUrl") or obj.get("image_url")
        if not isinstance(image_url, str):
            raise ValueError("image-info-json 缺少 ImageUrl")
        normalized: Dict[str, Any] = {"ImageUrl": _ensure_http_url(image_url, "ImageInfos.ImageUrl")}
        reference_type = obj.get("ReferenceType") or obj.get("referenceType") or obj.get("reference_type")
        if reference_type is not None:
            if not isinstance(reference_type, str) or reference_type not in ALLOWED_REFERENCE_TYPES:
                raise ValueError(f"ReferenceType 不合法: {reference_type}")
            normalized["ReferenceType"] = reference_type
        items.append(normalized)

    return items


def _build_store_cos_param(
    *,
    bucket_name: Optional[str],
    bucket_region: Optional[str],
    bucket_path: Optional[str],
) -> Optional[Dict[str, Any]]:
    if not any([bucket_name, bucket_region, bucket_path]):
        return None
    payload: Dict[str, Any] = {}
    if bucket_name:
        payload["CosBucketName"] = bucket_name
    if bucket_region:
        payload["CosBucketRegion"] = bucket_region
    if bucket_path:
        payload["CosBucketPath"] = bucket_path
    return payload


def _build_extra_parameters(
    *,
    resolution: Optional[str],
    aspect_ratio: Optional[str],
    logo_add: Optional[int],
    enable_audio: Optional[bool],
    offpeak: Optional[bool],
) -> Optional[Dict[str, Any]]:
    payload: Dict[str, Any] = {}
    if resolution is not None:
        if resolution not in ALLOWED_RESOLUTIONS:
            raise ValueError(f"resolution 不合法: {resolution}")
        payload["Resolution"] = resolution
    if aspect_ratio is not None:
        if aspect_ratio not in ALLOWED_ASPECT_RATIOS:
            raise ValueError(f"aspect_ratio 不合法: {aspect_ratio}")
        payload["AspectRatio"] = aspect_ratio
    if logo_add is not None:
        if logo_add not in ALLOWED_LOGO_ADD:
            raise ValueError(f"logo_add 不合法: {logo_add}")
        payload["LogoAdd"] = logo_add
    if enable_audio is not None:
        payload["EnableAudio"] = enable_audio
    if offpeak is not None:
        payload["OffPeak"] = offpeak
    return payload or None


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


def _build_validation_notes(
    *,
    model: str,
    image_infos: List[Dict[str, Any]],
    resolution: Optional[str],
    aspect_ratio: Optional[str],
    offpeak: Optional[bool],
    response_body: Optional[Dict[str, Any]] = None,
) -> List[str]:
    notes: List[str] = []
    if model not in KNOWN_MODELS:
        notes.append(f"模型 `{model}` 不在当前截图确认集合中；若网关报错，请先回退到 `{DEFAULT_MODEL}`。")

    if model.startswith("Hailuo"):
        if resolution is None:
            notes.append("截图标注 Hailuo 默认分辨率为 `768P`；当前未显式传 `Resolution`，将沿用接口默认值。")
        if aspect_ratio is not None:
            notes.append("截图标注 Hailuo 当前不支持 `AspectRatio`；若网关拒绝，请先移除该字段。")

    if any("ReferenceType" in item for item in image_infos) and not model.startswith("GV-"):
        notes.append("截图标注 `ReferenceType` 仅 GV 模型支持；当前已保留提交能力，但若网关拒绝请先去掉该字段。")

    if aspect_ratio in {"4:3", "3:4"} and not model.startswith("Vidu-q2"):
        notes.append("截图标注 `4:3 / 3:4` 仅 q2 支持；当前模型若非 `Vidu-q2*`，失败时请先改回 `16:9 / 9:16 / 1:1`。")

    if offpeak and not model.startswith("Vidu"):
        notes.append("截图标注 `OffPeak` 仅 Vidu 支持；当前模型若非 `Vidu-*`，失败时请先去掉该字段。")

    if response_body:
        text_parts = _collect_text_leaves(response_body)
        merged = " | ".join(text_parts)
        if "quota" in merged.lower() or "额度" in merged or "余额" in merged:
            notes.append("当前更像额度或配额问题；优先检查 `.env` 中的 `ANYFAST_VIDEO_API_KEY` 是否仍有余额。")
        if "unauthorized" in merged.lower() or "authorization failed" in merged.lower() or "invalid token" in merged.lower():
            notes.append("当前更像鉴权问题；优先检查 Bearer Token 与 Base URL 是否匹配。")
        if "model_not_found" in merged.lower() or "no available channel for model" in merged.lower():
            notes.append(f"当前更像该网关尚未给 `{model}` 开通可用 channel；若只是验证链路，可临时改用更旧模型，但默认值仍保持最高版本。")
    return notes


def submit_video(
    *,
    prompt: Optional[str],
    model: str,
    scene_type: Optional[str],
    negative_prompt: Optional[str],
    enhance_prompt: Optional[bool],
    image_url: Optional[str],
    image_infos: List[Dict[str, Any]],
    last_image_url: Optional[str],
    duration: Optional[int],
    additional_parameters: Optional[str],
    operator: Optional[str],
    store_cos_param: Optional[Dict[str, Any]],
    extra_parameters: Optional[Dict[str, Any]],
    api_key: str,
    base_url: str,
    timeout: int,
    dry_run: bool,
    print_payload: bool,
) -> Dict[str, Any]:
    prompt_value = (prompt or "").strip()
    normalized_image_url = _ensure_http_url(image_url, "ImageUrl") if image_url else None
    normalized_last_image_url = _ensure_http_url(last_image_url, "LastImageUrl") if last_image_url else None

    if not prompt_value and not normalized_image_url and not image_infos:
        raise ValueError("Prompt / ImageUrl / ImageInfos 至少需要提供一项")

    payload: Dict[str, Any] = {"Model": model}
    if scene_type:
        payload["SceneType"] = scene_type
    if prompt_value:
        payload["Prompt"] = prompt_value
    if negative_prompt:
        payload["NegativePrompt"] = negative_prompt
    if enhance_prompt is not None:
        payload["EnhancePrompt"] = enhance_prompt
    if normalized_image_url:
        payload["ImageUrl"] = normalized_image_url
    if image_infos:
        payload["ImageInfos"] = image_infos
    if normalized_last_image_url:
        payload["LastImageUrl"] = normalized_last_image_url
    if duration is not None:
        payload["Duration"] = duration
    if additional_parameters:
        payload["AdditionalParameters"] = additional_parameters
    if operator:
        payload["Operator"] = operator
    if store_cos_param:
        payload["StoreCosParam"] = store_cos_param
    if extra_parameters:
        payload["ExtraParameters"] = extra_parameters

    headers = {
        "Authorization": _normalize_auth_header(api_key),
        "Accept": "application/json",
        "Content-Type": "application/json",
    }
    url = f"{base_url.rstrip('/')}/v1/video/generations"
    request_summary = _request_summary(method="POST", url=url, headers=headers, data=payload)
    validation_notes = _build_validation_notes(
        model=model,
        image_infos=image_infos,
        resolution=(extra_parameters or {}).get("Resolution"),
        aspect_ratio=(extra_parameters or {}).get("AspectRatio"),
        offpeak=(extra_parameters or {}).get("OffPeak"),
    )

    if print_payload or dry_run:
        print(json.dumps(request_summary, ensure_ascii=False, indent=2))
    if dry_run:
        return {
            "ok": True,
            "request_summary": request_summary,
            "normalized_submit": None,
            "raw_response": None,
            "validation_notes": validation_notes,
            "diagnostic_hint": None,
        }

    response = requests.post(url, headers=headers, json=payload, timeout=timeout)
    try:
        body = response.json()
    except ValueError:
        body = {"non_json_response": response.text}

    updated_notes = _build_validation_notes(
        model=model,
        image_infos=image_infos,
        resolution=(extra_parameters or {}).get("Resolution"),
        aspect_ratio=(extra_parameters or {}).get("AspectRatio"),
        offpeak=(extra_parameters or {}).get("OffPeak"),
        response_body=body if isinstance(body, dict) else None,
    )
    diagnostic_hint = " ".join(updated_notes) if updated_notes else None

    return {
        "ok": response.ok,
        "request_summary": request_summary,
        "normalized_submit": _normalize_submit_response(body) if response.ok else None,
        "raw_response": body,
        "status_code": response.status_code,
        "error": None if response.ok else "创建任务失败",
        "validation_notes": updated_notes,
        "diagnostic_hint": diagnostic_hint,
    }


def build_parser() -> argparse.ArgumentParser:
    common_parser = argparse.ArgumentParser(add_help=False)
    common_parser.add_argument("--api-key", help="API Key，不传则读取 .env")
    common_parser.add_argument("--base-url", default=_env_base_url(), help="API 基础 URL")
    common_parser.add_argument("--timeout", type=int, default=DEFAULT_TIMEOUT, help="HTTP 超时秒数")
    common_parser.add_argument("--project-name", default=DEFAULT_PROJECT_NAME, help="项目名，用于默认输出目录")
    common_parser.add_argument("--output-dir", help="覆盖默认输出目录")
    common_parser.add_argument("--filename-prefix", default="minimax", help="报告文件名前缀")
    common_parser.add_argument("--report-json", help="显式指定报告 JSON 路径")

    parser = argparse.ArgumentParser(
        description="Submit MiniMax Hailuo video generation create tasks",
        parents=[common_parser],
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    submit_parser = subparsers.add_parser(
        "submit",
        aliases=["create"],
        help="创建视频任务",
        parents=[common_parser],
    )
    submit_parser.add_argument(
        "--model",
        default=DEFAULT_MODEL,
        help=f"模型 ID；默认自动选择当前已登记 Hailuo 系列最高版本（当前为 {DEFAULT_MODEL}）",
    )
    submit_parser.add_argument("--scene-type", help="SceneType")
    submit_parser.add_argument("--prompt", help="Prompt，和图像输入三选一")
    submit_parser.add_argument("--negative-prompt", help="NegativePrompt")
    submit_parser.add_argument(
        "--enhance-prompt",
        help="是否开启提示词增强：true/false",
    )
    submit_parser.add_argument("--image-url", help="ImageUrl，单图参考 URL")
    submit_parser.add_argument(
        "--image-info",
        action="append",
        default=[],
        help="ImageInfos 条目，格式：URL|style 或 URL|asset；若无 |type 则仅传 ImageUrl",
    )
    submit_parser.add_argument(
        "--image-info-json",
        action="append",
        default=[],
        help='直接传单个 ImageInfo JSON，例如 {"ImageUrl":"https://...","ReferenceType":"style"}',
    )
    submit_parser.add_argument("--last-image-url", help="LastImageUrl，尾帧图 URL")
    submit_parser.add_argument("--duration", type=int, help="Duration，视频时长（秒）")
    submit_parser.add_argument("--additional-parameters", help="AdditionalParameters，原样字符串")
    submit_parser.add_argument("--operator", help="Operator")
    submit_parser.add_argument("--cos-bucket-name", help="StoreCosParam.CosBucketName")
    submit_parser.add_argument("--cos-bucket-region", help="StoreCosParam.CosBucketRegion")
    submit_parser.add_argument("--cos-bucket-path", help="StoreCosParam.CosBucketPath")
    submit_parser.add_argument(
        "--resolution",
        choices=sorted(ALLOWED_RESOLUTIONS),
        help="ExtraParameters.Resolution",
    )
    submit_parser.add_argument(
        "--aspect-ratio",
        choices=sorted(ALLOWED_ASPECT_RATIOS),
        help="ExtraParameters.AspectRatio",
    )
    submit_parser.add_argument(
        "--logo-add",
        type=int,
        choices=sorted(ALLOWED_LOGO_ADD),
        help="ExtraParameters.LogoAdd，0 或 1",
    )
    submit_parser.add_argument("--enable-audio", help="ExtraParameters.EnableAudio，true/false")
    submit_parser.add_argument("--offpeak", help="ExtraParameters.OffPeak，true/false")
    submit_parser.add_argument("--dry-run", action="store_true", help="只打印请求，不真正发出")
    submit_parser.add_argument("--print-payload", action="store_true", help="打印请求摘要")
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()

    api_key = args.api_key or _env_api_key()
    if not api_key:
        raise ValueError(
            "缺少 API Key，请在 .env 中配置 ANYFAST_VIDEO_API_KEY / ANYFAST_API_KEY / FINEAPI_API_KEY"
        )
    if not args.base_url:
        raise ValueError(
            "缺少 Base URL，请配置 MINIMAX_API_BASE_URL / ANYFAST_API_BASE_URL / FINEAPI_API_BASE_URL 或显式传 --base-url"
        )

    output_dir = Path(args.output_dir) if args.output_dir else _default_output_dir(args.project_name)
    report_path = _make_report_path(output_dir, args.filename_prefix, args.command, args.report_json)

    image_infos = _parse_image_info_items(args.image_info, args.image_info_json)
    store_cos_param = _build_store_cos_param(
        bucket_name=args.cos_bucket_name,
        bucket_region=args.cos_bucket_region,
        bucket_path=args.cos_bucket_path,
    )
    extra_parameters = _build_extra_parameters(
        resolution=args.resolution,
        aspect_ratio=args.aspect_ratio,
        logo_add=args.logo_add,
        enable_audio=_parse_bool_optional(args.enable_audio),
        offpeak=_parse_bool_optional(args.offpeak),
    )
    enhance_prompt = _parse_bool_optional(args.enhance_prompt)

    result = submit_video(
        prompt=args.prompt,
        model=args.model,
        scene_type=args.scene_type,
        negative_prompt=args.negative_prompt,
        enhance_prompt=enhance_prompt,
        image_url=args.image_url,
        image_infos=image_infos,
        last_image_url=args.last_image_url,
        duration=args.duration,
        additional_parameters=args.additional_parameters,
        operator=args.operator,
        store_cos_param=store_cos_param,
        extra_parameters=extra_parameters,
        api_key=api_key,
        base_url=args.base_url,
        timeout=args.timeout,
        dry_run=args.dry_run,
        print_payload=args.print_payload,
    )

    report = {
        "ok": result.get("ok", False),
        "command": args.command,
        "request_summary": result.get("request_summary"),
        "normalized_submit": result.get("normalized_submit"),
        "validation_notes": result.get("validation_notes"),
        "diagnostic_hint": result.get("diagnostic_hint"),
        "raw_response": result.get("raw_response"),
        "error": result.get("error"),
    }
    _write_json(report_path, report)
    print(json.dumps({"report_json": str(report_path), **report}, ensure_ascii=False, indent=2))
    return 0 if result.get("ok", False) else 1


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:
        print(f"❌ {exc}", file=sys.stderr)
        raise
