#!/usr/bin/env python3
from __future__ import annotations

import argparse
import copy
import importlib.util
import json
import re
import sys
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Any


DEFAULT_ASPECT_RATIO = "16:9"
DEFAULT_IMAGE_SIZE = "4K"
PROMPT_SECTION_RE = re.compile(
    r"^\*\*(?P<label>full_generation_prompt|prompt整合)\*\*\s*\n(?P<content>.+?)(?=^\*\*|\Z)",
    re.MULTILINE | re.DOTALL | re.IGNORECASE,
)
ROLE_ID_RE = re.compile(r"((?:ROLE|CHR|CH)[-_]?\d+)", re.IGNORECASE)
INVALID_FILENAME_CHARS = re.compile(r'[<>:"/\\|?*\x00-\x1f]')


class SkillError(RuntimeError):
    pass


@dataclass
class PanelTask:
    role_id: str
    role_name: str
    role_tier: str
    costume_state: str
    design_prompt: str
    source_file: str
    source_kind: str
    explicit_refs: list[str] = field(default_factory=list)


def find_repo_root() -> Path:
    current = Path(__file__).resolve()
    for parent in current.parents:
        if (parent / ".agents").exists():
            return parent
    return Path.cwd()


REPO_ROOT = find_repo_root()
SKILL_DIR = Path(__file__).resolve().parents[1]
TEMPLATE_PATH = SKILL_DIR / "templates" / "角色面板-提示词.json"
PANEL_PARENT_DIR = SKILL_DIR.parent


def repo_rel(path: Path) -> str:
    try:
        return path.resolve().relative_to(REPO_ROOT.resolve()).as_posix()
    except Exception:
        return path.as_posix()


def resolve_path(value: str) -> Path:
    path = Path(value).expanduser()
    if not path.is_absolute():
        path = (REPO_ROOT / path).resolve()
    return path


def read_json(path: Path) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:
        raise SkillError(f"FAIL-RP-JSON: JSON 解析失败: {path} ({exc})") from exc


def write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def safe_name(text: str) -> str:
    cleaned = INVALID_FILENAME_CHARS.sub("-", str(text or "").strip())
    cleaned = re.sub(r"\s+", "", cleaned).strip(".-")
    return cleaned or "未命名角色"


def normalize_episode(value: str | None) -> str:
    text = str(value or "").strip()
    if not text:
        return "第1集"
    if text.startswith("第") and text.endswith("集"):
        return text
    digits = re.findall(r"\d+", text)
    if digits:
        return f"第{int(digits[0])}集"
    return text


def normalize_id(value: str) -> str:
    text = str(value or "").strip()
    if not text:
        return ""
    return text.replace("_", "-").upper()


def split_refs(values: list[str]) -> list[str]:
    refs: list[str] = []
    for value in values:
        for item in str(value or "").split(","):
            clean = item.strip()
            if clean:
                refs.append(clean)
    return dedupe(refs, max_total=14)


def dedupe(values: list[str], max_total: int = 14) -> list[str]:
    out: list[str] = []
    seen: set[str] = set()
    for value in values:
        clean = str(value or "").strip()
        if not clean or clean in seen:
            continue
        seen.add(clean)
        out.append(clean)
        if len(out) >= max_total:
            break
    return out


def extract_prompt_from_markdown(text: str) -> str:
    matches = list(PROMPT_SECTION_RE.finditer(text))
    for preferred in ("full_generation_prompt", "prompt整合"):
        for match in matches:
            if match.group("label").lower() == preferred.lower():
                return match.group("content").strip()
    return ""


def infer_identity_from_path(path: Path) -> tuple[str, str]:
    stem = path.stem
    role_id = ""
    match = ROLE_ID_RE.search(stem)
    if match:
        role_id = normalize_id(match.group(1))
    role_name = stem
    for suffix in ("-角色设计", "-character-design", "_character_design", "-设计卡"):
        if role_name.endswith(suffix):
            role_name = role_name[: -len(suffix)]
    if role_id and role_name.upper().startswith(role_id):
        role_name = role_name[len(role_id) :].lstrip("-_ ")
    return role_id, role_name.strip() or stem


