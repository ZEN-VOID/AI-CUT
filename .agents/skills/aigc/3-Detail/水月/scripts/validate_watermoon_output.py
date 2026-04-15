#!/usr/bin/env python3
"""Validate `水月` field-patch sidecar output."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


ALLOWED_TARGET_FIELDS = {
    "组间设计.出场角色及穿搭",
    "分镜明细[].角色背景面",
    "分镜明细[].角色站位走位",
    "分镜明细[].道具及状态",
    "beat_patches[].镜头消费提示",
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
    if metadata.get("patch_owner") != "水月":
        errors.append("metadata.patch_owner 必须为 `水月`。")
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
        missing = sorted(ALLOWED_TARGET_FIELDS - target_fields)
        if missing:
            errors.append(f"{group_id}: 缺少必需 target_fields: {', '.join(missing)}")

        if "shot_patches" in group and group.get("shot_patches"):
            errors.append(f"{group_id}: `水月` 不得输出 `shot_patches`。")

        design_patch = group.get("group_design_patch", {})
        for key in design_patch:
            if key != "出场角色及穿搭":
                errors.append(f"{group_id}: `group_design_patch` 只允许 `出场角色及穿搭`。")

        beat_patches = group.get("beat_patches", [])
        if not isinstance(beat_patches, list):
            errors.append(f"{group_id}: `beat_patches` 必须是数组。")
            continue
        for index, beat in enumerate(beat_patches, start=1):
            beat_id = beat.get("beat_id", f"{group_id}-b{index:02d}")
            required = ("anchor_summary", "角色背景面", "角色站位走位", "道具及状态", "镜头消费提示")
            for field in required:
                if not isinstance(beat.get(field), str) or not beat.get(field).strip():
                    errors.append(f"{group_id}/{beat_id}: 缺少 `{field}`。")

        key_set = collect_keys(group)
        forbidden_tokens = ("剧本正文", "分镜ID", "时间段", "景别", "运镜手法", "摄影美学")
        for token in forbidden_tokens:
            if token in key_set:
                errors.append(f"{group_id}: 出现越权字段 `{token}`。")

    return errors


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Validate `3-Detail/水月/第N集.field-patch.json` ownership and structure."
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
