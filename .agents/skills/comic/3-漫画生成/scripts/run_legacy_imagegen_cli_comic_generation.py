#!/usr/bin/env python3
"""Legacy external CLI imagegen runner for a 9-page comic group.

This runner is preserved only for explicitly requested external CLI/API work.
It is not the active `comic-generation` route because `.agents/skills/cli/imagegen`
now means the built-in image_gen tool only. The script validates stage-2 JSON,
projects each page into one legacy CLI job, writes evidence files, and can invoke
the shared `.agents/skills/cli/imagegen/scripts/image_gen.py` CLI only after an
explicit legacy acknowledgement. It does not rewrite story, panel, character, or
scene truth.
"""

from __future__ import annotations

import argparse
from datetime import datetime
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[5]
SCRIPT_DIR = Path(__file__).resolve().parent
IMAGEGEN_CLI = REPO_ROOT / ".agents/skills/cli/imagegen/scripts/image_gen.py"

if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

import run_seedream_comic_generation as legacy_helpers


def _now_stamp() -> str:
    return datetime.now().strftime("%Y%m%d_%H%M%S")


def _write_json(path: Path, payload: dict[str, Any]) -> None:
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")


def _write_jsonl(path: Path, rows: list[dict[str, Any]]) -> None:
    path.write_text(
        "".join(json.dumps(row, ensure_ascii=False) + "\n" for row in rows),
        encoding="utf-8",
    )


def _page_number(page: dict[str, Any], fallback: int) -> int:
    try:
        return int(page.get("page_number", fallback))
    except (TypeError, ValueError):
        return fallback


