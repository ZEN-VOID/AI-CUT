#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Extract prop catalog from a director-episode JSON file."""

from __future__ import annotations

import argparse
import json
import re
import sys
from collections import defaultdict
from datetime import datetime
from pathlib import Path
from typing import Dict, Iterable, List, Sequence, Tuple


NO_PROP_TOKENS = {
    "",
    "无",
    "无道具",
    "无关键道具",
    "无明显道具",
    "无核心道具",
    "暂无",
    "暂无道具",
    "none",
    "n/a",
}

SPLIT_RE = re.compile(r"[，、；;|｜/]")
PAREN_RE = re.compile(r"[（(](.*?)[）)]")
PROP_INLINE_RE = re.compile(
    r"([\u4e00-\u9fffA-Za-z0-9]{0,8}?(?:"
    r"刀鞘|勾魂链|糖葫芦|令牌|腰牌|玉佩|火把|灯笼|提灯|烛台|牢门|牢栏|囚车|马车|门闩|门板|车厢|车轮|"
    r"衣箱|帐帘|铜镜|木梳|药瓶|药碗|药炉|文书|密信|地图|军报|卷轴|书卷|刀|剑|枪|链|盏|壶|杯|瓶|书|卷|"
    r"信|牌|印|镜|梳|门|锁|栏|车|箱|帘|灯|扇|佩|簪|冠|甲|鞘|囊|袍|衣|鞋|靴|旗|鼓|伞|炉|匣|匙|钥匙"
    r"))"
)
LEADING_CONTEXT_RE = re.compile(
    r"^(?:前景|后景|近景|远景|桌上|案上|柜台上|门边|地上|脚边|身旁|怀里|肩上|腰间|手中|手里|掌中|背后|画面中|镜头里)"
    r"(?:的)?"
)
STATE_NOISE_RE = re.compile(
    r"^(?:轻晃的|摇晃的|半开的|打开的|染血的|沾血的|破损的|旧的|湿的|紧握的|发光的|碎裂的|残破的|斑驳的)"
)
STATE_PREFIX_RE = re.compile(
    r"^(?:左手|右手|双手|手中|手里|掌中|腰间|怀里|门边|前景|后景|近景|远景|染血|沾血|半开|半开的|打开的|"
    r"高举的|高举|摇晃的|摇晃|垂落的|垂落|未全退的|未全退|轻撞的|轻撞|紧握的|紧握|湿冷的|湿冷|斑驳的|"
    r"残破的|破损的)"
)
EPISODE_FILE_RE = re.compile(r"第0*(?P<episode>\d+)集\.json$")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="从 `3-Detail/第N集.json` 抽取分镜级道具清单。")
    parser.add_argument("--input", required=True, help="输入 episode JSON")
    parser.add_argument("--output-dir", required=True, help="输出目录")
    parser.add_argument("--json-name", default="道具清单.json", help="输出 JSON 文件名")
    parser.add_argument("--dry-run", action="store_true", help="只做解析校验，不写文件")
    return parser.parse_args()


def read_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, payload: dict) -> None:
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def infer_project_name(input_path: Path) -> str:
    match = re.search(r"/projects/aigc/([^/]+)/", input_path.as_posix())
    if not match:
        match = re.search(r"/projects/([^/]+)/", input_path.as_posix())
    if match:
        return match.group(1)
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


def normalize_clause_text(clause: str) -> str:
    text = clause.strip()
    text = LEADING_CONTEXT_RE.sub("", text)
    text = STATE_NOISE_RE.sub("", text)
    text = text.strip(" ，。；;、/|｜")
    return text


def extract_parenthetical_state(text: str) -> Tuple[str, str]:
    states = [item.strip() for item in PAREN_RE.findall(text) if item.strip()]
    state_text = " / ".join(states)
    normalized = PAREN_RE.sub("", text).strip()
    return normalized, state_text


def pick_prop_name(text: str) -> str:
    match = PROP_INLINE_RE.search(text)
    if match:
        return match.group(1)
    words = [part for part in re.split(r"\s+", text) if part]
    return words[-1] if words else text


