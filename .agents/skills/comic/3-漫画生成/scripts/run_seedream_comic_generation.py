#!/usr/bin/env python3
"""Compile nine_blade_comic_prompts.v1 JSON and run Seedream once for 9 comic pages."""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from datetime import datetime
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[5]
VALIDATOR = REPO_ROOT / ".agents/skills/comic/2-九刀流漫画提示词/scripts/validate_nine_blade_prompt_json.py"
SEEDREAM_SCRIPT = REPO_ROOT / ".agents/skills/api/image/seedream/scripts/seedream_generate.py"


def _now_stamp() -> str:
    return datetime.now().strftime("%Y%m%d_%H%M%S")


def _self_test_data() -> dict[str, Any]:
    pages: list[dict[str, Any]] = []
    for page_number in range(1, 10):
        pages.append(
            {
                "page_number": page_number,
                "page_role": f"story beat {page_number}",
                "layout": {
                    "aspect_ratio": "9:16",
                    "layout_id": "three-tier-dramatic",
                    "panel_count": 1,
                    "panel_ratios": ["full page"],
                },
                "panels": [
                    {
                        "panel_id": f"{page_number}A",
                        "shot": "dramatic comic shot",
                        "action": f"unique visible action {page_number}",
                        "text_slots": [
                            {"type": "narration", "text": f"第{page_number}页"}
                        ],
                    }
                ],
                "positive_prompt": (
                    f"cinematic comic page, vertical 9:16 aspect ratio, "
                    f"Page {page_number}, unique visible action {page_number}"
                ),
            }
        )
    return {
        "generation_contract": {
            "hard_constraints": [
                "Generate exactly 9 separate images/pages.",
                "Do not create a nine-grid collage.",
                "Do not create nine variations of the same scene.",
            ]
        },
        "style_bible": {"base_style": "cinematic comic realism"},
        "character_locks": [],
        "comic_text_system": {"narration": "rectangular caption box"},
        "pages": pages,
        "global_negative_prompt": "collage, nine variations, unreadable Chinese text, watermark",
    }


def _load_json(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as fh:
        data = json.load(fh)
    if not isinstance(data, dict):
        raise ValueError("root must be a JSON object")
    return data


def _text_block(title: str, value: Any) -> str:
    if value in (None, "", [], {}):
        return ""
    if isinstance(value, str):
        body = value
    else:
        body = json.dumps(value, ensure_ascii=False, indent=2)
    return f"\n## {title}\n{body}\n"


def compile_master_prompt(data: dict[str, Any]) -> str:
    contract = data.get("generation_contract", {})
    hard_constraints = contract.get("hard_constraints", [])
    style_bible = data.get("style_bible", {})
    character_locks = data.get("character_locks", [])
    comic_text_system = data.get("comic_text_system", {})
    pages = data.get("pages", [])
    negative = data.get("global_negative_prompt", "")

    parts: list[str] = [
        "Generate exactly 9 separate images/pages. Each output image is one complete vertical 9:16 comic page. "
        "Do not create a nine-grid collage, contact sheet, or one image containing all pages. "
        "Do not create nine variations of the same scene. "
        "The nine images are consecutive comic pages from the same story, in page order from Page 1 to Page 9."
    ]
    parts.append(_text_block("Hard Constraints", hard_constraints))
    parts.append(_text_block("Global Style Bible", style_bible))
    parts.append(_text_block("Character Locks", character_locks))
    parts.append(_text_block("Comic Text System", comic_text_system))

    for page in pages:
        page_number = page.get("page_number")
        page_role = page.get("page_role", "")
        layout = page.get("layout", {})
        prompt = page.get("positive_prompt", "")
        panels = page.get("panels", [])
        parts.append(
            "\n## Page {page_number}: {page_role}\n"
            "This output image must be Page {page_number} only, a complete vertical 9:16 comic page, not a collage.\n"
            "Layout: {layout}\n"
            "Panels and text slots: {panels}\n"
            "Positive prompt: {prompt}\n".format(
                page_number=page_number,
                page_role=page_role,
                layout=json.dumps(layout, ensure_ascii=False),
                panels=json.dumps(panels, ensure_ascii=False),
                prompt=prompt,
            )
        )

    parts.append(_text_block("Global Negative Prompt", negative))
    return "\n".join(part for part in parts if part)


def _run_validator(json_path: Path) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(VALIDATOR), str(json_path)],
        cwd=str(REPO_ROOT),
        text=True,
        capture_output=True,
        check=False,
    )


