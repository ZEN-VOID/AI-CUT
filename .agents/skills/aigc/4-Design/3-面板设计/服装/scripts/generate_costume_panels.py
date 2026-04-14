#!/usr/bin/env python3
from __future__ import annotations

import argparse
import importlib.util
import json
import re
from pathlib import Path
from typing import Any, Dict, List


SKILL_DIR = Path(__file__).resolve().parents[1]
TEMPLATE_PATH = SKILL_DIR / "templates" / "服装面板-提示词.json"


class PanelBuildError(RuntimeError):
    pass


def _read_json(path: Path) -> Dict[str, Any]:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:
        raise PanelBuildError(f"JSON 读取失败: {path} ({exc})") from exc


def _repo_root() -> Path:
    current = Path(__file__).resolve()
    for parent in current.parents:
        if (parent / ".codex").exists():
            return parent
    return Path.cwd()


def _safe_name(value: str) -> str:
    text = re.sub(r'[\\/:*?"<>|]+', "-", (value or "").strip())
    return text or "unnamed-costume"


def _load_template() -> Dict[str, Any]:
    data = _read_json(TEMPLATE_PATH)
    payload = data.get("prompt_payload")
    if not isinstance(payload, dict):
        raise PanelBuildError(f"模板缺少 prompt_payload: {TEMPLATE_PATH}")
    return payload


