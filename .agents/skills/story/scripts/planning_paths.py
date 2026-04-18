#!/usr/bin/env python3
"""
Canonical + legacy planning artifact path helpers.

Canonical planning now keeps:
- one machine-readable holomap truth
- child-side pass artifacts under `2-Planning/pass-artifacts/`

Legacy directory-style paths are still supported as read fallback during migration.
"""

from __future__ import annotations

from pathlib import Path


_CANONICAL_REL_PATHS: dict[str, str] = {
    "holomap": "2-Planning/全息地图.json",
}

_CANONICAL_PASS_ARTIFACT_REL_PATHS: dict[str, str] = {
    "genre_selection": "2-Planning/pass-artifacts/1-题材选型.json",
    "chapter_planning": "2-Planning/pass-artifacts/2-章节规划.json",
    "story_outline": "2-Planning/pass-artifacts/3-故事大纲.json",
    "conflict_design": "2-Planning/pass-artifacts/4-冲突设计.json",
    "mission_design": "2-Planning/pass-artifacts/5-任务设计.json",
    "clue_design": "2-Planning/pass-artifacts/6-线索设计.json",
    "foreshadow_design": "2-Planning/pass-artifacts/7-伏笔设计.json",
}

_LEGACY_REL_PATHS: dict[str, str] = {
    "genre_selection": "2-Planning/1-题材选型/题材选型.json",
    "chapter_planning": "2-Planning/2-章节规划/章节规划.json",
    "story_outline": "2-Planning/3-故事大纲/故事大纲.json",
    "conflict_design": "2-Planning/4-冲突设计/冲突设计.json",
    "mission_design": "2-Planning/5-任务设计/任务设计.json",
    "clue_design": "2-Planning/6-线索设计/线索设计.json",
    "foreshadow_design": "2-Planning/7-伏笔设计/伏笔设计.json",
    "holomap": "2-Planning/8-全息地图/全息地图.json",
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


def canonical_planning_pass_artifact_relpath(artifact_key: str) -> str:
    return _CANONICAL_PASS_ARTIFACT_REL_PATHS[artifact_key]


def canonical_planning_pass_artifact_path(project_root: Path, artifact_key: str) -> Path:
    return project_root / canonical_planning_pass_artifact_relpath(artifact_key)


def resolve_planning_pass_artifact_path(project_root: Path, artifact_key: str) -> Path:
    canonical = canonical_planning_pass_artifact_path(project_root, artifact_key)
    if canonical.is_file():
        return canonical

    legacy = legacy_planning_artifact_path(project_root, artifact_key)
    if legacy.is_file():
        return legacy

    return canonical
