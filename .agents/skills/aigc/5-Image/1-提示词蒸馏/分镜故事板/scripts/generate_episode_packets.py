#!/usr/bin/env python3
from __future__ import annotations

import argparse
import copy
import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


SCRIPT_DIR = Path(__file__).resolve().parent
SHARED_DIR = SCRIPT_DIR.parent.parent / "_shared"
if str(SHARED_DIR) not in sys.path:
    sys.path.insert(0, str(SHARED_DIR))

from prompt_bridge_helpers import (  # noqa: E402
    ROOT,
    SOURCE_SCHEMA,
    TEMPLATE_JSON,
    build_camera_clauses,
    build_canonical_group_design_block,
    build_prompt_prefix,
    build_shot_display_index,
    build_time_range,
    ensure_sentence,
    load_prompt_assembly_spec,
    normalize_shot_for_prompt,
    ordered_canonical_shots,
    read_json,
    render_sentence_group,
    require_dict,
    require_list,
    require_non_empty_text,
    resolve_project_root,
    strip_tail_punct,
    validate_canonical_source_ready,
    write_json,
)


PROMPT_ASSEMBLY_SPEC = SCRIPT_DIR.parent / "prompt-assembly-spec.md"
TARGET_MAX = 3800
ALLOWED_PHASES = {"detail_in_progress", "ready"}
LEGACY_SCRIPT_AUTHORSHIP_ERROR = (
    "legacy script authorship is deprecated: this runner may only project canonical LLM-authored prompt truth and must not replace it."
)


def build_shot_text(shot: dict[str, Any], shot_index: int, level: str, spec: dict[str, Any]) -> str:
    shot_spec = require_dict(spec["shot"], "spec.shot")
    normalized_shot = normalize_shot_for_prompt(shot)
    normalized_shot["shot_index"] = build_shot_display_index(shot_index)
    opening = shot_spec["opening_template"].format(
        shot_index=normalized_shot["shot_index"],
        time_range=build_time_range(normalized_shot),
        分镜ID=normalized_shot.get("分镜ID", ""),
    )
    body_parts: list[str] = []
    script_bridge = require_dict(shot_spec["script_bridge"], "spec.shot.script_bridge")
    script_text = strip_tail_punct(str(normalized_shot.get("剧本正文", "")).strip())
    if script_text:
        rendered_script = strip_tail_punct(script_bridge["templates"][level].format(value=script_text))
        if rendered_script:
            body_parts.append(rendered_script)
    body_parts.extend(build_camera_clauses(normalized_shot, level, spec))
    detail_sentences = require_dict(shot_spec["detail_sentences"], "spec.shot.detail_sentences")
    for sentence_group in require_list(detail_sentences[level], f"spec.shot.detail_sentences.{level}"):
        rendered = render_sentence_group(require_dict(sentence_group, "detail_sentence_group"), normalized_shot, level)
        clean = strip_tail_punct(rendered)
        if clean:
            body_parts.append(clean)
    for hook in require_list(shot_spec.get("optional_hooks", []), "spec.shot.optional_hooks"):
        hook_spec = require_dict(hook, "optional_hook")
        level_spec = require_dict(require_dict(hook_spec["levels"], "optional_hook.levels").get(level, {}), f"optional_hook.levels.{level}")
        template = level_spec.get("template", "")
        if not template:
            continue
        raw_value = normalized_shot.get(hook_spec["field"], "")
        if not isinstance(raw_value, str) or not raw_value.strip():
            continue
        body_parts.append(strip_tail_punct(template.format(value=strip_tail_punct(raw_value), **normalized_shot)))
    body = ensure_sentence("，".join(part for part in body_parts if part))
    return f"{opening}{body}" if body else opening


def compose_prompt(group: dict[str, Any], detail_level: str, spec: dict[str, Any]) -> str:
    shot_lines = []
    for index, shot in enumerate(ordered_canonical_shots(group)):
        shot_lines.append(build_shot_text(shot, index, detail_level, spec))
    sections = [
        build_prompt_prefix(spec),
        build_canonical_group_design_block(group, spec),
        "\n".join(shot_lines),
    ]
    return "\n".join(section for section in sections if section).strip()


