#!/usr/bin/env python3
"""Build character design JSON and Markdown cards from role list triad."""

from __future__ import annotations

import argparse
from datetime import datetime
import json
import re
import subprocess
import sys
from pathlib import Path
from typing import Any


SHARED_SCRIPTS_DIR = Path(__file__).resolve().parents[2] / "_shared" / "scripts"
if SHARED_SCRIPTS_DIR.as_posix() not in sys.path:
    sys.path.insert(0, SHARED_SCRIPTS_DIR.as_posix())

from global_style_prefix import extract_global_style_prefix  # noqa: E402
from project_design_fallbacks import load_project_design_fallbacks, nested_get  # noqa: E402


SCRIPT_DIR = Path(__file__).resolve().parent
TEMPLATE_PATH = SCRIPT_DIR.parent / "templates" / "character_masterprompt.structured.v2.md"
VALIDATOR_PATH = SCRIPT_DIR / "validate_character_design_projection.py"
NON_ASCII_RE = re.compile(r"[^\x00-\x7F]")
INTEGRATED_PROMPT_MIN_BYTES = 1800
INTEGRATED_PROMPT_MAX_BYTES = 2200

ROLE_NAME_TRANSLATIONS = {
    "苏晴": "Su Qing",
    "苏国雄": "Su Guoxiong",
    "贺廷": "He Ting",
    "林深": "Lin Shen",
    "司机": "The Driver",
}

COSTUME_STATE_TRANSLATIONS = {}

PLACEHOLDER_PATTERNS = (
    "Character ",
    "documented continuity costume state",
    "premium urban-drama",
    "urban-romance",
    "contemporary urban luxury-drama",
)
LEGACY_SCRIPT_AUTHORSHIP_ERROR = (
    "根据 AGENTS.md 的 `内容创作型任务的 LLM 主创规则`，核心创作环节不得再由脚本直接生成。"
    "本脚本仅保留给受控兼容迁移/投影场景；如确需临时执行旧式脚本主创，请显式传入 "
    "`--allow-legacy-script-authorship`。"
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="从 `角色清单.json + role_design_bridge.json + 角色研究.json` 生成角色设计稿。"
    )
    parser.add_argument("--catalog", required=True, help="角色清单.json 路径")
    parser.add_argument("--research", help="角色研究.json 路径；默认按清单目录自动推断")
    parser.add_argument("--bridge", help="role_design_bridge.json 路径；默认按清单目录自动推断")
    parser.add_argument("--global-style", help="全局风格.md 路径；默认按项目根自动推断")
    parser.add_argument("--type-elements", help="全集类型元素.md 路径；默认按项目根自动推断")
    parser.add_argument("--design-elements", help="导演意图.md 路径；默认按项目根自动推断")
    parser.add_argument("--north-star", help="north_star.yaml 路径；默认按项目根自动推断")
    parser.add_argument("--init-handoff", help="init_handoff.yaml 路径；默认按项目根自动推断")
    parser.add_argument("--output-dir", help="输出目录；默认推断到 `4-Design/角色/2-设计/第N集/`")
    parser.add_argument("--design-name", default="character_design.json", help="设计 JSON 文件名")
    parser.add_argument("--manifest-name", default="_manifest.json", help="manifest 文件名")
    parser.add_argument("--role-id", action="append", dest="role_ids", help="只处理指定 role_id，可重复传入")
    parser.add_argument("--role-name", action="append", dest="role_names", help="只处理指定角色名，可重复传入")
    parser.add_argument("--dry-run", action="store_true", help="只打印 manifest，不写文件")
    parser.add_argument("--skip-auto-image", action="store_true", help="只生成设计文件，不调用 内置 imagegen 自动生图")
    parser.add_argument("--auto-image-dry-run", action="store_true", help="写 manifest 并验证自动生图 payload，不真实请求 API")
    parser.add_argument("--auto-image-timeout", type=int, default=300, help="单个自动生图子进程最长等待秒数")
    parser.add_argument(
        "--allow-legacy-script-authorship",
        action="store_true",
        help="受控兼容模式：允许旧式脚本直接生成创作型角色设计内容。",
    )
    return parser.parse_args()


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def write_text(path: Path, text: str) -> None:
    path.write_text(text.rstrip() + "\n", encoding="utf-8")


def read_text(path: Path | None) -> str:
    if path is None or not path.exists():
        return ""
    return path.read_text(encoding="utf-8")


def to_repo_path(path: Path) -> str:
    try:
        return path.resolve().relative_to(Path.cwd().resolve()).as_posix()
    except ValueError:
        return path.as_posix()


def compact_text(text: Any, limit: int = 220) -> str:
    clean = re.sub(r"\s+", " ", str(text or "")).strip()
    if len(clean) <= limit:
        return clean
    return clean[: limit - 3].rstrip() + "..."


def safe_filename(text: str) -> str:
    return re.sub(r"[\\/:*?\"<>|]+", "-", text).strip() or "unnamed"


def first_non_empty(*values: Any) -> Any:
    for value in values:
        if value not in (None, "", [], {}):
            return value
    return ""


def as_list(value: Any) -> list[Any]:
    if value in (None, ""):
        return []
    if isinstance(value, list):
        return value
    return [value]


