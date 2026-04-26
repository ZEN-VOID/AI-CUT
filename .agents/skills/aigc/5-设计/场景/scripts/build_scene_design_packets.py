#!/usr/bin/env python3
"""Build scene design JSON and Markdown cards from the scene list triad."""

from __future__ import annotations

import argparse
from datetime import datetime
import json
import re
import subprocess
import sys
from pathlib import Path
from typing import Any

SCRIPT_DIR = Path(__file__).resolve().parent
SHARED_SCRIPTS_DIR = SCRIPT_DIR
if SHARED_SCRIPTS_DIR.as_posix() not in sys.path:
    sys.path.insert(0, SHARED_SCRIPTS_DIR.as_posix())

from global_style_prefix import extract_global_style_prefix  # noqa: E402
from project_design_fallbacks import load_project_design_fallbacks, nested_get  # noqa: E402


TEMPLATE_PATH = SCRIPT_DIR.parent / "templates" / "scene_masterprompt.structured.v2.md"
NON_ASCII_RE = re.compile(r"[^\x00-\x7F]")
INTEGRATED_PROMPT_MIN_BYTES = 1800
INTEGRATED_PROMPT_MAX_BYTES = 2200
PLACEHOLDER_PATTERNS = (
    "Documented Scene",
    "Near-future lived-in public infrastructure",
    "holographic",
    "a 2049 near-future Chinese community setting",
)
LEGACY_SCRIPT_AUTHORSHIP_ERROR = (
    "根据 AGENTS.md 的 `内容创作型任务的 LLM 主创规则`，核心创作环节不得再由脚本直接生成。"
    "本脚本仅保留给受控兼容迁移/投影场景；如确需临时执行旧式脚本主创，请显式传入 "
    "`--allow-legacy-script-authorship`。"
)


SCENE_NAME_TRANSLATIONS = {
    "中央全息广场": "Central Holographic Plaza",
    "全息锦鲤池": "Holographic Koi Pond",
    "开放广场": "Open Community Plaza",
    "池边": "Koi Pond Edge",
    "锦鲤池": "Koi Pond",
    "广场": "Community Plaza",
    "广场舞区域": "Plaza Dance Area",
    "广场中心": "Plaza Center",
    "广场四周": "Outer Plaza Ring",
    "木星工程背景": "Jupiter Engineering Backdrop",
    "深空背景": "Deep-Space Backdrop",
    "卫生间门": "Bathroom Door",
    "卫生间": "Bathroom",
    "黑暗卧室与床头": "Dark Bedroom And Bedhead Wall",
    "空墙面": "Blank Wall",
    "洗手池": "Washbasin",
    "卫生间门板": "Bathroom Door Panel",
    "门板": "Door Panel",
    "吊顶": "Ceiling Void",
    "楼道": "Apartment Corridor",
    "卫生间吊顶": "Bathroom Ceiling Void",
}

