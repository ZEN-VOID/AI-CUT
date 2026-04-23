#!/usr/bin/env python3
"""Validate `3-Detail` reference-module structure for single-skill mode."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path


REQUIRED_FILES = (
    "references/思行网络.md",
    "references/能力通道图谱.yaml",
    "references/模板字段填写指南.md",
    "references/编剧手册.md",
    "references/镜头语言.md",
)
REQUIRED_SHARED_REF = ".agents/skills/aigc/3-Detail/_shared/node-pack-contract.md"
REQUIRED_SKILL_PHRASES = (
    "固定先执行 `1-分镜构图`",
    "references/能力通道图谱.yaml",
    "references/模板字段填写指南.md",
)
REQUIRED_YAML_KEYS = (
    "ordered_passes:",
    "pass_writes:",
    "required_before_projection:",
    "forbidden_overlap:",
)


def validate_stage_root(stage_root: Path) -> list[str]:
    errors: list[str] = []
    skill_path = stage_root / "SKILL.md"
    shared_contract = stage_root / "_shared" / "node-pack-contract.md"

    if not skill_path.exists():
        return [f"{skill_path}: 缺少根 SKILL.md。"]
    if not shared_contract.exists():
        errors.append(f"{shared_contract}: 缺少共享节点包合同。")

    skill_text = skill_path.read_text(encoding="utf-8")
    if REQUIRED_SHARED_REF not in skill_text:
        errors.append(f"{skill_path}: 未回指 `{REQUIRED_SHARED_REF}`。")
    for phrase in REQUIRED_SKILL_PHRASES:
        if phrase not in skill_text:
            errors.append(f"{skill_path}: 缺少关键短语 `{phrase}`。")

    for rel_path in REQUIRED_FILES:
        file_path = stage_root / rel_path
        if not file_path.exists():
            errors.append(f"{file_path}: 缺少必需 reference 模块。")
            continue
        text = file_path.read_text(encoding="utf-8")
        if rel_path.endswith(".yaml"):
            for key in REQUIRED_YAML_KEYS:
                if key not in text:
                    errors.append(f"{file_path}: 缺少 YAML 关键段 `{key}`。")
        if rel_path.endswith(".md") and "分镜构图" not in text:
            errors.append(f"{file_path}: 未声明 `分镜构图` 先行规则。")

    return errors


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Validate `3-Detail` single-skill reference modules."
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

    print(f"PASS: 3-Detail 单技能 references 结构校验通过。root={stage_root.name}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
