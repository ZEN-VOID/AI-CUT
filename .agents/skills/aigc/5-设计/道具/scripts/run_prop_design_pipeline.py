#!/usr/bin/env python3
"""Run the prop design pipeline for 5-设计/道具."""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path

from build_prop_design_packets import main as build_main


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="运行 5-设计/道具 pipeline，默认以 `道具清单.json` 为第一输入根。"
    )
    parser.add_argument("--catalog", required=True, help="道具清单.json 路径")
    parser.add_argument("--detail", help="3-Detail/第N集.json 路径；仅用于 traceability 补证，默认按项目根自动推断")
    parser.add_argument("--research", help="道具研究.json 路径；默认按清单目录自动推断")
    parser.add_argument("--bridge", help="prop_design_bridge.json 路径；默认按清单目录自动推断")
    parser.add_argument("--global-style", help="全局风格.md 路径；默认按项目根自动推断")
    parser.add_argument("--type-elements", dest="type_elements", help="全集类型元素.md 路径；默认按项目根自动推断")
    parser.add_argument("--design-elements", dest="design_elements", help="导演意图.md 路径；默认按项目根自动推断")
    parser.add_argument("--north-star", help="north_star.yaml 路径；默认按项目根自动推断")
    parser.add_argument("--init-handoff", help="init_handoff.yaml 路径；默认按项目根自动推断")
    parser.add_argument(
        "--output-dir",
        help="输出目录；默认推断到 `projects/aigc/<项目名>/4-设计/`",
    )
    parser.add_argument("--prop-id", action="append", dest="prop_ids", help="只处理指定 prop_id，可重复传入")
    parser.add_argument(
        "--prop-name",
        action="append",
        dest="prop_names",
        help="只处理指定 canonical_name，可重复传入",
    )
    parser.add_argument("--write-compat-json", action="store_true", help="额外导出 `道具设计.json` 与 `prop_design_prompt.json`")
    parser.add_argument("--skip-auto-image", action="store_true", help="只生成设计文件，不调用 内置 imagegen 自动生图")
    parser.add_argument("--auto-image-dry-run", action="store_true", help="自动生图步骤只验证 payload，不真实调用 API")
    parser.add_argument("--dry-run", action="store_true", help="只预览 manifest，不写文件")
    parser.add_argument(
        "--allow-legacy-script-authorship",
        action="store_true",
        help="受控兼容模式：允许旧式脚本直接生成创作型道具设计内容。",
    )
    return parser.parse_args()


def ensure_exists(path: Path, label: str) -> None:
    if not path.exists():
        raise FileNotFoundError(f"{label} 不存在: {path}")


def infer_project_root(catalog_path: Path) -> Path:
    resolved = catalog_path.resolve()
    for parent in resolved.parents:
        if parent.name == "5-设计":
            return parent.parent
    raise ValueError(f"无法从 catalog 路径推断项目根: {catalog_path}")


def infer_output_dir(catalog_path: Path) -> Path:
    return infer_project_root(catalog_path) / "5-设计"


def first_existing(*paths: Path) -> Path | None:
    for path in paths:
        if path.exists():
            return path
    return None


def update_auto_image_manifest(output_dir: Path, manifest_name: str = "_manifest.json", dry_run: bool = False) -> None:
    manifest_path = output_dir / manifest_name
    if not manifest_path.exists():
        return
    payload = json.loads(manifest_path.read_text(encoding="utf-8"))
    image_paths = []
    design_files = sorted(path for path in output_dir.glob("*.md") if path.is_file())
    for design_file in sorted(output_dir.glob("*.md")):
        for suffix in (".png", ".jpg", ".jpeg", ".webp"):
            image_path = design_file.with_suffix(suffix)
            if image_path.exists():
                image_paths.append(image_path.as_posix())
                break
    payload["auto_image"] = {
        "provider_skill": "imagegen",
        "provider_mode": "built-in image_gen",
        "default_model": "GPT-IMAGE-2",
        "mode": "single-subject-t2i",
        "prompt_field": "full_generation_prompt",
        "output_dir_policy": "same_directory_as_design_file",
        "filename_policy": "same_stem_as_design_file",
        "status": "dry_run" if dry_run else ("success" if design_files and len(image_paths) == len(design_files) else "failed"),
        "image_paths": image_paths,
    }
    output_files = payload.setdefault("output_files", [])
    for image_path in image_paths:
        if image_path not in output_files:
            output_files.append(image_path)
    manifest_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def mark_auto_image_skipped(output_dir: Path, manifest_name: str = "_manifest.json") -> None:
    manifest_path = output_dir / manifest_name
    if not manifest_path.exists():
        return
    payload = json.loads(manifest_path.read_text(encoding="utf-8"))
    payload["auto_image"] = {
        "provider_skill": "imagegen",
        "provider_mode": "built-in image_gen",
        "default_model": "GPT-IMAGE-2",
        "mode": "single-subject-t2i",
        "prompt_field": "full_generation_prompt",
        "output_dir_policy": "same_directory_as_design_file",
        "filename_policy": "same_stem_as_design_file",
        "status": "skipped_by_user",
        "image_paths": [],
    }
    manifest_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def run_auto_images(output_dir: Path, project_name: str, global_style_path: Path | None, dry_run: bool) -> int:
    helper = Path(__file__).resolve().parent / "ensure_design_auto_images.py"
    cmd = [
        sys.executable,
        helper.as_posix(),
        "--design-dir",
        output_dir.as_posix(),
        "--project-name",
        project_name,
    ]
    if global_style_path and global_style_path.exists():
        cmd.extend(["--global-style", global_style_path.as_posix()])
    if dry_run:
        cmd.append("--generation-dry-run")
    result = subprocess.run(cmd, check=False)
    return int(result.returncode)


