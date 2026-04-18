#!/usr/bin/env python3
"""Validate `镜花` owner bundle output."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


LEGACY_ALLOWED_TARGET_FIELDS = {
    "分镜明细[].分镜构图",
    "分镜明细[].分镜ID",
    "分镜明细[].时间段",
    "分镜明细[].景别",
    "分镜明细[].镜头框架",
    "分镜明细[].镜头类型",
    "分镜明细[].镜头视角",
    "分镜明细[].运镜手法",
    "分镜明细[].镜头速度",
    "分镜明细[].摄影美学",
    "分镜明细[].转场特效",
}

BRANCH_KEYS = {"分镜构图", "摄影美学", "运镜手法", "转场特效"}
FORBIDDEN_KEYS = {"角色表现", "运动表现", "氛围表现", "视觉强化"}


def validate_legacy(group: dict[str, object], errors: list[str]) -> None:
    group_id = group.get("group_id", "<missing-group-id>")
    target_fields = set(group.get("target_fields", []))
    disallowed = sorted(target_fields - LEGACY_ALLOWED_TARGET_FIELDS)
    if disallowed:
        errors.append(f"{group_id}: legacy 模式下出现越权 target_fields: {', '.join(disallowed)}")


def validate_bundle(group: dict[str, object], errors: list[str]) -> None:
    group_id = group.get("group_id", "<missing-group-id>")
    branch_patches = group.get("branch_patches")
    if not isinstance(branch_patches, dict) or not branch_patches:
        errors.append(f"{group_id}: assembly_only 模式下必须有 `branch_patches`。")
        return

    keys = set(branch_patches)
    if "分镜构图" not in keys:
        errors.append(f"{group_id}: 缺少 `分镜构图` branch patch。")
    forbidden = sorted(keys & FORBIDDEN_KEYS)
    if forbidden:
        errors.append(f"{group_id}: 不得包含水月 branch patch: {', '.join(forbidden)}")


def validate_file(path: Path) -> list[str]:
    errors: list[str] = []
    data = json.loads(path.read_text(encoding="utf-8"))

    metadata = data.get("metadata", {})
    schema_version = metadata.get("schema_version")
    if schema_version not in {
        "aigc/detail-patch-sidecar/v1",
        "aigc/detail-branch-bundle-sidecar/v1",
    }:
        errors.append("metadata.schema_version 非法。")
    if metadata.get("patch_owner") != "镜花":
        errors.append("metadata.patch_owner 必须为 `镜花`。")
    if metadata.get("script_body_policy") != "inherit_only":
        errors.append("metadata.script_body_policy 必须为 `inherit_only`。")

    bundle_mode = metadata.get("bundle_mode", "legacy_merge")
    if schema_version == "aigc/detail-branch-bundle-sidecar/v1" and bundle_mode != "assembly_only":
        errors.append("新 bundle schema 必须声明 `bundle_mode=assembly_only`。")

    groups = data.get("group_patches")
    if not isinstance(groups, list):
        return ["`group_patches` 必须是数组。"]

    if schema_version == "aigc/detail-branch-bundle-sidecar/v1":
        branch_sidecars = data.get("branch_sidecars")
        if not isinstance(branch_sidecars, list) or not branch_sidecars:
            errors.append("assembly_only 模式下 `branch_sidecars` 必须是非空数组。")

    for group in groups:
        if not isinstance(group, dict):
            errors.append("`group_patches[]` 元素必须是对象。")
            continue
        if schema_version == "aigc/detail-branch-bundle-sidecar/v1":
            validate_bundle(group, errors)
        else:
            validate_legacy(group, errors)

    return errors


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Validate `3-Detail/镜花/第N集.field-patch.json` owner bundle."
    )
    parser.add_argument("path", type=Path, help="Target JSON bundle path.")
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