def _load_panel_auto_generate_module() -> Any:
    module_path = Path(__file__).resolve().parents[2] / "_shared" / "panel_auto_generate.py"
    spec = importlib.util.spec_from_file_location("panel_auto_generate_bridge", module_path)
    if spec is None or spec.loader is None:
        raise PanelBuildError(f"无法加载自动生图桥接脚本: {module_path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _episode_dirs(input_root: Path, episode: str | None) -> List[Path]:
    if episode:
        target = input_root / episode
        if not target.exists():
            raise PanelBuildError(f"未找到 episode 目录: {target}")
        return [target]
    return sorted(path for path in input_root.iterdir() if path.is_dir() and (path / "服装设计.json").exists())


def _prompt_index(prompt_sidecar: Dict[str, Any]) -> Dict[str, Dict[str, Any]]:
    result: Dict[str, Dict[str, Any]] = {}
    for item in prompt_sidecar.get("costumes", []) or []:
        if isinstance(item, dict):
            costume_id = str(item.get("costume_id") or "").strip()
            if costume_id:
                result[costume_id] = item
    return result


def _join_non_empty(parts: List[str]) -> str:
    return "\n\n".join(part.strip() for part in parts if part and part.strip())


def _build_layout_doc(
    *,
    project_name: str,
    episode_id: str,
    costume_entry: Dict[str, Any],
    prompt_entry: Dict[str, Any] | None,
    template_payload: Dict[str, Any],
    output_path: Path,
    degraded_mode: bool,
    continuity_root: Path,
) -> Dict[str, Any]:
    costume_id = str(costume_entry.get("costume_id") or "").strip()
    label = str(costume_entry.get("canonical_label") or costume_entry.get("role_name") or "未命名服装").strip()
    if not costume_id:
        raise PanelBuildError(f"{episode_id} 存在缺少 costume_id 的服装条目")

    prompt_cn = ""
    negative_constraints: List[str] = []
    if prompt_entry:
        prompt_cn = str(prompt_entry.get("prompt_cn") or "").strip()
        negative_constraints = [str(item).strip() for item in prompt_entry.get("negative_constraints", []) or [] if str(item).strip()]
    if not prompt_cn:
        design_thesis = costume_entry.get("design_thesis") or {}
        prompt_cn = str(design_thesis.get("identity_goal") or costume_entry.get("prompt_anchor") or "").strip()

    mandatory_rules = [
        str(item).strip()
        for item in (template_payload.get("_prompt_text_assembly_guide") or {}).get("mandatory_rules", [])
        if str(item).strip()
    ]
    identity_prompt = f"Identity badge: {costume_id}+{label}."
    layout_prompt = str(template_payload.get("layout_generation_prompt") or "").strip()
    negative_prompt = "; ".join(negative_constraints)
    prompt = _join_non_empty(
        [
            identity_prompt,
            prompt_cn,
            layout_prompt,
            "Mandatory rules:\n- " + "\n- ".join(mandatory_rules) if mandatory_rules else "",
            f"Negative constraints: {negative_prompt}" if negative_prompt else "",
        ]
    )
    output_filename = f"{costume_id}-{_safe_name(label)}-CostumePanel.png"

    return {
        "meta": {
            "project_name": project_name,
            "episode_id": episode_id,
            "skill_id": "aigc-design-costume-panel",
            "source_design": f"projects/aigc/{project_name}/4-Design/服装/2-设计/{episode_id}/服装设计.json",
            "source_prompt": f"projects/aigc/{project_name}/4-Design/服装/2-设计/{episode_id}/costume_design_prompt.json",
        },
        "subject": {
            "costume_id": costume_id,
            "canonical_label": label,
            "identity_badge": f"{costume_id}+{label}",
            "role_id": costume_entry.get("role_id"),
            "costume_state": costume_entry.get("costume_state"),
        },
        "layout_contract": {
            "template_type": (template_payload.get("layout") or {}).get("template_type", "COSTUME_SYSTEM_DOSSIER"),
            "aspect_ratio": (template_payload.get("layout") or {}).get("aspect_ratio", "16:9"),
            "canvas_size": (template_payload.get("layout") or {}).get("canvas_size", "4096x2304"),
            "module_contract": template_payload.get("layout_modules", {}),
            "mandatory_rules": mandatory_rules,
        },
        "prompt_segments": {
            "identity_prompt": identity_prompt,
            "layout_prompt": layout_prompt,
            "negative_prompt_global": negative_prompt,
        },
        "prompt": prompt,
        "degraded_mode": degraded_mode,
        "image_generation": {
            "target_skill_id": "nano-banana-general",
            "smart_mode_default": "continuous-batch",
            "prompt_field": "prompt",
            "prompt_text": prompt,
            "prompt_reference_sections": [
                "prompt",
                "prompt_segments.identity_prompt",
                "prompt_segments.layout_prompt",
                "prompt_segments.negative_prompt_global",
            ],
            "reference_images": [],
            "explicit_references": [],
            "continuity_source_roots": [continuity_root.as_posix()],
            "output_filename": output_filename,
            "request_id": output_path.stem,
        },
        "output": {
            "packet_filename": output_path.name,
            "target_image_filename": output_filename,
            "layout_path": str(output_path),
        },
    }


def build_panels(
    project_name: str,
    episode: str | None,
    dry_run: bool,
    *,
    auto_generate: bool,
    smart_mode: str,
    explicit_references: List[str],
    max_concurrent: int,
    print_payload: bool,
    save_images: bool,
    no_report: bool,
) -> int:
    repo_root = _repo_root()
    project_root = repo_root / "projects" / "aigc" / project_name
    input_root = project_root / "4-Design" / "服装" / "2-设计"
    output_root = project_root / "4-Design" / "服装" / "3-面板"
    if not input_root.exists():
        raise PanelBuildError(f"未找到输入根目录: {input_root}")

    template_payload = _load_template()
    built_files = 0

    for episode_dir in _episode_dirs(input_root, episode):
        episode_id = episode_dir.name
        output_dir = output_root / episode_id
        design_master = _read_json(episode_dir / "服装设计.json")
        prompt_sidecar_path = episode_dir / "costume_design_prompt.json"
        prompt_sidecar = _read_json(prompt_sidecar_path) if prompt_sidecar_path.exists() else {"costumes": []}
        prompt_map = _prompt_index(prompt_sidecar)
        manifest: Dict[str, Any] = {
            "meta": {
                "project_name": project_name,
                "episode_id": episode_id,
                "skill_id": "aigc-design-costume-panel",
            },
            "inputs": {
                "design_master": str((episode_dir / "服装设计.json").relative_to(repo_root)),
                "prompt_sidecar": str(prompt_sidecar_path.relative_to(repo_root)),
                "template": str(TEMPLATE_PATH.relative_to(repo_root)),
            },
            "outputs": [],
            "degraded_costumes": [],
        }
        if auto_generate:
            manifest["image_generation"] = {
                "enabled": True,
                "smart_mode_requested": smart_mode,
                "status": "pending" if not dry_run else "skipped-dry-run",
            }
        costumes = design_master.get("costumes", []) or []
        if not isinstance(costumes, list) or not costumes:
            raise PanelBuildError(f"{episode_id} 未找到可消费的 costumes[]")

        if not dry_run:
            output_dir.mkdir(parents=True, exist_ok=True)

        for costume_entry in costumes:
            if not isinstance(costume_entry, dict):
                continue
            costume_id = str(costume_entry.get("costume_id") or "").strip()
            label = str(costume_entry.get("canonical_label") or "未命名服装").strip()
            if not costume_id:
                raise PanelBuildError(f"{episode_id} 存在缺少 costume_id 的服装条目")
            layout_path = output_dir / f"{costume_id}-{_safe_name(label)}-CostumePanel-layout.json"
            prompt_entry = prompt_map.get(costume_id)
            degraded_mode = prompt_entry is None
            layout_doc = _build_layout_doc(
                project_name=project_name,
                episode_id=episode_id,
                costume_entry=costume_entry,
                prompt_entry=prompt_entry,
                template_payload=template_payload,
                output_path=layout_path,
                degraded_mode=degraded_mode,
                continuity_root=episode_dir,
            )
            manifest["outputs"].append(str(layout_path.relative_to(repo_root)))
            if degraded_mode:
                manifest["degraded_costumes"].append(costume_id)
            if not dry_run:
                layout_path.write_text(json.dumps(layout_doc, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
            built_files += 1

        auto_generate_error: str | None = None
        if auto_generate and not dry_run:
            try:
                bridge_module = _load_panel_auto_generate_module()
                packet_paths = [repo_root / relative for relative in manifest["outputs"]]
                auto_generate_result = bridge_module.run_panel_auto_generate(
                    packet_paths,
                    manifest_path=output_dir / "_manifest.json",
                    smart_mode=smart_mode,
                    explicit_references=explicit_references,
                    max_concurrent=max_concurrent,
                    print_payload=print_payload,
                    save_images=save_images,
                    no_report=no_report,
                    pipeline_context="panel-stage",
                )
                manifest["image_generation"] = {
                    "enabled": True,
                    "smart_mode_requested": smart_mode,
                    "smart_mode_resolved": auto_generate_result.get("smart_mode_resolved", ""),
                    "success": bool(auto_generate_result.get("success", False)),
                    "task_count": auto_generate_result.get("task_count", 0),
                    "success_count": auto_generate_result.get("success_count", 0),
                    "failed_count": auto_generate_result.get("failed_count", 0),
                    "request_batch_path": auto_generate_result.get("request_batch_path"),
                    "bridge_report_path": auto_generate_result.get("bridge_report_path"),
                    "batch_report_path": auto_generate_result.get("batch_report_path"),
                }
                if not auto_generate_result.get("success", False):
                    auto_generate_error = f"{episode_id} 自动生图桥接失败，请查看 {auto_generate_result.get('bridge_report_path')}"
            except Exception as exc:
                manifest["image_generation"] = {
                    "enabled": True,
                    "smart_mode_requested": smart_mode,
                    "success": False,
                    "error": str(exc),
                }
                auto_generate_error = f"{episode_id} 自动生图桥接失败: {exc}"

        if not dry_run:
            (output_dir / "_manifest.json").write_text(
                json.dumps(manifest, ensure_ascii=False, indent=2) + "\n",
                encoding="utf-8",
            )
        if auto_generate_error:
            raise PanelBuildError(auto_generate_error)

    return built_files


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="根据服装设计真源生成 panel layout JSON")
    parser.add_argument("--project", required=True, help="项目名")
    parser.add_argument("--episode", help="可选；只处理指定集，例如 第1集")
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
    parser.add_argument("--dry-run", action="store_true", help="只检查输入并打印统计，不落盘")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    count = build_panels(
        args.project,
        args.episode,
        args.dry_run,
        auto_generate=args.auto_generate,
        smart_mode=args.smart_mode,
        explicit_references=args.reference,
        max_concurrent=args.max_concurrent,
        print_payload=args.print_payload,
        save_images=not args.no_save_images,
        no_report=args.no_report,
    )
    print(json.dumps({"status": "ok", "panel_count": count, "dry_run": args.dry_run}, ensure_ascii=False))


if __name__ == "__main__":
    main()
