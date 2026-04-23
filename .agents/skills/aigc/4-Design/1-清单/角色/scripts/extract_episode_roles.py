#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Extract canonical role catalog from a 3-Detail episode JSON."""

from __future__ import annotations

import argparse
import json
import re
import sys
from collections import Counter, defaultdict
from datetime import datetime
from pathlib import Path
from typing import Dict, Iterable, List, Sequence, Tuple


ROOT = Path(__file__).resolve().parents[7]
AIGC_SHARED_DIR = ROOT / ".agents" / "skills" / "aigc" / "_shared"
if str(AIGC_SHARED_DIR) not in sys.path:
    sys.path.insert(0, str(AIGC_SHARED_DIR))

from detail_root_adapter import CANONICAL_DETAIL_TEMPLATE, ensure_legacy_detail_payload  # noqa: E402


EPISODE_FILE_RE = re.compile(r"第0*(?P<episode>\d+)集\.json$")
GROUP_SPLIT_RE = re.compile(r"[；;]\s*")
ROLE_ANCHOR_RE = re.compile(r"(?P<name>[^：:；;，。,\\-—]{1,20})[：:](?P<desc>.+)")
ROLE_HYPHEN_ANCHOR_RE = re.compile(r"(?P<name>[^：:；;，。,\\-—]{1,20})[-—](?P<desc>.+)")
ROLE_NAME_RE = re.compile(r"[\u4e00-\u9fffA-Za-z0-9]{1,12}")
CLAUSE_SPLIT_RE = re.compile(r"[，,、；;。]\s*")
COLLECTIVE_KEYWORDS = ("众人", "人群", "围观者", "宾客群", "侍卫群", "保镖群", "服务生群")
CLOTHING_KEYWORDS = (
    "礼服",
    "西装",
    "工装",
    "衬衫",
    "外套",
    "裙",
    "高跟鞋",
    "毛巾",
    "钻饰",
    "项链",
    "袖口",
    "赤脚",
    "湿礼服",
    "装束",
    "衣着",
    "衣物",
    "长裙",
    "短裙",
    "制服",
)
PROP_HINTS = ("项链", "高脚杯", "毛巾", "衣物", "外套", "衬衫", "高跟鞋", "杯", "钻饰")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="从 `3-Detail/第N集.json` 抽取角色对象池。")
    parser.add_argument("--input", required=True, help="输入 episode JSON")
    parser.add_argument("--output-dir", required=True, help="输出目录")
    parser.add_argument("--json-name", default="角色清单.json", help="输出 JSON 文件名")
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
    meta = payload.get("meta", {})
    if isinstance(meta, dict) and meta.get("集数"):
        return str(meta["集数"])
    metadata = payload.get("metadata", {})
    if isinstance(metadata, dict) and metadata.get("episode_id"):
        return str(metadata["episode_id"])
    match = EPISODE_FILE_RE.search(input_path.name)
    if match:
        return f"第{int(match.group('episode'))}集"
    return input_path.stem


def get_groups(payload: dict) -> List[dict]:
    payload = ensure_legacy_detail_payload(payload)
    try:
        groups = payload["final_output"]["main_content"]["分镜组列表"]
    except KeyError as exc:
        raise ValueError("输入 JSON 既不符合 canonical detail root，也无法投影出 `分镜组列表` 兼容视图。") from exc
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


def clean_excerpt(text: str, limit: int = 90) -> str:
    cleaned = re.sub(r"\s+", "", str(text or "").strip())
    return cleaned[:limit]


def normalize_role_name(raw_name: str) -> str:
    name = re.sub(r"[（(].*?[）)]", "", str(raw_name or "")).strip("：:；;，,。 ")
    name = name.replace("“", "").replace("”", "")
    return name


def is_collective_role(name: str) -> bool:
    if not name:
        return False
    return any(keyword in name for keyword in COLLECTIVE_KEYWORDS)


