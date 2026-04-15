#!/usr/bin/env python3
"""Validate merged `3-Detail` stage output and acceptance artifacts."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


EPISODE_SCHEMA_VERSION = "aigc/director-episode-output/v1"
DETAIL_PATCH_SCHEMA_VERSION = "aigc/detail-patch-sidecar/v1"
ALLOWED_PHASES = {"detail_in_progress", "ready"}
REQUIRED_GROUP_KEYS = (
    "分镜组ID",
    "总时长",
    "剧本正文",
    "组间设计",
    "分镜切换",
    "分镜明细",
)
REQUIRED_DESIGN_KEYS = ("全局风格", "类型元素", "导演意图", "出场角色及穿搭")
REQUIRED_SHOT_KEYS = (
    "分镜ID",
    "时间段",
    "角色背景面",
    "角色站位走位",
    "道具及状态",
    "分镜表现",
    "运镜手法",
    "摄影美学",
)
REQUIRED_WATERMOON_TARGET_FIELDS = {
    "组间设计.出场角色及穿搭",
    "分镜明细[].角色背景面",
    "分镜明细[].角色站位走位",
    "分镜明细[].道具及状态",
    "beat_patches[].镜头消费提示",
}
REQUIRED_JINGHUA_TARGET_FIELDS = {
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
REQUIRED_REPORT_SECTIONS = (
    "## Layered Trace",
    "## Closure Triad",
    "## 已执行校验",
)


def load_json(path: Path) -> object:
    return json.loads(path.read_text(encoding="utf-8"))


def derive_sidecar_path(episode_path: Path, owner: str) -> Path:
    stage_root = episode_path.parent
    return stage_root / owner / f"{episode_path.stem}.field-patch.json"


def derive_report_path(episode_path: Path) -> Path:
    return episode_path.parent / "validation-report.md"


def validate_episode_shell(data: object, episode_path: Path) -> tuple[list[str], dict[str, dict[str, object]], str]:
    errors: list[str] = []
    groups_by_id: dict[str, dict[str, object]] = {}

    if not isinstance(data, dict):
        return ["episode JSON 顶层必须是对象。"], groups_by_id, ""

    metadata = data.get("metadata")
    final_output = data.get("final_output")

    if not isinstance(metadata, dict):
        errors.append("缺少 `metadata` 对象。")
        metadata = {}
    if not isinstance(final_output, dict):
        errors.append("缺少 `final_output` 对象。")
        final_output = {}

    if metadata.get("schema_version") != EPISODE_SCHEMA_VERSION:
        errors.append(f"metadata.schema_version 必须为 `{EPISODE_SCHEMA_VERSION}`。")
    if metadata.get("skill_id") != "aigc-detail":
        errors.append("metadata.skill_id 必须为 `aigc-detail`。")

    phase = metadata.get("document_phase")
    if phase not in ALLOWED_PHASES:
        errors.append(f"metadata.document_phase 必须属于 {sorted(ALLOWED_PHASES)}。")
        phase = ""

    if final_output.get("deliverable_type") != "director_episode_output":
        errors.append("final_output.deliverable_type 必须为 `director_episode_output`。")

    main_content = final_output.get("main_content")
    if not isinstance(main_content, dict):
        errors.append("final_output.main_content 必须是对象。")
        return errors, groups_by_id, phase

    groups = main_content.get("分镜组列表")
    if not isinstance(groups, list) or not groups:
        errors.append("final_output.main_content.分镜组列表 必须是非空数组。")
        return errors, groups_by_id, phase

    acceptance_notes = final_output.get("acceptance_notes")
    if not isinstance(acceptance_notes, list) or not acceptance_notes:
        errors.append("final_output.acceptance_notes 必须是非空数组。")

    for index, group in enumerate(groups, start=1):
        if not isinstance(group, dict):
            errors.append(f"第 {index} 个分镜组必须是对象。")
            continue
        group_id = str(group.get("分镜组ID", f"<missing-{index}>"))
        groups_by_id[group_id] = group

        for key in REQUIRED_GROUP_KEYS:
            if key not in group:
                errors.append(f"{group_id}: 缺少 `{key}`。")

        design = group.get("组间设计")
        if not isinstance(design, dict):
            errors.append(f"{group_id}: `组间设计` 必须是对象。")
        else:
            for key in REQUIRED_DESIGN_KEYS:
                if key not in design:
                    errors.append(f"{group_id}: `组间设计` 缺少 `{key}`。")

        shot_count = group.get("分镜切换")
        details = group.get("分镜明细")
        if not isinstance(details, list):
            errors.append(f"{group_id}: `分镜明细` 必须是数组。")
            continue
        if not isinstance(shot_count, int) or shot_count < 1:
            errors.append(f"{group_id}: `分镜切换` 必须是 >= 1 的整数。")
        elif phase == "ready" and len(details) != shot_count:
            errors.append(f"{group_id}: `ready` 状态下 `分镜切换`({shot_count}) 必须等于 `分镜明细` 数量({len(details)})。")

        previous_end = 0.0
        total_duration = group.get("总时长")
        for shot_index, shot in enumerate(details, start=1):
            if not isinstance(shot, dict):
                errors.append(f"{group_id}: 第 {shot_index} 个 `分镜明细` 必须是对象。")
                continue
            shot_id = str(shot.get("分镜ID", f"{group_id}-{shot_index}"))
            for key in REQUIRED_SHOT_KEYS:
                if key not in shot:
                    errors.append(f"{group_id}/{shot_id}: 缺少 `{key}`。")

            time_range = shot.get("时间段")
            if not isinstance(time_range, dict):
                errors.append(f"{group_id}/{shot_id}: `时间段` 必须是对象。")
                continue
            start = time_range.get("开始秒")
            end = time_range.get("结束秒")
            if not isinstance(start, (int, float)) or not isinstance(end, (int, float)):
                errors.append(f"{group_id}/{shot_id}: `时间段` 必须包含数值型 `开始秒 / 结束秒`。")
                continue
            if end < start:
                errors.append(f"{group_id}/{shot_id}: `结束秒` 不得小于 `开始秒`。")
            if shot_index == 1 and start != 0:
                errors.append(f"{group_id}/{shot_id}: 组内首镜 `开始秒` 必须为 0。")
            if start < previous_end:
                errors.append(f"{group_id}/{shot_id}: `开始秒` 不得早于上一镜结束秒。")
            previous_end = float(end)

        if phase == "ready" and isinstance(total_duration, (int, float)) and details:
            last_end = details[-1].get("时间段", {}).get("结束秒")
            if isinstance(last_end, (int, float)) and abs(float(last_end) - float(total_duration)) > 1e-6:
                errors.append(f"{group_id}: `ready` 状态下最后一镜结束秒({last_end}) 必须与 `总时长`({total_duration}) 对齐。")

    return errors, groups_by_id, phase


def validate_watermoon_sidecar(
    data: object,
    groups_by_id: dict[str, dict[str, object]],
) -> tuple[list[str], dict[str, set[str]]]:
    errors: list[str] = []
    beat_ids_by_group: dict[str, set[str]] = {}

    if not isinstance(data, dict):
        return ["水月 sidecar 顶层必须是对象。"], beat_ids_by_group

    metadata = data.get("metadata", {})
    if metadata.get("schema_version") != DETAIL_PATCH_SCHEMA_VERSION:
        errors.append(f"水月 sidecar schema_version 必须为 `{DETAIL_PATCH_SCHEMA_VERSION}`。")
    if metadata.get("patch_owner") != "水月":
        errors.append("水月 sidecar metadata.patch_owner 必须为 `水月`。")

    groups = data.get("group_patches")
    if not isinstance(groups, list) or not groups:
        return ["水月 sidecar `group_patches` 必须是非空数组。"], beat_ids_by_group

    for group in groups:
        if not isinstance(group, dict):
            errors.append("水月 sidecar 的 `group_patches[]` 元素必须是对象。")
            continue
        group_id = str(group.get("group_id", "<missing-group-id>"))
        if group_id not in groups_by_id:
            errors.append(f"水月 sidecar 命中未知 group_id: {group_id}")
        target_fields = set(group.get("target_fields", []))
        if target_fields != REQUIRED_WATERMOON_TARGET_FIELDS:
            errors.append(f"{group_id}: 水月 target_fields 必须精确等于 {sorted(REQUIRED_WATERMOON_TARGET_FIELDS)}。")

        beat_ids: set[str] = set()
        beat_patches = group.get("beat_patches")
        if not isinstance(beat_patches, list) or not beat_patches:
            errors.append(f"{group_id}: 水月 `beat_patches` 必须是非空数组。")
            continue
        for beat_index, beat in enumerate(beat_patches, start=1):
            if not isinstance(beat, dict):
                errors.append(f"{group_id}: 第 {beat_index} 个 beat patch 必须是对象。")
                continue
            beat_id = beat.get("beat_id")
            expected_prefix = f"{group_id}-b"
            if not isinstance(beat_id, str) or not beat_id.startswith(expected_prefix):
                errors.append(f"{group_id}: beat_id `{beat_id}` 必须遵循 `<group_id>-bNN`。")
                continue
            if beat_id in beat_ids:
                errors.append(f"{group_id}: beat_id 重复 `{beat_id}`。")
            beat_ids.add(beat_id)
        beat_ids_by_group[group_id] = beat_ids

    return errors, beat_ids_by_group


def validate_jinghua_sidecar(
    data: object,
    groups_by_id: dict[str, dict[str, object]],
    beat_ids_by_group: dict[str, set[str]],
    phase: str,
) -> list[str]:
    errors: list[str] = []

    if not isinstance(data, dict):
        return ["镜花 sidecar 顶层必须是对象。"]

    metadata = data.get("metadata", {})
    if metadata.get("schema_version") != DETAIL_PATCH_SCHEMA_VERSION:
        errors.append(f"镜花 sidecar schema_version 必须为 `{DETAIL_PATCH_SCHEMA_VERSION}`。")
    if metadata.get("patch_owner") != "镜花":
        errors.append("镜花 sidecar metadata.patch_owner 必须为 `镜花`。")

    groups = data.get("group_patches")
    if not isinstance(groups, list) or not groups:
        return ["镜花 sidecar `group_patches` 必须是非空数组。"]

    for group in groups:
        if not isinstance(group, dict):
            errors.append("镜花 sidecar 的 `group_patches[]` 元素必须是对象。")
            continue
        group_id = str(group.get("group_id", "<missing-group-id>"))
        storyboard_group = groups_by_id.get(group_id)
        if storyboard_group is None:
            errors.append(f"镜花 sidecar 命中未知 group_id: {group_id}")
            continue

        target_fields = set(group.get("target_fields", []))
        if target_fields != REQUIRED_JINGHUA_TARGET_FIELDS:
            errors.append(f"{group_id}: 镜花 target_fields 必须精确等于 {sorted(REQUIRED_JINGHUA_TARGET_FIELDS)}。")

        shot_patches = group.get("shot_patches")
        if not isinstance(shot_patches, list) or not shot_patches:
            errors.append(f"{group_id}: 镜花 `shot_patches` 必须是非空数组。")
            continue

        if phase == "ready":
            expected = storyboard_group.get("分镜切换")
            if isinstance(expected, int) and len(shot_patches) != expected:
                errors.append(f"{group_id}: `ready` 状态下镜花 shot_patches 数量({len(shot_patches)}) 必须等于 `分镜切换`({expected})。")

        group_beat_ids = beat_ids_by_group.get(group_id, set())
        for shot_index, shot in enumerate(shot_patches, start=1):
            if not isinstance(shot, dict):
                errors.append(f"{group_id}: 第 {shot_index} 个 shot patch 必须是对象。")
                continue
            shot_id = str(shot.get("分镜ID", f"{group_id}-{shot_index}"))
            beat_refs = shot.get("beat_refs")
            if not isinstance(beat_refs, list) or not beat_refs:
                errors.append(f"{group_id}/{shot_id}: `beat_refs` 必须是非空数组。")
                continue
            unknown = sorted(ref for ref in beat_refs if ref not in group_beat_ids)
            if unknown:
                errors.append(f"{group_id}/{shot_id}: `beat_refs` 引用了未知 beat_id: {', '.join(unknown)}")

    return errors


def validate_report(
    report_path: Path,
    episode_path: Path,
    watermoon_path: Path,
    jinghua_path: Path,
) -> list[str]:
    errors: list[str] = []
    if not report_path.exists():
        return [f"缺少阶段 validation-report: {report_path}"]

    text = report_path.read_text(encoding="utf-8")
    for section in REQUIRED_REPORT_SECTIONS:
        if section not in text:
            errors.append(f"validation-report 缺少章节 `{section}`。")

    expected_tokens = (
        episode_path.name,
        watermoon_path.name,
        jinghua_path.name,
        "Layered Trace",
        "Closure Triad",
    )
    for token in expected_tokens:
        if token not in text:
            errors.append(f"validation-report 未提及 `{token}`。")

    return errors


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Validate merged `3-Detail` stage output, child sidecars, and validation-report."
    )
    parser.add_argument("episode_json", type=Path, help="Path to `projects/aigc/<项目名>/3-Detail/第N集.json`.")
    parser.add_argument("--watermoon", type=Path, help="Override `水月` sidecar path.")
    parser.add_argument("--jinghua", type=Path, help="Override `镜花` sidecar path.")
    parser.add_argument("--report", type=Path, help="Override `validation-report.md` path.")
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()

    episode_path = args.episode_json.resolve()
    watermoon_path = (args.watermoon or derive_sidecar_path(episode_path, "水月")).resolve()
    jinghua_path = (args.jinghua or derive_sidecar_path(episode_path, "镜花")).resolve()
    report_path = (args.report or derive_report_path(episode_path)).resolve()

    missing_paths = [path for path in (episode_path, watermoon_path, jinghua_path) if not path.exists()]
    if missing_paths:
        for path in missing_paths:
            print(f"文件不存在: {path}")
        return 1

    errors: list[str] = []
    episode_errors, groups_by_id, phase = validate_episode_shell(load_json(episode_path), episode_path)
    errors.extend(episode_errors)

    watermoon_errors, beat_ids_by_group = validate_watermoon_sidecar(load_json(watermoon_path), groups_by_id)
    errors.extend(watermoon_errors)
    errors.extend(validate_jinghua_sidecar(load_json(jinghua_path), groups_by_id, beat_ids_by_group, phase))
    errors.extend(validate_report(report_path, episode_path, watermoon_path, jinghua_path))

    if errors:
        print("校验失败:")
        for error in errors:
            print(f"- {error}")
        return 1

    print(
        "校验通过。"
        f" episode={episode_path.name}"
        f" phase={phase}"
        f" watermoon={watermoon_path.name}"
        f" jinghua={jinghua_path.name}"
        f" report={report_path.name}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
