#!/usr/bin/env python3
"""Build and validate LibTV upload and slot ledgers for one group package."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any

import yaml


def _load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def _ordered_images(plan: dict[str, Any]) -> list[dict[str, Any]]:
    tasks = plan.get("tasks") or []
    if not tasks:
        return []
    images = [item for item in tasks[0].get("images", []) if isinstance(item, dict)]
    return sorted(images, key=lambda item: int(item.get("reference_index") or item.get("upload_index") or 0))


def _name(value: dict[str, Any]) -> str:
    return str(value.get("name") or value.get("yaml_name") or value.get("resolved_name") or "")


def _project_uuid(plan: dict[str, Any]) -> str:
    tasks = plan.get("tasks") or []
    if not tasks:
        return ""
    return str(tasks[0].get("projectUuid") or "")


def _task_value(plan: dict[str, Any], key: str) -> Any:
    tasks = plan.get("tasks") or []
    if not tasks:
        return ""
    return tasks[0].get(key)


def _slot_source(plan: dict[str, Any], image: dict[str, Any]) -> str:
    value = (
        image.get("slot_source")
        or image.get("ui_slot_source")
        or _task_value(plan, "slot_source")
        or _task_value(plan, "ui_slot_source")
        or _task_value(plan, "generation_slot_source")
        or "submit_plan_expected_order"
    )
    return str(value)


def _bound_by_slot(manifest: dict[str, Any]) -> dict[int, dict[str, Any]]:
    output: dict[int, dict[str, Any]] = {}
    for item in manifest.get("bound") or []:
        if not isinstance(item, dict):
            continue
        slot = int(item.get("reference_index") or item.get("upload_index") or 0)
        if slot:
            output[slot] = item
    return output


def _bound_by_name(manifest: dict[str, Any]) -> dict[str, dict[str, Any]]:
    output: dict[str, dict[str, Any]] = {}
    for item in manifest.get("bound") or []:
        if isinstance(item, dict) and item.get("name"):
            output[str(item["name"])] = item
    return output


def _find_upload_artifact(package_dir: Path, index: int, name: str, explicit_name: str = "") -> Path | None:
    if explicit_name:
        explicit_path = package_dir / explicit_name
        if explicit_path.exists():
            return explicit_path
    safe_name = re.sub(r"[^\w\u4e00-\u9fff（）()：:·.-]+", "*", name)
    patterns = [
        f"upload-{index:02d}-{name}.json",
        f"upload-{index:02d}-{safe_name}.json",
        f"upload-{index:02d}-*.json",
    ]
    for pattern in patterns:
        matches = sorted(package_dir.glob(pattern))
        if matches:
            return matches[0]
    return None


def _uploaded_url_from_artifact(path: Path | None) -> str:
    if not path or not path.exists():
        return ""
    data = _load_json(path)
    if isinstance(data.get("url"), str):
        return data["url"]
    if isinstance(data.get("uploaded_url"), str):
        return data["uploaded_url"]
    return ""


def build_ledger(package_dir: Path) -> dict[str, Any]:
    plan_path = package_dir / "libtv-submit-plan.json"
    manifest_path = package_dir / "reference-manifest.json"
    plan = _load_json(plan_path)
    manifest = _load_json(manifest_path)
    images = _ordered_images(plan)
    bound_by_slot = _bound_by_slot(manifest)
    project_uuid = _project_uuid(plan)
    slots: list[dict[str, Any]] = []
    asset_uploads: list[dict[str, Any]] = []
    generation_slots: list[dict[str, Any]] = []
    errors: list[str] = []
    warnings: list[str] = []

    expected_indices = list(range(1, len(images) + 1))
    actual_indices = [int(item.get("reference_index") or item.get("upload_index") or 0) for item in images]
    if actual_indices != expected_indices:
        errors.append(f"reference_index must be contiguous from 1: expected={expected_indices} actual={actual_indices}")

    for position, image in enumerate(images, start=1):
        name = str(image.get("name") or "")
        reference_index = int(image.get("reference_index") or image.get("upload_index") or position)
        upload_index = int(image.get("upload_index") or reference_index)
        oss_upload_index = int(image.get("oss_upload_index") or upload_index)
        slot_source = _slot_source(plan, image)
        uploaded_url = str(image.get("uploaded_url") or "")
        artifact = _find_upload_artifact(package_dir, oss_upload_index, name, str(image.get("upload_artifact") or ""))
        artifact_url = _uploaded_url_from_artifact(artifact)
        manifest_item = bound_by_slot.get(reference_index, {})

        if reference_index != position:
            errors.append(f"{name}: generation_slots reference_index must be contiguous from 1: got {reference_index} at position {position}")
        if artifact and artifact_url and artifact_url != uploaded_url:
            errors.append(f"{name}: upload artifact URL does not match submit plan URL")
        if not artifact:
            warnings.append(f"{name}: upload artifact for oss_upload_index={oss_upload_index:02d} not found")
        if manifest_item:
            if str(manifest_item.get("name") or "") != name:
                errors.append(f"{name}: manifest slot name mismatch: {manifest_item.get('name')!r}")
            manifest_url = str(manifest_item.get("uploaded_url") or "")
            if manifest_url and manifest_url != uploaded_url:
                errors.append(f"{name}: manifest uploaded_url does not match submit plan URL")
        else:
            warnings.append(f"{name}: reference-manifest bound slot missing")
        if project_uuid and f"/claw/{project_uuid}/" not in uploaded_url:
            errors.append(f"{name}: uploaded_url project scope does not match projectUuid={project_uuid}")

        asset_uploads.append({
            "name": name,
            "yaml_name": name,
            "category": image.get("category", ""),
            "canonical_asset_name": manifest_item.get("canonical_asset_name", ""),
            "source_path": image.get("path", ""),
            "local_path": image.get("path", ""),
            "source_sha256": image.get("source_sha256", ""),
            "source_size_bytes": image.get("source_size_bytes", 0),
            "source_mtime_ns": image.get("source_mtime_ns", 0),
            "reuse_policy": image.get("reuse_policy", "same_canvas_active_url"),
            "asset_registry_lookup_key": image.get("asset_registry_lookup_key", ""),
            "uploaded_url": uploaded_url,
            "upload_artifact": artifact.name if artifact else "",
            "upload_artifact_url": artifact_url,
            "oss_upload_index": oss_upload_index,
            "projectUuid": project_uuid,
            "identity_lock": f"{name} -> {uploaded_url}",
        })
        generation_slots.append({
            "slot": reference_index,
            "reference_index": reference_index,
            "ui_slot_index": reference_index,
            "mixedList_index": reference_index - 1,
            "portrait_token": f"{{{{Portrait {reference_index}}}}}",
            "image_token": f"{{{{Image {reference_index}}}}}",
            "uploaded_url": uploaded_url,
            "name": name,
            "resolved_name": name,
            "category": image.get("category", ""),
            "reuse_policy": image.get("reuse_policy", "same_canvas_active_url"),
            "asset_registry_lookup_key": image.get("asset_registry_lookup_key", ""),
            "slot_source": slot_source,
            "slot_lock": (
                f"slot={reference_index} mixedList[{reference_index - 1}] "
                f"{uploaded_url} -> {name}"
            ),
        })
        slots.append({
            "slot": reference_index,
            "upload_index": upload_index,
            "oss_upload_index": oss_upload_index,
            "reference_index": reference_index,
            "mixedList_index": reference_index - 1,
            "portrait_token": f"{{{{Portrait {reference_index}}}}}",
            "image_token": f"{{{{Image {reference_index}}}}}",
            "yaml_name": name,
            "manifest_name": manifest_item.get("name", ""),
            "category": image.get("category", ""),
            "canonical_asset_name": manifest_item.get("canonical_asset_name", ""),
            "local_path": image.get("path", ""),
            "source_sha256": image.get("source_sha256", ""),
            "source_size_bytes": image.get("source_size_bytes", 0),
            "source_mtime_ns": image.get("source_mtime_ns", 0),
            "reuse_policy": image.get("reuse_policy", "same_canvas_active_url"),
            "asset_registry_lookup_key": image.get("asset_registry_lookup_key", ""),
            "uploaded_url": uploaded_url,
            "upload_artifact": artifact.name if artifact else "",
            "upload_artifact_url": artifact_url,
            "projectUuid": project_uuid,
            "slot_source": slot_source,
            "slot_lock": (
                f"{name} reference_index={reference_index} "
                f"mixedList[{reference_index - 1}] {uploaded_url}"
            ),
        })

    return {
        "package_dir": str(package_dir),
        "project_name": plan.get("project_name", ""),
        "episode_id": plan.get("episode_id", ""),
        "group_id": _task_value(plan, "group_id") or manifest.get("group_id", ""),
        "projectUuid": project_uuid,
        "projectUrl": _task_value(plan, "projectUrl") or "",
        "verdict": "pass" if not errors else "needs_rework",
        "source_layer_rule": (
            "OSS upload only creates name-to-url identity mapping. "
            "Generation slot order is a separate authority: UI slot N / Portrait N "
            "wins when observed; otherwise use final mixedList order, then map "
            "back to yaml_name through uploaded_url."
        ),
        "ledger_rule": (
            "asset_uploads record yaml_name -> uploaded_url. generation_slots record "
            "slot N / mixedList[N-1] / Portrait N -> uploaded_url -> resolved_name."
        ),
        "asset_uploads": asset_uploads,
        "generation_slots": generation_slots,
        "slots": slots,
        "errors": errors,
        "warnings": warnings,
    }


def _slot_images_by_key(plan: dict[str, Any]) -> dict[tuple[int, str, str], dict[str, Any]]:
    images = _ordered_images(plan)
    keyed: dict[tuple[int, str, str], dict[str, Any]] = {}
    for image in images:
        reference_index = int(image.get("reference_index") or image.get("upload_index") or 0)
        keyed[(reference_index, _name(image), str(image.get("uploaded_url") or ""))] = image
    return keyed


def _merge_task_images(plan: dict[str, Any], slots: list[dict[str, Any]], manifest: dict[str, Any]) -> None:
    tasks = plan.setdefault("tasks", [])
    if not tasks:
        tasks.append({})
    task = tasks[0]
    by_key = _slot_images_by_key(plan)
    bound_by_name = _bound_by_name(manifest)
    images: list[dict[str, Any]] = []
    for slot in slots:
        reference_index = int(slot.get("reference_index") or slot.get("slot") or 0)
        name = _name(slot)
        uploaded_url = str(slot.get("uploaded_url") or "")
        source = (
            by_key.get((reference_index, name, uploaded_url))
            or bound_by_name.get(name)
            or {}
        )
        image = dict(source)
        image.update({
            "upload_index": reference_index,
            "reference_index": reference_index,
            "ui_slot_index": int(slot.get("ui_slot_index") or reference_index),
            "oss_upload_index": int(image.get("oss_upload_index") or reference_index),
            "name": name,
            "category": slot.get("category") or image.get("category", ""),
            "uploaded_url": uploaded_url,
            "portrait_token": slot.get("portrait_token") or f"{{{{Portrait {reference_index}}}}}",
            "image_token": slot.get("image_token") or f"{{{{Image {reference_index}}}}}",
            "slot_source": slot.get("slot_source") or "submit_plan_expected_order",
            "subject_inline": (
                f"{name} reference_index={reference_index} "
                f"{slot.get('portrait_token') or f'{{{{Portrait {reference_index}}}}}'} uploaded_url"
            ),
        })
        images.append(image)
    task["images"] = images
    task["slot_binding_phase"] = "final" if images else task.get("slot_binding_phase", "draft")
    task["generation_slot_source"] = images[0].get("slot_source", "submit_plan_expected_order") if images else ""


def _merge_manifest_slots(manifest: dict[str, Any], ledger: dict[str, Any]) -> None:
    slots = ledger.get("generation_slots") or []
    asset_uploads = ledger.get("asset_uploads") or []
    manifest["asset_uploads"] = asset_uploads
    manifest["generation_slots"] = slots
    slot_by_name = {_name(slot): slot for slot in slots}
    for item in manifest.get("bound") or []:
        if not isinstance(item, dict):
            continue
        slot = slot_by_name.get(str(item.get("name") or ""))
        if not slot:
            continue
        reference_index = int(slot.get("reference_index") or slot.get("slot") or 0)
        item.update({
            "uploaded_url": slot.get("uploaded_url", ""),
            "upload_index": reference_index,
            "reference_index": reference_index,
            "ui_slot_index": int(slot.get("ui_slot_index") or reference_index),
            "ui_slot_source": slot.get("slot_source", "submit_plan_expected_order"),
            "oss_upload_index": int(item.get("oss_upload_index") or reference_index),
            "portrait_token": slot.get("portrait_token") or f"{{{{Portrait {reference_index}}}}}",
            "image_token": slot.get("image_token") or f"{{{{Image {reference_index}}}}}",
        })


def _rewrite_yaml_bindings(text: str, slots: list[dict[str, Any]]) -> str:
    match = re.search(r"```yaml\n(.*?)\n```", text, re.S)
    if not match:
        return text
    data = yaml.safe_load(match.group(1)) or {}
    if not isinstance(data, dict):
        return text
    slot_by_name = {_name(slot): slot for slot in slots}
    for section in ("角色", "场景", "道具"):
        items = data.get(section)
        if not isinstance(items, list):
            continue
        rewritten: list[Any] = []
        for item in items:
            if isinstance(item, dict):
                name = str(item.get("name") or "")
                base: dict[str, Any] = dict(item)
            else:
                name = str(item)
                base = {"name": name}
            slot = slot_by_name.get(name)
            if slot:
                reference_index = int(slot.get("reference_index") or slot.get("slot") or 0)
                base.update({
                    "name": name,
                    "reference_index": reference_index,
                    "uploaded_url": slot.get("uploaded_url", ""),
                    "portrait_token": slot.get("portrait_token") or f"{{{{Portrait {reference_index}}}}}",
                })
                rewritten.append(base)
                continue
            for key in ("reference_index", "uploaded_url", "portrait_token", "image_token"):
                base.pop(key, None)
            rewritten.append(base["name"] if set(base) == {"name"} else base)
        data[section] = rewritten
    rendered = yaml.safe_dump(data, allow_unicode=True, sort_keys=False).strip()
    return text[: match.start(1)] + rendered + text[match.end(1) :]


def _rewrite_mixed_list(text: str, slots: list[dict[str, Any]]) -> str:
    mixed = [
        {"url": str(slot.get("uploaded_url")), "type": "image"}
        for slot in slots
        if slot.get("uploaded_url")
    ]
    if not mixed:
        return text
    replacement = "mixedList: " + json.dumps(mixed, ensure_ascii=False)
    if re.search(r"(?m)^mixedList:\s*\[.*\]\s*$", text):
        return re.sub(r"(?m)^mixedList:\s*\[.*\]\s*$", replacement, text, count=1)
    return text.replace("modeType: mixed2video", "modeType: mixed2video\n" + replacement, 1)


def sync_package(package_dir: Path) -> dict[str, Any]:
    plan_path = package_dir / "libtv-submit-plan.json"
    manifest_path = package_dir / "reference-manifest.json"
    plan = _load_json(plan_path)
    manifest = _load_json(manifest_path)
    ledger = build_ledger(package_dir)
    if ledger["verdict"] != "pass":
        return ledger

    slots = [slot for slot in ledger.get("generation_slots", []) if isinstance(slot, dict)]
    _merge_manifest_slots(manifest, ledger)
    _merge_task_images(plan, slots, manifest)
    manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    plan_path.write_text(json.dumps(plan, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    prompt_path = package_dir / "prompt.md"
    if prompt_path.exists():
        prompt_path.write_text(_rewrite_yaml_bindings(prompt_path.read_text(encoding="utf-8"), slots), encoding="utf-8")
    submission_path = package_dir / "libtv-submission.txt"
    if submission_path.exists():
        submission = submission_path.read_text(encoding="utf-8")
        submission = _rewrite_mixed_list(submission, slots)
        submission = _rewrite_yaml_bindings(submission, slots)
        submission_path.write_text(submission, encoding="utf-8")

    ledger["synced_files"] = [
        str(manifest_path),
        str(plan_path),
        *(str(prompt_path) for _ in [0] if prompt_path.exists()),
        *(str(submission_path) for _ in [0] if submission_path.exists()),
    ]
    ledger["sync_rule"] = "generation_slots is projected into manifest, submit plan, prompt YAML, and libtv submission mixedList"
    return ledger


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("package_dir", help="Group package directory containing LibTV plan and manifest")
    parser.add_argument("--write", action="store_true", help="Write upload-ledger.json in the package directory")
    parser.add_argument("--sync", action="store_true", help="Project generation_slots into manifest, submit plan, prompt YAML, and submission mixedList")
    args = parser.parse_args()
    package_dir = Path(args.package_dir)
    result = sync_package(package_dir) if args.sync else build_ledger(package_dir)
    if args.write:
        (package_dir / "upload-ledger.json").write_text(
            json.dumps(result, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result["verdict"] == "pass" else 2


if __name__ == "__main__":
    raise SystemExit(main())
