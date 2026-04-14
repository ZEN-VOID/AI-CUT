#!/usr/bin/env python3
"""Validate `镜花` field-patch sidecar output."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


ALLOWED_TARGET_FIELDS = {
    "分镜明细[].分镜ID",
    "分镜明细[].时间段",
    "分镜明细[].景别",
    "分镜明细[].镜头属性",
    "分镜明细[].镜头框架",
    "分镜明细[].镜头类型",
    "分镜明细[].镜头视角",
    "分镜明细[].运镜手法",
    "分镜明细[].镜头速度",
    "分镜明细[].摄影美学",
    "分镜明细[].转场特效",
}


def collect_keys(value: object) -> set[str]:
    keys: set[str] = set()
    if isinstance(value, dict):
        for key, nested in value.items():
            keys.add(str(key))
            keys.update(collect_keys(nested))
    elif isinstance(value, list):
        for item in value:
            keys.update(collect_keys(item))
    return keys


def validate_file(path: Path) -> list[str]:
    errors: list[str] = []
    data = json.loads(path.read_text(encoding="utf-8"))

    metadata = data.get("metadata", {})
    if metadata.get("schema_version") != "aigc/detail-patch-sidecar/v1":
        errors.append("metadata.schema_version 必须为 `aigc/detail-patch-sidecar/v1`。")
    if metadata.get("patch_owner") != "镜花":
        errors.append("metadata.patch_owner 必须为 `镜花`。")
    if metadata.get("script_body_policy") != "inherit_only":
        errors.append("metadata.script_body_policy 必须为 `inherit_only`。")

    groups = data.get("group_patches")
    if not isinstance(groups, list):
        return ["`group_patches` 必须是数组。"]

    for group in groups:
        group_id = group.get("group_id", "<missing-group-id>")
        target_fields = set(group.get("target_fields", []))
        disallowed = sorted(target_fields - ALLOWED_TARGET_FIELDS)
        if disallowed:
            errors.append(f"{group_id}: 出现越权 target_fields: {', '.join(disallowed)}")

        if group.get("group_design_patch"):
            errors.append(f"{group_id}: `镜花` 不得输出 `group_design_patch`。")
        if group.get("beat_patches"):
            errors.append(f"{group_id}: `镜花` 不得输出 `beat_patches`。")

        shot_patches = group.get("shot_patches", [])
        if not isinstance(shot_patches, list) or not shot_patches:
            errors.append(f"{group_id}: `shot_patches` 必须是非空数组。")
            continue
        for index, shot in enumerate(shot_patches, start=1):
            shot_id = shot.get("分镜ID", f"{group_id}-{index}")
            required = ("slot_id", "分镜ID", "beat_refs", "时间段", "景别", "镜头属性", "镜头框架", "镜头类型", "镜头视角", "运镜手法", "摄影美学")
            for field in required:
                if field not in shot:
                    errors.append(f"{group_id}/{shot_id}: 缺少 `{field}`。")
            if not isinstance(shot.get("beat_refs"), list) or not shot.get("beat_refs"):
                errors.append(f"{group_id}/{shot_id}: `beat_refs` 必须是非空数组。")
            time_range = shot.get("时间段", {})
            if not isinstance(time_range, dict) or "开始秒" not in time_range or "结束秒" not in time_range:
                errors.append(f"{group_id}/{shot_id}: `时间段` 必须包含 `开始秒 / 结束秒`。")

        key_set = collect_keys(group)
        forbidden_tokens = ("剧本正文", "出场角色及穿搭", "角色背景面", "角色站位走位", "道具及状态", "分镜表现", "镜头消费提示", "分镜切换")
        for token in forbidden_tokens:
            if token in key_set:
                errors.append(f"{group_id}: 出现越权字段 `{token}`。")

    return errors


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Validate `3-Detail/镜花/第N集.field-patch.json` ownership and structure."
    )
    parser.add_argument("path", type=Path, help="Target JSON patch file path.")
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
