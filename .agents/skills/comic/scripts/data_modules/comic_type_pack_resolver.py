#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Dynamic single-layer genre type-pack resolver for comic runtime."""

from __future__ import annotations

from copy import deepcopy
import hashlib
from pathlib import Path
from typing import Any

try:
    import yaml
except ImportError:  # pragma: no cover
    yaml = None


PACK_ROOT_REL = Path(".agents") / "skills" / "comic" / "type-packs"
COMIC_LIBRARY_DIR = "漫画"
RUNTIME_CONFIG_NAME = "runtime.yaml"
GENRE_META_NAME = "meta.yaml"
DEFAULT_METHOD_KERNEL = "comic-core-v1"
DEFAULT_BASE_PACK = "_base"
DEFAULT_PRIMARY_PACK = "经典漫画叙事"
CANONICAL_STAGES = (
    "script_adaptation",
    "nine_blade_prompting",
    "image_generation",
    "animation_generation",
    "episode_poster",
)


def _safe_dict(value: Any) -> dict[str, Any]:
    return value if isinstance(value, dict) else {}


def _safe_list(value: Any) -> list[Any]:
    return value if isinstance(value, list) else []


def _append_dedup(base: list[Any], extra: list[Any]) -> list[Any]:
    out = list(base)
    seen = {str(item) for item in out}
    for item in extra:
        key = str(item)
        if key in seen:
            continue
        out.append(item)
        seen.add(key)
    return out


def _deep_merge(base: dict[str, Any], extra: dict[str, Any]) -> dict[str, Any]:
    result = deepcopy(base)
    for key, value in extra.items():
        if key not in result:
            result[key] = deepcopy(value)
            continue
        current = result[key]
        if isinstance(current, dict) and isinstance(value, dict):
            result[key] = _deep_merge(current, value)
        elif isinstance(current, list) and isinstance(value, list):
            result[key] = _append_dedup(current, value)
        else:
            result[key] = deepcopy(value)
    return result


def _normalize_text_list(value: Any) -> list[str]:
    return [str(item).strip() for item in _safe_list(value) if str(item).strip()]


def _compact_text(value: Any) -> str:
    if value in (None, "", [], {}):
        return ""
    if isinstance(value, str):
        return " ".join(value.split()).strip()
    return str(value).strip()


def _read_yaml(path: Path) -> dict[str, Any]:
    if yaml is None or not path.is_file():
        return {}
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    return data if isinstance(data, dict) else {}


def _canonical_pack_root() -> Path:
    return Path(__file__).resolve().parents[2] / "type-packs"


def _comic_library_root() -> Path:
    root = _canonical_pack_root() / COMIC_LIBRARY_DIR
    return root if root.is_dir() else _canonical_pack_root()


def _runtime_config() -> dict[str, Any]:
    return _read_yaml(_canonical_pack_root() / RUNTIME_CONFIG_NAME)


def _genre_dir(genre_id: str) -> Path:
    return _comic_library_root() / genre_id


def _genre_meta(genre_id: str) -> dict[str, Any]:
    return _read_yaml(_genre_dir(genre_id) / GENRE_META_NAME)


def _genre_revision(genre_id: str) -> str:
    dir_path = _genre_dir(genre_id)
    digest = hashlib.sha1()
    if not dir_path.is_dir():
        return ""
    for path in sorted(dir_path.glob("*")):
        if not path.is_file():
            continue
        digest.update(path.name.encode("utf-8"))
        digest.update(path.read_bytes())
    return digest.hexdigest()[:12]


def _discover_genres() -> dict[str, dict[str, Any]]:
    registry: dict[str, dict[str, Any]] = {}
    library_root = _comic_library_root()
    if not library_root.is_dir():
        return registry
    for dir_path in sorted(library_root.iterdir()):
        if not dir_path.is_dir():
            continue
        genre_id = dir_path.name
        meta = _genre_meta(genre_id)
        if not meta:
            meta = {"pack_id": genre_id}
        meta["pack_id"] = str(meta.get("pack_id") or genre_id).strip() or genre_id
        meta["revision"] = _genre_revision(genre_id)
        registry[genre_id] = meta
    return registry


def list_available_genres() -> list[str]:
    return sorted(_discover_genres().keys())


def _build_genre_alias_map() -> dict[str, str]:
    mapping: dict[str, str] = {}
    for genre_id, meta in _discover_genres().items():
        alias_candidates = [genre_id] + _normalize_text_list(meta.get("aliases"))
        for alias in alias_candidates:
            mapping[alias.lower()] = genre_id
    return mapping


