#!/usr/bin/env python3
"""Compile per-page sora prompts from nine_blade JSON and optionally run image-to-video generation."""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
import tempfile
from datetime import datetime
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[5]
NINE_BLADE_VALIDATOR = REPO_ROOT / ".agents/skills/comic/2-九刀流漫画提示词/scripts/validate_nine_blade_prompt_json.py"
ANIMATION_VALIDATOR = REPO_ROOT / ".agents/skills/comic/4-动画生成/scripts/validate_comic_animation_prompt_json.py"
SORA_SCRIPT = REPO_ROOT / ".agents/skills/api/video/sora/scripts/sora_video_generate.py"

FIXED_PROMPT_PREFIX = (
    "Animate this vertical comic strip into a seamless, continuous cinematic video. "
    "Chronological sequence from right to left, top to bottom panels. "
    "Advanced camera movement transitioning smoothly between scenes. "
    "High-fidelity motion physics, 4K resolution, masterpiece quality."
)


def _load_json(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as fh:
        data = json.load(fh)
    if not isinstance(data, dict):
        raise ValueError("root must be a JSON object")
    return data


def _write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def _write_text(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def _slugify(value: str) -> str:
    slug = re.sub(r"[^A-Za-z0-9_-]+", "-", value.strip())
    slug = re.sub(r"-{2,}", "-", slug).strip("-_")
    return slug or "page-group"


def _group_meta(data: dict[str, Any]) -> dict[str, Any]:
    page_group = data.get("page_group", {})
    return page_group if isinstance(page_group, dict) else {}


def _derive_group_slug(data: dict[str, Any], input_path: Path) -> str:
    page_group = _group_meta(data)
    group_id = str(page_group.get("group_id", "")).strip()
    if group_id:
        return _slugify(group_id)
    stem = input_path.stem
    stem = re.sub(r"[-_]?nine_blade_comic_prompts$", "", stem)
    stem = re.sub(r"[-_]?comic_page_animation_prompts$", "", stem)
    stem = stem.strip("-_")
    return _slugify(stem)


def _infer_project_root(input_path: Path, project_name: str | None) -> Path:
    parts = input_path.resolve().parts
    for index in range(len(parts) - 2):
        if parts[index] == "projects" and parts[index + 1] == "comic":
            return Path(*parts[: index + 3])
        if (
            parts[index] == "projects"
            and parts[index + 1] == "aigc"
            and index + 5 < len(parts)
            and parts[index + 3] == "5-Image"
            and parts[index + 4] == "漫画"
        ):
            return Path(*parts[: index + 5])
    inferred_name = project_name or input_path.stem
    return REPO_ROOT / "projects/comic" / inferred_name


def _default_images_dir(project_root: Path, group_slug: str) -> Path:
    return project_root / "3-漫画生成" / group_slug


def _candidate_images(images_dir: Path, group_slug: str, page_number: int) -> list[Path]:
    names = [
        f"page{page_number:02d}",
        f"{group_slug}-page{page_number:02d}",
    ]
    candidates: list[Path] = []
    for stem in names:
        candidates.extend(sorted(images_dir.glob(f"{stem}.*")))
    return [path for path in candidates if path.is_file()]


def _resolve_page_image(images_dir: Path, group_slug: str, page_number: int) -> Path:
    candidates = _candidate_images(images_dir, group_slug, page_number)
    if not candidates:
        raise FileNotFoundError(
            f"未找到第 {page_number} 页首帧图；已搜索 {images_dir}/page{page_number:02d}.* 和 {group_slug}-page{page_number:02d}.*"
        )
    return candidates[0].resolve()


def _character_map(data: dict[str, Any]) -> dict[str, dict[str, Any]]:
    result: dict[str, dict[str, Any]] = {}
    main_character_lock = data.get("main_character_lock", {})
    if isinstance(main_character_lock, dict):
        character_id = str(main_character_lock.get("character_id", "")).strip()
        if character_id:
            result[character_id] = main_character_lock
    character_locks = data.get("character_locks", [])
    if isinstance(character_locks, list):
        for item in character_locks:
            if not isinstance(item, dict):
                continue
            character_id = str(item.get("character_id", "")).strip()
            if character_id:
                result[character_id] = item
    return result


def _scene_map(data: dict[str, Any]) -> dict[str, dict[str, Any]]:
    scene_bible = data.get("scene_continuity_bible", {})
    if not isinstance(scene_bible, dict):
        return {}
    scene_locks = scene_bible.get("scene_locks", [])
    result: dict[str, dict[str, Any]] = {}
    if isinstance(scene_locks, list):
        for item in scene_locks:
            if not isinstance(item, dict):
                continue
            scene_id = str(item.get("scene_id", "")).strip()
            if scene_id:
                result[scene_id] = item
    return result


def _short_text(value: Any, fallback: str) -> str:
    text = str(value or "").strip()
    return text or fallback


def _camera_motion(panel: dict[str, Any], shot_index: int) -> str:
    shot = _short_text(panel.get("shot"), "cinematic comic shot")
    lowered = shot.lower()
    if "close" in lowered:
        return "subtle push-in that preserves the panel framing"
    if "wide" in lowered or "establishing" in lowered:
        return "slow cinematic glide to reveal spatial depth while preserving the page composition"
    if shot_index == 1:
        return "gentle opening move that establishes the shot without breaking the page layout"
    return "smooth transitional camera move into the next panel beat"


def _subject_motion(panel: dict[str, Any]) -> str:
    action = _short_text(panel.get("action"), "subtle living motion")
    return f"natural body motion that completes this beat: {action}"


def _text_handling(panel: dict[str, Any]) -> str:
    slots = panel.get("text_slots", [])
    if not isinstance(slots, list) or not slots:
        return "preserve any visible Chinese lettering and page number without distortion"
    types = [str(slot.get("type", "")).strip() for slot in slots if isinstance(slot, dict)]
    compact_types = ", ".join([item for item in types if item]) or "text slots"
    return f"preserve the original {compact_types} placement, keep Chinese text readable, and do not morph lettering"


def _shot_plan(page: dict[str, Any]) -> list[dict[str, Any]]:
    panels = page.get("panels", [])
    if not isinstance(panels, list) or not panels:
        raise ValueError(f"page {page.get('page_number')} 缺少 panels[]，无法生成多分镜 shot plan")

    shots: list[dict[str, Any]] = []
    for shot_index, panel in enumerate(panels, start=1):
        if not isinstance(panel, dict):
            raise ValueError(f"page {page.get('page_number')} 的 panel {shot_index} 不是对象")
        shots.append(
            {
                "shot_index": shot_index,
                "source_panel_id": _short_text(panel.get("panel_id"), f"{page.get('page_number')}P{shot_index}"),
                "shot": _short_text(panel.get("shot"), "cinematic comic panel shot"),
                "action": _short_text(panel.get("action"), "panel beat motion"),
                "camera_motion": _camera_motion(panel, shot_index),
                "subject_motion": _subject_motion(panel),
                "text_handling": _text_handling(panel),
            }
        )
    return shots


def _shot_plan_text(shot_plan: list[dict[str, Any]]) -> str:
    lines: list[str] = []
    for shot in shot_plan:
        lines.append(
            f"Shot {shot['shot_index']} from panel {shot['source_panel_id']}: "
            f"{shot['shot']}. Action: {shot['action']}. "
            f"Camera: {shot['camera_motion']}. Subject motion: {shot['subject_motion']}. "
            f"Text handling: {shot['text_handling']}."
        )
    return " ".join(lines)


def _compile_page_prompt(
    *,
    page: dict[str, Any],
    shot_plan: list[dict[str, Any]],
    character_map: dict[str, dict[str, Any]],
    scene_map: dict[str, dict[str, Any]],
    continuity_context: dict[str, Any],
    main_character_lock: dict[str, Any],
    style_bible: dict[str, Any],
    size: str,
    seconds: int,
) -> str:
    page_number = int(page.get("page_number"))
    page_role = _short_text(page.get("page_role"), f"page {page_number}")
    positive_prompt = _short_text(page.get("positive_prompt"), "")
    layout = json.dumps(page.get("layout", {}), ensure_ascii=False)
    active_character_ids = page.get("active_character_ids", [])
    if not isinstance(active_character_ids, list):
        active_character_ids = []
    active_locks = [
        character_map[character_id].get("anchor_prompt", "")
        for character_id in active_character_ids
        if character_id in character_map
    ]
    scene_lock = scene_map.get(str(page.get("scene_id", "")).strip(), {})
    scene_anchor = _short_text(scene_lock.get("anchor_prompt"), "")
    overlay = page.get("page_number_overlay", {})
    overlay_text = json.dumps(overlay, ensure_ascii=False)
    continuity_text = json.dumps(continuity_context, ensure_ascii=False)
    style_text = json.dumps(style_bible, ensure_ascii=False)
    shot_plan_text = _shot_plan_text(shot_plan)
    main_anchor = _short_text(main_character_lock.get("anchor_prompt"), "")
    active_anchor_text = " ".join([item for item in active_locks if item]).strip()

    parts = [
        FIXED_PROMPT_PREFIX,
        f"Preserve the exact source image composition, panel layout, manga rendering style, character identity, costume, props, Chinese lettering, and page number for Page {page_number}.",
        f"Animate Page {page_number} as a vertical 9:16 image-to-video clip for {seconds} seconds at {size}.",
        f"Page role: {page_role}.",
        f"Original comic page prompt: {positive_prompt}",
        f"Layout contract: {layout}",
        f"Main character lock: {main_anchor}",
    ]
    if active_anchor_text:
        parts.append(f"Active character locks for this page: {active_anchor_text}")
    if scene_anchor:
        parts.append(f"Scene continuity lock: {scene_anchor}")
    parts.extend(
        [
            f"Continuity context: {continuity_text}",
            f"Style bible: {style_text}",
            f"Page number overlay contract: {overlay_text}",
            "Use one panel becomes one cinematic shot by default, ordered from right to left and top to bottom panels.",
            f"Shot plan: {shot_plan_text}",
            "Keep all visible Chinese text readable and stable. Preserve the page number in the bottom-right corner. Do not add new panels, characters, props, or story beats. Do not redraw the page in a different style or collapse the page into a single-shot motion poster.",
        ]
    )
    return " ".join(part for part in parts if part).strip()


def _compile_animation_payload(
    data: dict[str, Any],
    input_path: Path,
    images_dir: Path,
    model: str,
    seconds: int,
    size: str,
) -> dict[str, Any]:
    page_group = _group_meta(data)
    continuity_context = data.get("continuity_context", {})
    if not isinstance(continuity_context, dict):
        continuity_context = {}
    main_character_lock = data.get("main_character_lock", {})
    if not isinstance(main_character_lock, dict):
        main_character_lock = {}
    style_bible = data.get("style_bible", {})
    if not isinstance(style_bible, dict):
        style_bible = {}
    pages = data.get("pages", [])
    if not isinstance(pages, list) or len(pages) != 9:
        raise ValueError("nine_blade JSON 必须包含 9 页 pages[]")

    group_slug = _derive_group_slug(data, input_path)
    character_map = _character_map(data)
    scene_map = _scene_map(data)
    compiled_pages: list[dict[str, Any]] = []

    for page in pages:
        if not isinstance(page, dict):
            raise ValueError("pages[] 内必须全部是对象")
        page_number = int(page.get("page_number"))
        source_image = _resolve_page_image(images_dir, group_slug, page_number)
        shot_plan = _shot_plan(page)
        compiled_pages.append(
            {
                "page_number": page_number,
                "page_role": _short_text(page.get("page_role"), f"page {page_number}"),
                "source_image": str(source_image),
                "active_character_ids": page.get("active_character_ids", []),
                "scene_id": page.get("scene_id"),
                "page_number_overlay": page.get("page_number_overlay", {}),
                "storyboard_policy": {
                    "panel_to_shot": "one_panel_one_shot_default",
                    "reading_order": "right_to_left_top_to_bottom",
                },
                "layout": page.get("layout", {}),
                "shot_plan": shot_plan,
                "sora_prompt": _compile_page_prompt(
                    page=page,
                    shot_plan=shot_plan,
                    character_map=character_map,
                    scene_map=scene_map,
                    continuity_context=continuity_context,
                    main_character_lock=main_character_lock,
                    style_bible=style_bible,
                    size=size,
                    seconds=seconds,
                ),
            }
        )

    return {
        "schema_version": "comic_page_animation_prompts.v1",
        "source_nine_blade_json": str(input_path.resolve()),
        "source_images_dir": str(images_dir.resolve()),
        "prompt_prefix": FIXED_PROMPT_PREFIX,
        "page_group": page_group,
        "continuity_context": continuity_context,
        "video_generation_contract": {
            "provider": "sora",
            "mode": "image_to_video",
            "model": model,
            "seconds": seconds,
            "size": size,
            "aspect_ratio": "9:16",
        },
        "pages": compiled_pages,
    }


def _run_validator(script_path: Path, json_path: Path) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(script_path), str(json_path)],
        cwd=str(REPO_ROOT),
        text=True,
        capture_output=True,
        check=False,
    )


