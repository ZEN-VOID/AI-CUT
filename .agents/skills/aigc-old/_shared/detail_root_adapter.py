#!/usr/bin/env python3
"""Adapt canonical `3-Detail` roots to legacy consumer-friendly projections."""

from __future__ import annotations

import re
from typing import Any


CANONICAL_DETAIL_TEMPLATE = ".agents/skills/aigc/3-Detail/_shared/episode_detail.json"
LEGACY_DETAIL_SCHEMA = ".agents/skills/aigc/_shared/director_episode_output.schema.json"
GENERIC_ROLE_TOKENS = {"", "无", "暂无", "未知", "角色", "人物", "主体", "群像", "众人", "人群"}
TIME_RE = re.compile(r"^(?P<start>\d+(?:\.\d+)?)-(?P<end>\d+(?:\.\d+)?)秒$")
ID_SPLIT_RE = re.compile(r"(\d+)")
ROLE_SPLIT_RE = re.compile(r"[、，,；;／/\s]+")


def sort_identifier(value: str) -> tuple[Any, ...]:
    parts = ID_SPLIT_RE.split(str(value))
    output: list[Any] = []
    for part in parts:
        if not part:
            continue
        output.append(int(part) if part.isdigit() else part)
    return tuple(output)


def normalize_text(value: Any) -> str:
    if not isinstance(value, str):
        return ""
    return " ".join(value.strip().split())


def join_non_empty(parts: list[str], sep: str = "，") -> str:
    return sep.join(part for part in parts if part)


def parse_time_window(time_text: Any) -> tuple[float, float]:
    if not isinstance(time_text, str):
        return 0.0, 0.0
    matched = TIME_RE.match(time_text.strip())
    if not matched:
        return 0.0, 0.0
    return float(matched.group("start")), float(matched.group("end"))


def _ordered_shots(group: dict[str, Any]) -> list[tuple[str, dict[str, Any]]]:
    shot_map = group.get("detail", {}).get("分镜列表")
    if not isinstance(shot_map, dict):
        return []
    return sorted(
        (
            (str(shot_id), shot)
            for shot_id, shot in shot_map.items()
            if isinstance(shot, dict)
        ),
        key=lambda item: sort_identifier(item[0]),
    )


def _role_tokens(group: dict[str, Any]) -> list[str]:
    tokens: list[str] = []
    for _, shot in _ordered_shots(group):
        anchor = shot.get("主体锚定")
        if not isinstance(anchor, dict):
            continue
        role_text = normalize_text(anchor.get("角色"))
        if not role_text:
            continue
        for token in ROLE_SPLIT_RE.split(role_text):
            cleaned = token.strip()
            if not cleaned or cleaned in GENERIC_ROLE_TOKENS or cleaned in tokens:
                continue
            tokens.append(cleaned)
    return tokens


def _derive_cast_anchor(group: dict[str, Any]) -> str:
    role_tokens = _role_tokens(group)
    if not role_tokens:
        return "群像:当前组镜头主体"
    return "；".join(f"{token}:当前组镜头主体" for token in role_tokens)


def _derive_group_script(group: dict[str, Any], ordered_shots: list[tuple[str, dict[str, Any]]]) -> str:
    global_block = group.get("global")
    if isinstance(global_block, dict):
        script_body = normalize_text(global_block.get("剧本正文"))
        if script_body:
            return script_body
    snippets: list[str] = []
    for _, shot in ordered_shots:
        snippet = normalize_text(shot.get("剧本正文"))
        if snippet:
            snippets.append(snippet)
    return "\n".join(snippets)


def _build_reference_items(script_body: str, projected_shots: list[dict[str, Any]]) -> tuple[str, list[dict[str, Any]]]:
    references: list[dict[str, Any]] = []
    if not script_body:
        script_body = "\n".join(normalize_text(shot.get("剧本正文")) for shot in projected_shots if normalize_text(shot.get("剧本正文")))
    if not script_body:
        return "", references

    cursor = 0
    fallback_needed = False
    for shot in projected_shots:
        shot_id = str(shot["分镜ID"])
        snippet = normalize_text(shot.get("剧本正文"))
        if not snippet:
            continue
        position = script_body.find(snippet, cursor)
        if position < 0:
            fallback_needed = True
            break
        references.append(
            {
                "beat_id": shot_id,
                "原文片段": snippet,
                "char_range": {"start": position, "end": position + len(snippet)},
            }
        )
        cursor = position + len(snippet)

    if not fallback_needed and references:
        return script_body, references

    rebuilt_parts: list[str] = []
    references = []
    cursor = 0
    for shot in projected_shots:
        shot_id = str(shot["分镜ID"])
        snippet = normalize_text(shot.get("剧本正文"))
        if not snippet:
            continue
        if rebuilt_parts:
            rebuilt_parts.append("\n")
            cursor += 1
        start = cursor
        rebuilt_parts.append(snippet)
        cursor += len(snippet)
        references.append(
            {
                "beat_id": shot_id,
                "原文片段": snippet,
                "char_range": {"start": start, "end": cursor},
            }
        )
    rebuilt_script = "".join(rebuilt_parts)
    return rebuilt_script, references


