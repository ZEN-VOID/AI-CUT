#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
网文项目初始化脚本

目标：
- 生成可运行的项目结构（推荐位于 `projects/<小说名>/`）
- 创建/更新 .webnovel/state.json（运行时真相）
- 生成基础 stage 目录与兼容性规划模板文件（供 /story-plan 与 /story-write 使用）

说明：
- 该脚本是命令 /story-init 的“唯一允许的文件生成入口”（与命令文档保持一致）。
- 生成的内容以“模板骨架”为主，便于 AI/作者后续补全；但保证所有关键文件存在。
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from datetime import datetime
from pathlib import Path

from runtime_compat import enable_windows_utf8_stdio
from typing import Any, Dict, List
import re

# 安全修复：导入安全工具函数
from security_utils import sanitize_commit_message, atomic_write_json, is_git_available
from project_locator import write_current_project_pointer


RUNTIME_STATE_REL = Path(".webnovel") / "state.json"
WORKFLOW_STATE_REL = Path(".webnovel") / "workflow_state.json"
EXECUTION_STATE_REL = Path(".webnovel") / "execution_state.json"
TASK_LOG_REL = Path(".webnovel") / "task_log.jsonl"
TASK_ARTIFACTS_ROOT_REL = Path(".webnovel") / "tasks"
IDEA_BANK_REL = Path(".webnovel") / "idea_bank.json"
PROJECT_STATE_MANIFEST_REL = Path("STATE.json")
TEAM_MANIFEST_REL = Path("TEAM.toml")
CHANGELOG_REL = Path("CHANGELOG.md")
PLANNING_SKILL_PATHS = [
    ".agents/skills/story/0-Init",
    ".agents/skills/story/1-Cards",
    ".agents/skills/story/2-Planning",
]
PRODUCTION_SKILL_PATHS = [
    ".agents/skills/story/3-Drafting",
    ".agents/skills/story/5-Loopback",
]
REVIEW_SKILL_PATHS = [
    ".agents/skills/story/4-Validation",
    ".agents/skills/story/review",
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


def _cleanup_lock_file(path: Path) -> None:
    lock_path = path.with_suffix(path.suffix + ".lock")
    if lock_path.exists():
        lock_path.unlink()


def _toml_quote(value: str) -> str:
    return json.dumps(value, ensure_ascii=False)


def _render_toml_array(values: List[str]) -> str:
    return "[" + ", ".join(_toml_quote(value) for value in values if value) + "]"


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

    team_mode = "unspecified"
    if shared_agents:
        team_mode = "same_lineup"
        planning_members = list(shared_agents)
        production_members = list(shared_agents)
        review_members = list(shared_agents)
    elif any((planning_members, production_members, review_members)):
        team_mode = "per_stage"
    elif legacy_advisor_agents:
        team_mode = "legacy_planning_only"
        planning_members = list(legacy_advisor_agents)

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
        }

    return {
        "team_mode": team_mode,
        "shared_agents": _unique_preserve_order(shared_agents),
        "legacy_advisor_agents": _unique_preserve_order(legacy_advisor_agents),
        "planning_agents": team_roles["planning"]["members"],
        "production_agents": team_roles["production"]["members"],
        "review_agents": team_roles["review"]["members"],
        "roles": team_roles,
    }


