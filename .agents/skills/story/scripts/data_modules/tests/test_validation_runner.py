#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import sys
from pathlib import Path


def _load_module():
    scripts_dir = Path(__file__).resolve().parents[2]
    if str(scripts_dir) not in sys.path:
        sys.path.insert(0, str(scripts_dir))
    import validation_runner

    return validation_runner


def _seed_project(project_root: Path, chapter: int, manuscript_text: str) -> None:
    (project_root / "STATE.json").write_text("{}", encoding="utf-8")
    (project_root / ".webnovel").mkdir(parents=True, exist_ok=True)
    drafting_dir = project_root / "3-Drafting"
    drafting_dir.mkdir(parents=True, exist_ok=True)
    (drafting_dir / f"第{chapter}集.md").write_text(manuscript_text, encoding="utf-8")
    init_dir = project_root / "0-Init"
    init_dir.mkdir(parents=True, exist_ok=True)
    (init_dir / "north_star.yaml").write_text(
        "\n".join(
            [
                "type_stack:",
                "  method_kernel: story-core-v1",
                "  base: _base",
                "  primary: 网文高冲击",
                "  secondary: [规则悬疑]",
                "  platform: []",
                "  audience: []",
            ]
        ),
        encoding="utf-8",
    )


def test_validation_runner_writes_structure_report(tmp_path):
    module = _load_module()
    _seed_project(
        tmp_path,
        3,
        "清晨，李青还站在山门前。长老拦住他，问他为何执意下山。李青没有多解释，只说自己要把昨夜留下的线索查清。",
    )

    result = module.run_validator(
        project_root=tmp_path,
        chapter_num=3,
        role_id="structure-validator",
        validation_context="drafting_inline",
        current_step_id="Step 1",
    )

    assert result["agent"] == "structure-validator"
    assert isinstance(result["report_ref"], str)
    assert (tmp_path / result["report_ref"]).is_file()


def test_validation_runner_logic_detects_contrivance_markers(tmp_path):
    module = _load_module()
    _seed_project(
        tmp_path,
        4,
        "李青突然就出现在山巅，莫名得到了秘宝，凭空知道了敌人的计划，事情一下子全都解决了。",
    )

    result = module.run_validator(
        project_root=tmp_path,
        chapter_num=4,
        role_id="logic-validator",
        validation_context="drafting_inline",
        current_step_id="Step 1",
    )

    assert result["pass"] is False
    assert result["issues"]
    assert result["metrics"]["contrivance_risk"] in {"medium", "high"}


def test_validation_runner_batch_returns_all_results(tmp_path):
    module = _load_module()
    _seed_project(
        tmp_path,
        5,
        "清晨，李青又回到旧祠堂。沈舟跟在他身后，两人沿着昨夜留下的脚印继续往里走。",
    )

    payload = module.run_batch(
        project_root=tmp_path,
        chapter_num=5,
        role_ids=["structure-validator", "timeline-validator", "type-pack-fit-validator"],
        validation_context="drafting_inline",
        current_step_id="Step 2",
    )

    assert payload["chapter"] == 5
    assert {item["role_id"] for item in payload["results"]} == {
        "structure-validator",
        "timeline-validator",
        "type-pack-fit-validator",
    }


def test_validation_runner_emits_type_pack_fit_summary(tmp_path):
    module = _load_module()
    _seed_project(
        tmp_path,
        6,
        "李青走进旧楼，却只做情绪回忆，没有给出任何规则、线索或下一步牵引。",
    )

    result = module.run_validator(
        project_root=tmp_path,
        chapter_num=6,
        role_id="structure-validator",
        validation_context="final_acceptance",
    )

    summary = result["type_pack_fit_summary"]
    assert summary["enabled"] is True
    assert "网文高冲击" in summary["active_packs"]
    assert "规则悬疑" in summary["active_packs"]
    assert isinstance(result["type_pack_fail_signals"], list)


def test_validation_runner_type_pack_fit_validator_uses_step_specific_hooks(tmp_path):
    module = _load_module()
    _seed_project(
        tmp_path,
        7,
        "她只是反复说自己很难受、很委屈，眼泪一直掉下来，整章都停在情绪宣告里，没有任何实际转折。",
    )

    north_star = tmp_path / "0-Init" / "north_star.yaml"
    north_star.write_text(
        "\n".join(
            [
                "type_stack:",
                "  method_kernel: story-core-v1",
                "  base: _base",
                "  primary: 网文高冲击",
                "  secondary: [女频强情绪]",
                "  platform: []",
                "  audience: []",
            ]
        ),
        encoding="utf-8",
    )

    result = module.run_validator(
        project_root=tmp_path,
        chapter_num=7,
        role_id="type-pack-fit-validator",
        validation_context="drafting_inline",
        current_step_id="Step 5",
    )

    assert result["pass"] is False
    assert result["current_step_id"] == "Step 5"
    assert any(item.get("rework_target_step") == "5-对白个性化和声口优化" for item in result["issues"])
