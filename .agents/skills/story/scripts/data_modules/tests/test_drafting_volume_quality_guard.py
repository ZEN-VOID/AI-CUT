#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
from pathlib import Path


def _load_module():
    scripts_dir = Path(__file__).resolve().parents[2]
    if str(scripts_dir) not in sys.path:
        sys.path.insert(0, str(scripts_dir))
    import drafting_volume_quality_guard

    return drafting_volume_quality_guard


def test_quality_guard_blocks_missing_snapshot(tmp_path):
    module = _load_module()
    write_log = tmp_path / "第1卷.写作日志.yaml"
    write_log.write_text(
        "\n".join(
            [
                "volume_num: 1",
                "chapter_refs:",
                "  - 3-Drafting/第1卷/第1章.md",
                "  - 3-Drafting/第1卷/第2章.md",
            ]
        )
        + "\n",
        encoding="utf-8",
    )

    result = module.validate_volume_log(write_log, volume_num=1)

    assert result["status"] == "block"
    issue_codes = {item["code"] for item in result["issues"]}
    assert "missing_quality_gate_snapshot" in issue_codes


def test_quality_guard_blocks_legacy_rework_snapshot(tmp_path):
    module = _load_module()
    write_log = tmp_path / "第1卷.写作日志.yaml"
    write_log.write_text(
        "\n".join(
            [
                "volume_num: 1",
                "chapter_refs:",
                "  - 3-Drafting/第1卷/第5章.md",
                "  - 3-Drafting/第1卷/第8章.md",
                "post_review_summary:",
                "  review_mode: subagent-review-council",
                "  reviewed_at: '2026-04-22T13:10:00-07:00'",
                "  reviewer_source: team-explicit",
                "  reviewers:",
                "    - 金庸",
                "    - 徐克",
                "  verdict: rework_required_before_validation",
                "  next_action: 3-Drafting-rework",
                "  representative_chapter_refs:",
                "    - 3-Drafting/第1卷/第5章.md",
                "  primary_issues:",
                "    - 程序化推进过重",
                "  priority_rework_targets:",
                "    - 3-Drafting/第1卷/第5章.md",
            ]
        )
        + "\n",
        encoding="utf-8",
    )

    result = module.validate_volume_log(write_log, volume_num=1)

    assert result["status"] == "block"
    assert result["reason"] == "quality_rework_required_before_validation"


def test_quality_guard_passes_ready_snapshot(tmp_path):
    module = _load_module()
    write_log = tmp_path / "第1卷.写作日志.yaml"
    write_log.write_text(
        "\n".join(
            [
                "volume_num: 1",
                "chapter_refs:",
                "  - 3-Drafting/第1卷/第5章.md",
                "  - 3-Drafting/第1卷/第8章.md",
                "  - 3-Drafting/第1卷/第10章.md",
                "quality_gate_snapshot:",
                "  checkpoint_stage: pre_validation",
                "  review_mode: subagent-review-council",
                "  reviewed_at: '2026-04-22T13:10:00-07:00'",
                "  reviewer_source: team-explicit",
                "  reviewers:",
                "    - 金庸",
                "    - 徐克",
                "  verdict: ready_for_validation",
                "  next_action: 4-Validation",
                "  representative_chapter_refs:",
                "    - 3-Drafting/第1卷/第5章.md",
                "    - 3-Drafting/第1卷/第8章.md",
                "    - 3-Drafting/第1卷/第10章.md",
                "  primary_issues: []",
                "  priority_rework_targets: []",
                "  cross_volume_upgrade_axes:",
                "    - 保持卷内场域分相",
                "  guard_axes:",
                "    anti_formula_progression: pass",
                "    relationship_friction: pass",
                "    spatial_separation: pass",
                "    antagonist_face: pass",
                "    volume_closure: pass",
            ]
        )
        + "\n",
        encoding="utf-8",
    )

    result = module.validate_volume_log(write_log, volume_num=1)

    assert result["status"] == "pass"
    assert result["verdict"] == module.READY_VERDICT
    assert result["metrics"]["passed_axes"] == len(module.REQUIRED_AXES)
