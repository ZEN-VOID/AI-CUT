#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Formal writer for story2026 1-Cards outputs.

The writer turns a normalized cards payload into canonical JSON files under
`Cards/`, while stamping the trace contract required by 1-Cards:
- `content.module_route`
- `content.loaded_references`
- `content.writeback_plan`
"""

from __future__ import annotations

import argparse
import copy
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional
import yaml

from cards_coverage_validator import build_cards_coverage_report
from data_modules.cli_args import load_json_arg
from project_locator import resolve_project_root
from runtime_compat import enable_windows_utf8_stdio
from security_utils import atomic_write_json


SKILL_ID = "story-cards"
CARDS_SKILL_ROOT = Path(__file__).resolve().parent.parent / "1-Cards"
STATE_REL = Path("STATE.json")
NORTH_STAR_REL = Path("0-Init") / "north_star.yaml"


SECTION_SPECS: Dict[str, Dict[str, Any]] = {
    "styles": {
        "kind": "style",
        "schema_key": "style_card",
        "template_name": "style-card.json",
        "source_skill_id": "story-cards-style",
        "child_skill_path": "风格卡/SKILL.md",
        "child_context_path": "风格卡/CONTEXT.md",
        "child_template_path": "风格卡/templates/style-card.json",
        "source_route": "0-Init > story-cards > 风格卡/SKILL.md",
        "module_route": "story-cards > 风格卡/SKILL.md",
        "index_rel": Path("Cards") / "1-风格卡" / "风格索引.json",
        "bucket_dirs": {
            "global_styles": "总风格",
        },
        "bucket_labels": {
            "global_styles": "global_style",
        },
        "link_fields": ("style_contract_refs",),
    },
    "characters": {
        "kind": "character",
        "schema_key": "character_card",
        "template_name": "character-card.json",
        "source_skill_id": "story-cards-character",
        "child_skill_path": "角色卡/SKILL.md",
        "child_context_path": "角色卡/CONTEXT.md",
        "child_template_path": "角色卡/templates/character-card.json",
        "source_route": "0-Init > story-cards > 角色卡/SKILL.md",
        "module_route": "story-cards > 角色卡/SKILL.md",
        "index_rel": Path("Cards") / "2-角色卡" / "角色索引.json",
        "bucket_dirs": {
            "protagonists": "主要角色",
            "antagonists": "反派角色",
            "supporting": "次要角色",
            "ensemble": "群像角色",
        },
        "bucket_labels": {
            "protagonists": "protagonist",
            "antagonists": "antagonist",
            "supporting": "supporting",
            "ensemble": "ensemble",
        },
        "link_fields": ("relationship_edges",),
    },
    "scenes": {
        "kind": "scene",
        "schema_key": "scene_card",
        "template_name": "scene-card.json",
        "source_skill_id": "story-cards-scene",
        "child_skill_path": "场景卡/SKILL.md",
        "child_context_path": "场景卡/CONTEXT.md",
        "child_template_path": "场景卡/templates/scene-card.json",
        "source_route": "0-Init > story-cards > 场景卡/SKILL.md",
        "module_route": "story-cards > 场景卡/SKILL.md",
        "index_rel": Path("Cards") / "3-场景卡" / "场景索引.json",
        "bucket_dirs": {
            "indoor": "室内",
            "outdoor": "室外",
            "natural": "自然",
            "surreal": "超现实",
        },
        "bucket_labels": {
            "indoor": "indoor",
            "outdoor": "outdoor",
            "natural": "natural",
            "surreal": "surreal",
        },
        "link_fields": ("scene_links",),
    },
    "items": {
        "kind": "item",
        "schema_key": "item_card",
        "template_name": "item-card.json",
        "source_skill_id": "story-cards-item",
        "child_skill_path": "物品卡/SKILL.md",
        "child_context_path": "物品卡/CONTEXT.md",
        "child_template_path": "物品卡/templates/item-card.json",
        "source_route": "0-Init > story-cards > 物品卡/SKILL.md",
        "module_route": "story-cards > 物品卡/SKILL.md",
        "index_rel": Path("Cards") / "4-物品卡" / "物品索引.json",
        "bucket_dirs": {
            "weapons_equipment": "武器装备",
            "clue_items": "线索物品",
            "narrative_items": "重要叙事物品",
            "relics": "文物",
            "adornments": "点缀物",
        },
        "bucket_labels": {
            "weapons_equipment": "weapons_equipment",
            "clue_items": "clue_items",
            "narrative_items": "narrative_items",
            "relics": "relics",
            "adornments": "adornments",
        },
        "link_fields": ("ownership_links", "exclusive_item_hooks"),
    },
}

VALID_MODES = {"full-build", "incremental-writeback", "coverage-repair", "source-contract-fix"}


def _load_json(path: Path) -> Dict[str, Any]:
    if not path.is_file():
        return {}
    if path.suffix in {".yaml", ".yml"}:
        raw = yaml.safe_load(path.read_text(encoding="utf-8"))
    else:
        raw = json.loads(path.read_text(encoding="utf-8"))
    return raw if isinstance(raw, dict) else {}


def _safe_dict(value: Any) -> Dict[str, Any]:
    return value if isinstance(value, dict) else {}


def _safe_list(value: Any) -> List[Any]:
    return value if isinstance(value, list) else []


def _deep_merge(base: Dict[str, Any], patch: Dict[str, Any]) -> Dict[str, Any]:
    for key, value in patch.items():
        if isinstance(value, dict) and isinstance(base.get(key), dict):
            _deep_merge(base[key], value)
        else:
            base[key] = copy.deepcopy(value)
    return base


def _load_template(template_path_rel: str) -> Dict[str, Any]:
    template_path = CARDS_SKILL_ROOT / template_path_rel
    if not template_path.is_file():
        raise FileNotFoundError(f"未找到模板: {template_path}")
    return json.loads(template_path.read_text(encoding="utf-8"))


def _now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def _build_loaded_references(spec: Dict[str, Any]) -> List[str]:
    return [
        "SKILL.md",
        "CONTEXT.md",
        str(spec["child_skill_path"]),
        str(spec["child_context_path"]),
        str(spec["child_template_path"]),
    ]


def _normalize_boundary_notes(payload: Dict[str, Any], section_payload: Dict[str, Any]) -> List[str]:
    notes: List[str] = []
    for source in (payload.get("boundary_notes"), section_payload.get("boundary_notes")):
        if isinstance(source, list):
            notes.extend(str(item) for item in source if str(item).strip())
    return notes


def _project_name(project_root: Path, payload: Dict[str, Any]) -> str:
    explicit = str(payload.get("project_name") or "").strip()
    if explicit:
        return explicit

    state = _load_json(project_root / STATE_REL)
    project_info = _safe_dict(state.get("project_info"))
    for key in ("title", "project_name"):
        value = str(project_info.get(key) or "").strip()
        if value:
            return value

    north_star = _load_json(project_root / NORTH_STAR_REL)
    project_identity = _safe_dict(north_star.get("project_identity"))
    for key in ("title", "project_name", "book_title"):
        value = str(project_identity.get(key) or "").strip()
        if value:
            return value
    return project_root.name


def _normalize_sections(payload: Dict[str, Any]) -> Dict[str, Dict[str, Any]]:
    sections = _safe_dict(payload.get("sections"))
    normalized: Dict[str, Dict[str, Any]] = {}
    for section_name in SECTION_SPECS:
        section_payload = _safe_dict(sections.get(section_name) or payload.get(section_name))
        if section_payload:
            normalized[section_name] = section_payload
    return normalized


def _require_valid_payload(payload: Dict[str, Any], sections: Dict[str, Dict[str, Any]]) -> str:
    mode = str(payload.get("mode") or "").strip()
    if mode not in VALID_MODES:
        raise ValueError(f"`mode` 非法，必须属于 {sorted(VALID_MODES)}")
    if not sections:
        raise ValueError("至少需要提供一个 cards section。")
    if mode == "full-build":
        missing = [name for name in SECTION_SPECS if name not in sections]
        if missing:
            raise ValueError(f"`full-build` 必须同时提供 styles/characters/scenes/items；当前缺少: {missing}")
    return mode


def _default_gate_summary(template: Dict[str, Any], override: Dict[str, Any]) -> Dict[str, Any]:
    gate_summary = copy.deepcopy(_safe_dict(template.get("gate_summary")))
    _deep_merge(gate_summary, override)
    gate_summary.setdefault("status", "REVIEW_REQUIRED")
    gate_summary.setdefault("total_score", 0)
    gate_summary.setdefault("max_score", 60)
    gate_summary.setdefault("fail_codes", [])
    gate_summary.setdefault("repair_entry", "")
    return gate_summary


def _default_execution_notes(template: Dict[str, Any], override: Dict[str, Any]) -> Dict[str, Any]:
    execution_notes = copy.deepcopy(_safe_dict(template.get("execution_notes")))
    _deep_merge(execution_notes, override)
    execution_notes.setdefault("design_rationale", "")
    execution_notes.setdefault("risk_notes", "")
    return execution_notes


def _safe_file_stem(raw: str) -> str:
    stem = str(raw or "").strip().replace("/", "-").replace("\\", "-")
    return stem or "unnamed-card"


def _card_filename(card: Dict[str, Any], entry: Dict[str, Any]) -> str:
    explicit_name = str(entry.get("file_name") or "").strip()
    if explicit_name:
        return explicit_name if explicit_name.endswith(".json") else f"{explicit_name}.json"

    explicit_stem = str(entry.get("file_stem") or "").strip()
    if explicit_stem:
        return f"{_safe_file_stem(explicit_stem)}.json"

    identity = _safe_dict(card.get("core", {}).get("identity"))
    name = str(identity.get("name") or card.get("card_id") or "").strip()
    return f"{_safe_file_stem(name)}.json"


def _new_index_groups(spec: Dict[str, Any]) -> Dict[str, List[str]]:
    return {bucket: [] for bucket in spec["bucket_dirs"]}


def _normalize_existing_groups(existing: Dict[str, Any], spec: Dict[str, Any]) -> Dict[str, List[str]]:
    groups = _safe_dict(existing.get("card_groups"))
    normalized = _new_index_groups(spec)
    for bucket in normalized:
        normalized[bucket] = [str(item) for item in _safe_list(groups.get(bucket)) if isinstance(item, str) and str(item).strip()]
    return normalized


def _prepare_trace_block(
    *,
    spec: Dict[str, Any],
    mode: str,
    target_paths: List[str],
    upstream_patch_required: bool,
    boundary_notes: List[str],
) -> Dict[str, Any]:
    return {
        "module_route": str(spec["module_route"]),
        "loaded_references": _build_loaded_references(spec),
        "writeback_plan": {
            "mode": mode,
            "target_paths": target_paths,
            "upstream_patch_required": upstream_patch_required,
            "boundary_notes": boundary_notes,
        },
    }


def _build_card_payload(
    *,
    project_name: str,
    created_at: str,
    mode: str,
    section_name: str,
    section_payload: Dict[str, Any],
    entry: Dict[str, Any],
) -> tuple[Path, Dict[str, Any], str]:
    spec = SECTION_SPECS[section_name]
    template = _load_template(str(spec["child_template_path"]))
    payload = copy.deepcopy(template)
    content = _safe_dict(payload.setdefault("content", {}))
    card_schema = _safe_dict(content.setdefault("card_schema", {}))
    raw_card = copy.deepcopy(_safe_dict(entry.get("card")))
    if not raw_card:
        raise ValueError(f"{section_name} 存在缺少 `card` 的条目。")

    bucket = str(entry.get("bucket") or "").strip()
    if bucket not in spec["bucket_dirs"]:
        raise ValueError(f"{section_name} 存在非法 bucket: {bucket}")

    file_name = _card_filename(raw_card, entry)
    bucket_dir = spec["bucket_dirs"][bucket]
    card_rel = spec["index_rel"].parent / bucket_dir / file_name
    boundary_notes = _normalize_boundary_notes(section_payload, entry)
    upstream_patch_required = bool(
        entry.get("upstream_patch_required", section_payload.get("upstream_patch_required", False))
    )

    payload.setdefault("meta", {})
    payload["meta"]["skill_id"] = SKILL_ID
    payload["meta"]["source_skill_id"] = str(spec["source_skill_id"])
    payload["meta"]["project_name"] = project_name
    payload["meta"]["created_at"] = created_at
    payload["meta"]["source_route"] = str(spec["source_route"])

    content.update(
        _prepare_trace_block(
            spec=spec,
            mode=mode,
            target_paths=[str(card_rel), str(spec["index_rel"])],
            upstream_patch_required=upstream_patch_required,
            boundary_notes=boundary_notes,
        )
    )
    content["card_groups"] = _new_index_groups(spec)
    for field_name in spec["link_fields"]:
        content[field_name] = []

    raw_card.setdefault("card_id", Path(file_name).stem)
    raw_card.setdefault("card_type", spec["kind"])
    raw_card.setdefault("group", spec["bucket_labels"][bucket])
    card_schema[spec["schema_key"]] = raw_card

    content_patch = _safe_dict(entry.get("content_patch"))
    if content_patch:
        _deep_merge(content, content_patch)

    payload["gate_summary"] = _default_gate_summary(template, _safe_dict(entry.get("gate_summary")))
    payload["execution_notes"] = _default_execution_notes(template, _safe_dict(entry.get("execution_notes")))
    return card_rel, payload, bucket


def _build_index_payload(
    *,
    project_root: Path,
    project_name: str,
    created_at: str,
    mode: str,
    section_name: str,
    section_payload: Dict[str, Any],
    card_refs_by_bucket: Dict[str, List[str]],
) -> Dict[str, Any]:
    spec = SECTION_SPECS[section_name]
    template = _load_template(str(spec["child_template_path"]))
    existing = _load_json(project_root / spec["index_rel"])
    replace_existing = bool(section_payload.get("replace_existing", mode != "incremental-writeback"))

    payload = copy.deepcopy(template)
    if existing and not replace_existing:
        _deep_merge(payload, existing)
    content = _safe_dict(payload.setdefault("content", {}))
    payload.setdefault("meta", {})
    payload["meta"]["skill_id"] = SKILL_ID
    payload["meta"]["source_skill_id"] = str(spec["source_skill_id"])
    payload["meta"]["project_name"] = project_name
    payload["meta"]["created_at"] = created_at
    payload["meta"]["source_route"] = str(spec["source_route"])

    content.update(
        _prepare_trace_block(
            spec=spec,
            mode=mode,
            target_paths=[str(spec["index_rel"])],
            upstream_patch_required=bool(section_payload.get("upstream_patch_required", False)),
            boundary_notes=_normalize_boundary_notes({"boundary_notes": []}, section_payload),
        )
    )
    content["card_schema"] = {}

    if replace_existing:
        groups = _new_index_groups(spec)
    else:
        groups = _normalize_existing_groups(content, spec)

    for bucket, refs in card_refs_by_bucket.items():
        for ref in refs:
            for group_refs in groups.values():
                if ref in group_refs:
                    group_refs.remove(ref)
            if ref not in groups[bucket]:
                groups[bucket].append(ref)
    content["card_groups"] = groups

    for field_name in spec["link_fields"]:
        if replace_existing or field_name in section_payload:
            content[field_name] = copy.deepcopy(_safe_list(section_payload.get(field_name)))
        else:
            content[field_name] = _safe_list(content.get(field_name))

    if replace_existing or "current_focus" in section_payload:
        content["current_focus"] = copy.deepcopy(_safe_dict(section_payload.get("current_focus")))
    else:
        content["current_focus"] = _safe_dict(content.get("current_focus"))

    content_patch = _safe_dict(section_payload.get("content_patch"))
    if content_patch:
        _deep_merge(content, content_patch)

    payload["gate_summary"] = _default_gate_summary(template, _safe_dict(section_payload.get("gate_summary")))
    payload["execution_notes"] = _default_execution_notes(template, _safe_dict(section_payload.get("execution_notes")))
    return payload


def write_cards_payload(project_root: Path, payload: Dict[str, Any], *, run_gate: bool = False) -> Dict[str, Any]:
    sections = _normalize_sections(payload)
    mode = _require_valid_payload(payload, sections)
    project_name = _project_name(project_root, payload)
    created_at = _now_iso()

    written_files: List[str] = []
    section_reports: Dict[str, Dict[str, Any]] = {}

    for section_name, section_payload in sections.items():
        spec = SECTION_SPECS[section_name]
        cards = _safe_list(section_payload.get("cards"))
        card_refs_by_bucket = _new_index_groups(spec)

        for entry_value in cards:
            entry = _safe_dict(entry_value)
            card_rel, card_payload, bucket = _build_card_payload(
                project_name=project_name,
                created_at=created_at,
                mode=mode,
                section_name=section_name,
                section_payload=section_payload,
                entry=entry,
            )
            atomic_write_json(project_root / card_rel, card_payload, use_lock=True, backup=False)
            written_files.append(str(card_rel))
            card_refs_by_bucket[bucket].append(str(card_rel))

        index_payload = _build_index_payload(
            project_root=project_root,
            project_name=project_name,
            created_at=created_at,
            mode=mode,
            section_name=section_name,
            section_payload=section_payload,
            card_refs_by_bucket=card_refs_by_bucket,
        )
        atomic_write_json(project_root / spec["index_rel"], index_payload, use_lock=True, backup=False)
        written_files.append(str(spec["index_rel"]))

        section_reports[section_name] = {
            "index_path": str(spec["index_rel"]),
            "written_cards": sum(len(refs) for refs in card_refs_by_bucket.values()),
            "module_route": str(spec["module_route"]),
            "loaded_references": _build_loaded_references(spec),
            "card_refs_by_bucket": card_refs_by_bucket,
        }

    gate_report: Optional[Dict[str, Any]] = None
    if run_gate:
        gate_report = build_cards_coverage_report(project_root)
        section_to_report_key = {
            "styles": "styles",
            "characters": "characters",
            "scenes": "scenes",
            "items": "items",
        }
        for section_name, report_key in section_to_report_key.items():
            if section_name not in sections:
                continue
            spec = SECTION_SPECS[section_name]
            index_path = project_root / spec["index_rel"]
            index_payload = _load_json(index_path)
            if not index_payload:
                continue
            section_gate = _safe_dict(gate_report.get("sections", {}).get(report_key))
            blocking_findings = _safe_list(section_gate.get("blocking_findings"))
            gate_summary = _safe_dict(index_payload.get("gate_summary"))
            gate_summary["status"] = "PASS" if section_gate.get("ok") else "FAIL-QUALITY"
            gate_summary["fail_codes"] = [str(item.get("code")) for item in blocking_findings if isinstance(item, dict) and item.get("code")]
            gate_summary["repair_entry"] = gate_summary["fail_codes"][0] if gate_summary["fail_codes"] else ""
            index_payload["gate_summary"] = gate_summary
            atomic_write_json(index_path, index_payload, use_lock=True, backup=False)

    ok = bool(gate_report["ok"]) if gate_report is not None else True
    return {
        "ok": ok,
        "project_root": str(project_root),
        "project_name": project_name,
        "mode": mode,
        "written_files": written_files,
        "sections": section_reports,
        "gate_report": gate_report,
    }


def parse_args(argv: Optional[List[str]] = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Write story2026 1-Cards payloads into canonical JSON outputs")
    parser.add_argument("--project-root", help="书项目根目录或工作区根目录（可选，默认自动检测）")
    parser.add_argument("--data", required=True, help="cards payload，支持 JSON 字符串或 @payload.json")
    parser.add_argument("--run-gate", action="store_true", help="写入后立即执行 cards-check，并回填索引 gate_summary")
    parser.add_argument("--format", choices=["text", "json"], default="text", help="输出格式")
    return parser.parse_args(argv)


def _print_text_report(report: Dict[str, Any]) -> None:
    status = "PASS" if report["ok"] else "FAIL-QUALITY"
    print(f"{status} cards write: {report['project_root']}")
    print(f"mode: {report['mode']}")
    for section_name, section in report["sections"].items():
        print(f"- {section_name}: {section['written_cards']} cards -> {section['index_path']}")
    if report["gate_report"] is not None:
        blocking = len(_safe_list(report["gate_report"].get("blocking_findings")))
        print(f"gate: {'PASS' if report['gate_report'].get('ok') else 'FAIL-QUALITY'} ({blocking} blocking findings)")


def main(argv: Optional[List[str]] = None) -> int:
    args = parse_args(argv)
    project_root = resolve_project_root(args.project_root) if args.project_root else resolve_project_root()
    payload = load_json_arg(args.data)
    if not isinstance(payload, dict):
        raise ValueError("cards payload 顶层必须是 JSON object。")
    report = write_cards_payload(project_root, payload, run_gate=args.run_gate)
    if args.format == "json":
        print(json.dumps(report, ensure_ascii=False, indent=2))
    else:
        _print_text_report(report)
    return 0 if report["ok"] else 1


if __name__ == "__main__":
    enable_windows_utf8_stdio(skip_in_pytest=True)
    raise SystemExit(main())
