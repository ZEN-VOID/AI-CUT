#!/usr/bin/env python3
"""Build canonical prop design Markdown cards and optional compatibility JSON."""

from __future__ import annotations

import argparse
from datetime import datetime
import json
import re
import sys
from pathlib import Path
from typing import Any


SHARED_SCRIPTS_DIR = Path(__file__).resolve().parents[2] / "_shared" / "scripts"
if SHARED_SCRIPTS_DIR.as_posix() not in sys.path:
    sys.path.insert(0, SHARED_SCRIPTS_DIR.as_posix())

from global_style_prefix import extract_global_style_prefix  # noqa: E402


SCRIPT_DIR = Path(__file__).resolve().parent
TEMPLATE_PATH = SCRIPT_DIR.parent / "templates" / "prop_masterprompt.structured.v2.md"
NON_ASCII_RE = re.compile(r"[^\x00-\x7F]")
INTEGRATED_PROMPT_MIN_BYTES = 1800
INTEGRATED_PROMPT_MAX_BYTES = 2200


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="从 `道具清单.json` 生成逐道具 Markdown 设计卡，并按需导出兼容 JSON。"
    )
    parser.add_argument("--catalog", required=True, help="道具清单.json 路径")
    parser.add_argument("--detail", help="3-Detail/第N集.json 路径")
    parser.add_argument("--research", help="道具研究.json 路径")
    parser.add_argument("--bridge", help="prop_design_bridge.json 路径")
    parser.add_argument("--global-style", help="全局风格.md 路径")
    parser.add_argument("--type-elements", help="全集类型元素.md 或分组全集类型元素.md 路径")
    parser.add_argument("--design-elements", help="导演意图.md 路径")
    parser.add_argument("--north-star", help="north_star.yaml 路径")
    parser.add_argument("--init-handoff", help="init_handoff.yaml 路径")
    parser.add_argument("--output-dir", required=True, help="输出目录")
    parser.add_argument("--design-name", default="道具设计.json", help="compat design JSON 文件名")
    parser.add_argument("--prompt-name", default="prop_design_prompt.json", help="compat prompt JSON 文件名")
    parser.add_argument("--manifest-name", default="_manifest.json", help="manifest 文件名")
    parser.add_argument("--prop-id", action="append", dest="prop_ids", help="只处理指定 prop_id，可重复传入")
    parser.add_argument("--prop-name", action="append", dest="prop_names", help="只处理指定 canonical_name，可重复传入")
    parser.add_argument("--write-compat-json", action="store_true", help="额外导出 compat JSON")
    parser.add_argument("--dry-run", action="store_true", help="只预览 manifest，不写文件")
    return parser.parse_args()


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def read_text(path: Path | None) -> str:
    if path is None or not path.exists():
        return ""
    return path.read_text(encoding="utf-8")


def compact_text(text: str, limit: int = 220) -> str:
    clean = " ".join(text.split())
    if len(clean) <= limit:
        return clean
    return clean[: limit - 3] + "..."


def to_repo_path(path: Path) -> str:
    try:
        return path.resolve().relative_to(Path.cwd().resolve()).as_posix()
    except ValueError:
        return path.as_posix()


def safe_filename(text: str) -> str:
    return re.sub(r"[\\\\/:*?\"<>|]+", "-", text).strip() or "unnamed"


def markdown_filename(prop_id: str, canonical_name: str) -> str:
    return f"{safe_filename(prop_id)}-{safe_filename(canonical_name)}.md"


def first_non_empty(*values: Any) -> Any:
    for value in values:
        if value not in (None, "", [], {}):
            return value
    return ""


def select_props(props: list[dict[str, Any]], prop_ids: list[str], prop_names: list[str]) -> list[dict[str, Any]]:
    if not prop_ids and not prop_names:
        return props
    id_set = {item for item in prop_ids if item}
    name_set = {item for item in prop_names if item}
    selected = []
    for prop in props:
        if id_set and str(prop.get("prop_id", "")) in id_set:
            selected.append(prop)
            continue
        if name_set and str(prop.get("canonical_name", "")) in name_set:
            selected.append(prop)
    return selected


