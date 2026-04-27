#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
网文项目初始化脚本

目标：
- 生成可运行的项目结构（推荐位于 `projects/story/<小说名>/`）
- 创建/更新项目根 `STATE.json`（运行时真相）
- 生成基础 stage 目录与兼容性规划模板文件（供 /story-plan 与 /story-write 使用）

说明：
- 该脚本是命令 /story-init 的“唯一允许的文件生成入口”（与命令文档保持一致）。
- 生成的内容以“模板骨架”为主，便于 AI/作者后续补全；但保证所有关键文件存在。
"""

from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime
from pathlib import Path
import yaml

from runtime_compat import enable_windows_utf8_stdio
from typing import Any, Dict, List
import re

# 安全修复：导入安全工具函数
from security_utils import atomic_write_json
from project_locator import write_current_project_pointer
from workflow_manager import build_initial_execution_state, build_initial_workflow_state


RUNTIME_STATE_REL = Path("STATE.json")
PROJECT_STATE_MANIFEST_REL = Path("STATE.json")
TEAM_MANIFEST_REL = Path("team.yaml")
PROJECT_MEMORY_REL = Path("MEMORY.md")
CHANGELOG_REL = Path("CHANGELOG.md")
INIT_STAGE_REL = Path("0-初始化")
SOURCE_ROOT_REL = Path("源")
SETTING_STAGE_REL = Path("1-设定")
PLANNING_STAGE_REL = Path("2-卷章")
DRAFT_STAGE_REL = Path("3-初稿")
POLISH_STAGE_REL = Path("4-润色")
REVIEW_STAGE_REL = Path("review")
CONTEXT_RETURN_STAGE_REL = Path("context-return")
PROJECT_MEMORY_TEMPLATE = Path(__file__).resolve().parents[1] / "0-初始化" / "templates" / "project-memory.template.md"
PLANNING_SKILL_PATHS = [
    ".agents/skills/story/0-初始化",
    ".agents/skills/story/1-设定",
    ".agents/skills/story/2-卷章",
]
PRODUCTION_SKILL_PATHS = [
    ".agents/skills/story/3-初稿",
    ".agents/skills/story/4-润色",
    ".agents/skills/story/context-return",
]
REVIEW_SKILL_PATHS = [
    ".agents/skills/story/review",
    ".agents/skills/story/review",
]
PROJECT_SKELETON_DIRS = [
    str(INIT_STAGE_REL),
    str(SETTING_STAGE_REL),
    str(PLANNING_STAGE_REL),
    str(DRAFT_STAGE_REL),
    str(POLISH_STAGE_REL),
    str(REVIEW_STAGE_REL),
    str(CONTEXT_RETURN_STAGE_REL),
    "CONTEXT",
    str(SOURCE_ROOT_REL),
]
TEAM_ROLE_SPECS = {
    "planning": {
        "label": "策划",
        "skills": PLANNING_SKILL_PATHS,
    },
    "production": {
        "label": "监制",
        "skills": PRODUCTION_SKILL_PATHS,
    },
    "review": {
        "label": "评审",
        "skills": REVIEW_SKILL_PATHS,
    },
}


# Windows 编码兼容性修复
if sys.platform == "win32":
    enable_windows_utf8_stdio()


def _read_text_if_exists(path: Path) -> str:
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8")


def _write_text_if_missing(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists():
        return
    path.write_text(content, encoding="utf-8")


def _write_text(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def _cleanup_lock_file(path: Path) -> None:
    lock_path = path.with_suffix(path.suffix + ".lock")
    if lock_path.exists():
        lock_path.unlink()


def _write_yaml(path: Path, payload: Dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        yaml.safe_dump(payload, allow_unicode=True, sort_keys=False),
        encoding="utf-8",
    )


def _toml_quote(value: str) -> str:
    return json.dumps(value, ensure_ascii=False)


def _render_toml_array(values: List[str]) -> str:
    return "[" + ", ".join(_toml_quote(value) for value in values if value) + "]"


def _yaml_quote(value: str) -> str:
    return json.dumps(value, ensure_ascii=False)


def _yaml_inline_list(values: List[str]) -> str:
    return "[" + ", ".join(_yaml_quote(value) for value in values if value) + "]"


def _yaml_bool(value: bool) -> str:
    return "true" if value else "false"


def _normalize_team_setup(
    *,
    advisor_agents: str = "",
    shared_council_agents: str = "",
    planning_agents: str = "",
    production_agents: str = "",
    review_agents: str = "",
) -> Dict[str, Any]:
    legacy_advisor_agents = _split_list_values(advisor_agents)
    shared_agents = _split_list_values(shared_council_agents)
    planning_members = _split_list_values(planning_agents)
    production_members = _split_list_values(production_agents)
    review_members = _split_list_values(review_agents)

    team_lineup_mode = "auto"
    team_mode = "unspecified"
    if shared_agents:
        team_lineup_mode = "custom"
        team_mode = "same_lineup"
        planning_members = list(shared_agents)
        production_members = list(shared_agents)
        review_members = list(shared_agents)
    elif any((planning_members, production_members, review_members)):
        team_lineup_mode = "custom"
        team_mode = "per_stage"
    elif legacy_advisor_agents:
        team_lineup_mode = "custom"
        team_mode = "legacy_planning_only"
        planning_members = list(legacy_advisor_agents)
    else:
        team_mode = "auto"

    role_members = {
        "planning": planning_members,
        "production": production_members,
        "review": review_members,
    }

    team_roles: Dict[str, Dict[str, Any]] = {}
    for role_key, spec in TEAM_ROLE_SPECS.items():
        members = _unique_preserve_order(role_members[role_key])
        team_roles[role_key] = {
            "label": spec["label"],
            "enabled": True if members else "",
            "members": members,
            "governs": list(spec["skills"]) if members else [],
            "source_skill_refs": list(spec["skills"]),
        }

    return {
        "init_mode": "team_roleplay",
        "selector_scope_root": ".agents/skills/team/",
        "team_lineup_mode": team_lineup_mode,
        "team_mode": team_mode,
        "shared_agents": _unique_preserve_order(shared_agents),
        "legacy_advisor_agents": _unique_preserve_order(legacy_advisor_agents),
        "required_departments": ["小说组", "导演组", "评审组"],
        "optional_departments_considered": [],
        "department_lineup_notes": [],
        "role_allocation_mode": "overlap_allowed",
        "role_overlap_notes": [],
        "recommendation_todo_paths": [],
        "planning_agents": team_roles["planning"]["members"],
        "production_agents": team_roles["production"]["members"],
        "review_agents": team_roles["review"]["members"],
        "roles": team_roles,
    }


def _council_mode_display(team_mode: str) -> str:
    mapping = {
        "auto": "自动组队",
        "same_lineup": "同一套班底，三阶段通用",
        "per_stage": "三阶段分别指定",
        "legacy_planning_only": "兼容旧字段（仅策划阶段）",
        "unspecified": "无",
    }
    return mapping.get(team_mode, "无")


def _format_team_members(team_setup: Dict[str, Any], role_key: str) -> str:
    role = team_setup.get("roles", {}).get(role_key, {})
    members = role.get("members", [])
    return ", ".join(members) if members else "无"


def _split_genre_keys(genre: str) -> list[str]:
    raw = (genre or "").strip()
    if not raw:
        return []
    # 支持复合题材：A+B / A+B / A、B / A与B
    raw = re.sub(r"[＋/、]", "+", raw)
    raw = raw.replace("与", "+")
    parts = [p.strip() for p in raw.split("+") if p.strip()]
    return parts or [raw]


def _normalize_genre_key(key: str) -> str:
    aliases = {
        "修仙/玄幻": "修仙",
        "玄幻修仙": "修仙",
        "玄幻": "修仙",
        "修真": "修仙",
        "都市修真": "都市异能",
        "都市高武": "高武",
        "都市奇闻": "都市脑洞",
        "古言脑洞": "古言",
        "游戏电竞": "电竞",
        "电竞文": "电竞",
        "直播": "直播文",
        "直播带货": "直播文",
        "主播": "直播文",
        "克系": "克苏鲁",
        "克系悬疑": "克苏鲁",
    }
    return aliases.get(key, key)


def _apply_label_replacements(text: str, replacements: Dict[str, str]) -> str:
    if not text or not replacements:
        return text
    lines = text.splitlines()
    for i, line in enumerate(lines):
        stripped = line.lstrip()
        for label, value in replacements.items():
            if not value:
                continue
            prefix = f"- {label}："
            if stripped.startswith(prefix):
                leading = line[: len(line) - len(stripped)]
                lines[i] = f"{leading}{prefix}{value}"
    return "\n".join(lines)


def _parse_tier_map(raw: str) -> Dict[str, str]:
    result: Dict[str, str] = {}
    if not raw:
        return result
    for part in raw.split(";"):
        part = part.strip()
        if not part:
            continue
        if ":" in part:
            key, val = part.split(":", 1)
            result[key.strip()] = val.strip()
    return result


def _render_team_rows(names: List[str], roles: List[str]) -> List[str]:
    rows = []
    for idx, name in enumerate(names):
        role = roles[idx] if idx < len(roles) else ""
        rows.append(f"| {name} | {role or '主线/副线'} | | | |")
    return rows


def _split_list_values(raw: str) -> List[str]:
    if not raw:
        return []
    return [item.strip() for item in re.split(r"[，,、;；]", raw) if item.strip()]


def _unique_preserve_order(values: List[str]) -> List[str]:
    return list(dict.fromkeys(value for value in values if value))


def _normalize_field_paths(raw: str) -> List[str]:
    if not raw:
        return []
    return _unique_preserve_order(
        [item.strip() for item in re.split(r"[，,、;；]", raw) if item.strip()]
    )


def _sanitize_project_leaf(name: str) -> str:
    raw = (name or "").strip().replace(" ", "-")
    raw = re.sub(r'[<>:"/\\|?*]+', "-", raw)
    raw = re.sub(r"[^\w\u4e00-\u9fff-]+", "-", raw)
    raw = re.sub(r"-+", "-", raw).strip("-_.")
    if not raw:
        raw = "proj-project"
    if raw.startswith("."):
        raw = f"proj-{raw.lstrip('.')}"
    return raw[:120]


def _resolve_project_path(project_dir: str, title: str) -> Path:
    requested = Path(project_dir).expanduser()
    requested_leaf = requested.name
    normalized = requested
    if not requested_leaf or requested_leaf.startswith(".") or requested_leaf != _sanitize_project_leaf(requested_leaf):
        normalized = requested.parent / _sanitize_project_leaf(title or requested_leaf or "project")

    project_path = normalized.resolve()
    skill_root = Path(__file__).resolve().parent.parent
    if ".claude" in project_path.parts:
        raise SystemExit("Refusing to initialize a project inside .claude. Choose a different directory.")
    if project_path == skill_root or skill_root in project_path.parents:
        raise SystemExit(f"Refusing to initialize a project inside story2026 skill package: {skill_root}")
    return project_path


def _compact_values(*values: Any) -> List[Any]:
    return [value for value in values if value not in ("", [], {}, None)]


def _normalize_init_mode(raw: str) -> str:
    value = (raw or "").strip().lower()
    if not value:
        return "team代入模式"
    mapping = {
        "team代入模式": "team代入模式",
        "team-roleplay": "team代入模式",
        "team_roleplay": "team代入模式",
        "team": "team代入模式",
        "智能顾问团模式": "team代入模式",
        "顾问团模式": "team代入模式",
        "顾问团": "team代入模式",
        "advisor": "team代入模式",
        "advisory": "team代入模式",
        "council": "team代入模式",
        "快速模式": "team代入模式",
        "快速": "team代入模式",
        "quick": "team代入模式",
        "fast": "team代入模式",
        "自主模式": "team代入模式",
        "自主": "team代入模式",
        "autonomous": "team代入模式",
        "interactive": "team代入模式",
        "deep": "team代入模式",
        "深度模式": "team代入模式",
    }
    return mapping.get(raw.strip(), mapping.get(value, "team代入模式"))


def _normalize_mode_source(raw: str, normalized_mode: str) -> str:
    value = (raw or "").strip().lower()
    mapping = {
        "user_selected": "user_selected",
        "defaulted": "defaulted",
        "inferred": "inferred",
        "switched_midway": "switched_midway",
    }
    if value in mapping:
        return mapping[value]
    return "defaulted"


def _normalize_decision_owner(raw: str, normalized_mode: str) -> str:
    value = (raw or "").strip().lower()
    if value in {"assistant", "user"}:
        return value
    return "user"


def _ensure_state_schema(state: Dict[str, Any]) -> Dict[str, Any]:
    """确保 STATE.json 具备 v5.1 架构所需的字段集合（v5.4 沿用）。

    v5.1 变更:
    - entities_v3 和 alias_index 已迁移到 index.db，不再存储在 STATE.json
    - structured_relationships 已迁移到 index.db relationships 表
    - STATE.json 保持精简 (< 5KB)
    """
    state.setdefault("project_info", {})
    state.setdefault("progress", {})
    state.setdefault("protagonist_state", {})
    state.setdefault("relationships", {})  # update_state.py 需要此字段
    state.setdefault("disambiguation_warnings", [])
    state.setdefault("disambiguation_pending", [])
    state.setdefault("world_settings", {"power_system": [], "factions": [], "locations": []})
    state.setdefault("plot_threads", {"active_threads": [], "foreshadowing": []})
    state.setdefault("review_checkpoints", [])
    state.setdefault("chapter_meta", {})
    state.setdefault("carryover_context", {})
    state.setdefault("planning_projection", {})
    state.setdefault("query_projection", {})
    state.setdefault("runtime_markers", {})
    state.setdefault("setting_route_packet", {"writer_context_projection": {"memory_projection": {}}})
    state.setdefault(
        "strand_tracker",
        {
            "last_quest_chapter": 0,
            "last_fire_chapter": 0,
            "last_constellation_chapter": 0,
            "current_dominant": "quest",
            "chapters_since_switch": 0,
            "history": [],
        },
    )
    # v5.1: entities_v3, alias_index, structured_relationships 已迁移到 index.db
    # 不再在 STATE.json 中初始化这些字段

    # progress schema evolution
    state["progress"].setdefault("current_chapter", 0)
    state["progress"].setdefault("total_words", 0)
    state["progress"].setdefault("last_updated", datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    state["progress"].setdefault("volumes_completed", [])
    state["progress"].setdefault("current_volume", 1)
    state["progress"].setdefault("volumes_planned", [])

    # protagonist schema evolution
    ps = state["protagonist_state"]
    ps.setdefault("name", "")
    ps.setdefault("power", {"realm": "", "layer": 1, "bottleneck": ""})
    ps.setdefault("location", {"current": "", "last_chapter": 0})
    ps.setdefault("golden_finger", {"name": "", "level": 1, "cooldown": 0, "skills": []})
    ps.setdefault("attributes", {})

    return state


def _ensure_workflow_state_schema(state: Dict[str, Any]) -> Dict[str, Any]:
    if not isinstance(state, dict):
        state = {}
    base = build_initial_workflow_state()
    for key, value in base.items():
        state.setdefault(key, json.loads(json.dumps(value)) if isinstance(value, (list, dict)) else value)
    state["updated_at"] = datetime.now().isoformat()
    return state


def _ensure_execution_state_schema(state: Dict[str, Any]) -> Dict[str, Any]:
    if not isinstance(state, dict):
        state = {}
    base = build_initial_execution_state()
    stage_progress = state.get("stage_progress")
    if not isinstance(stage_progress, dict):
        stage_progress = {}
    defaults = base.get("stage_progress", {})
    for stage_id, default_snapshot in defaults.items():
        snapshot = stage_progress.get(stage_id)
        if not isinstance(snapshot, dict):
            snapshot = {}
        for key, value in default_snapshot.items():
            snapshot.setdefault(key, value)
        stage_progress[stage_id] = snapshot
    state["stage_progress"] = stage_progress
    for key, value in base.items():
        if key == "stage_progress":
            continue
        state.setdefault(key, json.loads(json.dumps(value)) if isinstance(value, (list, dict)) else value)
    state["updated_at"] = datetime.now().isoformat()
    return state


def _sync_init_stage_progress(execution_state: Dict[str, Any], *, completed_at: str) -> None:
    stage_progress = execution_state.setdefault("stage_progress", {})
    if not isinstance(stage_progress, dict):
        stage_progress = {}
        execution_state["stage_progress"] = stage_progress

    snapshot = stage_progress.setdefault(
        "0-init",
        {
            "stage_label": "初始化",
            "status": "idle",
            "latest_run_id": None,
            "latest_command": None,
            "latest_governance_refs": None,
            "current_step": None,
            "resume_ready": False,
            "last_started_at": None,
            "last_completed_at": None,
            "last_failed_at": None,
            "last_cleared_at": None,
        },
    )
    snapshot["stage_label"] = "初始化"
    snapshot["status"] = "completed"
    snapshot["latest_command"] = "story-init"
    snapshot["current_step"] = None
    snapshot["resume_ready"] = False
    snapshot["last_completed_at"] = completed_at


def _append_task_log_if_missing(log_path: Path, row: Dict[str, Any]) -> None:
    log_path.parent.mkdir(parents=True, exist_ok=True)
    if log_path.exists() and log_path.stat().st_size > 0:
        return
    with open(log_path, "a", encoding="utf-8") as f:
        f.write(json.dumps(row, ensure_ascii=False) + "\n")


def _build_master_outline(target_chapters: int, *, chapters_per_volume: int = 50) -> str:
    volumes = (target_chapters - 1) // chapters_per_volume + 1 if target_chapters > 0 else 1
    lines: list[str] = [
        "# 总纲",
        "",
        "> 本文件为 legacy 兼容骨架；正式规划真源应由 /story-plan 收敛到 2-卷章/整体规划.md，并继续展开到 第N卷/卷规划.md 与 第N卷/第N章.md。",
        "",
        "## 卷结构",
        "",
    ]

    for v in range(1, volumes + 1):
        start = (v - 1) * chapters_per_volume + 1
        end = min(v * chapters_per_volume, target_chapters)
        lines.extend(
            [
                f"### 第{v}卷（第{start}-{end}章）",
                "- 核心冲突：",
                "- 关键爽点：",
                "- 卷末高潮：",
                "- 主要登场角色：",
                "- 关键伏笔（埋/收）：",
                "",
            ]
        )

    return "\n".join(lines).rstrip() + "\n"


def _inject_volume_rows(template_text: str, target_chapters: int, *, chapters_per_volume: int = 50) -> str:
    """在总纲模板的卷表中注入卷行（若存在表头）。"""
    lines = template_text.splitlines()
    header_idx = None
    for i, line in enumerate(lines):
        if line.strip().startswith("| 卷号"):
            header_idx = i
            break
    if header_idx is None:
        return template_text

    insert_idx = header_idx + 2 if header_idx + 1 < len(lines) else len(lines)
    volumes = (target_chapters - 1) // chapters_per_volume + 1 if target_chapters > 0 else 1
    rows = []
    for v in range(1, volumes + 1):
        start = (v - 1) * chapters_per_volume + 1
        end = min(v * chapters_per_volume, target_chapters)
        rows.append(f"| {v} | | 第{start}-{end}章 | | |")

    # 避免重复插入（若模板已有数据行）
    existing = {line.strip() for line in lines}
    rows = [r for r in rows if r.strip() not in existing]
    return "\n".join(lines[:insert_idx] + rows + lines[insert_idx:])


def _prepend_init_seed_notice(content: str) -> str:
    notice = "\n".join(
        [
            "> 说明：本文件是 `0-初始化` 阶段生成的 seed / legacy-compat 材料，不是项目 canonical 真源。",
            "> 正式真源统一以 `1-设定/**/*.json` 为准；后续阶段禁止继续人工维护本文件，除非做一次性迁移。",
            "",
        ]
    )
    if content.startswith("> 说明：本文件是 `0-初始化` 阶段生成的 seed / legacy-compat 材料"):
        return content
    return notice + content.lstrip()


def _join_list_for_display(values: List[str], empty: str = "（待补充）") -> str:
    cleaned = [str(value).strip() for value in values if str(value).strip()]
    return "、".join(cleaned) if cleaned else empty


def _inject_legacy_outline_contract_snapshot(content: str, payload: Dict[str, Any]) -> str:
    if "## 初始化合同快照" in content:
        return content

    project_contract = payload["project_contract"]
    cards_seed = payload["cards_seed"]
    planning_seed = payload["planning_seed"]
    unknowns = payload["unknowns"]
    protagonist = payload["protagonist"]
    golden_finger = payload["golden_finger"]
    relationship = payload["relationship"]

    creative = project_contract["creative_mandate"]
    promise = project_contract["promise_surface"]
    world_seed = cards_seed["global_seed"]
    story_engine = planning_seed["story_engine"]

    genre_parts = _split_genre_keys(creative["genre"])
    genre_display = " / ".join(genre_parts) if genre_parts else "（待补充）"
    reader_platform_display = " / ".join(
        part for part in [creative["target_reader"], creative["platform"]] if part
    ) or "（待补充）"
    world_anchor = "；".join(
        part for part in [world_seed["world_scale"], world_seed["factions"], world_seed["power_system_type"]] if part
    ) or "（待补充）"
    golden_finger_display = " / ".join(
        part
        for part in [
            golden_finger["name"] or golden_finger["type"],
            golden_finger["irreversible_cost"],
            golden_finger["growth_rhythm"],
        ]
        if part
    ) or "（待补充）"

    contract_snapshot = "\n".join(
        [
            "## 初始化合同快照",
            f"- 题材 / 平台：{genre_display} / {reader_platform_display}",
            f"- 一句话故事：{creative['one_liner'] or '（待补充）'}",
            f"- 核心冲突：{creative['core_conflict'] or '（待补充）'}",
            f"- 核心卖点：{_join_list_for_display(promise['core_selling_points'])}",
            f"- 反套路规则：{promise['anti_trope'] or '（待补充）'}",
            f"- 硬约束：{_join_list_for_display(promise['hard_constraints'])}",
            f"- 开篇钩子：{promise['opening_hook'] or '（待补充）'}",
            f"- 主角锚点：{protagonist['name'] or '（待补充）'} / 欲望：{protagonist['desire'] or '（待补充）'} / 缺陷：{protagonist['flaw'] or '（待补充）'}",
            f"- 世界锚点：{world_anchor}",
            f"- 金手指锚点：{golden_finger_display}",
            f"- Unknowns：{_join_list_for_display(unknowns['unresolved_questions'], '无')}",
            "",
        ]
    )

    content = content.replace(
        "{一句话概括主线矛盾与成长方向}",
        creative["one_liner"] or "{一句话概括主线矛盾与成长方向}",
    )
    content = _apply_label_replacements(
        content,
        {
            "反套路规则": promise["anti_trope"],
            "硬约束（世界/能力/行为）": _join_list_for_display(promise["hard_constraints"]),
            "主角缺陷": protagonist["flaw"],
            "反派镜像": story_engine["antagonist_mirror"],
            "主线目标": protagonist["desire"] or creative["one_liner"],
            "主要阻力": creative["core_conflict"],
            "世界观要点": "；".join(part for part in [world_seed["world_scale"], world_seed["factions"]] if part),
            "力量体系要点": "；".join(
                part for part in [world_seed["power_system_type"], world_seed["cultivation_chain"]] if part
            ),
            "起点状态": protagonist["name"],
            "（多主角）分工与冲突": _join_list_for_display(relationship["co_protagonist_roles"], "（按需要补充）"),
        },
    )

    lines = content.splitlines()
    insert_at = 0
    if lines and lines[0].strip() == "# 总纲":
        insert_at = 1
        while insert_at < len(lines) and (
            not lines[insert_at].strip() or lines[insert_at].lstrip().startswith(">")
        ):
            insert_at += 1

    merged = lines[:insert_at] + [""] + contract_snapshot.splitlines() + lines[insert_at:]
    return "\n".join(merged).rstrip() + "\n"


def _build_north_star_contract(payload: Dict[str, Any]) -> Dict[str, Any]:
    project_contract = payload["project_contract"]
    creative = project_contract["creative_mandate"]
    promise = project_contract["promise_surface"]
    protagonist = payload["protagonist"]
    relationship = payload["relationship"]
    golden_finger = payload["golden_finger"]
    story_engine = payload["planning_seed"]["story_engine"]
    world_seed = payload["cards_seed"]["global_seed"]
    north_star_inputs = payload.get("north_star_inputs", {})
    macro_factions = _split_list_values(world_seed.get("factions", ""))
    rule_system = [
        {"label": "力量体系", "value": world_seed["power_system_type"]},
        {"label": "资源分布", "value": world_seed["resource_distribution"]},
        {"label": "货币体系", "value": world_seed["currency_system"]},
        {"label": "货币兑换", "value": world_seed["currency_exchange"]},
        {"label": "门派层级", "value": world_seed["sect_hierarchy"]},
        {"label": "修炼链路", "value": world_seed["cultivation_chain"]},
        {"label": "修炼子层级", "value": world_seed["cultivation_subtiers"]},
    ]
    global_contract = {
        "worldview": {
            "world_scale": world_seed["world_scale"],
            "genre": creative["genre"],
            "target_reader": creative["target_reader"],
            "platform": creative["platform"],
            "summary": creative["one_liner"],
        },
        "rule_system": [item for item in rule_system if item["value"]],
        "era_constraints": {
            "era_anchor": world_seed["world_scale"],
            "worldline_mode": north_star_inputs.get("worldline_mode", ""),
            "hard_boundaries": north_star_inputs.get("must_not_do", []),
        },
        "culture_and_arts": {
            "culture": _compact_values(world_seed["social_class"], world_seed["factions"]),
            "arts": _compact_values(
                north_star_inputs.get("tone", ""),
                north_star_inputs.get("violence_texture", ""),
            ),
        },
        "faction_topology": {
            "tiers": macro_factions,
            "rule_holders": _compact_values(world_seed["factions"]),
            "resource_controllers": _compact_values(world_seed["resource_distribution"]),
            "relation_patterns": _compact_values(relationship["antagonist_mirror"]),
            "protagonist_entry_path": protagonist["desire"],
            "escalation_logic": _compact_values(creative["core_conflict"]),
        },
        "power_or_technology": {
            "system_type": _compact_values(world_seed["power_system_type"]),
            "tech_or_martial": _compact_values(
                world_seed["power_system_type"],
                world_seed["cultivation_chain"],
                world_seed["sect_hierarchy"],
            ),
            "resources": _compact_values(world_seed["resource_distribution"], world_seed["currency_system"]),
        },
        "golden_finger": {
            "name": golden_finger["name"],
            "type": golden_finger["type"],
            "style": golden_finger["style"],
            "visibility": golden_finger["visibility"],
            "core_function": golden_finger["name"],
            "trigger_conditions": [],
            "costs": _compact_values(golden_finger["irreversible_cost"]),
            "limits": promise["hard_constraints"],
            "counterplay": [],
            "growth_path": _compact_values(golden_finger["growth_rhythm"]),
        },
        "relationship_overview": {
            "macro_factions": macro_factions,
            "power_tensions": _compact_values(relationship["antagonist_mirror"]),
            "macro_conflicts": _compact_values(creative["core_conflict"]),
            "downstream_hooks": _compact_values(
                relationship["antagonist_level"],
                protagonist["structure"],
            ),
        },
        "current_focus": {
            "enforcement_focus": promise["hard_constraints"],
            "confirmed_facts": _compact_values(
                creative["genre"],
                creative["target_reader"],
                creative["platform"],
                world_seed["world_scale"],
                world_seed["power_system_type"],
            ),
            "invariant_defaults": north_star_inputs.get("must_keep", []) + north_star_inputs.get("must_not_do", []),
            "long_term_open_questions": payload["unknowns"]["deferred_to_cards"],
        },
    }
    style_contract = {
        "style_identity": {
            "one_line_definition": north_star_inputs.get("tone", "") or creative["genre"],
            "overall_tone": {
                "base_tone": north_star_inputs.get("tone", ""),
                "emotional_temperature": "",
                "dark_bright_balance": "",
                "tragic_comic_ratio": "",
                "gravity_level": "",
            },
        },
        "experience_contract": {
            "core_pleasures": promise["core_selling_points"],
            "expected_aftertaste": [],
            "anti_trope": _compact_values(promise["anti_trope"]),
            "no_fly_zones": north_star_inputs.get("no_fly_zones", []),
        },
        "narrative_style": {
            "pov_mode": "",
            "narrator_distance": "",
            "chronology_mode": "",
            "information_release_style": "",
            "suspense_method": "",
            "chapter_hook_style": promise["opening_hook"],
            "chapter_end_style": "",
            "pacing_profile": "",
        },
        "dialogue_style": {
            "dialogue_density": "",
            "speech_rhythm": "",
            "subtext_level": "",
            "wit_sharpness": "",
            "register_policy": "",
            "character_voice_separation": [],
            "inner_monologue_ratio": "",
            "forbidden_dialogue_patterns": [],
        },
        "visual_style": {
            "image_texture": north_star_inputs.get("violence_texture", ""),
            "color_palette": [],
            "light_shadow_tendency": "",
            "motion_texture": "",
            "spatial_feeling": "",
            "violence_imagery": north_star_inputs.get("violence_texture", ""),
            "romance_imagery": relationship["heroine_config"],
            "landmark_images": [],
        },
        "prose_style": {
            "sentence_length_tendency": "",
            "paragraph_rhythm": "",
            "diction_register": "",
            "metaphor_density": "",
            "sensory_bias": [],
            "description_density": "",
            "exposition_policy": "",
        },
        "scene_style": {
            "action_rendering": "",
            "emotion_rendering": "",
            "atmosphere_rendering": "",
            "transition_style": "",
            "set_piece_policy": "",
        },
        "style_gate": {
            "must_keep": north_star_inputs.get("must_keep", []),
            "must_avoid": north_star_inputs.get("must_not_do", []) + north_star_inputs.get("no_fly_zones", []),
            "drift_signals": [],
            "repair_actions": [],
        },
    }
    genre_contract = {
        "story_promise": {
            "reader_promise": promise["core_selling_points"],
            "platform_fit": _compact_values(creative["platform"], creative["target_reader"]),
            "forbidden_zone": north_star_inputs.get("no_fly_zones", []),
            "promise_matrix": {
                "primary_genre": creative["genre"],
                "secondary_genres": [],
            },
        },
        "genre_corridor": {
            "allowed_modes": _compact_values(creative["genre"], north_star_inputs.get("tone", "")),
            "tone_band": north_star_inputs.get("tone", ""),
            "narrative_density": north_star_inputs.get("mystery_density", ""),
        },
        "forbidden_zone": north_star_inputs.get("no_fly_zones", []),
        "navigation_rules": promise["hard_constraints"],
        "anti_cliche_bans": _compact_values(promise["anti_trope"]),
        "drift_corrections": [],
        "planning_projection": {
            "story_promise": "north_star.genre_contract.story_promise",
            "genre_corridor": "north_star.genre_contract.genre_corridor",
            "navigation_rules": "north_star.genre_contract.navigation_rules",
        },
    }
    cards_projection = {
        "scope": "full-series",
        "character_seed": payload["cards_seed"]["character_seed"],
        "scene_seed": {
            "world_scale": world_seed["world_scale"],
            "factions": macro_factions,
            "rule_pressure": promise["hard_constraints"],
        },
        "item_seed": payload["cards_seed"]["item_seed"],
        "legacy_projection": {
            "world_system": global_contract,
            "style_system": style_contract,
            "genre_system": genre_contract,
        },
    }

    return {
        "schema_version": "story2026/north-star/v1",
        "meta": {
            "source_stage": "0-初始化",
            "generated_at": payload["meta"]["generated_at"],
            "role": "primary-init-artifact",
            "scope": "full-series",
            "canonical_consumers": ["1-设定", "2-卷章"],
            "north_star_role": "global-style-genre-truth",
            "cards_role": "character-scene-item-seed",
        },
        "project_identity": {
            "title": creative["title"],
            "genre": creative["genre"],
            "target_words": creative["target_words"],
            "target_chapters": creative["target_chapters"],
            "target_reader": creative["target_reader"],
            "platform": creative["platform"],
        },
        "story_kernel": {
            "premise": creative["one_liner"],
            "opening_hook": promise["opening_hook"],
            "protagonist_drive": protagonist["desire"],
            "core_conflict": creative["core_conflict"],
            "antagonist_pressure": relationship["antagonist_level"] or story_engine["antagonist_mirror"],
            "protagonist_wound": protagonist["flaw"],
            "value_collision": story_engine["antagonist_mirror"] or promise["anti_trope"],
            "cost_of_victory": promise["hard_constraints"],
            "why_this_story_now": north_star_inputs.get("story_kernel_why_now", ""),
            "ending_vector": north_star_inputs.get("story_kernel_ending_vector", ""),
        },
        "reader_promise": {
            "primary_pleasures": promise["core_selling_points"],
            "anti_trope": promise["anti_trope"],
            "hard_constraints": promise["hard_constraints"],
            "no_fly_zones": north_star_inputs.get("no_fly_zones", []),
        },
        "aesthetic_axes": {
            "tone": north_star_inputs.get("tone", ""),
            "violence_texture": north_star_inputs.get("violence_texture", ""),
            "mystery_density": north_star_inputs.get("mystery_density", ""),
            "romance_policy": relationship["heroine_config"],
        },
        "ip_boundary": {
            "worldline_mode": north_star_inputs.get("worldline_mode", ""),
            "old_character_policy": north_star_inputs.get("old_character_policy", ""),
            "must_keep": north_star_inputs.get("must_keep", []),
            "must_not_do": north_star_inputs.get("must_not_do", []),
        },
        "global_contract": global_contract,
        "style_contract": style_contract,
        "genre_contract": genre_contract,
        "cards": cards_projection,
        "decision_policy": project_contract["decision_policy"],
        "init_session": payload["init_session"],
        "cards_seed": payload["cards_seed"],
        "planning_seed": payload["planning_seed"],
        "unknowns": payload["unknowns"],
        "sources_breakdown": payload["sources_breakdown"],
    }


def _build_story_source_manifest(*, title: str, now_iso: str) -> Dict[str, Any]:
    return {
        "manifest_version": "story2026-story-source/v1",
        "source_root": "源/",
        "primary_story_source": {
            "status": "missing",
            "source_type": "",
            "path": "",
            "coverage_scope": f"{title} 当前初始化未绑定正式故事主源。",
            "preset_retention_mode": "standard",
            "detail_expansion_mode": "free_expansion",
            "locked_preset_axes": [],
            "preset_registry": [],
            "authoritative_for": ["1-设定", "2-卷章"],
            "notes": "后续若补入正文、提纲或设定源，应先登记到本文件，再进入 planning。",
        },
        "auxiliary_sources": [],
        "development_briefs": [],
        "readiness": {
            "can_enter_cards": True,
            "can_enter_planning": True,
            "planning_scope": "seed_first",
            "blocking_reason": "",
            "partial_limitations": [
                "当前 planning 只能基于 north star seed 与用户输入推进，不能声称具备完整剧情主源。",
            ],
            "allowed_next_entries_when_blocked": ["1-设定", "2-卷章"],
            "required_user_action": [
                "若有正式正文、章节大纲或设定文档，请补充到项目 `源/` 后再回刷初始化源。",
            ],
        },
        "missing_prompt": {
            "summary": "当前已足够进入 cards 与 seed-first planning，但故事主源仍为空。",
            "ask_user_to_provide": [
                "故事正文、章节大纲、世界观设定或其它正式故事源。",
            ],
        },
        "generated_at": now_iso,
    }


def _collect_nonempty_field_paths(payload: Dict[str, Any]) -> List[str]:
    ordered_paths: List[str] = []
    for section in ("project", "protagonist", "relationship", "golden_finger", "world", "constraints"):
        section_values = payload.get(section, {})
        if not isinstance(section_values, dict):
            continue
        for key, value in section_values.items():
            if value not in ("", [], {}, None):
                ordered_paths.append(f"{section}.{key}")
    return _unique_preserve_order(ordered_paths)


def _collect_nonempty_field_values(payload: Dict[str, Any]) -> Dict[str, Any]:
    values: Dict[str, Any] = {}
    for section in ("project", "protagonist", "relationship", "golden_finger", "world", "constraints"):
        section_values = payload.get(section, {})
        if not isinstance(section_values, dict):
            continue
        for key, value in section_values.items():
            if value not in ("", [], {}, None):
                values[f"{section}.{key}"] = value
    return values


def _build_sources_breakdown(
    payload: Dict[str, Any],
    *,
    normalized_mode: str,
    decision_owner: str,
    user_confirmed_fields: str,
    council_advised_fields: str,
    assistant_inferred_fields: str,
) -> Dict[str, List[str]]:
    all_fields = _collect_nonempty_field_paths(payload)
    default_bucket = "assistant_inferred" if decision_owner == "assistant" else "user_confirmed"
    breakdown = {
        "user_confirmed": [field for field in _normalize_field_paths(user_confirmed_fields) if field in all_fields],
        "council_advised": [field for field in _normalize_field_paths(council_advised_fields) if field in all_fields],
        "assistant_inferred": [
            field for field in _normalize_field_paths(assistant_inferred_fields) if field in all_fields
        ],
    }
    if not any(breakdown.values()):
        return {
            "user_confirmed": all_fields if default_bucket == "user_confirmed" else [],
            "council_advised": all_fields if default_bucket == "council_advised" else [],
            "assistant_inferred": all_fields if default_bucket == "assistant_inferred" else [],
        }

    assigned = set()
    for key in ("user_confirmed", "council_advised", "assistant_inferred"):
        unique_fields = []
        for field in breakdown[key]:
            if field not in assigned:
                unique_fields.append(field)
                assigned.add(field)
        breakdown[key] = unique_fields

    breakdown[default_bucket].extend(field for field in all_fields if field not in assigned)
    breakdown[default_bucket] = _unique_preserve_order(breakdown[default_bucket])
    return breakdown


def _group_confirmation_fields(payload: Dict[str, Any], field_paths: List[str]) -> Dict[str, Dict[str, Any]]:
    field_values = _collect_nonempty_field_values(payload)
    grouped: Dict[str, Dict[str, Any]] = {}
    for field_path in field_paths:
        section, _, key = field_path.partition(".")
        if not section or not key or field_path not in field_values:
            continue
        grouped.setdefault(section, {})[key] = field_values[field_path]
    return grouped


def _build_init_handoff_payload(
    *,
    init_mode: str,
    mode_source: str,
    decision_owner: str,
    advisor_agents: str,
    shared_council_agents: str,
    planning_agents: str,
    production_agents: str,
    review_agents: str,
    research_policy: str,
    user_confirmed_fields: str,
    council_advised_fields: str,
    assistant_inferred_fields: str,
    title: str,
    genre: str,
    protagonist_name: str,
    target_words: int,
    target_chapters: int,
    one_liner: str,
    core_conflict: str,
    golden_finger_name: str,
    golden_finger_type: str,
    golden_finger_style: str,
    golden_finger_growth_rhythm: str,
    core_selling_points: str,
    protagonist_structure: str,
    heroine_config: str,
    heroine_names: str,
    heroine_role: str,
    co_protagonists: str,
    co_protagonist_roles: str,
    antagonist_tiers: str,
    antagonist_mirror: str,
    world_scale: str,
    factions: str,
    power_system_type: str,
    social_class: str,
    resource_distribution: str,
    gf_visibility: str,
    gf_irreversible_cost: str,
    protagonist_desire: str,
    protagonist_flaw: str,
    protagonist_archetype: str,
    antagonist_level: str,
    target_reader: str,
    platform: str,
    anti_trope: str,
    hard_constraints: str,
    opening_hook: str,
    currency_system: str,
    currency_exchange: str,
    sect_hierarchy: str,
    cultivation_chain: str,
    cultivation_subtiers: str,
    story_kernel_why_now: str,
    story_kernel_ending_vector: str,
    tone: str,
    violence_texture: str,
    mystery_density: str,
    worldline_mode: str,
    old_character_policy: str,
    must_keep: str,
    must_not_do: str,
    no_fly_zones: str,
    now_iso: str,
) -> Dict[str, Any]:
    normalized_mode = _normalize_init_mode(init_mode)
    team_setup = _normalize_team_setup(
        advisor_agents=advisor_agents,
        shared_council_agents=shared_council_agents,
        planning_agents=planning_agents,
        production_agents=production_agents,
        review_agents=review_agents,
    )
    advisor_agent_list = team_setup["planning_agents"]
    normalized_research_policy = (research_policy or "").strip() or "none"
    normalized_mode_source = _normalize_mode_source(mode_source, normalized_mode)
    normalized_decision_owner = _normalize_decision_owner(decision_owner, normalized_mode)
    normalized_hard_constraints = _split_list_values(hard_constraints)

    legacy_project = {
        "title": title,
        "genre": genre,
        "target_words": int(target_words),
        "target_chapters": int(target_chapters),
        "one_liner": one_liner,
        "core_conflict": core_conflict,
        "target_reader": target_reader,
        "platform": platform,
    }
    legacy_protagonist = {
        "name": protagonist_name,
        "desire": protagonist_desire,
        "flaw": protagonist_flaw,
        "archetype": protagonist_archetype,
        "structure": protagonist_structure or "单主角",
    }
    legacy_relationship = {
        "heroine_config": heroine_config,
        "heroine_names": _split_list_values(heroine_names),
        "heroine_role": heroine_role,
        "co_protagonists": _split_list_values(co_protagonists),
        "co_protagonist_roles": _split_list_values(co_protagonist_roles),
        "antagonist_tiers": _parse_tier_map(antagonist_tiers),
        "antagonist_level": antagonist_level,
        "antagonist_mirror": antagonist_mirror,
    }
    legacy_golden_finger = {
        "type": golden_finger_type,
        "name": golden_finger_name,
        "style": golden_finger_style,
        "visibility": gf_visibility,
        "irreversible_cost": gf_irreversible_cost,
        "growth_rhythm": golden_finger_growth_rhythm,
    }
    legacy_world = {
        "scale": world_scale,
        "factions": factions,
        "power_system_type": power_system_type,
        "social_class": social_class,
        "resource_distribution": resource_distribution,
        "currency_system": currency_system,
        "currency_exchange": currency_exchange,
        "sect_hierarchy": sect_hierarchy,
        "cultivation_chain": cultivation_chain,
        "cultivation_subtiers": cultivation_subtiers,
    }
    legacy_constraints = {
        "anti_trope": anti_trope,
        "hard_constraints": normalized_hard_constraints,
        "core_selling_points": _split_list_values(core_selling_points),
        "opening_hook": opening_hook,
    }
    payload = {
        "schema_version": "story2026/init-handoff/v2",
        "meta": {
            "source_stage": "0-初始化",
            "generated_at": now_iso,
            "canonical_consumer": "1-设定",
            "canonical_truth": "0-初始化/north_star.yaml + 1-设定/**/*",
            "seed_policy": "新项目默认不生成额外 Init seed 文档；若历史项目存在旧 Init/*.md，仅视为 legacy-compat，不得持续维护",
            "contract_model": "project_contract + cards_seed + planning_seed + unknowns",
        },
        "init_session": {
            "mode": normalized_mode,
            "mode_source": normalized_mode_source,
            "advisor_agents": advisor_agent_list,
            "team_setup": team_setup,
            "research_policy": normalized_research_policy,
            "decision_owner": normalized_decision_owner,
        },
        "project_contract": {
            "creative_mandate": legacy_project,
            "decision_policy": {
                "init_mode": normalized_mode,
                "decision_owner": normalized_decision_owner,
                "research_policy": normalized_research_policy,
                "advisor_agents": advisor_agent_list,
                "team_setup": team_setup,
                "mode_source": normalized_mode_source,
            },
            "promise_surface": {
                "core_selling_points": legacy_constraints["core_selling_points"],
                "anti_trope": anti_trope,
                "hard_constraints": normalized_hard_constraints,
                "opening_hook": opening_hook,
            },
        },
        "cards_seed": {
            "global_seed": {
                "genre": genre,
                "target_reader": target_reader,
                "platform": platform,
                "world_scale": world_scale,
                "factions": factions,
                "power_system_type": power_system_type,
                "social_class": social_class,
                "resource_distribution": resource_distribution,
                "currency_system": currency_system,
                "currency_exchange": currency_exchange,
                "sect_hierarchy": sect_hierarchy,
                "cultivation_chain": cultivation_chain,
                "cultivation_subtiers": cultivation_subtiers,
            },
            "character_seed": {
                "protagonist": legacy_protagonist,
                "relationship": legacy_relationship,
            },
            "item_seed": {
                "golden_finger": legacy_golden_finger,
                "exclusive_item_hooks": {
                    "heroine_names": legacy_relationship["heroine_names"],
                    "co_protagonists": legacy_relationship["co_protagonists"],
                },
            },
        },
        "planning_seed": {
            "story_engine": {
                "one_liner": one_liner,
                "core_conflict": core_conflict,
                "protagonist_desire": protagonist_desire,
                "protagonist_flaw": protagonist_flaw,
                "antagonist_level": antagonist_level,
                "antagonist_mirror": antagonist_mirror,
                "golden_finger_cost": gf_irreversible_cost,
                "golden_finger_growth_rhythm": golden_finger_growth_rhythm,
                "opening_hook": opening_hook,
            },
            "pacing_scale": {
                "target_words": int(target_words),
                "target_chapters": int(target_chapters),
                "protagonist_structure": protagonist_structure or "单主角",
                "heroine_config": heroine_config,
            },
            "constraint_seed": {
                "anti_trope": anti_trope,
                "hard_constraints": normalized_hard_constraints,
                "core_selling_points": legacy_constraints["core_selling_points"],
            },
        },
        "unknowns": {
            "unresolved_questions": [],
            "deferred_to_cards": [],
            "deferred_to_planning": [],
        },
        "confirmation": {
            "user_confirmed": {},
            "assistant_inferred": {},
            "pending_questions": [],
        },
        "sources_breakdown": {
            "user_confirmed": [],
            "council_advised": [],
            "assistant_inferred": [],
        },
        "north_star_inputs": {
            "story_kernel_why_now": story_kernel_why_now,
            "story_kernel_ending_vector": story_kernel_ending_vector,
            "tone": tone,
            "violence_texture": violence_texture,
            "mystery_density": mystery_density,
            "worldline_mode": worldline_mode,
            "old_character_policy": old_character_policy,
            "must_keep": _split_list_values(must_keep),
            "must_not_do": _split_list_values(must_not_do),
            "no_fly_zones": _split_list_values(no_fly_zones),
        },
        # legacy mirror: 保留一层兼容字段，避免老合同与新 handoff 一次断裂
        "project": legacy_project,
        "protagonist": legacy_protagonist,
        "relationship": legacy_relationship,
        "golden_finger": legacy_golden_finger,
        "world": legacy_world,
        "constraints": legacy_constraints,
    }

    pending_checks = [
        ("project.one_liner", payload["project"]["one_liner"]),
        ("project.core_conflict", payload["project"]["core_conflict"]),
        ("constraints.anti_trope", payload["constraints"]["anti_trope"]),
        ("constraints.hard_constraints", payload["constraints"]["hard_constraints"]),
        ("constraints.opening_hook", payload["constraints"]["opening_hook"]),
        ("relationship.antagonist_mirror", payload["relationship"]["antagonist_mirror"]),
        ("golden_finger.growth_rhythm", payload["golden_finger"]["growth_rhythm"]),
    ]
    payload["confirmation"]["pending_questions"] = [field for field, value in pending_checks if not value]
    payload["unknowns"]["unresolved_questions"] = list(payload["confirmation"]["pending_questions"])
    payload["unknowns"]["deferred_to_cards"] = [
        field
        for field in payload["confirmation"]["pending_questions"]
        if field.startswith(("protagonist.", "relationship.", "world."))
    ]
    payload["unknowns"]["deferred_to_planning"] = [
        field
        for field in payload["confirmation"]["pending_questions"]
        if field.startswith(("project.", "constraints.", "golden_finger."))
    ]

    payload["sources_breakdown"] = _build_sources_breakdown(
        payload,
        normalized_mode=normalized_mode,
        decision_owner=normalized_decision_owner,
        user_confirmed_fields=user_confirmed_fields,
        council_advised_fields=council_advised_fields,
        assistant_inferred_fields=assistant_inferred_fields,
    )
    payload["confirmation"]["user_confirmed"] = _group_confirmation_fields(
        payload,
        payload["sources_breakdown"]["user_confirmed"],
    )
    payload["confirmation"]["assistant_inferred"] = _group_confirmation_fields(
        payload,
        payload["sources_breakdown"]["assistant_inferred"],
    )
    return payload


def _build_init_handoff_artifact(payload: Dict[str, Any]) -> Dict[str, Any]:
    init_session = payload["init_session"]
    return {
        "north_star_ref": "0-初始化/north_star.yaml",
        "story_source_manifest_ref": "0-初始化/story-source-manifest.yaml",
        "team_ref": "team.yaml",
        "project_contract": {
            "initialization_goal": "以 team 代入模式完成小说项目初始化，锁定北极星、故事源状态、团队编组与唯一下一入口。",
            "acceptance_hint": "优先进入 `1-设定` 建卡；若已有足够故事源，再进入 `2-卷章`。",
            "current_stage": "0-初始化",
            "recommended_next_stage": "1-设定",
            "creative_mandate": payload["project_contract"]["creative_mandate"],
            "promise_surface": payload["project_contract"]["promise_surface"],
            "decision_policy": payload["project_contract"]["decision_policy"],
        },
        "stage_entry_seeds": {
            "cards_seed": payload["cards_seed"],
            "planning_seed": payload["planning_seed"],
        },
        "unknowns": payload["unknowns"],
        "sources_breakdown": payload["sources_breakdown"],
        "risk_notes": [
            "当前未绑定正式故事主源，planning 只能按 seed-first 模式推进。",
            "初始化固定题包直答的结论已折叠进 seeds；后续若补入正式故事源，应先回刷 `0-初始化` 三文件。",
        ],
        "init_session": {
            "mode": init_session["mode"],
            "mode_source": init_session["mode_source"],
            "decision_owner": init_session["decision_owner"],
            "advisor_agents": init_session["advisor_agents"],
            "team_setup": init_session["team_setup"],
            "research_policy": init_session["research_policy"],
        },
    }


def _render_sources_breakdown_block(payload: Dict[str, Any]) -> List[str]:
    breakdown = payload.get("sources_breakdown", {})
    return [
        "## 字段来源",
        f"- 用户确认：{', '.join(breakdown.get('user_confirmed', [])) if breakdown.get('user_confirmed') else '无'}",
        f"- 顾问团建议：{', '.join(breakdown.get('council_advised', [])) if breakdown.get('council_advised') else '无'}",
        f"- 助手推断：{', '.join(breakdown.get('assistant_inferred', [])) if breakdown.get('assistant_inferred') else '无'}",
        "",
    ]


def _render_init_readme() -> str:
    return (
        "\n".join(
            [
                "# 0-初始化 目录说明",
                "",
                "- `north_star.yaml`：初始化主文件，承载故事核、读者承诺、审美轴、IP 边界与长期对象约束。",
                "- `story-source-manifest.yaml`：故事主源登记与 readiness 判定。",
                "- `init_handoff.yaml`：阶段入口种子、unknowns 与来源分层。",
                "- 项目根目录的 `STATE.json`：项目运行态、入口状态与 workflow runtime 的唯一状态文件。",
                "- 项目根目录的 `team.yaml`：团队治理真源，初始化写入 `策划 / 监制 / 评审` 三角色编组与 provenance。",
                "- 项目根目录的 `CHANGELOG.md`：项目级变更记录入口。",
                "- 新项目默认不再生成额外 `Init/*.md` seed 文档或并行 init companion 文件。",
                "- 原“全局卡 / 风格卡 / 类型卡”概念已废弃；长期总规范统一归入 `north_star.yaml` 的 `global_contract / style_contract / genre_contract`。",
                "- 一旦 `1-设定` 完成建卡，人物、场景、物品的正式真源统一以 `1-设定/**/*.json` 为准。",
                "",
            ]
        )
        + "\n"
    )


def _build_project_state_manifest(
    *,
    title: str,
    genre: str,
    now_iso: str,
    init_mode: str,
    mode_source: str,
    decision_owner: str,
    team_setup: Dict[str, Any],
    research_policy: str,
) -> Dict[str, Any]:
    return {
        "schema_version": "story2026/project-state-manifest/v1",
        "meta": {
            "generated_at": now_iso,
            "role": "project-entry-manifest",
            "status": "initialized",
        },
        "project": {
            "title": title,
            "genre": genre,
        },
        "init_session": {
            "mode": init_mode,
            "mode_source": mode_source,
            "decision_owner": decision_owner,
            "advisor_agents": team_setup["planning_agents"],
            "team_setup": team_setup,
            "research_policy": research_policy,
        },
        "paths": {
            "runtime_state": str(RUNTIME_STATE_REL),
            "north_star": "0-初始化/north_star.yaml",
            "story_source_manifest": "0-初始化/story-source-manifest.yaml",
            "init_handoff": "0-初始化/init_handoff.yaml",
            "team_manifest": str(TEAM_MANIFEST_REL),
            "changelog": str(CHANGELOG_REL),
        },
        "truth_layers": {
            "project_entry": str(PROJECT_STATE_MANIFEST_REL),
            "runtime_snapshot": str(RUNTIME_STATE_REL),
            "object_truth": "1-设定/**/*.json",
            "planning_truth": "2-卷章/整体规划.md",
        },
    }


def _render_team_manifest_toml(
    *,
    title: str,
    now_iso: str,
    team_setup: Dict[str, Any],
) -> str:
    lines = [
        "# story2026 团队治理模板",
        f'schema_version = "story2026/team/v1"',
        f"generated_at = {_toml_quote(now_iso)}",
        f"project_title = {_toml_quote(title)}",
        f'"布阵模式" = {_toml_quote(_council_mode_display(team_setup.get("team_mode", "unspecified")))}',
        "",
    ]
    for role_key in ("planning", "production", "review"):
        role = team_setup["roles"][role_key]
        lines.extend(
            [
                f'["{role["label"]}"]',
                f'"智能顾问团" = {"true" if role["enabled"] is True else _toml_quote("")}',
                f'"成员" = {_render_toml_array(role["members"])}',
                f'"管辖" = {_render_toml_array(role["governs"])}',
                "",
            ]
        )
    return "\n".join(lines)


def _render_team_manifest_yaml(
    *,
    title: str,
    now_iso: str,
    team_setup: Dict[str, Any],
    init_mode: str,
    mode_source: str,
    decision_owner: str,
    research_policy: str,
) -> str:
    team_lineup_mode = team_setup.get("team_lineup_mode", "auto")
    auto_notes = []
    custom_notes = []
    if team_lineup_mode == "auto":
        auto_notes = [
            "默认由 0-初始化 根据题材与故事核从 .agents/skills/team/ 里自动挑选代入顾问。",
            "当前脚本只负责写入初始化真源；实际自动选人与固定题包直答调度由 0-初始化 主技能执行。",
        ]
    else:
        custom_notes = [
            "当前 team.yaml 记录了用户或上游流程显式指定的顾问成员。",
            "若存在 legacy advisor_agents，它们只作为 planning 角色兼容镜像保留。",
        ]

    lines = [
        "# team.yaml",
        "#",
        "# 角色：",
        "# - story2026 项目级 team 代入真源",
        "# - 由 `0-初始化` 首次生成，供 `1-设定 / 2-卷章 / 3-初稿 / context-return / review` 消费",
        "# - 不替代各阶段 canonical，只提供治理角色、成员、初始化 provenance 与运行策略",
        "",
        f"enabled: {_yaml_bool(True)}",
        "",
        "init_contract:",
        f"  init_mode: {_yaml_quote('team_roleplay')}",
        f"  init_mode_display: {_yaml_quote(init_mode)}",
        f"  team_lineup_mode: {_yaml_quote(team_lineup_mode)}",
        f"  selector_scope_root: {_yaml_quote(team_setup.get('selector_scope_root', '.agents/skills/team/'))}",
        f"  lineup_source: {_yaml_quote('0-初始化')}",
        f"  mode_source: {_yaml_quote(mode_source)}",
        f"  locked_by: {_yaml_quote(decision_owner)}",
        f"  research_policy: {_yaml_quote(research_policy or 'none')}",
        f"  auto_selection_notes: {_yaml_inline_list(auto_notes)}",
        f"  custom_selection_notes: {_yaml_inline_list(custom_notes)}",
        f"  lineup_gap_todo_paths: {_yaml_inline_list(team_setup.get('recommendation_todo_paths', []))}",
        "",
        "team_setup:",
        f"  team_mode: {_yaml_quote(team_setup.get('team_mode', 'auto'))}",
        f"  shared_agents: {_yaml_inline_list(team_setup.get('shared_agents', []))}",
        f"  role_allocation_mode: {_yaml_quote(team_setup.get('role_allocation_mode', 'overlap_allowed'))}",
        f"  same_person_cross_role_allowed: {_yaml_bool(True)}",
        f"  required_departments: {_yaml_inline_list(team_setup.get('required_departments', []))}",
        f"  optional_departments_considered: {_yaml_inline_list(team_setup.get('optional_departments_considered', []))}",
        f"  department_lineup_notes: {_yaml_inline_list(team_setup.get('department_lineup_notes', []))}",
        f"  role_overlap_notes: {_yaml_inline_list(team_setup.get('role_overlap_notes', []))}",
        f"  recommendation_todo_paths: {_yaml_inline_list(team_setup.get('recommendation_todo_paths', []))}",
        "",
        "roles:",
    ]

    for role_key in ("planning", "production", "review"):
        role = team_setup["roles"][role_key]
        kickoff_owner = role_key == "planning"
        requires_subagents = role_key == "planning"
        lines.extend(
            [
                f"  {role_key}:",
                f"    label: {_yaml_quote(role['label'])}",
                f"    enabled: {_yaml_bool(bool(role['members']))}",
                f"    members: {_yaml_inline_list(role['members'])}",
                f"    governs: {_yaml_inline_list(role['governs'])}",
                "    init_execution:",
                f"      kickoff_owner: {_yaml_bool(kickoff_owner)}",
                f"      requires_subagents: {_yaml_bool(requires_subagents)}",
                f"      execution_mode: {_yaml_quote('direct-answer-packet' if kickoff_owner else 'on_demand')}",
                f"    source_skill_refs: {_yaml_inline_list(role.get('source_skill_refs', []))}",
            ]
        )

    lines.extend(
        [
            "",
            "runtime_policy:",
            f"  use_subagents_by_default: {_yaml_bool(True)}",
            f"  require_subagents_for_init_execution: {_yaml_bool(True)}",
            f"  init_execution_owner_role: {_yaml_quote('planning')}",
            f"  init_execution_subagents_policy: {_yaml_quote('required')}",
            f"  fallback_when_subagents_unavailable: {_yaml_quote('block_and_report_for_init_execution')}",
            f"  canonical_owner: {_yaml_quote('main_agent')}",
            "",
            "decision_policy:",
            f"  decision_owner: {_yaml_quote(decision_owner)}",
            f"  conflict_rule: {_yaml_quote('user_confirmed > review_gate > planning_direct_answer_consensus > role_consensus > main_agent_inferred')}",
            "",
            "meta:",
            f"  generated_at: {_yaml_quote(now_iso)}",
            f"  project_title: {_yaml_quote(title)}",
        ]
    )
    return "\n".join(lines) + "\n"


def _render_changelog(title: str, now: str) -> str:
    return (
        "\n".join(
            [
                "# Changelog",
                "",
                "All notable changes to this story project will be documented in this file.",
                "",
                "## [Unreleased]",
                "",
                f"## [{now}]",
                "### Added",
                f"- 初始化项目骨架：{title}",
                "- 建立 `STATE.json`、`team.yaml`、`MEMORY.md`、`CHANGELOG.md` 标准配置。",
                "- 创建项目级 `CONTEXT/` 目录，作为整个创作阶段共享附加上下文根。",
                "- 写入 `0-初始化/north_star.yaml`、`0-初始化/story-source-manifest.yaml`、`0-初始化/init_handoff.yaml` 初始化三件套。",
                "",
            ]
        )
        + "\n"
    )


def _render_project_memory(title: str, now: str) -> str:
    template = _read_text_if_exists(PROJECT_MEMORY_TEMPLATE)
    if not template:
        template = (
            "# MEMORY.md\n\n"
            "项目：__PROJECT_TITLE__\n"
            "初始化日期：__DATE__\n\n"
            "## 用途\n\n"
            "- 记录当前项目跨阶段持续生效的创作偏好、口味、习惯、特殊元素、禁区与长期要求。\n"
            "- 这里只保存“这个项目后续还要继续遵守”的记忆，不记录 skill 调试经验、脚本故障或跨项目 heuristic。\n\n"
            "## 已确认的长期偏好\n\n"
            "- 暂无\n"
        )
    return template.replace("__PROJECT_TITLE__", title).replace("__DATE__", now)


def init_project(
    project_dir: str,
    title: str,
    genre: str,
    *,
    init_mode: str = "team代入模式",
    mode_source: str = "",
    decision_owner: str = "",
    advisor_agents: str = "",
    shared_council_agents: str = "",
    planning_agents: str = "",
    production_agents: str = "",
    review_agents: str = "",
    research_policy: str = "",
    user_confirmed_fields: str = "",
    council_advised_fields: str = "",
    assistant_inferred_fields: str = "",
    protagonist_name: str = "",
    target_words: int = 2_000_000,
    target_chapters: int = 600,
    one_liner: str = "",
    core_conflict: str = "",
    golden_finger_name: str = "",
    golden_finger_type: str = "",
    golden_finger_style: str = "",
    golden_finger_growth_rhythm: str = "",
    core_selling_points: str = "",
    protagonist_structure: str = "",
    heroine_config: str = "",
    heroine_names: str = "",
    heroine_role: str = "",
    co_protagonists: str = "",
    co_protagonist_roles: str = "",
    antagonist_tiers: str = "",
    antagonist_mirror: str = "",
    world_scale: str = "",
    factions: str = "",
    power_system_type: str = "",
    social_class: str = "",
    resource_distribution: str = "",
    gf_visibility: str = "",
    gf_irreversible_cost: str = "",
    protagonist_desire: str = "",
    protagonist_flaw: str = "",
    protagonist_archetype: str = "",
    antagonist_level: str = "",
    target_reader: str = "",
    platform: str = "",
    anti_trope: str = "",
    hard_constraints: str = "",
    opening_hook: str = "",
    currency_system: str = "",
    currency_exchange: str = "",
    sect_hierarchy: str = "",
    cultivation_chain: str = "",
    cultivation_subtiers: str = "",
    story_kernel_why_now: str = "",
    story_kernel_ending_vector: str = "",
    tone: str = "",
    violence_texture: str = "",
    mystery_density: str = "",
    worldline_mode: str = "",
    old_character_policy: str = "",
    must_keep: str = "",
    must_not_do: str = "",
    no_fly_zones: str = "",
) -> None:
    project_path = _resolve_project_path(project_dir, title)
    project_path.mkdir(parents=True, exist_ok=True)

    # 目录结构：初始化即预建当前阶段树要求的 source/stage roots，避免下游仍按旧骨架猜目录。
    for dir_path in PROJECT_SKELETON_DIRS:
        (project_path / dir_path).mkdir(parents=True, exist_ok=True)

    # STATE.json（创建或增量补齐）
    state_path = project_path / RUNTIME_STATE_REL
    if state_path.exists():
        try:
            state: Dict[str, Any] = json.loads(state_path.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            state = {}
    else:
        state = {}

    state = _ensure_state_schema(state)
    normalized_init_mode = _normalize_init_mode(init_mode)
    team_setup = _normalize_team_setup(
        advisor_agents=advisor_agents,
        shared_council_agents=shared_council_agents,
        planning_agents=planning_agents,
        production_agents=production_agents,
        review_agents=review_agents,
    )
    advisor_agent_list = team_setup["planning_agents"]
    normalized_research_policy = (research_policy or "").strip() or "none"
    normalized_mode_source = _normalize_mode_source(mode_source, normalized_init_mode)
    normalized_decision_owner = _normalize_decision_owner(decision_owner, normalized_init_mode)
    created_at = state.get("project_info", {}).get("created_at") or datetime.now().strftime("%Y-%m-%d")

    state["project_info"].update(
        {
            "title": title,
            "genre": genre,
            "created_at": created_at,
            "target_words": int(target_words),
            "target_chapters": int(target_chapters),
            "init_mode": normalized_init_mode,
            "mode_source": normalized_mode_source,
            "decision_owner": normalized_decision_owner,
            "advisor_agents": advisor_agent_list,
            "shared_council_agents": team_setup["shared_agents"],
            "planning_council_agents": team_setup["planning_agents"],
            "production_council_agents": team_setup["production_agents"],
            "review_council_agents": team_setup["review_agents"],
            "council_team_mode": team_setup["team_mode"],
            "team_lineup_mode": team_setup["team_lineup_mode"],
            "selector_scope_root": team_setup["selector_scope_root"],
            "team_setup": team_setup,
            "research_policy": normalized_research_policy,
            "init_contract_model": "north_star+story_source_manifest+init_handoff",
            "primary_init_artifact": "0-初始化/north_star.yaml",
            "north_star_schema_version": "story2026/north-star/v1",
            "story_source_manifest_schema_version": "story2026-story-source/v1",
            "init_handoff_schema_version": "story2026/init-handoff/v2",
            "project_entry_state_file": str(PROJECT_STATE_MANIFEST_REL),
            "team_manifest_file": str(TEAM_MANIFEST_REL),
            "changelog_file": str(CHANGELOG_REL),
            "story_source_root": "源/",
            "project_context_root": "CONTEXT/",
            "setting_root": "1-设定/",
            "planning_root": "2-卷章/",
            "drafting_root": "3-初稿/",
            "polish_root": "4-润色/",
            "review_root": "review/",
            "context_return_root": "context-return/",
            "one_liner": one_liner,
            "core_conflict": core_conflict,
            "anti_trope": anti_trope,
            "hard_constraints": _split_list_values(hard_constraints),
            "opening_hook": opening_hook,
            # 下面字段属于“初始化元信息”，不影响运行时脚本
            "golden_finger_name": golden_finger_name,
            "golden_finger_type": golden_finger_type,
            "golden_finger_style": golden_finger_style,
            "golden_finger_growth_rhythm": golden_finger_growth_rhythm,
            "core_selling_points": core_selling_points,
            "protagonist_structure": protagonist_structure,
            "heroine_config": heroine_config,
            "heroine_names": heroine_names,
            "heroine_role": heroine_role,
            "co_protagonists": co_protagonists,
            "co_protagonist_roles": co_protagonist_roles,
            "antagonist_tiers": antagonist_tiers,
            "antagonist_mirror": antagonist_mirror,
            "world_scale": world_scale,
            "factions": factions,
            "power_system_type": power_system_type,
            "social_class": social_class,
            "resource_distribution": resource_distribution,
            "gf_visibility": gf_visibility,
            "gf_irreversible_cost": gf_irreversible_cost,
            "target_reader": target_reader,
            "platform": platform,
            "currency_system": currency_system,
            "currency_exchange": currency_exchange,
            "sect_hierarchy": sect_hierarchy,
            "cultivation_chain": cultivation_chain,
            "cultivation_subtiers": cultivation_subtiers,
            "story_kernel_why_now": story_kernel_why_now,
            "story_kernel_ending_vector": story_kernel_ending_vector,
            "tone": tone,
            "violence_texture": violence_texture,
            "mystery_density": mystery_density,
            "worldline_mode": worldline_mode,
            "old_character_policy": old_character_policy,
            "must_keep": _split_list_values(must_keep),
            "must_not_do": _split_list_values(must_not_do),
            "no_fly_zones": _split_list_values(no_fly_zones),
        }
    )
    state["project_name"] = title
    state["task_id"] = f"init-{_sanitize_project_leaf(title)}"
    state["project_root"] = str(project_path)
    state["current_stage"] = "0-初始化"
    state["status"] = "initialized"
    state["recommended_next_stage"] = "1-设定"
    state["recommended_entry_path"] = "1-设定"
    state["recommended_next_step"] = "进入 `1-设定`，基于 `0-初始化/north_star.yaml` 与 `0-初始化/init_handoff.yaml` 建立角色/场景/物品 cards 真源。"
    state["governance_mode"] = "lightweight_init"
    state["story_source_status"] = "seed_only_no_primary_story_source"
    state["init_session"] = {
        "mode": normalized_init_mode,
        "mode_source": normalized_mode_source,
        "decision_owner": normalized_decision_owner,
        "advisor_agents": advisor_agent_list,
        "team_setup": team_setup,
        "research_policy": normalized_research_policy,
    }
    state["paths"] = {
        "runtime_state": str(RUNTIME_STATE_REL),
        "source_root": "源/",
        "context_root": "CONTEXT/",
        "project_memory": str(PROJECT_MEMORY_REL),
        "init_root": "0-初始化/",
        "setting_root": "1-设定/",
        "planning_root": "2-卷章/",
        "drafting_root": "3-初稿/",
        "polish_root": "4-润色/",
        "review_root": "review/",
        "context_return_root": "context-return/",
        "north_star": "0-初始化/north_star.yaml",
        "story_source_manifest": "0-初始化/story-source-manifest.yaml",
        "init_handoff": "0-初始化/init_handoff.yaml",
        "team_manifest": str(TEAM_MANIFEST_REL),
        "project_memory": str(PROJECT_MEMORY_REL),
        "changelog": str(CHANGELOG_REL),
    }
    state["main_artifacts"] = {
        "north_star": "0-初始化/north_star.yaml",
        "init_handoff": "0-初始化/init_handoff.yaml",
        "story_source_manifest": "0-初始化/story-source-manifest.yaml",
        "team": "team.yaml",
        "project_memory": "MEMORY.md",
        "project_state": "STATE.json",
    }
    state["open_unknowns"] = [
        "当前尚未绑定正式故事主源；planning 只能按初始化 seeds 推进。",
    ]
    state["user_action_items"] = [
        "如有正文、大纲或设定主源，请补入项目 `源/` 后回刷 `0-初始化/story-source-manifest.yaml`。",
        "如有需要长期记住的偏好、口味、特殊元素或禁区，请补入项目 `MEMORY.md`。",
        "如有贯穿整个创作阶段的共享附加上下文，请补入项目 `CONTEXT/`。",
        "进入 `1-设定` 建立角色、场景、物品 cards 真源。",
    ]
    state["notes"] = []
    workflow_runtime = state.get("workflow_runtime")
    if not isinstance(workflow_runtime, dict):
        workflow_runtime = {}
        state["workflow_runtime"] = workflow_runtime

    if protagonist_name:
        state["protagonist_state"]["name"] = protagonist_name

    gf_type_norm = (golden_finger_type or "").strip()
    if gf_type_norm in {"无", "无金手指", "无外挂", "none"}:
        state["protagonist_state"]["golden_finger"]["name"] = "无金手指"
        state["protagonist_state"]["golden_finger"]["level"] = 0
        state["protagonist_state"]["golden_finger"]["cooldown"] = 0
    elif golden_finger_name:
        state["protagonist_state"]["golden_finger"]["name"] = golden_finger_name

    # 确保 golden_finger 字段存在且可编辑
    if not state["protagonist_state"]["golden_finger"].get("name"):
        state["protagonist_state"]["golden_finger"]["name"] = "未命名金手指"

    state["progress"]["last_updated"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    state_path.parent.mkdir(parents=True, exist_ok=True)
    # 使用原子化写入（初始化不需要备份旧文件）
    atomic_write_json(state_path, state, use_lock=True, backup=False)

    init_now = datetime.now()
    now = init_now.strftime("%Y-%m-%d")
    now_iso = init_now.isoformat()

    workflow_state = _ensure_workflow_state_schema(state.get("workflow_runtime", {}).get("workflow_state", {}))
    execution_state = _ensure_execution_state_schema(state.get("workflow_runtime", {}).get("execution_state", {}))
    task_log: List[Dict[str, Any]] = state.get("workflow_runtime", {}).get("task_log", [])
    if not isinstance(task_log, list):
        task_log = []
    init_task_row = {
        "timestamp": now_iso,
        "event": "project_initialized",
        "payload": {
            "title": title,
            "genre": genre,
            "project_root": str(project_path),
            "target_words": int(target_words),
            "target_chapters": int(target_chapters),
            "init_mode": normalized_init_mode,
            "mode_source": normalized_mode_source,
            "decision_owner": normalized_decision_owner,
            "advisor_agents": advisor_agent_list,
            "shared_council_agents": team_setup["shared_agents"],
            "planning_council_agents": team_setup["planning_agents"],
            "production_council_agents": team_setup["production_agents"],
            "review_council_agents": team_setup["review_agents"],
            "council_team_mode": team_setup["team_mode"],
            "team_lineup_mode": team_setup["team_lineup_mode"],
            "selector_scope_root": team_setup["selector_scope_root"],
            "team_setup": team_setup,
            "research_policy": normalized_research_policy,
            "init_contract_model": "north_star+story_source_manifest+init_handoff",
            "primary_init_artifact": "0-初始化/north_star.yaml",
            "project_entry_state_file": str(PROJECT_STATE_MANIFEST_REL),
            "team_manifest_file": str(TEAM_MANIFEST_REL),
            "project_memory_file": str(PROJECT_MEMORY_REL),
            "changelog_file": str(CHANGELOG_REL),
            "project_context_root": "CONTEXT/",
            "one_liner": one_liner,
            "core_conflict": core_conflict,
        },
    }
    task_log.append(init_task_row if not task_log else {**init_task_row, "event": "project_reinitialized"})

    _sync_init_stage_progress(execution_state, completed_at=now_iso)

    init_payload = _build_init_handoff_payload(
        init_mode=normalized_init_mode,
        mode_source=normalized_mode_source,
        decision_owner=normalized_decision_owner,
        advisor_agents=advisor_agents,
        shared_council_agents=shared_council_agents,
        planning_agents=planning_agents,
        production_agents=production_agents,
        review_agents=review_agents,
        research_policy=normalized_research_policy,
        user_confirmed_fields=user_confirmed_fields,
        council_advised_fields=council_advised_fields,
        assistant_inferred_fields=assistant_inferred_fields,
        title=title,
        genre=genre,
        protagonist_name=protagonist_name,
        target_words=target_words,
        target_chapters=target_chapters,
        one_liner=one_liner,
        core_conflict=core_conflict,
        golden_finger_name=golden_finger_name,
        golden_finger_type=golden_finger_type,
        golden_finger_style=golden_finger_style,
        golden_finger_growth_rhythm=golden_finger_growth_rhythm,
        core_selling_points=core_selling_points,
        protagonist_structure=protagonist_structure,
        heroine_config=heroine_config,
        heroine_names=heroine_names,
        heroine_role=heroine_role,
        co_protagonists=co_protagonists,
        co_protagonist_roles=co_protagonist_roles,
        antagonist_tiers=antagonist_tiers,
        antagonist_mirror=antagonist_mirror,
        world_scale=world_scale,
        factions=factions,
        power_system_type=power_system_type,
        social_class=social_class,
        resource_distribution=resource_distribution,
        gf_visibility=gf_visibility,
        gf_irreversible_cost=gf_irreversible_cost,
        protagonist_desire=protagonist_desire,
        protagonist_flaw=protagonist_flaw,
        protagonist_archetype=protagonist_archetype,
        antagonist_level=antagonist_level,
        target_reader=target_reader,
        platform=platform,
        anti_trope=anti_trope,
        hard_constraints=hard_constraints,
        opening_hook=opening_hook,
        currency_system=currency_system,
        currency_exchange=currency_exchange,
        sect_hierarchy=sect_hierarchy,
        cultivation_chain=cultivation_chain,
        cultivation_subtiers=cultivation_subtiers,
        story_kernel_why_now=story_kernel_why_now,
        story_kernel_ending_vector=story_kernel_ending_vector,
        tone=tone,
        violence_texture=violence_texture,
        mystery_density=mystery_density,
        worldline_mode=worldline_mode,
        old_character_policy=old_character_policy,
        must_keep=must_keep,
        must_not_do=must_not_do,
        no_fly_zones=no_fly_zones,
        now_iso=now_iso,
    )
    north_star_payload = _build_north_star_contract(init_payload)
    story_source_manifest = _build_story_source_manifest(title=title, now_iso=now_iso)
    init_handoff_payload = _build_init_handoff_artifact(init_payload)

    state["main_artifacts"] = {
        "north_star": "0-初始化/north_star.yaml",
        "init_handoff": "0-初始化/init_handoff.yaml",
        "story_source_manifest": "0-初始化/story-source-manifest.yaml",
        "team": "team.yaml",
        "project_memory": "MEMORY.md",
        "project_state": "STATE.json",
    }
    state["workflow_runtime"] = {
        "workflow_state": workflow_state,
        "execution_state": execution_state,
        "task_log": task_log,
        "governance_index": execution_state.get("governance_index", {}),
    }

    _write_yaml(project_path / INIT_STAGE_REL / "north_star.yaml", north_star_payload)
    _write_yaml(project_path / INIT_STAGE_REL / "story-source-manifest.yaml", story_source_manifest)
    _write_yaml(project_path / INIT_STAGE_REL / "init_handoff.yaml", init_handoff_payload)
    atomic_write_json(state_path, state, use_lock=True, backup=False)
    _write_text(
        project_path / TEAM_MANIFEST_REL,
        _render_team_manifest_yaml(
            title=title,
            now_iso=now_iso,
            team_setup=team_setup,
            init_mode=normalized_init_mode,
            mode_source=normalized_mode_source,
            decision_owner=normalized_decision_owner,
            research_policy=normalized_research_policy,
        ),
    )
    _write_text_if_missing(project_path / PROJECT_MEMORY_REL, _render_project_memory(title, now))
    _write_text_if_missing(project_path / CHANGELOG_REL, _render_changelog(title, now))
    for lock_target in (
        state_path,
        project_path / INIT_STAGE_REL / "north_star.yaml",
        project_path / INIT_STAGE_REL / "story-source-manifest.yaml",
        project_path / INIT_STAGE_REL / "init_handoff.yaml",
    ):
        _cleanup_lock_file(lock_target)

    # 记录工作区默认项目指针（非阻断）
    try:
        pointer_file = write_current_project_pointer(project_path)
        if pointer_file is not None:
            print(f"Default project pointer updated: {pointer_file}")
    except Exception as e:
        print(f"Default project pointer update failed (non-fatal): {e}")

    print(f"\nProject initialized at: {project_path}")
    print("Generated files:")
    print(" - STATE.json")
    print(" - team.yaml")
    print(" - MEMORY.md")
    print(" - CHANGELOG.md")
    print(" - 0-初始化/north_star.yaml")
    print(" - 0-初始化/story-source-manifest.yaml")
    print(" - 0-初始化/init_handoff.yaml")
    print("Generated directories:")
    print(" - 源/")
    print(" - CONTEXT/")
    print(" - 1-设定/")
    print(" - 2-卷章/")
    print(" - 3-初稿/")
    print(" - 4-润色/")
    print(" - review/")
    print(" - context-return/")
    print("2-卷章/整体规划.md is not created during /story-init; generate it via /story-plan.")
    print("Workflow runtime now lives inside STATE.json.workflow_runtime.")


def main() -> None:
    parser = argparse.ArgumentParser(description="网文项目初始化脚本（生成项目结构 + STATE.json + 基础模板）")
    parser.add_argument("project_dir", help="项目目录（建议 ./projects/story/<小说名>）")
    parser.add_argument("title", help="小说标题")
    parser.add_argument(
        "genre",
        help="题材类型（可用“+”组合，如：都市脑洞+规则怪谈；示例：修仙/系统流/都市异能/古言/现实题材）",
    )

    parser.add_argument("--init-mode", default="team代入模式", help="初始化模式（统一归一为 team代入模式；旧模式值仍兼容）")
    parser.add_argument("--mode-source", default="", help="模式来源（user_selected/defaulted/inferred/switched_midway）")
    parser.add_argument("--decision-owner", default="", help="最终拍板者（user/assistant）")
    parser.add_argument("--advisor-agents", default="", help="顾问团 agent 路径（legacy 兼容：默认映射到策划阶段），多个用逗号分隔")
    parser.add_argument("--shared-council-agents", default="", help="同一套班底三阶段通用的 agent 路径，多个用逗号分隔")
    parser.add_argument("--planning-agents", default="", help="策划阶段坐镇 agent 路径，多个用逗号分隔")
    parser.add_argument("--production-agents", default="", help="监制阶段坐镇 agent 路径，多个用逗号分隔")
    parser.add_argument("--review-agents", default="", help="评审阶段坐镇 agent 路径，多个用逗号分隔")
    parser.add_argument("--research-policy", default="", help="联网补全策略（如 none/targeted-web-precision）")
    parser.add_argument("--user-confirmed-fields", default="", help="用户确认字段路径，多个用逗号分隔")
    parser.add_argument("--council-advised-fields", default="", help="顾问团建议字段路径，多个用逗号分隔")
    parser.add_argument("--assistant-inferred-fields", default="", help="助手推断字段路径，多个用逗号分隔")
    parser.add_argument("--protagonist-name", default="", help="主角姓名")
    parser.add_argument("--target-words", type=int, default=2_000_000, help="目标总字数（默认 2000000）")
    parser.add_argument("--target-chapters", type=int, default=600, help="目标总章节数（默认 600）")
    parser.add_argument("--one-liner", default="", help="一句话故事（项目立项合同）")
    parser.add_argument("--core-conflict", default="", help="核心冲突（项目立项合同）")

    parser.add_argument("--golden-finger-name", default="", help="金手指称呼/系统名（建议读者可见的代号）")
    parser.add_argument("--golden-finger-type", default="", help="金手指类型（如 系统流/鉴定流/签到流）")
    parser.add_argument("--golden-finger-style", default="", help="金手指风格（如 冷漠工具型/毒舌吐槽型）")
    parser.add_argument("--golden-finger-growth-rhythm", default="", help="金手指成长节奏（慢热/中速/快节奏）")
    parser.add_argument("--core-selling-points", default="", help="核心卖点（逗号分隔）")
    parser.add_argument("--protagonist-structure", default="", help="主角结构（单主角/多主角）")
    parser.add_argument("--heroine-config", default="", help="女主配置（无女主/单女主/多女主）")
    parser.add_argument("--heroine-names", default="", help="女主姓名（多个用逗号分隔）")
    parser.add_argument("--heroine-role", default="", help="女主定位（事业线/情感线/对抗线）")
    parser.add_argument("--co-protagonists", default="", help="多主角姓名（逗号分隔）")
    parser.add_argument("--co-protagonist-roles", default="", help="多主角定位（逗号分隔）")
    parser.add_argument("--antagonist-tiers", default="", help="反派分层（如 小反派:张三;中反派:李四;大反派:王五）")
    parser.add_argument("--antagonist-mirror", default="", help="主角与反派的镜像关系")
    parser.add_argument("--world-scale", default="", help="世界规模")
    parser.add_argument("--factions", default="", help="势力格局/核心势力")
    parser.add_argument("--power-system-type", default="", help="力量体系类型")
    parser.add_argument("--social-class", default="", help="社会阶层")
    parser.add_argument("--resource-distribution", default="", help="资源分配")
    parser.add_argument("--gf-visibility", default="", help="金手指可见度（明牌/半明牌/暗牌）")
    parser.add_argument("--gf-irreversible-cost", default="", help="金手指不可逆代价")
    parser.add_argument("--currency-system", default="", help="货币体系")
    parser.add_argument("--currency-exchange", default="", help="货币兑换/面值规则")
    parser.add_argument("--sect-hierarchy", default="", help="宗门/组织层级")
    parser.add_argument("--cultivation-chain", default="", help="典型境界链")
    parser.add_argument("--cultivation-subtiers", default="", help="小境界划分（初/中/后/巅 等）")
    parser.add_argument("--story-kernel-why-now", default="", help="故事核：为何是这场故事、此刻才爆发")
    parser.add_argument("--story-kernel-ending-vector", default="", help="故事核：终局方向/终局姿态")
    parser.add_argument("--tone", default="", help="审美轴：整体气质/基调")
    parser.add_argument("--violence-texture", default="", help="审美轴：暴力与受伤质地")
    parser.add_argument("--mystery-density", default="", help="审美轴：谜团/迷雾密度")
    parser.add_argument("--worldline-mode", default="", help="IP 边界：同世界/平行线/重写线")
    parser.add_argument("--old-character-policy", default="", help="IP 边界：旧角色使用策略")
    parser.add_argument("--must-keep", default="", help="IP 边界：必须保留项，逗号分隔")
    parser.add_argument("--must-not-do", default="", help="IP 边界：禁止做的事，逗号分隔")
    parser.add_argument("--no-fly-zones", default="", help="读者承诺：禁飞区，逗号分隔")

    # 初始化扩展字段（统一 team 代入模式下均可预填）
    parser.add_argument("--protagonist-desire", default="", help="主角核心欲望（初始化扩展字段）")
    parser.add_argument("--protagonist-flaw", default="", help="主角性格弱点（初始化扩展字段）")
    parser.add_argument("--protagonist-archetype", default="", help="主角人设类型（初始化扩展字段）")
    parser.add_argument("--antagonist-level", default="", help="反派等级（初始化扩展字段）")
    parser.add_argument("--target-reader", default="", help="目标读者（初始化扩展字段）")
    parser.add_argument("--platform", default="", help="发布平台（初始化扩展字段）")
    parser.add_argument("--anti-trope", default="", help="反套路主规则（初始化扩展字段）")
    parser.add_argument("--hard-constraints", default="", help="硬约束（逗号分隔，初始化扩展字段）")
    parser.add_argument("--opening-hook", default="", help="开篇钩子（初始化扩展字段）")

    args = parser.parse_args()

    init_project(
        args.project_dir,
        args.title,
        args.genre,
        init_mode=args.init_mode,
        mode_source=args.mode_source,
        decision_owner=args.decision_owner,
        advisor_agents=args.advisor_agents,
        shared_council_agents=args.shared_council_agents,
        planning_agents=args.planning_agents,
        production_agents=args.production_agents,
        review_agents=args.review_agents,
        research_policy=args.research_policy,
        user_confirmed_fields=args.user_confirmed_fields,
        council_advised_fields=args.council_advised_fields,
        assistant_inferred_fields=args.assistant_inferred_fields,
        protagonist_name=args.protagonist_name,
        target_words=args.target_words,
        target_chapters=args.target_chapters,
        one_liner=args.one_liner,
        core_conflict=args.core_conflict,
        golden_finger_name=args.golden_finger_name,
        golden_finger_type=args.golden_finger_type,
        golden_finger_style=args.golden_finger_style,
        golden_finger_growth_rhythm=args.golden_finger_growth_rhythm,
        core_selling_points=args.core_selling_points,
        protagonist_structure=args.protagonist_structure,
        heroine_config=args.heroine_config,
        heroine_names=args.heroine_names,
        heroine_role=args.heroine_role,
        co_protagonists=args.co_protagonists,
        co_protagonist_roles=args.co_protagonist_roles,
        antagonist_tiers=args.antagonist_tiers,
        antagonist_mirror=args.antagonist_mirror,
        world_scale=args.world_scale,
        factions=args.factions,
        power_system_type=args.power_system_type,
        social_class=args.social_class,
        resource_distribution=args.resource_distribution,
        gf_visibility=args.gf_visibility,
        gf_irreversible_cost=args.gf_irreversible_cost,
        protagonist_desire=args.protagonist_desire,
        protagonist_flaw=args.protagonist_flaw,
        protagonist_archetype=args.protagonist_archetype,
        antagonist_level=args.antagonist_level,
        target_reader=args.target_reader,
        platform=args.platform,
        anti_trope=args.anti_trope,
        hard_constraints=args.hard_constraints,
        opening_hook=args.opening_hook,
        currency_system=args.currency_system,
        currency_exchange=args.currency_exchange,
        sect_hierarchy=args.sect_hierarchy,
        cultivation_chain=args.cultivation_chain,
        cultivation_subtiers=args.cultivation_subtiers,
        story_kernel_why_now=args.story_kernel_why_now,
        story_kernel_ending_vector=args.story_kernel_ending_vector,
        tone=args.tone,
        violence_texture=args.violence_texture,
        mystery_density=args.mystery_density,
        worldline_mode=args.worldline_mode,
        old_character_policy=args.old_character_policy,
        must_keep=args.must_keep,
        must_not_do=args.must_not_do,
        no_fly_zones=args.no_fly_zones,
    )


if __name__ == "__main__":
    main()