def _read_seedream_report(path: Path) -> dict[str, Any]:
    return _load_json(path)


def _infer_project_root(json_path: Path, project_name: str | None) -> Path:
    parts = json_path.resolve().parts
    for index in range(len(parts) - 2):
        if parts[index] == "projects" and parts[index + 1] == "comic":
            return Path(*parts[: index + 3])

    inferred_name = project_name or json_path.stem
    return REPO_ROOT / "projects/comic" / inferred_name


def main() -> int:
    parser = argparse.ArgumentParser(description="Run Seedream once for 9 comic pages from JSON")
    parser.add_argument("json_path", nargs="?", type=Path)
    parser.add_argument("--output-dir", type=Path)
    parser.add_argument("--project-name", help="Comic project name used when JSON is outside projects/comic/<name>/")
    parser.add_argument("--filename-prefix")
    parser.add_argument("--size", default="2K")
    parser.add_argument("--timeout", type=int, default=600)
    parser.add_argument("--dry-run", action="store_true", help="Write plan only; do not call Seedream")
    parser.add_argument("--execute", action="store_true", help="Actually call Seedream")
    parser.add_argument("--self-test", action="store_true", help="Run an in-memory compiler self-test")
    parser.add_argument("--no-watermark", action="store_true", default=True)
    args = parser.parse_args()

    if args.self_test:
        prompt = compile_master_prompt(_self_test_data())
        required = [
            "Generate exactly 9 separate images/pages",
            "Do not create a nine-grid collage",
            "Do not create nine variations of the same scene",
            "Page 9",
            "vertical 9:16",
        ]
        missing = [text for text in required if text not in prompt]
        if missing:
            print(f"FAIL self-test missing: {missing}", file=sys.stderr)
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
    validator_result = _run_validator(json_path)
    if validator_result.returncode != 0:
        print(validator_result.stdout, end="")
        print(validator_result.stderr, end="", file=sys.stderr)
        return validator_result.returncode

    data = _load_json(json_path)
    master_prompt = compile_master_prompt(data)
    project_root = _infer_project_root(json_path, args.project_name)
    output_dir = args.output_dir or (project_root / "3-漫画生成")
    output_dir.mkdir(parents=True, exist_ok=True)
    prefix = args.filename_prefix or json_path.stem
    seedream_report = output_dir / f"seedream_report_{_now_stamp()}.json"
    master_prompt_path = output_dir / "seedream_master_prompt.txt"

    command = [
        sys.executable,
        str(SEEDREAM_SCRIPT),
        "--prompt",
        master_prompt,
        "--max-images",
        "9",
        "--size",
        args.size,
        "--stream",
        "--output-dir",
        str(output_dir),
        "--filename-prefix",
        prefix,
        "--report-json",
        str(seedream_report),
        "--timeout",
        str(args.timeout),
    ]
    if args.no_watermark:
        command.append("--no-watermark")

    plan = {
        "ok": True,
        "input_json": str(json_path),
        "output_dir": str(output_dir),
        "master_prompt_path": str(master_prompt_path),
        "seedream_report": str(seedream_report),
        "seedream_command_preview": [
            token if token != master_prompt else "<compiled master prompt>"
            for token in command
        ],
        "expected_result_count": 9,
    }
    master_prompt_path.write_text(master_prompt, encoding="utf-8")
    (output_dir / "generation_plan.json").write_text(
        json.dumps(plan, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    if args.dry_run:
        print(f"PASS dry-run: {output_dir / 'generation_plan.json'}")
        return 0

    result = subprocess.run(command, cwd=str(REPO_ROOT), text=True, check=False)
    if result.returncode != 0:
        return result.returncode

    report = _read_seedream_report(seedream_report)
    saved_files = report.get("saved_files", [])
    if report.get("result_count") != 9 or not isinstance(saved_files, list) or len(saved_files) != 9:
        print("FAIL: Seedream did not return exactly 9 saved files", file=sys.stderr)
        return 3

    comic_report = {
        "ok": True,
        "input_json": str(json_path),
        "output_dir": str(output_dir),
        "master_prompt_path": str(master_prompt_path),
        "seedream_report": str(seedream_report),
        "saved_files": saved_files,
        "result_count": report.get("result_count"),
        "stream_event_count": report.get("stream_event_count"),
        "stream_event_types": report.get("stream_event_types"),
    }
    report_path = output_dir / "comic_generation_report.json"
    report_path.write_text(json.dumps(comic_report, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"PASS generated 9 comic pages: {report_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
