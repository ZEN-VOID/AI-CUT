#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
validation_runner.py - story2026 validation runtime baseline runner

用途：
- 为 `3-Drafting` 的 inline validation hooks 提供第一版可执行自动 runner
- 为 `4-Validation` 的维度检查提供统一的本地规则基线

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
from typing import Any, Callable, Optional

from chapter_paths import drafting_root_md_path
from extract_chapter_context import build_chapter_context_payload
from project_locator import resolve_project_root
from runtime_compat import enable_windows_utf8_stdio, normalize_windows_path
from data_modules.type_pack_resolver import normalize_drafting_step_id, resolve_stage_projection

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
    "type-pack-fit-validator": "类型兑现",
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
    r"^(首先|然后|接着|最后|总之|原来|实际上|本章|这一集|简单来说)",
    r"(总而言之|换句话说|事情的经过是)",
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


def _registry_path() -> Path:
    return Path(__file__).resolve().parent.parent / "4-Validation" / "_shared" / "validation-dimension-registry.yaml"


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
    return Path(__file__).resolve().parent.parent / "4-Validation" / "_shared" / "validation-aggregate.template.json"


def _load_aggregate_template() -> dict[str, Any]:
    path = _aggregate_template_path()
    if not path.is_file():
        return {}
    data = json.loads(path.read_text(encoding="utf-8"))
    return data if isinstance(data, dict) else {}


def _aggregate_output_ref(chapter_num: int) -> str:
    return f"4-Validation/第{chapter_num}集.validation.json"


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


def _read_text_if_exists(path: Path) -> str:
    if not path.is_file():
        return ""
    return path.read_text(encoding="utf-8")


def _previous_manuscript_path(project_root: Path, chapter_num: int) -> Optional[Path]:
    if chapter_num <= 1:
        return None
    path = drafting_root_md_path(project_root, chapter_num - 1)
    return path if path.is_file() else None


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
            "type_pack_profile": _safe_dict(init_truth.get("type_pack_profile")),
            "project_preferences": _safe_dict(init_truth.get("project_preferences")),
            "style_contract_ref": str(init_truth.get("style_contract_ref") or "").strip(),
            "global_contract_refs": list(init_truth.get("global_contract_refs") or []),
            "genre": str(_safe_dict(init_truth.get("genre_profile")).get("genre") or "").strip(),
        }

    return {
        "draft_snapshot": draft_snapshot,
        "cards_truth": cards_truth,
        "planning_truth": planning_truth,
        "init_truth": init_truth,
        "runtime_context": runtime_context,
        "promise_slice": promise_slice,
        "chapter_board": _safe_dict(planning_truth.get("chapter_board")),
        "cards_state_history_slice": _safe_dict(cards_truth.get("cards_state_history_slice")),
        "foreshadow_silence_slice": _safe_dict(planning_truth.get("foreshadow_silence_slice")),
        "style_gate": _safe_dict(runtime_context.get("style_gate")),
        "global_truth_slice": _safe_dict(cards_truth.get("global_truth_slice")),
        "type_pack_profile": _safe_dict(init_truth.get("type_pack_profile")) or _safe_dict(promise_slice.get("type_pack_profile")),
    }


def _build_runtime_context(project_root: Path, chapter_num: int, current_step_id: str | None = None) -> dict[str, Any]:
    manuscript_path = drafting_root_md_path(project_root, chapter_num)
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


def _clamp_score(score: float) -> int:
    return max(0, min(100, int(round(score))))


def _severity_counts(issues: list[dict[str, Any]]) -> dict[str, int]:
    counts = {"critical": 0, "high": 0, "medium": 0, "low": 0}
    for issue in issues:
        severity = str(issue.get("severity") or "low")
        if severity in counts:
            counts[severity] += 1
    return counts


def _semantic_tags(profile: dict[str, Any]) -> set[str]:
    return {
        str(item).strip()
        for item in (profile.get("semantic_tags") or [])
        if str(item).strip()
    }


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
        "draft_snapshot": "3-Drafting",
        "cards_truth": "1-Cards",
        "planning_truth": "2-Planning",
        "init_truth": "0-Init",
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
                source_layer_owner=owner_map.get(str(slice_name), "4-Validation"),
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
        source_layer_owner="4-Validation",
        can_override=False,
    )


