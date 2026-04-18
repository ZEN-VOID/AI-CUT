#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Extract canonical scene catalog from a 3-Detail episode JSON."""

from __future__ import annotations

import argparse
import json
import re
import sys
from collections import defaultdict
from datetime import datetime
from pathlib import Path
from typing import Dict, Iterable, List, Sequence, Tuple


SCENE_SUFFIXES: Tuple[str, ...] = (
    "全息锦鲤池",
    "中央全息广场",
    "高层住宅电梯内",
    "安全通道",
    "楼梯间",
    "家门口",
    "单元门",
    "电梯门口",
    "门厅",
    "玄关",
    "宴会厅",
    "消防通道",
    "车内",
    "阁楼外间",
    "阁楼里间",
    "深巷酒吧一楼",
    "出租屋卧室",
    "出租屋卫生间",
    "小出租屋",
    "卫生间吊顶",
    "吊顶检修口",
    "卫生间门板",
    "卫生间门",
    "卫生间",
    "洗手池",
    "水龙头",
    "吊顶",
    "门板",
    "门框",
    "墙面",
    "床头墙面",
    "床头",
    "地砖",
    "车内",
    "广场",
    "步道",
    "池边",
    "池",
    "走廊",
    "楼道",
    "电梯",
    "轿厢",
    "大厅",
    "前厅",
    "后院",
    "庭院",
    "院落",
    "书房",
    "教室",
    "礼堂",
    "包厢",
    "街道",
    "街口",
    "巷口",
    "店铺",
    "茶馆",
    "码头",
    "渡口",
    "河岸",
    "河边",
    "江边",
    "江岸",
    "山路",
    "山道",
    "天台",
    "大殿",
    "殿前",
    "廊下",
    "长廊",
    "房间",
    "卧室",
    "客厅",
    "厨房",
    "办公室",
    "控制室",
    "舱室",
    "实验室",
    "操场",
    "球场",
    "宿舍",
)
SCENE_MATCH_RE = re.compile(
    r"(?P<scene>[\u4e00-\u9fffA-Za-z0-9]{1,18}(?:"
    + "|".join(sorted({re.escape(item) for item in SCENE_SUFFIXES}, key=len, reverse=True))
    + r"))"
)
SCENE_HINT_WORDS: Tuple[str, ...] = (
    "广场", "池", "步道", "门口", "走廊", "楼道", "楼梯间", "安全通道", "电梯", "轿厢",
    "庭院", "院落", "大厅", "房间", "街", "巷", "码头", "河", "江", "山路", "天台", "殿", "廊",
    "卫生间", "洗手池", "水龙头", "吊顶", "门板", "门框", "墙面", "床头", "地砖", "出租屋",
)
STRONG_SCENE_PHRASES: Tuple[str, ...] = (
    "出租屋卫生间",
    "出租屋卧室",
    "小出租屋",
    "卫生间吊顶",
    "吊顶检修口",
    "卫生间门板",
    "卫生间门",
    "卧室床头墙面",
    "卧室床头",
    "楼道门外",
    "卫生间",
    "洗手池",
    "水龙头",
    "吊顶",
    "门板",
    "门框",
    "楼道",
    "中央全息广场",
    "全息锦鲤池",
    "木星通讯画面",
    "木星工程背景",
    "深空基地系统",
    "深空基地",
    "深空背景",
    "社区广场",
    "开放广场",
    "广场中心",
    "广场舞区域",
    "广场四周",
    "围观路线",
    "晨间步道",
    "锦鲤池",
    "池边",
    "广场",
)
LEADING_NOISE_RE = re.compile(
    r"^(?:人物|角色|主角|镜头|画面|前景|后景|中景|近景|远景|身后是|背后是|前方是|仍被|仍在|仍靠着|靠着|位于|处于|形成|保持|作为|由|被)"
)
TRAILING_NOISE_RE = re.compile(r"(?:方向|一侧|外缘|环境|空间|位置|关系|状态|背景面|背景)$")
SENTENCE_NOISE_RE = re.compile(
    r"(?:静姐|老刘|张飞|刘星宇|人物|视觉中心|生怕|仍|已经|突然|忽然|重新|现场|关系|异物|投射|退场|回归|睡前|擦干|拧紧|确认|报警|冲回|显示|播放|低语)"
)
SCRIPT_SCENE_HEADING_RE = re.compile(
    r"^###\s*场景\d+[：:](?P<scene>.+?)(?:\s+(?:清晨|早晨|白天|日|夜|黄昏|傍晚|内/外|外/内|内|外).*)?$"
)
UNTRUSTWORTHY_SCENE_RE = re.compile(
    r"(?:^###|动作画面|对白|写成|形成|强化|主动选择|反向气压|私人角落|保护而非|暧昧)"
)
MICRO_ANCHOR_HINTS: Tuple[str, ...] = (
    "墙面",
    "门板",
    "门框",
    "吊顶",
    "洗手池",
    "水龙头",
    "床头",
    "地砖",
)
EPISODE_FILE_RE = re.compile(r"第0*(?P<episode>\d+)集\.json$")
NO_SCENE_TOKENS = {"", "unknown", "无", "暂无"}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="从 `3-Detail/第N集.json` 抽取场景对象池。")
    parser.add_argument("--input", required=True, help="输入 episode JSON")
    parser.add_argument("--output-dir", required=True, help="输出目录")
    parser.add_argument("--json-name", default="场景清单.json", help="输出 JSON 文件名")
    parser.add_argument("--dry-run", action="store_true", help="只校验链路，不写文件")
    return parser.parse_args()


