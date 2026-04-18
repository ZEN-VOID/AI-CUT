#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import sys
from pathlib import Path

import pytest


def _load_module():
    scripts_dir = Path(__file__).resolve().parents[2]
    if str(scripts_dir) not in sys.path:
        sys.path.insert(0, str(scripts_dir))
    import init_project

    return init_project


def test_init_project_creates_execution_state_files(tmp_path, monkeypatch):
    module = _load_module()

    monkeypatch.setattr(module, "is_git_available", lambda: False)
    monkeypatch.setattr(module, "write_current_project_pointer", lambda *_args, **_kwargs: None)

    project_root = tmp_path / "projects" / "测试小说"
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

    state = json.loads((project_root / ".webnovel" / "state.json").read_text(encoding="utf-8"))
    project_state = json.loads((project_root / "STATE.json").read_text(encoding="utf-8"))
    workflow_state = json.loads((project_root / ".webnovel" / "workflow_state.json").read_text(encoding="utf-8"))
    execution_state = json.loads((project_root / ".webnovel" / "execution_state.json").read_text(encoding="utf-8"))
    north_star = json.loads((project_root / "Init" / "north_star_contract.json").read_text(encoding="utf-8"))
    init_handoff = json.loads((project_root / "Init" / "初始化简报.json").read_text(encoding="utf-8"))
    init_summary = (project_root / "Init" / "访谈摘要.md").read_text(encoding="utf-8")
    confirmation_card = (project_root / "Init" / "确认卡.md").read_text(encoding="utf-8")
    legacy_outline = (project_root / "Planning" / "legacy" / "总纲.md").read_text(encoding="utf-8")
    idea_bank = json.loads((project_root / ".webnovel" / "idea_bank.json").read_text(encoding="utf-8"))
    team_manifest = (project_root / "TEAM.toml").read_text(encoding="utf-8")
    changelog = (project_root / "CHANGELOG.md").read_text(encoding="utf-8")

    assert state["project_info"]["title"] == "测试小说"
    assert workflow_state["current_task"] is None
    assert workflow_state["history"] == []
    assert execution_state["active_run_id"] is None
    assert execution_state["run_sequence"] == 0
    assert execution_state["stage_progress"]["0-init"]["stage_label"] == "初始化"
    assert execution_state["stage_progress"]["3-drafting"]["status"] == "idle"
    assert execution_state["runs"] == []
    assert state["project_info"]["init_mode"] == "智能顾问团模式"
    assert state["project_info"]["mode_source"] == "user_selected"
    assert state["project_info"]["decision_owner"] == "user"
    assert state["project_info"]["advisor_agents"] == [
        ".codex/agents/小说家/金庸.md",
        ".codex/agents/导演/徐克.md",
    ]
    assert state["project_info"]["planning_council_agents"] == [
        ".codex/agents/小说家/金庸.md",
        ".codex/agents/导演/徐克.md",
    ]
    assert state["project_info"]["production_council_agents"] == []
    assert state["project_info"]["review_council_agents"] == [".codex/agents/评审/博尔赫斯.md"]
    assert state["project_info"]["council_team_mode"] == "per_stage"
    assert state["project_info"]["research_policy"] == "targeted-web-precision"
    assert state["project_info"]["init_contract_model"] == "north_star_contract+cards_seed+planning_seed+unknowns"
    assert state["project_info"]["primary_init_artifact"] == "Init/north_star_contract.json"
    assert state["project_info"]["north_star_schema_version"] == "story2026/north-star-contract/v2"
    assert state["project_info"]["init_handoff_schema_version"] == "story2026/init-handoff/v4"
    assert state["project_info"]["project_entry_state_file"] == "STATE.json"
    assert state["project_info"]["team_manifest_file"] == "TEAM.toml"
    assert state["project_info"]["changelog_file"] == "CHANGELOG.md"
    assert state["project_info"]["task_artifacts_root"] == ".webnovel/tasks"
    assert state["project_info"]["one_liner"] == "林默被迫在修仙规则副本里求生"
    assert state["project_info"]["anti_trope"] == "不用无脑碾压升级，而用规则理解差建立压迫感"
    assert project_state["meta"]["role"] == "project-entry-manifest"
    assert project_state["paths"]["runtime_state"] == ".webnovel/state.json"
    assert project_state["paths"]["team_manifest"] == "TEAM.toml"
    assert project_state["paths"]["changelog"] == "CHANGELOG.md"
    assert project_state["paths"]["task_artifacts_root"] == ".webnovel/tasks"
    assert project_state["init_session"]["mode"] == "智能顾问团模式"
    assert project_state["init_session"]["team_setup"]["roles"]["review"]["members"] == [".codex/agents/评审/博尔赫斯.md"]
    assert project_state["truth_layers"]["project_entry"] == "STATE.json"
    assert north_star["meta"]["role"] == "primary-init-artifact"
    assert north_star["meta"]["companion_handoff"] == "Init/初始化简报.json"
    assert north_star["meta"]["cards_role"] == "north-star-object-constraints"
    assert north_star["story_kernel"]["premise"] == "林默被迫在修仙规则副本里求生"
    assert north_star["story_kernel"]["opening_hook"] == "开篇第一夜就有人因误读规则暴毙"
    assert north_star["story_kernel"]["core_conflict"] == "他必须同时遵守两套互相咬杀的生存法则"
    assert north_star["reader_promise"]["anti_trope"] == "不用无脑碾压升级，而用规则理解差建立压迫感"
    assert north_star["cards"]["section_order"][0] == "文字风格"
    assert north_star["cards"]["world_system"]["worldview"]["genre"] == "修仙+规则怪谈"
    assert north_star["cards"]["relationship_overview"]["macro_conflicts"] == ["他必须同时遵守两套互相咬杀的生存法则"]
    assert init_handoff["meta"]["canonical_consumer"] == "1-Cards"
    assert init_handoff["meta"]["primary_artifact"] == "Init/north_star_contract.json"
    assert init_handoff["meta"]["contract_model"] == "north_star_contract + cards_seed + planning_seed + unknowns"
    assert init_handoff["meta"]["project_entry_state"] == "STATE.json"
    assert init_handoff["meta"]["team_manifest"] == "TEAM.toml"
    assert init_handoff["meta"]["changelog_file"] == "CHANGELOG.md"
    assert init_handoff["init_session"]["mode"] == "智能顾问团模式"
    assert init_handoff["init_session"]["mode_source"] == "user_selected"
    assert init_handoff["init_session"]["decision_owner"] == "user"
    assert init_handoff["init_session"]["advisor_agents"] == [
        ".codex/agents/小说家/金庸.md",
        ".codex/agents/导演/徐克.md",
    ]
    assert init_handoff["init_session"]["team_setup"]["team_mode"] == "per_stage"
    assert init_handoff["init_session"]["team_setup"]["roles"]["planning"]["members"] == [
        ".codex/agents/小说家/金庸.md",
        ".codex/agents/导演/徐克.md",
    ]
    assert init_handoff["init_session"]["team_setup"]["roles"]["production"]["members"] == []
    assert init_handoff["init_session"]["team_setup"]["roles"]["review"]["members"] == [".codex/agents/评审/博尔赫斯.md"]
    assert init_handoff["init_session"]["research_policy"] == "targeted-web-precision"
    assert "project.title" in init_handoff["sources_breakdown"]["user_confirmed"]
    assert "protagonist.name" in init_handoff["sources_breakdown"]["council_advised"]
    assert init_handoff["sources_breakdown"]["assistant_inferred"] == []
    assert init_handoff["cards_seed"]["character_seed"]["protagonist"]["name"] == "林默"
    assert init_handoff["planning_seed"]["story_engine"]["golden_finger_growth_rhythm"] == "慢热"
    assert "project.one_liner" not in init_handoff["unknowns"]["unresolved_questions"]
    assert init_handoff["north_star_ref"] == "Init/north_star_contract.json"
    assert "project_contract" not in init_handoff
    assert "project" not in init_handoff
    assert idea_bank["selected_idea"]["one_liner"] == "林默被迫在修仙规则副本里求生"
    assert idea_bank["constraints_inherited"]["opening_hook"] == "开篇第一夜就有人因误读规则暴毙"
    assert idea_bank["init_session"]["mode_source"] == "user_selected"
    assert idea_bank["init_session"]["decision_owner"] == "user"
    assert idea_bank["init_session"]["team_setup"]["roles"]["review"]["members"] == [".codex/agents/评审/博尔赫斯.md"]
    assert "- 模式：智能顾问团模式" in init_summary
    assert "- 模式来源：user_selected" in init_summary
    assert "- 顾问团布阵：三阶段分别指定" in init_summary
    assert "- 策划坐镇：.codex/agents/小说家/金庸.md, .codex/agents/导演/徐克.md" in init_summary
    assert "- 评审坐镇：.codex/agents/评审/博尔赫斯.md" in init_summary
    assert "- 初始化模式：智能顾问团模式" in confirmation_card
    assert "- 模式来源：user_selected" in confirmation_card
    assert "- 顾问团布阵：三阶段分别指定" in confirmation_card
    assert "## 文件角色" in init_summary
    assert "## 字段来源" in init_summary
    assert "## Unknowns" in init_summary
    assert "Deferred to Cards" in confirmation_card
    assert "- 主文件：`Init/north_star_contract.json`" in init_summary
    assert "- 项目入口状态：`STATE.json`（标准入口，指向运行态与关键工件路径）" in init_summary
    assert "- 长期对象约束：`Init/north_star_contract.json.cards`" in init_summary
    assert "- `STATE.json` 是项目入口状态清单，不替代 `.webnovel/state.json` 运行快照" in confirmation_card
    assert "`1-Cards` 是人物、世界、规则、物品的唯一 canonical" in confirmation_card
    assert "`north_star_contract.json.cards` 承担原全局卡的长期对象总规范。" in confirmation_card
    assert '["策划"]' in team_manifest
    assert '"智能顾问团" = true' in team_manifest
    assert '".codex/agents/小说家/金庸.md"' in team_manifest
    assert '".agents/skills/story/2-Planning"' in team_manifest
    assert '["监制"]' in team_manifest
    assert '"智能顾问团" = ""' in team_manifest
    assert '["评审"]' in team_manifest
    assert '".codex/agents/评审/博尔赫斯.md"' in team_manifest
    assert '"布阵模式" = "三阶段分别指定"' in team_manifest
    assert "## [Unreleased]" in changelog
    assert "- 建立 `STATE.json`、`TEAM.toml`、`CHANGELOG.md` 标准配置。" in changelog
    assert "原“全局卡/全局总览”概念已废弃" in (project_root / "Init" / "README.md").read_text(encoding="utf-8")
    assert (project_root / ".webnovel" / "tasks").is_dir()
    assert not (project_root / "Cards" / "1-全局总览").exists()
    assert not (project_root / "Init" / "世界观.md").exists()
    assert not (project_root / "Init" / "力量体系.md").exists()
    assert not (project_root / "Init" / "主角卡.md").exists()
    assert not (project_root / "Init" / "女主卡.md").exists()
    assert not (project_root / "Init" / "主角组.md").exists()
    assert not (project_root / "Init" / "金手指设计.md").exists()
    assert not (project_root / "Init" / "复合题材-融合逻辑.md").exists()
    assert not (project_root / "Init" / "反派设计.md").exists()
    assert "## 初始化合同快照" in legacy_outline
    assert "- 一句话故事：林默被迫在修仙规则副本里求生" in legacy_outline
    assert "- 开篇钩子：开篇第一夜就有人因误读规则暴毙" in legacy_outline
    assert "- 反套路规则：不用无脑碾压升级，而用规则理解差建立压迫感" in legacy_outline

    task_log = (project_root / ".webnovel" / "task_log.jsonl").read_text(encoding="utf-8").strip().splitlines()
    assert task_log
    first_row = json.loads(task_log[0])
    assert first_row["event"] == "project_initialized"
    assert first_row["payload"]["title"] == "测试小说"
    assert first_row["payload"]["init_mode"] == "智能顾问团模式"
    assert first_row["payload"]["mode_source"] == "user_selected"
    assert first_row["payload"]["decision_owner"] == "user"
    assert first_row["payload"]["init_contract_model"] == "north_star_contract+cards_seed+planning_seed+unknowns"
    assert first_row["payload"]["primary_init_artifact"] == "Init/north_star_contract.json"
    assert first_row["payload"]["project_entry_state_file"] == "STATE.json"
    assert first_row["payload"]["team_manifest_file"] == "TEAM.toml"
    assert first_row["payload"]["changelog_file"] == "CHANGELOG.md"
    assert first_row["payload"]["task_artifacts_root"] == ".webnovel/tasks"
    assert first_row["payload"]["planning_council_agents"] == [
        ".codex/agents/小说家/金庸.md",
        ".codex/agents/导演/徐克.md",
    ]
    assert first_row["payload"]["review_council_agents"] == [".codex/agents/评审/博尔赫斯.md"]
    assert first_row["payload"]["team_setup"]["team_mode"] == "per_stage"


