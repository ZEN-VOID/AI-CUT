#!/usr/bin/env python3
"""Build costume catalog artifacts from the role list and episode evidence."""

from __future__ import annotations

import argparse
import json
import re
from collections import defaultdict
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, Iterable, List, Tuple


DEFAULT_ROLE_LIST_NAME = "角色清单.json"
DEFAULT_OUTPUT_FILES = (
    "服装清单.json",
    "服装研究.json",
    "costume_design_bridge.json",
    "_manifest.json",
)
DIRECTOR_INPUT_ALIASES = ("编导", "3-Detail")
COLOR_TERMS = ("黑", "白", "灰", "青", "蓝", "赤", "红", "金", "银", "紫", "绿", "棕")
MATERIAL_TERMS = ("丝", "绸", "麻", "皮", "革", "纱", "布", "缎", "棉", "金属", "锦")
ACCESSORY_TERMS = ("冠", "簪", "佩", "腰封", "披风", "斗篷", "护腕", "手套", "靴", "鞋", "带", "链")
LAYER_TERMS = ("内搭", "外袍", "披风", "斗篷", "外套", "长衫", "罩衫", "腰封", "围裙")
EPISODE_STEM_RE = re.compile(r"第0*(?P<ep>\d+)集")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="从角色清单提取服装清单与设计桥接")
    parser.add_argument("--role-list", help="显式指定角色清单 JSON 路径")
    parser.add_argument("--input", help="兼容参数；等价于 --role-list")
    parser.add_argument("--project", help="项目名；配合 --episode 自动推断输入")
    parser.add_argument("--episode", help="集标识，例如 第1集")
    parser.add_argument("--output-dir", help="显式输出目录")
    parser.add_argument("--dry-run", action="store_true", help="仅打印统计，不落盘")
    return parser.parse_args()


def normalize_episode_label(raw: str) -> str:
    text = str(raw or "").strip()
    match = EPISODE_STEM_RE.search(text)
    if match:
        return f"第{int(match.group('ep'))}集"
    if text.isdigit():
        return f"第{int(text)}集"
    return text or "第1集"


def resolve_role_list_path(role_list: str | None, project: str | None, episode: str | None) -> Path:
    candidate = role_list or ""
    if candidate:
        path = Path(candidate)
        if path.exists():
            return path
    if project and episode:
        episode_label = normalize_episode_label(episode)
        path = Path("projects") / project / "4-Design" / "2-角色" / "1-清单" / episode_label / DEFAULT_ROLE_LIST_NAME
        if path.exists():
            return path
    raise FileNotFoundError("未找到角色清单；请提供 --role-list，或使用 --project + --episode。")


def infer_output_dir(role_list_path: Path, explicit_output_dir: str | None, episode_label: str) -> Path:
    if explicit_output_dir:
        return Path(explicit_output_dir)
    parts = role_list_path.resolve().parts
    if "projects" in parts:
        idx = parts.index("projects")
        project_root = Path(*parts[: idx + 2])
        return project_root / "4-Design" / "3-服装" / "1-清单" / episode_label
    return role_list_path.parent.parent.parent / "3-服装" / "1-清单" / episode_label


def _infer_project_name(path: Path) -> str:
    parts = path.resolve().parts
    if "projects" in parts:
        idx = parts.index("projects")
        if idx + 1 < len(parts):
            return parts[idx + 1]
    return "unknown-project"


def _resolve_detail_path(role_list_path: Path, episode_label: str) -> Path | None:
    parts = role_list_path.resolve().parts
    if "projects" not in parts:
        return None
    idx = parts.index("projects")
    project_root = Path(*parts[: idx + 2])
    for alias in DIRECTOR_INPUT_ALIASES:
        candidate = project_root / alias / f"{episode_label}.json"
        if candidate.exists():
            return candidate
    return None


def _load_json(path: Path) -> Dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def _safe_name(value: str) -> str:
    text = re.sub(r"[\\/:*?\"<>|]+", "-", (value or "").strip())
    text = re.sub(r"\s+", "-", text)
    return text or "unnamed"


def _as_list(value: Any) -> List[Any]:
    if value is None:
        return []
    if isinstance(value, list):
        return value
    return [value]


def _flatten_text(value: Any) -> str:
    if isinstance(value, dict):
        parts: List[str] = []
        for item in value.values():
            parts.append(_flatten_text(item))
        return "；".join(part for part in parts if part)
    if isinstance(value, list):
        return "；".join(_flatten_text(item) for item in value if _flatten_text(item))
    return str(value or "").strip()


