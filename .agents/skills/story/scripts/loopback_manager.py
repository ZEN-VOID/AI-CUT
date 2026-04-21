#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
story2026 validated actualization manager.

只负责 `5-Loopback` 的 PASS-only 回写闭环：
- 生成 loopback artifact
- 回写 Cards.current_state/history
- 回写 story_map.actualization
- 刷新下一轮 projection / runtime markers
"""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import re
from pathlib import Path
from typing import Any, Dict, Iterable, List, Tuple

from planning_paths import canonical_planning_artifact_relpath, resolve_planning_artifact_path
from project_locator import resolve_project_root, resolve_state_file
from runtime_compat import enable_windows_utf8_stdio
from security_utils import atomic_write_json, create_secure_directory, sanitize_filename


def _scripts_dir() -> Path:
    return Path(__file__).resolve().parent


def _story2026_root() -> Path:
    return _scripts_dir().parent


def _template_path() -> Path:
    return _story2026_root() / "5-Loopback" / "templates" / "loopback.json"


def _load_json_file(path: Path) -> Dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def _load_json_arg(raw: str) -> Dict[str, Any]:
    if raw.startswith("@"):
        return _load_json_file(Path(raw[1:]))
    return json.loads(raw)


def _deep_merge(base: Dict[str, Any], patch: Dict[str, Any]) -> Dict[str, Any]:
    merged = copy.deepcopy(base)
    for key, value in patch.items():
        if isinstance(value, dict) and isinstance(merged.get(key), dict):
            merged[key] = _deep_merge(merged[key], value)
        else:
            merged[key] = copy.deepcopy(value)
    return merged


def _project_name(project_root: Path, state: Dict[str, Any]) -> str:
    project_info = state.get("project_info", {}) if isinstance(state.get("project_info"), dict) else {}
    raw_name = (
        project_info.get("title")
        or project_info.get("name")
        or project_info.get("project_name")
        or project_root.name
    )
    return sanitize_filename(str(raw_name), max_length=80)


def _relpath(path: Path, project_root: Path) -> str:
    try:
        return str(path.relative_to(project_root))
    except ValueError:
        return str(path)


def _episode_ref_candidates(episode: int) -> List[str]:
    return [f"第{episode}集", f"第{episode:03d}集"]


def _build_artifact_path(project_root: Path, state: Dict[str, Any], episode: int) -> Path:
    output_dir = project_root / "5-Loopback"
    create_secure_directory(str(output_dir))
    return output_dir / f"第{episode}集.loopback.json"


def _load_template() -> Dict[str, Any]:
    path = _template_path()
    if not path.is_file():
        raise FileNotFoundError(f"缺少 loopback 模板: {path}")
    return _load_json_file(path)


def _normalize_delta_payload(
    validation_payload: Dict[str, Any],
    explicit_delta: Dict[str, Any] | None,
) -> Dict[str, List[Dict[str, Any]]]:
    if explicit_delta is not None:
        source = explicit_delta
    else:
        source = (
            validation_payload.get("loopback_delta")
            if isinstance(validation_payload.get("loopback_delta"), dict)
            else validation_payload
        )

    return {
        "card_deltas": list(source.get("card_deltas") or []),
        "map_deltas": list(source.get("map_deltas") or []),
        "projection_refresh": list(source.get("projection_refresh") or []),
        "evidence_refs": list(source.get("evidence_refs") or []),
    }


def _validate_allowed_keys(payload: Dict[str, Any], allowed_keys: set[str], context: str) -> None:
    extra_keys = sorted(set(payload.keys()) - allowed_keys)
    if extra_keys:
        raise ValueError(f"{context} 存在未授权字段: {', '.join(extra_keys)}")


def _ensure_json_like(value: Any, context: str) -> None:
    try:
        json.dumps(value, ensure_ascii=False)
    except TypeError as exc:
        raise ValueError(f"{context} 不是合法 JSON 值") from exc


def _normalize_handoff_targets(raw: Any) -> List[str]:
    if not isinstance(raw, list):
        return []
    normalized: List[str] = []
    for item in raw:
        value = str(item or "").strip()
        if value:
            normalized.append(value)
    return normalized


def _normalize_handoff_target_token(raw: str) -> str:
    return raw.strip().rstrip("/").replace("\\", "/").lower()


def _loopback_handoff_granted(
    validation_payload: Dict[str, Any],
) -> tuple[str, List[str], bool, List[str]]:
    routing_decision = str(validation_payload.get("routing_decision") or "").strip()
    handoff_targets = _normalize_handoff_targets(validation_payload.get("handoff_targets"))
    normalized_targets = {_normalize_handoff_target_token(item) for item in handoff_targets}
    loopback_aliases = {"5-loopback", "story-loopback"}
    review_aliases = {"review", "story-review"}

    fail_codes: List[str] = []
    if routing_decision != "handoff_to_review_and_loopback":
        fail_codes.append("routing_decision_must_be_handoff_to_review_and_loopback")
    if not (normalized_targets & review_aliases):
        fail_codes.append("handoff_targets_missing_review")
    if not (normalized_targets & loopback_aliases):
        fail_codes.append("handoff_targets_missing_loopback")

    return routing_decision, handoff_targets, not fail_codes, fail_codes


def _extract_governance_refs(validation_payload: Dict[str, Any]) -> Dict[str, str]:
    source = (
        validation_payload.get("governance_refs")
        if isinstance(validation_payload.get("governance_refs"), dict)
        else {}
    )
    refs: Dict[str, str] = {}
    for key in ("validation_report_ref", "artifact_manifest_ref", "mission_brief_ref"):
        raw = source.get(key, validation_payload.get(key))
        value = str(raw or "").strip()
        refs[key] = value
    return refs


def _validate_card_delta(item: Dict[str, Any]) -> None:
    _validate_allowed_keys(
        item,
        {"target_ref", "target_type", "write_policy", "current_state_patch", "history_append", "expected_revision"},
        "card_delta",
    )
    if item.get("write_policy") not in (None, "", "validated-current-state-history-only"):
        raise ValueError("card_delta.write_policy 非法")
    current_state_patch = item.get("current_state_patch") or {}
    if current_state_patch and not isinstance(current_state_patch, dict):
        raise ValueError("card_delta.current_state_patch 必须是对象")
    forbidden_current_state_keys = {
        "core",
        "card_schema",
        "history",
        "current_state",
        "writeback_plan",
        "gate_summary",
        "execution_notes",
        "meta",
        "content",
        "review_metrics",
        "review_handoff_summary",
        "validation_status",
        "routing_decision",
        "handoff_targets",
    }
    current_state_keys = set(current_state_patch.keys()) if isinstance(current_state_patch, dict) else set()
    illegal_current_state = sorted(current_state_keys & forbidden_current_state_keys)
    if illegal_current_state:
        raise ValueError(f"card_delta.current_state_patch 存在越权字段: {', '.join(illegal_current_state)}")
    _ensure_json_like(current_state_patch, "card_delta.current_state_patch")

    history_append = item.get("history_append") or {}
    if history_append and not isinstance(history_append, dict):
        raise ValueError("card_delta.history_append 必须是对象")
    if history_append:
        _validate_allowed_keys(
            history_append,
            {
                "episode_ref",
                "loopback_ref",
                "validation_ref",
                "changed_fields",
                "change_summary",
                "impact_scope",
                "evidence_refs",
                "timestamp",
                "growth_delta",
            },
            "card_delta.history_append",
        )
        _ensure_json_like(history_append, "card_delta.history_append")


def _validate_map_delta(item: Dict[str, Any]) -> None:
    _validate_allowed_keys(
        item,
        {"target_bucket", "target_ref", "slice_ref", "write_policy", "actualization_patch", "expected_revision"},
        "map_delta",
    )
    if item.get("write_policy") not in (None, "", "actualization-only"):
        raise ValueError("map_delta.write_policy 非法")
    actualization_patch = item.get("actualization_patch") or {}
    if actualization_patch and not isinstance(actualization_patch, dict):
        raise ValueError("map_delta.actualization_patch 必须是对象")
    forbidden_map_keys = {
        "issues",
        "severity_counts",
        "critical_issues",
        "overall_score",
        "review_metrics",
        "review_handoff_summary",
        "validation_status",
        "routing_decision",
        "handoff_targets",
        "suggested_fix",
        "source_fix",
        "draft_rewrite",
    }
    illegal_map_keys = sorted(
        key for key in actualization_patch.keys() if key in forbidden_map_keys or key.startswith("planned_")
    )
    if illegal_map_keys:
        raise ValueError(f"map_delta.actualization_patch 存在越权字段: {', '.join(illegal_map_keys)}")
    _ensure_json_like(actualization_patch, "map_delta.actualization_patch")


def _validate_projection_refresh_entry(item: Dict[str, Any]) -> None:
    _validate_allowed_keys(
        item,
        {"target_ref", "target_type", "refresh_mode", "payload", "expected_revision"},
        "projection_refresh",
    )
    if not str(item.get("target_type") or "").strip():
        raise ValueError("projection_refresh.target_type 不能为空")
    _ensure_json_like(item.get("payload"), "projection_refresh.payload")
    if item.get("target_type") == "runtime_marker" and not isinstance(item.get("payload") or {}, dict):
        raise ValueError("runtime_marker payload 必须是对象")


def _validate_delta_payload(delta_payload: Dict[str, List[Dict[str, Any]]]) -> None:
    for item in delta_payload["card_deltas"]:
        if isinstance(item, dict):
            _validate_card_delta(item)
    for item in delta_payload["map_deltas"]:
        if isinstance(item, dict):
            _validate_map_delta(item)
    for item in delta_payload["projection_refresh"]:
        if isinstance(item, dict):
            _validate_projection_refresh_entry(item)


def _map_bucket_key(bucket: str) -> str:
    mapping = {
        "episode_nodes": "episode_ref",
        "clue_points": "clue_ref",
        "foreshadow_points": "foreshadow_ref",
        "promise_threads": "thread_ref",
        "suspense_threads": "thread_ref",
        "tasklines": "taskline_ref",
        "threads": "thread_ref",
    }
    if bucket not in mapping:
        raise ValueError(f"不支持的 map bucket: {bucket}")
    return mapping[bucket]


def _default_projection_path(target_type: str) -> list[str]:
    mapping = {
        "writer_projection": ["setting_route_packet", "writer_context_projection", "memory_projection"],
        "planning_projection": ["planning_projection"],
        "query_projection": ["query_projection"],
        "carryover_context": ["carryover_context"],
    }
    if target_type not in mapping:
        raise ValueError(f"不支持的 projection target_type: {target_type}")
    return list(mapping[target_type])


def _get_loopback_state_owner(payload: Dict[str, Any], target_path: Path) -> Dict[str, Any]:
    content = payload.get("content")
    card_schema = content.get("card_schema") if isinstance(content, dict) else None
    if isinstance(card_schema, dict):
        for schema_key in (
            "character_card",
            "item_card",
            "scene_card",
            "style_card",
            "global_card",
        ):
            candidate = card_schema.get(schema_key)
            if isinstance(candidate, dict):
                return candidate
        raise ValueError(f"Card 缺少受支持的 card_schema 节点: {target_path}")
    return payload


def _projection_path_suffix(target_ref: str) -> List[str]:
    ref = str(target_ref or "").strip()
    if not ref:
        return []
    return [part for part in re.split(r"[/.]+", ref) if part]


def _get_nested_value(payload: Dict[str, Any], path: Iterable[str]) -> Any:
    current: Any = payload
    for part in path:
        if not isinstance(current, dict) or part not in current:
            return None
        current = current[part]
    return copy.deepcopy(current)


def _set_nested_value(payload: Dict[str, Any], path: Iterable[str], value: Any) -> None:
    parts = [part for part in path if part]
    if not parts:
        raise ValueError("nested path 不能为空")

    current = payload
    for part in parts[:-1]:
        next_value = current.get(part)
        if not isinstance(next_value, dict):
            next_value = {}
            current[part] = next_value
        current = next_value
    current[parts[-1]] = copy.deepcopy(value)


def _apply_refresh_mode(existing: Any, refresh_mode: str, payload: Any) -> Any:
    mode = str(refresh_mode or "replace").strip().lower() or "replace"
    if mode == "replace":
        return copy.deepcopy(payload)
    if mode == "merge":
        if existing is None:
            existing = {}
        if not isinstance(existing, dict) or not isinstance(payload, dict):
            raise ValueError("merge 模式要求 existing/payload 都是对象")
        return _deep_merge(existing, payload)
    if mode == "append":
        if existing is None:
            existing = []
        if not isinstance(existing, list):
            raise ValueError("append 模式要求 existing 是数组")
        merged = copy.deepcopy(existing)
        if isinstance(payload, list):
            merged.extend(copy.deepcopy(payload))
        else:
            merged.append(copy.deepcopy(payload))
        return merged
    raise ValueError(f"不支持的 refresh_mode: {refresh_mode}")


def _normalize_revision(value: Any, context: str) -> int:
    if value in (None, ""):
        return 0
    try:
        revision = int(value)
    except (TypeError, ValueError) as exc:
        raise ValueError(f"{context} 必须是整数 revision") from exc
    if revision < 0:
        raise ValueError(f"{context} 不能为负数")
    return revision


def _get_card_revision(payload: Dict[str, Any], target_path: Path) -> int:
    state_owner = _get_loopback_state_owner(payload, target_path)
    return _normalize_revision(state_owner.get("loopback_revision"), f"{target_path} loopback_revision")


def _set_card_revision(payload: Dict[str, Any], target_path: Path, revision: int) -> None:
    state_owner = _get_loopback_state_owner(payload, target_path)
    state_owner["loopback_revision"] = revision


def _actualization_defaults() -> Dict[str, Any]:
    return {
        "write_policy": "actualization-only",
        "episode_nodes": [],
        "clue_points": [],
        "foreshadow_points": [],
        "promise_threads": [],
        "suspense_threads": [],
        "tasklines": [],
        "threads": [],
    }


def _get_map_actualization_root(payload: Dict[str, Any]) -> Dict[str, Any]:
    content = payload.setdefault("content", {})
    holomap_slice = content.get("holomap_slice")
    if isinstance(holomap_slice, dict):
        return holomap_slice.setdefault("actualization", _actualization_defaults())
    return content.setdefault("holomap", {}).setdefault("actualization", _actualization_defaults())


def _get_map_revision(payload: Dict[str, Any]) -> int:
    actualization = _get_map_actualization_root(payload)
    return _normalize_revision(actualization.get("revision"), "story_map.actualization.revision")


def _set_map_revision(payload: Dict[str, Any], revision: int) -> None:
    actualization = _get_map_actualization_root(payload)
    actualization["revision"] = revision


def _resolve_slice_ref(
    holomap_payload: Dict[str, Any],
    episode: int,
    map_deltas: List[Dict[str, Any]],
) -> str:
    explicit_refs = {
        str(item.get("slice_ref") or "").strip()
        for item in map_deltas
        if isinstance(item, dict) and str(item.get("slice_ref") or "").strip()
    }
    if len(explicit_refs) > 1:
        raise ValueError("map_deltas 指向多个 slice_ref，当前 loopback 只支持单集写回一个 slice")
    if explicit_refs:
        return next(iter(explicit_refs))

    holomap = _safe_holomap(holomap_payload)
    episode_axis = holomap.get("episode_sequence_axis") or []
    candidates = set(_episode_ref_candidates(episode))
    for row in episode_axis:
        if not isinstance(row, dict):
            continue
        if str(row.get("episode_ref") or "").strip() in candidates:
            return str(row.get("slice_ref") or "").strip()
    return ""


def _safe_holomap(holomap_payload: Dict[str, Any]) -> Dict[str, Any]:
    content = holomap_payload.get("content")
    if not isinstance(content, dict):
        return {}
    holomap = content.get("holomap")
    return holomap if isinstance(holomap, dict) else {}


def _resolve_slice_path(
    project_root: Path,
    holomap_payload: Dict[str, Any],
    slice_ref: str,
) -> Path | None:
    if not slice_ref:
        return None

    holomap = _safe_holomap(holomap_payload)
    manifest = holomap.get("episode_slice_manifest") or []
    file_ref = ""
    for row in manifest:
        if not isinstance(row, dict):
            continue
        if str(row.get("slice_id") or "").strip() == slice_ref:
            file_ref = str(row.get("file_ref") or "").strip()
            break
    if not file_ref:
        return None

    rel = file_ref if file_ref.startswith("2-Planning/") else f"2-Planning/{file_ref}"
    path = project_root / rel
    return path if path.is_file() else None


def _resolve_episode_ref_for_summary(holomap_payload: Dict[str, Any], episode: int) -> str:
    holomap = _safe_holomap(holomap_payload)
    episode_axis = holomap.get("episode_sequence_axis") or []
    candidates = set(_episode_ref_candidates(episode))
    for row in episode_axis:
        if not isinstance(row, dict):
            continue
        value = str(row.get("episode_ref") or "").strip()
        if value in candidates:
            return value
    return f"第{episode:03d}集"


def _upsert_status_entry(entries: List[Dict[str, Any]], key: str, value: str, patch: Dict[str, Any]) -> None:
    match = None
    for row in entries:
        if isinstance(row, dict) and str(row.get(key) or "").strip() == value:
            match = row
            break
    if match is None:
        item = {key: value}
        item.update(copy.deepcopy(patch))
        entries.append(item)
    else:
        match.update(copy.deepcopy(patch))


def _refresh_root_actualization_indexes(
    holomap_payload: Dict[str, Any],
    *,
    episode: int,
    slice_ref: str,
    validation_ref: str,
    artifact_ref: str,
) -> List[str]:
    actualization = _get_map_actualization_root(holomap_payload)
    episode_entries = actualization.setdefault("episode_status_index", [])
    slice_entries = actualization.setdefault("slice_status_index", [])
    if not isinstance(episode_entries, list) or not isinstance(slice_entries, list):
        raise ValueError("story_map.actualization status index 必须为数组")

    episode_ref = _resolve_episode_ref_for_summary(holomap_payload, episode)
    _upsert_status_entry(
        episode_entries,
        "episode_ref",
        episode_ref,
        {
            "status": "completed",
            "validation_ref": validation_ref,
            "loopback_ref": artifact_ref,
        },
    )

    written_refs = [f"episode_status_index:{episode_ref}"]

    if slice_ref:
        holomap = _safe_holomap(holomap_payload)
        episode_axis = holomap.get("episode_sequence_axis") or []
        slice_episode_refs = [
            str(row.get("episode_ref") or "").strip()
            for row in episode_axis
            if isinstance(row, dict) and str(row.get("slice_ref") or "").strip() == slice_ref
        ]
        completed_refs = {
            str(row.get("episode_ref") or "").strip()
            for row in episode_entries
            if isinstance(row, dict) and str(row.get("status") or "").strip() == "completed"
        }
        slice_status = "completed" if slice_episode_refs and set(slice_episode_refs).issubset(completed_refs) else "in_progress"
        _upsert_status_entry(
            slice_entries,
            "slice_id",
            slice_ref,
            {
                "status": slice_status,
                "last_episode_ref": episode_ref,
                "validation_ref": validation_ref,
                "loopback_ref": artifact_ref,
            },
        )
        written_refs.append(f"slice_status_index:{slice_ref}")

    return written_refs


def _get_state_revision(state: Dict[str, Any]) -> int:
    runtime_markers = state.get("runtime_markers")
    if not isinstance(runtime_markers, dict):
        return 0
    return _normalize_revision(runtime_markers.get("loopback_state_revision"), "runtime_markers.loopback_state_revision")


def _set_state_revision(state: Dict[str, Any], revision: int) -> None:
    runtime_markers = state.setdefault("runtime_markers", {})
    if not isinstance(runtime_markers, dict):
        runtime_markers = {}
        state["runtime_markers"] = runtime_markers
    runtime_markers["loopback_state_revision"] = revision


def _apply_projection_refresh(
    state: Dict[str, Any],
    projection_refresh: List[Dict[str, Any]],
) -> List[str]:
    refreshed_refs: List[str] = []
    for item in projection_refresh:
        if not isinstance(item, dict):
            continue

        target_type = str(item.get("target_type") or "").strip()
        payload = copy.deepcopy(item.get("payload") or {})
        target_ref = str(item.get("target_ref") or "").strip()
        refresh_mode = str(item.get("refresh_mode") or "replace").strip()

        if target_type == "runtime_marker":
            nested_path = ["runtime_markers", target_ref or "loopback"]
        else:
            nested_path = _default_projection_path(target_type) + _projection_path_suffix(target_ref)

        existing = _get_nested_value(state, nested_path)
        refreshed_value = _apply_refresh_mode(existing, refresh_mode, payload)
        _set_nested_value(state, nested_path, refreshed_value)
        refreshed_refs.append(".".join(nested_path))

    return refreshed_refs


def _build_commit_manifest(
    *,
    episode: int,
    validation_ref: str,
    artifact_ref: str,
    written_card_refs: List[str],
    written_map_refs: List[str],
    refreshed_projection_refs: List[str],
    observed_revisions: Dict[str, Any],
    next_revisions: Dict[str, Any],
    phase: str,
) -> Dict[str, Any]:
    manifest_seed = json.dumps(
        {
            "episode": episode,
            "validation_ref": validation_ref,
            "artifact_ref": artifact_ref,
            "written_card_refs": written_card_refs,
            "written_map_refs": written_map_refs,
            "refreshed_projection_refs": refreshed_projection_refs,
        },
        ensure_ascii=False,
        sort_keys=True,
    )
    manifest_id = f"loopback-{episode}-{hashlib.sha1(manifest_seed.encode('utf-8')).hexdigest()[:12]}"
    return {
        "manifest_id": manifest_id,
        "phase": phase,
        "episode_ref": f"第{episode}集",
        "validation_ref": validation_ref,
        "artifact_ref": artifact_ref,
        "written_card_refs": copy.deepcopy(written_card_refs),
        "written_map_refs": copy.deepcopy(written_map_refs),
        "refreshed_projection_refs": copy.deepcopy(refreshed_projection_refs),
        "observed_revisions": copy.deepcopy(observed_revisions),
        "next_revisions": copy.deepcopy(next_revisions),
    }


def _apply_map_deltas(
    holomap: Dict[str, Any],
    map_deltas: List[Dict[str, Any]],
) -> Tuple[Dict[str, Any], List[str]]:
    staged_holomap = copy.deepcopy(holomap)
    actualization = _get_map_actualization_root(staged_holomap)

    written_refs: List[str] = []
    for item in map_deltas:
        if not isinstance(item, dict):
            continue

        bucket = str(item.get("target_bucket") or "").strip()
        key_name = _map_bucket_key(bucket)
        patch = copy.deepcopy(item.get("actualization_patch") or {})
        target_ref = str(item.get("target_ref") or "").strip()
        match_value = str(patch.get(key_name) or target_ref or "").strip()
        if not match_value:
            raise ValueError(f"{bucket} 缺少 target_ref/{key_name}")

        entries = actualization.setdefault(bucket, [])
        if not isinstance(entries, list):
            raise ValueError(f"actualization.{bucket} 必须是数组")

        match = None
        for row in entries:
            if isinstance(row, dict) and str(row.get(key_name) or "").strip() == match_value:
                match = row
                break

        if match is None:
            new_entry = copy.deepcopy(patch)
            new_entry.setdefault(key_name, match_value)
            entries.append(new_entry)
        else:
            match.update(patch)

        written_refs.append(f"{bucket}:{target_ref or match_value}")

    return staged_holomap, written_refs


def _apply_card_deltas(
    project_root: Path,
    artifact_ref: str,
    validation_ref: str,
    card_deltas: List[Dict[str, Any]],
) -> Tuple[Dict[Path, Dict[str, Any]], List[str]]:
    staged_payloads: Dict[Path, Dict[str, Any]] = {}
    written_refs: List[str] = []
    for item in card_deltas:
        if not isinstance(item, dict):
            continue

        target_ref = str(item.get("target_ref") or "").strip()
        if not target_ref:
            raise ValueError("card_delta.target_ref 不能为空")

        target_path = (project_root / target_ref).resolve()
        if not target_path.is_file():
            raise FileNotFoundError(f"Card 文件不存在: {target_path}")

        payload = staged_payloads.get(target_path)
        if payload is None:
            payload = _load_json_file(target_path)
        if not isinstance(payload, dict):
            raise ValueError(f"Card JSON 非对象: {target_path}")

        payload = copy.deepcopy(payload)
        state_owner = _get_loopback_state_owner(payload, target_path)

        state_owner.setdefault("current_state", {})
        state_owner.setdefault("history", [])

        current_patch = item.get("current_state_patch") or {}
        if isinstance(current_patch, dict):
            state_owner["current_state"] = _deep_merge(state_owner["current_state"], current_patch)

        history_append = copy.deepcopy(item.get("history_append") or {})
        if history_append:
            history_append.setdefault("validation_ref", validation_ref)
            history_append["loopback_ref"] = artifact_ref
            state_owner["history"].append(history_append)

        staged_payloads[target_path] = payload
        if target_ref not in written_refs:
            written_refs.append(target_ref)

    return staged_payloads, written_refs


def _derive_actual_outcome_summary(map_deltas: List[Dict[str, Any]]) -> str:
    for item in map_deltas:
        if not isinstance(item, dict):
            continue
        patch = item.get("actualization_patch") or {}
        summary = str(patch.get("actual_outcome_summary") or "").strip()
        if summary:
            return summary
    return ""


def _build_artifact(
    template: Dict[str, Any],
    *,
    project_root: Path,
    state: Dict[str, Any],
    episode: int,
    manuscript_ref: str,
    validation_ref: str,
    routing_decision: str,
    handoff_targets: List[str],
    draft_packet_ref: str,
    story_map_ref: str,
    story_map_slice_ref: str,
    delta_payload: Dict[str, List[Dict[str, Any]]],
    artifact_ref: str,
    governance_refs: Dict[str, str],
) -> Dict[str, Any]:
    artifact = copy.deepcopy(template)
    meta = artifact.setdefault("meta", {})
    meta["project_name"] = _project_name(project_root, state)
    meta["episode_ref"] = f"第{episode}集"
    meta["created_at"] = ""
    meta["loopback_ref"] = artifact_ref

    inputs = artifact.setdefault("inputs", {})
    inputs["project_root"] = str(project_root)
    inputs["manuscript_ref"] = manuscript_ref
    inputs["validation_ref"] = validation_ref
    inputs["draft_packet_ref"] = draft_packet_ref
    inputs["story_map_ref"] = story_map_ref
    inputs["story_map_slice_ref"] = story_map_slice_ref
    inputs["validation_status"] = "PASS"
    inputs["routing_decision"] = routing_decision
    inputs["handoff_targets"] = copy.deepcopy(handoff_targets)

    content = artifact.setdefault("content", {})
    loopback_delta = content.setdefault("loopback_delta", {})
    loopback_delta["card_deltas"] = copy.deepcopy(delta_payload["card_deltas"])
    loopback_delta["map_deltas"] = copy.deepcopy(delta_payload["map_deltas"])
    loopback_delta["projection_refresh"] = copy.deepcopy(delta_payload["projection_refresh"])
    loopback_delta["evidence_refs"] = copy.deepcopy(delta_payload["evidence_refs"])
    writeback_summary = content.setdefault("writeback_summary", {})
    writeback_summary.setdefault("written_card_refs", [])
    writeback_summary.setdefault("written_map_refs", [])
    writeback_summary.setdefault("refreshed_projection_refs", [])

    gate_summary = artifact.setdefault("gate_summary", {})
    gate_summary["status"] = "PASS"
    gate_summary["validation_gate"] = "PASS-only"
    gate_summary["handoff_grant"] = "granted"
    gate_summary.setdefault("fail_codes", [])
    gate_summary.setdefault("repair_entry", "")

    execution_notes = artifact.setdefault("execution_notes", {})
    execution_notes["actual_outcome_summary"] = _derive_actual_outcome_summary(delta_payload["map_deltas"])
    execution_notes.setdefault("risk_notes", "")
    execution_notes["governance_refs"] = copy.deepcopy(governance_refs)

    return artifact


def _commit_json_writes(
    write_plan: List[Tuple[Path, Dict[str, Any], bool, bool]],
    originals: Dict[Path, Dict[str, Any] | None],
) -> None:
    written_paths: List[Path] = []
    try:
        for path, payload, use_lock, backup in write_plan:
            atomic_write_json(path, payload, use_lock=use_lock, backup=backup)
            written_paths.append(path)
    except Exception as exc:
        rollback_errors: List[str] = []
        for path in reversed(written_paths):
            original_payload = originals.get(path)
            try:
                if original_payload is None:
                    if path.exists():
                        path.unlink()
                else:
                    atomic_write_json(path, original_payload, use_lock=True, backup=False)
            except Exception as rollback_exc:  # pragma: no cover - 极端 I/O 故障
                rollback_errors.append(f"{path}: {rollback_exc}")

        if rollback_errors:
            raise RuntimeError(
                "loopback writeback 失败，且回滚未完全成功: " + "; ".join(rollback_errors)
            ) from exc
        raise


def actualize(args: argparse.Namespace) -> int:
    project_root = resolve_project_root(str(args.project_root))
    state_path = resolve_state_file(explicit_project_root=str(project_root))
    requested_story_map_rel = str(args.story_map_ref or "").strip()
    story_map_rel = requested_story_map_rel or canonical_planning_artifact_relpath("holomap")
    if requested_story_map_rel:
        story_map_path = project_root / requested_story_map_rel
    else:
        story_map_path = resolve_planning_artifact_path(project_root, "holomap")

    if not state_path.is_file():
        raise SystemExit(f"缺少 STATE.json: {state_path}")
    if not story_map_path.is_file():
        raise SystemExit(f"缺少 story_map: {story_map_path}")

    state = _load_json_file(state_path)
    validation_payload = _load_json_arg(args.validation_data)
    validation_status = str(validation_payload.get("validation_status") or "").strip()
    if validation_status != "PASS":
        print(
            json.dumps(
                {
                    "ok": False,
                    "error": "validation_status_must_be_pass",
                    "validation_status": validation_status or "missing",
                },
                ensure_ascii=False,
                indent=2,
            )
        )
        return 1

    routing_decision, handoff_targets, loopback_granted, gate_fail_codes = _loopback_handoff_granted(validation_payload)
    if not loopback_granted:
        print(
            json.dumps(
                {
                    "ok": False,
                    "error": "loopback_handoff_not_granted",
                    "validation_status": validation_status,
                    "routing_decision": routing_decision or "missing",
                    "handoff_targets": handoff_targets,
                    "fail_codes": gate_fail_codes,
                },
                ensure_ascii=False,
                indent=2,
            )
        )
        return 1

    delta_payload = _normalize_delta_payload(
        validation_payload,
        _load_json_arg(args.loopback_delta) if args.loopback_delta else None,
    )
    _validate_delta_payload(delta_payload)
    if not (
        delta_payload["card_deltas"]
        or delta_payload["map_deltas"]
        or delta_payload["projection_refresh"]
    ):
        print(
            json.dumps(
                {
                    "ok": False,
                    "error": "loopback_delta_empty",
                    "validation_ref": str(
                        args.validation_ref
                        or validation_payload.get("validation_ref")
                        or validation_payload.get("report_file")
                        or ""
                    ).strip(),
                    "message": "未提供任何 card/map/projection actualization delta，禁止把空 loopback 冒充成功写回。",
                },
                ensure_ascii=False,
                indent=2,
            )
        )
        return 1

    artifact_path = _build_artifact_path(project_root, state, args.episode)
    artifact_ref = _relpath(artifact_path, project_root)
    validation_ref = str(
        args.validation_ref
        or validation_payload.get("validation_ref")
        or validation_payload.get("report_file")
        or ""
    ).strip()

    observed_card_revisions: Dict[str, int] = {}
    next_card_revisions: Dict[str, int] = {}
    for item in delta_payload["card_deltas"]:
        if not isinstance(item, dict):
            continue
        target_ref = str(item.get("target_ref") or "").strip()
        if not target_ref or target_ref in observed_card_revisions:
            continue
        payload = _load_json_file((project_root / target_ref).resolve())
        current_revision = _get_card_revision(payload, (project_root / target_ref).resolve())
        expected_revision = item.get("expected_revision")
        if expected_revision not in (None, ""):
            if current_revision != _normalize_revision(expected_revision, f"{target_ref}.expected_revision"):
                raise ValueError(f"{target_ref} revision 已漂移，拒绝 loopback 写回")
        observed_card_revisions[target_ref] = current_revision
        next_card_revisions[target_ref] = current_revision + 1

    observed_map_revision = _get_map_revision(_load_json_file(story_map_path))
    map_expected_revisions = {
        _normalize_revision(item.get("expected_revision"), "map_delta.expected_revision")
        for item in delta_payload["map_deltas"]
        if isinstance(item, dict) and item.get("expected_revision") not in (None, "")
    }
    if map_expected_revisions and map_expected_revisions != {observed_map_revision}:
        raise ValueError("story_map actualization revision 已漂移，拒绝 loopback 写回")

    observed_state_revision = _get_state_revision(state)
    state_expected_revisions = {
        _normalize_revision(item.get("expected_revision"), "projection_refresh.expected_revision")
        for item in delta_payload["projection_refresh"]
        if isinstance(item, dict) and item.get("expected_revision") not in (None, "")
    }
    if state_expected_revisions and state_expected_revisions != {observed_state_revision}:
        raise ValueError("STATE projection revision 已漂移，拒绝 loopback 写回")

    artifact = _build_artifact(
        _load_template(),
        project_root=project_root,
        state=state,
        episode=args.episode,
        manuscript_ref=args.manuscript_ref,
        validation_ref=validation_ref,
        routing_decision=routing_decision,
        handoff_targets=handoff_targets,
        draft_packet_ref=str(args.draft_packet_ref or ""),
        story_map_ref=story_map_rel,
        story_map_slice_ref="",
        delta_payload=delta_payload,
        artifact_ref=artifact_ref,
        governance_refs=_extract_governance_refs(validation_payload),
    )

    staged_card_payloads, written_card_refs = _apply_card_deltas(
        project_root,
        artifact_ref,
        validation_ref,
        delta_payload["card_deltas"],
    )
    for card_path, payload in staged_card_payloads.items():
        target_ref = _relpath(card_path, project_root)
        if target_ref in next_card_revisions:
            _set_card_revision(payload, card_path, next_card_revisions[target_ref])

    holomap = _load_json_file(story_map_path)
    original_holomap = copy.deepcopy(holomap)
    slice_ref = _resolve_slice_ref(holomap, args.episode, delta_payload["map_deltas"])
    slice_path = _resolve_slice_path(project_root, holomap, slice_ref)
    written_map_slice_refs: List[str] = []

    if slice_path is not None:
        slice_payload = _load_json_file(slice_path)
        staged_slice_payload, written_map_slice_refs = _apply_map_deltas(slice_payload, delta_payload["map_deltas"])
        if written_map_slice_refs:
            _set_map_revision(staged_slice_payload, _get_map_revision(slice_payload) + 1)
        written_map_refs = _refresh_root_actualization_indexes(
            holomap,
            episode=args.episode,
            slice_ref=slice_ref,
            validation_ref=validation_ref,
            artifact_ref=artifact_ref,
        )
        next_map_revision = observed_map_revision + (1 if written_map_refs else 0)
        if written_map_refs:
            _set_map_revision(holomap, next_map_revision)
    else:
        staged_slice_payload = None
        staged_holomap, written_map_refs = _apply_map_deltas(holomap, delta_payload["map_deltas"])
        holomap = staged_holomap
        next_map_revision = observed_map_revision + (1 if written_map_refs else 0)
        if written_map_refs:
            _set_map_revision(holomap, next_map_revision)

    staged_state = copy.deepcopy(state)
    refreshed_projection_refs = _apply_projection_refresh(staged_state, delta_payload["projection_refresh"])
    next_state_revision = observed_state_revision + 1
    _set_state_revision(staged_state, next_state_revision)

    commit_manifest = _build_commit_manifest(
        episode=args.episode,
        validation_ref=validation_ref,
        artifact_ref=artifact_ref,
        written_card_refs=written_card_refs,
        written_map_refs=[*written_map_refs, *written_map_slice_refs],
        refreshed_projection_refs=refreshed_projection_refs,
        observed_revisions={
            "cards": observed_card_revisions,
            "story_map_actualization": observed_map_revision,
            "state_projection": observed_state_revision,
        },
        next_revisions={
            "cards": next_card_revisions,
            "story_map_actualization": next_map_revision,
            "state_projection": next_state_revision,
        },
        phase="committed",
    )

    runtime_markers = staged_state.setdefault("runtime_markers", {})
    if not isinstance(runtime_markers, dict):
        runtime_markers = {}
        staged_state["runtime_markers"] = runtime_markers
    loopback_marker = runtime_markers.setdefault("loopback", {})
    if not isinstance(loopback_marker, dict):
        loopback_marker = {}
        runtime_markers["loopback"] = loopback_marker
    loopback_marker["last_actualized_episode"] = f"第{args.episode}集"
    loopback_marker["last_commit_manifest"] = copy.deepcopy(commit_manifest)
    runtime_markers.pop("loopback_pending", None)

    artifact["content"]["writeback_summary"]["written_card_refs"] = written_card_refs
    artifact["content"]["writeback_summary"]["written_map_refs"] = written_map_refs
    artifact["content"]["writeback_summary"]["written_map_slice_refs"] = written_map_slice_refs
    artifact["content"]["writeback_summary"]["refreshed_projection_refs"] = refreshed_projection_refs
    artifact["execution_notes"]["commit_manifest"] = copy.deepcopy(commit_manifest)
    artifact["inputs"]["story_map_slice_ref"] = _relpath(slice_path, project_root) if slice_path is not None else ""

    artifact_original = _load_json_file(artifact_path) if artifact_path.is_file() else None
    write_plan: List[Tuple[Path, Dict[str, Any], bool, bool]] = []
    originals: Dict[Path, Dict[str, Any] | None] = {
        state_path: copy.deepcopy(state),
        story_map_path: original_holomap,
        artifact_path: artifact_original,
    }

    for card_path, payload in staged_card_payloads.items():
        originals[card_path] = _load_json_file(card_path)
        write_plan.append((card_path, payload, True, True))

    if slice_path is not None and staged_slice_payload is not None:
        originals[slice_path] = _load_json_file(slice_path)
        write_plan.append((slice_path, staged_slice_payload, True, True))

    write_plan.extend(
        [
            (story_map_path, holomap, True, True),
            (state_path, staged_state, True, True),
            (artifact_path, artifact, True, False),
        ]
    )
    pending_state = copy.deepcopy(state)
    pending_runtime_markers = pending_state.setdefault("runtime_markers", {})
    if not isinstance(pending_runtime_markers, dict):
        pending_runtime_markers = {}
        pending_state["runtime_markers"] = pending_runtime_markers
    pending_runtime_markers["loopback_pending"] = _build_commit_manifest(
        episode=args.episode,
        validation_ref=validation_ref,
        artifact_ref=artifact_ref,
        written_card_refs=written_card_refs,
        written_map_refs=[*written_map_refs, *written_map_slice_refs],
        refreshed_projection_refs=refreshed_projection_refs,
        observed_revisions={
            "cards": observed_card_revisions,
            "story_map_actualization": observed_map_revision,
            "state_projection": observed_state_revision,
        },
        next_revisions={
            "cards": next_card_revisions,
            "story_map_actualization": next_map_revision,
            "state_projection": next_state_revision,
        },
        phase="pending",
    )
    atomic_write_json(state_path, pending_state, use_lock=True, backup=True)
    try:
        _commit_json_writes(write_plan, originals)
    except Exception:
        atomic_write_json(state_path, state, use_lock=True, backup=False)
        raise

    print(
        json.dumps(
            {
                "ok": True,
                "loopback_ref": artifact_ref,
                "episode_ref": f"第{args.episode}集",
                "validation_ref": validation_ref,
                "validation_status": "PASS",
                "routing_decision": routing_decision,
                "handoff_targets": handoff_targets,
                "card_deltas": delta_payload["card_deltas"],
                "map_deltas": delta_payload["map_deltas"],
                "projection_refresh": delta_payload["projection_refresh"],
                "evidence_refs": delta_payload["evidence_refs"],
                "written_card_refs": written_card_refs,
                "written_map_refs": written_map_refs,
                "written_map_slice_refs": written_map_slice_refs,
                "refreshed_projection_refs": refreshed_projection_refs,
            },
            ensure_ascii=False,
            indent=2,
        )
    )
    return 0


def main() -> None:
    parser = argparse.ArgumentParser(description="story2026 loopback actualization manager")
    parser.add_argument("--project-root", required=True, help="书项目根目录或工作区根目录")
    sub = parser.add_subparsers(dest="command", required=True)

    p_actualize = sub.add_parser("actualize", help="执行 PASS-only loopback actualization")
    p_actualize.add_argument("--episode", type=int, required=True, help="目标 episode/chapter 编号")
    p_actualize.add_argument("--validation-data", required=True, help="验证聚合结果 JSON 或 @文件路径")
    p_actualize.add_argument("--manuscript-ref", required=True, help="正文稿件路径（相对 project_root）")
    p_actualize.add_argument("--validation-ref", help="验证报告路径（相对 project_root）")
    p_actualize.add_argument("--draft-packet-ref", help="可选 draft packet 引用")
    p_actualize.add_argument("--story-map-ref", default=canonical_planning_artifact_relpath("holomap"), help="story_map 相对路径")
    p_actualize.add_argument("--loopback-delta", help="可选 loopback delta JSON 或 @文件路径")
    p_actualize.set_defaults(func=actualize)

    args = parser.parse_args()
    raise SystemExit(int(args.func(args) or 0))


if __name__ == "__main__":
    enable_windows_utf8_stdio(skip_in_pytest=True)
    main()
