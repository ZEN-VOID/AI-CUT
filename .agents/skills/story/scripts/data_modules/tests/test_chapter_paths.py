#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
from pathlib import Path


def _load_module():
    scripts_dir = Path(__file__).resolve().parents[2]
    if str(scripts_dir) not in sys.path:
        sys.path.insert(0, str(scripts_dir))

    import chapter_paths

    return chapter_paths


def test_default_chapter_draft_path_uses_outline_heading_title(tmp_path):
    module = _load_module()

    planning_dir = tmp_path / "2-Planning"
    planning_dir.mkdir(parents=True, exist_ok=True)
    (planning_dir / "全息地图.json").write_text(
        """
        {
          "schema_version": "story2026/holomap/v1",
          "content": {
            "holomap": {
              "chapter_boards": [
                {"chapter": 1, "title": "测试标题", "summary": "测试大纲"}
              ]
            }
          }
        }
        """,
        encoding="utf-8",
    )

    draft_path = module.default_chapter_draft_path(tmp_path, 1)

    assert draft_path == tmp_path / "3-Drafting" / "第1集.md"


def test_default_chapter_draft_path_falls_back_to_split_outline_filename(tmp_path):
    module = _load_module()

    outline_dir = tmp_path / "2-Planning" / "legacy"
    outline_dir.mkdir(parents=True, exist_ok=True)
    (outline_dir / "第0002章-标题 文件.md").write_text("无章节标题 heading", encoding="utf-8")

    draft_path = module.default_chapter_draft_path(tmp_path, 2)

    assert draft_path == tmp_path / "3-Drafting" / "第2集.md"


def test_find_chapter_file_prefers_3_drafting_root(tmp_path):
    module = _load_module()

    canonical_path = tmp_path / "3-Drafting" / "第3集.md"
    canonical_path.parent.mkdir(parents=True, exist_ok=True)
    canonical_path.write_text("正文", encoding="utf-8")

    legacy_path = tmp_path / "正文" / "第0003章-山雨欲来.md"
    legacy_path.parent.mkdir(parents=True, exist_ok=True)
    legacy_path.write_text("旧正文", encoding="utf-8")

    found = module.find_chapter_file(tmp_path, 3)

    assert found == canonical_path


def test_find_chapter_file_supports_titled_flat_filename(tmp_path):
    module = _load_module()

    chapter_path = tmp_path / "正文" / "第0003章-山雨欲来.md"
    chapter_path.parent.mkdir(parents=True, exist_ok=True)
    chapter_path.write_text("正文", encoding="utf-8")

    found = module.find_chapter_file(tmp_path, 3)

    assert found == chapter_path


def test_drafting_root_md_path_uses_ascii_chapter_workspace(tmp_path):
    module = _load_module()

    root_path = module.drafting_root_md_path(tmp_path, 7)

    assert root_path == tmp_path / "3-Drafting" / "第7集.md"
