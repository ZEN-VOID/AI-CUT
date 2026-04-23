#!/usr/bin/env python3
"""Compile per-page comic animation prompts and optionally run Man-Tui Sora image-to-video generation."""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[5]
NINE_BLADE_VALIDATOR = REPO_ROOT / ".agents/skills/comic/2-九刀流漫画提示词/scripts/validate_nine_blade_prompt_json.py"
ANIMATION_VALIDATOR = REPO_ROOT / ".agents/skills/comic/4-动画生成/scripts/validate_comic_animation_prompt_json.py"
SORA_SCRIPT = REPO_ROOT / ".agents/skills/api/man-tui/video/sora/scripts/sora_video.py"
DEFAULT_MODEL = "sora-2"
DEFAULT_SIZE = "720x1280"
SECONDS_CHOICES = [10, 15]
SIZE_CHOICES = ["720x1280", "1280x720"]
LEGACY_SCRIPT_AUTHORSHIP_ERROR = (
    "根据 AGENTS.md 的 `内容创作型任务的 LLM 主创规则`，`comic/4-动画生成` 的页级 video_prompt 正文不得再由脚本默认主创。"
    "本脚本默认只允许消费 LLM 已直出的 `comic_page_animation_prompts.v1`，并负责校验、URL 映射、执行与报告。"
    "如确需临时兼容 legacy `nine_blade_comic_prompts.v1 -> 脚本编译 video_prompt` 路径，请显式传入 "
    "`--allow-legacy-script-authorship`。"
)

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
    stem = input_path.stem
    episode_number = _extract_episode_number(stem)
    if episode_number is None:
        for parent in input_path.parents:
            episode_number = _extract_episode_number(parent.name)
            if episode_number is not None:
                break

    slug_parts: list[str] = []
    if episode_number is not None:
        slug_parts.append(f"ep{episode_number:02d}")

    if group_id:
        slug_parts.append(_slugify(group_id))
    else:
        normalized_stem = re.sub(r"[-_]?nine_blade_comic_prompts$", "", stem)
        normalized_stem = re.sub(r"[-_]?comic_page_animation_prompts$", "", normalized_stem)
        normalized_stem = normalized_stem.strip("-_")
        candidate = _slugify(normalized_stem) if normalized_stem else ""
        if candidate and candidate not in {"nine_blade_comic_prompts", "comic_page_animation_prompts"}:
            slug_parts.append(candidate)

    if not slug_parts:
        group_index = page_group.get("group_index")
        if isinstance(group_index, int) and group_index >= 1:
            slug_parts.append(f"page-group-{group_index:02d}")

    return "-".join(slug_parts) if slug_parts else "page-group"


def _group_aliases(data: dict[str, Any], input_path: Path) -> list[str]:
    page_group = _group_meta(data)
    aliases: list[str] = []

    def add(candidate: str) -> None:
        normalized = candidate.strip()
        if normalized and normalized not in aliases:
            aliases.append(normalized)

    add(_derive_group_slug(data, input_path))

    group_id = str(page_group.get("group_id", "")).strip()
    add(group_id)
    if group_id:
        add(_slugify(group_id))

    group_index = page_group.get("group_index")
    if isinstance(group_index, int) and group_index >= 1:
        add(f"page-group-{group_index:02d}")

    return aliases


def _extract_episode_number(text: str) -> int | None:
    for pattern in (r"第(\d+)集", r"\bep(?:isode)?[-_ ]?(\d+)\b", r"\bepisode[-_ ]?(\d+)\b"):
        match = re.search(pattern, text, flags=re.IGNORECASE)
        if match:
            return int(match.group(1))
    return None


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


def _project_name_from_root(project_root: Path, fallback: str | None) -> str:
    parts = project_root.resolve().parts
    for index in range(len(parts) - 2):
        if parts[index] == "projects" and parts[index + 1] == "comic":
            return parts[index + 2]
        if parts[index] == "projects" and parts[index + 1] == "aigc":
            return parts[index + 2]
    return fallback or project_root.name


