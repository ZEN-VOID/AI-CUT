#!/usr/bin/env python3
"""Validate Story2026 planning output for monolith and decile-slice layouts."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any


LEGACY_REQUIRED_HOLOMAP_KEYS = [
    "story_promise",
    "genre_corridor",
    "story_spine",
    "timeline_axis",
    "space_axis",
    "episode_sequence_axis",
    "character_roster_projection",
    "relationship_graph_projection",
    "volume_boards",
    "chapter_boards",
    "conflict_threads",
    "mission_threads",
    "clue_threads",
    "foreshadow_threads",
    "cross_thread_indexes",
    "actualization",
    "state_transitions",
    "navigation_rules",
]

SPLIT_REQUIRED_HOLOMAP_KEYS = [
    "story_promise",
    "genre_corridor",
    "story_spine",
    "timeline_axis",
    "space_axis",
    "episode_sequence_axis",
    "episode_slice_manifest",
    "character_roster_projection",
    "relationship_graph_projection",
    "volume_boards",
    "conflict_threads",
    "mission_threads",
    "clue_threads",
    "foreshadow_threads",
    "cross_thread_indexes",
    "actualization",
    "state_transitions",
    "navigation_rules",
]

SPLIT_SLICE_REQUIRED_KEYS = [
    "slice_scope",
    "slice_style_contract",
    "chapter_boards",
    "episode_sequence_axis",
    "cross_chapter_continuity_matrix",
    "thread_window_slice",
    "foreshadow_silence_slice",
    "actualization",
]

VOLUME_BOARD_REQUIRED_FIELDS = [
    "volume_ref",
    "chapter_range",
    "core_function",
    "volume_promise",
    "wave_duty",
    "entry_promise",
    "exit_hook",
    "visual_climate",
    "action_grammar",
    "mystery_mode",
    "emotional_temperature",
    "scene_materials",
    "performance_axis",
    "taboo_writeups",
]

SLICE_STYLE_REQUIRED_FIELDS = [
    "contract_ref",
    "volume_ref",
    "volume_promise",
    "wave_duty",
    "entry_promise",
    "exit_hook",
    "visual_climate",
    "action_grammar",
    "mystery_mode",
    "emotional_temperature",
    "scene_materials",
    "performance_axis",
    "taboo_writeups",
]

CHAPTER_PLANNED_STATE_REQUIRED_FIELDS = [
    "chapter_promise",
    "entry_state",
    "carryover_threads",
    "expected_exit_delta",
    "character_focus",
    "relationship_focus",
]

CONTINUITY_MATRIX_REQUIRED_FIELDS = [
    "from_episode_ref",
    "to_episode_ref",
    "bridge_summary",
    "carryover_threads",
    "expected_shift",
]

PROHIBITED_ROOT_ACTUALIZATION_DETAIL_KEYS = [
    "episode_nodes",
    "clue_points",
    "foreshadow_points",
    "promise_threads",
    "suspense_threads",
    "tasklines",
    "threads",
]

SLICE_RANGE_FILENAME_RE = re.compile(r"^第(\d{3})-(\d{3})集\.json$")
SLICE_VOLUME_FILENAME_RE = re.compile(r"^第(\d+)卷\.json$")


def _load_json(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as f:
        data = json.load(f)
    if not isinstance(data, dict):
        raise SystemExit(f"顶层必须是 object: {path}")
    return data


def _extract_episode_num(value: Any) -> int | None:
    if isinstance(value, int):
        return value
    if not isinstance(value, str):
        return None
    match = re.search(r"(\d+)", value)
    if not match:
        return None
    return int(match.group(1))


def _validate_bundled_elements(board: dict[str, Any], errors: list[str], prefix: str) -> None:
    bundled = board.get("bundled_elements", {})
    if not isinstance(bundled, dict):
        errors.append(f"{prefix}.bundled_elements 必须是 object")
        return
    for key in ("events", "conflicts", "missions", "clues", "foreshadows", "characters"):
        if key not in bundled:
            errors.append(f"{prefix}.bundled_elements 缺少 {key}")


def _is_non_empty_value(value: Any) -> bool:
    if value is None:
        return False
    if isinstance(value, str):
        return bool(value.strip())
    if isinstance(value, list):
        return any(_is_non_empty_value(item) for item in value)
    if isinstance(value, dict):
        return bool(value)
    return True


def _validate_required_fields(
    payload: Any,
    required_fields: list[str],
    errors: list[str],
    prefix: str,
) -> None:
    if not isinstance(payload, dict):
        errors.append(f"{prefix} 必须是 object")
        return
    for field in required_fields:
        if field not in payload:
            errors.append(f"{prefix} 缺少 {field}")
            continue
        if not _is_non_empty_value(payload.get(field)):
            errors.append(f"{prefix}.{field} 不得为空")


def _validate_volume_boards(holomap: dict[str, Any], errors: list[str], *, strict: bool) -> None:
    volume_boards = holomap.get("volume_boards")
    if not isinstance(volume_boards, list) or not volume_boards:
        errors.append("volume_boards 必须为非空数组")
        return
    if not strict:
        return
    for idx, board in enumerate(volume_boards):
        _validate_required_fields(board, VOLUME_BOARD_REQUIRED_FIELDS, errors, f"volume_boards[{idx}]")


def _validate_chapter_board_planned_state(board: dict[str, Any], errors: list[str], prefix: str) -> None:
    planned_state = board.get("planned_state")
    _validate_required_fields(
        planned_state,
        CHAPTER_PLANNED_STATE_REQUIRED_FIELDS,
        errors,
        f"{prefix}.planned_state",
    )


def _validate_slice_style_contract(slice_content: dict[str, Any], errors: list[str], prefix: str, *, strict: bool) -> None:
    contract = slice_content.get("slice_style_contract")
    if not isinstance(contract, dict):
        errors.append(f"{prefix}.slice_style_contract 必须是 object")
        return
    if strict:
        _validate_required_fields(contract, SLICE_STYLE_REQUIRED_FIELDS, errors, f"{prefix}.slice_style_contract")


def _validate_continuity_matrix(slice_content: dict[str, Any], errors: list[str], prefix: str, *, strict: bool) -> None:
    matrix = slice_content.get("cross_chapter_continuity_matrix")
    if not isinstance(matrix, list) or not matrix:
        errors.append(f"{prefix}.cross_chapter_continuity_matrix 必须为非空数组")
        return
    if not strict:
        return
    for idx, entry in enumerate(matrix):
        _validate_required_fields(
            entry,
            CONTINUITY_MATRIX_REQUIRED_FIELDS,
            errors,
            f"{prefix}.cross_chapter_continuity_matrix[{idx}]",
        )


def _validate_legacy(data: dict[str, Any], strict: bool) -> list[str]:
    errors: list[str] = []

    if data.get("schema_version") != "story2026/story-map/v3":
        errors.append("schema_version 必须为 story2026/story-map/v3")

    meta = data.get("meta")
    if not isinstance(meta, dict):
        errors.append("缺少 meta object")
    elif meta.get("skill_id") != "story-plan":
        errors.append("meta.skill_id 必须为 story-plan")

    holomap = data.get("content", {}).get("holomap")
    if not isinstance(holomap, dict):
        errors.append("缺少 content.holomap object")
        return errors

    for key in LEGACY_REQUIRED_HOLOMAP_KEYS:
        if key not in holomap:
            errors.append(f"content.holomap 缺少 {key}")

    _validate_volume_boards(holomap, errors, strict=strict)

    chapter_boards = holomap.get("chapter_boards", [])
    if not isinstance(chapter_boards, list) or not chapter_boards:
        errors.append("chapter_boards 必须为非空数组")
    elif strict:
        for idx, board in enumerate(chapter_boards):
            if not isinstance(board, dict):
                errors.append(f"chapter_boards[{idx}] 必须是 object")
                continue
            _validate_bundled_elements(board, errors, f"chapter_boards[{idx}]")
            _validate_chapter_board_planned_state(board, errors, f"chapter_boards[{idx}]")

    if strict and not holomap.get("cross_thread_indexes"):
        errors.append("strict 模式要求 cross_thread_indexes 非空")

    return errors


def _validate_split(root_path: Path, data: dict[str, Any], strict: bool) -> list[str]:
    errors: list[str] = []

    if data.get("schema_version") != "story2026/story-map/v3":
        errors.append("split 模式下 schema_version 必须为 story2026/story-map/v3")

    meta = data.get("meta")
    if not isinstance(meta, dict):
        errors.append("缺少 meta object")
        return errors
    if meta.get("skill_id") != "story-plan":
        errors.append("meta.skill_id 必须为 story-plan")
    if meta.get("layout_mode") != "total-index-plus-deciles":
        errors.append("split 模式要求 meta.layout_mode = total-index-plus-deciles")

    holomap = data.get("content", {}).get("holomap")
    if not isinstance(holomap, dict):
        errors.append("缺少 content.holomap object")
        return errors

    for key in SPLIT_REQUIRED_HOLOMAP_KEYS:
        if key not in holomap:
            errors.append(f"split 模式下 content.holomap 缺少 {key}")

    _validate_volume_boards(holomap, errors, strict=strict)

    chapter_boards = holomap.get("chapter_boards")
    if chapter_boards not in (None, []):
        errors.append("split 模式下 root 不得再承载完整 chapter_boards；应改用 episode_slice_manifest + slices")

    actualization = holomap.get("actualization")
    if not isinstance(actualization, dict):
        errors.append("split 模式下 content.holomap.actualization 必须是 object")
    else:
        for key in PROHIBITED_ROOT_ACTUALIZATION_DETAIL_KEYS:
            if key in actualization and actualization.get(key):
                errors.append(f"split 模式下 root.actualization 不得承载明细字段 {key}")

    manifest = holomap.get("episode_slice_manifest")
    if not isinstance(manifest, list) or not manifest:
        errors.append("split 模式下 episode_slice_manifest 必须为非空数组")
        return errors

    root_dir = root_path.parent
    seen_episodes: set[int] = set()
    manifest_ids: dict[str, tuple[int, int, Path]] = {}
    ordered_ranges: list[tuple[int, int]] = []

    for idx, entry in enumerate(manifest):
        prefix = f"episode_slice_manifest[{idx}]"
        if not isinstance(entry, dict):
            errors.append(f"{prefix} 必须是 object")
            continue
        slice_id = entry.get("slice_id")
        start = entry.get("episode_start")
        end = entry.get("episode_end")
        file_ref = entry.get("file_ref")
        if not isinstance(slice_id, str):
            errors.append(f"{prefix}.slice_id 必须是 string")
        if not isinstance(start, int) or not isinstance(end, int):
            errors.append(f"{prefix}.episode_start / episode_end 必须是 int")
            continue
        if start > end:
            errors.append(f"{prefix} 的 episode_start 不能大于 episode_end")
            continue
        if not isinstance(file_ref, str):
            errors.append(f"{prefix}.file_ref 必须是 string")
            continue
        filename = Path(file_ref).name
        range_match = SLICE_RANGE_FILENAME_RE.match(filename)
        volume_match = SLICE_VOLUME_FILENAME_RE.match(filename)
        if range_match:
            name_start = int(range_match.group(1))
            name_end = int(range_match.group(2))
            if (name_start, name_end) != (start, end):
                errors.append(f"{prefix}.file_ref 与 episode range 不一致")
        elif volume_match:
            volume_num = int(volume_match.group(1))
            expected_volume = ((start - 1) // 10) + 1
            if volume_num != expected_volume:
                errors.append(f"{prefix}.file_ref 与卷号不一致，期望第{expected_volume}卷.json")
        else:
            errors.append(f"{prefix}.file_ref 命名不合法，应为 第N卷.json（或 legacy 第001-010集.json）")
            continue

        slice_path = (root_dir / file_ref).resolve()
        manifest_ids[slice_id] = (start, end, slice_path)
        ordered_ranges.append((start, end))

        for episode in range(start, end + 1):
            if episode in seen_episodes:
                errors.append(f"{prefix} 与其他 slice 存在 episode {episode} 重叠")
            seen_episodes.add(episode)

        if not slice_path.exists():
            errors.append(f"{prefix}.file_ref 指向的 slice 文件不存在: {slice_path}")
            continue

        slice_data = _load_json(slice_path)
        if slice_data.get("schema_version") != "story2026/story-map-slice/v1":
            errors.append(f"{slice_path.name} 的 schema_version 必须为 story2026/story-map-slice/v1")
        slice_content = slice_data.get("content", {}).get("holomap_slice")
        if not isinstance(slice_content, dict):
            errors.append(f"{slice_path.name} 缺少 content.holomap_slice")
            continue

        for key in SPLIT_SLICE_REQUIRED_KEYS:
            if key not in slice_content:
                errors.append(f"{slice_path.name}.content.holomap_slice 缺少 {key}")

        _validate_slice_style_contract(slice_content, errors, f"{slice_path.name}.content.holomap_slice", strict=strict)
        _validate_continuity_matrix(slice_content, errors, f"{slice_path.name}.content.holomap_slice", strict=strict)

        slice_scope = slice_content.get("slice_scope")
        if isinstance(slice_scope, dict):
            if slice_scope.get("slice_id") != slice_id:
                errors.append(f"{slice_path.name}.slice_scope.slice_id 与 manifest 不一致")
            if slice_scope.get("episode_start") != start or slice_scope.get("episode_end") != end:
                errors.append(f"{slice_path.name}.slice_scope episode range 与 manifest 不一致")

        slice_axis = slice_content.get("episode_sequence_axis")
        if not isinstance(slice_axis, list) or not slice_axis:
            errors.append(f"{slice_path.name}.episode_sequence_axis 必须为非空数组")
        else:
            for axis_entry in slice_axis:
                if not isinstance(axis_entry, dict):
                    errors.append(f"{slice_path.name}.episode_sequence_axis[] 必须是 object")
                    continue
                if axis_entry.get("slice_ref") != slice_id:
                    errors.append(f"{slice_path.name}.episode_sequence_axis[].slice_ref 必须回指 {slice_id}")

        slice_boards = slice_content.get("chapter_boards")
        if not isinstance(slice_boards, list) or not slice_boards:
            errors.append(f"{slice_path.name}.chapter_boards 必须为非空数组")
        else:
            for board_idx, board in enumerate(slice_boards):
                if not isinstance(board, dict):
                    errors.append(f"{slice_path.name}.chapter_boards[{board_idx}] 必须是 object")
                    continue
                episode_ref = board.get("episode_ref")
                episode_num = _extract_episode_num(episode_ref)
                if episode_num is not None and not (start <= episode_num <= end):
                    errors.append(
                        f"{slice_path.name}.chapter_boards[{board_idx}].episode_ref={episode_ref} 超出 manifest range"
                    )
                if strict:
                    _validate_bundled_elements(
                        board,
                        errors,
                        f"{slice_path.name}.chapter_boards[{board_idx}]",
                    )
                    _validate_chapter_board_planned_state(
                        board,
                        errors,
                        f"{slice_path.name}.chapter_boards[{board_idx}]",
                    )

    if ordered_ranges:
        ordered_ranges.sort()
        expected = ordered_ranges[0][0]
        for start, end in ordered_ranges:
            if start != expected:
                errors.append(f"slice coverage 不连续：期望从 episode {expected} 开始，实际从 {start} 开始")
                expected = start
            expected = end + 1

    root_axis = holomap.get("episode_sequence_axis")
    if not isinstance(root_axis, list) or not root_axis:
        errors.append("split 模式下 root.episode_sequence_axis 必须为非空数组")
    else:
        for idx, axis_entry in enumerate(root_axis):
            if not isinstance(axis_entry, dict):
                errors.append(f"root episode_sequence_axis[{idx}] 必须是 object")
                continue
            slice_ref = axis_entry.get("slice_ref")
            if slice_ref not in manifest_ids:
                errors.append(f"root episode_sequence_axis[{idx}].slice_ref 未命中 manifest")
                continue
            episode_num = _extract_episode_num(axis_entry.get("episode_ref"))
            if episode_num is not None:
                start, end, _ = manifest_ids[slice_ref]
                if not (start <= episode_num <= end):
                    errors.append(
                        f"root episode_sequence_axis[{idx}] 的 episode_ref 不在 slice_ref={slice_ref} 的区间内"
                    )

    if strict and not holomap.get("cross_thread_indexes"):
        errors.append("strict 模式要求 cross_thread_indexes 非空")

    return errors


def _validate(path: Path, strict: bool) -> list[str]:
    data = _load_json(path)
    meta = data.get("meta", {})
    layout_mode = meta.get("layout_mode") if isinstance(meta, dict) else None
    if layout_mode == "total-index-plus-deciles":
        return _validate_split(path, data, strict=strict)
    return _validate_legacy(data, strict=strict)


def main() -> None:
    parser = argparse.ArgumentParser(description="Validate Story2026 story_map output")
    parser.add_argument("path", help="Path to 2-Planning/全息地图.json")
    parser.add_argument("--strict", action="store_true", help="Require non-empty thread indexes")
    args = parser.parse_args()

    target_path = Path(args.path).resolve()
    errors = _validate(target_path, strict=args.strict)
    if errors:
        for err in errors:
            print(f"FAIL: {err}")
        raise SystemExit(1)

    print("PASS: story_map output structure is valid")


if __name__ == "__main__":
    main()
