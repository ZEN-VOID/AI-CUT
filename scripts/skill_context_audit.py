#!/usr/bin/env python3
"""Audit repository SKILL.md files for sibling CONTEXT.md loading contracts."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path


DEFAULT_EXCLUDED_DIRS = {
    ".git",
    "cache",
    "sessions",
    "shell_snapshots",
    "sqlite",
    "worktrees",
}
DEFAULT_EXCLUDED_PREFIXES = (
    ("plugins", "cache"),
    ("vendor_imports",),
)
CONTRACT_HEADING = "## Context Loading Contract"
REQUIRED_PHRASE = "必须同时加载同目录 `CONTEXT.md`"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Validate that every in-scope SKILL.md has a sibling CONTEXT.md "
            "and an explicit context loading contract."
        )
    )
    parser.add_argument(
        "--root",
        default=".",
        help="Repository root to scan. Defaults to the current directory.",
    )
    parser.add_argument(
        "--strict",
        action="store_true",
        help="Exit non-zero when any failure is found.",
    )
    return parser.parse_args()


def is_excluded(path: Path) -> bool:
    parts = path.parts
    if any(part in DEFAULT_EXCLUDED_DIRS for part in parts):
        return True
    return any(
        parts[: len(prefix)] == prefix for prefix in DEFAULT_EXCLUDED_PREFIXES
    )


def discover_skill_docs(root: Path) -> list[Path]:
    return sorted(
        path
        for path in root.rglob("SKILL.md")
        if not is_excluded(path.relative_to(root))
    )


def audit_skill_doc(path: Path) -> list[str]:
    failures: list[str] = []
    text = path.read_text(encoding="utf-8")
    context_path = path.with_name("CONTEXT.md")

    if not context_path.is_file():
        failures.append(f"{context_path}: missing sibling CONTEXT.md")

    heading_count = text.count(CONTRACT_HEADING)
    if heading_count == 0:
        failures.append(f"{path}: missing {CONTRACT_HEADING}")
    elif heading_count > 1:
        failures.append(f"{path}: duplicate {CONTRACT_HEADING}")

    if REQUIRED_PHRASE not in text:
        failures.append(f"{path}: missing required CONTEXT.md loading phrase")

    return failures


def main() -> int:
    args = parse_args()
    root = Path(args.root).resolve()
    skill_docs = discover_skill_docs(root)
    failures: list[str] = []

    for skill_doc in skill_docs:
        failures.extend(audit_skill_doc(skill_doc))

    print("Skill context audit")
    print(f"repo_root: {root}")
    print(f"discovered_skill_docs: {len(skill_docs)}")
    print(f"failures: {len(failures)}")

    if failures:
        print()
        print("Failures:")
        for failure in failures:
            print(f"- {failure}")

    if args.strict and failures:
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