def read_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, payload: dict) -> None:
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def infer_project_name(input_path: Path) -> str:
    parts = input_path.resolve().parts
    if "projects" in parts:
        idx = parts.index("projects")
        if idx + 2 < len(parts) and parts[idx + 1] == "aigc":
            return parts[idx + 2]
        if idx + 1 < len(parts):
            return parts[idx + 1]
    return input_path.parent.name


def infer_episode_id(input_path: Path, payload: dict) -> str:
    metadata = payload.get("metadata", {})
    if isinstance(metadata, dict) and metadata.get("episode_id"):
        return str(metadata["episode_id"])
    match = EPISODE_FILE_RE.search(input_path.name)
    if match:
        return f"第{int(match.group('episode'))}集"
    return input_path.stem


def get_groups(payload: dict) -> List[dict]:
    try:
        groups = payload["final_output"]["main_content"]["分镜组列表"]
    except KeyError as exc:
        raise ValueError("输入 JSON 不符合 director episode schema，缺少 `final_output.main_content.分镜组列表`。") from exc
    if not isinstance(groups, list):
        raise ValueError("`分镜组列表` 必须是数组。")
    return groups


def unique_preserve(items: Iterable[str]) -> List[str]:
    seen = set()
    output: List[str] = []
    for item in items:
        if not item or item in seen:
            continue
        seen.add(item)
        output.append(item)
    return output


def normalize_scene_fragment(text: str) -> str:
    cleaned = str(text or "").strip()
    cleaned = cleaned.replace("作为人物背景面", "").replace("作为背景面", "").replace("成为前景关系点", "")
    cleaned = re.sub(r"[，。；;、|｜/（）()【】]", " ", cleaned)
    cleaned = LEADING_NOISE_RE.sub("", cleaned).strip()
    cleaned = TRAILING_NOISE_RE.sub("", cleaned).strip()
    if "的" in cleaned:
        tail = cleaned.split("的")[-1].strip()
        if any(hint in tail for hint in SCENE_HINT_WORDS):
            cleaned = tail
    cleaned = cleaned.strip(" -_")
    return cleaned


