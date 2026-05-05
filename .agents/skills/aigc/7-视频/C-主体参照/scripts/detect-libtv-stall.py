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

    for message in messages:
        role = message.get("role") or message.get("senderType") or message.get("type")
        content = _content(message)
        video_urls.extend(VIDEO_URL_RE.findall(content))
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
        if "create_generation_task" in content or "generation_task" in content:
            generation_markers.append("content:generation_task")

    if video_urls:
        verdict = "generated"
        local_status = "download_ready"
        remote_status = "video_url_available"
    elif ask_user_calls or wait_messages:
        verdict = "stalled_remote_ask_user"
        local_status = "stalled_remote_ask_user"
        remote_status = "no_generation_node"
    elif tool_errors:
        verdict = "generation_tool_error"
        local_status = "generation_tool_error"
        remote_status = "generation_tool_failed"
    elif generation_markers:
        verdict = "submitted"
        local_status = "pending_remote_generation"
        remote_status = "generation_node_seen"
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
        "ask_user_calls": len(ask_user_calls),
        "wait_messages": wait_messages,
        "generation_markers": generation_markers,
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
    return 2 if result["verdict"] in {"stalled_remote_ask_user", "generation_tool_error"} else 0


if __name__ == "__main__":
    raise SystemExit(main())
