#!/usr/bin/env python3
"""Backfill governance-state.yaml for existing AIGC project runtimes."""

from __future__ import annotations

import argparse
import copy
import json
import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import yaml


REPO_ROOT = Path(__file__).resolve().parents[1]
PROJECTS_ROOT = REPO_ROOT / "projects" / "aigc"
TEMPLATE_PATH = REPO_ROOT / ".agents/skills/aigc/_shared/governance-state.template.yaml"
CANONICAL_STATE_FILENAME = "STATE.json"
LEGACY_STATE_FILENAME = "project_state.yaml"
STAGE_PATH_PATTERN = re.compile(r"\d+-[^\s/，。,；;（）()]+(?:/\d+-[^\s，。,；;（）()]+)?")
PREFERRED_ENTRY_PATTERNS = (
    re.compile(r"下一步进入\s*(" + STAGE_PATH_PATTERN.pattern + r")"),
    re.compile(r"优先进入\s*(" + STAGE_PATH_PATTERN.pattern + r")"),
    re.compile(r"推荐.*?进入\s*(" + STAGE_PATH_PATTERN.pattern + r")"),
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Backfill projects/aigc/<项目名>/governance-state.yaml from existing AIGC governance artifacts."
    )
    parser.add_argument(
        "--project",
        action="append",
        default=[],
        help=(
            "Specific project name(s) under projects/aigc/ to backfill. "
            f"Defaults to every project with {CANONICAL_STATE_FILENAME} "
            f"(or legacy {LEGACY_STATE_FILENAME})."
        ),
    )
    parser.add_argument(
        "--write",
        action="store_true",
        help="Write governance-state.yaml files. Without this flag, only print a preview.",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Overwrite an existing governance-state.yaml.",
    )
    return parser.parse_args()


def load_yaml(path: Path) -> dict[str, Any]:
    return yaml.safe_load(path.read_text(encoding="utf-8")) or {}


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8")) or {}