PHRASE_TRANSLATIONS = {
    "公共广场": "public community plaza",
    "室外": "exterior public space",
    "室内": "interior space",
    "景观": "landscape space",
    "玻璃/投影介质": "glass and projection media",
    "混凝土/石材": "concrete and stone",
    "水体/湿面": "water and wet surfaces",
    "金属/工程结构": "metal engineering structure",
    "清亮白金": "clear platinum morning light",
    "冷青灰": "cool cyan-gray",
    "暖金红": "warm gold-red",
    "开敞中心": "open central layout",
    "水岸/池缘边界": "pool-edge boundary",
    "线性通行": "linear circulation",
    "围观路线": "spectator circulation ring",
    "晨间": "morning",
    "晨光": "morning light",
    "洁净空气": "clean air",
    "秩序": "orderly atmosphere",
    "红光": "red alert glow",
    "高危红": "high-risk red alert light",
    "震动": "vibration",
    "风": "wind",
    "世界/秩序建立": "world and order establishment",
    "关系推进": "relationship progression",
    "场景承接": "scene handoff support",
    "危险": "danger signal",
    "失控": "loss of control",
    "作为": "as",
    "全息鱼": "holographic fish",
    "水景节点": "waterscape node",
    "交通过渡空间": "transitional circulation space",
    "水域边界": "water boundary",
    "晨间步道": "morning walkway",
    "步道": "walkway",
    "社区广场": "community plaza",
    "人物仍被池边日常空间包围": "characters are still surrounded by ordinary poolside space",
    "人物关系处于短暂顺风状态": "the relationship is briefly moving smoothly",
    "但危险信号已经在老刘手中炸开": "but the danger signal has already erupted in Lao Liu's hand",
    "和现场荒诞形成软性反差": "softly contrasts with the absurd situation",
    "对比现实鱼的证据背景": "evidence backdrop contrasting holographic fish with real fish",
    "广场中央忽然被扇形光柱占住": "the plaza center is suddenly occupied by a fan-shaped light beam",
    "日常空间被异物强行打开": "ordinary daily space is forced open by a technological anomaly",
    "广场舞大妈群像位于张飞矛尖指向的前方区域": "the plaza-dance crowd sits in the area in front of the spear's mistaken direction",
    "成为荒诞误判的背景面": "serving as the background plane for an absurd misjudgment",
    "深邃宇宙": "deep space",
    "恒星强光和缓慢旋转的金属结构占据张飞身侧上方": "stellar glare and slowly rotating metal structures occupy the upper side background",
    "广场空间被拉出宇宙尺度": "the plaza is stretched into a cosmic scale",
    "深空金属结构和工程语境继续稳压在画面上方": "deep-space metal structures and engineering context press calmly above the frame",
    "广场显得更小更可笑": "the plaza feels smaller and more comically exposed",
    "木星工程背景和操作面板成为技术收束的冷静背景层": "the Jupiter engineering backdrop and control panels become a calm technical background layer",
    "科技词汇和生活场景故意形成反差": "technological vocabulary deliberately contrasts with the everyday community setting",
    "锦鲤池和数据鱼保持可读": "the koi pond and data fish remain readable",
    "视觉中心从池景转向老刘手中的核桃": "the visual center shifts from the pond to the walnut in Lao Liu's hand",
    "静姐一侧仍靠着锦鲤池": "Jingjie's side of the frame remains anchored by the koi pond",
    "静姐背后仍是锦鲤池和整洁社区": "behind Jingjie remain the koi pond and tidy community",
    "池边环境仍稳定": "the poolside environment remains stable",
    "池边空间还没乱": "the poolside space has not yet fallen into disorder",
    "不要把角色动作句直接升格成场景主键。": "do not promote character action lines into permanent scene keys",
    "不要因为单镜头状态词就发明新的永久场景。": "do not invent a permanent scene from one shot-state phrase",
    "不要补写上游未给出的完整建筑考据。": "do not add unsupported architectural scholarship",
    "不要把整句背景句直接当作 scene name。": "do not treat a full background sentence as the scene name",
    "不要在没有证据时补充新建筑构件。": "do not invent new architectural components without evidence",
    "不要丢失门禁、边界和主通行线。": "do not lose gates, boundaries, or primary circulation",
    "世界/秩序建立": "world and order establishment",
    "心理恐怖": "psychological horror",
    "声音怪谈": "sound-driven urban haunting",
    "犯罪恐怖": "crime horror reveal",
    "出租屋": "old rental apartment",
    "旧出租屋": "old rental apartment",
    "窄床": "narrow bed",
    "床头墙": "bedhead wall",
    "卫生间门": "bathroom door",
    "卫生间": "bathroom",
    "洗手池": "washbasin",
    "水龙头": "faucet",
    "地砖": "floor tiles",
    "墙面": "wall surface",
    "空墙面": "blank wall",
    "门板": "door panel",
    "木门": "wooden door",
    "吊顶": "ceiling void",
    "吊顶缝": "ceiling gap",
    "吊顶裂口": "opened ceiling gap",
    "楼道": "apartment corridor",
    "警戒线": "police tape",
    "手机屏幕": "phone screen",
    "黑白线稿": "black-and-white line art",
    "墨影": "ink-shadow massing",
    "纸面颗粒": "paper-grain texture",
    "声效字": "sound-effect lettering",
    "冷硬灯光": "cold hard light",
    "大面积留黑": "large black negative space",
    "重复格": "repeated comic panels",
    "留白": "negative space",
    "空间压迫": "spatial compression",
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="从 `场景清单.json + 场景研究.json + scene_design_bridge.json` 生成场景设计稿。"
    )
    parser.add_argument("--catalog", required=True, help="场景清单.json 路径")
    parser.add_argument("--research", help="场景研究.json 路径；默认按清单目录自动推断")
    parser.add_argument("--bridge", help="scene_design_bridge.json 路径；默认按清单目录自动推断")
    parser.add_argument("--global-style", help="全局风格.md 路径；默认按项目根自动推断")
    parser.add_argument("--type-elements", dest="type_elements", help="全集类型元素.md 或分组类型元素.md 路径")
    parser.add_argument("--design-elements", dest="design_elements", help="导演意图.md 路径")
    parser.add_argument("--north-star", help="north_star.yaml 路径")
    parser.add_argument("--init-handoff", help="init_handoff.yaml 路径")
    parser.add_argument("--output-dir", help="输出目录；默认推断到 `projects/aigc/<项目名>/4-设计/`")
    parser.add_argument("--design-name", default="scene_design.json", help="设计 JSON 文件名")
    parser.add_argument("--manifest-name", default="_manifest.json", help="manifest 文件名")
    parser.add_argument("--scene-id", action="append", dest="scene_ids", help="只处理指定 scene_id，可重复传入")
    parser.add_argument("--scene-name", action="append", dest="scene_names", help="只处理指定 scene_name，可重复传入")
    parser.add_argument("--dry-run", action="store_true", help="只打印将生成的 manifest，不写文件")
    parser.add_argument("--skip-auto-image", action="store_true", help="只生成设计文件，不调用 内置 imagegen 自动生图")
    parser.add_argument("--auto-image-dry-run", action="store_true", help="写 manifest 并验证自动生图 payload，不真实请求 API")
    parser.add_argument("--auto-image-timeout", type=int, default=300, help="单个自动生图子进程最长等待秒数")
    parser.add_argument(
        "--allow-legacy-script-authorship",
        action="store_true",
        help="受控兼容模式：允许旧式脚本直接生成创作型场景设计内容。",
    )
    return parser.parse_args()


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


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


def read_text(path: Path | None) -> str:
    if path is None or not path.exists():
        return ""
    return path.read_text(encoding="utf-8")


def compact_text(text: Any, limit: int = 220) -> str:
    clean = re.sub(r"\s+", " ", str(text or "")).strip()
    if len(clean) <= limit:
        return clean
    cut = clean[: limit - 3].rstrip()
    boundary = cut.rfind(" ")
    if boundary > int(limit * 0.65):
        cut = cut[:boundary].rstrip()
    return cut + "..."


def to_repo_path(path: Path) -> str:
    try:
        return path.resolve().relative_to(Path.cwd().resolve()).as_posix()
    except ValueError:
        return path.as_posix()


def safe_filename(text: str) -> str:
    return re.sub(r"[\\\\/:*?\"<>|]+", "-", text).strip() or "unnamed"


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


def translate_fragment(text: Any) -> str:
    clean = str(text or "").strip()
    if clean in SCENE_NAME_TRANSLATIONS:
        return SCENE_NAME_TRANSLATIONS[clean]
    if clean in PHRASE_TRANSLATIONS:
        return PHRASE_TRANSLATIONS[clean]
    stripped = clean.strip(" 。；;，,")
    if stripped in SCENE_NAME_TRANSLATIONS:
        return SCENE_NAME_TRANSLATIONS[stripped]
    if stripped in PHRASE_TRANSLATIONS:
        return PHRASE_TRANSLATIONS[stripped]
    contains_map = [
        ("人物仍被池边日常空间包围", "characters remain surrounded by ordinary poolside space while the danger signal erupts in Lao Liu's hand"),
        ("人物关系处于短暂顺风状态", "the relationship is briefly moving smoothly against the absurd situation"),
        ("全息鱼", "holographic fish evidence contrasting with real fish"),
        ("广场中央忽然被扇形光柱占住", "a fan-shaped light beam suddenly occupies the plaza center and forces open ordinary daily space"),
        ("广场舞大妈群像", "the plaza-dance crowd becomes the background plane for an absurd misjudgment"),
        ("恒星强光", "stellar glare and slow rotating metal structures expand the plaza into cosmic scale"),
        ("深邃宇宙", "deep-space engineering context above the community plaza"),
        ("深空金属结构", "deep-space metal structures keep a calm engineering pressure above the frame"),
        ("木星工程背景", "Jupiter engineering backdrop and control panels form a calm technical background layer"),
        ("科技词汇和生活场景", "technological vocabulary deliberately contrasts with everyday community life"),
        ("锦鲤池和数据鱼保持可读", "the koi pond and data fish remain readable"),
        ("视觉中心从池景转向老刘手中的核桃", "the visual center shifts from the pond to the walnut in Lao Liu's hand"),
        ("静姐一侧仍靠着锦鲤池", "Jingjie's side remains anchored by the koi pond"),
        ("静姐背后仍是锦鲤池和整洁社区", "behind Jingjie remain the koi pond and tidy community"),
        ("池边环境仍稳定", "the poolside environment remains stable"),
        ("池边空间还没乱", "the poolside space has not yet fallen into disorder"),
    ]
    for needle, replacement in contains_map:
        if needle in clean:
            return replacement
    if NON_ASCII_RE.search(clean):
        return ""
    return clean


