#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from __future__ import annotations

import json
import re
from pathlib import Path

try:
    from planning_paths import canonical_planning_artifact_relpath, resolve_planning_artifact_path
except ImportError:  # pragma: no cover
    from scripts.planning_paths import canonical_planning_artifact_relpath, resolve_planning_artifact_path

try:
    from chapter_paths import volume_num_for_chapter
except ImportError:  # pragma: no cover
    from scripts.chapter_paths import volume_num_for_chapter

try:
    from project_locator import resolve_state_file
except ImportError:  # pragma: no cover
    from scripts.project_locator import resolve_state_file


_CHAPTER_RANGE_RE = re.compile(r"^\s*(\d+)\s*-\s*(\d+)\s*$")
_CHAPTER_REF_RE = re.compile(r"第\s*(\d+)\s*章(?:[：:]\s*(.+))?")


def _parse_chapters_range(value: object) -> tuple[int, int] | None:
    if not isinstance(value, str):
        return None
    match = _CHAPTER_RANGE_RE.match(value)
    if not match:
        return None
    try:
        start = int(match.group(1))
        end = int(match.group(2))
    except ValueError:
        return None
    if start <= 0 or end <= 0 or start > end:
        return None
    return start, end


def volume_num_for_chapter_from_state(project_root: Path, chapter_num: int) -> int | None:
    state_path = resolve_state_file(explicit_project_root=str(project_root))
    if not state_path.exists():
        return None

    try:
        state = json.loads(state_path.read_text(encoding="utf-8"))
    except Exception:
        return None

    if not isinstance(state, dict):
        return None

    progress = state.get("progress")
    if not isinstance(progress, dict):
        return None

    volumes_planned = progress.get("volumes_planned")
    if not isinstance(volumes_planned, list):
        return None

    best: tuple[int, int] | None = None
    for item in volumes_planned:
        if not isinstance(item, dict):
            continue
        volume = item.get("volume")
        if not isinstance(volume, int) or volume <= 0:
            continue
        parsed = _parse_chapters_range(item.get("chapters_range"))
        if not parsed:
            continue
        start, end = parsed
        if start <= chapter_num <= end:
            candidate = (start, volume)
            if best is None or candidate[0] > best[0] or (candidate[0] == best[0] and candidate[1] < best[1]):
                best = candidate

    return best[1] if best else None


def _holomap_path(project_root: Path) -> Path:
    return resolve_planning_artifact_path(project_root, "holomap")


def _load_holomap(project_root: Path) -> dict | None:
    holomap_path = _holomap_path(project_root)
    if not holomap_path.exists():
        return None
    try:
        data = json.loads(holomap_path.read_text(encoding="utf-8"))
    except Exception:
        return None
    return data if isinstance(data, dict) else None


def _extract_holomap_root(data: dict) -> dict:
    content = data.get("content")
    if isinstance(content, dict):
        holomap = content.get("holomap")
        if isinstance(holomap, dict):
            return holomap
    holomap = data.get("holomap")
    return holomap if isinstance(holomap, dict) else {}


def _extract_chapter_num(value: object) -> int | None:
    if isinstance(value, int):
        return value if value > 0 else None
    if isinstance(value, str):
        raw = value.strip()
        if not raw:
            return None
        if raw.isdigit():
            parsed = int(raw)
            return parsed if parsed > 0 else None
        match = _CHAPTER_REF_RE.search(raw)
        if match:
            parsed = int(match.group(1))
            return parsed if parsed > 0 else None
    if isinstance(value, dict):
        for key in ("chapter", "chapter_num", "chapter_number", "number", "index", "seq", "id", "label"):
            parsed = _extract_chapter_num(value.get(key))
            if parsed is not None:
                return parsed
    return None


def _collect_holomap_chapter_boards(holomap: dict) -> list[dict]:
    boards: list[dict] = []
    direct = holomap.get("chapter_boards")
    if isinstance(direct, list):
        boards.extend(item for item in direct if isinstance(item, dict))

    volumes = holomap.get("volume_boards")
    if isinstance(volumes, list):
        for volume in volumes:
            if not isinstance(volume, dict):
                continue
            for key in ("chapter_boards", "chapters", "chapter_nodes"):
                nested = volume.get(key)
                if isinstance(nested, list):
                    boards.extend(item for item in nested if isinstance(item, dict))
    return boards


