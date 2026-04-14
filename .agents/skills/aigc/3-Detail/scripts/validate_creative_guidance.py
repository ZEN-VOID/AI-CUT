#!/usr/bin/env python3
"""Validate `3-Detail` creative-guidance reference pack for child skills."""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

REQUIRED_REFERENCE_FILES = (
    "module-index.md",
    "route-profile.yaml",
    "examples.md",
    "creative-review-rubric.md",
)

ROUTE_PROFILE_KEYS = (
    "profile_goal",
    "default_strategy",
    "route_profiles",
)

REQUIRED_SHARED_CREATIVE_GUIDANCE_REF = (
    ".agents/skills/aigc/3-Detail/_shared/creative-guidance-contract.md"
)
LEGACY_SHARED_CREATIVE_GUIDANCE_REF = (
    ".agents/skills/aigc/3-Detail/references/creative-guidance-contract.md"
)
FORBIDDEN_PARENT_TOPOLOGY_PHRASES = (
    "1-分镜表现/1-切换",
    "`1-切换` 的实际切镜窗口",
)


def discover_skill_roots(stage_root: Path) -> list[Path]:
    return sorted(
        child
        for child in stage_root.iterdir()
        if child.is_dir() and (child / "references" / "module-index.md").exists()
    )


def validate_route_profile(skill_root: Path, route_profile_path: Path) -> list[str]:
    errors: list[str] = []
    text = route_profile_path.read_text(encoding="utf-8")
    rel_path = route_profile_path.relative_to(skill_root)

    for key in ROUTE_PROFILE_KEYS:
        if not re.search(rf"^\s*{re.escape(key)}\s*:", text, re.MULTILINE):
            errors.append(f"{skill_root.name}: {rel_path} 缺少必需键 `{key}`。")

    if not re.search(r"^\s*-\s*signal_id\s*:", text, re.MULTILINE):
        errors.append(f"{skill_root.name}: {rel_path} 未声明任何 `signal_id` 路由。")
    return errors


def validate_module_index(skill_root: Path, module_index_path: Path) -> list[str]:
    text = module_index_path.read_text(encoding="utf-8")
    rel_path = module_index_path.relative_to(skill_root)
    required_phrases = (
        "作用",
        "汇流顺序",
        "配置真源规则",
    )

    errors: list[str] = []
    for phrase in required_phrases:
        if phrase not in text:
            errors.append(f"{skill_root.name}: {rel_path} 缺少关键章节 `{phrase}`。")
    return errors


def validate_skill_root(skill_root: Path) -> list[str]:
    errors: list[str] = []
    references_root = skill_root / "references"

    for filename in REQUIRED_REFERENCE_FILES:
        file_path = references_root / filename
        if not file_path.exists():
            errors.append(f"{skill_root.name}: 缺少 references/{filename}。")

    module_index_path = references_root / "module-index.md"
    route_profile_path = references_root / "route-profile.yaml"

    if module_index_path.exists():
        errors.extend(validate_module_index(skill_root, module_index_path))
    if route_profile_path.exists():
        errors.extend(validate_route_profile(skill_root, route_profile_path))

    for contract_file in (skill_root / "SKILL.md", module_index_path):
        if not contract_file.exists():
            continue
        text = contract_file.read_text(encoding="utf-8")
        rel_path = contract_file.relative_to(skill_root)
        if REQUIRED_SHARED_CREATIVE_GUIDANCE_REF not in text:
            errors.append(
                f"{skill_root.name}: {rel_path} 未回指共享创作引导真源 `{REQUIRED_SHARED_CREATIVE_GUIDANCE_REF}`。"
            )
        if LEGACY_SHARED_CREATIVE_GUIDANCE_REF in text:
            errors.append(
                f"{skill_root.name}: {rel_path} 仍引用已删除路径 `{LEGACY_SHARED_CREATIVE_GUIDANCE_REF}`。"
            )
    return errors


def validate_stage_contracts(stage_root: Path) -> list[str]:
    errors: list[str] = []

    shared_contract = stage_root / "_shared" / "creative-guidance-contract.md"
    if not shared_contract.exists():
        errors.append(
            f"{stage_root.name}: 缺少共享创作引导真源 {shared_contract.relative_to(stage_root.parent)}。"
        )

    stage_skill = stage_root / "SKILL.md"
    stage_context = stage_root / "CONTEXT.md"

    if stage_skill.exists():
        stage_skill_text = stage_skill.read_text(encoding="utf-8")
        if "分镜构图" not in stage_skill_text:
            errors.append(f"{stage_root.name}: 父层 SKILL.md 未声明 `分镜构图` 先行拓扑。")
        for phrase in FORBIDDEN_PARENT_TOPOLOGY_PHRASES:
            if phrase in stage_skill_text:
                errors.append(f"{stage_root.name}: 父层 SKILL.md 仍残留已删除镜花叶子引用 `{phrase}`。")

    if stage_context.exists():
        stage_context_text = stage_context.read_text(encoding="utf-8")
        for phrase in FORBIDDEN_PARENT_TOPOLOGY_PHRASES[1:]:
            if phrase in stage_context_text:
                errors.append(f"{stage_root.name}: 父层 CONTEXT.md 仍残留旧镜花拓扑表述 `{phrase}`。")
    return errors


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Validate `3-Detail` creative-guidance references (`module-index.md`, `route-profile.yaml`, `examples.md`, `creative-review-rubric.md`)."
    )
    parser.add_argument(
        "skill_roots",
        nargs="*",
        type=Path,
        help="Optional child-skill roots like `.agents/skills/aigc/3-Detail/水月`.",
    )
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()

    script_path = Path(__file__).resolve()
    stage_root = script_path.parent.parent
    skill_roots = args.skill_roots or discover_skill_roots(stage_root)

    if not skill_roots:
        print(f"未发现可校验的 child skill roots: {stage_root}")
        return 1

    errors: list[str] = []
    errors.extend(validate_stage_contracts(stage_root))
    for skill_root in skill_roots:
        errors.extend(validate_skill_root(skill_root.resolve()))

    if errors:
        print("校验失败:")
        for error in errors:
            print(f"- {error}")
        return 1

    checked = ", ".join(path.name for path in skill_roots)
    print(f"PASS: 创作引导校验通过。roots={checked}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