def infer_project_root(catalog_path: Path) -> Path:
    try:
        return catalog_path.resolve().parents[4]
    except IndexError as exc:
        raise ValueError(f"无法从 catalog 路径推断项目根: {catalog_path}") from exc


def infer_output_dir(catalog_path: Path) -> Path:
    episode_dir = catalog_path.parent
    return episode_dir.parent.parent / "2-设计" / episode_dir.name


def first_existing(*paths: Path) -> Path | None:
    for path in paths:
        if path.exists():
            return path
    return None


def select_roles(roles: list[dict[str, Any]], role_ids: list[str], role_names: list[str]) -> list[dict[str, Any]]:
    if not role_ids and not role_names:
        return roles
    id_set = {item for item in role_ids if item}
    name_set = {item for item in role_names if item}
    selected: list[dict[str, Any]] = []
    for role in roles:
        if id_set and str(role.get("role_id", "")) in id_set:
            selected.append(role)
            continue
        if name_set and str(role.get("canonical_name", "")) in name_set:
            selected.append(role)
    return selected


def lookup_role(items: list[dict[str, Any]], role_id: str, role_name: str) -> dict[str, Any]:
    for item in items:
        if str(item.get("role_id", "")) == role_id:
            return item
    for item in items:
        if str(item.get("canonical_name", "")) == role_name:
            return item
    return {}


def role_name_en(role_name: str, role_id: str, *, project_fallbacks: dict[str, Any] | None = None) -> str:
    registry_translation = nested_get(project_fallbacks, "roles", "name_translations", role_name, default="")
    if registry_translation:
        return registry_translation
    if role_name in ROLE_NAME_TRANSLATIONS:
        return ROLE_NAME_TRANSLATIONS[role_name]
    if not NON_ASCII_RE.search(role_name):
        return role_name.title()
    return role_name


def ascii_or_fallback(value: Any, fallback: str) -> str:
    text = compact_text(value, 260)
    if not text:
        return fallback
    return text


def force_ascii(text: str) -> str:
    return re.sub(r"\s+", " ", str(text or "")).strip()


def ascii_list_or_fallback(values: list[Any], fallback: str) -> list[str]:
    cleaned = [force_ascii(compact_text(value, 80)) for value in values if compact_text(value, 80)]
    cleaned = [value for value in cleaned if value]
    return cleaned or [fallback]


def english_style_prefix(style_text: str) -> str:
    prefix = extract_global_style_prefix(style_text, limit=220)
    if "侍魂天草降临" in prefix or "徐克1994香港武侠电影美学" in prefix or "和田惠美" in prefix:
        return (
            "A gothic-romantic wuxia design language with 35mm film grain, soft halation, volumetric fog, "
            "wind-lifted robes, floating debris, low-angle momentum, practical smoke, and operatic costume silhouettes."
        )
    if "港风都市记忆质感" in prefix and "潮湿夜色" in prefix:
        return (
            "A restrained premium urban-drama look with humid night air, layered reflections, "
            "warm low-saturation interiors, realistic skin detail, and cinematic depth that keeps "
            "public glamour and private ache in the same frame."
        )
    if prefix:
        return "Follow the established project-wide cinematic style in a grounded, production-ready visual direction."
    return "Follow the documented project-wide cinematic style without inventing a different genre."


