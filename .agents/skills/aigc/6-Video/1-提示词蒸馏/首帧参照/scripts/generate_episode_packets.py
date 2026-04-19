#!/usr/bin/env python3
from __future__ import annotations

import argparse
import copy
import json
import math
import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


def find_repo_root() -> Path:
    current = Path(__file__).resolve()
    for parent in current.parents:
        if (parent / "AGENTS.md").exists():
            return parent
    raise RuntimeError("无法定位仓库根目录。")


ROOT = find_repo_root()
PROJECTS_ROOT = ROOT / "projects" / "aigc"
TEMPLATE_JSON = ROOT / ".agents/skills/aigc/6-Video/_shared/video-generation-input.template.json"
PROMPT_ASSEMBLY_SPEC = ROOT / ".agents/skills/aigc/6-Video/1-提示词蒸馏/首帧参照/prompt-assembly-spec.md"
SOURCE_SCHEMA = ".agents/skills/aigc/_shared/director_episode_output.schema.json"
TARGET_MAX = 1900
TARGET_CHAR_LIMIT = 1900


def read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, payload: Any) -> None:
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def resolve_project_root(project_name: str) -> Path:
    project_root = PROJECTS_ROOT / project_name
    if project_root.exists():
        return project_root
    raise FileNotFoundError(
        f"未找到 canonical AIGC 项目根：{project_root}。"
        "本技能只消费 projects/aigc/<项目名>/ 下的运行时真源。"
    )


def load_prompt_assembly_spec() -> dict[str, Any]:
    content = PROMPT_ASSEMBLY_SPEC.read_text(encoding="utf-8")
    match = re.search(r"```json\s*(\{.*\})\s*```", content, re.DOTALL)
    if not match:
        raise ValueError(f"{PROMPT_ASSEMBLY_SPEC} 缺少 canonical JSON spec code block。")
    return require_dict(json.loads(match.group(1)), "prompt_assembly_spec")


def normalize_space(text: str) -> str:
    text = re.sub(r"\s+", " ", text.strip())
    text = text.replace(" ，", "，").replace(" 。", "。").replace(" ？", "？").replace(" ！", "！")
    return text


def strip_tail_punct(text: str) -> str:
    return re.sub(r"[。！？；;，,、\s]+$", "", text.strip())


def ensure_sentence(text: str) -> str:
    clean = normalize_space(text)
    if not clean:
        return ""
    if re.search(r"[。！？!?；;][”’\"]?$", clean):
        return clean
    return clean + "。"


def compact_clause(text: str) -> str:
    clean = strip_tail_punct(normalize_space(text))
    if not clean:
        return ""
    return re.split(r"[，；。]", clean, maxsplit=1)[0].strip()


def combine_clauses(*parts: str, sep: str = "，") -> str:
    clauses = [strip_tail_punct(part) for part in parts if part and strip_tail_punct(part)]
    if not clauses:
        return ""
    return ensure_sentence(sep.join(clauses))


def join_non_empty(parts: list[str]) -> str:
    return "，".join(item.strip() for item in parts if isinstance(item, str) and item.strip())


def stringify_branch_design(value: Any, ordered_keys: tuple[str, ...]) -> str:
    if not isinstance(value, dict):
        return ""
    return join_non_empty([str(value.get(key, "")).strip() for key in ordered_keys])


def compact_branch_design(value: Any, ordered_keys: tuple[str, ...], limit: int = 2) -> str:
    if not isinstance(value, dict):
        return ""
    picked: list[str] = []
    for key in ordered_keys:
        raw = value.get(key, "")
        if not isinstance(raw, str) or not raw.strip():
            continue
        compacted = compact_clause(raw)
        if not compacted or compacted in picked:
            continue
        picked.append(compacted)
        if len(picked) >= limit:
            break
    return "，".join(picked)


def first_non_empty(*values: str) -> str:
    for value in values:
        if isinstance(value, str) and value.strip():
            return value.strip()
    return ""


def pick_branch_object(shot: dict[str, Any], *field_names: str) -> Any:
    for field_name in field_names:
        value = shot.get(field_name)
        if isinstance(value, dict):
            return value
    return {}


