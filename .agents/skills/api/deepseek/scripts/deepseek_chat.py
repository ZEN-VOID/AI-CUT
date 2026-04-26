#!/usr/bin/env python3
"""
DeepSeek chat CLI.

Features:
- prompt/system convenience mode
- raw messages passthrough
- thinking mode and reasoning effort handling
- JSON Output helper
- SSE streaming support
- dry-run payload validation
- text/report sidecars
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

import requests

try:
    from dotenv import load_dotenv

    try:
        load_dotenv()
    except Exception:
        load_dotenv(dotenv_path=str(Path.cwd() / ".env"))
except ImportError:
    print("缺少依赖: pip install requests python-dotenv", file=sys.stderr)
    sys.exit(1)


DEFAULT_MODEL = "deepseek-v4-pro"
DEFAULT_BASE_URL = "https://api.deepseek.com"
ALLOWED_MODELS = {DEFAULT_MODEL}
REASONING_EFFORT_MAP = {
    "low": "high",
    "medium": "high",
    "high": "high",
    "xhigh": "max",
    "max": "max",
}


def _now_stamp() -> str:
    return datetime.now().strftime("%Y%m%d_%H%M%S")


def _safe_name(text: str, max_len: int = 48) -> str:
    text = re.sub(r"\s+", "_", text.strip())
    text = re.sub(r"[^0-9A-Za-z_\u4e00-\u9fff-]+", "", text)
    return (text or "deepseek")[:max_len]


def _redact(text: str) -> str:
    text = re.sub(r"(Bearer\s+)([A-Za-z0-9._-]+)", r"\1<redacted>", text)
    text = re.sub(r"(api[_-]?key=)([^&\s]+)", r"\1<redacted>", text, flags=re.I)
    text = re.sub(r"(key=)([^&\s]+)", r"\1<redacted>", text, flags=re.I)
    text = re.sub(r"sk-[A-Za-z0-9._-]+", "sk-<redacted>", text)
    return text


def _load_json_text(raw: str, label: str) -> Any:
    try:
        return json.loads(raw)
    except json.JSONDecodeError as exc:
        raise ValueError(f"{label} 不是合法 JSON: {exc}") from exc


def _load_json_file(path: str) -> Any:
    return _load_json_text(Path(path).read_text(encoding="utf-8"), path)


def _env_api_key() -> Optional[str]:
    return os.getenv("DEEPSEEK_API_KEY")


def _env_base_url() -> str:
    return (
        os.getenv("DEEPSEEK_BASE_URL")
        or os.getenv("DEEPSEEK_API_BASE_URL")
        or DEFAULT_BASE_URL
    )


def _normalize_api_url(value: str) -> str:
    clean = value.rstrip("/")
    if clean.endswith("/chat/completions"):
        return clean
    return f"{clean}/chat/completions"


def _normalize_task_kind(value: Optional[str]) -> str:
    normalized = (value or "test").strip().lower()
    if normalized not in {"project", "test", "temp"}:
        return "test"
    return normalized


def _resolve_project_name(project_name: Optional[str], task_kind: str) -> str:
    if project_name:
        return project_name
    if task_kind == "project":
        return "未命名项目"
    if task_kind == "temp":
        return "临时"
    return "测试"


def _default_output_dir(project_name: str) -> Path:
    return Path("output") / "影片" / project_name / "5-API" / "llm" / "deepseek"


def _validate_range(name: str, value: Optional[float], lower: float, upper: float) -> None:
    if value is None:
        return
    if value < lower or value > upper:
        raise ValueError(f"{name} 超出范围，应位于 {lower}..{upper}")


def _normalize_reasoning_effort(value: Optional[str]) -> Tuple[str, Optional[str]]:
    raw = (value or "high").strip().lower()
    if raw not in REASONING_EFFORT_MAP:
        raise ValueError("reasoning_effort 必须是 low / medium / high / xhigh / max 之一")
    normalized = REASONING_EFFORT_MAP[raw]
    if raw != normalized:
        return normalized, f"reasoning_effort={raw} 已按 DeepSeek 兼容规则映射为 {normalized}"
    return normalized, None


def _message_content_to_text(content: Any) -> str:
    if isinstance(content, str):
        return content
    if isinstance(content, list):
        parts: List[str] = []
        for item in content:
            if not isinstance(item, dict):
                continue
            if item.get("type") == "text" and isinstance(item.get("text"), str):
                parts.append(item["text"])
            elif "text" in item and isinstance(item["text"], str):
                parts.append(item["text"])
        return "\n".join(parts).strip()
    if content is None:
        return ""
    return str(content)


def _extract_response_text(choice: Dict[str, Any]) -> str:
    message = choice.get("message") or {}
    content = message.get("content")
    if isinstance(content, list):
        return _message_content_to_text(content)
    if isinstance(content, str):
        return content
    return ""


def _extract_reasoning(choice: Dict[str, Any]) -> str:
    message = choice.get("message") or {}
    reasoning = message.get("reasoning_content")
    if isinstance(reasoning, str):
        return reasoning
    return ""


def _read_sse_payloads(response: requests.Response) -> List[Dict[str, Any]]:
    payloads: List[Dict[str, Any]] = []
    for raw_line in response.iter_lines(decode_unicode=True):
        if not raw_line:
            continue
        line = raw_line.strip()
        if line.startswith("event:"):
            continue
        if line.startswith("data:"):
            line = line[5:].strip()
        if line in {"[DONE]", "DONE"}:
            break
        try:
            payloads.append(json.loads(line))
        except json.JSONDecodeError:
            continue
    return payloads


def _merge_stream_content(payloads: List[Dict[str, Any]]) -> Tuple[str, str, Optional[Dict[str, Any]]]:
    text_parts: List[str] = []
    reasoning_parts: List[str] = []
    last_payload: Optional[Dict[str, Any]] = None

    for payload in payloads:
        last_payload = payload
        for choice in payload.get("choices", []) or []:
            delta = choice.get("delta") or {}
            content = delta.get("content")
            if isinstance(content, str):
                text_parts.append(content)
            reasoning = delta.get("reasoning_content")
            if isinstance(reasoning, str):
                reasoning_parts.append(reasoning)

    final_text = "".join(text_parts).strip()
    final_reasoning = "".join(reasoning_parts).strip()

    if (not final_text or not final_reasoning) and isinstance(last_payload, dict):
        choices = last_payload.get("choices", []) or []
        if choices:
            if not final_text:
                final_text = _extract_response_text(choices[0]).strip()
            if not final_reasoning:
                final_reasoning = _extract_reasoning(choices[0]).strip()

    return final_text, final_reasoning, last_payload


def _message_has_required_content(item: Dict[str, Any]) -> bool:
    role = item.get("role")
    content = item.get("content")
    if role in {"system", "user", "tool"}:
        return content is not None and content != ""
    if role == "assistant":
        return (content is not None and content != "") or bool(item.get("tool_calls")) or bool(item.get("reasoning_content"))
    return False


def _build_messages(
    prompt: Optional[str],
    system: Optional[str],
    payload_input: Dict[str, Any],
    messages_json: Optional[str],
    messages_file: Optional[str],
) -> List[Dict[str, Any]]:
    if messages_json:
        messages = _load_json_text(messages_json, "messages_json")
    elif messages_file:
        messages = _load_json_file(messages_file)
    elif "messages" in payload_input:
        messages = payload_input["messages"]
    else:
        messages = []
        if system:
            messages.append({"role": "system", "content": system})
        if prompt:
            messages.append({"role": "user", "content": prompt})

    if not isinstance(messages, list) or not messages:
        raise ValueError("缺少合法 messages。请提供 prompt，或通过 messages_json/messages_file/input_json.messages 传入。")

    normalized: List[Dict[str, Any]] = []
    for i, item in enumerate(messages):
        if not isinstance(item, dict):
            raise ValueError(f"messages[{i}] 必须是对象")
        role = item.get("role")
        if role not in {"system", "user", "assistant", "tool"}:
            raise ValueError(f"messages[{i}].role 非法: {role}")
        if role == "tool" and not item.get("tool_call_id"):
            raise ValueError(f"messages[{i}].tool_call_id 不能为空")
        if not _message_has_required_content(item):
            raise ValueError(f"messages[{i}] 缺少该角色所需 content/reasoning/tool_calls")
        normalized.append(item)
    return normalized


def _has_json_instruction(messages: List[Dict[str, Any]]) -> bool:
    for item in messages:
        text = _message_content_to_text(item.get("content"))
        if "json" in text.lower():
            return True
    return False


def _normalize_stop(value: Any) -> Optional[List[str]]:
    if value is None:
        return None
    if isinstance(value, str):
        return [value]
    if isinstance(value, list) and all(isinstance(item, str) for item in value):
        return value
    raise ValueError("stop 必须是字符串或字符串数组")


@dataclass
class RunConfig:
    api_key: str
    api_url: str
    timeout: int


class DeepSeekClient:
    def __init__(self, cfg: RunConfig):
        self.cfg = cfg
        self.headers = {
            "Authorization": f"Bearer {cfg.api_key}",
            "Content-Type": "application/json",
        }

    def create_chat_completion(
        self, payload: Dict[str, Any], stream: bool
    ) -> Tuple[List[Dict[str, Any]], Optional[Dict[str, Any]]]:
        if stream:
            with requests.post(
                self.cfg.api_url,
                headers=self.headers,
                json=payload,
                stream=True,
                timeout=self.cfg.timeout,
            ) as resp:
                try:
                    resp.raise_for_status()
                except requests.HTTPError as exc:
                    raise RuntimeError(_redact(f"HTTP {resp.status_code}: {resp.text}")) from exc
                payloads = _read_sse_payloads(resp)
                return payloads, (payloads[-1] if payloads else None)

        resp = requests.post(
            self.cfg.api_url,
            headers=self.headers,
            json=payload,
            timeout=self.cfg.timeout,
        )
        try:
            resp.raise_for_status()
        except requests.HTTPError as exc:
            raise RuntimeError(_redact(f"HTTP {resp.status_code}: {resp.text}")) from exc
        body = resp.json()
        return [body], body


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="DeepSeek chat CLI")
    parser.add_argument("--prompt", help="用户提示词")
    parser.add_argument("--system", help="system 提示词")
    parser.add_argument("--messages-json", help="JSON 字符串格式的 messages")
    parser.add_argument("--messages-file", help="JSON 文件格式的 messages")
    parser.add_argument("--input-json", help="输入 JSON 文件，支持 messages/model/params/output_dir")

    parser.add_argument("--api-key", help="DeepSeek API Key；不传则读取 DEEPSEEK_API_KEY")
    parser.add_argument("--api-url", help="完整 API URL；不传则根据 base URL 组装")
    parser.add_argument("--model", help=f"模型名，默认 {DEFAULT_MODEL}")
    parser.add_argument(
        "--thinking",
        choices=["enabled", "disabled"],
        default=None,
        help="思考模式开关，默认 enabled",
    )
    parser.add_argument(
        "--reasoning-effort",
        choices=["low", "medium", "high", "xhigh", "max"],
        help="推理强度，发送前映射为 high/max",
    )
    parser.add_argument("--max-tokens", type=int, help="最大生成 token")
    parser.add_argument("--temperature", type=float, help="采样温度，0..2；思考模式下不生效")
    parser.add_argument("--top-p", type=float, help="核采样阈值，0..1；思考模式下不生效")
    parser.add_argument("--frequency-penalty", type=float, help="频率惩罚，-2..2；思考模式下不生效")
    parser.add_argument("--presence-penalty", type=float, help="存在惩罚，-2..2；思考模式下不生效")
    parser.add_argument("--json-output", action="store_true", help="设置 response_format={\"type\":\"json_object\"}")
    parser.add_argument("--stop", action="append", default=None, help="停止序列，可重复传入，最多 16 条")
    parser.add_argument(
        "--stream",
        action=argparse.BooleanOptionalAction,
        default=None,
        help="是否启用流式输出",
    )
    parser.add_argument("--stream-include-usage", action="store_true", help="流式输出最后额外返回 usage")
    parser.add_argument("--timeout", type=int, default=180, help="请求超时时间（秒）")
    parser.add_argument("--extra-json", help="额外顶层 JSON 字段")

    parser.add_argument("--project-name", help="项目名")
    parser.add_argument("--task-kind", choices=["project", "test", "temp"], help="任务类型")
    parser.add_argument("--output-dir", help="输出目录")
    parser.add_argument("--filename-prefix", default="deepseek", help="输出文件名前缀")
    parser.add_argument("--text-output", help="显式文本输出文件路径")
    parser.add_argument("--report-json", help="显式报告 JSON 路径")
    parser.add_argument("--no-save-text", action="store_true", help="不保存文本 sidecar")
    parser.add_argument("--no-report", action="store_true", help="不保存报告 JSON")
    parser.add_argument("--print-reasoning", action="store_true", help="控制台额外打印 reasoning_content")

    parser.add_argument("--dry-run", action="store_true", help="只生成 payload，不发请求")
    parser.add_argument("--print-payload", action="store_true", help="打印最终 payload")
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()

    payload_input: Dict[str, Any] = {}
    if args.input_json:
        loaded = _load_json_file(args.input_json)
        if not isinstance(loaded, dict):
            print("input-json 必须是 JSON 对象", file=sys.stderr)
            return 1
        payload_input = loaded

    try:
        messages = _build_messages(
            prompt=args.prompt or payload_input.get("prompt"),
            system=args.system or payload_input.get("system"),
            payload_input=payload_input,
            messages_json=args.messages_json,
            messages_file=args.messages_file,
        )

        model = args.model or payload_input.get("model") or DEFAULT_MODEL
        if model not in ALLOWED_MODELS:
            raise ValueError("本技能固定使用 deepseek-v4-pro，不支持覆盖为其他 model")

        thinking = args.thinking or payload_input.get("thinking", "enabled")
        if isinstance(thinking, dict):
            thinking_type = thinking.get("type", "enabled")
        else:
            thinking_type = str(thinking)
        if thinking_type not in {"enabled", "disabled"}:
            raise ValueError("thinking 必须是 enabled 或 disabled")

        effort: Optional[str] = None
        effort_warning: Optional[str] = None
        compatibility_warnings: List[str] = []
        if thinking_type == "enabled":
            effort, effort_warning = _normalize_reasoning_effort(
                args.reasoning_effort or payload_input.get("reasoning_effort")
            )
        elif args.reasoning_effort or payload_input.get("reasoning_effort"):
            compatibility_warnings.append("thinking=disabled 时不会发送 reasoning_effort")
        max_tokens = args.max_tokens if args.max_tokens is not None else payload_input.get("max_tokens")
        temperature = args.temperature if args.temperature is not None else payload_input.get("temperature")
        top_p = args.top_p if args.top_p is not None else payload_input.get("top_p")
        frequency_penalty = (
            args.frequency_penalty
            if args.frequency_penalty is not None
            else payload_input.get("frequency_penalty")
        )
        presence_penalty = (
            args.presence_penalty
            if args.presence_penalty is not None
            else payload_input.get("presence_penalty")
        )
        stop = _normalize_stop(args.stop if args.stop is not None else payload_input.get("stop"))
        stream = args.stream if args.stream is not None else payload_input.get("stream", False)

        _validate_range("temperature", temperature, 0, 2)
        _validate_range("top_p", top_p, 0, 1)
        _validate_range("frequency_penalty", frequency_penalty, -2, 2)
        _validate_range("presence_penalty", presence_penalty, -2, 2)
        if max_tokens is not None and max_tokens < 1:
            raise ValueError("max_tokens 必须 >= 1")
        if stop is not None and len(stop) > 16:
            raise ValueError("stop 最多允许 16 条")

        if effort_warning:
            compatibility_warnings.append(effort_warning)

        sampling_fields = {
            "temperature": temperature,
            "top_p": top_p,
            "frequency_penalty": frequency_penalty,
            "presence_penalty": presence_penalty,
        }
        if thinking_type == "enabled":
            for name, value in sampling_fields.items():
                if value is not None:
                    compatibility_warnings.append(f"thinking=enabled 时 {name} 会被 DeepSeek 兼容忽略")

        if args.json_output or payload_input.get("json_output"):
            if not _has_json_instruction(messages):
                compatibility_warnings.append("JSON Output 要求 system 或 user prompt 中包含 json 字样")

        api_key = args.api_key or payload_input.get("api_key") or _env_api_key()
        if not api_key:
            raise ValueError("缺少 API Key。请设置 DEEPSEEK_API_KEY，或显式传入 --api-key。")

        api_url_source = args.api_url or payload_input.get("api_url") or _env_base_url()
        api_url = _normalize_api_url(api_url_source)

        extra_json: Dict[str, Any] = {}
        if payload_input.get("extra_json") and isinstance(payload_input["extra_json"], dict):
            extra_json.update(payload_input["extra_json"])
        if args.extra_json:
            extra_loaded = _load_json_text(args.extra_json, "extra_json")
            if not isinstance(extra_loaded, dict):
                raise ValueError("extra_json 必须是 JSON 对象")
            extra_json.update(extra_loaded)

        payload: Dict[str, Any] = {
            "model": model,
            "messages": messages,
            "thinking": {"type": thinking_type},
            "stream": bool(stream),
        }
        if effort:
            payload["reasoning_effort"] = effort
        if max_tokens is not None:
            payload["max_tokens"] = max_tokens
        for name, value in sampling_fields.items():
            if value is not None:
                payload[name] = value
        if args.json_output or payload_input.get("json_output"):
            payload["response_format"] = {"type": "json_object"}
        if stop:
            payload["stop"] = stop
        if args.stream_include_usage or payload_input.get("stream_include_usage"):
            payload["stream_options"] = {"include_usage": True}
        payload.update(extra_json)

        if args.print_payload:
            print(json.dumps(payload, ensure_ascii=False, indent=2))

        task_kind = _normalize_task_kind(args.task_kind or payload_input.get("task_kind"))
        project_name = _resolve_project_name(args.project_name or payload_input.get("project_name"), task_kind)
        output_dir = Path(args.output_dir or payload_input.get("output_dir") or _default_output_dir(project_name))
        stamp = _now_stamp()
        prefix = _safe_name(args.filename_prefix or "deepseek")

        text_output = Path(args.text_output) if args.text_output else output_dir / f"{prefix}_{stamp}.txt"
        report_json = Path(args.report_json) if args.report_json else output_dir / f"{prefix}_report_{stamp}.json"

        if args.dry_run:
            return 0

        output_dir.mkdir(parents=True, exist_ok=True)
        client = DeepSeekClient(RunConfig(api_key=api_key, api_url=api_url, timeout=args.timeout))

        payloads, final_payload = client.create_chat_completion(payload, stream=bool(stream))
        if stream:
            response_text, reasoning_content, final_payload = _merge_stream_content(payloads)
        else:
            choices = (final_payload or {}).get("choices", []) if isinstance(final_payload, dict) else []
            response_text = _extract_response_text(choices[0]) if choices else ""
            reasoning_content = _extract_reasoning(choices[0]) if choices else ""

        usage = (final_payload or {}).get("usage") if isinstance(final_payload, dict) else None
        finish_reason = None
        if isinstance(final_payload, dict):
            choices = final_payload.get("choices", []) or []
            if choices:
                finish_reason = choices[0].get("finish_reason")

        saved_files: List[str] = []
        if not args.no_save_text:
            text_output.write_text(response_text or "", encoding="utf-8")
            saved_files.append(str(text_output))

        if not args.no_report:
            saved_files.append(str(report_json))

        report = {
            "ok": True,
            "api_url": api_url,
            "request_summary": {
                "model": model,
                "message_count": len(messages),
                "thinking": thinking_type,
                "reasoning_effort": effort,
                "stream": bool(stream),
                "max_tokens": max_tokens,
                "temperature": temperature,
                "top_p": top_p,
                "frequency_penalty": frequency_penalty,
                "presence_penalty": presence_penalty,
                "json_output": bool(args.json_output or payload_input.get("json_output")),
                "stop": stop or [],
                "project_name": project_name,
                "task_kind": task_kind,
            },
            "compatibility_warnings": compatibility_warnings,
            "response_text": response_text,
            "reasoning_content": reasoning_content,
            "usage": usage,
            "finish_reason": finish_reason,
            "stream_event_count": len(payloads) if stream else 0,
            "saved_files": saved_files,
            "error": None,
        }

        if not args.no_report:
            report_json.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")

        if args.print_reasoning and reasoning_content:
            print(reasoning_content)
            print()
        if response_text:
            print(response_text)
        else:
            print("[empty response]")
        return 0

    except Exception as exc:
        message = _redact(str(exc))
        print(f"错误: {message}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
