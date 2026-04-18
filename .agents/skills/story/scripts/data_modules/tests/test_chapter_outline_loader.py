#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import sys
from pathlib import Path


def _ensure_scripts_on_path() -> None:
    scripts_dir = Path(__file__).resolve().parents[2]
    if str(scripts_dir) not in sys.path:
        sys.path.insert(0, str(scripts_dir))


def _write_project(tmp_path: Path) -> Path:
    project_root = tmp_path / "book"
    planning_dir = project_root / "2-Planning"
    planning_dir.mkdir(parents=True, exist_ok=True)
    state = {
        "project_info": {
            "title": "笑傲江湖之风云再再起",
            "core_selling_points": "令狐冲与任盈盈东渡东瀛，在异域刀局与残意神话中求生破局。",
            "heroine_names": "任盈盈",
            "antagonist_tiers": "地方恶压、幕府鹰犬与东方残意共同织成追杀之网。",
        }
    }
    (project_root / "STATE.json").write_text(json.dumps(state, ensure_ascii=False), encoding="utf-8")

    holomap = {
        "holomap": {
            "volume_boards": [
                {
                    "volume_ref": "V1",
                    "title": "海雾东渡",
                    "chapter_range": "1-10",
                    "payoff_target": "双主角在东瀛站稳脚跟，并发现真正敌人是一张网。",
                }
            ],
            "chapter_boards": [
                {
                    "node_id": "node-01",
                    "episode_ref": "第1章",
                    "timeline_ref": "phase-01",
                    "bundled_elements": {
                        "events": ["双主角抵达海雾港町", "第一次感到异域压迫不是传闻"],
                        "conflicts": ["地方恶压扑面而来"],
                        "clues": ["白鹤酒壶后的旧痕"],
                        "characters": ["令狐冲", "任盈盈"],
                        "scenes": ["海雾港町"],
                        "items": ["白鹤酒壶"],
                        "rule_impacts": ["外乡人破规会被整个港口秩序盯上"],
                    },
                    "planned_state": {"notes": "冷开场，落地即压迫。"},
                },
                {
                    "node_id": "node-02",
                    "episode_ref": "第2章",
                    "bundled_elements": {
                        "events": ["港口收账名单逼近普通人", "令狐冲被迫第一次站出来"],
                        "characters": ["令狐冲", "琉球少年"],
                        "items": ["令狐冲佩剑"],
                    },
                },
            ],
        }
    }
    (planning_dir / "全息地图.json").write_text(json.dumps(holomap, ensure_ascii=False), encoding="utf-8")
    return project_root


def test_load_chapter_outline_reads_bundled_elements(tmp_path):
    _ensure_scripts_on_path()
    from chapter_outline_loader import load_chapter_outline

    project_root = _write_project(tmp_path)
    outline = load_chapter_outline(project_root, 1, max_chars=None)

    assert "### 第1章" in outline
    assert "双主角抵达海雾港町" in outline
    assert "地方恶压扑面而来" in outline
    assert "外乡人破规会被整个港口秩序盯上" in outline
