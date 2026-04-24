#!/usr/bin/env python3
"""Legacy Seedream runner for nine_blade_comic_prompts.v1 JSON.

The comic-generation skill now defaults to Codex built-in image_gen with
model_policy=GPT-IMAGE-2-default. Use this script only when the user explicitly
asks for the legacy Seedream/API fallback.
"""

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
DATA_MODULES_ROOT = Path(__file__).resolve().parents[2] / "scripts"
if str(DATA_MODULES_ROOT) not in sys.path:
    sys.path.insert(0, str(DATA_MODULES_ROOT))

from data_modules.nine_blade_prompt_normalizer import normalize_nine_blade_prompt_data

VALIDATOR = REPO_ROOT / ".agents/skills/comic/2-九刀流漫画提示词/scripts/validate_nine_blade_prompt_json.py"
SEEDREAM_SCRIPT = REPO_ROOT / ".agents/skills/api/anyfast/image/seedream/scripts/seedream_generate.py"


def _now_stamp() -> str:
    return datetime.now().strftime("%Y%m%d_%H%M%S")


def _self_test_data() -> dict[str, Any]:
    pages: list[dict[str, Any]] = []
    layout_ids = [
        "splash-with-insets",
        "asymmetric-investigation-page",
        "diagonal-cut-action",
        "split-diopter-page",
        "vertical-cascade",
        "impact-sfx-page",
        "silent-reaction-grid",
        "border-breaking-cliffhanger",
        "noir-evidence-strip",
    ]
    for page_number in range(1, 10):
        active_character_ids = (
            ["protagonist", "companion"] if page_number in {2, 3, 4, 6} else ["protagonist"]
        )
        positive_prompt_parts = [
            "cinematic comic page, vertical 9:16 aspect ratio",
            f"Page {page_number}",
            "Character locked across all panels: Sun Wukong, golden fur, consistent face, consistent costume, consistent silhouette",
            "render clear legible Chinese text, use speech bubbles near speakers for dialogue, rectangular caption boxes for narration, thought bubbles or inner captions clearly different from dialogue for inner monologue, and integrated SFX inside the action panel",
        ]
        if len(active_character_ids) >= 2:
            positive_prompt_parts.append(
                "Zhu Bajie remains visually consistent and clearly distinguishable with patched vest and round snout"
            )
        positive_prompt_parts.extend(
            [
                "scene locked across relevant pages: Thunder Gate Courtyard, black stone gate, lightning totems, consistent architecture and landmark props",
                f"place page number \"{page_number}\" in the bottom-right corner, digits only",
                f"unique visible action {page_number}",
            ]
        )
        panel_a_slots: list[dict[str, Any]] = [
            {
                "type": "narration",
                "text": f"第{page_number}页",
                "placement": "panel_edge_caption",
                "bubble_style": "caption_box",
                "inside_panel": True,
            }
        ]
        panel_b_slots: list[dict[str, Any]] = []
        if page_number in {2, 3, 8}:
            panel_b_slots.append(
                {
                    "type": "dialogue",
                    "speaker_id": active_character_ids[0],
                    "text": "快走！",
                    "placement": "near_speaker_inside_panel",
                    "bubble_style": "speech_bubble",
                    "inside_panel": True,
                }
            )
        if page_number in {4, 9}:
            panel_b_slots.append(
                {
                    "type": "inner_monologue",
                    "speaker_id": "protagonist",
                    "text": "不能退。",
                    "placement": "near_thinker_inside_panel",
                    "bubble_style": "thought_bubble",
                    "inside_panel": True,
                }
            )
        if page_number in {1, 3, 6, 7, 9}:
            panel_b_slots.append(
                {
                    "type": "sfx",
                    "text": "轰",
                    "placement": "integrated_with_action_inside_panel",
                    "bubble_style": "integrated_sfx",
                    "inside_panel": True,
                }
            )
        pages.append(
            {
                "page_number": page_number,
                "page_role": f"story beat {page_number}",
                "source_fragment": f"source fragment {page_number}",
                "active_character_ids": active_character_ids,
                "scene_id": "thunder_gate",
                "layout": {
                    "aspect_ratio": "9:16",
                    "layout_id": layout_ids[page_number - 1],
                    "panel_count": 2,
                    "panel_ratios": [
                        "dominant irregular panel 70%",
                        "supporting inset/reaction panel 30%",
                    ],
                },
                "panels": [
                    {
                        "panel_id": f"{page_number}A",
                        "shot": "dramatic comic shot",
                        "action": f"unique visible action {page_number}",
                        "comic_techniques": ["bold gutter"],
                        "text_slots": panel_a_slots,
                    },
                    {
                        "panel_id": f"{page_number}B",
                        "shot": "supporting reaction or detail panel",
                        "action": f"supporting visible action {page_number}",
                        "comic_techniques": ["reaction inset"],
                        "text_slots": panel_b_slots,
                    },
                ],
                "page_number_overlay": {
                    "text": str(page_number),
                    "position": "bottom-right",
                    "style_prompt": (
                        f"place page number \"{page_number}\" in the bottom-right corner, "
                        "digits only, small but readable"
                    ),
                },
                "positive_prompt": ", ".join(positive_prompt_parts),
            }
        )
    return {
        "schema_version": "nine_blade_comic_prompts.v1",
        "page_group": {
            "group_id": "page-group-01",
            "group_index": 1,
            "total_groups": 3,
            "estimated_source_chars": 480,
            "target_source_chars": 500,
            "source_span_summary": "Thunder Gate anomaly -> ritual hall reveal",
            "rhythm_rationale": "Keep the setup and cliffhanger in one stable 9-page group.",
        },
        "continuity_context": {
            "inherit_global_locks": True,
            "same_visual_dna_rule": (
                "Reuse the same rendering medium, line system, shadow method, lettering feeling, "
                "and character age ratio across all groups."
            ),
            "previous_group_hook": "",
            "next_group_hook": "Ritual hall first appears",
        },
        "generation_contract": {
            "provider": "seedream",
            "call_mode": "single_request_sequential",
            "image_count": 9,
            "page_aspect_ratio": "9:16",
            "hard_constraints": [
                "Generate exactly 9 separate images/pages.",
                "Do not create a nine-grid collage.",
                "Do not create nine variations of the same scene.",
                "Every page must contain multiple comic panels, never a single full-page illustration.",
                "Keep character and scene consistency across all pages.",
                "Place a small page number in the bottom-right corner of every page, using digits 1-9 only.",
            ],
        },
        "type_stack_ref": {
            "method_kernel": "comic-core-v1",
            "base": "_base",
            "primary": "经典漫画叙事",
            "secondary": ["少年战斗冒险"],
            "platform": ["条漫平台"],
            "audience": ["少年热血受众"],
            "active_packs": ["_base", "经典漫画叙事", "少年战斗冒险", "条漫平台", "少年热血受众"],
        },
        "type_pack_context": {
            "resolution_mode": "single-layer-genre-comic-type-pack",
            "knowledge_refs": [
                ".agents/skills/comic/type-packs/漫画/少年战斗冒险/少年战斗冒险.md"
            ],
            "knowledge_digest": [
                "少年战斗冒险 > 核心冲突引擎: 主角在更大的世界规则里升级、立誓、结盟、翻盘。",
                "少年战斗冒险 > 翻页机制: 招式命名、宿敌惊讶、代价上身是高价值翻页点。",
            ],
            "pack_revisions": {
                "少年战斗冒险": "dynamic-runtime"
            },
            "semantic_tags": ["oath", "destiny", "page-impact"],
            "control_surface": {
                "conflict_engine": {
                    "premise": "主角在更大的规则世界里被迫升级、立誓、结盟、翻盘。",
                    "escalation_loop": "压制现状 -> 立场显形 -> 新理解或新代价 -> 胜负改写",
                },
                "role_matrix": {
                    "protagonist": "主动求胜且短板可见的成长者",
                    "rival_or_counterforce": "兼具战力和价值镜像的宿敌",
                },
                "page_turn_mechanism": {
                    "turn_trigger": "招式命名、宿敌惊讶、代价上身",
                    "reveal_pattern": "翻页后先给姿态和结果，再补局部解释",
                },
                "panel_grammar": {
                    "dominant_panel_shapes": ["爆点大跨页", "斜切突进格"],
                },
                "visual_carrier": {
                    "primary": ["身体姿态", "速度轨迹", "宿敌对视"],
                },
                "dialogue_register": {
                    "line_length": "short",
                    "exposition_rule": "说明性台词必须让位于动作和结果",
                },
                "motif_system": {
                    "recurring_motifs": ["誓言", "宿命双生", "代价印记"],
                },
                "failure_modes": ["设定说明压过动作因果"],
            },
            "control_surface_digest": [
                "control_surface.conflict_engine.premise: 主角在更大的规则世界里被迫升级、立誓、结盟、翻盘。",
                "control_surface.page_turn_mechanism.turn_trigger: 招式命名、宿敌惊讶、代价上身",
                "control_surface.panel_grammar.dominant_panel_shapes: 爆点大跨页, 斜切突进格",
                "control_surface.visual_carrier.primary: 身体姿态, 速度轨迹, 宿敌对视",
            ],
            "stage_projection": {
                "script_adaptation": {"adaptation_posture": "comic-first"},
                "nine_blade_prompting": {"layout_bias": ["splash", "diagonal"]},
                "image_generation": {"render_bias": ["sharp comic contrast", "ritual silhouette"]},
                "animation_generation": {"motion_bias": ["charged pause", "impact release"]},
                "episode_poster": {"poster_bias": ["forbidden-title"]}
            },
        },
        "main_character_lock": {
            "character_id": "protagonist",
            "name": "Sun Wukong",
            "anchor_prompt": (
                "Character locked across all panels: Sun Wukong, muscular monkey demon, golden fur, "
                "consistent face, consistent costume, consistent silhouette."
            ),
        },
        "scene_continuity_bible": {
            "default_rule": (
                "Keep recurring locations consistent in architecture, landmark props, "
                "lighting mood, and spatial geography across all relevant pages."
            ),
            "scene_locks": [
                {
                    "scene_id": "thunder_gate",
                    "name": "Thunder Gate Courtyard",
                    "anchor_prompt": (
                        "Scene locked across relevant pages: Thunder Gate Courtyard, "
                        "black stone gate, lightning totems, cracked steps, storm-dark sky, "
                        "consistent architecture, landmark props, lighting mood and spatial geography."
                    ),
                }
            ],
        },
        "style_bible": {
            "base_style": "cinematic manga comic realism",
            "rendering_medium": "inked line art with screentone shading and printed comic texture",
            "layout_directive": "multiple comic panels, bold gutters, dynamic panel borders, oversized SFX",
        },
        "character_locks": [
            {
                "character_id": "companion",
                "name": "Zhu Bajie",
                "anchor_prompt": (
                    "Character locked across all relevant pages: Zhu Bajie, heavy build, "
                    "round snout, patched vest, clearly distinguishable from Sun Wukong."
                ),
            }
        ],
        "comic_text_system": {
            "dialogue": {
                "visual_form": "speech bubble containing clear legible Chinese text",
                "placement_rule": "near the speaking character, inside the panel, not at the far edge",
                "legibility_rule": "clear legible Chinese text, short sentence, do not cover faces",
                "max_chars": 18,
            },
            "narration": {
                "visual_form": "rectangular caption box containing clear legible Chinese text",
                "placement_rule": "panel edge or gutter edge caption, readable and not blocking key acting",
                "legibility_rule": "clear legible Chinese text for narration compression",
                "max_chars": 24,
            },
            "inner_monologue": {
                "visual_form": "thought bubble or inner monologue caption containing clear legible Chinese text",
                "placement_rule": "near the thinker or as an inner caption inside the panel, clearly different from dialogue",
                "legibility_rule": "clear legible Chinese text, emotionally concise",
                "max_chars": 20,
            },
            "sfx": {
                "visual_form": "large hand-lettered comic SFX text integrated inside the panel",
                "placement_rule": "integrated with the action source inside the panel, never floating like a sticker",
                "legibility_rule": "clear legible Chinese onomatopoeia as part of the drawing",
                "max_chars": 6,
            },
        },
        "pages": pages,
        "global_negative_prompt": "collage, nine variations, unreadable Chinese text, watermark",
    }