def test_init_project_fast_mode_tracks_assistant_inference(tmp_path, monkeypatch):
    module = _load_module()

    monkeypatch.setattr(module, "is_git_available", lambda: False)
    monkeypatch.setattr(module, "write_current_project_pointer", lambda *_args, **_kwargs: None)

    project_root = tmp_path / "projects" / "快速模式书"
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

    state = json.loads((project_root / ".webnovel" / "state.json").read_text(encoding="utf-8"))
    handoff = json.loads((project_root / "Init" / "初始化简报.json").read_text(encoding="utf-8"))

    assert state["project_info"]["init_mode"] == "快速模式"
    assert state["project_info"]["mode_source"] == "user_selected"
    assert state["project_info"]["decision_owner"] == "assistant"
    assert handoff["init_session"]["mode"] == "快速模式"
    assert handoff["init_session"]["decision_owner"] == "assistant"
    assert "project.one_liner" in handoff["sources_breakdown"]["assistant_inferred"]
    assert "constraints.anti_trope" in handoff["sources_breakdown"]["assistant_inferred"]


def test_init_project_shared_council_shortcut_populates_all_team_sections(tmp_path, monkeypatch):
    module = _load_module()

    monkeypatch.setattr(module, "is_git_available", lambda: False)
    monkeypatch.setattr(module, "write_current_project_pointer", lambda *_args, **_kwargs: None)

    project_root = tmp_path / "projects" / "共享班底书"
    module.init_project(
        str(project_root),
        "共享班底书",
        "都市异能",
        init_mode="顾问团模式",
        mode_source="user_selected",
        decision_owner="user",
        shared_council_agents=".codex/agents/策划/王家卫.md,.codex/agents/编辑/张爱玲.md",
    )

    state = json.loads((project_root / ".webnovel" / "state.json").read_text(encoding="utf-8"))
    handoff = json.loads((project_root / "Init" / "初始化简报.json").read_text(encoding="utf-8"))
    team_manifest = (project_root / "TEAM.toml").read_text(encoding="utf-8")

    expected = [
        ".codex/agents/策划/王家卫.md",
        ".codex/agents/编辑/张爱玲.md",
    ]

    assert state["project_info"]["council_team_mode"] == "same_lineup"
    assert state["project_info"]["shared_council_agents"] == expected
    assert state["project_info"]["planning_council_agents"] == expected
    assert state["project_info"]["production_council_agents"] == expected
    assert state["project_info"]["review_council_agents"] == expected
    assert handoff["init_session"]["team_setup"]["team_mode"] == "same_lineup"
    assert handoff["init_session"]["team_setup"]["roles"]["production"]["members"] == expected
    assert handoff["init_session"]["team_setup"]["roles"]["review"]["members"] == expected
    assert '"布阵模式" = "同一套班底，三阶段通用"' in team_manifest
    assert '["监制"]' in team_manifest
    assert '["评审"]' in team_manifest
    assert '".codex/agents/策划/王家卫.md"' in team_manifest
    assert '".codex/agents/编辑/张爱玲.md"' in team_manifest