def lookup_by_key(items: list[dict[str, Any]], prop_id: str, canonical_name: str) -> dict[str, Any]:
    for item in items:
        if str(item.get("prop_id", "")) == prop_id:
            return item
    for item in items:
        if str(item.get("canonical_name", "")) == canonical_name:
            return item
    return {}


def extract_global_style_hint(global_style_text: str, type_elements_text: str, design_elements_text: str) -> str:
    prefix = extract_global_style_prefix(global_style_text)
    if prefix:
        return prefix
    return compact_text(global_style_text, 220)


def build_story_text(prop_name: str, design_context: dict[str, Any], display_profile: dict[str, Any], narrative: dict[str, Any]) -> str:
    chronicle = str(design_context.get("chronicle", "")).strip()
    description = str(display_profile.get("description", "")).strip()
    reason = str(narrative.get("reason", "")).strip()
    continuity = str(narrative.get("continuity_guard", "")).strip()

    parts = [text for text in (chronicle, description) if text]
    if narrative.get("is_special"):
        parts.append(
            f"{prop_name} 不能被处理成普通背景摆件；它必须保住 {narrative.get('story_function', '关键剧情功能')} 的识别度。"
        )
    if reason:
        parts.append(reason)
    if continuity:
        parts.append(continuity)
    if not parts:
        parts.append(f"{prop_name} 需要作为可被设计、可被镜头稳定识别的器物来处理。")
    return " ".join(parts)


def build_reasoning_pivot(display_profile: dict[str, Any], narrative: dict[str, Any], physical_character: dict[str, Any]) -> str:
    pieces = [
        str(display_profile.get("visual_signature", "")).strip(),
        str(narrative.get("visual_obligation", "")).strip(),
        str(physical_character.get("surface_temperament", "")).strip(),
    ]
    pieces = [item for item in pieces if item]
    return pieces[0] if pieces else "先保住器物轮廓、材质性格与镜头可读性。"


def ensure_terminal_punctuation(text: str) -> str:
    clean = str(text or "").strip()
    if clean and not clean.endswith(("。", "！", "？", ".", "!", "?")):
        return f"{clean}。"
    return clean


def translate_global_style_prefix(style_text: str) -> str:
    source = ensure_terminal_punctuation(style_text)
    if "近未来社区生活喜剧影视质感" in source and "轻量全息奇观" in source:
        return (
            "A near-future community-life comedy with cinematic realism, orderly lived-in spaces, "
            "soft atmospheric depth, gentle absurdist rhythm, and lightweight holographic spectacle "
            "that always serves the story dignity, loneliness, and clumsy romance."
        )
    if "黑白恐怖漫画质感" in source:
        return (
            "A black-and-white psychological horror comic style with dense hand-drawn linework, "
            "ink-shadow layering, paper-grain texture, visible sound-effect rhythm, ordinary objects "
            "turning uncanny through restraint and negative space, and controlled treatment of corpse evidence."
        )
    return (
        "A grounded cinematic prop design style with practical material logic, readable silhouette, "
        "controlled atmosphere, restrained contrast, and production-ready inspection clarity."
    )


