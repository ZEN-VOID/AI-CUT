#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Build scene research and bridge truth sources from the scene catalog."""

from __future__ import annotations

import argparse
import json
import re
import sys
from collections import Counter
from datetime import datetime
from pathlib import Path
from typing import Dict, Iterable, List, Sequence, Tuple


BUILDING_TYPE_MAP: Dict[str, Sequence[str]] = {
    "公共广场": ("广场", "平台", "社区中央"),
    "水景节点": ("锦鲤池", "池边", "池", "水景"),
    "交通过渡空间": ("步道", "走廊", "楼道", "楼梯间", "安全通道", "电梯", "轿厢", "门厅"),
    "住宅门禁空间": ("家门口", "玄关", "单元门", "门口"),
    "街巷商用空间": ("街道", "街口", "巷口", "店铺", "茶馆", "码头"),
    "礼制/大型建筑": ("大殿", "殿前", "长廊", "庭院", "院落"),
    "自然地貌": ("河岸", "河边", "江边", "江岸", "山路", "山道", "天台"),
}
SPACE_TYPE_MAP: Dict[str, Sequence[str]] = {
    "室内": ("电梯", "轿厢", "房间", "客厅", "厨房", "办公室", "实验室", "控制室", "门厅", "玄关"),
    "室外": ("广场", "池边", "步道", "街道", "街口", "巷口", "庭院", "院落", "码头", "天台"),
    "半开放": ("走廊", "楼道", "楼梯间", "安全通道", "门口", "殿前", "长廊"),
    "水域边界": ("锦鲤池", "池", "河岸", "河边", "江边", "江岸"),
}
MATERIAL_MAP: Dict[str, Sequence[str]] = {
    "混凝土/石材": ("广场", "台阶", "平台", "池边", "楼道", "长廊", "门厅"),
    "玻璃/投影介质": ("全息", "投影", "数据鱼", "屏幕", "穹顶"),
    "金属/工业部件": ("电梯", "轿厢", "按钮", "门禁", "护栏", "扶手"),
    "木构/旧建筑": ("庭院", "院落", "大殿", "长廊", "门扇"),
    "水体/湿面": ("池", "河", "江", "水景", "水面"),
}
PALETTE_MAP: Dict[str, Sequence[str]] = {
    "冷青灰": ("冷", "蓝", "青", "荧光", "晨光白金", "洁净空气"),
    "暖金红": ("暖", "金", "夕照", "火光", "门灯"),
    "清亮白金": ("白金", "晨光", "洁净", "轻亮", "明亮"),
    "高危红": ("红光", "警报", "危险", "失控"),
}
TOPOLOGY_MAP: Dict[str, Sequence[str]] = {
    "开敞中心": ("广场", "平台", "社区中央"),
    "线性通行": ("步道", "走廊", "楼道", "长廊", "山路"),
    "门禁收束": ("电梯", "单元门", "门口", "玄关", "安全通道"),
    "水岸/池缘边界": ("池边", "锦鲤池", "河岸", "江边"),
}
TIME_LIGHT_TERMS: Sequence[str] = (
    "清晨", "晨间", "白天", "黄昏", "入夜", "深夜", "晨光", "夕照", "红光", "冷光", "暖光",
)
ENVIRONMENT_TERMS: Sequence[str] = (
    "洁净空气", "警报", "失控", "危险", "潮湿", "风", "雨", "雾", "人流", "秩序", "震动",
)
ANCHOR_TERMS: Sequence[str] = (
    "广场", "锦鲤池", "池边", "步道", "走廊", "楼道", "楼梯间", "安全通道", "电梯", "轿厢",
    "门口", "单元门", "门厅", "玄关", "庭院", "院落", "大殿", "长廊", "街道", "码头", "河岸", "山路",
)
QUALITY_FIELD_LABELS = {
    "building_type_candidates": "建筑类型",
    "space_type_candidates": "空间类型",
    "material_candidates": "材质表面",
    "palette_candidates": "主色/色温",
    "topology_candidates": "空间拓扑",
    "must_show_anchors": "必须出镜锚点",
}
ENRICHMENT_ACTION_MAP = {
    "建筑类型": "补足空间所属类型，例如广场/门厅/走廊/池边/庭院等。",
    "空间类型": "补足室内/室外/半开放/水域边界等明确分类。",
    "材质表面": "补足地面、墙面、门禁或投影介质的材质信息。",
    "主色/色温": "补足主光源、色温或警报/晨光等色光线索。",
    "空间拓扑": "补足主通行线、中心区、边界区或门禁收束关系。",
    "必须出镜锚点": "至少保留 2 个不可删的场景视觉锚点。",
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="从 `场景清单.json` 生成 `场景研究.json` 与 `scene_design_bridge.json`。")
    parser.add_argument("--input", required=True, help="输入 场景清单.json")
    parser.add_argument("--output-dir", required=True, help="输出目录")
    parser.add_argument("--catalog-name", default="场景清单.json", help="场景清单文件名")
    parser.add_argument("--research-name", default="场景研究.json", help="场景研究文件名")
    parser.add_argument("--bridge-name", default="scene_design_bridge.json", help="场景桥接文件名")
    parser.add_argument("--dry-run", action="store_true", help="只校验，不写文件")
    return parser.parse_args()


