#!/usr/bin/env python3
"""Authoritative density quantizer for `aigc/3-Detail`.

This script turns grouped-script evidence into stage-local shot-count truth.
It does not read prose shot drafts. It only reads `1-Planning/3-分组/第N集.md`.

The quantizer is intentionally source-first:
- candidate beats are segmented from action / dialogue / focus / turn signals
- no scene-mode window clamps are applied
- no extra format coefficient is applied
- final shot count is decided by:
  `round(candidate_beats * pace_coefficient) + split_bonus - merge_discount`
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

SUBJECT_HINTS = (
    "苏晴",
    "林深",
    "苏国雄",
    "贺廷",
    "司机",
    "宾客",
    "太太",
    "旁人",
    "人群",
    "全场",
    "项链",
    "酒吧",
    "阁楼",
)


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


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="计算 `3-Detail` authoritative 分镜密度。")
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
        return speaker
    for token in SUBJECT_HINTS:
        if token in text:
            return token
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
    prev_unit = previous.units[-1]
    if unit.kind == "support":
        return False
    if prev_unit.kind == "support":
        prev_kind = "action" if previous.has_action and not previous.has_dialogue else "dialogue"
    else:
        prev_kind = prev_unit.kind

    if unit.turn_signal:
        return True
    if unit.kind != prev_kind:
        return True
    if unit.kind == "dialogue" and unit.subject != previous.focus_owner:
        return True
    if unit.kind == "action" and unit.subject not in {previous.focus_owner, "场景"}:
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
                focus_owner=unit.subject or "场景",
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
                    focus_owner=unit.subject or "场景",
                )
            )
            continue
        current.units.append(unit)
        current.has_action = current.has_action or unit.kind in {"action", "support"}
        current.has_dialogue = current.has_dialogue or unit.kind == "dialogue"
        current.turn_signal = current.turn_signal or unit.turn_signal
        if unit.kind != "support":
            current.focus_owner = unit.subject or current.focus_owner
    return segments


def build_group_metrics(section: GroupSection, pace_tier: str) -> dict[str, Any]:
    canonical_body, hook_body = split_tail_hook_block(section.body)
    canonical_units = parse_units(canonical_body)
    hook_units = parse_units(hook_body)
    segments = build_segments(canonical_units)
    hook_segments = build_segments(hook_units)

    canonical_beat_count = max(1, len(segments))
    action_phase_points = sum(1 for seg in segments if seg.has_action)
    dialogue_breath_points = sum(1 for seg in segments if seg.has_dialogue)
    focus_shift_points = sum(
        1
        for idx in range(1, len(segments))
        if segments[idx - 1].focus_owner != segments[idx].focus_owner
    )
    structural_turn_points = sum(1 for seg in segments if seg.turn_signal)
    hook_preview_count = len(hook_segments)

    pace_coef = PACE_COEFFICIENT[pace_tier]
    recommended_shot_baseline = max(1, round(canonical_beat_count * pace_coef))

    split_bonus = 0
    split_bonus_reasons: list[str] = []
    if hook_preview_count:
        split_bonus += 1
        split_bonus_reasons.append("tail-hook 形成预映余波")
    if any(token in canonical_body for token in CROWD_KEYWORDS) and focus_shift_points >= 1:
        split_bonus += 1
        split_bonus_reasons.append("存在群体压力或多对象接力反应")
    if split_bonus < 2 and any(token in canonical_body for token in BURST_KEYWORDS) and structural_turn_points >= 1:
        split_bonus += 1
        split_bonus_reasons.append("存在爆点/落锁/失控等必须单独着陆的转折")
    split_bonus = min(split_bonus, 2)

    merge_discount = 0
    merge_discount_reasons: list[str] = []
    focus_counter = Counter(seg.focus_owner for seg in segments)
    dominant_focus, dominant_focus_count = focus_counter.most_common(1)[0]
    if canonical_beat_count >= 2 and dominant_focus_count >= max(2, canonical_beat_count - 1):
        merge_discount += 1
        merge_discount_reasons.append(f"主焦点长期稳定在 `{dominant_focus}`，可合镜")
    if structural_turn_points == 0 and focus_shift_points <= 1:
        merge_discount += 1
        merge_discount_reasons.append("转折与焦点切换有限，连续动作/对话链可压并")
    merge_discount = min(merge_discount, 2)

    shot_count_decision = max(1, recommended_shot_baseline + split_bonus - merge_discount)

    why_not_fewer = (
        f"当前组至少有 {canonical_beat_count} 个候选节拍，"
        f"且触发了 {split_bonus} 项拆镜加权，压得更少会吞掉关键落点。"
    )
    why_not_more = (
        f"当前组已有 {merge_discount} 项合镜折减，且主焦点/动作链存在可连续完成的部分，"
        "继续加镜会把同一信息切碎。"
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
        "split_bonus": split_bonus,
        "split_bonus_reasons": split_bonus_reasons,
        "merge_discount": merge_discount,
        "merge_discount_reasons": merge_discount_reasons,
        "shot_count_decision": shot_count_decision,
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
    shot_distribution = Counter(group["shot_count_decision"] for group in groups)

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
            f"+split={group['split_bonus']} -merge={group['merge_discount']} "
            f"=> shots={group['shot_count_decision']}"
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
