#!/usr/bin/env python3
from __future__ import annotations

import json
import math
import re
import sys
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
AIGC_SHARED_DIR = ROOT / ".agents" / "skills" / "aigc" / "_shared"
if str(AIGC_SHARED_DIR) not in sys.path:
    sys.path.insert(0, str(AIGC_SHARED_DIR))

from detail_root_adapter import CANONICAL_DETAIL_TEMPLATE, ensure_legacy_detail_payload, sort_identifier  # noqa: E402


SOURCE_SCHEMA = CANONICAL_DETAIL_TEMPLATE
TEMPLATE_JSON = ROOT / ".agents/skills/aigc/5-Image/_shared/image-generation-input.template.json"
SHOT_SCALE_TOKENS = (
    "超大全景",
    "大全景",
    "大远景",
    "中远景",
    "中近景",
    "全景",
    "远景",
    "中景",
    "近景",
    "特写",
)
SHOT_ANGLE_TOKENS = (
    "略后侧视角",
    "后侧视角",
    "略侧平视",
    "侧平视",
    "侧视角",
    "低角度仰视",
    "高角度俯视",
    "平视",
    "俯视",
    "仰视",
    "过肩",
    "主观视角",
    "鸟瞰",
)
SHOT_SPEED_TOKENS = (
    "极慢推近",
    "极慢速收束",
    "慢速压近",
    "缓慢推进",
    "极慢速推进",
    "慢速推进",
    "静止",
    "极慢",
    "慢速",
    "缓慢",
    "定镜",
)


def read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def resolve_project_root(project_name: str) -> Path:
    project_root = PROJECTS_ROOT / project_name
    if not project_root.exists():
        raise FileNotFoundError(
            f"未找到 canonical AIGC 项目根：{project_root}。"
            "本技能只消费 projects/aigc/<项目名>/ 下的运行时真源。"
        )
    return project_root


def load_prompt_assembly_spec(path: Path) -> dict[str, Any]:
    content = path.read_text(encoding="utf-8")
    match = re.search(r"```json\s*(\{.*\})\s*```", content, re.DOTALL)
    if not match:
        raise ValueError(f"{path} 缺少 canonical JSON spec code block。")
    return require_dict(json.loads(match.group(1)), f"{path.name}.spec")


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


def flatten_text_value(value: Any, preferred_keys: tuple[str, ...] = ()) -> str:
    if isinstance(value, str):
        return normalize_space(value)
    if isinstance(value, list):
        return join_non_empty([flatten_text_value(item, preferred_keys) for item in value])
    if isinstance(value, dict):
        ordered_keys = list(preferred_keys)
        ordered_keys.extend(key for key in value.keys() if key not in ordered_keys)
        return join_non_empty([flatten_text_value(value.get(key), preferred_keys) for key in ordered_keys])
    return ""


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


def extract_token(text: str, candidates: tuple[str, ...]) -> str:
    for candidate in candidates:
        if candidate in text:
            return candidate
    return ""


def infer_shot_descriptor(normalized: dict[str, Any], candidates: tuple[str, ...]) -> str:
    sources = (
        str(normalized.get("运镜手法", "")).strip(),
        str(normalized.get("分镜构图", "")).strip(),
        str(normalized.get("分镜表现", "")).strip(),
        str(normalized.get("镜头框架", "")).strip(),
        str(normalized.get("镜头类型", "")).strip(),
        str(normalized.get("镜头类型兼容", "")).strip(),
    )
    for source in sources:
        token = extract_token(source, candidates)
        if token:
            return token
    return ""