def _keyword_hits(raw: str, mapping: dict[str, str]) -> list[str]:
    text = str(raw or "").strip().lower()
    results: list[str] = []
    if not text:
        return results
    for keyword, pack_id in sorted(mapping.items(), key=lambda item: len(item[0]), reverse=True):
        if keyword in text and pack_id not in results:
            results.append(pack_id)
    return results


def _knowledge_refs_for_genre(genre_id: str) -> list[str]:
    dir_path = _genre_dir(genre_id)
    if not dir_path.is_dir():
        return []
    refs: list[str] = []
    main_file = dir_path / f"{genre_id}.md"
    if main_file.is_file():
        refs.append(str(PACK_ROOT_REL / COMIC_LIBRARY_DIR / genre_id / main_file.name))
    for path in sorted(dir_path.glob("*.md")):
        if path == main_file:
            continue
        refs.append(str(PACK_ROOT_REL / COMIC_LIBRARY_DIR / genre_id / path.name))
    return refs


def _flatten_structure_lines(
    value: Any,
    *,
    prefix: str = "",
    max_lines: int = 24,
    max_depth: int = 4,
) -> list[str]:
    lines: list[str] = []

    def walk(node: Any, current_prefix: str, depth: int) -> None:
        if len(lines) >= max_lines or depth > max_depth:
            return
        if isinstance(node, dict):
            for key, child in node.items():
                next_prefix = f"{current_prefix}.{key}" if current_prefix else str(key)
                walk(child, next_prefix, depth + 1)
                if len(lines) >= max_lines:
                    return
            return
        if isinstance(node, list):
            compact_items = [_compact_text(item) for item in node]
            compact_items = [item for item in compact_items if item]
            if compact_items:
                label = current_prefix or "items"
                lines.append(f"{label}: {', '.join(compact_items[:8])}")
            return
        compact = _compact_text(node)
        if compact:
            label = current_prefix or "value"
            lines.append(f"{label}: {compact}")

    walk(value, prefix, 0)
    return lines[:max_lines]


def _digest_markdown_refs(refs: list[str], *, max_lines: int = 24) -> list[str]:
    digest: list[str] = []
    repo_root = _canonical_pack_root().parents[4]
    for raw in refs:
        path = repo_root / raw
        if not path.is_file():
            continue
        heading_stack: list[str] = []
        for line in path.read_text(encoding="utf-8").splitlines():
            stripped = line.strip()
            if not stripped:
                continue
            if stripped.startswith("#"):
                heading = stripped.lstrip("#").strip()
                if heading:
                    level = len(stripped) - len(stripped.lstrip("#"))
                    keep = max(level - 1, 0)
                    heading_stack[:] = heading_stack[:keep]
                    heading_stack.append(heading)
                continue
            text = stripped.lstrip("-").strip()
            if len(text) < 2:
                continue
            prefix = " > ".join(heading_stack[-2:])
            digest_line = f"{prefix}: {text}" if prefix else text
            if digest_line not in digest:
                digest.append(digest_line)
            if len(digest) >= max_lines:
                return digest
    return digest


def _profile_overlay(bucket: str, pack_id: str) -> dict[str, Any]:
    runtime = _runtime_config()
    return _safe_dict(_safe_dict(runtime.get(bucket)).get(pack_id))


def _base_overlay() -> dict[str, Any]:
    return _safe_dict(_runtime_config().get("base_profile"))


def infer_type_stack(
    *,
    genre: str = "",
    platform: str = "",
    target_audience: str = "",
    tone: str = "",
) -> dict[str, Any]:
    runtime = _runtime_config()
    default_stack = _safe_dict(runtime.get("default_stack"))
    genre_map = _build_genre_alias_map()

    platform_map: dict[str, str] = {}
    for pack_id, row in _safe_dict(runtime.get("platform_profiles")).items():
        for alias in [pack_id] + _normalize_text_list(_safe_dict(row).get("aliases")):
            platform_map[alias.lower()] = pack_id

    audience_map: dict[str, str] = {}
    for pack_id, row in _safe_dict(runtime.get("audience_profiles")).items():
        for alias in [pack_id] + _normalize_text_list(_safe_dict(row).get("aliases")):
            audience_map[alias.lower()] = pack_id

    secondary = _keyword_hits(" ".join([genre, tone]), genre_map)
    platforms = _keyword_hits(platform, platform_map)
    audiences = _keyword_hits(target_audience, audience_map)

    return {
        "method_kernel": str(runtime.get("method_kernel") or DEFAULT_METHOD_KERNEL),
        "base": str(default_stack.get("base") or DEFAULT_BASE_PACK),
        "primary": str(default_stack.get("primary") or DEFAULT_PRIMARY_PACK),
        "secondary": secondary,
        "platform": platforms or _normalize_text_list(default_stack.get("platform")),
        "audience": audiences or _normalize_text_list(default_stack.get("audience")),
    }


