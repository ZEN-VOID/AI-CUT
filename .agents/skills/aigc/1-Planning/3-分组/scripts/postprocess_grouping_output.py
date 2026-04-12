#!/usr/bin/env python3
"""Postprocess grouped-script outputs for `1-Planning/3-分组`.

Current contract:
1) no machine sidecar generation,
2) no agents-plan initialization,
3) validator + quantizer are the default exit gate.
"""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
VALIDATOR = SCRIPT_DIR / "validate_grouping_output.py"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="校验 3-分组 grouped script 输出，并通过 quantizer/validator 执行量化门槛。")
    parser.add_argument("--input", required=True, help="输入文件或目录（第N集.md 或 3-分组 目录）")
    parser.add_argument("--include-pattern", default="第*集.md", help="目录模式匹配（默认: 第*集.md）")
    parser.add_argument("--dry-run", action="store_true", help="仅打印即将校验的文件，不执行 validator")
    return parser.parse_args()


def collect_files(input_path: Path, include_pattern: str) -> list[Path]:
    if not input_path.exists():
        raise FileNotFoundError(f"输入路径不存在: {input_path}")
    if input_path.is_file():
        return [input_path]
    files = sorted(path for path in input_path.glob(include_pattern) if path.is_file())
    if files:
        return files
    return sorted(path for path in input_path.glob("*.md") if path.is_file())


def main() -> int:
    args = parse_args()
    try:
        files = collect_files(Path(args.input), args.include_pattern)
    except Exception as exc:  # noqa: BLE001
        print(str(exc), file=sys.stderr)
        return 1

    if not files:
        print("未找到可处理的 markdown 文件。", file=sys.stderr)
        return 1

    for path in files:
        print(f"准备校验 grouped script: {path}")

    if args.dry_run:
        return 0

    command = [sys.executable, str(VALIDATOR), "--input", args.input, "--include-pattern", args.include_pattern]
    result = subprocess.run(command, check=False)
    return result.returncode


if __name__ == "__main__":
    raise SystemExit(main())