PHRASE_TRANSLATIONS = {
    "量子核桃的主体轮廓": "the Quantum Walnut's main silhouette",
    "全息锦鲤池的主体轮廓": "the holographic koi pond's main silhouette",
    "数据鱼的主体轮廓": "the data fish's main silhouette",
    "丈八蛇矛的主体轮廓": "the long spear's main silhouette",
    "智能手环的主体轮廓": "the smart wristband's main silhouette",
    "功能端与握持/受力端的关系": "the relationship between the functional end and the force points",
    "状态痕迹最明显的局部细节": "the local details where state marks are most visible",
    "主材质优先按 金属 处理": "primary metal material treatment",
    "主材质优先按 复合材 处理": "primary composite-material treatment",
    "表面工艺优先按 雕刻 处理": "engraved surface craft",
    "表面工艺优先按 常规制作 处理": "practical manufactured surface craft",
    "在掌心转动": "rotating wear pattern on the object surface",
    "被碰响": "making a small impact sound",
    "仍在手中发亮": "active blue glow state",
    "仍在手中转动": "continued rotation state",
    "继续发出稳定蓝光": "continuing to emit a stable blue glow",
    "剧烈震动": "shaking violently",
    "持续异常震动": "continuing abnormal vibration",
    "从手中投射扇形光柱": "projecting a fan-shaped light beam from the device",
    "熄火": "powering down",
    "已经失去光效": "losing its light effect",
    "只剩普通核桃状态": "reverting to an ordinary walnut state",
    "核桃归于普通状态": "returning to an ordinary walnut state",
    "平稳运行": "running smoothly",
    "作为柔和动态背景": "acting as a soft dynamic background element",
    "被抬起指向错误目标": "raised and pointed at the wrong target",
    "被调出关闭程序界面": "calling up a shutdown interface",
    "不要把镜头状态词直接并入 canonical prop name": "do not fold shot-state words into the canonical prop name",
    "不要补写上游证据里不存在的现代零件或多余装饰": "do not invent modern parts or extra decoration unsupported by upstream evidence",
    "不要把道具画成纯背景纹样，必须保留功能逻辑": "do not reduce the prop to a background pattern; preserve its functional logic",
    "不要把具有特殊叙事意义的道具降格为普通背景摆件": "do not downgrade a narratively significant prop into an ordinary background object",
}

PROP_NAME_TRANSLATIONS = {
    "量子核桃": "Quantum Walnut",
    "全息锦鲤池": "Holographic Koi Pond",
    "数据鱼": "Data Fish",
    "丈八蛇矛": "Long Serpent Spear",
    "智能手环": "Smart Wristband",
}


def translate_fragment(text: str) -> str:
    clean = str(text).strip()
    return PHRASE_TRANSLATIONS.get(clean, clean)


def join_brief(items: list[str], limit: int = 4) -> str:
    values = [translate_fragment(str(item)) for item in items if str(item).strip()]
    return "; ".join(values[:limit]) if values else "TBD"


def english_fragment(value: Any, fallback: str) -> str:
    translated = translate_fragment(str(value))
    if not translated or translated == "TBD" or NON_ASCII_RE.search(translated):
        return fallback
    for source, replacement in (
        ("handheld", "portable"),
        ("held", "presented"),
        ("holding", "displaying"),
        ("hands", "device body"),
        ("hand", "device body"),
        ("palm", "surface"),
        ("grip", "force point"),
        ("touch", "surface interaction"),
        ("user", "off-frame use context"),
        ("characters", "off-frame narrative context"),
        ("character", "off-frame narrative context"),
    ):
        translated = re.sub(rf"\b{re.escape(source)}\b", replacement, translated, flags=re.IGNORECASE)
    return translated


def english_join_brief(items: list[str], fallback: str, limit: int = 4) -> str:
    values = [english_fragment(item, "") for item in items if str(item).strip()]
    values = [item for item in values if item]
    return "; ".join(values[:limit]) if values else fallback


def fit_integrated_prompt(sentences: list[str]) -> str:
    prompt = " ".join(" ".join(sentence.split()) for sentence in sentences if sentence.strip())
    reinforcement = [
        "Keep the object isolated enough for concept-art inspection on a neutral reference background while still implying the established world through scale, light, and material behavior.",
        "Integrate silhouette, surface craft, surface interaction logic, state marks, and narrative function into one coherent image brief, not a list of disconnected labels.",
        "Make the material decisions readable at thumbnail scale and at close inspection, with clear primary structure, secondary details, and no unsupported decorative additions.",
        "Preserve all documented constraints as visual boundaries for the image model, especially what the prop must not become, what parts must stay readable, and what story role must remain visible.",
        "Use camera distance, angle, lens feel, and lighting as design tools that reveal construction and function rather than hiding missing evidence behind atmosphere.",
    ]
    for sentence in reinforcement:
        candidate = f"{prompt} {sentence}"
        if len(candidate.encode("utf-8")) <= INTEGRATED_PROMPT_MAX_BYTES:
            prompt = candidate
        if len(prompt.encode("utf-8")) >= INTEGRATED_PROMPT_MIN_BYTES:
            break
    if len(prompt.encode("utf-8")) > INTEGRATED_PROMPT_MAX_BYTES:
        words = prompt.split()
        trimmed: list[str] = []
        for word in words:
            candidate = " ".join([*trimmed, word])
            if len(candidate.encode("utf-8")) > INTEGRATED_PROMPT_MAX_BYTES - 1:
                break
            trimmed.append(word)
        prompt = " ".join(trimmed).rstrip(" ,;:") + "."
    return prompt


