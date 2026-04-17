#!/usr/bin/env python3
"""
FineAPI Veo creation CLI.

Current confirmed scope:
- submit/create: create a Veo video task via POST /v1/video/create

The currently confirmed material covers the create endpoint only.
Status polling and result download must not be invented until newer docs are available.
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


DEFAULT_PROJECT_NAME = "测试"
DEFAULT_TIMEOUT = 180
DRY_RUN_API_KEY_PLACEHOLDER = "__VEO_DRY_RUN_NO_KEY__"
DRY_RUN_BASE_URL_PLACEHOLDER = "https://dry-run.invalid"
DEFAULT_SUBMIT_PATH = "/v1/video/create"
ANYFAST_FALLBACK_SUBMIT_PATH = "/v1/video/generations"
ALLOWED_MODELS = {
    "veo2",
    "veo2-fast",
    "veo2-fast-frames",
    "veo2-fast-components",
    "veo2-pro",
    "veo2-pro-components",
    "veo3",
    "veo3-fast",
    "veo3-fast-frames",
    "veo3-frames",
    "veo3-pro",
    "veo3-pro-frames",
    "veo3.1",
    "veo3.1-fast",
    "veo3.1-pro",
}
ALLOWED_ASPECT_RATIOS = {"16:9", "9:16"}
MODEL_IMAGE_LIMITS = {
    "veo2-fast-frames": 2,
    "veo3-fast-frames": 2,
    "veo3-pro-frames": 1,
    "veo2-fast-components": 3,
}
MODELS_REQUIRING_IMAGES = {
    "veo2-fast-frames",
    "veo2-fast-components",
    "veo2-pro-components",
    "veo3-fast-frames",
    "veo3-frames",
    "veo3-pro-frames",
}


def _model_sort_key(model: str) -> tuple[int, int, int, int, str]:
    match = re.fullmatch(
        r"veo(?P<major>\d+)(?:\.(?P<minor>\d+))?(?:-(?P<variant>[A-Za-z0-9-]+))?",
        model,
    )
    if not match:
        return (-1, -1, -1, -1, model)

    major = int(match.group("major"))
    minor = int(match.group("minor") or 0)
    variant = (match.group("variant") or "").lower()

    capability_rank = 0
    if "frames" in variant:
        capability_rank = -2
    elif "components" in variant:
        capability_rank = -1

    if variant.endswith("pro"):
        variant_rank = 3
    elif variant == "":
        variant_rank = 2
    elif variant.endswith("fast"):
        variant_rank = 1
    else:
        variant_rank = 0

    return (major, minor, capability_rank, variant_rank, model)


def _highest_general_model(models: set[str]) -> str:
    general_models = {
        model
        for model in models
        if "frames" not in model and "components" not in model
    }
    if not general_models:
        raise ValueError("未找到可作为默认值的通用 Veo 模型")
    return max(general_models, key=_model_sort_key)


DEFAULT_MODEL = _highest_general_model(ALLOWED_MODELS)


def _now_stamp() -> str:
    return datetime.now().strftime("%Y%m%d_%H%M%S")


def _safe_name(text: str, max_len: int = 64) -> str:
    normalized = re.sub(r"\s+", "_", text.strip())
    normalized = re.sub(r"[^0-9A-Za-z_\u4e00-\u9fff-]+", "", normalized)
    return (normalized or "veo_video")[:max_len]


def _env_api_key() -> Optional[str]:
    return (
        os.getenv("VEO_API_KEY")
        or os.getenv("ANYFAST_VIDEO_API_KEY")
        or os.getenv("ANYFAST_API_KEY")
        or os.getenv("FINEAPI_API_KEY")
    )


def _env_base_url() -> Optional[str]:
    return (
        os.getenv("VEO_API_BASE_URL")
        or os.getenv("ANYFAST_API_BASE_URL")
        or os.getenv("FINEAPI_API_BASE_URL")
    )


def _resolve_api_key(explicit: Optional[str], *, allow_missing: bool = False) -> str:
    value = explicit or _env_api_key()
    if not value:
        if allow_missing:
            return DRY_RUN_API_KEY_PLACEHOLDER
        raise ValueError(
            "缺少 API Key，请配置 VEO_API_KEY / ANYFAST_VIDEO_API_KEY / ANYFAST_API_KEY / FINEAPI_API_KEY 或显式传 --api-key"
        )
    return value


def _resolve_base_url(explicit: Optional[str], *, allow_missing: bool = False) -> str:
    value = explicit or _env_base_url()
    if not value:
        if allow_missing:
            return DRY_RUN_BASE_URL_PLACEHOLDER
        raise ValueError(
            "缺少 Base URL，请配置 VEO_API_BASE_URL / ANYFAST_API_BASE_URL / FINEAPI_API_BASE_URL 或显式传 --base-url"
        )
    return value.rstrip("/")


def _normalize_auth_header(api_key: str) -> str:
    token = api_key.strip()
    if token.lower().startswith("bearer "):
        return token
    return f"Bearer {token}"


def _redact_auth_header(value: str) -> str:
    return "Bearer ***" if value else value


def _parse_bool_optional(raw: Optional[str]) -> Optional[bool]:
    if raw is None:
        return None
    normalized = raw.strip().lower()
    if normalized == "true":
        return True
    if normalized == "false":
        return False
    raise ValueError("布尔参数只接受 true / false")


def _contains_chinese(text: str) -> bool:
    return bool(re.search(r"[\u4e00-\u9fff]", text))


def _is_remote_url(value: str) -> bool:
    parsed = urlparse(value)
    return parsed.scheme in {"http", "https"} and bool(parsed.netloc)


def _default_output_dir(project_name: str) -> Path:
    project = project_name.strip() or DEFAULT_PROJECT_NAME
    return Path("output") / "影片" / project / "5-API" / "video" / "veo"


def _write_json(path: Path, data: Dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def _make_report_path(output_dir: Path, prefix: str, command: str, explicit: Optional[str]) -> Path:
    if explicit:
        return Path(explicit)
    stem = _safe_name(prefix or "veo")
    return output_dir / f"{stem}_{command}_report_{_now_stamp()}.json"


def _session_headers(api_key: str) -> Dict[str, str]:
    return {
        "Authorization": _normalize_auth_header(api_key),
        "Accept": "application/json",
        "Content-Type": "application/json",
    }


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
    choices = body.get("choices")
    first_choice = choices[0] if isinstance(choices, list) and choices else None
    return {
        "id": body.get("id"),
        "status": body.get("status"),
        "status_update_time": body.get("status_update_time"),
        "enhanced_prompt": body.get("enhanced_prompt"),
        "object": body.get("object"),
        "created": body.get("created"),
        "finish_reason": first_choice.get("finish_reason") if isinstance(first_choice, dict) else None,
        "usage": body.get("usage"),
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


def _build_validation_notes(
    *,
    model: str,
    prompt: str,
    images: List[str],
    enable_upsample: Optional[bool],
    enhance_prompt: Optional[bool],
    aspect_ratio: Optional[str],
    response_body: Optional[Dict[str, Any]] = None,
) -> List[str]:
    notes: List[str] = []

    if images and model not in MODELS_REQUIRING_IMAGES and "components" not in model and "frames" not in model:
        notes.append("当前模型支持无图创建；已随请求发送 images，如网关拒绝可先去掉图片后重试。")
    if model in MODELS_REQUIRING_IMAGES and not images:
        notes.append("当前模型名包含 frames/components 语义，通常需要 images；若网关拒绝，请补充图片 URL。")
    if _contains_chinese(prompt) and enhance_prompt is not True:
        notes.append("prompt 含中文；文档说明 Veo 仅支持英文提示词，建议显式传 `--enhance-prompt true`。")
    if images and enable_upsample is None:
        notes.append("图生页把 `enable_upsample` 标成必填；若网关报字段缺失，请显式传 `--enable-upsample true/false`。")
    if images and enhance_prompt is None:
        notes.append("图生页把 `enhance_prompt` 标成必填；若网关报字段缺失，请显式传 `--enhance-prompt true/false`。")
    if model.startswith("veo3") and aspect_ratio is None:
        notes.append("当前示例中的 `veo3*` 请求都带 `aspect_ratio`；若网关报字段缺失，请显式传 `16:9` 或 `9:16`。")
    if model == "veo2-pro-components":
        notes.append("当前材料只明确给了 `veo2-fast-components` 的 3 图上限；`veo2-pro-components` 若失败，请优先收敛到最多 3 张图。")
    if response_body:
        _, merged = _collect_error_strings(response_body)
        lower = merged.lower()
        if "quota" in lower or "余额" in merged or "额度" in merged:
            notes.append("当前更像额度或配额问题；优先检查 FineAPI/Veo 通道余额。")
        if "unauthorized" in lower or "authorization" in lower or (
            "token" in lower and "quota" not in lower and "额度" not in merged and "余额" not in merged
        ):
            notes.append("当前更像鉴权问题；优先检查 Bearer Token 与 Base URL 是否匹配。")
        if "aspect_ratio" in lower:
            notes.append("当前更像比例字段不被模型接受；优先确认该模型是否属于 `veo3*`。")
    return notes


def _should_retry_with_fallback_path(status_code: int, response_body: Any) -> bool:
    if status_code != 404 or not isinstance(response_body, dict):
        return False
    _, merged = _collect_error_strings(response_body)
    return "invalid url" in merged.lower()


def _validate_inputs(
    *,
    prompt: str,
    model: str,
    images: List[str],
    aspect_ratio: Optional[str],
) -> None:
    if not prompt.strip():
        raise ValueError("prompt 不能为空")
    if model not in ALLOWED_MODELS:
        raise ValueError(f"model 不合法: {model}")
    if aspect_ratio is not None:
        if aspect_ratio not in ALLOWED_ASPECT_RATIOS:
            raise ValueError(f"aspect_ratio 不合法: {aspect_ratio}")
        if not model.startswith("veo3"):
            raise ValueError("aspect_ratio 仅支持 veo3* 家族模型")
    invalid_images = [item for item in images if not _is_remote_url(item)]
    if invalid_images:
        raise ValueError("images 仅接受公网 http/https 链接，以下输入不合法: " + ", ".join(invalid_images))
    if model in MODELS_REQUIRING_IMAGES and not images:
        raise ValueError(f"{model} 需要通过 --image 传入至少一张图片 URL")
    max_images = MODEL_IMAGE_LIMITS.get(model)
    if max_images is not None and len(images) > max_images:
        raise ValueError(f"{model} 最多支持 {max_images} 张图片，当前收到 {len(images)} 张")


def submit_video(
    *,
    prompt: str,
    model: str,
    images: List[str],
    enable_upsample: Optional[bool],
    enhance_prompt: Optional[bool],
    aspect_ratio: Optional[str],
    api_key: str,
    base_url: str,
    submit_path: str,
    timeout: int,
    dry_run: bool,
    print_payload: bool,
) -> Dict[str, Any]:
    _validate_inputs(prompt=prompt, model=model, images=images, aspect_ratio=aspect_ratio)

    payload: Dict[str, Any] = {
        "model": model,
        "prompt": prompt,
    }
    if enable_upsample is not None:
        payload["enable_upsample"] = enable_upsample
    if enhance_prompt is not None:
        payload["enhance_prompt"] = enhance_prompt
    if images:
        payload["images"] = images
    if aspect_ratio is not None:
        payload["aspect_ratio"] = aspect_ratio

    headers = _session_headers(api_key)
    candidate_paths = [submit_path]
    if submit_path == "auto":
        candidate_paths = [DEFAULT_SUBMIT_PATH, ANYFAST_FALLBACK_SUBMIT_PATH]

    attempt_summaries: List[Dict[str, Any]] = []
    validation_notes = _build_validation_notes(
        model=model,
        prompt=prompt,
        images=images,
        enable_upsample=enable_upsample,
        enhance_prompt=enhance_prompt,
        aspect_ratio=aspect_ratio,
    )

    primary_url = f"{base_url.rstrip('/')}/{candidate_paths[0].lstrip('/')}"
    primary_request_summary = _request_summary(method="POST", url=primary_url, headers=headers, data=payload)
    if print_payload or dry_run:
        print(json.dumps(primary_request_summary, ensure_ascii=False, indent=2))
    if dry_run:
        diagnostic = []
        if api_key == DRY_RUN_API_KEY_PLACEHOLDER:
            diagnostic.append("未提供 API Key，dry-run 使用占位符")
        if base_url == DRY_RUN_BASE_URL_PLACEHOLDER:
            diagnostic.append("未提供 Base URL，dry-run 使用占位符")
        if submit_path == "auto":
            diagnostic.append(
                f"submit_path=auto；将优先尝试 {candidate_paths[0]}，若网关返回 Invalid URL 再回退到 {candidate_paths[1]}"
            )
        return {
            "ok": True,
            "submit_path": candidate_paths[0],
            "request_summary": primary_request_summary,
            "normalized_submit": None,
            "raw_response": None,
            "diagnostic_hint": "；".join(diagnostic) if diagnostic else None,
            "validation_notes": validation_notes,
        }

    final_request_summary = primary_request_summary
    final_response_body: Any = None
    final_status_code: Optional[int] = None
    final_ok = False
    diagnostic_hint: Optional[str] = None

    for idx, candidate_path in enumerate(candidate_paths):
        url = f"{base_url.rstrip('/')}/{candidate_path.lstrip('/')}"
        request_summary = _request_summary(method="POST", url=url, headers=headers, data=payload)
        response = requests.post(url, headers=headers, json=payload, timeout=timeout)
        try:
            body = response.json()
        except ValueError:
            body = {"non_json_response": response.text}

        attempt_summaries.append(
            {
                "submit_path": candidate_path,
                "status_code": response.status_code,
                "ok": response.ok,
                "raw_response": body,
            }
        )
        final_request_summary = request_summary
        final_response_body = body
        final_status_code = response.status_code
        final_ok = response.ok

        if response.ok:
            if idx > 0:
                diagnostic_hint = (
                    f"主路径 {candidate_paths[0]} 返回 Invalid URL，已自动回退到 {candidate_path} 并完成提交。"
                )
            break

        if not (
            submit_path == "auto"
            and idx < len(candidate_paths) - 1
            and _should_retry_with_fallback_path(response.status_code, body)
        ):
            break

        diagnostic_hint = (
            f"主路径 {candidate_path} 返回 Invalid URL，自动回退到 {candidate_paths[idx + 1]} 继续尝试。"
        )

    return {
        "ok": final_ok,
        "submit_path": final_request_summary["url"].replace(base_url.rstrip("/"), "", 1) or candidate_paths[0],
        "request_summary": final_request_summary,
        "attempts": attempt_summaries,
        "normalized_submit": _normalize_submit_response(final_response_body)
        if final_ok and isinstance(final_response_body, dict)
        else None,
        "raw_response": final_response_body,
        "status_code": final_status_code,
        "error": None if final_ok else "创建任务失败",
        "diagnostic_hint": diagnostic_hint,
        "validation_notes": _build_validation_notes(
            model=model,
            prompt=prompt,
            images=images,
            enable_upsample=enable_upsample,
            enhance_prompt=enhance_prompt,
            aspect_ratio=aspect_ratio,
            response_body=final_response_body if isinstance(final_response_body, dict) else None,
        ),
    }


def build_parser() -> argparse.ArgumentParser:
    common_parser = argparse.ArgumentParser(add_help=False)
    common_parser.add_argument("--api-key", help="API Key，不传则读取 .env")
    common_parser.add_argument("--base-url", default=_env_base_url(), help="API 基础 URL；当前必须显式配置")
    common_parser.add_argument("--timeout", type=int, default=DEFAULT_TIMEOUT, help="HTTP 超时秒数")
    common_parser.add_argument("--project-name", default=DEFAULT_PROJECT_NAME, help="项目名，用于默认输出目录")
    common_parser.add_argument("--output-dir", help="覆盖默认输出目录")
    common_parser.add_argument("--filename-prefix", default="veo", help="报告文件名前缀")
    common_parser.add_argument("--report-json", help="显式指定报告 JSON 路径")

    parser = argparse.ArgumentParser(
        description="Submit FineAPI Veo create tasks",
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
    submit_parser.add_argument("--model", default=DEFAULT_MODEL, choices=sorted(ALLOWED_MODELS), help="Veo 模型 ID")
    submit_parser.add_argument(
        "--image",
        dest="images",
        action="append",
        default=[],
        help="图片 URL，可重复传参；当前不支持本地文件直传",
    )
    submit_parser.add_argument(
        "--enable-upsample",
        choices=["true", "false"],
        help="显式发送 enable_upsample；图生页把它写成必填",
    )
    submit_parser.add_argument(
        "--enhance-prompt",
        choices=["true", "false"],
        help="显式发送 enhance_prompt；中文 prompt 建议传 true",
    )
    submit_parser.add_argument(
        "--aspect-ratio",
        choices=sorted(ALLOWED_ASPECT_RATIOS),
        help="仅 veo3* 支持：16:9 / 9:16",
    )
    submit_parser.add_argument(
        "--submit-path",
        default="auto",
        choices=["auto", DEFAULT_SUBMIT_PATH, ANYFAST_FALLBACK_SUBMIT_PATH],
        help="提交路径；auto 会优先尝试 /v1/video/create，若网关返回 Invalid URL 再回退到 /v1/video/generations",
    )
    submit_parser.add_argument("--dry-run", action="store_true")
    submit_parser.add_argument("--print-payload", action="store_true")

    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()

    try:
        allow_missing_env = bool(getattr(args, "dry_run", False) and args.command in {"submit", "create"})
        api_key = _resolve_api_key(args.api_key, allow_missing=allow_missing_env)
        base_url = _resolve_base_url(args.base_url, allow_missing=allow_missing_env)
        output_dir = Path(args.output_dir) if args.output_dir else _default_output_dir(args.project_name)

        if args.command not in {"submit", "create"}:
            raise ValueError(f"不支持的命令: {args.command}")

        result = submit_video(
            prompt=args.prompt,
            model=args.model,
            images=args.images,
            enable_upsample=_parse_bool_optional(args.enable_upsample),
            enhance_prompt=_parse_bool_optional(args.enhance_prompt),
            aspect_ratio=args.aspect_ratio,
            api_key=api_key,
            base_url=base_url,
            submit_path=args.submit_path,
            timeout=args.timeout,
            dry_run=args.dry_run,
            print_payload=args.print_payload,
        )

        result["command"] = "submit"
        report_path = _make_report_path(output_dir, args.filename_prefix, "submit", args.report_json)
        _write_json(report_path, result)
        result["report_json"] = str(report_path)
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 0 if result.get("ok") else 1

    except Exception as exc:
        fallback_output_dir = (
            Path(getattr(args, "output_dir", ""))
            if getattr(args, "output_dir", None)
            else _default_output_dir(getattr(args, "project_name", DEFAULT_PROJECT_NAME))
        )
        error_result = {"ok": False, "command": getattr(args, "command", "unknown"), "error": str(exc)}
        report_path = _make_report_path(
            fallback_output_dir,
            getattr(args, "filename_prefix", "veo"),
            "submit",
            getattr(args, "report_json", None),
        )
        _write_json(report_path, error_result)
        error_result["report_json"] = str(report_path)
        print(json.dumps(error_result, ensure_ascii=False, indent=2))
        return 1


if __name__ == "__main__":
    sys.exit(main())