def role_profile(role_name: str, role_tier: str, *, project_fallbacks: dict[str, Any] | None = None) -> dict[str, str]:
    defaults = {
        "identity": f"{role_name_en(role_name, 'role', project_fallbacks=project_fallbacks)} should read as a documented {role_tier} whose design stays grounded in the current story world and visible role pressure.",
        "tension": "Show discipline, fatigue, danger, and unfinished feeling inside the posture before overt action begins.",
        "power_axis": "public restraint versus private fracture",
        "differentiation": "status signal, costume continuity, weather exposure, and emotional containment",
        "face_signature": "features should stay grounded in story evidence and avoid generic beauty-shot smoothing",
        "hair_signature": "hair and head silhouette should follow travel, weather, labor, class, and sword-world continuity",
        "body_signature": "the silhouette should stay readable, tense, and story-specific before any action flourish",
        "costume_signature": "costume logic should reflect the documented world, status, travel condition, and continuity chain rather than modern styling tropes",
        "continuity_signature": "repeat costume states, key accessories, and recurring prop anchors must stay stable across linked groups and shots",
        "story_narrative": f"{role_name_en(role_name, 'role', project_fallbacks=project_fallbacks)} should carry visible role pressure, lived-in continuity, and the emotional cost of the current episode in one clean reference portrait.",
    }
    registry_profiles = nested_get(project_fallbacks, "roles", "profiles", default={}) or {}
    profiles = {
        "苏晴": {
            "identity": "Su Qing is the heiress being publicly priced on her birthday night, carrying luxury polish as a shell while her agency struggles to return.",
            "tension": "She must look expensive, controlled, and socially trained, yet every frame should hint that the public display is already breaking from inside.",
            "power_axis": "a publicly displayed heiress versus a woman fighting to reclaim self-definition",
            "differentiation": "birthday glamour, cold restraint, rain-soaked escape, and recovered agency",
            "face_signature": "polite smile, frost in the eyes, delicate glamour under emotional suppression",
            "hair_signature": "well-kept formal styling that can later loosen with rain, escape, and exhaustion",
            "body_signature": "slender poised silhouette, shoulders held by social training, posture cracking only when control slips",
            "costume_signature": "luxury birthday dress system that can transition into wet, damaged, and survival-led states without losing continuity",
            "continuity_signature": "dress state, jewelry removal, bare feet, and recovery layers must stay readable as one emotional chain",
            "story_narrative": "Su Qing starts as a polished display object inside an upscale family ritual, then turns into a rain-soaked runaway who slowly reclaims warmth and subjecthood without losing the memory of that public humiliation.",
        },
        "苏国雄": {
            "identity": "Su Guoxiong is the patriarch who treats etiquette, tailoring, and public staging as instruments of control.",
            "tension": "He must look calm, expensive, and immovable, so the violence arrives through order, not visible rage.",
            "power_axis": "institutional paternal authority versus the daughter's attempt to leave the price system",
            "differentiation": "chairman discipline, display instinct, and emotionally sterile control",
            "face_signature": "measured expression, firm gaze, and almost administrative emotional temperature",
            "hair_signature": "disciplined business grooming with no softness",
            "body_signature": "stable centered posture, minimal wasted motion, authority communicated through stillness",
            "costume_signature": "dark precise business tailoring with no looseness or decorative warmth",
            "continuity_signature": "main stage suit, glass, watch, and host position must keep his public power legible",
            "story_narrative": "Su Guoxiong should feel like a man who can turn celebration into an instrument of valuation without ever raising his voice, making control appear as order.",
        },
        "贺廷": {
            "identity": "He Ting is the polished alliance candidate whose calm manners still carry the pressure of a transaction.",
            "tension": "He must appear composed and socially effortless, while his proximity and gestures feel like formalized takeover rather than romance.",
            "power_axis": "gentle surface etiquette versus the coercive logic of alliance and possession",
            "differentiation": "tailored calm, social fluency, and invasive closeness disguised as reasonableness",
            "face_signature": "well-managed expression, socially attractive surface, and confidence without overt warmth",
            "hair_signature": "precise upscale grooming that matches polished tailoring",
            "body_signature": "upright elegant silhouette with movement that is calm but encroaching",
            "costume_signature": "refined suit system built for alliance display, not intimacy",
            "continuity_signature": "proposal jewelry, formal gloves or cuff details, and ceremonial stance must stay transaction-readable",
            "story_narrative": "He Ting should be designed as a man who looks acceptable to everyone in the room while still reading as an extension of the power structure closing around Su Qing.",
        },
        "林深": {
            "identity": "Lin Shen is the warm refuge in the alley, a man whose practicality and care become the opposite of the public price system.",
            "tension": "He must feel grounded, capable, and emotionally open without losing the fatigue and rough edges of real work.",
            "power_axis": "ordinary working warmth versus elite public spectacle",
            "differentiation": "rolled-up sleeves, lived-in softness, and instinctive care under restraint",
            "face_signature": "tired but attentive eyes, clean emotional readability, and understated attractiveness",
            "hair_signature": "practical real-world styling with minimal vanity",
            "body_signature": "functional working silhouette, dependable physical support, and gentle restraint",
            "costume_signature": "post-shift clothing that can absorb rain, labor, and protective action without becoming shabby costume shorthand",
            "continuity_signature": "rolled sleeves, workwear layers, and care-taking proximity must remain consistent across shelter scenes",
            "story_narrative": "Lin Shen should immediately read as the first space of safety Su Qing can enter, with everyday practicality and quiet emotional steadiness replacing spectacle.",
        },
        "司机": {
            "identity": "The Driver is a lower-ranking witness trapped inside the same family order, useful as a pressure-transfer figure rather than a full protagonist.",
            "tension": "He should look like someone trained to obey hierarchy while still visibly registering discomfort when the emotional violence becomes undeniable.",
            "power_axis": "service labor under hierarchy versus the heroine's decisive refusal",
            "differentiation": "functional uniformity, hesitation, and reluctant witness energy",
            "face_signature": "reserved expression with reluctant eye contact",
            "hair_signature": "practical service grooming",
            "body_signature": "kept-in posture shaped by work discipline and caution",
            "costume_signature": "driver or service-oriented clothing with hierarchy-coded neatness",
            "continuity_signature": "keys, front-seat rhythm, and the handoff of returned valuables must stay clear",
            "story_narrative": "The Driver should be designed as the human edge of the family machine, someone who keeps the order moving but cannot fully hide his discomfort when Su Qing rejects it.",
        },
    }
    return {**defaults, **profiles.get(role_name, {}), **registry_profiles.get(role_name, {})}


def has_placeholder_text(text: Any) -> bool:
    clean = compact_text(text, 320)
    if not clean:
        return True
    markers = (
        "unknown",
        "情绪张力待补",
        "角色表现目前最强的镜头提示是",
        "###场景",
    )
    return any(marker in clean for marker in markers)


def choose_clean_text(primary: Any, fallback: str) -> str:
    text = compact_text(primary, 320)
    if has_placeholder_text(text):
        return fallback
    return text