def _default_output_dir(project_root: Path) -> Path:
    return project_root / "4-动画生成"


def _default_images_dir(project_root: Path, group_aliases: list[str]) -> Path:
    stage_root = project_root / "3-漫画生成"
    for alias in group_aliases:
        preferred = stage_root / alias
        if preferred.exists():
            return preferred
    return stage_root


def _candidate_image_dirs(project_root: Path, group_aliases: list[str]) -> list[Path]:
    stage_root = project_root / "3-漫画生成"
    candidates: list[Path] = []
    for alias in group_aliases:
        candidate = stage_root / alias
        if candidate not in candidates:
            candidates.append(candidate)
    candidates.append(stage_root)
    return candidates


def _candidate_images(images_dir: Path, group_aliases: list[str], page_number: int) -> list[Path]:
    names = [f"page{page_number:02d}"]
    for alias in group_aliases:
        names.append(f"{alias}-page{page_number:02d}")
    candidates: list[Path] = []
    for stem in names:
        candidates.extend(sorted(images_dir.glob(f"{stem}.*")))
    return [path for path in candidates if path.is_file()]


def _resolve_images_dir(project_root: Path, group_aliases: list[str]) -> Path:
    for candidate in _candidate_image_dirs(project_root, group_aliases):
        if _candidate_images(candidate, group_aliases, 1):
            return candidate.resolve()
    return _default_images_dir(project_root, group_aliases).resolve()


