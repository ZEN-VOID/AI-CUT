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
DESIGN_2_ROOT = ROOT / "4-Design" / "2-设计"
DESIGN_2_CANONICAL_TEMPLATES = {
    DESIGN_2_ROOT / "角色" / "templates" / "character_masterprompt.structured.v2.md",
    DESIGN_2_ROOT / "道具" / "templates" / "prop_masterprompt.structured.v2.md",
    DESIGN_2_ROOT / "场景" / "templates" / "scene_masterprompt.structured.v2.md",
}
DESIGN_SLOT_REVIEW_CONTRACT = DESIGN_2_ROOT / "_shared" / "design-slot-review-contract.md"
DESIGN_SLOT_RESOLVER = DESIGN_2_ROOT / "_shared" / "scripts" / "resolve_design_slot_bundles.py"
DESIGN_SUBAGENT_SUPERVISION_CONTRACT = DESIGN_2_ROOT / "_shared" / "subagent-supervision-contract.md"
DESIGN_SLOT_RUNTIME_MARKERS = (
    "slot_bundles",
    "SCENE-BUNDLE-01",
    "ROLE-BUNDLE-01",
    "PROP-BUNDLE-01",
    "design-slot-review-contract.md",
)
AMBIGUOUS_OUTPUT_TEMPLATE_NAME = "output-" "template.md"

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
]
CONTEXT_KB_SECTIONS = [
    "## Type Map",
    "## Repair Playbook",
    "## Reusable Heuristics",
]
DEFAULT_SOFT_LIMIT_CHARS = 20000
DEFAULT_HARD_LIMIT_CHARS = 40000
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
)
SUBTYPE_PATH_PREFIXES = ("subtypes/", "./subtypes/")
SHARED_RUNTIME_ROWS = {
    "0-Init": "projects/aigc/<项目名>/0-Init/",
    "Story": "projects/aigc/<项目名>/Story/",
    "1-Planning": "projects/aigc/<项目名>/1-Planning/",
    "2-Global": "projects/aigc/<项目名>/2-Global/",
    "3-Detail": "projects/aigc/<项目名>/3-Detail/",
    "4-Design": "projects/aigc/<项目名>/4-Design/",
    "5-Image": "projects/aigc/<项目名>/5-Image/",
    "6-Video": "projects/aigc/<项目名>/6-Video/",
    "7-Cut": "projects/aigc/<项目名>/7-Cut/",
}
ROOT_STAGE_LANDING = (
    "projects/aigc/<项目名>/0-Init/",
    "projects/aigc/<项目名>/Story/",
    "projects/aigc/<项目名>/1-Planning/",
    "projects/aigc/<项目名>/2-Global/",
    "projects/aigc/<项目名>/3-Detail/",
    "projects/aigc/<项目名>/4-Design/",
    "projects/aigc/<项目名>/5-Image/",
    "projects/aigc/<项目名>/6-Video/",
    "projects/aigc/<项目名>/7-Cut/",
)
ROOT_FORBIDDEN_STAGE_LANDING = (
    "projects/aigc/<项目名>/设定/",
    "projects/aigc/<项目名>/1-规划/",
    "projects/aigc/<项目名>/2-组间/",
    "projects/aigc/<项目名>/3-明细/",
    "projects/aigc/<项目名>/主体/",
    "projects/aigc/<项目名>/4-主体/",
    "projects/aigc/<项目名>/5-画面/",
    "projects/aigc/<项目名>/6-视频/",
    "projects/aigc/<项目名>/7-后期/",
)
PROJECT_GOVERNANCE_ARTIFACTS = (
    "projects/aigc/<项目名>/STATE.json",
    "projects/aigc/<项目名>/governance-state.yaml",
)
COUNCIL_STAGE_REVIEW_PATHS = {
    "1-Planning": "projects/aigc/<项目名>/1-Planning/validation-report.md",
    "2-Global": "projects/aigc/<项目名>/2-Global/validation-report.md",
    "3-Detail": "projects/aigc/<项目名>/3-Detail/validation-report.md",
    "4-Design": "projects/aigc/<项目名>/4-Design/validation-report.md",
}
PROJECT_LEVEL_VALIDATION_REPORT = "projects/aigc/<项目名>/validation-report.md"
STAGE_RUNTIME_EXPECTATIONS = {
    ROOT / "0-Init" / "SKILL.md": (
        "projects/aigc/<项目名>/0-Init/",
        "projects/aigc/<项目名>/Story/",
        "projects/aigc/<项目名>/Assets/",
        "projects/aigc/<项目名>/Assets/角色/",
        "projects/aigc/<项目名>/Assets/道具/",
        "projects/aigc/<项目名>/Assets/场景/",
        "projects/aigc/<项目名>/Assets/服装/",
        "projects/aigc/<项目名>/Assets/分镜画板/分镜帧/",
        "projects/aigc/<项目名>/Assets/分镜画板/分镜故事板/",
        "projects/aigc/<项目名>/Assets/分镜画板/漫画/",
        "projects/aigc/<项目名>/1-Planning/",
        "projects/aigc/<项目名>/1-Planning/1-分集/",
        "projects/aigc/<项目名>/1-Planning/2-格式/",
        "projects/aigc/<项目名>/1-Planning/3-分组/",
        "projects/aigc/<项目名>/2-Global/",
        "projects/aigc/<项目名>/3-Detail/",
        "projects/aigc/<项目名>/3-Detail/水月/",
        "projects/aigc/<项目名>/3-Detail/镜花/",
        "projects/aigc/<项目名>/4-Design/",
        "projects/aigc/<项目名>/4-Design/场景/1-清单/",
        "projects/aigc/<项目名>/4-Design/场景/2-设计/",
        "projects/aigc/<项目名>/4-Design/场景/3-面板/",
        "projects/aigc/<项目名>/4-Design/角色/1-清单/",
        "projects/aigc/<项目名>/4-Design/角色/2-设计/",
        "projects/aigc/<项目名>/4-Design/角色/3-面板/",
        "projects/aigc/<项目名>/4-Design/道具/1-清单/",
        "projects/aigc/<项目名>/4-Design/道具/2-设计/",
        "projects/aigc/<项目名>/4-Design/道具/3-面板/",
        "projects/aigc/<项目名>/5-Image/",
        "projects/aigc/<项目名>/5-Image/分镜故事板/",
        "projects/aigc/<项目名>/5-Image/分镜帧/",
        "projects/aigc/<项目名>/5-Image/漫画/",
        "projects/aigc/<项目名>/5-Image/2-参照引用/",
        "projects/aigc/<项目名>/5-Image/3-图像生成/",
        "projects/aigc/<项目名>/6-Video/",
        "projects/aigc/<项目名>/6-Video/全能参照/",
        "projects/aigc/<项目名>/6-Video/首帧参照/",
        "projects/aigc/<项目名>/6-Video/生成任务/",
        "projects/aigc/<项目名>/7-Cut/",
    ),
    ROOT / "1-Planning" / "SKILL.md": (
        "projects/aigc/<项目名>/1-Planning/",
        "projects/aigc/<项目名>/1-Planning/validation-report.md",
    ),
    ROOT / "4-Design" / "SKILL.md": (
        "projects/aigc/<项目名>/4-Design/",
    ),
    ROOT / "5-Image" / "1-提示词蒸馏" / "SKILL.md": (
        "projects/aigc/<项目名>/5-Image/",
        "projects/aigc/<项目名>/5-Image/分镜故事板/",
        "projects/aigc/<项目名>/5-Image/分镜帧/",
        "projects/aigc/<项目名>/5-Image/漫画/",
    ),
    ROOT / "5-Image" / "SKILL.md": (
        "projects/aigc/<项目名>/5-Image/",
        "projects/aigc/<项目名>/5-Image/分镜故事板/",
        "projects/aigc/<项目名>/5-Image/分镜帧/",
        "projects/aigc/<项目名>/5-Image/漫画/",
        "projects/aigc/<项目名>/5-Image/2-参照引用/",
        "projects/aigc/<项目名>/5-Image/3-图像生成/",
    ),
    ROOT / "5-Image" / "3-图像生成" / "SKILL.md": (
        "projects/aigc/<项目名>/5-Image/3-图像生成/",
        "output_dir",
        "expected_outputs",
        "result_outputs",
    ),
    ROOT / "6-Video" / "SKILL.md": (
        "projects/aigc/<项目名>/6-Video/",
        "projects/aigc/<项目名>/6-Video/全能参照/",
        "projects/aigc/<项目名>/6-Video/首帧参照/",
        "projects/aigc/<项目名>/6-Video/生成任务/",
    ),
}
STAGE_RUNTIME_FORBIDDEN = {
    ROOT / "0-Init" / "SKILL.md": (
        "projects/aigc/<项目名>/主体/",
        "projects/aigc/<项目名>/4-主体/",
        "projects/aigc/<项目名>/5-画面/",
        "projects/aigc/<项目名>/6-视频/",
        "projects/aigc/<项目名>/2-组间/validation-report.md",
        "projects/aigc/<项目名>/3-明细/validation-report.md",
    ),
    ROOT / "1-Planning" / "SKILL.md": (
        "runtime 根目录：`projects/aigc/<项目名>/0-Init/`",
        "阶段验证报告：`projects/aigc/<项目名>/0-Init/validation-report.md`",
    ),
    ROOT / "6-Video" / "SKILL.md": (
        "projects/aigc/<项目名>/设定/",
        "projects/aigc/<项目名>/5-画面/",
        "projects/aigc/<项目名>/主体/",
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
    "aigc-image-stage-entry",
}
REQUIRED_STAGE_AGENT_DOCS = {
}
AGENT_REFERENCE_PATTERN = re.compile(r"\.codex/agents/aigc/[^\s`)\]>\"']+\.md")
BOOTSTRAP_COMPAT_MODE = "bootstrap_compat"
BOOTSTRAP_COMPAT_ROUTE_POLICIES = {
    "aigc-bootstrap-compat-mode",
}
BOOTSTRAP_COMPAT_STAGE_CHILD_SKILLS = {
    ROOT / "5-Image": (
        ROOT / "5-Image" / "1-提示词蒸馏" / "SKILL.md",
        ROOT / "5-Image" / "1-提示词蒸馏" / "分镜故事板" / "SKILL.md",
        ROOT / "5-Image" / "1-提示词蒸馏" / "分镜帧" / "SKILL.md",
        ROOT / "5-Image" / "1-提示词蒸馏" / "漫画" / "SKILL.md",
        ROOT / "5-Image" / "2-参照引用" / "SKILL.md",
        ROOT / "5-Image" / "3-图像生成" / "SKILL.md",
    ),
    ROOT / "6-Video": (
        ROOT / "6-Video" / "1-提示词蒸馏" / "全能参照" / "SKILL.md",
        ROOT / "6-Video" / "1-提示词蒸馏" / "首帧参照" / "SKILL.md",
        ROOT / "6-Video" / "2-参照引用" / "SKILL.md",
        ROOT / "6-Video" / "3-视频生成" / "SKILL.md",
    ),
    ROOT / "review": (
        ROOT / "review" / "subtypes" / "preflight-review" / "SKILL.md",
        ROOT / "review" / "subtypes" / "acceptance-review" / "SKILL.md",
        ROOT / "review" / "subtypes" / "learning-bridge" / "SKILL.md",
    ),
}
BOOTSTRAP_COMPAT_RUNTIME_EXPECTATIONS = {
    ROOT / "_shared" / "project-runtime-layout.md": (
        ".agents/skills/aigc/6-Video/2-参照引用",
        ".agents/skills/aigc/6-Video/3-视频生成",
        "projects/aigc/<项目名>/6-Video/2-参照引用/",
        "projects/aigc/<项目名>/6-Video/生成任务/",
    ),
    ROOT / "0-Init" / "SKILL.md": (
        "1-提示词蒸馏/全能参照`、`1-提示词蒸馏/首帧参照`、`2-参照引用`、`3-视频生成",
        "6-Video/2-参照引用/",
        "6-Video/生成任务/",
    ),
}
BOOTSTRAP_COMPAT_RUNTIME_FORBIDDEN = {
    ROOT / "_shared" / "project-runtime-layout.md": (
        ".agents/skills/aigc/6-Video/2-视频生成",
    ),
    ROOT / "0-Init" / "SKILL.md": (
        "技能树 active 路径：`1-提示词蒸馏/全能参照`、`1-提示词蒸馏/首帧参照`、`2-视频生成`",
        "`生成任务/` 是 `2-视频生成` 的业务语义落盘名",
    ),
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


def has_stale_case_log_markup(content: str) -> bool:
    return any(
        pattern.search(content)
        for pattern in (
            re.compile(r"^##\s+Case Log\s*$", re.MULTILINE),
            re.compile(r"^###\s+Case-", re.MULTILINE),
            re.compile(r"^- milestone_type:", re.MULTILINE),
        )
    )


def audit_context_quality(context_path: Path, context: str, warnings: list[str]) -> None:
    char_count = len(context)
    soft_limit_chars = extract_context_limit(context, "soft_limit_chars", DEFAULT_SOFT_LIMIT_CHARS)
    hard_limit_chars = extract_context_limit(context, "hard_limit_chars", DEFAULT_HARD_LIMIT_CHARS)

    if char_count >= soft_limit_chars:
        warnings.append(
            f"{context_path}: chars={char_count} reached soft limit {soft_limit_chars}; compact KB or move long timelines to CHANGELOG.md"
        )
    if char_count >= hard_limit_chars:
        warnings.append(
            f"{context_path}: chars={char_count} reached hard limit {hard_limit_chars}; archive older material before further growth"
        )
    if has_stale_case_log_markup(context):
        warnings.append(
            f"{context_path}: found stale `Case Log` / `Case-*` / `milestone_type` markup; migrate details to CHANGELOG.md or reports and keep CONTEXT.md KB-only"
        )


def audit_all_context_hygiene(warnings: list[str]) -> None:
    for context_path in sorted(ROOT.rglob("CONTEXT.md")):
        if not context_path.exists() or context_path.stat().st_size == 0:
            continue
        audit_context_quality(context_path, context_path.read_text(encoding="utf-8"), warnings)


def audit_skill_file(path: Path, failures: list[str], checked_paths: set[Path] | None = None) -> None:
    if checked_paths is not None:
        checked_paths.add(path)
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
    if has_stale_case_log_markup(context):
        failures.append(f"{context_path}: contains deprecated `Case Log` / `Case-*` / `milestone_type` markup")
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
    if runtime_control.get("canonical_project_runtime") != "projects/aigc/<项目名>/":
        failures.append(
            f"{REGISTRY}: `aigc.runtime_control.canonical_project_runtime` must be `projects/aigc/<项目名>/`"
        )
    if runtime_control.get("project_state_carrier") != "projects/aigc/<项目名>/STATE.json":
        failures.append(
            f"{REGISTRY}: `aigc.runtime_control.project_state_carrier` must be `projects/aigc/<项目名>/STATE.json`"
        )
    if runtime_control.get("governance_state_carrier") != "projects/aigc/<项目名>/governance-state.yaml":
        failures.append(
            f"{REGISTRY}: `aigc.runtime_control.governance_state_carrier` must be `projects/aigc/<项目名>/governance-state.yaml`"
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

    if aigc_runtime.get("canonical_runtime_root") != "projects/aigc/<项目名>/":
        failures.append(f"{ROUTES}: `aigc-project-runtime` canonical root mismatch")
    if aigc_runtime.get("project_state_carrier") != "projects/aigc/<项目名>/STATE.json":
        failures.append(f"{ROUTES}: `aigc-project-runtime` project_state carrier mismatch")
    if aigc_runtime.get("governance_state_carrier") != "projects/aigc/<项目名>/governance-state.yaml":
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
        for path, expected_markers in BOOTSTRAP_COMPAT_RUNTIME_EXPECTATIONS.items():
            if not path.exists():
                failures.append(f"{path}: missing")
                continue
            content = path.read_text(encoding="utf-8")
            for marker in expected_markers:
                if marker not in content:
                    failures.append(f"{path}: missing bootstrap runtime marker `{marker}`")

        for path, forbidden_markers in BOOTSTRAP_COMPAT_RUNTIME_FORBIDDEN.items():
            if not path.exists():
                continue
            content = path.read_text(encoding="utf-8")
            for marker in forbidden_markers:
                if marker in content:
                    failures.append(f"{path}: contains stale bootstrap runtime marker `{marker}`")
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


def audit_stage_review_carriers(failures: list[str]) -> None:
    """Ensure stage parent contracts do not drift from their canonical review carriers."""
    for stage_name, review_path in COUNCIL_STAGE_REVIEW_PATHS.items():
        skill_path = ROOT / stage_name / "SKILL.md"
        if not skill_path.exists():
            continue

        content = skill_path.read_text(encoding="utf-8")
        if "validation-report.md" not in content:
            continue

        if review_path not in content:
            failures.append(
                f"{skill_path}: missing canonical stage review carrier `{review_path}`"
            )
        if review_path != PROJECT_LEVEL_VALIDATION_REPORT and PROJECT_LEVEL_VALIDATION_REPORT in content:
            failures.append(
                f"{skill_path}: contains project-level review carrier "
                f"`{PROJECT_LEVEL_VALIDATION_REPORT}`; expected stage carrier `{review_path}`"
            )


def audit_design_2_template_registry(failures: list[str]) -> None:
    """Ensure 4-Design/2-设计 has exactly one Markdown template truth per domain."""
    if not DESIGN_2_ROOT.exists():
        return

    for stale_template in sorted(DESIGN_2_ROOT.rglob(AMBIGUOUS_OUTPUT_TEMPLATE_NAME)):
        failures.append(f"{stale_template}: remove ambiguous legacy output template reference; use canonical templates instead")

    shared_contract = DESIGN_2_ROOT / "_shared" / "design-output-contract.md"
    if not shared_contract.exists():
        failures.append(f"{shared_contract}: missing shared output contract")
        return

    shared_content = shared_contract.read_text(encoding="utf-8")
    if "## Markdown Template Registry" not in shared_content:
        failures.append(f"{shared_contract}: missing `Markdown Template Registry`")

    for template_path in sorted(DESIGN_2_CANONICAL_TEMPLATES):
        if not template_path.exists():
            failures.append(f"{template_path}: missing canonical design Markdown template")
            continue
        if template_path.as_posix() not in shared_content:
            failures.append(f"{shared_contract}: missing canonical template `{template_path.as_posix()}`")

    renderer_expectations = {
        DESIGN_2_ROOT / "场景" / "scripts" / "build_scene_design_packets.py": "scene_masterprompt.structured.v2.md",
        DESIGN_2_ROOT / "道具" / "scripts" / "build_prop_design_packets.py": "prop_masterprompt.structured.v2.md",
    }
    for renderer, template_name in renderer_expectations.items():
        if not renderer.exists():
            failures.append(f"{renderer}: missing renderer for canonical template `{template_name}`")
            continue
        renderer_content = renderer.read_text(encoding="utf-8")
        if template_name not in renderer_content or "TEMPLATE_PATH" not in renderer_content:
            failures.append(f"{renderer}: renderer must bind `TEMPLATE_PATH` to `{template_name}`")

    template_like_markers = ("```md", "**物语**", "**解构**", "**prompt整合**")
    for path in sorted(DESIGN_2_ROOT.rglob("*.md")):
        if path in DESIGN_2_CANONICAL_TEMPLATES:
            continue
        content = path.read_text(encoding="utf-8")
        if all(marker in content for marker in template_like_markers):
            failures.append(
                f"{path}: contains a complete Markdown card template; move structure to the canonical `templates/*.structured.v2.md` file"
            )


def audit_design_slot_bundle_runtime(failures: list[str]) -> None:
    """Ensure slot-bundle governance has a real execution carrier, not docs only."""
    if not DESIGN_2_ROOT.exists():
        return

    if not DESIGN_SLOT_REVIEW_CONTRACT.exists():
        failures.append(f"{DESIGN_SLOT_REVIEW_CONTRACT}: missing shared slot-review contract")
        return

    if not DESIGN_SLOT_RESOLVER.exists():
        failures.append(
            f"{DESIGN_SLOT_RESOLVER}: missing slot-bundle resolver runtime for `design-slot-review-contract.md`"
        )
    else:
        resolver_content = DESIGN_SLOT_RESOLVER.read_text(encoding="utf-8")
        for marker in DESIGN_SLOT_RUNTIME_MARKERS:
            if marker not in resolver_content:
                failures.append(
                    f"{DESIGN_SLOT_RESOLVER}: missing runtime marker `{marker}` for slot-bundle resolution"
                )

    if not DESIGN_SUBAGENT_SUPERVISION_CONTRACT.exists():
        failures.append(f"{DESIGN_SUBAGENT_SUPERVISION_CONTRACT}: missing shared supervision contract")
        return

    supervision_content = DESIGN_SUBAGENT_SUPERVISION_CONTRACT.read_text(encoding="utf-8")
    for marker in ("slot_bundle_findings", "slot_bundles: []", "design-slot-review-contract.md"):
        if marker not in supervision_content:
            failures.append(
                f"{DESIGN_SUBAGENT_SUPERVISION_CONTRACT}: missing slot-bundle marker `{marker}`"
            )


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
    for removed_mode in ("主创会诊模式", "快速成案模式", "自主问答模式"):
        if f"| {removed_mode} |" in init_content:
            failures.append(f"{init_skill}: legacy init mode `{removed_mode}` should not remain in the active mode table")
    if "`0-Init` 现只允许 `init_mode == smart_advisor`；旧的 `主创会诊模式 / 快速成案模式 / 自主问答模式` 全部失效。" not in init_content:
        failures.append(f"{init_skill}: missing explicit single-mode smart-advisor rule for 0-Init")
    if "开场必须展示“初始化元选项卡”，让用户在 `自动组队 / 自定义组队` 间拍板；不得无确认自动锁 `team_lineup_mode`。" not in init_content:
        failures.append(f"{init_skill}: missing explicit gate that `team_lineup_mode` must be user-confirmed")
    if "固定 `init_mode = smart_advisor`；若用户尚未明确选择 `auto/custom`，发送一次初始化元选项卡并等待确认。" not in init_content:
        failures.append(f"{init_skill}: missing execution-step lock for `smart_advisor` plus `auto/custom` lineup choice")
    if "planning interview 必须真实使用 subagents" not in init_content:
        failures.append(f"{init_skill}: missing mandatory subagent rule for the planning interview")
    if "若 subagents 不可用，本轮初始化停止并报告阻塞" not in init_content:
        failures.append(f"{init_skill}: missing block-and-report rule when init interview subagents are unavailable")
    if "selector_scope_root" not in init_content or ".agents/skills/team/" not in init_content:
        failures.append(f"{init_skill}: missing explicit selector-scope rule for `.agents/skills/team/`")
    if "## Story Source Completeness Gate (Mandatory)" not in init_content:
        failures.append(f"{init_skill}: missing `Story Source Completeness Gate (Mandatory)`")
    if "## Story Source Reconciliation Contract (Mandatory)" not in init_content:
        failures.append(f"{init_skill}: missing `Story Source Reconciliation Contract (Mandatory)`")
    if "source-light bootstrap" not in init_content or "source-grounded bootstrap" not in init_content:
        failures.append(
            f"{init_skill}: missing explicit split between source-light and source-grounded bootstrap modes"
        )
    if "必须先执行一次回刷对齐" not in init_content:
        failures.append(
            f"{init_skill}: missing explicit rule that backfilled story sources must trigger init artifact reconciliation"
        )
    if "## Stage Entry Ownership Contract (Mandatory)" not in init_content:
        failures.append(f"{init_skill}: missing `Stage Entry Ownership Contract (Mandatory)`")
    if "`north_star.yaml` 不得出现 `stage_entry_contract`、`recommended_next_stage`、`stage_priority_order`、`rebootstrap_status` 等状态型字段。" not in init_content:
        failures.append(
            f"{init_skill}: missing explicit prohibition that `north_star.yaml` must not own stage-entry or reset-state fields"
        )

    north_star_template = ROOT / "0-Init" / "templates" / "north-star.template.yaml"
    if north_star_template.exists():
        north_star_template_content = north_star_template.read_text(encoding="utf-8")
        for forbidden_marker in ("stage_entry_contract:", "rebootstrap_status:"):
            if forbidden_marker in north_star_template_content:
                failures.append(
                    f"{north_star_template}: contains forbidden init-state field `{forbidden_marker.rstrip(':')}`"
                )

    init_openai = ROOT / "0-Init" / "agents" / "openai.yaml"
    if init_openai.exists() and ".codex/agents/aigc/初始组/" in init_openai.read_text(encoding="utf-8"):
        failures.append(f"{init_openai}: should not reference external init-agent contracts")

    team_template = ROOT / "_shared" / "council-runtime" / "team.template.yaml"
    if team_template.exists():
        team_template_content = team_template.read_text(encoding="utf-8")
        for required_marker in (
            'init_mode: "smart_advisor"',
            'team_lineup_mode: "auto"',
            'selector_scope_root: ".agents/skills/team/"',
            'require_subagents_for_init_interview: true',
            'init_interview_owner_role: "planning"',
        ):
            if required_marker not in team_template_content:
                failures.append(f"{team_template}: missing smart-advisor team marker `{required_marker}`")

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
        planning_root / "2-格式" / "SKILL.md",
        planning_root / "2-格式" / "agents" / "openai.yaml",
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
        global_root / "templates" / "全集类型元素.template.md",
        global_root / "templates" / "分组类型元素.template.md",
        global_root / "templates" / "导演意图.template.md",
    )

    skill_content = global_skill.read_text(encoding="utf-8")
    if "## Internal Capability Fusion Contract (Mandatory)" not in skill_content:
        failures.append(f"{global_skill}: missing `Internal Capability Fusion Contract (Mandatory)`")
    if forbidden_marker in skill_content:
        failures.append(
            f"{global_skill}: 2-Global must internalize style/type/director capabilities into the parent SKILL instead of referencing `.codex/agents/aigc/导演组/`"
        )

    required_root_outputs = (
        "projects/aigc/<项目名>/2-Global/全局风格.md",
        "projects/aigc/<项目名>/2-Global/导演意图.md",
        "projects/aigc/<项目名>/2-Global/全集类型元素.md",
        "projects/aigc/<项目名>/2-Global/分组类型元素.md",
    )
    io_contract = global_root / "_shared" / "IO_CONTRACT.md"
    if io_contract.exists():
        io_content = io_contract.read_text(encoding="utf-8")
        for output_path in required_root_outputs:
            if output_path not in io_content:
                failures.append(f"{io_contract}: missing canonical output `{output_path}`")
        if "| derived | `projects/aigc/<项目名>/2-Global/类型元素.md`" in io_content:
            failures.append(f"{io_contract}: old `类型元素.md` compatibility projection must not remain an output row")

    if (global_root / "templates" / "类型元素.template.md").exists():
        failures.append(f"{global_root / 'templates' / '类型元素.template.md'}: old combined type template should be split into `全集类型元素.template.md` and `分组类型元素.template.md`")

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

        skill_path = path / "SKILL.md"
        context_path = path / "CONTEXT.md"
        if not path.exists():
            failures.append(f"{path}: missing for active stage `{stage['id']}`")
            continue
        if not skill_path.exists():
            failures.append(f"{skill_path}: missing for active stage `{stage['id']}`")
        if not context_path.exists():
            failures.append(f"{context_path}: missing for active stage `{stage['id']}`")

        if contract_mode == BOOTSTRAP_COMPAT_MODE:
            continue


def audit_bootstrap_compat_active_stage_parents(
    stage_index: list[dict], failures: list[str], checked_paths: set[Path]
) -> None:
    """Keep active stage parent contracts auditable during bootstrap_compat."""
    for stage in stage_index:
        if stage.get("contract_status") != "active":
            continue
        skill_path = Path(stage["path"]) / "SKILL.md"
        if not skill_path.exists():
            continue
        audit_skill_file(skill_path, failures, checked_paths)


def bootstrap_compat_governed_leaf_skills(stage_index: list[dict]) -> set[Path]:
    governed: set[Path] = set()

    for stage in stage_index:
        for leaf in stage.get("leaf_index", []):
            if leaf.get("contract_status") not in {"active", "partial-active"}:
                continue
            governed.add(Path(leaf["path"]) / "SKILL.md")

    for stage_root, child_skills in BOOTSTRAP_COMPAT_STAGE_CHILD_SKILLS.items():
        if not stage_root.exists():
            continue
        governed.update(child_skills)

    return governed


def audit_bootstrap_compat_governed_leaf_skills(
    stage_index: list[dict], failures: list[str], checked_paths: set[Path]
) -> None:
    for skill_path in sorted(bootstrap_compat_governed_leaf_skills(stage_index)):
        if not skill_path.exists():
            failures.append(f"{skill_path}: missing for bootstrap_compat governed leaf")
            continue
        audit_skill_file(skill_path, failures, checked_paths)


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


def audit_bootstrap_compat_satellite_roots(
    satellite_index: list[dict], failures: list[str], checked_paths: set[Path]
) -> None:
    for entry in satellite_index:
        skill_path = Path(entry["path"]) / "SKILL.md"
        if not skill_path.exists():
            continue
        audit_skill_file(skill_path, failures, checked_paths)


def shelved_stage_roots(stage_index: list[dict]) -> list[Path]:
    return [Path(stage["path"]) for stage in stage_index if stage.get("contract_status") == "shelved"]


def main() -> int:
    args = parse_args()
    failures: list[str] = []
    warnings: list[str] = []
    checked_skill_paths: set[Path] = set()

    if not ROOT_SKILL.exists():
        failures.append(f"{ROOT_SKILL}: missing")
    else:
        root_content = ROOT_SKILL.read_text(encoding="utf-8")
        if "projects/aigc/<项目名>/" not in root_content:
            failures.append(f"{ROOT_SKILL}: missing canonical project-root runtime declaration")

    if ROOT_CONTEXT.exists() and ROOT_CONTEXT.stat().st_size == 0:
        failures.append(f"{ROOT_CONTEXT}: CONTEXT.md is empty")

    audit_all_context_hygiene(warnings)

    stage_index, satellite_index, contract_mode = audit_registry(failures)
    audit_routes(contract_mode, failures)
    audit_runtime_alignment(contract_mode, failures)
    audit_stage_review_carriers(failures)
    audit_design_2_template_registry(failures)
    audit_design_slot_bundle_runtime(failures)
    audit_init_single_skill_contract(failures)
    audit_planning_internal_skill_contract(failures)
    audit_global_single_skill_contract(failures)
    audit_detail_single_skill_contract(failures)
    if stage_index:
        audit_stage_subagent_contracts(stage_index, contract_mode, failures)

    skipped_roots = shelved_stage_roots(stage_index)

    if ROOT_SKILL.exists():
        audit_skill_file(ROOT_SKILL, failures, checked_skill_paths)

    if contract_mode == BOOTSTRAP_COMPAT_MODE:
        if stage_index:
            audit_bootstrap_compat_active_stage_parents(stage_index, failures, checked_skill_paths)
            audit_bootstrap_compat_governed_leaf_skills(stage_index, failures, checked_skill_paths)
        if satellite_index:
            audit_bootstrap_compat_satellite_roots(satellite_index, failures, checked_skill_paths)
    else:
        for skill_path in sorted(ROOT.rglob("SKILL.md")):
            if skill_path == ROOT_SKILL:
                continue
            if any(root in skill_path.parents for root in skipped_roots):
                continue
            audit_skill_file(skill_path, failures, checked_skill_paths)

    if stage_index:
        audit_stage_index(stage_index, contract_mode, failures)
    if satellite_index:
        audit_satellite_index(satellite_index, failures)

    discovered_skill_docs = sorted(ROOT.rglob("SKILL.md"))
    skipped_skill_docs = [path for path in discovered_skill_docs if path not in checked_skill_paths]

    print("AIGC skill tree audit")
    print(f"repo_root: {Path.cwd()}")
    print(f"discovered_skill_docs: {len(discovered_skill_docs)}")
    print(f"checked_skill_docs: {len(checked_skill_paths)}")
    print(f"skipped_skill_docs: {len(skipped_skill_docs)}")
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
