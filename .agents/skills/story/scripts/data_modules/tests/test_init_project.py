#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import sys
from pathlib import Path

import pytest
import yaml


def _load_module():
    scripts_dir = Path(__file__).resolve().parents[2]
    if str(scripts_dir) not in sys.path:
        sys.path.insert(0, str(scripts_dir))
    import init_project

    return init_project


def _load_yaml(path: Path):
    return yaml.safe_load(path.read_text(encoding="utf-8"))


def test_init_project_creates_five_init_files_and_inlines_workflow_runtime(tmp_path, monkeypatch, capsys):
    module = _load_module()

    monkeypatch.setattr(module, "write_current_project_pointer", lambda *_args, **_kwargs: None)

    project_root = tmp_path / "projects" / "story" / "测试小说"
    module.init_project(
        str(project_root),
        "测试小说",
        "修仙+规则怪谈",
        init_mode="顾问团模式",
        mode_source="user_selected",
        decision_owner="user",
        planning_agents=".codex/agents/小说家/金庸.md,.codex/agents/导演/徐克.md",
        review_agents=".codex/agents/评审/博尔赫斯.md",
        research_policy="targeted-web-precision",
        user_confirmed_fields="project.title,project.genre,project.one_liner,project.core_conflict",
        council_advised_fields="protagonist.name,relationship.antagonist_mirror,constraints.anti_trope,constraints.opening_hook",
        protagonist_name="林默",
        target_words=500000,
        target_chapters=120,
        one_liner="林默被迫在修仙规则副本里求生",
        core_conflict="他必须同时遵守两套互相咬杀的生存法则",
        golden_finger_growth_rhythm="慢热",
        antagonist_mirror="反派代表绝对服从规则，主角代表用规则撕开规则",
        anti_trope="不用无脑碾压升级，而用规则理解差建立压迫感",
        hard_constraints="不能随意越级开挂,每次破局都要付出代价",
        opening_hook="开篇第一夜就有人因误读规则暴毙",
    )

    state = json.loads((project_root / "STATE.json").read_text(encoding="utf-8"))
    team_manifest = _load_yaml(project_root / "team.yaml")
    north_star = _load_yaml(project_root / "0-Init" / "north_star.yaml")
    source_manifest = _load_yaml(project_root / "0-Init" / "story-source-manifest.yaml")
    init_handoff = _load_yaml(project_root / "0-Init" / "init_handoff.yaml")
    changelog = (project_root / "CHANGELOG.md").read_text(encoding="utf-8")
    assert state["project_name"] == "测试小说"
    assert state["current_stage"] == "0-Init"
    assert state["recommended_next_stage"] == "1-Cards"
    assert state["paths"]["story_root"] == "Story/"
    assert state["paths"]["context_root"] == "CONTEXT/"
    assert state["paths"]["cards_root"] == "1-Cards/"
    assert state["paths"]["loopback_root"] == "5-Loopback/"
    assert state["main_artifacts"]["north_star"] == "0-Init/north_star.yaml"
    assert state["main_artifacts"]["story_source_manifest"] == "0-Init/story-source-manifest.yaml"
    assert state["main_artifacts"]["init_handoff"] == "0-Init/init_handoff.yaml"
    assert state["main_artifacts"]["team"] == "team.yaml"
    assert state["workflow_runtime"]["workflow_state"]["current_task"] is None
    assert state["workflow_runtime"]["execution_state"]["active_run_id"] is None
    assert state["workflow_runtime"]["execution_state"]["schema_version"] == "1.1"
    assert state["workflow_runtime"]["execution_state"]["stage_progress"]["0-init"]["stage_label"] == "初始化"
    assert state["workflow_runtime"]["execution_state"]["stage_progress"]["0-init"]["status"] == "completed"
    assert state["workflow_runtime"]["execution_state"]["stage_progress"]["0-init"]["latest_command"] == "story-init"
    assert state["workflow_runtime"]["task_log"][0]["event"] == "project_initialized"
    assert state["project_info"]["init_handoff_schema_version"] == "story2026/init-handoff/v2"
    assert state["project_info"]["story_source_root"] == "Story/"
    assert state["project_info"]["project_context_root"] == "CONTEXT/"

    assert team_manifest["init_contract"]["init_mode"] == "team_roleplay"
    assert team_manifest["init_contract"]["team_lineup_mode"] == "custom"
    assert team_manifest["init_contract"]["selector_scope_root"] == ".agents/skills/team/"
    assert team_manifest["runtime_policy"]["require_subagents_for_init_execution"] is True
    assert team_manifest["runtime_policy"]["init_execution_owner_role"] == "planning"
    assert team_manifest["roles"]["planning"]["init_execution"]["execution_mode"] == "direct-answer-packet"
    assert team_manifest["roles"]["planning"]["members"] == [
        ".codex/agents/小说家/金庸.md",
        ".codex/agents/导演/徐克.md",
    ]
    assert team_manifest["roles"]["review"]["members"] == [".codex/agents/评审/博尔赫斯.md"]

    assert north_star["project_identity"]["title"] == "测试小说"
    assert north_star["story_kernel"]["premise"] == "林默被迫在修仙规则副本里求生"
    assert north_star["story_kernel"]["opening_hook"] == "开篇第一夜就有人因误读规则暴毙"
    assert north_star["reader_promise"]["anti_trope"] == "不用无脑碾压升级，而用规则理解差建立压迫感"
    assert north_star["cards"]["world_system"]["worldview"]["genre"] == "修仙+规则怪谈"

    assert source_manifest["primary_story_source"]["status"] == "missing"
    assert source_manifest["readiness"]["can_enter_cards"] is True
    assert source_manifest["readiness"]["can_enter_planning"] is True

    assert init_handoff["north_star_ref"] == "0-Init/north_star.yaml"
    assert init_handoff["story_source_manifest_ref"] == "0-Init/story-source-manifest.yaml"
    assert init_handoff["team_ref"] == "team.yaml"
    assert init_handoff["project_contract"]["recommended_next_stage"] == "1-Cards"
    assert init_handoff["stage_entry_seeds"]["cards_seed"]["character_seed"]["protagonist"]["name"] == "林默"
    assert init_handoff["stage_entry_seeds"]["planning_seed"]["story_engine"]["golden_finger_growth_rhythm"] == "慢热"
    assert (project_root / "Story").is_dir()
    assert (project_root / "CONTEXT").is_dir()
    assert (project_root / "3-Drafting").is_dir()
    assert (project_root / "1-Cards" / "1-风格卡" / "总风格").is_dir()
    assert (project_root / "1-Cards" / "5-类型卡" / "总题材").is_dir()
    assert (project_root / "2-Planning").is_dir()
    assert (project_root / "4-Validation").is_dir()
    assert (project_root / "5-Loopback").is_dir()
    assert not (project_root / "Drafting").exists()
    assert not (project_root / "正文").exists()
    assert not (project_root / "1-Cards" / "其他设定").exists()
    assert not (project_root / ".webnovel").exists()
    assert not (project_root / ".env.example").exists()
    assert not (project_root / "2-Planning" / "legacy").exists()
    assert not (project_root / ".git").exists()

    assert "创建项目级 `CONTEXT/` 目录，作为整个创作阶段共享附加上下文根。" in changelog
    assert "写入 `0-Init/north_star.yaml`、`0-Init/story-source-manifest.yaml`、`0-Init/init_handoff.yaml` 初始化三件套。" in changelog

    captured = capsys.readouterr()
    assert "Generated files:" in captured.out
    assert " - Story/" in captured.out
    assert " - CONTEXT/" in captured.out
    assert " - 1-Cards/" in captured.out
    assert " - 2-Planning/" in captured.out
    assert " - 4-Validation/" in captured.out
    assert " - 5-Loopback/" in captured.out
    assert "2-Planning/整体规划.md is not created during /story-init; generate it via /story-plan." in captured.out