def choose_detail_level(group: dict[str, Any], spec: dict[str, Any]) -> tuple[str, str]:
    for level, budget in (("full", "normal"), ("normal", "normal"), ("tight", "tight"), ("ultra", "tight")):
        prompt = compose_prompt(group, level, spec)
        if len(prompt) <= TARGET_MAX:
            return level, budget
    raise ValueError(f"分镜组 {group.get('分镜组ID')} 在 ultra 压缩后仍超过 {TARGET_MAX} 字。")


def build_request_packet(
    template: dict[str, Any],
    episode_id: str,
    source_rel: str,
    group: dict[str, Any],
    prompt: str,
) -> dict[str, Any]:
    packet = copy.deepcopy(template)
    packet["meta"]["episode_id"] = episode_id
    packet["meta"]["source_tranche"] = "分镜故事板"
    packet["meta"]["shot_level"] = "storyboard_group"
    packet["meta"]["group_id"] = group["分镜组ID"]
    packet["meta"]["source_shot_ids"] = [shot["分镜ID"] for shot in ordered_canonical_shots(group)]
    packet["meta"]["source_file"] = source_rel
    packet["meta"]["source_schema"] = SOURCE_SCHEMA
    packet["meta"]["template_version"] = "v2"
    packet["prompt_style"]["type"] = "storyboard_group"
    packet["prompt_style"]["language"] = "mixed"
    packet["prompt_style"]["char_limit"] = TARGET_MAX
    packet["model"]["provider"] = ""
    packet["model"]["model_version"] = ""
    packet["model"]["ratio"] = "16:9"
    packet["model"]["image_size"] = "1920x1080"
    packet["model"]["output_format"] = "png"
    packet["model"]["num_images"] = max(1, len(packet["meta"]["source_shot_ids"]))
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


def validate_sheet_packet(packet: dict[str, Any], group: dict[str, Any], prefix: str) -> None:
    prompt = require_non_empty_text(packet.get("prompt"), "packet.prompt")
    group_id = group["分镜组ID"]
    if packet["prompt_char_count"] != len(prompt):
        raise ValueError(f"{group_id} 的 prompt_char_count 与实际长度不一致。")
    if not prompt.startswith(prefix):
        raise ValueError(f"{group_id} 未保留固定英文前缀。")
    forbidden_labels = [
        "剧本正文：",
        "正文切分参考：",
        "正文回指：",
        "类型元素：",
        "导演意图：",
        "出场角色及穿搭：",
        "时间段：",
        "角色表现：",
        "运动表现：",
        "氛围表现：",
        "视觉强化：",
        "分镜构图：",
        "摄影美学：",
        "运镜手法：",
        "镜头速度：",
        "镜头视角：",
        "道具及状态：",
        "镜头类型兼容：",
    ]
    if any(label in prompt for label in forbidden_labels):
        raise ValueError(f"{group_id} 泄露了字段标题。")
    group_style_source = group.get("global") if isinstance(group.get("global"), dict) else group.get("组间设计")
    style_anchor = strip_tail_punct(str(require_dict(group_style_source, f"{group_id}.style_source").get("全局风格", "")).strip())
    if style_anchor and style_anchor not in prompt:
        raise ValueError(f"{group_id} 未保留组级设计块中的全局风格。")
    if packet["meta"]["group_id"] != group_id:
        raise ValueError(f"{group_id} 的 group_id 回链错误。")
    ordered_shots = ordered_canonical_shots(group)
    expected_ids = [shot["分镜ID"] for shot in ordered_shots]
    if packet["meta"]["source_shot_ids"] != expected_ids:
        raise ValueError(f"{group_id} 的 source_shot_ids 与组内分镜顺序不一致。")
    for index, shot_id in enumerate(expected_ids):
        expected_anchor = f"{build_time_range(ordered_shots[index])}｜分镜{build_shot_display_index(index)}："
        if expected_anchor not in prompt:
            raise ValueError(f"{group_id} 缺少镜级锚点 {expected_anchor}。")
        if f"分镜{shot_id}：" in prompt or f"分镜 {shot_id} " in prompt:
            raise ValueError(f"{group_id} 泄露了完整四段式分镜ID `{shot_id}`。")


