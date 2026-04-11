#!/usr/bin/env python3
"""Audit the AIGC skill tree against rollout, registry, and runtime contracts."""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

import yaml


ROOT = Path(".agents/skills/aigc")
ROOT_SKILL = ROOT / "SKILL.md"
ROOT_CONTEXT = ROOT / "CONTEXT.md"
REGISTRY = Path(".codex/registry/skills.yaml")
ROUTES = Path(".codex/registry/routes.yaml")

ROOT_CAUSE_SECTION_PATTERNS = [
    re.compile(r"^##\s+Root-Cause Execution Contract \(Mandatory\)\s*$", re.MULTILINE),
    re.compile(r"^###\s+Root-Cause 执行契约\s*$", re.MULTILINE),
    re.compile(r"^##\s+Root-Cause 执行契约\s*$", re.MULTILINE),
]
CHAIN_OF_THOUGHT_REQUIRED_SECTIONS = [
    "## Field Master",
    "## Thought Pass Map",
    "## Pass Table",
]
CONTEXT_REQUIRED_SECTIONS = [
    "## Context Health",
    "## Case Log",
]
CONTEXT_KB_SECTIONS = [
    "## Type Map",
    "## Repair Playbook",
    "## Reusable Heuristics",
]
REFERENCE_MODULES = (
    "chain-of-thought.md",
    "execution-flow.md",
    "type-strategies.md",
    "output-template.md",
)
SUBTYPE_PATH_PREFIXES = ("subtypes/", "./subtypes/")
SHARED_RUNTIME_ROWS = {
    "0-Init": "projects/<项目名>/Init/",
    "1-规划": "projects/<项目名>/规划/",
    "2-组间": "projects/<项目名>/编导/",
    "3-明细": "projects/<项目名>/编导/",
    "4-主体": "projects/<项目名>/主体/",
    "5-画面": "projects/<项目名>/画面/",
    "6-视频": "projects/<项目名>/视频/",
    "7-后期": "projects/<项目名>/后期/",
}
ROOT_STAGE_LANDING = (
    "projects/<项目名>/Init/",
    "projects/<项目名>/规划/",
    "projects/<项目名>/编导/",
    "projects/<项目名>/主体/",
    "projects/<项目名>/画面/",
    "projects/<项目名>/视频/",
    "projects/<项目名>/后期/",
)
ROOT_FORBIDDEN_STAGE_LANDING = (
    "projects/<项目名>/设定/",
    "projects/<项目名>/1-规划/",
    "projects/<项目名>/2-组间/",
    "projects/<项目名>/3-明细/",
    "projects/<项目名>/4-主体/",
    "projects/<项目名>/5-画面/",
)
PROJECT_GOVERNANCE_ARTIFACTS = (
    "projects/<项目名>/project_state.yaml",
    "projects/<项目名>/governance-state.yaml",
)
COUNCIL_STAGE_REVIEW_PATHS = {
    "1-规划": "projects/<项目名>/规划/validation-report.md",
    "2-组间": "projects/<项目名>/编导/validation-report.md",
    "3-明细": "projects/<项目名>/编导/validation-report.md",
    "4-主体": "projects/<项目名>/主体/validation-report.md",
}
STAGE_RUNTIME_EXPECTATIONS = {
    ROOT / "0-Init" / "SKILL.md": (
        "projects/<项目名>/规划/",
        "projects/<项目名>/主体/",
        "projects/<项目名>/画面/",
        "projects/<项目名>/governance-state.yaml",
    ),
    ROOT / "1-规划" / "SKILL.md": (
        "projects/<项目名>/规划/",
        "projects/<项目名>/规划/validation-report.md",
    ),
    ROOT / "4-主体" / "SKILL.md": (
        "projects/<项目名>/主体/",
    ),
    ROOT / "5-画面" / "SKILL.md": (
        "projects/<项目名>/画面/",
    ),
    ROOT / "6-视频" / "SKILL.md": (
        "projects/<项目名>/视频/",
    ),
    ROOT / "6-视频" / "references" / "execution-flow.md": (
        "projects/<项目名>/主体/",
        "projects/<项目名>/画面/",
        "projects/<项目名>/视频/",
    ),
}
STAGE_RUNTIME_FORBIDDEN = {
    ROOT / "0-Init" / "SKILL.md": (
        "projects/<项目名>/2-组间/validation-report.md",
        "projects/<项目名>/3-明细/validation-report.md",
    ),
    ROOT / "1-规划" / "SKILL.md": (
        "runtime 根目录：`projects/<项目名>/Init/`",
        "阶段验证报告：`projects/<项目名>/Init/validation-report.md`",
    ),
    ROOT / "6-视频" / "references" / "execution-flow.md": (
        "projects/<项目名>/设定/",
        "projects/<项目名>/5-画面/",
    ),
}
REQUIRED_SATELLITES = {
    "aigc-query": ROOT / "query",
    "aigc-resume": ROOT / "resume",
    "aigc-review": ROOT / "review",
}
REQUIRED_ROUTE_POLICIES = {
    "aigc-query-satellite-entry",
    "aigc-resume-satellite-entry",
    "aigc-review-satellite-entry",
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Validate the .agents/skills/aigc tree and its harness alignment."
    )
    parser.add_argument(
        "--strict",
        action="store_true",
        help="Exit non-zero if any audit failure is found.",
    )
    return parser.parse_args()