def _project_motion_branch(shot: dict[str, Any]) -> dict[str, str]:
    anchor = shot.get("主体锚定") if isinstance(shot.get("主体锚定"), dict) else {}
    acting = shot.get("角色表现") if isinstance(shot.get("角色表现"), dict) else {}
    composition = shot.get("分镜构图") if isinstance(shot.get("分镜构图"), dict) else {}
    transition = shot.get("转场特效") if isinstance(shot.get("转场特效"), dict) else {}
    return {
        "位置和方向": join_non_empty(
            [
                normalize_text(anchor.get("角色")),
                normalize_text(anchor.get("场景")),
                normalize_text(anchor.get("道具")),
            ]
        ),
        "逻辑性": normalize_text(acting.get("动作戏")),
        "一致性": join_non_empty(
            [normalize_text(acting.get("对话戏")), normalize_text(acting.get("内心戏"))]
        ),
        "位置基线": normalize_text(composition.get("构图形式")),
        "动作路径": normalize_text(acting.get("动作戏")),
        "连续性说明": join_non_empty(
            [normalize_text(transition.get("组内")), normalize_text(transition.get("组间"))]
        ),
    }


def _project_visual_branch(shot: dict[str, Any]) -> dict[str, str]:
    anchor = shot.get("主体锚定") if isinstance(shot.get("主体锚定"), dict) else {}
    composition = shot.get("分镜构图") if isinstance(shot.get("分镜构图"), dict) else {}
    photo = shot.get("摄影表现") if isinstance(shot.get("摄影表现"), dict) else {}
    camera = shot.get("运镜手法") if isinstance(shot.get("运镜手法"), dict) else {}
    focus = join_non_empty(
        [
            normalize_text(anchor.get("角色")),
            normalize_text(anchor.get("道具")),
            normalize_text(anchor.get("场景")),
        ]
    )
    return {
        "冲击力": normalize_text(anchor.get("道具")) or normalize_text(anchor.get("角色")),
        "观赏性": normalize_text(composition.get("构图形式")),
        "品味": normalize_text(photo.get("质感")),
        "第一抓手": focus,
        "观看节奏": normalize_text(camera.get("速度")) or normalize_text(camera.get("变化")),
        "镜头消费提示": normalize_text(photo.get("光影")) or normalize_text(composition.get("镜头类型")),
    }


def _project_shot(shot_id: str, shot: dict[str, Any]) -> dict[str, Any]:
    start, end = parse_time_window(shot.get("时间"))
    anchor = shot.get("主体锚定") if isinstance(shot.get("主体锚定"), dict) else {}
    composition = shot.get("分镜构图") if isinstance(shot.get("分镜构图"), dict) else {}
    acting = shot.get("角色表现") if isinstance(shot.get("角色表现"), dict) else {}
    atmosphere = shot.get("氛围表现") if isinstance(shot.get("氛围表现"), dict) else {}
    photo = shot.get("摄影表现") if isinstance(shot.get("摄影表现"), dict) else {}
    camera = shot.get("运镜手法") if isinstance(shot.get("运镜手法"), dict) else {}
    transition = shot.get("转场特效") if isinstance(shot.get("转场特效"), dict) else {}
    motion = _project_motion_branch(shot)
    visual = _project_visual_branch(shot)
    script_text = normalize_text(shot.get("剧本正文"))
    return {
        "分镜ID": shot_id,
        "时间": normalize_text(shot.get("时间")),
        "时间段": {"开始秒": start, "结束秒": end},
        "剧本正文": script_text,
        "主体锚定": anchor,
        "分镜构图": composition,
        "运镜手法": camera,
        "角色表现": acting,
        "氛围表现": atmosphere,
        "摄影表现": photo,
        "摄影美学": photo,
        "转场特效": transition,
        "运动表现": motion,
        "视觉强化": visual,
        "人物表演锚点": acting,
        "动作路径": motion,
        "空间氛围": atmosphere,
        "视觉抓手": visual,
        "构图策略": composition,
        "摄影策略": photo,
        "运镜策略": camera,
        "景别": normalize_text(composition.get("景别景深")),
        "镜头视角": normalize_text(composition.get("构图形式")) or normalize_text(composition.get("镜头类型")),
        "镜头速度": normalize_text(camera.get("速度")),
        "道具及状态": normalize_text(anchor.get("道具")),
        "角色站位走位": join_non_empty(
            [
                normalize_text(anchor.get("角色")),
                normalize_text(anchor.get("场景")),
                normalize_text(acting.get("动作戏")),
            ]
        ),
        "角色背景面": normalize_text(atmosphere.get("层次")) or normalize_text(anchor.get("场景")),
        "分镜表现": join_non_empty(
            [
                normalize_text(composition.get("构图形式")),
                normalize_text(acting.get("动作戏")),
                normalize_text(atmosphere.get("意境")),
            ]
        ),
    }


