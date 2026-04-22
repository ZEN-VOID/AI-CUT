#!/usr/bin/env python3
"""
Canonical + compatibility planning artifact path helpers.

Primary planning truth now keeps:
- `2-Planning/整体规划.md`
- `2-Planning/第N卷/卷规划.md`
- `2-Planning/第N卷/第N章.md`

Legacy `全息地图.json` and old step artifacts are still supported as compatibility fallbacks.
"""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Iterable


PLANNING_CHAPTERS_PER_VOLUME = 10
_CHAPTER_RANGE_RE = re.compile(r"^\s*(\d+)\s*-\s*(\d+)\s*$")

_CANONICAL_REL_PATHS: dict[str, str] = {
    "book_plan": "2-Planning/整体规划.md",
    "holomap": "2-Planning/全息地图.json",
}

_LEGACY_REL_PATHS: dict[str, str] = {
    "genre_selection": "1-Cards/5-类型卡/总题材/类型总卡.json",
    "chapter_planning": "2-Planning/2-章节规划/章节规划.json",
    "story_outline": "2-Planning/3-故事大纲/故事大纲.json",
    "conflict_design": "2-Planning/4-冲突设计/冲突设计.json",
    "mission_design": "2-Planning/5-任务设计/任务设计.json",
    "clue_design": "2-Planning/6-线索设计/线索设计.json",
    "foreshadow_design": "2-Planning/7-伏笔设计/伏笔设计.json",
    "holomap": "2-Planning/8-全息地图/全息地图.json",
}


def _parse_chapters_range(raw: object) -> tuple[int, int] | None:
    text = str(raw or "").strip()
    match = _CHAPTER_RANGE_RE.fullmatch(text)
    if not match:
        return None
    start = int(match.group(1))
    end = int(match.group(2))
    if start <= 0 or end < start:
        return None
    return start, end


def _load_state_payload(project_root: Path) -> dict:
    state_path = project_root / "STATE.json"
    if not state_path.is_file():
        return {}
    try:
        payload = json.loads(state_path.read_text(encoding="utf-8"))
    except Exception:
        return {}
    return payload if isinstance(payload, dict) else {}


def _volumes_planned(project_root: Path) -> list[dict]:
    state = _load_state_payload(project_root)
    progress = state.get("progress")
    if not isinstance(progress, dict):
        return []
    rows = progress.get("volumes_planned")
    if not isinstance(rows, list):
        return []
    return [row for row in rows if isinstance(row, dict)]


def _state_volume_num_for_chapter(project_root: Path, chapter_num: int) -> int | None:
    best: tuple[int, int] | None = None
    for row in _volumes_planned(project_root):
        volume = row.get("volume")
        if not isinstance(volume, int) or volume <= 0:
            continue
        parsed = _parse_chapters_range(row.get("chapters_range"))
        if not parsed:
            continue
        start, end = parsed
        if start <= chapter_num <= end:
            candidate = (start, volume)
            if best is None or candidate[0] > best[0] or (candidate[0] == best[0] and candidate[1] < best[1]):
                best = candidate
    return best[1] if best else None


def planning_volume_num_for_chapter(chapter_num: int, project_root: Path | None = None) -> int:
    if chapter_num <= 0:
        raise ValueError("chapter_num must be >= 1")
    if project_root is not None:
        resolved = _state_volume_num_for_chapter(project_root, chapter_num)
        if resolved is not None:
            return resolved
    return (chapter_num - 1) // PLANNING_CHAPTERS_PER_VOLUME + 1


