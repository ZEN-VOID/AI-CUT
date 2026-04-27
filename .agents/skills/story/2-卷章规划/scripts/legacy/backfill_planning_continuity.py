#!/usr/bin/env python3
"""Legacy compatibility tool for old holomap + slice planning continuity backfill.

This script only serves projects still using `2-卷章规划/全息地图.json` +
`卷分片/*.json` as compatibility carriers.
"""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[6]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Backfill legacy holomap planning continuity fields for a story project"
    )
    parser.add_argument("project_root", help="Path to projects/story/<项目名> (legacy `projects/aigc/<项目名>` also supported)")
    parser.add_argument(
        "--write",
        action="store_true",
        help="Persist changes; default is dry-run preview",
    )
    return parser.parse_args()


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def dump_json(path: Path, payload: dict[str, Any]) -> None:
    path.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )


def shorten(text: str, limit: int = 54) -> str:
    text = re.sub(r"\s+", " ", text).strip()
    for sep in ("；", "。", "，"):
        if sep in text:
            text = text.split(sep, 1)[0].strip()
            break
    if len(text) <= limit:
        return text
    return text[: limit - 1].rstrip() + "…"


def safe_list(value: Any) -> list[Any]:
    if value is None:
        return []
    if isinstance(value, list):
        return value
    return [value]


def title_map(holomap: dict[str, Any]) -> dict[str, dict[str, str]]:
    buckets = [
        "conflict_threads",
        "mission_threads",
        "clue_threads",
        "foreshadow_threads",
    ]
    result: dict[str, dict[str, str]] = {}
    for bucket in buckets:
        for item in holomap.get(bucket, []):
            thread_id = item.get("thread_id")
            if not thread_id:
                continue
            result[thread_id] = {
                "thread_id": thread_id,
                "thread_type": item.get("thread_type", bucket.removesuffix("_threads")),
                "title": item.get("title", ""),
                "pressure": item.get("pressure")
                or item.get("surface_goal")
                or item.get("carrier")
                or item.get("service_domain")
                or "",
            }
    return result


def derive_wave_duty(volume_board: dict[str, Any]) -> str:
    return (
        volume_board.get("wave_duty")
        or volume_board.get("core_function")
        or volume_board.get("emotional_duty")
        or ""
    )


def derive_entry_promise(volume_board: dict[str, Any]) -> str:
    if volume_board.get("entry_promise"):
        return volume_board["entry_promise"]
    emotional = volume_board.get("emotional_duty", "")
    performance = shorten(str(volume_board.get("performance_axis", "")), 42)
    if emotional and performance:
        return f"卷首先兑现“{emotional}”，并以{performance}把本卷主线正式推开。"
    if performance:
        return f"卷首必须以{performance}起盘。"
    return f"卷首必须先把{shorten(str(volume_board.get('core_function', '本卷主线')))}落成当前行动压力。"


def derive_exit_hook(
    volume_board: dict[str, Any], next_volume_board: dict[str, Any] | None
) -> str:
    if volume_board.get("exit_hook"):
        return volume_board["exit_hook"]
    end_episode = safe_list(volume_board.get("episode_range"))
    end_label = f"第{end_episode[-1]}集" if end_episode else "卷末"
    if next_volume_board:
        next_title = next_volume_board.get("title", "下一卷")
        next_core = shorten(str(next_volume_board.get("core_function", "下一轮主线压力")), 36)
        return f"{end_label}必须把战线推到《{next_title}》，并留下{next_core}的入口。"
    return f"{end_label}必须留下下一轮主线升级入口。"


