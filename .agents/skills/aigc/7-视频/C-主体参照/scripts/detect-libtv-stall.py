#!/usr/bin/env python3
"""Detect LibTV Agent-IM post-submit stalls from query_session JSON."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any


VIDEO_URL_RE = re.compile(r"https?://[^\s)\"']+\.(?:mp4|mov|webm)(?:\?[^\s)\"']*)?", re.I)
WAIT_RE = re.compile(r"(等待用户|等待.*下一条消息|请稍候|请将上述 question|展示给用户)", re.I)
AUDIO_URL_RE = re.compile(r"https?://[^\s)\"']+\.(?:mp3|wav|m4a|aac|flac|ogg)(?:\?[^\s)\"']*)?", re.I)
STRING_FIELD_RE_TEMPLATE = r'"{key}"\s*:\s*"([^"]*)"'


def _parse_jsonish(value: Any) -> Any:
    if not isinstance(value, str):
        return value
    try:
        return json.loads(value)
    except json.JSONDecodeError:
        return value


def _walk(value: Any):
    yield value
    if isinstance(value, dict):
        for child in value.values():
            yield from _walk(child)
    elif isinstance(value, list):
        for child in value:
            yield from _walk(child)


def _enabled(value: Any) -> bool:
    if value is True:
        return True
    if isinstance(value, (int, float)) and value == 1:
        return True
    if isinstance(value, str):
        return value.strip().lower() in {"on", "true", "1", "yes", "enabled", "enable"}
    return False


def _extract_string_field(raw: Any, key: str) -> str | None:
    if not isinstance(raw, str):
        return None
    match = re.search(STRING_FIELD_RE_TEMPLATE.format(key=re.escape(key)), raw)
    if not match:
        return None
    return match.group(1)


def _extract_generation_call(call: dict[str, Any]) -> dict[str, Any] | None:
    function = call.get("function") or {}
    name = function.get("name") or call.get("name")
    if name != "create_generation_task":
        return None
    raw_args = function.get("arguments", call.get("arguments", {}))
    args = _parse_jsonish(raw_args)
    if not isinstance(args, dict):
        return {"name": name, "raw_args": raw_args, "args_parse_error": True}
    raw_params = args.get("params", {})
    params = _parse_jsonish(raw_params)
    params_parse_error = bool(raw_params) and not isinstance(params, dict)
    if not isinstance(params, dict):
        params = {}
    enable_sound = params.get("enableSound")
    mode_type = params.get("modeType")
    if enable_sound is None:
        enable_sound = _extract_string_field(raw_params, "enableSound")
    if mode_type is None:
        mode_type = _extract_string_field(raw_params, "modeType")
    return {
        "name": name,
        "args": args,
        "params": params,
        "uses_task_type": "task_type" in args,
        "uses_taskType": "taskType" in args,
        "params_was_string": isinstance(raw_params, str),
        "params_parse_error": params_parse_error,
        "enableSound": enable_sound,
        "modeType": mode_type,
    }


def _content(message: dict[str, Any]) -> str:
    value = message.get("content") or message.get("text") or ""
    if isinstance(value, str):
        return value
    return json.dumps(value, ensure_ascii=False)


def detect(data: dict[str, Any]) -> dict[str, Any]:
    messages = data.get("messages") or []
    roles = [m.get("role") or m.get("senderType") or m.get("type") for m in messages]
    video_urls: list[str] = []
    ask_user_calls: list[dict[str, Any]] = []
    wait_messages: list[str] = []
    generation_markers: list[str] = []
    tool_errors: list[str] = []
    generation_calls: list[dict[str, Any]] = []
    audio_urls: list[str] = []
    audio_lists: list[list[Any]] = []

    for message in messages:
        role = message.get("role") or message.get("senderType") or message.get("type")
        content = _content(message)
        video_urls.extend(VIDEO_URL_RE.findall(content))
        audio_urls.extend(AUDIO_URL_RE.findall(content))
        if role != "user" and WAIT_RE.search(content):
            wait_messages.append(content[:500])
        if role == "tool" and ("error" in content.lower() or "isError" in content):
            tool_errors.append(content[:500])
        for call in message.get("toolCalls") or message.get("tool_calls") or []:
            function = call.get("function") or {}
            name = function.get("name") or call.get("name")
            if name == "ask_user":
                ask_user_calls.append(call)
            if name and ("generation" in name or "video" in name or "task" in name):
                generation_markers.append(name)
            generation_call = _extract_generation_call(call)
            if generation_call:
                generation_calls.append(generation_call)
        if role != "user" and ("create_generation_task" in content or "generation_task" in content):
            generation_markers.append("content:generation_task")

    for node in _walk(data):
        if isinstance(node, dict):
            for key, value in node.items():
                if key == "audios" and isinstance(value, list):
                    audio_lists.append(value)
                elif isinstance(value, str):
                    audio_urls.extend(AUDIO_URL_RE.findall(value))

    generation_tool_errors = [
        call for call in generation_calls
        if call.get("args_parse_error")
    ]
    generation_envelope_variants = [
        call for call in generation_calls
        if call.get("uses_task_type") or call.get("params_was_string") or call.get("params_parse_error")
    ]
    audio_preflight_failures = [
        call for call in generation_calls
        if not _enabled(call.get("enableSound"))
    ]

    if ask_user_calls or wait_messages:
        verdict = "stalled_remote_ask_user"
        local_status = "stalled_remote_ask_user"
        remote_status = "no_generation_node"
    elif tool_errors or generation_tool_errors:
        verdict = "generation_tool_error"
        local_status = "generation_tool_error"
        remote_status = "generation_tool_failed"
    elif generation_calls and audio_preflight_failures:
        verdict = "submitted_audio_preflight_unverified"
        local_status = "pending_remote_generation"
        remote_status = "generation_node_seen_audio_preflight_unverified"
    elif video_urls and audio_lists and not any(audio_lists) and not audio_urls:
        verdict = "audio_missing"
        local_status = "audio_missing"
        remote_status = "video_url_available_but_no_audio_result"
    elif video_urls and not audio_urls and not any(audio_lists):
        verdict = "audio_unverified"
        local_status = "audio_unverified"
        remote_status = "video_url_available_audio_not_verified"
    elif video_urls:
        verdict = "generated"
        local_status = "download_ready"
        remote_status = "video_url_available"
    elif generation_markers:
        verdict = "submitted"
        local_status = "pending_remote_generation"
        remote_status = "generation_node_seen_envelope_variant" if generation_envelope_variants else "generation_node_seen"
    else:
        verdict = "unknown_pending"
        local_status = "pending_remote_generation_unverified"
        remote_status = "no_generation_marker_seen"

    return {
        "verdict": verdict,
        "local_status": local_status,
        "remote_status": remote_status,
        "messages_count": len(messages),
        "roles": roles,
        "video_urls": video_urls,
        "audio_urls": audio_urls,
        "audio_lists_count": len(audio_lists),
        "ask_user_calls": len(ask_user_calls),
        "wait_messages": wait_messages,
        "generation_markers": generation_markers,
        "generation_calls": generation_calls,
        "generation_envelope_variants_count": len(generation_envelope_variants),
        "tool_errors": tool_errors,
        "projectUrl": data.get("projectUrl", ""),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("query_json", nargs="?", help="Path to query_session JSON; reads stdin when omitted.")
    args = parser.parse_args()

    if args.query_json:
        data = json.loads(Path(args.query_json).read_text(encoding="utf-8"))
    else:
        data = json.load(sys.stdin)

    result = detect(data)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    failure_verdicts = {
        "stalled_remote_ask_user",
        "generation_tool_error",
        "audio_missing",
        "audio_unverified",
    }
    return 2 if result["verdict"] in failure_verdicts else 0


if __name__ == "__main__":
    raise SystemExit(main())