def _resolve_page_image(images_dir: Path, group_aliases: list[str], page_number: int) -> Path:
    candidates = _candidate_images(images_dir, group_aliases, page_number)
    if not candidates:
        alias_patterns = " 和 ".join(f"{alias}-page{page_number:02d}.*" for alias in group_aliases)
        raise FileNotFoundError(
            f"未找到第 {page_number} 页首帧图；已搜索 {images_dir}/page{page_number:02d}.*"
            + (f" 以及 {alias_patterns}" if alias_patterns else "")
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


def _compact_text(value: Any) -> str:
    text = str(value or "").strip()
    return " ".join(text.split()) if text else ""


def _flatten_structure_lines(
    value: Any,
    *,
    prefix: str = "",
    max_lines: int = 14,
    max_depth: int = 4,
) -> list[str]:
    lines: list[str] = []

    def walk(node: Any, current_prefix: str, depth: int) -> None:
        if len(lines) >= max_lines or depth > max_depth:
            return
        if isinstance(node, dict):
            for key, child in node.items():
                next_prefix = f"{current_prefix}.{key}" if current_prefix else str(key)
                walk(child, next_prefix, depth + 1)
                if len(lines) >= max_lines:
                    return
            return
        if isinstance(node, list):
            compact_items = [_compact_text(item) for item in node]
            compact_items = [item for item in compact_items if item]
            if compact_items:
                lines.append(f"{current_prefix}: {', '.join(compact_items[:8])}")
            return
        compact = _compact_text(node)
        if compact:
            lines.append(f"{current_prefix}: {compact}")

    walk(value, prefix, 0)
    return lines[:max_lines]


def _summarize_control_surface(value: Any) -> list[str]:
    if not isinstance(value, dict):
        return []
    digest = value.get("control_surface_digest")
    if isinstance(digest, list) and digest:
        return [str(item).strip() for item in digest[:14] if str(item).strip()]
    surface = value.get("control_surface")
    if isinstance(surface, dict):
        return _flatten_structure_lines(surface, prefix="control_surface", max_lines=14)
    return []


def _camera_motion(panel: dict[str, Any], shot_index: int) -> str:
    shot = _short_text(panel.get("shot"), "cinematic comic shot")
    lowered = shot.lower()
    if "close" in lowered:
        return "motivated push-in with breathing handheld energy, eye-line shift, and shallow focus change, never a static zoom"
    if "wide" in lowered or "establishing" in lowered:
        return "cinematic crane or glide move with clear foreground-midground-background parallax, weather motion, and spatial depth reveal"
    if "detail" in lowered or "hook" in lowered:
        return "macro drift or rack focus reveal that turns the detail into a living cinematic beat instead of a frozen insert"
    if shot_index == 1:
        return "opening move with real depth, layered parallax, and a motivated entry into the panel world, not a flat page hold"
    return "motivated transitional camera move with depth travel, foreground wipe or focus pull into the next panel beat, not a Ken Burns pan"


def _subject_motion(panel: dict[str, Any]) -> str:
    action = _short_text(panel.get("action"), "subtle living motion")
    return (
        "cinematic character performance with body-weight shift, head turn, eye focus, hand interaction, "
        f"secondary cloth or hair motion, and environmental response that completes this beat: {action}"
    )


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
    type_stack_ref: dict[str, Any],
    type_pack_context: dict[str, Any],
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
    active_packs = ", ".join(str(item) for item in type_stack_ref.get("active_packs", []))
    animation_projection = json.dumps(
        type_pack_context.get("stage_projection", {}).get("animation_generation", {}),
        ensure_ascii=False,
    )
    control_surface_lines = _summarize_control_surface(type_pack_context)
    shot_plan_text = _shot_plan_text(shot_plan)
    main_anchor = _short_text(main_character_lock.get("anchor_prompt"), "")
    active_anchor_text = " ".join([item for item in active_locks if item]).strip()

    parts = [
        FIXED_PROMPT_PREFIX,
        (
            f"Use the source comic page for Page {page_number} as storyboard truth and visual bible: preserve story order, "
            "character identity, costume, props, Chinese lettering, page number, key composition logic, and manga visual DNA, "
            "but transform the frozen page into living cinematic blocking with real depth and momentum."
        ),
        f"Animate Page {page_number} as a vertical 9:16 image-to-video clip for {seconds} seconds at {size}.",
        f"Page role: {page_role}.",
        (
            "This must feel like an animated film sequence, not a slideshow, PPT animation, simple pan-zoom, "
            "Ken Burns move, motion poster, or paper cut-out puppet drift."
        ),
        (
            "Do not keep the whole comic page statically pinned to the screen. Enter the panel world, travel through depth, "
            "use motivated shot-to-shot transitions, layered foreground-midground-background separation, and visible atmospheric motion."
        ),
        (
            "Add believable environmental motion and cinematic texture: rain streaks, cloth flutter, hair movement, breath, reflections, "
            "splashes, drifting particles, crowd micro-motion, and impact follow-through where appropriate."
        ),
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
            f"Type stack active packs: {active_packs}",
            f"Type pack animation projection: {animation_projection}",
            f"Style bible: {style_text}",
            f"Page number overlay contract: {overlay_text}",
            "Use one panel becomes one cinematic shot by default, ordered from right to left and top to bottom panels.",
            f"Shot plan: {shot_plan_text}",
            (
                "Keep all visible Chinese text readable and stable. Preserve the page number in the bottom-right corner. "
                "Do not add new panels, characters, props, or story beats. Do not redraw the page in a different style. "
                "Do not collapse the sequence into a single-shot motion poster or static page hold."
            ),
        ]
    )
    if control_surface_lines:
        parts.append("Type pack control surface:")
        parts.extend(control_surface_lines)
    return " ".join(part for part in parts if part).strip()