def normalize_shot_for_prompt(shot: dict[str, Any]) -> dict[str, Any]:
    normalized = dict(shot)
    normalized["角色表现"] = first_non_empty(
        compact_branch_design(
            pick_branch_object(normalized, "角色表现", "人物表演锚点", "人物表演"),
            ("动作戏", "对话戏", "内心戏", "对手戏", "表演目标", "关系施压", "服装锚点"),
            limit=2,
        ),
        str(normalized.get("角色表现", "")).strip(),
        str(normalized.get("人物表演锚点", "")).strip(),
        str(normalized.get("人物表演", "")).strip(),
    )
    normalized["运动表现"] = first_non_empty(
        compact_branch_design(
            pick_branch_object(normalized, "运动表现", "动作路径", "动作调度"),
            ("位置和方向", "逻辑性", "一致性", "位置基线", "动作路径", "连续性说明"),
            limit=2,
        ),
        str(normalized.get("运动表现", "")).strip(),
        str(normalized.get("动作路径", "")).strip(),
        str(normalized.get("动作调度", "")).strip(),
        str(normalized.get("角色站位走位", "")).strip(),
    )
    normalized["分镜构图"] = first_non_empty(
        compact_branch_design(
            pick_branch_object(normalized, "分镜构图", "构图骨架", "构图策略"),
            ("景别景深", "构图形式", "镜头类型", "构图骨架", "视线组织"),
            limit=2,
        ),
        str(normalized.get("分镜构图", "")).strip(),
        str(normalized.get("构图骨架", "")).strip(),
        str(normalized.get("构图策略", "")).strip(),
        str(normalized.get("镜头框架", "")).strip(),
        str(normalized.get("分镜表现", "")).strip(),
    )
    normalized["氛围表现"] = first_non_empty(
        compact_branch_design(pick_branch_object(normalized, "氛围表现", "空间氛围"), ("层次", "意境", "空间诗学", "空间支架", "空气层", "物象压力"), limit=2),
        str(normalized.get("氛围表现", "")).strip(),
        str(normalized.get("空间氛围", "")).strip(),
        str(normalized.get("场景氛围", "")).strip(),
        str(normalized.get("角色背景面", "")).strip(),
    )
    normalized["摄影美学"] = first_non_empty(
        compact_branch_design(
            pick_branch_object(normalized, "摄影美学", "摄影策略"),
            ("光影", "色彩", "质感", "视觉控制线", "光影策略", "色彩策略", "质感策略"),
            limit=2,
        ),
        str(normalized.get("摄影美学", "")).strip(),
        str(normalized.get("摄影策略", "")).strip(),
    )
    normalized["运镜手法"] = first_non_empty(
        compact_branch_design(pick_branch_object(normalized, "运镜手法", "运镜策略"), ("组合", "变化", "运动动机", "运动路径"), limit=2),
        str(normalized.get("运镜手法", "")).strip(),
        str(normalized.get("运镜策略", "")).strip(),
    )
    normalized["镜头速度"] = first_non_empty(
        compact_branch_design(pick_branch_object(normalized, "运镜手法", "运镜策略"), ("速度", "速度设计"), limit=1),
        str(normalized.get("镜头速度", "")).strip(),
    )
    normalized["视觉强化"] = first_non_empty(
        compact_branch_design(
            pick_branch_object(normalized, "视觉强化", "视觉抓手", "视觉焦点"),
            ("冲击力", "观赏性", "品味", "第一抓手", "观看节奏", "镜头消费提示"),
            limit=2,
        ),
        str(normalized.get("视觉强化", "")).strip(),
        str(normalized.get("视觉抓手", "")).strip(),
        str(normalized.get("视觉焦点", "")).strip(),
        str(normalized.get("分镜表现", "")).strip(),
    )
    normalized["转场特效"] = first_non_empty(
        compact_branch_design(pick_branch_object(normalized, "转场特效", "转场策略"), ("切接逻辑", "组内衔接", "组间或特效策略"), limit=1),
        str(normalized.get("转场特效", "")).strip(),
        str(normalized.get("转场策略", "")).strip(),
    )

    normalized["角色站位走位"] = first_non_empty(normalized["运动表现"], str(normalized.get("角色站位走位", "")).strip())
    normalized["角色背景面"] = first_non_empty(
        compact_branch_design(pick_branch_object(normalized, "氛围表现", "空间氛围"), ("层次", "空间支架"), limit=1),
        compact_branch_design(pick_branch_object(normalized, "分镜构图", "构图骨架", "构图策略"), ("构图形式", "构图骨架"), limit=1),
        str(normalized.get("角色背景面", "")).strip(),
    )
    normalized["场景氛围"] = first_non_empty(normalized["氛围表现"], str(normalized.get("场景氛围", "")).strip())
    normalized["镜头框架"] = first_non_empty(
        str(normalized.get("镜头框架", "")).strip(),
        compact_branch_design(pick_branch_object(normalized, "分镜构图", "构图骨架", "构图策略"), ("构图形式", "构图骨架", "视线组织"), limit=1),
    )
    normalized["分镜表现"] = first_non_empty(str(normalized.get("分镜表现", "")).strip(), normalized["视觉强化"], normalized["分镜构图"])
    normalized["景别"] = first_non_empty(
        compact_branch_design(pick_branch_object(normalized, "分镜构图", "构图骨架", "构图策略"), ("景别景深",), limit=1),
        str(normalized.get("景别", "")).strip(),
    )
    normalized["镜头类型"] = first_non_empty(
        str(normalized.get("镜头类型", "")).strip(),
        compact_branch_design(pick_branch_object(normalized, "分镜构图", "构图骨架", "构图策略"), ("镜头类型",), limit=1),
    )
    normalized["镜头类型兼容"] = first_non_empty(
        str(normalized.get("镜头类型兼容", "")).strip(),
        str(normalized.get("镜头属性", "")).strip(),
    )
    normalized["人物表演"] = normalized["角色表现"]
    normalized["动作调度"] = normalized["运动表现"]
    normalized["空间氛围"] = normalized["氛围表现"]
    normalized["视觉焦点"] = normalized["视觉强化"]
    normalized["构图策略"] = normalized["分镜构图"]
    normalized["摄影策略"] = normalized["摄影美学"]
    normalized["运镜策略"] = normalized["运镜手法"]
    return normalized


