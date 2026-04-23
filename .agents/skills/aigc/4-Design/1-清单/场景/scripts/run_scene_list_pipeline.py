#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Run the scene list triad pipeline for 4-Design/场景/1-清单."""

from __future__ import annotations

import argparse
import json
import shlex
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import List, Optional


SCRIPT_DIR = Path(__file__).resolve().parent
EXTRACT_SCRIPT = SCRIPT_DIR / "extract_episode_scenes.py"
CONTEXT_SCRIPT = SCRIPT_DIR / "build_scene_design_context.py"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="从 `projects/aigc/<项目名>/3-Detail/第N集.json` 生成场景三真源。"
    )
    parser.add_argument("--input", required=True, help="输入 episode JSON")
    parser.add_argument("--output-dir", help="输出目录；默认推断到 `projects/aigc/<项目名>/4-Design/场景/1-清单/第N集/`")
    parser.add_argument("--catalog-name", default="场景清单.json", help="场景清单文件名")
    parser.add_argument("--research-name", default="场景研究.json", help="场景研究文件名")
    parser.add_argument("--bridge-name", default="scene_design_bridge.json", help="场景桥接文件名")
    parser.add_argument("--manifest-name", default="_manifest.json", help="manifest 文件名")
    parser.add_argument("--dry-run", action="store_true", help="仅校验链路，不保留输出文件")
    parser.add_argument(
        "--allow-legacy-script-authorship",
        action="store_true",
        help="受控兼容模式：允许旧式脚本直接生成研究结论与桥接文案。",
    )
    return parser.parse_args()


def resolve_input_path(raw_input: str) -> Path:
    candidate = Path(raw_input)
    if candidate.exists():
        return candidate

    path_str = candidate.as_posix()
    if "/3-Detail/" in path_str:
        fallback = Path(path_str.replace("/3-Detail/", "/编导/"))
        if fallback.exists():
            return fallback
    if "/编导/" in path_str:
        fallback = Path(path_str.replace("/编导/", "/3-Detail/"))
        if fallback.exists():
            return fallback
    return candidate


def resolve_output_dir(input_path: Path, explicit: Optional[str]) -> Path:
    if explicit:
        return Path(explicit)

    parts = input_path.parts
    try:
        projects_index = parts.index("projects")
        if projects_index + 2 < len(parts) and parts[projects_index + 1] == "aigc":
            project_root = Path(*parts[: projects_index + 3])
        else:
            project_root = Path(*parts[: projects_index + 2])
        return project_root / "4-Design" / "场景" / "1-清单" / input_path.stem
    except ValueError:
        pass

    return input_path.parent / "4-Design-场景-1-清单" / input_path.stem


def run_cmd(cmd: List[str]) -> None:
    print("$ " + " ".join(shlex.quote(part) for part in cmd))
    subprocess.run(cmd, check=True)


def read_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def write_manifest(args: argparse.Namespace, input_path: Path, output_dir: Path) -> Path:
    catalog = read_json(output_dir / args.catalog_name)
    meta = catalog.get("meta", {})
    manifest = {
        "status": "ok",
        "episode_id": meta.get("episode_id") or input_path.stem,
        "input_file": input_path.as_posix(),
        "output_dir": output_dir.as_posix(),
        "output_files": [
            (output_dir / args.catalog_name).as_posix(),
            (output_dir / args.research_name).as_posix(),
            (output_dir / args.bridge_name).as_posix(),
            (output_dir / args.manifest_name).as_posix(),
        ],
        "statistics": catalog.get("statistics", {}),
        "notes": [
            "业务三真源为 `场景清单.json + 场景研究.json + scene_design_bridge.json`；`_manifest.json` 仅为审计侧车。",
        ],
    }
    manifest_path = output_dir / args.manifest_name
    manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return manifest_path


def build_extract_cmd(args: argparse.Namespace, input_path: Path, output_dir: Path) -> List[str]:
    return [
        sys.executable,
        str(EXTRACT_SCRIPT),
        "--input",
        input_path.as_posix(),
        "--output-dir",
        output_dir.as_posix(),
        "--json-name",
        args.catalog_name,
    ]


def build_context_cmd(args: argparse.Namespace, output_dir: Path, dry_run: bool) -> List[str]:
    cmd = [
        sys.executable,
        str(CONTEXT_SCRIPT),
        "--input",
        (output_dir / args.catalog_name).as_posix(),
        "--output-dir",
        output_dir.as_posix(),
        "--catalog-name",
        args.catalog_name,
        "--research-name",
        args.research_name,
        "--bridge-name",
        args.bridge_name,
    ]
    if dry_run:
        cmd.append("--dry-run")
    if args.allow_legacy_script_authorship:
        cmd.append("--allow-legacy-script-authorship")
    return cmd


def run_dry_run(args: argparse.Namespace, input_path: Path) -> int:
    with tempfile.TemporaryDirectory(prefix="aigc-scene-list-") as tmp_dir_str:
        tmp_dir = Path(tmp_dir_str)
        run_cmd(build_extract_cmd(args=args, input_path=input_path, output_dir=tmp_dir))
        run_cmd(build_context_cmd(args=args, output_dir=tmp_dir, dry_run=True))
    print("[DRY-RUN] 场景清单链路校验完成。")
    return 0


def run_normal(args: argparse.Namespace, input_path: Path) -> int:
    output_dir = resolve_output_dir(input_path=input_path, explicit=args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    run_cmd(build_extract_cmd(args=args, input_path=input_path, output_dir=output_dir))
    run_cmd(build_context_cmd(args=args, output_dir=output_dir, dry_run=False))
    manifest_path = write_manifest(args=args, input_path=input_path, output_dir=output_dir)

    print(f"输出目录: {output_dir.as_posix()}")
    print(f"- 场景清单: {(output_dir / args.catalog_name).as_posix()}")
    print(f"- 场景研究: {(output_dir / args.research_name).as_posix()}")
    print(f"- 场景桥接: {(output_dir / args.bridge_name).as_posix()}")
    print(f"- 审计侧车: {manifest_path.as_posix()}")
    return 0


def main() -> int:
    args = parse_args()
    missing = [path.as_posix() for path in (EXTRACT_SCRIPT, CONTEXT_SCRIPT) if not path.exists()]
    if missing:
        print(f"[ERROR] 缺少依赖脚本: {', '.join(missing)}", file=sys.stderr)
        return 1

    input_path = resolve_input_path(args.input)
    if not input_path.exists():
        print(f"[ERROR] 输入文件不存在: {input_path}", file=sys.stderr)
        return 1

    try:
        if args.dry_run:
            return run_dry_run(args=args, input_path=input_path)
        return run_normal(args=args, input_path=input_path)
    except subprocess.CalledProcessError as exc:
        return exc.returncode
    except Exception as exc:  # noqa: BLE001
        print(f"[ERROR] {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
