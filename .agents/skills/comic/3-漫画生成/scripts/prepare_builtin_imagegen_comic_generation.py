#!/usr/bin/env python3
"""Prepare built-in image_gen handoff prompts for a 9-page comic group.

This runner is mechanical: it validates the stage-2 JSON, projects each page
into one built-in image_gen prompt, and writes handoff evidence files. It does
not call the built-in image_gen tool, local CLI scripts, or external APIs.
Actual image creation is performed by the agent through `.agents/skills/cli/imagegen`.
"""

from __future__ import annotations

import argparse
from datetime import datetime
import json
from pathlib import Path
import sys
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[5]
SCRIPT_DIR = Path(__file__).resolve().parent

if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

# This module still owns shared mechanical helpers for loading and summarizing
# nine_blade_comic_prompts.v1 JSON. Its legacy generation routes are not used.
import run_seedream_comic_generation as legacy_helpers


def _now_stamp() -> str:
    return datetime.now().strftime("%Y%m%d_%H%M%S")


def _write_json(path: Path, payload: dict[str, Any]) -> None:
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")


def _page_number(page: dict[str, Any], fallback: int) -> int:
    try:
        return int(page.get("page_number", fallback))
    except (TypeError, ValueError):
        return fallback


def compile_page_prompt(
    data: dict[str, Any],
    page: dict[str, Any],
    fallback_index: int,
    *,
    resolution_value: str,
) -> str:
    """Project one upstream page object into one built-in image_gen prompt."""
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
            f"Built-in image_gen request for Page {page_no}: generate exactly one complete "
            "vertical 9:16 comic page as this single image asset, not the full 9-page set. "
            "Do not create a collage, contact sheet, or variants sheet. Keep multiple comic "
            f"panels and place a small bottom-right page number using the exact digit {page_no}. "
            f"Target {resolution_value} delivery quality for this 9:16 page."
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
            "Final built-in image_gen constraint: one image asset only; vertical 9:16; "
            "multi-panel comic page; not a nine-grid; not a contact sheet; not a single poster "
            "illustration; preserve character and scene continuity; bottom-right page number "
            f"must be the digit {page_no}."
        ),
    ]
    return "\n".join(section for section in sections if section)


def compile_page_prompts(
    data: dict[str, Any],
    *,
    resolution_value: str,
) -> list[dict[str, Any]]:
    pages = data.get("pages", [])
    if not isinstance(pages, list) or len(pages) != 9:
        raise ValueError("expected exactly 9 pages in normalized JSON")
    return [
        {
            "page_number": _page_number(page, index),
            "prompt": compile_page_prompt(
                data,
                page,
                index,
                resolution_value=resolution_value,
            ),
        }
        for index, page in enumerate(pages, start=1)
    ]


def _contract_imagegen(data: dict[str, Any]) -> dict[str, Any]:
    contract = data.get("generation_contract", {})
    if not isinstance(contract, dict):
        return {}
    imagegen = contract.get("imagegen", {})
    return imagegen if isinstance(imagegen, dict) else {}


def _output_dir_for(args: argparse.Namespace, json_path: Path, data: dict[str, Any]) -> Path:
    project_root = legacy_helpers._infer_project_root(json_path, args.project_name)
    group_slug = legacy_helpers._derive_group_slug(data, json_path)
    if args.output_dir:
        return args.output_dir.resolve()
    return project_root / "3-漫画生成" / group_slug / "built-in-imagegen"


def _filename_prefix(args: argparse.Namespace, output_dir: Path, group_slug: str) -> str:
    if args.filename_prefix:
        return args.filename_prefix
    if output_dir.parent.name != group_slug:
        return f"{group_slug}-page"
    return "page"


