#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from pathlib import Path
import importlib.util
import sys
import yaml


def _load_module():
    scripts_dir = Path(__file__).resolve().parents[2]
    if str(scripts_dir) not in sys.path:
        sys.path.insert(0, str(scripts_dir))
    from data_modules.comic_type_pack_resolver import TypePackResolver, infer_type_stack, resolve_stage_projection

    return TypePackResolver, infer_type_stack, resolve_stage_projection


def _load_script_module(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    assert spec is not None and spec.loader is not None
    spec.loader.exec_module(module)
    return module


def test_infer_type_stack_for_single_layer_taxonomy():
    _, infer_fn, _ = _load_module()
    stack = infer_fn(
        genre="少年战斗冒险+黑暗奇幻",
        platform="条漫",
        target_audience="少年热血",
        tone="中二 高冲击",
    )
    assert stack["primary"] == "经典漫画叙事"
    assert "少年战斗冒险" in stack["secondary"]
    assert "黑暗奇幻" in stack["secondary"]
    assert "条漫平台" in stack["platform"]
    assert "少年热血受众" in stack["audience"]


def test_resolver_collects_single_layer_genre_projection():
    TypePackResolver, _, resolve_stage_projection = _load_module()
    resolver = TypePackResolver()
    profile = resolver.resolve(
        {
            "method_kernel": "comic-core-v1",
            "base": "_base",
            "primary": "经典漫画叙事",
            "secondary": ["少年战斗冒险"],
            "platform": ["条漫平台"],
            "audience": ["少年热血受众"],
        }
    )
    assert profile["active_packs"][0] == "_base"
    assert "少年战斗冒险" in profile["active_packs"]
    assert profile["resolution_mode"] == "single-layer-genre-comic-type-pack"
    assert any("漫画/少年战斗冒险/少年战斗冒险.md" in ref for ref in profile["knowledge_refs"])
    assert profile["pack_revisions"].get("少年战斗冒险")
    assert isinstance(profile.get("control_surface"), dict)
    assert isinstance(profile.get("control_surface_digest"), list) and profile["control_surface_digest"]
    assert isinstance(profile["control_surface"].get("page_turn_mechanism"), dict)
    projection = resolve_stage_projection(profile, "script_adaptation")
    assert projection.get("adaptation_posture") in {"genre-led", None}


def test_all_genre_meta_files_expose_control_surface():
    root = Path(__file__).resolve().parents[3] / "2-九刀流漫画提示词" / "types" / "漫画"
    expected_keys = {
        "conflict_engine",
        "role_matrix",
        "page_turn_mechanism",
        "panel_grammar",
        "visual_carrier",
        "dialogue_register",
        "motif_system",
        "failure_modes",
    }
    for meta_path in sorted(root.glob("*/meta.yaml")):
        data = yaml.safe_load(meta_path.read_text(encoding="utf-8"))
        assert isinstance(data, dict), meta_path
        surface = data.get("control_surface")
        assert isinstance(surface, dict), meta_path
        assert expected_keys.issubset(surface.keys()), meta_path


def test_all_genre_main_docs_cover_control_surface_sections():
    root = Path(__file__).resolve().parents[3] / "2-九刀流漫画提示词" / "types" / "漫画"
    required_headings = [
        "## 核心冲突引擎",
        "## 角色原型",
        "## 翻页机制",
        "## 信息主载体",
        "## 对白与旁白",
        "## 母题系统",
        "## 禁写模式",
    ]
    for genre_dir in sorted(path for path in root.iterdir() if path.is_dir()):
        main_doc = genre_dir / f"{genre_dir.name}.md"
        assert main_doc.is_file(), genre_dir
        text = main_doc.read_text(encoding="utf-8")
        for heading in required_headings:
            assert heading in text, f"{main_doc} missing {heading}"


def test_seedream_master_prompt_consumes_control_surface():
    script_path = Path(__file__).resolve().parents[3] / "3-漫画生成/scripts/run_seedream_comic_generation.py"
    module = _load_script_module(script_path, "run_seedream_comic_generation_test")
    sample = module._self_test_data()
    prompt = module.compile_master_prompt(sample)
    assert "Type Pack Control Surface" in prompt
    assert "control_surface.conflict_engine.premise" in prompt
    assert "control_surface.page_turn_mechanism.turn_trigger" in prompt


def test_episode_poster_validator_uses_imagegen_handoff():
    script_path = Path(__file__).resolve().parents[3] / "4-剧集海报/scripts/validate_episode_poster_json.py"
    module = _load_script_module(script_path, "validate_episode_poster_json_test")
    assert module.IMAGEGEN_SKILL_PATH == ".agents/skills/cli/imagegen"
