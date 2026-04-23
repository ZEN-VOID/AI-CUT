#!/usr/bin/env python3
"""Validate canonical `3-Detail` stage output and validation-report."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path


TIME_RE = re.compile(r"^\d+(?:\.\d+)?-\d+(?:\.\d+)?秒$")
ROOT_META_KEYS = ("剧名", "集数", "组数", "总时长")
GROUP_GLOBAL_KEYS = ("全局风格", "类型元素", "导演意图")
ANCHOR_KEYS = ("场景", "角色", "道具")
SHOT_FIELD_KEYS = ("时间", "剧本正文", "主体锚定", "分镜构图", "运镜手法", "角色表现", "氛围表现", "摄影表现", "转场特效")
TRIPLE_KEYS = ("构图形式", "景别景深", "镜头类型")
CAMERA_KEYS = ("变化", "速度", "组合")
PERFORMANCE_KEYS = ("动作戏", "对话戏", "内心戏")
ATMOSPHERE_KEYS = ("层次", "空间诗学", "意境")
PHOTO_KEYS = ("光影", "色彩", "质感")
TRANSITION_KEYS = ("特效", "组内", "组间")
LEGACY_TRANSITION_KEYS = ("切接逻辑", "组内衔接", "组间或特效策略")
REPORT_SECTIONS = (
    "## Layered Trace",
    "## Closure Triad",
    "## 已执行校验",
    "## Academy Knowledge Evidence",
)
ACADEMY_REPORT_TOKENS = (
    "knowledge_mode",
    "knowledge_domain",
    "selected_bundles",
    "applied_passes",
    "translation_targets",
)
SUPERVISION_SECTIONS = ("## 监制强化", "reviewer_source", "mode", "used_subagents", "patched_targets", "synthesis")


def load_json(path: Path) -> object:
    return json.loads(path.read_text(encoding="utf-8"))


def derive_report_path(episode_path: Path) -> Path:
    return episode_path.parent / "validation-report.md"


def is_template_mode(path: Path) -> bool:
    return "/.agents/skills/" in str(path.resolve())


def normalize_text(value: object) -> str:
    if not isinstance(value, str):
        return ""
    return " ".join(value.strip().split())


def format_seconds(value: object) -> str:
    if isinstance(value, int):
        return str(value)
    if isinstance(value, float):
        if value.is_integer():
            return str(int(value))
        return f"{value}".rstrip("0").rstrip(".")
    return ""


def detect_schema(data: object) -> str:
    if not isinstance(data, dict):
        return "invalid"
    if isinstance(data.get("meta"), dict) and isinstance(data.get("groups"), list):
        return "canonical"
    if isinstance(data.get("metadata"), dict) and isinstance(data.get("final_output"), dict):
        return "legacy"
    return "unknown"


def validate_string_keys(
    owner: str,
    payload: object,
    required_keys: tuple[str, ...],
    errors: list[str],
    allow_empty: bool,
) -> None:
    if not isinstance(payload, dict):
        errors.append(f"{owner}: 必须是对象。")
        return
    for key in required_keys:
        value = payload.get(key)
        if not isinstance(value, str):
            errors.append(f"{owner}: 缺少字符串字段 `{key}`。")
            continue
        if not allow_empty and not normalize_text(value):
            errors.append(f"{owner}: `{key}` 不能为空。")


def validate_dict_or_compat_string(
    owner: str,
    payload: object,
    required_keys: tuple[str, ...],
    errors: list[str],
) -> None:
    if isinstance(payload, dict):
        validate_string_keys(owner, payload, required_keys, errors, allow_empty=False)
        return
    if isinstance(payload, str) and normalize_text(payload):
        return
    errors.append(f"{owner}: 必须是对象或非空兼容字符串。")


def validate_time(owner: str, value: object, errors: list[str], allow_empty: bool) -> None:
    if not isinstance(value, str):
        errors.append(f"{owner}: `时间` 必须是字符串。")
        return
    if allow_empty and not value:
        return
    if not TIME_RE.match(value):
        errors.append(f"{owner}: `时间` 必须形如 `0-3秒`。")


def validate_canonical_episode(path: Path, allow_empty: bool) -> list[str]:
    data = load_json(path)
    errors: list[str] = []

    if not isinstance(data, dict):
        return ["episode JSON 顶层必须是对象。"]

    meta = data.get("meta")
    groups = data.get("groups")
    if not isinstance(meta, dict):
        errors.append("顶层缺少 `meta`。")
    else:
        for key in ROOT_META_KEYS:
            if key not in meta:
                errors.append(f"meta: 缺少 `{key}`。")
        if not isinstance(meta.get("组数"), int):
            errors.append("meta.组数 必须是整数。")
        if not isinstance(meta.get("总时长"), (int, float)):
            errors.append("meta.总时长 必须是数值。")
        if not allow_empty:
            for key in ("剧名", "集数"):
                if not normalize_text(meta.get(key)):
                    errors.append(f"meta.{key} 不能为空。")

    if not isinstance(groups, list) or not groups:
        errors.append("顶层 `groups` 必须是非空数组。")
        return errors

    if isinstance(meta, dict) and isinstance(meta.get("组数"), int) and not allow_empty and meta["组数"] != len(groups):
        errors.append(f"meta.组数({meta['组数']}) 必须等于 groups 数量({len(groups)})。")

    total_duration = 0.0
    for group in groups:
        if not isinstance(group, dict):
            errors.append("groups[] 元素必须是对象。")
            continue

        group_id = group.get("分镜组ID", "<missing-group-id>")
        if not isinstance(group_id, str):
            errors.append("group.分镜组ID 必须是字符串。")
            group_id = "<invalid-group-id>"
        elif not allow_empty and not normalize_text(group_id):
            errors.append("group.分镜组ID 不能为空。")

        global_block = group.get("global")
        detail = group.get("detail")
        validate_string_keys(f"{group_id}.global", global_block, GROUP_GLOBAL_KEYS, errors, allow_empty)
        if not allow_empty:
            if not isinstance(global_block, dict) or not normalize_text(global_block.get("剧本正文")):
                errors.append(f"{group_id}.global: 运行时输出必须保留继承自 2-Global 的 `剧本正文`。")
        if not isinstance(detail, dict):
            errors.append(f"{group_id}: 缺少 `detail`。")
            continue

        shot_count = detail.get("分镜数")
        shot_map = detail.get("分镜列表")
        if not isinstance(shot_count, int):
            errors.append(f"{group_id}: `detail.分镜数` 必须是整数。")
        if not isinstance(shot_map, dict) or not shot_map:
            errors.append(f"{group_id}: `detail.分镜列表` 必须是非空对象。")
            continue
        if isinstance(shot_count, int) and not allow_empty and shot_count != len(shot_map):
            errors.append(f"{group_id}: `分镜数`({shot_count}) 必须等于 `分镜列表` 数量({len(shot_map)})。")

        previous_end = 0.0
        for shot_id, shot in shot_map.items():
            owner = f"{group_id}/{shot_id}"
            if not isinstance(shot, dict):
                errors.append(f"{owner}: 分镜内容必须是对象。")
                continue
            for key in SHOT_FIELD_KEYS:
                if key not in shot:
                    errors.append(f"{owner}: 缺少 `{key}`。")

            validate_time(owner, shot.get("时间"), errors, allow_empty)
            if not allow_empty and not normalize_text(shot.get("剧本正文")):
                errors.append(f"{owner}: `剧本正文` 不能为空。")
            validate_string_keys(f"{owner}.主体锚定", shot.get("主体锚定"), ANCHOR_KEYS, errors, allow_empty)
            validate_string_keys(f"{owner}.分镜构图", shot.get("分镜构图"), TRIPLE_KEYS, errors, allow_empty)
            validate_string_keys(f"{owner}.运镜手法", shot.get("运镜手法"), CAMERA_KEYS, errors, allow_empty)
            validate_string_keys(f"{owner}.角色表现", shot.get("角色表现"), PERFORMANCE_KEYS, errors, allow_empty)
            validate_string_keys(f"{owner}.氛围表现", shot.get("氛围表现"), ATMOSPHERE_KEYS, errors, allow_empty)
            validate_string_keys(f"{owner}.摄影表现", shot.get("摄影表现"), PHOTO_KEYS, errors, allow_empty)
            validate_string_keys(f"{owner}.转场特效", shot.get("转场特效"), TRANSITION_KEYS, errors, allow_empty)

            time_text = shot.get("时间")
            if isinstance(time_text, str) and TIME_RE.match(time_text):
                start_text, end_text = time_text[:-1].split("-")
                start = float(start_text)
                end = float(end_text)
                if end < start:
                    errors.append(f"{owner}: `时间` 结束秒不得小于开始秒。")
                if start < previous_end:
                    errors.append(f"{owner}: `时间` 不得早于上一镜结束秒。")
                previous_end = end

        total_duration += previous_end

    if isinstance(meta, dict) and isinstance(meta.get("总时长"), (int, float)) and not allow_empty:
        if abs(float(meta["总时长"]) - total_duration) > 1e-6:
            errors.append(f"meta.总时长({meta['总时长']}) 必须等于各组末镜时长之和({total_duration})。")

    return errors


def validate_legacy_time(owner: str, payload: object, errors: list[str]) -> float:
    if not isinstance(payload, dict):
        errors.append(f"{owner}.时间段: 必须是对象。")
        return 0.0
    start = payload.get("开始秒")
    end = payload.get("结束秒")
    if not isinstance(start, (int, float)) or not isinstance(end, (int, float)):
        errors.append(f"{owner}.时间段: `开始秒/结束秒` 必须是数值。")
        return 0.0
    if end < start:
        errors.append(f"{owner}.时间段: `结束秒` 不得小于 `开始秒`。")
    legacy_time = f"{format_seconds(start)}-{format_seconds(end)}秒"
    if not TIME_RE.match(legacy_time):
        errors.append(f"{owner}.时间段: 无法转换为 canonical 时间字符串。")
    return float(end)


def validate_legacy_transition(owner: str, payload: object, errors: list[str]) -> None:
    if payload is None:
        return
    if isinstance(payload, str) and normalize_text(payload):
        return
    if not isinstance(payload, dict):
        errors.append(f"{owner}: 必须是对象。")
        return
    if all(isinstance(payload.get(key), str) for key in TRANSITION_KEYS):
        for key in TRANSITION_KEYS:
            if not normalize_text(payload.get(key)):
                errors.append(f"{owner}: `{key}` 不能为空。")
        return
    if all(isinstance(payload.get(key), str) for key in LEGACY_TRANSITION_KEYS):
        for key in LEGACY_TRANSITION_KEYS:
            if not normalize_text(payload.get(key)):
                errors.append(f"{owner}: `{key}` 不能为空。")
        return
    errors.append(f"{owner}: 必须提供 canonical 或 legacy 的转场字段集合。")


def validate_legacy_episode(path: Path) -> list[str]:
    data = load_json(path)
    errors: list[str] = []

    if not isinstance(data, dict):
        return ["episode JSON 顶层必须是对象。"]

    metadata = data.get("metadata")
    final_output = data.get("final_output")
    if not isinstance(metadata, dict):
        errors.append("顶层缺少 `metadata`。")
    else:
        for key in ("schema_version", "skill_id", "episode_id", "document_phase"):
            if not normalize_text(metadata.get(key)):
                errors.append(f"metadata.{key} 不能为空。")
    if not isinstance(final_output, dict):
        errors.append("顶层缺少 `final_output`。")
        return errors

    main_content = final_output.get("main_content")
    if not isinstance(main_content, dict):
        errors.append("final_output.main_content 必须是对象。")
        return errors

    groups = main_content.get("分镜组列表")
    if not isinstance(groups, list) or not groups:
        errors.append("final_output.main_content.分镜组列表 必须是非空数组。")
        return errors

    for group in groups:
        if not isinstance(group, dict):
            errors.append("分镜组列表[] 元素必须是对象。")
            continue

        group_id = group.get("分镜组ID", "<missing-group-id>")
        if not isinstance(group_id, str) or not normalize_text(group_id):
            errors.append("group.分镜组ID 必须是非空字符串。")
            group_id = "<invalid-group-id>"
        if not isinstance(group.get("总时长"), (int, float)):
            errors.append(f"{group_id}: `总时长` 必须是数值。")
        if not normalize_text(group.get("剧本正文")):
            errors.append(f"{group_id}: `剧本正文` 不能为空。")

        style_block = group.get("组间设计")
        validate_string_keys(f"{group_id}.组间设计", style_block, GROUP_GLOBAL_KEYS, errors, allow_empty=False)

        shot_count = group.get("分镜切换")
        shot_list = group.get("分镜明细")
        if not isinstance(shot_count, int):
            errors.append(f"{group_id}: `分镜切换` 必须是整数。")
        if not isinstance(shot_list, list) or not shot_list:
            errors.append(f"{group_id}: `分镜明细` 必须是非空数组。")
            continue
        if isinstance(shot_count, int) and shot_count != len(shot_list):
            errors.append(f"{group_id}: `分镜切换`({shot_count}) 必须等于 `分镜明细` 数量({len(shot_list)})。")

        previous_end = 0.0
        for shot in shot_list:
            if not isinstance(shot, dict):
                errors.append(f"{group_id}: 分镜明细[] 元素必须是对象。")
                continue
            shot_id = shot.get("分镜ID", "<missing-shot-id>")
            owner = f"{group_id}/{shot_id}"
            if not isinstance(shot_id, str) or not normalize_text(shot_id):
                errors.append(f"{group_id}: `分镜ID` 必须是非空字符串。")
                owner = f"{group_id}/<invalid-shot-id>"

            end = validate_legacy_time(owner, shot.get("时间段"), errors)
            if end < previous_end:
                errors.append(f"{owner}: `时间段.开始秒` 不得早于上一镜结束秒。")
            previous_end = end

            if not isinstance(shot.get("正文回指"), dict):
                errors.append(f"{owner}: 缺少 `正文回指` 对象。")
            validate_dict_or_compat_string(f"{owner}.分镜构图", shot.get("分镜构图"), TRIPLE_KEYS, errors)
            validate_string_keys(f"{owner}.角色表现", shot.get("角色表现"), PERFORMANCE_KEYS, errors, allow_empty=False)
            validate_string_keys(f"{owner}.氛围表现", shot.get("氛围表现"), ATMOSPHERE_KEYS, errors, allow_empty=False)
            validate_dict_or_compat_string(
                f"{owner}.摄影美学",
                shot.get("摄影美学") or shot.get("摄影表现"),
                PHOTO_KEYS,
                errors,
            )
            validate_dict_or_compat_string(f"{owner}.运镜手法", shot.get("运镜手法"), CAMERA_KEYS, errors)
            validate_legacy_transition(f"{owner}.转场特效", shot.get("转场特效"), errors)

        if isinstance(group.get("总时长"), (int, float)) and abs(float(group["总时长"]) - previous_end) > 1e-6:
            errors.append(f"{group_id}: `总时长`({group['总时长']}) 必须等于末镜结束秒({previous_end})。")

    return errors


def validate_report(report_path: Path, episode_path: Path, require_supervision: bool) -> list[str]:
    errors: list[str] = []
    if not report_path.exists():
        return [f"缺少阶段 validation-report: {report_path}"]

    text = report_path.read_text(encoding="utf-8")
    for section in REPORT_SECTIONS:
        if section not in text:
            errors.append(f"validation-report 缺少章节 `{section}`。")
    for token in (episode_path.name, "Layered Trace", "Closure Triad"):
        if token not in text:
            errors.append(f"validation-report 未提及 `{token}`。")
    for token in ACADEMY_REPORT_TOKENS:
        if token not in text:
            errors.append(f"validation-report 缺少学院派知识证据槽位 `{token}`。")
    if require_supervision:
        for section in SUPERVISION_SECTIONS:
            if section not in text:
                errors.append(f"validation-report 缺少监制强化槽位 `{section}`。")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate canonical `3-Detail` stage output and validation-report.")
    parser.add_argument("episode_json", type=Path, help="Path to `projects/aigc/<项目名>/3-Detail/第N集.json` or the shared template.")
    parser.add_argument("--report", type=Path, help="Override `validation-report.md` path.")
    parser.add_argument("--team-yaml", type=Path, help="Require supervision slots when team review is active.")
    args = parser.parse_args()

    episode_path = args.episode_json.resolve()
    if not episode_path.exists():
        print(f"文件不存在: {episode_path}")
        return 1

    data = load_json(episode_path)
    schema = detect_schema(data)

    if schema == "invalid":
        errors = ["episode JSON 顶层必须是对象。"]
    elif schema == "unknown":
        errors = ["无法识别 `3-Detail` 输出结构；当前仅支持 canonical `meta + groups` 或 legacy `metadata + final_output`。"]
    elif schema == "canonical":
        errors = validate_canonical_episode(episode_path, allow_empty=is_template_mode(episode_path))
    else:
        errors = validate_legacy_episode(episode_path)

    if not is_template_mode(episode_path):
        report_path = (args.report or derive_report_path(episode_path)).resolve()
        errors.extend(validate_report(report_path, episode_path, require_supervision=bool(args.team_yaml)))

    if errors:
        print("校验失败:")
        for error in errors:
            print(f"- {error}")
        return 1

    mode = "template" if is_template_mode(episode_path) else f"runtime/{schema}"
    print(f"校验通过。 episode={episode_path.name} mode={mode}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