def read_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, payload: dict) -> None:
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def unique_preserve(items: Iterable[str]) -> List[str]:
    seen = set()
    output: List[str] = []
    for item in items:
        if not item or item == "unknown" or item in seen:
            continue
        seen.add(item)
        output.append(item)
    return output


def known_or_unknown(items: Iterable[str], max_items: int | None = None) -> List[str]:
    values = unique_preserve(items)
    if max_items is not None:
        values = values[:max_items]
    return values or ["unknown"]


def score_labels(text: str, mapping: Dict[str, Sequence[str]]) -> List[str]:
    scores: List[Tuple[str, int]] = []
    for label, keywords in mapping.items():
        score = sum(1 for keyword in keywords if keyword and keyword in text)
        if score > 0:
            scores.append((label, score))
    scores.sort(key=lambda item: (-item[1], item[0]))
    return [label for label, _ in scores[:3]] or ["unknown"]


def collect_terms(text: str, terms: Sequence[str], max_items: int = 5) -> List[str]:
    hits = [term for term in terms if term in text]
    return known_or_unknown(hits, max_items=max_items)


def build_evidence_ledger(rows: Sequence[dict]) -> List[dict]:
    ledger: List[dict] = []
    for row in rows:
        ledger.append(
            {
                "group_id": row.get("group_id", ""),
                "shot_id": row.get("shot_id", ""),
                "role_background_face": row.get("role_background_face", ""),
                "shot_expression": row.get("shot_expression", ""),
                "cinematography": row.get("cinematography", ""),
                "director_intent": row.get("director_intent", ""),
                "time_range": row.get("time_range", {}),
            }
        )
    return ledger


def build_scene_bible_card(scene_name: str, detail_profile: dict, scene_function: str) -> dict:
    anchors = "、".join(detail_profile.get("must_show_anchors", ["unknown"])[:3])
    materials = "、".join(detail_profile.get("material_candidates", ["unknown"])[:2])
    palette = "、".join(detail_profile.get("palette_candidates", ["unknown"])[:2])
    return {
        "title": scene_name,
        "tagline": f"{scene_name} / {scene_function}",
        "summary": f"{scene_name}的设计重点是先锁住 {anchors}，再让 {materials} 与 {palette} 形成统一感知。",
        "visual_memory_points": detail_profile.get("must_show_anchors", ["unknown"]),
        "dramatic_function": scene_function,
        "continuity_guard": "同一场景复现时，优先保持主空间识别与门禁/边界关系稳定。",
    }


