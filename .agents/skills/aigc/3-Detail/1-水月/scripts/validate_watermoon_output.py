#!/usr/bin/env python3
"""Validate `水月` owner bundle output."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


LEGACY_ALLOWED_TARGET_FIELDS = {
    "组间设计.出场角色及穿搭",
    "分镜明细[].角色背景面",
    "分镜明细[].角色站位走位",
    "分镜明细[].道具及状态",
    "beat_patches[].镜头消费提示",
}

BRANCH_KEYS = {"角色表现", "运动表现", "氛围表现", "视觉强化"}
FORBIDDEN_KEYS = {"分镜构图", "摄影美学", "运镜手法", "转场特效"}


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


def contains_hard_truncation(text: object) -> bool:
    normalized = normalize_text(text)
    if not normalized:
        return False
    return "…" in normalized or normalized.endswith("...") or normalized.endswith("……")


def flatten_strings(value: object) -> list[str]:
    results: list[str] = []
    if isinstance(value, str):
        text = normalize_text(value)
        if text:
            results.append(text)
    elif isinstance(value, dict):
        for nested in value.values():
            results.extend(flatten_strings(nested))
    elif isinstance(value, list):
        for nested in value:
            results.extend(flatten_strings(nested))
    return results


def validate_legacy(group: dict[str, object], errors: list[str]) -> None:
    group_id = group.get("group_id", "<missing-group-id>")
    target_fields = set(group.get("target_fields", []))
    disallowed = sorted(target_fields - LEGACY_ALLOWED_TARGET_FIELDS)
    if disallowed:
        errors.append(f"{group_id}: legacy 模式下出现越权 target_fields: {', '.join(disallowed)}")
    missing = sorted(LEGACY_ALLOWED_TARGET_FIELDS - target_fields)
    if missing:
        errors.append(f"{group_id}: legacy 模式下缺少 target_fields: {', '.join(missing)}")


def validate_bundle(group: dict[str, object], errors: list[str]) -> None:
    group_id = group.get("group_id", "<missing-group-id>")
    branch_patches = group.get("branch_patches")
    if not isinstance(branch_patches, dict) or not branch_patches:
        errors.append(f"{group_id}: assembly_only 模式下必须有 `branch_patches`。")
        return

    keys = set(branch_patches)
    if not keys & BRANCH_KEYS:
        errors.append(f"{group_id}: 缺少水月 branch patch。")
    forbidden = sorted(keys & FORBIDDEN_KEYS)
    if forbidden:
        errors.append(f"{group_id}: 不得包含镜花 branch patch: {', '.join(forbidden)}")

    compatibility = group.get("compatibility_projection")
    canonical_texts = []
    for branch_key in BRANCH_KEYS:
        canonical_texts.extend(flatten_strings(branch_patches.get(branch_key, {})))

    if isinstance(compatibility, dict):
        for projection_key, projection_value in compatibility.items():
            if projection_key == "group_design_patch":
                continue
            projection_text = normalize_text(projection_value)
            if not projection_text:
                continue
            if contains_hard_truncation(projection_text):
                errors.append(
                    f"{group_id}: compatibility_projection.`{projection_key}` 出现省略号或半截短语，未完成具像化摘要。"
                )
            for canonical_text in canonical_texts:
                if is_mechanical_duplicate(projection_text, canonical_text):
                    errors.append(
                        f"{group_id}: compatibility_projection.`{projection_key}` 与 canonical branch patch 机械重复，未做摘要化去重。"
                    )
                    break


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
    if metadata.get("patch_owner") != "水月":
        errors.append("metadata.patch_owner 必须为 `水月`。")
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
        description="Validate `3-Detail/水月/第N集.field-patch.json` owner bundle."
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
