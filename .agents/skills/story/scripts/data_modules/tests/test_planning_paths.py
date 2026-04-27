#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import sys
from pathlib import Path


def _ensure_scripts_on_path() -> None:
    scripts_dir = Path(__file__).resolve().parents[2]
    if str(scripts_dir) not in sys.path:
        sys.path.insert(0, str(scripts_dir))


def test_planning_paths_default_volume_mapping():
    _ensure_scripts_on_path()
    from planning_paths import canonical_chapter_plan_relpath, planning_volume_num_for_chapter

    assert planning_volume_num_for_chapter(12) == 2
    assert canonical_chapter_plan_relpath(12) == "2-卷章/第2卷/第12章.md"


def test_planning_paths_respect_state_volume_override(tmp_path):
    _ensure_scripts_on_path()
    from planning_paths import (
        canonical_chapter_plan_actualization_relpath,
        canonical_chapter_plan_relpath,
        planned_chapter_numbers_for_volume,
        planning_volume_num_for_chapter,
    )

    project_root = tmp_path / "book"
    project_root.mkdir(parents=True, exist_ok=True)
    (project_root / "STATE.json").write_text(
        json.dumps(
            {
                "progress": {
                    "volumes_planned": [
                        {"volume": 1, "chapters_range": "1-12"},
                        {"volume": 2, "chapters_range": "13-18"},
                    ]
                }
            },
            ensure_ascii=False,
        ),
        encoding="utf-8",
    )

    assert planning_volume_num_for_chapter(12, project_root=project_root) == 1
    assert canonical_chapter_plan_relpath(12, project_root=project_root) == "2-卷章/第1卷/第12章.md"
    assert canonical_chapter_plan_actualization_relpath(12, project_root=project_root) == (
        "2-卷章/第1卷/第12章.actualization.json"
    )
    assert planned_chapter_numbers_for_volume(project_root, 1) == list(range(1, 13))