def build_integrated_prompt_text(
    packet: dict[str, Any],
) -> str:
    prop_name = packet["canonical_name"]
    prop_name_en = PROP_NAME_TRANSLATIONS.get(prop_name, prop_name)
    if NON_ASCII_RE.search(prop_name_en):
        prop_name_en = "the documented prop"
    narrative = packet["narrative_significance"]
    shot_route = packet["shot_route"]
    physical_character = packet["physical_character"]
    display_profile = packet["display_profile"]
    structure = english_join_brief(packet["structure_modules"], "documented structure modules", 3)
    material = english_join_brief(packet["material_and_finish"], "documented material and finish evidence", 3)
    wear = english_join_brief(packet["wear_marks"], "documented wear and state marks", 5)
    negative = english_join_brief(packet["negative_constraints"], "do not invent unsupported parts or decoration", 4)
    visual_obligation = english_fragment(
        narrative.get("visual_obligation", ""),
        "keep the key silhouette and readable functional logic clear",
    )
    story_function = english_fragment(narrative.get("story_function", ""), "story support")
    story_text = english_fragment(packet["story_text"], "the documented story premise")
    shot_size = english_fragment(shot_route.get("shot_size", ""), "medium hero shot")
    camera_angle = english_fragment(shot_route.get("camera_angle", ""), "eye-level three-quarter")
    focal_length = english_fragment(shot_route.get("focal_length", ""), "50mm")
    lighting = english_fragment(shot_route.get("lighting", ""), "story-motivated lighting with readable edge separation")
    surface = english_fragment(
        physical_character.get("surface_temperament", ""),
        "a readable material surface with clear primary and secondary finishes",
    )
    force_logic = english_fragment(physical_character.get("force_logic", ""), "functional interaction, display, and force logic")
    visual_signature = english_fragment(
        display_profile.get("visual_signature", "") or packet["reasoning_pivot"],
        "the documented visual priority",
    )
    narrative_focus = ""
    if narrative.get("is_special"):
        narrative_level = english_fragment(narrative.get("level", ""), "notable")
        narrative_focus = (
            f" Treat it as a {narrative_level}-level narrative prop for {story_function}; "
            f"{visual_obligation}."
        )
    return fit_integrated_prompt([
        f"Create a 16:9 single-subject prop concept image for {prop_name_en}, an isolated pure prop view. "
        f"Integrate the story premise into a tangible object: {story_text}.",
        "This is a clean prop reference image with no hands, no characters, no body parts, no holder, and no performance action.",
        f"Use the reasoning pivot as the visual priority: {visual_signature}.",
        f"Show the prop as a {shot_size}, {camera_angle}, with a {focal_length} lens feel and {lighting}.",
        f"Preserve these deconstruction details as visible design evidence: structure modules ({structure}); material and finish ({material}); surface temperament ({surface}).",
        f"Make wear and state marks readable through {wear}, and let ergonomics, display behavior, or force transfer follow {force_logic}.",
        f"{narrative_focus} Keep the background neutral and minimal so the object remains the only subject.",
        "Avoid adding extra mechanisms, decorative parts, scale changes, or symbolic motifs that are not supported by the design card above.",
        f"Do not violate these constraints: {negative}.",
    ])


def build_full_prompt(global_style_hint: str, integrated_prompt: str) -> str:
    style_text = global_style_hint.strip() or (
        "Follow the established project visual style without inventing a new genre."
    )
    return f"Global style prefix: {style_text}\n\nIntegrated prompt: {integrated_prompt.strip()}"