def prompt_from_json_item(item: dict[str, Any]) -> str:
    paths = [
        ("full_generation_prompt",),
        ("final_prompt",),
        ("final_prompt", "text"),
        ("prompt_integration",),
        ("prompt_payload", "prompt_text"),
        ("prompt_payload", "prompt"),
        ("prompt",),
        ("design_prompt",),
        ("prompt_text",),
    ]
    for path in paths:
        current: Any = item
        for key in path:
            if isinstance(current, dict) and key in current:
                current = current[key]
            else:
                current = None
                break
        if isinstance(current, str) and current.strip():
            return current.strip()
    return ""


def task_from_markdown(path: Path, defaults: dict[str, Any] | None = None) -> PanelTask | None:
    defaults = defaults or {}
    text = path.read_text(encoding="utf-8")
    prompt = extract_prompt_from_markdown(text)
    if not prompt:
        return None
    inferred_id, inferred_name = infer_identity_from_path(path)
    role_id = normalize_id(str(defaults.get("role_id") or inferred_id or "ROLE-001"))
    role_name = str(defaults.get("role_name") or defaults.get("canonical_name") or inferred_name).strip()
    return PanelTask(
        role_id=role_id,
        role_name=role_name,
        role_tier=str(defaults.get("role_tier") or "unknown").strip().lower() or "unknown",
        costume_state=str(defaults.get("costume_state") or "baseline").strip() or "baseline",
        design_prompt=prompt,
        source_file=repo_rel(path),
        source_kind="markdown_prompt_integration",
    )


def task_from_json_item(item: dict[str, Any], source_path: Path) -> PanelTask | None:
    prompt = prompt_from_json_item(item)
    markdown_value = item.get("structured_markdown_path") or item.get("markdown_path")
    if not prompt and isinstance(markdown_value, str) and markdown_value.strip():
        markdown_path = resolve_path(markdown_value)
        if markdown_path.exists():
            defaults = {
                "role_id": item.get("role_id") or item.get("character_id") or item.get("id"),
                "role_name": item.get("role_name") or item.get("canonical_name") or item.get("name"),
                "role_tier": item.get("role_tier") or item.get("tier"),
                "costume_state": item.get("costume_state") or item.get("state"),
            }
            return task_from_markdown(markdown_path, defaults)
    if not prompt:
        return None
    role_id = normalize_id(str(item.get("role_id") or item.get("character_id") or item.get("id") or "ROLE-001"))
    role_name = str(item.get("role_name") or item.get("canonical_name") or item.get("name") or role_id).strip()
    return PanelTask(
        role_id=role_id,
        role_name=role_name,
        role_tier=str(item.get("role_tier") or item.get("tier") or "unknown").strip().lower() or "unknown",
        costume_state=str(item.get("costume_state") or item.get("state") or "baseline").strip() or "baseline",
        design_prompt=prompt,
        source_file=repo_rel(source_path),
        source_kind="json_prompt_field",
    )


def tasks_from_json(path: Path) -> list[PanelTask]:
    payload = read_json(path)
    tasks: list[PanelTask] = []
    if isinstance(payload, dict) and isinstance(payload.get("roles"), list):
        for item in payload["roles"]:
            if isinstance(item, dict):
                task = task_from_json_item(item, path)
                if task:
                    tasks.append(task)
    elif isinstance(payload, dict):
        task = task_from_json_item(payload, path)
        if task:
            tasks.append(task)
    return tasks


def tasks_from_manifest(design_dir: Path) -> list[PanelTask]:
    manifest_path = design_dir / "_manifest.json"
    if not manifest_path.exists():
        return []
    manifest = read_json(manifest_path)
    items = manifest.get("design_items") if isinstance(manifest, dict) else None
    if not isinstance(items, list):
        return []
    tasks: list[PanelTask] = []
    for item in items:
        if not isinstance(item, dict):
            continue
        md_value = item.get("markdown_path")
        if not isinstance(md_value, str) or not md_value.strip():
            continue
        md_path = resolve_path(md_value)
        if not md_path.exists():
            continue
        defaults = {
            "role_id": item.get("role_id"),
            "role_name": item.get("canonical_name") or item.get("role_name"),
            "role_tier": item.get("role_tier"),
            "costume_state": item.get("costume_state"),
        }
        task = task_from_markdown(md_path, defaults)
        if task:
            tasks.append(task)
    return tasks


