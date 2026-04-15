#!/usr/bin/env python3
"""Generate prop panel layout JSONs and optionally invoke nano-banana/general."""

from __future__ import annotations

import argparse
import importlib.util
import json
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterable


DEFAULT_ASPECT_RATIO = "16:9"
DEFAULT_IMAGE_SIZE = "4K"
DEFAULT_CANVAS_SIZE = "4096x2304"
PROMPT_SECTION_RE = re.compile(
    r"^\*\*(?P<label>full_generation_prompt|prompt整合)\*\*\s*\n(?P<body>.+?)(?=^\*\*|\Z)",
    re.MULTILINE | re.DOTALL | re.IGNORECASE,
)
PROP_ID_RE = re.compile(r"(?P<id>(?:PRP|prop)[-_]?\d+)", re.IGNORECASE)


MORPHOLOGY_GUARDRAILS: dict[str, tuple[str, ...]] = {
    "cup_handleless_gate": (
        "Use period-authentic handleless cup morphology; avoid mug-style side handles and modern coffee-cup ergonomics.",
        "Preserve ancient tea vessel proportions and restrained glaze behavior; forbid modern industrial tableware cues.",
    ),
    "fine_chain_gate": (
        "Keep chain silhouette slender and court-grade; reject chunky modern Cuban-link massing.",
        "Use period-consistent clasp logic and subtle metal wear; avoid modern mirror-polish showroom look.",
    ),
    "blueprint_antique_gate": (
        "Render as pre-modern hand-drawn paper/scroll drafting with brush-and-ink annotation rhythm.",
        "Forbid modern CAD blueprint language, cyan engineering sheets, and printer-clean industrial linework.",
    ),
    "ancient_bell_gate": (
        "Use period bronze warning-bell morphology with plausible suspension and striker structure.",
        "Reject modern electronic bell housings, machine screws, plastics, and contemporary safety hardware.",
    ),
}


@dataclass
class PropPanelTask:
    prop_id: str
    prop_name: str
    prompt: str
    source_file: Path | None
    prompt_source_type: str
    continuity_root: Path | None


class PropPanelError(RuntimeError):
    pass


def _repo_root() -> Path:
    current = Path(__file__).resolve()
    for parent in current.parents:
        if (parent / ".codex").exists():
            return parent
    return Path.cwd()


def _skill_dir() -> Path:
    return Path(__file__).resolve().parents[1]


def _read_json(path: Path) -> dict[str, Any]:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:
        raise PropPanelError(f"JSON 读取失败: {path} ({exc})") from exc


def _write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def _safe_name(value: str) -> str:
    text = re.sub(r'[\\/:*?"<>|]+', "-", str(value or "").strip())
    return text or "unnamed-prop"


def _repo_relative(path: Path, repo_root: Path) -> str:
    try:
        return path.resolve().relative_to(repo_root.resolve()).as_posix()
    except ValueError:
        return path.as_posix()


def _dedupe_tasks(tasks: Iterable[PropPanelTask]) -> list[PropPanelTask]:
    result: list[PropPanelTask] = []
    seen: set[tuple[str, str, str]] = set()
    for task in tasks:
        key = (task.prop_id, task.prop_name, task.prompt)
        if key in seen:
            continue
        seen.add(key)
        result.append(task)
    return result


def _load_template() -> dict[str, Any]:
    template_path = _skill_dir() / "templates" / "道具面板-提示词.json"
    payload = _read_json(template_path).get("prompt_payload")
    if not isinstance(payload, dict):
        raise PropPanelError(f"模板缺少 prompt_payload: {template_path}")
    required = ("layout", "layout_generation_prompt", "layout_modules", "_prompt_text_assembly_guide")
    missing = [key for key in required if key not in payload]
    if missing:
        raise PropPanelError(f"模板缺少字段: {', '.join(missing)}")
    return payload


