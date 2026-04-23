#!/usr/bin/env python3
"""Validate `3-Detail` creative-guidance references for single-skill mode."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path


REQUIRED_FILES = (
    "references/路由画像.yaml",
    "references/正反例.md",
    "references/创作评审标尺.md",
    "references/validation-report-closure-guide.md",
    "references/编剧手册.md",
    "references/镜头语言.md",
    "references/电影学院派知识接线.md",
)
REQUIRED_SHARED_REF = ".agents/skills/aigc/3-Detail/_shared/creative-guidance-contract.md"
REQUIRED_ROUTE_KEYS = (
    "profile_goal:",
    "default_strategy:",
    "route_profiles:",
    "signal_id:",
)
REQUIRED_SKILL_PHRASES = (
    "references/路由画像.yaml",
    "references/正反例.md",
    "references/创作评审标尺.md",
    "references/电影学院派知识接线.md",
    "references/validation-report-closure-guide.md",
)


def validate_stage_root(stage_root: Path) -> list[str]:
    errors: list[str] = []
    skill_path = stage_root / "SKILL.md"
    shared_contract = stage_root / "_shared" / "creative-guidance-contract.md"

    if not skill_path.exists():
        return [f"{skill_path}: 缺少根 SKILL.md。"]
    if not shared_contract.exists():
        errors.append(f"{shared_contract}: 缺少共享创作引导合同。")

    skill_text = skill_path.read_text(encoding="utf-8")
    if REQUIRED_SHARED_REF not in skill_text:
        errors.append(f"{skill_path}: 未回指 `{REQUIRED_SHARED_REF}`。")
    for phrase in REQUIRED_SKILL_PHRASES:
        if phrase not in skill_text:
            errors.append(f"{skill_path}: 缺少关键 reference 引用 `{phrase}`。")

    route_path = stage_root / REQUIRED_FILES[0]
    if route_path.exists():
        route_text = route_path.read_text(encoding="utf-8")
        for key in REQUIRED_ROUTE_KEYS:
            if key not in route_text:
                errors.append(f"{route_path}: 缺少路由键 `{key}`。")

    for rel_path in REQUIRED_FILES[1:]:
        file_path = stage_root / rel_path
        if not file_path.exists():
            errors.append(f"{file_path}: 缺少必需 creative reference。")
            continue
        text = file_path.read_text(encoding="utf-8")
        if rel_path.endswith("电影学院派知识接线.md"):
            for marker in ("Pass Mapping", "Translation Rules", "knowledge-base/电影学院派"):
                if marker not in text:
                    errors.append(f"{file_path}: 缺少学院派知识接线关键段 `{marker}`。")
            continue
        if rel_path.endswith("validation-report-closure-guide.md"):
            for marker in ("思考过程", "关键证据", "风险/例外", "下一入口"):
                if marker not in text:
                    errors.append(f"{file_path}: closure guide 缺少关键槽位 `{marker}`。")
            continue
        if "分镜构图" not in text and "结构" not in text and "角色表现" not in text:
            errors.append(f"{file_path}: 应至少回链到结构或 `分镜构图` 先行规则。")

    return errors


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Validate `3-Detail` single-skill creative-guidance references."
    )
    parser.add_argument(
        "stage_root",
        nargs="?",
        type=Path,
        help="Optional stage root path; defaults to `.agents/skills/aigc/3-Detail`.",
    )
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()

    script_path = Path(__file__).resolve()
    default_stage_root = script_path.parent.parent
    stage_root = (args.stage_root or default_stage_root).resolve()

    errors = validate_stage_root(stage_root)
    if errors:
        print("校验失败:")
        for error in errors:
            print(f"- {error}")
        return 1

    print(f"PASS: 3-Detail 创作引导 references 校验通过。root={stage_root.name}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