def load_yaml_optional(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    return load_yaml(path)


def resolve_project_state_path(project_root: Path) -> Path | None:
    canonical = project_root / CANONICAL_STATE_FILENAME
    if canonical.exists():
        return canonical

    legacy = project_root / LEGACY_STATE_FILENAME
    if legacy.exists():
        return legacy

    return None


def load_project_state_optional(project_root: Path) -> tuple[dict[str, Any], Path]:
    project_state_path = resolve_project_state_path(project_root)
    if project_state_path is None:
        return {}, project_root / CANONICAL_STATE_FILENAME
    if project_state_path.suffix == ".json":
        return load_json(project_state_path), project_state_path
    return load_yaml(project_state_path), project_state_path


def read_text_optional(path: Path) -> str:
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8")


def file_status(path: Path) -> str:
    return "present" if path.exists() else "missing"


def first_non_empty(*values: Any) -> str:
    for value in values:
        if isinstance(value, str) and value.strip():
            return value.strip()
    return ""


def extract_stage_candidates(*texts: str) -> list[str]:
    candidates: list[str] = []
    seen: set[str] = set()
    for text in texts:
        for match in STAGE_PATH_PATTERN.findall(text or ""):
            if match not in seen:
                seen.add(match)
                candidates.append(match)
    return candidates


def extract_preferred_entry(text: str) -> str:
    for pattern in PREFERRED_ENTRY_PATTERNS:
        match = pattern.search(text or "")
        if match:
            return match.group(1)
    return ""


def stage_root_of(path_or_stage: str) -> str:
    if not path_or_stage:
        return ""
    return path_or_stage.split("/", 1)[0]


def infer_focus_path(
    project_state: dict[str, Any],
    route_plan: dict[str, Any],
    init_handoff: dict[str, Any],
) -> tuple[str, str, str, list[str]]:
    route_notes = route_plan.get("handoff_notes") or []
    route_text = "\n".join(str(item) for item in route_notes)
    handoff_project_contract = init_handoff.get("project_contract") or {}
    step_text = str(project_state.get("recommended_next_step", ""))
    explicit_preferred_entries = [
        entry
        for entry in (
            first_non_empty(str(project_state.get("recommended_entry_path", ""))),
            extract_preferred_entry(step_text),
            extract_preferred_entry(route_text),
            first_non_empty(str(handoff_project_contract.get("recommended_next_stage", ""))),
        )
        if entry
    ]

    stage_candidates = extract_stage_candidates(
        step_text,
        route_text,
        str(project_state.get("recommended_entry_path", "")),
        str(handoff_project_contract.get("recommended_next_stage", "")),
    )
    recommended_stage = first_non_empty(
        project_state.get("recommended_next_stage"),
        handoff_project_contract.get("recommended_next_stage"),
        stage_root_of(project_state.get("current_stage", "")),
    )

    preferred_path = first_non_empty(
        project_state.get("recommended_entry_path"),
        extract_preferred_entry(step_text),
        extract_preferred_entry(route_text),
        handoff_project_contract.get("recommended_next_stage"),
    )

    if not preferred_path and recommended_stage:
        preferred_path = next(
            (candidate for candidate in stage_candidates if stage_root_of(candidate) == recommended_stage),
            "",
        )

    if not preferred_path:
        preferred_path = first_non_empty(
            stage_candidates[0] if stage_candidates else "",
            project_state.get("current_stage", ""),
            recommended_stage,
        )

    rationale = first_non_empty(
        project_state.get("recommended_next_step"),
        route_notes[0] if route_notes else "",
        handoff_project_contract.get("acceptance_hint"),
    )

    required_repairs: list[str] = []
    if len(set(explicit_preferred_entries)) > 1:
        required_repairs.append(
            "统一 `project_state / route-plan / init_handoff` 中的下一入口表达，避免多条 stage path 并存。"
        )
    if recommended_stage and preferred_path and stage_root_of(preferred_path) != recommended_stage:
        required_repairs.append(
            "校正 `recommended_next_stage` 与更具体的 `recommended_entry_path`，避免 stage root 与 subtype path 脱节。"
        )

    return recommended_stage, preferred_path, rationale, required_repairs


def map_skill_from_path(path_or_stage: str) -> str:
    mapping = {
        "0-Init": "aigc-init",
        "1-Planning": "aigc-planning",
        "1-Planning/1-分集": "aigc-planning-episode-splitter",
        "1-Planning/2-格式": "aigc-planning-script",
        "1-Planning/3-分组": "aigc-planning-grouping",
        "1-规划": "aigc-planning",
        "1-规划/1-分集": "aigc-planning-episode-split",
        "1-规划/2-格式": "aigc-planning-format",
        "1-规划/3-分组": "aigc-planning-grouping",
        "1-规划/4-节奏": "aigc-planning-rhythm",
        "2-组间": "aigc-global",
        "2-Global": "aigc-global",
        "3-明细": "aigc-detail",
        "3-Detail": "aigc-detail",
        "4-Design": "aigc-design",
        "4-主体": "aigc-subject",
        "5-Image": "aigc-visual-prompt-distillation",
        "5-画面": "aigc-visuals",
        "6-Video": "aigc-video",
        "6-视频": "aigc-video",
        "7-Cut": "aigc-cut",
        "query": "aigc-query",
        "resume": "aigc-resume",
        "review": "aigc-review",
    }
    if path_or_stage in mapping:
        return mapping[path_or_stage]
    return mapping.get(stage_root_of(path_or_stage), "aigc")


def infer_phase(project_root: Path, project_state: dict[str, Any]) -> str:
    current_stage = str(project_state.get("current_stage", "")).strip()
    current_stage_root = stage_root_of(current_stage)
    learning = read_text_optional(project_root / "learning-record.md").strip()
    validation = read_text_optional(project_root / "validation-report.md").strip()
    preflight = read_text_optional(project_root / "preflight-verdict.yaml").strip()
    route_plan = read_text_optional(project_root / "route-plan.yaml").strip()
    mission_brief = read_text_optional(project_root / "mission-brief.yaml").strip()

    stage_dirs = [
        project_root / "1-Planning",
        project_root / "2-Global",
        project_root / "3-Detail",
        project_root / "4-Design",
        project_root / "5-Image",
        project_root / "6-Video",
        project_root / "7-Cut",
        project_root / "规划",
        project_root / "编导",
        project_root / "主体",
        project_root / "画面",
        project_root / "视频",
        project_root / "后期",
    ]
    has_stage_outputs = any(
        stage_dir.exists() and any(path.is_file() for path in stage_dir.rglob("*"))
        for stage_dir in stage_dirs
    )

    if current_stage_root in {
        "1-Planning",
        "1-规划",
        "2-Global",
        "2-组间",
        "3-Detail",
        "3-明细",
        "4-Design",
        "4-主体",
        "5-Image",
        "5-画面",
        "6-Video",
        "6-视频",
        "7-Cut",
        "7-后期",
    }:
        return "执行"
    if learning:
        return "沉淀"
    if validation:
        return "验收"
    if preflight:
        return "预审"
    if has_stage_outputs:
        return "执行"
    if route_plan or mission_brief:
        return "起草"
    return "受命"


def parse_preflight_status(project_root: Path) -> str:
    data = load_yaml_optional(project_root / "preflight-verdict.yaml")
    verdict = str(data.get("verdict", "")).strip().lower()
    return verdict or file_status(project_root / "preflight-verdict.yaml")


def parse_validation_status(project_root: Path) -> str:
    content = read_text_optional(project_root / "validation-report.md")
    match = re.search(r"verdict:\s*`?([A-Za-z_-]+)`?", content)
    if match:
        return match.group(1).lower()
    return file_status(project_root / "validation-report.md")


def parse_learning_status(project_root: Path) -> str:
    content = read_text_optional(project_root / "learning-record.md").strip()
    return "recorded" if content else "missing"


def build_governance_state(project_root: Path) -> dict[str, Any]:
    template = copy.deepcopy(load_yaml(TEMPLATE_PATH))
    project_state, project_state_path = load_project_state_optional(project_root)
    route_plan = load_yaml_optional(project_root / "route-plan.yaml")
    init_handoff = load_yaml_optional(project_root / "0-Init" / "init_handoff.yaml")
    task_id = first_non_empty(
        project_state.get("task_id"),
        route_plan.get("task_id"),
        project_root.name,
    )

    recommended_stage, recommended_path, rationale, alignment_repairs = infer_focus_path(
        project_state, route_plan, init_handoff
    )
    current_stage = first_non_empty(project_state.get("current_stage"), recommended_path, recommended_stage, "0-Init")
    active_path = first_non_empty(recommended_path, recommended_stage, current_stage)
    active_stage = stage_root_of(active_path)

    artifact_paths = {
        "team": project_root / "team.yaml",
        "project_state": project_state_path,
        "governance_state": project_root / "governance-state.yaml",
        "mandate": project_root / "mandate.yaml",
        "mission_brief": project_root / "mission-brief.yaml",
        "route_plan": project_root / "route-plan.yaml",
        "preflight_verdict": project_root / "preflight-verdict.yaml",
        "validation_report": project_root / "validation-report.md",
        "learning_record": project_root / "learning-record.md",
    }

    project_state_rel = Path(project_state_path.name)
    source_artifacts = [
        relative.as_posix()
        for relative in [
            Path("0-Init/north_star.yaml"),
            Path("0-Init/init_handoff.yaml"),
            project_state_rel,
            Path("route-plan.yaml"),
            Path("validation-report.md"),
            Path("learning-record.md"),
        ]
        if (project_root / relative).exists()
    ]

    required_repairs = [
        f"补齐 `{name}`。" for name, path in artifact_paths.items() if name != "governance_state" and not path.exists()
    ]
    if project_state_path.name == LEGACY_STATE_FILENAME:
        required_repairs.append(
            f"将 legacy `{LEGACY_STATE_FILENAME}` 迁移为 canonical `{CANONICAL_STATE_FILENAME}`。"
        )
    required_repairs.extend(alignment_repairs)

    blockers = [str(item) for item in project_state.get("open_unknowns") or []]

    template["project_name"] = str(project_state.get("project_name") or project_root.name)
    template["canonical_runtime"]["project_root"] = f"projects/aigc/{project_root.name}/"
    template["lifecycle"]["phase"] = infer_phase(project_root, project_state)
    template["lifecycle"]["status"] = first_non_empty(project_state.get("status"), "governance_state_backfilled")
    template["current_focus"]["active_skill"] = map_skill_from_path(active_path)
    template["current_focus"]["active_stage"] = active_path
    template["current_focus"]["active_scope"] = active_stage or "project"
    template["current_focus"]["active_step"] = first_non_empty(project_state.get("status"), "resume_ready")
    template["last_stable_checkpoint"]["checkpoint_id"] = f"CHK-{re.sub(r'[^A-Za-z0-9]+', '-', task_id).strip('-')}"
    template["last_stable_checkpoint"]["summary"] = first_non_empty(
        project_state.get("recommended_next_step"),
        f"最近稳定阶段：{current_stage}",
    )
    template["last_stable_checkpoint"]["source_artifacts"] = source_artifacts
    template["last_stable_checkpoint"]["verified_by"]["carrier"] = "validation-report.md"
    template["last_stable_checkpoint"]["verified_by"]["status"] = parse_validation_status(project_root)
    template["resume_contract"]["recommended_entry_skill"] = map_skill_from_path(active_path)
    template["resume_contract"]["recommended_entry_stage"] = active_stage or recommended_stage or current_stage
    template["resume_contract"]["recommended_entry_path"] = active_path
    template["resume_contract"]["rationale"] = rationale
    template["resume_contract"]["blockers"] = blockers
    template["resume_contract"]["required_repairs"] = required_repairs

    for name, path in artifact_paths.items():
        template["artifact_status"][name] = file_status(path)
    template["artifact_status"]["governance_state"] = "present"

    template["review_bridge"]["latest_preflight_status"] = parse_preflight_status(project_root)
    template["review_bridge"]["latest_acceptance_status"] = parse_validation_status(project_root)
    template["review_bridge"]["latest_learning_status"] = parse_learning_status(project_root)
    template["updated_at"] = datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")
    return template


def candidate_projects(selected_projects: list[str]) -> list[Path]:
    if selected_projects:
        return [PROJECTS_ROOT / project_name for project_name in selected_projects]
    candidates = {
        path.parent for path in PROJECTS_ROOT.glob(f"*/{CANONICAL_STATE_FILENAME}")
    }
    candidates.update(path.parent for path in PROJECTS_ROOT.glob(f"*/{LEGACY_STATE_FILENAME}"))
    return sorted(candidates)


def main() -> int:
    args = parse_args()
    if not TEMPLATE_PATH.exists():
        raise SystemExit(f"missing template: {TEMPLATE_PATH}")

    projects = candidate_projects(args.project)
    if not projects:
        print(f"No project with {CANONICAL_STATE_FILENAME} found (legacy {LEGACY_STATE_FILENAME} also absent).")
        return 0

    for project_root in projects:
        project_state_path = resolve_project_state_path(project_root)
        if project_state_path is None:
            print(
                f"SKIP {project_root}: missing {CANONICAL_STATE_FILENAME} "
                f"(legacy {LEGACY_STATE_FILENAME} also absent)"
            )
            continue

        target = project_root / "governance-state.yaml"
        if target.exists() and not args.force:
            print(f"SKIP {project_root.name}: governance-state.yaml already exists")
            continue

        data = build_governance_state(project_root)
        if args.write:
            target.write_text(
                yaml.safe_dump(data, allow_unicode=True, sort_keys=False),
                encoding="utf-8",
            )
            print(f"WROTE {target}")
        else:
            print(f"PREVIEW {project_root.name} -> {target}")
            print(yaml.safe_dump(data, allow_unicode=True, sort_keys=False))

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