def _extract_prompt_from_markdown(text: str, path: Path) -> str:
    matches = list(PROMPT_SECTION_RE.finditer(text))
    prompt = ""
    for preferred in ("full_generation_prompt", "prompt整合"):
        for match in matches:
            if match.group("label").lower() == preferred.lower():
                prompt = match.group("body").strip()
                break
        if prompt:
            break
    if not prompt:
        raise PropPanelError(f"Markdown 缺少 **full_generation_prompt** 或 **prompt整合** 区块: {path}")
    if not prompt:
        raise PropPanelError(f"Markdown prompt整合 为空: {path}")
    return prompt


def _infer_id_name_from_path(path: Path) -> tuple[str, str]:
    stem = path.stem
    match = PROP_ID_RE.search(stem)
    if match:
        prop_id = match.group("id")
        prop_name = stem[match.end() :].strip("-_ ") or stem
        return prop_id, prop_name
    return "prop-001", stem or "未命名道具"


def _markdown_task(path: Path, continuity_root: Path | None) -> PropPanelTask:
    prop_id, prop_name = _infer_id_name_from_path(path)
    prompt = _extract_prompt_from_markdown(path.read_text(encoding="utf-8"), path)
    return PropPanelTask(
        prop_id=prop_id,
        prop_name=prop_name,
        prompt=prompt,
        source_file=path,
        prompt_source_type="markdown.prompt整合",
        continuity_root=continuity_root,
    )


def _tasks_from_prompt_json(path: Path, continuity_root: Path | None) -> list[PropPanelTask]:
    payload = _read_json(path)
    props = payload.get("props")
    if not isinstance(props, list):
        props = payload.get("items") if isinstance(payload.get("items"), list) else []
    tasks: list[PropPanelTask] = []
    for index, item in enumerate(props, start=1):
        if not isinstance(item, dict):
            continue
        prompt = str(
            item.get("full_generation_prompt")
            or item.get("prompt_en")
            or item.get("prompt_cn")
            or item.get("prompt")
            or item.get("prompt_text")
            or ""
        ).strip()
        if not prompt:
            continue
        prop_id = str(item.get("prop_id") or f"prop-{index:03d}").strip()
        prop_name = str(item.get("canonical_name") or item.get("prop_name") or item.get("name") or prop_id).strip()
        tasks.append(PropPanelTask(prop_id, prop_name, prompt, path, "json.prompt", continuity_root))
    return tasks


def _tasks_from_design_json(path: Path, continuity_root: Path | None) -> list[PropPanelTask]:
    payload = _read_json(path)
    props = payload.get("props")
    if not isinstance(props, list):
        props = payload.get("design_items") if isinstance(payload.get("design_items"), list) else []
    tasks: list[PropPanelTask] = []
    for index, item in enumerate(props, start=1):
        if not isinstance(item, dict):
            continue
        prompt = str(item.get("prompt_anchor") or item.get("prompt") or item.get("prompt_text") or "").strip()
        if not prompt:
            continue
        prop_id = str(item.get("prop_id") or f"prop-{index:03d}").strip()
        prop_name = str(item.get("canonical_name") or item.get("prop_name") or item.get("name") or prop_id).strip()
        tasks.append(PropPanelTask(prop_id, prop_name, prompt, path, "json.design_fallback", continuity_root))
    return tasks


def _tasks_from_text_file(path: Path, continuity_root: Path | None) -> list[PropPanelTask]:
    text = path.read_text(encoding="utf-8").strip()
    if not text:
        raise PropPanelError(f"文本 prompt 为空: {path}")
    prop_id, prop_name = _infer_id_name_from_path(path)
    return [PropPanelTask(prop_id, prop_name, text, path, "text.prompt", continuity_root)]