def extract_candidate_names(text: str) -> List[str]:
    matches = [match.group(1).strip() for match in PROP_INLINE_RE.finditer(text) if match.group(1).strip()]
    output: List[str] = []
    for item in matches:
        cleaned = STATE_PREFIX_RE.sub("", item).strip(" ，。；;、")
        if cleaned and cleaned not in output:
            output.append(cleaned)
    return output


def infer_prop_type(prop_name: str) -> str:
    if any(token in prop_name for token in ("刀", "剑", "枪", "链", "甲", "鞭")):
        return "weapon_or_restraint"
    if any(token in prop_name for token in ("令牌", "腰牌", "印", "文书", "密信", "军报", "地图", "卷轴", "书", "卷", "信")):
        return "document_or_token"
    if any(token in prop_name for token in ("门", "栏", "囚车", "马车", "帐帘", "箱", "炉", "灯笼", "火把", "提灯")):
        return "set_piece"
    if any(token in prop_name for token in ("玉佩", "簪", "冠", "扇", "镜", "梳", "钥匙")):
        return "wearable_or_handheld"
    return "general_prop"


def parse_prop_mentions(prop_text: str) -> List[dict]:
    raw = (prop_text or "").strip()
    if raw in NO_PROP_TOKENS:
        return []

    normalized = raw.replace("：", ":")
    clauses = [normalize_clause_text(part) for part in SPLIT_RE.split(normalized)]
    mentions: List[dict] = []

    for clause in clauses:
        if not clause or clause in NO_PROP_TOKENS:
            continue

        stripped_clause, paren_state = extract_parenthetical_state(clause)
        candidate_names = extract_candidate_names(stripped_clause)
        if not candidate_names:
            fallback_name = pick_prop_name(stripped_clause)
            if fallback_name and fallback_name not in NO_PROP_TOKENS:
                candidate_names = [fallback_name]

        if not candidate_names:
            continue

        state_base = stripped_clause
        for candidate_name in candidate_names:
            state_base = state_base.replace(candidate_name, " ")
        state_base = normalize_clause_text(state_base)
        states = [item for item in (state_base, paren_state) if item]
        state = " / ".join([item for item in states if item]) or "unknown"

        for prop_name in candidate_names:
            mentions.append(
                {
                    "prop_name": prop_name,
                    "state": state,
                    "raw": clause,
                    "prop_type": infer_prop_type(prop_name),
                }
            )

    dedup: Dict[Tuple[str, str, str], dict] = {}
    for item in mentions:
        key = (item["prop_name"], item["state"], item["raw"])
        dedup[key] = item
    return list(dedup.values())


def unique_preserve(items: Iterable[str]) -> List[str]:
    seen = set()
    output: List[str] = []
    for item in items:
        if not item or item in seen:
            continue
        seen.add(item)
        output.append(item)
    return output


def build_display_profile(prop_name: str, prop_type: str, scenes: Sequence[str], states: Sequence[str]) -> dict:
    scene_anchor = next((item for item in scenes if item), "当前镜头")
    state_anchor = next((item for item in states if item and item != "unknown"), "状态稳定")
    prop_type_title = {
        "weapon_or_restraint": "器械型道具",
        "document_or_token": "凭证型道具",
        "set_piece": "场域型道具",
        "wearable_or_handheld": "近身型道具",
        "general_prop": "剧情道具",
    }.get(prop_type, "剧情道具")
    return {
        "title": prop_name,
        "short_tagline": f"{prop_type_title} / {scene_anchor}",
        "description": f"{prop_name}在{scene_anchor}中反复出现，当前以“{state_anchor}”这一镜头状态最值得被保留到设计阶段。",
        "visual_signature": f"{prop_name}需要保留其在{scene_anchor}中的辨识轮廓与状态痕迹。",
        "dramatic_value": f"{prop_name}承担镜头内的动作提示、空间提示或权力提示，不宜在设计阶段被弱化为背景装饰。",
    }