def infer_role_level(name: str) -> str:
    if is_collective_role(name):
        return "群像角色"
    if name.startswith("unknown-role-"):
        return "unknown"
    return "单人角色"


def select_costume_anchor(description: str) -> str:
    clauses = [clean_excerpt(part, limit=40) for part in CLAUSE_SPLIT_RE.split(str(description or "")) if clean_excerpt(part)]
    for clause in clauses:
        if any(keyword in clause for keyword in CLOTHING_KEYWORDS):
            return clause
    return clauses[0] if clauses else "unknown"


def parse_group_role_anchors(raw_text: str) -> List[Tuple[str, str, str]]:
    anchors: List[Tuple[str, str, str]] = []
    for chunk in GROUP_SPLIT_RE.split(str(raw_text or "").strip()):
        chunk = chunk.strip("。 ")
        if not chunk:
            continue
        match = ROLE_ANCHOR_RE.match(chunk)
        if not match:
            match = ROLE_HYPHEN_ANCHOR_RE.match(chunk)
        if not match:
            continue
        name = normalize_role_name(match.group("name"))
        description = clean_excerpt(match.group("desc"), limit=80)
        if not name:
            continue
        anchors.append((name, description, select_costume_anchor(description)))
    return anchors


def infer_role_tier(group_count: int, shot_count: int, role_level: str) -> str:
    if role_level == "群像角色":
        return "群像"
    if shot_count >= 10 or group_count >= 5:
        return "主角"
    if shot_count >= 4 or group_count >= 3:
        return "重要配角"
    return "功能配角"


def collect_prop_hints(*texts: str) -> List[str]:
    hits: List[str] = []
    combined = " ".join(str(text or "") for text in texts)
    for hint in PROP_HINTS:
        if hint in combined:
            hits.append(hint)
    return unique_preserve(hits)


def build_display_profile(name: str, tier: str, costume_state: str, shot_count: int) -> dict:
    return {
        "title": name,
        "short_tagline": f"{tier}|shots={shot_count}",
        "summary": f"shot_count={shot_count}; primary_costume_state={costume_state}",
        "visual_hook": f"canonical_name={name}; primary_costume_state={costume_state}",
    }


def stringify_branch_design(value: object, ordered_keys: Sequence[str]) -> str:
    if not isinstance(value, dict):
        return ""
    return "；".join(str(value.get(key, "")).strip() for key in ordered_keys if str(value.get(key, "")).strip())


def pick_branch_object(shot: dict, *field_names: str) -> object:
    for field_name in field_names:
        value = shot.get(field_name)
        if isinstance(value, dict):
            return value
    return {}