def test_init_project_tracks_assistant_inference_in_handoff(tmp_path, monkeypatch):
    module = _load_module()
    monkeypatch.setattr(module, "write_current_project_pointer", lambda *_args, **_kwargs: None)

    project_root = tmp_path / "projects" / "story" / "快速模式书"
    module.init_project(
        str(project_root),
        "快速模式书",
        "都市异能",
        init_mode="快速模式",
        mode_source="user_selected",
        decision_owner="assistant",
        assistant_inferred_fields="project.one_liner,constraints.anti_trope,golden_finger.type",
        one_liner="他一夜之间能看见所有人的秘密价格",
        anti_trope="不用扮猪吃虎，直接把代价明示",
        golden_finger_type="定价视野",
        target_words=300000,
        target_chapters=90,
    )

    state = json.loads((project_root / "STATE.json").read_text(encoding="utf-8"))
    init_handoff = _load_yaml(project_root / "0-Init" / "init_handoff.yaml")

    assert state["project_info"]["decision_owner"] == "assistant"
    assert init_handoff["init_session"]["decision_owner"] == "assistant"
    assert "project.one_liner" in init_handoff["sources_breakdown"]["assistant_inferred"]
    assert "constraints.anti_trope" in init_handoff["sources_breakdown"]["assistant_inferred"]


