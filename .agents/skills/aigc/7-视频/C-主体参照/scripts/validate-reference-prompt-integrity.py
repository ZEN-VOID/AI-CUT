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


URL_RE = re.compile(r"https?://[^\s)\"'，。；]+")
MIXED_URL_RE = re.compile(r'"url"\s*:\s*"(https?://[^"]+)"')
YAML_UPLOADED_URL_RE = re.compile(r"uploaded_url\s*:\s*[\"']?(https?://[^\s\"']+)[\"']?")
YAML_REFERENCE_INDEX_RE = re.compile(r"reference_index\s*:\s*(\d+)")
LIBTV_CLAW_PROJECT_RE = re.compile(r"https?://[^/]+/claw/([^/]+)/")
REMOTE_MISSING_PHRASES = (
    "无独立参照图",
    "无缓存 URL",
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


def _check_fingerprint(entry: dict[str, Any], errors: list[str]) -> None:
    raw_path = entry.get("path", "")
    name = entry.get("name", "")
    if not raw_path:
        errors.append(f"{name}: missing path")
        return
    path = Path(raw_path)
    if not path.exists():
        errors.append(f"{name}: bound path does not exist: {raw_path}")
        return
    expected_hash = entry.get("source_sha256")
    expected_size = entry.get("source_size_bytes")
    expected_mtime = entry.get("source_mtime_ns")
    if entry.get("uploaded_url") and not entry.get("resolved_from_current_generation_dir"):
        errors.append(f"{name}: uploaded_url used before fresh local resolution")
    if entry.get("uploaded_url") and entry.get("upload_cache_hit_after_fresh_resolution") and not entry.get("upload_cache_lookup_key"):
        errors.append(f"{name}: cache hit lacks upload_cache_lookup_key")
    if entry.get("uploaded_url") and (not expected_hash or not expected_size or not expected_mtime):
        errors.append(f"{name}: uploaded_url lacks source fingerprint")
        return
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


def validate(package_dir: Path) -> dict[str, Any]:
    manifest = _load_json(package_dir / "reference-manifest.json")
    plan = _load_json(package_dir / "libtv-submit-plan.json")
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
    for legacy_marker in ("主体参照说明：", "分镜组原文：", "缺图、无缓存 URL 或未进入预算主体："):
        if legacy_marker in prompt:
            errors.append(f"prompt.md uses legacy reorganized prompt marker: {legacy_marker}")

    for label, names in {"missing": missing, "ambiguous": ambiguous, "excluded": excluded}.items():
        overlap = sorted(bound_names & names)
        if overlap:
            errors.append(f"bound subjects also listed in {label}: {', '.join(overlap)}")

    prompt_missing = set()
    match = re.search(r"缺图、无缓存 URL 或未进入预算主体：(.+)", prompt)
    if match:
        prompt_missing = {part.strip() for part in re.split(r"[、,，]", match.group(1)) if part.strip()}
    overlap = sorted(bound_names & prompt_missing)
    if overlap:
        errors.append(f"prompt lists bound subjects as missing/excluded: {', '.join(overlap)}")

    for entry in bound:
        _check_fingerprint(entry, errors)
    _check_duplicates(bound, "path", errors)
    _check_duplicates(bound, "uploaded_url", errors)

    tasks = plan.get("tasks") or []
    images = [item for task in tasks for item in task.get("images", []) if isinstance(item, dict)]
    images_ordered = sorted(
        [item for item in images if item.get("uploaded_url")],
        key=lambda item: int(item.get("upload_index") or 0),
    )
    image_urls = {item.get("uploaded_url") for item in images if item.get("uploaded_url")}
    image_urls_ordered = [str(item.get("uploaded_url")) for item in images_ordered]
    prompt_uploaded_urls_ordered = YAML_UPLOADED_URL_RE.findall(prompt)
    prompt_uploaded_urls = set(prompt_uploaded_urls_ordered)
    prompt_reference_indexes = [int(value) for value in YAML_REFERENCE_INDEX_RE.findall(prompt)]
    mixed_urls_ordered = MIXED_URL_RE.findall(submission)
    mixed_urls = set(mixed_urls_ordered)
    submission_urls = set(URL_RE.findall(submission))
    if image_urls and image_urls != prompt_uploaded_urls:
        errors.append(
            "prompt YAML uploaded_url set does not match images[] uploaded_url set: "
            f"prompt_only={sorted(prompt_uploaded_urls - image_urls)} images_only={sorted(image_urls - prompt_uploaded_urls)}"
        )
    if image_urls != mixed_urls:
        errors.append(
            "images[] uploaded_url set does not match mixedList urls: "
            f"images_only={sorted(image_urls - mixed_urls)} mixed_only={sorted(mixed_urls - image_urls)}"
        )
    if image_urls_ordered and image_urls_ordered != prompt_uploaded_urls_ordered:
        errors.append(
            "prompt YAML uploaded_url order does not match images[] upload_index order: "
            f"prompt={prompt_uploaded_urls_ordered} images={image_urls_ordered}"
        )
    if image_urls_ordered and image_urls_ordered != mixed_urls_ordered:
        errors.append(
            "mixedList URL order does not match images[] upload_index order: "
            f"mixedList={mixed_urls_ordered} images={image_urls_ordered}"
        )
    if image_urls_ordered:
        expected_indexes = list(range(1, len(image_urls_ordered) + 1))
        if prompt_reference_indexes != expected_indexes:
            errors.append(
                "prompt YAML reference_index order must be contiguous and match images[] upload_index order: "
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
    if mixed_urls or image_urls:
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
        "verdict": "pass" if not errors else "needs_rework",
        "errors": errors,
        "warnings": warnings,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("package_dir", help="Group package directory containing reference-manifest.json and libtv-submit-plan.json")
    args = parser.parse_args()
    result = validate(Path(args.package_dir))
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result["verdict"] == "pass" else 2


if __name__ == "__main__":
    raise SystemExit(main())