def mirror_slice_style_contract(
    slice_contract: dict[str, Any],
    volume_board: dict[str, Any],
    next_volume_board: dict[str, Any] | None,
) -> dict[str, Any]:
    updated = dict(slice_contract)
    updated["contract_ref"] = updated.get("contract_ref") or f"volume:{volume_board.get('volume_ref', '')}"
    updated["volume_ref"] = updated.get("volume_ref") or volume_board.get("volume_ref", "")
    updated["volume_promise"] = updated.get("volume_promise") or volume_board.get("volume_promise", "")
    updated["wave_duty"] = updated.get("wave_duty") or derive_wave_duty(volume_board)
    updated["entry_promise"] = updated.get("entry_promise") or derive_entry_promise(volume_board)
    updated["exit_hook"] = updated.get("exit_hook") or derive_exit_hook(volume_board, next_volume_board)
    updated["visual_climate"] = updated.get("visual_climate") or volume_board.get("visual_climate", "")
    updated["action_grammar"] = updated.get("action_grammar") or volume_board.get("action_grammar", "")
    updated["mystery_mode"] = updated.get("mystery_mode") or volume_board.get("mystery_mode", "")
    updated["emotional_temperature"] = updated.get("emotional_temperature") or volume_board.get(
        "emotional_temperature", ""
    )
    updated["scene_materials"] = safe_list(updated.get("scene_materials") or volume_board.get("scene_materials"))
    updated["performance_axis"] = updated.get("performance_axis") or volume_board.get("performance_axis", "")
    updated["taboo_writeups"] = safe_list(updated.get("taboo_writeups") or volume_board.get("taboo_writeups"))
    return updated


def _thread_ids(board: dict[str, Any], key: str) -> list[str]:
    elements = board.get("bundled_elements", {})
    if not isinstance(elements, dict):
        return []
    values = safe_list(elements.get(key))
    result: list[str] = []
    for value in values:
        if isinstance(value, dict):
            thread_id = value.get("thread_id") or value.get("ref") or value.get("id")
        else:
            thread_id = value
        if isinstance(thread_id, str) and thread_id:
            result.append(thread_id)
    return result


def _relationship_focus(board: dict[str, Any]) -> dict[str, Any]:
    planned_state = board.get("planned_state")
    if not isinstance(planned_state, dict):
        return {}
    focus = planned_state.get("relationship_focus")
    return focus if isinstance(focus, dict) else {}


def chapter_promise(board: dict[str, Any]) -> str:
    promise = board.get("planned_state", {}).get("chapter_promise")
    if isinstance(promise, str) and promise.strip():
        return promise.strip()

    event_values = safe_list(board.get("bundled_elements", {}).get("events"))
    conflict_values = safe_list(board.get("bundled_elements", {}).get("conflicts"))
    event_text = shorten(str(event_values[0]), 28) if event_values else "当前主推进"
    conflict_text = shorten(str(conflict_values[0]), 18) if conflict_values else "当前代价"
    return f"本章要让{event_text}与{conflict_text}同时被看见。"


def entry_state(board: dict[str, Any]) -> dict[str, Any]:
    planned_state = board.get("planned_state")
    if not isinstance(planned_state, dict):
        planned_state = {}
    if isinstance(planned_state.get("entry_state"), dict) and planned_state["entry_state"]:
        return planned_state["entry_state"]

    character_focus = planned_state.get("character_focus")
    lead = ""
    if isinstance(character_focus, dict):
        lead = str(character_focus.get("lead") or character_focus.get("character_id") or "").strip()
    if not lead:
        bundled_characters = safe_list(board.get("bundled_elements", {}).get("characters"))
        if bundled_characters:
            lead = str(bundled_characters[0])

    return {
        "lead_character": lead or "待定主视角",
        "pressure": shorten(
            str(board.get("bundled_elements", {}).get("conflicts", ["当前主压强"])[0]),
            24,
        ),
    }