def main() -> int:
    args = parse_args()
    catalog_path = Path(args.catalog)
    try:
        ensure_exists(catalog_path, "catalog")
        project_root = infer_project_root(catalog_path)
        episode_dir = catalog_path.parent
        episode_id = episode_dir.name

        output_dir = Path(args.output_dir) if args.output_dir else infer_output_dir(catalog_path)

        detail_path = Path(args.detail) if args.detail else project_root / "3-Detail" / f"{episode_id}.json"
        research_path = Path(args.research) if args.research else episode_dir / "道具研究.json"
        bridge_path = Path(args.bridge) if args.bridge else episode_dir / "prop_design_bridge.json"
        global_style_path = (
            Path(args.global_style)
            if args.global_style
            else first_existing(
                project_root / "2-Global" / "全局风格.md",
                project_root / "2-Global" / "全局风格" / "全局风格设计.md",
            )
        )
        type_elements_path = (
            Path(args.type_elements)
            if args.type_elements
            else first_existing(
                project_root / "2-Global" / "全集类型元素.md",
                project_root / "2-Global" / "类型元素" / "全集设计.md",
                project_root / "2-Global" / "类型元素.md",
            )
        )
        design_elements_path = (
            Path(args.design_elements)
            if args.design_elements
            else first_existing(
                project_root / "2-Global" / "导演意图.md",
                project_root / "2-Global" / "设计元素" / "设计元素.md",
            )
        )
        north_star_path = Path(args.north_star) if args.north_star else project_root / "0-Init" / "north_star.yaml"
        init_handoff_path = Path(args.init_handoff) if args.init_handoff else project_root / "0-Init" / "init_handoff.yaml"
    except (FileNotFoundError, ValueError) as exc:
        print(f"[ERROR] {exc}", file=sys.stderr)
        return 1

    argv = [
        "build_prop_design_packets.py",
        "--catalog",
        catalog_path.as_posix(),
        "--output-dir",
        output_dir.as_posix(),
    ]
    for flag, value in (
        ("--detail", detail_path),
        ("--research", research_path),
        ("--bridge", bridge_path),
        ("--global-style", global_style_path),
        ("--type-elements", type_elements_path),
        ("--design-elements", design_elements_path),
        ("--north-star", north_star_path),
        ("--init-handoff", init_handoff_path),
    ):
        if value is not None and Path(value).exists():
            argv.extend([flag, Path(value).as_posix()])

    for prop_id in args.prop_ids or []:
        argv.extend(["--prop-id", prop_id])
    for prop_name in args.prop_names or []:
        argv.extend(["--prop-name", prop_name])
    if args.write_compat_json:
        argv.append("--write-compat-json")
    if args.dry_run:
        argv.append("--dry-run")
    if args.allow_legacy_script_authorship:
        argv.append("--allow-legacy-script-authorship")

    old_argv = sys.argv
    try:
        sys.argv = argv
        build_status = build_main()
    finally:
        sys.argv = old_argv

    if build_status != 0 or args.dry_run:
        return build_status
    if args.skip_auto_image:
        mark_auto_image_skipped(output_dir)
        return 0
    return run_auto_images(
        output_dir,
        project_name=project_root.name,
        global_style_path=global_style_path,
        dry_run=args.auto_image_dry_run,
    )


if __name__ == "__main__":
    raise SystemExit(main())