def _compile_animation_payload(
    data: dict[str, Any],
    input_path: Path,
    images_dir: Path,
    model: str,
    seconds: int,
    size: str,
    reference_url_map: dict[str, str] | None,
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
    type_stack_ref = data.get("type_stack_ref", {})
    if not isinstance(type_stack_ref, dict):
        type_stack_ref = {}
    type_pack_context = data.get("type_pack_context", {})
    if not isinstance(type_pack_context, dict):
        type_pack_context = {}
    pages = data.get("pages", [])
    if not isinstance(pages, list) or len(pages) != 9:
        raise ValueError("nine_blade JSON 必须包含 9 页 pages[]")

    group_slug = _derive_group_slug(data, input_path)
    group_aliases = _group_aliases(data, input_path)
    character_map = _character_map(data)
    scene_map = _scene_map(data)
    compiled_pages: list[dict[str, Any]] = []

    for page in pages:
        if not isinstance(page, dict):
            raise ValueError("pages[] 内必须全部是对象")
        page_number = int(page.get("page_number"))
        source_image = _resolve_page_image(images_dir, group_aliases, page_number)
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
                "input_reference_url": _resolve_reference_url(
                    {"source_image": str(source_image)},
                    group_aliases,
                    page_number,
                    reference_url_map,
                ),
                "video_prompt": _compile_page_prompt(
                    page=page,
                    shot_plan=shot_plan,
                    character_map=character_map,
                    scene_map=scene_map,
                    continuity_context=continuity_context,
                    main_character_lock=main_character_lock,
                    style_bible=style_bible,
                    type_stack_ref=type_stack_ref,
                    type_pack_context=type_pack_context,
                    size=size,
                    seconds=seconds,
                ),
            }
        )

    return {
        "schema_version": "comic_page_animation_prompts.v1",
        "source_nine_blade_json": str(input_path.resolve()),
        "type_stack_ref": data.get("type_stack_ref", {}),
        "type_pack_context": data.get("type_pack_context", {}),
        "source_images_dir": str(images_dir.resolve()),
        "prompt_prefix": FIXED_PROMPT_PREFIX,
        "page_group": page_group,
        "continuity_context": continuity_context,
        "video_generation_contract": {
            "provider": "man-tui",
            "mode": "image_to_video",
            "model": model,
            "seconds": seconds,
            "size": size,
            "input_reference_mode": "public_url_required",
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
    reference_url_map: dict[str, str] | None,
) -> dict[str, Any]:
    data = _load_json(input_path)
    schema_version = data.get("schema_version")
    if schema_version == "comic_page_animation_prompts.v1":
        return _normalize_compiled_payload(data, input_path, images_dir, model, seconds, size, reference_url_map)
    if schema_version != "nine_blade_comic_prompts.v1":
        raise ValueError("输入必须是 nine_blade_comic_prompts.v1 或 comic_page_animation_prompts.v1")

    validator_result = _run_validator(NINE_BLADE_VALIDATOR, input_path)
    if validator_result.returncode != 0:
        raise ValueError(
            "nine_blade JSON 校验失败:\n"
            + validator_result.stdout
            + validator_result.stderr
        )
    return _compile_animation_payload(data, input_path, images_dir, model, seconds, size, reference_url_map)


def _normalize_compiled_payload(
    data: dict[str, Any],
    input_path: Path,
    images_dir: Path,
    model: str,
    seconds: int,
    size: str,
    reference_url_map: dict[str, str] | None,
) -> dict[str, Any]:
    payload = json.loads(json.dumps(data, ensure_ascii=False))
    group_slug = _derive_group_slug(payload, input_path)
    group_aliases = _group_aliases(payload, input_path)
    payload["source_images_dir"] = str(images_dir.resolve())
    if "type_stack_ref" not in payload:
        payload["type_stack_ref"] = {}
    if "type_pack_context" not in payload:
        payload["type_pack_context"] = {}
    contract = payload.get("video_generation_contract", {})
    if not isinstance(contract, dict):
        contract = {}
    contract.update(
        {
            "provider": "man-tui",
            "mode": "image_to_video",
            "model": model,
            "seconds": seconds,
            "size": size,
            "input_reference_mode": "public_url_required",
            "aspect_ratio": "9:16",
        }
    )
    payload["video_generation_contract"] = contract

    pages = payload.get("pages", [])
    if not isinstance(pages, list):
        raise ValueError("compiled animation JSON 的 pages[] 必须是数组")
    for page in pages:
        if not isinstance(page, dict):
            continue
        if "video_prompt" not in page and "sora_prompt" in page:
            page["video_prompt"] = page.pop("sora_prompt")
        page_number = int(page.get("page_number"))
        source_image = str(page.get("source_image", "")).strip()
        if not source_image:
            page["source_image"] = str(_resolve_page_image(images_dir, group_aliases, page_number))
        page["input_reference_url"] = _resolve_reference_url(
            page,
            group_aliases,
            page_number,
            reference_url_map,
        )
    return payload


def _page_slug(group_slug: str, page_number: int) -> str:
    page_tag = f"page{page_number:02d}"
    return f"{group_slug}-{page_tag}" if group_slug else page_tag


def _load_reference_url_map(path: Path | None) -> dict[str, str] | None:
    if path is None:
        return None
    payload = _load_json(path.resolve())
    resolved: dict[str, str] = {}
    for raw_key, raw_value in payload.items():
        key = str(raw_key).strip()
        value = str(raw_value).strip()
        if key and value:
            resolved[key] = value
    return resolved


def _auto_reference_url_map(images_dir: Path) -> dict[str, str] | None:
    report_candidates = sorted(images_dir.glob("*-seedream_report_*.json"))
    if not report_candidates:
        return None
    report_path = report_candidates[-1]
    try:
        payload = _load_json(report_path)
    except Exception:
        return None
    results = payload.get("results", [])
    if not isinstance(results, list) or not results:
        return None
    saved_files = payload.get("saved_files", [])
    if not isinstance(saved_files, list):
        saved_files = []

    resolved: dict[str, str] = {}
    for index, result in enumerate(results, start=1):
        if not isinstance(result, dict):
            continue
        url = str(result.get("url", "")).strip()
        if not url:
            continue
        page_tag = f"page{index:02d}"
        resolved[page_tag] = url
        if index - 1 < len(saved_files):
            raw_path = str(saved_files[index - 1]).strip()
            if raw_path:
                resolved[raw_path] = url
                resolved[Path(raw_path).name] = url
    return resolved or None


def _resolve_reference_url(
    page: dict[str, Any],
    group_aliases: list[str],
    page_number: int,
    reference_url_map: dict[str, str] | None,
) -> str | None:
    current = str(page.get("input_reference_url", "")).strip()
    if current:
        return current
    if not reference_url_map:
        return None
    page_tag = f"page{page_number:02d}"
    source_image = str(page.get("source_image", "")).strip()
    candidates = [page_tag]
    for alias in group_aliases:
        candidates.append(_page_slug(alias, page_number))
    candidates.extend(
        [
            str(page_number),
            source_image,
            Path(source_image).name if source_image else "",
        ]
    )
    for key in candidates:
        if key and key in reference_url_map:
            return reference_url_map[key]
    return None


def _existing_page_report(
    *,
    page_dir: Path,
    page_tag: str,
    page_number: int,
    source_image: str,
    input_reference_url: str | None,
    output_video: Path,
) -> dict[str, Any] | None:
    if not output_video.exists():
        return None

    report_candidates = [
        page_dir / f"{page_tag}-sora_create_report.json",
        page_dir / f"{page_tag}-actual-create-report.json",
        page_dir / f"{page_tag}-status-report.json",
    ]
    report_body: dict[str, Any] = {}
    chosen_report: Path | None = None
    for candidate in report_candidates:
        if candidate.exists():
            try:
                report_body = _load_json(candidate)
                chosen_report = candidate
                break
            except Exception:
                continue

    response = report_body.get("response", {}) if isinstance(report_body, dict) else {}
    if not isinstance(response, dict):
        response = {}
    wait_result = report_body.get("wait_result", {}) if isinstance(report_body, dict) else {}
    if not isinstance(wait_result, dict):
        wait_result = {}
    download_result = report_body.get("download_result", {}) if isinstance(report_body, dict) else {}
    if not isinstance(download_result, dict):
        download_result = {}
    response_status = None
    waited = wait_result.get("response", {})
    if isinstance(waited, dict):
        response_status = waited.get("status")
    if response_status is None:
        response_status = response.get("status")

    return {
        "page_number": page_number,
        "source_image": source_image,
        "input_reference_url": input_reference_url,
        "page_dir": str(page_dir),
        "report_json": str(chosen_report) if chosen_report else None,
        "ok": True,
        "task_id": response.get("task_id") or response.get("id"),
        "status": response_status or "completed",
        "saved_file": str(output_video),
        "final_url": download_result.get("final_url"),
        "error": None,
        "returncode": 0,
        "skipped_existing": True,
    }


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
        "type_stack_ref": {
            "method_kernel": "comic-core-v1",
            "base": "_base",
            "primary": "经典漫画叙事",
            "secondary": ["推理悬疑"],
            "platform": ["漫剧平台"],
            "audience": ["情绪强冲突受众"],
            "active_packs": ["_base", "经典漫画叙事", "推理悬疑", "漫剧平台", "情绪强冲突受众"]
        },
        "type_pack_context": {
            "resolution_mode": "single-layer-genre-comic-type-pack",
            "knowledge_refs": [".agents/skills/comic/type-packs/漫画/推理悬疑/推理悬疑.md"],
            "knowledge_digest": [
                "推理悬疑 > 核心冲突引擎: 线索链缓慢点亮，而真相始终晚半步抵达。"
            ],
            "pack_revisions": {
                "推理悬疑": "dynamic-runtime"
            },
            "semantic_tags": ["withheld-truth", "threat"],
            "control_surface": {
                "conflict_engine": {
                    "premise": "线索链缓慢点亮，而真相始终晚半步抵达。",
                },
                "role_matrix": {
                    "protagonist": "有盲区和代价的观察者或追查者",
                },
                "page_turn_mechanism": {
                    "turn_trigger": "页尾未完成动作、半露真相、证据细节",
                },
                "panel_grammar": {
                    "dominant_panel_shapes": ["细节特写格", "页尾悬停格"],
                },
                "visual_carrier": {
                    "primary": ["物证细节", "视线方向", "空间异常"],
                },
                "dialogue_register": {
                    "exposition_rule": "解释必须晚于证据显影",
                },
                "motif_system": {
                    "recurring_motifs": ["门缝", "录音", "重复场景再看"],
                },
                "failure_modes": ["只有反转，没有可回溯线索"],
            },
            "control_surface_digest": [
                "control_surface.conflict_engine.premise: 线索链缓慢点亮，而真相始终晚半步抵达。",
                "control_surface.page_turn_mechanism.turn_trigger: 页尾未完成动作、半露真相、证据细节",
            ],
            "stage_projection": {
                "script_adaptation": {},
                "nine_blade_prompting": {},
                "image_generation": {},
                "animation_generation": {"motion_bias": ["slow push", "threat pause"]},
                "episode_poster": {}
            }
        },
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
        compiled = _compile_animation_payload(sample, source_json, images_dir, DEFAULT_MODEL, 10, DEFAULT_SIZE, None)
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
    parser = argparse.ArgumentParser(description="Compile and optionally run comic animation for comic pages")
    parser.add_argument("input_json", nargs="?")
    parser.add_argument("--images-dir", type=Path)
    parser.add_argument("--output-dir", type=Path)
    parser.add_argument("--project-name")
    parser.add_argument("--model", default=DEFAULT_MODEL)
    parser.add_argument("--seconds", type=int, default=10, choices=SECONDS_CHOICES)
    parser.add_argument("--size", default=DEFAULT_SIZE, choices=SIZE_CHOICES)
    parser.add_argument("--reference-url-map", type=Path)
    parser.add_argument("--timeout", type=int, default=180)
    parser.add_argument("--poll-interval", type=int, default=10)
    parser.add_argument("--wait-timeout", type=int, default=900)
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--execute", action="store_true")
    parser.add_argument("--self-test", action="store_true")
    parser.add_argument(
        "--allow-legacy-script-authorship",
        action="store_true",
        help="受控兼容模式：允许旧式脚本从 nine_blade JSON 直接编译页级 video_prompt。",
    )
    args = parser.parse_args()

    if args.self_test:
        if not args.allow_legacy_script_authorship:
            raise SystemExit(f"[ERROR] {LEGACY_SCRIPT_AUTHORSHIP_ERROR}")
        return _self_test()

    if not args.input_json:
        parser.error("input_json is required unless --self-test is used")
    if args.dry_run and args.execute:
        parser.error("choose only one of --dry-run or --execute")
    if not args.dry_run and not args.execute:
        parser.error("pass --dry-run or --execute")

    input_path = Path(args.input_json).resolve()
    raw_input = _load_json(input_path)
    if raw_input.get("schema_version") == "nine_blade_comic_prompts.v1" and not args.allow_legacy_script_authorship:
        raise SystemExit(f"[ERROR] {LEGACY_SCRIPT_AUTHORSHIP_ERROR}")
    group_slug = _derive_group_slug(raw_input, input_path)
    group_aliases = _group_aliases(raw_input, input_path)
    project_root = _infer_project_root(input_path, args.project_name)
    project_name = _project_name_from_root(project_root, args.project_name)
    images_dir = args.images_dir.resolve() if args.images_dir else _resolve_images_dir(project_root, group_aliases)
    output_dir = args.output_dir.resolve() if args.output_dir else _default_output_dir(project_root)
    reference_url_map = _load_reference_url_map(args.reference_url_map) or _auto_reference_url_map(images_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    compiled = _load_or_compile(
        input_path,
        images_dir=images_dir,
        model=args.model,
        seconds=args.seconds,
        size=args.size,
        reference_url_map=reference_url_map,
    )
    compiled_prefix = group_slug or "comic-animation"
    compiled_path = output_dir / f"{compiled_prefix}-comic_page_animation_prompts.json"
    _write_json(compiled_path, compiled)

    animation_validator = _run_validator(ANIMATION_VALIDATOR, compiled_path)
    if animation_validator.returncode != 0:
        print(animation_validator.stdout, end="")
        print(animation_validator.stderr, end="", file=sys.stderr)
        return animation_validator.returncode

    pages = compiled["pages"]
    animation_plan_path = output_dir / f"{compiled_prefix}-animation_plan.json"
    animation_report_path = output_dir / f"{compiled_prefix}-animation_generation_report.json"

    plan = {
        "ok": True,
        "input_json": str(input_path),
        "compiled_prompt_json": str(compiled_path),
        "group_slug": group_slug,
        "project_name": project_name,
        "source_images_dir": str(images_dir),
        "output_dir": str(output_dir),
        "video_generation_contract": compiled["video_generation_contract"],
        "provider_skill": str(SORA_SCRIPT.relative_to(REPO_ROOT)),
        "reference_url_map": str(args.reference_url_map.resolve()) if args.reference_url_map else None,
        "page_jobs": [
            {
                "page_number": page["page_number"],
                "source_image": page["source_image"],
                "input_reference_url": page.get("input_reference_url"),
                "prompt_preview": page["video_prompt"][:240] + ("..." if len(page["video_prompt"]) > 240 else ""),
                "page_dir": str(output_dir / _page_slug(group_slug, int(page["page_number"])))
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
        "project_name": project_name,
        "animation_plan_path": str(animation_plan_path),
        "reference_policy": "execute requires public input_reference_url for every page",
        "pages": []
    }
    _write_json(animation_report_path, pending_report)

    for page in pages:
        page_slug = _page_slug(group_slug, int(page["page_number"]))
        page_dir = output_dir / page_slug
        _write_text(page_dir / f"{page_slug}-video_prompt.txt", page["video_prompt"])

    if args.dry_run:
        print(f"PASS dry-run: {animation_plan_path}")
        return 0

    missing_reference_pages = [
        int(page["page_number"])
        for page in pages
        if not str(page.get("input_reference_url", "")).strip()
    ]
    if missing_reference_pages:
        final_report = {
            "ok": False,
            "status": "blocked",
            "input_json": str(input_path),
            "compiled_prompt_json": str(compiled_path),
            "group_slug": group_slug,
            "project_name": project_name,
            "animation_plan_path": str(animation_plan_path),
            "error": "man-tui sora execute requires public input_reference_url values; local page images are not accepted",
            "missing_reference_pages": missing_reference_pages,
            "pages": [],
        }
        _write_json(animation_report_path, final_report)
        print(json.dumps(final_report, ensure_ascii=False, indent=2), file=sys.stderr)
        return 1

    page_reports: list[dict[str, Any]] = []
    overall_ok = True
    for page in pages:
        page_number = int(page["page_number"])
        page_tag = _page_slug(group_slug, page_number)
        page_dir = output_dir / page_tag
        report_json = page_dir / f"{page_tag}-sora_create_report.json"
        output_video = page_dir / f"{page_tag}.mp4"
        existing_report = _existing_page_report(
            page_dir=page_dir,
            page_tag=page_tag,
            page_number=page_number,
            source_image=page["source_image"],
            input_reference_url=page.get("input_reference_url"),
            output_video=output_video,
        )
        if existing_report:
            page_reports.append(existing_report)
            _write_json(
                animation_report_path,
                {
                    "ok": overall_ok,
                    "status": "running",
                    "input_json": str(input_path),
                    "compiled_prompt_json": str(compiled_path),
                    "group_slug": group_slug,
                    "project_name": project_name,
                    "animation_plan_path": str(animation_plan_path),
                    "pages": page_reports,
                },
            )
            continue
        command = [
            sys.executable,
            str(SORA_SCRIPT),
            "create",
            "--prompt",
            page["video_prompt"],
            "--input-reference",
            page["input_reference_url"],
            "--model",
            args.model,
            "--seconds",
            str(args.seconds),
            "--size",
            args.size,
            "--task-kind",
            "project",
            "--project-name",
            project_name,
            "--output-dir",
            str(page_dir),
            "--report-json",
            str(report_json),
            "--timeout",
            str(args.timeout),
            "--wait",
            "--poll-interval",
            str(args.poll_interval),
            "--wait-timeout",
            str(args.wait_timeout),
            "--download-on-complete",
            "--output",
            str(output_video),
        ]
        result = subprocess.run(command, cwd=str(REPO_ROOT), text=True, capture_output=True, check=False)
        if result.stdout:
            print(result.stdout, end="")
        if result.stderr:
            print(result.stderr, end="", file=sys.stderr)
        report_body = _load_json(report_json) if report_json.exists() else {
            "ok": False,
            "error": "missing sora report",
            "stdout": result.stdout,
            "stderr": result.stderr,
        }
        wait_result = report_body.get("wait_result", {}) if isinstance(report_body, dict) else {}
        download_result = report_body.get("download_result", {}) if isinstance(report_body, dict) else {}
        response = report_body.get("response", {}) if isinstance(report_body, dict) else {}
        response_status = None
        if isinstance(wait_result, dict):
            waited = wait_result.get("response", {})
            if isinstance(waited, dict):
                response_status = waited.get("status")
        if response_status is None and isinstance(response, dict):
            response_status = response.get("status")
        page_ok = bool(download_result.get("ok")) and result.returncode == 0 and output_video.exists()
        page_report = {
            "page_number": page_number,
            "source_image": page["source_image"],
            "input_reference_url": page.get("input_reference_url"),
            "page_dir": str(page_dir),
            "report_json": str(report_json),
            "ok": page_ok,
            "task_id": response.get("task_id") or response.get("id"),
            "status": response_status,
            "saved_file": download_result.get("saved_file") or report_body.get("saved_file"),
            "final_url": download_result.get("final_url"),
            "error": report_body.get("error") or wait_result.get("error") or download_result.get("error"),
            "returncode": result.returncode,
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
                "project_name": project_name,
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
        "project_name": project_name,
        "animation_plan_path": str(animation_plan_path),
        "pages": page_reports
    }
    _write_json(animation_report_path, final_report)
    print(json.dumps(final_report, ensure_ascii=False, indent=2))
    return 0 if overall_ok else 1


if __name__ == "__main__":
    sys.exit(main())