def test_init_project_shared_council_shortcut_populates_all_team_sections(tmp_path, monkeypatch):
    module = _load_module()
    monkeypatch.setattr(module, "write_current_project_pointer", lambda *_args, **_kwargs: None)

    project_root = tmp_path / "projects" / "story" / "共享班底书"
    module.init_project(
        str(project_root),
        "共享班底书",
        "都市异能",
        init_mode="顾问团模式",
        mode_source="user_selected",
        decision_owner="user",
        shared_council_agents=".codex/agents/策划/王家卫.md,.codex/agents/编辑/张爱玲.md",
    )

    state = json.loads((project_root / "STATE.json").read_text(encoding="utf-8"))
    init_handoff = _load_yaml(project_root / "0-Init" / "init_handoff.yaml")
    team_manifest = _load_yaml(project_root / "team.yaml")

    expected = [
        ".codex/agents/策划/王家卫.md",
        ".codex/agents/编辑/张爱玲.md",
    ]

    assert state["project_info"]["council_team_mode"] == "same_lineup"
    assert state["project_info"]["shared_council_agents"] == expected
    assert init_handoff["init_session"]["team_setup"]["roles"]["production"]["members"] == expected
    assert init_handoff["init_session"]["team_setup"]["roles"]["review"]["members"] == expected
    assert team_manifest["roles"]["planning"]["members"] == expected


def test_init_project_reinit_refreshes_team_manifest(tmp_path, monkeypatch):
    module = _load_module()
    monkeypatch.setattr(module, "write_current_project_pointer", lambda *_args, **_kwargs: None)

    project_root = tmp_path / "projects" / "story" / "重跑初始化书"
    module.init_project(
        str(project_root),
        "重跑初始化书",
        "历史古代+悬疑脑洞",
    )

    module.init_project(
        str(project_root),
        "重跑初始化书",
        "历史古代+悬疑脑洞",
        mode_source="inferred",
        decision_owner="assistant",
        planning_agents=".agents/skills/team/study/历史系/易中天/SKILL.md,.agents/skills/team/aigc/编剧组/罗伯特·麦基/SKILL.md",
        production_agents=".agents/skills/team/aigc/导演组/杜琪峰/SKILL.md",
        review_agents=".agents/skills/team/study/历史系/易中天/SKILL.md",
        one_liner="史官在刺客档案中发现自己的死期。",
        core_conflict="他要在被写死前找出写传者。",
    )

    state = json.loads((project_root / "STATE.json").read_text(encoding="utf-8"))
    team_manifest = _load_yaml(project_root / "team.yaml")
    assert team_manifest["init_contract"]["team_lineup_mode"] == "custom"
    assert team_manifest["init_contract"]["mode_source"] == "inferred"
    assert team_manifest["decision_policy"]["decision_owner"] == "assistant"
    assert team_manifest["decision_policy"]["conflict_rule"] == "user_confirmed > review_gate > planning_direct_answer_consensus > role_consensus > main_agent_inferred"
    assert team_manifest["roles"]["planning"]["enabled"] is True
    assert team_manifest["roles"]["planning"]["members"] == [
        ".agents/skills/team/study/历史系/易中天/SKILL.md",
        ".agents/skills/team/aigc/编剧组/罗伯特·麦基/SKILL.md",
    ]
    assert team_manifest["roles"]["production"]["members"] == [
        ".agents/skills/team/aigc/导演组/杜琪峰/SKILL.md",
    ]
    assert team_manifest["roles"]["review"]["members"] == [
        ".agents/skills/team/study/历史系/易中天/SKILL.md",
    ]
    assert state["workflow_runtime"]["task_log"][-1]["event"] == "project_reinitialized"
    assert state["workflow_runtime"]["execution_state"]["stage_progress"]["0-init"]["status"] == "completed"
    assert state["workflow_runtime"]["execution_state"]["stage_progress"]["0-init"]["latest_command"] == "story-init"