def planned_chapter_numbers_for_volume(project_root: Path, volume_num: int) -> list[int]:
    if volume_num <= 0:
        raise ValueError("volume_num must be >= 1")

    for row in _volumes_planned(project_root):
        if int(row.get("volume") or 0) != volume_num:
            continue
        parsed = _parse_chapters_range(row.get("chapters_range"))
        if parsed:
            start, end = parsed
            return list(range(start, end + 1))

    volume_dir = project_root / "2-Planning" / f"第{volume_num}卷"
    chapter_nums: list[int] = []
    if volume_dir.is_dir():
        for path in volume_dir.glob("第*章.md"):
            name = path.stem
            match = re.fullmatch(r"第(\d+)章", name)
            if match:
                chapter_nums.append(int(match.group(1)))
    if chapter_nums:
        return sorted(set(chapter_nums))

    start = (volume_num - 1) * PLANNING_CHAPTERS_PER_VOLUME + 1
    end = start + PLANNING_CHAPTERS_PER_VOLUME - 1
    return list(range(start, end + 1))


def canonical_planning_artifact_relpath(artifact_key: str) -> str:
    return _CANONICAL_REL_PATHS[artifact_key]


def legacy_planning_artifact_relpath(artifact_key: str) -> str:
    return _LEGACY_REL_PATHS[artifact_key]


def canonical_planning_artifact_path(project_root: Path, artifact_key: str) -> Path:
    return project_root / canonical_planning_artifact_relpath(artifact_key)


def legacy_planning_artifact_path(project_root: Path, artifact_key: str) -> Path:
    return project_root / legacy_planning_artifact_relpath(artifact_key)


def resolve_planning_artifact_path(project_root: Path, artifact_key: str) -> Path:
    canonical = canonical_planning_artifact_path(project_root, artifact_key)
    if canonical.is_file():
        return canonical

    if artifact_key in _LEGACY_REL_PATHS:
        legacy = legacy_planning_artifact_path(project_root, artifact_key)
        if legacy.is_file():
            return legacy

    return canonical


def canonical_book_plan_relpath() -> str:
    return _CANONICAL_REL_PATHS["book_plan"]


def canonical_book_plan_path(project_root: Path) -> Path:
    return project_root / canonical_book_plan_relpath()


def canonical_volume_plan_relpath(volume_num: int) -> str:
    return f"2-Planning/第{volume_num}卷/卷规划.md"


def canonical_volume_plan_path(project_root: Path, volume_num: int) -> Path:
    return project_root / canonical_volume_plan_relpath(volume_num)


def canonical_chapter_plan_relpath(
    chapter_num: int,
    volume_num: int | None = None,
    project_root: Path | None = None,
) -> str:
    volume = volume_num or planning_volume_num_for_chapter(chapter_num, project_root=project_root)
    return f"2-Planning/第{volume}卷/第{chapter_num}章.md"


def canonical_chapter_plan_path(project_root: Path, chapter_num: int, volume_num: int | None = None) -> Path:
    return project_root / canonical_chapter_plan_relpath(chapter_num, volume_num, project_root=project_root)


def canonical_book_plan_actualization_relpath() -> str:
    return "2-Planning/整体规划.actualization.json"


def canonical_book_plan_actualization_path(project_root: Path) -> Path:
    return project_root / canonical_book_plan_actualization_relpath()


def canonical_volume_plan_actualization_relpath(volume_num: int) -> str:
    return f"2-Planning/第{volume_num}卷/卷规划.actualization.json"


def canonical_volume_plan_actualization_path(project_root: Path, volume_num: int) -> Path:
    return project_root / canonical_volume_plan_actualization_relpath(volume_num)


def canonical_chapter_plan_actualization_relpath(
    chapter_num: int,
    volume_num: int | None = None,
    project_root: Path | None = None,
) -> str:
    volume = volume_num or planning_volume_num_for_chapter(chapter_num, project_root=project_root)
    return f"2-Planning/第{volume}卷/第{chapter_num}章.actualization.json"


def canonical_chapter_plan_actualization_path(project_root: Path, chapter_num: int, volume_num: int | None = None) -> Path:
    return project_root / canonical_chapter_plan_actualization_relpath(
        chapter_num,
        volume_num,
        project_root=project_root,
    )