def compute_quality_flags(role: dict[str, Any], bridge_role: dict[str, Any], research_role: dict[str, Any]) -> list[str]:
    flags = list(as_list(first_non_empty(bridge_role.get("quality_flags"), research_role.get("quality_flags"), [])))
    if "unknown_by_shot_evidence" in json.dumps(bridge_role, ensure_ascii=False):
        flags.append("face_and_hair_need_manual_lock")
    return sorted(set(flag for flag in flags if flag))


def english_role_tier(role_tier: str) -> str:
    mapping = {"主角": "lead", "重要配角": "major supporting", "功能配角": "supporting", "群像": "ensemble"}
    return mapping.get(role_tier, "supporting")


def translate_costume_state(value: Any, *, project_fallbacks: dict[str, Any] | None = None) -> str:
    text = compact_text(value, 160)
    if not text:
        return "documented continuity costume state"
    registry_translation = nested_get(project_fallbacks, "roles", "costume_state_translations", text, default="")
    if registry_translation:
        return registry_translation
    if text in COSTUME_STATE_TRANSLATIONS:
        return COSTUME_STATE_TRANSLATIONS[text]
    if NON_ASCII_RE.search(text):
        return "documented continuity costume state"
    return text


def build_structured_fields(
    role: dict[str, Any],
    bridge_role: dict[str, Any],
    profile: dict[str, str],
    *,
    project_fallbacks: dict[str, Any] | None = None,
) -> dict[str, Any]:
    costume_state = str(role.get("costume_state", "unknown"))
    role_name = str(role.get("canonical_name", "Character"))
    role_en = role_name_en(role_name, str(role.get("role_id", "role-000")), project_fallbacks=project_fallbacks)
    return {
        "face": {
            "reference": role_en,
            "makeup": "natural realism tuned to emotional pressure",
            "face_shape": "balanced oval with readable cheek and jaw structure",
            "bone_structure": "clean cheekbones and realistic mid-face tension",
            "eyes": profile["face_signature"],
            "eyelashes": "natural lashes with cinematic realism",
            "brows": "controlled brows that show class and emotional restraint",
            "nose": "clean natural bridge, not stylized",
            "mouth": "restraint-first lips that can hold suppressed emotion",
        },
        "hair": {
            "style": profile["hair_signature"],
            "length": "medium length unless explicit evidence requires otherwise",
            "color": "natural dark tone",
            "texture": "real-world texture with humidity-aware behavior",
            "hairline": "natural realistic hairline",
            "temple_hair": "soft real flyaways only when evidence supports stress or rain",
        },
        "body": {
            "reference": role_en,
            "age": "young adult to middle-aged as documented by role function",
            "species": "human",
            "gender": "story-documented presentation",
            "occupation": english_role_tier(str(role.get("role_tier", "功能配角"))),
            "style": profile["body_signature"],
            "height": "realistic adult proportion grounded in the documented role",
            "weight": "natural build with no exaggerated stylization",
            "build": profile["body_signature"],
            "posture": "posture carries social role before overt movement",
            "proportion": "believable wuxia-drama anatomy with practical movement logic",
            "upper_arm": "arms follow class, work, and emotional control signals",
            "finger": "hands should look usable, not mannequin-like",
            "leg": "leg line follows costume and stance requirements",
            "foot": "footwear logic must remain continuous with costume state",
        },
        "costume": {
            "era": "historical or wuxia-inflected East Asian story world",
            "brand": "evidence-driven costume craft rather than modern logo branding",
            "style": profile["costume_signature"],
            "culture": "East Asian martial-world costume logic driven by status, travel, labor, and continuity",
            "type": costume_state,
            "attribute": bridge_role.get("costume_bridge", {}).get("costume_system", costume_state),
            "head": "minimal head accessories unless explicitly documented",
            "upper": costume_state,
            "lower": "coherent with silhouette and movement",
            "foot": "footwear must match the documented state chain",
        },
        "camera": {
            "photo_type": "single character design portrait",
            "shot_size": "three-quarter to full body character sheet framing",
            "background": "solid color background, no scene background elements",
            "composition": "single-subject centered composition with premium editorial clarity",
            "camera_setup": "cinematic portrait realism with restrained depth and readable skin texture",
            "midjourney_params": "--ar 2:3 --stylize 120 --v 8",
        },
    }


def render_template(template_text: str, values: dict[str, str]) -> str:
    output = template_text
    for key, value in values.items():
        output = output.replace(f"[{key}]", str(value))
    return output


