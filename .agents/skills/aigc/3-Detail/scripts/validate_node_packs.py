#!/usr/bin/env python3
"""Validate `3-Detail` node-pack structure for child skills."""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

REQUIRED_SPEC_KEYS = (
    "module_id",
    "module_level",
    "purpose",
    "triggers",
    "must_answer",
    "patch_contract",
    "merge_policy",
    "quality_gates",
)

REQUIRED_SHARED_NODE_PACK_REF = ".agents/skills/aigc/3-Detail/_shared/node-pack-contract.md"
LEGACY_SHARED_NODE_PACK_REF = ".agents/skills/aigc/3-Detail/references/node-pack-contract.md"

CHILD_PATH_RE = re.compile(r"^\s*-\s+path:\s*(.+?)\s*$", re.MULTILINE)


def discover_skill_roots(stage_root: Path) -> list[Path]:
    return sorted(
        child
        for child in stage_root.iterdir()
        if child.is_dir() and (child / "module-index.md").exists()
    )


def parse_child_paths(spec_text: str) -> list[str]:
    return [match.group(1).strip() for match in CHILD_PATH_RE.finditer(spec_text)]


def validate_spec_file(skill_root: Path, spec_path: Path) -> list[str]:
    errors: list[str] = []
    spec_text = spec_path.read_text(encoding="utf-8")
    guide_path = spec_path.with_name("module-guide.md")
    rel_spec = spec_path.relative_to(skill_root)

    if not guide_path.exists():
        errors.append(f"{skill_root.name}: {rel_spec} 缺少配对的 module-guide.md。")

    for key in REQUIRED_SPEC_KEYS:
        if not re.search(rf"^\s*{re.escape(key)}\s*:", spec_text, re.MULTILINE):
            errors.append(f"{skill_root.name}: {rel_spec} 缺少必需键 `{key}`。")

    if re.search(r"^\s*module_level\s*:\s*branch\s*$", spec_text, re.MULTILINE):
        child_paths = parse_child_paths(spec_text)
        if not child_paths:
            errors.append(f"{skill_root.name}: {rel_spec} 是 branch，但未声明 child_modules.path。")
        for child_path in child_paths:
            child_file = skill_root / child_path
            if not child_file.exists():
                errors.append(
                    f"{skill_root.name}: {rel_spec} 引用的 child spec 不存在: {child_path}"
                )
    return errors


def validate_skill_root(skill_root: Path) -> list[str]:
    errors: list[str] = []
    spec_files = sorted(skill_root.rglob("module-spec.yaml"))
    if not spec_files:
        return [f"{skill_root.name}: 技能包内未找到 module-spec.yaml。"]

    for spec_path in spec_files:
        errors.extend(validate_spec_file(skill_root, spec_path))

    for contract_file in (skill_root / "SKILL.md", skill_root / "module-index.md"):
        text = contract_file.read_text(encoding="utf-8")
        rel_path = contract_file.relative_to(skill_root)
        if REQUIRED_SHARED_NODE_PACK_REF not in text:
            errors.append(
                f"{skill_root.name}: {rel_path} 未回指共享节点包真源 `{REQUIRED_SHARED_NODE_PACK_REF}`。"
            )
        if LEGACY_SHARED_NODE_PACK_REF in text:
            errors.append(
                f"{skill_root.name}: {rel_path} 仍引用已删除路径 `{LEGACY_SHARED_NODE_PACK_REF}`。"
            )
    return errors


def validate_stage_shared_contract(stage_root: Path) -> list[str]:
    shared_contract = stage_root / "_shared" / "node-pack-contract.md"
    if shared_contract.exists():
        return []
    return [f"{stage_root.name}: 缺少共享节点包真源 {shared_contract.relative_to(stage_root.parent)}。"]


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Validate `3-Detail` child-skill node packs (`module-spec.yaml` / `module-guide.md` / child links)."
    )
    parser.add_argument(
        "skill_roots",
        nargs="*",
        type=Path,
        help="Optional child-skill roots like `.agents/skills/aigc/3-Detail/1-水月`.",
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
    errors.extend(validate_stage_shared_contract(stage_root))
    for skill_root in skill_roots:
        errors.extend(validate_skill_root(skill_root.resolve()))

    if errors:
        print("校验失败:")
        for error in errors:
            print(f"- {error}")
        return 1

    checked = ", ".join(path.name for path in skill_roots)
    print(f"PASS: 节点包结构校验通过。roots={checked}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