def carryover_threads(board: dict[str, Any], lookup: dict[str, dict[str, str]]) -> list[dict[str, str]]:
    existing = board.get("planned_state", {}).get("carryover_threads")
    if isinstance(existing, list) and existing:
        return existing

    result: list[dict[str, str]] = []
    for key in ("missions", "conflicts", "clues", "foreshadows"):
        for thread_id in _thread_ids(board, key):
            info = lookup.get(thread_id, {"thread_id": thread_id, "thread_type": key.rstrip("s"), "title": ""})
            result.append(
                {
                    "thread_id": thread_id,
                    "thread_type": info.get("thread_type", key.rstrip("s")),
                    "summary": shorten(info.get("pressure") or info.get("title") or thread_id, 36),
                }
            )
    if not result:
        result.append(
            {
                "thread_id": "thread:chapter-line",
                "thread_type": "chapter",
                "summary": shorten(chapter_promise(board), 36),
            }
        )
    return result


def expected_exit_delta(board: dict[str, Any]) -> dict[str, Any]:
    planned_state = board.get("planned_state")
    if not isinstance(planned_state, dict):
        planned_state = {}
    if isinstance(planned_state.get("expected_exit_delta"), dict) and planned_state["expected_exit_delta"]:
        return planned_state["expected_exit_delta"]

    mission_ids = _thread_ids(board, "missions")
    conflict_ids = _thread_ids(board, "conflicts")
    return {
        "pressure_up": shorten(
            str(board.get("bundled_elements", {}).get("conflicts", ["当前冲突继续升级"])[0]),
            24,
        ),
        "mission_carryover": mission_ids,
        "conflict_carryover": conflict_ids,
    }


def ensure_relationship_focus(board: dict[str, Any]) -> dict[str, Any]:
    focus = _relationship_focus(board)
    if focus:
        return focus
    return {"edge_refs": []}


def continuity_bridge(current_board: dict[str, Any], next_board: dict[str, Any]) -> dict[str, Any]:
    current_episode = current_board.get("episode_ref", "")
    next_episode = next_board.get("episode_ref", "")
    current_exit = expected_exit_delta(current_board)
    next_entry = entry_state(next_board)
    carryover = carryover_threads(current_board, {})
    bridge_summary = (
        f"{current_episode}把“{shorten(str(current_exit.get('pressure_up', '当前压强')), 24)}”"
        f"带入{next_episode}，使其以“{shorten(str(next_entry.get('pressure', '下一章压力')), 24)}”起盘。"
    )
    return {
        "from_episode_ref": current_episode,
        "to_episode_ref": next_episode,
        "bridge_summary": bridge_summary,
        "carryover_threads": carryover,
        "expected_shift": shorten(str(current_exit.get("pressure_up", "当前压强继续升级")), 32),
    }


def enrich_chapter_boards(chapter_boards: list[dict[str, Any]], lookup: dict[str, dict[str, str]]) -> None:
    for index, board in enumerate(chapter_boards):
        if not isinstance(board, dict):
            continue
        planned_state = board.setdefault("planned_state", {})
        planned_state["chapter_promise"] = chapter_promise(board)
        planned_state["entry_state"] = entry_state(board)
        planned_state["carryover_threads"] = carryover_threads(board, lookup)
        planned_state["expected_exit_delta"] = expected_exit_delta(board)
        planned_state["relationship_focus"] = ensure_relationship_focus(board)
        if "character_focus" not in planned_state or not isinstance(planned_state["character_focus"], dict):
            bundled_characters = safe_list(board.get("bundled_elements", {}).get("characters"))
            planned_state["character_focus"] = {
                "lead": str(bundled_characters[0]) if bundled_characters else "待定主视角"
            }
        board.setdefault("rhythm_role", {"duty": "carry", "reason": f"承接章节 {index + 1} 的推进压力"})


def enrich_volume_boards(holomap: dict[str, Any]) -> None:
    volume_boards = holomap.get("volume_boards", [])
    for index, board in enumerate(volume_boards):
        if not isinstance(board, dict):
            continue
        board["wave_duty"] = board.get("wave_duty") or derive_wave_duty(board) or "carry"
        board["entry_promise"] = board.get("entry_promise") or derive_entry_promise(board)
        next_board = volume_boards[index + 1] if index + 1 < len(volume_boards) else None
        if isinstance(next_board, dict):
            board["exit_hook"] = board.get("exit_hook") or derive_exit_hook(board, next_board)


