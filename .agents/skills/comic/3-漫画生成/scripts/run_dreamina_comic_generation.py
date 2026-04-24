#!/usr/bin/env python3
"""Legacy Dreamina runner for nine_blade_comic_prompts.v1 JSON.

The comic-generation skill now defaults to Codex built-in image_gen with
model_policy=GPT-IMAGE-2-default. Use this script only when the user explicitly
asks for the legacy Dreamina CLI fallback.
"""

from __future__ import annotations

import argparse
from datetime import datetime
import json
import re
import subprocess
import sys
import time
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[5]
DATA_MODULES_ROOT = Path(__file__).resolve().parents[2] / "scripts"
if str(DATA_MODULES_ROOT) not in sys.path:
    sys.path.insert(0, str(DATA_MODULES_ROOT))

from data_modules.nine_blade_prompt_normalizer import normalize_nine_blade_prompt_data
import run_seedream_comic_generation as seedream_runner


VALIDATOR = REPO_ROOT / ".agents/skills/comic/2-九刀流漫画提示词/scripts/validate_nine_blade_prompt_json.py"
IMAGE_SUFFIXES = {".png", ".jpg", ".jpeg", ".webp"}


def _now_stamp() -> str:
    return datetime.now().strftime("%Y%m%d_%H%M%S")


def _timestamp() -> str:
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def _write_json(path: Path, payload: dict[str, Any]) -> None:
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")


def _extract_json(raw: str) -> dict[str, Any] | None:
    text = raw.strip()
    if not text:
        return None
    try:
        parsed = json.loads(text)
    except json.JSONDecodeError:
        match = re.search(r"(\{.*\}|\[.*\])", text, re.DOTALL)
        if not match:
            return None
        try:
            parsed = json.loads(match.group(1))
        except json.JSONDecodeError:
            return None
    return parsed if isinstance(parsed, dict) else {"raw_payload": parsed}


def _search_value(payload: Any, target_key: str) -> Any:
    if isinstance(payload, dict):
        for key, value in payload.items():
            if key == target_key:
                return value
            found = _search_value(value, target_key)
            if found is not None:
                return found
    elif isinstance(payload, list):
        for item in payload:
            found = _search_value(item, target_key)
            if found is not None:
                return found
    return None


def _extract_submit_id(payload: dict[str, Any] | None, raw_text: str) -> str:
    if payload is not None:
        for key in ("submit_id", "submitId"):
            value = _search_value(payload, key)
            if isinstance(value, str) and value.strip():
                return value.strip()
    match = re.search(r'"submit_id"\s*:\s*"([^"]+)"', raw_text)
    if match:
        return match.group(1).strip()
    return ""


def _extract_status(payload: dict[str, Any] | None, raw_text: str) -> str:
    candidates = []
    if payload is not None:
        for key in ("gen_status", "status", "task_status", "remote_status"):
            value = _search_value(payload, key)
            if isinstance(value, str) and value.strip():
                candidates.append(value.strip())
    lowered = " ".join(candidates).lower()
    raw_lower = raw_text.lower()
    for needle in ("success", "succeed", "completed", "downloaded"):
        if needle in lowered or needle in raw_lower:
            return "success"
    for needle in ("fail", "failed", "error"):
        if needle in lowered or needle in raw_lower:
            return "failed"
    for needle in ("querying", "queued", "running", "pending", "processing", "wait"):
        if needle in lowered or needle in raw_lower:
            return "querying"
    return "unknown"


def _run_command(command: list[str]) -> tuple[dict[str, Any] | None, str]:
    result = subprocess.run(
        command,
        cwd=str(REPO_ROOT),
        text=True,
        capture_output=True,
        check=False,
    )
    stdout = result.stdout or ""
    stderr = result.stderr or ""
    raw_text = stdout if stdout.strip() else stderr
    payload = _extract_json(stdout) or _extract_json(stderr)
    if result.returncode != 0 and payload is None:
        raise RuntimeError(f"command failed: {' '.join(command)}\n{stderr or stdout}")
    return payload, raw_text


def _run_validator(json_path: Path) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(VALIDATOR), str(json_path)],
        cwd=str(REPO_ROOT),
        text=True,
        capture_output=True,
        check=False,
    )


