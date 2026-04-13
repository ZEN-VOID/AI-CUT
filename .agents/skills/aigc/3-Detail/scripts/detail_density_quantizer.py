#!/usr/bin/env python3
"""Structured density budget quantizer for `aigc/3-Detail`.

This script turns grouped-script evidence into stage-local shot-budget guidance.
It does not read prose shot drafts. It only reads `1-Planning/3-分组/第N集.md`.

The quantizer is intentionally source-first:
- candidate beats are segmented from action / dialogue / focus / turn signals
- no scene-mode window clamps are applied
- no extra format coefficient is applied
- the output is a flexible budget:
  `preferred_shot_count + [shot_budget_floor, shot_budget_ceiling]`
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from collections import Counter
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

PACE_COEFFICIENT = {
    "超快节奏": 1.4,
    "快节奏": 1.2,
    "正常节奏": 1.0,
    "中节奏": 1.0,
    "慢节奏": 0.8,
    "超慢节奏": 0.6,
}

GROUP_HEADER_RE = re.compile(r"^##\s*【(?P<group_id>\d+-\d+-\d+)】(?:\s+(?P<title>.+))?$")
SCENE_HEADER_RE = re.compile(r"^###\s*场景(?P<label>[^：:]+)\s*[：:]\s*(?P<title>.+?)\s*$")
ACTION_RE = re.compile(r"^动作画面\s*[：:]\s*(?P<text>.+)$")
VOICE_RE = re.compile(r"^(对白|独白|内心独白|旁白)(?:（(?P<speaker>.+?)）|\((?P<speaker_alt>.+?)\))?\s*[：:]\s*(?P<text>.+)$")
VOICE_VISUAL_RE = re.compile(r"^(对白画面|独白画面|内心独白画面|旁白画面)\s*[：:]\s*(?P<text>.+)$")
TAIL_HOOK_COMMENT_RE = re.compile(
    r"^<!--\s*tail-hook:\s*from=(?P<group_id>\d+-\d+-\d+)(?:\s*;\s*quantize=(?P<quantize>[a-z-]+))?\s*-->$"
)

TURN_KEYWORDS = (
    "突然",
    "忽然",
    "猛地",
    "骤然",
    "终于",
    "一下子",
    "话音一落",
    "话音落下",
    "下一秒",
    "转身",
    "扑进",
    "吻了上去",
    "剧烈",
    "彻底",
    "随即",
    "却",
    "但",
    "然而",
)

CROWD_KEYWORDS = (
    "宾客",
    "众人",
    "人群",
    "所有人",
    "全场",
    "掌声",
    "笑声",
    "围观",
    "祝贺",
)

CROWD_SUBJECT_RE = re.compile(r"(宾客|旁人|众人|人群|全场|围观|太太|老人|广场舞大妈)")

BURST_KEYWORDS = (
    "突然",
    "猛地",
    "剧烈",
    "扯落",
    "扑进",
    "吻",
    "宣 布",
    "宣布",
    "落下",
    "加冕",
    "锁",
    "断开",
)

ACTION_SUBJECT_PATTERNS = (
    re.compile(
        r"^(?:主位上的|门口的|吧台边|人群里的|人群中|一位|另一位|几位|周围几位)?"
        r"(?P<subject>[一-龥]{2,6})"
        r"(?:[，,、 ]|穿着|站在|看着|走出|走向|转进|转身|坐进|低头|抬头|伸手|举杯|笑|"
        r"望着|摸到|推门|赤脚|背靠着|护住|扶住|抱住|吻|递给|拿着|追下车|安顿在|盯着|"
        r"回到|回了|把|将)"
    ),
    re.compile(r"^(?P<subject>[一-龥]{2,6})的话音"),
)

GENERIC_SCENE_SUBJECTS = {
    "晨光",
    "阳光",
    "空气",
    "雨水",
    "雨点",
    "灯光",
    "弦乐",
    "掌声",
    "笑声",
    "高跟鞋",
    "卷帘",
    "背景",
    "现场",
    "广场",
    "宴会厅",
    "酒吧",
    "阁楼",
}


class DensityQuantizationError(RuntimeError):
    """Raised when density quantization input is malformed."""


@dataclass
class GroupSection:
    group_id: str
    title: str
    body: str


@dataclass
class Unit:
    kind: str
    text: str
    speaker: str | None = None
    subject: str | None = None
    turn_signal: bool = False


@dataclass
class Segment:
    units: list[Unit] = field(default_factory=list)
    has_action: bool = False
    has_dialogue: bool = False
    turn_signal: bool = False
    focus_owner: str = "场景"


def normalize_subject(subject: str | None) -> str:
    if not subject:
        return "场景"
    token = subject.strip()
    if not token:
        return "场景"
    if CROWD_SUBJECT_RE.search(token):
        return "群体"
    return token


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="计算 `3-Detail` 的结构化分镜密度预算。")
    parser.add_argument("--grouped-script", required=True, help="输入 grouped script 路径（第N集.md）")
    parser.add_argument("--group-id", help="仅输出单个分镜组的量化结果")
    parser.add_argument("--json", action="store_true", help="以 JSON 输出")
    return parser.parse_args()


def parse_frontmatter(text: str) -> tuple[dict[str, str], str]:
    if not text.startswith("---\n"):
        raise DensityQuantizationError("grouped script 必须以 frontmatter 开头。")
    try:
        _, rest = text.split("---\n", 1)
        block, body = rest.split("\n---\n", 1)
    except ValueError as exc:
        raise DensityQuantizationError("frontmatter 结束分隔符缺失。") from exc

    data: dict[str, str] = {}
    for raw_line in block.splitlines():
        line = raw_line.strip()
        if not line or ":" not in line:
            continue
        key, value = line.split(":", 1)
        data[key.strip()] = value.strip()
    return data, body

def parse_group_sections(body: str) -> list[GroupSection]:
    groups: list[tuple[str, str, int]] = []
    lines = body.splitlines()
    for index, raw_line in enumerate(lines):
        match = GROUP_HEADER_RE.match(raw_line.strip())
        if match:
            groups.append((match.group("group_id"), (match.group("title") or "").strip(), index))
    if not groups:
        raise DensityQuantizationError("未发现任何分镜组标题。")

    result: list[GroupSection] = []
    for idx, (group_id, title, start) in enumerate(groups):
        end = groups[idx + 1][2] if idx + 1 < len(groups) else len(lines)
        section_body = "\n".join(lines[start + 1 : end]).strip()
        result.append(GroupSection(group_id=group_id, title=title, body=section_body))
    return result


def split_tail_hook_block(text: str) -> tuple[str, str]:
    lines = text.splitlines()
    for index, raw_line in enumerate(lines):
        if TAIL_HOOK_COMMENT_RE.match(raw_line.strip()):
            canonical = "\n".join(lines[:index]).rstrip()
            hook = "\n".join(lines[index + 1 :]).strip()
            return canonical, hook
    return text.rstrip(), ""


def infer_subject(text: str, speaker: str | None = None) -> str:
    if speaker:
        return normalize_subject(speaker)
    if CROWD_SUBJECT_RE.search(text):
        return "群体"
    for pattern in ACTION_SUBJECT_PATTERNS:
        match = pattern.match(text)
        if not match:
            continue
        subject = normalize_subject(match.group("subject"))
        if subject not in GENERIC_SCENE_SUBJECTS:
            return subject
    return "场景"


def has_turn_signal(text: str) -> bool:
    return any(keyword in text for keyword in TURN_KEYWORDS)


def parse_units(text: str) -> list[Unit]:
    units: list[Unit] = []
    for raw_line in text.splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or line.startswith("<!--"):
            continue
        if SCENE_HEADER_RE.match(line):
            continue
        action_match = ACTION_RE.match(line)
        if action_match:
            action_text = action_match.group("text").strip()
            units.append(
                Unit(
                    kind="action",
                    text=action_text,
                    subject=infer_subject(action_text),
                    turn_signal=has_turn_signal(action_text),
                )
            )
            continue
        voice_match = VOICE_RE.match(line)
        if voice_match:
            speaker = (voice_match.group("speaker") or voice_match.group("speaker_alt") or "").strip() or None
            voice_text = voice_match.group("text").strip()
            units.append(
                Unit(
                    kind="dialogue",
                    text=voice_text,
                    speaker=speaker,
                    subject=infer_subject(voice_text, speaker=speaker),
                    turn_signal=has_turn_signal(voice_text),
                )
            )
            continue
        visual_match = VOICE_VISUAL_RE.match(line)
        if visual_match:
            visual_text = visual_match.group("text").strip()
            units.append(
                Unit(
                    kind="support",
                    text=visual_text,
                    subject=infer_subject(visual_text),
                    turn_signal=has_turn_signal(visual_text),
                )
            )
            continue
    return units


def should_start_new_segment(previous: Segment, unit: Unit) -> bool:
    if unit.kind == "support":
        return False

    if unit.turn_signal:
        return True
    current_focus = normalize_subject(unit.subject)
    previous_focus = normalize_subject(previous.focus_owner)
    if previous.turn_signal:
        return True
    if current_focus == previous_focus:
        return False
    if current_focus == "群体" and previous_focus == "群体":
        return False
    if unit.kind == "dialogue" and previous.has_dialogue and current_focus != previous_focus:
        return True
    if unit.kind == "action" and previous.has_action and current_focus not in {previous_focus, "场景"}:
        return True
    return False


def build_segments(units: list[Unit]) -> list[Segment]:
    segments: list[Segment] = []
    for unit in units:
        if not segments:
            segment = Segment(
                units=[unit],
                has_action=unit.kind in {"action", "support"},
                has_dialogue=unit.kind == "dialogue",
                turn_signal=unit.turn_signal,
                focus_owner=normalize_subject(unit.subject),
            )
            segments.append(segment)
            continue
        current = segments[-1]
        if should_start_new_segment(current, unit):
            segments.append(
                Segment(
                    units=[unit],
                    has_action=unit.kind in {"action", "support"},
                    has_dialogue=unit.kind == "dialogue",
                    turn_signal=unit.turn_signal,
                    focus_owner=normalize_subject(unit.subject),
                )
            )
            continue
        current.units.append(unit)
        current.has_action = current.has_action or unit.kind in {"action", "support"}
        current.has_dialogue = current.has_dialogue or unit.kind == "dialogue"
        current.turn_signal = current.turn_signal or unit.turn_signal
        if unit.kind != "support":
            current.focus_owner = normalize_subject(unit.subject)
    return segments


def has_crowd_pressure(section_body: str, focus_shift_points: int) -> bool:
    return any(token in section_body for token in CROWD_KEYWORDS) and focus_shift_points >= 2


def has_burst_pivot(section_body: str, structural_turn_points: int) -> bool:
    return any(token in section_body for token in BURST_KEYWORDS) and structural_turn_points >= 2


def has_dialogue_relay(dialogue_line_count: int, focus_shift_points: int, canonical_beat_count: int) -> bool:
    return dialogue_line_count >= 3 and focus_shift_points >= 1 and canonical_beat_count <= 3


def build_group_metrics(section: GroupSection, pace_tier: str) -> dict[str, Any]:
    canonical_body, hook_body = split_tail_hook_block(section.body)
    canonical_units = parse_units(canonical_body)
    hook_units = parse_units(hook_body)
    segments = build_segments(canonical_units)
    hook_segments = build_segments(hook_units)

    canonical_beat_count = max(1, len(segments))
    action_phase_points = sum(1 for seg in segments if seg.has_action)
    dialogue_breath_points = sum(1 for seg in segments if seg.has_dialogue)
    dialogue_line_count = sum(1 for unit in canonical_units if unit.kind == "dialogue")
    focus_shift_points = sum(
        1
        for idx in range(1, len(segments))
        if segments[idx - 1].focus_owner != segments[idx].focus_owner
    )
    structural_turn_points = sum(1 for seg in segments if seg.turn_signal)
    hook_preview_count = len(hook_segments)

    pace_coef = PACE_COEFFICIENT[pace_tier]
    recommended_shot_baseline = max(1, round(canonical_beat_count * pace_coef))
    dialogue_relay = has_dialogue_relay(
        dialogue_line_count=dialogue_line_count,
        focus_shift_points=focus_shift_points,
        canonical_beat_count=canonical_beat_count,
    )
    single_beat_release = canonical_beat_count == 1 and hook_preview_count >= 1 and structural_turn_points >= 1

    expansion_headroom = 0
    expansion_reasons: list[str] = []
    if hook_preview_count and (structural_turn_points >= 1 or dialogue_relay):
        expansion_headroom += 1
        expansion_reasons.append("存在 hook preview，可在需要余波/预感时上探一镜")
    if single_beat_release:
        expansion_headroom += 1
        expansion_reasons.append("单拍收束组带余波释放，需要给结果着陆留空间")
    if dialogue_relay:
        expansion_headroom += 1
        expansion_reasons.append("对白接力与显性揭心思并存，可保留额外反应/承接镜空间")
    if has_crowd_pressure(canonical_body, focus_shift_points):
        expansion_headroom += 1
        expansion_reasons.append("存在群体压力或多对象接力反应，可保留额外反应镜空间")
    if expansion_headroom < 2 and has_burst_pivot(canonical_body, structural_turn_points):
        expansion_headroom += 1
        expansion_reasons.append("存在强转折/爆点，可保留单独着陆镜空间")
    expansion_headroom = min(expansion_headroom, 2)

    compression_headroom = 0
    compression_reasons: list[str] = []
    focus_counter = Counter(seg.focus_owner for seg in segments)
    dominant_focus, dominant_focus_count = focus_counter.most_common(1)[0]
    if canonical_beat_count >= 3 and dominant_focus_count >= max(2, canonical_beat_count - 1):
        compression_headroom += 1
        compression_reasons.append(f"主焦点长期稳定在 `{dominant_focus}`，可压并")
    if structural_turn_points == 0 and focus_shift_points <= 1 and not dialogue_relay:
        compression_headroom += 1
        compression_reasons.append("转折与焦点切换有限，连续动作/对话链可压并")
    compression_headroom = min(compression_headroom, 2)

    preferred_delta = 0
    preferred_reasons: list[str] = []
    if has_burst_pivot(canonical_body, structural_turn_points):
        preferred_delta += 1
        preferred_reasons.append("强转折需要保留明确落点")
    elif single_beat_release:
        preferred_delta += 1
        preferred_reasons.append("单拍收束后还承接余波时，宜留出结果镜")
    elif dialogue_relay:
        preferred_delta += 1
        preferred_reasons.append("对白接力里存在独立揭示/反应链，宜略高于基准")
    elif has_crowd_pressure(canonical_body, focus_shift_points):
        preferred_delta += 1
        preferred_reasons.append("群体接力反应更适合略高于基准的镜数")

    if canonical_beat_count >= 3 and dominant_focus_count >= max(2, canonical_beat_count - 1):
        preferred_delta -= 1
        preferred_reasons.append("主焦点长期稳定，可优先压回更紧凑的镜数")
    elif structural_turn_points == 0 and focus_shift_points <= 1 and not dialogue_relay:
        preferred_delta -= 1
        preferred_reasons.append("结构转折有限，可优先合镜")

    shot_budget_floor = max(1, recommended_shot_baseline - compression_headroom)
    shot_budget_ceiling = max(shot_budget_floor, recommended_shot_baseline + expansion_headroom)
    preferred_shot_count = max(
        shot_budget_floor,
        min(shot_budget_ceiling, recommended_shot_baseline + preferred_delta),
    )

    why_not_fewer = (
        f"当前组候选节拍约为 {canonical_beat_count}，预算下限为 {shot_budget_floor}；"
        "若再压低，容易吞掉当前组的关键任务切换或情绪着陆点。"
    )
    why_not_more = (
        f"当前组预算上限为 {shot_budget_ceiling}；若继续加镜，"
        "高概率会把同一信息链切碎，或让下游维度被迫用模板补镜。"
    )

    return {
        "group_id": section.group_id,
        "group_title": section.title,
        "canonical_beat_count": canonical_beat_count,
        "hook_preview_count": hook_preview_count,
        "action_phase_points": action_phase_points,
        "dialogue_breath_points": dialogue_breath_points,
        "focus_shift_points": focus_shift_points,
        "structural_turn_points": structural_turn_points,
        "pace_tier": pace_tier,
        "recommended_shot_baseline": recommended_shot_baseline,
        "expansion_headroom": expansion_headroom,
        "expansion_reasons": expansion_reasons,
        "compression_headroom": compression_headroom,
        "compression_reasons": compression_reasons,
        "preferred_shot_count": preferred_shot_count,
        "preferred_reasons": preferred_reasons,
        "shot_budget_floor": shot_budget_floor,
        "shot_budget_ceiling": shot_budget_ceiling,
        # legacy alias kept for downstream compatibility; validator now reads the budget range.
        "shot_count_decision": preferred_shot_count,
        "why_not_fewer": why_not_fewer,
        "why_not_more": why_not_more,
    }


def build_quantization_result(grouped_script_path: Path) -> dict[str, Any]:
    text = grouped_script_path.read_text(encoding="utf-8")
    frontmatter, body = parse_frontmatter(text)
    pace_tier = frontmatter.get("pace_tier")
    if not pace_tier:
        raise DensityQuantizationError("frontmatter 缺少 `pace_tier`。")
    if pace_tier not in PACE_COEFFICIENT:
        raise DensityQuantizationError(f"未知 pace_tier: {pace_tier}")

    sections = parse_group_sections(body)
    groups = [build_group_metrics(section, pace_tier=pace_tier) for section in sections]
    shot_distribution = Counter(group["preferred_shot_count"] for group in groups)

    return {
        "episode_label": frontmatter.get("集数", grouped_script_path.stem),
        "pace_tier": pace_tier,
        "group_count": len(groups),
        "shot_distribution": dict(sorted(shot_distribution.items())),
        "groups": groups,
    }


def main() -> int:
    args = parse_args()
    try:
        payload = build_quantization_result(Path(args.grouped_script))
    except Exception as exc:  # noqa: BLE001
        print(str(exc), file=sys.stderr)
        return 1

    groups = payload["groups"]
    if args.group_id:
        groups = [group for group in groups if group["group_id"] == args.group_id]
        if not groups:
            print(f"未找到分镜组: {args.group_id}", file=sys.stderr)
            return 1
        payload = {**payload, "groups": groups, "group_count": len(groups)}

    if args.json:
        print(json.dumps(payload, ensure_ascii=False, indent=2))
        return 0

    print(f"episode: {payload['episode_label']}")
    print(f"pace_tier: {payload['pace_tier']}")
    print(f"group_count: {payload['group_count']}")
    print(f"shot_distribution: {payload['shot_distribution']}")
    for group in payload["groups"]:
        print(
            f"{group['group_id']}: beats={group['canonical_beat_count']} "
            f"baseline={group['recommended_shot_baseline']} "
            f"preferred={group['preferred_shot_count']} "
            f"range={group['shot_budget_floor']}-{group['shot_budget_ceiling']}"
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