def tasks_from_dir(design_dir: Path) -> list[PanelTask]:
    if not design_dir.exists():
        raise SkillError(f"FAIL-RP-INPUT: 设计目录不存在: {design_dir}")
    tasks = tasks_from_manifest(design_dir)
    if not tasks and (design_dir / "character_design.json").exists():
        tasks = tasks_from_json(design_dir / "character_design.json")
    if not tasks:
        for md_path in sorted(design_dir.glob("*.md")):
            task = task_from_markdown(md_path)
            if task:
                tasks.append(task)
    if not tasks:
        raise SkillError(f"FAIL-RP-PROMPT: 未能从设计目录提取角色 prompt: {design_dir}")
    return tasks


def discover_design_dir(project: str, episode: str) -> Path:
    return REPO_ROOT / "projects" / "aigc" / project / "4-Design" / "角色" / "2-设计" / episode


def default_output_dir(project: str, episode: str) -> Path:
    return REPO_ROOT / "projects" / "aigc" / project / "4-Design" / "角色" / "3-面板" / episode


def load_template(path: Path) -> dict[str, Any]:
    payload = read_json(path)
    if not isinstance(payload, dict) or not isinstance(payload.get("prompt_payload"), dict):
        raise SkillError(f"FAIL-RP-TEMPLATE: 模板缺少 prompt_payload: {path}")
    return payload


def layout_prompt_from_template(template: dict[str, Any]) -> str:
    payload = template["prompt_payload"]
    generation = payload.get("layout_generation_prompt") or {}
    if not isinstance(generation, dict):
        raise SkillError("FAIL-RP-TEMPLATE: layout_generation_prompt 必须是对象")
    lines: list[str] = []
    canvas = str(generation.get("canvas_setup") or "").strip()
    if canvas:
        lines.append(canvas)
    for key in ("left_panel_instructions", "center_panel_instructions", "right_panel_instructions"):
        section = generation.get(key)
        if not isinstance(section, dict):
            continue
        title = str(section.get("title") or "").strip()
        if title:
            lines.append(f"\n{title}")
        for module in section.get("modules") or []:
            if not isinstance(module, dict):
                continue
            name = str(module.get("module") or "").strip()
            content = str(module.get("content") or "").strip()
            if name and content:
                lines.append(f"- {name}: {content}")
    requirements = [str(item).strip() for item in generation.get("critical_requirements") or [] if str(item).strip()]
    if requirements:
        lines.append("\nCritical requirements:")
        lines.extend(f"- {item}" for item in requirements)
    return "\n".join(lines).strip()


def resolve_smart_mode(args: argparse.Namespace) -> str:
    if args.smart_mode != "auto":
        return args.smart_mode
    if args.prompt_text:
        return "natural-language-t2i"
    if args.prompt_file:
        return "single-doc-t2i"
    return "continuous-batch"