def render_template(template_text: str, values: dict[str, Any]) -> str:
    rendered = template_text
    for key, value in values.items():
        rendered = rendered.replace(f"[{key}]", str(value or "TBD"))
    return rendered


def build_markdown_card(packet: dict[str, Any]) -> str:
    prop_name = packet["canonical_name"]
    display_profile = packet["display_profile"]
    narrative = packet["narrative_significance"]
    shot_route = packet["shot_route"]
    attribute_profile = packet["attribute_profile"]
    physical_character = packet["physical_character"]
    template_text = TEMPLATE_PATH.read_text(encoding="utf-8")
    values = {
        "prop_name_en": prop_name,
        "story_narrative": packet["story_text"],
        "reasoning_pivot_en": packet["reasoning_pivot"],
        "photo_type": "single prop design sheet",
        "photo_shot_size": shot_route.get("shot_size", "medium hero shot"),
        "photo_background": "neutral plain background for a pure prop reference, no hands, no characters",
        "style_backbone": packet["style_backbone"],
        "prop_type_en": packet["prop_type"],
        "design_inspiration_en": packet["design_inspiration"],
        "period_attribute_en": packet["period_attribute"],
        "functionality_en": narrative.get("story_function") or "story_support",
        "shape_en": "；".join(packet["structure_modules"][:3]) or "保持主体轮廓与功能端关系",
        "line_sense_en": narrative.get("continuity_guard") or physical_character.get("state_anchor", "由状态痕迹决定"),
        "volume_en": physical_character.get("volume_density", "以主体体量与关键局部层次为主"),
        "size_en": attribute_profile.get("scale_hint", "small portable prop"),
        "material_en": "；".join(packet["material_and_finish"][:3]) or "以 design_handoff 的主材质与工艺为准",
        "texture_en": physical_character.get("surface_temperament", "主次表面必须分明"),
        "decoration_en": display_profile.get("visual_signature", "只保留 evidence 已出现的识别锚点"),
        "pattern_en": display_profile.get("short_tagline", "围绕 narrative_significance 的关键纹样与局部细节"),
        "art_element_en": packet["art_elements"],
        "culture_en": packet["cultural_elements"],
        "ergonomics_en": physical_character.get("force_logic", "围绕功能端与受力逻辑组织"),
        "global_style_prefix": packet["global_style_prefix"],
        "prompt_integration": packet["prompt_integration"],
    }
    return render_template(template_text, values).rstrip() + "\n"




