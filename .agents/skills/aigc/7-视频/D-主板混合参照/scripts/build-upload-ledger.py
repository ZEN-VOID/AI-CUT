#!/usr/bin/env python3
"""Build and optionally sync hybrid-reference upload and generation-slot ledgers."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any

import yaml


def _load_doc(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    text = path.read_text(encoding="utf-8")
    if path.suffix in {".yaml", ".yml"}:
        return yaml.safe_load(text) or {}
    return json.loads(text)


def _write_doc(path: Path, data: dict[str, Any]) -> None:
    if path.suffix in {".yaml", ".yml"}:
        path.write_text(yaml.safe_dump(data, allow_unicode=True, sort_keys=False), encoding="utf-8")
        return
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def _first_existing(package_dir: Path, names: list[str], pattern: str) -> Path | None:
    for name in names:
        path = package_dir / name
        if path.exists():
            return path
    matches = sorted(package_dir.glob(pattern))
    return matches[0] if matches else None


def _tasks(plan: dict[str, Any]) -> list[dict[str, Any]]:
    values = plan.get("tasks") or plan.get("jobs") or []
    if isinstance(values, list) and values:
        return [item for item in values if isinstance(item, dict)]
    return [plan] if plan else []


def _images(task: dict[str, Any]) -> list[dict[str, Any]]:
    values = task.get("images") or task.get("reference_images") or []
    if values:
        return [item for item in values if isinstance(item, dict)]
    mixed = task.get("mixedList") or task.get("mixed_list") or []
    output: list[dict[str, Any]] = []
    for index, item in enumerate(mixed, start=1):
        if isinstance(item, str):
            output.append({"uploaded_url": item, "reference_index": index})
        elif isinstance(item, dict):
            copied = dict(item)
            copied.setdefault("uploaded_url", copied.get("url", ""))
            copied.setdefault("reference_index", index)
            output.append(copied)
    return output


def _task_value(plan: dict[str, Any], key: str) -> Any:
    tasks = _tasks(plan)
    if not tasks:
        return ""
    return tasks[0].get(key)


def _project_uuid(plan: dict[str, Any]) -> str:
    return str(_task_value(plan, "projectUuid") or "")


def _to_int(value: Any, default: int = 0) -> int:
    try:
        return int(value)
    except (TypeError, ValueError):
        return default


def _identity(image: dict[str, Any], index: int) -> tuple[str, str, str]:
    role = str(image.get("role") or image.get("reference_role") or image.get("type") or "")
    if role in {"storyboard", "storyboard_sheet", "故事板总参照"}:
        return "storyboard_sheet", "故事板总参照", "storyboard"
    name = str(image.get("name") or image.get("yaml_name") or image.get("subject_name") or f"reference-{index}")
    category = str(image.get("category") or image.get("section") or "subject")
    return category, name, "subject"


def _slot_source(plan: dict[str, Any], image: dict[str, Any]) -> str:
    return str(
        image.get("slot_source")
        or image.get("ui_slot_source")
        or _task_value(plan, "slot_source")
        or _task_value(plan, "ui_slot_source")
        or _task_value(plan, "generation_slot_source")
        or "submit_plan_expected_order"
    )


def _images_by_url(images: list[dict[str, Any]]) -> dict[str, dict[str, Any]]:
    return {
        str(image.get("uploaded_url") or image.get("url") or ""): image
        for image in images
        if image.get("uploaded_url") or image.get("url")
    }


def _slot_images(plan: dict[str, Any], manifest: dict[str, Any], errors: list[str]) -> list[dict[str, Any]]:
    tasks = _tasks(plan)
    task = tasks[0] if tasks else {}
    images = _images(task)
    by_url = _images_by_url(images)
    manifest_slots = [
        item for item in manifest.get("generation_slots", [])
        if isinstance(item, dict) and (item.get("uploaded_url") or item.get("url"))
    ]
    if manifest_slots:
        output: list[dict[str, Any]] = []
        for position, slot in enumerate(
            sorted(manifest_slots, key=lambda item: _to_int(item.get("reference_index") or item.get("slot"), 999)),
            start=1,
        ):
            reference_index = _to_int(slot.get("reference_index") or slot.get("slot"), position)
            if reference_index != position:
                errors.append(f"generation_slots reference_index must be contiguous from 1: got {reference_index} at position {position}")
            uploaded_url = str(slot.get("uploaded_url") or slot.get("url") or "")
            merged = dict(by_url.get(uploaded_url, {}))
            merged.update(slot)
            merged["uploaded_url"] = uploaded_url
            merged["reference_index"] = reference_index
            output.append(merged)
        return output

    ordered = sorted(images, key=lambda item: _to_int(item.get("reference_index") or item.get("upload_index"), 999))
    expected = list(range(1, len(ordered) + 1))
    actual = [_to_int(item.get("reference_index") or item.get("upload_index"), index) for index, item in enumerate(ordered, start=1)]
    if actual != expected:
        errors.append(f"fallback reference_index must be contiguous from 1 when generation_slots are absent: expected={expected} actual={actual}")
    return ordered


def _build_slots(plan: dict[str, Any], manifest: dict[str, Any]) -> tuple[list[dict[str, Any]], list[dict[str, Any]], list[str]]:
    asset_uploads: list[dict[str, Any]] = []
    generation_slots: list[dict[str, Any]] = []
    errors: list[str] = []
    project_uuid = _project_uuid(plan)
    ordered = _slot_images(plan, manifest, errors)
    for position, image in enumerate(ordered, start=1):
        uploaded_url = str(image.get("uploaded_url") or image.get("url") or "")
        if not uploaded_url:
            errors.append(f"hybrid slot {position}: missing uploaded_url")
            continue
        category, name, reference_type = _identity(image, position)
        reference_index = _to_int(image.get("reference_index") or image.get("slot"), position)
        if project_uuid and f"/claw/{project_uuid}/" not in uploaded_url:
            errors.append(f"{name}: uploaded_url project scope does not match projectUuid={project_uuid}")
        asset_uploads.append({
            "name": name,
            "yaml_name": "" if reference_type == "storyboard" else name,
            "reference_type": reference_type,
            "category": category,
            "uploaded_url": uploaded_url,
            "path": image.get("path", ""),
            "source_sha256": image.get("source_sha256", ""),
            "projectUuid": project_uuid,
            "identity_lock": f"{reference_type}:{name} -> {uploaded_url}",
        })
        generation_slots.append({
            "slot": reference_index,
            "reference_index": reference_index,
            "mixedList_index": reference_index - 1,
            "image_token": image.get("image_token") or f"{{{{Image {reference_index}}}}}",
            "uploaded_url": uploaded_url,
            "name": name,
            "reference_type": reference_type,
            "category": category,
            "projectUuid": project_uuid,
            "slot_source": _slot_source(plan, image),
            "slot_lock": f"slot={reference_index} mixedList[{reference_index - 1}] {uploaded_url} -> {reference_type}:{name}",
        })
    return asset_uploads, generation_slots, errors


def _rewrite_yaml(text: str, slots: list[dict[str, Any]]) -> str:
    match = re.search(r"```yaml\n(.*?)\n```", text, re.S)
    if not match:
        return text
    data = yaml.safe_load(match.group(1)) or {}
    if not isinstance(data, dict):
        return text
    subject_slots = {slot["name"]: slot for slot in slots if slot.get("reference_type") != "storyboard"}
    storyboard_slots = [slot for slot in slots if slot.get("reference_type") == "storyboard"]
    if storyboard_slots:
        slot = storyboard_slots[0]
        data["故事板参照"] = {
            "name": "故事板总参照",
            "role": "storyboard_sheet",
            "reference_index": slot["reference_index"],
            "uploaded_url": slot["uploaded_url"],
            "image_token": slot["image_token"],
        }
    else:
        data.pop("故事板参照", None)
    for section in ("角色", "场景", "道具"):
        items = data.get(section)
        if not isinstance(items, list):
            continue
        rewritten: list[Any] = []
        for item in items:
            if isinstance(item, dict):
                base = dict(item)
                name = str(base.get("name") or "")
            else:
                name = str(item)
                base = {"name": name}
            slot = subject_slots.get(name)
            if slot:
                base.update({
                    "name": name,
                    "reference_index": slot["reference_index"],
                    "uploaded_url": slot["uploaded_url"],
                    "image_token": slot["image_token"],
                })
                rewritten.append(base)
                continue
            for key in ("reference_index", "uploaded_url", "image_token"):
                base.pop(key, None)
            rewritten.append(base["name"] if set(base) == {"name"} else base)
        data[section] = rewritten
    rendered = yaml.safe_dump(data, allow_unicode=True, sort_keys=False).strip()
    return text[: match.start(1)] + rendered + text[match.end(1) :]


def _rewrite_mixed_list(text: str, slots: list[dict[str, Any]]) -> str:
    mixed = [{"url": slot["uploaded_url"], "type": "image"} for slot in slots]
    replacement = "mixedList: " + json.dumps(mixed, ensure_ascii=False)
    if re.search(r"(?m)^mixedList:\s*\[.*\]\s*$", text):
        return re.sub(r"(?m)^mixedList:\s*\[.*\]\s*$", replacement, text, count=1)
    return text.replace("modeType: mixed2video", "modeType: mixed2video\n" + replacement, 1)


def build(package_dir: Path, *, sync: bool) -> dict[str, Any]:
    plan_path = _first_existing(package_dir, ["libtv-submit-plan.json", "libtv-batch.yaml", "libtv-batch.yml"], "*libtv*.*")
    manifest_path = _first_existing(package_dir, ["reference-manifest.json"], "*reference-manifest.json")
    if not plan_path:
        return {"package_dir": str(package_dir), "verdict": "needs_rework", "errors": ["submit plan/batch not found"], "warnings": []}
    plan = _load_doc(plan_path)
    manifest = _load_doc(manifest_path) if manifest_path else {}
    asset_uploads, generation_slots, errors = _build_slots(plan, manifest)
    if sync and not errors:
        manifest["asset_uploads"] = asset_uploads
        manifest["generation_slots"] = generation_slots
        if manifest_path:
            _write_doc(manifest_path, manifest)
        tasks = _tasks(plan)
        if tasks:
            tasks[0]["asset_uploads"] = asset_uploads
            tasks[0]["generation_slots"] = generation_slots
            tasks[0]["generation_slot_source"] = generation_slots[0]["slot_source"] if generation_slots else ""
        _write_doc(plan_path, plan)
        for prompt_path in sorted(package_dir.glob("*prompt*.md")) + sorted((package_dir / "prompts").glob("*.md")):
            prompt_path.write_text(_rewrite_yaml(prompt_path.read_text(encoding="utf-8"), generation_slots), encoding="utf-8")
        for submission_path in sorted(package_dir.glob("*libtv-submission.txt")) + sorted((package_dir / "prompts").glob("*libtv-submission.txt")):
            text = submission_path.read_text(encoding="utf-8")
            text = _rewrite_mixed_list(_rewrite_yaml(text, generation_slots), generation_slots)
            submission_path.write_text(text, encoding="utf-8")
    return {
        "package_dir": str(package_dir),
        "plan_path": str(plan_path),
        "manifest_path": str(manifest_path) if manifest_path else "",
        "verdict": "pass" if not errors else "needs_rework",
        "asset_uploads": asset_uploads,
        "generation_slots": generation_slots,
        "sync_rule": "generation_slots projects storyboard/subject refs into manifest, plan, prompt YAML, and mixedList",
        "errors": errors,
        "warnings": [],
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("package_dir")
    parser.add_argument("--sync", action="store_true")
    args = parser.parse_args()
    result = build(Path(args.package_dir), sync=args.sync)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result["verdict"] == "pass" else 2


if __name__ == "__main__":
    raise SystemExit(main())
