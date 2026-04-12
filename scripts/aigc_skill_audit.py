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
DEFAULT_SOFT_LIMIT_CHARS = 20000
DEFAULT_HARD_LIMIT_CHARS = 40000
DEFAULT_SOFT_LIMIT_CASES = 16
DEFAULT_HARD_LIMIT_CASES = 32
CASE_LOG_DOMINANCE_RATIO = 0.6
CASE_LOG_DOMINANCE_MIN_CASES = 8
REFERENCE_MODULES = (
    "chain-of-thought.md",
    "execution-flow.md",
    "type-strategies.md",
    "capability-playbook.md",
    "分镜表现.md",
    "角色表现.md",
    "场景氛围.md",
    "运镜手法.md",
    "摄影美学.md",
    "转场特效.md",
    "output-template.md",
)
SUBTYPE_PATH_PREFIXES = ("subtypes/", "./subtypes/")
SHARED_RUNTIME_ROWS = {
    "0-Init": "projects/<项目名>/0-Init/",
    "Story": "projects/<项目名>/Story/",
    "1-Planning": "projects/<项目名>/1-Planning/",
    "2-Global": "projects/<项目名>/2-Global/",
    "3-Detail": "projects/<项目名>/3-Detail/",
    "4-Design": "projects/<项目名>/4-Design/",
    "5-Image": "projects/<项目名>/5-Image/",
    "6-Video": "projects/<项目名>/6-Video/",
    "7-Cut": "projects/<项目名>/7-Cut/",
}
ROOT_STAGE_LANDING = (
    "projects/<项目名>/0-Init/",
    "projects/<项目名>/Story/",
    "projects/<项目名>/1-Planning/",
    "projects/<项目名>/2-Global/",
    "projects/<项目名>/3-Detail/",
    "projects/<项目名>/4-Design/",
    "projects/<项目名>/5-Image/",
    "projects/<项目名>/6-Video/",
    "projects/<项目名>/7-Cut/",
)
ROOT_FORBIDDEN_STAGE_LANDING = (
    "projects/<项目名>/设定/",
    "projects/<项目名>/1-规划/",
    "projects/<项目名>/2-组间/",
    "projects/<项目名>/3-明细/",
    "projects/<项目名>/主体/",
    "projects/<项目名>/4-主体/",
    "projects/<项目名>/5-画面/",
    "projects/<项目名>/6-视频/",
    "projects/<项目名>/7-后期/",
)
PROJECT_GOVERNANCE_ARTIFACTS = (
    "projects/<项目名>/project_state.yaml",
    "projects/<项目名>/governance-state.yaml",
)
COUNCIL_STAGE_REVIEW_PATHS = {
    "1-Planning": "projects/<项目名>/1-Planning/validation-report.md",
    "2-Global": "projects/<项目名>/2-Global/validation-report.md",
    "3-Detail": "projects/<项目名>/3-Detail/validation-report.md",
    "4-Design": "projects/<项目名>/4-Design/validation-report.md",
}
STAGE_RUNTIME_EXPECTATIONS = {
    ROOT / "0-Init" / "SKILL.md": (
        "projects/<项目名>/Story/",
        "projects/<项目名>/1-Planning/1-分集/",
        "projects/<项目名>/1-Planning/2-剧本/",
        "projects/<项目名>/1-Planning/3-分组/",
        "projects/<项目名>/1-Planning/",
        "projects/<项目名>/4-Design/1-场景/1-清单/",
        "projects/<项目名>/4-Design/2-角色/1-清单/",
        "projects/<项目名>/5-Image/",
        "projects/<项目名>/5-Image/分镜故事板/",
        "projects/<项目名>/6-Video/全能参照/",
    ),
    ROOT / "1-Planning" / "SKILL.md": (
        "projects/<项目名>/1-Planning/",
        "projects/<项目名>/1-Planning/validation-report.md",
    ),
    ROOT / "4-Design" / "SKILL.md": (
        "projects/<项目名>/4-Design/",
    ),
    ROOT / "5-Image" / "1-提示词蒸馏" / "SKILL.md": (
        "projects/<项目名>/5-Image/",
        "projects/<项目名>/5-Image/分镜故事板/",
        "projects/<项目名>/5-Image/分镜帧/",
        "projects/<项目名>/5-Image/漫画/",
    ),
    ROOT / "6-Video" / "SKILL.md": (
        "projects/<项目名>/6-Video/",
        "projects/<项目名>/6-Video/全能参照/",
        "projects/<项目名>/6-Video/首帧参照/",
        "projects/<项目名>/6-Video/生成任务/",
    ),
}
STAGE_RUNTIME_FORBIDDEN = {
    ROOT / "0-Init" / "SKILL.md": (
        "projects/<项目名>/主体/",
        "projects/<项目名>/4-主体/",
        "projects/<项目名>/5-画面/",
        "projects/<项目名>/6-视频/",
        "projects/<项目名>/2-组间/validation-report.md",
        "projects/<项目名>/3-明细/validation-report.md",
    ),
    ROOT / "1-Planning" / "SKILL.md": (
        "runtime 根目录：`projects/<项目名>/0-Init/`",
        "阶段验证报告：`projects/<项目名>/0-Init/validation-report.md`",
    ),
    ROOT / "6-Video" / "SKILL.md": (
        "projects/<项目名>/设定/",
        "projects/<项目名>/5-画面/",
        "projects/<项目名>/主体/",
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
REQUIRED_STAGE_AGENT_DOCS = {
}
AGENT_REFERENCE_PATTERN = re.compile(r"\.codex/agents/aigc/[^\s`)\]>\"']+\.md")
BOOTSTRAP_COMPAT_MODE = "bootstrap_compat"
BOOTSTRAP_COMPAT_ROUTE_POLICIES = {
    "aigc-bootstrap-compat-mode",
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


def extract_context_limit(content: str, limit_name: str, default: int) -> int:
    pattern = rf"^- {re.escape(limit_name)}:\s*(\d+)\s*$"
    match = re.search(pattern, content, re.MULTILINE)
    return int(match.group(1)) if match else default


def case_count_of(content: str) -> int:
    return len(re.findall(r"^###\s+Case-", content, re.MULTILINE))


def has_case_before_case_log(content: str) -> bool:
    case_matches = list(re.finditer(r"^###\s+Case-", content, re.MULTILINE))
    if not case_matches:
        return False
    case_log_match = re.search(r"^##\s+Case Log\s*$", content, re.MULTILINE)
    if not case_log_match:
        return False
    return any(match.start() < case_log_match.start() for match in case_matches)


def case_log_dominates(content: str) -> bool:
    first_case_match = re.search(r"^###\s+Case-", content, re.MULTILINE)
    if not first_case_match:
        return False
    case_count = case_count_of(content)
    if case_count < CASE_LOG_DOMINANCE_MIN_CASES:
        return False
    case_payload = content[first_case_match.start() :]
    return len(case_payload) / max(len(content), 1) >= CASE_LOG_DOMINANCE_RATIO


def audit_context_quality(context_path: Path, context: str, warnings: list[str]) -> None:
    char_count = len(context)
    cases = case_count_of(context)
    soft_limit_chars = extract_context_limit(context, "soft_limit_chars", DEFAULT_SOFT_LIMIT_CHARS)
    hard_limit_chars = extract_context_limit(context, "hard_limit_chars", DEFAULT_HARD_LIMIT_CHARS)
    soft_limit_cases = extract_context_limit(context, "soft_limit_cases", DEFAULT_SOFT_LIMIT_CASES)
    hard_limit_cases = extract_context_limit(context, "hard_limit_cases", DEFAULT_HARD_LIMIT_CASES)

    if char_count >= soft_limit_chars:
        warnings.append(
            f"{context_path}: chars={char_count} reached soft limit {soft_limit_chars}; compact KB or move long timelines to CHANGELOG.md"
        )
    if cases >= soft_limit_cases:
        warnings.append(
            f"{context_path}: cases={cases} reached soft limit {soft_limit_cases}; keep only milestone conclusions in Case Log"
        )
    if char_count >= hard_limit_chars:
        warnings.append(
            f"{context_path}: chars={char_count} reached hard limit {hard_limit_chars}; archive older material before further growth"
        )
    if cases >= hard_limit_cases:
        warnings.append(
            f"{context_path}: cases={cases} reached hard limit {hard_limit_cases}; archive older cases before appending new ones"
        )
    if has_case_before_case_log(context):
        warnings.append(
            f"{context_path}: found `Case-*` sections before `## Case Log`; move them under Case Log or externalize detailed timeline to CHANGELOG.md"
        )
    if case_log_dominates(context):
        warnings.append(
            f"{context_path}: Case content dominates the file; move long process history to CHANGELOG.md or reports and keep CONTEXT.md as KB"
        )


def audit_all_context_hygiene(warnings: list[str]) -> None:
    for context_path in sorted(ROOT.rglob("CONTEXT.md")):
        if not context_path.exists() or context_path.stat().st_size == 0:
            continue
        audit_context_quality(context_path, context_path.read_text(encoding="utf-8"), warnings)


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


def audit_registry(failures: list[str]) -> tuple[list[dict], list[dict], str]:
    if not REGISTRY.exists():
        failures.append(f"{REGISTRY}: missing")
        return [], [], ""

    registry = load_yaml(REGISTRY)
    active_skills = registry.get("active_skills", [])
    aigc_entry = next((item for item in active_skills if item.get("id") == "aigc"), None)
    if not aigc_entry:
        failures.append(f"{REGISTRY}: missing active skill `aigc`")
        return [], [], ""

    contract_mode = aigc_entry.get("contract_mode", "")
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
    return stage_index, satellite_index, contract_mode


def audit_routes(contract_mode: str, failures: list[str]) -> None:
    if not ROUTES.exists():
        failures.append(f"{ROUTES}: missing")
        return

    routes = load_yaml(ROUTES)
    route_policies = routes.get("route_policies", [])
    route_policy_ids = {item.get("id") for item in route_policies}
    required_route_policies = set(REQUIRED_ROUTE_POLICIES)
    if contract_mode == BOOTSTRAP_COMPAT_MODE:
        required_route_policies |= BOOTSTRAP_COMPAT_ROUTE_POLICIES
    missing_route_policies = sorted(required_route_policies - route_policy_ids)
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
    if contract_mode == BOOTSTRAP_COMPAT_MODE and aigc_runtime.get("contract_mode") != BOOTSTRAP_COMPAT_MODE:
        failures.append(
            f"{ROUTES}: `aigc-project-runtime.contract_mode` must be `{BOOTSTRAP_COMPAT_MODE}`"
        )


def audit_runtime_alignment(contract_mode: str, failures: list[str]) -> None:
    shared_layout = ROOT / "_shared" / "project-runtime-layout.md"
    if not shared_layout.exists():
        failures.append(f"{shared_layout}: missing")
        return

    shared_content = shared_layout.read_text(encoding="utf-8")
    for governance_file in PROJECT_GOVERNANCE_ARTIFACTS:
        if governance_file not in shared_content:
            failures.append(f"{shared_layout}: missing project governance artifact `{governance_file}`")

    root_content = ROOT_SKILL.read_text(encoding="utf-8") if ROOT_SKILL.exists() else ""
    for governance_file in PROJECT_GOVERNANCE_ARTIFACTS:
        if governance_file not in root_content:
            failures.append(f"{ROOT_SKILL}: missing project governance artifact `{governance_file}`")

    if contract_mode == BOOTSTRAP_COMPAT_MODE:
        return

    for stage_name, runtime_root in SHARED_RUNTIME_ROWS.items():
        row = f"| `{stage_name}` | `{runtime_root}` |"
        if row not in shared_content:
            failures.append(f"{shared_layout}: missing canonical runtime row `{row}`")
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


def audit_init_single_skill_contract(failures: list[str]) -> None:
    init_skill = ROOT / "0-Init" / "SKILL.md"
    if not init_skill.exists():
        return
    init_content = init_skill.read_text(encoding="utf-8")
    if "## Internal Capability Fusion Contract (Mandatory)" not in init_content:
        failures.append(f"{init_skill}: missing `Internal Capability Fusion Contract (Mandatory)`")
    if ".codex/agents/aigc/初始组/" in init_content:
        failures.append(
            f"{init_skill}: 0-Init must internalize init routing/mode/audit capabilities into the parent SKILL instead of referencing `.codex/agents/aigc/初始组/`"
        )

    init_openai = ROOT / "0-Init" / "agents" / "openai.yaml"
    if init_openai.exists() and ".codex/agents/aigc/初始组/" in init_openai.read_text(encoding="utf-8"):
        failures.append(f"{init_openai}: should not reference external init-agent contracts")

    refs_root = ROOT / "0-Init" / "references"
    if refs_root.exists():
        for path in sorted(refs_root.rglob("*.md")):
            content = path.read_text(encoding="utf-8")
            if ".codex/agents/aigc/初始组/" in content:
                failures.append(f"{path}: reference stub still points to deleted external init-agent contracts")


def audit_planning_internal_skill_contract(failures: list[str]) -> None:
    planning_root = ROOT / "1-Planning"
    if not planning_root.exists():
        return

    forbidden_marker = ".codex/agents/aigc/规划组/"
    targets = (
        planning_root / "SKILL.md",
        planning_root / "agents" / "openai.yaml",
        planning_root / "2-剧本" / "SKILL.md",
        planning_root / "2-剧本" / "agents" / "openai.yaml",
        planning_root / "3-分组" / "SKILL.md",
    )

    for path in targets:
        if not path.exists():
            continue
        content = path.read_text(encoding="utf-8")
        if path.suffix == ".md" and path.name == "SKILL.md":
            if "## Internal Capability Fusion Contract (Mandatory)" not in content:
                failures.append(f"{path}: missing `Internal Capability Fusion Contract (Mandatory)`")
        if forbidden_marker in content:
            failures.append(f"{path}: should not reference deleted planning-agent contracts")


def audit_global_single_skill_contract(failures: list[str]) -> None:
    global_root = ROOT / "2-Global"
    global_skill = global_root / "SKILL.md"
    if not global_skill.exists():
        return

    forbidden_marker = ".codex/agents/aigc/导演组/"
    targets = (
        global_skill,
        global_root / "_shared" / "IO_CONTRACT.md",
        global_root / "agents" / "openai.yaml",
        global_root / "templates" / "全局风格.template.md",
        global_root / "templates" / "类型指导.template.md",
        global_root / "templates" / "导演意图.template.md",
    )

    skill_content = global_skill.read_text(encoding="utf-8")
    if "## Internal Capability Fusion Contract (Mandatory)" not in skill_content:
        failures.append(f"{global_skill}: missing `Internal Capability Fusion Contract (Mandatory)`")
    if forbidden_marker in skill_content:
        failures.append(
            f"{global_skill}: 2-Global must internalize style/type/director capabilities into the parent SKILL instead of referencing `.codex/agents/aigc/导演组/`"
        )

    for path in targets[1:]:
        if not path.exists():
            continue
        content = path.read_text(encoding="utf-8")
        if forbidden_marker in content:
            failures.append(f"{path}: should not reference deleted director-group contracts")


def audit_detail_single_skill_contract(failures: list[str]) -> None:
    detail_root = ROOT / "3-Detail"
    detail_skill = detail_root / "SKILL.md"
    if not detail_skill.exists():
        return

    forbidden_marker = ".codex/agents/aigc/制作组/"
    targets = (
        detail_skill,
        detail_root / "_shared" / "IO_CONTRACT.md",
        detail_root / "agents" / "openai.yaml",
    )

    refs_root = detail_root / "references"
    ref_targets = sorted(refs_root.rglob("*.md")) if refs_root.exists() else []

    skill_content = detail_skill.read_text(encoding="utf-8")
    if "## Internal Capability Fusion Contract (Mandatory)" not in skill_content:
        failures.append(f"{detail_skill}: missing `Internal Capability Fusion Contract (Mandatory)`")
    if forbidden_marker in skill_content:
        failures.append(
            f"{detail_skill}: 3-Detail must internalize former production-team capabilities into the parent SKILL instead of referencing `.codex/agents/aigc/制作组/`"
        )

    for path in (*targets[1:], *ref_targets):
        if not path.exists():
            continue
        content = path.read_text(encoding="utf-8")
        if forbidden_marker in content:
            failures.append(f"{path}: should not reference deleted production-team contracts")


def audit_stage_subagent_contracts(stage_index: list[dict], contract_mode: str, failures: list[str]) -> None:
    if contract_mode == BOOTSTRAP_COMPAT_MODE:
        return

    for stage in stage_index:
        if stage.get("contract_status") == "shelved":
            continue

        stage_root = Path(stage["path"])
        if not stage_root.exists():
            continue

        for doc in REQUIRED_STAGE_AGENT_DOCS.get(stage_root.name, ()):
            if not doc.exists():
                failures.append(f"{doc}: missing required {stage_root.name} subagent contract")

        for path in sorted(stage_root.rglob("*")):
            if not path.is_file() or path.suffix not in {".md", ".yaml"}:
                continue
            content = path.read_text(encoding="utf-8")
            for raw_ref in sorted(set(AGENT_REFERENCE_PATTERN.findall(content))):
                ref = Path(raw_ref)
                if not ref.exists():
                    failures.append(f"{path}: references missing agent contract `{raw_ref}`")


def audit_stage_index(stage_index: list[dict], contract_mode: str, failures: list[str]) -> None:
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

        if contract_mode == BOOTSTRAP_COMPAT_MODE:
            if not path.exists():
                failures.append(f"{path}: missing for active stage `{stage['id']}`")
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
    warnings: list[str] = []

    if not ROOT_SKILL.exists():
        failures.append(f"{ROOT_SKILL}: missing")
    else:
        root_content = ROOT_SKILL.read_text(encoding="utf-8")
        if "projects/<项目名>/" not in root_content:
            failures.append(f"{ROOT_SKILL}: missing canonical project-root runtime declaration")

    if ROOT_CONTEXT.exists() and ROOT_CONTEXT.stat().st_size == 0:
        failures.append(f"{ROOT_CONTEXT}: CONTEXT.md is empty")

    audit_all_context_hygiene(warnings)

    stage_index, satellite_index, contract_mode = audit_registry(failures)
    audit_routes(contract_mode, failures)
    audit_runtime_alignment(contract_mode, failures)
    audit_init_single_skill_contract(failures)
    audit_planning_internal_skill_contract(failures)
    audit_global_single_skill_contract(failures)
    audit_detail_single_skill_contract(failures)
    if stage_index:
        audit_stage_subagent_contracts(stage_index, contract_mode, failures)

    skipped_roots = shelved_stage_roots(stage_index)

    if ROOT_SKILL.exists():
        audit_skill_file(ROOT_SKILL, failures)

    if contract_mode != BOOTSTRAP_COMPAT_MODE:
        for skill_path in sorted(ROOT.rglob("SKILL.md")):
            if skill_path == ROOT_SKILL:
                continue
            if any(root in skill_path.parents for root in skipped_roots):
                continue
            audit_skill_file(skill_path, failures)

    if stage_index:
        audit_stage_index(stage_index, contract_mode, failures)
    if satellite_index:
        audit_satellite_index(satellite_index, failures)

    print("AIGC skill tree audit")
    print(f"repo_root: {Path.cwd()}")
    print(f"discovered_skill_docs: {len(list(ROOT.rglob('SKILL.md')))}")
    print(f"registry_stage_entries: {len(stage_index)}")
    print(f"registry_satellite_entries: {len(satellite_index)}")
    print(f"failures: {len(failures)}")
    print(f"warnings: {len(warnings)}")

    if failures:
        print("")
        print("Audit failures:")
        for failure in failures:
            print(f"- {failure}")
    if warnings:
        print("")
        print("Audit warnings:")
        for warning in warnings:
            print(f"- {warning}")
    if not failures and not warnings:
        print("")
        print("All checked AIGC skill contracts are aligned.")
    elif not failures:
        print("")
        print("All checked AIGC skill contracts passed strict checks; review warnings for context hygiene drift.")

    if args.strict and failures:
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
