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
TEMPLATE_JSON = ROOT / ".agents/skills/aigc/6-Video/_shared/video-generation-input.template.json"
SOURCE_SCHEMA = ".agents/skills/aigc/_shared/director_episode_output.schema.json"
CHAR_LIMIT = 1900


def read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, payload: Any) -> None:
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def normalize_space(text: str) -> str:
    text = re.sub(r"\s+", " ", text.strip())
    text = text.replace(" ，", "，").replace(" 。", "。")
    return text


def strip_tail_punct(text: str) -> str:
    return re.sub(r"[。！？；;，,、\s]+$", "", text.strip())


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


def build_time_range(shot: dict[str, Any]) -> str:
    timing = shot.get("时间段", {})
    return f"{timing.get('开始秒')}秒-{timing.get('结束秒')}秒"


def build_group_bridge(group: dict[str, Any]) -> str:
    design = group.get("组间设计", {})
    parts = [
        design.get("类型元素", ""),
        design.get("导演意图", ""),
        f"本组出场角色及穿搭为{strip_tail_punct(design.get('出场角色及穿搭', ''))}" if design.get("出场角色及穿搭") else "",
    ]
    return combine_clauses(*parts)


def build_camera_sentence(shot: dict[str, Any], level: str) -> str:
    shot_id = shot.get("分镜ID", "")
    opening = f"分镜{shot_id} {build_time_range(shot)}"
    clauses = [opening]

    if shot.get("镜头属性"):
        clauses.append(shot["镜头属性"])
    if shot.get("景别"):
        clauses.append(f"以{shot['景别']}切入" if level in {"full", "normal"} else shot["景别"])
    if shot.get("运镜手法"):
        movement = strip_tail_punct(shot["运镜手法"]) if level in {"full", "normal"} else compact_clause(shot["运镜手法"])
        clauses.append(f"镜头{movement}" if level in {"full", "normal"} else movement)
    if shot.get("镜头速度"):
        speed = strip_tail_punct(shot["镜头速度"]) if level in {"full", "normal"} else compact_clause(shot["镜头速度"])
        clauses.append(f"整体速度{speed}" if level in {"full", "normal"} else speed)
    if shot.get("镜头视角"):
        angle_text = strip_tail_punct(shot["镜头视角"])
        if level in {"full", "normal"}:
            clauses.append(f"视角保持{angle_text}")
        else:
            clauses.append(angle_text)

    return combine_clauses(*clauses)


def build_other_sentence(shot: dict[str, Any], level: str) -> str:
    frame = shot.get("镜头框架")
    shot_type = shot.get("镜头类型")
    storyboard_effect = shot.get("分镜表现")

    if level == "full":
        return combine_clauses(
            f"构图上{strip_tail_punct(frame)}" if frame else "",
            f"整体按{strip_tail_punct(shot_type)}处理" if shot_type else "",
            f"重点落在{strip_tail_punct(storyboard_effect)}" if storyboard_effect else "",
        )
    if level == "normal":
        return combine_clauses(
            f"构图上{strip_tail_punct(frame)}" if frame else "",
            strip_tail_punct(storyboard_effect) if storyboard_effect else (strip_tail_punct(shot_type) if shot_type else ""),
        )
    if level == "tight":
        return combine_clauses(
            compact_clause(storyboard_effect) if storyboard_effect else "",
            compact_clause(shot_type) if shot_type else "",
        )
    return combine_clauses(compact_clause(storyboard_effect) if storyboard_effect else "")


