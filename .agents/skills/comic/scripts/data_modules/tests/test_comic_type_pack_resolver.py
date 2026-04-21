#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from pathlib import Path
import sys


def _load_module():
    scripts_dir = Path(__file__).resolve().parents[2]
    if str(scripts_dir) not in sys.path:
        sys.path.insert(0, str(scripts_dir))
    from data_modules.comic_type_pack_resolver import TypePackResolver, infer_type_stack, resolve_stage_projection

    return TypePackResolver, infer_type_stack, resolve_stage_projection


def test_infer_type_stack_for_chunibyo_battle():
    _, infer_fn, _ = _load_module()
    stack = infer_fn(genre="中二战斗+黑暗奇幻", platform="条漫", target_audience="少年热血")
    assert stack["primary"] == "漫画高冲击"
    assert "中二战斗" in stack["secondary"]
    assert "黑暗奇幻" in stack["secondary"]
    assert "条漫平台" in stack["platform"]
    assert "少年热血受众" in stack["audience"]
    comedy_stack = infer_fn(genre="喜剧", platform="", target_audience="")
    assert "搞笑颜艺" in comedy_stack["secondary"]


def test_resolver_collects_stage_projection():
    TypePackResolver, _, resolve_stage_projection = _load_module()
    resolver = TypePackResolver()
    profile = resolver.resolve(
        {
            "method_kernel": "comic-core-v1",
            "base": "_base",
            "primary": "漫画高冲击",
            "secondary": ["中二战斗"],
            "platform": ["条漫平台"],
            "audience": ["少年热血受众"],
        }
    )
    assert profile["active_packs"][0] == "_base"
    assert "中二战斗" in profile["active_packs"]
    assert profile["resolution_mode"] == "dynamic-directory-discovery-comic-type-pack"
    assert profile["knowledge_refs"]
    assert any("漫画/中二战斗/中二战斗.md" in ref for ref in profile["knowledge_refs"])
    assert profile["pack_revisions"].get("中二战斗")
    projection = resolve_stage_projection(profile, "script_adaptation")
    assert projection.get("adaptation_posture") in {"comic-first", None}