def _council_mode_display(team_mode: str) -> str:
    mapping = {
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
        return "自主模式"
    mapping = {
        "智能顾问团模式": "智能顾问团模式",
        "顾问团模式": "智能顾问团模式",
        "顾问团": "智能顾问团模式",
        "advisor": "智能顾问团模式",
        "advisory": "智能顾问团模式",
        "council": "智能顾问团模式",
        "快速模式": "快速模式",
        "快速": "快速模式",
        "quick": "快速模式",
        "fast": "快速模式",
        "自主模式": "自主模式",
        "自主": "自主模式",
        "autonomous": "自主模式",
        "interactive": "自主模式",
        "deep": "自主模式",
        "深度模式": "自主模式",
    }
    return mapping.get(raw.strip(), mapping.get(value, "自主模式"))


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
    return "defaulted" if normalized_mode == "自主模式" else "inferred"


def _normalize_decision_owner(raw: str, normalized_mode: str) -> str:
    value = (raw or "").strip().lower()
    if value in {"assistant", "user"}:
        return value
    return "assistant" if normalized_mode == "快速模式" else "user"


def _ensure_state_schema(state: Dict[str, Any]) -> Dict[str, Any]:
    """确保 state.json 具备 v5.1 架构所需的字段集合（v5.4 沿用）。

    v5.1 变更:
    - entities_v3 和 alias_index 已迁移到 index.db，不再存储在 state.json
    - structured_relationships 已迁移到 index.db relationships 表
    - state.json 保持精简 (< 5KB)
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
    # 不再在 state.json 中初始化这些字段

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
    state.setdefault("schema_version", "2.0")
    state.setdefault("updated_at", datetime.now().isoformat())
    state.setdefault("current_task", None)
    state.setdefault("last_stable_state", None)
    state.setdefault("history", [])
    state["updated_at"] = datetime.now().isoformat()
    return state


def _ensure_execution_state_schema(state: Dict[str, Any]) -> Dict[str, Any]:
    if not isinstance(state, dict):
        state = {}
    stage_progress = state.get("stage_progress")
    if not isinstance(stage_progress, dict):
        stage_progress = {}
    defaults = {
        "0-init": "初始化",
        "1-cards": "卡片层",
        "2-planning": "规划层",
        "3-drafting": "起草层",
        "4-validation": "验证层",
        "review": "审查层",
        "5-loopback": "回写层",
        "query": "查询层",
        "resume": "恢复层",
    }
    for stage_id, label in defaults.items():
        snapshot = stage_progress.get(stage_id)
        if not isinstance(snapshot, dict):
            snapshot = {}
        snapshot.setdefault("stage_label", label)
        snapshot.setdefault("status", "idle")
        snapshot.setdefault("latest_run_id", None)
        snapshot.setdefault("latest_command", None)
        snapshot.setdefault("current_step", None)
        snapshot.setdefault("resume_ready", False)
        snapshot.setdefault("last_started_at", None)
        snapshot.setdefault("last_completed_at", None)
        snapshot.setdefault("last_failed_at", None)
        snapshot.setdefault("last_cleared_at", None)
        stage_progress[stage_id] = snapshot
    state["stage_progress"] = stage_progress
    state.setdefault("schema_version", "1.0")
    state.setdefault("updated_at", datetime.now().isoformat())
    state.setdefault("active_run_id", None)
    state.setdefault("run_sequence", 0)
    state.setdefault("latest_resume_point", None)
    state.setdefault("runs", [])
    state.setdefault("artifacts_index", {})
    state["updated_at"] = datetime.now().isoformat()
    return state


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
        "> 本文件为 legacy 兼容骨架；正式规划真源应由 /story-plan 收敛到 Planning/8-全息地图.json。",
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
            "> 说明：本文件是 `0-Init` 阶段生成的 seed / legacy-compat 材料，不是项目 canonical 真源。",
            "> 正式真源统一以 `Cards/**/*.json` 为准；后续阶段禁止继续人工维护本文件，除非做一次性迁移。",
            "",
        ]
    )
    if content.startswith("> 说明：本文件是 `0-Init` 阶段生成的 seed / legacy-compat 材料"):
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
    cards_projection = {
        "scope": "full-series",
        "section_order": [
            "文字风格",
            "叙事风格",
            "世界观",
            "规则体系",
            "年代约时",
            "文化",
            "艺术",
            "科技武功",
            "关系网总览",
        ],
        "style_system": {
            "text_style": {
                "tone": north_star_inputs.get("tone", ""),
                "genre_corridor": creative["genre"],
                "anti_trope": promise["anti_trope"],
            },
            "narrative_style": {
                "opening_hook": promise["opening_hook"],
                "mystery_density": north_star_inputs.get("mystery_density", ""),
                "romance_policy": relationship["heroine_config"],
            },
            "tone_promises": promise["core_selling_points"],
            "taboo_styles": north_star_inputs.get("no_fly_zones", []),
            "downstream_constraints": promise["hard_constraints"],
        },
        "world_system": {
            "worldview": {
                "world_scale": world_seed["world_scale"],
                "genre": creative["genre"],
                "target_reader": creative["target_reader"],
                "platform": creative["platform"],
            },
            "rule_system": [item for item in rule_system if item["value"]],
            "era_timeline": {
                "era_anchor": world_seed["world_scale"],
                "worldline_mode": north_star_inputs.get("worldline_mode", ""),
            },
            "culture": _compact_values(world_seed["social_class"]),
            "arts": _compact_values(
                north_star_inputs.get("tone", ""),
                north_star_inputs.get("violence_texture", ""),
            ),
            "tech_or_martial": _compact_values(
                world_seed["power_system_type"],
                world_seed["cultivation_chain"],
                world_seed["sect_hierarchy"],
            ),
            "section_constraints": north_star_inputs.get("must_keep", []) + north_star_inputs.get("must_not_do", []),
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

    return {
        "schema_version": "story2026/north-star-contract/v2",
        "meta": {
            "source_stage": "0-Init",
            "generated_at": payload["meta"]["generated_at"],
            "role": "primary-init-artifact",
            "scope": "full-series",
            "canonical_consumers": ["1-Cards", "2-Planning"],
            "companion_handoff": "Init/初始化简报.json",
            "cards_role": "north-star-object-constraints",
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
        "cards": cards_projection,
        "decision_policy": project_contract["decision_policy"],
    }


def _build_init_companion_payload(payload: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "schema_version": "story2026/init-handoff/v4",
        "meta": {
            "source_stage": "0-Init",
            "generated_at": payload["meta"]["generated_at"],
            "canonical_consumer": "1-Cards",
            "primary_artifact": "Init/north_star_contract.json",
            "companion_role": "cards-planning-handoff",
            "contract_model": "north_star_contract + cards_seed + planning_seed + unknowns",
            "project_entry_state": str(PROJECT_STATE_MANIFEST_REL),
            "team_manifest": str(TEAM_MANIFEST_REL),
            "changelog_file": str(CHANGELOG_REL),
        },
        "init_session": payload["init_session"],
        "north_star_ref": "Init/north_star_contract.json",
        "cards_seed": payload["cards_seed"],
        "planning_seed": payload["planning_seed"],
        "unknowns": payload["unknowns"],
        "sources_breakdown": payload["sources_breakdown"],
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


def _build_sources_breakdown(
    payload: Dict[str, Any],
    *,
    normalized_mode: str,
    user_confirmed_fields: str,
    council_advised_fields: str,
    assistant_inferred_fields: str,
) -> Dict[str, List[str]]:
    all_fields = _collect_nonempty_field_paths(payload)
    default_bucket = {
        "自主模式": "user_confirmed",
        "智能顾问团模式": "council_advised",
        "快速模式": "assistant_inferred",
    }[normalized_mode]
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
    normalized_research_policy = (research_policy or "").strip() or (
        "targeted-web-precision" if normalized_mode == "快速模式" else "none"
    )
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
            "source_stage": "0-Init",
            "generated_at": now_iso,
            "canonical_consumer": "1-Cards",
            "canonical_truth": "Cards/**/*.json",
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

    user_confirmed: Dict[str, Dict[str, Any]] = {}
    for section in ("project", "protagonist", "relationship", "golden_finger", "world", "constraints"):
        section_values = payload[section]
        confirmed = {key: value for key, value in section_values.items() if value not in ("", [], {}, None)}
        if confirmed:
            user_confirmed[section] = confirmed
    payload["confirmation"]["user_confirmed"] = user_confirmed
    payload["sources_breakdown"] = _build_sources_breakdown(
        payload,
        normalized_mode=normalized_mode,
        user_confirmed_fields=user_confirmed_fields,
        council_advised_fields=council_advised_fields,
        assistant_inferred_fields=assistant_inferred_fields,
    )
    return payload


def _render_sources_breakdown_block(payload: Dict[str, Any]) -> List[str]:
    breakdown = payload.get("sources_breakdown", {})
    return [
        "## 字段来源",
        f"- 用户确认：{', '.join(breakdown.get('user_confirmed', [])) if breakdown.get('user_confirmed') else '无'}",
        f"- 顾问团建议：{', '.join(breakdown.get('council_advised', [])) if breakdown.get('council_advised') else '无'}",
        f"- 助手推断：{', '.join(breakdown.get('assistant_inferred', [])) if breakdown.get('assistant_inferred') else '无'}",
        "",
    ]


def _render_init_summary_markdown(payload: Dict[str, Any]) -> str:
    init_session = payload["init_session"]
    team_setup = init_session.get("team_setup", {})
    unknowns = payload["unknowns"]
    pending_lines = [f"- {item}" for item in unknowns["unresolved_questions"]] or ["- 无"]

    return "\n".join(
        [
            "# 访谈摘要",
            "",
            "> 本页只保留初始化产物导航，不重复承载核心设定正文。",
            "",
            "## 文件角色",
            "- 主文件：`Init/north_star_contract.json`",
            "- 伴生交接物：`Init/初始化简报.json`",
            "- 长期对象约束：`Init/north_star_contract.json.cards`",
            "- 项目入口状态：`STATE.json`（标准入口，指向运行态与关键工件路径）",
            "- 团队治理模板：`TEAM.toml`",
            "- 版本变更记录：`CHANGELOG.md`",
            "- 对象真源阶段：`Cards/**/*.json`",
            "- 规划真源阶段：`Planning/8-全息地图.json`",
            "",
            "## 会话元信息",
            f"- 模式：{init_session['mode'] or '（待补充）'}",
            f"- 模式来源：{init_session['mode_source'] or '（待补充）'}",
            f"- 顾问团布阵：{_council_mode_display(team_setup.get('team_mode', 'unspecified'))}",
            f"- 策划坐镇：{_format_team_members(team_setup, 'planning')}",
            f"- 监制坐镇：{_format_team_members(team_setup, 'production')}",
            f"- 评审坐镇：{_format_team_members(team_setup, 'review')}",
            f"- 联网策略：{init_session['research_policy'] or 'none'}",
            f"- 默认拍板者：{init_session['decision_owner'] or 'user'}",
            "",
            *_render_sources_breakdown_block(payload),
            "## Unknowns",
            *pending_lines,
            f"- Deferred to Cards：{', '.join(unknowns['deferred_to_cards']) if unknowns['deferred_to_cards'] else '无'}",
            f"- Deferred to Planning：{', '.join(unknowns['deferred_to_planning']) if unknowns['deferred_to_planning'] else '无'}",
            "",
        ]
    ) + "\n"


def _render_confirmation_card_markdown(payload: Dict[str, Any]) -> str:
    init_session = payload["init_session"]
    team_setup = init_session.get("team_setup", {})
    unknowns = payload["unknowns"]
    pending_lines = [f"- {item}" for item in unknowns["unresolved_questions"]] or ["- 无"]
    return "\n".join(
        [
            "# 确认卡",
            "",
            "> 本卡只冻结初始化文件角色与交接边界，不重复正文设定。",
            "",
            "## 文件裁决",
            "- 主文件：`Init/north_star_contract.json`",
            "- 伴生交接物：`Init/初始化简报.json`",
            "- 原“全局卡/全局总览”长期约束已并入 `north_star_contract.json.cards`",
            "- `STATE.json` 是项目入口状态清单，不替代 `.webnovel/state.json` 运行快照",
            "- `TEAM.toml` 是团队治理模板，`策划 / 监制 / 评审` 三阶段按已知程度落盘",
            "- `CHANGELOG.md` 是项目级变更记录入口",
            "- `0-Init` 不再把重复设定正文散落到多个 Init 文件",
            "",
            "## 会话裁决",
            f"- 初始化模式：{init_session['mode'] or '（待补充）'}",
            f"- 模式来源：{init_session['mode_source'] or '（待补充）'}",
            f"- 顾问团布阵：{_council_mode_display(team_setup.get('team_mode', 'unspecified'))}",
            f"- 策划坐镇：{_format_team_members(team_setup, 'planning')}",
            f"- 监制坐镇：{_format_team_members(team_setup, 'production')}",
            f"- 评审坐镇：{_format_team_members(team_setup, 'review')}",
            f"- 默认拍板者：{init_session['decision_owner'] or 'user'}",
            f"- 主文件状态：{'ready' if not unknowns['unresolved_questions'] else 'pending'}",
            "",
            *_render_sources_breakdown_block(payload),
            "## Unknowns",
            *pending_lines,
            f"- Deferred to Cards：{', '.join(unknowns['deferred_to_cards']) if unknowns['deferred_to_cards'] else '无'}",
            f"- Deferred to Planning：{', '.join(unknowns['deferred_to_planning']) if unknowns['deferred_to_planning'] else '无'}",
            "",
            "## 交接规则",
            "- `north_star_contract.json` 是初始化主文件。",
            "- `north_star_contract.json.cards` 承担原全局卡的长期对象总规范。",
            "- `初始化简报.json` 是伴生 handoff，用于承接 `cards_seed / planning_seed / unknowns`。",
            "- `访谈摘要.md` / `确认卡.md` 仅保留指针与边界，不重复正文设定。",
            "- `1-Cards` 是人物、世界、规则、物品的唯一 canonical。",
            "",
        ]
    ) + "\n"


def _render_init_readme() -> str:
    return (
        "\n".join(
            [
                "# Init 目录说明",
                "",
                "- `north_star_contract.json`：初始化主文件，承载故事核、读者承诺、审美轴、IP 边界，以及 `cards` 长期对象约束分区。",
                "- `初始化简报.json`：伴生 handoff，只承接 `cards_seed / planning_seed / unknowns`。",
                "- `访谈摘要.md` / `确认卡.md`：仅保留导航、边界与未决项，不重复正文设定。",
                "- 项目根目录的 `STATE.json`：项目入口状态清单，统一声明运行态与关键工件路径。",
                "- 项目根目录的 `TEAM.toml`：团队治理模板，初始化按已知信息填好 `策划 / 监制 / 评审` 三阶段。",
                "- 项目根目录的 `CHANGELOG.md`：项目级变更记录入口。",
                "- `.webnovel/tasks/`：复杂任务治理工件根目录，后续 tracked run 会在其下写入三省 shadow 工件。",
                "- 新项目默认不再生成额外 `Init/*.md` seed 文档。",
                "- 原“全局卡/全局总览”概念已废弃；长期总规范统一归入 `north_star_contract.json.cards`。",
                "- 一旦 `1-Cards` 完成建卡，人物、场景、物品的正式真源统一以 `Cards/**/*.json` 为准。",
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
            "workflow_state": str(WORKFLOW_STATE_REL),
            "execution_state": str(EXECUTION_STATE_REL),
            "task_log": str(TASK_LOG_REL),
            "task_artifacts_root": str(TASK_ARTIFACTS_ROOT_REL),
            "idea_bank": str(IDEA_BANK_REL),
            "north_star_contract": "Init/north_star_contract.json",
            "init_handoff": "Init/初始化简报.json",
            "team_manifest": str(TEAM_MANIFEST_REL),
            "changelog": str(CHANGELOG_REL),
        },
        "truth_layers": {
            "project_entry": str(PROJECT_STATE_MANIFEST_REL),
            "runtime_snapshot": str(RUNTIME_STATE_REL),
            "object_truth": "Cards/**/*.json",
            "planning_truth": "Planning/8-全息地图.json",
        },
    }


def _render_team_manifest(
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
                "- 建立 `STATE.json`、`TEAM.toml`、`CHANGELOG.md` 标准配置。",
                "- 写入 `Init/north_star_contract.json` 与 `Init/初始化简报.json` 初始化合同。",
                "",
            ]
        )
        + "\n"
    )


def init_project(
    project_dir: str,
    title: str,
    genre: str,
    *,
    init_mode: str = "自主模式",
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

    # 目录结构：内容输出统一进入 stage 目录；运行时状态仍保留在 .webnovel/
    directories = [
        ".webnovel/backups",
        ".webnovel/archive",
        ".webnovel/summaries",
        ".webnovel/observability",
        "Init",
        "Cards/2-角色卡/主要角色",
        "Cards/2-角色卡/次要角色",
        "Cards/2-角色卡/反派角色",
        "Cards/2-角色卡/群像角色",
        "Cards/3-场景卡/室内",
        "Cards/3-场景卡/室外",
        "Cards/3-场景卡/自然",
        "Cards/3-场景卡/超现实",
        "Cards/4-物品卡/武器装备",
        "Cards/4-物品卡/线索物品",
        "Cards/4-物品卡/重要叙事物品",
        "Cards/4-物品卡/文物",
        "Cards/4-物品卡/点缀物",
        "Cards/4-物品卡",
        "Cards/其他设定",
        "Planning/8-全息地图",
        "Planning/legacy",
        "Drafting",
        "正文",
        "Validation",
        "Loopback",
    ]
    for dir_path in directories:
        (project_path / dir_path).mkdir(parents=True, exist_ok=True)

    # state.json（创建或增量补齐）
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
    normalized_research_policy = (research_policy or "").strip() or (
        "targeted-web-precision" if normalized_init_mode == "快速模式" else "none"
    )
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
            "team_setup": team_setup,
            "research_policy": normalized_research_policy,
            "init_contract_model": "north_star_contract+cards_seed+planning_seed+unknowns",
            "primary_init_artifact": "Init/north_star_contract.json",
            "north_star_schema_version": "story2026/north-star-contract/v2",
            "init_handoff_schema_version": "story2026/init-handoff/v4",
            "init_companion_schema_version": "story2026/init-handoff/v4",
            "project_entry_state_file": str(PROJECT_STATE_MANIFEST_REL),
            "team_manifest_file": str(TEAM_MANIFEST_REL),
            "changelog_file": str(CHANGELOG_REL),
            "task_artifacts_root": str(TASK_ARTIFACTS_ROOT_REL),
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

    workflow_state_path = project_path / WORKFLOW_STATE_REL
    if workflow_state_path.exists():
        try:
            workflow_state: Dict[str, Any] = json.loads(workflow_state_path.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            workflow_state = {}
    else:
        workflow_state = {}
    workflow_state = _ensure_workflow_state_schema(workflow_state)
    atomic_write_json(workflow_state_path, workflow_state, use_lock=True, backup=False)

    execution_state_path = project_path / EXECUTION_STATE_REL
    if execution_state_path.exists():
        try:
            execution_state: Dict[str, Any] = json.loads(execution_state_path.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            execution_state = {}
    else:
        execution_state = {}
    execution_state = _ensure_execution_state_schema(execution_state)
    atomic_write_json(execution_state_path, execution_state, use_lock=True, backup=False)
    (project_path / TASK_ARTIFACTS_ROOT_REL).mkdir(parents=True, exist_ok=True)

    _append_task_log_if_missing(
        project_path / TASK_LOG_REL,
        {
            "timestamp": datetime.now().isoformat(),
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
                "team_setup": team_setup,
                "research_policy": normalized_research_policy,
                "init_contract_model": "north_star_contract+cards_seed+planning_seed+unknowns",
                "primary_init_artifact": "Init/north_star_contract.json",
                "project_entry_state_file": str(PROJECT_STATE_MANIFEST_REL),
                "team_manifest_file": str(TEAM_MANIFEST_REL),
                "changelog_file": str(CHANGELOG_REL),
                "task_artifacts_root": str(TASK_ARTIFACTS_ROOT_REL),
                "one_liner": one_liner,
                "core_conflict": core_conflict,
            },
        },
    )

    init_now = datetime.now()
    now = init_now.strftime("%Y-%m-%d")
    now_iso = init_now.isoformat()

    init_handoff_payload = _build_init_handoff_payload(
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
    north_star_payload = _build_north_star_contract(init_handoff_payload)
    init_companion_payload = _build_init_companion_payload(init_handoff_payload)
    atomic_write_json(project_path / "Init" / "north_star_contract.json", north_star_payload, use_lock=True, backup=False)
    atomic_write_json(project_path / "Init" / "初始化简报.json", init_companion_payload, use_lock=True, backup=False)
    (project_path / "Init" / "访谈摘要.md").write_text(
        _render_init_summary_markdown(init_companion_payload),
        encoding="utf-8",
    )
    (project_path / "Init" / "确认卡.md").write_text(
        _render_confirmation_card_markdown(init_companion_payload),
        encoding="utf-8",
    )
    (project_path / "Init" / "README.md").write_text(_render_init_readme(), encoding="utf-8")

    idea_bank_payload = {
        "selected_idea": {
            "title": title,
            "one_liner": one_liner,
            "anti_trope": anti_trope,
            "hard_constraints": _split_list_values(hard_constraints),
        },
        "constraints_inherited": {
            "anti_trope": anti_trope,
            "hard_constraints": _split_list_values(hard_constraints),
            "protagonist_flaw": protagonist_flaw,
            "antagonist_mirror": antagonist_mirror,
            "opening_hook": opening_hook,
        },
        "init_session": {
            "mode": normalized_init_mode,
            "mode_source": normalized_mode_source,
            "decision_owner": normalized_decision_owner,
            "advisor_agents": advisor_agent_list,
            "team_setup": team_setup,
            "research_policy": normalized_research_policy,
        },
    }
    atomic_write_json(project_path / IDEA_BANK_REL, idea_bank_payload, use_lock=True, backup=False)
    project_state_payload = _build_project_state_manifest(
        title=title,
        genre=genre,
        now_iso=now_iso,
        init_mode=normalized_init_mode,
        mode_source=normalized_mode_source,
        decision_owner=normalized_decision_owner,
        team_setup=team_setup,
        research_policy=normalized_research_policy,
    )
    atomic_write_json(project_path / PROJECT_STATE_MANIFEST_REL, project_state_payload, use_lock=True, backup=False)
    _write_text_if_missing(project_path / TEAM_MANIFEST_REL, _render_team_manifest(title=title, now_iso=now_iso, team_setup=team_setup))
    _write_text_if_missing(project_path / CHANGELOG_REL, _render_changelog(title, now))
    for lock_target in (
        state_path,
        workflow_state_path,
        execution_state_path,
        project_path / IDEA_BANK_REL,
        project_path / PROJECT_STATE_MANIFEST_REL,
        project_path / "Init" / "north_star_contract.json",
        project_path / "Init" / "初始化简报.json",
    ):
        _cleanup_lock_file(lock_target)

    # 读取内置模板（可选）
    script_dir = Path(__file__).resolve().parent
    templates_dir = script_dir.parent / "templates"
    output_templates_dir = templates_dir / "output"
    output_outline = _read_text_if_exists(output_templates_dir / "大纲-总纲.md")

    outline_content = output_outline.strip() if output_outline else ""
    if outline_content:
        outline_content = _inject_volume_rows(outline_content, int(target_chapters)).rstrip() + "\n"
    else:
        outline_content = _build_master_outline(int(target_chapters))
    outline_content = _inject_legacy_outline_contract_snapshot(outline_content, init_handoff_payload)
    _write_text_if_missing(project_path / "Planning" / "legacy" / "总纲.md", outline_content)

    _write_text_if_missing(
        project_path / "Planning" / "legacy" / "爽点规划.md",
        "\n".join(
            [
                "# 爽点规划",
                "",
                f"> 项目：{title}｜题材：{genre}｜创建：{now}",
                "",
                "## 核心卖点（来自初始化输入）",
                f"- {core_selling_points or '（待填写，建议 1-3 条，用逗号分隔）'}",
                "",
                "## 密度目标（建议）",
                "- 每章至少 1 个小爽点",
                "- 每 5 章至少 1 个大爽点",
                "",
                "## 分布表（示例，可改）",
                "",
                "| 章节范围 | 主导爽点类型 | 备注 |",
                "|---|---|---|",
                "| 1-5 | 金手指/打脸/反转 | 开篇钩子 + 立人设 |",
                "| 6-10 | 升级/收获 | 进入主线节奏 |",
                "",
            ]
        ),
    )

    # 生成环境变量模板（不写入真实密钥）
    _write_text_if_missing(
        project_path / ".env.example",
        "\n".join(
            [
                "# story2026 配置示例（复制为 .env 后填写）",
                "# 注意：请勿将包含真实 API_KEY 的 .env 提交到版本库。",
                "",
                "# Embedding",
                "EMBED_BASE_URL=https://api-inference.modelscope.cn/v1",
                "EMBED_MODEL=Qwen/Qwen3-Embedding-8B",
                "EMBED_API_KEY=",
                "",
                "# Rerank",
                "RERANK_BASE_URL=https://api.jina.ai/v1",
                "RERANK_MODEL=jina-reranker-v3",
                "RERANK_API_KEY=",
                "",
            ]
        )
        + "\n",
    )

    # Git 初始化（仅当项目目录内尚无 .git 且 Git 可用）
    git_dir = project_path / ".git"
    if not git_dir.exists():
        if not is_git_available():
            print("\n⚠️  Git 不可用，跳过版本控制初始化")
            print("💡 如需启用 Git 版本控制，请安装 Git: https://git-scm.com/")
        else:
            print("\nInitializing Git repository...")
            try:
                subprocess.run(["git", "init"], cwd=project_path, check=True, capture_output=True, text=True)

                gitignore_file = project_path / ".gitignore"
                if not gitignore_file.exists():
                    gitignore_file.write_text(
                        """# Python
__pycache__/
*.py[cod]
*.so

# Env (keep .env.example)
.env
.env.*
!.env.example

# Temporary files
*.tmp
*.bak
.DS_Store

# IDE
.vscode/
.idea/

# Don't ignore .webnovel (we need to track state.json)
# But ignore cache files
.webnovel/context_cache.json
.webnovel/*.lock
.webnovel/*.bak
""",
                        encoding="utf-8",
                    )

                subprocess.run(["git", "add", "."], cwd=project_path, check=True, capture_output=True)
                # 安全修复：清理 title 防止命令注入
                safe_title = sanitize_commit_message(title)
                subprocess.run(
                    ["git", "commit", "-m", f"初始化网文项目：{safe_title}"],
                    cwd=project_path,
                    check=True,
                    capture_output=True,
                )
                print("Git initialized.")
            except subprocess.CalledProcessError as e:
                print(f"Git init failed (non-fatal): {e}")

    # 记录工作区默认项目指针（非阻断）
    try:
        pointer_file = write_current_project_pointer(project_path)
        if pointer_file is not None:
            print(f"Default project pointer updated: {pointer_file}")
    except Exception as e:
        print(f"Default project pointer update failed (non-fatal): {e}")

    print(f"\nProject initialized at: {project_path}")
    print("Primary files:")
    print(" - STATE.json")
    print(" - TEAM.toml")
    print(" - CHANGELOG.md")
    print(" - .webnovel/state.json")
    print(" - .webnovel/workflow_state.json")
    print(" - .webnovel/execution_state.json")
    print(" - .webnovel/task_log.jsonl")
    print(" - .webnovel/tasks/")
    print(" - Init/north_star_contract.json")
    print(" - Init/初始化简报.json")
    print(" - Init/访谈摘要.md")
    print(" - Init/确认卡.md")
    print(" - .webnovel/idea_bank.json")
    print(" - Planning/8-全息地图/")
    print(" - Planning/legacy/总纲.md")
    print(" - Planning/legacy/爽点规划.md")
    print("No extra Init seed files are generated by default.")


def main() -> None:
    parser = argparse.ArgumentParser(description="网文项目初始化脚本（生成项目结构 + state.json + 基础模板）")
    parser.add_argument("project_dir", help="项目目录（建议 ./projects/<小说名>）")
    parser.add_argument("title", help="小说标题")
    parser.add_argument(
        "genre",
        help="题材类型（可用“+”组合，如：都市脑洞+规则怪谈；示例：修仙/系统流/都市异能/古言/现实题材）",
    )

    parser.add_argument("--init-mode", default="自主模式", help="初始化模式（智能顾问团模式/快速模式/自主模式）")
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

    # 初始化扩展字段（自主模式 / 快速模式 / 顾问团模式均可预填）
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
