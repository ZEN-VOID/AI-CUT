#!/usr/bin/env python3
from __future__ import annotations

import argparse
import importlib.util
import json
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Any


SCRIPT_DIR = Path(__file__).resolve().parent
SKILL_DIR = SCRIPT_DIR.parent
TEMPLATE_PATH = SKILL_DIR / "templates" / "scene-panel-layout.template.json"
IMAGE_EXTENSIONS = {".png", ".jpg", ".jpeg", ".webp"}


@dataclass
class ScenePanel:
    scene_key: str
    scene_name: str
    scene_variant: str
    source_scene_ids: list[str]
    panel_prompt: str
    negative_prompt: str
    panel_handoff: str
    design_markdown_path: str


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Generate scene panel carriers from scene design carriers.",
    )
    parser.add_argument("--project", required=True, help="项目名")
    parser.add_argument("--episode", required=True, help="集数，如 第1集")
    parser.add_argument("--scene-key", help="仅生成指定 scene_key")
    parser.add_argument(
        "--design-file",
        help="显式指定场景设计 JSON；默认使用 projects/aigc/<项目名>/4-Design/场景/2-设计/<episode>/场景设计.json",
    )
    parser.add_argument(
        "--output-root",
        help="显式指定输出目录；默认使用 projects/aigc/<项目名>/4-Design/场景/3-面板/<episode>",
    )
    parser.add_argument("--dry-run", action="store_true", help="仅打印将写出的文件")
    parser.add_argument("--force", action="store_true", help="覆盖已存在输出")
    parser.add_argument("--auto-generate", action="store_true", help="写完 panel packet 后自动桥接到 nano-banana/general")
    parser.add_argument(
        "--smart-mode",
        choices=("auto", "continuous-batch", "single-doc-t2i", "off"),
        default="auto",
        help="自动生图桥的 SMART 模式",
    )
    parser.add_argument("--reference", action="append", default=[], help="显式追加参考图，可重复传入")
    parser.add_argument("--max-concurrent", type=int, default=100, help="自动生图桥最大并发")
    parser.add_argument("--print-payload", action="store_true", help="打印 nano-banana payload")
    parser.add_argument("--no-save-images", action="store_true", help="自动生图时不落 PNG")
    parser.add_argument("--no-report", action="store_true", help="自动生图时跳过 nano-banana report JSON")
    return parser.parse_args()