def compose_compendium(scene_name: str, detail_profile: dict, scene_function: str) -> str:
    anchors = "、".join(detail_profile.get("must_show_anchors", ["空间主锚点"])[:3])
    materials = "、".join(detail_profile.get("material_candidates", ["未知材质"])[:2])
    palette = "、".join(detail_profile.get("palette_candidates", ["未知色温"])[:2])
    topology = "、".join(detail_profile.get("topology_candidates", ["未知拓扑"])[:2])
    environment = "、".join(detail_profile.get("environment_cues", ["环境状态未明"])[:2])
    text = (
        f"走进{scene_name}，第一眼要先被{anchors}抓住，再感受到{materials}在空间表面留下的真实触感。"
        f"这个场景的主色与主光应稳定在{palette}一带，使人物一进入就知道自己处在怎样的空间秩序中。"
        f"它的布局更偏向{topology}，因此镜头和角色动线都不该任意漂移，而要围绕固定边界和主通行线组织。"
        f"环境层当前最值得保留的是{environment}，它决定这个场景在剧情里不是单纯背景，而是承担“{scene_function}”的叙事节点。"
    )
    return re.sub(r"\s+", "", text)


def build_display_profile(scene_name: str, scene_function: str, score: int) -> dict:
    return {
        "title": scene_name,
        "subtitle": f"{scene_function} / 具像化分 {score}",
        "summary": f"{scene_name}已折叠 research 与 bridge 信息，可直接作为场景设计输入根。",
        "tags": [scene_function, f"score-{score}"],
        "badges": ["scene-catalog", "design-context-folded"],
    }


def infer_scene_function(rows: Sequence[dict]) -> str:
    joined = " ".join(str(row.get("director_intent", "")) for row in rows)
    if any(keyword in joined for keyword in ("建立", "介绍", "立住")):
        return "世界/秩序建立"
    if any(keyword in joined for keyword in ("关系", "寒暄", "试探")):
        return "关系推进"
    if any(keyword in joined for keyword in ("危险", "失控", "转折", "警报")):
        return "危机转折"
    return "场景承接"


def build_detail_profile(scene: dict, rows: Sequence[dict]) -> dict:
    joined_text = " ".join(
        [
            scene.get("scene_name", ""),
            *scene.get("aliases", []),
            *scene.get("scene_variants", []),
            *[str(row.get("role_background_face", "")) for row in rows],
            *[str(row.get("shot_expression", "")) for row in rows],
            *[str(row.get("cinematography", "")) for row in rows],
            *[str(row.get("director_intent", "")) for row in rows],
        ]
    )
    building_type_candidates = score_labels(joined_text, BUILDING_TYPE_MAP)
    space_type_candidates = score_labels(joined_text, SPACE_TYPE_MAP)
    material_candidates = score_labels(joined_text, MATERIAL_MAP)
    palette_candidates = score_labels(joined_text, PALETTE_MAP)
    topology_candidates = score_labels(joined_text, TOPOLOGY_MAP)
    time_light_cues = collect_terms(joined_text, TIME_LIGHT_TERMS)
    environment_cues = collect_terms(joined_text, ENVIRONMENT_TERMS)
    must_show_anchors = known_or_unknown(
        [scene.get("scene_name", ""), *scene.get("scene_variants", []), *scene.get("aliases", []), *collect_terms(joined_text, ANCHOR_TERMS)],
        max_items=5,
    )
    scale_reference_objects = known_or_unknown([item for item in must_show_anchors if any(key in item for key in ("门", "池", "电梯", "广场", "楼", "台"))], max_items=3)

    return {
        "building_type_candidates": building_type_candidates,
        "space_type_candidates": space_type_candidates,
        "material_candidates": material_candidates,
        "palette_candidates": palette_candidates,
        "topology_candidates": topology_candidates,
        "must_show_anchors": must_show_anchors,
        "scale_reference_objects": scale_reference_objects,
        "time_light_cues": time_light_cues,
        "environment_cues": environment_cues,
    }