def _load_or_compile(
    input_path: Path,
    *,
    images_dir: Path,
    model: str,
    seconds: int,
    size: str,
) -> dict[str, Any]:
    data = _load_json(input_path)
    schema_version = data.get("schema_version")
    if schema_version == "comic_page_animation_prompts.v1":
        return data
    if schema_version != "nine_blade_comic_prompts.v1":
        raise ValueError("输入必须是 nine_blade_comic_prompts.v1 或 comic_page_animation_prompts.v1")

    validator_result = _run_validator(NINE_BLADE_VALIDATOR, input_path)
    if validator_result.returncode != 0:
        raise ValueError(
            "nine_blade JSON 校验失败:\n"
            + validator_result.stdout
            + validator_result.stderr
        )
    return _compile_animation_payload(data, input_path, images_dir, model, seconds, size)


def _self_test() -> int:
    sample_pages: list[dict[str, Any]] = []
    for page_number in range(1, 10):
        sample_pages.append(
            {
                "page_number": page_number,
                "page_role": f"story beat {page_number}",
                "active_character_ids": ["protagonist"],
                "scene_id": "scene-01",
                "layout": {
                    "aspect_ratio": "9:16",
                    "layout_id": "three-tier-dramatic",
                    "panel_count": 3,
                    "panel_ratios": ["40/30/30"],
                },
                "panels": [
                    {"panel_id": f"{page_number}A", "shot": "wide establishing shot", "action": "the hero notices the anomaly"},
                    {"panel_id": f"{page_number}B", "shot": "medium reaction shot", "action": "the hero reacts and steps forward"},
                    {"panel_id": f"{page_number}C", "shot": "close-up reveal", "action": "the mystery object starts glowing"},
                ],
                "page_number_overlay": {
                    "text": str(page_number),
                    "position": "bottom-right"
                },
                "positive_prompt": f"vertical 9:16 comic page, page {page_number}, dramatic manga paneling, preserve all Chinese lettering and page number"
            }
        )

    sample = {
        "schema_version": "nine_blade_comic_prompts.v1",
        "page_group": {"group_id": "page-group-01", "group_index": 1, "total_groups": 1},
        "continuity_context": {"same_visual_dna_rule": "same rendering medium and line system"},
        "main_character_lock": {
            "character_id": "protagonist",
            "anchor_prompt": "Character locked across all panels: the protagonist keeps the same face, costume, silhouette and palette."
        },
        "scene_continuity_bible": {
            "scene_locks": [
                {
                    "scene_id": "scene-01",
                    "anchor_prompt": "Scene locked across relevant pages: same temple hall architecture, lanterns, fog and geography."
                }
            ]
        },
        "style_bible": {"base_style": "cinematic comic realism"},
        "character_locks": [],
        "pages": sample_pages
    }

    with tempfile.TemporaryDirectory() as tmp_dir:
        tmp_root = Path(tmp_dir)
        source_json = tmp_root / "page-group-01-nine_blade_comic_prompts.json"
        images_dir = tmp_root / "images"
        images_dir.mkdir(parents=True, exist_ok=True)
        for page_number in range(1, 10):
            (images_dir / f"page{page_number:02d}.png").write_bytes(b"fake")
        _write_json(source_json, sample)
        compiled = _compile_animation_payload(sample, source_json, images_dir, "sora-2", 12, "720x1280")
        compiled_path = tmp_root / "page-group-01-comic_page_animation_prompts.json"
        _write_json(compiled_path, compiled)
        validation = _run_validator(ANIMATION_VALIDATOR, compiled_path)
        if validation.returncode != 0:
            print(validation.stdout, end="")
            print(validation.stderr, end="", file=sys.stderr)
            return validation.returncode
    print("PASS self-test")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description="Compile and optionally run sora animation for comic pages")
    parser.add_argument("input_json", nargs="?")
    parser.add_argument("--images-dir", type=Path)
    parser.add_argument("--output-dir", type=Path)
    parser.add_argument("--project-name")
    parser.add_argument("--model", default="sora-2")
    parser.add_argument("--seconds", type=int, default=12, choices=[4, 8, 12])
    parser.add_argument("--size", default="720x1280", choices=["720x1280", "1280x720", "1024x1792", "1792x1024"])
    parser.add_argument("--timeout", type=int, default=180)
    parser.add_argument("--poll-interval", type=int, default=10)
    parser.add_argument("--max-wait-seconds", type=int, default=900)
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--execute", action="store_true")
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()

    if args.self_test:
        return _self_test()

    if not args.input_json:
        parser.error("input_json is required unless --self-test is used")
    if args.dry_run and args.execute:
        parser.error("choose only one of --dry-run or --execute")
    if not args.dry_run and not args.execute:
        parser.error("pass --dry-run or --execute")

    input_path = Path(args.input_json).resolve()
    raw_input = _load_json(input_path)
    group_slug = _derive_group_slug(raw_input, input_path)
    project_root = _infer_project_root(input_path, args.project_name)
    images_dir = args.images_dir.resolve() if args.images_dir else _default_images_dir(project_root, group_slug)
    output_dir = args.output_dir.resolve() if args.output_dir else (project_root / "4-动画生成" / group_slug)
    output_dir.mkdir(parents=True, exist_ok=True)

    compiled = _load_or_compile(
        input_path,
        images_dir=images_dir,
        model=args.model,
        seconds=args.seconds,
        size=args.size,
    )
    compiled_path = output_dir / f"{group_slug}-comic_page_animation_prompts.json"
    _write_json(compiled_path, compiled)

    animation_validator = _run_validator(ANIMATION_VALIDATOR, compiled_path)
    if animation_validator.returncode != 0:
        print(animation_validator.stdout, end="")
        print(animation_validator.stderr, end="", file=sys.stderr)
        return animation_validator.returncode

    pages = compiled["pages"]
    animation_plan_path = output_dir / f"{group_slug}-animation_plan.json"
    animation_report_path = output_dir / f"{group_slug}-animation_generation_report.json"

    plan = {
        "ok": True,
        "input_json": str(input_path),
        "compiled_prompt_json": str(compiled_path),
        "group_slug": group_slug,
        "source_images_dir": str(images_dir),
        "output_dir": str(output_dir),
        "video_generation_contract": compiled["video_generation_contract"],
        "page_jobs": [
            {
                "page_number": page["page_number"],
                "source_image": page["source_image"],
                "prompt_preview": page["sora_prompt"][:240] + ("..." if len(page["sora_prompt"]) > 240 else ""),
                "page_dir": str(output_dir / f"page{page['page_number']:02d}")
            }
            for page in pages
        ]
    }
    _write_json(animation_plan_path, plan)
    pending_report = {
        "ok": False,
        "status": "pending" if args.execute else "planned",
        "input_json": str(input_path),
        "compiled_prompt_json": str(compiled_path),
        "group_slug": group_slug,
        "animation_plan_path": str(animation_plan_path),
        "pages": []
    }
    _write_json(animation_report_path, pending_report)

    for page in pages:
        page_dir = output_dir / f"page{page['page_number']:02d}"
        _write_text(page_dir / f"page{page['page_number']:02d}-sora_prompt.txt", page["sora_prompt"])

    if args.dry_run:
        print(f"PASS dry-run: {animation_plan_path}")
        return 0

    page_reports: list[dict[str, Any]] = []
    overall_ok = True
    for page in pages:
        page_number = int(page["page_number"])
        page_tag = f"page{page_number:02d}"
        page_dir = output_dir / page_tag
        report_json = page_dir / f"{page_tag}-sora_run_report.json"
        command = [
            sys.executable,
            str(SORA_SCRIPT),
            "run",
            "--prompt",
            page["sora_prompt"],
            "--image",
            page["source_image"],
            "--model",
            args.model,
            "--seconds",
            str(args.seconds),
            "--size",
            args.size,
            "--output-dir",
            str(page_dir),
            "--filename-prefix",
            page_tag,
            "--report-json",
            str(report_json),
            "--timeout",
            str(args.timeout),
            "--poll-interval",
            str(args.poll_interval),
            "--max-wait-seconds",
            str(args.max_wait_seconds),
        ]
        result = subprocess.run(command, cwd=str(REPO_ROOT), text=True, check=False)
        report_body = _load_json(report_json) if report_json.exists() else {
            "ok": False,
            "error": "missing sora report"
        }
        page_report = {
            "page_number": page_number,
            "source_image": page["source_image"],
            "page_dir": str(page_dir),
            "report_json": str(report_json),
            "ok": bool(report_body.get("ok")),
            "saved_file": report_body.get("saved_file"),
            "error": report_body.get("error"),
            "returncode": result.returncode
        }
        if not page_report["ok"]:
            overall_ok = False
        page_reports.append(page_report)
        _write_json(
            animation_report_path,
            {
                "ok": overall_ok,
                "status": "running",
                "input_json": str(input_path),
                "compiled_prompt_json": str(compiled_path),
                "group_slug": group_slug,
                "animation_plan_path": str(animation_plan_path),
                "pages": page_reports
            },
        )

    final_report = {
        "ok": overall_ok,
        "status": "completed" if overall_ok else "failed",
        "input_json": str(input_path),
        "compiled_prompt_json": str(compiled_path),
        "group_slug": group_slug,
        "animation_plan_path": str(animation_plan_path),
        "pages": page_reports
    }
    _write_json(animation_report_path, final_report)
    print(json.dumps(final_report, ensure_ascii=False, indent=2))
    return 0 if overall_ok else 1


if __name__ == "__main__":
    sys.exit(main())
