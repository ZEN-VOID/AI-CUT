#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import sys


def test_update_state_cli_add_acceptance_writes_checkpoint(tmp_path, monkeypatch):
    import update_state as update_state_module

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
        "acceptance_checkpoints": [],
    }
    state_file = tmp_path / "STATE.json"
    state_file.write_text(json.dumps(state, ensure_ascii=False), encoding="utf-8")

    # 避免在测试里创建备份目录/修改权限等非核心行为
    monkeypatch.setattr(update_state_module.StateUpdater, "backup", lambda self: True)

    acceptance_file = "4-润色/第1卷/第2章.acceptance.json"
    monkeypatch.setattr(
        sys,
        "argv",
        [
            "update_state",
            "--project-root",
            str(tmp_path),
            "--add-acceptance",
            "1-2",
            acceptance_file,
            "--acceptance-volume",
            "1",
            "--acceptance-anti-ai-force-check",
            "fail",
            "--acceptance-spoiler-risk",
            "high",
            "--acceptance-contrivance-risk",
            "medium",
            "--acceptance-cold-commentary-risk",
            "critical",
        ],
    )
    update_state_module.main()

    updated = json.loads(state_file.read_text(encoding="utf-8"))
    checkpoints = updated.get("acceptance_checkpoints")
    assert isinstance(checkpoints, list)
    assert checkpoints[-1]["chapters"] == "1-2"
    assert checkpoints[-1]["volume"] == 1
    assert checkpoints[-1]["volume_ref"] == "第1卷"
    assert checkpoints[-1]["chapter_refs"] == [1, 2]
    assert checkpoints[-1]["acceptance_ref"] == acceptance_file
    assert checkpoints[-1]["accepted_at"]
    assert checkpoints[-1]["anti_ai_force_check"] == "fail"
    assert checkpoints[-1]["spoiler_risk"] == "high"
    assert checkpoints[-1]["contrivance_risk"] == "medium"
    assert checkpoints[-1]["cold_commentary_risk"] == "critical"
