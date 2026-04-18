#!/usr/bin/env python3
"""Validate `3-Detail` branch process sidecar output."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


ALLOWED_BRANCH_TO_PATHS = {
    "角色表现": {
        "final_output.main_content.分镜组列表[].分镜明细[].角色表现",
        "final_output.main_content.分镜组列表[].分镜明细[].人物表演锚点",
        "final_output.main_content.分镜组列表[].分镜明细[].人物表演",
    },
    "运动表现": {
        "final_output.main_content.分镜组列表[].分镜明细[].运动表现",
        "final_output.main_content.分镜组列表[].分镜明细[].动作路径",
        "final_output.main_content.分镜组列表[].分镜明细[].动作调度",
    },
    "氛围表现": {
        "final_output.main_content.分镜组列表[].分镜明细[].氛围表现",
        "final_output.main_content.分镜组列表[].分镜明细[].空间氛围",
    },
    "视觉强化": {
        "final_output.main_content.分镜组列表[].分镜明细[].视觉强化",
        "final_output.main_content.分镜组列表[].分镜明细[].视觉抓手",
        "final_output.main_content.分镜组列表[].分镜明细[].视觉焦点",
    },
    "分镜构图": {
        "final_output.main_content.分镜组列表[].分镜明细[].分镜构图",
        "final_output.main_content.分镜组列表[].分镜明细[].构图骨架",
        "final_output.main_content.分镜组列表[].分镜明细[].构图策略",
    },
    "摄影美学": {
        "final_output.main_content.分镜组列表[].分镜明细[].摄影美学",
        "final_output.main_content.分镜组列表[].分镜明细[].摄影策略",
    },
    "运镜手法": {
        "final_output.main_content.分镜组列表[].分镜明细[].运镜手法",
        "final_output.main_content.分镜组列表[].分镜明细[].运镜策略",
    },
    "转场特效": {
        "final_output.main_content.分镜组列表[].分镜明细[].转场特效",
        "final_output.main_content.分镜组列表[].分镜明细[].转场策略",
    },
}

PARENT_BY_BRANCH = {
    "角色表现": "水月",
    "运动表现": "水月",
    "氛围表现": "水月",
    "视觉强化": "水月",
    "分镜构图": "镜花",
    "摄影美学": "镜花",
    "运镜手法": "镜花",
    "转场特效": "镜花",
}

BRANCH_REQUIRED_SLOT_MAP = {
    "角色表现": ("动作戏", "内心戏"),
    "运动表现": ("逻辑性", "位置和方向", "一致性"),
    "氛围表现": ("层次", "空间诗学", "意境"),
    "视觉强化": ("冲击力", "观赏性", "品味"),
    "分镜构图": ("景别景深", "镜头类型", "构图形式"),
    "摄影美学": ("光影", "色彩", "质感"),
    "运镜手法": ("变化", "速度", "组合"),
}

BRANCH_OPTIONAL_SLOT_MAP = {
    "角色表现": (("对话戏", "对手戏"),),
}


def normalize_text(value: object) -> str:
    if not isinstance(value, str):
        return ""
    return " ".join(value.strip().split())


def is_mechanical_duplicate(left: str, right: str) -> bool:
    if not left or not right:
        return False
    if left == right:
        return True
    shorter = min(len(left), len(right))
    if shorter < 12:
        return False
    return left in right or right in left


def validate_branch_slot_semantics(
    branch_owner: str, group_id: object, patch_payload: object, errors: list[str]
) -> None:
    required_slots = BRANCH_REQUIRED_SLOT_MAP.get(branch_owner)
    if not required_slots or not isinstance(patch_payload, dict):
        return
    optional_slots = BRANCH_OPTIONAL_SLOT_MAP.get(branch_owner, ())

    if branch_owner == "角色表现":
        pairs = (
            ("动作戏", "内心戏"),
            ("动作戏", "对话戏"),
            ("对话戏", "内心戏"),
        )
    elif branch_owner == "运动表现":
        pairs = (
            ("逻辑性", "位置和方向"),
            ("逻辑性", "一致性"),
            ("位置和方向", "一致性"),
        )
    elif branch_owner == "氛围表现":
        pairs = (
            ("层次", "空间诗学"),
            ("层次", "意境"),
            ("空间诗学", "意境"),
        )
    elif branch_owner == "视觉强化":
        pairs = (
            ("冲击力", "观赏性"),
            ("冲击力", "品味"),
            ("观赏性", "品味"),
        )
    elif branch_owner == "分镜构图":
        pairs = (
            ("景别景深", "镜头类型"),
            ("景别景深", "构图形式"),
            ("镜头类型", "构图形式"),
        )
    elif branch_owner == "摄影美学":
        pairs = (
            ("光影", "色彩"),
            ("光影", "质感"),
            ("色彩", "质感"),
        )
    elif branch_owner == "运镜手法":
        pairs = (
            ("变化", "速度"),
            ("变化", "组合"),
            ("速度", "组合"),
        )
    else:
        pairs = ()

    if "shot_patches" in patch_payload and isinstance(patch_payload["shot_patches"], dict):
        shot_payloads = patch_payload["shot_patches"].items()
    else:
        shot_payloads = [("<group-level>", patch_payload)]

    for shot_id, shot_payload in shot_payloads:
        if not isinstance(shot_payload, dict):
            errors.append(f"{group_id}/{shot_id}: `{branch_owner}` patch 必须是对象。")
            continue
        slot_values: dict[str, str] = {}
        for slot in required_slots:
            value = shot_payload.get(slot)
            if not isinstance(value, str) or not normalize_text(value):
                errors.append(f"{group_id}/{shot_id}: `{branch_owner}` 缺少有效槽位 `{slot}`。")
            else:
                slot_values[slot] = normalize_text(value)

        for slot_group in optional_slots:
            for slot in slot_group:
                value = shot_payload.get(slot)
                if isinstance(value, str) and normalize_text(value):
                    canonical_slot = slot_group[0]
                    slot_values[canonical_slot] = normalize_text(value)
                    break

        for left_slot, right_slot in pairs:
            left = slot_values.get(left_slot, "")
            right = slot_values.get(right_slot, "")
            if is_mechanical_duplicate(left, right):
                errors.append(
                    f"{group_id}/{shot_id}: `{branch_owner}` 的 `{left_slot}` 与 `{right_slot}` 出现机械复写，未形成槽位分工。"
                )


def validate_file(path: Path) -> list[str]:
    errors: list[str] = []
    data = json.loads(path.read_text(encoding="utf-8"))

    metadata = data.get("metadata", {})
    if metadata.get("schema_version") != "aigc/detail-branch-process-sidecar/v1":
        errors.append("metadata.schema_version 必须为 `aigc/detail-branch-process-sidecar/v1`。")

    branch_owner = metadata.get("branch_owner")
    parent_owner = metadata.get("parent_owner")
    if branch_owner not in ALLOWED_BRANCH_TO_PATHS:
        errors.append(f"metadata.branch_owner 非法: {branch_owner}")
    else:
        expected_parent = PARENT_BY_BRANCH[branch_owner]
        if parent_owner != expected_parent:
            errors.append(f"{branch_owner}: metadata.parent_owner 必须为 `{expected_parent}`。")

    if metadata.get("review_status") not in {"pending", "reviewed", "blocked"}:
        errors.append("metadata.review_status 必须属于 `pending|reviewed|blocked`。")

    groups = data.get("group_branch_patches")
    if not isinstance(groups, list) or not groups:
        return ["`group_branch_patches` 必须是非空数组。"]

    allowed_paths = ALLOWED_BRANCH_TO_PATHS.get(branch_owner, set())
    for group in groups:
        if not isinstance(group, dict):
            errors.append("`group_branch_patches[]` 元素必须是对象。")
            continue
        group_id = group.get("group_id", "<missing-group-id>")
        target_paths = set(group.get("target_json_paths", []))
        if not target_paths:
            errors.append(f"{group_id}: `target_json_paths` 不得为空。")
        disallowed = sorted(target_paths - allowed_paths)
        if disallowed:
            errors.append(f"{group_id}: 出现越权 target path: {', '.join(disallowed)}")

        thinking = group.get("thinking_process")
        if not isinstance(thinking, dict):
            errors.append(f"{group_id}: 缺少 `thinking_process`。")
        else:
            for key in ("context_anchor", "creative_thesis", "execution_steps", "self_check"):
                if key not in thinking:
                    errors.append(f"{group_id}: `thinking_process` 缺少 `{key}`。")

        patch_payload = group.get("patch_payload")
        if not isinstance(patch_payload, dict) or not patch_payload:
            errors.append(f"{group_id}: `patch_payload` 必须是非空对象。")
        else:
            validate_branch_slot_semantics(branch_owner, group_id, patch_payload, errors)

        review_trace = group.get("review_trace")
        if not isinstance(review_trace, dict):
            errors.append(f"{group_id}: 缺少 `review_trace`。")
        else:
            for key in ("requested_reviewers", "key_findings", "apply_decision"):
                if key not in review_trace:
                    errors.append(f"{group_id}: `review_trace` 缺少 `{key}`。")

    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate `3-Detail` branch process sidecar.")
    parser.add_argument("path", type=Path, help="Path to `<branch>/第N集.branch-patch.json`.")
    args = parser.parse_args()

    if not args.path.exists():
        print(f"文件不存在: {args.path}")
        return 1

    try:
        errors = validate_file(args.path)
    except json.JSONDecodeError as exc:
        print(f"JSON 解析失败: {exc}")
        return 1

    if errors:
        print("校验失败:")
        for error in errors:
            print(f"- {error}")
        return 1

    print("校验通过。")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