def extract_scene_candidates(text: str) -> List[str]:
    raw = str(text or "").strip()
    if raw in NO_SCENE_TOKENS:
        return []

    strong_matches = [
        phrase
        for phrase in STRONG_SCENE_PHRASES
        if phrase in raw and phrase not in NO_SCENE_TOKENS
    ]
    if strong_matches:
        return unique_preserve(strong_matches)

    matches: List[str] = []
    for match in SCENE_MATCH_RE.finditer(raw):
        scene = normalize_scene_fragment(match.group("scene"))
        if scene and scene not in NO_SCENE_TOKENS:
            matches.append(scene)

    if matches:
        return unique_preserve(matches)

    for fragment in re.split(r"[，。；;、|｜/]", raw):
        candidate = normalize_scene_fragment(fragment)
        if (
            candidate
            and any(hint in candidate for hint in SCENE_HINT_WORDS)
            and not SENTENCE_NOISE_RE.search(candidate)
        ):
            matches.append(candidate)

    return unique_preserve(matches)


def extract_script_heading_scene(script_body: str) -> str:
    first_line = str(script_body or "").splitlines()[0].strip() if str(script_body or "").strip() else ""
    if not first_line:
        return ""
    match = SCRIPT_SCENE_HEADING_RE.match(first_line)
    if not match:
        return ""
    return normalize_scene_fragment(match.group("scene").strip())


def is_untrustworthy_scene(scene_name: str) -> bool:
    text = str(scene_name or "").strip()
    if not text or text in NO_SCENE_TOKENS:
        return True
    if UNTRUSTWORTHY_SCENE_RE.search(text):
        return True
    if "被" in text and any(hint in text for hint in SCENE_HINT_WORDS):
        return True
    return False


def join_non_empty(parts: Iterable[str]) -> str:
    return " ".join(item.strip() for item in parts if isinstance(item, str) and item.strip())


def stringify_branch_design(value: object, ordered_keys: Sequence[str]) -> str:
    if not isinstance(value, dict):
        return ""
    return join_non_empty(str(value.get(key, "")).strip() for key in ordered_keys)


def pick_branch_object(shot: dict, *field_names: str) -> object:
    for field_name in field_names:
        value = shot.get(field_name)
        if isinstance(value, dict):
            return value
    return {}


def derive_scene_inputs(shot: dict) -> dict:
    atmosphere_anchor = stringify_branch_design(
        pick_branch_object(shot, "氛围表现", "空间氛围"),
        ("层次", "空间诗学", "意境", "空间支架", "空气层", "物象压力"),
    )
    composition_anchor = stringify_branch_design(
        pick_branch_object(shot, "分镜构图", "构图骨架", "构图策略"),
        ("景别景深", "镜头类型", "构图形式", "构图骨架", "视线组织"),
    )
    cinematography_anchor = stringify_branch_design(
        pick_branch_object(shot, "摄影美学", "摄影策略"),
        ("光影", "色彩", "质感", "视觉控制线", "光影策略", "色彩策略", "质感策略"),
    )
    visual_anchor = stringify_branch_design(
        pick_branch_object(shot, "视觉强化", "视觉抓手", "视觉焦点"),
        ("冲击力", "观赏性", "品味", "第一抓手", "观看节奏", "镜头消费提示"),
    )
    legacy_background_face = str(shot.get("角色背景面", "")).strip()
    legacy_expression = str(shot.get("分镜表现", "")).strip()
    legacy_cinematography = str(shot.get("摄影美学", "")).strip()
    primary_scene_anchor = join_non_empty(
        (atmosphere_anchor, composition_anchor, legacy_background_face)
    )
    fallback_scene_text = join_non_empty(
        (
            composition_anchor,
            cinematography_anchor,
            visual_anchor,
            legacy_expression,
            legacy_cinematography,
        )
    )
    return {
        "primary_scene_anchor": primary_scene_anchor,
        "fallback_scene_text": fallback_scene_text,
        "legacy_background_face": legacy_background_face,
        "legacy_expression": legacy_expression,
        "legacy_cinematography": legacy_cinematography,
        "atmosphere_anchor": atmosphere_anchor,
        "composition_anchor": composition_anchor,
        "cinematography_anchor": cinematography_anchor,
        "visual_anchor": visual_anchor,
    }