def test_init_project_defaults_mode_source_and_user_confirmed(tmp_path, monkeypatch):
    module = _load_module()
    monkeypatch.setattr(module, "write_current_project_pointer", lambda *_args, **_kwargs: None)

    project_root = tmp_path / "projects" / "story" / "自主模式书"
    module.init_project(
        str(project_root),
        "自主模式书",
        "悬疑",
        protagonist_name="周岚",
        target_words=250000,
        target_chapters=70,
        one_liner="周岚在封闭山城里追查失踪案",
    )

    state = json.loads((project_root / "STATE.json").read_text(encoding="utf-8"))
    init_handoff = _load_yaml(project_root / "0-Init" / "init_handoff.yaml")

    assert state["project_info"]["mode_source"] == "defaulted"
    assert state["project_info"]["team_lineup_mode"] == "auto"
    assert init_handoff["init_session"]["mode_source"] == "defaulted"
    assert "project.title" in init_handoff["sources_breakdown"]["user_confirmed"]
    assert "protagonist.name" in init_handoff["sources_breakdown"]["user_confirmed"]


def test_init_project_defaults_unassigned_fields_to_assistant_inferred_when_assistant_owns_decisions(
    tmp_path, monkeypatch
):
    module = _load_module()
    monkeypatch.setattr(module, "write_current_project_pointer", lambda *_args, **_kwargs: None)

    project_root = tmp_path / "projects" / "story" / "助手拍板书"
    module.init_project(
        str(project_root),
        "助手拍板书",
        "武侠",
        mode_source="inferred",
        decision_owner="assistant",
        user_confirmed_fields="project.title",
        one_liner="一个剑客在无敌后反向追索失败的意义。",
        core_conflict="他越接近天下第一，越无法和任何人真正相遇。",
        protagonist_name="独孤某",
    )

    init_handoff = _load_yaml(project_root / "0-Init" / "init_handoff.yaml")
    payload = module._build_init_handoff_payload(
        now_iso="2026-04-18T11:11:00",
        init_mode="team代入模式",
        mode_source="inferred",
        decision_owner="assistant",
        advisor_agents="",
        shared_council_agents="",
        planning_agents="",
        production_agents="",
        review_agents="",
        research_policy="none",
        user_confirmed_fields="project.title",
        council_advised_fields="",
        assistant_inferred_fields="",
        title="助手拍板书",
        genre="武侠",
        protagonist_name="独孤某",
        target_words=2000000,
        target_chapters=600,
        one_liner="一个剑客在无敌后反向追索失败的意义。",
        core_conflict="他越接近天下第一，越无法和任何人真正相遇。",
        golden_finger_name="",
        golden_finger_type="",
        golden_finger_style="",
        golden_finger_growth_rhythm="",
        core_selling_points="",
        protagonist_structure="",
        heroine_config="",
        heroine_names="",
        heroine_role="",
        co_protagonists="",
        co_protagonist_roles="",
        antagonist_tiers="",
        antagonist_mirror="",
        world_scale="",
        factions="",
        power_system_type="",
        social_class="",
        resource_distribution="",
        gf_visibility="",
        gf_irreversible_cost="",
        protagonist_desire="",
        protagonist_flaw="",
        protagonist_archetype="",
        antagonist_level="",
        target_reader="",
        platform="",
        anti_trope="",
        hard_constraints="",
        opening_hook="",
        currency_system="",
        currency_exchange="",
        sect_hierarchy="",
        cultivation_chain="",
        cultivation_subtiers="",
        story_kernel_why_now="",
        story_kernel_ending_vector="",
        tone="",
        violence_texture="",
        mystery_density="",
        worldline_mode="",
        old_character_policy="",
        must_keep="",
        must_not_do="",
        no_fly_zones="",
    )
    confirmation = payload["confirmation"]

    assert init_handoff["sources_breakdown"]["user_confirmed"] == ["project.title"]
    assert "project.one_liner" in init_handoff["sources_breakdown"]["assistant_inferred"]
    assert "project.core_conflict" in init_handoff["sources_breakdown"]["assistant_inferred"]
    assert "protagonist.name" in init_handoff["sources_breakdown"]["assistant_inferred"]
    assert "project" not in confirmation["user_confirmed"] or "one_liner" not in confirmation["user_confirmed"].get(
        "project", {}
    )
    assert confirmation["assistant_inferred"]["project"]["one_liner"] == "一个剑客在无敌后反向追索失败的意义。"
    assert confirmation["assistant_inferred"]["project"]["core_conflict"] == "他越接近天下第一，越无法和任何人真正相遇。"
    assert confirmation["assistant_inferred"]["protagonist"]["name"] == "独孤某"