def transform_text(value: str, transform: str) -> str:
    if transform == "strip_tail_punct":
        return strip_tail_punct(value)
    if transform == "compact_clause":
        return compact_clause(value)
    if transform == "normalize_space":
        return normalize_space(value)
    if transform == "raw":
        return value.strip()
    raise ValueError(f"未知文本变换：{transform}")


def render_part(part: dict[str, Any], source: dict[str, Any], level: str) -> str:
    raw_value = source.get(part["field"], "")
    if not isinstance(raw_value, str) or not raw_value.strip():
        return ""
    transforms = require_dict(part.get("transforms", {}), "part.transforms") if "transforms" in part else {}
    transform = transforms.get(level, part.get("transform", "strip_tail_punct"))
    value = transform_text(raw_value, transform)
    if not value:
        return ""
    templates = require_dict(part.get("templates", {}), "part.templates") if "templates" in part else {}
    template = templates.get(level, part.get("template", "{value}"))
    if not template:
        return ""
    return template.format(value=value, **source)


def render_sentence_group(group_spec: dict[str, Any], source: dict[str, Any], level: str) -> str:
    parts = [
        render_part(require_dict(part, "sentence_group.part"), source, level)
        for part in require_list(group_spec["parts"], "sentence_group.parts")
    ]
    rendered = [strip_tail_punct(part) for part in parts if strip_tail_punct(part)]
    if not rendered and group_spec.get("fallback_parts"):
        fallback = [
            render_part(require_dict(part, "sentence_group.fallback_part"), source, level)
            for part in require_list(group_spec["fallback_parts"], "sentence_group.fallback_parts")
        ]
        rendered = [strip_tail_punct(part) for part in fallback if strip_tail_punct(part)]
    if not rendered:
        return ""
    return ensure_sentence("，".join(rendered))


def require_dict(value: Any, label: str) -> dict[str, Any]:
    if not isinstance(value, dict):
        raise ValueError(f"{label} 必须是对象。")
    return value


def require_list(value: Any, label: str) -> list[Any]:
    if not isinstance(value, list):
        raise ValueError(f"{label} 必须是数组。")
    return value