def load_panel_auto_generate_module() -> Any:
    module_path = PANEL_PARENT_DIR / "_shared" / "panel_auto_generate.py"
    spec = importlib.util.spec_from_file_location("panel_auto_generate_bridge", module_path)
    if spec is None or spec.loader is None:
        raise SkillError(f"FAIL-RP-HANDOFF: 无法加载共享 SMART bridge: {module_path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def source_context(args: argparse.Namespace) -> str:
    if args.prompt_text or args.prompt_file:
        return "direct-request"
    return "panel-stage"


def continuity_roots_for_task(task: PanelTask, smart_mode: str) -> list[str]:
    if smart_mode != "continuous-batch" or task.source_file == "inline_prompt":
        return []
    source = resolve_path(task.source_file)
    root = source.parent if source.is_file() else source
    return [repo_rel(root)] if root.exists() else []


def compose_prompt(task: PanelTask, layout_prompt: str, reference_hint: str) -> str:
    parts = [
        f"### 角色ID: {task.role_id}",
        f"### 角色名: {task.role_name}",
        f"### 固定标签: {task.role_id}+{task.role_name}",
        "",
        "【设计主体】",
        task.design_prompt.strip(),
        "",
        "【布局合同】",
        layout_prompt,
    ]
    if reference_hint:
        parts.extend(["", "【参照图约束】", reference_hint])
    return "\n".join(parts).strip()


def build_layout_doc(
    *,
    task: PanelTask,
    project: str,
    episode: str,
    output_dir: Path,
    template: dict[str, Any],
    template_path: Path,
    smart_mode_requested: str,
    smart_mode_resolved: str,
) -> tuple[dict[str, Any], Path]:
    layout_prompt = layout_prompt_from_template(template)
    refs = dedupe(task.explicit_refs, max_total=14)
    images = [{"url": ref} for ref in refs]
    reference_hint = ""
    if smart_mode_resolved == "continuous-batch":
        reference_hint = "共享 SMART bridge 会自动匹配上游角色设计图作为形象连续性参照；保持身份、体态、服装状态和风格一致，但不得复制参照图中的偶发构图或噪声。"
    if task.explicit_refs:
        explicit_hint = "用户显式参考图优先，保持当前设计主体身份，不从服装或风格参考图偷换角色脸。"
        reference_hint = f"{reference_hint}\n{explicit_hint}".strip()
    prompt_text = compose_prompt(task, layout_prompt, reference_hint)

    prompt_payload = copy.deepcopy(template["prompt_payload"])
    prompt_payload["prompt_text"] = prompt_text
    segments = prompt_payload.setdefault("prompt_segments", {})
    if isinstance(segments, dict):
        segments["identity_prompt"] = f"{task.role_id}+{task.role_name}"
        segments["design_subject_prompt"] = task.design_prompt
        segments["layout_prompt"] = layout_prompt

    filename_prefix = f"{safe_name(task.role_id)}-{safe_name(task.role_name)}-{safe_name(task.costume_state)}-CharacterPanel"
    layout_path = output_dir / f"{filename_prefix}-layout.json"
    image_output_dir = output_dir / "generated" / filename_prefix
    image_filename = f"{filename_prefix}.png"
    now = datetime.now().astimezone().isoformat(timespec="seconds")
    layout_doc = {
        "meta": {
            "project_name": project,
            "episode_id": episode,
            "skill_id": "aigc/4-Design/角色/3-面板",
            "generated_at": now,
            "template_path": template_path.as_posix(),
            "source_role_design": task.source_file,
            "smart_mode_requested": smart_mode_requested,
            "smart_mode_resolved": smart_mode_resolved,
        },
        "subject": {
            "role_id": task.role_id,
            "role_name": task.role_name,
            "role_tier": task.role_tier,
            "costume_state": task.costume_state,
            "identity_badge": f"{task.role_id}+{task.role_name}",
            "group_portrait": task.role_tier in {"crowd", "group", "ensemble", "群像角色"} or "群像" in task.role_name,
        },
        "design_subject_source": task.source_kind,
        "design_subject": task.design_prompt,
        "prompt_payload": prompt_payload,
        "prompt": prompt_text,
        "images": images,
        "references": {
            "reference_images": [],
            "explicit_references": [{"url": ref, "ref_type": "explicit_reference"} for ref in task.explicit_refs],
        },
        "render_contract": {
            "target_skill_id": "imagegen",
            "render_mode": "CHARACTER_ATMOSPHERIC_DOSSIER",
            "aspect_ratio": DEFAULT_ASPECT_RATIO,
            "layout": "three-column",
        },
        "image_generation": {
            "target_skill_id": "imagegen",
            "smart_mode_requested": smart_mode_requested,
            "smart_mode_resolved": smart_mode_resolved,
            "prompt_field": "prompt_payload.prompt_text",
            "prompt_text": prompt_text,
            "reference_images": [],
            "explicit_references": refs,
            "continuity_source_roots": continuity_roots_for_task(task, smart_mode_resolved),
            "output_dir": image_output_dir.as_posix(),
            "output_filename": image_filename,
            "request_id": filename_prefix,
        },
        "output": {
            "packet_filename": layout_path.name,
            "target_image_filename": image_filename,
        },
    }
    return layout_doc, layout_path


def collect_tasks(args: argparse.Namespace, episode: str) -> list[PanelTask]:
    explicit_refs = split_refs([*args.reference_image, *args.subject_reference, *args.costume_reference])
    if args.prompt_text:
        return [
            PanelTask(
                role_id=normalize_id(args.role_id or "ROLE-001"),
                role_name=args.role_name or "自然语言角色",
                role_tier="manual",
                costume_state=args.costume_state or "baseline",
                design_prompt=args.prompt_text.strip(),
                source_file="inline_prompt",
                source_kind="natural_language_prompt",
                explicit_refs=explicit_refs,
            )
        ]

    if args.prompt_file:
        prompt_path = resolve_path(args.prompt_file)
        if not prompt_path.exists():
            raise SkillError(f"FAIL-RP-INPUT: prompt-file 不存在: {prompt_path}")
        if prompt_path.is_dir():
            tasks = tasks_from_dir(prompt_path)
        elif prompt_path.suffix.lower() == ".json":
            tasks = tasks_from_json(prompt_path)
        else:
            task = task_from_markdown(prompt_path)
            tasks = [task] if task else []
    else:
        tasks = tasks_from_dir(discover_design_dir(args.project, episode))

    if not tasks:
        raise SkillError("FAIL-RP-PROMPT: 未提取到任何角色面板任务")
    for task in tasks:
        task.explicit_refs = explicit_refs
    return tasks


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="生成角色 CharacterPanel layout JSON，并默认调用 built-in imagegen 生图")
    parser.add_argument("--project", required=True, help="项目名，对应 projects/aigc/<项目名>")
    parser.add_argument("--episode", default="第1集", help="集数，默认 第1集")
    parser.add_argument("--prompt-file", help="指定 Markdown / JSON / 目录")
    parser.add_argument("--prompt-text", help="自然语言 prompt，默认无参照 T2I")
    parser.add_argument("--role-id", default="", help="prompt-text 模式可指定角色 ID")
    parser.add_argument("--role-name", default="", help="prompt-text 模式可指定角色名")
    parser.add_argument("--costume-state", default="baseline", help="prompt-text 模式可指定服装状态")
    parser.add_argument("--output-dir", help="覆盖 layout 输出目录")
    parser.add_argument("--template", default=str(TEMPLATE_PATH), help="覆盖模板路径")
    parser.add_argument("--reference-image", action="append", default=[], help="显式参考图，可重复或逗号分隔")
    parser.add_argument("--subject-reference", action="append", default=[], help="显式人物参照图")
    parser.add_argument("--costume-reference", action="append", default=[], help="显式服装参照图")
    parser.add_argument(
        "--smart-mode",
        default="auto",
        choices=["auto", "continuous-batch", "single-doc-t2i", "natural-language-t2i", "off"],
        help="默认 auto：批量自动参照，单文件/自然语言默认 T2I",
    )
    parser.add_argument("--layout-only", action="store_true", help="只写 layout JSON 和 request sidecar，不调用生图")
    parser.add_argument("--json-only", action="store_true", help="同 --layout-only")
    parser.add_argument("--foreground", action="store_true", help="前台等待 内置 imagegen 完成；默认内置 imagegen 请求准备")
    parser.add_argument(
        "--dry-run",
        "--generation-dry-run",
        dest="dry_run",
        action="store_true",
        help="调用 built-in imagegen dry-run，不真实请求 API",
    )
    parser.add_argument("--print-payload", action="store_true", help="打印 imagegen payload")
    parser.add_argument("--max-concurrent", type=int, default=100, help="生图并发，默认 100")
    parser.add_argument("--timeout", type=int, default=180, help="单任务超时秒数")
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    try:
        episode = normalize_episode(args.episode)
        output_dir = resolve_path(args.output_dir) if args.output_dir else default_output_dir(args.project, episode)
        template_path = resolve_path(args.template)
        template = load_template(template_path)
        smart_mode = resolve_smart_mode(args)
        tasks = collect_tasks(args, episode)

        layout_paths: list[str] = []
        layout_path_objects: list[Path] = []
        for task in tasks:
            layout_doc, layout_path = build_layout_doc(
                task=task,
                project=args.project,
                episode=episode,
                output_dir=output_dir,
                template=template,
                template_path=template_path,
                smart_mode_requested=args.smart_mode,
                smart_mode_resolved=smart_mode,
            )
            write_json(layout_path, layout_doc)
            layout_paths.append(repo_rel(layout_path))
            layout_path_objects.append(layout_path)

        bridge_result: dict[str, Any] | None = None
        request_sidecar = ""
        if args.smart_mode != "off":
            bridge_module = load_panel_auto_generate_module()
            bridge_result = bridge_module.run_panel_auto_generate(
                layout_path_objects,
                smart_mode=smart_mode,
                dry_run=args.dry_run,
                print_payload=args.print_payload,
                max_concurrent=args.max_concurrent,
                timeout=args.timeout,
                generate=not (args.layout_only or args.json_only),
                background=not args.foreground,
                pipeline_context=source_context(args),
            )
            request_sidecar = bridge_result.get("request_batch_path", "")

        manifest = {
            "status": (
                "layout-only"
                if (args.layout_only or args.json_only)
                else ("dry-run" if args.dry_run else ((bridge_result or {}).get("status") or "generated"))
            ),
            "project_name": args.project,
            "episode_id": episode,
            "skill_id": "aigc-design-role-panel",
            "smart_mode_resolved": smart_mode,
            "layout_count": len(layout_paths),
            "layout_files": layout_paths,
            "request_sidecar": request_sidecar,
            "bridge_report_path": (bridge_result or {}).get("bridge_report_path", ""),
            "auto_reference_count": sum(
                int(task.get("continuity_reference_count", 0))
                for task in ((bridge_result or {}).get("trace", {}) or {}).get("tasks", [])
            ),
            "explicit_reference_count": sum(len(task.explicit_refs) for task in tasks),
        }
        if bridge_result is not None:
            manifest["generation_result"] = {
                "success": bridge_result.get("success"),
                "success_count": bridge_result.get("success_count"),
                "failed_count": bridge_result.get("failed_count"),
                "dry_run": args.dry_run,
                "skipped": bridge_result.get("skipped", False),
                "execution_mode": bridge_result.get("execution_mode"),
                "provider_skill": bridge_result.get("provider_skill"),
                "provider_mode": bridge_result.get("provider_mode"),
                "default_model": bridge_result.get("default_model"),
                "generated_source_path": bridge_result.get("generated_source_path"),
            }

        write_json(output_dir / "_manifest.json", manifest)
        print(f"✅ layout: {len(layout_paths)}")
        if request_sidecar:
            print(f"✅ request_sidecar: {request_sidecar}")
        if args.layout_only or args.json_only:
            print("✅ JSON-only 完成：未调用 built-in imagegen。")
            return 0
        if bridge_result is not None and not bridge_result.get("success", False):
            print(f"❌ generation_failed: {bridge_result.get('failed_count', 0)}")
            return 1
        if args.dry_run:
            print("✅ dry-run 完成：已构造 built-in imagegen 请求，未真实调用 API。")
            return 0
        failed = int((bridge_result or {}).get("failed_count", 0))
        print(f"✅ generation_success: {(bridge_result or {}).get('success_count', 0)}")
        print(f"❌ generation_failed: {failed}")
        return 0 if failed == 0 else 1
    except SkillError as exc:
        print(f"❌ {exc}")
        return 1
    except Exception as exc:  # pragma: no cover
        print(f"❌ FAIL-RP-TRACE: {exc}")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
