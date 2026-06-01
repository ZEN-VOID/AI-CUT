#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
review_runner.py - story2026 review runtime baseline runner

用途：
- 为 `3-初稿` 的 inline validation hooks 提供第一版可执行自动 runner
- 为 `review` 的维度检查提供统一的本地规则基线
- 在终验阶段默认后台触发 `code-reviewer`，并把其结果并入聚合结论

说明：
- 当前版本是 rule-based baseline，不试图替代完整的子技能审读能力。
- 当上游 pack / context 无法完整装配时，runner 会降级为 manuscript-first 模式，
  仍尽量产出结构化结果与 sidecar 报告，而不是直接中断总线。
"""

from __future__ import annotations

import argparse
from difflib import SequenceMatcher
import json
import re
from pathlib import Path
import subprocess
import sys
import time
from typing import Any, Callable, Optional

from chapter_paths import drafting_root_md_path, find_chapter_file
from extract_chapter_context import build_chapter_context_payload
from project_locator import resolve_project_root
from runtime_compat import enable_windows_utf8_stdio, normalize_windows_path

try:
    import yaml
except ImportError:  # pragma: no cover
    yaml = None


ROLE_ID_TO_DIMENSION = {
    "structure-validator": "结构兑现",
    "continuity-validator": "连续性",
    "logic-validator": "逻辑自洽校验",
    "character-validator": "人物一致性",
    "timeline-validator": "时间线",
    "task-convergence-validator": "任务汇聚",
    "prose-style-validator": "文体读感",
}

CANONICAL_DRAFTING_STEPS = {
    "Step 1": ("1-单章叙事起盘", "单章叙事起盘"),
    "Step 2": ("2-节奏优化", "节奏优化"),
    "Step 3": ("3-场景和氛围渲染", "场景和氛围渲染"),
    "Step 4": ("4-角色形象刻画", "角色形象刻画"),
    "Step 5": ("5-对白优化", "对白优化"),
    "Step 6": ("6-心理活动描写", "心理活动描写"),
    "Step 7": ("7-追读力强化", "追读力强化"),
    "Step 8": ("8-润色", "润色"),
}

TIME_MARKER_ORDER = {
    "黎明": 1,
    "清晨": 2,
    "早晨": 3,
    "上午": 4,
    "中午": 5,
    "午后": 6,
    "傍晚": 7,
    "夜里": 8,
    "深夜": 9,
    "凌晨": 10,
}

CONTRIVANCE_MARKERS = (
    "突然",
    "莫名",
    "凭空",
    "无端",
    "无缘无故",
    "毫无征兆",
    "一下子",
    "瞬间就",
)

SUMMARYISH_PATTERNS = (
    r"^(首先|然后|接着|最后|总之|原来|实际上|本章|这一章|简单来说)",
    r"(总而言之|换句话说|事情的经过是)",
)

SCREENPLAY_RESIDUE_MARKERS = (
    "画面骤碎",
    "画面猛断",
    "镜头一转",
    "镜头猛然",
    "蒙太奇",
    "交叉闪现",
    "切回",
    "CUT TO",
)

META_RESIDUE_MARKERS = (
    "第几卷",
    "阶段",
    "节点",
    "时间压力落锁",
    "任务完成",
)

PROSE_SENSORY_ANCHOR_MARKERS = (
    "风",
    "雨",
    "雪",
    "雾",
    "光",
    "影",
    "灯",
    "声",
    "响",
    "气味",
    "腥",
    "潮",
    "冷",
    "热",
    "疼",
    "痛",
    "汗",
    "血",
    "尘",
    "泥",
    "木",
    "铁",
    "纸",
    "门",
    "窗",
    "墙",
    "石",
    "衣",
    "袖",
    "手",
    "指",
    "肩",
    "背",
    "脚",
    "呼吸",
    "喉",
    "视线",
    "步",
    "退",
    "停",
    "摸",
    "握",
    "攥",
    "碰",
    "压",
    "擦",
)

AI_FORMULA_MARKERS = (
    "总之",
    "换句话说",
    "不难看出",
    "这意味着",
    "可以说",
    "某种意义上",
    "事实上",
    "由此可见",
    "归根结底",
    "毋庸置疑",
)

EMOTION_TELLING_MARKERS = (
    "很愤怒",
    "非常愤怒",
    "感到愤怒",
    "很震惊",
    "感到震惊",
    "很害怕",
    "感到害怕",
    "很悲伤",
    "感到悲伤",
    "心中一惊",
    "心里一惊",
    "脸色大变",
    "脸色惨白",
    "脸色发白",
    "脸都白了",
    "脸红了",
    "脸白了",
    "脸绿了",
    "脸黄了",
    "吓得脸",
)

OUTLINE_HOOK_PATTERNS = (
    r"问题只剩一个",
    r"答案只剩一个",
    r"接下来(会)?发生什么[？?]",
    r"接下来又会如何[？?]",
    r"究竟会怎样[？?]",
)

EXPLANATION_DIALOGUE_MARKERS = (
    "其实是因为",
    "你要知道",
    "换句话说",
    "简单来说",
    "我之所以",
)

REQUIRED_FACT_PACK_SLICES = (
    "draft_snapshot",
    "cards_truth",
    "planning_truth",
    "init_truth",
    "runtime_context",
)

SEVERITY_ORDER = {
    "critical": 4,
    "high": 3,
    "medium": 2,
    "low": 1,
}

RISK_ORDER = {
    "low": 1,
    "medium": 2,
    "high": 3,
    "critical": 4,
}

CODE_REVIEWER_ROOT = Path("/Users/vincentlee/.codex/skills/meta/构建/架构/code-reviewer")
CODE_REVIEWER_CHECKER = CODE_REVIEWER_ROOT / "scripts" / "code_quality_checker.py"
CODE_REVIEWER_REPORTER = CODE_REVIEWER_ROOT / "scripts" / "review_report_generator.py"
CODE_REVIEWER_TIMEOUT_SECONDS = 60.0


def _registry_path() -> Path:
    return Path(__file__).resolve().parent.parent / "review" / "_shared" / "validation-dimension-registry.yaml"


def _load_registry() -> dict[str, Any]:
    if yaml is None:
        raise RuntimeError("PyYAML is required to load validation registry")
    path = _registry_path()
    if not path.is_file():
        raise FileNotFoundError(f"missing validation registry: {path}")
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    return data if isinstance(data, dict) else {}


def _role_spec(role_id: str) -> dict[str, Any]:
    registry = _load_registry()
    for item in registry.get("dimensions", []) or []:
        if str(item.get("role_id") or "") == role_id:
            return item if isinstance(item, dict) else {}
    raise KeyError(f"unknown validator role_id: {role_id}")


def _strip_markdown_frontmatter(text: str) -> str:
    if not text.startswith("---"):
        return text
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        return text
    for index in range(1, len(lines)):
        if lines[index].strip() == "---":
            return "\n".join(lines[index + 1 :]).lstrip()
    return text


def _manuscript_body_text(text: str) -> str:
    body = _strip_markdown_frontmatter(str(text or ""))
    lines = body.splitlines()
    if lines and lines[0].lstrip().startswith("#"):
        lines = lines[1:]
    return "\n".join(lines).strip()


def _parse_markdown_frontmatter(text: str) -> dict[str, str]:
    if not text.startswith("---"):
        return {}
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        return {}
    out: dict[str, str] = {}
    for index in range(1, len(lines)):
        line = lines[index]
        if line.strip() == "---":
            return out
        if ":" not in line:
            continue
        key, value = line.split(":", 1)
        normalized_key = key.strip()
        if not normalized_key:
            continue
        normalized_value = value.strip().strip('"').strip("'")
        if normalized_value:
            out[normalized_key] = normalized_value
    return out


def _final_acceptance_specs() -> list[dict[str, Any]]:
    registry = _load_registry()
    specs: list[dict[str, Any]] = []
    for item in registry.get("dimensions", []) or []:
        spec = item if isinstance(item, dict) else {}
        if bool(_safe_dict(spec.get("final_acceptance")).get("mandatory")):
            specs.append(spec)
    return specs


def _final_acceptance_role_ids() -> list[str]:
    return [str(spec.get("role_id") or "").strip() for spec in _final_acceptance_specs() if str(spec.get("role_id") or "").strip()]


def _aggregate_template_path() -> Path:
    return Path(__file__).resolve().parent.parent / "review" / "_shared" / "validation-aggregate.template.json"


def _load_aggregate_template() -> dict[str, Any]:
    path = _aggregate_template_path()
    if not path.is_file():
        return {}
    data = json.loads(path.read_text(encoding="utf-8"))
    return data if isinstance(data, dict) else {}


def _aggregate_output_ref(chapter_num: int) -> str:
    return f"review/第{chapter_num}章.validation.json"


def _aggregate_output_path(project_root: Path, chapter_num: int) -> Path:
    return project_root / _aggregate_output_ref(chapter_num)


def _resolve_project_root(raw: Optional[str]) -> Path:
    if raw:
        return resolve_project_root(str(Path(normalize_windows_path(raw)).resolve()))
    return resolve_project_root()


def _safe_int(value: Any, default: int = 0) -> int:
    try:
        return int(value)
    except Exception:
        return default


def _safe_dict(value: Any) -> dict[str, Any]:
    return value if isinstance(value, dict) else {}


def normalize_drafting_step_id(raw: Any) -> str | None:
    text = str(raw or "").strip()
    if not text:
        return None
    for canonical, aliases in CANONICAL_DRAFTING_STEPS.items():
        if text == canonical or text in aliases:
            return canonical
    return text


def _read_text_if_exists(path: Path) -> str:
    if not path.is_file():
        return ""
    return path.read_text(encoding="utf-8")


def _previous_manuscript_path(project_root: Path, chapter_num: int) -> Optional[Path]:
    if chapter_num <= 1:
        return None
    path = find_chapter_file(project_root, chapter_num - 1)
    return path if path and path.is_file() else None


def _fact_pack_missing_slices(raw_fact_pack: dict[str, Any]) -> list[str]:
    return [slice_name for slice_name in REQUIRED_FACT_PACK_SLICES if not _safe_dict(raw_fact_pack.get(slice_name))]


def _derive_fact_pack_views(raw_fact_pack: dict[str, Any]) -> dict[str, Any]:
    draft_snapshot = _safe_dict(raw_fact_pack.get("draft_snapshot"))
    cards_truth = _safe_dict(raw_fact_pack.get("cards_truth"))
    planning_truth = _safe_dict(raw_fact_pack.get("planning_truth"))
    init_truth = _safe_dict(raw_fact_pack.get("init_truth"))
    runtime_context = _safe_dict(raw_fact_pack.get("runtime_context"))

    promise_slice = _safe_dict(planning_truth.get("promise_slice"))
    if not promise_slice and init_truth:
        promise_slice = {
            "project_preferences": _safe_dict(init_truth.get("project_preferences")),
            "style_contract_ref": str(init_truth.get("style_contract_ref") or "").strip(),
            "global_contract_refs": list(init_truth.get("global_contract_refs") or []),
            "genre": str(_safe_dict(init_truth.get("genre_profile")).get("genre") or "").strip(),
        }
    chapter_planning_packet = _safe_dict(planning_truth.get("chapter_planning_packet"))
    if not chapter_planning_packet:
        packets = planning_truth.get("chapter_planning_packets")
        if isinstance(packets, list) and packets:
            chapter_planning_packet = _safe_dict(packets[0])
    if not chapter_planning_packet:
        chapter_planning_packet = _safe_dict(planning_truth.get("chapter_board"))

    return {
        "draft_snapshot": draft_snapshot,
        "cards_truth": cards_truth,
        "planning_truth": planning_truth,
        "init_truth": init_truth,
        "runtime_context": runtime_context,
        "promise_slice": promise_slice,
        "volume_planning_summary": _safe_dict(planning_truth.get("volume_planning_summary")),
        "chapter_planning_packet": chapter_planning_packet,
        "chapter_board": _safe_dict(planning_truth.get("chapter_board")),
        "episode_rhythm_handoff": _safe_dict(planning_truth.get("episode_rhythm_handoff")),
        "cards_state_history_slice": _safe_dict(cards_truth.get("cards_state_history_slice")),
        "foreshadow_silence_slice": _safe_dict(planning_truth.get("foreshadow_silence_slice")),
        "style_gate": _safe_dict(runtime_context.get("style_gate")),
        "global_truth_slice": _safe_dict(cards_truth.get("global_truth_slice")),
    }


def _build_runtime_context(project_root: Path, chapter_num: int, current_step_id: str | None = None) -> dict[str, Any]:
    manuscript_path = find_chapter_file(project_root, chapter_num) or drafting_root_md_path(project_root, chapter_num)
    previous_path = _previous_manuscript_path(project_root, chapter_num)

    manuscript_text = _read_text_if_exists(manuscript_path)
    previous_text = _read_text_if_exists(previous_path) if previous_path else ""

    context_payload: dict[str, Any] = {}
    warnings: list[str] = []
    try:
        context_payload = build_chapter_context_payload(
            project_root,
            chapter_num,
            current_step_id=current_step_id,
        )
    except Exception as exc:  # pragma: no cover - exercised via fallback
        warnings.append(f"context_payload_fallback:{exc.__class__.__name__}")

    fact_pack = context_payload.get("validation_fact_pack", {}) if isinstance(context_payload, dict) else {}
    if not isinstance(fact_pack, dict):
        fact_pack = {}
    missing_slices = _fact_pack_missing_slices(fact_pack)
    if missing_slices:
        warnings.append("missing_fact_pack_slices:" + ",".join(missing_slices))

    return {
        "project_root": project_root,
        "chapter": chapter_num,
        "current_step_id": normalize_drafting_step_id(current_step_id),
        "manuscript_path": manuscript_path,
        "manuscript_text": manuscript_text,
        "previous_manuscript_path": previous_path,
        "previous_manuscript_text": previous_text,
        "context_payload": context_payload,
        "raw_fact_pack": fact_pack,
        "fact_pack_missing_slices": missing_slices,
        "fact_pack": _derive_fact_pack_views(fact_pack),
        "warnings": warnings,
    }


def _paragraphs(text: str) -> list[str]:
    return [row.strip() for row in re.split(r"\n{1,}|(?<=。)|(?<=！)|(?<=？)", text) if row.strip()]


def _dialogue_lines(text: str) -> list[str]:
    lines = re.findall(r"[“\"]([^”\"]{2,120})[”\"]", text)
    return [row.strip() for row in lines if row.strip()]


def _paragraph_blocks(text: str) -> list[str]:
    return [row.strip() for row in re.split(r"\n\s*\n", str(text or "")) if row.strip()]


def _marker_hits(text: str, markers: tuple[str, ...]) -> int:
    return sum(str(text or "").count(marker) for marker in markers)


def _sentence_rhythm_flattening_score(rows: list[str]) -> int:
    lengths = [len(_normalize_match_text(row)) for row in rows if len(_normalize_match_text(row)) >= 8]
    if len(lengths) < 10:
        return 0
    mean = sum(lengths) / len(lengths)
    if mean <= 0:
        return 0
    variance = sum((length - mean) ** 2 for length in lengths) / len(lengths)
    coefficient = (variance ** 0.5) / mean
    if coefficient < 0.28:
        return 2
    if coefficient < 0.38:
        return 1
    return 0


def _keyword_candidates(raw: Any) -> list[str]:
    if isinstance(raw, str):
        candidates = re.split(r"[，,、；;：:\s/|]+", raw)
    elif isinstance(raw, list):
        candidates = []
        for item in raw:
            candidates.extend(_keyword_candidates(item))
    elif isinstance(raw, dict):
        candidates = []
        for value in raw.values():
            candidates.extend(_keyword_candidates(value))
    else:
        candidates = []
    return [item.strip() for item in candidates if isinstance(item, str) and len(item.strip()) >= 2]


def _normalize_match_text(text: str) -> str:
    return re.sub(r"[^\u4e00-\u9fffA-Za-z0-9]", "", str(text or ""))


def _has_similar_sentence(text: str, candidate: str) -> bool:
    normalized_candidate = _normalize_match_text(candidate)
    if len(normalized_candidate) < 8:
        return False

    for row in _paragraphs(text):
        normalized_row = _normalize_match_text(row)
        if len(normalized_row) < 8:
            continue
        ratio = SequenceMatcher(None, normalized_candidate, normalized_row).ratio()
        if ratio >= 0.5:
            return True
    return False


def _text_contains_candidate(text: str, candidate: str) -> bool:
    if candidate and candidate in text:
        return True
    keywords = [word for word in _keyword_candidates(candidate) if len(word) >= 2]
    if keywords:
        hits = sum(1 for word in keywords if word in text)
        if hits >= min(2, len(keywords)):
            return True
    return _has_similar_sentence(text, candidate)


def _text_list(value: Any) -> list[str]:
    items: list[str] = []
    if isinstance(value, str):
        raw = value.strip()
        if raw:
            parts = [segment.strip(" -") for segment in re.split(r"(?:\n+|；|;)", raw) if segment.strip(" -")]
            items.extend(parts or [raw])
    elif isinstance(value, list):
        for item in value:
            items.extend(_text_list(item))
    elif isinstance(value, dict):
        for item in value.values():
            items.extend(_text_list(item))
    unique: list[str] = []
    seen: set[str] = set()
    for item in items:
        if item and item not in seen:
            unique.append(item)
            seen.add(item)
    return unique


def _relation_sources(raw: dict[str, Any]) -> list[dict[str, Any]]:
    sources = [raw]
    for key in ("task_relation", "task_lineage", "task_convergence", "任务关系", "任务从属", "任务汇聚"):
        nested = _safe_dict(raw.get(key))
        if nested:
            sources.append(nested)
    return sources


def _pick_task_values(sources: list[dict[str, Any]], *keys: str) -> list[str]:
    for source in sources:
        for key in keys:
            values = _text_list(source.get(key))
            if values:
                return values
    return []


def _pick_task_scalar(sources: list[dict[str, Any]], *keys: str) -> str:
    values = _pick_task_values(sources, *keys)
    return values[0] if values else ""


def _task_related(lhs: str, rhs: str) -> bool:
    left = str(lhs or "").strip()
    right = str(rhs or "").strip()
    if not left or not right:
        return False
    if left in right or right in left:
        return True
    left_keywords = set(_keyword_candidates(left))
    right_keywords = set(_keyword_candidates(right))
    return bool(left_keywords and right_keywords and left_keywords.intersection(right_keywords))


def _extract_task_relation(
    raw: dict[str, Any],
    *,
    upstream_keys: tuple[str, ...],
    main_keys: tuple[str, ...],
    branch_keys: tuple[str, ...],
    merge_keys: tuple[str, ...],
    open_keys: tuple[str, ...],
    fallback_main: list[str] | None = None,
    fallback_branches: list[str] | None = None,
    fallback_merge: list[str] | None = None,
    fallback_open: list[str] | None = None,
) -> dict[str, Any]:
    sources = _relation_sources(_safe_dict(raw))
    main_tasks = _pick_task_values(sources, *main_keys) or [item for item in (fallback_main or []) if str(item).strip()]
    branch_tasks = _pick_task_values(sources, *branch_keys) or [item for item in (fallback_branches or []) if str(item).strip()]
    merge_targets = _pick_task_values(sources, *merge_keys) or [item for item in (fallback_merge or []) if str(item).strip()]
    open_routes = _pick_task_values(sources, *open_keys) or [item for item in (fallback_open or []) if str(item).strip() and str(item).strip() != "无"]
    return {
        "upstream_task": _pick_task_scalar(sources, *upstream_keys),
        "main_tasks": main_tasks,
        "branch_tasks": branch_tasks,
        "merge_targets": merge_targets,
        "open_routes": open_routes,
    }


def _clamp_score(score: float) -> int:
    return max(0, min(100, int(round(score))))


def _screenplay_residue_stats(text: str, entity_candidates: list[str]) -> dict[str, Any]:
    marker_hits = sum(text.count(marker) for marker in SCREENPLAY_RESIDUE_MARKERS)
    tag_like_paragraphs = 0
    tag_examples: list[str] = []
    blocks = _paragraph_blocks(text)
    entity_set = {str(item).strip() for item in entity_candidates if str(item).strip()}

    for index, block in enumerate(blocks):
        plain = block.strip()
        if len(plain) > 8 or "“" in plain or any(ch in plain for ch in "，；：、"):
            continue
        bare = plain.rstrip("。！？!?. ")
        if len(bare) < 2 or len(bare) > 6:
            continue
        if entity_set and bare not in entity_set and not re.fullmatch(r"[\u4e00-\u9fffA-Za-z]{2,6}", bare):
            continue
        prev_len = len(blocks[index - 1]) if index > 0 else 0
        next_len = len(blocks[index + 1]) if index + 1 < len(blocks) else 0
        if max(prev_len, next_len) < 16:
            continue
        tag_like_paragraphs += 1
        if plain not in tag_examples:
            tag_examples.append(plain)

    return {
        "marker_hits": marker_hits,
        "tag_like_paragraphs": tag_like_paragraphs,
        "examples": tag_examples[:3],
    }


def _severity_counts(issues: list[dict[str, Any]]) -> dict[str, int]:
    counts = {"critical": 0, "high": 0, "medium": 0, "low": 0}
    for issue in issues:
        severity = str(issue.get("severity") or "low")
        if severity in counts:
            counts[severity] += 1
    return counts


def _merge_severity_counts(values: list[dict[str, int]]) -> dict[str, int]:
    merged = {"critical": 0, "high": 0, "medium": 0, "low": 0}
    for counts in values:
        for key in merged:
            merged[key] += _safe_int(_safe_dict(counts).get(key), 0)
    return merged


def _max_risk(*values: Any) -> str:
    best = "low"
    for raw in values:
        value = str(raw or "").strip().lower()
        if value in RISK_ORDER and RISK_ORDER[value] > RISK_ORDER[best]:
            best = value
    return best


def _covenant_issues(ctx: dict[str, Any], *, role_id: str = "context-agent") -> list[dict[str, Any]]:
    chapter = _safe_int(ctx.get("chapter"), 0)
    issues: list[dict[str, Any]] = []
    owner_map = {
        "draft_snapshot": "3-初稿",
        "cards_truth": "1-设定",
        "planning_truth": "2-卷章",
        "init_truth": "0-初始化",
        "runtime_context": "STATE",
    }
    for idx, slice_name in enumerate(ctx.get("fact_pack_missing_slices") or [], start=1):
        issues.append(
            _issue(
                role_id=role_id,
                chapter=chapter,
                index=idx,
                issue_type="验收契约",
                severity="critical",
                location=f"validation_fact_pack.{slice_name}",
                description=f"终验统一事实包缺少必需 slice：{slice_name}",
                suggestion="先修 pack producer 与上游 truth 装配，再重新进入 validation。",
                rework_target_step="source-contract-fix",
                source_layer_owner=owner_map.get(str(slice_name), "review"),
                can_override=False,
            )
        )
    return issues


def _runtime_issue(chapter: int, role_id: str, exc: Exception, index: int) -> dict[str, Any]:
    return _issue(
        role_id=role_id,
        chapter=chapter,
        index=index,
        issue_type="运行时失败",
        severity="critical",
        location=f"{role_id}.runtime",
        description=f"{role_id} 在终验过程中抛出 {exc.__class__.__name__}",
        suggestion="先修复 validator runtime，再重新执行终验聚合。",
        rework_target_step="source-contract-fix",
        source_layer_owner="review",
        can_override=False,
    )


def _issue(
    *,
    role_id: str,
    chapter: int,
    index: int,
    issue_type: str,
    severity: str,
    location: str,
    description: str,
    suggestion: str,
    rework_target_step: str,
    source_layer_owner: str = "3-初稿",
    can_override: Optional[bool] = None,
) -> dict[str, Any]:
    prefix = role_id.replace("-validator", "").replace("-", "_").upper()
    if can_override is None:
        can_override = severity in {"medium", "low"}
    return {
        "id": f"{prefix}-{chapter:03d}-{index:02d}",
        "type": issue_type,
        "severity": severity,
        "location": location,
        "description": description,
        "suggestion": suggestion,
        "can_override": bool(can_override),
        "rework_target_step": rework_target_step,
        "source_layer_owner": source_layer_owner,
    }


def _report_ref(chapter: int, role_id: str, report_filename: str) -> str:
    return f"review/第{chapter}章/{report_filename or ROLE_ID_TO_DIMENSION.get(role_id, role_id + '.md')}"


def _write_report(
    *,
    project_root: Path,
    chapter: int,
    role_id: str,
    dimension_label: str,
    report_filename: str,
    result: dict[str, Any],
    manuscript_path: Path,
    warnings: list[str],
) -> str:
    relative_ref = _report_ref(chapter, role_id, report_filename)
    absolute_path = project_root / relative_ref
    absolute_path.parent.mkdir(parents=True, exist_ok=True)

    issues = result.get("issues", []) or []
    severity_counts = result.get("severity_counts", {}) or {}
    metrics = result.get("metrics", {}) or {}
    lines = [
        f"# 第{chapter}章 {dimension_label} 验收报告",
        "",
        "## 维度结论",
        "",
        f"- `role_id`: {role_id}",
        f"- `validation_context`: {result.get('validation_context')}",
        f"- `pass`: {result.get('pass')}",
        f"- `overall_score`: {result.get('overall_score')}",
        f"- `summary`: {result.get('summary')}",
        "",
        "## 关键问题",
        "",
    ]
    if issues:
        for issue in issues:
            lines.append(
                "- "
                + " / ".join(
                    [
                        str(issue.get("id") or ""),
                        str(issue.get("severity") or ""),
                        str(issue.get("location") or ""),
                        str(issue.get("description") or ""),
                        str(issue.get("suggestion") or ""),
                        str(issue.get("rework_target_step") or ""),
                        str(issue.get("source_layer_owner") or ""),
                    ]
                )
            )
    else:
        lines.append("- 无 blocking issue")
    lines.extend(
        [
            "",
            "## 维度指标",
            "",
            "```json",
            json.dumps(metrics, ensure_ascii=False, indent=2),
            "```",
            "",
            "## 严重度汇总",
            "",
            "```json",
            json.dumps(severity_counts, ensure_ascii=False, indent=2),
            "```",
            "",
            "## 证据回指",
            "",
            f"- `manuscript_ref`: {manuscript_path.relative_to(project_root) if manuscript_path.is_absolute() else manuscript_path}",
            f"- `report_ref`: {relative_ref}",
        ]
    )
    if warnings:
        lines.extend(["", "## Runtime Warnings", ""])
        lines.extend([f"- {item}" for item in warnings])

    absolute_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return relative_ref


def _run_structure(ctx: dict[str, Any], role_id: str, spec: dict[str, Any], validation_context: str) -> dict[str, Any]:
    chapter = ctx["chapter"]
    text = str(ctx["manuscript_text"] or "")
    chapter_board = ctx["fact_pack"]["chapter_board"]
    cards_slice = ctx["fact_pack"]["cards_state_history_slice"]
    current_step_id = normalize_drafting_step_id(ctx.get("current_step_id"))
    obligations = []
    obligations.extend(chapter_board.get("chapter_goals", []) or [])
    obligations.extend(chapter_board.get("must_happen", []) or [])
    obligations = [item for item in obligations if item]
    checked_obligations = obligations[:6]
    beat_checkpoints = [str(item).strip() for item in (chapter_board.get("beat_checkpoints") or []) if str(item).strip()]
    terminal_beat = str(chapter_board.get("terminal_beat") or "").strip()
    bundled_entities = [str(item).strip() for item in ((_safe_dict(chapter_board.get("bundled_elements")).get("characters") or [])) if str(item).strip()]
    recent_entities = [str(item).strip() for item in (cards_slice.get("recent_entities") or []) if str(item).strip()]
    entity_candidates = list(dict.fromkeys([*bundled_entities, *recent_entities]))

    issues: list[dict[str, Any]] = []
    hits = 0
    for item in checked_obligations:
        if _text_contains_candidate(text, str(item)):
            hits += 1
            continue
        issues.append(
            _issue(
                role_id=role_id,
                chapter=chapter,
                index=len(issues) + 1,
                issue_type="结构兑现",
                severity="high" if validation_context == "final_acceptance" else "medium",
                location=f"第{chapter}章正文",
                description=f"规划义务未在正文中找到足够证据：{item}",
                suggestion="回到起盘或追读力强化，把该义务写成可感知的场面、局部兑现与续读牵引。",
                rework_target_step="1-单章叙事起盘",
            )
        )

    paragraphs = _paragraphs(text)
    summary_hits = sum(1 for row in paragraphs if any(re.search(pattern, row) for pattern in SUMMARYISH_PATTERNS))
    if summary_hits >= 3:
        issues.append(
            _issue(
                role_id=role_id,
                chapter=chapter,
                index=len(issues) + 1,
                issue_type="结构兑现",
                severity="medium",
                location=f"第{chapter}章正文段落层",
                description="说明腔/总结腔偏多，结构更像提纲复述而不是戏剧场面。",
                suggestion="减少摘要式解释，补足动作、冲突和即时反馈。",
                rework_target_step="7-追读力强化",
            )
        )

    beat_hits = sum(1 for item in beat_checkpoints if _text_contains_candidate(text, item))
    if len(beat_checkpoints) >= 3 and beat_hits < len(beat_checkpoints) - 1:
        issues.append(
            _issue(
                role_id=role_id,
                chapter=chapter,
                index=len(issues) + 1,
                issue_type="结构兑现",
                severity="high" if validation_context == "final_acceptance" else "medium",
                location=f"第{chapter}章 beat coverage",
                description="本章承诺的关键 beat 覆盖不足，正文只落了前半段或中段，尚未真正抵达 chapter board 承诺的终端碰撞。",
                suggestion="回到起盘，至少把开场局面、局势改向和当前章承诺的终端碰撞都写入正式正文。",
                rework_target_step="1-单章叙事起盘",
            )
        )

    terminal_beat_hit = bool(terminal_beat) and _text_contains_candidate(text, terminal_beat)
    if terminal_beat and not terminal_beat_hit:
        issues.append(
            _issue(
                role_id=role_id,
                chapter=chapter,
                index=len(issues) + 1,
                issue_type="结构兑现",
                severity="medium",
                location=f"第{chapter}章终端承诺",
                description=f"本章终端承诺尚未真正落地：{terminal_beat}",
                suggestion="回到起盘，把当前章 promised collision 写成场面，而不是停在前置铺垫。",
                rework_target_step="1-单章叙事起盘",
            )
        )

    screenplay_stats = _screenplay_residue_stats(text, entity_candidates)
    screenplay_hits = _safe_int(screenplay_stats.get("marker_hits"), 0) + _safe_int(screenplay_stats.get("tag_like_paragraphs"), 0)
    if screenplay_hits >= 2:
        residue_examples = " / ".join(screenplay_stats.get("examples") or [])
        issues.append(
            _issue(
                role_id=role_id,
                chapter=chapter,
                index=len(issues) + 1,
                issue_type="结构兑现",
                severity="medium",
                location=f"第{chapter}章 prose 句法层",
                description="正文残留明显影视分镜语法或角色报幕段，仍像脚本/分镜中间态而不是小说句法。"
                + (f" 例：{residue_examples}" if residue_examples else ""),
                suggestion="把镜头切换词和角色报幕段改成物象、动作、声音或人物感知过渡。",
                rework_target_step="1-单章叙事起盘" if current_step_id == "Step 1" else "8-润色",
            )
        )

    meta_residue_hits = sum(text.count(marker) for marker in META_RESIDUE_MARKERS)
    if meta_residue_hits:
        issues.append(
            _issue(
                role_id=role_id,
                chapter=chapter,
                index=len(issues) + 1,
                issue_type="结构兑现",
                severity="medium",
                location=f"第{chapter}章破次元术语层",
                description="正文仍残留规划/工作流层 meta 术语，破坏戏内沉浸。",
                suggestion="把外部术语翻译成人物能感觉到的风险、余波、局势或预感。",
                rework_target_step="8-润色",
            )
        )

    outline_hook_hits = sum(1 for row in paragraphs if any(re.search(pattern, row) for pattern in OUTLINE_HOOK_PATTERNS))
    if outline_hook_hits:
        issues.append(
            _issue(
                role_id=role_id,
                chapter=chapter,
                index=len(issues) + 1,
                issue_type="结构兑现",
                severity="medium",
                location=f"第{chapter}章章末 hook",
                description="章末存在明显提纲式发问，像作者替故事点题，而不是故事自己把麻烦推近。",
                suggestion="把尾问改成危险逼近、余波未平、消息将到或脚步声临近的戏内收束。",
                rework_target_step="8-润色",
            )
        )

    score = _clamp_score(
        92
        - (len(checked_obligations) - hits) * 18
        - summary_hits * 5
        - max(0, len(beat_checkpoints) - beat_hits) * 4
        - screenplay_hits * 4
        - meta_residue_hits * 4
        - outline_hook_hits * 6
    )
    return {
        "overall_score": score,
        "pass": len(issues) == 0,
        "issues": issues,
        "metrics": {
            "required_events_hit": hits,
            "missed_obligations": max(0, len(checked_obligations) - hits),
            "promise_breaks": 0 if len(issues) == 0 else min(1, len(issues)),
            "undramatized_exposition_hits": summary_hits,
            "beat_checkpoints": len(beat_checkpoints),
            "beat_hits": beat_hits,
            "terminal_beat_hit": terminal_beat_hit,
            "screenplay_residue_hits": screenplay_hits,
            "meta_residue_hits": meta_residue_hits,
            "outline_hook_hits": outline_hook_hits,
            "anti_ai_force_check": "fail" if summary_hits >= 3 else "pass",
            "cold_commentary_risk": "high" if summary_hits >= 3 or screenplay_hits >= 2 else ("medium" if meta_residue_hits or outline_hook_hits else "low"),
        },
        "summary": "结构义务已基本兑现。" if len(issues) == 0 else "存在结构兑现缺口或摘要式假兑现。",
    }


def _run_continuity(ctx: dict[str, Any], role_id: str, spec: dict[str, Any], validation_context: str) -> dict[str, Any]:
    chapter = ctx["chapter"]
    text = _strip_markdown_frontmatter(str(ctx["manuscript_text"] or ""))
    previous_text = _strip_markdown_frontmatter(str(ctx["previous_manuscript_text"] or ""))
    cards_slice = ctx["fact_pack"]["cards_state_history_slice"]
    recent_entities = [str(item) for item in cards_slice.get("recent_entities", []) if str(item).strip()]

    issues: list[dict[str, Any]] = []
    intro = text[:280]
    if chapter > 1 and previous_text:
        carries_transition = any(token in intro for token in ("仍", "还", "又", "再", "次日", "第二天", "与此同时", "这时", "此刻"))
        carries_entity = any(entity and entity in intro for entity in recent_entities[:4])
        if not carries_transition and not carries_entity:
            issues.append(
                _issue(
                    role_id=role_id,
                    chapter=chapter,
                    index=len(issues) + 1,
                    issue_type="连续性",
                    severity="medium",
                    location=f"第{chapter}章开头",
                    description="本章开场缺少明显承接信号，像重新起一章而不是延续上一章停点。",
                    suggestion="在前几段补上情绪/动作/信息承接锚点。",
                    rework_target_step="1-单章叙事起盘",
                )
            )

    if recent_entities and not any(entity in text for entity in recent_entities[:4]):
        issues.append(
            _issue(
                role_id=role_id,
                chapter=chapter,
                index=len(issues) + 1,
                issue_type="连续性",
                severity="low",
                location=f"第{chapter}章全文",
                description="近期活跃实体没有在当前章得到明确承接，线程连续性偏弱。",
                suggestion="至少让关键实体/线程在当前章获得一次显性回指。",
                rework_target_step="2-节奏优化",
            )
        )

    score = _clamp_score(90 - len(issues) * 18)
    return {
        "overall_score": score,
        "pass": len(issues) == 0,
        "issues": issues,
        "metrics": {
            "previous_episode_bridge": "strong" if chapter <= 1 or len(issues) == 0 else "weak",
            "transition_breaks": 1 if issues else 0,
            "thread_drop_count": sum(1 for item in issues if item.get("rework_target_step") == "2-节奏优化"),
            "carryover_gaps": len(issues),
        },
        "summary": "连续性承接正常。" if len(issues) == 0 else "存在开场承接或线程连续性偏弱的问题。",
    }


def _run_logic(ctx: dict[str, Any], role_id: str, spec: dict[str, Any], validation_context: str) -> dict[str, Any]:
    chapter = ctx["chapter"]
    text = str(ctx["manuscript_text"] or "")
    fact_pack = _safe_dict(ctx.get("fact_pack"))
    cards_slice = _safe_dict(fact_pack.get("cards_state_history_slice"))
    cards_truth = _safe_dict(fact_pack.get("cards_truth"))
    planning_truth = _safe_dict(fact_pack.get("planning_truth"))
    init_truth = _safe_dict(fact_pack.get("init_truth"))
    global_truth = _safe_dict(fact_pack.get("global_truth_slice"))
    global_summary = _safe_dict(global_truth.get("global_contract_summary"))
    chapter_board = _safe_dict(fact_pack.get("chapter_board"))
    current_location = str(cards_slice.get("current_location") or "").strip()
    contrivance_hits = sum(text.count(marker) for marker in CONTRIVANCE_MARKERS)
    recent_state_changes = [str(item) for item in (cards_slice.get("recent_state_changes") or []) if str(item).strip()]
    rule_system = global_summary.get("rule_system") or []
    rule_text = " ".join(
        str(
            _safe_dict(item).get("value")
            or _safe_dict(item).get("label")
            or item
        )
        for item in rule_system
    )
    golden_finger = _safe_dict(global_summary.get("golden_finger"))
    golden_finger_name = str(golden_finger.get("name") or "").strip()
    golden_finger_limits = [str(item) for item in (golden_finger.get("limits") or []) if str(item).strip()]
    cannot_change = [str(item) for item in (chapter_board.get("cannot_change") or []) if str(item).strip()]
    exception_tokens = ("越级", "禁术", "破例", "强开", "透支", "系统", "作弊")
    cost_tokens = ("代价", "反噬", "损耗", "后遗症", "负担", "受伤", "崩裂", "失控")
    no_limit_tokens = ("毫无代价", "毫发无伤", "不受限制", "无限", "随意", "轻易", "完全无视")

    issues: list[dict[str, Any]] = []
    if current_location and current_location not in text:
        issues.append(
            _issue(
                role_id=role_id,
                chapter=chapter,
                index=len(issues) + 1,
                issue_type="逻辑自洽校验",
                severity="medium",
                location=f"第{chapter}章场景层",
                description=f"当前态位置 `{current_location}` 未在正文中获得稳定锚定，状态连续性不足。",
                suggestion="补足位置/状态锚，避免读者失去空间与行动依据。",
                rework_target_step="1-单章叙事起盘",
            )
        )

    state_change_misses = [item for item in recent_state_changes[:3] if item not in text]
    if state_change_misses:
        issues.append(
            _issue(
                role_id=role_id,
                chapter=chapter,
                index=len(issues) + 1,
                issue_type="逻辑自洽校验",
                severity="medium",
                location=f"第{chapter}章状态层",
                description=f"近期对象状态变更未在正文中得到承接：{state_change_misses[0]}",
                suggestion="补上状态延续或明确说明为什么当前状态已变化。",
                rework_target_step="1-单章叙事起盘",
            )
        )

    explicit_no_cost = any(token in text for token in no_limit_tokens)
    if ("代价" in rule_text or "限制" in rule_text) and any(token in text for token in exception_tokens) and (explicit_no_cost or not any(token in text for token in cost_tokens)):
        issues.append(
            _issue(
                role_id=role_id,
                chapter=chapter,
                index=len(issues) + 1,
                issue_type="逻辑自洽校验",
                severity="high" if validation_context == "final_acceptance" else "medium",
                location=f"第{chapter}章世界规则层",
                description="上游真源已声明规则存在代价/限制，但正文在触发破例动作时没有体现对应成本。",
                suggestion="补足触发条件、代价或先例解释；若上游规则本身冲突，改走 source-contract 修复。",
                rework_target_step="1-单章叙事起盘",
                source_layer_owner="1-设定",
            )
        )

    if golden_finger_name and golden_finger_name in text and golden_finger_limits and any(token in text for token in no_limit_tokens):
        issues.append(
            _issue(
                role_id=role_id,
                chapter=chapter,
                index=len(issues) + 1,
                issue_type="逻辑自洽校验",
                severity="medium",
                location=f"第{chapter}章能力边界层",
                description=f"`{golden_finger_name}` 在上游真源中带有限制，但正文把它写成了近乎无上限能力。",
                suggestion="把能力使用改回限制内，或明确补写限制失效的条件与代价。",
                rework_target_step="1-单章叙事起盘",
                source_layer_owner="0-初始化",
            )
        )

    if cannot_change:
        misses = [item for item in cannot_change[:3] if item not in text]
        if misses:
            issues.append(
                _issue(
                    role_id=role_id,
                    chapter=chapter,
                    index=len(issues) + 1,
                    issue_type="逻辑自洽校验",
                    severity="medium",
                    location=f"第{chapter}章规划约束层",
                    description=f"planning truth 声明了本章不可擅自改写的约束，但正文没有给出清晰锚点：{misses[0]}",
                    suggestion="补上对应约束的存在感；若 planning 约束已过期或自相矛盾，回到 `2-卷章` 修源。",
                    rework_target_step="source-contract-fix",
                    source_layer_owner="2-卷章",
                )
            )

    if contrivance_hits >= 3:
        issues.append(
            _issue(
                role_id=role_id,
                chapter=chapter,
                index=len(issues) + 1,
                issue_type="逻辑自洽校验",
                severity="high",
                location=f"第{chapter}章因果链",
                description="文本中出现过多强行转折/凭空推进标记，因果链有拼接感。",
                suggestion="回到起盘，重写触发条件、过程与代价，让事件自然发生。",
                rework_target_step="1-单章叙事起盘",
            )
        )

    world_rule_conflicts = sum(
        1
        for issue in issues
        if str(issue.get("source_layer_owner") or "") in {"0-初始化", "1-设定"}
    )
    capability_conflicts = sum(
        1
        for issue in issues
        if "能力边界" in str(issue.get("location") or "")
    )
    exception_cost_gaps = 1 if any(token in text for token in exception_tokens) and (explicit_no_cost or not any(token in text for token in cost_tokens)) else 0
    social_ecology_conflicts = sum(
        1
        for issue in issues
        if str(issue.get("source_layer_owner") or "") == "2-卷章"
    )
    score = _clamp_score(91 - len(issues) * 18 - contrivance_hits * 3)
    return {
        "overall_score": score,
        "pass": len(issues) == 0,
        "issues": issues,
        "metrics": {
            "cause_effect_breaks": 1 if contrivance_hits >= 3 else 0,
            "state_conflicts": int(bool((current_location and current_location not in text) or state_change_misses)),
            "capability_conflicts": capability_conflicts,
            "world_rule_conflicts": world_rule_conflicts,
            "exception_cost_gaps": exception_cost_gaps,
            "social_ecology_conflicts": social_ecology_conflicts,
            "contrivance_risk": "high" if contrivance_hits >= 3 else ("medium" if contrivance_hits >= 1 else "low"),
        },
        "summary": "逻辑与设定链条基本自洽。" if len(issues) == 0 else "存在状态锚不足、设定破例未受约束或强行推进的逻辑风险。",
    }


def _run_character(ctx: dict[str, Any], role_id: str, spec: dict[str, Any], validation_context: str) -> dict[str, Any]:
    chapter = ctx["chapter"]
    text = str(ctx["manuscript_text"] or "")
    current_step_id = normalize_drafting_step_id(ctx.get("current_step_id"))
    dialogue = _dialogue_lines(text)
    cards_slice = ctx["fact_pack"]["cards_state_history_slice"]
    recent_entities = [str(item) for item in (cards_slice.get("recent_entities", []) or []) if str(item).strip()]
    growth_snapshot = _safe_dict(cards_slice.get("protagonist_growth_snapshot"))

    issues: list[dict[str, Any]] = []
    speech_violations = sum(
        1
        for line in dialogue
        if len(line) >= 55 or any(marker in line for marker in EXPLANATION_DIALOGUE_MARKERS)
    )
    should_block_speech = validation_context == "final_acceptance" or current_step_id in {"Step 5", "Step 6", "Step 8", ""}
    deferred_speech_to_step5 = validation_context == "drafting_inline" and current_step_id == "Step 4" and speech_violations >= 2

    if speech_violations >= 2 and should_block_speech:
        issues.append(
            _issue(
                role_id=role_id,
                chapter=chapter,
                index=len(issues) + 1,
                issue_type="人物一致性",
                severity="medium",
                location=f"第{chapter}章对白层",
                description="对白偏长或解释性过强，角色声口区分度不足。",
                suggestion="回到对白优化，压缩解释，改成更像角色本人会说的话。",
                rework_target_step="5-对白优化",
            )
        )

    if recent_entities and not any(entity in text for entity in recent_entities[:3]):
        issues.append(
            _issue(
                role_id=role_id,
                chapter=chapter,
                index=len(issues) + 1,
                issue_type="人物一致性",
                severity="low",
                location=f"第{chapter}章人物层",
                description="近期关键人物缺少显性出场或回指，人物连续性偏弱。",
                suggestion="回到角色刻画，补足关键人物的动作、反应或关系压力。",
                rework_target_step="4-角色形象刻画",
            )
        )

    growth_continuity_checked = bool(growth_snapshot.get("growth_enabled"))
    growth_signal_hits = 0
    if growth_continuity_checked:
        protagonist_name = str(growth_snapshot.get("character_name") or "").strip()
        carry_signals = [str(item) for item in (growth_snapshot.get("carry_signals") or []) if str(item).strip()]
        if protagonist_name and protagonist_name in text and carry_signals:
            growth_signal_hits = sum(1 for signal in carry_signals[:4] if signal in text)
        if protagonist_name and protagonist_name in text and carry_signals and growth_signal_hits == 0:
            issues.append(
                _issue(
                    role_id=role_id,
                    chapter=chapter,
                    index=len(issues) + 1,
                    issue_type="人物一致性",
                    severity="medium",
                    location=f"第{chapter}章成长轴",
                    description="主角已启用成长系统，但本章正文几乎看不见技能/心路/情感三轴的承接信号，成长连续性偏弱。",
                    suggestion="回到角色刻画或追读力强化，把当前 validated 的成长 tension 写进动作、选择、反应或代价里。",
                    rework_target_step="4-角色形象刻画",
                )
            )

    score = _clamp_score(92 - len(issues) * 16 - speech_violations * 4)
    if len(issues) == 0 and deferred_speech_to_step5:
        summary = "人物行为未见明显失真；对白声口问题留待 Step 5 处理。"
    elif len(issues) == 0:
        summary = "人物行为与对白未见明显失真。"
    else:
        summary = "存在对白声口或人物承接偏弱的问题。"
    return {
        "overall_score": score,
        "pass": len(issues) == 0,
        "issues": issues,
        "metrics": {
            "severe_ooc": 0,
            "motivation_breaks": 0,
            "speech_violations": speech_violations,
            "relationship_pressure_drops": 1 if recent_entities and not any(entity in text for entity in recent_entities[:3]) else 0,
            "growth_continuity_checked": growth_continuity_checked,
            "growth_signal_hits": growth_signal_hits,
        },
        "summary": summary,
    }


def _run_timeline(ctx: dict[str, Any], role_id: str, spec: dict[str, Any], validation_context: str) -> dict[str, Any]:
    chapter = ctx["chapter"]
    text = str(ctx["manuscript_text"] or "")
    markers: list[tuple[int, str, int]] = []
    for marker, order in TIME_MARKER_ORDER.items():
        for match in re.finditer(re.escape(marker), text):
            markers.append((match.start(), marker, order))
    markers.sort(key=lambda item: item[0])

    issues: list[dict[str, Any]] = []
    sequence_breaks = 0
    last_order = -1
    for _pos, marker, order in markers:
        if last_order >= 0 and order < last_order and marker not in {"凌晨"}:
            sequence_breaks += 1
        last_order = order
    distinct_markers = {item[1] for item in markers}
    duration_conflicts = 1 if len(distinct_markers) >= 5 and len(text) <= 1600 else 0

    if sequence_breaks:
        issues.append(
            _issue(
                role_id=role_id,
                chapter=chapter,
                index=len(issues) + 1,
                issue_type="时间线",
                severity="medium",
                location=f"第{chapter}章时间锚",
                description="时间锚出现逆序跳动，阅读时间感不稳定。",
                suggestion="回到节奏或起盘，理顺时间顺序与段落切换提示。",
                rework_target_step="2-节奏优化",
            )
        )

    if duration_conflicts:
        issues.append(
            _issue(
                role_id=role_id,
                chapter=chapter,
                index=len(issues) + 1,
                issue_type="时间线",
                severity="low",
                location=f"第{chapter}章段落时长",
                description="短篇幅内塞入过多时间段切换，可能造成时长压缩失真。",
                suggestion="减少无必要的时间跳切，给主要场景留出连续时段。",
                rework_target_step="1-单章叙事起盘",
            )
        )

    score = _clamp_score(92 - sequence_breaks * 18 - duration_conflicts * 10)
    return {
        "overall_score": score,
        "pass": len(issues) == 0,
        "issues": issues,
        "metrics": {
            "time_anchor_conflicts": sequence_breaks,
            "sequence_breaks": sequence_breaks,
            "duration_conflicts": duration_conflicts,
            "spoiler_risk": "low",
        },
        "summary": "时间顺序基本清楚。" if len(issues) == 0 else "存在时间锚或时长压缩风险。",
    }


def _run_task_convergence(
    ctx: dict[str, Any],
    role_id: str,
    spec: dict[str, Any],
    validation_context: str,
) -> dict[str, Any]:
    chapter = ctx["chapter"]
    text = str(ctx["manuscript_text"] or "")
    fact_pack = _safe_dict(ctx.get("fact_pack"))
    volume_summary = _safe_dict(fact_pack.get("volume_planning_summary"))
    chapter_packet = _safe_dict(fact_pack.get("chapter_planning_packet"))
    story_spine = _safe_dict(volume_summary.get("story_spine"))
    episode_handoff = _safe_dict(chapter_packet.get("episode_rhythm_handoff"))
    chapter_goals = [str(item).strip() for item in (chapter_packet.get("chapter_goals") or []) if str(item).strip()]

    volume_view = _extract_task_relation(
        volume_summary,
        upstream_keys=("上承部级主任务", "book_main_task", "upstream_book_task"),
        main_keys=("主线", "main_task", "volume_main_task", "本卷主线"),
        branch_keys=("支线", "branch_tasks", "volume_branches", "本卷支线"),
        merge_keys=("汇聚回主线", "convergence_target", "merge_back_to_main", "关键汇聚里程碑"),
        open_keys=("未汇聚任务去向", "open_branch_route", "branch_route"),
        fallback_main=[str(story_spine.get("headline") or "").strip()],
    )
    chapter_view = _extract_task_relation(
        chapter_packet,
        upstream_keys=("上承卷级任务", "upstream_volume_task"),
        main_keys=("主线", "main_task", "chapter_main_task", "本章主线"),
        branch_keys=("支线", "branch_tasks", "chapter_branches", "本章支线"),
        merge_keys=("汇聚动作", "convergence_action", "merge_action"),
        open_keys=("未汇聚任务去向", "open_branch_route", "branch_route"),
        fallback_main=[str(chapter_packet.get("story_overview") or "").strip(), *chapter_goals[:1]],
        fallback_branches=chapter_goals[1:3],
        fallback_merge=[
            str(chapter_packet.get("terminal_beat") or "").strip(),
            str(episode_handoff.get("exit_hook") or "").strip(),
        ],
    )

    issues: list[dict[str, Any]] = []
    unanchored_chapter_tasks = 0
    branch_merge_gaps = 0
    orphan_branch_count = 0
    open_branch_without_route = 0

    if not volume_view["main_tasks"]:
        issues.append(
            _issue(
                role_id=role_id,
                chapter=chapter,
                index=len(issues) + 1,
                issue_type="任务汇聚",
                severity="high",
                location=f"第{chapter}章 volume planning truth",
                description="卷级 planning truth 没有显式主任务，无法判断本卷支流到底服务哪条主线。",
                suggestion="回到 `2-卷章/第N卷/卷规划.md`，补 `上承部级主任务 / 主线 / 支线 / 汇聚回主线`。",
                rework_target_step="source-contract-fix",
                source_layer_owner="2-卷章",
                can_override=False,
            )
        )

    if not chapter_view["main_tasks"]:
        unanchored_chapter_tasks += 1
        issues.append(
            _issue(
                role_id=role_id,
                chapter=chapter,
                index=len(issues) + 1,
                issue_type="任务汇聚",
                severity="high",
                location=f"第{chapter}章 chapter planning truth",
                description="章级 planning truth 没有显式主任务，无法判断本章推进是否仍挂在卷级主线之下。",
                suggestion="回到 `2-卷章/第N卷/第N章.md`，补 `上承卷级任务 / 主线 / 支线 / 汇聚动作 / 未汇聚任务去向`。",
                rework_target_step="source-contract-fix",
                source_layer_owner="2-卷章",
                can_override=False,
            )
        )

    if chapter_view["upstream_task"] and volume_view["main_tasks"]:
        if not any(_task_related(chapter_view["upstream_task"], task) for task in volume_view["main_tasks"]):
            unanchored_chapter_tasks += 1
            issues.append(
                _issue(
                    role_id=role_id,
                    chapter=chapter,
                    index=len(issues) + 1,
                    issue_type="任务汇聚",
                    severity="high",
                    location=f"第{chapter}章 task lineage",
                    description="章级 `上承卷级任务` 无法回指卷级主线，任务从属关系失锚。",
                    suggestion="统一卷级/章级任务命名与挂靠关系，避免章级支流写成独立副本。",
                    rework_target_step="source-contract-fix",
                    source_layer_owner="2-卷章",
                    can_override=False,
                )
            )

    if chapter_view["branch_tasks"] and not chapter_view["merge_targets"] and not chapter_view["open_routes"]:
        orphan_branch_count += len(chapter_view["branch_tasks"])
        open_branch_without_route += len(chapter_view["branch_tasks"])
        issues.append(
            _issue(
                role_id=role_id,
                chapter=chapter,
                index=len(issues) + 1,
                issue_type="任务汇聚",
                severity="high",
                location=f"第{chapter}章支流任务合同",
                description="章级支流任务存在，但 planning truth 没有声明它们如何汇聚、转挂或保留开放。",
                suggestion="为每条支流补 `汇聚动作` 或 `未汇聚任务去向`，不要把未回收任务留成隐形账。",
                rework_target_step="source-contract-fix",
                source_layer_owner="2-卷章",
                can_override=False,
            )
        )

    branch_visible = sum(1 for task in chapter_view["branch_tasks"][:4] if _text_contains_candidate(text, task))
    merge_visible = sum(1 for target in chapter_view["merge_targets"][:3] if _text_contains_candidate(text, target))
    open_visible = sum(1 for route in chapter_view["open_routes"][:3] if _text_contains_candidate(text, route))
    if branch_visible and chapter_view["merge_targets"] and merge_visible == 0 and open_visible == 0:
        branch_merge_gaps += 1
        issues.append(
            _issue(
                role_id=role_id,
                chapter=chapter,
                index=len(issues) + 1,
                issue_type="任务汇聚",
                severity="medium" if validation_context == "final_acceptance" else "low",
                location=f"第{chapter}章正文任务汇聚",
                description="正文已展开支流任务，但没有把它明确汇回主线，也没有显式写成转挂/保留开放。",
                suggestion="回到起盘或追读力强化，把支流的回主线动作、转挂节点或保留开放信号写入正文。",
                rework_target_step="7-追读力强化",
            )
        )

    score = _clamp_score(92 - unanchored_chapter_tasks * 18 - orphan_branch_count * 10 - branch_merge_gaps * 14)
    return {
        "overall_score": score,
        "pass": len(issues) == 0,
        "issues": issues,
        "metrics": {
            "unanchored_chapter_tasks": unanchored_chapter_tasks,
            "branch_merge_gaps": branch_merge_gaps,
            "orphan_branch_count": orphan_branch_count,
            "open_branch_without_route": open_branch_without_route,
            "branch_tasks_visible": branch_visible,
            "merge_targets_visible": merge_visible,
            "open_routes_visible": open_visible,
        },
        "summary": "支流任务仍与主线保持挂靠并具备明确去向。" if len(issues) == 0 else "存在任务失锚、支流无去向或正文未完成汇聚的问题。",
    }


def _run_prose_style(ctx: dict[str, Any], role_id: str, spec: dict[str, Any], validation_context: str) -> dict[str, Any]:
    chapter = ctx["chapter"]
    body = _manuscript_body_text(str(ctx["manuscript_text"] or ""))
    rows = _paragraphs(body)
    current_step_id = normalize_drafting_step_id(ctx.get("current_step_id"))

    sensory_anchor_hits = _marker_hits(body, PROSE_SENSORY_ANCHOR_MARKERS)
    ai_formula_hits = _marker_hits(body, AI_FORMULA_MARKERS)
    meta_residue_hits = _marker_hits(body, META_RESIDUE_MARKERS) + _marker_hits(body, SCREENPLAY_RESIDUE_MARKERS)
    emotion_telling_hits = _marker_hits(body, EMOTION_TELLING_MARKERS)
    summaryish_hits = sum(1 for row in rows if any(re.search(pattern, row) for pattern in SUMMARYISH_PATTERNS))
    rhythm_flattening = _sentence_rhythm_flattening_score(rows)
    long_text = len(_normalize_match_text(body)) >= 1200
    medium_text = len(_normalize_match_text(body)) >= 600
    scene_density_gaps = 0

    issues: list[dict[str, Any]] = []
    if (long_text and sensory_anchor_hits < 8) or (medium_text and sensory_anchor_hits < 4):
        scene_density_gaps = 1
        issues.append(
            _issue(
                role_id=role_id,
                chapter=chapter,
                index=len(issues) + 1,
                issue_type="文体读感",
                severity="medium" if validation_context == "final_acceptance" else "low",
                location=f"第{chapter}章场景现场层",
                description="正文缺少足够的物件、声音、气味、身体反应或空间阻隔，信息虽然推进，但现场感偏空。",
                suggestion="回到场景和氛围渲染，补一个能推动人物反应、信息揭示或关系压力的现场发现。",
                rework_target_step="3-场景和氛围渲染",
            )
        )

    if ai_formula_hits + summaryish_hits >= 5:
        issues.append(
            _issue(
                role_id=role_id,
                chapter=chapter,
                index=len(issues) + 1,
                issue_type="文体读感",
                severity="medium",
                location=f"第{chapter}章叙述语气层",
                description="总结腔、说明腔或模型整理式套语偏多，读感更像信息归纳而不是小说现场。",
                suggestion="把总结判断改成动作、物象、误读、停顿、对白潜台词或局势反作用。",
                rework_target_step="8-润色" if current_step_id == "Step 8" else "3-场景和氛围渲染",
            )
        )

    if meta_residue_hits:
        issues.append(
            _issue(
                role_id=role_id,
                chapter=chapter,
                index=len(issues) + 1,
                issue_type="文体读感",
                severity="medium",
                location=f"第{chapter}章破沉浸 artifact",
                description="正文残留流程、规划或分镜类表达，破坏小说叙事内视角。",
                suggestion="把流程/镜头术语改成角色能感知到的声音、动作、物件、空间变化或危险余波。",
                rework_target_step="8-润色",
            )
        )

    if emotion_telling_hits >= 3:
        issues.append(
            _issue(
                role_id=role_id,
                chapter=chapter,
                index=len(issues) + 1,
                issue_type="文体读感",
                severity="medium",
                location=f"第{chapter}章情绪呈现层",
                description="情绪被直接标签化或落入脸色变化捷径，人物反应缺少具体身体和关系动作。",
                suggestion="回到心理活动描写，把情绪写成呼吸、手部细节、步伐、视线、物件误触、话语断裂或身份相关反应。",
                rework_target_step="6-心理活动描写",
            )
        )

    if rhythm_flattening >= 2:
        issues.append(
            _issue(
                role_id=role_id,
                chapter=chapter,
                index=len(issues) + 1,
                issue_type="文体读感",
                severity="low",
                location=f"第{chapter}章句群节奏层",
                description="句群长度和段落呼吸过分平均，存在通用顺滑化风险。",
                suggestion="在不改动事实的前提下恢复长短句、停顿、留白和段落重心变化。",
                rework_target_step="8-润色",
            )
        )

    dialogue = _dialogue_lines(body)
    explanation_dialogue_hits = sum(
        1
        for line in dialogue
        if len(line) >= 55 or any(marker in line for marker in EXPLANATION_DIALOGUE_MARKERS)
    )
    if explanation_dialogue_hits >= 2:
        issues.append(
            _issue(
                role_id=role_id,
                chapter=chapter,
                index=len(issues) + 1,
                issue_type="文体读感",
                severity="medium",
                location=f"第{chapter}章对白读感层",
                description="对白解释功能过重，潜台词、试探、回避或关系动作不足。",
                suggestion="回到对白优化，把说明压进人物的利益、遮掩、施压、索证或留退路动作里。",
                rework_target_step="5-对白优化",
            )
        )

    score = _clamp_score(
        94
        - scene_density_gaps * 14
        - (ai_formula_hits + summaryish_hits) * 3
        - meta_residue_hits * 6
        - emotion_telling_hits * 4
        - rhythm_flattening * 5
        - explanation_dialogue_hits * 4
    )
    return {
        "overall_score": score,
        "pass": len(issues) == 0,
        "issues": issues,
        "metrics": {
            "scene_density_gaps": scene_density_gaps,
            "ai_formula_hits": ai_formula_hits + summaryish_hits,
            "meta_residue_hits": meta_residue_hits,
            "emotion_telling_hits": emotion_telling_hits,
            "sentence_rhythm_flattening": rhythm_flattening,
            "sensory_anchor_hits": sensory_anchor_hits,
            "explanation_dialogue_hits": explanation_dialogue_hits,
            "cold_commentary_risk": "high"
            if ai_formula_hits + summaryish_hits >= 5 or scene_density_gaps
            else ("medium" if rhythm_flattening or emotion_telling_hits else "low"),
        },
        "summary": "文体读感、现场感与中文句群基本成立。" if len(issues) == 0 else "存在现场感不足、AI/说明腔、句群平均化或模板化情绪表达。",
    }


ROLE_RUNNERS: dict[str, Callable[[dict[str, Any], str, dict[str, Any], str], dict[str, Any]]] = {
    "structure-validator": _run_structure,
    "continuity-validator": _run_continuity,
    "logic-validator": _run_logic,
    "character-validator": _run_character,
    "timeline-validator": _run_timeline,
    "task-convergence-validator": _run_task_convergence,
    "prose-style-validator": _run_prose_style,
}


def _run_validator_with_context(
    *,
    ctx: dict[str, Any],
    role_id: str,
    validation_context: str,
) -> dict[str, Any]:
    spec = _role_spec(role_id)
    runner = ROLE_RUNNERS.get(role_id)
    if runner is None:
        raise KeyError(f"missing runner for role_id={role_id}")

    chapter_num = _safe_int(ctx.get("chapter"), 0)
    project_root = Path(ctx["project_root"])
    current_step_id = str(ctx.get("current_step_id") or "")
    manuscript_path = ctx["manuscript_path"]
    if not manuscript_path.is_file():
        raise FileNotFoundError(f"missing manuscript: {manuscript_path}")

    covenant_issues = _covenant_issues(ctx)
    if covenant_issues:
        result_core = {
            "overall_score": 0,
            "pass": False,
            "issues": covenant_issues,
            "metrics": {
                "missing_fact_pack_slices": list(ctx.get("fact_pack_missing_slices") or []),
            },
            "summary": "validation_fact_pack 缺少必需 slice，当前维度不具备可靠验收条件。",
        }
    else:
        result_core = runner(ctx, role_id, spec, validation_context)

    issues = list(result_core.get("issues", []) or [])
    severity_counts = _severity_counts(issues)
    dimension_key = str(spec.get("dimension") or role_id).strip() or role_id
    dimension_label = ROLE_ID_TO_DIMENSION.get(role_id, dimension_key)
    report_filename = str(spec.get("report_filename") or f"{dimension_label}.md")
    overall_score = _safe_int(result_core.get("overall_score"), 0)
    passed = bool(result_core.get("pass")) and not any(str(item.get("severity")) in {"critical", "high"} for item in issues)

    result = {
        "agent": role_id,
        "role_id": role_id,
        "dimension": dimension_key,
        "validation_context": validation_context,
        "chapter": chapter_num,
        "current_step_id": normalize_drafting_step_id(current_step_id),
        "overall_score": overall_score,
        "score": overall_score,
        "pass": passed,
        "issues": issues,
        "metrics": result_core.get("metrics", {}) or {},
        "summary": str(result_core.get("summary") or ""),
        "severity_counts": severity_counts,
        "critical_issues": [item for item in issues if str(item.get("severity")) == "critical"],
        "default_rework_targets": list(spec.get("default_rework_targets") or []),
        "source_trace": {
            "upstream_source_owners": list(spec.get("upstream_source_owners") or []),
            "runtime_warnings": list(ctx["warnings"]),
        },
        "blocking_scope": "stage" if any(str(item.get("severity")) in {"critical", "high"} for item in issues) else "local",
    }
    report_ref = _write_report(
        project_root=project_root,
        chapter=chapter_num,
        role_id=role_id,
        dimension_label=dimension_label,
        report_filename=report_filename,
        result=result,
        manuscript_path=manuscript_path,
        warnings=list(ctx["warnings"]),
    )
    result["report_ref"] = report_ref
    result["dimension_report_ref"] = report_ref
    return result


def run_validator(
    *,
    project_root: Path,
    chapter_num: int,
    role_id: str,
    validation_context: str,
    current_step_id: str | None = None,
) -> dict[str, Any]:
    ctx = _build_runtime_context(project_root, chapter_num, current_step_id=current_step_id)
    return _run_validator_with_context(
        ctx=ctx,
        role_id=role_id,
        validation_context=validation_context,
    )


def run_batch(
    *,
    project_root: Path,
    chapter_num: int,
    role_ids: list[str],
    validation_context: str,
    current_step_id: str | None = None,
) -> dict[str, Any]:
    results = []
    ctx = _build_runtime_context(project_root, chapter_num, current_step_id=current_step_id)
    for role_id in role_ids:
        results.append(
            {
                "role_id": role_id,
                "result": _run_validator_with_context(
                    ctx=ctx,
                    role_id=role_id,
                    validation_context=validation_context,
                ),
            }
        )
    return {
        "chapter": chapter_num,
        "validation_context": validation_context,
        "current_step_id": normalize_drafting_step_id(current_step_id),
        "results": results,
    }


def _dimension_score(result: dict[str, Any]) -> float:
    return round(_safe_int(result.get("overall_score"), 0) / 10.0, 2)


def _aggregate_rework_targets(issues: list[dict[str, Any]], routing_decision: str) -> list[dict[str, Any]]:
    groups: dict[str, list[str]] = {}
    for issue in issues:
        key = ""
        if routing_decision == "back_to_source_contract":
            key = str(issue.get("source_layer_owner") or "").strip()
        else:
            key = str(issue.get("rework_target_step") or "").strip()
        if not key:
            continue
        groups.setdefault(key, []).append(str(issue.get("id") or ""))

    targets = []
    for key, issue_ids in groups.items():
        if not issue_ids:
            continue
        reason = "上游真源存在缺口或冲突，需先修 source contract。" if routing_decision == "back_to_source_contract" else "当前节点是最早受影响的返工入口。"
        targets.append(
            {
                "step_id": key,
                "issue_ids": issue_ids,
                "reason": reason,
            }
        )
    return targets


def _write_aggregate_json(project_root: Path, chapter_num: int, payload: dict[str, Any]) -> str:
    output_path = _aggregate_output_path(project_root, chapter_num)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return _aggregate_output_ref(chapter_num)


def _code_reviewer_dir(project_root: Path, chapter_num: int) -> Path:
    output_dir = project_root / "review" / ".code-reviewer" / f"第{chapter_num}章"
    output_dir.mkdir(parents=True, exist_ok=True)
    return output_dir


def _run_detached_json_tool(
    *,
    script_path: Path,
    target_path: Path,
    output_path: Path,
    log_path: Path,
) -> dict[str, Any]:
    payload: dict[str, Any] = {
        "script": str(script_path),
        "target": str(target_path),
        "output_ref": str(output_path),
        "log_ref": str(log_path),
        "mode": "background_subprocess",
    }
    if not script_path.is_file():
        payload["status"] = "missing-script"
        return payload

    with log_path.open("w", encoding="utf-8") as log_file:
        process = subprocess.Popen(
            [
                sys.executable,
                str(script_path),
                str(target_path),
                "--json",
                "--output",
                str(output_path),
            ],
            stdout=log_file,
            stderr=subprocess.STDOUT,
            start_new_session=True,
        )
        payload["pid"] = process.pid
        try:
            return_code = process.wait(timeout=CODE_REVIEWER_TIMEOUT_SECONDS)
        except subprocess.TimeoutExpired:
            process.terminate()
            try:
                process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                process.kill()
                process.wait(timeout=5)
            payload["status"] = "timeout"
            return payload

    payload["status"] = "completed" if return_code == 0 else "failed"
    payload["returncode"] = return_code
    payload["output_exists"] = output_path.is_file()
    return payload


def _load_optional_json(path: Path) -> dict[str, Any]:
    if not path.is_file():
        return {}
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return {}
    return data if isinstance(data, dict) else {}


def _run_code_reviewer_audit(
    *,
    project_root: Path,
    chapter_num: int,
    target_path: Path,
) -> dict[str, Any]:
    output_dir = _code_reviewer_dir(project_root, chapter_num)
    checker_json = output_dir / "code_quality.json"
    checker_log = output_dir / "code_quality.log"
    report_json = output_dir / "review_report.json"
    report_log = output_dir / "review_report.log"

    checker_job = _run_detached_json_tool(
        script_path=CODE_REVIEWER_CHECKER,
        target_path=target_path,
        output_path=checker_json,
        log_path=checker_log,
    )
    reporter_job = _run_detached_json_tool(
        script_path=CODE_REVIEWER_REPORTER,
        target_path=target_path,
        output_path=report_json,
        log_path=report_log,
    )

    checker_payload = _load_optional_json(checker_json)
    reporter_payload = _load_optional_json(report_json)
    findings: list[dict[str, Any]] = []
    for packet in (checker_payload, reporter_payload):
        for item in packet.get("findings", []) or []:
            if isinstance(item, dict):
                findings.append(item)

    return {
        "provider": "code-reviewer",
        "mode": "background_subprocess_waited",
        "target_ref": str(target_path.relative_to(project_root)) if target_path.is_absolute() else str(target_path),
        "jobs": [checker_job, reporter_job],
        "checker_result": checker_payload,
        "report_result": reporter_payload,
        "findings": findings,
        "artifact_dir_ref": str(output_dir.relative_to(project_root)),
        "executed_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
    }


def _normalize_auto_fix_ops(finding: dict[str, Any]) -> list[dict[str, Any]]:
    raw = finding.get("auto_fix")
    if isinstance(raw, dict):
        return [raw]
    if isinstance(raw, list):
        return [item for item in raw if isinstance(item, dict)]
    return []


def _apply_auto_fix_ops(text: str, ops: list[dict[str, Any]]) -> tuple[str, bool, str]:
    current = text
    applied_any = False
    for op in ops:
        op_type = str(op.get("type") or "").strip()
        if op_type == "replace_text":
            old = str(op.get("old") or "")
            new = str(op.get("new") or "")
            count = _safe_int(op.get("count"), 1)
            if not old:
                return text, False, "missing_old_text"
            if old not in current:
                return text, False, "old_text_not_found"
            current = current.replace(old, new, count if count > 0 else -1)
            applied_any = True
            continue
        if op_type == "append_text":
            extra = str(op.get("text") or "")
            if not extra:
                return text, False, "missing_append_text"
            if extra in current:
                continue
            current = current + extra
            applied_any = True
            continue
        return text, False, f"unsupported_fix_type:{op_type or 'empty'}"
    return current, applied_any, "applied" if applied_any else "noop"


def _apply_external_auto_fixes(manuscript_path: Path, findings: list[dict[str, Any]]) -> dict[str, Any]:
    original_text = manuscript_path.read_text(encoding="utf-8")
    current_text = original_text
    applied_indices: list[int] = []
    skipped: list[dict[str, Any]] = []

    for index, finding in enumerate(findings, start=1):
        ops = _normalize_auto_fix_ops(finding)
        if not ops:
            continue
        updated_text, applied, reason = _apply_auto_fix_ops(current_text, ops)
        if applied:
            current_text = updated_text
            applied_indices.append(index)
        else:
            skipped.append({"index": index, "reason": reason})

    changed = current_text != original_text
    if changed:
        manuscript_path.write_text(current_text, encoding="utf-8")

    return {
        "attempted_count": len([1 for item in findings if _normalize_auto_fix_ops(item)]),
        "applied_count": len(applied_indices),
        "applied_indices": applied_indices,
        "changed_manuscript": changed,
        "skipped": skipped,
    }


def _unresolved_external_findings(external_review: dict[str, Any]) -> list[dict[str, Any]]:
    findings = list(external_review.get("findings", []) or [])
    applied = set(
        _safe_int(item, 0)
        for item in _safe_dict(external_review.get("auto_fix_summary")).get("applied_indices", [])
    )
    unresolved: list[dict[str, Any]] = []
    for index, item in enumerate(findings, start=1):
        if index in applied:
            continue
        unresolved.append(item)
    return unresolved


def _external_findings_to_issues(chapter_num: int, findings: list[dict[str, Any]]) -> list[dict[str, Any]]:
    issues: list[dict[str, Any]] = []
    for index, item in enumerate(findings, start=1):
        severity = str(item.get("severity") or item.get("priority") or "medium").strip().lower()
        if severity not in SEVERITY_ORDER:
            severity = "medium"
        location = str(item.get("location") or item.get("file") or f"第{chapter_num}章").strip()
        description = str(item.get("description") or item.get("title") or "code-reviewer 发现需要人工确认的问题").strip()
        suggestion = str(item.get("suggestion") or item.get("recommendation") or "回到最早受影响的 drafting step 修复后重跑 review").strip()
        issues.append(
            _issue(
                chapter=chapter_num,
                role_id="code-reviewer",
                index=index,
                issue_type="external_audit_finding",
                severity=severity,
                location=location,
                description=description,
                suggestion=suggestion,
                rework_target_step="1-单章叙事起盘",
                source_layer_owner="review",
                can_override=severity == "low",
            )
        )
    return issues


def _final_review_report_ref(chapter_num: int) -> str:
    return f"review/第{chapter_num}-{chapter_num}章审查报告.md"


def _write_final_review_report(
    *,
    project_root: Path,
    chapter_num: int,
    payload: dict[str, Any],
    external_review: dict[str, Any],
) -> str:
    relative_ref = _final_review_report_ref(chapter_num)
    absolute_path = project_root / relative_ref
    absolute_path.parent.mkdir(parents=True, exist_ok=True)

    lines = [
        f"# 第{chapter_num}章 review 审查报告",
        "",
        "## Gate Summary",
        "",
        f"- `validation_status`: {payload.get('validation_status')}",
        f"- `routing_decision`: {payload.get('routing_decision')}",
        f"- `overall_score`: {payload.get('overall_score')}",
        f"- `handoff_targets`: {json.dumps(payload.get('handoff_targets', []), ensure_ascii=False)}",
        "",
        "## Severity Counts",
        "",
        "```json",
        json.dumps(payload.get("severity_counts", {}), ensure_ascii=False, indent=2),
        "```",
        "",
        "## code-reviewer Dispatch",
        "",
        f"- `provider`: {external_review.get('provider') or 'code-reviewer'}",
        f"- `mode`: {external_review.get('mode') or 'not-run'}",
        f"- `artifact_dir_ref`: {external_review.get('artifact_dir_ref') or '-'}",
        f"- `auto_fix_summary`: {json.dumps(external_review.get('auto_fix_summary', {}), ensure_ascii=False)}",
        "",
        "## Findings Snapshot",
        "",
    ]
    findings = external_review.get("findings", []) or []
    if findings:
        for item in findings[:10]:
            lines.append(f"- {json.dumps(item, ensure_ascii=False)}")
    else:
        lines.append("- code-reviewer 未返回结构化 findings；当前以阶段聚合结果为准。")
    lines.extend(
        [
            "",
            "## Aggregate Ref",
            "",
            f"- `{payload.get('validation_ref')}`",
        ]
    )
    absolute_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return relative_ref


def run_final_acceptance(
    *,
    project_root: Path,
    chapter_num: int,
    current_step_id: str | None = None,
) -> dict[str, Any]:
    ctx = _build_runtime_context(project_root, chapter_num, current_step_id=current_step_id)
    manuscript_path = Path(ctx["manuscript_path"])
    if not manuscript_path.is_file():
        raise FileNotFoundError(f"missing manuscript: {manuscript_path}")

    specs = _final_acceptance_specs()
    role_ids = [str(spec.get("role_id") or "").strip() for spec in specs if str(spec.get("role_id") or "").strip()]
    template = _load_aggregate_template()
    manuscript_ref = str(manuscript_path.relative_to(project_root))
    aggregate_ref = _aggregate_output_ref(chapter_num)
    external_review = _run_code_reviewer_audit(
        project_root=project_root,
        chapter_num=chapter_num,
        target_path=manuscript_path,
    )
    external_review["auto_fix_summary"] = _apply_external_auto_fixes(
        manuscript_path,
        list(external_review.get("findings", []) or []),
    )
    if _safe_dict(external_review.get("auto_fix_summary")).get("changed_manuscript"):
        ctx = _build_runtime_context(project_root, chapter_num, current_step_id=current_step_id)
        manuscript_path = Path(ctx["manuscript_path"])
        manuscript_ref = str(manuscript_path.relative_to(project_root))
    accepted_manuscript_stage = "4-润色" if manuscript_ref.replace("\\", "/").startswith("4-润色/") else "3-初稿"

    payload: dict[str, Any] = template if isinstance(template, dict) else {}
    payload.update(
        {
            "chapter": chapter_num,
            "manuscript_ref": manuscript_ref,
            "manuscript_refs": [manuscript_ref],
            "accepted_manuscript_stage": accepted_manuscript_stage,
            "accepted_manuscript_refs": [manuscript_ref],
            "accepted_manuscript_note": (
                "post-polish final acceptance"
                if accepted_manuscript_stage == "4-润色"
                else "candidate draft accepted for polishing handoff; not eligible for context-return unless skip-polish is explicit"
            ),
            "validation_ref": aggregate_ref,
            "validation_mode": "final_acceptance",
            "selected_agents": ["context-agent", *role_ids],
            "dimension_packets": {},
            "dimension_report_refs": {},
            "issues": [],
            "severity_counts": {"critical": 0, "high": 0, "medium": 0, "low": 0},
            "critical_issues": [],
            "overall_score": 0.0,
            "dimension_scores": {},
            "anti_ai_force_check": "pending",
            "spoiler_risk": "low",
            "contrivance_risk": "low",
            "cold_commentary_risk": "low",
            "routing_decision": "back_to_source_contract",
            "handoff_targets": [],
            "rework_targets": [],
            "source_trace": [],
            "evidence_refs": [manuscript_ref],
            "external_review": external_review,
        }
    )

    covenant_issues = _covenant_issues(ctx)
    if covenant_issues:
        external_issues = _external_findings_to_issues(chapter_num, _unresolved_external_findings(external_review))
        payload["validation_status"] = "FAIL-COVENANT"
        payload["issues"] = [*covenant_issues, *external_issues]
        payload["severity_counts"] = _severity_counts(payload["issues"])
        payload["critical_issues"] = [issue for issue in payload["issues"] if str(issue.get("severity")) == "critical"]
        payload["source_trace"] = [{"source_layer_owner": issue.get("source_layer_owner"), "issue_id": issue.get("id")} for issue in payload["issues"]]
        payload["rework_targets"] = _aggregate_rework_targets(payload["issues"], "back_to_source_contract")
        payload["review_report_ref"] = _write_final_review_report(
            project_root=project_root,
            chapter_num=chapter_num,
            payload=payload,
            external_review=external_review,
        )
        _write_aggregate_json(project_root, chapter_num, payload)
        return payload

    dimension_packets: dict[str, Any] = {}
    dimension_report_refs: dict[str, str] = {}
    issues: list[dict[str, Any]] = []
    per_dimension_scores: dict[str, float] = {}
    severity_list: list[dict[str, int]] = []
    source_trace: list[dict[str, Any]] = []
    runtime_issues: list[dict[str, Any]] = []
    weighted_score = 0.0
    total_weight = 0.0
    anti_ai_force_check = "pass"
    spoiler_risk = "low"
    contrivance_risk = "low"
    cold_commentary_risk = "low"

    for idx, spec in enumerate(specs, start=1):
        role_id = str(spec.get("role_id") or "").strip()
        if not role_id:
            continue
        try:
            result = _run_validator_with_context(
                ctx=ctx,
                role_id=role_id,
                validation_context="final_acceptance",
            )
        except Exception as exc:
            runtime_issues.append(_runtime_issue(chapter_num, role_id or "context-agent", exc, idx))
            continue

        dimension_packets[role_id] = result
        dimension_report_refs[role_id] = str(result.get("dimension_report_ref") or result.get("report_ref") or "")
        issues.extend(list(result.get("issues") or []))
        severity_list.append(_safe_dict(result.get("severity_counts")))
        dimension_key = str(result.get("dimension") or role_id)
        per_dimension_scores[dimension_key] = _dimension_score(result)
        weight = float(_safe_dict(spec.get("final_acceptance")).get("weight") or 0.0)
        weighted_score += _safe_int(result.get("overall_score"), 0) * weight
        total_weight += weight

        metrics = _safe_dict(result.get("metrics"))
        anti_ai_force_check = "fail" if str(metrics.get("anti_ai_force_check") or "").strip().lower() == "fail" else anti_ai_force_check
        spoiler_risk = _max_risk(spoiler_risk, metrics.get("spoiler_risk"))
        contrivance_risk = _max_risk(contrivance_risk, metrics.get("contrivance_risk"))
        cold_commentary_risk = _max_risk(cold_commentary_risk, metrics.get("cold_commentary_risk"))

        result_source_trace = _safe_dict(result.get("source_trace"))
        owners = [str(item).strip() for item in (result_source_trace.get("upstream_source_owners") or []) if str(item).strip()]
        if owners or result_source_trace.get("runtime_warnings"):
            source_trace.append(
                {
                    "role_id": role_id,
                    "upstream_source_owners": owners,
                    "runtime_warnings": list(result_source_trace.get("runtime_warnings") or []),
                }
            )

    if runtime_issues:
        issues.extend(runtime_issues)
        severity_list.append(_severity_counts(runtime_issues))

    external_issues = _external_findings_to_issues(chapter_num, _unresolved_external_findings(external_review))
    if external_issues:
        issues.extend(external_issues)
        severity_list.append(_severity_counts(external_issues))
        source_trace.append(
            {
                "role_id": "code-reviewer",
                "upstream_source_owners": ["review"],
                "runtime_warnings": [],
            }
        )

    severity_counts = _merge_severity_counts(severity_list)
    critical_issues = [issue for issue in issues if str(issue.get("severity") or "") == "critical"]
    source_owners = {
        str(issue.get("source_layer_owner") or "").strip()
        for issue in issues
        if str(issue.get("source_layer_owner") or "").strip()
    }
    upstream_owners = {owner for owner in source_owners if owner in {"0-初始化", "1-设定", "2-卷章", "STATE"}}

    if runtime_issues:
        validation_status = "FAIL-RUNTIME"
        routing_decision = "back_to_source_contract"
        handoff_targets: list[str] = []
    elif upstream_owners:
        validation_status = "FAIL-COVENANT"
        routing_decision = "back_to_source_contract"
        handoff_targets = []
    elif issues:
        validation_status = "FAIL-QUALITY"
        routing_decision = "back_to_drafting_nodes"
        handoff_targets = ["3-初稿"]
    elif accepted_manuscript_stage == "4-润色":
        validation_status = "PASS"
        routing_decision = "handoff_to_review_and_context_return"
        handoff_targets = ["review/", "context-return"]
    else:
        validation_status = "PASS"
        routing_decision = "handoff_to_polishing"
        handoff_targets = ["review/", "4-润色"]

    payload.update(
        {
            "validation_status": validation_status,
            "dimension_packets": dimension_packets,
            "dimension_report_refs": dimension_report_refs,
            "issues": issues,
            "severity_counts": severity_counts,
            "critical_issues": critical_issues,
            "overall_score": round(weighted_score / total_weight, 2) if total_weight else 0.0,
            "dimension_scores": per_dimension_scores,
            "anti_ai_force_check": anti_ai_force_check,
            "spoiler_risk": spoiler_risk,
            "contrivance_risk": contrivance_risk,
            "cold_commentary_risk": cold_commentary_risk,
            "routing_decision": routing_decision,
            "handoff_targets": handoff_targets,
            "rework_targets": _aggregate_rework_targets(issues, routing_decision),
            "source_trace": source_trace,
            "evidence_refs": [manuscript_ref, *[ref for ref in dimension_report_refs.values() if ref]],
        }
    )
    payload["review_report_ref"] = _write_final_review_report(
        project_root=project_root,
        chapter_num=chapter_num,
        payload=payload,
        external_review=external_review,
    )

    _write_aggregate_json(project_root, chapter_num, payload)
    return payload


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="story2026 review runtime runner")
    parser.add_argument("--project-root", help="项目根目录")
    sub = parser.add_subparsers(dest="action", required=True)

    p_run = sub.add_parser("run-validator", help="执行单个 validator")
    p_run.add_argument("--chapter", type=int, required=True, help="集号")
    p_run.add_argument("--role-id", required=True, help="validator role_id")
    p_run.add_argument("--context", choices=["drafting_inline", "final_acceptance"], default="drafting_inline")
    p_run.add_argument("--step-id", help="当前 drafting step_id，可选")
    p_run.add_argument("--format", choices=["text", "json"], default="json")

    p_batch = sub.add_parser("run-batch", help="执行一批 validators")
    p_batch.add_argument("--chapter", type=int, required=True, help="集号")
    p_batch.add_argument("--context", choices=["drafting_inline", "final_acceptance"], default="drafting_inline")
    p_batch.add_argument("--step-id", help="当前 drafting step_id，可选")
    p_batch.add_argument("--role-id", action="append", dest="role_ids", required=True, help="可重复传入多个 role_id")
    p_batch.add_argument("--format", choices=["text", "json"], default="json")

    p_final = sub.add_parser("run-final-acceptance", help="执行 review 父层终验聚合，并自动触发 code-reviewer")
    p_final.add_argument("--chapter", type=int, required=True, help="集号")
    p_final.add_argument("--step-id", help="当前 drafting step_id，可选")
    p_final.add_argument("--format", choices=["text", "json"], default="json")
    return parser.parse_args()


def _render_text(payload: dict[str, Any]) -> str:
    if "results" not in payload:
        return json.dumps(payload, ensure_ascii=False, indent=2)
    lines = [f"# Review Runner Result / 第{payload.get('chapter')}集", ""]
    for item in payload.get("results", []) or []:
        result = item.get("result", {}) if isinstance(item, dict) else {}
        lines.extend(
            [
                f"## {item.get('role_id')}",
                "",
                f"- pass: {result.get('pass')}",
                f"- overall_score: {result.get('overall_score')}",
                f"- summary: {result.get('summary')}",
                f"- current_step_id: {result.get('current_step_id') or payload.get('current_step_id') or '-'}",
                f"- report_ref: {result.get('report_ref')}",
                "",
            ]
        )
    return "\n".join(lines).strip() + "\n"


def main() -> int:
    args = _parse_args()
    project_root = _resolve_project_root(args.project_root)

    if args.action == "run-validator":
        payload = run_validator(
            project_root=project_root,
            chapter_num=args.chapter,
            role_id=args.role_id,
            validation_context=args.context,
            current_step_id=args.step_id,
        )
    elif args.action == "run-batch":
        payload = run_batch(
            project_root=project_root,
            chapter_num=args.chapter,
            role_ids=list(args.role_ids or []),
            validation_context=args.context,
            current_step_id=args.step_id,
        )
    else:
        payload = run_final_acceptance(
            project_root=project_root,
            chapter_num=args.chapter,
            current_step_id=args.step_id,
        )

    if getattr(args, "format", "json") == "text":
        print(_render_text(payload))
    else:
        print(json.dumps(payload, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    enable_windows_utf8_stdio(skip_in_pytest=True)
    raise SystemExit(main())
