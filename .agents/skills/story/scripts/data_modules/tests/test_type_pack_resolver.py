#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from pathlib import Path
import sys


def _load_module():
    scripts_dir = Path(__file__).resolve().parents[2]
    if str(scripts_dir) not in sys.path:
        sys.path.insert(0, str(scripts_dir))
    from data_modules.type_pack_resolver import TypePackResolver, infer_type_stack, resolve_stage_projection

    return TypePackResolver, infer_type_stack, resolve_stage_projection


def test_infer_type_stack_from_fields():
    _, infer_fn, _ = _load_module()
    stack = infer_fn(genre="修仙+规则怪谈", platform="起点", target_reader="男频快节奏")
    assert stack["primary"] == "网文高冲击"
    assert "修仙" in stack["secondary"]
    assert "规则怪谈" in stack["secondary"]
    assert "起点连载" in stack["platform"]
    assert "男频快节奏" in stack["audience"]


def test_type_pack_resolver_uses_explicit_north_star_stack(tmp_path):
    TypePackResolver, _, _ = _load_module()
    init_dir = tmp_path / "0-Init"
    init_dir.mkdir(parents=True, exist_ok=True)
    (init_dir / "north_star.yaml").write_text(
        "\n".join(
            [
                "type_stack:",
                "  method_kernel: story-core-v1",
                "  base: _base",
                "  primary: 网文高冲击",
                "  secondary: [修仙]",
                "  platform: [起点连载]",
                "  audience: [男频快节奏]",
            ]
        ),
        encoding="utf-8",
    )

    resolver = TypePackResolver(tmp_path)
    profile = resolver.resolve()
    assert profile["active_packs"] == [
        "_base",
        "网文高冲击",
        "修仙",
        "起点连载",
        "男频快节奏",
    ]
    assert profile.get("resolution_mode") == "directory-first-bootstrap"
    assert not profile.get("pack_catalog_ref")
    refs = profile.get("knowledge_refs") or []
    assert any("网文/修仙/修仙.md" in str(item) for item in refs)


def test_infer_type_stack_absorbs_legacy_genre_cluster():
    _, infer_fn, _ = _load_module()
    stack = infer_fn(genre="古言+狗血言情+末世+知乎短篇", platform="", target_reader="女频")
    assert "古言剧" in stack["secondary"]
    assert "狗血言情" in stack["secondary"]
    assert "末世" in stack["secondary"]
    assert "知乎短篇" in stack["secondary"]


def test_type_pack_resolver_merges_knowledge_refs(tmp_path):
    TypePackResolver, _, _ = _load_module()
    init_dir = tmp_path / "0-Init"
    init_dir.mkdir(parents=True, exist_ok=True)
    (init_dir / "north_star.yaml").write_text(
        "\n".join(
            [
                "type_stack:",
                "  method_kernel: story-core-v1",
                "  base: _base",
                "  primary: 网文高冲击",
                "  secondary: [古言剧, 现实题材]",
                "  platform: []",
                "  audience: []",
            ]
        ),
        encoding="utf-8",
    )

    resolver = TypePackResolver(tmp_path)
    profile = resolver.resolve()
    refs = profile.get("knowledge_refs") or []
    assert any("网文/古言剧/ancient-dialogue.md" in str(item) for item in refs)
    assert any("网文/现实题材/character-depth.md" in str(item) for item in refs)
    assert profile.get("knowledge_digest")


def test_all_legacy_genre_files_are_absorbed_into_type_pack_indexes():
    legacy_root = Path(".agents/skills/story_backup/templates/genres")
    current_root = Path(".agents/skills/story/type-packs/网文")

    missing = []
    for path in legacy_root.glob("*.md"):
        if path.name == "README.md":
            continue
        current = current_root / path.stem / path.name
        if not current.is_file():
            missing.append(str(current))

    assert not missing, f"legacy entry files not yet landed under 网文/: {missing}"


def test_resolve_stage_projection_prefers_step_specific_hooks(tmp_path):
    TypePackResolver, _, resolve_stage_projection = _load_module()
    init_dir = tmp_path / "0-Init"
    init_dir.mkdir(parents=True, exist_ok=True)
    (init_dir / "north_star.yaml").write_text(
        "\n".join(
            [
                "type_stack:",
                "  method_kernel: story-core-v1",
                "  base: _base",
                "  primary: 网文高冲击",
                "  secondary: [直播文]",
                "  platform: []",
                "  audience: []",
            ]
        ),
        encoding="utf-8",
    )

    resolver = TypePackResolver(tmp_path)
    profile = resolver.resolve()
    projection = resolve_stage_projection(profile, "drafting", current_step_id="Step 5")
    assert projection.get("current_step_id") == "Step 5"
    assert isinstance(projection, dict)


def test_webnovel_family_dirs_exist_for_current_shared_craft():
    current_root = Path(".agents/skills/story/type-packs/网文")
    expected = {"狗血言情", "古言剧", "现实题材", "玄幻剧", "侦探剧", "知乎短篇"}
    existing = {path.name for path in current_root.iterdir() if path.is_dir()}
    assert expected <= existing


def test_infer_type_stack_covers_selected_legacy_genres():
    _, infer_fn, _ = _load_module()
    cases = {
        "电竞": {"secondary": {"电竞"}},
        "直播文": {"primary": "网文高冲击", "secondary": {"直播文"}},
        "都市日常": {"secondary": {"都市日常"}},
        "抗战谍战": {"secondary": {"抗战谍战"}},
        "民国言情": {"secondary": {"民国言情"}},
        "豪门总裁": {"secondary": {"豪门总裁"}},
        "种田": {"secondary": {"种田"}},
    }

    for genre, expected in cases.items():
        stack = infer_fn(genre=genre, platform="", target_reader="")
        if "primary" in expected:
            assert stack.get("primary") == expected["primary"]
        if "secondary" in expected:
            assert expected["secondary"] <= set(stack.get("secondary") or [])