def resolve_stage_projection(type_pack_profile: dict[str, Any], stage: str) -> dict[str, Any]:
    if stage not in CANONICAL_STAGES:
        return {}
    return deepcopy(_safe_dict(_safe_dict(type_pack_profile).get("stage_projection")).get(stage))


class TypePackResolver:
    def __init__(self, project_root: Path | None = None) -> None:
        self.project_root = project_root

    def resolve(self, explicit_stack: dict[str, Any] | None = None) -> dict[str, Any]:
        stack = explicit_stack or infer_type_stack()
        runtime = _runtime_config()
        genre_registry = _discover_genres()

        base = str(stack.get("base") or runtime.get("default_stack", {}).get("base") or DEFAULT_BASE_PACK)
        primary = str(stack.get("primary") or runtime.get("default_stack", {}).get("primary") or DEFAULT_PRIMARY_PACK)
        secondary = [item for item in _normalize_text_list(stack.get("secondary")) if item in genre_registry]
        platform = _normalize_text_list(stack.get("platform"))
        audience = _normalize_text_list(stack.get("audience"))

        active_packs = [base, primary] + secondary + platform + audience
        semantic_tags: list[str] = []
        knowledge_refs: list[str] = []
        stage_projection: dict[str, Any] = {stage: {} for stage in CANONICAL_STAGES}
        pack_revisions: dict[str, str] = {}
        control_surface: dict[str, Any] = {}

        overlays = [
            _base_overlay(),
            _profile_overlay("primary_profiles", primary),
        ]
        overlays.extend(_profile_overlay("platform_profiles", item) for item in platform)
        overlays.extend(_profile_overlay("audience_profiles", item) for item in audience)
        overlays.extend(_safe_dict(genre_registry.get(item)) for item in secondary)

        for overlay in overlays:
            semantic_tags = _append_dedup(semantic_tags, _normalize_text_list(_safe_dict(overlay).get("semantic_tags")))
            control_surface = _deep_merge(control_surface, _safe_dict(overlay).get("control_surface") or {})
            for stage in CANONICAL_STAGES:
                stage_projection[stage] = _deep_merge(
                    stage_projection[stage],
                    _safe_dict(_safe_dict(overlay).get("stage_projection")).get(stage) or {},
                )

        for genre_id in secondary:
            knowledge_refs = _append_dedup(knowledge_refs, _knowledge_refs_for_genre(genre_id))
            revision = str(_safe_dict(genre_registry.get(genre_id)).get("revision") or "").strip()
            if revision:
                pack_revisions[genre_id] = revision

        projection_summary = {
            stage: ", ".join(_normalize_text_list(_safe_dict(projection).get("focus")))
            or ", ".join(_normalize_text_list(_safe_dict(projection).get("layout_bias")))
            or ", ".join(_normalize_text_list(_safe_dict(projection).get("render_bias")))
            or ", ".join(_normalize_text_list(_safe_dict(projection).get("motion_bias")))
            or ", ".join(_normalize_text_list(_safe_dict(projection).get("poster_bias")))
            for stage, projection in stage_projection.items()
        }

        return {
            "method_kernel": str(stack.get("method_kernel") or runtime.get("method_kernel") or DEFAULT_METHOD_KERNEL),
            "base": base,
            "primary": primary,
            "secondary": secondary,
            "platform": platform,
            "audience": audience,
            "active_packs": active_packs,
            "resolution_mode": "single-layer-genre-comic-type-pack",
            "knowledge_refs": knowledge_refs,
            "knowledge_digest": _digest_markdown_refs(knowledge_refs),
            "control_surface": control_surface,
            "control_surface_digest": _flatten_structure_lines(control_surface, max_lines=28),
            "semantic_tags": semantic_tags,
            "stage_projection": stage_projection,
            "projection_summary": projection_summary,
            "pack_revisions": pack_revisions,
            "resolver_strategy": "runtime-yaml-plus-genre-meta-single-layer-autodiscovery",
        }