def test_init_project_autonomous_mode_defaults_mode_source_and_user_confirmed(tmp_path, monkeypatch):
    module = _load_module()

    monkeypatch.setattr(module, "is_git_available", lambda: False)
    monkeypatch.setattr(module, "write_current_project_pointer", lambda *_args, **_kwargs: None)

    project_root = tmp_path / "projects" / "自主模式书"
    module.init_project(
        str(project_root),
        "自主模式书",
        "悬疑",
        protagonist_name="周岚",
        target_words=250000,
        target_chapters=70,
        one_liner="周岚在封闭山城里追查失踪案",
    )

    state = json.loads((project_root / ".webnovel" / "state.json").read_text(encoding="utf-8"))
    handoff = json.loads((project_root / "Init" / "初始化简报.json").read_text(encoding="utf-8"))

    assert state["project_info"]["init_mode"] == "自主模式"
    assert state["project_info"]["mode_source"] == "defaulted"
    assert state["project_info"]["decision_owner"] == "user"
    assert handoff["init_session"]["mode_source"] == "defaulted"
    assert "project.title" in handoff["sources_breakdown"]["user_confirmed"]
    assert "protagonist.name" in handoff["sources_breakdown"]["user_confirmed"]
    assert handoff["sources_breakdown"]["assistant_inferred"] == []
    assert handoff["sources_breakdown"]["council_advised"] == []