def build_packet(
    prop: dict[str, Any],
    *,
    global_style_text: str,
    type_elements_text: str,
    design_elements_text: str,
    north_star_text: str,
    init_handoff_text: str,
    research_item: dict[str, Any],
    bridge_item: dict[str, Any],
) -> dict[str, Any]:
    design_context = prop.get("design_context", {})
    handoff = design_context.get("design_handoff", {})
    display_profile = first_non_empty(
        handoff.get("display_profile"),
        design_context.get("display_profile"),
        prop.get("display_profile"),
    ) or {}
    attribute_profile = design_context.get("attribute_profile", {})
    scene_usage_profile = design_context.get("scene_usage_profile", {})
    narrative = first_non_empty(
        handoff.get("narrative_significance"),
        design_context.get("narrative_significance"),
        bridge_item.get("narrative_significance"),
        research_item.get("narrative_significance"),
    ) or {}
    physical_character = first_non_empty(
        handoff.get("physical_character"),
        bridge_item.get("physical_character"),
    ) or {}
    shot_route = first_non_empty(
        handoff.get("shot_route"),
        bridge_item.get("shot_route"),
    ) or {}
    structure_modules = list(first_non_empty(handoff.get("structure_modules"), bridge_item.get("structure_modules"), []))
    material_and_finish = list(first_non_empty(handoff.get("material_and_finish"), bridge_item.get("material_and_finish"), []))
    wear_marks = list(first_non_empty(handoff.get("wear_marks"), bridge_item.get("wear_marks"), []))
    negative_constraints = list(first_non_empty(handoff.get("negative_constraints"), bridge_item.get("negative_constraints"), []))
    prompt_anchor = str(first_non_empty(handoff.get("prompt_anchor"), bridge_item.get("prompt_anchor"), prop.get("canonical_name", "")))
    style_backbone = extract_global_style_hint(global_style_text, type_elements_text, design_elements_text)

    packet = {
        "prop_id": str(prop.get("prop_id", "prop")),
        "canonical_name": str(prop.get("canonical_name", "unnamed_prop")),
        "prop_type": str(first_non_empty(handoff.get("prop_type"), prop.get("prop_type"), "general_prop")),
        "design_context": design_context,
        "display_profile": display_profile,
        "attribute_profile": attribute_profile,
        "scene_usage_profile": scene_usage_profile,
        "narrative_significance": narrative,
        "physical_character": physical_character,
        "shot_route": shot_route,
        "structure_modules": structure_modules,
        "material_and_finish": material_and_finish,
        "wear_marks": wear_marks,
        "negative_constraints": negative_constraints,
        "prompt_anchor": prompt_anchor,
        "style_backbone": style_backbone or compact_text(global_style_text, 120) or "项目全局风格约束",
        "period_attribute": compact_text(north_star_text, 90) or compact_text(init_handoff_text, 90) or "当前项目设定时期",
        "design_inspiration": prompt_anchor or compact_text(type_elements_text, 90) or "由上游 design_handoff 与类型元素共同约束",
        "art_elements": compact_text(
            first_non_empty(
                design_context.get("creative_expansion", {}).get("allowed_divergence"),
                display_profile.get("dramatic_value"),
                type_elements_text,
            )
            if not isinstance(first_non_empty(
                design_context.get("creative_expansion", {}).get("allowed_divergence"),
                display_profile.get("dramatic_value"),
                type_elements_text,
            ), list)
            else "；".join(design_context.get("creative_expansion", {}).get("allowed_divergence", [])[:2]),
            160,
        ),
        "cultural_elements": compact_text(
            " / ".join(
                filter(
                    None,
                    [
                        str(design_context.get("cultural_reference", {}).get("material_craft_hint", "")),
                        str(design_context.get("cultural_reference", {}).get("period_guardrail", "")),
                        compact_text(type_elements_text, 120),
                        compact_text(design_elements_text, 120),
                    ],
                )
            ),
            240,
        ),
    }
    packet["story_text"] = build_story_text(packet["canonical_name"], design_context, display_profile, narrative)
    packet["reasoning_pivot"] = build_reasoning_pivot(display_profile, narrative, physical_character)
    packet["global_style_prefix_source"] = ensure_terminal_punctuation(style_backbone or packet["style_backbone"])
    packet["global_style_prefix"] = translate_global_style_prefix(packet["global_style_prefix_source"])
    packet["prompt_integration"] = build_integrated_prompt_text(packet)
    packet["prompt_text"] = build_full_prompt(packet["global_style_prefix"], packet["prompt_integration"])
    return packet


