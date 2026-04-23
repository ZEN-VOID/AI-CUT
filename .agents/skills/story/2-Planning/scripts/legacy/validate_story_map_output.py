#!/usr/bin/env python3
"""Validate legacy Story2026 holomap planning output for monolith and decile-slice layouts."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


ROOT_REQUIRED_FIELDS = [
    "story_promise",
    "genre_corridor",
    "story_spine",
    "timeline_axis",
    "space_axis",
    "episode_sequence_axis",
    "character_roster_projection",
    "relationship_graph_projection",
    "volume_boards",
    "conflict_threads",
    "mission_threads",
    "clue_threads",
    "foreshadow_threads",
    "actualization",
    "state_transitions",
    "navigation_rules",
]

SLICE_REQUIRED_FIELDS = [
    "slice_scope",
    "slice_style_contract",
    "chapter_boards",
    "episode_sequence_axis",
    "cross_chapter_continuity_matrix",
    "thread_window_slice",
    "foreshadow_silence_slice",
    "actualization",
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

CONTINUITY_REQUIRED_FIELDS = [
    "from_episode_ref",
    "to_episode_ref",
    "bridge_summary",
    "carryover_threads",
    "expected_shift",
]

BOARD_REQUIRED_FIELDS = [
    "node_id",
    "episode_ref",
    "bundled_elements",
    "planned_state",
]

PLANNED_STATE_REQUIRED_FIELDS = [
    "chapter_promise",
    "entry_state",
    "carryover_threads",
    "expected_exit_delta",
    "character_focus",
    "relationship_focus",
]

VOLUME_BOARD_REQUIRED_FIELDS = [
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


def _load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def _chapter_number_from_ref(value: str) -> int | None:
    if not isinstance(value, str):
        return None
    digits = "".join(ch for ch in value if ch.isdigit())
    if not digits:
        return None
    return int(digits)


def _validate_required_fields(obj: dict[str, Any], fields: list[str], errors: list[str], prefix: str) -> None:
    for field in fields:
        if field not in obj:
            errors.append(f"{prefix} 缺少 {field}")


def _validate_non_empty(value: Any, errors: list[str], prefix: str) -> None:
    if value in (None, "", [], {}):
        errors.append(f"{prefix} 不得为空")


def _validate_planned_state(planned_state: dict[str, Any], errors: list[str], prefix: str, *, strict: bool) -> None:
    if not isinstance(planned_state, dict):
        errors.append(f"{prefix}.planned_state 必须是 object")
        return
    if strict:
        _validate_required_fields(planned_state, PLANNED_STATE_REQUIRED_FIELDS, errors, f"{prefix}.planned_state")
        for field in PLANNED_STATE_REQUIRED_FIELDS:
            _validate_non_empty(planned_state.get(field), errors, f"{prefix}.planned_state.{field}")


def _validate_board(board: dict[str, Any], errors: list[str], prefix: str, *, strict: bool) -> None:
    _validate_required_fields(board, BOARD_REQUIRED_FIELDS, errors, prefix)
    bundled = board.get("bundled_elements")
    if not isinstance(bundled, dict):
        errors.append(f"{prefix}.bundled_elements 必须是 object")
    if strict:
        _validate_non_empty(board.get("node_id"), errors, f"{prefix}.node_id")
        _validate_non_empty(board.get("episode_ref"), errors, f"{prefix}.episode_ref")
        _validate_planned_state(board.get("planned_state"), errors, prefix, strict=strict)


def _validate_volume_boards(holomap: dict[str, Any], errors: list[str], *, strict: bool) -> None:
    volume_boards = holomap.get("volume_boards")
    if not isinstance(volume_boards, list) or not volume_boards:
        errors.append("content.holomap.volume_boards 必须为非空数组")
        return
    for idx, board in enumerate(volume_boards):
        if not isinstance(board, dict):
            errors.append(f"content.holomap.volume_boards[{idx}] 必须是 object")
            continue
        if strict:
            _validate_required_fields(
                board,
                VOLUME_BOARD_REQUIRED_FIELDS,
                errors,
                f"content.holomap.volume_boards[{idx}]",
            )
            for field in VOLUME_BOARD_REQUIRED_FIELDS:
                _validate_non_empty(board.get(field), errors, f"content.holomap.volume_boards[{idx}].{field}")


def _validate_slice_style_contract(slice_content: dict[str, Any], errors: list[str], prefix: str, *, strict: bool) -> None:
    contract = slice_content.get("slice_style_contract")
    if not isinstance(contract, dict):
        errors.append(f"{prefix}.slice_style_contract 必须是 object")
        return
    if strict:
        _validate_required_fields(contract, SLICE_STYLE_REQUIRED_FIELDS, errors, f"{prefix}.slice_style_contract")
        for field in SLICE_STYLE_REQUIRED_FIELDS:
            _validate_non_empty(contract.get(field), errors, f"{prefix}.slice_style_contract.{field}")


def _validate_continuity_matrix(slice_content: dict[str, Any], errors: list[str], prefix: str, *, strict: bool) -> None:
    matrix = slice_content.get("cross_chapter_continuity_matrix")
    if not isinstance(matrix, list):
        errors.append(f"{prefix}.cross_chapter_continuity_matrix 必须是数组")
        return
    if strict and not matrix:
        errors.append(f"{prefix}.cross_chapter_continuity_matrix 不得为空")
        return
    for idx, row in enumerate(matrix):
        if not isinstance(row, dict):
            errors.append(f"{prefix}.cross_chapter_continuity_matrix[{idx}] 必须是 object")
            continue
        if strict:
            _validate_required_fields(
                row,
                CONTINUITY_REQUIRED_FIELDS,
                errors,
                f"{prefix}.cross_chapter_continuity_matrix[{idx}]",
            )
            for field in CONTINUITY_REQUIRED_FIELDS:
                _validate_non_empty(
                    row.get(field),
                    errors,
                    f"{prefix}.cross_chapter_continuity_matrix[{idx}].{field}",
                )


def _validate_monolith(data: dict[str, Any], errors: list[str], *, strict: bool) -> None:
    holomap = data.get("content", {}).get("holomap")
    if not isinstance(holomap, dict):
        errors.append("缺少 content.holomap object")
        return
    for key in ROOT_REQUIRED_FIELDS:
        if key not in holomap:
            errors.append(f"content.holomap 缺少 {key}")

    _validate_volume_boards(holomap, errors, strict=strict)

    chapter_boards = holomap.get("chapter_boards", [])
    if strict and (not isinstance(chapter_boards, list) or not chapter_boards):
        errors.append("monolith 模式下 chapter_boards 必须为非空数组")
    if isinstance(chapter_boards, list):
        for idx, board in enumerate(chapter_boards):
            if not isinstance(board, dict):
                errors.append(f"content.holomap.chapter_boards[{idx}] 必须是 object")
                continue
            _validate_board(board, errors, f"content.holomap.chapter_boards[{idx}]", strict=strict)

    if strict and not holomap.get("cross_thread_indexes"):
        errors.append("strict 模式下 content.holomap.cross_thread_indexes 不得为空")


def _validate(path: Path, *, strict: bool = False) -> list[str]:
    data = _load_json(path)
    errors: list[str] = []
    layout_mode = data.get("meta", {}).get("layout_mode")

    if layout_mode != "total-index-plus-deciles":
        _validate_monolith(data, errors, strict=strict)
        return errors

    holomap = data.get("content", {}).get("holomap")
    if not isinstance(holomap, dict):
        errors.append("缺少 content.holomap object")
        return errors

    for key in ROOT_REQUIRED_FIELDS:
        if key not in holomap:
            errors.append(f"split 模式下 content.holomap 缺少 {key}")

    _validate_volume_boards(holomap, errors, strict=strict)

    chapter_boards = holomap.get("chapter_boards")
    if chapter_boards not in (None, []):
        errors.append("split 模式下 root 不得再承载完整 chapter_boards；应改用 episode_slice_manifest + slices")

    actualization = holomap.get("actualization")
    if not isinstance(actualization, dict):
        errors.append("split 模式下 content.holomap.actualization 必须是 object")

    manifest = holomap.get("episode_slice_manifest")
    if not isinstance(manifest, list) or not manifest:
        errors.append("split 模式下 episode_slice_manifest 必须为非空数组")
        return errors

    manifest_ids: dict[str, tuple[int, int, Path]] = {}
    covered_episodes: set[int] = set()
    root_dir = path.parent

    for idx, entry in enumerate(manifest):
        if not isinstance(entry, dict):
            errors.append(f"episode_slice_manifest[{idx}] 必须是 object")
            continue
        prefix = f"episode_slice_manifest[{idx}]"
        slice_id = entry.get("slice_id")
        start = entry.get("episode_start")
        end = entry.get("episode_end")
        file_ref = entry.get("file_ref")
        if not isinstance(slice_id, str):
            errors.append(f"{prefix}.slice_id 必须是 string")
            continue
        if not isinstance(start, int) or not isinstance(end, int):
            errors.append(f"{prefix}.episode_start / episode_end 必须是 int")
            continue
        if start > end:
            errors.append(f"{prefix}.episode_start 不得大于 episode_end")
            continue
        if not isinstance(file_ref, str):
            errors.append(f"{prefix}.file_ref 必须是 string")
            continue

        slice_path = (root_dir / file_ref).resolve()
        manifest_ids[slice_id] = (start, end, slice_path)
        for episode in range(start, end + 1):
            if episode in covered_episodes:
                errors.append(f"{prefix} 与其他 slice 存在 episode {episode} 重叠")
            covered_episodes.add(episode)

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
        for key in SLICE_REQUIRED_FIELDS:
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
            board_chapter_numbers: list[int] = []
            for board_idx, board in enumerate(slice_boards):
                if not isinstance(board, dict):
                    errors.append(f"{slice_path.name}.chapter_boards[{board_idx}] 必须是 object")
                    continue
                episode_ref = board.get("episode_ref")
                number = _chapter_number_from_ref(episode_ref) if isinstance(episode_ref, str) else None
                if number is not None:
                    board_chapter_numbers.append(number)
                    if number < start or number > end:
                        errors.append(
                            f"{slice_path.name}.chapter_boards[{board_idx}].episode_ref={episode_ref} 超出 manifest range"
                        )

                _validate_board(
                    board,
                    errors,
                    f"{slice_path.name}.chapter_boards[{board_idx}]",
                    strict=strict,
                )

            if board_chapter_numbers:
                board_chapter_numbers = sorted(set(board_chapter_numbers))
                expected = start
                if board_chapter_numbers[0] != expected:
                    errors.append(f"slice coverage 不连续：期望从 episode {expected} 开始，实际从 {board_chapter_numbers[0]} 开始")

    root_axis = holomap.get("episode_sequence_axis")
    if not isinstance(root_axis, list) or not root_axis:
        errors.append("root episode_sequence_axis 必须为非空数组")
    else:
        for idx, axis_entry in enumerate(root_axis):
            if not isinstance(axis_entry, dict):
                errors.append(f"root episode_sequence_axis[{idx}] 必须是 object")
                continue
            slice_ref = axis_entry.get("slice_ref")
            if slice_ref not in manifest_ids:
                errors.append(f"root episode_sequence_axis[{idx}].slice_ref 未命中 manifest")
                continue
            episode_ref = axis_entry.get("episode_ref")
            number = _chapter_number_from_ref(episode_ref) if isinstance(episode_ref, str) else None
            if number is not None:
                start, end, _ = manifest_ids[slice_ref]
                if number < start or number > end:
                    errors.append(f"root episode_sequence_axis[{idx}] 的 episode_ref 不在 slice_ref={slice_ref} 的区间内")

    if strict and not holomap.get("cross_thread_indexes"):
        errors.append("strict 模式下 content.holomap.cross_thread_indexes 不得为空")

    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate legacy Story2026 holomap output")
    parser.add_argument("path", help="Path to legacy 2-Planning/全息地图.json")
    parser.add_argument("--strict", action="store_true", help="Enable strict validation")
    args = parser.parse_args()

    path = Path(args.path).expanduser().resolve()
    errors = _validate(path, strict=args.strict)
    if errors:
        for error in errors:
            print(error)
        return 1

    print("PASS: legacy story_map output structure is valid")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
