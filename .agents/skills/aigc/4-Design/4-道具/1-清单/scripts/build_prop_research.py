#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Build prop research and design bridge outputs from prop catalog JSON."""

from __future__ import annotations

import argparse
import json
import re
import sys
from collections import Counter
from datetime import datetime
from pathlib import Path
from typing import Dict, Iterable, List, Sequence, Tuple


MATERIAL_MAP: Dict[str, Sequence[str]] = {
    "metal": ("金", "银", "铜", "铁", "钢", "刃", "锁链", "甲"),
    "wood": ("木", "竹", "门板", "车轮", "车厢", "箱", "匣"),
    "jade_or_stone": ("玉", "石", "玛瑙", "宝石"),
    "paper_or_silk": ("纸", "文书", "书卷", "密信", "卷轴", "帛"),
    "textile": ("帘", "帐", "袍", "衣", "穗", "绳", "缎", "绸"),
    "leather": ("鞘", "囊", "鞭", "革", "皮"),
    "ceramic": ("盏", "壶", "瓶", "碗", "瓷", "陶"),
}

MATERIAL_LABELS = {
    "metal": "金属",
    "wood": "木质",
    "jade_or_stone": "玉石",
    "paper_or_silk": "纸绢",
    "textile": "织物",
    "leather": "皮革",
    "ceramic": "陶瓷",
    "mixed": "复合材",
}

CRAFT_MAP: Dict[str, Sequence[str]] = {
    "forged": ("锻", "铸", "刀", "剑", "枪", "链"),
    "carved": ("雕", "刻", "纹", "浮雕"),
    "assembled": ("门闩", "门板", "车轮", "铰链", "锁芯", "框"),
    "embroidered": ("绣", "缂", "织", "帘", "穗"),
    "sealed_document": ("封缄", "钤印", "印", "文书", "军报", "密信"),
}

CRAFT_LABELS = {
    "forged": "锻造",
    "carved": "雕刻",
    "assembled": "框架装配",
    "embroidered": "织绣",
    "sealed_document": "文书制式",
    "general_fabrication": "常规制作",
}

FUNCTION_MAP: Dict[str, Sequence[str]] = {
    "authority": ("令牌", "腰牌", "印", "军报", "文书"),
    "combat_or_restraint": ("刀", "剑", "枪", "链", "鞭", "甲", "牢"),
    "transport_or_space": ("囚车", "马车", "门", "栏", "帐帘", "箱"),
    "illumination": ("火把", "灯笼", "提灯", "烛台"),
    "token_or_memory": ("玉佩", "簪", "扇", "镜", "梳", "密信"),
}

FUNCTION_LABELS = {
    "authority": "权力凭证",
    "combat_or_restraint": "压迫/限制",
    "transport_or_space": "空间/承载",
    "illumination": "照明引导",
    "token_or_memory": "信物/记忆",
    "story_support": "剧情提示",
}

SHOT_ROUTE_MAP: Sequence[Tuple[str, Sequence[str], dict]] = (
    (
        "macro",
        ("令牌", "腰牌", "玉佩", "印", "钥匙", "密信", "文书"),
        {
            "shot_size": "macro close-up",
            "camera_angle": "three-quarter macro",
            "focal_length": "85-100mm",
            "lighting": "controlled rim light with soft fill",
        },
    ),
    (
        "profile",
        ("刀", "剑", "枪", "鞭", "火把"),
        {
            "shot_size": "hero profile",
            "camera_angle": "low three-quarter",
            "focal_length": "50-85mm",
            "lighting": "hard edge light with low-key side fill",
        },
    ),
    (
        "environmental",
        ("门", "栏", "囚车", "马车", "帐帘", "箱", "炉"),
        {
            "shot_size": "environmental wide",
            "camera_angle": "low-angle environmental",
            "focal_length": "28-35mm",
            "lighting": "motivated side light with depth haze",
        },
    ),
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="从道具清单 JSON 生成道具研究与设计桥接 JSON。")
    parser.add_argument("--input", required=True, help="输入 `道具清单.json`")
    parser.add_argument("--output-dir", required=True, help="输出目录")
    parser.add_argument("--research-name", default="道具研究.json", help="研究 JSON 文件名")
    parser.add_argument("--bridge-name", default="prop_design_bridge.json", help="桥接 JSON 文件名")
    parser.add_argument("--dry-run", action="store_true", help="只做解析校验，不写文件")
    return parser.parse_args()


def read_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, payload: dict) -> None:
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def unique_preserve(items: Iterable[str]) -> List[str]:
    seen = set()
    output: List[str] = []
    for item in items:
        if not item or item in seen:
            continue
        seen.add(item)
        output.append(item)
    return output