def _bullet_block(title: str, lines: list[str]) -> str:
    cleaned = [line.strip() for line in lines if line and line.strip()]
    if not cleaned:
        return ""
    return f"{title}:\n" + "\n".join(f"- {line}" for line in cleaned)


def _render_queue(queue_rows: list[dict[str, Any]]) -> str:
    lines = [
        "# Dreamina Queue",
        "",
        "| queue_id | page | submit_id | local_status | remote_status | created_at | last_checked_at | next_action | output_file | notes |",
        "| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |",
    ]
    for row in queue_rows:
        lines.append(
            "| {queue_id} | {page} | {submit_id} | {local_status} | {remote_status} | {created_at} | {last_checked_at} | {next_action} | {output_file} | {notes} |".format(
                queue_id=row.get("queue_id", ""),
                page=row.get("page_number", ""),
                submit_id=row.get("submit_id", ""),
                local_status=row.get("local_status", ""),
                remote_status=row.get("remote_status", ""),
                created_at=row.get("created_at", ""),
                last_checked_at=row.get("last_checked_at", ""),
                next_action=row.get("next_action", ""),
                output_file=row.get("output_file", ""),
                notes=row.get("notes", ""),
            )
        )
    return "\n".join(lines) + "\n"


def _write_queue(path: Path, queue_rows: list[dict[str, Any]]) -> None:
    path.write_text(_render_queue(queue_rows), encoding="utf-8")


def _safe_line(value: Any) -> str:
    if value in (None, "", [], {}):
        return ""
    if isinstance(value, str):
        return re.sub(r"\s+", " ", value).strip()
    return json.dumps(value, ensure_ascii=False, separators=(",", ":"))


def _summarize_page_prompt(data: dict[str, Any], page: dict[str, Any]) -> str:
    type_stack_ref = data.get("type_stack_ref", {})
    type_pack_context = data.get("type_pack_context", {})
    continuity_context = data.get("continuity_context", {})
    style_bible = data.get("style_bible", {})
    main_character_lock = data.get("main_character_lock", {})
    scene_bible = data.get("scene_continuity_bible", {})
    page_number = int(page.get("page_number", 0))
    page_role = _safe_line(page.get("page_role"))
    group_meta = data.get("page_group", {})
    character_map = seedream_runner._character_map(data)
    scene_map = seedream_runner._scene_map(data)
    active_character_ids = page.get("active_character_ids", []) if isinstance(page.get("active_character_ids"), list) else []
    scene_id = str(page.get("scene_id", "")).strip()
    scene_lock = scene_map.get(scene_id, {})
    page_number_overlay = page.get("page_number_overlay", {})
    image_projection = type_pack_context.get("stage_projection", {}).get("image_generation", {})

    prompt_sections = [
        "Generate one complete vertical 9:16 comic page, not a collage, not a contact sheet, not a single illustration without panels.",
        f"This is page {page_number} from a continuous 9-page sequence. Keep the same cast, rendering DNA, and scene continuity as the surrounding pages.",
        _bullet_block(
            "Global continuity",
            [
                f"group_id: {group_meta.get('group_id')}",
                f"group_index: {group_meta.get('group_index')}/{group_meta.get('total_groups')}",
                f"same_visual_dna_rule: {_safe_line(continuity_context.get('same_visual_dna_rule'))}",
                f"next_group_hook: {_safe_line(continuity_context.get('next_group_hook'))}",
            ],
        ),
        _bullet_block(
            "Type pack",
            [
                f"active_packs: {', '.join(str(item) for item in type_stack_ref.get('active_packs', []))}",
                f"image_generation_projection: {_safe_line(image_projection)}",
            ],
        ),
        _bullet_block(
            "Type pack control surface",
            [str(item) for item in type_pack_context.get("control_surface_digest", [])[:8]],
        ),
        _bullet_block(
            "Style bible",
            [
                f"base_style: {_safe_line(style_bible.get('base_style'))}",
                f"rendering_medium: {_safe_line(style_bible.get('rendering_medium'))}",
                f"layout_directive: {_safe_line(style_bible.get('layout_directive'))}",
            ],
        ),
        _bullet_block(
            "Main character lock",
            [seedream_runner._summarize_lock(main_character_lock, include_id=True)],
        ),
        _bullet_block(
            "Scene continuity",
            [
                f"default_rule: {_safe_line(scene_bible.get('default_rule'))}",
                seedream_runner._summarize_lock(scene_lock, include_id=True),
            ],
        ),
        _bullet_block(
            "Active character locks",
            [
                seedream_runner._summarize_lock(character_map[character_id], include_id=True)
                for character_id in active_character_ids
                if character_id in character_map
            ],
        ),
        _bullet_block(
            f"Page {page_number} contract",
            [
                f"page_role: {page_role}",
                f"source_fragment: {_safe_line(page.get('source_fragment'))}",
                f"layout: {_safe_line(page.get('layout'))}",
                "page_number_overlay: "
                f"text={_safe_line(page_number_overlay.get('text'))}; "
                f"position={_safe_line(page_number_overlay.get('position'))}; "
                f"style={_safe_line(page_number_overlay.get('style_prompt'))}",
                f"positive_prompt: {_safe_line(page.get('positive_prompt'))}",
            ],
        ),
        _bullet_block(
            "Panels and text slots",
            [seedream_runner._summarize_panel(panel) for panel in page.get("panels", []) if seedream_runner._summarize_panel(panel)],
        ),
        _bullet_block(
            "Hard constraints",
            [
                "Keep multiple comic panels on the page with a clear reading path.",
                f"Place page number {page_number} in the bottom-right corner, digits only.",
                "Render clear legible Chinese text where text slots require it.",
                "Do not switch character faces, costumes, scene geography, or rendering medium.",
            ],
        ),
        f"Negative prompt: {_safe_line(data.get('global_negative_prompt'))}",
    ]
    return "\n\n".join(section for section in prompt_sections if section)


