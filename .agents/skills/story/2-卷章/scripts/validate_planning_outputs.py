#!/usr/bin/env python3
"""Validate story planning markdown outputs for the new fractal planning layout."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path


BOOK_REQUIRED = [
    "书名：",
    "整体故事大纲：",
    "故事编年史：",
    "- `chronology_axis`：",
    "  - `prehistory_events`：",
    "  - `main_story_start`：",
    "  - `volume_time_spans`：",
    "  - `causal_milestones`：",
    "  - `hidden_events`：",
    "  - `end_state`：",
    "卷划分：",
    "整部任务关系：",
    "- 主任务树：",
    "- 卷级支流簇：",
    "- 关键汇聚里程碑：",
    "整体冲突：",
    "整部悬念总设计：",
    "- 核心真相/核心谜面：",
    "- 整书悬念池：",
    "  - `suspense_id`：",
    "  - `suspense_name`：",
    "  - `suspense_type`：",
    "  - `priority`：",
    "  - `status`：",
    "  - `owner_level`：",
    "  - `reveal_window`：",
    "  - `dependency`：",
    "  - `reader_state`：",
    "  - `pov_state`：",
    "  - `next_action`：",
    "- 读者认知曲线：",
    "- 主角认知曲线：",
    "- 卷级揭秘节奏：",
    "- 长线误导策略：",
    "- 多重悬念编排规则：",
    "- 禁止提前揭露：",
    "- 终局回收要求：",
    "整体节奏曲线：",
    "- 长线 promise 走廊：",
    "- 长线升压走廊：",
    "- 卷职责分配：",
    "- 节奏高点说明：",
    "- `book_wave_map`：",
    "  - `volume_intensity_map`：",
    "  - `volume_role_map`：",
    "  - `respite_corridor`：",
    "  - `payoff_distribution`：",
    "规避：",
]
VOLUME_REQUIRED = [
    "卷标题：",
    "本卷故事大纲：",
    "本卷时间线：",
    "- `volume_time_span`：",
    "- `chapter_chronology`：",
    "- `parallel_hidden_events`：",
    "- `time_jumps_or_compression`：",
    "- `volume_end_state`：",
    "章划分：",
    "本卷冲突：",
    "本卷悬念开关：",
    "- 上承整部悬念：",
    "- 本卷新增悬念：",
    "- 本卷悬念线程表：",
    "  - `suspense_id`：",
    "  - `priority`：",
    "  - `status`：",
    "  - `reveal_window`：",
    "  - `dependency`：",
    "  - `reader_state`：",
    "  - `pov_state`：",
    "  - `next_action`：",
    "- 本卷需要隐藏的：",
    "- 本卷允许露出的：",
    "- 本卷误导/疑阵：",
    "- 本卷揭秘的：",
    "- 延后到后续卷/章的：",
    "- 本卷悬念负载：",
    "- 对章级规划的约束：",
    "本卷节奏曲线：",
    "- 本卷 promise：",
    "- 六拍职责：",
    "- 章节职责分配：",
    "- `volume_orchestration_map`：",
    "  - `chapter_payoff_map`：",
    "  - `chapter_intensity_map`：",
    "  - `respite_chapters`：",
    "  - `pressure_chapters`：",
    "  - `handoff_to_chapter_level`：",
    "本卷登场人物：",
    "本卷主要场景：",
    "本卷关键道具：",
    "本卷任务线",
    "- 上承部级主任务：",
    "- 支流角色：",
    "- 下钻章级任务分配：",
    "- 汇聚回主线：",
    "卷末达成：",
    "规避：",
]
CHAPTER_REQUIRED = [
    "章标题：",
    "本章故事概要：",
    "本章时间推进：",
    "- `chapter_start_state`：",
    "- `visible_time_span`：",
    "- `event_order`：",
    "- `parallel_hidden_events`：",
    "- `chapter_end_state`：",
    "- `handoff_to_next_chapter`：",
    "本章冲突：",
    "本章爽点设计：",
    "本章悬念开关：",
    "- 上承卷级悬念：",
    "- 本章读者可知：",
    "- 本章角色可知：",
    "- 本章悬念线程动作：",
    "  - `suspense_id`：",
    "  - `priority`：",
    "  - `status_before`：",
    "  - `next_action`：",
    "  - `status_after`：",
    "  - `dependency`：",
    "  - `reader_state_delta`：",
    "  - `pov_state_delta`：",
    "- 本章需要隐藏的：",
    "- 本章误导/疑阵：",
    "- 本章揭秘的：",
    "- 本章只埋不揭的：",
    "- 章末悬念压力：",
    "- 本章悬念负载：",
    "- 正文禁止上帝视角说明：",
    "本章节奏曲线：",
    "`selected_pack`：",
    "`selected_mode`：",
    "`mode_selection_reason`：",
    "`payoff_type`：",
    "`rhythm_intensity`：",
    "`previous_next_contrast`：",
    "  - 承接上一章：",
    "  - 预留下一章：",
    "七步职责映射：",
    "规划义务：",
    "`entry_promise`：",
    "`conflict_axis`：",
    "`micro_payoff`：",
    "`exit_hook`：",
    "义务段位：",
    "建议写法：",
    "本章登场人物：",
    "本章主要场景：",
    "本章关键道具：",
    "本章任务线",
    "- 上承卷级任务：",
    "- 支流角色：",
    "- 汇聚动作：",
    "- 未汇聚任务去向：",
    "章末达成：",
    "本章线索：",
    "本章伏笔",
    "规避：",
]


def _require_headings(path: Path, headings: list[str]) -> list[str]:
    if not path.is_file():
        return [f"missing file: {path}"]
    text = path.read_text(encoding="utf-8")
    errors: list[str] = []
    for heading in headings:
        if heading not in text:
            errors.append(f"{path}: missing heading `{heading}`")
    if "```mermaid" not in text:
        errors.append(f"{path}: missing mermaid block")
    return errors


def _ensure_story_scripts_on_path() -> None:
    story_scripts_dir = Path(__file__).resolve().parents[2] / "scripts"
    if str(story_scripts_dir) not in sys.path:
        sys.path.insert(0, str(story_scripts_dir))


def validate(project_root: Path) -> list[str]:
    _ensure_story_scripts_on_path()
    from planning_paths import canonical_book_plan_path, canonical_volume_plan_path  # type: ignore

    planning_root = project_root / "2-卷章"
    errors: list[str] = []
    errors.extend(_require_headings(canonical_book_plan_path(project_root), BOOK_REQUIRED))

    for volume_dir in sorted(planning_root.glob("第*卷")):
        if not volume_dir.is_dir():
            continue
        volume_num_text = volume_dir.name.removeprefix("第").removesuffix("卷")
        if not volume_num_text.isdigit():
            continue
        volume_num = int(volume_num_text)
        errors.extend(_require_headings(canonical_volume_plan_path(project_root, volume_num), VOLUME_REQUIRED))
        for path in sorted(volume_dir.glob("第*章.md")):
            errors.extend(_require_headings(path, CHAPTER_REQUIRED))
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate new story planning markdown outputs.")
    parser.add_argument("project_root", nargs="?", default=".", help="Project root containing 2-卷章/")
    args = parser.parse_args()

    errors = validate(Path(args.project_root).resolve())
    if errors:
        for item in errors:
            print(item)
        return 1
    print("planning outputs validated")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
