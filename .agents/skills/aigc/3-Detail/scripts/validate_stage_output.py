#!/usr/bin/env python3
"""Validate merged `3-Detail` stage output and acceptance artifacts."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


EPISODE_SCHEMA_VERSION = "aigc/director-episode-output/v1"
ALLOWED_PHASES = {"detail_in_progress", "ready"}
LEGACY_PATCH_SCHEMA_VERSION = "aigc/detail-patch-sidecar/v1"
BRANCH_BUNDLE_SCHEMA_VERSION = "aigc/detail-branch-bundle-sidecar/v1"
REQUIRED_GROUP_KEYS = ("分镜组ID", "总时长", "剧本正文", "正文切分参考", "组间设计", "分镜切换", "分镜明细")
REQUIRED_DESIGN_KEYS = ("全局风格", "类型元素", "导演意图", "出场角色及穿搭")
REQUIRED_SHOT_KEYS = ("分镜ID", "时间段", "正文回指", "角色背景面", "角色站位走位", "道具及状态")
REQUIRED_BRANCH_SHOT_KEYS = (
    ("角色表现", "人物表演锚点", "人物表演"),
    ("运动表现", "动作路径", "动作调度"),
    ("氛围表现", "空间氛围"),
    ("视觉强化", "视觉抓手", "视觉焦点"),
    ("分镜构图", "构图骨架", "构图策略"),
    ("摄影美学", "摄影策略"),
    ("运镜手法", "运镜策略"),
    ("转场特效", "转场策略"),
)
REQUIRED_REPORT_SECTIONS = ("## Layered Trace", "## Closure Triad", "## 已执行校验")
REQUIRED_SUPERVISION_REPORT_SECTIONS = ("## 监制强化", "reviewer_source", "mode", "used_subagents", "patched_targets", "synthesis")
CAMERA_JARGON_TOKENS = ("镜头", "景", "大全景", "中景", "近景", "特写", "平视", "俯视", "仰视", "过肩", "推近", "推进", "跟随", "定镜", "摇", "移", "压近")
ABSTRACT_ONLY_TOKENS = ("主抓手", "关系压力", "情绪", "氛围", "更强", "更稳", "成立", "电影感", "高级感", "观感")


def find_repo_root() -> Path:
    current = Path(__file__).resolve()
    for parent in current.parents:
        if (parent / "AGENTS.md").exists():
            return parent
    raise RuntimeError("无法定位仓库根目录。")


ROOT = find_repo_root()


def load_json(path: Path) -> object:
    return json.loads(path.read_text(encoding="utf-8"))


def derive_sidecar_path(episode_path: Path, owner: str) -> Path:
    return episode_path.parent / owner / f"{episode_path.stem}.field-patch.json"


def derive_report_path(episode_path: Path) -> Path:
    return episode_path.parent / "validation-report.md"


def bundle_mode(data: object) -> str:
    if not isinstance(data, dict):
        return "invalid"
    metadata = data.get("metadata", {})
    schema_version = metadata.get("schema_version")
    if schema_version == BRANCH_BUNDLE_SCHEMA_VERSION:
        return "branch"
    if schema_version == LEGACY_PATCH_SCHEMA_VERSION:
        return "legacy"
    return "invalid"


def pick_branch_object(shot: dict[str, object], *field_names: str) -> object:
    for field_name in field_names:
        value = shot.get(field_name)
        if isinstance(value, dict):
            return value
    return {}


def normalize_text(value: object) -> str:
    if not isinstance(value, str):
        return ""
    return " ".join(value.strip().split())


def looks_like_camera_jargon(text: object) -> bool:
    normalized = normalize_text(text)
    return bool(normalized) and any(token in normalized for token in CAMERA_JARGON_TOKENS)


def looks_too_abstract(text: object) -> bool:
    normalized = normalize_text(text)
    if not normalized:
        return False
    abstract_hits = sum(token in normalized for token in ABSTRACT_ONLY_TOKENS)
    concrete_hits = sum(token in normalized for token in ("前景", "后景", "中轴", "门", "窗", "人群", "杯", "项链", "肩", "手", "光", "影", "位置", "左", "右", "前", "后", "中央", "边缘", "遮挡", "同框", "背景"))
    return abstract_hits >= 2 and concrete_hits == 0


def contains_hard_truncation(text: object) -> bool:
    normalized = normalize_text(text)
    if not normalized:
        return False
    return "…" in normalized or normalized.endswith("...") or normalized.endswith("……")


def stringify_branch_design(value: object, ordered_keys: tuple[str, ...]) -> list[str]:
    if not isinstance(value, dict):
        return []
    return [normalize_text(value.get(key)) for key in ordered_keys if normalize_text(value.get(key))]


def value_to_text(shot: dict[str, object], primary: tuple[str, ...], ordered_keys: tuple[str, ...]) -> str:
    direct_value = shot.get(primary[0])
    if isinstance(direct_value, str):
        return normalize_text(direct_value)
    return "，".join(stringify_branch_design(pick_branch_object(shot, *primary), ordered_keys))


def resolve_repo_relative_path(path_text: str) -> Path:
    candidate = Path(path_text)
    if candidate.is_absolute():
        return candidate
    return (ROOT / candidate).resolve()


def validate_script_segments(group_id: str, script_body: str, references: object) -> tuple[list[str], dict[str, dict[str, object]]]:
    errors: list[str] = []
    segments_by_id: dict[str, dict[str, object]] = {}

    if not isinstance(references, list) or not references:
        return [f"{group_id}: `正文切分参考` 必须是非空数组。"], segments_by_id

    body_length = len(script_body)
    for index, raw_item in enumerate(references, start=1):
        if not isinstance(raw_item, dict):
            errors.append(f"{group_id}: `正文切分参考[{index}]` 必须是对象。")
            continue
        beat_id = str(raw_item.get("beat_id", "")).strip()
        if not beat_id:
            errors.append(f"{group_id}: `正文切分参考[{index}]` 缺少 `beat_id`。")
            continue
        if beat_id in segments_by_id:
            errors.append(f"{group_id}: `正文切分参考` 出现重复 beat_id `{beat_id}`。")
            continue

        excerpt = raw_item.get("原文片段")
        if not isinstance(excerpt, str) or not excerpt:
            errors.append(f"{group_id}/{beat_id}: `原文片段` 不能为空。")
            continue

        segment_type = raw_item.get("segment_type")
        if segment_type not in {"动作", "对白", "反应", "环境", "转折", "复合"}:
            errors.append(f"{group_id}/{beat_id}: `segment_type` 非法。")

        char_range = raw_item.get("char_range")
        if not isinstance(char_range, dict):
            errors.append(f"{group_id}/{beat_id}: `char_range` 必须是对象。")
            continue
        start = char_range.get("start")
        end = char_range.get("end")
        if not isinstance(start, int) or not isinstance(end, int):
            errors.append(f"{group_id}/{beat_id}: `char_range.start/end` 必须是整数。")
            continue
        if start < 0 or end <= start or end > body_length:
            errors.append(f"{group_id}/{beat_id}: `char_range` 超出 `剧本正文` 范围。")
            continue
        if script_body[start:end] != excerpt:
            errors.append(f"{group_id}/{beat_id}: `原文片段` 与 `char_range` 指向的 `剧本正文` 子串不一致。")
            continue

        segments_by_id[beat_id] = raw_item

    return errors, segments_by_id


def validate_shot_script_reference(group_id: str, shot_id: str, shot: dict[str, object], segments_by_id: dict[str, dict[str, object]]) -> list[str]:
    errors: list[str] = []
    script_ref = shot.get("正文回指")
    if not isinstance(script_ref, dict):
        return [f"{group_id}/{shot_id}: `正文回指` 必须是对象。"]

    beat_refs = script_ref.get("beat_refs")
    if not isinstance(beat_refs, list) or not beat_refs:
        errors.append(f"{group_id}/{shot_id}: `正文回指.beat_refs` 必须是非空数组。")
    else:
        seen: set[str] = set()
        for beat_id in beat_refs:
            if not isinstance(beat_id, str) or not beat_id.strip():
                errors.append(f"{group_id}/{shot_id}: `正文回指.beat_refs[]` 只能包含非空字符串。")
                continue
            if beat_id in seen:
                errors.append(f"{group_id}/{shot_id}: `正文回指.beat_refs[]` 出现重复 `{beat_id}`。")
                continue
            seen.add(beat_id)
            if beat_id not in segments_by_id:
                errors.append(f"{group_id}/{shot_id}: `正文回指` 指向未知 beat_id `{beat_id}`。")

    coverage_mode = script_ref.get("coverage_mode")
    if coverage_mode not in {"direct", "reaction", "insert", "bridge", "composite"}:
        errors.append(f"{group_id}/{shot_id}: `正文回指.coverage_mode` 非法。")

    return errors


def validate_branch_sidecar_paths(data: object, phase: str, owner_label: str) -> list[str]:
    errors: list[str] = []
    if not isinstance(data, dict):
        return errors
    if data.get("metadata", {}).get("schema_version") != BRANCH_BUNDLE_SCHEMA_VERSION:
        return errors
    branch_sidecars = data.get("branch_sidecars", [])
    if not isinstance(branch_sidecars, list):
        return errors
    for item in branch_sidecars:
        if not isinstance(item, str) or not item.strip():
            errors.append(f"{owner_label}: `branch_sidecars[]` 只能包含非空字符串路径。")
            continue
        sidecar_path = resolve_repo_relative_path(item)
        if not sidecar_path.exists():
            errors.append(f"{owner_label}: branch sidecar 不存在: {item}")
            continue
        try:
            sidecar_data = load_json(sidecar_path)
        except json.JSONDecodeError as exc:
            errors.append(f"{owner_label}: branch sidecar JSON 解析失败 `{item}`: {exc}")
            continue
        metadata = sidecar_data.get("metadata", {}) if isinstance(sidecar_data, dict) else {}
        review_status = metadata.get("review_status")
        if phase == "ready" and review_status != "reviewed":
            errors.append(f"{owner_label}: `ready` 阶段 branch sidecar 必须是 reviewed: {item}")
        group_patches = sidecar_data.get("group_branch_patches", [])
        if not isinstance(group_patches, list) or not group_patches:
            errors.append(f"{owner_label}: branch sidecar 缺少 `group_branch_patches[]`: {item}")
            continue
        for group_patch in group_patches:
            if not isinstance(group_patch, dict):
                errors.append(f"{owner_label}: `{item}` 的 `group_branch_patches[]` 元素必须是对象。")
                continue
            review_trace = group_patch.get("review_trace")
            if not isinstance(review_trace, dict):
                errors.append(f"{owner_label}: `{item}` 缺少 `review_trace`。")
                continue
            reviewers = review_trace.get("requested_reviewers")
            if phase == "ready" and (not isinstance(reviewers, list) or not reviewers):
                errors.append(f"{owner_label}: `{item}` 在 `ready` 阶段必须声明 `requested_reviewers[]`。")
            if phase == "ready" and review_trace.get("apply_decision") in {None, "", "pending"}:
                errors.append(f"{owner_label}: `{item}` 在 `ready` 阶段必须给出非 pending 的 `apply_decision`。")
    return errors


def validate_episode_shell(data: object) -> tuple[list[str], dict[str, dict[str, object]], str]:
    errors: list[str] = []
    groups_by_id: dict[str, dict[str, object]] = {}

    if not isinstance(data, dict):
        return ["episode JSON 顶层必须是对象。"], groups_by_id, ""

    metadata = data.get("metadata", {})
    final_output = data.get("final_output", {})
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

    main_content = final_output.get("main_content", {})
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
        script_body = group.get("剧本正文")
        if isinstance(script_body, str):
            segment_errors, segments_by_id = validate_script_segments(group_id, script_body, group.get("正文切分参考"))
            errors.extend(segment_errors)
        else:
            segments_by_id = {}
        details = group.get("分镜明细")
        shot_count = group.get("分镜切换")
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
            errors.extend(validate_shot_script_reference(group_id, shot_id, shot, segments_by_id))
            if "分镜构图" not in shot and "分镜表现" not in shot:
                errors.append(f"{group_id}/{shot_id}: 缺少 `分镜构图 / 分镜表现` 兼容构图摘要。")
            time_range = shot.get("时间段")
            if not isinstance(time_range, dict) or "开始秒" not in time_range or "结束秒" not in time_range:
                errors.append(f"{group_id}/{shot_id}: `时间段` 必须包含 `开始秒 / 结束秒`。")
                continue
            start = time_range.get("开始秒")
            end = time_range.get("结束秒")
            if not isinstance(start, (int, float)) or not isinstance(end, (int, float)):
                errors.append(f"{group_id}/{shot_id}: `时间段` 必须是数值。")
                continue
            if end < start:
                errors.append(f"{group_id}/{shot_id}: `结束秒` 不得小于 `开始秒`。")
            if shot_index == 1 and start != 0:
                errors.append(f"{group_id}/{shot_id}: 首镜 `开始秒` 必须为 0。")
            if start < previous_end:
                errors.append(f"{group_id}/{shot_id}: `开始秒` 不得早于上一镜结束秒。")
            previous_end = float(end)

            performance = pick_branch_object(shot, "角色表现", "人物表演锚点", "人物表演")
            if isinstance(performance, dict):
                acting_goal = performance.get("动作戏", performance.get("表演目标"))
                dialogue_play = performance.get("对话戏", performance.get("对手戏", performance.get("关系施压")))
                inner_play = performance.get("内心戏")
                camera_summary = value_to_text(
                    shot,
                    ("运镜手法", "运镜策略"),
                    ("变化", "速度", "组合", "运动动机", "运动路径", "速度设计"),
                )
                if looks_like_camera_jargon(acting_goal) and normalize_text(acting_goal) == camera_summary:
                    errors.append(f"{group_id}/{shot_id}: `角色表现.动作戏` 不得直接复用 `运镜手法`。")
                if contains_hard_truncation(acting_goal):
                    errors.append(f"{group_id}/{shot_id}: `角色表现.动作戏` 出现省略号或半截短语，未完成具像化表达。")
                if contains_hard_truncation(dialogue_play):
                    errors.append(f"{group_id}/{shot_id}: `角色表现.对话戏` 出现省略号或半截短语，未完成具像化表达。")
                if contains_hard_truncation(inner_play):
                    errors.append(f"{group_id}/{shot_id}: `角色表现.内心戏` 出现省略号或半截短语，未完成具像化表达。")
                if normalize_text(dialogue_play) and normalize_text(acting_goal) == normalize_text(dialogue_play):
                    errors.append(f"{group_id}/{shot_id}: `角色表现.动作戏` 与 `对话戏` 机械同句，未形成字段分工。")

            composition_projection = value_to_text(
                shot,
                ("分镜构图", "构图骨架", "构图策略"),
                ("景别景深", "镜头类型", "构图形式", "构图骨架", "视线组织"),
            ) or normalize_text(shot.get("分镜表现"))
            if contains_hard_truncation(composition_projection):
                errors.append(f"{group_id}/{shot_id}: `分镜构图/分镜表现` 出现省略号或半截短语，未完成具像化表达。")
            if looks_too_abstract(composition_projection):
                errors.append(f"{group_id}/{shot_id}: `分镜构图/分镜表现` 过于抽象，缺少构图向具像信息。")

        if phase == "ready" and isinstance(total_duration, (int, float)) and details:
            last_end = details[-1].get("时间段", {}).get("结束秒")
            if isinstance(last_end, (int, float)) and abs(float(last_end) - float(total_duration)) > 1e-6:
                errors.append(f"{group_id}: 最后一镜结束秒({last_end}) 必须与 `总时长`({total_duration}) 对齐。")

    return errors, groups_by_id, phase


def validate_watermoon_sidecar(data: object, groups_by_id: dict[str, dict[str, object]]) -> tuple[list[str], bool]:
    errors: list[str] = []
    mode = bundle_mode(data)
    if mode == "invalid":
        return ["水月 sidecar schema_version 非法。"], False
    if not isinstance(data, dict):
        return ["水月 sidecar 顶层必须是对象。"], False

    metadata = data.get("metadata", {})
    if metadata.get("patch_owner") != "水月":
        errors.append("水月 sidecar metadata.patch_owner 必须为 `水月`。")

    groups = data.get("group_patches")
    if not isinstance(groups, list) or not groups:
        return ["水月 sidecar `group_patches` 必须是非空数组。"], mode == "branch"

    if mode == "branch":
        if metadata.get("bundle_mode") != "assembly_only":
            errors.append("水月新 bundle 必须声明 `bundle_mode=assembly_only`。")
        if not isinstance(data.get("branch_sidecars"), list) or not data.get("branch_sidecars"):
            errors.append("水月新 bundle 必须声明 `branch_sidecars[]`。")
        for group in groups:
            if not isinstance(group, dict):
                errors.append("水月 bundle `group_patches[]` 元素必须是对象。")
                continue
            group_id = str(group.get("group_id", "<missing-group-id>"))
            if group_id not in groups_by_id:
                errors.append(f"水月 bundle 命中未知 group_id: {group_id}")
            branch_patches = group.get("branch_patches")
            if not isinstance(branch_patches, dict):
                errors.append(f"{group_id}: 水月新 bundle 缺少 `branch_patches`。")
                continue
            for key in ("角色表现", "运动表现", "氛围表现", "视觉强化"):
                if key not in branch_patches:
                    errors.append(f"{group_id}: 缺少水月 branch patch `{key}`。")
    return errors, mode == "branch"


def validate_jinghua_sidecar(data: object, groups_by_id: dict[str, dict[str, object]], phase: str) -> tuple[list[str], bool]:
    errors: list[str] = []
    mode = bundle_mode(data)
    if mode == "invalid":
        return ["镜花 sidecar schema_version 非法。"], False
    if not isinstance(data, dict):
        return ["镜花 sidecar 顶层必须是对象。"], False

    metadata = data.get("metadata", {})
    if metadata.get("patch_owner") != "镜花":
        errors.append("镜花 sidecar metadata.patch_owner 必须为 `镜花`。")

    groups = data.get("group_patches")
    if not isinstance(groups, list) or not groups:
        return ["镜花 sidecar `group_patches` 必须是非空数组。"], mode == "branch"

    if mode == "branch":
        if metadata.get("bundle_mode") != "assembly_only":
            errors.append("镜花新 bundle 必须声明 `bundle_mode=assembly_only`。")
        if not isinstance(data.get("branch_sidecars"), list) or not data.get("branch_sidecars"):
            errors.append("镜花新 bundle 必须声明 `branch_sidecars[]`。")
        for group in groups:
            if not isinstance(group, dict):
                errors.append("镜花 bundle `group_patches[]` 元素必须是对象。")
                continue
            group_id = str(group.get("group_id", "<missing-group-id>"))
            storyboard_group = groups_by_id.get(group_id)
            if storyboard_group is None:
                errors.append(f"镜花 bundle 命中未知 group_id: {group_id}")
                continue
            branch_patches = group.get("branch_patches")
            if not isinstance(branch_patches, dict):
                errors.append(f"{group_id}: 镜花新 bundle 缺少 `branch_patches`。")
                continue
            if "分镜构图" not in branch_patches:
                errors.append(f"{group_id}: 缺少 `分镜构图` branch patch。")
            for key in ("摄影美学", "运镜手法", "转场特效"):
                if key not in branch_patches:
                    errors.append(f"{group_id}: 缺少镜花 branch patch `{key}`。")
            if phase == "ready" and isinstance(storyboard_group.get("分镜切换"), int):
                # new mode keeps count in root; branch bundle no longer needs shot_patches cardinality
                pass
    return errors, mode == "branch"


def validate_branch_canonical_fields(groups_by_id: dict[str, dict[str, object]], new_mode: bool) -> list[str]:
    errors: list[str] = []
    if not new_mode:
        return errors
    suffix_match_count = 0
    projection_match_count = 0
    for group_id, group in groups_by_id.items():
        details = group.get("分镜明细", [])
        for shot in details:
            if not isinstance(shot, dict):
                continue
            shot_id = shot.get("分镜ID", "<missing-shot-id>")
            for key_group in REQUIRED_BRANCH_SHOT_KEYS:
                branch_value = pick_branch_object(shot, *key_group)
                if not isinstance(branch_value, dict) or not branch_value:
                    errors.append(f"{group_id}/{shot_id}: 新 bundle 模式下缺少 branch-owned canonical 字段 `{' / '.join(key_group)}`。")
            visual_focus = pick_branch_object(shot, "视觉强化", "视觉抓手", "视觉焦点")
            expression = shot.get("分镜表现")
            if isinstance(visual_focus, dict) and isinstance(expression, str):
                hint = normalize_text(visual_focus.get("观赏性") or visual_focus.get("冲击力") or visual_focus.get("品味"))
                if isinstance(hint, str) and hint and expression.strip().endswith(hint.strip()):
                    suffix_match_count += 1
            projection_pairs = (
                (
                    shot.get("角色背景面"),
                    stringify_branch_design(pick_branch_object(shot, "氛围表现", "空间氛围"), ("层次", "空间支架"))
                    + stringify_branch_design(pick_branch_object(shot, "分镜构图", "构图骨架", "构图策略"), ("构图形式", "构图骨架")),
                ),
                (
                    shot.get("角色站位走位"),
                    stringify_branch_design(pick_branch_object(shot, "运动表现", "动作路径", "动作调度"), ("位置和方向", "位置基线", "动作路径")),
                ),
                (
                    shot.get("摄影美学"),
                    stringify_branch_design(pick_branch_object(shot, "摄影美学", "摄影策略"), ("光影", "色彩", "质感", "视觉控制线", "光影策略", "色彩策略", "质感策略")),
                ),
                (
                    shot.get("运镜手法"),
                    stringify_branch_design(pick_branch_object(shot, "运镜手法", "运镜策略"), ("变化", "速度", "组合", "运动动机", "运动路径", "速度设计")),
                ),
                (
                    shot.get("转场特效"),
                    stringify_branch_design(pick_branch_object(shot, "转场特效", "转场策略"), ("切接逻辑", "组内衔接", "组间或特效策略")),
                ),
            )
            for legacy_value, branch_candidates in projection_pairs:
                legacy_text = normalize_text(legacy_value)
                if not legacy_text:
                    continue
                if any(legacy_text == candidate or legacy_text.endswith(candidate) or candidate.endswith(legacy_text) for candidate in branch_candidates if candidate):
                    projection_match_count += 1
    if suffix_match_count > 2:
        errors.append("新 bundle 模式下 `分镜表现` 仍大量直接复用 `视觉抓手/视觉焦点.镜头消费提示` 作为 suffix，疑似回流到旧式语义压缩。")
    if projection_match_count > 6:
        errors.append("新 bundle 模式下多个 legacy compatibility 字段仍与 branch-owned canonical 子槽高度同文复写，疑似仍停留在 projection-first 而非 canonical-first。")
    return errors


def validate_report(report_path: Path, episode_path: Path, watermoon_path: Path, jinghua_path: Path, supervision_team_yaml: Path | None) -> list[str]:
    errors: list[str] = []
    if not report_path.exists():
        return [f"缺少阶段 validation-report: {report_path}"]
    text = report_path.read_text(encoding="utf-8")
    for section in REQUIRED_REPORT_SECTIONS:
        if section not in text:
            errors.append(f"validation-report 缺少章节 `{section}`。")
    for token in (episode_path.name, watermoon_path.name, jinghua_path.name, "Layered Trace", "Closure Triad"):
        if token not in text:
            errors.append(f"validation-report 未提及 `{token}`。")
    if supervision_team_yaml is not None:
        for section in REQUIRED_SUPERVISION_REPORT_SECTIONS:
            if section not in text:
                errors.append(f"validation-report 缺少监制强化槽位 `{section}`。")
        for token in (supervision_team_yaml.name, "监制强化", "used_subagents"):
            if token not in text:
                errors.append(f"validation-report 未提及监制强化关键信息 `{token}`。")
    return errors


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Validate merged `3-Detail` stage output, owner bundles, and validation-report.")
    parser.add_argument("episode_json", type=Path, help="Path to `projects/aigc/<项目名>/3-Detail/第N集.json`.")
    parser.add_argument("--watermoon", type=Path, help="Override `水月` bundle path.")
    parser.add_argument("--jinghua", type=Path, help="Override `镜花` bundle path.")
    parser.add_argument("--report", type=Path, help="Override `validation-report.md` path.")
    parser.add_argument("--team-yaml", type=Path, help="Require supervision slots when team review is active.")
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()

    episode_path = args.episode_json.resolve()
    watermoon_path = (args.watermoon or derive_sidecar_path(episode_path, "水月")).resolve()
    jinghua_path = (args.jinghua or derive_sidecar_path(episode_path, "镜花")).resolve()
    report_path = (args.report or derive_report_path(episode_path)).resolve()
    team_yaml_path = args.team_yaml.resolve() if args.team_yaml else None

    missing_paths = [path for path in (episode_path, watermoon_path, jinghua_path) if not path.exists()]
    if team_yaml_path is not None and not team_yaml_path.exists():
        missing_paths.append(team_yaml_path)
    if missing_paths:
        for path in missing_paths:
            print(f"文件不存在: {path}")
        return 1

    errors: list[str] = []
    episode_errors, groups_by_id, phase = validate_episode_shell(load_json(episode_path))
    errors.extend(episode_errors)

    watermoon_errors, watermoon_new_mode = validate_watermoon_sidecar(load_json(watermoon_path), groups_by_id)
    jinghua_errors, jinghua_new_mode = validate_jinghua_sidecar(load_json(jinghua_path), groups_by_id, phase)
    errors.extend(watermoon_errors)
    errors.extend(jinghua_errors)
    errors.extend(validate_branch_sidecar_paths(load_json(watermoon_path), phase, "水月"))
    errors.extend(validate_branch_sidecar_paths(load_json(jinghua_path), phase, "镜花"))
    errors.extend(validate_branch_canonical_fields(groups_by_id, watermoon_new_mode or jinghua_new_mode))
    errors.extend(validate_report(report_path, episode_path, watermoon_path, jinghua_path, team_yaml_path))

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