def load_yaml(path: Path) -> dict:
    return yaml.safe_load(path.read_text(encoding="utf-8"))


def frontmatter_of(path: Path) -> dict:
    content = path.read_text(encoding="utf-8")
    match = re.match(r"^---\n(.*?)\n---\n", content, re.DOTALL)
    if not match:
        raise ValueError("missing YAML frontmatter")
    return yaml.safe_load(match.group(1)) or {}


def has_root_cause_contract(content: str) -> bool:
    return any(pattern.search(content) for pattern in ROOT_CAUSE_SECTION_PATTERNS)


def has_field_master_semantics(content: str) -> bool:
    return "## Field Master" in content or "| field_id |" in content


def has_thought_pass_semantics(content: str) -> bool:
    return "## Thought Pass Map" in content or "| step_id |" in content


def has_pass_table_semantics(content: str) -> bool:
    return (
        "## Pass Table" in content
        or "Rework Entry" in content
        or "返工入口" in content
    )


def declared_local_reference_modules(content: str) -> set[str]:
    matches = re.findall(r"`([^`]+)`|\]\(([^)]+)\)", content)
    declared_paths = {
        candidate
        for pair in matches
        for candidate in pair
        if candidate
    }
    local_modules: set[str] = set()
    for reference_name in REFERENCE_MODULES:
        aliases = {f"references/{reference_name}", f"./references/{reference_name}"}
        if declared_paths & aliases:
            local_modules.add(reference_name)
    return local_modules


def declared_local_subtype_paths(content: str) -> set[str]:
    matches = re.findall(r"`([^`]+)`|\]\(([^)]+)\)", content)
    declared_paths = {
        candidate.strip()
        for pair in matches
        for candidate in pair
        if candidate
    }
    subtype_paths: set[str] = set()
    for candidate in declared_paths:
        normalized = candidate.removeprefix("./")
        if not normalized.startswith("subtypes/"):
            continue
        if any(marker in normalized for marker in ("<", ">", "*", "{", "}", "[", "]")):
            continue
        if normalized in {"subtypes", "subtypes/"}:
            continue
        if "/providers/" in normalized or normalized.endswith("/providers"):
            continue
        if len(Path(normalized).parts) < 2:
            continue
        subtype_paths.add(normalized.rstrip("/"))
    return subtype_paths


