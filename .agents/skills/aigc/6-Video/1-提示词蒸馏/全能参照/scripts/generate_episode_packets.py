#!/usr/bin/env python3
from __future__ import annotations

import argparse
import copy
import json
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
PROMPT_ASSEMBLY_SPEC = ROOT / ".agents/skills/aigc/6-Video/1-提示词蒸馏/全能参照/prompt-assembly-spec.md"
SOURCE_SCHEMA = ".agents/skills/aigc/_shared/director_episode_output.schema.json"
CHAR_LIMIT = 1900
FIXED_AUDIO_DIRECTIVE = "不生成字幕，不生成BGM，要生成物理互动音效与环境音。"


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
    text = text.replace(" ，", "，").replace(" 。", "。")
    return text


def strip_tail_punct(text: str) -> str:
    return re.sub(r"[。！？；;，,、\s]+$", "", text.strip())


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


def compact_clause(text: str) -> str:
    clean = strip_tail_punct(text)
    if not clean:
        return ""
    return re.split(r"[，；。]", clean, maxsplit=1)[0].strip()


def ensure_sentence(text: str) -> str:
    clean = normalize_space(text)
    if not clean:
        return ""
    if clean[-1] in "。！？!?；;":
        return clean
    return clean + "。"


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
    parts = [render_part(require_dict(part, "sentence_group.part"), source, level) for part in require_list(group_spec["parts"], "sentence_group.parts")]
    rendered = [strip_tail_punct(part) for part in parts if strip_tail_punct(part)]
    if not rendered and group_spec.get("fallback_parts"):
        fallback = [render_part(require_dict(part, "sentence_group.fallback_part"), source, level) for part in require_list(group_spec["fallback_parts"], "sentence_group.fallback_parts")]
        rendered = [strip_tail_punct(part) for part in fallback if strip_tail_punct(part)]
    if not rendered:
        return ""
    return ensure_sentence("，".join(rendered))


def validate_shot_ready(group_id: str, shot: dict[str, Any]) -> None:
    shot_id = require_non_empty_text(shot.get("分镜ID"), f"{group_id}.分镜明细[].分镜ID")
    timing = require_dict(shot.get("时间段"), f"{group_id}.{shot_id}.时间段")
    require_int(timing.get("开始秒"), f"{group_id}.{shot_id}.时间段.开始秒")
    require_int(timing.get("结束秒"), f"{group_id}.{shot_id}.时间段.结束秒")
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