def _extract_board_value(board: dict, *keys: str) -> object:
    for key in keys:
        if key in board:
            return board.get(key)

    for container_key in ("bundled_elements", "bundles", "node_groups", "grouped_nodes", "planned_state"):
        container = board.get(container_key)
        if not isinstance(container, dict):
            continue
        for key in keys:
            if key in container:
                return container.get(key)
    return None


def _board_chapter_num(board: dict) -> int | None:
    for key in (
        "chapter",
        "chapter_num",
        "chapter_number",
        "number",
        "index",
        "seq",
        "chapter_ref",
        "chapter_id",
        "chapter_label",
        "id",
        "title",
        "label",
        "episode_ref",
    ):
        parsed = _extract_chapter_num(board.get(key))
        if parsed is not None:
            return parsed
    return None


def _collect_sorted_chapter_boards(holomap: dict) -> list[tuple[int, dict]]:
    ordered: list[tuple[int, dict]] = []
    for board in _collect_holomap_chapter_boards(holomap):
        chapter_num = _board_chapter_num(board)
        if chapter_num is None:
            continue
        ordered.append((chapter_num, board))
    ordered.sort(key=lambda item: item[0])
    return ordered


def _find_holomap_chapter_board(project_root: Path, chapter_num: int) -> dict | None:
    data = _load_holomap(project_root)
    if not data:
        return None

    holomap = _extract_holomap_root(data)
    for board in _collect_holomap_chapter_boards(holomap):
        if _board_chapter_num(board) == chapter_num:
            return board
    return None