def choose_scene_name(primary_scene_anchor: str, fallback_text: str, script_body: str) -> Tuple[str, List[str]]:
    primary_candidates = extract_scene_candidates(primary_scene_anchor)
    script_scene = extract_script_heading_scene(script_body)
    script_candidates = extract_scene_candidates(script_scene) if script_scene else []
    if script_scene and not script_candidates and script_scene not in NO_SCENE_TOKENS:
        script_candidates = [script_scene]

    if script_candidates:
        merged = unique_preserve([*script_candidates, *primary_candidates])
        return merged[0], merged

    if primary_candidates:
        primary = primary_candidates[0]
        if not is_untrustworthy_scene(primary):
            return primary, unique_preserve(primary_candidates)

    if fallback_text:
        fallback_candidates = extract_scene_candidates(fallback_text)
        fallback_candidates = [
            item
            for item in fallback_candidates
            if not SENTENCE_NOISE_RE.search(item) and not is_untrustworthy_scene(item)
        ]
        if fallback_candidates:
            return fallback_candidates[0], fallback_candidates
    return "unknown", []


def build_display_profile(scene_name: str, variants: Sequence[str], shot_count: int) -> dict:
    variant_label = next((item for item in variants if item and item != scene_name), scene_name)
    return {
        "title": scene_name,
        "short_tagline": f"{scene_name} / {shot_count}镜证据",
        "summary": f"{scene_name}在当前集至少出现 {shot_count} 个镜头，变体主要围绕“{variant_label}”展开。",
        "visual_hook": f"设计阶段应优先锁住 {scene_name} 的主空间识别，再处理方位与状态差分。",
    }


