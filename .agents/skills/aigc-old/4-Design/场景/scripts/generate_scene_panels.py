#!/usr/bin/env python3
from __future__ import annotations

import argparse
import importlib.util
import json
import re
import sys
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Any, Iterable


SCRIPT_DIR = Path(__file__).resolve().parent
SKILL_DIR = SCRIPT_DIR.parent
TEMPLATE_PATH = SKILL_DIR / "templates" / "场景面板-提示词.json"
IMAGE_EXTENSIONS = {".png", ".jpg", ".jpeg", ".webp"}
PROMPT_KEYS = (
    "full_generation_prompt",
    "final_prompt",
    "final_scene_prompt",
    "prompt整合",
    "prompt_integration",
    "design_prompt",
    "prompt",
)
LEGACY_SCRIPT_AUTHORSHIP_ERROR = (
    "根据 AGENTS.md 的 `内容创作型任务的 LLM 主创规则`，面板 layout 与面板 prompt 决策不得再由脚本直接主创。"
    "本脚本仅保留给受控兼容迁移/投影；如确需临时运行旧式脚本主创，请显式传入 "
    "`--allow-legacy-script-authorship`。"
)


@dataclass
class SceneTask:
    scene_id: str
    scene_name: str
    prompt: str
    source_path: str
    source_prompt_field: str
    continuity_roots: list[str]
    reference_images: list[str]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Generate scene panel layout JSON and optionally call built-in imagegen.")
    parser.add_argument("--project", help="项目名；默认批量模式必填")
    parser.add_argument("--episode", help="集数，如 第1集；默认批量模式必填")
    parser.add_argument("--scene-id", help="仅生成指定 scene_id / scene_key")
    parser.add_argument("--design-file", help="显式指定 scene_design.json")
    parser.add_argument("--prompt-file", help="指定 Markdown/TXT/JSON 文件或目录；默认 direct-request")
    parser.add_argument("--prompt-text", help="自然语言 prompt；默认 direct-request")
    parser.add_argument("--scene-name", help="prompt-text 模式下的场景名")
    parser.add_argument("--output-root", help="显式输出目录")
    parser.add_argument("--layout-only", action="store_true", help="只写 layout JSON，不自动生图")
    parser.add_argument("--json-only", action="store_true", help="兼容别名：只写 layout JSON，不自动生图")
    parser.add_argument("--smart-mode", choices=("auto", "continuous-batch", "single-doc-t2i", "natural-language-t2i", "off"), default="auto")
    parser.add_argument("--reference", action="append", default=[], help="显式参考图，可重复传入")
    parser.add_argument("--max-concurrent", type=int, default=100)
    parser.add_argument("--foreground", action="store_true", help="前台等待 内置 imagegen 完成；默认内置 imagegen 请求准备")
    parser.add_argument(
        "--dry-run",
        "--generation-dry-run",
        dest="dry_run",
        action="store_true",
        help="写 JSON 与 request sidecar，但 nano 只 dry-run",
    )
    parser.add_argument("--print-payload", action="store_true", help="打印 imagegen request")
    parser.add_argument("--no-report", action="store_true", help="调用 nano 时跳过 report")
    parser.add_argument("--force", action="store_true", help="覆盖已存在 layout/manifest")
    parser.add_argument(
        "--allow-legacy-script-authorship",
        action="store_true",
        help="受控兼容模式：允许旧式脚本直接生成场景面板 layout 与 prompt。",
    )
    return parser.parse_args()


def _repo_root() -> Path:
    current = Path(__file__).resolve()
    for parent in current.parents:
        if (parent / ".codex").exists():
            return parent
    return Path.cwd()


