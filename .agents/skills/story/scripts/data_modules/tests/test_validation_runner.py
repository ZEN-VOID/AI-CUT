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


def _seed_validation_truth(project_root: Path, chapter: int) -> None:
    planning_dir = project_root / "2-Planning"
    planning_dir.mkdir(parents=True, exist_ok=True)
    (planning_dir / "全息地图.json").write_text(
        json.dumps(
            {
                "schema_version": "story2026/holomap/v1",
                "content": {
                    "holomap": {
                        "chapter_boards": [
                            {
                                "chapter": chapter,
                                "summary": "李青必须带着代价突破，并保留宗门压力。",
                                "chapter_goals": ["突破后必须暴露代价"],
                                "must_happen": ["留下规则线索"],
                                "cannot_change": ["宗门压力仍然存在"],
                            }
                        ]
                    }
                },
            },
            ensure_ascii=False,
            indent=2,
        ),
        encoding="utf-8",
    )

    global_card_dir = project_root / "1-Cards" / "0-全局卡" / "总设定"
    global_card_dir.mkdir(parents=True, exist_ok=True)
    global_card_ref = "1-Cards/0-全局卡/总设定/世界总卡.json"
    (project_root / "1-Cards" / "0-全局卡" / "全局索引.json").write_text(
        json.dumps(
            {
                "content": {
                    "card_groups": {"master_globals": [global_card_ref]},
                    "global_contract_refs": [{"card_id": "世界总卡", "path": global_card_ref}],
                }
            },
            ensure_ascii=False,
            indent=2,
        ),
        encoding="utf-8",
    )
    (project_root / global_card_ref).write_text(
        json.dumps(
            {
                "content": {
                    "card_schema": {
                        "global_card": {
                            "core": {
                                "worldview": {"genre": "xuanhuan"},
                                "rule_system": [{"label": "铁律", "value": "越级有代价"}],
                                "golden_finger": {"name": "系统", "limits": ["每日一次", "越级要付出代价"]},
                            }
                        }
                    }
                }
            },
            ensure_ascii=False,
            indent=2,
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


def test_text_contains_candidate_accepts_split_scene_realization():
    module = _load_module()
    text = (
        "令狐冲本只想买酒避世，却先看见税线恶压，"
        "又看见晨雾未散前平民被逼得跪成一排。"
    )

    assert module._text_contains_candidate(
        text,
        "却看见税线在晨雾未散前逼平民下跪",
    )


def test_structure_validator_scores_checked_obligations_only(tmp_path):
    module = _load_module()
    result = module._run_structure(
        ctx={
            "chapter": 1,
            "manuscript_text": (
                "令狐冲与任盈盈在那霸港雨脚与潮气里，只想买酒避世。"
                "他们抵达那霸港后，却先看见税线恶压。"
                "令狐冲本只想买酒避世，却先看见税线恶压，又看见晨雾未散前平民被逼得跪成一排。"
            ),
            "fact_pack": {
                "chapter_board": {
                    "chapter_goals": [
                        "令狐冲与任盈盈在那霸港雨脚与潮气里",
                        "只想买酒避世",
                        "却看见税线在晨雾未散前逼平民下跪",
                    ],
                    "must_happen": [
                        "令狐冲与任盈盈抵达那霸港",
                        "只想买酒避世",
                        "却先看见税线恶压",
                        "第一次不是因仇而动",
                        "而是因看见眼前人被迫在雨里折腰而动心",
                    ],
                }
            },
        },
        role_id="structure-validator",
        spec={},
        validation_context="final_acceptance",
    )

    assert result["pass"] is True
    assert result["metrics"]["required_events_hit"] == 6
    assert result["metrics"]["missed_obligations"] == 0
    assert result["overall_score"] > 0


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


def test_validation_runner_logic_compares_upstream_truth(tmp_path):
    module = _load_module()
    _seed_project(
        tmp_path,
        8,
        "李青在宗门里借助系统强行越级突破，却毫无代价，宗门压力也像从未存在过，一切都轻易解决。",
    )
    _seed_validation_truth(tmp_path, 8)

    result = module.run_validator(
        project_root=tmp_path,
        chapter_num=8,
        role_id="logic-validator",
        validation_context="final_acceptance",
        current_step_id="Step 1",
    )

    assert result["pass"] is False
    assert result["metrics"]["world_rule_conflicts"] >= 1
    assert result["metrics"]["exception_cost_gaps"] >= 1
    assert any(item.get("source_layer_owner") in {"0-Init", "1-Cards", "2-Planning"} for item in result["issues"])


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


def test_continuity_validator_ignores_markdown_frontmatter_when_checking_intro(tmp_path):
    module = _load_module()
    _seed_project(
        tmp_path,
        2,
        "\n".join(
            [
                "---",
                "episode_num: 2",
                'episode_title: "承接测试"',
                "processed_steps:",
                '  - "1-单集叙事起盘"',
                "---",
                "",
                "# 第2集",
                "",
                "从门口那张血书前离开后，李青沿着长街走了很久。",
                "他掌心里还压着昨夜留下的纸角，也还记得自己是怎么被人一步步逼进局里的。",
            ]
        ),
    )
    drafting_dir = tmp_path / "3-Drafting"
    (drafting_dir / "第1集.md").write_text(
        "# 第1集\n\n李青在门口看见血书，终于意识到昨夜那场赢像被人安排过。",
        encoding="utf-8",
    )

    result = module.run_validator(
        project_root=tmp_path,
        chapter_num=2,
        role_id="continuity-validator",
        validation_context="drafting_inline",
        current_step_id="Step 8",
    )

    assert result["pass"] is True
    assert result["metrics"]["previous_episode_bridge"] == "strong"


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
    assert any(
        item.get("rework_target_step") in {"5-对白个性化", "6-心理活动描写", "7-追读力强化"}
        for item in result["issues"]
    )


def test_character_validator_reports_growth_continuity_metrics_when_growth_enabled(tmp_path):
    module = _load_module()
    _seed_project(
        tmp_path,
        11,
        "独孤求败站在门前，没有立刻拔剑。他知道若再顺着那股本能冲出去，就只是替别人把局走完。",
    )

    protagonist_card = tmp_path / "1-Cards" / "2-角色卡" / "主要角色" / "独孤求败.json"
    protagonist_card.parent.mkdir(parents=True, exist_ok=True)
    protagonist_card.write_text(
        json.dumps(
            {
                "content": {
                    "card_schema": {
                        "character_card": {
                            "card_id": "独孤求败",
                            "core": {
                                "identity": {"name": "独孤求败"},
                                "cast_markers": {"primary_alignment": "protagonist", "is_protagonist": True},
                                "growth_contract": {"growth_enabled": True, "growth_role": "protagonist"},
                            },
                            "current_state": {
                                "growth_state": {
                                    "skill": {"focus": "没有立刻拔剑"},
                                    "heart": {"current_tension": "替别人把局走完"},
                                    "emotion": {"current_tension": "不敢再把人推远"},
                                }
                            },
                        }
                    }
                }
            },
            ensure_ascii=False,
            indent=2,
        ),
        encoding="utf-8",
    )

    result = module.run_validator(
        project_root=tmp_path,
        chapter_num=11,
        role_id="character-validator",
        validation_context="final_acceptance",
    )

    assert result["metrics"]["growth_continuity_checked"] is True
    assert result["metrics"]["growth_signal_hits"] >= 1


def test_character_validator_fails_when_growth_enabled_but_text_drops_all_growth_signals(tmp_path):
    module = _load_module()
    _seed_project(
        tmp_path,
        12,
        "独孤求败走进院中，只与众人争执了一番，随后便转身离去。",
    )

    protagonist_card = tmp_path / "1-Cards" / "2-角色卡" / "主要角色" / "独孤求败.json"
    protagonist_card.parent.mkdir(parents=True, exist_ok=True)
    protagonist_card.write_text(
        json.dumps(
            {
                "content": {
                    "card_schema": {
                        "character_card": {
                            "card_id": "独孤求败",
                            "core": {
                                "identity": {"name": "独孤求败"},
                                "cast_markers": {"primary_alignment": "protagonist", "is_protagonist": True},
                                "growth_contract": {"growth_enabled": True, "growth_role": "protagonist"},
                            },
                            "current_state": {
                                "growth_state": {
                                    "skill": {"focus": "先收半寸剑"},
                                    "heart": {"current_tension": "别替别人把局走完"},
                                    "emotion": {"current_tension": "不敢再把人推远"},
                                }
                            },
                        }
                    }
                }
            },
            ensure_ascii=False,
            indent=2,
        ),
        encoding="utf-8",
    )

    result = module.run_validator(
        project_root=tmp_path,
        chapter_num=12,
        role_id="character-validator",
        validation_context="final_acceptance",
    )

    assert result["pass"] is False
    assert result["metrics"]["growth_continuity_checked"] is True
    assert result["metrics"]["growth_signal_hits"] == 0
    assert any(item.get("location") == "第12集成长轴" for item in result["issues"])


def test_character_validator_defers_dialogue_only_issues_until_step5(tmp_path):
    module = _load_module()
    _seed_project(
        tmp_path,
        10,
        """
“我不是不想说清楚，只是昨夜山门外那件事牵连太多，一旦现在全讲出来，宗门、秘司、旧案和你我都会一起被拖进来，而且每个人都会顺着这条线把整座山门翻个底朝天。”
“你总以为自己能扛，可你若还照昨夜那样只顾着赢，不看人心、不看后果、不看这局是谁替你铺好的路，下一次死的就不只是门外那一个，而是所有还站在你身边的人。”
        """.strip(),
    )

    step4_result = module.run_validator(
        project_root=tmp_path,
        chapter_num=10,
        role_id="character-validator",
        validation_context="drafting_inline",
        current_step_id="Step 4",
    )
    step5_result = module.run_validator(
        project_root=tmp_path,
        chapter_num=10,
        role_id="character-validator",
        validation_context="drafting_inline",
        current_step_id="Step 5",
    )

    assert step4_result["pass"] is True
    assert step4_result["metrics"]["speech_violations"] >= 2
    assert "留待 Step 5" in step4_result["summary"]
    assert step5_result["pass"] is False
    assert any(item.get("rework_target_step") == "5-对白个性化" for item in step5_result["issues"])


def test_validation_runner_final_acceptance_writes_aggregate_json(tmp_path):
    module = _load_module()
    _seed_project(
        tmp_path,
        9,
        "清晨，李青回到宗门。他追着昨夜留下的线索继续调查，却在章末留下了新的疑点与下一步动机。",
    )
    _seed_validation_truth(tmp_path, 9)

    payload = module.run_final_acceptance(
        project_root=tmp_path,
        chapter_num=9,
    )

    aggregate_path = tmp_path / "4-Validation" / "第9集.validation.json"
    assert aggregate_path.is_file()
    assert payload["validation_ref"] == "4-Validation/第9集.validation.json"
    assert "type-pack-fit-validator" in payload["selected_agents"]
    assert "type-pack-fit-validator" in payload["dimension_report_refs"]
    assert "type-pack-fit" in payload["dimension_scores"]
    assert payload["validation_status"] in {"PASS", "FAIL-QUALITY", "FAIL-COVENANT", "FAIL-RUNTIME"}
