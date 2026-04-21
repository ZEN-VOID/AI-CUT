#!/usr/bin/env python3
"""Backfill `正文切分参考` and `正文回指` for a 3-Detail episode root.

This compatibility repair script is meant for projects whose shared
`3-Detail/第N集.json` already carries canonical `剧本正文 + 分镜明细[]`, but
the bridge layer between them was never landed.
"""

from __future__ import annotations

import argparse
import difflib
import json
import math
import re
from copy import deepcopy
from pathlib import Path
from typing import Any


VISUAL_LINE_PREFIXES = {
    "动作画面：": "动作",
    "对白画面：": "对白",
}
SENTENCE_ENDINGS = "。！？!?"
CLAUSE_PUNCT = "，；、"


def find_repo_root() -> Path:
    current = Path(__file__).resolve()
    for parent in current.parents:
        if (parent / "AGENTS.md").exists():
            return parent
    raise RuntimeError("无法定位仓库根目录。")


ROOT = find_repo_root()


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )


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


def normalize_text(value: str) -> str:
    return re.sub(r"[\s，。！？；：、“”‘’（）()《》【】\-—,.!?;:]+", "", value)


def similarity(left: str, right: str) -> float:
    left_norm = normalize_text(left)
    right_norm = normalize_text(right)
    if not left_norm or not right_norm:
        return 0.0
    return difflib.SequenceMatcher(None, left_norm, right_norm).ratio()


def split_sentence_spans(text: str) -> list[tuple[int, int]]:
    spans: list[tuple[int, int]] = []
    start = 0
    for index, char in enumerate(text):
        if char in SENTENCE_ENDINGS:
            end = index + 1
            if text[start:end].strip():
                spans.append((start, end))
            start = end
    if text[start:].strip():
        spans.append((start, len(text)))
    return spans


def split_clause_once(text: str) -> tuple[tuple[int, int], tuple[int, int]] | None:
    candidates = [index for index, char in enumerate(text) if char in CLAUSE_PUNCT]
    if not candidates:
        return None
    midpoint = len(text) / 2
    split_at = min(candidates, key=lambda index: abs(index - midpoint))
    left = text[: split_at + 1].strip()
    right = text[split_at + 1 :].strip()
    if not left or not right:
        return None
    return (0, split_at + 1), (split_at + 1, len(text))


def extract_visual_segments(script_body: str, target_count: int) -> list[dict[str, Any]]:
    segments: list[dict[str, Any]] = []
    cursor = 0
    for raw_line in script_body.splitlines():
        prefix = next((item for item in VISUAL_LINE_PREFIXES if raw_line.startswith(item)), None)
        if not prefix:
            cursor += len(raw_line) + 1
            continue
        line_start = script_body.find(raw_line, cursor)
        if line_start < 0:
            raise ValueError("无法在 `剧本正文` 中定位 visual line。")
        body = raw_line[len(prefix) :]
        body_start = line_start + len(prefix)
        segment_type = VISUAL_LINE_PREFIXES[prefix]
        for relative_start, relative_end in split_sentence_spans(body):
            excerpt = body[relative_start:relative_end].strip()
            if not excerpt:
                continue
            absolute_start = body_start + relative_start
            absolute_end = body_start + relative_end
            segments.append(
                {
                    "segment_type": segment_type,
                    "原文片段": excerpt,
                    "char_range": {
                        "start": absolute_start,
                        "end": absolute_end,
                    },
                }
            )
        cursor = line_start + len(raw_line) + 1

    while len(segments) < target_count:
        split_index: int | None = None
        split_parts: tuple[tuple[int, int], tuple[int, int]] | None = None
        best_length = -1
        for index, segment in enumerate(segments):
            excerpt = segment["原文片段"]
            candidate = split_clause_once(excerpt)
            if candidate and len(excerpt) > best_length:
                split_index = index
                split_parts = candidate
                best_length = len(excerpt)
        if split_index is None or split_parts is None:
            break
        source = segments[split_index]
        source_start = source["char_range"]["start"]
        source_text = source["原文片段"]
        replacements: list[dict[str, Any]] = []
        for local_start, local_end in split_parts:
            excerpt = source_text[local_start:local_end].strip()
            if not excerpt:
                continue
            replacements.append(
                {
                    "segment_type": source["segment_type"],
                    "原文片段": excerpt,
                    "char_range": {
                        "start": source_start + local_start,
                        "end": source_start + local_end,
                    },
                }
            )
        if len(replacements) < 2:
            break
        segments[split_index : split_index + 1] = replacements

    for segment in segments:
        start = segment["char_range"]["start"]
        end = segment["char_range"]["end"]
        if script_body[start:end] != segment["原文片段"]:
            raise ValueError("切分出的 `原文片段` 与 `char_range` 不一致。")
    return segments