def load_json(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def dump_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as handle:
        json.dump(payload, handle, ensure_ascii=False, indent=2)
        handle.write("\n")


def join_nonempty(parts: list[str], *, separator: str = "\n\n") -> str:
    return separator.join(part.strip() for part in parts if part and part.strip())


def _load_panel_auto_generate_module() -> Any:
    module_path = Path(__file__).resolve().parents[2] / "_shared" / "panel_auto_generate.py"
    spec = importlib.util.spec_from_file_location("panel_auto_generate_bridge", module_path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"无法加载自动生图桥接脚本: {module_path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def collect_adjacent_images(markdown_path: str) -> list[str]:
    text = str(markdown_path).strip()
    if not text:
        return []
    path = Path(text)
    if not path.exists():
        return []
    return sorted(
        file.as_posix()
        for file in path.parent.iterdir()
        if file.is_file() and file.suffix.lower() in IMAGE_EXTENSIONS
    )


def build_negative_prompt(template_payload: dict[str, Any], reverse_taboos: list[str]) -> str:
    prompt_segments = template_payload["prompt_payload"]["prompt_segments"]
    template_bits = [
        prompt_segments.get("negative_prompt_global", ""),
        prompt_segments.get("negative_prompt_layout", ""),
        prompt_segments.get("negative_prompt_motion", ""),
    ]
    taboo_text = ", ".join(item.strip() for item in reverse_taboos if item and item.strip())
    if taboo_text:
        template_bits.append(taboo_text)
    return ", ".join(bit for bit in template_bits if bit)


def build_panel_prompt(template_payload: dict[str, Any], design: dict[str, Any]) -> str:
    payload = template_payload["prompt_payload"]
    layout = payload["layout"]
    contract = payload["panel_sheet_contract"]["constraints"]
    generation = payload["layout_generation_prompt"]
    final_scene_prompt = str(design.get("final_scene_prompt", "")).strip()
    panel_handoff = str(design.get("panel_handoff", "")).strip()
    identity_badge = f'{design["scene_key"]} + {design["scene_name"]}'
    return join_nonempty(
        [
            f"Identity badge: {identity_badge}",
            final_scene_prompt,
            panel_handoff,
            generation.get("canvas_setup", ""),
            "\n".join(f"- {item}" for item in contract),
            "\n".join(f"- {item}" for item in generation.get("critical_requirements", [])),
            f'Layout: {layout["aspect_ratio"]}, {layout["grid"]}, {layout["panel_count"]} panels.',
        ]
    )


def normalize_scene_design(entry: dict[str, Any], template_payload: dict[str, Any]) -> ScenePanel:
    scene_key = str(entry.get("scene_key", "")).strip()
    scene_name = str(entry.get("scene_name", "")).strip()
    final_scene_prompt = str(entry.get("final_scene_prompt", "")).strip()
    if not scene_key or not scene_name or not final_scene_prompt:
        raise ValueError("scene_design entry 缺少 scene_key / scene_name / final_scene_prompt")
    source_scene_ids = [str(item) for item in entry.get("source_scene_ids", [])]
    reverse_taboos = [str(item) for item in entry.get("reverse_taboos", [])]
    design_markdown_path = str(entry.get("design_markdown_path", "")).strip()
    return ScenePanel(
        scene_key=scene_key,
        scene_name=scene_name,
        scene_variant=str(entry.get("scene_variant", "")).strip(),
        source_scene_ids=source_scene_ids,
        panel_prompt=build_panel_prompt(template_payload, entry),
        negative_prompt=build_negative_prompt(template_payload, reverse_taboos),
        panel_handoff=str(entry.get("panel_handoff", "")).strip(),
        design_markdown_path=design_markdown_path,
    )


def ensure_writable(path: Path, force: bool) -> None:
    if path.exists() and not force:
        raise FileExistsError(f"输出已存在，使用 --force 覆盖: {path}")


def main() -> int:
    args = parse_args()
    project_root = Path("projects") / "aigc" / args.project
    design_path = (
        Path(args.design_file)
        if args.design_file
        else project_root / "4-Design" / "场景" / "2-设计" / args.episode / "场景设计.json"
    )
    output_root = (
        Path(args.output_root)
        if args.output_root
        else project_root / "4-Design" / "场景" / "3-面板" / args.episode
    )
    if not design_path.exists():
        raise FileNotFoundError(f"未找到场景设计输入: {design_path}")
    template_payload = load_json(TEMPLATE_PATH)
    design_payload = load_json(design_path)
    scene_designs = design_payload.get("scene_designs")
    if not isinstance(scene_designs, list) or not scene_designs:
        raise ValueError("场景设计 JSON 缺少非空 scene_designs[]")

    selected_entries = []
    for entry in scene_designs:
        if args.scene_key and str(entry.get("scene_key", "")).strip() != args.scene_key:
            continue
        selected_entries.append(normalize_scene_design(entry, template_payload))

    if not selected_entries:
        raise ValueError("没有命中任何 scene_designs；请检查 --scene-key 或输入文件")

    output_root.mkdir(parents=True, exist_ok=True)
    layout_contract = template_payload["prompt_payload"]["layout"]
    timestamp = datetime.now().astimezone().isoformat(timespec="seconds")
    episode_carrier: dict[str, Any] = {
        "meta": {
            "project_name": args.project,
            "episode_id": args.episode,
            "source_scene_design": design_path.as_posix(),
            "skill_id": "aigc/4-Design/场景/3-面板",
            "generated_at": timestamp,
        },
        "layout_contract": {
            "aspect_ratio": layout_contract["aspect_ratio"],
            "panel_count": layout_contract["panel_count"],
            "grid": layout_contract["grid"],
        },
        "panels": [],
    }
    output_files: list[str] = []

    for panel in selected_entries:
        layout_path = output_root / f"{panel.scene_key}-layout.json"
        ensure_writable(layout_path, args.force)
        reference_images = collect_adjacent_images(panel.design_markdown_path)
        layout_payload = {
            "meta": {
                "project_name": args.project,
                "episode_id": args.episode,
                "scene_key": panel.scene_key,
                "scene_name": panel.scene_name,
                "source_scene_design": design_path.as_posix(),
                "source_design_markdown": panel.design_markdown_path,
            },
            "subject": {
                "scene_key": panel.scene_key,
                "scene_name": panel.scene_name,
                "scene_variant": panel.scene_variant,
                "identity_badge": f"{panel.scene_key} + {panel.scene_name}",
                "source_scene_ids": panel.source_scene_ids,
            },
            "layout_contract": {
                "aspect_ratio": layout_contract["aspect_ratio"],
                "panel_count": layout_contract["panel_count"],
                "grid": layout_contract["grid"],
            },
            "prompt": panel.panel_prompt,
            "negative_prompt": panel.negative_prompt,
            "panel_handoff": panel.panel_handoff,
            "image_generation": {
                "target_skill_id": "nano-banana-general",
                "smart_mode_default": "continuous-batch",
                "prompt_field": "prompt",
                "prompt_text": panel.panel_prompt,
                "prompt_reference_sections": [
                    "prompt",
                    "negative_prompt",
                    "panel_handoff",
                ],
                "reference_images": reference_images,
                "explicit_references": args.reference,
                "continuity_source_roots": list(
                    dict.fromkeys(
                        [
                            design_path.parent.as_posix(),
                            *( [str(Path(panel.design_markdown_path).parent)] if panel.design_markdown_path else [] ),
                        ]
                    )
                ),
                "output_filename": f"{panel.scene_key}-ScenePanel.png",
                "request_id": f"{panel.scene_key}-scene-panel",
            },
            "output_hint": {
                "downstream_stage": "5-Image",
                "suggested_filename": f"{panel.scene_key}-ScenePanel.png",
            },
        }
        if not args.dry_run:
            dump_json(layout_path, layout_payload)
        output_files.append(layout_path.as_posix())
        episode_carrier["panels"].append(
            {
                "scene_key": panel.scene_key,
                "scene_name": panel.scene_name,
                "scene_variant": panel.scene_variant,
                "identity_badge": f"{panel.scene_key} + {panel.scene_name}",
                "source_scene_ids": panel.source_scene_ids,
                "panel_prompt": panel.panel_prompt,
                "negative_prompt": panel.negative_prompt,
                "panel_handoff": panel.panel_handoff,
                "layout_path": layout_path.as_posix(),
                "design_markdown_path": panel.design_markdown_path,
            }
        )

    episode_path = output_root / "场景面板.json"
    manifest_path = output_root / "_manifest.json"
    ensure_writable(episode_path, args.force)
    ensure_writable(manifest_path, args.force)
    manifest_payload = {
        "episode_id": args.episode,
        "selected_scene_keys": [panel.scene_key for panel in selected_entries],
        "source_inputs": [design_path.as_posix(), TEMPLATE_PATH.as_posix()],
        "output_files": [episode_path.as_posix(), manifest_path.as_posix(), *output_files],
        "review_status": "pass",
        "handoff_targets": [
            "5-Image",
            "nano-banana-general",
        ],
    }
    if args.auto_generate:
        manifest_payload["image_generation"] = {
            "enabled": True,
            "smart_mode_requested": args.smart_mode,
            "status": "pending" if not args.dry_run else "skipped-dry-run",
        }

    if args.dry_run:
        for path in [episode_path, manifest_path, *map(Path, output_files)]:
            print(path.as_posix())
        return 0

    dump_json(episode_path, episode_carrier)
    auto_generate_failed = False
    if args.auto_generate:
        try:
            bridge_module = _load_panel_auto_generate_module()
            auto_generate_result = bridge_module.run_panel_auto_generate(
                [Path(path) for path in output_files],
                manifest_path=manifest_path,
                smart_mode=args.smart_mode,
                explicit_references=args.reference,
                max_concurrent=args.max_concurrent,
                print_payload=args.print_payload,
                save_images=not args.no_save_images,
                no_report=args.no_report,
                pipeline_context="panel-stage",
            )
            manifest_payload["image_generation"] = {
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
            manifest_payload["image_generation"] = {
                "enabled": True,
                "smart_mode_requested": args.smart_mode,
                "success": False,
                "error": str(exc),
            }
            auto_generate_failed = True
    dump_json(manifest_path, manifest_payload)
    return 1 if auto_generate_failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
