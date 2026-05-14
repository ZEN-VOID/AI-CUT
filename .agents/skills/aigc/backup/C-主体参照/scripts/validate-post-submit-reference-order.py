#!/usr/bin/env python3
"""Validate remote LibTV generation params preserve YAML reference order."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any


def _parse_jsonish(value: Any) -> Any:
    if not isinstance(value, str):
        return value
    try:
        return json.loads(value)
    except json.JSONDecodeError:
        return value


def _generation_calls(query_data: dict[str, Any]) -> list[dict[str, Any]]:
    calls: list[dict[str, Any]] = []
    for message in query_data.get("messages") or []:
        for call in message.get("toolCalls") or message.get("tool_calls") or []:
            function = call.get("function") or {}
            name = function.get("name") or call.get("name")
            if name != "create_generation_task":
                continue
            args = _parse_jsonish(function.get("arguments", call.get("arguments", {})))
            if not isinstance(args, dict):
                calls.append({"args": {}, "params": {}, "args_parse_error": True})
                continue
            params = _parse_jsonish(args.get("params", {}))
            params_parse_error = bool(args.get("params")) and not isinstance(params, dict)
            if not isinstance(params, dict):
                params = {}
            calls.append({
                "args": args,
                "params": params,
                "args_parse_error": False,
                "params_parse_error": params_parse_error,
            })
    return calls


def _load_json(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))


def _to_int(value: Any, default: int = 0) -> int:
    try:
        return int(value)
    except (TypeError, ValueError):
        return default


def _ordered_images(plan: dict[str, Any]) -> list[dict[str, Any]]:
    tasks = plan.get("tasks") or []
    if not tasks:
        return []
    images = [item for item in tasks[0].get("images", []) if isinstance(item, dict)]
    return sorted(images, key=lambda item: _to_int(item.get("reference_index") or item.get("upload_index")))


def _expected_slots_from_registry(manifest: dict[str, Any], plan: dict[str, Any]) -> list[dict[str, Any]]:
    slots = [item for item in manifest.get("generation_slots", []) if isinstance(item, dict)]
    if slots:
        expected: list[dict[str, Any]] = []
        for fallback_position, slot in enumerate(slots, start=1):
            reference_index = _to_int(slot.get("reference_index") or slot.get("slot") or slot.get("ui_slot_index"), fallback_position)
            expected.append({
                "slot": _to_int(slot.get("slot"), reference_index),
                "name": slot.get("name", ""),
                "category": slot.get("category", ""),
                "reference_index": reference_index,
                "upload_index": reference_index,
                "mixedList_index": _to_int(slot.get("mixedList_index"), reference_index - 1),
                "portrait_token": slot.get("portrait_token") or f"{{{{Portrait {reference_index}}}}}",
                "image_token": slot.get("image_token") or f"{{{{Image {reference_index}}}}}",
                "uploaded_url": slot.get("uploaded_url", ""),
                "slot_source": "reference-manifest.generation_slots",
                "slot_lock": (
                    f"{slot.get('name', '')} reference_index={reference_index} "
                    f"mixedList[{reference_index - 1}] {slot.get('uploaded_url', '')}"
                ),
            })
        return sorted(expected, key=lambda item: _to_int(item.get("reference_index")))

    return _expected_slots(_ordered_images(plan))


def _mixed_urls(params: dict[str, Any]) -> list[str]:
    mixed = params.get("mixedList") or params.get("imageList") or []
    urls: list[str] = []
    if not isinstance(mixed, list):
        return urls
    for item in mixed:
        if isinstance(item, dict) and item.get("url"):
            urls.append(str(item["url"]))
        elif isinstance(item, str):
            urls.append(item)
    return urls


def _expected_slots(images: list[dict[str, Any]]) -> list[dict[str, Any]]:
    slots: list[dict[str, Any]] = []
    for position, image in enumerate(images, start=1):
        reference_index = int(image.get("reference_index") or image.get("upload_index") or position)
        slots.append({
            "slot": position,
            "name": image.get("name", ""),
            "category": image.get("category", ""),
            "reference_index": reference_index,
            "upload_index": int(image.get("upload_index") or reference_index),
            "mixedList_index": position - 1,
            "portrait_token": f"{{{{Portrait {position}}}}}",
            "image_token": f"{{{{Image {position}}}}}",
            "uploaded_url": image.get("uploaded_url", ""),
            "slot_lock": (
                f"{image.get('name', '')} reference_index={reference_index} "
                f"mixedList[{position - 1}] {image.get('uploaded_url', '')}"
            ),
        })
    return slots


def _subject_binding_present(prompt: str, image: dict[str, Any], position: int) -> bool:
    name = re.escape(str(image.get("name", "")))
    if not name:
        return False
    reference_index = int(image.get("reference_index") or image.get("upload_index") or position)
    url = re.escape(str(image.get("uploaded_url", "")))
    # Accept either raw uploaded_url adjacency or LibTV's normalized "uploaded_url对应mixedList[n]" projection.
    same_segment = re.compile(
        rf"{name}[\s\S]{{0,180}}reference_index\s*[=:：]?\s*{reference_index}"
        rf"[\s\S]{{0,260}}(?:{url}|mixedList\[{position - 1}\]|Portrait\s*{position}|Image\s*{position}|图片\s*{position})",
        re.I,
    )
    reverse_segment = re.compile(
        rf"(?:{url}|mixedList\[{position - 1}\]|Portrait\s*{position}|Image\s*{position}|图片\s*{position})"
        rf"[\s\S]{{0,260}}{name}[\s\S]{{0,180}}reference_index\s*[=:：]?\s*{reference_index}",
        re.I,
    )
    return bool(same_segment.search(prompt) or reverse_segment.search(prompt))


def validate(package_dir: Path, query_json: Path) -> dict[str, Any]:
    manifest = _load_json(package_dir / "reference-manifest.json")
    plan = _load_json(package_dir / "libtv-submit-plan.json")
    query = _load_json(query_json)
    expected_slots = _expected_slots_from_registry(manifest, plan)
    expected_urls = [str(item.get("uploaded_url")) for item in expected_slots if item.get("uploaded_url")]
    errors: list[str] = []
    warnings: list[str] = []

    calls = _generation_calls(query)
    if not expected_urls:
        return {
            "package_dir": str(package_dir),
            "query_json": str(query_json),
            "verdict": "pass",
            "reason": "no reference images in generation slot registry or submit plan",
            "expected_slots": expected_slots,
            "errors": [],
            "warnings": [],
        }
    if not calls:
        return {
            "package_dir": str(package_dir),
            "query_json": str(query_json),
            "verdict": "pending",
            "reason": "create_generation_task not observed yet",
            "expected_slots": expected_slots,
            "errors": [],
            "warnings": ["remote generation params unavailable"],
        }

    latest = calls[-1]
    params = latest.get("params") or {}
    if latest.get("args_parse_error") or latest.get("params_parse_error"):
        errors.append("create_generation_task arguments or params could not be parsed as JSON")
    mode_type = params.get("modeType") or latest.get("args", {}).get("modeType")
    if mode_type != "mixed2video":
        errors.append(f"remote modeType must be mixed2video for subject references, got {mode_type!r}")

    actual_urls = _mixed_urls(params)
    if actual_urls != expected_urls:
        errors.append(
            "remote mixedList/imageList order does not match generation slot registry order: "
            f"expected={expected_urls} actual={actual_urls}"
        )

    prompt = str(params.get("prompt", ""))
    if not prompt:
        errors.append("remote create_generation_task.params.prompt is empty or missing")
    else:
        for position, slot in enumerate(expected_slots, start=1):
            if not _subject_binding_present(prompt, slot, position):
                errors.append(
                    "remote prompt lacks adjacent subject binding: "
                    f"name={slot.get('name')} reference_index={slot.get('reference_index') or slot.get('upload_index')} "
                    f"position={position}"
                )

    return {
        "package_dir": str(package_dir),
        "query_json": str(query_json),
        "verdict": "pass" if not errors else "needs_rework",
        "checked_call_count": len(calls),
        "expected_slots": expected_slots,
        "expected_urls": expected_urls,
        "actual_urls": actual_urls if calls else [],
        "errors": errors,
        "warnings": warnings,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("package_dir", help="Group package directory containing libtv-submit-plan.json")
    parser.add_argument("query_json", help="query_session JSON captured after create_session")
    args = parser.parse_args()
    result = validate(Path(args.package_dir), Path(args.query_json))
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result["verdict"] in {"pass", "pending"} else 2


if __name__ == "__main__":
    raise SystemExit(main())