def audit_skill_file(path: Path, failures: list[str]) -> None:
    content = ""
    tier = None

    if path.stat().st_size == 0:
        failures.append(f"{path}: SKILL.md is empty")
    else:
        content = path.read_text(encoding="utf-8")
        try:
            frontmatter = frontmatter_of(path)
        except Exception as exc:  # noqa: BLE001
            failures.append(f"{path}: {exc}")
        else:
            tier = frontmatter.get("governance_tier")
            if tier not in {"full", "lite"}:
                failures.append(f"{path}: missing or invalid governance_tier")

        if not has_root_cause_contract(content):
            failures.append(f"{path}: missing section `## Root-Cause Execution Contract (Mandatory)`")

        chain_of_thought = path.parent / "references" / "chain-of-thought.md"
        field_sources = [content]
        if chain_of_thought.exists():
            field_sources.append(chain_of_thought.read_text(encoding="utf-8"))

        has_field_master = any(has_field_master_semantics(source) for source in field_sources)
        has_thought_pass = any(has_thought_pass_semantics(source) for source in field_sources)
        has_pass_table = any(has_pass_table_semantics(source) for source in field_sources)

        if tier == "full":
            if not has_field_master:
                failures.append(f"{path}: missing section `{CHAIN_OF_THOUGHT_REQUIRED_SECTIONS[0]}`")
            if not has_thought_pass:
                failures.append(f"{path}: missing section `{CHAIN_OF_THOUGHT_REQUIRED_SECTIONS[1]}`")
            if not has_pass_table:
                failures.append(f"{path}: missing section `{CHAIN_OF_THOUGHT_REQUIRED_SECTIONS[2]}`")

        for reference_name in declared_local_reference_modules(content):
            reference_path = path.parent / "references" / reference_name
            if not reference_path.exists():
                failures.append(f"{reference_path}: missing referenced module file")

        for subtype_ref in declared_local_subtype_paths(content):
            subtype_path = path.parent / subtype_ref
            if subtype_path.suffix:
                if not subtype_path.exists():
                    failures.append(f"{subtype_path}: missing declared subtype contract path")
                continue
            subtype_skill = subtype_path / "SKILL.md"
            if not subtype_skill.exists():
                failures.append(f"{subtype_skill}: missing for declared subtype path `{subtype_ref}`")

    context_path = path.with_name("CONTEXT.md")
    if not context_path.exists():
        failures.append(f"{context_path}: missing sibling CONTEXT.md")
        return
    if context_path.stat().st_size == 0:
        failures.append(f"{context_path}: CONTEXT.md is empty")
        return

    context = context_path.read_text(encoding="utf-8")
    for section in CONTEXT_REQUIRED_SECTIONS:
        if section not in context:
            failures.append(f"{context_path}: missing section `{section}`")
    if not any(section in context for section in CONTEXT_KB_SECTIONS):
        failures.append(
            f"{context_path}: missing knowledge-base core (`Type Map` / `Repair Playbook` / `Reusable Heuristics`)"
        )


def audit_registry(failures: list[str]) -> tuple[list[dict], list[dict]]:
    if not REGISTRY.exists():
        failures.append(f"{REGISTRY}: missing")
        return [], []

    registry = load_yaml(REGISTRY)
    active_skills = registry.get("active_skills", [])
    aigc_entry = next((item for item in active_skills if item.get("id") == "aigc"), None)
    if not aigc_entry:
        failures.append(f"{REGISTRY}: missing active skill `aigc`")
        return [], []

    runtime_control = aigc_entry.get("runtime_control", {})
    if runtime_control.get("canonical_project_runtime") != "projects/<项目名>/":
        failures.append(
            f"{REGISTRY}: `aigc.runtime_control.canonical_project_runtime` must be `projects/<项目名>/`"
        )
    if runtime_control.get("project_state_carrier") != "projects/<项目名>/project_state.yaml":
        failures.append(
            f"{REGISTRY}: `aigc.runtime_control.project_state_carrier` must be `projects/<项目名>/project_state.yaml`"
        )
    if runtime_control.get("governance_state_carrier") != "projects/<项目名>/governance-state.yaml":
        failures.append(
            f"{REGISTRY}: `aigc.runtime_control.governance_state_carrier` must be `projects/<项目名>/governance-state.yaml`"
        )

    stage_index = aigc_entry.get("stage_index", [])
    if len(stage_index) < 8:
        failures.append(f"{REGISTRY}: `aigc.stage_index` is incomplete")

    satellite_index = aigc_entry.get("satellite_index", [])
    satellite_ids = {item.get("id") for item in satellite_index}
    missing_satellites = sorted(set(REQUIRED_SATELLITES) - satellite_ids)
    if missing_satellites:
        failures.append(
            f"{REGISTRY}: `aigc.satellite_index` missing {', '.join(missing_satellites)}"
        )
    return stage_index, satellite_index


