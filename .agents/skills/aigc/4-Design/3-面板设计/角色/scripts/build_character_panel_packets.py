#!/usr/bin/env python3
"""Build character panel layout packets from character design carriers."""

from __future__ import annotations

import argparse
import importlib.util
import json
import re
import sys
from datetime import datetime
from pathlib import Path
from typing import Any


IMAGE_EXTENSIONS = {".png", ".jpg", ".jpeg", ".webp"}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="从角色设计稿生成角色面板 layout packet。")
    parser.add_argument("--design-json", required=True, help="character_design.json 路径")
    parser.add_argument("--output-dir", help="输出目录，默认推断为 3-面板/第N集/")
    parser.add_argument("--template", help="面板模板路径，默认使用本技能模板")
    parser.add_argument("--role-filter", help="逗号分隔的 role_id / 角色名 过滤列表")
    parser.add_argument(
        "--reference",
        action="append",
        default=[],
        help="显式追加参考图路径，可重复传入",
    )
    parser.add_argument("--auto-generate", action="store_true", help="写完 packet 后自动桥接到 nano-banana/general")
    parser.add_argument(
        "--smart-mode",
        choices=("auto", "continuous-batch", "single-doc-t2i", "off"),
        default="auto",
        help="自动生图桥的 SMART 模式",
    )
    parser.add_argument("--max-concurrent", type=int, default=100, help="自动生图桥最大并发")
    parser.add_argument("--print-payload", action="store_true", help="打印 nano-banana payload")
    parser.add_argument("--no-save-images", action="store_true", help="自动生图时不落 PNG，只保留请求与报告")
    parser.add_argument("--no-report", action="store_true", help="自动生图时跳过 nano-banana report JSON")
    parser.add_argument("--manifest-name", default="_manifest.json", help="manifest 文件名")
    parser.add_argument("--dry-run", action="store_true", help="只输出 manifest 预览，不写文件")
    return parser.parse_args()


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def compact_text(value: Any) -> str:
    if isinstance(value, str):
        return " ".join(value.split())
    if isinstance(value, list):
        parts = [compact_text(item) for item in value]
        return "；".join(part for part in parts if part)
    if isinstance(value, dict):
        parts: list[str] = []
        for key, item in value.items():
            text = compact_text(item)
            if text:
                parts.append(f"{key}: {text}")
        return "；".join(parts)
    return "" if value is None else str(value)


def infer_output_dir(design_json_path: Path) -> Path:
    parts = list(design_json_path.parts)
    candidates = [
        ("4-Design", "角色", "2-设计"),
        ("2-角色", "2-设计"),
    ]
    for candidate in candidates:
        candidate_len = len(candidate)
        for index in range(len(parts) - candidate_len):
            if tuple(parts[index : index + candidate_len]) != candidate:
                continue
            replaced = parts[:]
            if candidate[0] == "4-Design":
                replaced[index + 2] = "3-面板"
            else:
                replaced[index + 1] = "3-面板"
            return Path(*replaced[:-1])
    raise ValueError(
        "design-json 不在 `4-Design/角色/2-设计/` 或兼容旧路径 `2-角色/2-设计/` 下，无法自动推断输出路径。"
    )


def make_safe_token(value: str) -> str:
    safe = re.sub(r"[\\/:*?\"<>|]+", "-", value.strip())
    safe = re.sub(r"\s+", "-", safe)
    safe = safe.strip("-")
    return safe or "unknown"


