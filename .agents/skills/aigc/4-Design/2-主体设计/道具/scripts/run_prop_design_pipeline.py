#!/usr/bin/env python3
"""Run the prop design pipeline for 4-Design/道具/2-设计."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from build_prop_design_packets import main as build_main


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="运行 4-Design/道具/2-设计 pipeline。")
    parser.add_argument("--bridge", required=True, help="prop_design_bridge.json 路径")
    parser.add_argument("--research", required=True, help="道具研究.json 路径")
    parser.add_argument("--detail", required=True, help="3-Detail/第N集.json 路径")
    parser.add_argument("--catalog", help="道具清单.json 路径")
    parser.add_argument("--global-style", help="全局风格.md 路径")
    parser.add_argument(
        "--type-elements",
        dest="type_elements",
        metavar="TYPE_ELEMENTS",
        help="类型元素.md 路径",
    )
    parser.add_argument("--type-guide", dest="type_elements", help=argparse.SUPPRESS)
    parser.add_argument("--north-star", help="north_star.yaml 路径")
    parser.add_argument("--init-handoff", help="init_handoff.yaml 路径")
    parser.add_argument("--output-dir", help="输出目录；默认推断到 `projects/aigc/<项目名>/4-Design/道具/2-设计/第N集/`")
    parser.add_argument("--dry-run", action="store_true", help="只预览 manifest，不写文件")
    return parser.parse_args()


def normalize_output_dir(raw: Path) -> Path:
    text = raw.as_posix().replace("/角色/4-道具", "/道具/2-设计")
    text = text.replace("/2-角色/4-道具", "/道具/2-设计")
    return Path(text)


def infer_output_dir(bridge_path: Path) -> Path:
    try:
        episode_dir = bridge_path.parent
        design_root = episode_dir.parent.parent / "2-设计" / episode_dir.name
        return normalize_output_dir(design_root)
    except Exception as exc:  # noqa: BLE001
        raise ValueError(f"无法从 bridge 路径推断输出目录: {bridge_path}") from exc


def main() -> int:
    args = parse_args()
    bridge_path = Path(args.bridge)
    if not bridge_path.exists():
        print(f"[ERROR] bridge 不存在: {bridge_path}", file=sys.stderr)
        return 1

    output_dir = normalize_output_dir(Path(args.output_dir)) if args.output_dir else infer_output_dir(bridge_path)

    argv = [
        "build_prop_design_packets.py",
        "--bridge",
        args.bridge,
        "--research",
        args.research,
        "--detail",
        args.detail,
        "--output-dir",
        output_dir.as_posix(),
    ]
    for flag, value in (
        ("--catalog", args.catalog),
        ("--global-style", args.global_style),
        ("--type-elements", args.type_elements),
        ("--north-star", args.north_star),
        ("--init-handoff", args.init_handoff),
    ):
        if value:
            argv.extend([flag, value])
    if args.dry_run:
        argv.append("--dry-run")

    old_argv = sys.argv
    try:
        sys.argv = argv
        return build_main()
    finally:
        sys.argv = old_argv


if __name__ == "__main__":
    raise SystemExit(main())