def fit_integrated_prompt(sentences: list[str], *, extra_reinforcements: list[str] | None = None) -> str:
    prompt = " ".join(" ".join(sentence.split()) for sentence in sentences if sentence.strip())
    reinforcements = [
        "Keep the portrait grounded in cinematic wuxia realism, with believable skin texture, weathered material response, and emotional pressure carried by posture before gesture.",
        "Every visible choice must serve identity, costume continuity, and relationship pressure rather than decorative fantasy, and the image should read as one coherent production-ready design brief.",
        "Use solid color background and no scene background elements so the portrait functions as a clean downstream reference asset, not a narrative still, group tableau, or environment concept frame.",
        "Preserve the exact contrast between public polish and private fracture, using face tension, body control, and costume state as the main storytelling carriers inside the frame.",
        "Keep accessories, costume seams, fabric response, grooming details, and wear marks specific enough for panel continuity while staying within the documented world rather than drifting into modern fashion portrait logic.",
        "Do not add extra characters, props-as-environment, room context, street context, architecture, signage, or decorative scenic storytelling beyond what a pure character reference portrait can legitimately hold.",
        "Let camera distance, silhouette readability, and emotional restraint feel ready for casting sheets, design boards, and later continuity reference, with no dependence on scene geography.",
    ]
    if extra_reinforcements:
        reinforcements = [*reinforcements, *extra_reinforcements]
    for sentence in reinforcements:
        candidate = f"{prompt} {sentence}"
        if len(candidate.encode('utf-8')) <= INTEGRATED_PROMPT_MAX_BYTES:
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
    if len(prompt.encode("utf-8")) < INTEGRATED_PROMPT_MIN_BYTES:
        prompt = (
            f"{prompt} Keep identity clarity, continuity, silhouette, grooming, tailoring, and emotional readability all visible in one single-subject reference portrait. "
            "Maintain solid color background and no scene background elements as non-negotiable guardrails for downstream clean-reference usage."
        )
    return prompt


def build_packet(
    role: dict[str, Any],
    *,
    bridge_role: dict[str, Any],
    research_role: dict[str, Any],
    global_style_text: str,
    type_elements_text: str,
    design_elements_text: str,
    north_star_text: str,
    init_handoff_text: str,
    project_fallbacks: dict[str, Any] | None = None,
) -> dict[str, Any]:
    role_id = str(role.get("role_id", "role-000"))
    role_name = str(role.get("canonical_name", "Character"))
    role_en = role_name_en(role_name, role_id, project_fallbacks=project_fallbacks)
    role_tier = str(role.get("role_tier", "功能配角"))
    profile = role_profile(role_name, role_tier, project_fallbacks=project_fallbacks)
    bridge_profile = bridge_role.get("design_bridge_profile", {}) if isinstance(bridge_role, dict) else {}
    appearance_bridge = first_non_empty(bridge_profile.get("appearance_bridge"), bridge_role.get("appearance_bridge"), {}) or {}
    costume_bridge = first_non_empty(bridge_profile.get("costume_bridge"), bridge_role.get("costume_bridge"), {}) or {}
    continuity_bridge = first_non_empty(bridge_profile.get("continuity_bridge"), bridge_role.get("continuity_bridge"), {}) or {}
    prompt_ready = first_non_empty(bridge_profile.get("prompt_ready"), bridge_role.get("prompt_ready"), {}) or {}
    research_profile = research_role.get("research_profile", {}) if isinstance(research_role, dict) else {}
    display_profile = research_role.get("display_profile", {}) if isinstance(research_role, dict) else {}

    global_style_prefix = extract_global_style_prefix(global_style_text, limit=220)
    global_style_prefix_en = english_style_prefix(global_style_text)
    style_backbone = compact_text(global_style_prefix, 180) or compact_text(type_elements_text, 180) or "项目级风格骨架"
    character_style = (
        "grounded wuxia character realism with pressure carried by posture, weather, costume continuity, and restrained emotion"
    )
    design_guardrails = (
        "Keep the character grounded, emotionally legible, and continuity-safe; avoid modern portrait drift, cosplay exaggeration, and scenic-background storytelling."
    )
    identity_hook = choose_clean_text(prompt_ready.get("identity_hook"), profile["identity"])
    if "/" in identity_hook and len(identity_hook) <= 24:
        identity_hook = profile["identity"]
    narrative_tension = choose_clean_text(prompt_ready.get("narrative_tension"), profile["tension"])
    power_axis = profile["power_axis"]
    differentiation_axes = profile["differentiation"]
    costume_state_en = translate_costume_state(role.get("costume_state"), project_fallbacks=project_fallbacks)
    continuity_seed = as_list(continuity_bridge.get("core_props"))
    if not continuity_seed or continuity_seed == ["unknown"]:
        continuity_seed = as_list(continuity_bridge.get("recurring_states")) or [role.get("costume_state", "documented continuity objects")]
    continuity_items = [translate_costume_state(item, project_fallbacks=project_fallbacks) for item in continuity_seed]
    continuity_items = [item for item in continuity_items if item and item != "documented continuity costume state"] or ["documented continuity objects"]
    story_premise = choose_clean_text(
        first_non_empty(
            research_profile.get("sentence_conclusion"),
            research_profile.get("identity_read"),
            bridge_role.get("role_identity", {}).get("identity_read"),
            profile["story_narrative"],
        ),
        profile["story_narrative"],
    )
    structured_fields = build_structured_fields(role, bridge_role, profile, project_fallbacks=project_fallbacks)
    reasoning_pivot = (
        f"{role_en} must be designed as a single-subject wuxia reference portrait where identity pressure, costume continuity, "
        f"weather exposure, and emotional restraint are readable before action, keeping {power_axis} visible without scenic distraction."
    )

    prompt_sentences = [
        f"Design {role_en} as a single-character wuxia reference portrait, built for continuity-safe downstream use rather than a narrative still.",
        "Keep solid color background and no scene background elements at all times, so the frame stays clean for later reference reuse.",
        f"Identity hook: {identity_hook}. Narrative tension: {narrative_tension}.",
        f"Power axis: {power_axis}. Differentiation axes: {differentiation_axes}.",
        f"Face signature: {profile['face_signature']}. Hair signature: {profile['hair_signature']}. Body signature: {profile['body_signature']}.",
        f"Costume system: {profile['costume_signature']}. Current costume state: {costume_state_en}.",
        f"Continuity guard: {profile['continuity_signature']}.",
        f"Visual style backbone: {global_style_prefix_en}",
        "Use realistic skin detail, restrained cinematic lighting, believable anatomy, and costume craft that belongs to the documented martial world.",
        f"Reference any prop pressure only as off-screen continuity through {', '.join(continuity_items[:3])}, never as an environment or hand-held action in the frame.",
        f"Story premise: {story_premise}.",
        "The portrait must feel casting-ready, design-board ready, and emotionally specific, with posture carrying social pressure before any overt dramatic gesture.",
    ]
    extra_reinforcements = list(nested_get(project_fallbacks, "roles", "prompt_reinforcements", default=[]) or [])
    prompt_integration = force_ascii(fit_integrated_prompt(prompt_sentences, extra_reinforcements=extra_reinforcements))
    full_generation_prompt = (
        f"Global style prefix: {global_style_prefix_en}\n\n"
        f"Integrated prompt: {prompt_integration}"
    )

    return {
        "role_id": role_id,
        "canonical_name": role_name,
        "role_name": role_name,
        "role_name_en": role_en,
        "role_tier": role_tier,
        "costume_state": str(role.get("costume_state", "unknown")),
        "story_premise": story_premise,
        "identity_hook": identity_hook,
        "narrative_tension": narrative_tension,
        "style_backbone": style_backbone,
        "character_style": character_style,
        "design_guardrails": design_guardrails,
        "structured_fields": structured_fields,
        "prompt_integration": prompt_integration,
        "global_style_prefix": global_style_prefix,
        "global_style_prefix_en": global_style_prefix_en,
        "full_generation_prompt": full_generation_prompt,
        "final_prompt": full_generation_prompt,
        "quality_flags": compute_quality_flags(role, bridge_role, research_role),
        "source_trace": {
            "catalog_role_id": role_id,
            "catalog_group_ids": role.get("group_ids", []),
            "catalog_shot_ids": role.get("shot_ids", []),
            "bridge_present": bool(bridge_role),
            "research_present": bool(research_role),
            "source_inputs": {
                "catalog": True,
                "bridge": bool(bridge_role),
                "research": bool(research_role),
                "north_star": bool(north_star_text.strip()),
                "init_handoff": bool(init_handoff_text.strip()),
                "global_style": bool(global_style_text.strip()),
                "type_elements": bool(type_elements_text.strip()),
                "design_elements": bool(design_elements_text.strip()),
            },
        },
        "power_axis": power_axis,
        "differentiation_axes": differentiation_axes,
        "reasoning_pivot_en": reasoning_pivot,
        "story_narrative": profile["story_narrative"],
        "face_signature": choose_clean_text(appearance_bridge.get("face_signature"), profile["face_signature"]),
        "hair_signature": choose_clean_text(appearance_bridge.get("hair_signature"), profile["hair_signature"]),
        "body_reference": role_en,
        "body_signature": profile["body_signature"],
        "costume_signature": costume_bridge.get("costume_system", profile["costume_signature"]),
        "continuity_signature": continuity_bridge.get("continuity_guard", profile["continuity_signature"]),
        "photo_type": structured_fields["camera"]["photo_type"],
        "photo_shot_size": structured_fields["camera"]["shot_size"],
        "photo_background": structured_fields["camera"]["background"],
        "composition": structured_fields["camera"]["composition"],
        "camera_setup": structured_fields["camera"]["camera_setup"],
        "midjourney_params": structured_fields["camera"]["midjourney_params"],
        "display_profile": display_profile,
    }