def _evaluate_type_pack_fit(ctx: dict[str, Any], *, role_id: str = "type-pack-fit-validator") -> dict[str, Any]:
    text = str(ctx.get("manuscript_text") or "")
    chapter = _safe_int(ctx.get("chapter"), 0)
    current_step_id = normalize_drafting_step_id(ctx.get("current_step_id"))
    profile = _safe_dict(ctx.get("fact_pack", {}).get("type_pack_profile"))
    active_packs = [str(item) for item in (profile.get("active_packs") or []) if str(item).strip()]
    semantic_tags = _semantic_tags(profile)
    validation_projection = resolve_stage_projection(profile, "validation")
    drafting_projection = resolve_stage_projection(profile, "drafting", current_step_id=current_step_id)
    required_hooks = [str(item).strip() for item in (validation_projection.get("required_hooks") or []) if str(item).strip()]
    hard_fail_signals = [str(item).strip() for item in (validation_projection.get("hard_fail_signals") or []) if str(item).strip()]
    drafting_required_hooks = [str(item).strip() for item in (drafting_projection.get("required_hooks") or []) if str(item).strip()]

    issues: list[dict[str, Any]] = []
    if not active_packs:
        return {
            "enabled": False,
            "active_packs": [],
            "semantic_tags": [],
            "required_hooks": [],
            "hard_fail_signals": [],
            "fit_score": 100,
            "issues": issues,
            "current_step_id": current_step_id,
        }

    tail = text[-180:]
    paragraphs = [row for row in _paragraphs(text) if row]
    long_paragraphs = sum(1 for row in paragraphs if len(row) >= 120)

    if "high-impact-webnovel" in semantic_tags or "网文高冲击" in active_packs:
        if not any(token in tail for token in ("？", "!", "！", "……", "却", "但", "然而", "下一")):
            issues.append(
                _issue(
                    role_id=role_id,
                    chapter=chapter,
                    index=len(issues) + 1,
                    issue_type="类型兑现",
                    severity="medium",
                    location=f"第{chapter}集结尾",
                    description="已启用网文高冲击，但章末牵引信号偏弱。",
                    suggestion="在章末补足下一步动机、悬念或回报预告。",
                    rework_target_step="7-追读力强化",
                )
            )
        if long_paragraphs >= 4:
            issues.append(
                _issue(
                    role_id=role_id,
                    chapter=chapter,
                    index=len(issues) + 1,
                    issue_type="类型兑现",
                    severity="medium",
                    location=f"第{chapter}集段落层",
                    description="已启用网文高冲击，但长段过多，推进节奏偏慢。",
                    suggestion="拆分长段，前置冲突和结果，减少说明性拖沓。",
                    rework_target_step="2-节奏优化",
                )
            )

    if "upgrade-fantasy" in semantic_tags and not any(token in text for token in ("境界", "修为", "突破", "灵石", "资源", "宗门", "机缘")):
        issues.append(
            _issue(
                role_id=role_id,
                chapter=chapter,
                index=len(issues) + 1,
                issue_type="类型兑现",
                severity="low",
                location=f"第{chapter}集正文",
                description="已启用升级型玄幻/修仙 pack，但本章缺少明显升级/资源/势力信号。",
                suggestion="补足升级链、资源争夺或势力压迫中的至少一项。",
                rework_target_step="1-单集叙事起盘",
            )
        )

    if "rules-mystery" in semantic_tags and not any(token in text for token in ("规则", "线索", "真相", "疑点", "禁忌", "代价")):
        issues.append(
            _issue(
                role_id=role_id,
                chapter=chapter,
                index=len(issues) + 1,
                issue_type="类型兑现",
                severity="medium",
                location=f"第{chapter}集正文",
                description="已启用规则悬疑/规则怪谈 pack，但本章缺少规则/线索/代价的显性支点。",
                suggestion="补足可验证线索或规则代价，不要只保留抽象悬念。",
                rework_target_step="1-单集叙事起盘",
            )
        )

    if "urban-revenge" in semantic_tags and not any(token in text for token in ("打脸", "反击", "羞辱", "压迫", "翻盘", "反压")):
        issues.append(
            _issue(
                role_id=role_id,
                chapter=chapter,
                index=len(issues) + 1,
                issue_type="类型兑现",
                severity="low",
                location=f"第{chapter}集正文",
                description="已启用都市复仇/豪门强冲突 pack，但压迫/回击链条不够显性。",
                suggestion="补足压迫者、见证者与回击后果。",
                rework_target_step="7-追读力强化",
            )
        )

    if "female-emotion-suspense" in semantic_tags and not any(token in text for token in ("情绪", "心口", "眼神", "误会", "关系", "拉扯")):
        issues.append(
            _issue(
                role_id=role_id,
                chapter=chapter,
                index=len(issues) + 1,
                issue_type="类型兑现",
                severity="low",
                location=f"第{chapter}集正文",
                description="已启用女频悬疑/强情绪 pack，但情绪与关系张力显影不足。",
                suggestion="补足关系位移、误解或情绪代价，并让心理波动落进人物可感的内心层。",
                rework_target_step="6-心理活动描写",
            )
        )

    if current_step_id == "Step 2" and "删减无推进段" in drafting_required_hooks:
        if long_paragraphs >= 3:
            issues.append(
                _issue(
                    role_id=role_id,
                    chapter=chapter,
                    index=len(issues) + 1,
                    issue_type="类型兑现",
                    severity="medium",
                    location=f"第{chapter}集 Step 2",
                    description="当前是节奏优化步骤，但长段仍然偏多，未满足快节奏 pack 的 step hook。",
                    suggestion="继续拆分长段，前置动作结果闭环，减少说明段滞留。",
                    rework_target_step="2-节奏优化",
                )
            )

    if current_step_id == "Step 5" and "情绪升级必须伴随行动或代价" in drafting_required_hooks:
        emotion_tokens = ("情绪", "心口", "眼神", "关系", "难受", "委屈", "心酸", "痛苦")
        action_tokens = ("推开", "离开", "拒绝", "拥抱", "转身", "代价", "选择", "决定", "行动")
        if any(token in text for token in emotion_tokens) and not any(token in text for token in action_tokens):
            issues.append(
                _issue(
                    role_id=role_id,
                    chapter=chapter,
                    index=len(issues) + 1,
                    issue_type="类型兑现",
                    severity="medium",
                    location=f"第{chapter}集 Step 5",
                    description="当前启用了强情绪 pack，但情绪表达未转化为角色动作或代价。",
                    suggestion="让情绪显影落实到对白/动作/关系后果，不只停在心情宣告。",
                    rework_target_step="5-对白个性化",
                )
            )

    fit_score = _clamp_score(100 - len(issues) * 12)
    return {
        "enabled": True,
        "active_packs": active_packs,
        "semantic_tags": sorted(semantic_tags),
        "required_hooks": required_hooks,
        "drafting_required_hooks": drafting_required_hooks,
        "hard_fail_signals": hard_fail_signals,
        "fit_score": fit_score,
        "issues": issues,
        "current_step_id": current_step_id,
    }


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
    source_layer_owner: str = "3-Drafting",
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
    return f"4-Validation/第{chapter}集/{report_filename or ROLE_ID_TO_DIMENSION.get(role_id, role_id + '.md')}"


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
        f"# 第{chapter}集 {dimension_label} 验收报告",
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
    obligations = []
    obligations.extend(chapter_board.get("chapter_goals", []) or [])
    obligations.extend(chapter_board.get("must_happen", []) or [])
    obligations = [item for item in obligations if item]
    checked_obligations = obligations[:6]

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
                location=f"第{chapter}集正文",
                description=f"规划义务未在正文中找到足够证据：{item}",
                suggestion="回到起盘或追读力强化，把该义务写成可感知的场面、局部兑现与续读牵引。",
                rework_target_step="1-单集叙事起盘",
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
                location=f"第{chapter}集正文段落层",
                description="说明腔/总结腔偏多，结构更像提纲复述而不是戏剧场面。",
                suggestion="减少摘要式解释，补足动作、冲突和即时反馈。",
                rework_target_step="7-追读力强化",
            )
        )

    score = _clamp_score(92 - (len(checked_obligations) - hits) * 18 - summary_hits * 5)
    return {
        "overall_score": score,
        "pass": len(issues) == 0,
        "issues": issues,
        "metrics": {
            "required_events_hit": hits,
            "missed_obligations": max(0, len(checked_obligations) - hits),
            "promise_breaks": 0 if len(issues) == 0 else min(1, len(issues)),
            "undramatized_exposition_hits": summary_hits,
            "anti_ai_force_check": "fail" if summary_hits >= 3 else "pass",
            "cold_commentary_risk": "medium" if summary_hits >= 3 else "low",
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
                    location=f"第{chapter}集开头",
                    description="本集开场缺少明显承接信号，像重新起一章而不是延续上一集停点。",
                    suggestion="在前几段补上情绪/动作/信息承接锚点。",
                    rework_target_step="1-单集叙事起盘",
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
                location=f"第{chapter}集全文",
                description="近期活跃实体没有在当前集得到明确承接，线程连续性偏弱。",
                suggestion="至少让关键实体/线程在当前集获得一次显性回指。",
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
                location=f"第{chapter}集场景层",
                description=f"当前态位置 `{current_location}` 未在正文中获得稳定锚定，状态连续性不足。",
                suggestion="补足位置/状态锚，避免读者失去空间与行动依据。",
                rework_target_step="1-单集叙事起盘",
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
                location=f"第{chapter}集状态层",
                description=f"近期对象状态变更未在正文中得到承接：{state_change_misses[0]}",
                suggestion="补上状态延续或明确说明为什么当前状态已变化。",
                rework_target_step="1-单集叙事起盘",
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
                location=f"第{chapter}集世界规则层",
                description="上游真源已声明规则存在代价/限制，但正文在触发破例动作时没有体现对应成本。",
                suggestion="补足触发条件、代价或先例解释；若上游规则本身冲突，改走 source-contract 修复。",
                rework_target_step="1-单集叙事起盘",
                source_layer_owner="1-Cards",
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
                location=f"第{chapter}集能力边界层",
                description=f"`{golden_finger_name}` 在上游真源中带有限制，但正文把它写成了近乎无上限能力。",
                suggestion="把能力使用改回限制内，或明确补写限制失效的条件与代价。",
                rework_target_step="1-单集叙事起盘",
                source_layer_owner="0-Init",
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
                    location=f"第{chapter}集规划约束层",
                    description=f"planning truth 声明了本集不可擅自改写的约束，但正文没有给出清晰锚点：{misses[0]}",
                    suggestion="补上对应约束的存在感；若 planning 约束已过期或自相矛盾，回到 `2-Planning` 修源。",
                    rework_target_step="source-contract-fix",
                    source_layer_owner="2-Planning",
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
                location=f"第{chapter}集因果链",
                description="文本中出现过多强行转折/凭空推进标记，因果链有拼接感。",
                suggestion="回到起盘，重写触发条件、过程与代价，让事件自然发生。",
                rework_target_step="1-单集叙事起盘",
            )
        )

    world_rule_conflicts = sum(
        1
        for issue in issues
        if str(issue.get("source_layer_owner") or "") in {"0-Init", "1-Cards"}
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
        if str(issue.get("source_layer_owner") or "") == "2-Planning"
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
                location=f"第{chapter}集对白层",
                description="对白偏长或解释性过强，角色声口区分度不足。",
                suggestion="回到对白优化，压缩解释，改成更像角色本人会说的话。",
                rework_target_step="5-对白个性化",
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
                location=f"第{chapter}集人物层",
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
                    location=f"第{chapter}集成长轴",
                    description="主角已启用成长系统，但本集正文几乎看不见技能/心路/情感三轴的承接信号，成长连续性偏弱。",
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
                location=f"第{chapter}集时间锚",
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
                location=f"第{chapter}集段落时长",
                description="短篇幅内塞入过多时间段切换，可能造成时长压缩失真。",
                suggestion="减少无必要的时间跳切，给主要场景留出连续时段。",
                rework_target_step="1-单集叙事起盘",
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


def _run_type_pack_fit(ctx: dict[str, Any], role_id: str, spec: dict[str, Any], validation_context: str) -> dict[str, Any]:
    fit = _evaluate_type_pack_fit(ctx, role_id=role_id)
    if not fit.get("enabled"):
        return {
            "overall_score": 100,
            "pass": True,
            "issues": [],
            "metrics": {
                "type_pack_enabled": False,
                "active_packs": [],
                "required_hooks": [],
                "drafting_required_hooks": [],
                "current_step_id": normalize_drafting_step_id(ctx.get("current_step_id")),
            },
            "summary": "当前项目未启用显式 type-pack，类型兑现维度降级为观察态。",
        }

    score = _safe_int(fit.get("fit_score"), 100)
    issues = list(fit.get("issues") or [])
    return {
        "overall_score": score,
        "pass": len(issues) == 0,
        "issues": issues,
        "metrics": {
            "type_pack_enabled": True,
            "active_packs": list(fit.get("active_packs") or []),
            "required_hooks": list(fit.get("required_hooks") or []),
            "drafting_required_hooks": list(fit.get("drafting_required_hooks") or []),
            "hard_fail_signals": list(fit.get("hard_fail_signals") or []),
            "current_step_id": fit.get("current_step_id"),
        },
        "summary": "类型兑现基本达标。" if len(issues) == 0 else "存在 type-pack 兑现不足或 step hook 未落地的问题。",
    }


ROLE_RUNNERS: dict[str, Callable[[dict[str, Any], str, dict[str, Any], str], dict[str, Any]]] = {
    "structure-validator": _run_structure,
    "continuity-validator": _run_continuity,
    "logic-validator": _run_logic,
    "character-validator": _run_character,
    "timeline-validator": _run_timeline,
    "type-pack-fit-validator": _run_type_pack_fit,
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
    type_pack_fit = _evaluate_type_pack_fit(ctx)
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
        "type_pack_fit_summary": {
            "enabled": bool(type_pack_fit.get("enabled")),
            "active_packs": list(type_pack_fit.get("active_packs") or []),
            "semantic_tags": list(type_pack_fit.get("semantic_tags") or []),
            "fit_score": _safe_int(type_pack_fit.get("fit_score"), 0),
            "required_hooks": list(type_pack_fit.get("required_hooks") or []),
        },
        "type_pack_fail_signals": list(type_pack_fit.get("hard_fail_signals") or []),
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

    payload: dict[str, Any] = template if isinstance(template, dict) else {}
    payload.update(
        {
            "chapter": chapter_num,
            "manuscript_ref": manuscript_ref,
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
        }
    )

    covenant_issues = _covenant_issues(ctx)
    if covenant_issues:
        payload["validation_status"] = "FAIL-COVENANT"
        payload["issues"] = covenant_issues
        payload["severity_counts"] = _severity_counts(covenant_issues)
        payload["critical_issues"] = list(covenant_issues)
        payload["source_trace"] = [{"source_layer_owner": issue.get("source_layer_owner"), "issue_id": issue.get("id")} for issue in covenant_issues]
        payload["rework_targets"] = _aggregate_rework_targets(covenant_issues, "back_to_source_contract")
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

    severity_counts = _merge_severity_counts(severity_list)
    critical_issues = [issue for issue in issues if str(issue.get("severity") or "") == "critical"]
    source_owners = {
        str(issue.get("source_layer_owner") or "").strip()
        for issue in issues
        if str(issue.get("source_layer_owner") or "").strip()
    }
    upstream_owners = {owner for owner in source_owners if owner in {"0-Init", "1-Cards", "2-Planning", "STATE"}}

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
        handoff_targets = ["3-Drafting"]
    else:
        validation_status = "PASS"
        routing_decision = "handoff_to_review_and_loopback"
        handoff_targets = ["review/", "5-Loopback"]

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

    _write_aggregate_json(project_root, chapter_num, payload)
    return payload


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="story2026 validation runtime runner")
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

    p_final = sub.add_parser("run-final-acceptance", help="执行 4-Validation 父层终验聚合")
    p_final.add_argument("--chapter", type=int, required=True, help="集号")
    p_final.add_argument("--step-id", help="当前 drafting step_id，可选")
    p_final.add_argument("--format", choices=["text", "json"], default="json")
    return parser.parse_args()


def _render_text(payload: dict[str, Any]) -> str:
    if "results" not in payload:
        return json.dumps(payload, ensure_ascii=False, indent=2)
    lines = [f"# Validation Runner Result / 第{payload.get('chapter')}集", ""]
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