def test_init_project_legacy_advisor_agents_fallbacks_to_planning_team(tmp_path, monkeypatch):
    module = _load_module()

    monkeypatch.setattr(module, "is_git_available", lambda: False)
    monkeypatch.setattr(module, "write_current_project_pointer", lambda *_args, **_kwargs: None)

    project_root = tmp_path / "projects" / "兼容旧字段书"
    module.init_project(
        str(project_root),
        "兼容旧字段书",
        "悬疑",
        init_mode="顾问团模式",
        advisor_agents=".codex/agents/小说家/阿城.md",
    )

    handoff = json.loads((project_root / "Init" / "初始化简报.json").read_text(encoding="utf-8"))
    team_setup = handoff["init_session"]["team_setup"]

    assert team_setup["team_mode"] == "legacy_planning_only"
    assert team_setup["planning_agents"] == [".codex/agents/小说家/阿城.md"]
    assert team_setup["production_agents"] == []
    assert team_setup["review_agents"] == []


def test_init_project_rejects_skill_directory_target(monkeypatch):
    module = _load_module()

    monkeypatch.setattr(module, "is_git_available", lambda: False)
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

    monkeypatch.setattr(module, "is_git_available", lambda: False)
    monkeypatch.setattr(module, "write_current_project_pointer", lambda *_args, **_kwargs: None)

    hidden_root = tmp_path / ".draft"
    normalized_root = tmp_path / "测试-书"
    module.init_project(str(hidden_root), "测试 书?", "修仙")

    assert not hidden_root.exists()
    assert normalized_root.exists()
    assert (normalized_root / ".webnovel" / "state.json").exists()