def _tasks_from_path(path: Path, *, batch_context: bool) -> list[PropPanelTask]:
    if not path.exists():
        raise PropPanelError(f"输入路径不存在: {path}")
    continuity_root = path if path.is_dir() else path.parent
    if not batch_context:
        continuity_root = None

    if path.is_dir():
        tasks: list[PropPanelTask] = []
        markdown_files = sorted(item for item in path.glob("*.md") if not item.name.startswith("_"))
        for markdown_file in markdown_files:
            tasks.append(_markdown_task(markdown_file, continuity_root))
        if tasks:
            return _dedupe_tasks(tasks)
        prompt_json = path / "prop_design_prompt.json"
        if prompt_json.exists():
            tasks.extend(_tasks_from_prompt_json(prompt_json, continuity_root))
        design_json = path / "道具设计.json"
        if design_json.exists():
            tasks.extend(_tasks_from_design_json(design_json, continuity_root))
        if tasks:
            return _dedupe_tasks(tasks)
        raise PropPanelError(f"目录中未找到可消费的道具设计 prompt: {path}")

    suffix = path.suffix.lower()
    if suffix == ".md":
        return [_markdown_task(path, continuity_root)]
    if suffix == ".json":
        tasks = _tasks_from_prompt_json(path, continuity_root)
        if not tasks:
            tasks = _tasks_from_design_json(path, continuity_root)
        if tasks:
            return _dedupe_tasks(tasks)
        raise PropPanelError(f"JSON 中未找到可消费的 prompt: {path}")
    if suffix in {".txt", ".prompt"}:
        return _tasks_from_text_file(path, continuity_root)
    raise PropPanelError(f"不支持的输入文件类型: {path}")