def require_non_empty_text(value: Any, label: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{label} 不能为空。")
    return value.strip()


def require_int(value: Any, label: str) -> int:
    if not isinstance(value, int):
        raise ValueError(f"{label} 必须是整数。")
    return value


def require_numeric_seconds(value: Any, label: str) -> float:
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise ValueError(f"{label} 必须是有限数值秒数。")
    numeric = float(value)
    if not math.isfinite(numeric):
        raise ValueError(f"{label} 必须是有限数值秒数。")
    return numeric


def format_seconds_label(value: Any, label: str) -> str:
    numeric = require_numeric_seconds(value, label)
    return f"{numeric:g}"


def build_shot_display_index(index: int) -> str:
    return str(index + 1)


def build_script_segment_map(group: dict[str, Any]) -> dict[str, dict[str, Any]]:
    group_id = require_non_empty_text(group.get("分镜组ID"), "分镜组ID")
    script_body = require_non_empty_text(group.get("剧本正文"), f"{group_id}.剧本正文")
    references = require_list(group.get("正文切分参考"), f"{group_id}.正文切分参考")
    if not references:
        raise ValueError(f"{group_id}.正文切分参考 不能为空。")

    segment_map: dict[str, dict[str, Any]] = {}
    for index, raw_item in enumerate(references, start=1):
        item = require_dict(raw_item, f"{group_id}.正文切分参考[{index}]")
        beat_id = require_non_empty_text(item.get("beat_id"), f"{group_id}.正文切分参考[{index}].beat_id")
        if beat_id in segment_map:
            raise ValueError(f"{group_id}.正文切分参考 出现重复 beat_id `{beat_id}`。")
        excerpt = require_non_empty_text(item.get("原文片段"), f"{group_id}.{beat_id}.原文片段")
        char_range = require_dict(item.get("char_range"), f"{group_id}.{beat_id}.char_range")
        start = char_range.get("start")
        end = char_range.get("end")
        if not isinstance(start, int) or not isinstance(end, int):
            raise ValueError(f"{group_id}.{beat_id}.char_range.start/end 必须是整数。")
        if start < 0 or end <= start or end > len(script_body):
            raise ValueError(f"{group_id}.{beat_id}.char_range 超出剧本正文范围。")
        if script_body[start:end] != excerpt:
            raise ValueError(f"{group_id}.{beat_id}.原文片段 与 char_range 指向的剧本正文子串不一致。")
        segment_map[beat_id] = item
    return segment_map


def validate_shot_script_reference(group_id: str, shot: dict[str, Any], segment_map: dict[str, dict[str, Any]]) -> dict[str, Any]:
    shot_id = require_non_empty_text(shot.get("分镜ID"), f"{group_id}.分镜明细[].分镜ID")
    script_ref = require_dict(shot.get("正文回指"), f"{group_id}.{shot_id}.正文回指")
    beat_refs = require_list(script_ref.get("beat_refs"), f"{group_id}.{shot_id}.正文回指.beat_refs")
    if not beat_refs:
        raise ValueError(f"{group_id}.{shot_id}.正文回指.beat_refs 不能为空。")
    for beat_id in beat_refs:
        if not isinstance(beat_id, str) or not beat_id.strip():
            raise ValueError(f"{group_id}.{shot_id}.正文回指.beat_refs[] 只能包含非空字符串。")
        if beat_id not in segment_map:
            raise ValueError(f"{group_id}.{shot_id}.正文回指 指向未知 beat_id `{beat_id}`。")
    coverage_mode = script_ref.get("coverage_mode")
    if coverage_mode not in {"direct", "reaction", "insert", "bridge", "composite"}:
        raise ValueError(f"{group_id}.{shot_id}.正文回指.coverage_mode 非法。")
    return script_ref


def build_script_bridge_text(group_id: str, shot: dict[str, Any], segment_map: dict[str, dict[str, Any]]) -> str:
    script_ref = validate_shot_script_reference(group_id, shot, segment_map)
    beat_refs = require_list(script_ref.get("beat_refs"), f"{group_id}.{shot.get('分镜ID')}.正文回指.beat_refs")
    bridge_parts = [
        require_non_empty_text(segment_map[beat_id].get("原文片段"), f"{group_id}.{beat_id}.原文片段")
        for beat_id in beat_refs
    ]
    bridge_text = " ".join(strip_tail_punct(part) for part in bridge_parts if strip_tail_punct(part)).strip()
    strategy_note = str(script_ref.get("strategy_note", "")).strip()
    coverage_mode = str(script_ref.get("coverage_mode", "")).strip()
    if strategy_note and coverage_mode in {"reaction", "insert", "bridge", "composite"}:
        return "，".join(part for part in [bridge_text, strip_tail_punct(strategy_note)] if part)
    return bridge_text


def validate_shot_ready(group_id: str, shot: dict[str, Any], segment_map: dict[str, dict[str, Any]]) -> None:
    shot_id = require_non_empty_text(shot.get("分镜ID"), f"{group_id}.分镜明细[].分镜ID")
    timing = require_dict(shot.get("时间段"), f"{group_id}.{shot_id}.时间段")
    require_numeric_seconds(timing.get("开始秒"), f"{group_id}.{shot_id}.时间段.开始秒")
    require_numeric_seconds(timing.get("结束秒"), f"{group_id}.{shot_id}.时间段.结束秒")
    validate_shot_script_reference(group_id, shot, segment_map)
    branch_fields = (
        ("角色表现", "人物表演锚点", "人物表演"),
        ("运动表现", "动作路径", "动作调度"),
        ("氛围表现", "空间氛围"),
        ("视觉强化", "视觉抓手", "视觉焦点"),
        ("分镜构图", "构图骨架", "构图策略"),
        ("摄影美学", "摄影策略"),
        ("运镜手法", "运镜策略"),
    )
    for field_names in branch_fields:
        branch_value = pick_branch_object(shot, *field_names)
        require_dict(branch_value, f"{group_id}.{shot_id}.{'/'.join(field_names)}")
    normalized = normalize_shot_for_prompt(shot)
    for field in ("角色表现", "运动表现", "氛围表现", "视觉强化", "分镜构图", "摄影美学", "运镜手法", "景别", "镜头视角"):
        require_non_empty_text(normalized.get(field), f"{group_id}.{shot_id}.{field}")


def validate_group_ready(group: dict[str, Any]) -> None:
    group_id = require_non_empty_text(group.get("分镜组ID"), "分镜组ID")
    require_int(group.get("分镜切换"), f"{group_id}.分镜切换")
    require_non_empty_text(group.get("剧本正文"), f"{group_id}.剧本正文")
    segment_map = build_script_segment_map(group)
    design = require_dict(group.get("组间设计"), f"{group_id}.组间设计")
    for field in ("全局风格", "类型元素", "导演意图", "出场角色及穿搭"):
        require_non_empty_text(design.get(field), f"{group_id}.组间设计.{field}")
    shots = require_list(group.get("分镜明细"), f"{group_id}.分镜明细")
    if not shots:
        raise ValueError(f"{group_id}.分镜明细 不能为空。")
    if len(shots) != group["分镜切换"]:
        raise ValueError(
            f"{group_id} 的 分镜切换={group['分镜切换']}，但 分镜明细 数量为 {len(shots)}；"
            "这说明 3-Detail 仍未完成稳定 handoff。"
        )
    for shot in shots:
        validate_shot_ready(group_id, require_dict(shot, f"{group_id}.分镜明细[]"), segment_map)


def validate_source_ready(source_data: dict[str, Any]) -> tuple[str, list[dict[str, Any]]]:
    metadata = require_dict(source_data.get("metadata"), "metadata")
    episode_id = require_non_empty_text(metadata.get("episode_id"), "metadata.episode_id")
    phase = metadata.get("document_phase")
    if phase != "ready":
        raise ValueError(
            f"metadata.document_phase 当前为 {phase!r}；"
            "只有 ready 状态的 3-Detail shared root 才能被 6-Video/首帧参照消费。"
        )
    final_output = require_dict(source_data.get("final_output"), "final_output")
    main_content = require_dict(final_output.get("main_content"), "final_output.main_content")
    groups = require_list(main_content.get("分镜组列表"), "final_output.main_content.分镜组列表")
    if not groups:
        raise ValueError("final_output.main_content.分镜组列表 不能为空。")
    validated_groups: list[dict[str, Any]] = []
    for raw_group in groups:
        group = require_dict(raw_group, "final_output.main_content.分镜组列表[]")
        validate_group_ready(group)
        validated_groups.append(group)
    return episode_id, validated_groups


def build_time_range(shot: dict[str, Any]) -> str:
    timing = require_dict(shot.get("时间段"), "时间段")
    start = format_seconds_label(timing.get("开始秒"), f"{shot.get('分镜ID', 'unknown')}.时间段.开始秒")
    end = format_seconds_label(timing.get("结束秒"), f"{shot.get('分镜ID', 'unknown')}.时间段.结束秒")
    return f"{start}秒-{end}秒"


def build_min_visible_fact(shot: dict[str, Any]) -> str:
    shot = normalize_shot_for_prompt(shot)
    sentences = []
    first = combine_clauses(
        shot.get("运动表现", ""),
        shot.get("分镜构图", ""),
    )
    second = combine_clauses(
        shot.get("道具及状态", ""),
        shot.get("角色表现", ""),
        shot.get("氛围表现", ""),
    )
    if first:
        sentences.append(first)
    if second:
        sentences.append(second)
    if not sentences:
        sentences.append(ensure_sentence("画面只保留当前分镜可见的最小动作与空间事实"))
    return " ".join(sentences)


def bridge_slice(units: list[str], index: int, total: int) -> list[str]:
    if not units:
        return []
    start = (index * len(units)) // total
    end = ((index + 1) * len(units)) // total
    if end <= start:
        end = start + 1
    return units[start:end]


def build_group_design_block(group: dict[str, Any], spec: dict[str, Any]) -> str:
    design = require_dict(group.get("组间设计"), f"{group.get('分镜组ID')}.组间设计")
    bridge_spec = require_dict(spec["group_design_block"], "spec.group_design_block")
    parts = [
        render_part(require_dict(part, "group_design_block.part"), design, "group")
        for part in require_list(bridge_spec["parts"], "spec.group_design_block.parts")
    ]
    return combine_clauses(*parts, sep=bridge_spec.get("separator", "；"))


def render_clause_parts(parts_spec: list[dict[str, Any]], source: dict[str, Any], level: str) -> list[str]:
    rendered: list[str] = []
    for raw_part in parts_spec:
        part = require_dict(raw_part, "clause_part")
        value = render_part(part, source, level)
        clean = strip_tail_punct(value)
        if clean:
            rendered.append(clean)
    return rendered


def build_camera_clauses(shot: dict[str, Any], level: str, spec: dict[str, Any]) -> list[str]:
    shot_spec = require_dict(spec["shot"], "spec.shot")
    camera_spec = require_list(shot_spec["camera_clauses"], "spec.shot.camera_clauses")
    return render_clause_parts(camera_spec, shot, level)


def build_shot_text(group_id: str, shot: dict[str, Any], shot_index: int, bridge: str, level: str, spec: dict[str, Any]) -> str:
    shot_spec = require_dict(spec["shot"], "spec.shot")
    normalized_shot = normalize_shot_for_prompt(shot)
    normalized_shot["剧情桥段"] = normalize_space(bridge)
    normalized_shot["shot_index"] = build_shot_display_index(shot_index)

    opening = shot_spec["opening_template"].format(
        分镜ID=normalized_shot.get("分镜ID", ""),
        shot_index=normalized_shot["shot_index"],
        time_range=build_time_range(normalized_shot),
    )
    body_parts: list[str] = []

    bridge_spec = require_dict(shot_spec["script_bridge"], "spec.shot.script_bridge")
    bridge_text = render_part(bridge_spec, normalized_shot, level)
    if strip_tail_punct(bridge_text):
        body_parts.append(strip_tail_punct(bridge_text))

    body_parts.extend(build_camera_clauses(normalized_shot, level, spec))

    detail_sentences = require_dict(shot_spec["detail_sentences"], "spec.shot.detail_sentences")
    for sentence_group in require_list(detail_sentences[level], f"spec.shot.detail_sentences.{level}"):
        rendered = render_sentence_group(require_dict(sentence_group, "detail_sentence_group"), normalized_shot, level)
        clean = strip_tail_punct(rendered)
        if clean:
            body_parts.append(clean)

    for hook in require_list(shot_spec.get("optional_hooks", []), "spec.shot.optional_hooks"):
        hook_spec = require_dict(hook, "optional_hook")
        level_spec = require_dict(
            require_dict(hook_spec["levels"], "optional_hook.levels").get(level, {}),
            f"optional_hook.levels.{level}",
        )
        template = level_spec.get("template", "")
        if not template:
            continue
        raw_value = normalized_shot.get(hook_spec["field"], "")
        if not isinstance(raw_value, str) or not raw_value.strip():
            continue
        value = transform_text(raw_value, level_spec.get("transform", "strip_tail_punct"))
        if not value:
            continue
        body_parts.append(strip_tail_punct(template.format(value=value, **normalized_shot)))

    body = ensure_sentence("，".join(part for part in body_parts if part))
    return f"{opening}{body}" if body else opening


def compose_prompt(group: dict[str, Any], shot: dict[str, Any], shot_index: int, bridge: str, detail_level: str, spec: dict[str, Any]) -> str:
    sections = [
        build_group_design_block(group, spec),
        build_shot_text(require_non_empty_text(group.get("分镜组ID"), "分镜组ID"), shot, shot_index, bridge, detail_level, spec),
    ]
    return "\n".join(section for section in sections if section).strip()


def choose_detail_level(group: dict[str, Any], shot: dict[str, Any], shot_index: int, bridge: str, spec: dict[str, Any]) -> tuple[str, str]:
    prompt_full = compose_prompt(group, shot, shot_index, bridge, "full", spec)
    if len(prompt_full) <= TARGET_MAX:
        return "full", "normal"

    prompt_normal = compose_prompt(group, shot, shot_index, bridge, "normal", spec)
    if len(prompt_normal) <= TARGET_MAX:
        return "normal", "normal"

    prompt_tight = compose_prompt(group, shot, shot_index, bridge, "tight", spec)
    if len(prompt_tight) <= TARGET_MAX:
        return "tight", "tight"

    prompt_ultra = compose_prompt(group, shot, shot_index, bridge, "ultra", spec)
    if len(prompt_ultra) <= TARGET_MAX:
        return "ultra", "tight"

    raise ValueError(f"分镜 {shot.get('分镜ID')} 在 ultra 压缩后仍超过 {TARGET_MAX} 字。")


def build_request_packet(
    template: dict[str, Any],
    episode_id: str,
    source_rel: str,
    group: dict[str, Any],
    shot: dict[str, Any],
    prompt: str,
) -> dict[str, Any]:
    packet = copy.deepcopy(template)
    timing = require_dict(shot.get("时间段"), f"{shot.get('分镜ID')}.时间段")
    start = require_numeric_seconds(timing.get("开始秒"), f"{shot.get('分镜ID')}.时间段.开始秒")
    end = require_numeric_seconds(timing.get("结束秒"), f"{shot.get('分镜ID')}.时间段.结束秒")
    duration = max(1.0, end - start)

    packet["meta"]["episode_id"] = episode_id
    packet["meta"]["shot_level"] = "storyboard_frame"
    packet["meta"]["group_id"] = group["分镜组ID"]
    packet["meta"]["source_shot_ids"] = [shot["分镜ID"]]
    packet["meta"]["source_file"] = source_rel
    packet["meta"]["source_schema"] = SOURCE_SCHEMA
    packet["meta"]["template_version"] = "v1"
    packet["prompt_style"]["type"] = "multimodal2video"
    packet["prompt_style"]["language"] = "zh-CN"
    packet["prompt_style"]["char_limit"] = TARGET_CHAR_LIMIT
    packet["model"]["model_version"] = "seedance2.0"
    packet["model"]["duration"] = f"{duration:g}"
    packet["model"]["ratio"] = "16:9"
    packet["model"]["video_resolution"] = "720p"
    if "reference_images" not in packet["model"]:
        packet["model"]["reference_images"] = []
    if "image_markers" not in packet["model"] or not isinstance(packet["model"]["image_markers"], list):
        packet["model"]["image_markers"] = [
            {
                "image_ref": "<图片引用>",
                "ref_kind": "pending",
                "related_subject": "<关联主体>",
                "image_no": "图1",
            }
        ]
    packet["prompt"] = prompt
    packet["prompt_char_count"] = len(prompt)
    return packet


def build_txt_view(episode_id: str, packets: list[dict[str, Any]]) -> str:
    sections = [f"# {episode_id} 首帧参照"]
    for packet in packets:
        shot_display_index = packet["meta"].get("shot_display_index", "")
        sections.append(
            "\n".join(
                [
                    f"## 分镜{shot_display_index}",
                    "",
                    packet["prompt"],
                    "",
                    f"字数统计: {packet['prompt_char_count']}",
                    "",
                    "---",
                ]
            )
        )
    return "\n\n".join(sections).rstrip() + "\n"


def validate_packet(packet: dict[str, Any], group: dict[str, Any], shot: dict[str, Any]) -> None:
    prompt = require_non_empty_text(packet.get("prompt"), "packet.prompt")
    shot_id = shot["分镜ID"]
    group_id = group["分镜组ID"]
    shot_index = next(idx for idx, candidate in enumerate(require_list(group.get("分镜明细"), f"{group_id}.分镜明细")) if require_dict(candidate, f"{group_id}.分镜明细[]")["分镜ID"] == shot_id)
    expected_anchor = f"{build_time_range(shot)}｜分镜{build_shot_display_index(shot_index)}："
    forbidden_labels = [
        "类型元素：",
        "导演意图：",
        "出场角色及穿搭：",
        "时间段：",
        "角色背景面：",
        "角色站位走位：",
        "人物表演：",
        "人物表演锚点：",
        "动作调度：",
        "动作路径：",
        "空间氛围：",
        "视觉焦点：",
        "视觉抓手：",
        "构图策略：",
        "构图骨架：",
        "摄影策略：",
        "运镜策略：",
        "转场策略：",
        "景别：",
        "运镜手法：",
        "镜头速度：",
        "镜头视角：",
        "角色表现：",
        "运动表现：",
        "氛围表现：",
        "视觉强化：",
        "分镜构图：",
        "场景氛围：",
        "道具及状态：",
        "摄影美学：",
        "镜头属性：",
        "镜头类型兼容：",
        "镜头框架：",
        "镜头类型：",
        "分镜表现：",
        "转场特效：",
    ]

    if packet["prompt_char_count"] != len(prompt):
        raise ValueError(f"{shot_id} 的 prompt_char_count 与实际长度不一致。")
    if any(label in prompt for label in forbidden_labels):
        raise ValueError(f"{shot_id} 泄露了字段标题。")
    if re.search(rf"分镜\s*{re.escape(shot_id)}\s*的\s*\d+秒-\d+秒", prompt):
        raise ValueError(f"{shot_id} 出现了“分镜 ID 的 时间”写法。")
    if expected_anchor not in prompt:
        raise ValueError(f"{shot_id} 缺少时间锚点 {expected_anchor}。")
    if f"分镜 {shot_id} " in prompt or f"分镜{shot_id}：" in prompt:
        raise ValueError(f"{shot_id} 泄露了完整四段式分镜ID。")
    style_anchor = strip_tail_punct(str(group["组间设计"]["全局风格"]).strip())
    if style_anchor and style_anchor not in prompt:
        raise ValueError(f"{shot_id} 未保留组级设计块中的全局风格。")
    if packet["meta"]["group_id"] != group_id:
        raise ValueError(f"{shot_id} 的 group_id 回链错误。")
    if packet["meta"]["source_shot_ids"] != [shot_id]:
        raise ValueError(f"{shot_id} 的 source_shot_ids 必须仅包含自身。")
    if "reference_images" not in packet["model"]:
        raise ValueError(f"{shot_id} 缺少 reference_images 字段。")
    image_markers = packet["model"].get("image_markers")
    if not isinstance(image_markers, list) or not image_markers:
        raise ValueError(f"{shot_id} 缺少 image_markers 模板骨架。")
    for marker in image_markers:
        if not isinstance(marker, dict) or sorted(marker.keys()) != ["image_no", "image_ref", "ref_kind", "related_subject"]:
            raise ValueError(f"{shot_id} 的 image_markers 结构不符合共享模板骨架。")


def render_episode(project_name: str, episode_id: str, shot_id: str | None = None) -> dict[str, Any]:
    project_root = resolve_project_root(project_name)
    source_path = project_root / "3-Detail" / f"{episode_id}.json"
    output_dir = project_root / "6-Video" / "首帧参照" / episode_id
    output_dir.mkdir(parents=True, exist_ok=True)

    source_data = require_dict(read_json(source_path), str(source_path))
    prompt_spec = load_prompt_assembly_spec()
    detected_episode_id, groups = validate_source_ready(source_data)
    if detected_episode_id != episode_id:
        raise ValueError(f"文件内 episode_id={detected_episode_id}，但执行参数为 {episode_id}。")
    template = read_json(TEMPLATE_JSON)
    generated_at = datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")
    source_rel = str(source_path.relative_to(ROOT))

    request_packets: list[dict[str, Any]] = []
    manifest_shots: list[dict[str, Any]] = []
    bridge_strategy_summary = {"direct_match": 0, "ambiguous": 0}
    budget_strategy_summary = {"normal": 0, "tight": 0}
    target_shot_found = shot_id is None

    for group in groups:
        shots = require_list(group.get("分镜明细"), f"{group.get('分镜组ID')}.分镜明细")
        for index, raw_shot in enumerate(shots):
            shot = require_dict(raw_shot, f"{group.get('分镜组ID')}.分镜明细[]")
            current_shot_id = shot["分镜ID"]
            if shot_id and current_shot_id != shot_id:
                continue

            target_shot_found = True
            segment_map = build_script_segment_map(group)
            bridge = build_script_bridge_text(group["分镜组ID"], shot, segment_map)
            bridge_strategy = "direct_match" if require_dict(shot.get("正文回指"), f"{group['分镜组ID']}.{current_shot_id}.正文回指").get("coverage_mode") == "direct" else "ambiguous"
            bridge_note = str(require_dict(shot.get("正文回指"), f"{group['分镜组ID']}.{current_shot_id}.正文回指").get("strategy_note", "")).strip()
            detail_level, budget_strategy = choose_detail_level(group, shot, index, bridge, prompt_spec)
            prompt = compose_prompt(group, shot, index, bridge, detail_level, prompt_spec)
            packet = build_request_packet(template, episode_id, source_rel, group, shot, prompt)
            packet["meta"]["shot_display_index"] = build_shot_display_index(index)
            validate_packet(packet, group, shot)

            within_target_range = packet["prompt_char_count"] <= TARGET_MAX
            exception_notes = []
            if bridge_note:
                exception_notes.append(bridge_note)
            if budget_strategy == "tight":
                exception_notes.append("为命中首帧字数窗，已先压缩 P3，再收束部分 P2。")

            request_packets.append(packet)
            bridge_strategy_summary[bridge_strategy] += 1
            budget_strategy_summary[budget_strategy] += 1
            manifest_shots.append(
                {
                    "group_id": group["分镜组ID"],
                    "shot_id": current_shot_id,
                    "shot_display_index": build_shot_display_index(index),
                    "coverage_mode": require_dict(shot.get("正文回指"), f"{group['分镜组ID']}.{current_shot_id}.正文回指")["coverage_mode"],
                    "beat_refs": require_dict(shot.get("正文回指"), f"{group['分镜组ID']}.{current_shot_id}.正文回指")["beat_refs"],
                    "prompt_char_count": packet["prompt_char_count"],
                    "bridge_strategy": bridge_strategy,
                    "within_target_range": within_target_range,
                    "exception_note": " ".join(exception_notes).strip(),
                }
            )

    if not target_shot_found:
        raise ValueError(f"在 {episode_id} 中未找到目标分镜 {shot_id}。")
    if not request_packets:
        raise ValueError(f"{episode_id} 没有生成任何首帧参照请求。")

    episode_payload = {
        "episode_id": episode_id,
        "project_name": project_name,
        "source_file": source_rel,
        "source_schema": SOURCE_SCHEMA,
        "tranche": "6-Video/首帧参照",
        "request_type": "frame_request_packets",
        "generated_at": generated_at,
        "shot_count": len(request_packets),
        "request_packets": request_packets,
    }
    manifest_payload = {
        "episode_id": episode_id,
        "project_name": project_name,
        "source_file": source_rel,
        "generated_at": generated_at,
        "output_mode": "full_trace",
        "json_file": str((output_dir / f"{episode_id}.json").relative_to(ROOT)),
        "txt_file": str((output_dir / f"{episode_id}.txt").relative_to(ROOT)),
        "shot_count": len(request_packets),
        "bridge_strategy_summary": bridge_strategy_summary,
        "budget_strategy_summary": budget_strategy_summary,
        "shots": manifest_shots,
    }

    write_json(output_dir / f"{episode_id}.json", episode_payload)
    write_json(output_dir / "_manifest.json", manifest_payload)
    (output_dir / f"{episode_id}.txt").write_text(build_txt_view(episode_id, request_packets), encoding="utf-8")

    return {
        "episode_id": episode_id,
        "shot_count": len(request_packets),
        "bridge_strategy_summary": bridge_strategy_summary,
        "budget_strategy_summary": budget_strategy_summary,
        "max_prompt_chars": max(packet["prompt_char_count"] for packet in request_packets),
        "min_prompt_chars": min(packet["prompt_char_count"] for packet in request_packets),
        "output_dir": str(output_dir),
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="重建 6-Video/首帧参照 的 episode 三件套。")
    parser.add_argument("--project", required=True, help="项目名，例如 2049退休老头的快乐生活")
    parser.add_argument("--episode", required=True, help="集名，例如 第1集")
    parser.add_argument("--shot-id", help="可选，只生成单个分镜ID的首帧参照")
    args = parser.parse_args()

    print(
        json.dumps(
            render_episode(args.project, args.episode, args.shot_id),
            ensure_ascii=False,
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