def build_compat_payloads(
    packets: list[dict[str, Any]],
    *,
    project_name: str,
    episode_id: str,
    generated_at: str,
    source_inputs: list[str],
    output_dir_repo: str,
    design_name: str,
) -> tuple[dict[str, Any], dict[str, Any]]:
    design_output_repo = f"{output_dir_repo}/{design_name}"
    design_payload = {
        "meta": {
            "schema_version": "aigc/design-prop-design/v2-compat",
            "skill_id": "aigc-design-prop-design",
            "project_name": project_name,
            "episode_id": episode_id,
            "primary_input": source_inputs[0],
            "source_inputs": source_inputs,
            "generated_at": generated_at,
            "canonical_markdown_truth": True,
        },
        "props": [],
    }
    prompt_payload = {
        "meta": {
            "schema_version": "aigc/design-prop-design-prompt/v2-compat",
            "skill_id": "aigc-design-prop-design",
            "project_name": project_name,
            "episode_id": episode_id,
            "primary_input": design_output_repo,
            "source_inputs": [design_output_repo, *source_inputs],
            "generated_at": generated_at,
            "canonical_markdown_truth": True,
        },
        "props": [],
    }
    for packet in packets:
        markdown_path = f"{output_dir_repo}/{markdown_filename(packet['prop_id'], packet['canonical_name'])}"
        design_payload["props"].append(
            {
                "prop_id": packet["prop_id"],
                "canonical_name": packet["canonical_name"],
                "prop_type": packet["prop_type"],
                "markdown_path": markdown_path,
                "design_thesis": {
                    "story_text": packet["story_text"],
                    "reasoning_pivot": packet["reasoning_pivot"],
                    "narrative_significance": packet["narrative_significance"],
                },
                "structure_modules": packet["structure_modules"],
                "material_and_finish": packet["material_and_finish"],
                "wear_marks": packet["wear_marks"],
                "shot_route": packet["shot_route"],
                "physical_character": packet["physical_character"],
                "display_profile": packet["display_profile"],
                "style_backbone": packet["style_backbone"],
                "negative_constraints": packet["negative_constraints"],
                "prompt_anchor": packet["prompt_anchor"],
            }
        )
        prompt_payload["props"].append(
            {
                "prop_id": packet["prop_id"],
                "canonical_name": packet["canonical_name"],
                "markdown_path": markdown_path,
                "prompt_en": packet["prompt_text"],
                "full_generation_prompt": packet["prompt_text"],
                "negative_constraints": packet["negative_constraints"],
                "narrative_focus": {
                    "level": packet["narrative_significance"].get("level", "background"),
                    "visual_obligation": packet["narrative_significance"].get("visual_obligation", ""),
                },
                "render_hints": {
                    "render_mode": "SINGLE_SUBJECT_PROP_CONCEPT",
                    "section_source": "**prompt整合**",
                },
            }
        )
    return design_payload, prompt_payload


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def main() -> int:
    args = parse_args()
    catalog_path = Path(args.catalog)
    if not catalog_path.exists():
        print(f"[ERROR] catalog 不存在: {catalog_path}", file=sys.stderr)
        return 1

    catalog = read_json(catalog_path)
    props = catalog.get("props", [])
    selected = select_props(props, args.prop_ids or [], args.prop_names or [])
    if not selected:
        print("[ERROR] 过滤后没有命中任何 prop。", file=sys.stderr)
        return 1

    research_path = Path(args.research) if args.research else None
    bridge_path = Path(args.bridge) if args.bridge else None
    research = read_json(research_path) if research_path and research_path.exists() else {}
    bridge = read_json(bridge_path) if bridge_path and bridge_path.exists() else {}
    research_props = research.get("props", [])
    bridge_props = bridge.get("props", [])

    output_dir = Path(args.output_dir)
    output_dir_repo = to_repo_path(output_dir)
    episode_id = str(catalog.get("meta", {}).get("episode_id") or catalog_path.parent.name)
    project_name = str(catalog.get("meta", {}).get("project_name") or catalog_path.parents[4].name)
    generated_at = datetime.now().astimezone().isoformat(timespec="seconds")

    optional_paths = []
    for raw in (
        args.detail,
        args.research,
        args.bridge,
        args.global_style,
        args.type_elements,
        args.design_elements,
        args.north_star,
        args.init_handoff,
    ):
        if raw:
            path = Path(raw)
            if path.exists():
                optional_paths.append(to_repo_path(path))

    source_inputs = [to_repo_path(catalog_path), *optional_paths]
    global_style_text = read_text(Path(args.global_style)) if args.global_style else ""
    type_elements_text = read_text(Path(args.type_elements)) if args.type_elements else ""
    design_elements_text = read_text(Path(args.design_elements)) if args.design_elements else ""
    north_star_text = read_text(Path(args.north_star)) if args.north_star else ""
    init_handoff_text = read_text(Path(args.init_handoff)) if args.init_handoff else ""

    packets = []
    design_items = []
    for prop in selected:
        prop_id = str(prop.get("prop_id", "prop"))
        canonical_name = str(prop.get("canonical_name", "unnamed_prop"))
        design_context = prop.get("design_context", {})
        if not design_context.get("design_handoff"):
            print(f"[ERROR] `{canonical_name}` 缺少 `design_context.design_handoff`，请先回退 `1-清单/道具`。", file=sys.stderr)
            return 1

        packet = build_packet(
            prop,
            global_style_text=global_style_text,
            type_elements_text=type_elements_text,
            design_elements_text=design_elements_text,
            north_star_text=north_star_text,
            init_handoff_text=init_handoff_text,
            research_item=lookup_by_key(research_props, prop_id, canonical_name),
            bridge_item=lookup_by_key(bridge_props, prop_id, canonical_name),
        )
        markdown_name = markdown_filename(prop_id, canonical_name)
        markdown_path = output_dir / markdown_name
        packets.append(packet)
        design_items.append(
            {
                "prop_id": prop_id,
                "canonical_name": canonical_name,
                "prop_type": packet["prop_type"],
                "markdown_path": f"{output_dir_repo}/{markdown_name}",
            }
        )
        if not args.dry_run:
            output_dir.mkdir(parents=True, exist_ok=True)
            markdown_path.write_text(build_markdown_card(packet), encoding="utf-8")

    manifest_payload = {
        "status": "completed",
        "episode_id": episode_id,
        "input_file": to_repo_path(catalog_path),
        "output_dir": output_dir_repo,
        "output_files": [f"{output_dir_repo}/{args.manifest_name}", *[item["markdown_path"] for item in design_items]],
        "source_inputs": source_inputs,
        "selected_agents": ["物语合成", "结构材质整合", "提示词架构", "设计审计", "nano-banana-general-auto-image"],
        "statistics": {
            "prop_count": len(packets),
            "special_narrative_prop_count": sum(
                1 for item in packets if item["narrative_significance"].get("is_special")
            ),
            "has_compat_design_projection": bool(args.write_compat_json),
            "has_catalog": True,
            "used_catalog_primary_input": True,
            "used_compat_bridge_fallback": bool(bridge_path and bridge_path.exists()),
        },
        "path_normalization": {
            "requested_output_root": output_dir_repo,
            "canonical_output_root": output_dir_repo,
        },
        "notes": [
            "逐道具 Markdown 是 canonical design truth。",
            "第一输入根固定为 `道具清单.json`；`prop_design_bridge.json` 仅兼容 fallback。",
            "未显式开启 `--write-compat-json` 时，不再默认生成 `道具设计.json`。",
            "面板层与下游若需 prompt，统一从逐道具 Markdown 的 `**prompt整合**` 区块提取。",
            "正式 pipeline 默认继续调用 nano-banana general 生成同目录同 stem 单主体图片。",
        ],
        "design_items": design_items,
    }

    compat_outputs = []
    if args.write_compat_json:
        design_payload, prompt_payload = build_compat_payloads(
            packets,
            project_name=project_name,
            episode_id=episode_id,
            generated_at=generated_at,
            source_inputs=source_inputs,
            output_dir_repo=output_dir_repo,
            design_name=args.design_name,
        )
        compat_outputs = [
            f"{output_dir_repo}/{args.design_name}",
            f"{output_dir_repo}/{args.prompt_name}",
        ]
        manifest_payload["output_files"].extend(compat_outputs)

    if args.dry_run:
        print(json.dumps(manifest_payload, ensure_ascii=False, indent=2))
        return 0

    output_dir.mkdir(parents=True, exist_ok=True)
    write_json(output_dir / args.manifest_name, manifest_payload)
    if args.write_compat_json:
        write_json(output_dir / args.design_name, design_payload)
        write_json(output_dir / args.prompt_name, prompt_payload)

    print(f"[OK] 写入 manifest: {(output_dir / args.manifest_name).as_posix()}")
    print(f"[OK] 写入设计卡数量: {len(packets)}")
    if args.write_compat_json:
        print(f"[OK] 写入 compat design JSON: {(output_dir / args.design_name).as_posix()}")
        print(f"[OK] 写入 compat prompt JSON: {(output_dir / args.prompt_name).as_posix()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