def test_init_project_legacy_advisor_agents_fallbacks_to_planning_team(tmp_path, monkeypatch):
    module = _load_module()
    monkeypatch.setattr(module, "write_current_project_pointer", lambda *_args, **_kwargs: None)

    project_root = tmp_path / "projects" / "story" / "兼容旧字段书"
    module.init_project(
        str(project_root),
        "兼容旧字段书",
        "悬疑",
        init_mode="顾问团模式",
        advisor_agents=".codex/agents/小说家/阿城.md",
    )

    init_handoff = _load_yaml(project_root / "0-Init" / "init_handoff.yaml")
    team_setup = init_handoff["init_session"]["team_setup"]

    assert team_setup["team_mode"] == "legacy_planning_only"
    assert team_setup["planning_agents"] == [".codex/agents/小说家/阿城.md"]
    assert team_setup["production_agents"] == []
    assert team_setup["review_agents"] == []


def test_init_project_rejects_skill_directory_target(monkeypatch):
    module = _load_module()
    monkeypatch.setattr(module, "write_current_project_pointer", lambda *_args, **_kwargs: None)

    forbidden_root = Path(module.__file__).resolve().parents[1] / "tmp-init"
    try:
        with pytest.raises(SystemExit, match="story2026 skill package"):
            module.init_project(str(forbidden_root), "禁写项目", "修仙")
    finally:
        if forbidden_root.exists():
            raise AssertionError("forbidden project root should not be created")


def test_init_project_normalizes_hidden_project_leaf(tmp_path, monkeypatch):
    module = _load_module()
    monkeypatch.setattr(module, "write_current_project_pointer", lambda *_args, **_kwargs: None)

    hidden_root = tmp_path / ".draft"
    normalized_root = tmp_path / "测试-书"
    module.init_project(str(hidden_root), "测试 书?", "修仙")

    assert not hidden_root.exists()
    assert normalized_root.exists()
    assert (normalized_root / "STATE.json").exists()
    assert (normalized_root / "0-Init" / "north_star.yaml").exists()