def build_shot_text(shot: dict[str, Any], level: str) -> str:
    sentences: list[str] = [build_camera_sentence(shot, level)]

    if level == "full":
        for key in ("角色站位走位", "角色背景面", "角色表现", "场景氛围", "道具及状态", "摄影美学"):
            if shot.get(key):
                sentences.append(ensure_sentence(shot[key]))
        other = build_other_sentence(shot, level)
        if other:
            sentences.append(other)
    elif level == "normal":
        for sentence in (
            combine_clauses(shot.get("角色站位走位", ""), shot.get("角色背景面", "")),
            combine_clauses(shot.get("角色表现", ""), shot.get("场景氛围", "")),
            combine_clauses(shot.get("道具及状态", ""), shot.get("摄影美学", ""), build_other_sentence(shot, level)),
        ):
            if sentence:
                sentences.append(sentence)
    elif level == "tight":
        for sentence in (
            combine_clauses(compact_clause(shot.get("角色站位走位", "")), compact_clause(shot.get("角色背景面", ""))),
            combine_clauses(
                compact_clause(shot.get("角色表现", "")),
                compact_clause(shot.get("场景氛围", "")),
                compact_clause(shot.get("道具及状态", "")),
                compact_clause(shot.get("摄影美学", "")),
                build_other_sentence(shot, level),
            ),
        ):
            if sentence:
                sentences.append(sentence)
    else:
        summary = combine_clauses(
            compact_clause(shot.get("角色站位走位", "")),
            compact_clause(shot.get("角色背景面", "")),
            compact_clause(shot.get("角色表现", "")),
            compact_clause(shot.get("场景氛围", "")),
            compact_clause(shot.get("道具及状态", "")),
            build_other_sentence(shot, level),
        )
        if summary:
            sentences.append(summary)

    return " ".join(sentence for sentence in sentences if sentence)


def compose_prompt(group: dict[str, Any], shot_levels: list[str]) -> str:
    sections = [
        f"分镜组{group['分镜组ID']}",
        group["剧本正文"].strip(),
        group["组间设计"]["全局风格"].strip(),
    ]
    bridge = build_group_bridge(group)
    if bridge:
        sections.append(bridge)
    sections.append("\n\n".join(build_shot_text(shot, level) for shot, level in zip(group["分镜明细"], shot_levels, strict=True)))
    return "\n\n".join(part for part in sections if part).strip()


def choose_levels(group: dict[str, Any]) -> tuple[list[str], str]:
    shot_count = len(group["分镜明细"])
    levels = ["full"] * shot_count
    prompt = compose_prompt(group, levels)
    if len(prompt) <= CHAR_LIMIT:
        strategy = "underflow" if CHAR_LIMIT - len(prompt) >= 260 else "normal"
        return levels, strategy

    levels = ["normal"] * shot_count
    prompt = compose_prompt(group, levels)
    if len(prompt) <= CHAR_LIMIT:
        return levels, "normal"

    levels = ["normal"] * shot_count
    order = sorted(range(shot_count), key=lambda idx: len(build_shot_text(group["分镜明细"][idx], "normal")), reverse=True)
    for idx in order:
        levels[idx] = "tight"
        if len(compose_prompt(group, levels)) <= CHAR_LIMIT:
            return levels, "tight"

    for idx in order:
        levels[idx] = "ultra"
        if len(compose_prompt(group, levels)) <= CHAR_LIMIT:
            return levels, "tight"

    levels = ["ultra"] * shot_count
    if len(compose_prompt(group, levels)) <= CHAR_LIMIT:
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
        if any(label in prompt for label in forbidden_labels):
            raise ValueError(f"{group['分镜组ID']} 泄露了字段标题。")
        if bad_time_pattern.search(prompt):
            raise ValueError(f"{group['分镜组ID']} 出现了“分镜ID 的 时间”写法。")
        for shot in group["分镜明细"]:
            anchor = f"分镜{shot['分镜ID']} {build_time_range(shot)}"
            if anchor not in prompt:
                raise ValueError(f"{group['分镜组ID']} 缺少时间锚点 {anchor}。")


def render_episode(project_name: str, episode_id: str) -> dict[str, Any]:
    source_path = ROOT / "projects" / project_name / "3-Detail" / f"{episode_id}.json"
    output_dir = ROOT / "projects" / project_name / "6-Video" / "全能参照" / episode_id
    output_dir.mkdir(parents=True, exist_ok=True)

    source_data = read_json(source_path)
    groups = source_data["final_output"]["main_content"]["分镜组列表"]
    template = read_json(TEMPLATE_JSON)
    generated_at = datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")
    source_rel = str(source_path.relative_to(ROOT))

    packets: list[dict[str, Any]] = []
    manifest_groups: list[dict[str, Any]] = []
    budget_strategy_summary = {"normal": 0, "tight": 0, "underflow": 0}

    for group in groups:
        shot_levels, budget_strategy = choose_levels(group)
        prompt = compose_prompt(group, shot_levels)
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
