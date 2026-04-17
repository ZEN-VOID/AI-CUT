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


def validate_shot_ready(group_id: str, shot: dict[str, Any]) -> None:
    shot_id = require_non_empty_text(shot.get("分镜ID"), f"{group_id}.分镜明细[].分镜ID")
    timing = require_dict(shot.get("时间段"), f"{group_id}.{shot_id}.时间段")
    require_numeric_seconds(timing.get("开始秒"), f"{group_id}.{shot_id}.时间段.开始秒")
    require_numeric_seconds(timing.get("结束秒"), f"{group_id}.{shot_id}.时间段.结束秒")
    for field in ("角色背景面", "角色站位走位", "道具及状态", "分镜表现", "景别", "运镜手法", "摄影美学", "镜头视角"):
        require_non_empty_text(shot.get(field), f"{group_id}.{shot_id}.{field}")


def validate_group_ready(group: dict[str, Any]) -> None:
    group_id = require_non_empty_text(group.get("分镜组ID"), "分镜组ID")
    require_int(group.get("分镜切换"), f"{group_id}.分镜切换")
    require_non_empty_text(group.get("剧本正文"), f"{group_id}.剧本正文")
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
        validate_shot_ready(group_id, require_dict(shot, f"{group_id}.分镜明细[]"))


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


def split_sentences(text: str) -> list[str]:
    pattern = re.compile(r"[^。！？!?]+(?:[。！？!?][”’\"]?)?|[^。！？!?]+$")
    sentences = [normalize_space(item) for item in pattern.findall(normalize_space(text))]
    return [item for item in sentences if item]


def extract_script_blocks(script: str) -> list[str]:
    text = normalize_space(script)
    text = re.sub(r"#+\s*", "", text)
    marker_pattern = re.compile(r"(动作画面|对白画面|对白（[^）]+）)：")
    matches = list(marker_pattern.finditer(text))
    blocks: list[str] = []

    if not matches:
        return split_sentences(text)

    prefix = text[: matches[0].start()].strip()
    if prefix and not prefix.startswith("场景"):
        blocks.extend(split_sentences(prefix))

    for idx, match in enumerate(matches):
        start = match.end()
        end = matches[idx + 1].start() if idx + 1 < len(matches) else len(text)
        content = normalize_space(text[start:end])
        if content:
            blocks.append(content)

    return [block for block in blocks if block]