def _load_panel_auto_generate_module() -> Any:
    module_path = Path(__file__).resolve().parents[2] / "_shared" / "panel_auto_generate.py"
    spec = importlib.util.spec_from_file_location("panel_auto_generate_bridge", module_path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"无法加载自动生图桥接脚本: {module_path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def parse_filters(raw: str | None) -> set[str]:
    if not raw:
        return set()
    return {item.strip() for item in raw.split(",") if item.strip()}


def select_roles(roles: list[dict[str, Any]], filters: set[str]) -> list[dict[str, Any]]:
    if not filters:
        return roles
    selected = [
        role
        for role in roles
        if str(role.get("role_id", "")) in filters or str(role.get("canonical_name", "")) in filters
    ]
    if not selected:
        raise ValueError(f"未匹配到任何角色过滤条件: {sorted(filters)}")
    return selected


def extract_prompt_integration(markdown_text: str) -> str:
    if "**prompt整合**" not in markdown_text:
        return ""
    tail = markdown_text.split("**prompt整合**", 1)[1].strip()
    tail = re.split(r"\n##\s+|\n\*\*[^*]+\*\*\s*", tail, maxsplit=1)[0]
    return tail.strip()


def synthesize_design_subject(role: dict[str, Any]) -> str:
    lines = [
        f"角色身份：{compact_text(role.get('canonical_name'))}",
        f"视觉锚点：{compact_text(role.get('visual_anchor'))}",
        f"脸部特征：{compact_text(role.get('face_signature'))}",
        f"身体与轮廓：{compact_text(role.get('body_signature'))}；{compact_text(role.get('silhouette_signature'))}",
        f"服装系统：{compact_text(role.get('wardrobe_profile'))}",
        f"妆容与发型：{compact_text(role.get('makeup_profile'))}",
        f"性格与姿态：{compact_text(role.get('personality_profile'))}；{compact_text(role.get('pose_profile'))}",
        f"情绪锚点：{compact_text(role.get('emotion_anchor'))}",
        f"负面约束：{compact_text(role.get('negative_constraints'))}",
    ]
    return "\n".join(line for line in lines if line.split("：", 1)[1].strip())


def collect_reference_images(markdown_path: Path | None) -> list[str]:
    if markdown_path is None or not markdown_path.exists():
        return []
    return sorted(
        file.as_posix()
        for file in markdown_path.parent.iterdir()
        if file.is_file() and file.suffix.lower() in IMAGE_EXTENSIONS
    )


def build_layout_prompt(layout_generation_prompt: dict[str, Any]) -> str:
    lines = [layout_generation_prompt.get("canvas_setup", ""), ""]
    for key in ("left_panel_instructions", "center_panel_instructions", "right_panel_instructions"):
        section = layout_generation_prompt.get(key, {})
        title = section.get("title", "")
        if title:
            lines.append(title)
        for module in section.get("modules", []):
            lines.append(f"- {module.get('module', 'MODULE')}: {module.get('content', '')}")
        lines.append("")
    lines.append("Critical requirements:")
    for requirement in layout_generation_prompt.get("critical_requirements", []):
        lines.append(f"- {requirement}")
    return "\n".join(line for line in lines if line is not None).strip()


def build_prompt_text(
    *,
    role: dict[str, Any],
    design_subject: str,
    identity_badge: str,
    layout_prompt: str,
    group_portrait: bool,
) -> str:
    role_id = str(role.get("role_id", "unknown"))
    role_name = str(role.get("canonical_name", "未知角色"))
    negative_constraints = compact_text(role.get("negative_constraints"))
    lines = [
        f"### 角色ID: {role_id}",
        f"### 角色名: {role_name}",
        f"### 固定标签: {identity_badge}",
        "",
        "【设计主体】",
        design_subject,
        "",
        "【布局合同】",
        layout_prompt,
    ]
    if group_portrait:
        lines.extend(
            [
                "",
                "【群像模式】",
                "该角色属于 crowd 群像层，请将 layout 理解为同阶层、同世界观口径的 3-5 人群像角色设计板，而不是单一人物的 rigid turnaround sheet。保留差异轴，不得多人同脸复制。",
            ]
        )
    if negative_constraints:
        lines.extend(["", "【负面约束】", negative_constraints])
    return "\n".join(lines).strip()


def build_packet(
    *,
    role: dict[str, Any],
    template_path: Path,
    template_payload: dict[str, Any],
    design_subject: str,
    design_subject_source: str,
    project_name: str,
    episode_id: str,
    design_json_path: Path,
    markdown_path: Path | None,
    explicit_references: list[str],
) -> tuple[str, dict[str, Any]]:
    role_id = str(role.get("role_id", "role"))
    role_name = str(role.get("canonical_name", "未知角色"))
    role_tier = str(role.get("role_tier", "support"))
    costume_state = str(role.get("costume_state", "baseline"))
    identity_badge = f"{role_id}+{role_name}"
    group_portrait = role_tier == "crowd"
    local_references = collect_reference_images(markdown_path)
    continuity_source_roots = [design_json_path.parent.as_posix()]
    if markdown_path:
        continuity_source_roots.append(markdown_path.parent.as_posix())
    layout_prompt = build_layout_prompt(template_payload["layout_generation_prompt"])
    prompt_text = build_prompt_text(
        role=role,
        design_subject=design_subject,
        identity_badge=identity_badge,
        layout_prompt=layout_prompt,
        group_portrait=group_portrait,
    )

    prompt_payload = {
        "layout": template_payload["layout"],
        "render_style_contract": template_payload["render_style_contract"],
        "rule_profile": template_payload["rule_profile"],
        "views": template_payload.get("views", {}),
        "optional_viewpacks": template_payload.get("optional_viewpacks", {}),
        "prompt_segments": {
            "identity_prompt": identity_badge,
            "design_subject_prompt": design_subject,
            "layout_prompt": layout_prompt,
            "group_mode_prompt": "crowd_group_portrait" if group_portrait else "",
            "negative_prompt_global": compact_text(role.get("negative_constraints")),
        },
        "prompt_text": prompt_text,
    }

    filename = "-".join(
        [
            make_safe_token(role_id),
            make_safe_token(role_name),
            make_safe_token(costume_state),
            "CharacterPanel-layout.json",
        ]
    )

    packet = {
        "meta": {
            "project_name": project_name,
            "episode_id": episode_id,
            "skill_id": "aigc/4-Design/角色/3-面板",
            "generated_at": datetime.now().astimezone().isoformat(timespec="seconds"),
            "template_path": template_path.as_posix(),
            "source_character_design": design_json_path.as_posix(),
            "source_role_markdown": markdown_path.as_posix() if markdown_path else "",
        },
        "subject": {
            "role_id": role_id,
            "role_name": role_name,
            "role_tier": role_tier,
            "costume_state": costume_state,
            "identity_badge": identity_badge,
            "group_portrait": group_portrait,
        },
        "design_subject_source": design_subject_source,
        "design_subject": design_subject,
        "prompt_payload": prompt_payload,
        "references": {
            "reference_images": local_references,
            "explicit_references": explicit_references,
        },
        "render_contract": {
            "target_skill_id": "nano-banana-multiview-character",
            "render_mode": "CHARACTER_ATMOSPHERIC_DOSSIER",
            "aspect_ratio": template_payload["layout"]["aspect_ratio"],
            "layout": "three-column",
        },
        "image_generation": {
            "target_skill_id": "nano-banana-general",
            "smart_mode_default": "continuous-batch",
            "prompt_field": "prompt_payload.prompt_text",
            "prompt_text": prompt_text,
            "prompt_reference_sections": [
                "prompt_payload.prompt_text",
                "prompt_payload.prompt_segments.identity_prompt",
                "prompt_payload.prompt_segments.design_subject_prompt",
                "prompt_payload.prompt_segments.layout_prompt",
                "prompt_payload.prompt_segments.negative_prompt_global",
            ],
            "reference_images": local_references,
            "explicit_references": explicit_references,
            "continuity_source_roots": list(dict.fromkeys(continuity_source_roots)),
            "output_filename": filename.replace("-layout.json", ".png"),
            "request_id": filename.replace("-layout.json", ""),
        },
        "output": {
            "packet_filename": filename,
            "target_image_filename": filename.replace("-layout.json", ".png"),
        },
    }
    return filename, packet


def resolve_markdown_path(role: dict[str, Any], design_json_path: Path) -> Path | None:
    structured_path = str(role.get("structured_markdown_path", "")).strip()
    if structured_path:
        path = Path(structured_path)
        if path.exists():
            return path
    fallback = design_json_path.parent / f"{role.get('canonical_name', '角色')}.md"
    return fallback if fallback.exists() else None


def main() -> int:
    args = parse_args()
    design_json_path = Path(args.design_json)
    if not design_json_path.exists():
        print(f"[ERROR] 缺少 design-json: {design_json_path.as_posix()}", file=sys.stderr)
        return 1

    template_path = (
        Path(args.template)
        if args.template
        else Path(__file__).resolve().parents[1] / "templates/角色面板-提示词.json"
    )
    if not template_path.exists():
        print(f"[ERROR] 缺少模板: {template_path.as_posix()}", file=sys.stderr)
        return 1

    design_payload = read_json(design_json_path)
    roles = design_payload.get("roles", [])
    if not roles:
        print("[ERROR] character_design.json.roles[] 为空。", file=sys.stderr)
        return 1

    try:
        selected_roles = select_roles(roles, parse_filters(args.role_filter))
    except ValueError as exc:
        print(f"[ERROR] {exc}", file=sys.stderr)
        return 1

    try:
        output_dir = Path(args.output_dir) if args.output_dir else infer_output_dir(design_json_path)
    except ValueError as exc:
        print(f"[ERROR] {exc}", file=sys.stderr)
        return 1

    template_payload = read_json(template_path)["prompt_payload"]
    project_name = str(design_payload.get("meta", {}).get("project_name", "项目名"))
    episode_id = str(
        design_payload.get("meta", {}).get("episode_id") or design_json_path.parent.name or "第1集"
    )

    packets: list[tuple[str, dict[str, Any]]] = []
    reference_image_total = 0
    group_portrait_total = 0

    for role in selected_roles:
        markdown_path = resolve_markdown_path(role, design_json_path)
        markdown_text = markdown_path.read_text(encoding="utf-8") if markdown_path else ""
        prompt_integration = extract_prompt_integration(markdown_text)
        if prompt_integration:
            design_subject = prompt_integration
            design_subject_source = "markdown_prompt_integration"
        else:
            design_subject = synthesize_design_subject(role)
            design_subject_source = "fallback_json_synthesis"

        filename, packet = build_packet(
            role=role,
            template_path=template_path,
            template_payload=template_payload,
            design_subject=design_subject,
            design_subject_source=design_subject_source,
            project_name=project_name,
            episode_id=episode_id,
            design_json_path=design_json_path,
            markdown_path=markdown_path,
            explicit_references=args.reference,
        )
        reference_image_total += len(packet["references"]["reference_images"]) + len(
            packet["references"]["explicit_references"]
        )
        group_portrait_total += 1 if packet["subject"]["group_portrait"] else 0
        packets.append((filename, packet))

    manifest = {
        "meta": {
            "project_name": project_name,
            "episode_id": episode_id,
            "skill_id": "aigc/4-Design/角色/3-面板",
        },
        "inputs": {
            "character_design": design_json_path.as_posix(),
            "template": template_path.as_posix(),
        },
        "outputs": {
            "packet_files": [filename for filename, _ in packets],
            "manifest": args.manifest_name,
        },
        "selected_roles": [str(role.get("role_id", "")) for role in selected_roles],
        "statistics": {
            "role_count": len(packets),
            "group_portrait_count": group_portrait_total,
            "reference_image_count": reference_image_total,
        },
        "handoff_targets": [
            "5-Image",
            "nano-banana-general",
            "nano-banana-multiview-character",
        ],
    }
    if args.auto_generate:
        manifest["image_generation"] = {
            "enabled": True,
            "smart_mode_requested": args.smart_mode,
            "status": "pending" if not args.dry_run else "skipped-dry-run",
        }

    if args.dry_run:
        print(json.dumps(manifest, ensure_ascii=False, indent=2))
        return 0

    output_dir.mkdir(parents=True, exist_ok=True)
    for filename, packet in packets:
        write_json(output_dir / filename, packet)
    packet_paths = [output_dir / filename for filename, _ in packets]

    auto_generate_failed = False
    if args.auto_generate:
        try:
            bridge_module = _load_panel_auto_generate_module()
            auto_generate_result = bridge_module.run_panel_auto_generate(
                packet_paths,
                manifest_path=output_dir / args.manifest_name,
                smart_mode=args.smart_mode,
                explicit_references=args.reference,
                max_concurrent=args.max_concurrent,
                print_payload=args.print_payload,
                save_images=not args.no_save_images,
                no_report=args.no_report,
                pipeline_context="panel-stage",
            )
            manifest["image_generation"] = {
                "enabled": True,
                "smart_mode_requested": args.smart_mode,
                "smart_mode_resolved": auto_generate_result.get("smart_mode_resolved", ""),
                "success": bool(auto_generate_result.get("success", False)),
                "task_count": auto_generate_result.get("task_count", 0),
                "success_count": auto_generate_result.get("success_count", 0),
                "failed_count": auto_generate_result.get("failed_count", 0),
                "request_batch_path": auto_generate_result.get("request_batch_path"),
                "bridge_report_path": auto_generate_result.get("bridge_report_path"),
                "batch_report_path": auto_generate_result.get("batch_report_path"),
            }
            auto_generate_failed = not bool(auto_generate_result.get("success", False))
        except Exception as exc:
            manifest["image_generation"] = {
                "enabled": True,
                "smart_mode_requested": args.smart_mode,
                "success": False,
                "error": str(exc),
            }
            auto_generate_failed = True

    write_json(output_dir / args.manifest_name, manifest)

    print(f"[OK] 写入角色面板 packet 数量: {len(packets)}")
    print(f"[OK] 输出目录: {output_dir.as_posix()}")
    print(f"[OK] 写入 manifest: {(output_dir / args.manifest_name).as_posix()}")
    if args.auto_generate:
        print(f"[OK] 自动生图桥状态: {manifest['image_generation']['success']}")
    return 1 if auto_generate_failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