def translate_director_intent(text: str) -> str:
    clean = str(text or "").strip()
    if not clean:
        return "keep the scene readable before the technological interruption arrives"
    if "桃花源" in clean and "科技乌龙" in clean:
        return "establish a clean, believable morning order before the technological mishap intrudes"
    if "求偶表演" in clean and "笨拙试探" in clean:
        return "frame Lao Liu's courtship as a dignified but clumsy attempt, letting the gentle response hold warmth before the joke grows"
    if "张飞全息" in clean:
        return "let the Zhang Fei hologram strike the community order as the first heavy anomaly, then reveal shock and Lao Liu's embarrassment"
    if "围观感" in clean and "社死感" in clean:
        return "raise the public embarrassment and spectator pressure while keeping Jingjie's smile as both comic amplification and later emotional setup"
    if "木星来电" in clean:
        return "make the Jupiter call feel like a sudden scale-doubling rescue line, with engineering calm intensifying Lao Liu's awkward request for help"
    return english_fragment(clean, "keep the documented scene function readable without adding unsupported story events")


def translate_list(items: list[Any], *, fallback: str = "TBD", limit: int = 6) -> str:
    values = [translate_fragment(item) for item in items if str(item or "").strip()]
    values = [value for value in values if value and not NON_ASCII_RE.search(value)]
    return ", ".join(values[:limit]) if values else fallback


def english_fragment(value: Any, fallback: str) -> str:
    translated = translate_fragment(value)
    if not translated or translated == "TBD" or NON_ASCII_RE.search(translated):
        return fallback
    for source, replacement in (
        ("characters", "environmental story evidence"),
        ("character", "environmental story evidence"),
        ("crowd", "spatial pressure"),
        ("hand", "object anchor"),
        ("Lao Liu", "the documented story anchor"),
        ("Jingjie", "the documented story anchor"),
    ):
        translated = re.sub(rf"\b{re.escape(source)}\b", replacement, translated, flags=re.IGNORECASE)
    return translated