def shot_text(shot: dict[str, Any]) -> str:
    chunks: list[str] = []
    string_fields = (
        "分镜表现",
        "角色背景面",
        "角色站位走位",
        "道具及状态",
        "分镜构图",
        "摄影美学",
        "运镜手法",
    )
    dict_fields = (
        "角色表现",
        "人物表演",
        "运动表现",
        "动作调度",
        "氛围表现",
        "空间氛围",
        "视觉强化",
        "视觉焦点",
    )
    for field in string_fields:
        value = shot.get(field)
        if isinstance(value, str) and value.strip():
            chunks.append(value.strip())
    for field in dict_fields:
        value = shot.get(field)
        if not isinstance(value, dict):
            continue
        for item in value.values():
            if isinstance(item, str) and item.strip():
                chunks.append(item.strip())
    return " ".join(chunks)


def align_segments_to_shots(shots: list[dict[str, Any]], segments: list[dict[str, Any]]) -> list[list[int]]:
    shot_count = len(shots)
    segment_count = len(segments)
    if shot_count == 0 or segment_count == 0:
        raise ValueError("镜头或正文切分为空，无法对齐。")
    if segment_count < shot_count:
        # Final safety net: allow tail reuse when the script body cannot be split any further.
        result: list[list[int]] = []
        for index in range(shot_count):
            mapped = min(round(index * (segment_count - 1) / max(shot_count - 1, 1)), segment_count - 1)
            result.append([mapped])
        return result

    shot_texts = [shot_text(shot) for shot in shots]
    segment_texts = [segment["原文片段"] for segment in segments]
    chunk_cache: dict[tuple[int, int, int], float] = {}

    def chunk_score(shot_index: int, start: int, end: int) -> float:
        key = (shot_index, start, end)
        if key in chunk_cache:
            return chunk_cache[key]
        chunk_text = " ".join(segment_texts[start:end])
        semantic = similarity(shot_texts[shot_index], chunk_text)
        position_center = ((start + end - 1) / 2) / max(segment_count - 1, 1)
        shot_center = shot_index / max(shot_count - 1, 1) if shot_count > 1 else 0.0
        position_bonus = 0.15 * (1.0 - abs(position_center - shot_center))
        length_penalty = 0.03 * max(0, (end - start) - 2)
        score = semantic + position_bonus - length_penalty
        chunk_cache[key] = score
        return score

    neg_inf = -10**9
    dp = [[neg_inf] * (segment_count + 1) for _ in range(shot_count + 1)]
    prev: list[list[int | None]] = [[None] * (segment_count + 1) for _ in range(shot_count + 1)]
    dp[0][0] = 0.0

    for shot_index in range(1, shot_count + 1):
        for used_segments in range(shot_index, segment_count + 1):
            for split_at in range(shot_index - 1, used_segments):
                candidate = dp[shot_index - 1][split_at] + chunk_score(shot_index - 1, split_at, used_segments)
                if candidate > dp[shot_index][used_segments]:
                    dp[shot_index][used_segments] = candidate
                    prev[shot_index][used_segments] = split_at

    if math.isclose(dp[shot_count][segment_count], neg_inf):
        raise ValueError("无法为当前分镜组建立稳定的 beat_refs 对齐。")

    assignments: list[list[int]] = []
    shot_index = shot_count
    used_segments = segment_count
    while shot_index > 0:
        split_at = prev[shot_index][used_segments]
        if split_at is None:
            raise ValueError("回溯 `beat_refs` 对齐结果失败。")
        assignments.append(list(range(split_at, used_segments)))
        shot_index -= 1
        used_segments = split_at
    assignments.reverse()
    return assignments


