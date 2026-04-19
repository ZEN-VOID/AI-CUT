#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Type pack resolver for story runtime.
"""

from __future__ import annotations

from copy import deepcopy
from pathlib import Path
import re
from typing import Any, Dict, List, Optional

try:
    import yaml
except ImportError:  # pragma: no cover
    yaml = None


PACK_ROOT_REL = Path(".agents") / "skills" / "story" / "type-packs"
DEFAULT_METHOD_KERNEL = "story-core-v1"
DEFAULT_BASE_PACK = "_base"
WEBNOVEL_LIBRARY_DIR = "网文"
CANONICAL_DRAFTING_STEPS = {
    "Step 1": ("1-单集叙事起盘", "单集叙事起盘"),
    "Step 2": ("2-节奏优化", "节奏优化"),
    "Step 3": ("3-场景和氛围渲染", "场景和氛围渲染"),
    "Step 4": ("4-角色形象刻画", "角色形象刻画"),
    "Step 5": ("5-对白个性化和声口优化", "对白个性化和声口优化"),
    "Step 6": ("6-追读力强化", "追读力强化"),
    "Step 7": ("7-润色", "润色"),
}


def _safe_dict(value: Any) -> Dict[str, Any]:
    return value if isinstance(value, dict) else {}


def _safe_list(value: Any) -> List[Any]:
    return value if isinstance(value, list) else []


def normalize_drafting_step_id(raw: Any) -> Optional[str]:
    text = str(raw or "").strip()
    if not text:
        return None
    for canonical, aliases in CANONICAL_DRAFTING_STEPS.items():
        if text == canonical or text in aliases:
            return canonical
    return None


def resolve_stage_projection(
    type_pack_profile: Dict[str, Any],
    stage: str,
    *,
    current_step_id: Any = None,
) -> Dict[str, Any]:
    stage_projection = _safe_dict(_safe_dict(type_pack_profile).get("stage_projection"))
    base_projection = deepcopy(_safe_dict(stage_projection.get(stage)))
    if stage != "drafting":
        return base_projection

    step_id = normalize_drafting_step_id(current_step_id)
    if not step_id:
        return base_projection

    step_hooks = _safe_dict(base_projection.pop("step_hooks", {}))
    current_step_projection = _safe_dict(step_hooks.get(step_id))
    merged = _deep_merge(base_projection, current_step_projection)
    merged["current_step_id"] = step_id
    if current_step_projection:
        merged["step_specific"] = True
    return merged


def _append_dedup(base: List[Any], extra: List[Any]) -> List[Any]:
    out = list(base)
    seen = {str(item) for item in out}
    for item in extra:
        key = str(item)
        if key in seen:
            continue
        out.append(item)
        seen.add(key)
    return out


def _deep_merge(base: Dict[str, Any], extra: Dict[str, Any]) -> Dict[str, Any]:
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


def _read_yaml(path: Path) -> Dict[str, Any]:
    if yaml is None or not path.is_file():
        return {}
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    return data if isinstance(data, dict) else {}


def _catalog_path() -> Path:
    return _canonical_pack_root() / "pack-catalog.yaml"


def _load_pack_catalog() -> Dict[str, Any]:
    return _read_yaml(_catalog_path())


def _normalize_text_list(value: Any) -> List[str]:
    return [str(item).strip() for item in _safe_list(value) if str(item).strip()]


def _catalog_pack_entry(pack_id: str) -> Dict[str, Any]:
    catalog = _load_pack_catalog()
    packs = _safe_dict(catalog.get("packs"))
    return _safe_dict(packs.get(pack_id))


def _digest_markdown_refs(pack_root: Path, refs: List[str]) -> List[str]:
    digest: List[str] = []
    for raw in refs:
        rel = str(raw or "").strip()
        if not rel:
            continue
        path = pack_root.parent.parent.parent.parent / rel if rel.startswith(".agents/") else pack_root / rel
        if not path.is_file():
            continue
        for line in path.read_text(encoding="utf-8").splitlines():
            text = line.strip().lstrip("-").strip()
            if len(text) < 2:
                continue
            if text.startswith("#"):
                continue
            digest.append(text)
            if len(digest) >= 6:
                return digest
    return digest


def _extract_legacy_paths_from_markdown_refs(pack_root: Path, refs: List[str]) -> List[str]:
    legacy_paths: List[str] = []
    for raw in refs:
        rel = str(raw or "").strip()
        if not rel:
            continue
        path = pack_root.parent.parent.parent.parent / rel if rel.startswith(".agents/") else pack_root / rel
        if not path.is_file():
            continue
        for line in path.read_text(encoding="utf-8").splitlines():
            if "`" not in line or ".md" not in line:
                continue
            parts = line.split("`")
            for idx in range(1, len(parts), 2):
                item = str(parts[idx]).strip()
                if item.endswith(".md") and item not in legacy_paths:
                    legacy_paths.append(item)
    return legacy_paths


def _infer_from_text(raw: str, mapping: Dict[str, str]) -> List[str]:
    text = (raw or "").strip().lower()
    results: List[str] = []
    if not text:
        return results
    for needle, pack_id in mapping.items():
        if needle in text and pack_id not in results:
            results.append(pack_id)
    return results


def _canonical_pack_root() -> Path:
    return Path(__file__).resolve().parents[2] / "type-packs"


def _webnovel_library_root() -> Path:
    root = _canonical_pack_root() / WEBNOVEL_LIBRARY_DIR
    return root if root.is_dir() else _canonical_pack_root()


def _legacy_map_path() -> Path:
    return _canonical_pack_root() / "legacy-genre-pack-map.yaml"


def _load_legacy_map() -> Dict[str, Any]:
    return _read_yaml(_legacy_map_path())


def _knowledge_refs_for_dir(dir_path: Path) -> List[str]:
    refs: List[str] = []
    if not dir_path.is_dir():
        return refs
    for path in sorted(dir_path.glob("*.md")):
        refs.append(f".agents/skills/story/type-packs/{WEBNOVEL_LIBRARY_DIR}/{dir_path.name}/{path.name}")
    return refs


def _knowledge_refs_for_source_dirs(pack_root: Path, dir_names: List[str]) -> List[str]:
    refs: List[str] = []
    library_root = pack_root / WEBNOVEL_LIBRARY_DIR
    for dir_name in dir_names:
        dir_path = library_root / dir_name
        refs = _append_dedup(refs, _knowledge_refs_for_dir(dir_path))
    return refs


def _pack_layer(pack_id: str) -> str:
    catalog_pack = _catalog_pack_entry(pack_id)
    layer = str(catalog_pack.get("layer") or "").strip()
    if layer:
        return layer

    pack = _read_yaml(_canonical_pack_root() / pack_id / "pack.yaml")
    layer = str(pack.get("layer") or "").strip()
    if layer:
        return layer
    if pack_id in {"网文高冲击"}:
        return "primary"
    if pack_id in {"起点连载"}:
        return "platform"
    if pack_id in {"男频快节奏"}:
        return "audience"
    if (_webnovel_library_root() / pack_id).is_dir():
        return "secondary"
    return ""


def _legacy_entry_pack_targets(raw_genre: str) -> Dict[str, List[str]]:
    text = str(raw_genre or "").strip().lower()
    out = {"primary": [], "secondary": [], "platform": [], "audience": []}
    if not text:
        return out

    mapping = _safe_dict(_load_legacy_map().get("entry_template_absorption"))
    if not mapping:
        for dir_path in sorted(_webnovel_library_root().iterdir()) if _webnovel_library_root().is_dir() else []:
            if dir_path.is_dir():
                mapping[dir_path.name] = {"packs": [dir_path.name]}
    for legacy_name in sorted(mapping.keys(), key=len, reverse=True):
        if legacy_name.lower() not in text:
            continue
        row = _safe_dict(mapping.get(legacy_name))
        for pack_id in [str(item).strip() for item in _safe_list(row.get("packs")) if str(item).strip()]:
            layer = _pack_layer(pack_id)
            if layer == "primary":
                out["primary"] = _append_dedup(out["primary"], [pack_id])
            elif layer == "platform":
                out["platform"] = _append_dedup(out["platform"], [pack_id])
            elif layer == "audience":
                out["audience"] = _append_dedup(out["audience"], [pack_id])
            else:
                out["secondary"] = _append_dedup(out["secondary"], [pack_id])
    return out


def infer_type_stack(
    *,
    genre: str = "",
    platform: str = "",
    target_reader: str = "",
) -> Dict[str, Any]:
    genre_map = {
        "知乎短篇": "知乎短篇",
        "短篇": "知乎短篇",
        "狗血": "狗血言情",
        "替身": "替身文",
        "总裁": "豪门总裁",
        "甜宠": "青春甜宠",
        "古言": "古言剧",
        "宫斗": "宫斗宅斗",
        "宅斗": "宫斗宅斗",
        "历史古代": "历史古代",
        "历史脑洞": "历史脑洞",
        "现实题材": "现实题材",
        "年代": "年代",
        "职场": "职场婚恋",
        "婚恋": "职场婚恋",
        "都市日常": "都市日常",
        "都市脑洞": "都市脑洞",
        "都市异能": "都市异能",
        "克苏鲁": "克苏鲁",
        "无限流": "无限流",
        "末世": "末世",
        "科幻": "科幻",
        "黑暗": "黑暗题材",
        "修仙": "修仙",
        "玄幻": "修仙",
        "高武": "高武",
        "西幻": "西幻",
        "系统": "系统流",
        "规则怪谈": "规则怪谈",
        "规则": "规则怪谈",
        "悬疑灵异": "悬疑灵异",
        "悬疑脑洞": "悬疑脑洞",
        "悬疑": "悬疑脑洞",
        "怪谈": "规则怪谈",
        "豪门": "豪门总裁",
        "复仇": "豪门总裁",
        "打脸": "多子多福",
        "女频悬疑": "女频悬疑",
        "言情": "幻想言情",
        "情感": "幻想言情",
        "电竞": "电竞",
        "直播": "直播文",
        "游戏体育": "游戏体育",
    }
    platform_map = {
        "起点": "起点连载",
        "qidian": "起点连载",
    }
    audience_map = {
        "男": "男频快节奏",
        "爽": "男频快节奏",
        "快节奏": "男频快节奏",
        "fast": "男频快节奏",
    }

    legacy_targets = _legacy_entry_pack_targets(genre)
    fallback_secondaries = _infer_from_text(genre, genre_map)
    secondaries = _append_dedup(list(legacy_targets.get("secondary", [])), fallback_secondaries)
    platforms = _infer_from_text(platform, platform_map)
    audiences = _infer_from_text(target_reader, audience_map)
    platforms = _append_dedup(legacy_targets.get("platform", []), platforms)
    audiences = _append_dedup(legacy_targets.get("audience", []), audiences)
    notes: List[str] = []
    primary = "网文高冲击"
    legacy_primary = [item for item in legacy_targets.get("primary", []) if str(item).strip()]
    if legacy_primary:
        primary = legacy_primary[0]
        notes.append("primary inferred from legacy genre map")
    if secondaries:
        notes.append("secondary inferred from genre")
    if platforms:
        notes.append("platform inferred from platform field")
    if audiences:
        notes.append("audience inferred from target_reader")

    return {
        "method_kernel": DEFAULT_METHOD_KERNEL,
        "base": DEFAULT_BASE_PACK,
        "primary": primary,
        "secondary": secondaries,
        "platform": platforms,
        "audience": audiences,
        "notes": notes,
        "inferred": True,
    }


class TypePackResolver:
    def __init__(self, project_root: Path, *, skill_root: Optional[Path] = None):
        self.project_root = Path(project_root)
        self.skill_root = skill_root or Path(__file__).resolve().parents[2]

    def _pack_root_candidates(self) -> List[Path]:
        return [
            self.project_root / PACK_ROOT_REL,
            self.skill_root / "type-packs",
        ]

    def _pack_root(self) -> Path:
        for candidate in self._pack_root_candidates():
            if candidate.is_dir():
                return candidate
        return self.skill_root / "type-packs"

    def _north_star_path(self) -> Path:
        return self.project_root / "0-Init" / "north_star.yaml"

    def _load_north_star(self) -> Dict[str, Any]:
        return _read_yaml(self._north_star_path())

    def _raw_type_stack(self) -> Dict[str, Any]:
        north_star = self._load_north_star()
        type_stack = _safe_dict(north_star.get("type_stack"))
        if type_stack:
            type_stack.setdefault("method_kernel", DEFAULT_METHOD_KERNEL)
            type_stack.setdefault("base", DEFAULT_BASE_PACK)
            type_stack.setdefault("secondary", [])
            type_stack.setdefault("platform", [])
            type_stack.setdefault("audience", [])
            type_stack.setdefault("notes", [])
            type_stack.setdefault("inferred", False)
            return type_stack

        project_identity = _safe_dict(north_star.get("project_identity"))
        return infer_type_stack(
            genre=str(project_identity.get("genre") or ""),
            platform=str(project_identity.get("platform") or ""),
            target_reader=str(project_identity.get("target_reader") or ""),
        )

    def active_pack_ids(self) -> List[str]:
        stack = self._raw_type_stack()
        pack_ids = [str(stack.get("base") or DEFAULT_BASE_PACK)]
        primary = str(stack.get("primary") or "").strip()
        if primary:
            pack_ids.append(primary)
        pack_ids.extend(str(item).strip() for item in _safe_list(stack.get("secondary")) if str(item).strip())
        pack_ids.extend(str(item).strip() for item in _safe_list(stack.get("platform")) if str(item).strip())
        pack_ids.extend(str(item).strip() for item in _safe_list(stack.get("audience")) if str(item).strip())

        deduped: List[str] = []
        for item in pack_ids:
            if item and item not in deduped:
                deduped.append(item)
        return deduped

    def load_pack(self, pack_id: str) -> Dict[str, Any]:
        yaml_pack = _read_yaml(self._pack_root() / pack_id / "pack.yaml")
        catalog_pack = deepcopy(_catalog_pack_entry(pack_id))

        if yaml_pack:
            pack = _deep_merge(catalog_pack, yaml_pack)
        else:
            pack = catalog_pack

        source_dirs = _normalize_text_list(pack.get("source_dirs"))
        if not source_dirs:
            library_dir = self._pack_root() / WEBNOVEL_LIBRARY_DIR / pack_id
            if library_dir.is_dir():
                source_dirs = [pack_id]

        knowledge_refs = _normalize_text_list(pack.get("knowledge_refs"))
        if source_dirs:
            knowledge_refs = _append_dedup(
                knowledge_refs,
                _knowledge_refs_for_source_dirs(self._pack_root(), source_dirs),
            )

        if not pack and not knowledge_refs:
            return {}

        pack.setdefault("pack_id", pack_id)
        pack.setdefault("display_name", pack_id)
        pack.setdefault("layer", _pack_layer(pack_id) or "secondary")
        pack.setdefault("summary", f"{pack_id} 类型包")
        if source_dirs:
            pack["source_dirs"] = source_dirs
        if knowledge_refs:
            pack["knowledge_refs"] = knowledge_refs
        return pack

    def load_knowledge_index(self, pack_id: str) -> Dict[str, Any]:
        return _read_yaml(self._pack_root() / pack_id / "knowledge" / "legacy-index.yaml")

    def resolve(self) -> Dict[str, Any]:
        stack = self._raw_type_stack()
        active_pack_ids = self.active_pack_ids()
        merged: Dict[str, Any] = {
            "method_kernel": str(stack.get("method_kernel") or DEFAULT_METHOD_KERNEL),
            "type_stack": deepcopy(stack),
            "active_packs": active_pack_ids,
            "semantic_tags": [],
            "reader_promise": {},
            "narrative_engine": {},
            "forbidden_patterns": [],
            "stage_projection": {},
            "planning_projection": {},
            "cards_projection": {},
            "knowledge_refs": [],
            "knowledge_indexes": [],
            "knowledge_digest": [],
            "knowledge_entries": [],
            "legacy_source_refs": [],
            "resolution_trace": [],
            "resolver_ref": ".agents/skills/story/_shared/type-pack-loading-contract.md",
            "pack_catalog_ref": ".agents/skills/story/type-packs/pack-catalog.yaml",
            "pack_root": str(self._pack_root()),
        }

        for pack_id in active_pack_ids:
            pack = self.load_pack(pack_id)
            if not pack:
                merged["resolution_trace"].append({"pack_id": pack_id, "status": "missing"})
                continue
            merged["resolution_trace"].append(
                {"pack_id": pack_id, "layer": str(pack.get("layer") or ""), "status": "loaded"}
            )
            merged["reader_promise"] = _deep_merge(_safe_dict(merged["reader_promise"]), _safe_dict(pack.get("reader_promise")))
            merged["narrative_engine"] = _deep_merge(_safe_dict(merged["narrative_engine"]), _safe_dict(pack.get("narrative_engine")))
            merged["stage_projection"] = _deep_merge(_safe_dict(merged["stage_projection"]), _safe_dict(pack.get("stage_projection")))
            merged["planning_projection"] = _deep_merge(
                _safe_dict(merged["planning_projection"]),
                _safe_dict(pack.get("planning_projection")),
            )
            merged["cards_projection"] = _deep_merge(
                _safe_dict(merged["cards_projection"]),
                _safe_dict(pack.get("cards_projection")),
            )
            merged["forbidden_patterns"] = _append_dedup(_safe_list(merged["forbidden_patterns"]), _safe_list(pack.get("forbidden_patterns")))
            merged["semantic_tags"] = _append_dedup(
                _safe_list(merged["semantic_tags"]),
                _normalize_text_list(pack.get("semantic_tags")),
            )
            merged["knowledge_refs"] = _append_dedup(_safe_list(merged["knowledge_refs"]), _safe_list(pack.get("knowledge_refs")))

            knowledge_index = self.load_knowledge_index(pack_id)
            if knowledge_index:
                index_path = str(self._pack_root() / pack_id / "knowledge" / "legacy-index.yaml")
                merged["knowledge_indexes"] = _append_dedup(_safe_list(merged["knowledge_indexes"]), [index_path])
                merged["knowledge_digest"] = _append_dedup(
                    _safe_list(merged["knowledge_digest"]),
                    _normalize_text_list(knowledge_index.get("guidance_snippets")),
                )
                for section_key in ("entry_sources", "detail_sources", "shared_sources"):
                    for row in _safe_list(knowledge_index.get(section_key)):
                        item = _safe_dict(row)
                        legacy_path = str(item.get("legacy_path") or "").strip()
                        focus = str(item.get("focus") or "").strip()
                        carry = _normalize_text_list(item.get("carry"))
                        if legacy_path:
                            merged["legacy_source_refs"] = _append_dedup(
                                _safe_list(merged["legacy_source_refs"]),
                                [legacy_path],
                            )
                        if carry:
                            merged["knowledge_digest"] = _append_dedup(
                                _safe_list(merged["knowledge_digest"]),
                                carry,
                            )
                        merged["knowledge_entries"].append(
                            {
                                "pack_id": pack_id,
                                "section": section_key,
                                "legacy_path": legacy_path,
                                "focus": focus,
                                "carry": carry,
                            }
                        )
            else:
                knowledge_refs = _normalize_text_list(pack.get("knowledge_refs"))
                if knowledge_refs:
                    merged["legacy_source_refs"] = _append_dedup(
                        _safe_list(merged["legacy_source_refs"]),
                        _extract_legacy_paths_from_markdown_refs(self._pack_root(), knowledge_refs),
                    )
                    merged["knowledge_digest"] = _append_dedup(
                        _safe_list(merged["knowledge_digest"]),
                        _digest_markdown_refs(self._pack_root(), knowledge_refs),
                    )

        return merged


def resolve_type_pack_profile(project_root: Path) -> Dict[str, Any]:
    return TypePackResolver(project_root).resolve()
