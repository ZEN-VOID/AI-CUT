#!/usr/bin/env python3
"""
Canonical + legacy planning artifact path helpers.

2-Planning now writes sibling JSON files directly under `Planning/`.
Legacy directory-style paths are still supported as read fallback during migration.
"""

from __future__ import annotations

from pathlib import Path


_CANONICAL_REL_PATHS: dict[str, str] = {
    "genre_selection": "Planning/1-题材选型.json",
    "chapter_planning": "Planning/2-章节规划.json",
    "story_outline": "Planning/3-故事大纲.json",
    "conflict_design": "Planning/4-冲突设计.json",
    "mission_design": "Planning/5-任务设计.json",
    "clue_design": "Planning/6-线索设计.json",
    "foreshadow_design": "Planning/7-伏笔设计.json",
    "holomap": "Planning/8-全息地图.json",
}

_LEGACY_REL_PATHS: dict[str, str] = {
    "genre_selection": "Planning/1-题材选型/题材选型.json",
    "chapter_planning": "Planning/2-章节规划/章节规划.json",
    "story_outline": "Planning/3-故事大纲/故事大纲.json",
    "conflict_design": "Planning/4-冲突设计/冲突设计.json",
    "mission_design": "Planning/5-任务设计/任务设计.json",
    "clue_design": "Planning/6-线索设计/线索设计.json",
    "foreshadow_design": "Planning/7-伏笔设计/伏笔设计.json",
    "holomap": "Planning/8-全息地图/全息地图.json",
}


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

    legacy = legacy_planning_artifact_path(project_root, artifact_key)
    if legacy.is_file():
        return legacy

    return canonical
