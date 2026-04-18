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


def test_init_project_creates_five_init_files_and_inlines_workflow_runtime(tmp_path, monkeypatch):
    module = _load_module()

    monkeypatch.setattr(module, "is_git_available", lambda: False)
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
    legacy_outline = (project_root / "Planning" / "legacy" / "总纲.md").read_text(encoding="utf-8")

    assert state["project_name"] == "测试小说"
    assert state["current_stage"] == "0-Init"
    assert state["recommended_next_stage"] == "1-Cards"
    assert state["main_artifacts"]["north_star"] == "0-Init/north_star.yaml"
    assert state["main_artifacts"]["story_source_manifest"] == "0-Init/story-source-manifest.yaml"
    assert state["main_artifacts"]["init_handoff"] == "0-Init/init_handoff.yaml"
    assert state["main_artifacts"]["team"] == "team.yaml"
    assert state["workflow_runtime"]["workflow_state"]["current_task"] is None
    assert state["workflow_runtime"]["execution_state"]["active_run_id"] is None
    assert state["workflow_runtime"]["execution_state"]["stage_progress"]["0-init"]["stage_label"] == "初始化"
    assert state["workflow_runtime"]["task_log"][0]["event"] == "project_initialized"

    assert team_manifest["init_contract"]["init_mode"] == "team_roleplay"
    assert team_manifest["init_contract"]["team_lineup_mode"] == "custom"
    assert team_manifest["init_contract"]["selector_scope_root"] == ".agents/skills/team/"
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
    assert north_star["type_stack"]["primary"] == "网文高冲击"
    assert "修仙" in north_star["type_stack"]["secondary"]
    assert "规则怪谈" in north_star["type_stack"]["secondary"]

    assert source_manifest["primary_story_source"]["status"] == "missing"
    assert source_manifest["readiness"]["can_enter_cards"] is True
    assert source_manifest["readiness"]["can_enter_planning"] is True

    assert init_handoff["north_star_ref"] == "0-Init/north_star.yaml"
    assert init_handoff["story_source_manifest_ref"] == "0-Init/story-source-manifest.yaml"
    assert init_handoff["team_ref"] == "team.yaml"
    assert init_handoff["project_contract"]["recommended_next_stage"] == "1-Cards"
    assert init_handoff["stage_entry_seeds"]["cards_seed"]["character_seed"]["protagonist"]["name"] == "林默"
    assert init_handoff["stage_entry_seeds"]["planning_seed"]["story_engine"]["golden_finger_growth_rhythm"] == "慢热"
    assert init_handoff["stage_entry_seeds"]["planning_seed"]["type_stack"]["primary"] == "网文高冲击"

    assert "写入 `0-Init/north_star.yaml`、`0-Init/story-source-manifest.yaml`、`0-Init/init_handoff.yaml` 初始化三件套。" in changelog
    assert "## 初始化合同快照" in legacy_outline

    assert not (project_root / ".webnovel" / "workflow_state.json").exists()
    assert not (project_root / ".webnovel" / "execution_state.json").exists()
    assert not (project_root / ".webnovel" / "task_log.jsonl").exists()
    assert not (project_root / ".webnovel" / "tasks").exists()


def test_init_project_tracks_assistant_inference_in_handoff(tmp_path, monkeypatch):
    module = _load_module()
    monkeypatch.setattr(module, "is_git_available", lambda: False)
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


def test_init_project_infers_expanded_legacy_type_packs(tmp_path, monkeypatch):
    module = _load_module()
    monkeypatch.setattr(module, "is_git_available", lambda: False)
    monkeypatch.setattr(module, "write_current_project_pointer", lambda *_args, **_kwargs: None)

    project_root = tmp_path / "projects" / "story" / "旧题材映射书"
    module.init_project(
        str(project_root),
        "旧题材映射书",
        "古言+狗血言情+末世+知乎短篇",
        target_reader="女频",
        target_words=120000,
        target_chapters=36,
        one_liner="一座失控古城里，皇族遗脉在规则崩塌后求生并复仇。",
    )

    north_star = _load_yaml(project_root / "0-Init" / "north_star.yaml")
    stack = north_star["type_stack"]
    assert "古言剧" in stack["secondary"]
    assert "狗血言情" in stack["secondary"]
    assert "末世" in stack["secondary"]
    assert "知乎短篇" in stack["secondary"]


def test_init_project_shared_council_shortcut_populates_all_team_sections(tmp_path, monkeypatch):
    module = _load_module()
    monkeypatch.setattr(module, "is_git_available", lambda: False)
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


def test_init_project_allows_explicit_type_stack_override(tmp_path, monkeypatch):
    module = _load_module()
    monkeypatch.setattr(module, "is_git_available", lambda: False)
    monkeypatch.setattr(module, "write_current_project_pointer", lambda *_args, **_kwargs: None)

    project_root = tmp_path / "projects" / "story" / "显式类型包书"
    module.init_project(
        str(project_root),
        "显式类型包书",
        "都市",
        target_reader="大众",
        platform="任意平台",
        type_pack_primary="网文高冲击",
        type_pack_secondary="都市复仇,规则悬疑",
        type_pack_platform="起点连载",
        type_pack_audience="男频快节奏",
        type_pack_notes="user_override",
    )

    north_star = _load_yaml(project_root / "0-Init" / "north_star.yaml")
    stack = north_star["type_stack"]
    assert stack["primary"] == "网文高冲击"
    assert stack["secondary"] == ["都市复仇", "规则悬疑"]
    assert stack["platform"] == ["起点连载"]
    assert stack["audience"] == ["男频快节奏"]
    assert stack["inferred"] is False


def test_init_project_defaults_mode_source_and_user_confirmed(tmp_path, monkeypatch):
    module = _load_module()
    monkeypatch.setattr(module, "is_git_available", lambda: False)
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


def test_init_project_legacy_advisor_agents_fallbacks_to_planning_team(tmp_path, monkeypatch):
    module = _load_module()
    monkeypatch.setattr(module, "is_git_available", lambda: False)
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
    assert (normalized_root / "STATE.json").exists()
    assert (normalized_root / "0-Init" / "north_star.yaml").exists()