def audit_routes(failures: list[str]) -> None:
    if not ROUTES.exists():
        failures.append(f"{ROUTES}: missing")
        return

    routes = load_yaml(ROUTES)
    route_policies = routes.get("route_policies", [])
    route_policy_ids = {item.get("id") for item in route_policies}
    missing_route_policies = sorted(REQUIRED_ROUTE_POLICIES - route_policy_ids)
    if missing_route_policies:
        failures.append(
            f"{ROUTES}: missing route policies {', '.join(missing_route_policies)}"
        )

    workflow_carriers = routes.get("workflow_carriers", [])
    aigc_runtime = next((item for item in workflow_carriers if item.get("id") == "aigc-project-runtime"), None)
    if not aigc_runtime:
        failures.append(f"{ROUTES}: missing workflow carrier `aigc-project-runtime`")
        return

    if aigc_runtime.get("canonical_runtime_root") != "projects/<项目名>/":
        failures.append(f"{ROUTES}: `aigc-project-runtime` canonical root mismatch")
    if aigc_runtime.get("project_state_carrier") != "projects/<项目名>/project_state.yaml":
        failures.append(f"{ROUTES}: `aigc-project-runtime` project_state carrier mismatch")
    if aigc_runtime.get("governance_state_carrier") != "projects/<项目名>/governance-state.yaml":
        failures.append(f"{ROUTES}: `aigc-project-runtime` governance_state carrier mismatch")


def audit_runtime_alignment(failures: list[str]) -> None:
    shared_layout = ROOT / "_shared" / "project-runtime-layout.md"
    if not shared_layout.exists():
        failures.append(f"{shared_layout}: missing")
        return

    shared_content = shared_layout.read_text(encoding="utf-8")
    for governance_file in PROJECT_GOVERNANCE_ARTIFACTS:
        if governance_file not in shared_content:
            failures.append(f"{shared_layout}: missing project governance artifact `{governance_file}`")
    for stage_name, runtime_root in SHARED_RUNTIME_ROWS.items():
        row = f"| `{stage_name}` | `{runtime_root}` |"
        if row not in shared_content:
            failures.append(f"{shared_layout}: missing canonical runtime row `{row}`")

    root_content = ROOT_SKILL.read_text(encoding="utf-8") if ROOT_SKILL.exists() else ""
    for governance_file in PROJECT_GOVERNANCE_ARTIFACTS:
        if governance_file not in root_content:
            failures.append(f"{ROOT_SKILL}: missing project governance artifact `{governance_file}`")
    for runtime_root in ROOT_STAGE_LANDING:
        if runtime_root not in root_content:
            failures.append(f"{ROOT_SKILL}: missing canonical stage landing `{runtime_root}`")
    for forbidden_root in ROOT_FORBIDDEN_STAGE_LANDING:
        if forbidden_root in root_content:
            failures.append(f"{ROOT_SKILL}: contains legacy stage landing `{forbidden_root}`")

    council_spec = ROOT / "_shared" / "council-runtime" / "module-spec.md"
    if council_spec.exists():
        council_content = council_spec.read_text(encoding="utf-8")
        for stage_name, review_path in COUNCIL_STAGE_REVIEW_PATHS.items():
            row = f"| `{stage_name}` |"
            if row not in council_content or review_path not in council_content:
                failures.append(
                    f"{council_spec}: missing review checkpoint `{stage_name} -> {review_path}`"
                )
    else:
        failures.append(f"{council_spec}: missing")

    for path, expected_markers in STAGE_RUNTIME_EXPECTATIONS.items():
        if not path.exists():
            failures.append(f"{path}: missing")
            continue
        content = path.read_text(encoding="utf-8")
        for marker in expected_markers:
            if marker not in content:
                failures.append(f"{path}: missing runtime marker `{marker}`")

    for path, forbidden_markers in STAGE_RUNTIME_FORBIDDEN.items():
        if not path.exists():
            continue
        content = path.read_text(encoding="utf-8")
        for marker in forbidden_markers:
            if marker in content:
                failures.append(f"{path}: contains legacy runtime marker `{marker}`")