def find_packet_placeholders(packet: dict[str, Any]) -> list[str]:
    issues: list[str] = []
    serialized = json.dumps(packet, ensure_ascii=False)
    for token in PLACEHOLDER_PATTERNS:
        if token in serialized:
            issues.append(token)
    if "unknown_by_shot_evidence" in serialized:
        issues.append("unknown_by_shot_evidence")
    return sorted(set(issues))


def build_markdown(packet: dict[str, Any]) -> str:
    template_text = TEMPLATE_PATH.read_text(encoding="utf-8")
    face = packet["structured_fields"]["face"]
    hair = packet["structured_fields"]["hair"]
    body = packet["structured_fields"]["body"]
    costume = packet["structured_fields"]["costume"]
    camera = packet["structured_fields"]["camera"]
    values = {
        "role_name": packet["role_name"],
        "story_narrative": packet["story_narrative"],
        "reasoning_pivot_en": packet["reasoning_pivot_en"],
        "identity_hook": packet["identity_hook"],
        "narrative_tension": packet["narrative_tension"],
        "power_axis": packet["power_axis"],
        "differentiation_axes": packet["differentiation_axes"],
        "style_backbone": packet["style_backbone"],
        "character_style": packet["character_style"],
        "body_reference": packet["body_reference"],
        "face_signature": packet["face_signature"],
        "hair_signature": packet["hair_signature"],
        "body_signature": packet["body_signature"],
        "costume_signature": packet["costume_signature"],
        "continuity_signature": packet["continuity_signature"],
        "design_guardrails": packet["design_guardrails"],
        "face_makeup": face["makeup"],
        "face_shape_cn": face["face_shape"],
        "face_bone_cn": face["bone_structure"],
        "face_eyes_cn": face["eyes"],
        "face_eyelash_cn": face["eyelashes"],
        "face_brow_cn": face["brows"],
        "face_nose_cn": face["nose"],
        "face_mouth_cn": face["mouth"],
        "hair_style_cn": hair["style"],
        "hair_length_cn": hair["length"],
        "hair_color_cn": hair["color"],
        "hair_texture_cn": hair["texture"],
        "hairline_cn": hair["hairline"],
        "temple_hair_cn": hair["temple_hair"],
        "body_style_cn": body["style"],
        "body_age": body["age"],
        "body_species": body["species"],
        "body_gender": body["gender"],
        "body_occupation": body["occupation"],
        "body_height_cn": body["height"],
        "body_weight_cn": body["weight"],
        "body_type_cn": body["build"],
        "body_posture_cn": body["posture"],
        "body_ratio_cn": body["proportion"],
        "upper_arm_cn": body["upper_arm"],
        "finger_cn": body["finger"],
        "leg_cn": body["leg"],
        "foot_cn": body["foot"],
        "personality_constellation": "TBD",
        "personality_blood_type": "TBD",
        "personality_spirit": packet["identity_hook"],
        "personality_emotion": packet["narrative_tension"],
        "personality_interest": "TBD",
        "personality_inner": packet["story_premise"],
        "personality_id": packet["identity_hook"],
        "costume_era_cn": costume["era"],
        "costume_brand_cn": costume["brand"],
        "costume_style_cn": costume["style"],
        "costume_culture_cn": costume["culture"],
        "costume_type_cn": costume["type"],
        "costume_attribute_cn": costume["attribute"],
        "costume_head_cn": costume["head"],
        "costume_upper_cn": costume["upper"],
        "costume_lower_cn": costume["lower"],
        "costume_foot_cn": costume["foot"],
        "photo_type": camera["photo_type"],
        "photo_shot_size": camera["shot_size"],
        "photo_background": camera["background"],
        "composition": camera["composition"],
        "camera_setup": camera["camera_setup"],
        "midjourney_params": camera["midjourney_params"],
        "global_style_prefix": packet["global_style_prefix_en"],
        "prompt_integration": packet["prompt_integration"],
    }
    return render_template(template_text, values).rstrip() + "\n"


