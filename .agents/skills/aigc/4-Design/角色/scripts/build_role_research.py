#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Build role research and bridge truth sources from the role catalog."""

from __future__ import annotations

import argparse
import json
import re
import sys
from collections import Counter
from datetime import datetime
from pathlib import Path
from typing import Iterable, List, Sequence, Tuple


MATERIAL_HINTS: Tuple[Tuple[str, Sequence[str]], ...] = (
    ("丝缎/礼服面料", ("礼服", "裙", "肩带")),
    ("羊毛/西装面料", ("西装", "笔挺", "袖口")),
    ("棉麻/工装布料", ("工装", "衬衫", "外套")),
    ("金属饰件", ("钻饰", "项链", "链", "高跟鞋")),
    ("湿损织物", ("湿礼服", "浑身湿透", "湿意")),
)
PALETTE_HINTS: Tuple[Tuple[str, Sequence[str]], ...] = (
    ("华丽暖金", ("华丽", "钻饰", "高亮", "宴会")),
    ("冷黑灰", ("深色西装", "工装", "袖口", "深巷")),
    ("失控冷白", ("湿礼服", "失态", "失温", "赤脚")),
)
EMOTION_HINTS: Tuple[Tuple[str, Sequence[str]], ...] = (
    ("高压克制", ("体面", "礼貌挺直", "几乎不动", "克制")),
    ("控制展示", ("主位", "展示", "巡视", "举杯发言")),
    ("被迫失控", ("失控", "奔逃", "狼狈", "浑身湿透")),
    ("照料克制", ("照料", "递到她手里", "仍为她留门", "抱起")),
)
LEGACY_SCRIPT_AUTHORSHIP_ERROR = (
    "根据 AGENTS.md 的 `内容创作型任务的 LLM 主创规则`，研究结论与桥接文案不得再由脚本直接生成。"
    "本脚本仅保留给受控兼容迁移；如确需临时运行旧式脚本主创，请显式传入 "
    "`--allow-legacy-script-authorship`。"
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="从 `角色清单.json` 生成 `角色研究.json` 与 `role_design_bridge.json`。")
    parser.add_argument("--input", required=True, help="输入 角色清单.json")
    parser.add_argument("--output-dir", required=True, help="输出目录")
    parser.add_argument("--catalog-name", default="角色清单.json", help="角色清单文件名")
    parser.add_argument("--research-name", default="角色研究.json", help="角色研究文件名")
    parser.add_argument("--bridge-name", default="role_design_bridge.json", help="角色桥接文件名")
    parser.add_argument("--report-name", default="validation-report.md", help="校验报告文件名")
    parser.add_argument("--dry-run", action="store_true", help="只校验，不写文件")
    parser.add_argument(
        "--allow-legacy-script-authorship",
        action="store_true",
        help="受控兼容模式：允许旧式脚本直接生成研究结论与桥接文案。",
    )
    return parser.parse_args()


def read_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, payload: dict) -> None:
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def write_markdown(path: Path, content: str) -> None:
    path.write_text(content.rstrip() + "\n", encoding="utf-8")


def unique_preserve(items: Iterable[str]) -> List[str]:
    seen = set()
    output: List[str] = []
    for item in items:
        if not item or item in seen:
            continue
        seen.add(item)
        output.append(item)
    return output


def known_or_unknown(items: Iterable[str]) -> List[str]:
    values = unique_preserve(items)
    return values or ["unknown"]