def audit_stage_index(stage_index: list[dict], failures: list[str]) -> None:
    root_content = ROOT_SKILL.read_text(encoding="utf-8") if ROOT_SKILL.exists() else ""
    for stage in stage_index:
        path = Path(stage["path"])
        status = stage.get("contract_status")
        stage_name = path.name

        if status == "shelved":
            if stage_name not in root_content or "搁浅" not in root_content:
                failures.append(
                    f"{ROOT_SKILL}: shelved stage `{stage_name}` must be explicitly marked as `搁浅` in root status table"
                )
            continue

        skill_path = path / "SKILL.md"
        context_path = path / "CONTEXT.md"
        if not skill_path.exists():
            failures.append(f"{skill_path}: missing for active stage `{stage['id']}`")
        if not context_path.exists():
            failures.append(f"{context_path}: missing for active stage `{stage['id']}`")


def audit_satellite_index(satellite_index: list[dict], failures: list[str]) -> None:
    indexed_by_id = {item.get("id"): item for item in satellite_index}
    for satellite_id, expected_root in REQUIRED_SATELLITES.items():
        entry = indexed_by_id.get(satellite_id)
        if not entry:
            continue
        path = Path(entry["path"])
        if path != expected_root:
            failures.append(f"{REGISTRY}: `{satellite_id}` path must be `{expected_root}`")
        if entry.get("route_role") != "satellite":
            failures.append(f"{REGISTRY}: `{satellite_id}` route_role must be `satellite`")

        skill_path = expected_root / "SKILL.md"
        context_path = expected_root / "CONTEXT.md"
        if not skill_path.exists():
            failures.append(f"{skill_path}: missing for satellite `{satellite_id}`")
        if not context_path.exists():
            failures.append(f"{context_path}: missing for satellite `{satellite_id}`")


def shelved_stage_roots(stage_index: list[dict]) -> list[Path]:
    return [Path(stage["path"]) for stage in stage_index if stage.get("contract_status") == "shelved"]


def main() -> int:
    args = parse_args()
    failures: list[str] = []

    if not ROOT_SKILL.exists():
        failures.append(f"{ROOT_SKILL}: missing")
    else:
        root_content = ROOT_SKILL.read_text(encoding="utf-8")
        if "projects/<项目名>/" not in root_content:
            failures.append(f"{ROOT_SKILL}: missing canonical project-root runtime declaration")

    if ROOT_CONTEXT.exists() and ROOT_CONTEXT.stat().st_size == 0:
        failures.append(f"{ROOT_CONTEXT}: CONTEXT.md is empty")

    stage_index, satellite_index = audit_registry(failures)
    audit_routes(failures)
    audit_runtime_alignment(failures)

    skipped_roots = shelved_stage_roots(stage_index)

    for skill_path in sorted(ROOT.rglob("SKILL.md")):
        if any(root in skill_path.parents for root in skipped_roots):
            continue
        audit_skill_file(skill_path, failures)

    if stage_index:
        audit_stage_index(stage_index, failures)
    if satellite_index:
        audit_satellite_index(satellite_index, failures)

    print("AIGC skill tree audit")
    print(f"repo_root: {Path.cwd()}")
    print(f"discovered_skill_docs: {len(list(ROOT.rglob('SKILL.md')))}")
    print(f"registry_stage_entries: {len(stage_index)}")
    print(f"registry_satellite_entries: {len(satellite_index)}")
    print(f"failures: {len(failures)}")

    if failures:
        print("")
        print("Audit failures:")
        for failure in failures:
            print(f"- {failure}")
    else:
        print("")
        print("All checked AIGC skill contracts are aligned.")

    if args.strict and failures:
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