def group_needs_backfill(group: dict[str, Any], force: bool) -> bool:
    if force:
        return True
    references = group.get("正文切分参考")
    if not isinstance(references, list) or not references:
        return True
    shots = require_list(group.get("分镜明细"), f"{group.get('分镜组ID')}.分镜明细")
    return any(not isinstance(require_dict(shot, "分镜明细[]").get("正文回指"), dict) for shot in shots)


def backfill_group(group: dict[str, Any], force: bool) -> dict[str, Any]:
    group_id = require_non_empty_text(group.get("分镜组ID"), "分镜组ID")
    script_body = require_non_empty_text(group.get("剧本正文"), f"{group_id}.剧本正文")
    shots = [require_dict(item, f"{group_id}.分镜明细[]") for item in require_list(group.get("分镜明细"), f"{group_id}.分镜明细")]
    if not group_needs_backfill(group, force):
        return {
            "group_id": group_id,
            "status": "skipped",
            "shot_count": len(shots),
            "beat_count": len(require_list(group.get("正文切分参考"), f"{group_id}.正文切分参考")),
        }

    segments = extract_visual_segments(script_body, len(shots))
    assignments = align_segments_to_shots(shots, segments)
    beat_ids: list[str] = []
    references: list[dict[str, Any]] = []
    for index, segment in enumerate(segments, start=1):
        beat_id = f"{group_id}-b{index:02d}"
        beat_ids.append(beat_id)
        references.append(
            {
                "beat_id": beat_id,
                "原文片段": segment["原文片段"],
                "anchor_summary": segment["原文片段"],
                "segment_type": segment["segment_type"],
                "char_range": deepcopy(segment["char_range"]),
            }
        )

    for shot, segment_indexes in zip(shots, assignments):
        beat_refs = [beat_ids[index] for index in segment_indexes]
        coverage_mode = "direct" if len(beat_refs) == 1 else "composite"
        script_ref: dict[str, Any] = {
            "beat_refs": beat_refs,
            "coverage_mode": coverage_mode,
        }
        if coverage_mode == "composite":
            script_ref["strategy_note"] = "当前镜头通过相邻画面句聚合回链。"
        shot["正文回指"] = script_ref

    group["正文切分参考"] = references
    return {
        "group_id": group_id,
        "status": "updated",
        "shot_count": len(shots),
        "beat_count": len(references),
    }


def backfill_episode(episode_path: Path, group_ids: set[str] | None, force: bool, dry_run: bool) -> dict[str, Any]:
    data = load_json(episode_path)
    groups = require_list(
        require_dict(require_dict(data.get("final_output"), "final_output").get("main_content"), "final_output.main_content").get("分镜组列表"),
        "final_output.main_content.分镜组列表",
    )
    results: list[dict[str, Any]] = []
    updated = False
    for raw_group in groups:
        group = require_dict(raw_group, "分镜组列表[]")
        group_id = require_non_empty_text(group.get("分镜组ID"), "分镜组ID")
        if group_ids and group_id not in group_ids:
            continue
        result = backfill_group(group, force=force)
        results.append(result)
        updated = updated or result["status"] == "updated"

    if updated and not dry_run:
        write_json(episode_path, data)
    return {
        "episode_json": str(episode_path.relative_to(ROOT)),
        "updated": updated and not dry_run,
        "dry_run": dry_run,
        "groups": results,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="为 3-Detail episode root 回填 `正文切分参考` 与 `正文回指`。")
    parser.add_argument("episode_json", help="`projects/aigc/<项目名>/3-Detail/第N集.json` 路径")
    parser.add_argument("--group-id", action="append", dest="group_ids", help="仅修复指定分镜组，可重复传入")
    parser.add_argument("--force", action="store_true", help="即使当前组已有桥接层，也强制重建")
    parser.add_argument("--dry-run", action="store_true", help="只输出修复计划，不写回文件")
    args = parser.parse_args()

    episode_path = (ROOT / args.episode_json).resolve() if not Path(args.episode_json).is_absolute() else Path(args.episode_json)
    result = backfill_episode(
        episode_path=episode_path,
        group_ids=set(args.group_ids or []),
        force=args.force,
        dry_run=args.dry_run,
    )
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