def _latest_download(download_dir: Path, before: set[Path]) -> Path | None:
    files = [path for path in download_dir.iterdir() if path.is_file()]
    image_candidates = [path for path in files if path.suffix.lower() in IMAGE_SUFFIXES]
    if image_candidates:
        new_images = [path for path in image_candidates if path not in before]
        candidates = new_images or image_candidates
        return max(candidates, key=lambda item: item.stat().st_mtime)
    if files:
        new_files = [path for path in files if path not in before]
        candidates = new_files or files
        return max(candidates, key=lambda item: item.stat().st_mtime)
    return None


def _canonicalize_download(source: Path, target: Path) -> None:
    target.parent.mkdir(parents=True, exist_ok=True)
    if target.exists():
        target.unlink()
    source.replace(target)


def _load_json(path: Path) -> dict[str, Any]:
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError("root must be a JSON object")
    return normalize_nine_blade_prompt_data(data)


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Legacy fallback: generate nine comic pages with Dreamina CLI"
    )
    parser.add_argument("json_path", nargs="?", type=Path)
    parser.add_argument("--output-dir", type=Path)
    parser.add_argument("--project-name")
    parser.add_argument("--resolution-type", default="2k")
    parser.add_argument("--model-version")
    parser.add_argument("--submit-poll", type=int, default=3)
    parser.add_argument("--query-interval", type=int, default=20)
    parser.add_argument("--query-timeout", type=int, default=1200)
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--execute", action="store_true")
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()

    if args.self_test:
        sample = seedream_runner._self_test_data()
        prompts = [_summarize_page_prompt(sample, page) for page in sample.get("pages", [])]
        required = [
            "Generate one complete vertical 9:16 comic page",
            "Type pack control surface",
            "Main character lock",
            "Scene continuity",
            "Hard constraints",
            "bottom-right corner",
        ]
        if len(prompts) != 9:
            print("FAIL self-test: expected 9 prompts", file=sys.stderr)
            return 1
        missing = [needle for needle in required if not all(needle in prompt for prompt in prompts)]
        if missing:
            print(f"FAIL self-test missing: {missing}", file=sys.stderr)
            return 1
        print("PASS self-test")
        return 0

    if args.json_path is None:
        parser.error("json_path is required unless --self-test is used")
    if args.dry_run and args.execute:
        parser.error("choose only one of --dry-run or --execute")
    if not args.dry_run and not args.execute:
        parser.error("pass --dry-run or --execute")

    json_path = args.json_path.resolve()
    validator_result = _run_validator(json_path)
    if validator_result.returncode != 0:
        print(validator_result.stdout, end="")
        print(validator_result.stderr, end="", file=sys.stderr)
        return validator_result.returncode

    data = _load_json(json_path)
    pages = data.get("pages", [])
    if not isinstance(pages, list) or len(pages) != 9:
        print("FAIL: input JSON must contain exactly 9 pages", file=sys.stderr)
        return 2

    group_slug = seedream_runner._derive_group_slug(data, json_path)
    page_group = seedream_runner._group_meta(data)
    project_root = seedream_runner._infer_project_root(json_path, args.project_name)
    output_dir = args.output_dir.resolve() if args.output_dir else (project_root / "3-漫画生成" / group_slug / "dreamina-cli")
    output_dir.mkdir(parents=True, exist_ok=True)
    downloads_root = output_dir / "_downloads"
    downloads_root.mkdir(parents=True, exist_ok=True)

    plan_path = output_dir / f"{group_slug}-dreamina_generation_plan.json"
    report_path = output_dir / f"{group_slug}-dreamina_generation_report.json"
    queue_path = output_dir / f"{group_slug}-dreamina_queue.md"

    page_prompts: list[dict[str, Any]] = []
    for index, page in enumerate(pages, start=1):
        prompt = _summarize_page_prompt(data, page)
        prompt_path = output_dir / f"page{index:02d}-dreamina_prompt.txt"
        prompt_path.write_text(prompt, encoding="utf-8")
        page_prompts.append(
            {
                "page_number": index,
                "prompt_path": str(prompt_path),
                "prompt_preview": prompt[:240],
            }
        )

    plan = {
        "ok": True,
        "input_json": str(json_path),
        "page_group": page_group,
        "group_slug": group_slug,
        "output_dir": str(output_dir),
        "queue_path": str(queue_path),
        "report_path": str(report_path),
        "resolution_type": args.resolution_type,
        "model_version": args.model_version or "default",
        "submit_poll": args.submit_poll,
        "query_interval": args.query_interval,
        "query_timeout": args.query_timeout,
        "pages": page_prompts,
    }
    _write_json(plan_path, plan)

    queue_rows = [
        {
            "queue_id": f"Q-{index:03d}",
            "page_number": index,
            "submit_id": "",
            "local_status": "planned",
            "remote_status": "not_submitted",
            "created_at": _timestamp(),
            "last_checked_at": "",
            "next_action": "submit dreamina text2image",
            "output_file": "",
            "notes": "",
        }
        for index in range(1, 10)
    ]
    _write_queue(queue_path, queue_rows)

    pending_report = {
        "ok": False,
        "status": "pending",
        "input_json": str(json_path),
        "page_group": page_group,
        "group_slug": group_slug,
        "output_dir": str(output_dir),
        "plan_path": str(plan_path),
        "queue_path": str(queue_path),
        "pages": queue_rows,
    }
    _write_json(report_path, pending_report)

    if args.dry_run:
        print(f"PASS dry-run: {plan_path}")
        return 0

    completed = 0
    for index, page in enumerate(pages, start=1):
        prompt_path = output_dir / f"page{index:02d}-dreamina_prompt.txt"
        prompt = prompt_path.read_text(encoding="utf-8")
        submit_cmd = [
            "dreamina",
            "text2image",
            f"--prompt={prompt}",
            "--ratio=9:16",
            f"--resolution_type={args.resolution_type}",
            f"--poll={args.submit_poll}",
        ]
        if args.model_version:
            submit_cmd.append(f"--model_version={args.model_version}")

        queue_rows[index - 1]["local_status"] = "submitting"
        queue_rows[index - 1]["last_checked_at"] = _timestamp()
        queue_rows[index - 1]["next_action"] = "capture submit_id"
        _write_queue(queue_path, queue_rows)

        submit_payload, submit_raw = _run_command(submit_cmd)
        submit_id = _extract_submit_id(submit_payload, submit_raw)
        if not submit_id:
            queue_rows[index - 1]["local_status"] = "failed"
            queue_rows[index - 1]["remote_status"] = "submit_failed"
            queue_rows[index - 1]["notes"] = "missing submit_id"
            _write_queue(queue_path, queue_rows)
            _write_json(report_path, {**pending_report, "status": "failed", "pages": queue_rows})
            print(f"FAIL: missing submit_id for page {index}", file=sys.stderr)
            return 3

        queue_rows[index - 1]["submit_id"] = submit_id
        queue_rows[index - 1]["remote_status"] = _extract_status(submit_payload, submit_raw)
        queue_rows[index - 1]["local_status"] = "submitted"
        queue_rows[index - 1]["last_checked_at"] = _timestamp()
        queue_rows[index - 1]["next_action"] = "query_result and download"
        _write_queue(queue_path, queue_rows)

        download_dir = downloads_root / f"page{index:02d}"
        download_dir.mkdir(parents=True, exist_ok=True)
        started_at = time.time()
        final_file = None
        page_status = "querying"
        while time.time() - started_at <= args.query_timeout:
            before = {path for path in download_dir.iterdir() if path.is_file()}
            payload, raw_text = _run_command(
                [
                    "dreamina",
                    "query_result",
                    f"--submit_id={submit_id}",
                    f"--download_dir={download_dir}",
                ]
            )
            page_status = _extract_status(payload, raw_text)
            queue_rows[index - 1]["remote_status"] = page_status
            queue_rows[index - 1]["last_checked_at"] = _timestamp()

            latest = _latest_download(download_dir, before)
            if latest is not None and latest.stat().st_size > 0:
                canonical = output_dir / f"page{index:02d}{latest.suffix.lower() or '.png'}"
                _canonicalize_download(latest, canonical)
                final_file = canonical
                page_status = "success"
                break

            if page_status == "failed":
                break

            queue_rows[index - 1]["local_status"] = "querying"
            queue_rows[index - 1]["next_action"] = f"sleep {args.query_interval}s then query again"
            _write_queue(queue_path, queue_rows)
            time.sleep(args.query_interval)

        if final_file is None and page_status != "failed":
            queue_rows[index - 1]["local_status"] = "timed_out"
            queue_rows[index - 1]["remote_status"] = page_status
            queue_rows[index - 1]["next_action"] = "manual follow-up with query_result"
            queue_rows[index - 1]["notes"] = f"query timeout after {args.query_timeout}s"
            _write_queue(queue_path, queue_rows)
            _write_json(report_path, {**pending_report, "status": "timed_out", "pages": queue_rows})
            print(f"FAIL: timed out while waiting for page {index}", file=sys.stderr)
            return 4

        if final_file is None:
            queue_rows[index - 1]["local_status"] = "failed"
            queue_rows[index - 1]["next_action"] = "inspect remote task or retry"
            queue_rows[index - 1]["notes"] = "remote task failed"
            _write_queue(queue_path, queue_rows)
            _write_json(report_path, {**pending_report, "status": "failed", "pages": queue_rows})
            print(f"FAIL: Dreamina failed on page {index}", file=sys.stderr)
            return 5

        queue_rows[index - 1]["local_status"] = "downloaded"
        queue_rows[index - 1]["remote_status"] = "success"
        queue_rows[index - 1]["output_file"] = str(final_file)
        queue_rows[index - 1]["next_action"] = "completed"
        queue_rows[index - 1]["notes"] = ""
        _write_queue(queue_path, queue_rows)
        completed += 1

    final_report = {
        "ok": completed == 9,
        "status": "completed" if completed == 9 else "partial",
        "input_json": str(json_path),
        "page_group": page_group,
        "group_slug": group_slug,
        "output_dir": str(output_dir),
        "plan_path": str(plan_path),
        "queue_path": str(queue_path),
        "completed_pages": completed,
        "saved_files": [row["output_file"] for row in queue_rows if row.get("output_file")],
        "pages": queue_rows,
    }
    _write_json(report_path, final_report)
    print(f"PASS generated 9 Dreamina comic pages: {report_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