def _expected_files(output_dir: Path, prefix: str, output_format: str) -> list[str]:
    return [str(output_dir / f"{prefix}{index:02d}.{output_format}") for index in range(1, 10)]


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Prepare 9 built-in image_gen handoff prompts for one comic page group"
    )
    parser.add_argument("json_path", nargs="?", type=Path)
    parser.add_argument("--output-dir", type=Path)
    parser.add_argument("--project-name")
    parser.add_argument("--filename-prefix")
    parser.add_argument("--resolution-target", choices=["2k_default", "explicit_user_or_upstream"], default=None)
    parser.add_argument("--resolution-value", default=None)
    parser.add_argument("--output-format", default="png")
    parser.add_argument("--max-concurrency", type=int, default=9)
    parser.add_argument("--dry-run", action="store_true", help="Compatibility alias for the default planning mode")
    parser.add_argument("--execute", action="store_true", help="Write a blocked report; scripts cannot invoke built-in image_gen")
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()

    if args.max_concurrency < 1 or args.max_concurrency > 10:
        print("FAIL: --max-concurrency must be between 1 and 10", file=sys.stderr)
        return 2
    if args.dry_run and args.execute:
        print("FAIL: choose only one of --dry-run or --execute", file=sys.stderr)
        return 2

    if args.self_test:
        sample = legacy_helpers._self_test_data()
        resolution_value = args.resolution_value or "2K"
        prompts = compile_page_prompts(sample, resolution_value=resolution_value)
        required = [
            "Built-in image_gen request for Page 1",
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
        print("PASS self-test")
        return 0

    if args.json_path is None:
        parser.error("json_path is required unless --self-test is used")

    json_path = args.json_path.resolve()
    validator_result = legacy_helpers._run_validator(json_path)
    if validator_result.returncode != 0:
        print(validator_result.stdout, end="")
        print(validator_result.stderr, end="", file=sys.stderr)
        return validator_result.returncode

    data = legacy_helpers._load_json(json_path)
    imagegen_contract = _contract_imagegen(data)
    resolution_target = (
        args.resolution_target
        or str(imagegen_contract.get("resolution_target") or "2k_default")
    )
    resolution_value = (
        args.resolution_value
        or str(imagegen_contract.get("resolution_value") or "2K")
    )
    output_format = args.output_format or str(imagegen_contract.get("output_format") or "png")
    page_prompts = compile_page_prompts(data, resolution_value=resolution_value)
    page_group = legacy_helpers._group_meta(data)
    group_slug = legacy_helpers._derive_group_slug(data, json_path)
    output_dir = _output_dir_for(args, json_path, data)
    output_dir.mkdir(parents=True, exist_ok=True)
    prefix = _filename_prefix(args, output_dir, group_slug)

    prompt_paths: list[str] = []
    prompt_entries: list[dict[str, Any]] = []
    expected_files = _expected_files(output_dir, prefix, output_format)
    for item in page_prompts:
        page_no = int(item["page_number"])
        prompt_path = output_dir / f"{prefix}{page_no:02d}-imagegen_prompt.txt"
        prompt_path.write_text(item["prompt"], encoding="utf-8")
        prompt_paths.append(str(prompt_path))
        prompt_entries.append(
            {
                "label": f"{prefix}{page_no:02d}",
                "page_number": page_no,
                "prompt_path": str(prompt_path),
                "final_filename": f"{prefix}{page_no:02d}.{output_format}",
                "prompt": item["prompt"],
            }
        )

    prompt_set_path = output_dir / "imagegen_prompt_set.json"
    handoff_plan_path = output_dir / "imagegen_handoff_plan.json"
    comic_report_path = output_dir / "comic_generation_report.json"

    runtime = {
        "skill_path": ".agents/skills/cli/imagegen",
        "mode": "built_in_image_gen",
        "batch_execution": "subagents_parallel_default",
        "max_concurrency": args.max_concurrency,
        "resolution_target": resolution_target,
        "resolution_value": resolution_value,
        "output_format": output_format,
        "script_invokes_imagegen": False,
    }
    prompt_set = {
        "ok": True,
        "created_at": _now_stamp(),
        "input_json": str(json_path),
        "group_slug": group_slug,
        "provider": "built-in-imagegen",
        "runtime": runtime,
        "prompts": prompt_entries,
    }
    _write_json(prompt_set_path, prompt_set)

    plan = {
        "ok": True,
        "created_at": _now_stamp(),
        "input_json": str(json_path),
        "page_group": page_group,
        "group_slug": group_slug,
        "provider": "built-in-imagegen",
        "runtime": runtime,
        "output_dir": str(output_dir),
        "prompt_set": str(prompt_set_path),
        "prompt_paths": prompt_paths,
        "expected_files": expected_files,
        "filename_scheme": f"{prefix}01.{output_format} .. {prefix}09.{output_format}",
        "agent_handoff": (
            "Use `.agents/skills/cli/imagegen` built-in image_gen mode. Generate one image "
            "per prompt, defaulting to subagents parallel fan-out capped at 10, then copy or "
            "move each selected final into this output_dir using the expected filenames."
        ),
    }
    _write_json(handoff_plan_path, plan)

    blocked_execute = bool(args.execute)
    report = {
        "ok": not blocked_execute,
        "status": "blocked" if blocked_execute else "planned",
        "mode": "built-in-plan" if not blocked_execute else "blocked-script-execute",
        "input_json": str(json_path),
        "page_group": page_group,
        "group_slug": group_slug,
        "provider": "built-in-imagegen",
        "runtime": runtime,
        "output_dir": str(output_dir),
        "paths": {
            "handoff_plan": str(handoff_plan_path),
            "prompt_set": str(prompt_set_path),
        },
        "filename_scheme": plan["filename_scheme"],
        "expected_result_count": 9,
        "saved_files": [],
        "validation": {
            "json_validator": "pass",
            "prompt_count": len(prompt_entries),
            "built_in_tool_invoked_by_script": False,
        },
        "review": {
            "verdict": "blocked" if blocked_execute else "pass_with_todo",
            "notes": [
                "scripts cannot invoke built-in image_gen; run generation through the agent/tool handoff"
            ]
            if blocked_execute
            else ["handoff plan ready; generated images still need built-in image_gen execution"],
        },
    }
    _write_json(comic_report_path, report)

    if blocked_execute:
        print("FAIL: built-in image_gen execution cannot be launched from this script", file=sys.stderr)
        print(f"WROTE blocked handoff report: {comic_report_path}")
        return 2

    print(f"PASS built-in image_gen handoff plan: {handoff_plan_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