def fit_integrated_prompt(sentences: list[str]) -> str:
    prompt = " ".join(" ".join(sentence.split()) for sentence in sentences if sentence.strip())
    reinforcement = [
        "Keep every visible choice tied to the established story evidence, so the design reads as one integrated environment rather than a loose collage of motifs.",
        "Balance spatial clarity, material specificity, atmosphere, and camera logic in a single provider-ready image brief with no separate side instructions.",
        "Use the named structure, surface behavior, light direction, circulation, and negative guardrails as the only authority for what may appear in the frame.",
        "Preserve cinematic readability at first glance while leaving enough layered evidence for close inspection of architecture, object-scale cues, and technology.",
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


def translate_scene_name(scene_name: str, *, project_fallbacks: dict[str, Any] | None = None) -> str:
    registry_translation = nested_get(project_fallbacks, "scenes", "name_translations", scene_name, default="")
    if registry_translation:
        return registry_translation
    translated = SCENE_NAME_TRANSLATIONS.get(scene_name, "")
    if translated:
        return translated
    translated = translate_fragment(scene_name)
    if translated and not NON_ASCII_RE.search(translated):
        return translated.title()
    return scene_name.strip() or "Unnamed Scene"


def translate_global_style_prefix(style_text: str) -> str:
    source = compact_text(style_text, 260)
    if "侍魂天草降临" in source or "徐克1994香港武侠电影美学" in source or "和田惠美" in source:
        return (
            "A gothic-romantic wuxia environment language with 35mm film grain, soft halation, volumetric fog, "
            "wind pressure, lantern fire, damp practical surfaces, operatic spatial hierarchy, and practical smoke."
        )
    if "黑白恐怖漫画质感" in source and "声效节拍" in source:
        return (
            "A black-and-white psychological horror comic style with dense hand-drawn linework, "
            "ink-shadow layering, paper-grain texture, visible sound-effect rhythm, ordinary spaces "
            "turning uncanny, character reactions and negative space before explicit horror, and "
            "restrained treatment of corpse evidence."
        )
    if "近未来社区生活喜剧影视质感" in source and "轻量全息奇观" in source:
        return (
            "A near-future community-life comedy with cinematic realism, orderly lived-in spaces, "
            "soft atmospheric depth, gentle absurdist rhythm, and lightweight holographic spectacle "
            "that always serves the story dignity, loneliness, and clumsy romance."
        )
    if source:
        return "A grounded cinematic project style translated into clean English visual direction without copying named artists."
    return "Follow the established project visual style without inventing a new genre."


def infer_period_region(style_text: str) -> str:
    if "黑白恐怖漫画质感" in style_text or "出租屋" in style_text or "恐怖" in style_text:
        return "a contemporary old Chinese rental-apartment horror setting"
    if "近未来" in style_text or "全息" in style_text:
        return "a 2049 near-future Chinese community setting"
    if "武侠" in style_text or "海港" in style_text or "王府" in style_text:
        return "a historical East Asian port-city martial world"
    return "the documented project world"


def has_real_entries(items: list[Any]) -> bool:
    for item in items:
        text = str(item or "").strip()
        if text and text.lower() != "unknown":
            return True
    return False


def infer_scene_defaults(
    scene_name: str,
    anchors: list[Any],
    style_text: str,
    *,
    project_fallbacks: dict[str, Any] | None = None,
) -> dict[str, Any]:
    del style_text
    registry_defaults = nested_get(project_fallbacks, "scenes", "defaults_by_scene_name", scene_name, default={}) or {}
    if registry_defaults:
        return registry_defaults
    source = " ".join([scene_name, *[str(item) for item in anchors]])
    if "夜市" in source or "港" in source:
        return {
            "building_types": ["dockside night market"],
            "space_types": ["exterior trading space"],
            "materials": ["weathered timber", "damp stone pavement", "cloth awnings", "rope", "lantern hardware"],
            "topology": ["compressed harbor lanes", "stall fronts", "crowd-pressure chokepoints"],
            "time_light": ["night lantern light through sea fog", "warm firelight against damp haze"],
            "environment": ["sea wind", "damp haze", "lantern smoke"],
            "typology_reference": "Historical East Asian dockside night-market stalls, harbor lanes, timber awnings, damp stone paving, lantern strings, and pressure-filled chokepoints; use typology as reference, not a copied single location.",
            "style_detail": "Gothic-romantic wuxia realism with damp harbor air, lantern fire, salt haze, weathered wood, cloth canopies, and compressed pedestrian pressure.",
            "ornament_pattern": "Weathered signs, lantern strings, ropes, cloth canopies, and evidence-backed harbor-market details.",
            "fill_light": "soft bounce from lantern fire and damp ground surfaces",
            "back_light": "sea-fog glow and lantern rim light behind the architecture",
            "lighting_type": "cinematic practical lantern firelight with volumetric fog",
            "rhythm": "compressed nocturnal pressure before open violence",
            "momentum": "wind, haze, and blocked circulation held inside the market geometry before action breaks loose",
        }
    if "王府" in source or "回廊" in source:
        return {
            "building_types": ["palace corridor architecture"],
            "space_types": ["interior-exterior threshold space"],
            "materials": ["weathered timber", "stone paving", "lacquered beams", "screen-filtered lamplight"],
            "topology": ["layered corridor depth", "ceremonial thresholds", "column-framed circulation"],
            "time_light": ["lantern light through mist", "night palace glow"],
            "environment": ["incense haze", "still wind pressure", "damp night air"],
            "typology_reference": "Historical palace corridors, lacquered beams, stone thresholds, layered columns, and ritual circulation; use typology as reference, not a copied single location.",
            "style_detail": "Gothic-romantic wuxia realism with column rhythm, lacquered shadow, damp air, and ceremonial pressure held inside the corridor depth.",
            "ornament_pattern": "Restrained carved details, beams, screens, lantern glow, and evidence-backed ritual architecture.",
            "fill_light": "soft reflected lantern bounce from timber and stone surfaces",
            "back_light": "mist-softened lantern rim light through corridor depth",
            "lighting_type": "cinematic practical lantern light with volumetric haze",
            "rhythm": "suppressed ceremonial pressure before conflict breaks the etiquette shell",
            "momentum": "still architectural tension holding the frame before movement cuts through it",
        }
    if "税关" in source or "栈口" in source:
        return {
            "building_types": ["tax checkpoint architecture"],
            "space_types": ["guarded threshold exterior"],
            "materials": ["weathered timber", "rope barriers", "damp stone", "paper notices", "iron fittings"],
            "topology": ["narrow choke-point circulation", "checkpoint gates", "guard-facing frontage"],
            "time_light": ["hard lantern light in sea mist", "night checkpoint glow"],
            "environment": ["sea wind", "mist", "lantern smoke"],
            "typology_reference": "Historical dockside tax gates, timber barriers, rope lines, posted notices, and controlled chokepoints; use typology as reference, not a copied single location.",
            "style_detail": "Compressed wuxia realism with guarded thresholds, wind pressure, posted decrees, and rule-made violence visible in the architecture.",
            "ornament_pattern": "Timber barriers, rope lines, tax notices, seal marks, and evidence-backed checkpoint details.",
            "fill_light": "soft bounce from damp timber and stone",
            "back_light": "practical lantern edge light through sea mist",
            "lighting_type": "cinematic practical lantern light with damp volumetric haze",
            "rhythm": "contained checkpoint pressure before violence turns public",
            "momentum": "rule pressure, wind, and blocked circulation held inside the gate geometry",
        }
    return {
        "building_types": ["historical exterior setting"],
        "space_types": ["story-driven exterior environment"],
        "materials": ["weathered timber", "damp stone", "cloth surfaces", "rope and metal fittings"],
        "topology": ["readable exterior circulation", "pressure points", "story-facing boundaries"],
        "time_light": ["night practical light through fog"],
        "environment": ["wind", "damp haze", "practical smoke"],
        "typology_reference": "Historical East Asian exterior architecture with practical materials, readable thresholds, and story-driven circulation; use typology as reference, not a copied single location.",
        "style_detail": "Gothic-romantic wuxia realism with practical surfaces, damp air, and readable public pressure.",
        "ornament_pattern": "Evidence-backed architectural details, weathered fittings, and practical light sources.",
        "fill_light": "soft bounce from weathered practical surfaces",
        "back_light": "mist-softened practical edge light",
        "lighting_type": "cinematic practical light with volumetric haze",
        "rhythm": "held environmental pressure before action breaks loose",
        "momentum": "wind and circulation tension held inside the architecture before movement tears through it",
    }


def infer_project_root(catalog_path: Path) -> Path:
    resolved = catalog_path.resolve()
    for parent in resolved.parents:
        if parent.name == "5-设计":
            return parent.parent
    raise ValueError(f"无法从 catalog 路径推断项目根: {catalog_path}")


def infer_output_dir(catalog_path: Path) -> Path:
    return infer_project_root(catalog_path) / "5-设计"


def first_existing(*paths: Path) -> Path | None:
    for path in paths:
        if path.exists():
            return path
    return None


def select_scenes(scenes: list[dict[str, Any]], scene_ids: list[str], scene_names: list[str]) -> list[dict[str, Any]]:
    if not scene_ids and not scene_names:
        return scenes
    id_set = {item for item in scene_ids if item}
    name_set = {item for item in scene_names if item}
    selected = []
    for scene in scenes:
        if id_set and str(scene.get("scene_id", "")) in id_set:
            selected.append(scene)
            continue
        if name_set and str(scene.get("scene_name", "")) in name_set:
            selected.append(scene)
    return selected


def lookup_scene(items: list[dict[str, Any]], scene_id: str, scene_name: str) -> dict[str, Any]:
    for item in items:
        if str(item.get("scene_id", "")) == scene_id:
            return item
    for item in items:
        if str(item.get("scene_name", "")) == scene_name:
            return item
    return {}


def scene_type_from_profile(detail_profile: dict[str, Any]) -> str:
    candidates = " ".join(str(item) for item in as_list(detail_profile.get("space_type_candidates")))
    if "室内" in candidates:
        return "interior"
    if "野外" in candidates or "景观" in candidates:
        return "wilderness"
    if "室外" in candidates or candidates:
        return "exterior"
    return "unknown"


def build_reasoning_pivot(
    scene_name: str,
    scene_name_en: str,
    scene_function: str,
    topology: list[Any],
    materials: list[Any],
    atmosphere: list[Any],
    director_intent: str,
) -> str:
    topology_en = translate_list(topology, fallback="a readable spatial layout", limit=3)
    materials_en = translate_list(materials, fallback="evidence-backed material surfaces", limit=3)
    atmosphere_en = translate_list(atmosphere, fallback="story-motivated atmosphere", limit=3)
    function_en = translate_fragment(scene_function) if scene_function else "story support"
    return (
        f"{scene_name_en} must turn the scene function ({function_en}) into a drawable space: "
        f"organize {topology_en}, keep {materials_en} visible, and let {atmosphere_en} guide light, "
        f"movement, and camera readability. Director intent: {translate_director_intent(director_intent)}."
    )


def build_prompt_integration(packet: dict[str, Any]) -> str:
    scene_name_en = packet["scene_name_en"]
    design = packet["structured_fields"]["scene_design"]
    camera = packet["structured_fields"]["cinematography"]
    period_region = english_fragment(design.get("period_region"), "the documented project world")
    negative = "; ".join(
        english_fragment(item, "avoid unsupported additions") for item in packet["negative_constraints"]
    )
    if not negative:
        negative = "do not invent unsupported architecture or props"
    function_attribute = english_fragment(design["function_attribute"], "the scene's documented story function")
    symbolic_design = english_fragment(design["symbolic_design"], "its documented symbolic design cue")
    material_detail = english_fragment(design["material_detail"], "the documented primary material system")
    color_theme = english_fragment(design["color_theme"], "the documented color strategy")
    atmosphere = english_fragment(design["atmosphere"], "the documented atmosphere")
    design_type = english_fragment(design["design_type"], "a documented scene type")
    spatial_layout = english_fragment(design["spatial_layout"], "the documented spatial layout")
    reasoning_pivot = english_fragment(packet["reasoning_pivot"], "the documented reasoning pivot")
    shot_size = english_fragment(camera["shot_size"], "the documented shot size")
    lens_type = english_fragment(camera["lens_type"], "the documented lens behavior")
    camera_angle = english_fragment(camera["camera_angle"], "the documented camera angle")
    composition_layout = english_fragment(camera["composition_layout"], "the documented composition layout")
    key_light = english_fragment(camera["key_light"], "the documented key light")
    fill_light = english_fragment(camera["fill_light"], "the documented fill light")
    back_light = english_fragment(camera["back_light"], "the documented back light")
    story_brief = (
        f"The scene establishes {function_attribute} through {symbolic_design}, "
        f"using {material_detail}, {color_theme}, and {atmosphere} as its main "
        "visual memory."
    )
    return fit_integrated_prompt([
        f"Create a 16:9 cinematic scene design image for {scene_name_en}, an empty environmental shot of a {design_type} in a "
        f"{period_region}.",
        "This is a scene reference image with no characters, no people, no crowds, no hands, and no performance action in frame.",
        f"Preserve the story premise as an integrated design brief: {story_brief}",
        f"Use the reasoning pivot to keep the space readable: {reasoning_pivot}.",
        f"Build the environment from {spatial_layout}, {material_detail}, and {color_theme}, making each surface and boundary support the same narrative function.",
        f"Keep anchors and symbolic cues visible through {symbolic_design}, but treat them as grounded scene evidence rather than decorative spectacle.",
        f"Stage the frame with {shot_size}, {lens_type}, {camera_angle}, and {composition_layout}, so the viewer understands depth, circulation, scale, and the story focus immediately.",
        f"Lighting should use {key_light} with {fill_light} and {back_light}, maintaining {atmosphere} while preserving readable environmental edges and spatial hierarchy.",
        f"Integrate architectural structure, material wear, atmosphere, camera direction, and negative constraints into one coherent provider-ready prompt for a single image.",
        f"Guardrails: {negative}; keep the image empty of any role subject so it can be reused as a clean environment reference.",
    ])


def build_full_prompt(global_style_prefix: str, prompt_integration: str) -> str:
    return f"Global style prefix: {global_style_prefix.strip()}\n\nIntegrated prompt: {prompt_integration.strip()}"


def render_template(values: dict[str, Any]) -> str:
    rendered = TEMPLATE_PATH.read_text(encoding="utf-8")
    for key, value in values.items():
        rendered = rendered.replace(f"[{key}]", str(value or "TBD"))
    return rendered.rstrip() + "\n"


def build_packet(
    scene: dict[str, Any],
    *,
    research_item: dict[str, Any],
    bridge_item: dict[str, Any],
    global_style_text: str,
    type_elements_text: str,
    design_elements_text: str,
    north_star_text: str,
    init_handoff_text: str,
    project_fallbacks: dict[str, Any] | None = None,
) -> dict[str, Any]:
    del type_elements_text, design_elements_text, north_star_text, init_handoff_text
    scene_id = str(scene.get("scene_id", "scene"))
    scene_name = str(scene.get("scene_name", "unnamed_scene"))
    scene_name_en = translate_scene_name(scene_name, project_fallbacks=project_fallbacks)
    period_region = infer_period_region(global_style_text)
    design_context = scene.get("design_context", {})
    research_context = research_item or {}
    bridge_profile = first_non_empty(
        bridge_item.get("design_bridge_profile"),
        design_context.get("design_handoff"),
        {},
    ) or {}
    detail_profile = first_non_empty(
        research_context.get("detail_profile"),
        design_context.get("detail_profile"),
        {},
    ) or {}
    scene_blueprint = first_non_empty(
        research_context.get("scene_blueprint"),
        design_context.get("scene_blueprint"),
        {},
    ) or {}
    fixed_anchor = first_non_empty(
        bridge_profile.get("fixed_anchor_bridge"),
        scene_blueprint.get("fixed_anchor_layer"),
        {},
    ) or {}
    variable_state = first_non_empty(
        bridge_profile.get("variable_state_bridge"),
        scene_blueprint.get("variable_state_layer"),
        {},
    ) or {}
    narrative_layer = first_non_empty(scene_blueprint.get("narrative_layer"), {}) or {}
    bible_card = first_non_empty(
        bridge_item.get("scene_bible_card"),
        research_context.get("scene_bible_card"),
        design_context.get("scene_bible_card"),
        {},
    ) or {}
    world_rule = first_non_empty(
        research_context.get("world_rule_profile"),
        design_context.get("world_rule_profile"),
        {},
    ) or {}

    materials = as_list(first_non_empty(fixed_anchor.get("material_candidates"), detail_profile.get("material_candidates")))
    palette = as_list(first_non_empty(fixed_anchor.get("palette_candidates"), detail_profile.get("palette_candidates")))
    topology = as_list(first_non_empty(fixed_anchor.get("topology_candidates"), detail_profile.get("topology_candidates")))
    anchors = as_list(first_non_empty(fixed_anchor.get("must_show_anchors"), detail_profile.get("must_show_anchors"), [scene_name]))
    time_light = as_list(first_non_empty(variable_state.get("time_light_cues"), detail_profile.get("time_light_cues")))
    environment = as_list(first_non_empty(variable_state.get("environment_cues"), detail_profile.get("environment_cues")))
    space_types = as_list(detail_profile.get("space_type_candidates"))
    building_types = as_list(detail_profile.get("building_type_candidates"))
    defaults = infer_scene_defaults(scene_name, anchors, global_style_text, project_fallbacks=project_fallbacks)
    if not has_real_entries(materials):
        materials = defaults["materials"]
    if not has_real_entries(palette):
        palette = ["warm gold-red", "cool cyan-gray"]
    if not has_real_entries(topology):
        topology = defaults["topology"]
    if not has_real_entries(time_light):
        time_light = defaults["time_light"]
    if not has_real_entries(environment):
        environment = defaults["environment"]
    if not has_real_entries(space_types):
        space_types = defaults["space_types"]
    if not has_real_entries(building_types):
        building_types = defaults["building_types"]
    scene_function = str(first_non_empty(narrative_layer.get("scene_function"), bible_card.get("dramatic_function"), "story support"))
    director_intent = str(first_non_empty(world_rule.get("director_intent_anchor"), ""))
    scene_type = str(scene.get("scene_type") or scene_type_from_profile(detail_profile))
    style_backbone = extract_global_style_prefix(global_style_text) or compact_text(global_style_text, 220)
    global_style_prefix_en = translate_global_style_prefix(style_backbone)
    story_premise = str(first_non_empty(research_context.get("compendium"), design_context.get("compendium"), bible_card.get("summary")))
    negative_constraints = as_list(
        first_non_empty(
            bridge_profile.get("negative_constraints"),
            world_rule.get("negative_constraints"),
            design_context.get("design_handoff", {}).get("negative_constraints"),
        )
    )
    reasoning_pivot = build_reasoning_pivot(
        scene_name,
        scene_name_en,
        scene_function,
        topology,
        materials,
        environment or time_light,
        director_intent,
    )

    scene_design = {
        "style_backbone": style_backbone,
        "design_type": translate_list([*building_types, *space_types], fallback=scene_type, limit=3),
        "master_typology_reference": defaults["typology_reference"],
        "concept_translation": (
            f"{scene_name_en} translates {translate_fragment(scene_function)} into a stable spatial anchor for "
            f"{translate_list(anchors, fallback=scene_name, limit=4)}."
        ),
        "style_detail": defaults["style_detail"],
        "period_region": period_region,
        "function_attribute": translate_fragment(scene_function),
        "spatial_layout": translate_list(topology, fallback="readable open layout"),
        "space_type": translate_list(space_types, fallback=scene_type),
        "material_detail": translate_list(materials, fallback="evidence-backed practical surfaces"),
        "structural_detail": (
            f"Keep the main anchor layer ({translate_list(anchors, fallback=scene_name, limit=4)}) fixed, "
            f"with clear boundaries, access routes, and scale references."
        ),
        "circulation": (
            "Circulation remains legible around the main anchor; no implied role movement should erase the "
            "primary boundary or passage logic."
        ),
        "color_theme": translate_list(palette, fallback=translate_fragment(world_rule.get("style_anchor", "")) or "project-neutral warm-cool balance"),
        "symbolic_design": translate_list(anchors, fallback=scene_name),
        "ornament_pattern": defaults["ornament_pattern"],
        "lighting_design": "N/A - exterior or hybrid scene; use story-motivated environmental light.",
        "lamp_design": "N/A - do not invent interior fixtures without upstream evidence.",
        "furniture_design": "N/A unless upstream evidence explicitly requires community seating or service furniture.",
        "wall_decor": "N/A - no unsupported interior wall decor.",
        "floor_material": translate_list(materials, fallback="practical public-space ground surface", limit=2),
        "ecology_design": translate_list(environment, fallback="clean community air and stable public order"),
        "water_design": "Use visible water or wet-surface logic only when the scene evidence contains pool-edge or koi-pond cues.",
        "art_installation": "Keep secondary set dressing grounded in evidence-backed harbor, checkpoint, or palace details rather than speculative spectacle.",
        "atmosphere": translate_list([*environment, *time_light], fallback="story-motivated atmosphere"),
        "weather": "Clean, low-pressure community air unless the episode evidence says otherwise.",
        "season_time": translate_list(time_light, fallback="story-motivated time of day"),
    }
    cinematography = {
        "shot_size": "wide establishing design frame with readable architectural scale",
        "lens_type": "35mm equivalent, low distortion, cinematic realism",
        "camera_angle": "eye-level or slightly elevated observational angle",
        "composition_layout": "16:9 layered scene sheet: foreground circulation, middle-ground anchor, readable background context",
        "composition_method": "stable center-and-edge hierarchy with clean empty negative space",
        "shape_sense": "open geometric order softened by lived-in community details",
        "line_sense": "clean public-space lines, readable access paths, no arbitrary visual clutter",
        "tonal_sense": translate_list(palette, fallback="balanced warm-cool tonal structure", limit=3),
        "focus_sense": "deep enough focus to preserve spatial layout and anchor continuity",
        "rhythm_sense": defaults["rhythm"],
        "texture_sense": translate_list(materials, fallback="weathered practical surfaces with readable age and damp air response", limit=3),
        "momentum": defaults["momentum"],
        "key_light": translate_list(time_light, fallback="soft story-motivated daylight", limit=2),
        "fill_light": defaults["fill_light"],
        "back_light": defaults["back_light"],
        "lighting_type": defaults["lighting_type"],
        "color_hue": translate_list(palette, fallback="project-balanced hue range", limit=3),
        "color_value": "clean mid-to-high value range with readable public-space contrast",
        "color_saturation": "controlled, atmospheric, and never synthetic-neon",
        "color_temperature": "lantern-warm against fog-cool contrast",
        "color_psychology": "pressure, weather, ritual, and public danger held inside one readable environment",
        "camera_model": "cinematic digital camera emulation",
        "aperture": "f/5.6 to f/8 design-sheet clarity",
        "shutter": "1/125s still-frame equivalent",
        "iso": "ISO 200-400 clean image",
        "focal_length": "35mm equivalent",
        "resolution": "16:9 high-resolution scene concept",
    }
    packet = {
        "scene_id": scene_id,
        "scene_name": scene_name,
        "scene_name_en": scene_name_en,
        "scene_type": scene_type,
        "story_premise": story_premise,
        "compendium": story_premise,
        "reasoning_pivot": reasoning_pivot,
        "style_backbone": style_backbone,
        "scene_style": scene_design["style_detail"],
        "direction_anchor": director_intent or bible_card.get("continuity_guard", ""),
        "negative_guardrails": negative_constraints,
        "negative_constraints": negative_constraints,
        "global_style_prefix": style_backbone,
        "global_style_prefix_en": global_style_prefix_en,
        "structured_fields": {
            "scene_design": scene_design,
            "cinematography": cinematography,
            "reference": anchors,
            "concept_translation": scene_design["concept_translation"],
            "cultural_elements": {
                "symbolic_design": scene_design["symbolic_design"],
                "ornament_pattern": scene_design["ornament_pattern"],
            },
            "structure": topology,
            "layout": scene_design["spatial_layout"],
            "circulation": scene_design["circulation"],
            "materials": materials,
            "accessories": [],
            "ecology": environment,
            "atmosphere": [*environment, *time_light],
            "composition": cinematography["composition_layout"],
            "camera": cinematography,
            "negative_constraints": negative_constraints,
        },
        "quality_flags": list(as_list(bridge_profile.get("quality_flags"))),
        "source_trace": {
            "catalog_status": "present",
            "research_status": "present" if research_item else "research_degraded",
            "bridge_status": "present" if bridge_item else "bridge_degraded",
            "global_status": "present" if style_backbone else "global_style_degraded",
        },
    }
    packet["prompt_integration"] = build_prompt_integration(packet)
    packet["design_prompt"] = packet["prompt_integration"]
    packet["prompt"] = packet["design_prompt"]
    packet["full_generation_prompt"] = build_full_prompt(packet["global_style_prefix_en"], packet["prompt_integration"])
    packet["final_prompt"] = packet["full_generation_prompt"]
    return packet


def find_packet_placeholders(packet: dict[str, Any]) -> list[str]:
    issues: list[str] = []
    serialized = json.dumps(packet, ensure_ascii=False)
    for token in PLACEHOLDER_PATTERNS:
        if token in serialized:
            issues.append(token)
    if re.search(r"\bunknown\b", serialized):
        issues.append("unknown")
    return sorted(set(issues))


def build_markdown_card(packet: dict[str, Any]) -> str:
    scene_design = packet["structured_fields"]["scene_design"]
    cinematography = packet["structured_fields"]["cinematography"]
    values = {
        "scene_name_en": packet["scene_name_en"],
        "story_narrative": packet["story_premise"],
        "reasoning_pivot_en": packet["reasoning_pivot"],
        "style_backbone": packet["style_backbone"],
        "design_type_en": scene_design["design_type"],
        "design_master_prompt": scene_design["master_typology_reference"],
        "design_concept_prompt": scene_design["concept_translation"],
        "scene_style_prompt": scene_design["style_detail"],
        "period_region_en": scene_design["period_region"],
        "function_attribute_en": scene_design["function_attribute"],
        "space_layout_en": scene_design["spatial_layout"],
        "space_type_en": scene_design["space_type"],
        "material_detail_en": scene_design["material_detail"],
        "structural_detail_en": scene_design["structural_detail"],
        "circulation_en": scene_design["circulation"],
        "color_theme_en": scene_design["color_theme"],
        "symbolic_design_en": scene_design["symbolic_design"],
        "ornament_pattern_en": scene_design["ornament_pattern"],
        "lighting_design_en": scene_design["lighting_design"],
        "lamp_design_en": scene_design["lamp_design"],
        "furniture_design_en": scene_design["furniture_design"],
        "wall_decor_en": scene_design["wall_decor"],
        "floor_material_en": scene_design["floor_material"],
        "ecology_design_en": scene_design["ecology_design"],
        "water_design_en": scene_design["water_design"],
        "art_installation_en": scene_design["art_installation"],
        "atmosphere_en": scene_design["atmosphere"],
        "weather_en": scene_design["weather"],
        "season_time_en": scene_design["season_time"],
        "photo_shot_size_en": cinematography["shot_size"],
        "lens_type_en": cinematography["lens_type"],
        "camera_angle_en": cinematography["camera_angle"],
        "composition_layout_en": cinematography["composition_layout"],
        "composition_method_en": cinematography["composition_method"],
        "shape_sense_en": cinematography["shape_sense"],
        "line_sense_en": cinematography["line_sense"],
        "tonal_sense_en": cinematography["tonal_sense"],
        "focus_sense_en": cinematography["focus_sense"],
        "rhythm_sense_en": cinematography["rhythm_sense"],
        "texture_sense_en": cinematography["texture_sense"],
        "momentum_en": cinematography["momentum"],
        "main_light_en": cinematography["key_light"],
        "fill_light_en": cinematography["fill_light"],
        "back_light_en": cinematography["back_light"],
        "lighting_type_en": cinematography["lighting_type"],
        "color_hue_en": cinematography["color_hue"],
        "color_value_en": cinematography["color_value"],
        "color_saturation_en": cinematography["color_saturation"],
        "color_temperature_en": cinematography["color_temperature"],
        "color_psychology_en": cinematography["color_psychology"],
        "camera_model_en": cinematography["camera_model"],
        "aperture_en": cinematography["aperture"],
        "shutter_en": cinematography["shutter"],
        "iso_en": cinematography["iso"],
        "focal_length_en": cinematography["focal_length"],
        "resolution_en": cinematography["resolution"],
        "global_style_prefix": packet["global_style_prefix_en"],
        "prompt_integration": packet["prompt_integration"],
    }
    return render_template(values)


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


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

    research_path = Path(args.research) if args.research else episode_dir / "场景研究.json"
    bridge_path = Path(args.bridge) if args.bridge else episode_dir / "scene_design_bridge.json"
    global_style_path = (
        Path(args.global_style)
        if args.global_style
        else first_existing(
            project_root / "2-Global" / "全局风格.md",
            project_root / "2-Global" / "全局风格" / "全局风格设计.md",
        )
    )
    type_elements_path = (
        Path(args.type_elements)
        if args.type_elements
        else first_existing(
            project_root / "2-Global" / "全集类型元素.md",
            project_root / "2-Global" / "类型元素" / "全集设计.md",
            project_root / "2-Global" / "类型元素.md",
        )
    )
    design_elements_path = (
        Path(args.design_elements)
        if args.design_elements
        else first_existing(
            project_root / "2-Global" / "导演意图.md",
            project_root / "2-Global" / "设计元素" / "设计元素.md",
        )
    )
    north_star_path = Path(args.north_star) if args.north_star else project_root / "0-Init" / "north_star.yaml"
    init_handoff_path = Path(args.init_handoff) if args.init_handoff else project_root / "0-Init" / "init_handoff.yaml"

    catalog = read_json(catalog_path)
    scenes = catalog.get("scenes", [])
    selected = select_scenes(scenes, args.scene_ids or [], args.scene_names or [])
    if not selected:
        print("[ERROR] 过滤后没有命中任何 scene。", file=sys.stderr)
        return 1

    research = read_json(research_path) if research_path.exists() else {}
    bridge = read_json(bridge_path) if bridge_path.exists() else {}
    research_scenes = research.get("scenes", [])
    bridge_scenes = bridge.get("scenes", [])

    packets = [
        build_packet(
            scene,
            research_item=lookup_scene(research_scenes, str(scene.get("scene_id", "")), str(scene.get("scene_name", ""))),
            bridge_item=lookup_scene(bridge_scenes, str(scene.get("scene_id", "")), str(scene.get("scene_name", ""))),
            global_style_text=read_text(global_style_path),
            type_elements_text=read_text(type_elements_path),
            design_elements_text=read_text(design_elements_path),
            north_star_text=read_text(north_star_path),
            init_handoff_text=read_text(init_handoff_path),
            project_fallbacks=project_fallbacks,
        )
        for scene in selected
    ]
    packet_issues = {
        packet["scene_name"]: find_packet_placeholders(packet)
        for packet in packets
    }
    packet_issues = {name: issues for name, issues in packet_issues.items() if issues}
    if packet_issues:
        print(
            "[ERROR] 场景设计包仍含占位或错域回退，已阻止继续落盘: "
            + json.dumps(packet_issues, ensure_ascii=False),
            file=sys.stderr,
        )
        return 1

    generated_at = datetime.now().isoformat(timespec="seconds")
    output_dir_repo = to_repo_path(output_dir)
    source_inputs = [to_repo_path(catalog_path)]
    for path in (research_path, bridge_path, global_style_path, type_elements_path, design_elements_path, north_star_path, init_handoff_path):
        if path and path.exists():
            source_inputs.append(to_repo_path(path))

    design_payload = {
        "meta": {
            "schema_version": "aigc/design-scene-design/v2",
            "skill_id": "aigc-design-scene",
            "project_name": project_name,
            "episode_id": episode_id,
            "primary_input": to_repo_path(catalog_path),
            "source_inputs": source_inputs,
            "template": to_repo_path(TEMPLATE_PATH),
            "generated_at": generated_at,
            "markdown_projection_template_bound": True,
        },
        "scenes": [],
    }
    manifest = {
        "status": "ok",
        "domain": "场景",
        "episode_id": episode_id,
        "inputs": source_inputs,
        "outputs": {
            "design_truth": f"{output_dir_repo}/{args.design_name}",
            "markdown_files": [],
        },
        "statistics": {"scene_count": len(packets)},
        "template_validation": {
            "template": to_repo_path(TEMPLATE_PATH),
            "required_sections": [
                "**物语**",
                "**解构**",
                "Reasoning Pivot:",
                "## Scene Design ##",
                "## Cinematography ##",
                "**prompt整合**",
            ],
            "status": "pending_validation",
        },
        "auto_image": {
            "provider_skill": "imagegen",
            "provider_mode": "built-in image_gen",
            "default_model": "GPT-IMAGE-2",
            "mode": "single-subject-t2i",
            "prompt_field": "full_generation_prompt",
            "output_dir_policy": "same_directory_as_design_file",
            "filename_policy": "same_stem_as_design_file",
            "status": "not_run_in_template_repair",
            "image_paths": [],
        },
    }

    for packet in packets:
        markdown_name = f"{safe_filename(packet['scene_name'])}.md"
        markdown_path = output_dir / markdown_name
        markdown_repo = f"{output_dir_repo}/{markdown_name}"
        packet_for_json = dict(packet)
        packet_for_json["markdown_path"] = markdown_repo
        design_payload["scenes"].append(packet_for_json)
        manifest["outputs"]["markdown_files"].append(markdown_repo)
        if not args.dry_run:
            output_dir.mkdir(parents=True, exist_ok=True)
            markdown_path.write_text(build_markdown_card(packet), encoding="utf-8")

    if args.dry_run:
        print(json.dumps(manifest, ensure_ascii=False, indent=2))
        return 0

    write_json(output_dir / args.design_name, design_payload)
    manifest["template_validation"]["status"] = "generated_unvalidated"
    write_json(output_dir / args.manifest_name, manifest)
    if not args.skip_auto_image:
        auto_status = run_auto_image_guard(
            output_dir=output_dir,
            project_name=project_name,
            global_style_path=global_style_path,
            manifest_name=args.manifest_name,
            timeout=args.auto_image_timeout,
            generation_dry_run=args.auto_image_dry_run,
        )
        if auto_status != 0:
            return auto_status
    print(f"[OK] wrote {len(packets)} scene designs to {output_dir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