def read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, payload: Any, *, force: bool = True) -> None:
    if path.exists() and not force:
        raise FileExistsError(f"输出已存在，使用 --force 覆盖: {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def safe_slug(text: str, fallback: str = "scene") -> str:
    text = re.sub(r"\s+", "-", str(text or "").strip())
    text = re.sub(r"[^\w\u4e00-\u9fff.-]+", "-", text)
    text = text.strip("-_.")
    return text[:72] or fallback


def dedupe(values: Iterable[str]) -> list[str]:
    result: list[str] = []
    seen: set[str] = set()
    for value in values:
        text = str(value or "").strip()
        if not text or text in seen:
            continue
        seen.add(text)
        result.append(text)
    return result


def extract_prompt_integration(text: str) -> tuple[str, str]:
    patterns = [
        r"\*\*prompt整合\*\*\s*(?P<body>.+)$",
        r"^#+\s*prompt整合\s*(?P<body>.+)$",
        r"^prompt整合[:：]\s*(?P<body>.+)$",
    ]
    for pattern in patterns:
        match = re.search(pattern, text, flags=re.IGNORECASE | re.MULTILINE | re.DOTALL)
        if match:
            body = match.group("body").strip()
            return body, "markdown.prompt整合"
    stripped = text.strip()
    return stripped, "markdown.full_text_fallback"


def first_heading(text: str) -> str:
    match = re.search(r"^#\s+(.+)$", text, flags=re.MULTILINE)
    return match.group(1).strip() if match else ""


def prompt_from_json_entry(entry: dict[str, Any]) -> tuple[str, str]:
    for key in PROMPT_KEYS:
        value = entry.get(key)
        if isinstance(value, str) and value.strip():
            return value.strip(), key

    structured = entry.get("structured_fields")
    if isinstance(structured, dict):
        for key in PROMPT_KEYS:
            value = structured.get(key)
            if isinstance(value, str) and value.strip():
                return value.strip(), f"structured_fields.{key}"

    raise ValueError("JSON entry 缺少可用 prompt 字段")


def scene_identity(entry: dict[str, Any], fallback_stem: str) -> tuple[str, str]:
    scene_id = (
        str(entry.get("scene_id") or entry.get("scene_key") or entry.get("id") or "").strip()
    )
    scene_name = (
        str(entry.get("scene_name") or entry.get("name") or entry.get("title") or "").strip()
    )
    if not scene_id:
        scene_id = safe_slug(fallback_stem, "SCENE")
    if not scene_name:
        scene_name = fallback_stem
    return scene_id, scene_name


def image_list_from_entry(entry: dict[str, Any]) -> list[str]:
    raw_values: list[Any] = []
    for key in ("reference_images", "images", "image_refs", "refs"):
        value = entry.get(key)
        if isinstance(value, list):
            raw_values.extend(value)
    result: list[str] = []
    for item in raw_values:
        if isinstance(item, dict):
            result.append(str(item.get("url") or item.get("path") or ""))
        else:
            result.append(str(item))
    return dedupe(result)


def load_json_tasks(path: Path, *, selected_scene_id: str | None, project: str | None) -> list[SceneTask]:
    payload = read_json(path)
    if isinstance(payload, dict) and isinstance(payload.get("tasks"), list):
        entries = payload["tasks"]
    elif isinstance(payload, dict) and isinstance(payload.get("scenes"), list):
        entries = payload["scenes"]
    elif isinstance(payload, dict) and isinstance(payload.get("scene_designs"), list):
        entries = payload["scene_designs"]
    elif isinstance(payload, list):
        entries = payload
    elif isinstance(payload, dict):
        entries = [payload]
    else:
        raise ValueError(f"无法识别 JSON 结构: {path}")

    tasks: list[SceneTask] = []
    for index, entry in enumerate(entries, start=1):
        if not isinstance(entry, dict):
            continue
        scene_id, scene_name = scene_identity(entry, f"{path.stem}-{index:03d}")
        if selected_scene_id and selected_scene_id not in {scene_id, scene_name}:
            continue
        prompt, prompt_field = prompt_from_json_entry(entry)
        markdown_path = str(entry.get("design_markdown_path") or entry.get("markdown_path") or "").strip()
        continuity_roots = [path.parent.as_posix()]
        if markdown_path:
            md_path = Path(markdown_path)
            if not md_path.is_absolute():
                md_path = (_repo_root() / md_path).resolve()
            continuity_roots.append(md_path.parent.as_posix())
        tasks.append(
            SceneTask(
                scene_id=scene_id,
                scene_name=scene_name,
                prompt=prompt,
                source_path=path.as_posix(),
                source_prompt_field=prompt_field,
                continuity_roots=dedupe(continuity_roots),
                reference_images=image_list_from_entry(entry),
            )
        )
    if not tasks:
        raise ValueError("没有命中任何场景任务")
    return tasks


def load_markdown_task(path: Path, *, project: str | None) -> SceneTask:
    text = path.read_text(encoding="utf-8")
    prompt, prompt_field = extract_prompt_integration(text)
    if not prompt:
        raise ValueError(f"Markdown 中没有可用 prompt: {path}")
    heading = first_heading(text)
    fallback = heading or path.stem
    scene_id = safe_slug(path.stem, "SCENE")
    scene_name = fallback
    return SceneTask(
        scene_id=scene_id,
        scene_name=scene_name,
        prompt=prompt,
        source_path=path.as_posix(),
        source_prompt_field=prompt_field,
        continuity_roots=[path.parent.as_posix()],
        reference_images=[],
    )


def load_prompt_file_tasks(path: Path, *, selected_scene_id: str | None, project: str | None) -> list[SceneTask]:
    if path.is_dir():
        tasks: list[SceneTask] = []
        for child in sorted(path.iterdir()):
            if child.suffix.lower() in {".md", ".txt"} and child.is_file():
                task = load_markdown_task(child, project=project)
                if not selected_scene_id or selected_scene_id in {task.scene_id, task.scene_name}:
                    tasks.append(task)
            elif child.suffix.lower() == ".json" and child.is_file():
                tasks.extend(load_json_tasks(child, selected_scene_id=selected_scene_id, project=project))
        if not tasks:
            raise ValueError(f"目录下没有可用 prompt 文件: {path}")
        return tasks

    if path.suffix.lower() == ".json":
        return load_json_tasks(path, selected_scene_id=selected_scene_id, project=project)
    if path.suffix.lower() in {".md", ".txt"}:
        task = load_markdown_task(path, project=project)
        if selected_scene_id and selected_scene_id not in {task.scene_id, task.scene_name}:
            raise ValueError("指定 scene-id 未命中 prompt-file")
        return [task]
    raise ValueError(f"不支持的 prompt-file 类型: {path}")


def default_design_path(project: str, episode: str) -> Path:
    return Path("projects") / "aigc" / project / "4-Design" / "scene_design.json"


def default_output_root(project: str, episode: str) -> Path:
    return Path("projects") / "aigc" / project / "4-Design"


def infer_project_name(args: argparse.Namespace) -> str:
    if args.project:
        return args.project
    return "测试"


def build_prompt(template_payload: dict[str, Any], task: SceneTask) -> str:
    payload = template_payload["prompt_payload"]
    layout = payload["layout"]
    contract = payload["panel_sheet_contract"].get("constraints", [])
    generation = payload["layout_generation_prompt"]
    identity_badge = f"{task.scene_id}+{task.scene_name}"
    parts = [
        f"Identity badge: {identity_badge}",
        "【设计主体 prompt】",
        task.prompt,
        "【Scene panel layout contract】",
        generation.get("canvas_setup", ""),
        "\n".join(f"- {item}" for item in contract),
        "\n".join(f"- {item}" for item in generation.get("critical_requirements", [])),
        f"Layout: {layout['aspect_ratio']}, {layout['grid']}, {layout['panel_count']} panels.",
        "Live-action photoreal production-design board, coherent lighting, material continuity, no 2D illustration, no anime, no storyboard sketch.",
    ]
    return "\n\n".join(part.strip() for part in parts if part and part.strip())


def load_template() -> dict[str, Any]:
    payload = read_json(TEMPLATE_PATH)
    prompt_payload = payload.get("prompt_payload")
    if not isinstance(prompt_payload, dict):
        raise ValueError("模板缺少 prompt_payload")
    layout = prompt_payload.get("layout")
    if not isinstance(layout, dict):
        raise ValueError("模板缺少 prompt_payload.layout")
    if str(layout.get("aspect_ratio")) != "16:9" or str(layout.get("grid")) != "3x3":
        raise ValueError("模板必须固定为 16:9 + 3x3")
    if int(layout.get("panel_count", 0)) != 9:
        raise ValueError("模板 panel_count 必须为 9")
    return payload


def _load_panel_auto_generate_module() -> Any:
    module_path = SCRIPT_DIR / "panel_auto_generate.py"
    spec = importlib.util.spec_from_file_location("panel_auto_generate_bridge", module_path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"无法加载自动生图桥接脚本: {module_path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def source_context(args: argparse.Namespace) -> str:
    if args.prompt_file or args.prompt_text:
        return "direct-request"
    return "panel-stage"


def bridge_smart_mode(args: argparse.Namespace) -> str:
    if args.smart_mode != "auto":
        return args.smart_mode
    if args.prompt_text:
        return "natural-language-t2i"
    return args.smart_mode


def resolve_tasks(args: argparse.Namespace) -> tuple[list[SceneTask], str]:
    project = infer_project_name(args)
    if args.prompt_text:
        scene_id = safe_slug(args.scene_name or "single-scene", "SCENE")
        scene_name = args.scene_name or "single-scene"
        return [
            SceneTask(
                scene_id=scene_id,
                scene_name=scene_name,
                prompt=args.prompt_text.strip(),
                source_path="prompt-text",
                source_prompt_field="prompt_text",
                continuity_roots=[],
                reference_images=[],
            )
        ], project

    if args.prompt_file:
        return load_prompt_file_tasks(
            Path(args.prompt_file),
            selected_scene_id=args.scene_id,
            project=project,
        ), project

    if not args.project or not args.episode:
        raise ValueError("默认批量模式必须传 --project 与 --episode；或改用 --prompt-file / --prompt-text")
    design_path = Path(args.design_file) if args.design_file else default_design_path(args.project, args.episode)
    return load_json_tasks(design_path, selected_scene_id=args.scene_id, project=args.project), args.project


def main() -> int:
    args = parse_args()
    if not args.allow_legacy_script_authorship:
        print(f"[ERROR] {LEGACY_SCRIPT_AUTHORSHIP_ERROR}", file=sys.stderr)
        return 2
    tasks, project_name = resolve_tasks(args)
    template_payload = load_template()
    episode = args.episode or "direct-request"
    output_root = Path(args.output_root) if args.output_root else default_output_root(project_name, episode)
    output_root.mkdir(parents=True, exist_ok=True)

    layout_paths: list[Path] = []
    panels: list[dict[str, Any]] = []
    timestamp = datetime.now().astimezone().isoformat(timespec="seconds")
    layout_contract = template_payload["prompt_payload"]["layout"]

    for task in tasks:
        filename_prefix = f"{safe_slug(task.scene_id)}-{safe_slug(task.scene_name)}_ScenePanel"
        layout_path = output_root / f"{filename_prefix}-layout.json"
        prompt = build_prompt(template_payload, task)
        generated_output_dir = output_root / "generated" / filename_prefix
        layout_payload = {
            "meta": {
                "project_name": project_name,
                "episode_id": episode,
                "source_context": source_context(args),
                "source_path": task.source_path,
                "source_prompt_field": task.source_prompt_field,
                "skill_id": "aigc-design-scene",
                "generated_at": timestamp,
            },
            "subject": {
                "scene_id": task.scene_id,
                "scene_name": task.scene_name,
                "identity_badge": f"{task.scene_id}+{task.scene_name}",
            },
            "prompt": prompt,
            "images": [{"url": item} for item in dedupe([*task.reference_images, *args.reference])],
            "project_name": project_name,
            "task_kind": "project",
            "aspect_ratio": "16:9",
            "image_size": "4K",
            "request_id": f"{safe_slug(task.scene_id)}-scene-panel",
            "output_dir": generated_output_dir.as_posix(),
            "output_filename": f"{filename_prefix}.png",
            "filename_prefix": filename_prefix,
            "layout_contract": {
                "aspect_ratio": layout_contract["aspect_ratio"],
                "resolution": layout_contract["resolution"],
                "panel_count": layout_contract["panel_count"],
                "grid": layout_contract["grid"],
            },
            "image_generation": {
                "target_skill_id": "imagegen",
                "smart_mode_default": "continuous-batch" if source_context(args) == "panel-stage" else bridge_smart_mode(args),
                "prompt_field": "prompt",
                "prompt_text": prompt,
                "prompt_reference_sections": [
                    "prompt",
                    "templates/场景面板-提示词.json.prompt_payload",
                    task.source_prompt_field,
                ],
                "reference_images": task.reference_images,
                "explicit_references": args.reference,
                "continuity_source_roots": task.continuity_roots,
                "output_dir": generated_output_dir.as_posix(),
                "output_filename": f"{filename_prefix}.png",
                "request_id": f"{safe_slug(task.scene_id)}-scene-panel",
            },
        }
        write_json(layout_path, layout_payload, force=args.force)
        layout_paths.append(layout_path)
        panels.append(
            {
                "scene_id": task.scene_id,
                "scene_name": task.scene_name,
                "identity_badge": f"{task.scene_id}+{task.scene_name}",
                "layout_path": layout_path.as_posix(),
                "source_path": task.source_path,
                "source_prompt_field": task.source_prompt_field,
            }
        )

    episode_path = output_root / "场景面板.json"
    manifest_path = output_root / "_manifest.json"
    write_json(
        episode_path,
        {
            "meta": {
                "project_name": project_name,
                "episode_id": episode,
                "source_context": source_context(args),
                "generated_at": timestamp,
            },
            "layout_contract": {
                "aspect_ratio": layout_contract["aspect_ratio"],
                "resolution": layout_contract["resolution"],
                "panel_count": layout_contract["panel_count"],
                "grid": layout_contract["grid"],
            },
            "panels": panels,
        },
        force=args.force,
    )

    skip_generation = args.layout_only or args.json_only or args.smart_mode == "off"
    manifest_payload: dict[str, Any] = {
        "project_name": project_name,
        "episode_id": episode,
        "source_context": source_context(args),
        "selected_scene_ids": [task.scene_id for task in tasks],
        "outputs": {
            "episode_panel": episode_path.as_posix(),
            "layout_files": [path.as_posix() for path in layout_paths],
        },
        "template_path": TEMPLATE_PATH.as_posix(),
        "image_generation": {
            "enabled": not skip_generation,
            "smart_mode_requested": args.smart_mode,
            "status": "skipped-json-only" if skip_generation else "pending",
        },
    }

    generation_failed = False
    if not skip_generation:
        bridge_module = _load_panel_auto_generate_module()
        result = bridge_module.run_panel_auto_generate(
            layout_paths,
            manifest_path=manifest_path,
            smart_mode=bridge_smart_mode(args),
            explicit_references=args.reference,
            dry_run=args.dry_run,
            print_payload=args.print_payload,
            max_concurrent=args.max_concurrent,
            no_report=args.no_report,
            background=not args.foreground,
            pipeline_context=source_context(args),
        )
        generation_failed = not bool(result.get("success"))
        manifest_payload["image_generation"] = {
            "enabled": True,
            "smart_mode_requested": args.smart_mode,
            "smart_mode_resolved": result.get("smart_mode_resolved", ""),
            "success": bool(result.get("success")),
            "task_count": result.get("task_count", 0),
            "success_count": result.get("success_count", 0),
            "failed_count": result.get("failed_count", 0),
            "status": result.get("status", "completed" if result.get("success") else "failed"),
            "execution_mode": result.get("execution_mode"),
            "provider_skill": result.get("provider_skill"),
            "provider_mode": result.get("provider_mode"),
            "default_model": result.get("default_model"),
            "generated_source_path": result.get("generated_source_path"),
            "request_batch_path": result.get("request_batch_path"),
            "bridge_report_path": result.get("bridge_report_path"),
            "dry_run": bool(args.dry_run),
        }
    elif args.smart_mode != "off":
        bridge_module = _load_panel_auto_generate_module()
        result = bridge_module.run_panel_auto_generate(
            layout_paths,
            manifest_path=manifest_path,
            smart_mode=bridge_smart_mode(args),
            explicit_references=args.reference,
            max_concurrent=args.max_concurrent,
            no_report=args.no_report,
            generate=False,
            pipeline_context=source_context(args),
        )
        manifest_payload["image_generation"] = {
            "enabled": False,
            "smart_mode_requested": args.smart_mode,
            "smart_mode_resolved": result.get("smart_mode_resolved", ""),
            "status": "request-sidecar-only",
            "request_batch_path": result.get("request_batch_path"),
            "bridge_report_path": result.get("bridge_report_path"),
        }

    write_json(manifest_path, manifest_payload, force=True)
    print(json.dumps(manifest_payload, ensure_ascii=False, indent=2))
    return 1 if generation_failed else 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:
        print(f"FAIL-SCENE-PANEL: {exc}", file=sys.stderr)
        raise SystemExit(1)
