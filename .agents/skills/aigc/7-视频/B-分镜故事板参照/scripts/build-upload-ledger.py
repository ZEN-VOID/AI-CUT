#!/usr/bin/env python3
"""Build and optionally sync storyboard-reference upload and generation-slot ledgers."""

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


def _task_value(plan: dict[str, Any], key: str) -> Any:
    tasks = _tasks(plan)
    if not tasks:
        return ""
    return tasks[0].get(key)


def _project_uuid(plan: dict[str, Any]) -> str:
    return str(_task_value(plan, "projectUuid") or "")


def _storyboard_image(task: dict[str, Any]) -> dict[str, Any] | None:
    for key in ("images", "reference_images"):
        values = task.get(key) or []
        if values and isinstance(values[0], dict):
            return values[0]
    image_list = task.get("imageList") or task.get("image_list") or []
    if image_list:
        first = image_list[0]
        if isinstance(first, str):
            return {"uploaded_url": first}
        if isinstance(first, dict):
            copied = dict(first)
            copied.setdefault("uploaded_url", copied.get("url", ""))
            return copied
    return None


def _manifest_storyboard_slot(manifest: dict[str, Any]) -> dict[str, Any]:
    for item in manifest.get("generation_slots", []):
        if isinstance(item, dict) and (item.get("uploaded_url") or item.get("url")):
            return item
    return {}


def _build_slots(plan: dict[str, Any], manifest: dict[str, Any]) -> tuple[list[dict[str, Any]], list[dict[str, Any]], list[str]]:
    tasks = _tasks(plan)
    task = tasks[0] if tasks else {}
    group_id = str(task.get("group_id") or plan.get("group_id") or "")
    image = _storyboard_image(task) or {}
    manifest_slot = _manifest_storyboard_slot(manifest)
    if manifest_slot:
        merged = dict(image)
        merged.update(manifest_slot)
        image = merged
    if not image:
        return [], [], []
    uploaded_url = str(image.get("uploaded_url") or image.get("url") or "")
    if not uploaded_url:
        return [], [], ["storyboard image missing uploaded_url"]
    project_uuid = _project_uuid(plan)
    errors: list[str] = []
    if project_uuid and f"/claw/{project_uuid}/" not in uploaded_url:
        errors.append(f"故事板总参照: uploaded_url project scope does not match projectUuid={project_uuid}")
    storyboard_uploads = [{
        "group_id": group_id,
        "name": "故事板总参照",
        "role": "storyboard_sheet",
        "uploaded_url": uploaded_url,
        "path": image.get("path", ""),
        "source_sha256": image.get("source_sha256", ""),
        "projectUuid": project_uuid,
        "identity_lock": f"{group_id}/storyboard_sheet -> {uploaded_url}",
    }]
    reference_index = int(image.get("reference_index") or image.get("slot") or 1)
    if reference_index != 1:
        errors.append(f"故事板总参照: generation_slots reference_index must be 1, got {reference_index}")
    generation_slots = [{
        "slot": reference_index,
        "reference_index": reference_index,
        "imageList_index": reference_index - 1,
        "image_token": image.get("image_token") or f"{{{{Image {reference_index}}}}}",
        "uploaded_url": uploaded_url,
        "name": "故事板总参照",
        "role": "storyboard_sheet",
        "group_id": group_id,
        "projectUuid": project_uuid,
        "slot_source": image.get("slot_source") or task.get("generation_slot_source") or "submit_plan_expected_order",
        "slot_lock": f"slot={reference_index} imageList[{reference_index - 1}] {uploaded_url} -> 故事板总参照",
    }]
    return storyboard_uploads, generation_slots, errors


def _rewrite_yaml(text: str, slots: list[dict[str, Any]]) -> str:
    match = re.search(r"```yaml\n(.*?)\n```", text, re.S)
    if not match:
        return text
    data = yaml.safe_load(match.group(1)) or {}
    if not isinstance(data, dict):
        return text
    if slots:
        slot = slots[0]
        data["故事板参照"] = {
            "name": "故事板总参照",
            "role": "storyboard_sheet",
            "reference_index": 1,
            "uploaded_url": slot["uploaded_url"],
            "image_token": slot["image_token"],
        }
    else:
        data.pop("故事板参照", None)
    rendered = yaml.safe_dump(data, allow_unicode=True, sort_keys=False).strip()
    return text[: match.start(1)] + rendered + text[match.end(1) :]


def _rewrite_image_list(text: str, slots: list[dict[str, Any]]) -> str:
    image_list = [slot["uploaded_url"] for slot in slots]
    replacement = "imageList: " + json.dumps(image_list, ensure_ascii=False)
    if re.search(r"(?m)^imageList:\s*\[.*\]\s*$", text):
        return re.sub(r"(?m)^imageList:\s*\[.*\]\s*$", replacement, text, count=1)
    return text.replace("modeType: singleImage2video", "modeType: singleImage2video\n" + replacement, 1)


def build(package_dir: Path, *, sync: bool) -> dict[str, Any]:
    plan_path = _first_existing(package_dir, ["libtv-submit-plan.json", "libtv-batch.yaml", "libtv-batch.yml"], "*libtv*.*")
    manifest_path = _first_existing(package_dir, ["reference-manifest.json"], "*reference-manifest.json")
    if not plan_path:
        return {"package_dir": str(package_dir), "verdict": "needs_rework", "errors": ["submit plan/batch not found"], "warnings": []}
    plan = _load_doc(plan_path)
    manifest = _load_doc(manifest_path) if manifest_path else {}
    storyboard_uploads, generation_slots, errors = _build_slots(plan, manifest)

    if sync and not errors:
        manifest["storyboard_uploads"] = storyboard_uploads
        manifest["generation_slots"] = generation_slots
        if manifest_path:
            _write_doc(manifest_path, manifest)
        tasks = _tasks(plan)
        if tasks:
            tasks[0]["storyboard_uploads"] = storyboard_uploads
            tasks[0]["generation_slots"] = generation_slots
            tasks[0]["generation_slot_source"] = generation_slots[0]["slot_source"] if generation_slots else ""
        _write_doc(plan_path, plan)
        for prompt_path in sorted(package_dir.glob("*prompt*.md")) + sorted((package_dir / "prompts").glob("*.md")):
            prompt_path.write_text(_rewrite_yaml(prompt_path.read_text(encoding="utf-8"), generation_slots), encoding="utf-8")
        for submission_path in sorted(package_dir.glob("*libtv-submission.txt")) + sorted((package_dir / "prompts").glob("*libtv-submission.txt")):
            text = submission_path.read_text(encoding="utf-8")
            text = _rewrite_image_list(_rewrite_yaml(text, generation_slots), generation_slots)
            submission_path.write_text(text, encoding="utf-8")

    return {
        "package_dir": str(package_dir),
        "plan_path": str(plan_path),
        "manifest_path": str(manifest_path) if manifest_path else "",
        "verdict": "pass" if not errors else "needs_rework",
        "storyboard_uploads": storyboard_uploads,
        "generation_slots": generation_slots,
        "sync_rule": "generation_slots projects storyboard ref into manifest, plan, prompt YAML, and imageList",
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
