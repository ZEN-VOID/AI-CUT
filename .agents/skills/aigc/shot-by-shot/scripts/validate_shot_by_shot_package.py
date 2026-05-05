#!/usr/bin/env python3
"""Mechanical validator for shot-by-shot Markdown packages."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path


REQUIRED_MAIN_SECTIONS = (
    "## 思考过程",
    "## 素材证据",
    "## 逐镜拆解表",
    "## 临摹原则",
    "## 禁止照搬清单",
)

CONTEXT_OUTPUTS = {
    "画面风格解析.md": "# 画面风格解析",
    "编导解析.md": "# 编导解析",
    "摄影解析.md": "# 摄影解析",
    "设计解析.md": "# 设计解析",
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("path", help="Path to shot-by-shot.md")
    parser.add_argument(
        "--context-root",
        help="Optional path to CONTEXT/shot-by-shot/<reference_slug>.",
    )
    return parser.parse_args()


def infer_context_root(path: Path) -> Path | None:
    parts = path.parts
    try:
        projects_index = parts.index("projects")
        shot_index = parts.index("shot-by-shot", projects_index)
    except ValueError:
        return None

    if shot_index + 1 >= len(parts):
        return None

    project_root = Path(*parts[:shot_index])
    reference_slug = parts[shot_index + 1]
    return project_root / "CONTEXT" / "shot-by-shot" / reference_slug


def main() -> int:
    args = parse_args()
    path = Path(args.path)
    if not path.is_file():
        print(f"missing file: {path}", file=sys.stderr)
        return 2

    text = path.read_text(encoding="utf-8")
    failures = [section for section in REQUIRED_MAIN_SECTIONS if section not in text]
    if failures:
        for section in failures:
            print(f"missing section: {section}", file=sys.stderr)
        return 1

    context_root = Path(args.context_root) if args.context_root else infer_context_root(path)
    if context_root is not None:
        for filename, heading in CONTEXT_OUTPUTS.items():
            if filename not in text:
                continue
            context_file = context_root / filename
            if not context_file.is_file():
                print(f"missing context analysis: {context_file}", file=sys.stderr)
                return 1
            context_text = context_file.read_text(encoding="utf-8")
            if heading not in context_text:
                print(f"missing heading in {context_file}: {heading}", file=sys.stderr)
                return 1

    print(f"ok: {path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
