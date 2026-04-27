#!/usr/bin/env python3
"""Validate nine_blade_comic_prompts.v1 JSON for downstream comic generation."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

DATA_MODULES_ROOT = Path(__file__).resolve().parents[2] / "scripts"
if str(DATA_MODULES_ROOT) not in sys.path:
    sys.path.insert(0, str(DATA_MODULES_ROOT))

from data_modules.nine_blade_prompt_normalizer import normalize_nine_blade_prompt_data


REQUIRED_HARD_CONSTRAINTS = [
    "9 separate",
    "nine-grid",
    "variations of the same scene",
    "multiple comic panels",
]

STYLE_KEYWORDS = [
    "manga",
    "comic",
    "panel",
    "gutter",
    "ink",
    "line art",
    "screentone",
    "sfx",
    "printed",
]

DYNAMIC_LAYOUT_KEYWORDS = [
    "splash",
    "inset",
    "diagonal",
    "split",
    "cascade",
    "impact",
    "cliffhanger",
    "border",
    "zigzag",
    "asymmetric",
    "overlapping",
    "noir",
]

MAIN_CHARACTER_ANCHOR_KEYWORDS = [
    "character locked across all panels",
    "consistent face",
    "consistent costume",
]

TEXT_SYSTEM_RULES = {
    "dialogue": {
        "max_chars": 18,
        "requires_speaker": True,
        "bubble_styles": {"speech_bubble"},
        "placements": {"near_speaker_inside_panel"},
        "inside_panel": True,
        "system_keywords": {
            "visual_form": ("speech", "bubble"),
            "placement_rule": ("speaker", "panel"),
            "legibility_rule": ("legible", "chinese"),
        },
        "prompt_keywords": ("speech bubble", "speaker"),
    },
    "narration": {
        "max_chars": 24,
        "requires_speaker": False,
        "bubble_styles": {"caption_box"},
        "placements": {"panel_edge_caption", "gutter_edge_caption"},
        "inside_panel": None,
        "system_keywords": {
            "visual_form": ("caption",),
            "placement_rule": ("caption",),
            "legibility_rule": ("legible", "chinese"),
        },
        "prompt_keywords": ("caption",),
    },
    "inner_monologue": {
        "max_chars": 20,
        "requires_speaker": True,
        "bubble_styles": {"thought_bubble", "inner_caption"},
        "placements": {"near_thinker_inside_panel", "inner_caption_inside_panel"},
        "inside_panel": True,
        "system_keywords": {
            "visual_form": ("thought", "inner"),
            "placement_rule": ("thinker", "caption", "panel"),
            "legibility_rule": ("legible", "chinese"),
        },
        "prompt_keywords": ("thought bubble", "inner caption"),
    },
    "sfx": {
        "max_chars": 6,
        "requires_speaker": False,
        "bubble_styles": {"integrated_sfx"},
        "placements": {"integrated_with_action_inside_panel"},
        "inside_panel": True,
        "system_keywords": {
            "visual_form": ("sfx",),
            "placement_rule": ("action", "panel"),
            "legibility_rule": ("legible", "chinese"),
        },
        "prompt_keywords": ("sfx",),
    },
}


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
        prompt_parts = [
            "cinematic comic page, vertical 9:16 aspect ratio",
            f"Page {page_number}",
            "Character locked across all panels: Sun Wukong, a muscular monkey demon with golden fur, consistent face, consistent costume, consistent silhouette",
            "render clear legible Chinese text, use speech bubbles near speakers for dialogue, rectangular caption boxes for narration, thought bubbles or inner captions clearly different from dialogue for inner monologue, and integrated SFX inside the action panel",
        ]
        if len(active_character_ids) >= 2:
            prompt_parts.append(
                "Zhu Bajie remains visually consistent and clearly distinguishable with heavy build, round snout, patched vest"
            )
        prompt_parts.extend(
            [
                "scene locked across relevant pages: Thunder Gate Courtyard, black stone gate, lightning totems, consistent architecture and landmark props",
                f"place page number \"{page_number}\" in the bottom-right corner, digits only",
                "keep character and scene consistency across all pages",
                f"unique visible action {page_number}",
            ]
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
                    "panel_ratios": ["dominant irregular panel 70%", "supporting inset/reaction panel 30%"],
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
                    }
                ],
                "page_number_overlay": {
                    "text": str(page_number),
                    "position": "bottom-right",
                    "style_prompt": (
                        f"place page number \"{page_number}\" in the bottom-right corner, "
                        "digits only, small but readable"
                    ),
                },
                "positive_prompt": ", ".join(prompt_parts),
            }
        )
    return {
        "schema_version": "nine_blade_comic_prompts.v1",
        "page_group": {
            "group_id": "page-group-01",
            "group_index": 1,
            "total_groups": 1,
            "estimated_source_chars": 480,
            "target_source_chars": 500,
            "source_span_summary": "Thunder Gate anomaly -> ritual hall reveal",
            "rhythm_rationale": (
                "Cover the full setup, escalation, and cliffhanger of the current group without "
                "mechanically cutting a scene boundary."
            ),
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
            "provider": "cli-imagegen",
            "call_mode": "per_page_batch",
            "image_count": 9,
            "page_aspect_ratio": "9:16",
            "imagegen": {
                "tool_skill_path": ".agents/skills/cli/imagegen",
                "model": "gpt-image-2",
                "size": "1152x2048",
            },
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
            "secondary": ["推理悬疑"],
            "platform": ["条漫平台"],
            "audience": ["情绪强冲突受众"],
            "active_packs": ["_base", "经典漫画叙事", "推理悬疑", "条漫平台", "情绪强冲突受众"],
        },
        "type_pack_context": {
            "resolution_mode": "single-layer-genre-comic-type-pack",
            "knowledge_refs": [
                ".agents/skills/comic/2-九刀流漫画提示词/types/漫画/推理悬疑/推理悬疑.md"
            ],
            "knowledge_digest": [
                "危险要比解释先到。",
                "真相必须分层释放。"
            ],
            "control_surface_digest": [
                "control_surface.conflict_engine.premise: 线索链缓慢点亮，而真相始终晚半步抵达。"
            ],
            "semantic_tags": ["withheld-truth", "threat"],
            "pack_revisions": {
                "推理悬疑": "dynamic-runtime"
            },
            "control_surface": {
                "conflict_engine": {"premise": "线索链缓慢点亮，而真相始终晚半步抵达。"},
                "role_matrix": {"protagonist": "有盲区和代价的观察者或追查者"},
                "page_turn_mechanism": {"turn_trigger": "页尾未完成动作、半露真相、证据细节"},
                "panel_grammar": {"dominant_panel_shapes": ["细节特写格", "页尾悬停格"]},
                "visual_carrier": {"primary": ["物证细节", "视线方向", "空间异常"]},
                "dialogue_register": {"exposition_rule": "解释必须晚于证据显影"},
                "motif_system": {"recurring_motifs": ["门缝", "录音", "重复场景再看"]},
                "failure_modes": ["只有反转，没有可回溯线索"]
            },
            "projection_summary": {
                "nine_blade_prompting": "多用静默格、细节特写、翻页机关。"
            },
            "stage_projection": {
                "script_adaptation": {"adaptation_posture": "comic-first"},
                "nine_blade_prompting": {"layout_bias": ["silent beat", "detail close-up"]},
                "image_generation": {"render_bias": ["shadow pressure"]},
                "animation_generation": {"motion_bias": ["slow push", "threat pause"]},
                "episode_poster": {"poster_bias": ["door-title"]}
            },
        },
        "main_character_lock": {
            "character_id": "protagonist",
            "name": "Sun Wukong",
            "anchor_prompt": (
                "Character locked across all panels: Sun Wukong, "
                "a muscular monkey demon with golden fur, a pronounced thunder-god mouth, "
                "sunken eyes with bright golden pupils, wearing a tattered grey-brown Daoist robe, "
                "consistent face, costume, silhouette and color palette in every panel and every page."
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
            "base_style": "cinematic comic realism",
            "manga_style_keywords": [
                "dynamic manga paneling",
                "dramatic inked line art",
                "high contrast black gutters",
                "oversized SFX",
            ],
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
        "global_negative_prompt": (
            "collage, nine variations, unreadable Chinese text, watermark"
        ),
    }


def _load_json(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as fh:
        data = json.load(fh)
    if not isinstance(data, dict):
        raise ValueError("root must be a JSON object")
    return data


def _contains(texts: list[str], needle: str) -> bool:
    needle = needle.lower()
    return any(needle in text.lower() for text in texts)


def _has_character_scene_consistency(text: str) -> bool:
    lower = text.lower()
    has_character = "character" in lower
    has_scene = "scene" in lower or "location" in lower
    has_consistency = (
        "consistent" in lower
        or "consistency" in lower
        or "continuity" in lower
    )
    return has_character and has_scene and has_consistency


def _has_main_character_anchor(text: str, character_name: str) -> bool:
    lower = text.lower()
    if character_name.lower() not in lower:
        return False
    return any(keyword in lower for keyword in MAIN_CHARACTER_ANCHOR_KEYWORDS)


def _has_bottom_right_numeric_page_number(text: str, page_number: int) -> bool:
    lower = text.lower()
    has_position = "bottom-right" in lower or "bottom right" in lower
    has_numeric_only = (
        "digits only" in lower
        or "numeric only" in lower
        or "pure digits" in lower
    )
    has_number = f"\"{page_number}\"" in text or f" {page_number} " in f" {text} "
    return has_position and has_numeric_only and has_number


def _mentioned_names(text: str, names: list[str]) -> list[str]:
    lower = text.lower()
    return [name for name in names if name.lower() in lower]


def _stringify(value: Any) -> str:
    if isinstance(value, str):
        return value
    return json.dumps(value, ensure_ascii=False)


def _contains_any(text: str, needles: tuple[str, ...]) -> bool:
    lower = text.lower()
    return any(needle in lower for needle in needles)


def validate(data: dict[str, Any]) -> list[str]:
    data = normalize_nine_blade_prompt_data(data)
    errors: list[str] = []

    if data.get("schema_version") != "nine_blade_comic_prompts.v1":
        errors.append("schema_version must be nine_blade_comic_prompts.v1")

    page_group = data.get("page_group")
    if page_group is not None:
        if not isinstance(page_group, dict):
            errors.append("page_group must be an object when present")
            page_group = {}
        group_id = str(page_group.get("group_id", "")).strip()
        if not group_id:
            errors.append("page_group.group_id must be a non-empty string when present")
        group_index = page_group.get("group_index")
        total_groups = page_group.get("total_groups")
        if not isinstance(group_index, int) or group_index < 1:
            errors.append("page_group.group_index must be an integer >= 1 when present")
        if not isinstance(total_groups, int) or total_groups < 1:
            errors.append("page_group.total_groups must be an integer >= 1 when present")
        if isinstance(group_index, int) and isinstance(total_groups, int) and group_index > total_groups:
            errors.append("page_group.group_index must be <= page_group.total_groups")
        estimated_source_chars = page_group.get("estimated_source_chars")
        if not isinstance(estimated_source_chars, int) or estimated_source_chars < 1:
            errors.append("page_group.estimated_source_chars must be an integer >= 1 when present")
        target_source_chars = page_group.get("target_source_chars")
        if not isinstance(target_source_chars, int) or target_source_chars < 1:
            errors.append("page_group.target_source_chars must be an integer >= 1 when present")
        if len(str(page_group.get("source_span_summary", "")).strip()) < 4:
            errors.append("page_group.source_span_summary must be a descriptive string when present")
        if len(str(page_group.get("rhythm_rationale", "")).strip()) < 12:
            errors.append("page_group.rhythm_rationale must explain the grouping rationale when present")

    continuity_context = data.get("continuity_context")
    if continuity_context is not None:
        if not isinstance(continuity_context, dict):
            errors.append("continuity_context must be an object when present")
            continuity_context = {}
        if not isinstance(continuity_context.get("inherit_global_locks"), bool):
            errors.append("continuity_context.inherit_global_locks must be boolean when present")
        same_visual_dna_rule = str(continuity_context.get("same_visual_dna_rule", "")).strip()
        if len(same_visual_dna_rule) < 20:
            errors.append(
                "continuity_context.same_visual_dna_rule must be a descriptive rule when present"
            )

    contract = data.get("generation_contract")
    if not isinstance(contract, dict):
        errors.append("generation_contract must be an object")
        contract = {}

    if contract.get("provider") != "cli-imagegen":
        errors.append("generation_contract.provider must be cli-imagegen")
    if contract.get("call_mode") != "per_page_batch":
        errors.append("generation_contract.call_mode must be per_page_batch")
    if contract.get("image_count") != 9:
        errors.append("generation_contract.image_count must be 9")
    if contract.get("page_aspect_ratio") != "9:16":
        errors.append("generation_contract.page_aspect_ratio must be 9:16")

    type_stack_ref = data.get("type_stack_ref")
    if not isinstance(type_stack_ref, dict):
        errors.append("type_stack_ref must be an object")
        type_stack_ref = {}
    if type_stack_ref.get("method_kernel") != "comic-core-v1":
        errors.append("type_stack_ref.method_kernel must be comic-core-v1")
    active_packs = type_stack_ref.get("active_packs")
    if not isinstance(active_packs, list) or len(active_packs) < 2:
        errors.append("type_stack_ref.active_packs must contain at least base and primary packs")

    type_pack_context = data.get("type_pack_context")
    if not isinstance(type_pack_context, dict):
        errors.append("type_pack_context must be an object")
        type_pack_context = {}
    resolution_mode = str(type_pack_context.get("resolution_mode", "")).strip()
    if len(resolution_mode) < 8:
        errors.append("type_pack_context.resolution_mode must be a descriptive string")
    knowledge_refs = type_pack_context.get("knowledge_refs")
    if not isinstance(knowledge_refs, list) or not knowledge_refs:
        errors.append("type_pack_context.knowledge_refs must be a non-empty array")
    semantic_tags = type_pack_context.get("semantic_tags")
    if not isinstance(semantic_tags, list) or not semantic_tags:
        errors.append("type_pack_context.semantic_tags must be a non-empty array")
    control_surface = type_pack_context.get("control_surface")
    if not isinstance(control_surface, dict):
        errors.append("type_pack_context.control_surface must be an object")
        control_surface = {}
    else:
        for key in ("conflict_engine", "role_matrix", "page_turn_mechanism", "panel_grammar", "visual_carrier", "dialogue_register", "motif_system"):
            if not isinstance(control_surface.get(key), dict):
                errors.append(f"type_pack_context.control_surface.{key} must be an object")
        if not isinstance(control_surface.get("failure_modes"), list) or not control_surface.get("failure_modes"):
            errors.append("type_pack_context.control_surface.failure_modes must be a non-empty array")
    stage_projection = type_pack_context.get("stage_projection")
    if not isinstance(stage_projection, dict):
        errors.append("type_pack_context.stage_projection must be an object")
    else:
        for stage_name in ("script_adaptation", "nine_blade_prompting", "image_generation", "animation_generation", "episode_poster"):
            if not isinstance(stage_projection.get(stage_name), dict):
                errors.append(f"type_pack_context.stage_projection.{stage_name} must be an object")

    hard_constraints = contract.get("hard_constraints")
    if not isinstance(hard_constraints, list) or not all(isinstance(x, str) for x in hard_constraints):
        errors.append("generation_contract.hard_constraints must be a string array")
        hard_constraints = []
    for needle in REQUIRED_HARD_CONSTRAINTS:
        if not _contains(hard_constraints, needle):
            errors.append(f"hard_constraints must mention {needle!r}")
    joined_constraints = " ".join(hard_constraints)
    if not _has_character_scene_consistency(joined_constraints):
        errors.append(
            "hard_constraints must explicitly require character and scene consistency"
        )
    if "bottom-right" not in joined_constraints.lower() or "digits 1-9 only" not in joined_constraints.lower():
        errors.append(
            "hard_constraints must require a bottom-right digits-only page number on every page"
        )

    imagegen = contract.get("imagegen", {})
    if not isinstance(imagegen, dict):
        errors.append("generation_contract.imagegen must be an object")
    else:
        if imagegen.get("tool_skill_path") != ".agents/skills/cli/imagegen":
            errors.append("generation_contract.imagegen.tool_skill_path must be .agents/skills/cli/imagegen")
        if imagegen.get("model") not in (None, "gpt-image-2"):
            errors.append("generation_contract.imagegen.model should default to gpt-image-2")

    main_character_lock = data.get("main_character_lock")
    if not isinstance(main_character_lock, dict):
        errors.append("main_character_lock must be an object")
        main_character_lock = {}
    main_character_id = str(main_character_lock.get("character_id", "")).strip()
    main_character_name = str(main_character_lock.get("name", "")).strip()
    main_character_anchor = str(main_character_lock.get("anchor_prompt", "")).strip()
    if not main_character_id:
        errors.append("main_character_lock.character_id must be a non-empty string")
    if not main_character_name:
        errors.append("main_character_lock.name must be a non-empty string")
    if len(main_character_anchor) < 40:
        errors.append("main_character_lock.anchor_prompt must be a detailed anchor string")
    else:
        anchor_lower = main_character_anchor.lower()
        if "character locked across all panels" not in anchor_lower:
            errors.append(
                "main_character_lock.anchor_prompt should include 'Character locked across all panels'"
            )
        if "consistent" not in anchor_lower:
            errors.append(
                "main_character_lock.anchor_prompt should explicitly describe stable appearance semantics"
            )
        if main_character_name and main_character_name.lower() not in anchor_lower:
            errors.append(
                "main_character_lock.anchor_prompt must include main_character_lock.name"
            )

    scene_continuity_bible = data.get("scene_continuity_bible")
    scene_names_by_id: dict[str, str] = {}
    if not isinstance(scene_continuity_bible, dict):
        errors.append("scene_continuity_bible must be an object")
        scene_continuity_bible = {}
    default_rule = str(scene_continuity_bible.get("default_rule", "")).strip()
    if len(default_rule) < 20:
        errors.append("scene_continuity_bible.default_rule must be a descriptive rule")
    scene_locks = scene_continuity_bible.get("scene_locks")
    if not isinstance(scene_locks, list) or not scene_locks:
        errors.append("scene_continuity_bible.scene_locks must be a non-empty array")
        scene_locks = []
    for index, scene_lock in enumerate(scene_locks, start=1):
        if not isinstance(scene_lock, dict):
            errors.append(f"scene_continuity_bible.scene_locks[{index}] must be an object")
            continue
        scene_id = str(scene_lock.get("scene_id", "")).strip()
        scene_name = str(scene_lock.get("name", "")).strip()
        anchor_prompt = str(scene_lock.get("anchor_prompt", "")).strip()
        if not scene_id:
            errors.append(f"scene_continuity_bible.scene_locks[{index}].scene_id must be non-empty")
            continue
        if not scene_name:
            errors.append(f"scene_continuity_bible.scene_locks[{index}].name must be non-empty")
        if len(anchor_prompt) < 40:
            errors.append(
                f"scene_continuity_bible.scene_locks[{index}].anchor_prompt must be detailed"
            )
        scene_names_by_id[scene_id] = scene_name

    character_names_by_id: dict[str, str] = {}
    if main_character_id:
        character_names_by_id[main_character_id] = main_character_name

    character_locks = data.get("character_locks")
    if not isinstance(character_locks, list):
        errors.append("character_locks must be an array")
        character_locks = []
    for index, lock in enumerate(character_locks, start=1):
        if not isinstance(lock, dict):
            errors.append(f"character_locks[{index}] must be an object")
            continue
        character_id = str(lock.get("character_id", "")).strip()
        name = str(lock.get("name", "")).strip()
        anchor_prompt = str(lock.get("anchor_prompt", "")).strip()
        if not character_id:
            errors.append(f"character_locks[{index}].character_id must be non-empty")
            continue
        if not name:
            errors.append(f"character_locks[{index}].name must be non-empty")
        if len(anchor_prompt) < 20:
            errors.append(f"character_locks[{index}].anchor_prompt must be descriptive")
        character_names_by_id[character_id] = name

    style_bible = data.get("style_bible")
    if not isinstance(style_bible, dict):
        errors.append("style_bible must be an object")
        style_bible = {}
    style_text = _stringify(style_bible).lower()
    style_hits = [keyword for keyword in STYLE_KEYWORDS if keyword in style_text]
    if len(style_hits) < 3:
        errors.append(
            "style_bible must include sharper comic style grammar, "
            "for example manga/comic, ink or line art, gutters, panels, screentone, SFX"
        )

    comic_text_system = data.get("comic_text_system")
    if not isinstance(comic_text_system, dict):
        errors.append("comic_text_system must be an object")
        comic_text_system = {}
    for slot_type, rules in TEXT_SYSTEM_RULES.items():
        entry = comic_text_system.get(slot_type)
        if not isinstance(entry, dict):
            errors.append(f"comic_text_system.{slot_type} must be an object")
            continue
        for field in ("visual_form", "placement_rule", "legibility_rule"):
            value = str(entry.get(field, "")).strip()
            if not value:
                errors.append(f"comic_text_system.{slot_type}.{field} must be a non-empty string")
                continue
            if not _contains_any(value, rules["system_keywords"][field]):
                errors.append(
                    f"comic_text_system.{slot_type}.{field} should mention {rules['system_keywords'][field]}"
                )
        if entry.get("max_chars") != rules["max_chars"]:
            errors.append(
                f"comic_text_system.{slot_type}.max_chars must be {rules['max_chars']}"
            )

    pages = data.get("pages")
    if not isinstance(pages, list):
        errors.append("pages must be an array")
        pages = []
    if len(pages) != 9:
        errors.append("pages must contain exactly 9 page objects")

    seen_page_numbers: set[int] = set()
    layout_ids: list[str] = []
    dynamic_layout_count = 0
    used_slot_types: set[str] = set()
    for i, page in enumerate(pages, start=1):
        if not isinstance(page, dict):
            errors.append(f"pages[{i}] must be an object")
            continue
        page_number = page.get("page_number")
        if page_number != i:
            errors.append(f"pages[{i}] page_number must be {i}")
        if isinstance(page_number, int):
            seen_page_numbers.add(page_number)

        layout = page.get("layout")
        if not isinstance(layout, dict):
            errors.append(f"pages[{i}].layout must be an object")
            layout = {}
        layout_id = layout.get("layout_id")
        if isinstance(layout_id, str):
            layout_ids.append(layout_id)
            layout_text = _stringify(layout).lower()
            if any(keyword in layout_text for keyword in DYNAMIC_LAYOUT_KEYWORDS):
                dynamic_layout_count += 1
        if layout.get("aspect_ratio") != "9:16":
            errors.append(f"pages[{i}].layout.aspect_ratio must be 9:16")
        panel_count = layout.get("panel_count")
        panels = page.get("panels")
        if not isinstance(panels, list) or not panels:
            errors.append(f"pages[{i}].panels must be a non-empty array")
            panels = []
        if isinstance(panel_count, int) and panel_count != len(panels):
            errors.append(f"pages[{i}].layout.panel_count must match panels length")
        if isinstance(panel_count, int) and panel_count < 2:
            errors.append(f"pages[{i}].layout.panel_count must be at least 2 for a multi-panel comic page")
        if isinstance(panels, list) and len(panels) < 2:
            errors.append(f"pages[{i}].panels must contain at least 2 panels for a multi-panel comic page")

        active_character_ids = page.get("active_character_ids")
        if not isinstance(active_character_ids, list) or not active_character_ids:
            errors.append(f"pages[{i}].active_character_ids must be a non-empty array")
            active_character_ids = []
        else:
            unknown_character_ids = [
                character_id
                for character_id in active_character_ids
                if character_id not in character_names_by_id
            ]
            if unknown_character_ids:
                errors.append(
                    f"pages[{i}].active_character_ids contains unknown ids: {unknown_character_ids}"
                )

        scene_id = str(page.get("scene_id", "")).strip()
        if not scene_id:
            errors.append(f"pages[{i}].scene_id must be a non-empty string")
        elif scene_id not in scene_names_by_id:
            errors.append(f"pages[{i}].scene_id must reference scene_continuity_bible.scene_locks")

        page_number_overlay = page.get("page_number_overlay")
        if not isinstance(page_number_overlay, dict):
            errors.append(f"pages[{i}].page_number_overlay must be an object")
            page_number_overlay = {}
        else:
            overlay_text = str(page_number_overlay.get("text", "")).strip()
            if overlay_text != str(i):
                errors.append(f"pages[{i}].page_number_overlay.text must equal '{i}'")
            position = str(page_number_overlay.get("position", "")).strip().lower()
            if position != "bottom-right":
                errors.append(f"pages[{i}].page_number_overlay.position must be bottom-right")
            style_prompt = str(page_number_overlay.get("style_prompt", "")).strip()
            if len(style_prompt) < 20:
                errors.append(f"pages[{i}].page_number_overlay.style_prompt must be descriptive")
            elif not _has_bottom_right_numeric_page_number(style_prompt, i):
                errors.append(
                    f"pages[{i}].page_number_overlay.style_prompt must require bottom-right digits-only page number {i}"
                )

        positive_prompt = page.get("positive_prompt")
        if not isinstance(positive_prompt, str) or not positive_prompt.strip():
            errors.append(f"pages[{i}].positive_prompt must be a non-empty string")
        else:
            if "9:16" not in positive_prompt:
                errors.append(f"pages[{i}].positive_prompt must mention 9:16")
            if not _contains_any(
                positive_prompt,
                ("clear legible chinese text", "readable chinese text"),
            ):
                errors.append(
                    f"pages[{i}].positive_prompt must mention clear legible Chinese text"
                )
            if main_character_name and not _has_main_character_anchor(
                positive_prompt, main_character_name
            ):
                errors.append(
                    f"pages[{i}].positive_prompt must inject the main character anchor with {main_character_name}"
                )
            if not _has_character_scene_consistency(positive_prompt):
                errors.append(
                    f"pages[{i}].positive_prompt must mention character and scene consistency"
                )
            if not _has_bottom_right_numeric_page_number(positive_prompt, i):
                errors.append(
                    f"pages[{i}].positive_prompt must require bottom-right digits-only page number {i}"
                )
            if scene_id in scene_names_by_id:
                scene_name = scene_names_by_id[scene_id]
                if scene_name.lower() not in positive_prompt.lower():
                    errors.append(
                        f"pages[{i}].positive_prompt must mention the active scene lock name {scene_name!r}"
                    )
            if len(active_character_ids) >= 2:
                active_names = [
                    character_names_by_id[character_id]
                    for character_id in active_character_ids
                    if character_id in character_names_by_id
                ]
                mentioned = _mentioned_names(positive_prompt, active_names)
                if len(mentioned) < 2:
                    errors.append(
                        f"pages[{i}].positive_prompt must mention at least two active recurring character names for multi-character pages"
                    )

        for panel in panels:
            if not isinstance(panel, dict):
                errors.append(f"pages[{i}].panels entries must be objects")
                continue
            if not panel.get("panel_id"):
                errors.append(f"pages[{i}] panel missing panel_id")
            if not panel.get("shot"):
                errors.append(f"pages[{i}] panel missing shot")
            if not panel.get("action"):
                errors.append(f"pages[{i}] panel missing action")
            text_slots = panel.get("text_slots", [])
            if not isinstance(text_slots, list):
                errors.append(f"pages[{i}] panel text_slots must be an array")
                continue
            for slot in text_slots:
                if not isinstance(slot, dict):
                    errors.append(f"pages[{i}] text slot must be an object")
                    continue
                slot_type = slot.get("type")
                if slot_type not in {"dialogue", "narration", "inner_monologue", "sfx"}:
                    errors.append(f"pages[{i}] text slot has invalid type")
                    continue
                used_slot_types.add(slot_type)
                if not isinstance(slot.get("text"), str):
                    errors.append(f"pages[{i}] text slot text must be a string")
                    continue
                text_value = slot["text"].strip()
                if not text_value:
                    errors.append(f"pages[{i}] text slot text must be non-empty")
                max_chars = TEXT_SYSTEM_RULES[slot_type]["max_chars"]
                if len(text_value) > max_chars:
                    errors.append(
                        f"pages[{i}] {slot_type} text slot exceeds max length {max_chars}"
                    )
                bubble_style = slot.get("bubble_style")
                if bubble_style not in TEXT_SYSTEM_RULES[slot_type]["bubble_styles"]:
                    errors.append(
                        f"pages[{i}] {slot_type} bubble_style must be one of {sorted(TEXT_SYSTEM_RULES[slot_type]['bubble_styles'])}"
                    )
                placement = slot.get("placement")
                if placement not in TEXT_SYSTEM_RULES[slot_type]["placements"]:
                    errors.append(
                        f"pages[{i}] {slot_type} placement must be one of {sorted(TEXT_SYSTEM_RULES[slot_type]['placements'])}"
                    )
                expected_inside_panel = TEXT_SYSTEM_RULES[slot_type]["inside_panel"]
                inside_panel = slot.get("inside_panel")
                if expected_inside_panel is not None and inside_panel is not expected_inside_panel:
                    errors.append(
                        f"pages[{i}] {slot_type} inside_panel must be {expected_inside_panel}"
                    )
                speaker_id = str(slot.get("speaker_id", "")).strip()
                if TEXT_SYSTEM_RULES[slot_type]["requires_speaker"]:
                    if not speaker_id:
                        errors.append(f"pages[{i}] {slot_type} text slot must include speaker_id")
                    elif speaker_id not in active_character_ids:
                        errors.append(
                            f"pages[{i}] {slot_type} speaker_id must belong to active_character_ids"
                        )
                if isinstance(positive_prompt, str) and not _contains_any(
                    positive_prompt, TEXT_SYSTEM_RULES[slot_type]["prompt_keywords"]
                ):
                    errors.append(
                        f"pages[{i}].positive_prompt must mention {slot_type} rendering cues {TEXT_SYSTEM_RULES[slot_type]['prompt_keywords']}"
                    )

    if seen_page_numbers and seen_page_numbers != set(range(1, 10)):
        errors.append("page_number values must be exactly 1..9")

    if len(pages) == 9:
        if len(set(layout_ids)) < 5:
            errors.append("pages[].layout_id must use at least 5 distinct layouts across 9 pages")
        if dynamic_layout_count < 3:
            errors.append(
                "pages[].layout should include at least 3 dynamic classic comic layouts "
                "(splash, inset, diagonal, split, cascade, impact, cliffhanger, border-breaking, zigzag, asymmetric)"
            )
        if used_slot_types != set(TEXT_SYSTEM_RULES):
            errors.append(
                "pages must cover all four text slot types across the 9 pages: dialogue, narration, inner_monologue, sfx"
            )

    negative = data.get("global_negative_prompt")
    if not isinstance(negative, str) or not negative.strip():
        errors.append("global_negative_prompt must be a non-empty string")
    else:
        lower_negative = negative.lower()
        for needle in ["collage", "variations", "watermark", "unreadable"]:
            if needle not in lower_negative:
                errors.append(f"global_negative_prompt should mention {needle!r}")

    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate nine_blade_comic_prompts.v1 JSON")
    parser.add_argument("json_path", nargs="?", type=Path)
    parser.add_argument("--self-test", action="store_true", help="Run an in-memory validator self-test")
    args = parser.parse_args()

    if args.self_test:
        errors = validate(_self_test_data())
        if errors:
            print("FAIL")
            for error in errors:
                print(f"- {error}")
            return 1
        print("PASS self-test")
        return 0

    if args.json_path is None:
        parser.error("json_path is required unless --self-test is used")

    try:
        errors = validate(_load_json(args.json_path))
    except Exception as exc:
        print(f"FAIL: {exc}", file=sys.stderr)
        return 2

    if errors:
        print("FAIL")
        for error in errors:
            print(f"- {error}")
        return 1

    print("PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