def project_group_to_legacy(group: dict[str, Any]) -> dict[str, Any]:
    group_id = normalize_text(group.get("分镜组ID"))
    ordered_shots = _ordered_shots(group)
    projected_shots = [_project_shot(shot_id, shot) for shot_id, shot in ordered_shots]
    detail_block = group.get("detail") if isinstance(group.get("detail"), dict) else {}
    declared_shot_count = detail_block.get("分镜数") if isinstance(detail_block.get("分镜数"), int) else len(projected_shots)
    script_body = _derive_group_script(group, ordered_shots)
    script_body, references = _build_reference_items(script_body, projected_shots)
    for shot in projected_shots:
        shot["正文回指"] = {
            "beat_refs": [shot["分镜ID"]],
            "coverage_mode": "direct",
            "strategy_note": "",
        }
    global_block = group.get("global") if isinstance(group.get("global"), dict) else {}
    return {
        "分镜组ID": group_id,
        "剧本正文": script_body,
        "正文切分参考": references,
        "组间设计": {
            "全局风格": normalize_text(global_block.get("全局风格")),
            "类型元素": normalize_text(global_block.get("类型元素")),
            "导演意图": normalize_text(global_block.get("导演意图")),
            "出场角色及穿搭": _derive_cast_anchor(group),
        },
        "分镜切换": declared_shot_count,
        "分镜明细": projected_shots,
    }


def infer_episode_id(payload: dict[str, Any]) -> str:
    meta = payload.get("meta") if isinstance(payload.get("meta"), dict) else {}
    episode_id = normalize_text(meta.get("集数"))
    return episode_id or "第1集"


def infer_phase(projected_groups: list[dict[str, Any]]) -> str:
    if not projected_groups:
        return "detail_in_progress"
    for group in projected_groups:
        if not group.get("分镜明细"):
            return "detail_in_progress"
        if group.get("分镜切换") != len(group.get("分镜明细", [])):
            return "detail_in_progress"
        for shot in group["分镜明细"]:
            required = (
                normalize_text(shot.get("时间")),
                normalize_text(shot.get("剧本正文")),
                normalize_text(shot.get("景别")),
                normalize_text(shot.get("镜头视角")),
            )
            if not all(required):
                return "detail_in_progress"
    return "ready"


def project_detail_root_to_legacy(payload: dict[str, Any]) -> dict[str, Any]:
    raw_groups = payload.get("groups")
    if not isinstance(raw_groups, list):
        raise ValueError("canonical 3-Detail root 缺少 `groups[]`。")
    projected_groups = [
        project_group_to_legacy(group)
        for group in sorted(
            (item for item in raw_groups if isinstance(item, dict)),
            key=lambda item: sort_identifier(str(item.get("分镜组ID", ""))),
        )
    ]
    episode_id = infer_episode_id(payload)
    return {
        "metadata": {
            "episode_id": episode_id,
            "document_phase": infer_phase(projected_groups),
        },
        "final_output": {
            "main_content": {
                "分镜组列表": projected_groups,
            }
        },
    }


def ensure_legacy_detail_payload(payload: dict[str, Any]) -> dict[str, Any]:
    if isinstance(payload.get("final_output"), dict):
        return payload
    if isinstance(payload.get("groups"), list) and isinstance(payload.get("meta"), dict):
        return project_detail_root_to_legacy(payload)
    raise ValueError("输入 JSON 既不是 legacy director root，也不是 canonical `3-Detail` detail root。")