def build_min_visible_fact(shot: dict[str, Any]) -> str:
    sentences = []
    first = combine_clauses(
        shot.get("角色站位走位", ""),
        shot.get("角色背景面", ""),
    )
    second = combine_clauses(
        shot.get("道具及状态", ""),
        shot.get("角色表现", ""),
        shot.get("场景氛围", ""),
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


def extract_bridge(
    group: dict[str, Any],
    shot: dict[str, Any],
    shot_index: int,
) -> tuple[str, str, str]:
    shots = require_list(group.get("分镜明细"), f"{group.get('分镜组ID')}.分镜明细")
    script_text = require_non_empty_text(group.get("剧本正文"), f"{group.get('分镜组ID')}.剧本正文")
    script_blocks = extract_script_blocks(script_text)
    script_units = script_blocks if len(script_blocks) >= len(shots) else [sentence for block in script_blocks for sentence in split_sentences(block)]

    if len(shots) == 1:
        return normalize_space(group["剧本正文"]), "single_shot", ""

    if len(script_units) >= len(shots):
        selected = bridge_slice(script_units, shot_index, len(shots))
        bridge = " ".join(selected).strip()
        if bridge:
            return bridge, "direct_match", ""

    selected = bridge_slice(script_units, shot_index, len(shots))
    visible_fallback = build_min_visible_fact(shot)
    bridge_base = " ".join(selected).strip()
    if bridge_base:
        note = "剧本正文桥段边界不足以稳定一镜一段，已保守压到目标分镜可见事实。"
        return f"{bridge_base} {visible_fallback}".strip(), "ambiguous", note
    note = "剧本正文无法稳定拆到镜级，已仅保留目标分镜可见的最小剧情事实。"
    return visible_fallback, "ambiguous", note


def build_group_context(design: dict[str, Any], level: str, spec: dict[str, Any]) -> str:
    bridge_spec = require_dict(spec["group_bridge"], "spec.group_bridge")
    parts = [
        render_part(require_dict(part, "group_bridge.part"), design, level)
        for part in require_list(bridge_spec["parts"], "spec.group_bridge.parts")
    ]
    return combine_clauses(*parts, sep=bridge_spec.get("separator", "，"))


def build_camera_sentence(shot: dict[str, Any], level: str, spec: dict[str, Any]) -> str:
    shot_id = require_non_empty_text(shot.get("分镜ID"), "分镜ID")
    shot_spec = require_dict(spec["shot"], "spec.shot")
    camera_spec = require_dict(shot_spec["camera_sentence"], "spec.shot.camera_sentence")
    opening = shot_spec["opening_template"].format(分镜ID=shot_id, time_range=build_time_range(shot))
    clauses = [opening]
    for clause_spec in require_list(camera_spec["clauses"], "spec.shot.camera_sentence.clauses"):
        rendered = render_part(require_dict(clause_spec, "camera_clause"), shot, level)
        if rendered:
            clauses.append(rendered)
    return combine_clauses(*clauses, sep=camera_spec.get("separator", "，"))


def build_shot_text(shot: dict[str, Any], level: str, spec: dict[str, Any]) -> str:
    shot_spec = require_dict(spec["shot"], "spec.shot")
    sentences: list[str] = [build_camera_sentence(shot, level, spec)]

    detail_sentences = require_dict(shot_spec["detail_sentences"], "spec.shot.detail_sentences")
    for sentence_group in require_list(detail_sentences[level], f"spec.shot.detail_sentences.{level}"):
        rendered = render_sentence_group(require_dict(sentence_group, "detail_sentence_group"), shot, level)
        if rendered:
            sentences.append(rendered)

    for hook in require_list(shot_spec.get("optional_hooks", []), "spec.shot.optional_hooks"):
        hook_spec = require_dict(hook, "optional_hook")
        level_spec = require_dict(
            require_dict(hook_spec["levels"], "optional_hook.levels").get(level, {}),
            f"optional_hook.levels.{level}",
        )
        template = level_spec.get("template", "")
        if not template:
            continue
        raw_value = shot.get(hook_spec["field"], "")
        if not isinstance(raw_value, str) or not raw_value.strip():
            continue
        value = transform_text(raw_value, level_spec.get("transform", "strip_tail_punct"))
        if not value:
            continue
        sentences.append(ensure_sentence(template.format(value=value, **shot)))

    return " ".join(sentence for sentence in sentences if sentence)


def compose_prompt(group: dict[str, Any], shot: dict[str, Any], bridge: str, detail_level: str, spec: dict[str, Any]) -> str:
    design = require_dict(group.get("组间设计"), f"{group.get('分镜组ID')}.组间设计")
    sections = [
        f"分镜组 {group['分镜组ID']}",
        ensure_sentence(bridge),
        design["全局风格"].strip(),
        build_group_context(design, detail_level, spec),
        build_shot_text(shot, detail_level, spec),
    ]
    return "\n\n".join(section for section in sections if section).strip()


def choose_detail_level(group: dict[str, Any], shot: dict[str, Any], bridge: str, spec: dict[str, Any]) -> tuple[str, str]:
    prompt_full = compose_prompt(group, shot, bridge, "full", spec)
    if len(prompt_full) <= TARGET_MAX:
        return "full", "normal"

    prompt_normal = compose_prompt(group, shot, bridge, "normal", spec)
    if len(prompt_normal) <= TARGET_MAX:
        return "normal", "normal"

    prompt_tight = compose_prompt(group, shot, bridge, "tight", spec)
    if len(prompt_tight) <= TARGET_MAX:
        return "tight", "tight"

    prompt_ultra = compose_prompt(group, shot, bridge, "ultra", spec)
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
        shot_id = packet["meta"]["source_shot_ids"][0]
        group_id = packet["meta"]["group_id"]
        sections.append(
            "\n".join(
                [
                    f"## 分镜 {shot_id}",
                    f"所属分镜组: {group_id}",
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
    expected_anchor = f"分镜 {shot_id} {build_time_range(shot)}"
    forbidden_labels = [
        "类型元素：",
        "导演意图：",
        "出场角色及穿搭：",
        "时间段：",
        "角色背景面：",
        "角色站位走位：",
        "景别：",
        "运镜手法：",
        "镜头速度：",
        "镜头视角：",
        "角色表现：",
        "场景氛围：",
        "道具及状态：",
        "摄影美学：",
        "镜头属性：",
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
    if group["组间设计"]["全局风格"].strip() not in prompt:
        raise ValueError(f"{shot_id} 未原文保留全局风格。")
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
    bridge_strategy_summary = {"single_shot": 0, "direct_match": 0, "ambiguous": 0}
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
            bridge, bridge_strategy, bridge_note = extract_bridge(group, shot, index)
            detail_level, budget_strategy = choose_detail_level(group, shot, bridge, prompt_spec)
            prompt = compose_prompt(group, shot, bridge, detail_level, prompt_spec)
            packet = build_request_packet(template, episode_id, source_rel, group, shot, prompt)
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