def enrich_slice(
    slice_payload: dict[str, Any],
    volume_board: dict[str, Any],
    next_volume_board: dict[str, Any] | None,
    lookup: dict[str, dict[str, str]],
) -> None:
    holomap_slice = slice_payload["content"]["holomap_slice"]
    holomap_slice["slice_style_contract"] = mirror_slice_style_contract(
        holomap_slice.get("slice_style_contract", {}),
        volume_board,
        next_volume_board,
    )

    chapter_boards = holomap_slice.get("chapter_boards", [])
    if not isinstance(chapter_boards, list):
        return

    enrich_chapter_boards(chapter_boards, lookup)

    continuity_matrix = []
    for idx in range(len(chapter_boards) - 1):
        current = chapter_boards[idx]
        nxt = chapter_boards[idx + 1]
        if not isinstance(current, dict) or not isinstance(nxt, dict):
            continue
        continuity_matrix.append(continuity_bridge(current, nxt))
    holomap_slice["cross_chapter_continuity_matrix"] = continuity_matrix


def main() -> int:
    args = parse_args()
    project_root = Path(args.project_root).expanduser().resolve()
    planning_root_path = project_root / "2-卷章规划" / "全息地图.json"
    planning_root = load_json(planning_root_path)
    holomap = planning_root["content"]["holomap"]
    enrich_volume_boards(holomap)

    thread_lookup = title_map(holomap)
    board_lookup = {
        str(board.get("volume_ref")): board
        for board in holomap.get("volume_boards", [])
        if isinstance(board, dict)
    }
    manifest = holomap.get("episode_slice_manifest", [])
    changed_paths = [planning_root_path]

    for idx, entry in enumerate(manifest):
        if not isinstance(entry, dict):
            continue
        file_ref = str(entry.get("file_ref", ""))
        slice_path = project_root / "2-卷章规划" / file_ref
        if not slice_path.exists():
            alt_path = project_root / "2-卷章规划" / "卷分片" / Path(file_ref).name
            slice_path = alt_path
        if not slice_path.exists():
            raise FileNotFoundError(f"slice file missing: {file_ref}")
        slice_payload = load_json(slice_path)
        volume_ref = ""
        contract_ref = (
            slice_payload.get("content", {})
            .get("holomap_slice", {})
            .get("slice_style_contract", {})
            .get("volume_ref")
        )
        if isinstance(contract_ref, str) and contract_ref:
            volume_ref = contract_ref
        if not volume_ref:
            slice_scope = slice_payload["content"]["holomap_slice"].get("slice_scope", {})
            start = slice_scope.get("episode_start")
            if isinstance(start, int):
                volume_ref = next(
                    (
                        board.get("volume_ref", "")
                        for board in holomap.get("volume_boards", [])
                        if isinstance(board, dict)
                        and safe_list(board.get("episode_range"))
                        and safe_list(board.get("episode_range"))[0] <= start <= safe_list(board.get("episode_range"))[-1]
                    ),
                    "",
                )
        volume_board = board_lookup.get(volume_ref)
        if not isinstance(volume_board, dict):
            raise ValueError(f"cannot resolve volume board for {slice_path}")
        boards = holomap.get("volume_boards", [])
        next_volume_board = None
        for board_idx, candidate in enumerate(boards):
            if candidate is volume_board and board_idx + 1 < len(boards):
                next_volume_board = boards[board_idx + 1]
                break
        enrich_slice(slice_payload, volume_board, next_volume_board, thread_lookup)
        if args.write:
            dump_json(slice_path, slice_payload)
        changed_paths.append(slice_path)

    if args.write:
        dump_json(planning_root_path, planning_root)

    mode = "WRITE" if args.write else "DRY-RUN"
    for path in changed_paths:
        print(f"{mode}: {path.relative_to(project_root)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