def _pick_terms(text: str, terms: Iterable[str]) -> List[str]:
    return [term for term in terms if term in text]


def _build_costume_entry(role: Dict[str, Any]) -> Dict[str, Any]:
    role_id = str(role.get("role_id") or role.get("id") or "").strip()
    role_name = str(role.get("name") or role.get("canonical_name") or role_id or "未命名角色").strip()
    costume_state = str(role.get("costume_state") or "baseline").strip() or "baseline"
    costume_profile_text = _flatten_text(role.get("costume_profile"))
    evidence = [item for item in _as_list(role.get("evidence")) if isinstance(item, dict)]
    group_ids = [str(item).strip() for item in _as_list(role.get("group_ids")) if str(item).strip()]
    shot_ids = [str(item).strip() for item in _as_list(role.get("shot_ids")) if str(item).strip()]
    costume_id = f"costume-{_safe_name(role_id or role_name)}-{_safe_name(costume_state)}"
    label_suffix = "常服" if costume_state == "baseline" else costume_state
    canonical_label = f"{role_name}-{label_suffix}"
    color_terms = _pick_terms(costume_profile_text, COLOR_TERMS)
    material_terms = _pick_terms(costume_profile_text, MATERIAL_TERMS)
    accessory_terms = _pick_terms(costume_profile_text, ACCESSORY_TERMS)
    layer_terms = _pick_terms(costume_profile_text, LAYER_TERMS)

    return {
        "costume_id": costume_id,
        "role_id": role_id,
        "role_name": role_name,
        "canonical_label": canonical_label,
        "costume_state": costume_state,
        "role_level": role.get("role_level") or role.get("role_tier"),
        "group_ids": group_ids,
        "shot_ids": shot_ids,
        "display_card": role.get("display_card"),
        "silhouette_hint": costume_profile_text,
        "material_hint": material_terms,
        "color_hint": color_terms,
        "accessory_hint": accessory_terms,
        "layer_hint": layer_terms,
        "continuity_notes": [str(item).strip() for item in _as_list(role.get("variation_rules")) if str(item).strip()],
        "evidence": evidence,
    }