def render_episode(project_name: str, episode_id: str, group_id: str | None = None, output_mode: str = "json_only") -> dict[str, Any]:
    project_root = resolve_project_root(project_name)
    source_path = project_root / "3-Detail" / f"{episode_id}.json"
    output_dir = project_root / "5-Image" / "分镜故事板" / episode_id
    output_dir.mkdir(parents=True, exist_ok=True)

    source_data = require_dict(read_json(source_path), str(source_path))
    prompt_spec = load_prompt_assembly_spec(PROMPT_ASSEMBLY_SPEC)
    prefix = build_prompt_prefix(prompt_spec)
    detected_episode_id, groups = validate_canonical_source_ready(source_data, ALLOWED_PHASES)
    if detected_episode_id != episode_id:
        raise ValueError(f"文件内 episode_id={detected_episode_id}，但执行参数为 {episode_id}。")
    template = read_json(TEMPLATE_JSON)
    generated_at = datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")
    source_rel = str(source_path.relative_to(ROOT))

    request_packets: list[dict[str, Any]] = []
    manifest_groups: list[dict[str, Any]] = []
    budget_strategy_summary = {"normal": 0, "tight": 0}
    target_group_found = group_id is None

    for group in groups:
        current_group_id = group["分镜组ID"]
        if group_id and current_group_id != group_id:
            continue
        target_group_found = True
        detail_level, budget_strategy = choose_detail_level(group, prompt_spec)
        prompt = compose_prompt(group, detail_level, prompt_spec)
        packet = build_request_packet(template, episode_id, source_rel, group, prompt)
        validate_sheet_packet(packet, group, prefix)
        request_packets.append(packet)
        budget_strategy_summary[budget_strategy] += 1
        manifest_groups.append(
            {
                "group_id": current_group_id,
                "source_shot_ids": packet["meta"]["source_shot_ids"],
                "prompt_char_count": packet["prompt_char_count"],
                "has_reference_slots": True,
                "exception_note": "" if budget_strategy == "normal" else "为命中故事板字数窗，已压缩部分镜级细节表达。",
            }
        )

    if not target_group_found:
        raise ValueError(f"在 {episode_id} 中未找到目标分镜组 {group_id}。")
    if not request_packets:
        raise ValueError(f"{episode_id} 没有生成任何分镜故事板请求。")

    output_payload = {
        "episode_id": episode_id,
        "project_name": project_name,
        "source_file": source_rel,
        "source_schema": SOURCE_SCHEMA,
        "tranche": "5-Image/分镜故事板",
        "request_type": "storyboard_group_request_packets",
        "output_mode": output_mode,
        "generated_at": generated_at,
        "group_count": len(request_packets),
        "request_packets": request_packets,
    }
    write_json(output_dir / f"{episode_id}.json", output_payload)

    if output_mode == "full_trace":
        manifest_payload = {
            "episode_id": episode_id,
            "project_name": project_name,
            "source_file": source_rel,
            "generated_at": generated_at,
            "output_mode": output_mode,
            "json_file": str((output_dir / f"{episode_id}.json").relative_to(ROOT)),
            "group_count": len(request_packets),
            "budget_strategy_summary": budget_strategy_summary,
            "groups": manifest_groups,
        }
        write_json(output_dir / "_manifest.json", manifest_payload)

    return {
        "episode_id": episode_id,
        "group_count": len(request_packets),
        "budget_strategy_summary": budget_strategy_summary,
        "max_prompt_chars": max(packet["prompt_char_count"] for packet in request_packets),
        "min_prompt_chars": min(packet["prompt_char_count"] for packet in request_packets),
        "output_dir": str(output_dir),
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="重建 5-Image/分镜故事板 的 episode 请求 JSON。")
    parser.add_argument("--project", required=True, help="项目名，例如 晴深不渝")
    parser.add_argument("--episode", required=True, help="集名，例如 第1集")
    parser.add_argument("--group-id", help="可选，只生成单个分镜组ID")
    parser.add_argument("--output-mode", choices=["json_only", "full_trace"], default="json_only")
    parser.add_argument(
        "--allow-legacy-script-authorship",
        action="store_true",
        help="兼容保留参数；当前 runner 已默认按 canonical detail 直读生成，不再需要该开关。",
    )
    args = parser.parse_args()
    if args.allow_legacy_script_authorship:
        print(LEGACY_SCRIPT_AUTHORSHIP_ERROR, file=sys.stderr)
    print(json.dumps(render_episode(args.project, args.episode, args.group_id, args.output_mode), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