def _load_json(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as fh:
        data = json.load(fh)
    if not isinstance(data, dict):
        raise ValueError("root must be a JSON object")
    return normalize_nine_blade_prompt_data(data)


def _text_block(title: str, value: Any) -> str:
    if value in (None, "", [], {}):
        return ""
    if isinstance(value, str):
        body = value
    else:
        body = json.dumps(value, ensure_ascii=False, indent=2)
    return f"\n## {title}\n{body}\n"


def _compact_text(value: Any) -> str:
    if value in (None, "", [], {}):
        return ""
    if isinstance(value, str):
        return re.sub(r"\s+", " ", value).strip()
    return json.dumps(value, ensure_ascii=False, separators=(",", ":"))


def _flatten_structure_lines(
    value: Any,
    *,
    prefix: str = "",
    max_lines: int = 20,
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
                label = current_prefix or "items"
                lines.append(f"{label}: {', '.join(compact_items[:8])}")
            return
        compact = _compact_text(node)
        if compact:
            label = current_prefix or "value"
            lines.append(f"{label}: {compact}")

    walk(value, prefix, 0)
    return lines[:max_lines]


def _bullet_block(title: str, lines: list[str]) -> str:
    cleaned = [line.strip() for line in lines if line and line.strip()]
    if not cleaned:
        return ""
    body = "\n".join(f"- {line}" for line in cleaned)
    return f"\n## {title}\n{body}\n"


def _summarize_type_pack_context(value: Any) -> list[str]:
    if not isinstance(value, dict):
        return []
    lines: list[str] = []
    active_packs = value.get("active_packs")
    if isinstance(active_packs, list) and active_packs:
        lines.append(f"active_packs: {', '.join(str(item) for item in active_packs)}")
    semantic_tags = value.get("semantic_tags")
    if isinstance(semantic_tags, list) and semantic_tags:
        lines.append(f"semantic_tags: {', '.join(str(item) for item in semantic_tags[:10])}")
    projection_summary = value.get("projection_summary")
    if isinstance(projection_summary, dict):
        for key in ("nine_blade_prompting", "image_generation", "animation_generation"):
            summary = _compact_text(projection_summary.get(key))
            if summary:
                lines.append(f"{key}: {summary}")
    stage_projection = value.get("stage_projection")
    if isinstance(stage_projection, dict):
        for key in ("nine_blade_prompting", "image_generation"):
            projection = stage_projection.get(key)
            summary = _compact_text(projection)
            if summary:
                lines.append(f"{key}_detail: {summary}")
    knowledge_digest = value.get("knowledge_digest")
    if isinstance(knowledge_digest, list) and knowledge_digest:
        lines.append(f"knowledge_digest: {' | '.join(str(item) for item in knowledge_digest[:8])}")
    return lines


def _summarize_control_surface(value: Any, *, max_lines: int = 20) -> list[str]:
    if not isinstance(value, dict):
        return []
    digest = value.get("control_surface_digest")
    if isinstance(digest, list) and digest:
        return [str(item).strip() for item in digest[:max_lines] if str(item).strip()]
    control_surface = value.get("control_surface")
    if isinstance(control_surface, dict):
        return _flatten_structure_lines(control_surface, prefix="control_surface", max_lines=max_lines)
    return []


def _summarize_style_bible(value: Any) -> list[str]:
    if not isinstance(value, dict):
        return []
    lines: list[str] = []
    for key in (
        "base_style",
        "layout_directive",
        "style_anchor_prompt",
        "style_continuity_rule",
        "rendering",
        "color_script",
        "quality_tags",
    ):
        summary = _compact_text(value.get(key))
        if summary:
            lines.append(f"{key}: {summary}")
    keywords = value.get("manga_style_keywords")
    if isinstance(keywords, list) and keywords:
        lines.append(f"manga_style_keywords: {', '.join(str(item) for item in keywords[:12])}")
    shifts = value.get("forbidden_style_shifts")
    if isinstance(shifts, list) and shifts:
        lines.append(f"forbidden_style_shifts: {', '.join(str(item) for item in shifts[:8])}")
    return lines


def _summarize_text_system(value: Any) -> list[str]:
    if not isinstance(value, dict):
        return []
    lines: list[str] = []
    for key in ("dialogue", "narration", "inner_monologue", "sfx"):
        entry = value.get(key)
        if not isinstance(entry, dict):
            continue
        lines.append(
            f"{key}: form={_compact_text(entry.get('visual_form'))}; "
            f"placement={_compact_text(entry.get('placement_rule'))}; "
            f"legibility={_compact_text(entry.get('legibility_rule'))}; "
            f"max_chars={entry.get('max_chars')}"
        )
    return lines


def _summarize_lock(lock: dict[str, Any], *, include_id: bool = False) -> str:
    if not isinstance(lock, dict):
        return ""
    parts: list[str] = []
    if include_id:
        raw_id = str(lock.get("character_id") or lock.get("scene_id") or "").strip()
        if raw_id:
            parts.append(f"id={raw_id}")
    name = str(lock.get("name", "")).strip()
    if name:
        parts.append(f"name={name}")
    anchor_prompt = _compact_text(lock.get("anchor_prompt"))
    if anchor_prompt:
        parts.append(f"anchor={anchor_prompt}")
    return "; ".join(parts)


def _summarize_panel(panel: Any) -> str:
    if not isinstance(panel, dict):
        return ""
    panel_id = str(panel.get("panel_id", "")).strip()
    shot = _compact_text(panel.get("shot"))
    action = _compact_text(panel.get("action"))
    techniques = panel.get("comic_techniques", [])
    technique_text = ", ".join(str(item) for item in techniques[:4]) if isinstance(techniques, list) else ""
    slot_summaries: list[str] = []
    text_slots = panel.get("text_slots", [])
    if isinstance(text_slots, list):
        for slot in text_slots[:4]:
            if not isinstance(slot, dict):
                continue
            slot_type = str(slot.get("type", "")).strip()
            slot_text = _compact_text(slot.get("text"))
            if slot_type and slot_text:
                slot_summaries.append(f"{slot_type}={slot_text}")
    parts = [
        f"{panel_id}" if panel_id else "",
        f"shot={shot}" if shot else "",
        f"action={action}" if action else "",
        f"techniques={technique_text}" if technique_text else "",
        f"text={'; '.join(slot_summaries)}" if slot_summaries else "",
    ]
    return " | ".join(part for part in parts if part)


def _character_map(data: dict[str, Any]) -> dict[str, dict[str, Any]]:
    result: dict[str, dict[str, Any]] = {}
    main_character_lock = data.get("main_character_lock", {})
    if isinstance(main_character_lock, dict):
        character_id = str(main_character_lock.get("character_id", "")).strip()
        if character_id:
            result[character_id] = main_character_lock
    character_locks = data.get("character_locks", [])
    if isinstance(character_locks, list):
        for lock in character_locks:
            if not isinstance(lock, dict):
                continue
            character_id = str(lock.get("character_id", "")).strip()
            if character_id:
                result[character_id] = lock
    return result


def _scene_map(data: dict[str, Any]) -> dict[str, dict[str, Any]]:
    result: dict[str, dict[str, Any]] = {}
    scene_bible = data.get("scene_continuity_bible", {})
    if not isinstance(scene_bible, dict):
        return result
    scene_locks = scene_bible.get("scene_locks", [])
    if not isinstance(scene_locks, list):
        return result
    for scene_lock in scene_locks:
        if not isinstance(scene_lock, dict):
            continue
        scene_id = str(scene_lock.get("scene_id", "")).strip()
        if scene_id:
            result[scene_id] = scene_lock
    return result


def compile_master_prompt(data: dict[str, Any]) -> str:
    page_group = data.get("page_group", {})
    continuity_context = data.get("continuity_context", {})
    contract = data.get("generation_contract", {})
    type_stack_ref = data.get("type_stack_ref", {})
    type_pack_context = data.get("type_pack_context", {})
    hard_constraints = contract.get("hard_constraints", [])
    main_character_lock = data.get("main_character_lock", {})
    scene_continuity_bible = data.get("scene_continuity_bible", {})
    style_bible = data.get("style_bible", {})
    character_locks = data.get("character_locks", [])
    comic_text_system = data.get("comic_text_system", {})
    pages = data.get("pages", [])
    negative = data.get("global_negative_prompt", "")
    character_map = _character_map(data)
    scene_map = _scene_map(data)

    parts: list[str] = [
        "Generate exactly 9 separate images/pages. Each output image is one complete vertical 9:16 comic page. "
        "Do not create a nine-grid collage, contact sheet, or one image containing all pages. "
        "Do not create nine variations of the same scene. "
        "The nine images are consecutive comic pages from the same story, in page order from Page 1 to Page 9. "
        "Place a small page number in the bottom-right corner of every page, using digits 1-9 only."
    ]
    parts.append(_bullet_block("Hard Constraints", [str(item) for item in hard_constraints]))
    parts.append(
        _bullet_block(
            "Page Group Meta",
            [
                f"group_id: {page_group.get('group_id')}",
                f"group_index: {page_group.get('group_index')}/{page_group.get('total_groups')}",
                f"source_span_summary: {_compact_text(page_group.get('source_span_summary'))}",
                f"rhythm_rationale: {_compact_text(page_group.get('rhythm_rationale'))}",
            ],
        )
    )
    parts.append(
        _bullet_block(
            "Continuity Context",
            [
                f"inherit_global_locks: {continuity_context.get('inherit_global_locks')}",
                f"same_visual_dna_rule: {_compact_text(continuity_context.get('same_visual_dna_rule'))}",
                f"previous_group_hook: {_compact_text(continuity_context.get('previous_group_hook'))}",
                f"next_group_hook: {_compact_text(continuity_context.get('next_group_hook'))}",
            ],
        )
    )
    parts.append(
        _bullet_block(
            "Type Stack Ref",
            [
                f"method_kernel: {type_stack_ref.get('method_kernel')}",
                f"active_packs: {', '.join(str(item) for item in type_stack_ref.get('active_packs', []))}",
                f"secondary: {', '.join(str(item) for item in type_stack_ref.get('secondary', []))}",
                f"platform: {', '.join(str(item) for item in type_stack_ref.get('platform', []))}",
                f"audience: {', '.join(str(item) for item in type_stack_ref.get('audience', []))}",
            ],
        )
    )
    parts.append(_bullet_block("Type Pack Context", _summarize_type_pack_context(type_pack_context)))
    parts.append(_bullet_block("Type Pack Control Surface", _summarize_control_surface(type_pack_context)))
    parts.append(_bullet_block("Main Character Lock", [_summarize_lock(main_character_lock, include_id=True)]))
    scene_bible_lines = [
        f"default_rule: {_compact_text(scene_continuity_bible.get('default_rule'))}"
    ]
    scene_locks = scene_continuity_bible.get("scene_locks", [])
    if isinstance(scene_locks, list):
        scene_bible_lines.extend(_summarize_lock(lock, include_id=True) for lock in scene_locks[:6])
    parts.append(_bullet_block("Scene Continuity Bible", scene_bible_lines))
    parts.append(_bullet_block("Global Style Bible", _summarize_style_bible(style_bible)))
    parts.append(
        _bullet_block(
            "Character Locks",
            [_summarize_lock(lock, include_id=True) for lock in character_locks[:10] if isinstance(lock, dict)],
        )
    )
    parts.append(_bullet_block("Comic Text System", _summarize_text_system(comic_text_system)))

    for page in pages:
        page_number = page.get("page_number")
        page_role = page.get("page_role", "")
        layout = page.get("layout", {})
        prompt = page.get("positive_prompt", "")
        panels = page.get("panels", [])
        active_character_ids = page.get("active_character_ids", [])
        scene_id = str(page.get("scene_id", "")).strip()
        page_number_overlay = page.get("page_number_overlay", {})
        active_character_locks = [
            character_map[character_id]
            for character_id in active_character_ids
            if isinstance(active_character_ids, list) and character_id in character_map
        ]
        scene_lock = scene_map.get(scene_id, {})
        page_lines = [
            f"This output image must be Page {page_number} only, a complete vertical 9:16 comic page, not a collage.",
            f"page_role: {page_role}",
            f"source_fragment: {_compact_text(page.get('source_fragment'))}",
            f"active_character_ids: {', '.join(str(item) for item in active_character_ids)}",
            "Active character locks:",
        ]
        page_lines.extend(
            f"  - {_summarize_lock(lock, include_id=True)}"
            for lock in active_character_locks
            if isinstance(lock, dict)
        )
        scene_summary = _summarize_lock(scene_lock, include_id=True)
        if scene_summary:
            page_lines.append(f"Scene continuity lock: {scene_summary}")
        page_lines.append(
            "Page number overlay: "
            f"text={_compact_text(page_number_overlay.get('text'))}; "
            f"position={_compact_text(page_number_overlay.get('position'))}; "
            f"style={_compact_text(page_number_overlay.get('style_prompt'))}"
        )
        page_lines.append(
            "Layout: "
            f"layout_id={_compact_text(layout.get('layout_id'))}; "
            f"panel_count={layout.get('panel_count')}; "
            f"panel_ratios={', '.join(str(item) for item in layout.get('panel_ratios', [])) if isinstance(layout.get('panel_ratios'), list) else ''}"
        )
        page_lines.append("Panels and text slots:")
        page_lines.extend(f"  - {_summarize_panel(panel)}" for panel in panels if _summarize_panel(panel))
        page_lines.append(
            "Page focus prompt: "
            f"highlight {_compact_text(page.get('source_fragment'))}; "
            f"use {_compact_text(layout.get('layout_id'))}; "
            f"respect all active character locks and the active scene lock; "
            f"show bottom-right digits-only page number {page_number}; "
            f"keep readable visual storytelling for {scene_lock.get('name', scene_id)}."
        )
        parts.append(f"\n## Page {page_number}: {page_role}\n" + "\n".join(page_lines) + "\n")

    parts.append(_bullet_block("Global Negative Prompt", [negative]))
    return "\n".join(part for part in parts if part)


def _slugify(value: str) -> str:
    slug = re.sub(r"[^A-Za-z0-9_-]+", "-", value.strip())
    slug = re.sub(r"-{2,}", "-", slug).strip("-_")
    return slug or "page-group"


def _group_meta(data: dict[str, Any]) -> dict[str, Any]:
    page_group = data.get("page_group", {})
    return page_group if isinstance(page_group, dict) else {}


def _derive_group_slug(data: dict[str, Any], json_path: Path) -> str:
    page_group = _group_meta(data)
    group_id = str(page_group.get("group_id", "")).strip()
    if group_id:
        return _slugify(group_id)

    stem = json_path.stem
    stem = re.sub(r"[-_]?nine_blade_comic_prompts$", "", stem)
    stem = stem.strip("-_")
    if stem:
        return _slugify(stem)
    return "page-group"


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


def _write_json(path: Path, payload: dict[str, Any]) -> None:
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")


def _canonicalize_page_filenames(
    saved_files: list[str], output_dir: Path, filename_stem_prefix: str
) -> list[str]:
    renamed_files: list[str] = []
    for index, raw_path in enumerate(saved_files, start=1):
        path = Path(raw_path)
        suffix = path.suffix or ".png"
        canonical_path = output_dir / f"{filename_stem_prefix}{index:02d}{suffix}"
        if path.resolve() != canonical_path.resolve():
            path.replace(canonical_path)
        renamed_files.append(str(canonical_path))
    return renamed_files


def _infer_project_root(json_path: Path, project_name: str | None) -> Path:
    parts = json_path.resolve().parts
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

    inferred_name = project_name or json_path.stem
    return REPO_ROOT / "projects/comic" / inferred_name


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Legacy fallback: run Seedream once for 9 comic pages from JSON"
    )
    parser.add_argument("json_path", nargs="?", type=Path)
    parser.add_argument("--output-dir", type=Path)
    parser.add_argument("--project-name", help="Comic project name used when JSON is outside projects/comic/<name>/")
    parser.add_argument("--filename-prefix")
    parser.add_argument("--size", default="2K")
    parser.add_argument("--timeout", type=int, default=600)
    parser.add_argument("--dry-run", action="store_true", help="Write legacy Seedream plan only")
    parser.add_argument("--execute", action="store_true", help="Actually call legacy Seedream fallback")
    parser.add_argument("--self-test", action="store_true", help="Run an in-memory compiler self-test")
    parser.add_argument("--no-watermark", action="store_true", default=True)
    args = parser.parse_args()

    if args.self_test:
        sample = _self_test_data()
        with tempfile.TemporaryDirectory() as tmp_dir:
            sample_path = Path(tmp_dir) / "page-group-01-nine_blade_comic_prompts.json"
            _write_json(sample_path, sample)
            validator_result = _run_validator(sample_path)
            if validator_result.returncode != 0:
                print(validator_result.stdout, end="")
                print(validator_result.stderr, end="", file=sys.stderr)
                print("FAIL self-test: sample payload does not pass stage-2 validator", file=sys.stderr)
                return validator_result.returncode

        prompt = compile_master_prompt(sample)
        required = [
            "Generate exactly 9 separate images/pages",
            "Do not create a nine-grid collage",
            "Do not create nine variations of the same scene",
            "Page Group Meta",
            "Continuity Context",
            "Page 9",
            "vertical 9:16",
            "bottom-right corner",
            "digits 1-9 only",
            "Scene Continuity Bible",
            "Active character locks",
            "Type Pack Control Surface",
            "control_surface.conflict_engine.premise",
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
    page_group = _group_meta(data)
    group_slug = _derive_group_slug(data, json_path)
    project_root = _infer_project_root(json_path, args.project_name)
    output_dir = (args.output_dir.resolve() if args.output_dir else (project_root / "3-漫画生成" / group_slug))
    output_dir.mkdir(parents=True, exist_ok=True)
    user_supplied_prefix = bool(args.filename_prefix)
    shared_output_dir = args.output_dir is not None and output_dir.name != group_slug
    auto_filename_prefix = f"{group_slug}-page" if shared_output_dir else "page"
    prefix = args.filename_prefix or auto_filename_prefix
    seedream_report = output_dir / f"{group_slug}-seedream_report_{_now_stamp()}.json"
    master_prompt_path = output_dir / f"{group_slug}-seedream_master_prompt.txt"
    comic_report_path = output_dir / f"{group_slug}-comic_generation_report.json"
    generation_plan_path = output_dir / f"{group_slug}-generation_plan.json"

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
        "page_group": page_group,
        "group_slug": group_slug,
        "output_dir": str(output_dir),
        "master_prompt_path": str(master_prompt_path),
        "seedream_report": str(seedream_report),
        "output_filename_scheme": (
            f"{prefix}01.ext .. {prefix}09.ext" if not user_supplied_prefix else "custom prefix"
        ),
        "seedream_command_preview": [
            token if token != master_prompt else "<compiled master prompt>"
            for token in command
        ],
        "expected_result_count": 9,
    }
    master_prompt_path.write_text(master_prompt, encoding="utf-8")
    _write_json(generation_plan_path, plan)
    pending_report = {
        "ok": False,
        "status": "pending",
        "input_json": str(json_path),
        "page_group": page_group,
        "group_slug": group_slug,
        "output_dir": str(output_dir),
        "generation_plan_path": str(generation_plan_path),
        "master_prompt_path": str(master_prompt_path),
        "seedream_report": str(seedream_report),
        "expected_result_count": 9,
        "saved_files": [],
    }
    _write_json(comic_report_path, pending_report)

    if args.dry_run:
        print(f"PASS dry-run: {generation_plan_path}")
        return 0

    result = subprocess.run(command, cwd=str(REPO_ROOT), text=True, check=False)
    if result.returncode != 0:
        _write_json(
            comic_report_path,
            {
                **pending_report,
                "status": "failed",
                "error": "seedream subprocess returned non-zero exit code",
                "seedream_exit_code": result.returncode,
            },
        )
        return result.returncode

    report = _read_seedream_report(seedream_report)
    saved_files = report.get("saved_files", [])
    if report.get("result_count") != 9 or not isinstance(saved_files, list) or len(saved_files) != 9:
        _write_json(
            comic_report_path,
            {
                **pending_report,
                "status": "failed",
                "error": "Seedream did not return exactly 9 saved files",
                "seedream_result_count": report.get("result_count"),
                "saved_files": saved_files if isinstance(saved_files, list) else [],
                "stream_event_count": report.get("stream_event_count"),
                "stream_event_types": report.get("stream_event_types"),
            },
        )
        print("FAIL: Seedream did not return exactly 9 saved files", file=sys.stderr)
        return 3

    if not user_supplied_prefix:
        saved_files = _canonicalize_page_filenames(saved_files, output_dir, prefix)
        report["saved_files"] = saved_files
        _write_json(seedream_report, report)

    comic_report = {
        "ok": True,
        "status": "completed",
        "input_json": str(json_path),
        "page_group": page_group,
        "group_slug": group_slug,
        "output_dir": str(output_dir),
        "generation_plan_path": str(generation_plan_path),
        "master_prompt_path": str(master_prompt_path),
        "seedream_report": str(seedream_report),
        "saved_files": saved_files,
        "result_count": report.get("result_count"),
        "stream_event_count": report.get("stream_event_count"),
        "stream_event_types": report.get("stream_event_types"),
    }
    _write_json(comic_report_path, comic_report)
    print(f"PASS generated 9 comic pages: {comic_report_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