def build_scene_blueprint(detail_profile: dict, scene: dict, scene_function: str) -> dict:
    return {
        "fixed_anchor_layer": {
            "scene_name": scene.get("scene_name", ""),
            "must_show_anchors": detail_profile.get("must_show_anchors", ["unknown"]),
            "material_candidates": detail_profile.get("material_candidates", ["unknown"]),
            "palette_candidates": detail_profile.get("palette_candidates", ["unknown"]),
            "topology_candidates": detail_profile.get("topology_candidates", ["unknown"]),
        },
        "variable_state_layer": {
            "scene_variants": scene.get("scene_variants", []) or ["unknown"],
            "time_light_cues": detail_profile.get("time_light_cues", ["unknown"]),
            "environment_cues": detail_profile.get("environment_cues", ["unknown"]),
        },
        "narrative_layer": {
            "scene_function": scene_function,
            "continuity_guard": "同一场景重复出现时，先保留空间主锚、边界和主色温，再考虑状态差分。",
        },
    }


def build_quality_profile(detail_profile: dict, evidence_count: int) -> dict:
    filled_fields = 0
    missing_fields: List[str] = []
    for field_key, label in QUALITY_FIELD_LABELS.items():
        values = detail_profile.get(field_key, ["unknown"])
        if values and values != ["unknown"]:
            filled_fields += 1
        else:
            missing_fields.append(label)
    score = min(100, 20 + filled_fields * 12 + min(evidence_count * 4, 20))
    if score >= 75:
        level = "strong"
    elif score >= 55:
        level = "medium"
    else:
        level = "weak"
    enrichment_actions = [ENRICHMENT_ACTION_MAP[label] for label in missing_fields if label in ENRICHMENT_ACTION_MAP]
    return {
        "concretization_score": score,
        "quality_level": level,
        "missing_fields": missing_fields,
        "enrichment_actions": enrichment_actions,
    }


def build_world_rule_profile(rows: Sequence[dict], scene_function: str, detail_profile: dict) -> dict:
    director_anchor = next((str(row.get("director_intent", "")).strip() for row in rows if row.get("director_intent")), "unknown")
    return {
        "director_intent_anchor": director_anchor,
        "scene_function": scene_function,
        "style_anchor": " / ".join(detail_profile.get("palette_candidates", ["unknown"])[:2]),
        "negative_constraints": [
            "不要把角色动作句直接升格成场景主键。",
            "不要因为单镜头状态词就发明新的永久场景。",
            "不要补写上游未给出的完整建筑考据。",
        ],
    }


def build_design_handoff(scene: dict, detail_profile: dict, quality_profile: dict) -> dict:
    scene_name = scene.get("scene_name", "unknown")
    materials = " / ".join(detail_profile.get("material_candidates", ["unknown"])[:2])
    palette = " / ".join(detail_profile.get("palette_candidates", ["unknown"])[:2])
    topology = " / ".join(detail_profile.get("topology_candidates", ["unknown"])[:2])
    return {
        "prompt_anchor": f"{scene_name} / material={materials} / palette={palette} / topology={topology}",
        "fixed_anchor_bridge": {
            "scene_name": scene_name,
            "must_show_anchors": detail_profile.get("must_show_anchors", ["unknown"]),
            "material_candidates": detail_profile.get("material_candidates", ["unknown"]),
            "palette_candidates": detail_profile.get("palette_candidates", ["unknown"]),
            "topology_candidates": detail_profile.get("topology_candidates", ["unknown"]),
        },
        "variable_state_bridge": {
            "scene_variants": scene.get("scene_variants", []) or ["unknown"],
            "time_light_cues": detail_profile.get("time_light_cues", ["unknown"]),
            "environment_cues": detail_profile.get("environment_cues", ["unknown"]),
        },
        "negative_constraints": [
            "不要把整句背景句直接当作 scene name。",
            "不要在没有证据时补充新建筑构件。",
            "不要丢失门禁、边界和主通行线。",
        ],
        "quality_flags": [
            *quality_profile.get("missing_fields", []),
            *(["needs_manual_review"] if quality_profile.get("quality_level") == "weak" else []),
        ],
    }


