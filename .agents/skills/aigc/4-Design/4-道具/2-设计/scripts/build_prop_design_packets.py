#!/usr/bin/env python3
"""Build prop design master, prompt sidecar, and manifest from prop bridge inputs."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any


SELECTED_AGENTS = [
    "模型师",
    "材质工艺师",
    "痕迹叙事师",
    "提示词架构师",
    "设计审计",
]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="从道具 bridge 生成道具设计主稿与 prompt sidecar。")
    parser.add_argument("--bridge", required=True, help="prop_design_bridge.json 路径")
    parser.add_argument("--research", required=True, help="道具研究.json 路径")
    parser.add_argument("--detail", required=True, help="3-Detail/第N集.json 路径")
    parser.add_argument("--catalog", help="道具清单.json 路径")
    parser.add_argument("--global-style", help="全局风格.md 路径")
    parser.add_argument("--type-guide", help="类型指导.md 路径")
    parser.add_argument("--north-star", help="north_star.yaml 路径")
    parser.add_argument("--init-handoff", help="init_handoff.yaml 路径")
    parser.add_argument("--output-dir", required=True, help="输出目录")
    parser.add_argument("--design-name", default="道具设计.json", help="design master 文件名")
    parser.add_argument("--prompt-name", default="prop_design_prompt.json", help="prompt sidecar 文件名")
    parser.add_argument("--manifest-name", default="_manifest.json", help="manifest 文件名")
    parser.add_argument("--dry-run", action="store_true", help="只预览，不写文件")
    return parser.parse_args()


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def read_text(path: Path | None) -> str:
    if path is None or not path.exists():
        return ""
    return path.read_text(encoding="utf-8")


def compact_text(text: str, limit: int = 220) -> str:
    compact = " ".join(text.split())
    if len(compact) <= limit:
        return compact
    return compact[: limit - 3] + "..."


def lookup_item(items: list[dict[str, Any]], key: str, fallback_key: str) -> dict[str, Any]:
    indexed = {str(item.get("prop_id", "")): item for item in items if item.get("prop_id")}
    if key and key in indexed:
        return indexed[key]
    by_name = {str(item.get("canonical_name", "")): item for item in items if item.get("canonical_name")}
    return by_name.get(fallback_key, {})


def infer_design_goal(
    prop_name: str,
    route: dict[str, Any],
    functions: list[str],
    narrative_significance: dict[str, Any] | None = None,
) -> str:
    function_hint = functions[0] if functions else "story_support"
    route_hint = str(route.get("route_type", "coverage"))
    if narrative_significance and narrative_significance.get("is_special"):
        return (
            f"把 {prop_name} 按{narrative_significance.get('level', 'notable')}级叙事道具处理，"
            f"保留其 {function_hint} 识别度，并确保 {route_hint} 路径下的关键可读性。"
        )
    return f"保持 {prop_name} 的 {function_hint} 识别度，并让它在 {route_hint} 镜头路径中始终可辨识。"


def infer_continuity_rule(route: dict[str, Any], wear_marks: list[str]) -> str:
    route_hint = str(route.get("route_type", "coverage"))
    wear_hint = "、".join(wear_marks[:2]) if wear_marks else "当前状态"
    return f"在 {route_hint} 路径中持续保留 {wear_hint} 的可见痕迹，不把状态词并入 canonical 名称。"


def normalize_narrative_significance(
    bridge_prop: dict[str, Any],
    research_prop: dict[str, Any],
    functions: list[str],
    shot_route: dict[str, Any],
) -> dict[str, Any]:
    candidate = bridge_prop.get("narrative_significance") or research_prop.get("narrative_significance") or {}
    level = str(candidate.get("level", "background"))
    if level not in {"critical", "notable", "background"}:
        level = "background"
    is_special = bool(candidate.get("is_special", level in {"critical", "notable"}))
    story_function = str(candidate.get("story_function", functions[0] if functions else "story_support"))
    route_type = str(candidate.get("route_type", shot_route.get("route_type", "standard")))
    return {
        "is_special": is_special,
        "level": level,
        "story_function": story_function,
        "reason": str(candidate.get("reason", "")),
        "visual_obligation": str(candidate.get("visual_obligation", "")),
        "continuity_guard": str(candidate.get("continuity_guard", "")),
        "evidence_count": int(candidate.get("evidence_count", 0) or 0),
        "state_change_required": bool(candidate.get("state_change_required", False)),
        "route_type": route_type,
        "anchor_states": candidate.get("anchor_states", []),
    }


def build_prompt_text(prop: dict[str, Any]) -> str:
    structure = "；".join(prop.get("structure_modules", [])[:3])
    material = "；".join(prop.get("material_and_finish", [])[:3])
    wear = "；".join(prop.get("wear_marks", [])[:3])
    style_refs = prop.get("style_refs", {})
    narrative_significance = prop.get("design_thesis", {}).get("narrative_significance", {})
    narrative_clause = ""
    if narrative_significance.get("is_special"):
        narrative_clause = (
            f" 该道具具有{narrative_significance.get('level', 'notable')}级叙事权重，"
            f"必须保留{narrative_significance.get('visual_obligation', '关键可读性')}。"
        )
    style_hint = " ".join(
        filter(
            None,
            [
                style_refs.get("north_star_ref", ""),
                style_refs.get("global_style_ref", ""),
                style_refs.get("type_guide_ref", ""),
            ],
        )
    )
    return (
        f"为 {prop['canonical_name']} 生成专业 PROP_DESIGN_SHEET 道具设计页，16:9 三栏布局，"
        f"主体必须突出其功能骨架与轮廓识别。结构重点：{structure}。"
        f"材质与表面：{material}。磨损与状态：{wear}。"
        f"{narrative_clause}"
        f"风格锚点：{style_hint or '遵循项目既有风格，不额外发明新流派。'} "
        f"保持背景克制，不让布局说明覆盖道具本体，避免加入上游证据不存在的附属零件。"
    )


def build_payloads(
    *,
    bridge: dict[str, Any],
    research: dict[str, Any],
    catalog: dict[str, Any] | None,
    detail_path: Path,
    global_style_text: str,
    type_guide_text: str,
    north_star_text: str,
    init_handoff_text: str,
    bridge_path: Path,
    research_path: Path,
) -> tuple[dict[str, Any], dict[str, Any], dict[str, Any]]:
    bridge_props = bridge.get("props", [])
    research_props = research.get("props", [])
    catalog_props = catalog.get("props", []) if catalog else []
    detail = read_json(detail_path)
    episode_id = str(bridge.get("meta", {}).get("episode_id") or detail_path.stem)
    project_name = str(
        bridge.get("meta", {}).get("project_name")
        or research.get("meta", {}).get("project_name")
        or detail.get("项目名", "项目名")
    )

    design_props: list[dict[str, Any]] = []
    prompt_props: list[dict[str, Any]] = []

    for bridge_prop in bridge_props:
        prop_id = str(bridge_prop.get("prop_id", ""))
        canonical_name = str(bridge_prop.get("canonical_name", "unknown"))
        research_prop = lookup_item(research_props, prop_id, canonical_name)
        catalog_prop = lookup_item(catalog_props, prop_id, canonical_name)
        attribute_profile = research_prop.get("attribute_profile", {})
        scene_usage_profile = research_prop.get("scene_usage_profile", {})
        functions = attribute_profile.get("primary_functions", [])
        wear_marks = bridge_prop.get("wear_marks", [])
        shot_route = bridge_prop.get("shot_route", {})
        narrative_significance = normalize_narrative_significance(
            bridge_prop=bridge_prop,
            research_prop=research_prop,
            functions=functions,
            shot_route=shot_route,
        )

        design_prop = {
            "prop_id": prop_id,
            "canonical_name": canonical_name,
            "prop_type": bridge_prop.get("prop_type", "general_prop"),
            "evidence": {
                "group_ids": scene_usage_profile.get("group_ids", catalog_prop.get("group_ids", [])),
                "shot_ids": scene_usage_profile.get("shot_ids", catalog_prop.get("shot_ids", [])),
                "evidence_ledger": research_prop.get("evidence_ledger", []),
            },
            "design_thesis": {
                "design_goal": infer_design_goal(canonical_name, shot_route, functions, narrative_significance),
                "narrative_function": functions[0] if functions else "story_support",
                "narrative_significance": narrative_significance,
                "silhouette_hook": (bridge_prop.get("structure_modules") or [f"{canonical_name} 的主轮廓"])[0],
                "continuity_rule": narrative_significance.get("continuity_guard")
                or infer_continuity_rule(shot_route, wear_marks),
            },
            "structure_modules": bridge_prop.get("structure_modules", []),
            "material_and_finish": bridge_prop.get("material_and_finish", []),
            "wear_marks": wear_marks,
            "shot_route": shot_route,
            "physical_character": bridge_prop.get("physical_character", {}),
            "display_profile": bridge_prop.get("display_profile", research_prop.get("display_profile", {})),
            "style_refs": {
                "north_star_ref": compact_text(north_star_text),
                "global_style_ref": compact_text(global_style_text),
                "type_guide_ref": compact_text(type_guide_text),
                "master_method_mapping": [],
                "signature_motif": [],
                "init_handoff_ref": compact_text(init_handoff_text),
            },
            "negative_constraints": bridge_prop.get("negative_constraints", []),
            "render_contract": {
                "target_skill_id": "nano-banana-multiview-prop",
                "render_mode": "PROP_DESIGN_SHEET",
                "aspect_ratio": "16:9",
                "layout": "three-column",
                "reference_priority": [
                    "canonical_design",
                    "project_style",
                    "prompt_sidecar",
                ],
            },
            "prompt_anchor": bridge_prop.get("prompt_anchor", canonical_name),
        }
        design_props.append(design_prop)

        prompt_props.append(
            {
                "prop_id": prop_id,
                "canonical_name": canonical_name,
                "target_skill_id": "nano-banana-multiview-prop",
                "prompt_cn": build_prompt_text(design_prop),
                "negative_constraints": design_prop["negative_constraints"],
                "narrative_focus": {
                    "level": narrative_significance.get("level", "background"),
                    "visual_obligation": narrative_significance.get("visual_obligation", ""),
                },
                "render_hints": {
                    "render_mode": "PROP_DESIGN_SHEET",
                    "aspect_ratio": "16:9",
                    "layout": "three-column",
                },
            }
        )

    design_payload = {
        "meta": {
            "project_name": project_name,
            "episode_id": episode_id,
            "skill_id": "aigc/4-Design/4-道具/2-设计",
            "source_bridge": bridge_path.as_posix(),
            "source_research": research_path.as_posix(),
        },
        "props": design_props,
    }
    prompt_payload = {
        "meta": {
            "project_name": project_name,
            "episode_id": episode_id,
            "skill_id": "aigc/4-Design/4-道具/2-设计",
            "source_design_master": "道具设计.json",
        },
        "props": prompt_props,
    }
    manifest_payload = {
        "meta": {
            "project_name": project_name,
            "episode_id": episode_id,
            "skill_id": "aigc/4-Design/4-道具/2-设计",
        },
        "inputs": {
            "bridge": bridge_path.as_posix(),
            "research": research_path.as_posix(),
            "detail": detail_path.as_posix(),
        },
        "outputs": {
            "design_master": "道具设计.json",
            "prompt_sidecar": "prop_design_prompt.json",
            "manifest": "_manifest.json",
        },
        "selected_agents": SELECTED_AGENTS,
        "coverage": {
            "prop_count": len(design_props),
            "special_narrative_prop_count": sum(
                1 for item in design_props if item.get("design_thesis", {}).get("narrative_significance", {}).get("is_special")
            ),
            "has_design_master": True,
            "has_prompt_sidecar": True,
            "has_catalog": catalog is not None,
        },
        "path_normalization": {
            "requested_output_root": "",
            "canonical_output_root": "",
        },
    }
    return design_payload, prompt_payload, manifest_payload


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def main() -> int:
    args = parse_args()
    bridge_path = Path(args.bridge)
    research_path = Path(args.research)
    detail_path = Path(args.detail)
    catalog_path = Path(args.catalog) if args.catalog else None
    output_dir = Path(args.output_dir)

    missing = [path.as_posix() for path in (bridge_path, research_path, detail_path) if not path.exists()]
    if missing:
        print("[ERROR] 缺少必需输入：", ", ".join(missing), file=sys.stderr)
        return 1

    bridge = read_json(bridge_path)
    research = read_json(research_path)
    catalog = read_json(catalog_path) if catalog_path and catalog_path.exists() else None

    design_payload, prompt_payload, manifest_payload = build_payloads(
        bridge=bridge,
        research=research,
        catalog=catalog,
        detail_path=detail_path,
        global_style_text=read_text(Path(args.global_style) if args.global_style else None),
        type_guide_text=read_text(Path(args.type_guide) if args.type_guide else None),
        north_star_text=read_text(Path(args.north_star) if args.north_star else None),
        init_handoff_text=read_text(Path(args.init_handoff) if args.init_handoff else None),
        bridge_path=bridge_path,
        research_path=research_path,
    )
    manifest_payload["path_normalization"]["requested_output_root"] = output_dir.as_posix()
    manifest_payload["path_normalization"]["canonical_output_root"] = output_dir.as_posix()

    if args.dry_run:
        print(json.dumps(manifest_payload, ensure_ascii=False, indent=2))
        return 0

    output_dir.mkdir(parents=True, exist_ok=True)
    write_json(output_dir / args.design_name, design_payload)
    write_json(output_dir / args.prompt_name, prompt_payload)
    write_json(output_dir / args.manifest_name, manifest_payload)

    print(f"[OK] 写入道具设计主稿: {(output_dir / args.design_name).as_posix()}")
    print(f"[OK] 写入 prompt sidecar: {(output_dir / args.prompt_name).as_posix()}")
    print(f"[OK] 写入 manifest: {(output_dir / args.manifest_name).as_posix()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
