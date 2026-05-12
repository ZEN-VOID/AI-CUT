#!/usr/bin/env python3
"""Validate C-subject reference bindings across manifest, plan, and prompts."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from pathlib import Path
from typing import Any

import yaml


URL_RE = re.compile(r"https?://[^\s)\"'，。；]+")
MIXED_URL_RE = re.compile(r'"url"\s*:\s*"(https?://[^"]+)"')
YAML_UPLOADED_URL_RE = re.compile(r"uploaded_url\s*:\s*[\"']?(https?://[^\s\"']+)[\"']?")
YAML_REFERENCE_INDEX_RE = re.compile(r"reference_index\s*:\s*(\d+)")
LIBTV_CLAW_PROJECT_RE = re.compile(r"https?://[^/]+/claw/([^/]+)/")
REMOTE_MISSING_PHRASES = (
    "无独立参照图",
    "无缓存 URL",
    "无可复用 URL",
    "未进入预算主体",
    "不创建空图片槽",
)


def _section(text: str, heading: str) -> str:
    marker = f"【{heading}】"
    start = text.find(marker)
    if start < 0:
        return ""
    body_start = start + len(marker)
    next_heading = re.search(r"\n【[^】]+】", text[body_start:])
    if not next_heading:
        return text[body_start:]
    return text[body_start : body_start + next_heading.start()]


def _heading_line_index(text: str, heading: str) -> int:
    match = re.search(rf"(?m)^【{re.escape(heading)}】\s*$", text)
    return match.start() if match else -1


def _load_json(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))


def _names(items: list[Any]) -> set[str]:
    names: set[str] = set()
    for item in items:
        if isinstance(item, dict):
            name = item.get("name")
        else:
            name = item
        if isinstance(name, str) and name:
            names.add(name)
    return names


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _check_local_asset_evidence(entry: dict[str, Any], errors: list[str], warnings: list[str]) -> None:
    raw_path = entry.get("path", "")
    name = entry.get("name", "")
    if not raw_path:
        if entry.get("uploaded_url"):
            reuse_marker = entry.get("asset_registry_lookup_key") or entry.get("asset_reuse_policy") or entry.get("reuse_policy")
            if not reuse_marker:
                warnings.append(f"{name}: uploaded_url reused without local path; record asset_registry_lookup_key or reuse_policy")
            return
        errors.append(f"{name}: missing path and uploaded_url")
        return
    path = Path(raw_path)
    if not path.exists():
        if entry.get("uploaded_url"):
            warnings.append(f"{name}: local path is unavailable; relying on same-canvas uploaded_url reuse: {raw_path}")
            return
        errors.append(f"{name}: bound path does not exist and no uploaded_url is available: {raw_path}")
        return
    expected_hash = entry.get("source_sha256")
    expected_size = entry.get("source_size_bytes")
    expected_mtime = entry.get("source_mtime_ns")
    if entry.get("uploaded_url") and entry.get("upload_cache_hit_after_fresh_resolution") and not entry.get("upload_cache_lookup_key"):
        warnings.append(f"{name}: legacy cache hit lacks upload_cache_lookup_key")
    if expected_hash and _sha256(path) != expected_hash:
        errors.append(f"{name}: source_sha256 mismatch")
    stat = path.stat()
    if expected_size and int(expected_size) != stat.st_size:
        errors.append(f"{name}: source_size_bytes mismatch")
    if expected_mtime and int(expected_mtime) != stat.st_mtime_ns:
        errors.append(f"{name}: source_mtime_ns mismatch")


def _check_duplicates(entries: list[dict[str, Any]], key: str, errors: list[str]) -> None:
    seen: dict[str, list[dict[str, Any]]] = {}
    for entry in entries:
        value = entry.get(key)
        if value:
            seen.setdefault(str(value), []).append(entry)
    for value, grouped in seen.items():
        if len(grouped) <= 1:
            continue
        if all(entry.get("shared_reference_group") for entry in grouped):
            continue
        names = "/".join(str(entry.get("name", "")) for entry in grouped)
        errors.append(f"duplicate {key} without shared_reference_group: {names} -> {value}")


def _libtv_claw_project(url: str) -> str | None:
    match = LIBTV_CLAW_PROJECT_RE.search(url)
    if not match:
        return None
    return match.group(1)


def _prompt_yaml_bindings(prompt: str, errors: list[str]) -> list[dict[str, Any]]:
    match = re.search(r"```yaml\n(.*?)\n```", prompt, re.S)
    if not match:
        return []
    try:
        data = yaml.safe_load(match.group(1)) or {}
    except yaml.YAMLError as exc:
        errors.append(f"prompt YAML could not be parsed: {exc}")
        return []
    bindings: list[dict[str, Any]] = []
    for section in ("角色", "场景", "道具"):
        items = data.get(section) or []
        if not isinstance(items, list):
            continue
        for item in items:
            if not isinstance(item, dict):
                continue
            name = item.get("name")
            url = item.get("uploaded_url")
            reference_index = item.get("reference_index")
            if not url and not reference_index:
                continue
            if not url or not reference_index:
                errors.append(f"prompt YAML incomplete reference binding in {section}: {item}")
                continue
            try:
                index = int(reference_index)
            except (TypeError, ValueError):
                errors.append(f"prompt YAML invalid reference_index in {section}: {item}")
                continue
            if not isinstance(name, str) or not name:
                errors.append(f"prompt YAML bound item lacks name in {section}: {item}")
                continue
            bindings.append({
                "section": section,
                "name": name,
                "reference_index": index,
                "uploaded_url": str(url),
                "portrait_token": item.get("portrait_token", ""),
            })
    return bindings


def _to_int(value: Any, default: int = 0) -> int:
    try:
        return int(value)
    except (TypeError, ValueError):
        return default


def _ordered_plan_images(plan: dict[str, Any]) -> list[dict[str, Any]]:
    tasks = plan.get("tasks") or []
    images = [item for task in tasks for item in task.get("images", []) if isinstance(item, dict)]
    return sorted(
        [item for item in images if item.get("uploaded_url")],
        key=lambda item: _to_int(item.get("reference_index") or item.get("upload_index")),
    )


def _canonical_generation_slots(manifest: dict[str, Any], plan: dict[str, Any]) -> list[dict[str, Any]]:
    slots = [item for item in manifest.get("generation_slots", []) if isinstance(item, dict)]
    if slots:
        ordered: list[dict[str, Any]] = []
        for fallback_position, slot in enumerate(slots, start=1):
            reference_index = _to_int(slot.get("reference_index") or slot.get("slot") or slot.get("ui_slot_index"), fallback_position)
            ordered.append({
                "name": str(slot.get("name", "")),
                "category": str(slot.get("category", "")),
                "reference_index": reference_index,
                "slot": _to_int(slot.get("slot"), reference_index),
                "mixedList_index": _to_int(slot.get("mixedList_index"), reference_index - 1),
                "uploaded_url": str(slot.get("uploaded_url", "")),
                "source": "reference-manifest.generation_slots",
            })
        return sorted(ordered, key=lambda item: item["reference_index"])

    ordered_images = _ordered_plan_images(plan)
    fallback_slots: list[dict[str, Any]] = []
    for fallback_position, image in enumerate(ordered_images, start=1):
        reference_index = _to_int(image.get("reference_index") or image.get("upload_index"), fallback_position)
        fallback_slots.append({
            "name": str(image.get("name", "")),
            "category": str(image.get("category", "")),
            "reference_index": reference_index,
            "slot": reference_index,
            "mixedList_index": reference_index - 1,
            "uploaded_url": str(image.get("uploaded_url", "")),
            "source": "libtv-submit-plan.images_fallback",
        })
    return fallback_slots


def _check_reference_slot_registry(
    manifest: dict[str, Any],
    plan: dict[str, Any],
    prompt_yaml_bindings: list[dict[str, Any]],
    mixed_urls_ordered: list[str],
    phase: str,
    errors: list[str],
    warnings: list[str],
) -> list[dict[str, Any]]:
    slots = _canonical_generation_slots(manifest, plan)
    if not slots:
        return slots

    indexes = [slot["reference_index"] for slot in slots]
    expected_indexes = list(range(1, len(slots) + 1))
    if indexes != expected_indexes:
        errors.append(
            "generation slot registry reference_index values must be contiguous: "
            f"expected={expected_indexes} actual={indexes}"
        )

    if any(not slot["name"] or not slot["uploaded_url"] for slot in slots):
        errors.append("generation slot registry entries must each include name and uploaded_url")

    asset_by_url: dict[str, dict[str, Any]] = {}
    for asset in manifest.get("asset_uploads", []):
        if isinstance(asset, dict) and asset.get("uploaded_url"):
            asset_by_url[str(asset["uploaded_url"])] = asset
    for slot in slots:
        asset = asset_by_url.get(slot["uploaded_url"])
        if asset and str(asset.get("name", "")) != slot["name"]:
            errors.append(
                "generation slot registry name does not match asset_uploads for uploaded_url: "
                f"reference_index={slot['reference_index']} slot_name={slot['name']} "
                f"asset_name={asset.get('name')} url={slot['uploaded_url']}"
            )

    plan_by_index = {
        _to_int(image.get("reference_index") or image.get("upload_index")): image
        for image in _ordered_plan_images(plan)
    }
    for slot in slots:
        image = plan_by_index.get(slot["reference_index"])
        if not image:
            if phase == "final":
                errors.append(f"submit plan images[] missing reference_index={slot['reference_index']} from generation slot registry")
            continue
        if str(image.get("name", "")) != slot["name"] or str(image.get("uploaded_url", "")) != slot["uploaded_url"]:
            errors.append(
                "submit plan images[] does not match generation slot registry: "
                f"reference_index={slot['reference_index']} "
                f"slot=({slot['name']}, {slot['uploaded_url']}) "
                f"plan=({image.get('name')}, {image.get('uploaded_url')})"
            )

    prompt_by_index = {binding["reference_index"]: binding for binding in prompt_yaml_bindings}
    if phase == "final":
        for slot in slots:
            binding = prompt_by_index.get(slot["reference_index"])
            if not binding:
                errors.append(f"prompt YAML missing bound item for reference_index={slot['reference_index']} name={slot['name']}")
                continue
            if binding["name"] != slot["name"] or binding["uploaded_url"] != slot["uploaded_url"]:
                errors.append(
                    "prompt YAML subject reference does not match generation slot registry: "
                    f"reference_index={slot['reference_index']} "
                    f"slot=({slot['name']}, {slot['uploaded_url']}) "
                    f"prompt=({binding['name']}, {binding['uploaded_url']})"
                )
        for binding in prompt_yaml_bindings:
            slot = next((item for item in slots if item["reference_index"] == binding["reference_index"]), None)
            if not slot:
                errors.append(
                    "prompt YAML references a slot absent from generation slot registry: "
                    f"reference_index={binding['reference_index']} name={binding['name']} url={binding['uploaded_url']}"
                )

    expected_urls = [slot["uploaded_url"] for slot in slots if slot["uploaded_url"]]
    if phase == "final" and mixed_urls_ordered and mixed_urls_ordered != expected_urls:
        errors.append(
            "mixedList URL order does not match generation slot registry: "
            f"expected={expected_urls} actual={mixed_urls_ordered}"
        )
    if slots and slots[0]["source"].endswith("fallback"):
        warnings.append("reference-manifest.generation_slots missing; using submit plan images[] as fallback slot registry")

    return slots


def _check_libtv_project_scope(
    bound: list[dict[str, Any]],
    tasks: list[dict[str, Any]],
    mixed_urls: set[str],
    errors: list[str],
) -> None:
    uploaded_urls = {
        str(entry.get("uploaded_url"))
        for entry in bound
        if entry.get("uploaded_url")
    }
    uploaded_urls |= mixed_urls

    image_urls_by_task: list[tuple[str, str, str]] = []
    for task in tasks:
        task_group = str(task.get("group_id", ""))
        project_uuid = str(task.get("projectUuid", "") or "")
        for image in task.get("images", []):
            if not isinstance(image, dict) or not image.get("uploaded_url"):
                continue
            url = str(image["uploaded_url"])
            uploaded_urls.add(url)
            image_urls_by_task.append((task_group, project_uuid, url))

    if not uploaded_urls:
        return

    task_project_uuids = {
        str(task.get("projectUuid"))
        for task in tasks
        if task.get("projectUuid")
    }
    if not task_project_uuids:
        errors.append("uploaded_url present but submit plan lacks projectUuid; run change_project before upload and render submission")
        return

    if len(task_project_uuids) > 1:
        errors.append(f"multiple projectUuid values in one group submit plan: {sorted(task_project_uuids)}")
        return

    expected_project_uuid = next(iter(task_project_uuids))
    for url in sorted(uploaded_urls):
        claw_project = _libtv_claw_project(url)
        if not claw_project:
            errors.append(f"uploaded_url is not a LibTV claw URL with project scope: {url}")
            continue
        if claw_project != expected_project_uuid:
            errors.append(
                "uploaded_url project scope mismatch: "
                f"url_project={claw_project} plan_projectUuid={expected_project_uuid} url={url}"
            )

    for group_id, project_uuid, url in image_urls_by_task:
        if not project_uuid:
            errors.append(f"{group_id}: image uploaded_url present but task.projectUuid is empty: {url}")


def _task_phase(plan: dict[str, Any], requested_phase: str) -> str:
    if requested_phase != "auto":
        return requested_phase
    tasks = plan.get("tasks") or []
    if tasks and isinstance(tasks[0], dict):
        phase = str(tasks[0].get("slot_binding_phase") or tasks[0].get("reference_binding_phase") or "")
        if phase in {"draft", "final"}:
            return phase
    return "final"


def validate(package_dir: Path, phase: str = "auto") -> dict[str, Any]:
    manifest = _load_json(package_dir / "reference-manifest.json")
    plan = _load_json(package_dir / "libtv-submit-plan.json")
    phase = _task_phase(plan, phase)
    prompt = (package_dir / "prompt.md").read_text(encoding="utf-8") if (package_dir / "prompt.md").exists() else ""
    submission = (package_dir / "libtv-submission.txt").read_text(encoding="utf-8") if (package_dir / "libtv-submission.txt").exists() else ""
    errors: list[str] = []
    warnings: list[str] = []

    bound = [item for item in manifest.get("bound", []) if isinstance(item, dict)]
    missing = _names(manifest.get("missing", []))
    ambiguous = _names(manifest.get("ambiguous", []))
    excluded = _names(manifest.get("excluded_from_libtv_images", [])) | _names(manifest.get("excluded_due_to_budget", []))
    bound_names = _names(bound)
    group_id = manifest.get("group_id", "")

    if group_id and not prompt.lstrip().startswith(f"## {group_id}"):
        errors.append("prompt.md must be source-first and start with the original group heading")
    for legacy_marker in ("主体参照说明：", "分镜组原文：", "缺图、无缓存 URL 或未进入预算主体：", "缺图、无可复用 URL 或未进入预算主体："):
        if legacy_marker in prompt:
            errors.append(f"prompt.md uses legacy reorganized prompt marker: {legacy_marker}")

    for label, names in {"missing": missing, "ambiguous": ambiguous, "excluded": excluded}.items():
        overlap = sorted(bound_names & names)
        if overlap:
            errors.append(f"bound subjects also listed in {label}: {', '.join(overlap)}")

    prompt_missing = set()
    match = re.search(r"缺图、(?:无缓存 URL|无可复用 URL) 或未进入预算主体：(.+)", prompt)
    if match:
        prompt_missing = {part.strip() for part in re.split(r"[、,，]", match.group(1)) if part.strip()}
    overlap = sorted(bound_names & prompt_missing)
    if overlap:
        errors.append(f"prompt lists bound subjects as missing/excluded: {', '.join(overlap)}")

    for entry in bound:
        _check_local_asset_evidence(entry, errors, warnings)
    _check_duplicates(bound, "path", errors)
    _check_duplicates(bound, "uploaded_url", errors)

    tasks = plan.get("tasks") or []
    images = [item for task in tasks for item in task.get("images", []) if isinstance(item, dict)]
    images_ordered = _ordered_plan_images(plan)
    image_urls = {item.get("uploaded_url") for item in images if item.get("uploaded_url")}
    image_urls_ordered = [str(item.get("uploaded_url")) for item in images_ordered]
    prompt_yaml_bindings = _prompt_yaml_bindings(prompt, errors)
    prompt_uploaded_urls_ordered = [
        binding["uploaded_url"]
        for binding in sorted(prompt_yaml_bindings, key=lambda item: item["reference_index"])
    ] if prompt_yaml_bindings else YAML_UPLOADED_URL_RE.findall(prompt)
    prompt_uploaded_urls = set(prompt_uploaded_urls_ordered)
    prompt_reference_indexes = [binding["reference_index"] for binding in prompt_yaml_bindings] if prompt_yaml_bindings else [int(value) for value in YAML_REFERENCE_INDEX_RE.findall(prompt)]
    mixed_urls_ordered = MIXED_URL_RE.findall(submission)
    mixed_urls = set(mixed_urls_ordered)
    submission_urls = set(URL_RE.findall(submission))
    generation_slots = _check_reference_slot_registry(
        manifest,
        plan,
        prompt_yaml_bindings,
        mixed_urls_ordered,
        phase,
        errors,
        warnings,
    )
    generation_slot_urls_ordered = [slot["uploaded_url"] for slot in generation_slots if slot.get("uploaded_url")]
    generation_slot_urls = set(generation_slot_urls_ordered)
    if phase == "final" and generation_slot_urls and image_urls != generation_slot_urls:
        errors.append(
            "images[] uploaded_url set does not match generation slot registry: "
            f"images_only={sorted(image_urls - generation_slot_urls)} slots_only={sorted(generation_slot_urls - image_urls)}"
        )
    if phase == "draft" and (prompt_uploaded_urls or prompt_reference_indexes):
        warnings.append("draft phase contains reference_index/uploaded_url; prefer leaving prompt YAML unbound until UI slots are confirmed")
    if phase == "final" and image_urls and image_urls != prompt_uploaded_urls:
        errors.append(
            "prompt YAML uploaded_url set does not match images[] uploaded_url set: "
            f"prompt_only={sorted(prompt_uploaded_urls - image_urls)} images_only={sorted(image_urls - prompt_uploaded_urls)}"
        )
    if phase == "final" and image_urls != mixed_urls:
        errors.append(
            "images[] uploaded_url set does not match mixedList urls: "
            f"images_only={sorted(image_urls - mixed_urls)} mixed_only={sorted(mixed_urls - image_urls)}"
        )
    if phase == "final" and image_urls_ordered and image_urls_ordered != prompt_uploaded_urls_ordered:
        errors.append(
            "prompt YAML uploaded_url order by reference_index does not match images[] upload_index order: "
            f"prompt={prompt_uploaded_urls_ordered} images={image_urls_ordered}"
        )
    if phase == "final" and image_urls_ordered and image_urls_ordered != mixed_urls_ordered:
        errors.append(
            "mixedList URL order does not match images[] upload_index order: "
            f"mixedList={mixed_urls_ordered} images={image_urls_ordered}"
        )
    if phase == "final" and image_urls_ordered:
        expected_indexes = list(range(1, len(image_urls_ordered) + 1))
        if sorted(prompt_reference_indexes) != expected_indexes:
            errors.append(
                "prompt YAML reference_index values must be contiguous and match images[] upload_index slots: "
                f"expected={expected_indexes} actual={prompt_reference_indexes}"
            )
    missing_named_urls = sorted(mixed_urls - submission_urls)
    if missing_named_urls:
        errors.append(f"mixedList urls missing from remote subject URL text: {missing_named_urls}")
    _check_duplicates(images, "uploaded_url", errors)
    _check_libtv_project_scope(bound, tasks, mixed_urls, errors)

    if re.search(r"^[^\n：:]{1,40}[：:]\s*参照图\d+\b", submission, flags=re.M):
        errors.append("remote submission contains manual reference numbering")
    if "@projects/" in submission or "/Volumes/" in submission:
        errors.append("remote submission leaks local paths")
    for phrase in REMOTE_MISSING_PHRASES:
        if phrase in submission:
            errors.append(f"remote submission contains missing/excluded subject prose: {phrase}")
    subject_section = _section(submission, "主体参照说明")
    if "生成时保持" in subject_section:
        errors.append("remote subject reference lines repeat continuity prose; keep continuity in direct request")
    continuity_count = submission.count("生成时保持")
    if continuity_count > 1:
        errors.append(f"remote submission repeats continuity prose {continuity_count} times")
    if phase == "final" and (mixed_urls or image_urls):
        if "参照连续性总领" in submission:
            errors.append("remote submission contains standalone continuity heading; fold continuity into direct request")
        elif "生成时保持" not in submission:
            errors.append("remote submission lacks single continuity sentence before source text")
        else:
            source_heading_index = _heading_line_index(submission, "分镜组源文本")
            if source_heading_index >= 0 and submission.index("生成时保持") > source_heading_index:
                errors.append("continuity sentence must appear before 【分镜组源文本】")

    return {
        "package_dir": str(package_dir),
        "phase": phase,
        "verdict": "pass" if not errors else "needs_rework",
        "errors": errors,
        "warnings": warnings,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("package_dir", help="Group package directory containing reference-manifest.json and libtv-submit-plan.json")
    parser.add_argument("--phase", choices=["auto", "draft", "final"], default="auto", help="draft allows unbound prompt YAML before UI slot confirmation; final requires complete reference projection")
    args = parser.parse_args()
    result = validate(Path(args.package_dir), args.phase)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result["verdict"] == "pass" else 2


if __name__ == "__main__":
    raise SystemExit(main())
