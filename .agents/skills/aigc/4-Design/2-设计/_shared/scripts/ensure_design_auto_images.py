#!/usr/bin/env python3
"""Ensure 4-Design/2-设计 Markdown files have same-stem built-in imagegen requests."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Iterable


REPO_ROOT = Path(__file__).resolve().parents[7]
SCRIPT_DIR = Path(__file__).resolve().parent
RUN_DESIGN_AUTO_IMAGE = SCRIPT_DIR / "run_design_auto_image.py"
IMAGE_EXTENSIONS = (".png", ".jpg", ".jpeg", ".webp")
ACTIVE_DOMAINS = ("场景", "角色", "道具")
if SCRIPT_DIR.as_posix() not in sys.path:
    sys.path.insert(0, SCRIPT_DIR.as_posix())

from run_design_auto_image import build_full_prompt, build_request_doc  # noqa: E402


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="扫描 4-Design/2-设计 输出目录，补齐每个 Markdown 设计文件的同 stem 自动图。"
    )
    parser.add_argument("--project", help="项目名；用于自动发现 projects/aigc/<项目名>/4-Design/<域>/2-设计")
    parser.add_argument("--domain", action="append", choices=ACTIVE_DOMAINS, help="限定域，可重复传入")
    parser.add_argument("--episode", action="append", help="限定 episode 目录名，如 第1集；可重复传入")
    parser.add_argument("--design-dir", action="append", default=[], help="直接指定 2-设计/第N集 输出目录，可重复传入")
    parser.add_argument("--project-name", help="写入内置 imagegen 侧车的项目名；默认从 --project 或路径推断")
    parser.add_argument("--global-style", help="全局风格.md 路径；默认交给 run_design_auto_image.py 自动推断")
    parser.add_argument("--timeout", type=int, default=300, help="单个自动生图子进程最长等待秒数")
    parser.add_argument("--max-concurrent", type=int, default=1, help="兼容旧参数；内置 imagegen 由 Codex 逐资产调用")
    parser.add_argument("--foreground", action="store_true", help="兼容旧参数；内置 imagegen 由 Codex 会话前台执行")
    parser.add_argument("--write-report", action="store_true", help="兼容旧参数；本 helper 始终写 request sidecar")
    parser.add_argument("--generation-dry-run", action="store_true", help="只验证侧车生成，不代表已经调用内置 imagegen")
    parser.add_argument("--plan-only", action="store_true", help="只打印缺图计划，不调用 helper，也不写 manifest")
    parser.add_argument("--manifest-name", default="_manifest.json", help="要更新的 manifest 文件名")
    return parser.parse_args()


def repo_relative(path: Path) -> str:
    try:
        return path.resolve().relative_to(REPO_ROOT.resolve()).as_posix()
    except ValueError:
        return path.as_posix()


def resolve_path(value: str) -> Path:
    path = Path(value).expanduser()
    if not path.is_absolute():
        path = (REPO_ROOT / path).resolve()
    return path


def infer_project_name(design_dir: Path, explicit_project: str | None, fallback: str | None) -> str:
    if fallback:
        return fallback
    if explicit_project:
        return explicit_project
    parts = design_dir.resolve().parts
    for index, part in enumerate(parts):
        if part == "aigc" and index + 1 < len(parts):
            return parts[index + 1]
    return "未命名项目"


def discover_design_dirs(args: argparse.Namespace) -> list[Path]:
    dirs: list[Path] = [resolve_path(item) for item in args.design_dir]
    if args.project:
        domains = args.domain or list(ACTIVE_DOMAINS)
        for domain in domains:
            root = REPO_ROOT / "projects" / "aigc" / args.project / "4-Design" / domain / "2-设计"
            if not root.exists():
                continue
            if args.episode:
                dirs.extend(root / episode for episode in args.episode)
            else:
                dirs.extend(path for path in sorted(root.iterdir()) if path.is_dir())
    deduped: list[Path] = []
    seen: set[str] = set()
    for path in dirs:
        key = path.resolve().as_posix()
        if key in seen:
            continue
        seen.add(key)
        deduped.append(path)
    return deduped


def markdown_files(design_dir: Path) -> list[Path]:
    return sorted(path for path in design_dir.glob("*.md") if path.is_file() and not path.name.startswith("_"))


def same_stem_image(design_file: Path) -> Path | None:
    for suffix in IMAGE_EXTENSIONS:
        candidate = design_file.with_suffix(suffix)
        if candidate.exists():
            return candidate
    return None


def read_manifest(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return {}
    return payload if isinstance(payload, dict) else {}


def write_manifest(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def update_output_files(payload: dict[str, Any], image_paths: Iterable[str]) -> None:
    output_files = payload.setdefault("output_files", [])
    if not isinstance(output_files, list):
        output_files = []
        payload["output_files"] = output_files
    seen = {str(item) for item in output_files}
    for image_path in image_paths:
        if image_path not in seen:
            output_files.append(image_path)
            seen.add(image_path)


def build_missing_request_docs(
    design_files: Iterable[Path],
    *,
    project_name: str,
    global_style: Path | None,
) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    request_docs: list[dict[str, Any]] = []
    attempts: list[dict[str, Any]] = []
    for design_file in design_files:
        try:
            full_prompt = build_full_prompt(design_file, None, global_style)
            request_docs.append(
                build_request_doc(
                    design_file=design_file,
                    project_name=project_name,
                    prompt=full_prompt,
                    aspect_ratio="16:9",
                    image_size="4K",
                )
            )
            attempts.append(
                {
                    "design_file": repo_relative(design_file),
                    "returncode": None,
                    "planned": True,
                    "request_id": f"design-auto-image-{design_file.stem}",
                }
            )
        except Exception as exc:
            attempts.append(
                {
                    "design_file": repo_relative(design_file),
                    "returncode": 1,
                    "planned": False,
                    "error": str(exc),
                }
            )
    return request_docs, attempts


def write_batch_request(design_dir: Path, request_docs: list[dict[str, Any]]) -> Path:
    request_dir = design_dir / "generated" / "requests"
    request_dir.mkdir(parents=True, exist_ok=True)
    request_path = request_dir / "design_auto_image_batch.json"
    request_path.write_text(json.dumps({"tasks": request_docs}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return request_path


def run_batch_requests(
    request_path: Path,
    *,
    timeout: int,
    max_concurrent: int,
    write_report: bool,
    generation_dry_run: bool,
    foreground: bool,
) -> dict[str, Any]:
    return {
        "execution_mode": "codex-builtin-imagegen",
        "status": "request_ready",
        "returncode": 0,
        "request_batch_path": request_path.as_posix(),
        "provider_skill": "imagegen",
        "provider_mode": "built-in image_gen",
        "default_model": "GPT-IMAGE-2",
        "foreground": bool(foreground),
        "generation_dry_run": bool(generation_dry_run),
        "next_step": "Call built-in image_gen once per task, then copy selected generated images into each task output_dir/output_filename.",
    }


def ensure_dir(args: argparse.Namespace, design_dir: Path) -> tuple[dict[str, Any], int]:
    manifest_path = design_dir / args.manifest_name
    project_name = infer_project_name(design_dir, args.project, args.project_name)
    global_style = resolve_path(args.global_style) if args.global_style else None
    files = markdown_files(design_dir) if design_dir.exists() else []
    initial_images: dict[Path, Path | None] = {path: same_stem_image(path) for path in files}
    missing = [path for path, image in initial_images.items() if image is None]

    attempts: list[dict[str, Any]] = []
    batch_result: dict[str, Any] = {}
    if missing:
        if args.plan_only:
            attempts = [{"design_file": repo_relative(design_file), "returncode": None, "planned": True} for design_file in missing]
        else:
            request_docs, attempts = build_missing_request_docs(
                missing,
                project_name=project_name,
                global_style=global_style,
            )
            if request_docs:
                request_path = write_batch_request(design_dir, request_docs)
                batch_result = run_batch_requests(
                    request_path,
                    timeout=args.timeout,
                    max_concurrent=args.max_concurrent,
                    write_report=args.write_report,
                    generation_dry_run=args.generation_dry_run,
                    foreground=args.foreground,
                )

    final_images = {path: same_stem_image(path) for path in files}
    image_paths = [repo_relative(image) for image in final_images.values() if image is not None]
    missing_after = [repo_relative(path) for path, image in final_images.items() if image is None]

    if args.generation_dry_run:
        status = "dry_run"
    elif batch_result.get("execution_mode") == "codex-builtin-imagegen":
        status = "request_ready"
    elif not files:
        status = "no_markdown"
    elif missing_after:
        status = "failed"
    else:
        status = "success"

    auto_image = {
        "provider_skill": "imagegen",
        "provider_mode": "built-in image_gen",
        "default_model": "GPT-IMAGE-2",
        "mode": "single-subject-t2i",
        "prompt_field": "full_generation_prompt",
        "output_dir_policy": "same_directory_as_design_file",
        "filename_policy": "same_stem_as_design_file",
        "status": status,
        "image_paths": image_paths,
        "checked_design_files": [repo_relative(path) for path in files],
        "missing_design_files": missing_after,
        "attempted_count": len(attempts),
        "existing_count": sum(1 for image in initial_images.values() if image is not None),
        "generated_count": max(0, len(image_paths) - sum(1 for image in initial_images.values() if image is not None)),
        "timeout_seconds": args.timeout,
        "max_concurrent": args.max_concurrent,
        "execution_mode": batch_result.get("execution_mode", "plan-only" if args.plan_only else "already-complete"),
        "request_batch_path": batch_result.get("request_batch_path", ""),
        "generated_source_path": "",
        "generation_dry_run": bool(args.generation_dry_run),
        "next_step": batch_result.get("next_step", ""),
        "attempts": attempts,
    }

    report = {
        "design_dir": repo_relative(design_dir),
        "project_name": project_name,
        "auto_image": auto_image,
    }

    if not args.plan_only:
        manifest = read_manifest(manifest_path)
        manifest["auto_image"] = auto_image
        update_output_files(manifest, image_paths)
        write_manifest(manifest_path, manifest)

    return report, 0 if status in {"success", "dry_run", "request_ready"} else 1


def main() -> int:
    args = parse_args()
    design_dirs = discover_design_dirs(args)
    if not design_dirs:
        print("[ensure-auto-images][ERROR] 未找到任何 2-设计 输出目录", file=sys.stderr)
        return 1

    reports: list[dict[str, Any]] = []
    failed = False
    for design_dir in design_dirs:
        report, returncode = ensure_dir(args, design_dir)
        reports.append(report)
        failed = failed or returncode != 0

    print(json.dumps({"reports": reports}, ensure_ascii=False, indent=2))
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