def validate_source_ready(source_data: dict[str, Any]) -> list[dict[str, Any]]:
    metadata = require_dict(source_data.get("metadata"), "metadata")
    phase = metadata.get("document_phase")
    if phase != "ready":
        raise ValueError(
            f"metadata.document_phase 当前为 {phase!r}；"
            "只有 ready 状态的 3-Detail shared root 才能被 6-Video/全能参照消费。"
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
    return validated_groups


def build_time_range(shot: dict[str, Any]) -> str:
    timing = shot.get("时间段", {})
    return f"{timing.get('开始秒')}秒-{timing.get('结束秒')}秒"


def build_group_bridge(group: dict[str, Any], spec: dict[str, Any]) -> str:
    design = group.get("组间设计", {})
    bridge_spec = require_dict(spec["group_bridge"], "spec.group_bridge")
    parts = [
        render_part(require_dict(part, "group_bridge.part"), design, "group")
        for part in require_list(bridge_spec["parts"], "spec.group_bridge.parts")
    ]
    return combine_clauses(*parts, sep=bridge_spec.get("separator", "，"))


def build_camera_sentence(shot: dict[str, Any], level: str, spec: dict[str, Any]) -> str:
    shot_id = shot.get("分镜ID", "")
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
        level_spec = require_dict(require_dict(hook_spec["levels"], "optional_hook.levels").get(level, {}), f"optional_hook.levels.{level}")
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


def compose_prompt(group: dict[str, Any], shot_levels: list[str], spec: dict[str, Any]) -> str:
    sections = [
        f"分镜组{group['分镜组ID']}",
        group["剧本正文"].strip(),
        FIXED_AUDIO_DIRECTIVE,
        group["组间设计"]["全局风格"].strip(),
    ]
    bridge = build_group_bridge(group, spec)
    if bridge:
        sections.append(bridge)
    sections.append("\n\n".join(build_shot_text(shot, level, spec) for shot, level in zip(group["分镜明细"], shot_levels, strict=True)))
    return "\n\n".join(part for part in sections if part).strip()


def choose_levels(group: dict[str, Any], spec: dict[str, Any]) -> tuple[list[str], str]:
    shot_count = len(group["分镜明细"])
    budgeting = require_dict(spec["budgeting"], "spec.budgeting")
    underflow_margin = budgeting.get("underflow_margin_chars", 260)
    levels = ["full"] * shot_count
    prompt = compose_prompt(group, levels, spec)
    if len(prompt) <= CHAR_LIMIT:
        strategy = "underflow" if CHAR_LIMIT - len(prompt) >= underflow_margin else "normal"
        return levels, strategy

    levels = ["normal"] * shot_count
    prompt = compose_prompt(group, levels, spec)
    if len(prompt) <= CHAR_LIMIT:
        return levels, "normal"

    levels = ["normal"] * shot_count
    order = sorted(range(shot_count), key=lambda idx: len(build_shot_text(group["分镜明细"][idx], "normal", spec)), reverse=True)
    for idx in order:
        levels[idx] = "tight"
        if len(compose_prompt(group, levels, spec)) <= CHAR_LIMIT:
            return levels, "tight"

    for idx in order:
        levels[idx] = "ultra"
        if len(compose_prompt(group, levels, spec)) <= CHAR_LIMIT:
            return levels, "tight"

    levels = ["ultra"] * shot_count
    if len(compose_prompt(group, levels, spec)) <= CHAR_LIMIT:
        return levels, "tight"

    raise ValueError(f"分镜组 {group['分镜组ID']} 在 ultra 压缩后仍超过 {CHAR_LIMIT} 字。")


def build_request_packet(template: dict[str, Any], episode_id: str, source_rel: str, group: dict[str, Any], prompt: str) -> dict[str, Any]:
    packet = copy.deepcopy(template)
    packet["meta"]["episode_id"] = episode_id
    packet["meta"]["shot_level"] = "storyboard_group"
    packet["meta"]["group_id"] = group["分镜组ID"]
    packet["meta"]["source_shot_ids"] = [shot["分镜ID"] for shot in group["分镜明细"]]
    packet["meta"]["source_file"] = source_rel
    packet["meta"]["source_schema"] = SOURCE_SCHEMA
    packet["meta"]["template_version"] = "v1"
    packet["prompt_style"]["type"] = "multimodal2video"
    packet["prompt_style"]["language"] = "zh-CN"
    packet["prompt_style"]["char_limit"] = CHAR_LIMIT
    packet["model"]["model_version"] = "seedance2.0"
    packet["model"]["duration"] = str(group.get("总时长", 15))
    packet["model"]["ratio"] = "16:9"
    packet["model"]["video_resolution"] = "720p"
    packet["model"]["reference_images"] = []
    packet["model"]["image_markers"] = []
    packet["prompt"] = prompt
    packet["prompt_char_count"] = len(prompt)
    return packet


def build_txt_view(episode_id: str, packets: list[dict[str, Any]]) -> str:
    sections = [f"# {episode_id} 全能参照"]
    for packet in packets:
        group_id = packet["meta"]["group_id"]
        prompt = packet["prompt"]
        display_prompt = prompt.split("\n\n", 1)[1] if prompt.startswith(f"分镜组{group_id}\n\n") else prompt
        sections.append(
            "\n".join(
                [
                    f"## 分镜组 {group_id}",
                    "",
                    display_prompt,
                    "",
                    f"字数统计: {packet['prompt_char_count']}",
                    "",
                    "---",
                ]
            )
        )
    return "\n\n".join(sections).rstrip() + "\n"


def validate_packets(packets: list[dict[str, Any]], groups: list[dict[str, Any]]) -> None:
    forbidden_labels = [
        "时间段：",
        "镜头属性：",
        "景别：",
        "角色站位走位：",
        "角色背景面：",
        "角色表现：",
        "场景氛围：",
        "道具及状态：",
        "摄影美学：",
        "镜头框架：",
        "镜头类型：",
        "分镜表现：",
    ]
    bad_time_pattern = re.compile(r"分镜[\d-]+的\d+秒-\d+秒")

    for packet, group in zip(packets, groups, strict=True):
        prompt = packet["prompt"]
        if len(prompt) != packet["prompt_char_count"]:
            raise ValueError(f"{group['分镜组ID']} 的 prompt_char_count 与实际长度不一致。")
        if packet["prompt_char_count"] > CHAR_LIMIT:
            raise ValueError(f"{group['分镜组ID']} 超出 {CHAR_LIMIT} 字限制。")
        if FIXED_AUDIO_DIRECTIVE not in prompt:
            raise ValueError(f"{group['分镜组ID']} 缺少固定音频约束行。")
        if any(label in prompt for label in forbidden_labels):
            raise ValueError(f"{group['分镜组ID']} 泄露了字段标题。")
        if bad_time_pattern.search(prompt):
            raise ValueError(f"{group['分镜组ID']} 出现了“分镜ID 的 时间”写法。")
        for shot in group["分镜明细"]:
            anchor = f"分镜{shot['分镜ID']} {build_time_range(shot)}"
            if anchor not in prompt:
                raise ValueError(f"{group['分镜组ID']} 缺少时间锚点 {anchor}。")


def render_episode(project_name: str, episode_id: str) -> dict[str, Any]:
    project_root = resolve_project_root(project_name)
    source_path = project_root / "3-Detail" / f"{episode_id}.json"
    output_dir = project_root / "6-Video" / "全能参照" / episode_id
    output_dir.mkdir(parents=True, exist_ok=True)

    source_data = read_json(source_path)
    prompt_spec = load_prompt_assembly_spec()
    groups = validate_source_ready(require_dict(source_data, str(source_path)))
    template = read_json(TEMPLATE_JSON)
    generated_at = datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")
    source_rel = str(source_path.relative_to(ROOT))

    packets: list[dict[str, Any]] = []
    manifest_groups: list[dict[str, Any]] = []
    budget_strategy_summary = {"normal": 0, "tight": 0, "underflow": 0}

    for group in groups:
        shot_levels, budget_strategy = choose_levels(group, prompt_spec)
        prompt = compose_prompt(group, shot_levels, prompt_spec)
        packet = build_request_packet(template, episode_id, source_rel, group, prompt)
        packets.append(packet)
        budget_strategy_summary[budget_strategy] += 1
        manifest_groups.append(
            {
                "group_id": group["分镜组ID"],
                "source_shot_ids": packet["meta"]["source_shot_ids"],
                "budget_strategy": budget_strategy,
                "prompt_char_count": packet["prompt_char_count"],
                "within_target_limit": packet["prompt_char_count"] <= CHAR_LIMIT,
                "exception_note": "为控制 1900 字上限，已优先压缩 P3，并对部分 P2 做了收束。" if budget_strategy == "tight" else "",
            }
        )

    validate_packets(packets, groups)

    episode_payload = {
        "episode_id": episode_id,
        "project_name": project_name,
        "source_file": source_rel,
        "source_schema": SOURCE_SCHEMA,
        "tranche": "6-Video/全能参照",
        "request_type": "group_request_packets",
        "generated_at": generated_at,
        "group_count": len(groups),
        "request_packets": packets,
    }
    manifest_payload = {
        "episode_id": episode_id,
        "project_name": project_name,
        "source_file": source_rel,
        "generated_at": generated_at,
        "output_mode": "full_trace",
        "group_count": len(groups),
        "budget_strategy_summary": budget_strategy_summary,
        "groups": manifest_groups,
    }

    write_json(output_dir / f"{episode_id}.json", episode_payload)
    write_json(output_dir / "_manifest.json", manifest_payload)
    (output_dir / f"{episode_id}.txt").write_text(build_txt_view(episode_id, packets), encoding="utf-8")

    return {
        "group_count": len(groups),
        "max_prompt_chars": max(packet["prompt_char_count"] for packet in packets),
        "budget_strategy_summary": budget_strategy_summary,
        "output_dir": str(output_dir),
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="重建 6-Video/全能参照 的 episode 三件套。")
    parser.add_argument("--project", required=True, help="项目名，例如 晴深不渝")
    parser.add_argument("--episode", required=True, help="集名，例如 第1集")
    args = parser.parse_args()

    print(json.dumps(render_episode(args.project, args.episode), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