def run_auto_image_guard(
    *,
    output_dir: Path,
    project_name: str,
    global_style_path: Path | None,
    manifest_name: str,
    timeout: int,
    generation_dry_run: bool,
) -> int:
    helper = SHARED_SCRIPTS_DIR / "ensure_design_auto_images.py"
    cmd = [
        sys.executable,
        helper.as_posix(),
        "--design-dir",
        output_dir.as_posix(),
        "--project-name",
        project_name,
        "--manifest-name",
        manifest_name,
        "--timeout",
        str(timeout),
    ]
    if global_style_path and global_style_path.exists():
        cmd.extend(["--global-style", global_style_path.as_posix()])
    if generation_dry_run:
        cmd.append("--generation-dry-run")
    result = subprocess.run(cmd, check=False)
    return int(result.returncode)


def validate_output(output_dir: Path, design_path: Path, manifest_path: Path) -> int:
    cmd = [
        sys.executable,
        VALIDATOR_PATH.as_posix(),
        "--output-dir",
        output_dir.as_posix(),
        "--design-json",
        design_path.as_posix(),
        "--manifest",
        manifest_path.as_posix(),
    ]
    result = subprocess.run(cmd, check=False)
    return int(result.returncode)


def main() -> int:
    args = parse_args()
    if not args.allow_legacy_script_authorship:
        print(f"[ERROR] {LEGACY_SCRIPT_AUTHORSHIP_ERROR}", file=sys.stderr)
        return 2
    catalog_path = Path(args.catalog)
    if not catalog_path.exists():
        print(f"[ERROR] catalog 不存在: {catalog_path}", file=sys.stderr)
        return 1
    if not TEMPLATE_PATH.exists():
        print(f"[ERROR] template 不存在: {TEMPLATE_PATH}", file=sys.stderr)
        return 1

    project_root = infer_project_root(catalog_path)
    project_fallbacks = load_project_design_fallbacks(project_root)
    episode_dir = catalog_path.parent
    episode_id = episode_dir.name
    project_name = project_root.name
    output_dir = Path(args.output_dir) if args.output_dir else infer_output_dir(catalog_path)

    research_path = Path(args.research) if args.research else episode_dir / "角色研究.json"
    bridge_path = Path(args.bridge) if args.bridge else episode_dir / "role_design_bridge.json"
    global_style_path = Path(args.global_style) if args.global_style else first_existing(project_root / "2-Global" / "全局风格.md")
    type_elements_path = Path(args.type_elements) if args.type_elements else first_existing(project_root / "2-Global" / "全集类型元素.md")
    design_elements_path = Path(args.design_elements) if args.design_elements else first_existing(project_root / "2-Global" / "导演意图.md")
    north_star_path = Path(args.north_star) if args.north_star else project_root / "0-Init" / "north_star.yaml"
    init_handoff_path = Path(args.init_handoff) if args.init_handoff else project_root / "0-Init" / "init_handoff.yaml"

    catalog = read_json(catalog_path)
    roles = catalog.get("roles", [])
    selected = select_roles(roles, args.role_ids or [], args.role_names or [])
    if not selected:
        print("[ERROR] 过滤后没有命中任何 role。", file=sys.stderr)
        return 1

    research = read_json(research_path) if research_path.exists() else {}
    bridge = read_json(bridge_path) if bridge_path.exists() else {}
    research_roles = research.get("roles", [])
    bridge_roles = bridge.get("roles", [])

    packets = [
        build_packet(
            role,
            bridge_role=lookup_role(bridge_roles, str(role.get("role_id", "")), str(role.get("canonical_name", ""))),
            research_role=lookup_role(research_roles, str(role.get("role_id", "")), str(role.get("canonical_name", ""))),
            global_style_text=read_text(global_style_path),
            type_elements_text=read_text(type_elements_path),
            design_elements_text=read_text(design_elements_path),
            north_star_text=read_text(north_star_path),
            init_handoff_text=read_text(init_handoff_path),
            project_fallbacks=project_fallbacks,
        )
        for role in selected
    ]
    packet_issues = {
        packet["canonical_name"]: find_packet_placeholders(packet)
        for packet in packets
    }
    packet_issues = {name: issues for name, issues in packet_issues.items() if issues}
    if packet_issues:
        print(
            "[ERROR] 角色设计包仍含占位或错域回退，已阻止继续落盘: "
            + json.dumps(packet_issues, ensure_ascii=False),
            file=sys.stderr,
        )
        return 1

    generated_at = datetime.now().isoformat(timespec="seconds")
    output_dir_repo = to_repo_path(output_dir)
    design_path = output_dir / args.design_name
    manifest_path = output_dir / args.manifest_name

    source_inputs = [to_repo_path(catalog_path)]
    for path in (research_path, bridge_path, global_style_path, type_elements_path, design_elements_path, north_star_path, init_handoff_path):
        if path and path.exists():
            source_inputs.append(to_repo_path(path))
    source_inputs = list(dict.fromkeys(source_inputs))

    design_payload = {
        "meta": {
            "schema_version": "aigc/character-design/v1",
            "skill_id": "aigc-design-role-design",
            "project_name": project_name,
            "episode_id": episode_id,
            "generated_at": generated_at,
            "source_inputs": source_inputs,
        },
        "roles": packets,
    }

    output_files = [f"{output_dir_repo}/{args.design_name}", f"{output_dir_repo}/{args.manifest_name}"]
    for packet in packets:
        output_files.append(f"{output_dir_repo}/{safe_filename(packet['role_name'])}.md")

    manifest = {
        "status": "design_files_ready",
        "project_name": project_name,
        "episode_id": episode_id,
        "generated_at": generated_at,
        "input_files": source_inputs,
        "output_dir": output_dir_repo,
        "output_files": output_files,
        "role_count": len(packets),
        "selected_roles": [packet["role_name"] for packet in packets],
        "auto_image": {
            "provider_skill": "imagegen",
            "provider_mode": "built-in image_gen",
            "default_model": "GPT-IMAGE-2",
            "mode": "single-subject-t2i",
            "status": "skipped_by_user" if args.skip_auto_image else ("dry_run" if args.auto_image_dry_run else "pending"),
            "prompt_field": "full_generation_prompt",
            "output_dir_policy": "same_directory_as_design_file",
            "filename_policy": "same_stem_as_design_file",
            "image_paths": [],
        },
        "notes": [
            "character_design.json 是 machine-first canonical truth。",
            "同目录 `[角色名].md` 是 human projection，不得抢占 JSON 主权。",
        ],
    }

    if args.dry_run:
        print(json.dumps(manifest, ensure_ascii=False, indent=2))
        return 0

    output_dir.mkdir(parents=True, exist_ok=True)
    write_json(design_path, design_payload)
    for packet in packets:
        markdown_path = output_dir / f"{safe_filename(packet['role_name'])}.md"
        write_text(markdown_path, build_markdown(packet))
    write_json(manifest_path, manifest)

    validation_exit = validate_output(output_dir, design_path, manifest_path)
    if validation_exit != 0:
        return validation_exit

    if not args.skip_auto_image:
        auto_exit = run_auto_image_guard(
            output_dir=output_dir,
            project_name=project_name,
            global_style_path=global_style_path,
            manifest_name=args.manifest_name,
            timeout=args.auto_image_timeout,
            generation_dry_run=args.auto_image_dry_run,
        )
        if auto_exit != 0:
            return auto_exit

    print(f"[OK] 写入角色设计真源: {design_path.as_posix()}")
    print(f"[OK] 写入角色 Markdown 数量: {len(packets)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
    costume_state_en = ascii_or_fallback(role.get("costume_state"), "documented continuity costume state")
    continuity_items = ascii_list_or_fallback(as_list(continuity_bridge.get("core_props")), "documented continuity objects")