def summarize_quality(scenes: Sequence[dict]) -> dict:
    scores = [int(scene.get("design_context", {}).get("quality_profile", {}).get("concretization_score", 0)) for scene in scenes]
    if not scores:
        return {
            "average_concretization_score": 0,
            "strong_scene_count": 0,
            "medium_scene_count": 0,
            "weak_scene_count": 0,
            "scene_ids_need_enrichment": [],
            "top_missing_fields": [],
        }

    level_counter = Counter(
        scene.get("design_context", {}).get("quality_profile", {}).get("quality_level", "weak")
        for scene in scenes
    )
    missing_counter = Counter()
    weak_scene_ids: List[str] = []
    for scene in scenes:
        quality = scene.get("design_context", {}).get("quality_profile", {})
        for label in quality.get("missing_fields", []):
            missing_counter[label] += 1
        if quality.get("quality_level") == "weak":
            weak_scene_ids.append(scene.get("scene_id", "unknown"))

    return {
        "average_concretization_score": int(sum(scores) / len(scores)),
        "strong_scene_count": level_counter.get("strong", 0),
        "medium_scene_count": level_counter.get("medium", 0),
        "weak_scene_count": level_counter.get("weak", 0),
        "scene_ids_need_enrichment": weak_scene_ids,
        "top_missing_fields": [label for label, _ in missing_counter.most_common(5)],
    }


def merge_design_context(catalog: dict) -> dict:
    merged = dict(catalog)
    merged_meta = dict(merged.get("meta", {}))
    merged_meta["generated_at"] = datetime.now().astimezone().isoformat(timespec="seconds")
    merged["meta"] = merged_meta

    group_scene_rows = catalog.get("group_scene_map", [])
    merged_scenes: List[dict] = []
    for scene in catalog.get("scenes", []):
        scene_id = scene.get("scene_id", "")
        rows = [row for row in group_scene_rows if row.get("scene_id") == scene_id]
        scene_function = infer_scene_function(rows)
        detail_profile = build_detail_profile(scene=scene, rows=rows)
        scene_blueprint = build_scene_blueprint(detail_profile=detail_profile, scene=scene, scene_function=scene_function)
        scene_bible_card = build_scene_bible_card(scene_name=scene.get("scene_name", "unknown"), detail_profile=detail_profile, scene_function=scene_function)
        compendium = compose_compendium(scene_name=scene.get("scene_name", "unknown"), detail_profile=detail_profile, scene_function=scene_function)
        quality_profile = build_quality_profile(detail_profile=detail_profile, evidence_count=len(rows))
        display_profile = build_display_profile(scene_name=scene.get("scene_name", "unknown"), scene_function=scene_function, score=quality_profile["concretization_score"])
        design_handoff = build_design_handoff(scene=scene, detail_profile=detail_profile, quality_profile=quality_profile)
        evidence_ledger = build_evidence_ledger(rows)

        scene_with_context = dict(scene)
        scene_with_context["display_profile"] = display_profile
        scene_with_context["design_context"] = {
            "evidence_ledger": evidence_ledger,
            "key_anchors": {
                "scene_name": scene.get("scene_name", ""),
                "aliases": scene.get("aliases", []),
                "scene_variants": scene.get("scene_variants", []),
                "group_ids": scene.get("group_ids", []),
                "shot_ids": scene.get("shot_ids", []),
            },
            "detail_profile": detail_profile,
            "scene_blueprint": scene_blueprint,
            "scene_bible_card": scene_bible_card,
            "display_profile": display_profile,
            "compendium": compendium,
            "world_rule_profile": build_world_rule_profile(rows=rows, scene_function=scene_function, detail_profile=detail_profile),
            "quality_profile": quality_profile,
            "design_handoff": design_handoff,
        }
        merged_scenes.append(scene_with_context)

    merged["scenes"] = merged_scenes
    merged_statistics = dict(merged.get("statistics", {}))
    merged_statistics["quality_overview"] = summarize_quality(merged_scenes)
    merged["statistics"] = merged_statistics
    return merged


