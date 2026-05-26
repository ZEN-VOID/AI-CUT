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
    "全局风格解析.md": "# 全局风格解析",
    "编剧风格解析.md": "# 编剧风格解析",
    "摄影风格解析.md": "# 摄影风格解析",
    "设计风格解析.md": "# 设计风格解析",
}

# All outputs now land in the same shot-by-shot/<reference_slug>/ directory
# No separate CONTEXT/ path anymore.

STORYBOARD_COLUMNS = (
    "镜号",
    "时长",
    "画面描述",
    "角色1",
    "角色描述1",
    "角色图1",
    "角色2",
    "角色描述2",
    "角色图2",
    "参考",
    "景别",
    "角色动作",
    "情绪",
    "场景标签",
    "光影氛围",
    "音效",
    "对白",
    "分镜提示词",
    "视频运动提示词",
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("path", help="Path to shot-by-shot.md")
    parser.add_argument(
        "--context-root",
        help="Optional path to shot-by-shot/<reference_slug> (legacy: previously used CONTEXT/shot-by-shot/<reference_slug>/).",
    )
    return parser.parse_args()


def infer_context_root(path: Path) -> Path | None:
    """Infer the shot-by-shot/<reference_slug> root from the main report path.

    Legacy: Previously the four analysis docs landed in CONTEXT/shot-by-shot/<slug>/.
    Current: All outputs land in shot-by-shot/<reference_slug>/ alongside the main report.
    This function now returns the same directory as the main report (no separate CONTEXT/).
    """
    parts = path.parts
    try:
        projects_index = parts.index("projects")
        shot_index = parts.index("shot-by-shot", projects_index)
    except ValueError:
        return None

    if shot_index + 1 >= len(parts):
        return None

    # All outputs are in the same shot-by-shot/<reference_slug> directory
    project_root = Path(*parts[:shot_index])
    reference_slug = parts[shot_index + 1]
    return project_root / "shot-by-shot" / reference_slug


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

    if "分镜脚本.md" in text:
        storyboard_path = path.parent / "分镜脚本.md"
        if not storyboard_path.is_file():
            print(f"missing storyboard script: {storyboard_path}", file=sys.stderr)
            return 1
        storyboard_text = storyboard_path.read_text(encoding="utf-8")
        if "# 分镜脚本" not in storyboard_text:
            print(f"missing heading in {storyboard_path}: # 分镜脚本", file=sys.stderr)
            return 1
        header = "| " + " | ".join(STORYBOARD_COLUMNS) + " |"
        if header not in storyboard_text:
            print("storyboard table columns do not match Numbers example", file=sys.stderr)
            return 1

    print(f"ok: {path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