def normalize_shot_for_prompt(shot: dict[str, Any]) -> dict[str, Any]:
    normalized = dict(shot)
    anchor = pick_branch_object(normalized, "主体锚定")
    normalized["主体锚定"] = first_non_empty(
        flatten_text_value(anchor, ("场景", "角色", "道具")),
        str(normalized.get("主体锚定", "")).strip(),
    )
    normalized["道具及状态"] = first_non_empty(
        str(normalized.get("道具及状态", "")).strip(),
        flatten_text_value(anchor.get("道具") if isinstance(anchor, dict) else ""),
    )
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
        compact_branch_design(
            pick_branch_object(normalized, "氛围表现", "空间氛围"),
            ("层次", "意境", "空间诗学", "空间支架", "空气层", "物象压力"),
            limit=2,
        ),
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
        compact_branch_design(
            pick_branch_object(normalized, "运镜手法", "运镜策略"),
            ("组合", "变化", "运动动机", "运动路径"),
            limit=2,
        ),
        str(normalized.get("运镜手法", "")).strip(),
        str(normalized.get("运镜策略", "")).strip(),
    )
    normalized["镜头速度"] = first_non_empty(
        compact_branch_design(pick_branch_object(normalized, "运镜手法", "运镜策略"), ("速度", "速度设计"), limit=1),
        str(normalized.get("镜头速度", "")).strip(),
        infer_shot_descriptor(normalized, SHOT_SPEED_TOKENS),
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
        infer_shot_descriptor(normalized, SHOT_SCALE_TOKENS),
    )
    normalized["镜头视角"] = first_non_empty(
        str(normalized.get("镜头视角", "")).strip(),
        infer_shot_descriptor(normalized, SHOT_ANGLE_TOKENS),
    )
    normalized["镜头类型"] = first_non_empty(
        str(normalized.get("镜头类型", "")).strip(),
        compact_branch_design(pick_branch_object(normalized, "分镜构图", "构图骨架", "构图策略"), ("镜头类型",), limit=1),
    )
    normalized["镜头类型兼容"] = first_non_empty(
        str(normalized.get("镜头类型兼容", "")).strip(),
        str(normalized.get("镜头属性", "")).strip(),
        normalized["镜头类型"],
        normalized["镜头框架"],
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


def render_clause_parts(parts_spec: list[dict[str, Any]], source: dict[str, Any], level: str) -> list[str]:
    rendered: list[str] = []
    for raw_part in parts_spec:
        part = require_dict(raw_part, "clause_part")
        value = render_part(part, source, level)
        clean = strip_tail_punct(value)
        if clean:
            rendered.append(clean)
    return rendered


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
    return f"{require_numeric_seconds(value, label):g}"


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


def validate_source_ready(source_data: dict[str, Any], allowed_phases: set[str]) -> tuple[str, list[dict[str, Any]]]:
    source_payload = ensure_legacy_detail_payload(source_data)
    metadata = require_dict(source_payload.get("metadata"), "metadata")
    episode_id = require_non_empty_text(metadata.get("episode_id"), "metadata.episode_id")
    phase = metadata.get("document_phase")
    if phase not in allowed_phases:
        phase_label = ", ".join(sorted(allowed_phases))
        raise ValueError(
            f"3-Detail detail root 当前推断的 readiness 为 {phase!r}；"
            f"只有 {phase_label} 状态的 canonical detail root 才能被 5-Image 叶子消费。"
        )
    final_output = require_dict(source_payload.get("final_output"), "final_output")
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
    if isinstance(shot.get("时间段"), dict):
        timing = require_dict(shot.get("时间段"), "时间段")
        start = format_seconds_label(timing.get("开始秒"), f"{shot.get('分镜ID', 'unknown')}.时间段.开始秒")
        end = format_seconds_label(timing.get("结束秒"), f"{shot.get('分镜ID', 'unknown')}.时间段.结束秒")
        return f"{start}秒-{end}秒"
    time_text = require_non_empty_text(shot.get("时间"), f"{shot.get('分镜ID', 'unknown')}.时间")
    matched = re.match(r"^\s*(?P<start>\d+(?:\.\d+)?)\s*-\s*(?P<end>\d+(?:\.\d+)?)秒\s*$", time_text)
    if not matched:
        raise ValueError(f"{shot.get('分镜ID', 'unknown')}.时间 必须符合 `<开始>-<结束>秒`。")
    return f"{matched.group('start')}秒-{matched.group('end')}秒"


def build_group_design_block(group: dict[str, Any], spec: dict[str, Any]) -> str:
    design = require_dict(group.get("组间设计"), f"{group.get('分镜组ID')}.组间设计")
    bridge_spec = require_dict(spec["group_design_block"], "spec.group_design_block")
    parts = [
        render_part(require_dict(part, "group_design_block.part"), design, "group")
        for part in require_list(bridge_spec["parts"], "spec.group_design_block.parts")
    ]
    return combine_clauses(*parts, sep=bridge_spec.get("separator", "；"))


def build_camera_clauses(shot: dict[str, Any], level: str, spec: dict[str, Any]) -> list[str]:
    shot_spec = require_dict(spec["shot"], "spec.shot")
    camera_spec = require_list(shot_spec["camera_clauses"], "spec.shot.camera_clauses")
    return render_clause_parts(camera_spec, shot, level)


def build_prompt_prefix(spec: dict[str, Any]) -> str:
    prefix_lines = require_list(spec["prefix_lines"], "spec.prefix_lines")
    return "\n".join(require_non_empty_text(line, "spec.prefix_line") for line in prefix_lines)


def ordered_canonical_groups(source_data: dict[str, Any]) -> list[dict[str, Any]]:
    if isinstance(source_data.get("groups"), list):
        groups = require_list(source_data.get("groups"), "groups")
    else:
        source_payload = ensure_legacy_detail_payload(source_data)
        metadata = require_dict(source_payload.get("metadata"), "metadata")
        require_non_empty_text(metadata.get("episode_id"), "metadata.episode_id")
        final_output = require_dict(source_payload.get("final_output"), "final_output")
        main_content = require_dict(final_output.get("main_content"), "final_output.main_content")
        groups = require_list(main_content.get("分镜组列表"), "final_output.main_content.分镜组列表")
    ordered = sorted(
        (group for group in groups if isinstance(group, dict)),
        key=lambda item: sort_identifier(str(item.get("分镜组ID", ""))),
    )
    if not ordered:
        raise ValueError("groups[] 不能为空。")
    return ordered


def ordered_canonical_shots(group: dict[str, Any]) -> list[dict[str, Any]]:
    group_id = require_non_empty_text(group.get("分镜组ID"), "分镜组ID")
    ordered: list[dict[str, Any]] = []
    if isinstance(group.get("detail"), dict):
        detail = require_dict(group.get("detail"), f"{group_id}.detail")
        shot_map = require_dict(detail.get("分镜列表"), f"{group_id}.detail.分镜列表")
        for shot_id, raw_shot in sorted(shot_map.items(), key=lambda item: sort_identifier(str(item[0]))):
            shot = require_dict(raw_shot, f"{group_id}.detail.分镜列表.{shot_id}")
            ordered.append({"分镜ID": str(shot_id), **shot})
    else:
        for raw_shot in require_list(group.get("分镜明细"), f"{group_id}.分镜明细"):
            shot = require_dict(raw_shot, f"{group_id}.分镜明细[]")
            ordered.append(shot)
    if not ordered:
        raise ValueError(f"{group_id} 未提供可消费的分镜列表。")
    return ordered


def validate_canonical_shot_ready(group_id: str, shot: dict[str, Any]) -> None:
    shot_id = require_non_empty_text(shot.get("分镜ID"), f"{group_id}.detail.分镜列表[].分镜ID")
    require_non_empty_text(shot.get("时间"), f"{group_id}.{shot_id}.时间")
    require_non_empty_text(shot.get("剧本正文"), f"{group_id}.{shot_id}.剧本正文")
    require_dict(shot.get("主体锚定"), f"{group_id}.{shot_id}.主体锚定")
    for branch_field in ("分镜构图", "运镜手法", "角色表现", "氛围表现", "摄影表现", "转场特效"):
        require_dict(shot.get(branch_field), f"{group_id}.{shot_id}.{branch_field}")
    normalized = normalize_shot_for_prompt(shot)
    for field in ("主体锚定", "角色表现", "运动表现", "氛围表现", "分镜构图", "摄影美学", "运镜手法", "景别", "镜头视角"):
        require_non_empty_text(normalized.get(field), f"{group_id}.{shot_id}.{field}")


def validate_canonical_group_ready(group: dict[str, Any]) -> None:
    group_id = require_non_empty_text(group.get("分镜组ID"), "分镜组ID")
    if not isinstance(group.get("detail"), dict):
        validate_group_ready(group)
        return
    global_block = require_dict(group.get("global"), f"{group_id}.global")
    for field in ("全局风格", "类型元素", "导演意图"):
        require_non_empty_text(global_block.get(field), f"{group_id}.global.{field}")
    detail = require_dict(group.get("detail"), f"{group_id}.detail")
    declared_shot_count = require_int(detail.get("分镜数"), f"{group_id}.detail.分镜数")
    shots = ordered_canonical_shots(group)
    if declared_shot_count != len(shots):
        raise ValueError(
            f"{group_id} 的 detail.分镜数={declared_shot_count}，但 detail.分镜列表 数量为 {len(shots)}；"
            "这说明 canonical detail 仍未完成稳定 handoff。"
        )
    for shot in shots:
        validate_canonical_shot_ready(group_id, shot)


def infer_canonical_phase(groups: list[dict[str, Any]]) -> str:
    try:
        for group in groups:
            validate_canonical_group_ready(group)
    except ValueError:
        return "detail_in_progress"
    return "ready"


def validate_canonical_source_ready(source_data: dict[str, Any], allowed_phases: set[str]) -> tuple[str, list[dict[str, Any]]]:
    if isinstance(source_data.get("meta"), dict):
        meta = require_dict(source_data.get("meta"), "meta")
        episode_id = require_non_empty_text(meta.get("集数"), "meta.集数")
    else:
        source_payload = ensure_legacy_detail_payload(source_data)
        metadata = require_dict(source_payload.get("metadata"), "metadata")
        episode_id = require_non_empty_text(metadata.get("episode_id"), "metadata.episode_id")
    groups = ordered_canonical_groups(source_data)
    phase = infer_canonical_phase(groups)
    if phase not in allowed_phases:
        phase_label = ", ".join(sorted(allowed_phases))
        raise ValueError(
            f"canonical detail root 当前推断的 readiness 为 {phase!r}；"
            f"只有 {phase_label} 状态的 canonical detail root 才能被 5-Image 叶子消费。"
        )
    for group in groups:
        validate_canonical_group_ready(group)
    return episode_id, groups


def build_canonical_group_design_block(group: dict[str, Any], spec: dict[str, Any]) -> str:
    group_id = require_non_empty_text(group.get("分镜组ID"), "分镜组ID")
    global_block = (
        require_dict(group.get("global"), f"{group_id}.global")
        if isinstance(group.get("global"), dict)
        else require_dict(group.get("组间设计"), f"{group_id}.组间设计")
    )
    bridge_spec = require_dict(spec["group_design_block"], "spec.group_design_block")
    parts = [
        render_part(require_dict(part, "group_design_block.part"), global_block, "group")
        for part in require_list(bridge_spec["parts"], "spec.group_design_block.parts")
    ]
    return combine_clauses(*parts, sep=bridge_spec.get("separator", "；"))
