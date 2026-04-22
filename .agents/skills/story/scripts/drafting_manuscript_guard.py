#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
drafting_manuscript_guard.py - chapter-complete manuscript guard for story2026 drafting

用途：
- 在 `3-Drafting` 收口前阻止“压缩版剧情稿/摘要稿”冒充 canonical 正文
- 提供一个可单独执行的章节完整度检查入口
"""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any, Optional

from chapter_paths import drafting_root_md_path
from project_locator import resolve_project_root
from runtime_compat import enable_windows_utf8_stdio, normalize_windows_path


DEFAULT_MIN_BODY_CHARS = 1500
DEFAULT_MIN_PARAGRAPHS = 6


def _strip_markdown_frontmatter(text: str) -> str:
    if not text.startswith("---"):
        return text
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        return text
    for index in range(1, len(lines)):
        if lines[index].strip() == "---":
            return "\n".join(lines[index + 1 :]).lstrip()
    return text


def _parse_markdown_frontmatter(text: str) -> dict[str, str]:
    if not text.startswith("---"):
        return {}
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        return {}
    out: dict[str, str] = {}
    for index in range(1, len(lines)):
        line = lines[index]
        if line.strip() == "---":
            return out
        if ":" not in line:
            continue
        key, value = line.split(":", 1)
        normalized_key = key.strip()
        if not normalized_key:
            continue
        out[normalized_key] = value.strip().strip('"').strip("'")
    return out


def _resolve_project_root(raw: Optional[str]) -> Path:
    if raw:
        return resolve_project_root(str(Path(normalize_windows_path(raw)).resolve()))
    return resolve_project_root()


def _expected_hook_from_planning(planning_path: Path) -> str:
    if not planning_path.is_file():
        return ""
    text = planning_path.read_text(encoding="utf-8")
    match = re.search(r"对下章的直接推动：([^\n]+)", text)
    return match.group(1).strip() if match else ""


def _paragraphs(body: str) -> list[str]:
    content = body.strip()
    if not content:
        return []
    raw_chunks = re.split(r"\n\s*\n", content)
    return [
        chunk.strip()
        for chunk in raw_chunks
        if chunk.strip() and not chunk.strip().startswith("#")
    ]


def validate_manuscript(
    manuscript_path: Path,
    *,
    planning_path: Optional[Path] = None,
    min_body_chars: int = DEFAULT_MIN_BODY_CHARS,
    min_paragraphs: int = DEFAULT_MIN_PARAGRAPHS,
) -> dict[str, Any]:
    if not manuscript_path.is_file():
        return {
            "status": "block",
            "reason": "missing_manuscript",
            "issues": [{"code": "missing_manuscript", "message": f"missing manuscript: {manuscript_path}"}],
        }

    text = manuscript_path.read_text(encoding="utf-8")
    frontmatter = _parse_markdown_frontmatter(text)
    body = _strip_markdown_frontmatter(text)
    body_chars = len(re.sub(r"\s+", "", body))
    paragraphs = _paragraphs(body)
    heading_present = bool(re.search(r"^#\s+第\d+集", body, re.M))
    expected_hook = _expected_hook_from_planning(planning_path) if planning_path else ""

    issues: list[dict[str, str]] = []
    if not heading_present:
        issues.append({"code": "missing_heading", "message": "missing canonical chapter heading"})
    if body_chars < max(1, int(min_body_chars)):
        issues.append(
            {
                "code": "body_too_short",
                "message": f"body chars {body_chars} < min {min_body_chars}",
            }
        )
    if len(paragraphs) < max(1, int(min_paragraphs)):
        issues.append(
            {
                "code": "paragraphs_too_few",
                "message": f"paragraphs {len(paragraphs)} < min {min_paragraphs}",
            }
        )
    if expected_hook and expected_hook not in body:
        issues.append(
            {
                "code": "missing_exit_hook",
                "message": f"missing planning exit hook: {expected_hook}",
            }
        )
    if not frontmatter.get("episode_title"):
        issues.append({"code": "missing_episode_title", "message": "frontmatter missing episode_title"})
    if not frontmatter.get("rhythm_type"):
        issues.append({"code": "missing_rhythm_type", "message": "frontmatter missing rhythm_type"})

    return {
        "status": "pass" if not issues else "block",
        "reason": "chapter_complete_manuscript_passed" if not issues else "chapter_complete_manuscript_failed",
        "manuscript_path": str(manuscript_path),
        "planning_path": str(planning_path) if planning_path else "",
        "metrics": {
            "body_chars": body_chars,
            "paragraphs": len(paragraphs),
            "min_body_chars": min_body_chars,
            "min_paragraphs": min_paragraphs,
        },
        "expected_exit_hook": expected_hook,
        "issues": issues,
    }


def validate_project_chapter(
    project_root: Path,
    chapter_num: int,
    *,
    planning_path: Optional[Path] = None,
    min_body_chars: int = DEFAULT_MIN_BODY_CHARS,
    min_paragraphs: int = DEFAULT_MIN_PARAGRAPHS,
) -> dict[str, Any]:
    manuscript_path = drafting_root_md_path(project_root, chapter_num)
    resolved_planning = planning_path
    if resolved_planning is None:
        frontmatter = _parse_markdown_frontmatter(manuscript_path.read_text(encoding="utf-8")) if manuscript_path.is_file() else {}
        planning_ref = str(frontmatter.get("planning_ref") or "").strip()
        if planning_ref:
            resolved_planning = project_root / planning_ref
    return validate_manuscript(
        manuscript_path,
        planning_path=resolved_planning,
        min_body_chars=min_body_chars,
        min_paragraphs=min_paragraphs,
    )


def main(argv: Optional[list[str]] = None) -> int:
    parser = argparse.ArgumentParser(description="chapter-complete manuscript guard")
    parser.add_argument("--project-root", help="project root path")
    parser.add_argument("--chapter", type=int, help="chapter / episode number")
    parser.add_argument("--manuscript", help="explicit manuscript path")
    parser.add_argument("--planning", help="explicit planning chapter path")
    parser.add_argument("--min-body-chars", type=int, default=DEFAULT_MIN_BODY_CHARS)
    parser.add_argument("--min-paragraphs", type=int, default=DEFAULT_MIN_PARAGRAPHS)
    args = parser.parse_args(argv)

    if args.manuscript:
        manuscript_path = Path(normalize_windows_path(args.manuscript)).resolve()
        planning_path = Path(normalize_windows_path(args.planning)).resolve() if args.planning else None
        result = validate_manuscript(
            manuscript_path,
            planning_path=planning_path,
            min_body_chars=args.min_body_chars,
            min_paragraphs=args.min_paragraphs,
        )
    else:
        if not args.chapter:
            raise SystemExit("--chapter is required when --manuscript is omitted")
        project_root = _resolve_project_root(args.project_root)
        planning_path = Path(normalize_windows_path(args.planning)).resolve() if args.planning else None
        result = validate_project_chapter(
            project_root,
            args.chapter,
            planning_path=planning_path,
            min_body_chars=args.min_body_chars,
            min_paragraphs=args.min_paragraphs,
        )

    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result.get("status") == "pass" else 2


if __name__ == "__main__":
    enable_windows_utf8_stdio(skip_in_pytest=True)
    raise SystemExit(main())