def compile_page_prompt(data: dict[str, Any], page: dict[str, Any], fallback_index: int) -> str:
    """Project one upstream page object into one CLI imagegen prompt."""
    page_group = data.get("page_group", {})
    continuity_context = data.get("continuity_context", {})
    contract = data.get("generation_contract", {})
    type_stack_ref = data.get("type_stack_ref", {})
    type_pack_context = data.get("type_pack_context", {})
    style_bible = data.get("style_bible", {})
    main_character_lock = data.get("main_character_lock", {})
    scene_bible = data.get("scene_continuity_bible", {})
    comic_text_system = data.get("comic_text_system", {})
    hard_constraints = contract.get("hard_constraints", [])
    negative = data.get("global_negative_prompt", "")
    character_map = legacy_helpers._character_map(data)
    scene_map = legacy_helpers._scene_map(data)

    page_no = _page_number(page, fallback_index)
    active_character_ids = page.get("active_character_ids", [])
    if not isinstance(active_character_ids, list):
        active_character_ids = []
    scene_id = str(page.get("scene_id", "")).strip()
    layout = page.get("layout", {})
    panels = page.get("panels", [])
    page_number_overlay = page.get("page_number_overlay", {})
    active_character_locks = [
        character_map[character_id]
        for character_id in active_character_ids
        if character_id in character_map
    ]
    scene_lock = scene_map.get(scene_id, {})

    sections = [
        (
            f"CLI imagegen execution for Page {page_no}: generate exactly one complete "
            "vertical 9:16 comic page for this job, not the full 9-page set. Do not "
            "create a collage, contact sheet, or variants sheet. Keep multiple comic "
            f"panels and place a small bottom-right page number using the exact digit {page_no}."
        ),
        legacy_helpers._bullet_block(
            "Page Group Meta",
            [
                f"group_id: {page_group.get('group_id')}",
                f"group_index: {page_group.get('group_index')}/{page_group.get('total_groups')}",
                f"source_span_summary: {legacy_helpers._compact_text(page_group.get('source_span_summary'))}",
                f"rhythm_rationale: {legacy_helpers._compact_text(page_group.get('rhythm_rationale'))}",
            ],
        ),
        legacy_helpers._bullet_block(
            "Continuity Context",
            [
                f"inherit_global_locks: {continuity_context.get('inherit_global_locks')}",
                f"same_visual_dna_rule: {legacy_helpers._compact_text(continuity_context.get('same_visual_dna_rule'))}",
                f"previous_group_hook: {legacy_helpers._compact_text(continuity_context.get('previous_group_hook'))}",
                f"next_group_hook: {legacy_helpers._compact_text(continuity_context.get('next_group_hook'))}",
            ],
        ),
        legacy_helpers._bullet_block(
            "Type Stack Ref",
            [
                f"method_kernel: {type_stack_ref.get('method_kernel')}",
                f"active_packs: {', '.join(str(item) for item in type_stack_ref.get('active_packs', []))}",
            ],
        ),
        legacy_helpers._bullet_block(
            "Type Pack Context",
            legacy_helpers._summarize_type_pack_context(type_pack_context),
        ),
        legacy_helpers._bullet_block(
            "Type Pack Control Surface",
            legacy_helpers._summarize_control_surface(type_pack_context),
        ),
        legacy_helpers._bullet_block(
            "Global Style Bible",
            legacy_helpers._summarize_style_bible(style_bible),
        ),
        legacy_helpers._bullet_block(
            "Main Character Lock",
            [legacy_helpers._summarize_lock(main_character_lock, include_id=True)],
        ),
        legacy_helpers._bullet_block(
            "Active Character Locks",
            [
                legacy_helpers._summarize_lock(lock, include_id=True)
                for lock in active_character_locks
            ],
        ),
        legacy_helpers._bullet_block(
            "Scene Continuity",
            [
                f"default_rule: {legacy_helpers._compact_text(scene_bible.get('default_rule'))}",
                legacy_helpers._summarize_lock(scene_lock, include_id=True),
            ],
        ),
        legacy_helpers._bullet_block(
            "Comic Text System",
            legacy_helpers._summarize_text_system(comic_text_system),
        ),
        legacy_helpers._bullet_block(
            f"Page {page_no} Source Truth",
            [
                f"page_role: {legacy_helpers._compact_text(page.get('page_role'))}",
                f"source_fragment: {legacy_helpers._compact_text(page.get('source_fragment'))}",
                f"active_character_ids: {', '.join(str(item) for item in active_character_ids)}",
                f"scene_id: {scene_id}",
                f"layout_id: {legacy_helpers._compact_text(layout.get('layout_id'))}",
                f"panel_count: {layout.get('panel_count')}",
                f"page_number_overlay: text={legacy_helpers._compact_text(page_number_overlay.get('text'))}; "
                f"position={legacy_helpers._compact_text(page_number_overlay.get('position'))}; "
                f"style={legacy_helpers._compact_text(page_number_overlay.get('style_prompt'))}",
            ],
        ),
        legacy_helpers._bullet_block(
            "Panels And Text Slots",
            [
                legacy_helpers._summarize_panel(panel)
                for panel in panels
                if legacy_helpers._summarize_panel(panel)
            ],
        ),
        legacy_helpers._text_block("Original Positive Prompt", page.get("positive_prompt", "")),
        legacy_helpers._bullet_block("Hard Constraints", [str(item) for item in hard_constraints]),
        legacy_helpers._bullet_block("Global Negative Prompt", [negative]),
        (
            "Final CLI job constraint: one image only; vertical 9:16; multi-panel comic page; "
            "not a nine-grid; not a contact sheet; not a single poster illustration; preserve "
            f"character and scene continuity; bottom-right page number must be the digit {page_no}."
        ),
    ]
    return "\n".join(section for section in sections if section)


def compile_page_prompts(data: dict[str, Any]) -> list[dict[str, Any]]:
    pages = data.get("pages", [])
    if not isinstance(pages, list) or len(pages) != 9:
        raise ValueError("expected exactly 9 pages in normalized JSON")
    return [
        {
            "page_number": _page_number(page, index),
            "prompt": compile_page_prompt(data, page, index),
        }
        for index, page in enumerate(pages, start=1)
    ]


def _output_dir_for(args: argparse.Namespace, json_path: Path, data: dict[str, Any]) -> Path:
    project_root = legacy_helpers._infer_project_root(json_path, args.project_name)
    group_slug = legacy_helpers._derive_group_slug(data, json_path)
    if args.output_dir:
        return args.output_dir.resolve()
    return project_root / "3-漫画生成" / group_slug / "legacy-imagegen-cli"


def _filename_prefix(args: argparse.Namespace, output_dir: Path, group_slug: str) -> str:
    if args.filename_prefix:
        return args.filename_prefix
    if output_dir.parent.name != group_slug:
        return f"{group_slug}-page"
    return "page"