def _load_panel_auto_generate_module() -> Any:
    repo_root = _repo_root()
    module_path = repo_root / ".agents" / "skills" / "aigc" / "4-Design" / "3-面板" / "_shared" / "panel_auto_generate.py"
    spec = importlib.util.spec_from_file_location("panel_auto_generate_bridge", module_path)
    if spec is None or spec.loader is None:
        raise PropPanelError(f"无法加载自动生图桥接脚本: {module_path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _morphology_guardrails(prop_name: str, prompt: str) -> list[str]:
    text = f"{prop_name} {prompt}".lower()
    guardrails: list[str] = []
    if any(token in text for token in ("tea cup", "drinking cup", "茶杯", "杯子")):
        guardrails.extend(MORPHOLOGY_GUARDRAILS["cup_handleless_gate"])
    if any(token in text for token in ("fine gold chain", "细金链")):
        guardrails.extend(MORPHOLOGY_GUARDRAILS["fine_chain_gate"])
    if any(token in text for token in ("architecture blueprint", "图纸", "蓝图")):
        guardrails.extend(MORPHOLOGY_GUARDRAILS["blueprint_antique_gate"])
    if any(token in text for token in ("warning bell", "铜铃")):
        guardrails.extend(MORPHOLOGY_GUARDRAILS["ancient_bell_gate"])
    return guardrails


def _join_non_empty(parts: Iterable[str]) -> str:
    return "\n\n".join(part.strip() for part in parts if part and part.strip())


def _build_layout_doc(
    *,
    project_name: str,
    episode_id: str,
    task: PropPanelTask,
    template_payload: dict[str, Any],
    layout_path: Path,
    repo_root: Path,
    pipeline_context: str,
    explicit_references: list[str],
) -> dict[str, Any]:
    layout = template_payload.get("layout") or {}
    guide = template_payload.get("_prompt_text_assembly_guide") or {}
    mandatory_rules = [str(item).strip() for item in guide.get("mandatory_rules", []) if str(item).strip()]
    guardrails = _morphology_guardrails(task.prop_name, task.prompt)
    identity_badge = f"{task.prop_id}+{task.prop_name}"
    identity_prompt = f"Identity badge: {identity_badge}. Keep it fixed in the top-left safe area."
    layout_prompt = str(template_payload.get("layout_generation_prompt") or "").strip()
    guardrail_prompt = "Morphology guardrails:\n- " + "\n- ".join(guardrails) if guardrails else ""
    prompt_text = _join_non_empty(
        [
            identity_prompt,
            task.prompt,
            layout_prompt,
            "Mandatory rules:\n- " + "\n- ".join(mandatory_rules) if mandatory_rules else "",
            guardrail_prompt,
        ]
    )
    output_filename = f"{_safe_name(task.prop_id)}-{_safe_name(task.prop_name)}-PropPanel.png"
    continuity_roots = []
    if pipeline_context == "panel-stage" and task.continuity_root is not None:
        continuity_roots.append(_repo_relative(task.continuity_root, repo_root))

    return {
        "meta": {
            "project_name": project_name,
            "episode_id": episode_id,
            "skill_id": "aigc-design-prop-panel",
            "source_prompt": _repo_relative(task.source_file, repo_root) if task.source_file else "inline:text",
            "prompt_source_type": task.prompt_source_type,
        },
        "subject": {
            "prop_id": task.prop_id,
            "prop_name": task.prop_name,
            "canonical_name": task.prop_name,
            "identity_badge": identity_badge,
        },
        "layout_contract": {
            "template_type": layout.get("template_type", "PROP_ATMOSPHERIC_DOSSIER"),
            "aspect_ratio": layout.get("aspect_ratio", DEFAULT_ASPECT_RATIO),
            "canvas_size": layout.get("canvas_size", DEFAULT_CANVAS_SIZE),
            "module_contract": template_payload.get("layout_modules", {}),
            "mandatory_rules": mandatory_rules,
            "morphology_guardrails": guardrails,
        },
        "prompt_payload": {
            "layout": layout,
            "layout_generation_prompt": layout_prompt,
            "layout_modules": template_payload.get("layout_modules", {}),
            "prompt_segments": {
                "identity_prompt": identity_prompt,
                "design_prompt": task.prompt,
                "layout_prompt": layout_prompt,
                "morphology_guardrails": guardrails,
            },
            "prompt_text": prompt_text,
        },
        "prompt": prompt_text,
        "images": [{"url": item} for item in explicit_references],
        "project_name": project_name,
        "task_kind": "project",
        "aspect_ratio": DEFAULT_ASPECT_RATIO,
        "image_size": DEFAULT_IMAGE_SIZE,
        "request_id": layout_path.stem,
        "output_dir": layout_path.parent.as_posix(),
        "output_filename": output_filename,
        "filename_prefix": f"{_safe_name(task.prop_id)}-{_safe_name(task.prop_name)}-PropPanel",
        "image_generation": {
            "target_skill_id": "nano-banana-general",
            "smart_mode_default": "continuous-batch" if pipeline_context == "panel-stage" else "single-doc-t2i",
            "pipeline_context": pipeline_context,
            "prompt_field": "prompt",
            "prompt_text": prompt_text,
            "prompt_reference_sections": [
                "prompt",
                "prompt_payload.prompt_segments.design_prompt",
                "prompt_payload.prompt_segments.layout_prompt",
            ],
            "reference_images": [],
            "explicit_references": explicit_references,
            "continuity_source_roots": continuity_roots,
            "output_filename": output_filename,
            "request_id": layout_path.stem,
        },
        "output": {
            "output_filename": output_filename,
            "layout_path": _repo_relative(layout_path, repo_root),
        },
    }


def _episode_dirs(input_root: Path, episode: str | None) -> list[Path]:
    if episode:
        target = input_root / episode
        if not target.exists():
            raise PropPanelError(f"未找到 episode 目录: {target}")
        return [target]
    return sorted(path for path in input_root.iterdir() if path.is_dir())


def _default_output_dir(project_name: str, episode_id: str) -> Path:
    return _repo_root() / "projects" / "aigc" / project_name / "4-Design" / "道具" / "3-面板" / episode_id


def build_panels(
    *,
    project_name: str,
    episode: str | None,
    prompt_file: Path | None,
    text: str | None,
    output_dir: Path | None,
    layout_only: bool,
    dry_run: bool,
    generation_dry_run: bool,
    smart_mode: str,
    explicit_references: list[str],
    max_concurrent: int,
    print_payload: bool,
    save_images: bool,
    no_report: bool,
) -> int:
    repo_root = _repo_root()
    project_root = repo_root / "projects" / "aigc" / project_name
    input_root = project_root / "4-Design" / "道具" / "2-设计"
    template_payload = _load_template()
    built_files = 0

    if text:
        episode_id = episode or "单次"
        target_output_dir = output_dir or _default_output_dir(project_name, episode_id)
        task = PropPanelTask("prop-001", "自然语言道具", text.strip(), None, "inline.text", None)
        built_files += _build_episode(
            project_name=project_name,
            episode_id=episode_id,
            tasks=[task],
            output_dir=target_output_dir,
            template_payload=template_payload,
            repo_root=repo_root,
            pipeline_context="direct-request",
            layout_only=layout_only,
            dry_run=dry_run,
            generation_dry_run=generation_dry_run,
            smart_mode=smart_mode,
            explicit_references=explicit_references,
            max_concurrent=max_concurrent,
            print_payload=print_payload,
            save_images=save_images,
            no_report=no_report,
        )
        return built_files

    if prompt_file is not None:
        source = prompt_file
        if not source.is_absolute():
            source = (repo_root / source).resolve()
        episode_id = episode or (source.name if source.is_dir() else source.parent.name)
        target_output_dir = output_dir or _default_output_dir(project_name, episode_id)
        tasks = _tasks_from_path(source, batch_context=False)
        built_files += _build_episode(
            project_name=project_name,
            episode_id=episode_id,
            tasks=tasks,
            output_dir=target_output_dir,
            template_payload=template_payload,
            repo_root=repo_root,
            pipeline_context="direct-request",
            layout_only=layout_only,
            dry_run=dry_run,
            generation_dry_run=generation_dry_run,
            smart_mode=smart_mode,
            explicit_references=explicit_references,
            max_concurrent=max_concurrent,
            print_payload=print_payload,
            save_images=save_images,
            no_report=no_report,
        )
        return built_files

    if not input_root.exists():
        raise PropPanelError(f"未找到输入根目录: {input_root}")
    for episode_dir in _episode_dirs(input_root, episode):
        episode_id = episode_dir.name
        target_output_dir = output_dir or _default_output_dir(project_name, episode_id)
        tasks = _tasks_from_path(episode_dir, batch_context=True)
        built_files += _build_episode(
            project_name=project_name,
            episode_id=episode_id,
            tasks=tasks,
            output_dir=target_output_dir,
            template_payload=template_payload,
            repo_root=repo_root,
            pipeline_context="panel-stage",
            layout_only=layout_only,
            dry_run=dry_run,
            generation_dry_run=generation_dry_run,
            smart_mode=smart_mode,
            explicit_references=explicit_references,
            max_concurrent=max_concurrent,
            print_payload=print_payload,
            save_images=save_images,
            no_report=no_report,
        )
    return built_files


def _build_episode(
    *,
    project_name: str,
    episode_id: str,
    tasks: list[PropPanelTask],
    output_dir: Path,
    template_payload: dict[str, Any],
    repo_root: Path,
    pipeline_context: str,
    layout_only: bool,
    dry_run: bool,
    generation_dry_run: bool,
    smart_mode: str,
    explicit_references: list[str],
    max_concurrent: int,
    print_payload: bool,
    save_images: bool,
    no_report: bool,
) -> int:
    if not tasks:
        raise PropPanelError(f"{episode_id} 没有可消费的道具 prompt")
    if not dry_run:
        output_dir.mkdir(parents=True, exist_ok=True)

    packet_paths: list[Path] = []
    manifest: dict[str, Any] = {
        "meta": {
            "project_name": project_name,
            "episode_id": episode_id,
            "skill_id": "aigc-design-prop-panel",
            "pipeline_context": pipeline_context,
        },
        "inputs": [
            {
                "source_file": _repo_relative(task.source_file, repo_root) if task.source_file else "inline:text",
                "prompt_source_type": task.prompt_source_type,
                "prop_id": task.prop_id,
                "prop_name": task.prop_name,
            }
            for task in tasks
        ],
        "outputs": [],
        "statistics": {
            "task_count": len(tasks),
            "layout_count": 0 if dry_run else len(tasks),
        },
        "image_generation": {
            "enabled": not layout_only,
            "smart_mode_requested": smart_mode,
            "pipeline_context": pipeline_context,
            "status": "skipped-layout-only" if layout_only else ("skipped-dry-run" if dry_run else "pending"),
        },
    }

    for task in tasks:
        layout_name = f"{_safe_name(task.prop_id)}-{_safe_name(task.prop_name)}-PropPanel-layout.json"
        layout_path = output_dir / layout_name
        layout_doc = _build_layout_doc(
            project_name=project_name,
            episode_id=episode_id,
            task=task,
            template_payload=template_payload,
            layout_path=layout_path,
            repo_root=repo_root,
            pipeline_context=pipeline_context,
            explicit_references=explicit_references,
        )
        packet_paths.append(layout_path)
        manifest["outputs"].append(_repo_relative(layout_path, repo_root))
        if not dry_run:
            _write_json(layout_path, layout_doc)

    if not layout_only and not dry_run:
        try:
            bridge_module = _load_panel_auto_generate_module()
            result = bridge_module.run_panel_auto_generate(
                packet_paths,
                manifest_path=output_dir / "_manifest.json",
                smart_mode=smart_mode,
                explicit_references=explicit_references,
                dry_run=generation_dry_run,
                max_concurrent=max_concurrent,
                print_payload=print_payload,
                save_images=save_images,
                no_report=no_report,
                pipeline_context=pipeline_context,
            )
            manifest["image_generation"].update(
                {
                    "status": "completed" if result.get("success", False) else "failed",
                    "success": bool(result.get("success", False)),
                    "smart_mode_resolved": result.get("smart_mode_resolved"),
                    "task_count": result.get("task_count", 0),
                    "success_count": result.get("success_count", 0),
                    "failed_count": result.get("failed_count", 0),
                    "request_batch_path": result.get("request_batch_path"),
                    "bridge_report_path": result.get("bridge_report_path"),
                }
            )
            if not result.get("success", False):
                raise PropPanelError(f"{episode_id} 自动生图失败，请查看 {result.get('bridge_report_path')}")
        except Exception as exc:
            manifest["image_generation"].update({"status": "failed", "success": False, "error": str(exc)})
            if not dry_run:
                _write_json(output_dir / "_manifest.json", manifest)
            raise

    if not dry_run:
        _write_json(output_dir / "_manifest.json", manifest)
    return len(tasks)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="从 4-Design/道具/2-设计 生成道具面板 layout JSON，并默认自动生图。")
    parser.add_argument("--project", required=True, help="项目名，对应 projects/aigc/<项目名>/")
    parser.add_argument("--episode", help="可选，仅处理指定 episode，例如 第1集")
    parser.add_argument("--prompt-file", help="指定单个设计文件、prompt JSON、文本文件或目录")
    parser.add_argument("--text", help="自然语言 prompt；默认无参照直接生成")
    parser.add_argument("--output-dir", help="覆盖输出目录")
    parser.add_argument("--layout-only", action="store_true", help="只写 layout JSON，不调用生图")
    parser.add_argument("--json-only", action="store_true", help="兼容别名：只写 layout JSON，不调用生图")
    parser.add_argument("--dry-run", action="store_true", help="只校验输入并统计，不写文件也不调用远端")
    parser.add_argument("--generation-dry-run", action="store_true", help="写 layout 与 request sidecar，但 nano-banana 只 dry-run")
    parser.add_argument("--smart-mode", choices=("auto", "continuous-batch", "single-doc-t2i", "off"), default="auto", help="SMART 生图模式")
    parser.add_argument("--reference", action="append", default=[], help="显式追加参考图，可重复传入")
    parser.add_argument("--max-concurrent", type=int, default=100, help="自动生图最大并发")
    parser.add_argument("--print-payload", action="store_true", help="打印 nano-banana payload")
    parser.add_argument("--no-save-images", action="store_true", help="自动生图时不落 PNG")
    parser.add_argument("--no-report", action="store_true", help="跳过 nano-banana report JSON")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    try:
        built_files = build_panels(
            project_name=args.project,
            episode=args.episode,
            prompt_file=Path(args.prompt_file) if args.prompt_file else None,
            text=args.text,
            output_dir=Path(args.output_dir) if args.output_dir else None,
            layout_only=args.layout_only or args.json_only,
            dry_run=args.dry_run,
            generation_dry_run=args.generation_dry_run,
            smart_mode=args.smart_mode,
            explicit_references=args.reference,
            max_concurrent=args.max_concurrent,
            print_payload=args.print_payload,
            save_images=not args.no_save_images,
            no_report=args.no_report,
        )
    except Exception as exc:
        print(f"[prop-panel][ERROR] {exc}", file=sys.stderr)
        return 1
    print(f"[prop-panel] built_files={built_files} dry_run={str(args.dry_run).lower()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