def build_catalog(input_path: Path, payload: dict) -> dict:
    groups = get_groups(payload)
    project_name = infer_project_name(input_path)
    episode_id = infer_episode_id(input_path, payload)

    meta = {
        "schema_version": "aigc/design-role-list/v1",
        "skill_id": "aigc-design-role-list",
        "project_name": project_name,
        "episode_id": episode_id,
        "primary_input": input_path.as_posix(),
        "source_input": input_path.as_posix(),
        "source_inputs": [input_path.as_posix()],
        "source_schema": CANONICAL_DETAIL_TEMPLATE,
        "generated_at": datetime.now().astimezone().isoformat(timespec="seconds"),
    }

    role_pool: Dict[str, dict] = {}
    role_order: List[str] = []
    map_rows: List[dict] = []
    groups_without_role_anchor: List[str] = []
    shot_evidence_count = 0

    for group in groups:
        group_id = str(group.get("分镜组ID", "unknown"))
        group_design = group.get("组间设计", {}) if isinstance(group.get("组间设计"), dict) else {}
        role_anchor_text = str(group_design.get("出场角色及穿搭", "")).strip()
        script_body = clean_excerpt(group.get("剧本正文", ""), limit=120)
        anchors = parse_group_role_anchors(role_anchor_text)

        if not anchors:
            groups_without_role_anchor.append(group_id)

        group_role_names: List[str] = []
        for name, description, costume_anchor in anchors:
            group_role_names.append(name)
            if name not in role_pool:
                role_pool[name] = {
                    "canonical_name": name,
                    "role_level": infer_role_level(name),
                    "group_ids": [],
                    "shot_ids": [],
                    "costume_anchors": [],
                    "costume_variants": [],
                    "group_anchor_descriptions": [],
                    "prop_hints": [],
                    "evidence_counter": Counter(),
                    "first_appearance": {"group_id": group_id, "shot_id": ""},
                }
                role_order.append(name)

            role_entry = role_pool[name]
            role_entry["group_ids"].append(group_id)
            role_entry["costume_anchors"].append(costume_anchor)
            role_entry["group_anchor_descriptions"].append(description)
            role_entry["prop_hints"].extend(collect_prop_hints(description))
            role_entry["evidence_counter"]["group_anchor"] += 1

            existing_variant_keys = {item["costume_anchor"] for item in role_entry["costume_variants"]}
            if costume_anchor not in existing_variant_keys:
                role_entry["costume_variants"].append(
                    {
                        "costume_anchor": costume_anchor,
                        "first_group_id": group_id,
                        "trigger_shot_ids": [],
                        "source_excerpt": description,
                    }
                )

            map_rows.append(
                {
                    "canonical_name": name,
                    "group_id": group_id,
                    "shot_id": "",
                    "source_slot": "组间设计.出场角色及穿搭",
                    "evidence_excerpt": description,
                    "role_anchor_excerpt": description,
                    "motion_excerpt": "",
                    "performance_excerpt": "",
                    "prop_excerpt": "",
                    "background_excerpt": "",
                    "script_excerpt": script_body,
                    "costume_anchor": costume_anchor,
                }
            )

        shots = group.get("分镜明细", [])
        if not isinstance(shots, list):
            continue

        for shot in shots:
            shot_id = str(shot.get("分镜ID", "unknown"))
            role_motion = (
                stringify_branch_design(pick_branch_object(shot, "运动表现", "动作路径"), ("位置和方向", "逻辑性", "一致性", "位置基线", "动作路径", "连续性说明"))
                or str(shot.get("角色站位走位", "")).strip()
            )
            performance = (
                stringify_branch_design(pick_branch_object(shot, "角色表现", "人物表演锚点"), ("动作戏", "对话戏", "内心戏", "对手戏", "表演目标", "关系施压"))
                or str(shot.get("分镜表现", "")).strip()
            )
            prop_state = str(shot.get("道具及状态", "")).strip()
            background = (
                stringify_branch_design(pick_branch_object(shot, "氛围表现", "空间氛围"), ("层次", "空间诗学", "意境", "空间支架"))
                or str(shot.get("角色背景面", "")).strip()
            )
            visual_anchor = (
                stringify_branch_design(pick_branch_object(shot, "视觉强化", "视觉抓手"), ("冲击力", "观赏性", "品味", "第一抓手", "观看节奏", "镜头消费提示"))
            )
            combined = " ".join([role_motion, performance, prop_state, background, visual_anchor, script_body])

            matched_names = [name for name in group_role_names if name and name in combined]
            if not matched_names and len(group_role_names) == 1 and role_motion:
                matched_names = list(group_role_names)

            for name in matched_names:
                role_entry = role_pool[name]
                role_entry["shot_ids"].append(shot_id)
                role_entry["prop_hints"].extend(collect_prop_hints(prop_state, performance))
                role_entry["evidence_counter"]["shot_presence"] += 1
                shot_evidence_count += 1

                role_specific_excerpts = [
                    excerpt
                    for excerpt in (
                        role_motion if name in role_motion or len(group_role_names) == 1 else "",
                        performance if name in performance else "",
                        prop_state if name in prop_state or any(hint in prop_state for hint in PROP_HINTS) else "",
                        background if name in background else "",
                        visual_anchor if name in visual_anchor else "",
                    )
                    if excerpt
                ]
                evidence_excerpt = clean_excerpt("；".join(role_specific_excerpts or [role_motion or performance or prop_state or background]))

                map_rows.append(
                    {
                        "canonical_name": name,
                        "group_id": group_id,
                        "shot_id": shot_id,
                        "source_slot": "分镜明细",
                        "evidence_excerpt": evidence_excerpt,
                        "role_anchor_excerpt": role_anchor_text,
                        "motion_excerpt": clean_excerpt(role_motion),
                        "performance_excerpt": clean_excerpt(performance),
                        "prop_excerpt": clean_excerpt(prop_state),
                        "background_excerpt": clean_excerpt(background),
                        "script_excerpt": script_body,
                        "costume_anchor": role_entry["costume_anchors"][0] if role_entry["costume_anchors"] else "unknown",
                    }
                )

                for variant in role_entry["costume_variants"]:
                    if variant["costume_anchor"] == role_entry["costume_anchors"][0]:
                        variant["trigger_shot_ids"] = unique_preserve(variant["trigger_shot_ids"] + [shot_id])
                        break

    roles: List[dict] = []
    role_id_map: Dict[str, str] = {}
    for idx, name in enumerate(role_order, start=1):
        role_entry = role_pool[name]
        group_ids = unique_preserve(role_entry["group_ids"])
        shot_ids = unique_preserve(role_entry["shot_ids"])
        costume_anchors = unique_preserve(role_entry["costume_anchors"])
        role_level = role_entry["role_level"]
        role_tier = infer_role_tier(len(group_ids), len(shot_ids), role_level)
        primary_costume = costume_anchors[0] if costume_anchors else "unknown"
        role_id = f"role-{idx:03d}"
        role_id_map[name] = role_id
        roles.append(
            {
                "role_id": role_id,
                "canonical_name": name,
                "role_level": role_level,
                "role_tier": role_tier,
                "costume_state": primary_costume,
                "group_ids": group_ids,
                "shot_ids": shot_ids,
                "first_appearance": role_entry["first_appearance"],
                "costume_variants": role_entry["costume_variants"],
                "prop_hints": unique_preserve(role_entry["prop_hints"]),
                "group_anchor_descriptions": unique_preserve(role_entry["group_anchor_descriptions"]),
                "display_profile": build_display_profile(name, role_tier, primary_costume, len(shot_ids)),
            }
        )

    group_role_map: List[dict] = []
    for row in map_rows:
        group_role_map.append(
            {
                "role_id": role_id_map.get(row["canonical_name"], "unknown"),
                "canonical_name": row["canonical_name"],
                "group_id": row["group_id"],
                "shot_id": row["shot_id"],
                "source_slot": row["source_slot"],
                "evidence_excerpt": row["evidence_excerpt"],
                "role_anchor_excerpt": row["role_anchor_excerpt"],
                "motion_excerpt": row["motion_excerpt"],
                "performance_excerpt": row["performance_excerpt"],
                "prop_excerpt": row["prop_excerpt"],
                "background_excerpt": row["background_excerpt"],
                "script_excerpt": row["script_excerpt"],
                "costume_anchor": row["costume_anchor"],
            }
        )

    statistics = {
        "source_group_count": len(groups),
        "total_roles": len(roles),
        "group_anchor_count": sum(1 for row in group_role_map if not row["shot_id"]),
        "shot_evidence_count": shot_evidence_count,
        "groups_without_role_anchor": unique_preserve(groups_without_role_anchor),
    }

    return {
        "meta": meta,
        "roles": roles,
        "group_role_map": group_role_map,
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
            f"roles={len(catalog.get('roles', []))} "
            f"maps={len(catalog.get('group_role_map', []))} "
            f"output={output_path.as_posix()}"
        )
        return 0

    output_dir.mkdir(parents=True, exist_ok=True)
    write_json(output_path, catalog)
    print(f"[OK] 写入角色清单: {output_path.as_posix()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