def build_artifacts(role_list_path: Path) -> Tuple[Dict[str, Any], Dict[str, Any], Dict[str, Any], Dict[str, Any]]:
    role_list = _load_json(role_list_path)
    meta = role_list.get("meta") or {}
    episode_label = normalize_episode_label(str(meta.get("episode_id") or role_list_path.parent.name))
    project_name = str(meta.get("project_name") or _infer_project_name(role_list_path))
    detail_path = _resolve_detail_path(role_list_path, episode_label)
    source_detail = (
        str(detail_path).replace(str(Path.cwd()) + "/", "") if detail_path else f"projects/{project_name}/3-Detail/{episode_label}.json"
    )

    roles = [item for item in role_list.get("roles", []) if isinstance(item, dict)]
    group_role_map = [item for item in role_list.get("group_role_map", []) if isinstance(item, dict)]
    costumes = [_build_costume_entry(role) for role in roles]

    costume_catalog = {
        "meta": {
            "project_name": project_name,
            "episode_id": episode_label,
            "source_role_list": str(role_list_path).replace(str(Path.cwd()) + "/", ""),
            "source_episode_detail": source_detail,
            "skill_id": "aigc/4-Design/服装/1-清单",
            "generated_at": datetime.now().astimezone().isoformat(timespec="seconds"),
        },
        "statistics": {
            "role_count": len(roles),
            "costume_count": len(costumes),
            "group_map_count": len(group_role_map),
        },
        "group_costume_map": [],
        "costumes": costumes,
    }

    for item in group_role_map:
        costume_mentions = item.get("costume_mentions") or {}
        if isinstance(costume_mentions, list):
            mention_list = [str(entry).strip() for entry in costume_mentions if str(entry).strip()]
        elif isinstance(costume_mentions, dict):
            mention_list = []
            for entries in costume_mentions.values():
                for entry in _as_list(entries):
                    text = str(entry).strip()
                    if text:
                        mention_list.append(text)
        else:
            mention_list = [str(costume_mentions).strip()] if str(costume_mentions).strip() else []
        costume_catalog["group_costume_map"].append(
            {
                "group_id": item.get("group_id"),
                "shot_id": item.get("shot_id"),
                "scene": item.get("shot_scene"),
                "role_text": item.get("role_text"),
                "roles": item.get("roles", []),
                "costume_mentions": mention_list,
                "source_file": item.get("source_file") or source_detail,
            }
        )

    research_items = []
    bridge_items = []
    for costume in costumes:
        silhouette_text = costume["silhouette_hint"]
        materials = costume["material_hint"] or ["待补材质"]
        accessories = costume["accessory_hint"]
        layers = costume["layer_hint"] or ["待补层次"]
        colors = costume["color_hint"] or ["待补色板"]
        research_items.append(
            {
                "costume_id": costume["costume_id"],
                "role_id": costume["role_id"],
                "role_name": costume["role_name"],
                "canonical_label": costume["canonical_label"],
                "costume_state": costume["costume_state"],
                "evidence_ledger": costume["evidence"],
                "silhouette_profile": {
                    "summary": silhouette_text,
                    "shape_terms": layers,
                },
                "material_profile": {
                    "materials": materials,
                    "colors": colors,
                },
                "accessory_profile": {
                    "items": accessories,
                },
                "continuity_profile": {
                    "notes": costume["continuity_notes"],
                },
                "display_profile": {
                    "identity_badge": f'{costume["costume_id"]}+{costume["canonical_label"]}',
                    "role_level": costume.get("role_level"),
                },
                "chronicle": silhouette_text,
            }
        )
        bridge_items.append(
            {
                "costume_id": costume["costume_id"],
                "role_id": costume["role_id"],
                "role_name": costume["role_name"],
                "canonical_label": costume["canonical_label"],
                "costume_state": costume["costume_state"],
                "prompt_anchor": " / ".join(
                    part
                    for part in [
                        costume["canonical_label"],
                        f'silhouette={silhouette_text}' if silhouette_text else "",
                        f"materials={','.join(materials)}" if materials else "",
                        f"colors={','.join(colors)}" if colors else "",
                    ]
                    if part
                ),
                "silhouette_system": {
                    "summary": silhouette_text,
                },
                "layer_system": layers,
                "material_palette": materials + colors,
                "accessory_system": accessories,
                "continuity_rules": costume["continuity_notes"],
                "negative_constraints": [
                    "不得偏离角色已锁定的身份与时代语境",
                    "不得把未出现的道具功能强加到服装上",
                ],
                "evidence": costume["evidence"],
            }
        )

    research = {
        "meta": costume_catalog["meta"],
        "costumes": research_items,
    }
    bridge = {
        "meta": costume_catalog["meta"],
        "costumes": bridge_items,
    }
    manifest = {
        "status": "ok",
        "episode_id": episode_label,
        "input_file": str(role_list_path).replace(str(Path.cwd()) + "/", ""),
        "output_files": list(DEFAULT_OUTPUT_FILES),
        "statistics": costume_catalog["statistics"],
        "notes": [
            "第一输入根固定为角色清单；导演 episode JSON 仅作证据补包。",
        ],
    }
    return costume_catalog, research, bridge, manifest


def write_outputs(output_dir: Path, payloads: Tuple[Dict[str, Any], Dict[str, Any], Dict[str, Any], Dict[str, Any]]) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    for filename, data in zip(DEFAULT_OUTPUT_FILES, payloads):
        (output_dir / filename).write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def main() -> None:
    args = parse_args()
    role_list_path = resolve_role_list_path(args.role_list or args.input, args.project, args.episode)
    role_list = _load_json(role_list_path)
    episode_label = normalize_episode_label(str((role_list.get("meta") or {}).get("episode_id") or role_list_path.parent.name))
    output_dir = infer_output_dir(role_list_path, args.output_dir, episode_label)
    payloads = build_artifacts(role_list_path)

    if args.dry_run:
        costume_catalog = payloads[0]
        print(
            json.dumps(
                {
                    "episode_id": episode_label,
                    "project_name": costume_catalog["meta"]["project_name"],
                    "output_dir": str(output_dir),
                    "statistics": costume_catalog["statistics"],
                },
                ensure_ascii=False,
                indent=2,
            )
        )
        return

    write_outputs(output_dir, payloads)
    print(json.dumps({"status": "ok", "output_dir": str(output_dir)}, ensure_ascii=False))


if __name__ == "__main__":
    main()