def index_groups_by_id(episode_payload: dict) -> Dict[str, dict]:
    groups = episode_payload.get("final_output", {}).get("main_content", {}).get("分镜组列表", [])
    return {str(group.get("分镜组ID", "unknown")): group for group in groups if isinstance(group, dict)}


def score_labels(text: str, mapping: Dict[str, Sequence[str]], default: str) -> List[str]:
    counter = Counter()
    for label, keywords in mapping.items():
        for keyword in keywords:
            if keyword and keyword in text:
                counter[label] += max(1, len(keyword) // 2)
    if not counter:
        return [default]
    return [item for item, _count in counter.most_common(2)]


def infer_scale(prop_name: str) -> str:
    if any(token in prop_name for token in ("门", "栏", "车", "帐", "箱", "炉")):
        return "large_set_prop"
    if any(token in prop_name for token in ("刀", "剑", "枪", "鞭", "火把")):
        return "mid_handheld_prop"
    if any(token in prop_name for token in ("令牌", "印", "玉佩", "簪", "钥匙", "密信")):
        return "small_hero_prop"
    return "general_handheld_prop"


def infer_physical_character(prop_name: str, materials: Sequence[str], states: Sequence[str]) -> dict:
    material = materials[0] if materials else "mixed"
    state_text = " / ".join([item for item in states if item and item != "unknown"]) or "状态稳定"

    if any(token in prop_name for token in ("门", "栏", "车", "箱", "炉")):
        mass_impression = "沉重厚实"
        proportion_signature = "体块先行，纵横比例以稳定承重为主"
        cross_section = "厚板或框架型截面"
        force_logic = "重心下沉，以承载和阻隔为主"
        volume_density = "大体量、致密结构"
    elif any(token in prop_name for token in ("刀", "剑", "枪", "鞭", "火把")):
        mass_impression = "均衡或前重"
        proportion_signature = "长向轮廓显著，握持段与功能端有明显比例差"
        cross_section = "楔形或杆状截面"
        force_logic = "强调挥动、刺击或压迫性动作"
        volume_density = "中等体量、重心明确"
    else:
        mass_impression = "轻巧但有存在感"
        proportion_signature = "便携尺度，轮廓依赖边缘和局部装饰识别"
        cross_section = "薄片、牌状或小型立体截面"
        force_logic = "以递交、佩戴、展示或藏匿为主"
        volume_density = "小体量、局部细节密集"

    surface_temperament_map = {
        "metal": "冷硬金属反光与边角磨痕并存",
        "wood": "木纤维与使用磨痕明显",
        "jade_or_stone": "表面温润但边口偏硬",
        "paper_or_silk": "薄、脆、易折且边缘容易起皱",
        "textile": "柔软垂坠，边缘与褶皱决定质感",
        "leather": "韧性包裹感强，折痕和磨损容易出戏",
        "ceramic": "硬脆且表面反光集中",
        "mixed": "复合材质，主次表面必须分明",
    }

    return {
        "mass_impression": mass_impression,
        "proportion_signature": proportion_signature,
        "cross_section": cross_section,
        "surface_temperament": surface_temperament_map.get(material, surface_temperament_map["mixed"]),
        "force_logic": force_logic,
        "volume_density": volume_density,
        "state_anchor": state_text,
    }


def infer_shot_route(prop_name: str) -> dict:
    for route_name, keywords, payload in SHOT_ROUTE_MAP:
        if any(keyword in prop_name for keyword in keywords):
            return {
                "route_type": route_name,
                **payload,
            }
    return {
        "route_type": "standard",
        "shot_size": "medium hero shot",
        "camera_angle": "eye-level three-quarter",
        "focal_length": "50mm",
        "lighting": "story-motivated key light with readable edge separation",
    }


def compose_analysis_text(prop: dict, rows: Sequence[dict], group_index: Dict[str, dict]) -> str:
    parts = [prop["canonical_name"], prop["canonical_name"]]
    for row in rows:
        if row.get("scene"):
            parts.append(str(row["scene"]))
        if row.get("roles"):
            parts.append(str(row["roles"]))
        if row.get("raw_prop_text"):
            parts.append(str(row["raw_prop_text"]))
        group = group_index.get(str(row.get("group_id", "")), {})
        script_text = str(group.get("剧本正文", "")).strip()
        if script_text:
            parts.append(script_text)
        group_design = group.get("组间设计", {})
        if isinstance(group_design, dict):
            parts.extend(
                [
                    str(group_design.get("全局风格", "")).strip(),
                    str(group_design.get("类型元素", "")).strip(),
                    str(group_design.get("导演意图", "")).strip(),
                ]
            )
        shot_list = group.get("分镜明细", [])
        for shot in shot_list:
            if str(shot.get("分镜ID", "")) != str(row.get("shot_id", "")):
                continue
            parts.extend(
                [
                    str(shot.get("场景及方位", "")).strip(),
                    str(shot.get("角色及站位和穿搭", "")).strip(),
                    str(shot.get("道具及状态", "")).strip(),
                    str(shot.get("分镜表现", "")).strip(),
                    str(shot.get("角色表现", "")).strip(),
                    str(shot.get("摄影美学", "")).strip(),
                ]
            )
            break
    return "\n".join([part for part in parts if part])


def build_evidence_ledger(prop: dict, rows: Sequence[dict]) -> List[dict]:
    evidence: List[dict] = []
    for row in rows:
        evidence.append(
            {
                "group_id": row.get("group_id", "unknown"),
                "shot_id": row.get("shot_id", "unknown"),
                "scene": row.get("scene", ""),
                "roles": row.get("roles", ""),
                "raw_prop_text": row.get("raw_prop_text", ""),
            }
        )
    return evidence


def build_display_profile(prop_name: str, materials: Sequence[str], functions: Sequence[str], states: Sequence[str]) -> dict:
    material_label = MATERIAL_LABELS.get(materials[0], materials[0] if materials else "复合材")
    function_label = FUNCTION_LABELS.get(functions[0], functions[0] if functions else "剧情提示")
    state_label = next((item for item in states if item and item != "unknown"), "状态稳定")
    return {
        "title": prop_name,
        "short_tagline": f"{function_label} / {material_label}",
        "description": f"{prop_name}当前最重要的可视信息不是抽象设定，而是“{state_label}”这一镜头状态与其{material_label}质地所形成的即时压迫感。",
        "visual_signature": f"设计时优先保留{prop_name}的轮廓、受力关系与{material_label}表面处理。",
        "dramatic_value": f"{prop_name}承担{function_label}提示，不应被画成无功能的背景摆件。",
    }


def compose_chronicle(prop_name: str, materials: Sequence[str], functions: Sequence[str], scenes: Sequence[str], states: Sequence[str]) -> str:
    material_label = MATERIAL_LABELS.get(materials[0], materials[0] if materials else "复合材")
    function_label = FUNCTION_LABELS.get(functions[0], functions[0] if functions else "剧情提示")
    scene_label = scenes[0] if scenes else "当前场景"
    state_label = next((item for item in states if item and item != "unknown"), "静置")
    text = (
        f"{prop_name}不是一件被随手摆在画面里的装饰物，它在{scene_label}里首先以“{state_label}”的状态闯入视线，"
        f"把{function_label}这层戏剧意图压进了镜头的呼吸里。它的主体质感更接近{material_label}，边口、握持处或受力位置都该留下清晰的使用痕迹，"
        f"让人一眼就能判断它经历过怎样的动作与磨耗。设计时不应只追求漂亮轮廓，而要让它带着重量、温度和旧痕，"
        f"像一个真正被人反复拿起、递交、挥动、阻隔或藏匿过的器物。"
    )
    text = re.sub(r"\s+", "", text)
    if len(text) < 150:
        text += "它的存在感来自功能、材质和状态三者同时成立，而不是单纯靠花纹或形容词撑住。"
    if len(text) > 300:
        text = text[:298] + "。"
    return text


def build_research_payload(catalog: dict) -> Tuple[dict, dict]:
    meta = dict(catalog.get("meta", {}))
    meta["generated_at"] = datetime.now().astimezone().isoformat(timespec="seconds")

    source_input = meta.get("source_input")
    episode_payload = read_json(Path(source_input)) if source_input and Path(source_input).exists() else {}
    group_index = index_groups_by_id(episode_payload)

    group_prop_rows = catalog.get("group_prop_map", [])
    props = catalog.get("props", [])

    research_props: List[dict] = []
    bridge_props: List[dict] = []

    for prop in props:
        prop_name = str(prop.get("canonical_name", "unknown"))
        rows = [
            row
            for row in group_prop_rows
            if any(
                isinstance(mention, dict) and str(mention.get("prop_name", "")) == prop_name
                for mention in row.get("prop_mentions", [])
            )
        ]
        analysis_text = compose_analysis_text(prop=prop, rows=rows, group_index=group_index)
        material_candidates = score_labels(analysis_text, MATERIAL_MAP, "mixed")
        craft_candidates = score_labels(analysis_text, CRAFT_MAP, "general_fabrication")
        function_candidates = score_labels(analysis_text, FUNCTION_MAP, "story_support")
        scenes = unique_preserve(prop.get("scene_anchors", []))
        states = unique_preserve(prop.get("state_variants", []))
        evidence_ledger = build_evidence_ledger(prop=prop, rows=rows)
        shot_route = infer_shot_route(prop_name)
        physical_character = infer_physical_character(
            prop_name=prop_name,
            materials=material_candidates,
            states=states,
        )
        display_profile = build_display_profile(
            prop_name=prop_name,
            materials=material_candidates,
            functions=function_candidates,
            states=states,
        )
        chronicle = compose_chronicle(
            prop_name=prop_name,
            materials=material_candidates,
            functions=function_candidates,
            scenes=scenes,
            states=states,
        )

        design_bridge_profile = {
            "structure_modules": [
                f"{prop_name}的主体轮廓",
                "功能端与握持/受力端的关系",
                "状态痕迹最明显的局部细节",
            ],
            "material_and_finish": [
                f"主材质优先按 {MATERIAL_LABELS.get(material_candidates[0], material_candidates[0])} 处理",
                f"表面工艺优先按 {CRAFT_LABELS.get(craft_candidates[0], craft_candidates[0])} 处理",
            ],
            "wear_marks": states if states else ["unknown"],
            "shot_route": shot_route,
            "physical_character": physical_character,
            "negative_constraints": [
                "不要把镜头状态词直接并入 canonical prop name",
                "不要补写上游证据里不存在的现代零件或多余装饰",
                "不要把道具画成纯背景纹样，必须保留功能逻辑",
            ],
            "prompt_anchor": (
                f"{prop_name} / material={MATERIAL_LABELS.get(material_candidates[0], material_candidates[0])} / "
                f"function={FUNCTION_LABELS.get(function_candidates[0], function_candidates[0])} / "
                f"route={shot_route['route_type']}"
            ),
        }

        research_props.append(
            {
                "prop_id": prop.get("prop_id", ""),
                "canonical_name": prop_name,
                "prop_type": prop.get("prop_type", "general_prop"),
                "evidence_ledger": evidence_ledger,
                "attribute_profile": {
                    "primary_functions": function_candidates,
                    "material_candidates": material_candidates,
                    "craft_candidates": craft_candidates,
                    "scale_hint": infer_scale(prop_name),
                },
                "scene_usage_profile": {
                    "group_ids": prop.get("group_ids", []),
                    "shot_ids": prop.get("shot_ids", []),
                    "scene_anchors": scenes,
                    "role_anchors": prop.get("role_anchors", []),
                    "state_variants": states,
                },
                "historical_cultural_profile": {
                    "period_confidence": "unknown_by_default",
                    "social_signal": function_candidates[0],
                    "design_warning": "时代与装饰细节应以后续项目设定补证，不在本层臆造。",
                },
                "design_bridge_profile": design_bridge_profile,
                "display_profile": display_profile,
                "chronicle": chronicle,
            }
        )

        bridge_props.append(
            {
                "prop_id": prop.get("prop_id", ""),
                "canonical_name": prop_name,
                "prop_type": prop.get("prop_type", "general_prop"),
                "prompt_anchor": design_bridge_profile["prompt_anchor"],
                "structure_modules": design_bridge_profile["structure_modules"],
                "material_and_finish": design_bridge_profile["material_and_finish"],
                "wear_marks": design_bridge_profile["wear_marks"],
                "shot_route": design_bridge_profile["shot_route"],
                "physical_character": design_bridge_profile["physical_character"],
                "negative_constraints": design_bridge_profile["negative_constraints"],
                "display_profile": display_profile,
            }
        )

    research = {
        "meta": meta,
        "props": research_props,
    }
    bridge = {
        "meta": meta,
        "props": bridge_props,
    }
    return research, bridge


def main() -> int:
    args = parse_args()
    input_path = Path(args.input)
    if not input_path.exists():
        print(f"[ERROR] 输入文件不存在: {input_path}", file=sys.stderr)
        return 1

    try:
        catalog = read_json(input_path)
        research, bridge = build_research_payload(catalog)
    except Exception as exc:  # noqa: BLE001
        print(f"[ERROR] {exc}", file=sys.stderr)
        return 1

    output_dir = Path(args.output_dir)
    research_path = output_dir / args.research_name
    bridge_path = output_dir / args.bridge_name

    if args.dry_run:
        print(
            "[DRY-RUN] "
            f"research_props={len(research['props'])} "
            f"research={research_path.as_posix()} "
            f"bridge={bridge_path.as_posix()}"
        )
        return 0

    output_dir.mkdir(parents=True, exist_ok=True)
    write_json(research_path, research)
    write_json(bridge_path, bridge)
    print(f"[OK] 写入道具研究: {research_path.as_posix()}")
    print(f"[OK] 写入道具桥接: {bridge_path.as_posix()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