def build_catalog(input_path: Path, payload: dict) -> dict:
    groups = get_groups(payload)
    project_name = infer_project_name(input_path)
    episode_id = infer_episode_id(input_path, payload)

    meta = {
        "schema_version": "aigc/design-scene-list/v1",
        "skill_id": "aigc-design-scene-list",
        "project_name": project_name,
        "episode_id": episode_id,
        "primary_input": input_path.as_posix(),
        "source_input": input_path.as_posix(),
        "source_inputs": [input_path.as_posix()],
        "source_schema": ".agents/skills/aigc/_shared/director_episode_output.schema.json",
        "generated_at": datetime.now().astimezone().isoformat(timespec="seconds"),
    }

    scene_rows: List[dict] = []
    scene_index: Dict[str, dict] = {}
    scene_order: List[str] = []
    groups_without_scene: List[str] = []

    for group in groups:
        group_id = str(group.get("分镜组ID", "unknown"))
        group_design = group.get("组间设计", {}) if isinstance(group.get("组间设计"), dict) else {}
        director_intent = str(group_design.get("导演意图", "")).strip()
        script_body = str(group.get("剧本正文", "")).strip()
        shots = group.get("分镜明细", [])

        if not isinstance(shots, list) or not shots:
            groups_without_scene.append(group_id)
            continue

        for shot in shots:
            shot_id = str(shot.get("分镜ID", "unknown"))
            scene_inputs = derive_scene_inputs(shot)
            time_range = shot.get("时间段", {})
            fallback_text = join_non_empty(
                (
                    scene_inputs["fallback_scene_text"],
                    director_intent,
                    script_body,
                )
            )
            scene_name, candidates = choose_scene_name(
                scene_inputs["primary_scene_anchor"],
                fallback_text,
                script_body,
            )
            scene_variant_seed = (
                scene_inputs["legacy_background_face"]
                or scene_inputs["primary_scene_anchor"]
                or "unknown"
            )
            scene_variant = next(
                (item for item in candidates[1:] if item != scene_name),
                scene_variant_seed[:48] or "unknown",
            )

            row = {
                "scene_name": scene_name,
                "scene_candidates": candidates,
                "scene_variant": scene_variant,
                "group_id": group_id,
                "shot_id": shot_id,
                "space_anchor": scene_inputs["atmosphere_anchor"],
                "composition_anchor": scene_inputs["composition_anchor"],
                "cinematography_anchor": scene_inputs["cinematography_anchor"],
                "visual_anchor": scene_inputs["visual_anchor"],
                "role_background_face": scene_inputs["legacy_background_face"],
                "shot_expression": scene_inputs["legacy_expression"],
                "cinematography": scene_inputs["legacy_cinematography"],
                "director_intent": director_intent,
                "script_body_excerpt": script_body[:120],
                "time_range": {
                    "开始秒": time_range.get("开始秒"),
                    "结束秒": time_range.get("结束秒"),
                },
            }
            scene_rows.append(row)

            if scene_name not in scene_index:
                scene_order.append(scene_name)
                scene_index[scene_name] = {
                    "scene_name": scene_name,
                    "aliases": [],
                    "scene_variants": [],
                    "group_ids": [],
                    "shot_ids": [],
                    "first_appearance": {"group_id": group_id, "shot_id": shot_id},
                }

            scene_entry = scene_index[scene_name]
            scene_entry["aliases"].extend(candidates)
            if scene_variant and scene_variant != "unknown":
                scene_entry["scene_variants"].append(scene_variant)
            scene_entry["group_ids"].append(group_id)
            scene_entry["shot_ids"].append(shot_id)

    scenes: List[dict] = []
    scene_id_map: Dict[str, str] = {}
    for idx, scene_name in enumerate(scene_order, start=1):
        entry = scene_index[scene_name]
        scene_id = f"scene-{idx:03d}"
        scene_id_map[scene_name] = scene_id
        aliases = unique_preserve(entry["aliases"])
        variants = unique_preserve(entry["scene_variants"])
        group_ids = unique_preserve(entry["group_ids"])
        shot_ids = unique_preserve(entry["shot_ids"])
        scenes.append(
            {
                "scene_id": scene_id,
                "scene_name": scene_name,
                "scene_level": "主场景",
                "aliases": aliases,
                "scene_variants": variants,
                "group_ids": group_ids,
                "shot_ids": shot_ids,
                "occurrence": {
                    "group_count": len(group_ids),
                    "shot_count": len(shot_ids),
                },
                "first_appearance": entry["first_appearance"],
                "display_profile": build_display_profile(scene_name, variants or aliases, len(shot_ids)),
            }
        )

    group_scene_map = []
    unknown_scene_rows = 0
    for row in scene_rows:
        if row["scene_name"] == "unknown":
            unknown_scene_rows += 1
        group_scene_map.append(
            {
                "scene_id": scene_id_map.get(row["scene_name"], "unknown"),
                "scene_name": row["scene_name"],
                "scene_variant": row["scene_variant"],
                "scene_candidates": row["scene_candidates"],
                "group_id": row["group_id"],
                "shot_id": row["shot_id"],
                "role_background_face": row["role_background_face"],
                "shot_expression": row["shot_expression"],
                "cinematography": row["cinematography"],
                "director_intent": row["director_intent"],
                "script_body_excerpt": row["script_body_excerpt"],
                "time_range": row["time_range"],
            }
        )

    statistics = {
        "source_group_count": len(groups),
        "source_shot_count": len(scene_rows),
        "total_scenes": len(scenes),
        "unknown_scene_rows": unknown_scene_rows,
        "groups_without_scene_anchor": unique_preserve(groups_without_scene),
    }

    return {
        "meta": meta,
        "scenes": scenes,
        "group_scene_map": group_scene_map,
        "statistics": statistics,
    }


def main() -> int:
    args = parse_args()
    input_path = Path(args.input)
    if not input_path.exists():
        print(f"[ERROR] 输入文件不存在: {input_path}", file=sys.stderr)
        return 1

    try:
        payload = read_json(input_path)
        catalog = build_catalog(input_path=input_path, payload=payload)
    except Exception as exc:  # noqa: BLE001
        print(f"[ERROR] {exc}", file=sys.stderr)
        return 1

    output_dir = Path(args.output_dir)
    output_path = output_dir / args.json_name

    if args.dry_run:
        print(
            "[DRY-RUN] "
            f"scenes={len(catalog.get('scenes', []))} "
            f"shots={catalog.get('statistics', {}).get('source_shot_count', 0)} "
            f"output={output_path.as_posix()}"
        )
        return 0

    output_dir.mkdir(parents=True, exist_ok=True)
    write_json(output_path, catalog)
    print(f"[OK] 写入场景清单: {output_path.as_posix()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
