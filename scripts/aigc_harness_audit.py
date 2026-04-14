#!/usr/bin/env python3
"""Audit the minimum harness bootstrap layout for AIGC-FILM."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path


REQUIRED_PATHS = [
    Path("HARNESS.md"),
    Path(".codex/agents/harness治理/中书省.md"),
    Path(".codex/agents/harness治理/门下省.md"),
    Path(".codex/agents/harness治理/尚书省.md"),
    Path(".codex/templates/harness/office-governance-contract.md"),
    Path(".codex/registry/skills.yaml"),
    Path(".codex/registry/routes.yaml"),
    Path(".codex/runbooks/task-lifecycle.md"),
    Path(".codex/state/tasks/README.md"),
    Path(".codex/evals/README.md"),
    Path("scripts/aigc_skill_audit.py"),
    Path(".codex/templates/harness/mandate.yaml"),
    Path(".codex/templates/harness/mission-brief.yaml"),
    Path(".codex/templates/harness/route-plan.yaml"),
    Path(".codex/templates/harness/preflight-verdict.yaml"),
    Path(".codex/templates/harness/validation-report.md"),
    Path(".codex/templates/harness/learning-record.md"),
    Path("docs/plans/2026-04-08-san-sheng-liu-bu-architecture.md"),
]

AGENT_REQUIRED_SNIPPETS = {
    Path(".codex/agents/harness治理/中书省.md"): [
        ".codex/templates/harness/office-governance-contract.md",
        "## 输出合同",
        "## 分层上溯",
        "## 移交合同",
    ],
    Path(".codex/agents/harness治理/门下省.md"): [
        ".codex/templates/harness/office-governance-contract.md",
        "## 输出合同",
        "## 否决条件",
        "## 分层上溯",
    ],
    Path(".codex/agents/harness治理/尚书省.md"): [
        ".codex/templates/harness/office-governance-contract.md",
        "## 输出合同",
        "## 执行约束",
        "## 分层上溯",
    ],
}

ROOT_REQUIRED_SNIPPETS = {
    Path("AGENTS.md"): [
        "### HARNESS.md 总览与同步（强制）",
        "### AIGC 改造兼容模式（强制）",
        "bootstrap_compat",
        "根目录 `HARNESS.md`",
        "必须在同一轮任务内同步检查并更新根目录 `HARNESS.md`",
    ],
    Path("HARNESS.md"): [
        "## 当前工程化构思",
        "bootstrap_compat",
        "## 当前已实现真源",
        "## 可期发展方向",
        "## 更新维护合同",
    ],
}

TEMPLATE_REQUIRED_SNIPPETS = {
    Path(".codex/templates/harness/preflight-verdict.yaml"): [
        "layered_trace:",
        "meta_rule_source:",
        "rollback_watchpoints:",
    ],
    Path(".codex/templates/harness/validation-report.md"): [
        "## Layered Trace",
        "## Anti-Regression",
        "systemic prevention fix:",
    ],
    Path(".codex/templates/harness/learning-record.md"): [
        "milestone_type:",
        "promote_to_agents_or_meta:",
    ],
}

RUNBOOK_REQUIRED_SNIPPETS = [
    "projects/aigc/<项目名>/",
    "Workflow-Specific Control Planes",
]

REGISTRY_REQUIRED_SNIPPETS = {
    Path(".codex/registry/skills.yaml"): [
        "contract_mode: bootstrap_compat",
        "canonical_project_runtime: projects/aigc/<项目名>/",
        "contract_status: shelved",
    ],
    Path(".codex/registry/routes.yaml"): [
        "id: aigc-bootstrap-compat-mode",
        "contract_mode: bootstrap_compat",
        "id: aigc-project-runtime",
        "canonical_runtime_root: projects/aigc/<项目名>/",
        "id: aigc-shelved-stages",
    ],
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Validate the minimum 三省六部制 harness bootstrap layout."
    )
    parser.add_argument(
        "--strict",
        action="store_true",
        help="Exit non-zero if any required bootstrap carrier is missing.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    repo_root = Path.cwd()

    missing = [path for path in REQUIRED_PATHS if not (repo_root / path).exists()]
    contract_failures: list[str] = []

    for path, snippets in AGENT_REQUIRED_SNIPPETS.items():
        full_path = repo_root / path
        if not full_path.exists():
            continue
        content = full_path.read_text(encoding="utf-8")
        for snippet in snippets:
            if snippet not in content:
                contract_failures.append(f"{path}: missing snippet `{snippet}`")

    for path, snippets in ROOT_REQUIRED_SNIPPETS.items():
        full_path = repo_root / path
        if not full_path.exists():
            continue
        content = full_path.read_text(encoding="utf-8")
        for snippet in snippets:
            if snippet not in content:
                contract_failures.append(f"{path}: missing snippet `{snippet}`")

    for path, snippets in TEMPLATE_REQUIRED_SNIPPETS.items():
        full_path = repo_root / path
        if not full_path.exists():
            continue
        content = full_path.read_text(encoding="utf-8")
        for snippet in snippets:
            if snippet not in content:
                contract_failures.append(f"{path}: missing snippet `{snippet}`")

    runbook_path = repo_root / ".codex/runbooks/task-lifecycle.md"
    if runbook_path.exists():
        runbook_content = runbook_path.read_text(encoding="utf-8")
        for snippet in RUNBOOK_REQUIRED_SNIPPETS:
            if snippet not in runbook_content:
                contract_failures.append(
                    f".codex/runbooks/task-lifecycle.md: missing snippet `{snippet}`"
                )

    for path, snippets in REGISTRY_REQUIRED_SNIPPETS.items():
        full_path = repo_root / path
        if not full_path.exists():
            continue
        content = full_path.read_text(encoding="utf-8")
        for snippet in snippets:
            if snippet not in content:
                contract_failures.append(f"{path}: missing snippet `{snippet}`")

    print("AIGC-FILM harness bootstrap audit")
    print(f"repo_root: {repo_root}")
    print(f"required_paths: {len(REQUIRED_PATHS)}")
    print(f"missing_paths: {len(missing)}")
    print(f"contract_failures: {len(contract_failures)}")

    if missing:
        print("")
        print("Missing carriers:")
        for path in missing:
            print(f"- {path}")
    else:
        print("")
        print("All required bootstrap carriers are present.")

    if contract_failures:
        print("")
        print("Contract anchor failures:")
        for failure in contract_failures:
            print(f"- {failure}")
    else:
        print("")
        print("All checked contract anchors are present.")

    if args.strict and (missing or contract_failures):
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