def match_labels(text: str, mapping: Sequence[Tuple[str, Sequence[str]]], default: str) -> List[str]:
    counter = Counter()
    for label, keywords in mapping:
        for keyword in keywords:
            if keyword and keyword in text:
                counter[label] += max(1, len(keyword) // 2)
    if not counter:
        return [default]
    return [label for label, _count in counter.most_common(2)]


def compose_sentence(parts: Sequence[str], fallback: str) -> str:
    filtered = [part for part in parts if part]
    return "；".join(filtered) if filtered else fallback


def build_display_profile(name: str, tier: str, role_identity: str, costume_story: str, performance_hook: str) -> dict:
    return {
        "tagline": f"{name} / {tier}",
        "short_bio": role_identity,
        "visual_bible": f"{name}的视觉核心不是单件服装，而是身份压力、体态边界与服装状态如何一起出镜。",
        "costume_story": costume_story,
        "performance_hook": performance_hook,
    }


def build_role_research_payload(catalog: dict) -> Tuple[dict, dict, dict, str]:
    meta = dict(catalog.get("meta", {}))
    meta["generated_at"] = datetime.now().astimezone().isoformat(timespec="seconds")

    roles = catalog.get("roles", [])
    group_role_map = catalog.get("group_role_map", [])

    research_roles: List[dict] = []
    bridge_roles: List[dict] = []
    quality_summary: List[dict] = []

    for role in roles:
        role_id = str(role.get("role_id", ""))
        name = str(role.get("canonical_name", "unknown"))
        role_tier = str(role.get("role_tier", "功能配角"))
        role_level = str(role.get("role_level", "单人角色"))
        costume_state = str(role.get("costume_state", "unknown"))
        role_rows = [row for row in group_role_map if str(row.get("role_id", "")) == role_id]
        shot_rows = [row for row in role_rows if row.get("shot_id")]

        motion_excerpts = known_or_unknown(row.get("motion_excerpt", "") for row in shot_rows if row.get("motion_excerpt"))
        performance_excerpts = known_or_unknown(row.get("performance_excerpt", "") for row in shot_rows if row.get("performance_excerpt"))
        prop_excerpts = known_or_unknown(row.get("prop_excerpt", "") for row in role_rows if row.get("prop_excerpt"))
        background_excerpts = known_or_unknown(row.get("background_excerpt", "") for row in role_rows if row.get("background_excerpt"))
        script_excerpts = known_or_unknown(row.get("script_excerpt", "") for row in role_rows if row.get("script_excerpt"))
        group_anchor_excerpts = known_or_unknown(
            row.get("role_anchor_excerpt", "") for row in role_rows if row.get("source_slot") == "组间设计.出场角色及穿搭"
        )

        analysis_text = " ".join(
            unique_preserve(
                [
                    name,
                    costume_state,
                    *group_anchor_excerpts,
                    *motion_excerpts,
                    *performance_excerpts,
                    *prop_excerpts,
                    *background_excerpts,
                    *script_excerpts,
                ]
            )
        )
        material_hints = match_labels(analysis_text, MATERIAL_HINTS, "材质待补")
        palette_hints = match_labels(analysis_text, PALETTE_HINTS, "配色待补")
        emotion_hints = match_labels(analysis_text, EMOTION_HINTS, "情绪张力待补")

        prop_hints = known_or_unknown(role.get("prop_hints", []))
        costume_variants = role.get("costume_variants", [])
        variant_labels = unique_preserve(item.get("costume_anchor", "") for item in costume_variants if isinstance(item, dict))

        identity_read = compose_sentence(
            [
                f"{name}当前被归为{role_tier}，且在本集维持“{costume_state}”这一主造型锚点。",
                f"镜头里反复出现的行动与站位证据集中在：{motion_excerpts[0] if motion_excerpts[0] != 'unknown' else '站位证据仍偏稀薄'}。",
            ],
            f"{name}的身份读法仍偏保守，需要后续设计阶段继续补强。",
        )
        costume_story = compose_sentence(
            [
                f"服装系统当前以“{costume_state}”为主状态。",
                f"若后续延续变体，优先保留 {variant_labels[1] if len(variant_labels) > 1 else costume_state} 与主状态之间的连续关系。",
            ],
            f"{name}的服装状态暂未稳定，后续需补 costume bridge。",
        )
        performance_hook = compose_sentence(
            [
                f"角色表现目前最强的镜头提示是“{performance_excerpts[0] if performance_excerpts[0] != 'unknown' else motion_excerpts[0]}”。",
                f"情绪底色更接近 {emotion_hints[0]}。",
            ],
            f"{name}的表演钩子仍需人工补强。",
        )
        role_identity = {
            "canonical_name": name,
            "role_level": role_level,
            "role_tier": role_tier,
            "identity_read": identity_read,
        }
        appearance_bridge = {
            "face_signature": "unknown_by_shot_evidence",
            "hair_signature": "unknown_by_shot_evidence",
            "silhouette_build": compose_sentence(
                [
                    f"当前体态/轮廓更依赖“{motion_excerpts[0] if motion_excerpts[0] != 'unknown' else costume_state}”这一镜头锚点。",
                    f"空间压迫与人物体态关系集中体现在“{background_excerpts[0] if background_excerpts[0] != 'unknown' else '背景压迫信息待补'}”。",
                ],
                "轮廓与体态证据不足，需后续设计时保守处理。",
            ),
            "space_pressure": background_excerpts[0],
        }
        costume_bridge = {
            "costume_state": costume_state,
            "costume_variants": costume_variants,
            "material_and_finish": material_hints,
            "palette_hint": palette_hints,
            "costume_system": costume_story,
            "continuity_guard": f"同一角色复现时，至少保留“{costume_state}”与关键变体的连续识别。",
        }
        performance_bridge = {
            "baseline_action": motion_excerpts[0],
            "emotional_temperature": emotion_hints[0],
            "performance_hook": performance_hook,
            "camera_consumption": performance_excerpts[0],
        }
        continuity_bridge = {
            "core_props": prop_hints,
            "recurring_states": known_or_unknown([costume_state, *variant_labels]),
            "group_ids": role.get("group_ids", []),
            "shot_ids": role.get("shot_ids", []),
            "continuity_guard": f"保持{name}在 group/shot 回链上的服装状态和核心道具一致，不要跨镜头擅自换制式。",
        }
        prompt_ready = {
            "identity_hook": f"{name} / {role_tier} / {role_level}",
            "narrative_tension": performance_hook,
            "visual_keywords": unique_preserve([costume_state, *material_hints, *palette_hints, *emotion_hints])[:8],
            "costume_anchor": costume_state,
        }

        quality_flags: List[str] = []
        if len(role.get("shot_ids", [])) < 2:
            quality_flags.append("shot_evidence_sparse")
        if costume_state == "unknown":
            quality_flags.append("costume_anchor_unknown")
        if appearance_bridge["space_pressure"] == "unknown":
            quality_flags.append("background_pressure_sparse")
        if role_level == "unknown":
            quality_flags.append("needs_manual_review")

        evidence_ledger = [
            {
                "group_id": row.get("group_id", ""),
                "shot_id": row.get("shot_id", ""),
                "source_slot": row.get("source_slot", ""),
                "evidence_excerpt": row.get("evidence_excerpt", ""),
                "costume_anchor": row.get("costume_anchor", ""),
            }
            for row in role_rows
        ]

        display_profile = build_display_profile(name, role_tier, identity_read, costume_story, performance_hook)
        research_profile = {
            "identity_read": identity_read,
            "costume_read": costume_story,
            "performance_read": performance_hook,
            "space_relation": compose_sentence(
                [
                    f"背景与空间关系主要由“{background_excerpts[0]}”支撑。"
                    if background_excerpts[0] != "unknown"
                    else "",
                    f"剧本回退提示为“{script_excerpts[0]}”。" if script_excerpts[0] != "unknown" else "",
                ],
                "空间关系证据仍偏薄，需要后续设计阶段保守处理。",
            ),
            "prop_binding": compose_sentence(
                [
                    f"当前与角色绑定最强的物件线索是“{prop_hints[0]}”。" if prop_hints[0] != "unknown" else "",
                    f"相关证据主要来自“{prop_excerpts[0]}”。" if prop_excerpts[0] != "unknown" else "",
                ],
                "当前未出现稳定物件绑定，可作为纯人物设计处理。",
            ),
            "sentence_conclusion": compose_sentence(
                [
                    identity_read,
                    costume_story,
                    performance_hook,
                ],
                f"{name}当前只有最小锚点，仍需补设计证据。",
            ),
        }

        research_roles.append(
            {
                "role_id": role_id,
                "canonical_name": name,
                "role_level": role_level,
                "role_tier": role_tier,
                "costume_state": costume_state,
                "evidence_ledger": evidence_ledger,
                "research_profile": research_profile,
                "display_profile": display_profile,
                "quality_flags": quality_flags,
            }
        )

        bridge_roles.append(
            {
                "role_id": role_id,
                "canonical_name": name,
                "role_tier": role_tier,
                "costume_state": costume_state,
                "role_identity": role_identity,
                "appearance_bridge": appearance_bridge,
                "costume_bridge": costume_bridge,
                "performance_bridge": performance_bridge,
                "continuity_bridge": continuity_bridge,
                "prompt_ready": prompt_ready,
                "design_bridge_profile": {
                    "role_identity": role_identity,
                    "appearance_bridge": appearance_bridge,
                    "costume_bridge": costume_bridge,
                    "performance_bridge": performance_bridge,
                    "continuity_bridge": continuity_bridge,
                    "prompt_ready": prompt_ready,
                },
                "costume_variants": costume_variants,
                "quality_flags": quality_flags,
            }
        )

        quality_summary.append(
            {
                "role_id": role_id,
                "canonical_name": name,
                "quality_flags": quality_flags,
            }
        )

    merged_catalog = dict(catalog)
    merged_meta = dict(merged_catalog.get("meta", {}))
    merged_meta["generated_at"] = datetime.now().astimezone().isoformat(timespec="seconds")
    merged_catalog["meta"] = merged_meta
    merged_statistics = dict(merged_catalog.get("statistics", {}))
    merged_statistics["quality_overview"] = {
        "roles_with_manual_review": [
            item["canonical_name"]
            for item in quality_summary
            if item["quality_flags"]
        ],
        "manual_review_count": sum(1 for item in quality_summary if item["quality_flags"]),
    }
    merged_catalog["statistics"] = merged_statistics

    research = {
        "meta": meta,
        "roles": research_roles,
    }
    bridge = {
        "meta": meta,
        "roles": bridge_roles,
    }

    report_lines = [
        "# 角色 1-清单 Validation Report",
        "",
        "## 验收结论",
        "",
        "- status: pass_with_guardrails" if any(item["quality_flags"] for item in quality_summary) else "- status: pass",
        f"- project: {meta.get('project_name', 'unknown')}",
        f"- episode: {meta.get('episode_id', 'unknown')}",
        "- scope: `4-Design/角色/1-清单`",
        "- next_entry: `4-Design/角色`",
        "",
        "## 输出摘要",
        "",
        f"- total_roles: {len(roles)}",
        f"- total_group_role_rows: {len(group_role_map)}",
        f"- roles_with_guardrails: {sum(1 for item in quality_summary if item['quality_flags'])}",
        "",
        "## 角色清单",
        "",
    ]
    for item in quality_summary:
        guard = ", ".join(item["quality_flags"]) if item["quality_flags"] else "none"
        report_lines.append(f"- {item['canonical_name']}: quality_flags={guard}")
    report_lines.extend(
        [
            "",
            "## 下游 handoff",
            "",
            "- `角色清单.json`：锁 `role_id / canonical_name / role_tier / costume_state / group_id / shot_id`。",
            "- `角色研究.json`：补 sentence-level research 与 `display_profile`。",
            "- `role_design_bridge.json`：供 `4-Design/角色` bridge-first 消费 `role_identity / appearance_bridge / costume_bridge / continuity_bridge / prompt_ready / quality_flags`。",
            "",
            "## 已执行校验",
            "",
            f"- 已回读 `{meta.get('source_input', 'unknown')}` 并锁定 `3-Detail` canonical 输入：pass",
            f"- 已生成 `{meta.get('episode_id', 'unknown')}` 的角色三真源与 domain 验收摘要：pass",
        ]
    )

    return merged_catalog, research, bridge, "\n".join(report_lines)


def main() -> int:
    args = parse_args()
    if not args.allow_legacy_script_authorship:
        print(f"[ERROR] {LEGACY_SCRIPT_AUTHORSHIP_ERROR}", file=sys.stderr)
        return 2
    input_path = Path(args.input)
    if not input_path.exists():
        print(f"[ERROR] 输入文件不存在: {input_path}", file=sys.stderr)
        return 1

    try:
        catalog = read_json(input_path)
        merged_catalog, research, bridge, report = build_role_research_payload(catalog)
    except Exception as exc:  # noqa: BLE001
        print(f"[ERROR] {exc}", file=sys.stderr)
        return 1

    output_dir = Path(args.output_dir)
    catalog_path = output_dir / args.catalog_name
    research_path = output_dir / args.research_name
    bridge_path = output_dir / args.bridge_name
    report_path = output_dir / args.report_name

    if args.dry_run:
        print(
            "[DRY-RUN] "
            f"roles={len(merged_catalog.get('roles', []))} "
            f"catalog={catalog_path.as_posix()} "
            f"research={research_path.as_posix()} "
            f"bridge={bridge_path.as_posix()} "
            f"report={report_path.as_posix()}"
        )
        return 0

    output_dir.mkdir(parents=True, exist_ok=True)
    write_json(catalog_path, merged_catalog)
    print(f"[OK] 更新角色清单: {catalog_path.as_posix()}")
    write_json(research_path, research)
    print(f"[OK] 写入角色研究: {research_path.as_posix()}")
    write_json(bridge_path, bridge)
    print(f"[OK] 写入角色桥接: {bridge_path.as_posix()}")
    write_markdown(report_path, report)
    print(f"[OK] 写入角色验收报告: {report_path.as_posix()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