def _compact_whitespace(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip()


def _summarize_value(value: object) -> str:
    if value is None:
        return ""
    if isinstance(value, (str, int, float, bool)):
        return _compact_whitespace(str(value))
    if isinstance(value, dict):
        parts: list[str] = []
        for key in (
            "title",
            "name",
            "label",
            "summary",
            "description",
            "status",
            "goal",
            "outcome",
            "effect",
            "note",
        ):
            raw = value.get(key)
            if raw is None:
                continue
            text = _compact_whitespace(str(raw))
            if text and text not in parts:
                parts.append(text)
        if parts:
            return " / ".join(parts[:3])
        return _compact_whitespace(json.dumps(value, ensure_ascii=False))
    if isinstance(value, list):
        parts = [_summarize_value(item) for item in value]
        parts = [part for part in parts if part]
        return "；".join(parts[:3])
    return _compact_whitespace(str(value))


def _collect_section_items(board: dict, *keys: str) -> list[str]:
    value = _extract_board_value(board, *keys)
    if value is None:
        return []
    if isinstance(value, list):
        items = [_summarize_value(item) for item in value]
    else:
        items = [_summarize_value(value)]
    return [item for item in items if item]


def _extract_holomap_title(board: dict, chapter_num: int) -> str:
    for key in ("chapter_title", "title", "name", "label"):
        raw = board.get(key)
        if not raw:
            continue
        text = str(raw).strip()
        match = _CHAPTER_REF_RE.search(text)
        if match and int(match.group(1)) == chapter_num:
            return _compact_whitespace(match.group(2) or "")
        return _compact_whitespace(text)

    chapter_ref = board.get("chapter_ref")
    if isinstance(chapter_ref, dict):
        for key in ("title", "name", "label"):
            raw = chapter_ref.get(key)
            if raw:
                return _compact_whitespace(str(raw))
    return ""


def _render_holomap_board(board: dict, chapter_num: int) -> str:
    title = _extract_holomap_title(board, chapter_num)
    heading = f"### 第{chapter_num}章"
    if title:
        heading += f"：{title}"

    summary = _summarize_value(
        _extract_board_value(
            board,
            "summary",
            "synopsis",
            "chapter_summary",
            "core_summary",
            "purpose",
            "notes",
        )
    )
    time_anchor = _summarize_value(
        _extract_board_value(board, "timeline_anchor", "timeline_ref", "time_window", "time_slot", "time_marker")
    )
    board_role = _summarize_value(
        _extract_board_value(board, "chapter_role", "board_role", "function_slot", "slot", "beat_label")
    )
    volume_ref = _summarize_value(_extract_board_value(board, "volume_ref", "volume", "arc_ref", "arc"))

    lines = [heading, "", f"> 来源：{canonical_planning_artifact_relpath('holomap')}", ""]

    if summary:
        lines.append(summary)
        lines.append("")

    if time_anchor:
        lines.append(f"- 时间定位：{time_anchor}")
    if volume_ref:
        lines.append(f"- 卷篇定位：{volume_ref}")
    if board_role:
        lines.append(f"- 章节功能：{board_role}")
    if time_anchor or volume_ref or board_role:
        lines.append("")

    section_specs = [
        ("事件", ("events", "key_events", "event_nodes")),
        ("冲突", ("conflicts", "conflict_nodes")),
        ("任务", ("missions", "tasks", "objectives")),
        ("线索", ("clues", "clue_nodes")),
        ("伏笔", ("foreshadows", "foreshadow_nodes", "payoffs")),
        ("角色", ("characters", "cast")),
        ("场景", ("scenes", "scene_nodes", "locations")),
        ("物品", ("items", "props")),
        ("规则影响", ("rule_impacts", "rules", "world_rules")),
        ("状态变化", ("state_delta", "state_change", "outcome_state", "resolution_state")),
    ]
    for section_title, keys in section_specs:
        items = _collect_section_items(board, *keys)
        if not items:
            continue
        lines.append(f"#### {section_title}")
        lines.append("")
        for item in items:
            lines.append(f"- {item}")
        lines.append("")

    return "\n".join(lines).strip()

def _find_split_outline_file(outline_dir: Path, chapter_num: int) -> Path | None:
    patterns = [
        f"第{chapter_num}章*.md",
        f"第{chapter_num:02d}章*.md",
        f"第{chapter_num:03d}章*.md",
        f"第{chapter_num:04d}章*.md",
    ]
    for pattern in patterns:
        matches = sorted(outline_dir.glob(pattern))
        if matches:
            return matches[0]
    return None


def _find_volume_outline_file(project_root: Path, chapter_num: int) -> Path | None:
    outline_dir = project_root / "2-Planning" / "legacy"
    volume_num = volume_num_for_chapter_from_state(project_root, chapter_num) or volume_num_for_chapter(chapter_num)
    candidates = [
        outline_dir / f"第{volume_num}卷-详细大纲.md",
        outline_dir / f"第{volume_num}卷 - 详细大纲.md",
        outline_dir / f"第{volume_num}卷 详细大纲.md",
    ]
    return next((path for path in candidates if path.exists()), None)


def _extract_outline_section(content: str, chapter_num: int) -> str | None:
    patterns = [
        rf"###\s*第\s*{chapter_num}\s*章[：:]\s*(.+?)(?=###\s*第\s*\d+\s*章|##\s|$)",
        rf"###\s*第{chapter_num}章[：:]\s*(.+?)(?=###\s*第\d+章|##\s|$)",
    ]
    for pattern in patterns:
        match = re.search(pattern, content, re.DOTALL)
        if match:
            return match.group(0).strip()
    return None


def load_chapter_outline(project_root: Path, chapter_num: int, max_chars: int | None = 1500) -> str:
    holomap_board = _find_holomap_chapter_board(project_root, chapter_num)
    if holomap_board is not None:
        outline = _render_holomap_board(holomap_board, chapter_num)
        if max_chars and len(outline) > max_chars:
            return outline[:max_chars] + "\n...(已截断)"
        return outline

    outline_dir = project_root / "2-Planning" / "legacy"

    split_outline = _find_split_outline_file(outline_dir, chapter_num)
    if split_outline is not None:
        return split_outline.read_text(encoding="utf-8")

    volume_outline = _find_volume_outline_file(project_root, chapter_num)
    if volume_outline is None:
        return f"⚠️ 大纲文件不存在：第 {chapter_num} 章"

    outline = _extract_outline_section(volume_outline.read_text(encoding="utf-8"), chapter_num)
    if outline is None:
        return f"⚠️ 未找到第 {chapter_num} 章的大纲"

    if max_chars and len(outline) > max_chars:
        return outline[:max_chars] + "\n...(已截断)"
    return outline