def build_research_payload(catalog: dict) -> dict:
    meta = dict(catalog.get("meta", {}))
    meta["schema_version"] = "aigc/design-scene-research/v1"
    meta["generated_at"] = datetime.now().astimezone().isoformat(timespec="seconds")
    return {
        "meta": meta,
        "statistics": catalog.get("statistics", {}),
        "quality_overview": catalog.get("statistics", {}).get("quality_overview", {}),
        "scenes": [
            {
                "scene_id": scene.get("scene_id", ""),
                "scene_name": scene.get("scene_name", ""),
                "aliases": scene.get("aliases", []),
                "scene_variants": scene.get("scene_variants", []),
                "occurrence": scene.get("occurrence", {}),
                "evidence_ledger": scene.get("design_context", {}).get("evidence_ledger", []),
                "detail_profile": scene.get("design_context", {}).get("detail_profile", {}),
                "scene_blueprint": scene.get("design_context", {}).get("scene_blueprint", {}),
                "scene_bible_card": scene.get("design_context", {}).get("scene_bible_card", {}),
                "display_profile": scene.get("design_context", {}).get("display_profile", {}),
                "compendium": scene.get("design_context", {}).get("compendium", ""),
                "world_rule_profile": scene.get("design_context", {}).get("world_rule_profile", {}),
                "quality_profile": scene.get("design_context", {}).get("quality_profile", {}),
            }
            for scene in catalog.get("scenes", [])
        ],
    }


def build_bridge_payload(catalog: dict) -> dict:
    meta = dict(catalog.get("meta", {}))
    meta["schema_version"] = "aigc/design-scene-bridge/v1"
    meta["generated_at"] = datetime.now().astimezone().isoformat(timespec="seconds")
    return {
        "meta": meta,
        "scenes": [
            {
                "scene_id": scene.get("scene_id", ""),
                "scene_name": scene.get("scene_name", ""),
                "group_ids": scene.get("group_ids", []),
                "shot_ids": scene.get("shot_ids", []),
                "display_profile": scene.get("design_context", {}).get("display_profile", {}),
                "scene_bible_card": scene.get("design_context", {}).get("scene_bible_card", {}),
                "design_bridge_profile": scene.get("design_context", {}).get("design_handoff", {}),
                "quality_flags": scene.get("design_context", {}).get("design_handoff", {}).get("quality_flags", []),
            }
            for scene in catalog.get("scenes", [])
        ],
    }


def main() -> int:
    args = parse_args()
    input_path = Path(args.input)
    if not input_path.exists():
        print(f"[ERROR] 输入文件不存在: {input_path}", file=sys.stderr)
        return 1

    try:
        catalog = read_json(input_path)
        merged_catalog = merge_design_context(catalog)
        research_payload = build_research_payload(merged_catalog)
        bridge_payload = build_bridge_payload(merged_catalog)
    except Exception as exc:  # noqa: BLE001
        print(f"[ERROR] {exc}", file=sys.stderr)
        return 1

    output_dir = Path(args.output_dir)
    catalog_path = output_dir / args.catalog_name
    research_path = output_dir / args.research_name
    bridge_path = output_dir / args.bridge_name

    if args.dry_run:
        print(
            "[DRY-RUN] "
            f"scenes={len(merged_catalog.get('scenes', []))} "
            f"avg_score={merged_catalog.get('statistics', {}).get('quality_overview', {}).get('average_concretization_score', 0)} "
            f"catalog={catalog_path.as_posix()} "
            f"research={research_path.as_posix()} "
            f"bridge={bridge_path.as_posix()}"
        )
        return 0

    output_dir.mkdir(parents=True, exist_ok=True)
    write_json(catalog_path, merged_catalog)
    write_json(research_path, research_payload)
    write_json(bridge_path, bridge_payload)
    print(f"[OK] 更新场景清单: {catalog_path.as_posix()}")
    print(f"[OK] 写入场景研究: {research_path.as_posix()}")
    print(f"[OK] 写入场景桥接: {bridge_path.as_posix()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
