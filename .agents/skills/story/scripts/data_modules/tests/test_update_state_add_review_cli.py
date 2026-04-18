#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import sys


def test_update_state_cli_add_review_writes_checkpoint(tmp_path, monkeypatch):
    import update_state as update_state_module

    webnovel_dir = tmp_path / ".webnovel"
    webnovel_dir.mkdir(parents=True, exist_ok=True)

    state = {
        "project_info": {},
        "progress": {"current_chapter": 1, "total_words": 0},
        "protagonist_state": {
            "power": {"realm": "炼气", "layer": 1, "bottleneck": None},
            "location": "村口",
        },
        "relationships": {},
        "world_settings": {},
        "plot_threads": {},
        "review_checkpoints": [],
    }
    state_file = webnovel_dir / "state.json"
    state_file.write_text(json.dumps(state, ensure_ascii=False), encoding="utf-8")

    # 避免在测试里创建备份目录/修改权限等非核心行为
    monkeypatch.setattr(update_state_module.StateUpdater, "backup", lambda self: True)

    report_file = "review/report_1_2.md"
    monkeypatch.setattr(
        sys,
        "argv",
        [
            "update_state",
            "--project-root",
            str(tmp_path),
            "--add-review",
            "1-2",
            report_file,
            "--review-anti-ai-force-check",
            "fail",
            "--review-spoiler-risk",
            "high",
            "--review-contrivance-risk",
            "medium",
            "--review-cold-commentary-risk",
            "critical",
        ],
    )
    update_state_module.main()

    updated = json.loads(state_file.read_text(encoding="utf-8"))
    checkpoints = updated.get("review_checkpoints")
    assert isinstance(checkpoints, list)
    assert checkpoints[-1]["chapters"] == "1-2"
    assert checkpoints[-1]["report"] == report_file
    assert checkpoints[-1]["anti_ai_force_check"] == "fail"
    assert checkpoints[-1]["spoiler_risk"] == "high"
    assert checkpoints[-1]["contrivance_risk"] == "medium"
    assert checkpoints[-1]["cold_commentary_risk"] == "critical"
