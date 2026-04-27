#!/usr/bin/env python3
"""
Chapter file path helpers.

This project currently uses the canonical drafting layout:
1) Canonical layout: 3-初稿/第1卷/第7章.md

Legacy published-manuscript layouts may still exist in older projects:
2) Legacy flat 3-初稿 layout: 3-初稿/第7章.md
3) Legacy flat 3-初稿 layout: 3-初稿/第7集.md
4) Legacy flat layout: 正文/第0007章.md
5) Volume layout:      正文/第1卷/第007章-章节标题.md

To keep scripts robust, always resolve chapter files via these helpers instead of hardcoding a format.
"""

from __future__ import annotations

import re
from pathlib import Path
from typing import Optional

try:
    from planning_paths import planning_volume_num_for_chapter
except ImportError:  # pragma: no cover
    from scripts.planning_paths import planning_volume_num_for_chapter


_CHAPTER_NUM_RE = re.compile(r"第(?P<num>\d+)(?:章|集)")
_OUTLINE_HEADING_RE = re.compile(r"^#{1,6}\s*第\s*(?P<num>\d+)\s*章[：:]\s*(?P<title>.+?)\s*$", re.MULTILINE)
_SPLIT_OUTLINE_FILENAME_RE = re.compile(r"^第0*(?P<num>\d+)章[-—_ ]+(?P<title>.+?)\.md$")


def volume_num_for_chapter(chapter_num: int, *, chapters_per_volume: int = 10) -> int:
    if chapter_num <= 0:
        raise ValueError("chapter_num must be >= 1")
    return (chapter_num - 1) // chapters_per_volume + 1


def extract_chapter_num_from_filename(filename: str) -> Optional[int]:
    m = _CHAPTER_NUM_RE.search(filename)
    if not m:
        return None
    try:
        return int(m.group("num"))
    except ValueError:
        return None


def _safe_title_for_filename(title: str) -> str:
    cleaned = title.strip()
    if not cleaned:
        return ""

    try:
        from security_utils import sanitize_filename
    except ImportError:  # pragma: no cover
        from scripts.security_utils import sanitize_filename

    safe_title = sanitize_filename(cleaned, max_length=60)
    return "" if safe_title == "unnamed_entity" else safe_title


def _extract_title_from_outline_text(outline_text: str, chapter_num: int) -> str:
    for match in _OUTLINE_HEADING_RE.finditer(outline_text):
        if int(match.group("num")) != chapter_num:
            continue
        return _safe_title_for_filename(match.group("title"))
    return ""


def _extract_title_from_split_outline_filename(outline_dir: Path, chapter_num: int) -> str:
    patterns = [
        f"第{chapter_num}章*.md",
        f"第{chapter_num:02d}章*.md",
        f"第{chapter_num:03d}章*.md",
        f"第{chapter_num:04d}章*.md",
    ]
    for pattern in patterns:
        for path in sorted(outline_dir.glob(pattern)):
            match = _SPLIT_OUTLINE_FILENAME_RE.match(path.name)
            if not match:
                continue
            if int(match.group("num")) != chapter_num:
                continue
            title = _safe_title_for_filename(match.group("title"))
            if title:
                return title
    return ""


def extract_chapter_title(project_root: Path, chapter_num: int) -> str:
    """优先从 canonical chapter plan 提取标题，缺失时回退到兼容 carrier 或旧大纲。"""
    try:
        from chapter_outline_loader import load_chapter_outline
    except ImportError:  # pragma: no cover
        from scripts.chapter_outline_loader import load_chapter_outline

    outline_text = load_chapter_outline(project_root, chapter_num, max_chars=None)
    if not outline_text.startswith("⚠️"):
        title = _extract_title_from_outline_text(outline_text, chapter_num)
        if title:
            return title

    outline_dir = project_root / "2-卷章" / "legacy"
    if outline_dir.exists():
        return _extract_title_from_split_outline_filename(outline_dir, chapter_num)
    return ""


def _build_chapter_filename(project_root: Path, chapter_num: int, *, use_volume_layout: bool) -> str:
    padded = f"{chapter_num:03d}" if use_volume_layout else f"{chapter_num:04d}"
    title = extract_chapter_title(project_root, chapter_num)
    if title:
        return f"第{padded}章-{title}.md"
    return f"第{padded}章.md"


def find_chapter_file(project_root: Path, chapter_num: int) -> Optional[Path]:
    """
    Find an existing chapter file for chapter_num.

    Resolution order:
    1) canonical 3-初稿 root (`第N卷/第N章.md`)
    2) legacy flat 3-初稿 root (`第N章.md`)
    3) legacy flat 3-初稿 root (`第N集.md`)
    4) legacy 正文 flat layout
    5) legacy 正文 volume/custom layout
    Returns the first match (stable sorted order) or None if not found.
    """
    canonical = drafting_root_md_path(project_root, chapter_num)
    if canonical.exists():
        return canonical

    legacy_flat_chapter = project_root / "3-初稿" / f"第{chapter_num}章.md"
    if legacy_flat_chapter.exists():
        return legacy_flat_chapter

    legacy_flat_episode = project_root / "3-初稿" / f"第{chapter_num}集.md"
    if legacy_flat_episode.exists():
        return legacy_flat_episode

    chapters_dir = project_root / "正文"
    if not chapters_dir.exists():
        return None

    legacy = chapters_dir / f"第{chapter_num:04d}章.md"
    if legacy.exists():
        return legacy

    if chapter_num > 0:
        vol_dir = chapters_dir / f"第{volume_num_for_chapter(chapter_num)}卷"
        if vol_dir.exists():
            candidates = sorted(vol_dir.glob(f"第{chapter_num:03d}章*.md")) + sorted(vol_dir.glob(f"第{chapter_num:04d}章*.md"))
            for c in candidates:
                if c.is_file():
                    return c

    candidates = sorted(chapters_dir.rglob(f"第{chapter_num:03d}章*.md")) + sorted(chapters_dir.rglob(f"第{chapter_num:04d}章*.md"))
    for c in candidates:
        if c.is_file():
            return c

    return None


def default_chapter_draft_path(project_root: Path, chapter_num: int, *, use_volume_layout: bool = False) -> Path:
    """
    Preferred canonical draft path when creating a new chapter file.

    Args:
        project_root: 项目根目录
        chapter_num: 章节号
        use_volume_layout: legacy arg; ignored for canonical 3-初稿 layout

    Current canonical root is `3-初稿/第N卷/第N章.md`.
    """
    return drafting_root_md_path(project_root, chapter_num)


def drafting_root_md_path(project_root: Path, chapter_num: int) -> Path:
    """
    Canonical stage-runtime root file for 3-初稿.

    Example:
        3-初稿/第1卷/第7章.md
    """
    if chapter_num <= 0:
        raise ValueError("chapter_num must be >= 1")
    volume_num = planning_volume_num_for_chapter(chapter_num, project_root=project_root)
    return project_root / "3-初稿" / f"第{volume_num}卷" / f"第{chapter_num}章.md"


def polishing_root_md_path(project_root: Path, chapter_num: int) -> Path:
    """
    Canonical stage-runtime root file for 4-润色.

    Example:
        4-润色/第1卷/第7章.md
    """
    if chapter_num <= 0:
        raise ValueError("chapter_num must be >= 1")
    volume_num = planning_volume_num_for_chapter(chapter_num, project_root=project_root)
    return project_root / "4-润色" / f"第{volume_num}卷" / f"第{chapter_num}章.md"