def _expected_files(output_dir: Path, prefix: str, output_format: str) -> list[str]:
    return [str(output_dir / f"{prefix}{index:02d}.{output_format}") for index in range(1, 10)]


def _build_jobs(
    page_prompts: list[dict[str, Any]],
    *,
    prefix: str,
    model: str,
    size: str,
    quality: str,
    output_format: str,
) -> list[dict[str, Any]]:
    return [
        {
            "prompt": item["prompt"],
            "out": f"{prefix}{int(item['page_number']):02d}.{output_format}",
            "model": model,
            "size": size,
            "quality": quality,
            "output_format": output_format,
            "n": 1,
        }
        for item in page_prompts
    ]


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Legacy external CLI/API runner for one 9-page comic group"
    )
    parser.add_argument("json_path", nargs="?", type=Path)
    parser.add_argument("--output-dir", type=Path)
    parser.add_argument("--project-name")
    parser.add_argument("--filename-prefix")
    parser.add_argument("--model", default="gpt-image-2")
    parser.add_argument("--size", default="1152x2048")
    parser.add_argument("--quality", default="medium")
    parser.add_argument("--output-format", default="png")
    parser.add_argument("--concurrency", type=int, default=3)
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--execute", action="store_true")
    parser.add_argument("--ack-legacy-cli", action="store_true")
    parser.add_argument("--force", action="store_true")
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()

    if args.self_test:
        sample = legacy_helpers._self_test_data()
        prompts = compile_page_prompts(sample)
        required = [
            "CLI imagegen execution for Page 1",
            "Type Pack Control Surface",
            "Original Positive Prompt",
            "bottom-right page number",
            "not a nine-grid",
        ]
        combined = "\n".join(item["prompt"] for item in prompts)
        missing = [text for text in required if text not in combined]
        if len(prompts) != 9 or missing:
            print(f"FAIL self-test missing: {missing}", file=sys.stderr)
            return 1
        with tempfile.TemporaryDirectory() as tmp_dir:
            tmp = Path(tmp_dir)
            jobs = _build_jobs(
                prompts,
                prefix="page",
                model=args.model,
                size=args.size,
                quality=args.quality,
                output_format=args.output_format,
            )
            _write_jsonl(tmp / "imagegen_jobs.jsonl", jobs)
            if len((tmp / "imagegen_jobs.jsonl").read_text(encoding="utf-8").splitlines()) != 9:
                print("FAIL self-test JSONL job count", file=sys.stderr)
                return 1
        print("PASS self-test")
        return 0

    if args.json_path is None:
        parser.error("json_path is required unless --self-test is used")
    if args.dry_run and args.execute:
        print("FAIL: choose only one of --dry-run or --execute", file=sys.stderr)
        return 2
    if not args.dry_run and not args.execute:
        print("FAIL: pass --dry-run or --execute", file=sys.stderr)
        return 2

    json_path = args.json_path.resolve()
    validator_result = legacy_helpers._run_validator(json_path)
    if validator_result.returncode != 0:
        print(validator_result.stdout, end="")
        print(validator_result.stderr, end="", file=sys.stderr)
        return validator_result.returncode

    data = legacy_helpers._load_json(json_path)
    page_prompts = compile_page_prompts(data)
    page_group = legacy_helpers._group_meta(data)
    group_slug = legacy_helpers._derive_group_slug(data, json_path)
    output_dir = _output_dir_for(args, json_path, data)
    output_dir.mkdir(parents=True, exist_ok=True)
    prefix = _filename_prefix(args, output_dir, group_slug)

    prompt_paths: list[str] = []
    for item in page_prompts:
        page_no = int(item["page_number"])
        prompt_path = output_dir / f"{prefix}{page_no:02d}-imagegen_prompt.txt"
        prompt_path.write_text(item["prompt"], encoding="utf-8")
        prompt_paths.append(str(prompt_path))

    jobs_path = output_dir / "imagegen_jobs.jsonl"
    generation_plan_path = output_dir / "imagegen_generation_plan.json"
    comic_report_path = output_dir / "comic_generation_report.json"
    expected_files = _expected_files(output_dir, prefix, args.output_format)
    jobs = _build_jobs(
        page_prompts,
        prefix=prefix,
        model=args.model,
        size=args.size,
        quality=args.quality,
        output_format=args.output_format,
    )
    _write_jsonl(jobs_path, jobs)

    command = [
        sys.executable,
        str(IMAGEGEN_CLI),
        "generate-batch",
        "--input",
        str(jobs_path),
        "--out-dir",
        str(output_dir),
        "--model",
        args.model,
        "--size",
        args.size,
        "--quality",
        args.quality,
        "--output-format",
        args.output_format,
        "--concurrency",
        str(args.concurrency),
        "--no-augment",
    ]
    if args.force:
        command.append("--force")

    plan = {
        "ok": True,
        "created_at": _now_stamp(),
        "input_json": str(json_path),
        "page_group": page_group,
        "group_slug": group_slug,
        "provider": "legacy-cli-imagegen",
        "runtime": {
            "skill_path": ".agents/skills/cli/imagegen",
            "script": str(IMAGEGEN_CLI),
            "subcommand": "generate-batch",
            "model": args.model,
            "size": args.size,
            "quality": args.quality,
            "output_format": args.output_format,
            "concurrency": args.concurrency,
            "augment": False,
        },
        "output_dir": str(output_dir),
        "jobs_jsonl": str(jobs_path),
        "prompt_paths": prompt_paths,
        "expected_files": expected_files,
        "filename_scheme": f"{prefix}01.png .. {prefix}09.png",
        "command_preview": command,
    }
    _write_json(generation_plan_path, plan)

    pending_report = {
        "ok": False,
        "status": "planned",
        "mode": "dry-run" if args.dry_run else "execute",
        "input_json": str(json_path),
        "page_group": page_group,
        "group_slug": group_slug,
        "provider": "legacy-cli-imagegen",
        "runtime": plan["runtime"],
        "output_dir": str(output_dir),
        "paths": {
            "generation_plan": str(generation_plan_path),
            "jobs_jsonl": str(jobs_path),
        },
        "filename_scheme": plan["filename_scheme"],
        "expected_result_count": 9,
        "saved_files": [],
        "validation": {
            "json_validator": "pass",
            "job_count": len(jobs),
            "cli_exit_code": None,
        },
        "review": {
            "verdict": "pass_with_todo" if args.dry_run else "pending",
            "notes": [],
        },
    }

    if args.dry_run:
        _write_json(comic_report_path, {**pending_report, "ok": True, "status": "planned"})
        print(f"PASS dry-run: {generation_plan_path}")
        return 0

    if not args.ack_legacy_cli:
        _write_json(
            comic_report_path,
            {
                **pending_report,
                "status": "blocked",
                "error": "legacy CLI execute requires --ack-legacy-cli",
                "review": {"verdict": "blocked", "notes": ["legacy CLI route not acknowledged"]},
            },
        )
        print("FAIL: pass --ack-legacy-cli to use this external legacy route", file=sys.stderr)
        return 2

    if not os.getenv("OPENAI_API_KEY"):
        _write_json(
            comic_report_path,
            {
                **pending_report,
                "status": "blocked",
                "error": "OPENAI_API_KEY is not set; legacy CLI imagegen execute requires it.",
                "review": {"verdict": "blocked", "notes": ["missing OPENAI_API_KEY"]},
            },
        )
        print("FAIL: OPENAI_API_KEY is not set", file=sys.stderr)
        return 2

    result = subprocess.run(command, cwd=str(REPO_ROOT), text=True, check=False)
    existing_files = [path for path in expected_files if Path(path).is_file()]
    ok = result.returncode == 0 and len(existing_files) == 9
    report = {
        **pending_report,
        "ok": ok,
        "status": "generated" if ok else "failed",
        "saved_files": existing_files,
        "validation": {
            "json_validator": "pass",
            "job_count": len(jobs),
            "cli_exit_code": result.returncode,
            "file_count": len(existing_files),
        },
        "review": {
            "verdict": "pass" if ok else "needs_rework",
            "notes": [] if ok else ["CLI exited non-zero or did not create 9 expected PNG files"],
        },
    }
    _write_json(comic_report_path, report)
    if not ok:
        print("FAIL: CLI imagegen did not create 9 expected PNG files", file=sys.stderr)
        return result.returncode or 1
    print(f"PASS generated 9 comic pages: {comic_report_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