def build_catalog(input_path: Path, payload: dict) -> dict:
    groups = get_groups(payload)
    project_name = infer_project_name(input_path)
    episode_id = infer_episode_id(input_path, payload)
    meta = {
        "project_name": project_name,
        "episode_id": episode_id,
        "source_input": input_path.as_posix(),
        "source_schema": ".agents/skills/aigc/_shared/director_episode_output.schema.json",
        "skill_id": "aigc/4-Design/道具/1-清单",
        "generated_at": datetime.now().astimezone().isoformat(timespec="seconds"),
    }

    group_prop_map: List[dict] = []
    groups_without_props: List[str] = []
    props_index: Dict[str, dict] = {}
    prop_order: List[str] = []

    for group in groups:
        group_id = str(group.get("分镜组ID", "unknown"))
        script_text = str(group.get("剧本正文", "")).strip()
        group_design = group.get("组间设计", {}) if isinstance(group.get("组间设计"), dict) else {}
        shots = group.get("分镜明细", [])
        group_has_prop = False

        for shot in shots:
            shot_id = str(shot.get("分镜ID", "unknown"))
            scene_value = str(shot.get("角色背景面") or shot.get("场景及方位") or "").strip()
            roles_value = str(shot.get("角色站位走位") or shot.get("角色及站位和穿搭") or "").strip()
            prop_value = str(shot.get("道具及状态", "")).strip()
            mentions = parse_prop_mentions(prop_value)
            if mentions:
                group_has_prop = True

            row = {
                "group_id": group_id,
                "shot_id": shot_id,
                "scene": scene_value,
                "roles": roles_value,
                "raw_prop_text": prop_value,
                "script_excerpt": script_text,
                "group_design": {
                    "全局风格": str(group_design.get("全局风格", "")).strip(),
                    "类型元素": str(group_design.get("类型元素", "")).strip(),
                    "导演意图": str(group_design.get("导演意图", "")).strip(),
                },
                "prop_mentions": mentions,
            }
            group_prop_map.append(row)

            for mention in mentions:
                prop_name = mention["prop_name"]
                if prop_name not in props_index:
                    prop_order.append(prop_name)
                    props_index[prop_name] = {
                        "prop_id": f"prop-{len(prop_order):03d}",
                        "canonical_name": prop_name,
                        "prop_type": mention["prop_type"],
                        "aliases": [],
                        "group_ids": [],
                        "shot_ids": [],
                        "scene_anchors": [],
                        "role_anchors": [],
                        "state_variants": [],
                        "raw_mentions": [],
                        "display_profile": {},
                    }
                item = props_index[prop_name]
                item["aliases"].append(mention["raw"])
                item["group_ids"].append(group_id)
                item["shot_ids"].append(shot_id)
                item["scene_anchors"].append(scene_value)
                item["role_anchors"].append(roles_value)
                item["state_variants"].append(mention["state"])
                item["raw_mentions"].append(
                    {
                        "group_id": group_id,
                        "shot_id": shot_id,
                        "raw": mention["raw"],
                        "state": mention["state"],
                    }
                )

        if not group_has_prop:
            groups_without_props.append(group_id)

    props: List[dict] = []
    for prop_name in prop_order:
        item = props_index[prop_name]
        scenes = unique_preserve(item["scene_anchors"])
        states = unique_preserve(item["state_variants"])
        item["display_profile"] = build_display_profile(
            prop_name=prop_name,
            prop_type=item["prop_type"],
            scenes=scenes,
            states=states,
        )
        props.append(
            {
                "prop_id": item["prop_id"],
                "canonical_name": item["canonical_name"],
                "prop_type": item["prop_type"],
                "aliases": unique_preserve(item["aliases"]),
                "group_ids": unique_preserve(item["group_ids"]),
                "shot_ids": unique_preserve(item["shot_ids"]),
                "scene_anchors": scenes,
                "role_anchors": unique_preserve(item["role_anchors"]),
                "state_variants": states,
                "occurrence_count": len(item["raw_mentions"]),
                "display_profile": item["display_profile"],
                "raw_mentions": item["raw_mentions"],
            }
        )

    return {
        "meta": meta,
        "group_prop_map": group_prop_map,
        "groups_without_props": groups_without_props,
        "props": props,
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
        print(f"[DRY-RUN] props={len(catalog['props'])} output={output_path.as_posix()}")
        return 0

    output_dir.mkdir(parents=True, exist_ok=True)
    write_json(output_path, catalog)
    print(f"[OK] 写入道具清单: {output_path.as_posix()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
