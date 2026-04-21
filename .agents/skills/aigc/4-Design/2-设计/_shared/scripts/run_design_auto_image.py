#!/usr/bin/env python3
"""Generate one same-name image for a 4-Design/2-设计 subject file."""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from datetime import datetime
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[7]
NANO_SCRIPT = REPO_ROOT / ".agents/skills/api/anyfast/image/nano-banana/scripts/nano_banana_generate.py"
SCRIPT_DIR = Path(__file__).resolve().parent
if SCRIPT_DIR.as_posix() not in sys.path:
    sys.path.insert(0, SCRIPT_DIR.as_posix())

from global_style_prefix import extract_global_style_prefix_from_path  # noqa: E402


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="从单个主体设计文件生成同目录同名图片，prompt 自动加载全局风格前缀。"
    )
    parser.add_argument("--design-file", required=True, help="单一主体 Markdown 设计文件路径")
    parser.add_argument("--prompt", help="已包含全局风格前缀的完整 prompt；传入后不再从 Markdown 提取")
    parser.add_argument("--global-style", help="全局风格.md；默认按项目根自动推断")
    parser.add_argument("--project-name", help="项目名；默认按 projects/aigc/<项目名> 自动推断")
    parser.add_argument("--aspect-ratio", default="16:9", help="传给 nano-banana 的宽高比")
    parser.add_argument("--image-size", default="4K", help="传给 nano-banana 的清晰度")
    parser.add_argument("--max-concurrent", type=int, default=100, help="批量并发上限；后台模式透传给 nano-banana")
    parser.add_argument("--foreground", action="store_true", help="前台等待 nano-banana 完成；默认后台提交")
    parser.add_argument("--write-report", action="store_true", help="保留 nano-banana report JSON")
    parser.add_argument("--dry-run", action="store_true", help="只打印 payload，不调用 API")
    parser.add_argument(
        "--timeout",
        type=int,
        default=300,
        help="nano-banana 子进程最长等待秒数；超时返回 124，避免批量 pipeline 无限挂起",
    )
    return parser.parse_args()


def infer_project_root(design_file: Path) -> Path | None:
    for parent in design_file.resolve().parents:
        if parent.name == "4-Design":
            return parent.parent
    return None


def extract_prompt_section(markdown_text: str) -> str:
    patterns = [
        r"\*\*prompt整合\*\*\s*(.*)",
        r"^#+\s*prompt整合\s*(.*)",
        r"prompt整合[:：]?\s*(.*)",
    ]
    for pattern in patterns:
        match = re.search(pattern, markdown_text, flags=re.S | re.M | re.I)
        if not match:
            continue
        prompt = match.group(1).strip()
        prompt = re.split(r"\n\s*(?:```|#{1,6}\s+|\*\*物语\*\*|\*\*解构\*\*)", prompt, maxsplit=1)[0].strip()
        prompt = re.sub(r"\s+", " ", prompt)
        if prompt:
            return prompt
    raise ValueError("无法从设计文件提取 `prompt整合` 区块，请传入 --prompt 或修复设计文件。")


def prompt_has_global_style(prompt: str) -> bool:
    return bool(
        re.search(
            r"(?:Global Style Prefix|Global style prefix|global_style_prefix|全局风格前缀|Full Generation Prompt)[:：]",
            prompt,
            flags=re.I,
        )
    )


def translate_global_style_prefix(prefix: str) -> str:
    source = prefix.strip()
    if "近未来社区生活喜剧影视质感" in source and "轻量全息奇观" in source:
        return (
            "A near-future community-life comedy with cinematic realism, orderly lived-in spaces, "
            "soft atmospheric depth, gentle absurdist rhythm, and lightweight holographic spectacle "
            "that always serves the characters' dignity, loneliness, and clumsy romance."
        )
    return f"Translate this project style into a grounded cinematic English visual direction: {source}"


def build_full_prompt(design_file: Path, explicit_prompt: str | None, global_style_path: Path | None) -> str:
    if explicit_prompt:
        return explicit_prompt.strip()

    prompt = extract_prompt_section(design_file.read_text(encoding="utf-8"))
    if prompt_has_global_style(prompt):
        return prompt
    if global_style_path and global_style_path.exists():
        prefix = extract_global_style_prefix_from_path(global_style_path)
        if prefix:
            return f"Global style prefix: {translate_global_style_prefix(prefix)}\n\nIntegrated prompt: {prompt}"
    return prompt


def build_request_doc(
    *,
    design_file: Path,
    project_name: str,
    prompt: str,
    aspect_ratio: str,
    image_size: str,
) -> dict[str, Any]:
    """Build the nano-banana/general structured request for one design file."""
    return {
        "prompt": prompt,
        "project_name": project_name,
        "task_kind": "project",
        "request_id": f"design-auto-image-{design_file.stem}",
        "caller_skill": ".agents/skills/aigc/4-Design/2-设计",
        "aspect_ratio": aspect_ratio,
        "image_size": image_size,
        "output_dir": design_file.parent.as_posix(),
        "output_filename": f"{design_file.stem}.png",
    }


def write_request_sidecar(design_file: Path, request_doc: dict[str, Any]) -> Path:
    request_dir = design_file.parent / "generated" / "requests"
    request_dir.mkdir(parents=True, exist_ok=True)
    request_path = request_dir / f"{design_file.stem}-auto-image-request.json"
    request_path.write_text(json.dumps(request_doc, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return request_path


def background_log_path(design_file: Path) -> Path:
    log_dir = design_file.parent / "generated" / "logs"
    log_dir.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    return log_dir / f"{design_file.stem}-auto-image-{stamp}.log"


def build_nano_command(
    *,
    request_path: Path,
    max_concurrent: int,
    timeout: int,
    write_report: bool,
    dry_run: bool,
) -> list[str]:
    cmd = [
        sys.executable,
        NANO_SCRIPT.as_posix(),
        "--input-json",
        request_path.as_posix(),
        "--max-concurrent",
        str(max_concurrent),
        "--timeout",
        str(timeout),
    ]
    if not write_report:
        cmd.append("--no-report")
    if dry_run:
        cmd.extend(["--dry-run", "--print-payload"])
    return cmd


def main() -> int:
    args = parse_args()
    design_file = Path(args.design_file)
    if not design_file.exists():
        print(f"[ERROR] design file 不存在: {design_file}", file=sys.stderr)
        return 1

    project_root = infer_project_root(design_file)
    project_name = args.project_name or (project_root.name if project_root else None) or "未命名项目"
    global_style_path = (
        Path(args.global_style)
        if args.global_style
        else (
            project_root / "2-Global" / "全局风格.md"
            if project_root and (project_root / "2-Global" / "全局风格.md").exists()
            else (
                project_root / "2-Global" / "全局风格" / "全局风格设计.md"
                if project_root
                else None
            )
        )
    )

    try:
        full_prompt = build_full_prompt(design_file, args.prompt, global_style_path)
    except ValueError as exc:
        print(f"[ERROR] {exc}", file=sys.stderr)
        return 1

    request_doc = build_request_doc(
        design_file=design_file,
        project_name=project_name,
        prompt=full_prompt,
        aspect_ratio=args.aspect_ratio,
        image_size=args.image_size,
    )
    request_path = write_request_sidecar(design_file, request_doc)
    cmd = build_nano_command(
        request_path=request_path,
        max_concurrent=args.max_concurrent,
        timeout=args.timeout,
        write_report=args.write_report,
        dry_run=args.dry_run,
    )

    if not args.foreground and not args.dry_run:
        log_path = background_log_path(design_file)
        log_file = log_path.open("ab")
        process = subprocess.Popen(
            cmd,
            cwd=REPO_ROOT,
            stdout=log_file,
            stderr=subprocess.STDOUT,
            start_new_session=True,
        )
        log_file.close()
        summary = {
            "design_file": design_file.as_posix(),
            "project_name": project_name,
            "global_style": global_style_path.as_posix() if global_style_path else None,
            "request_path": request_path.as_posix(),
            "output_dir": request_doc["output_dir"],
            "output_stem": design_file.stem,
            "requested_output_filename": request_doc["output_filename"],
            "execution_mode": "background-batch-concurrent",
            "background_pid": process.pid,
            "background_log": log_path.as_posix(),
            "max_concurrent": args.max_concurrent,
            "timeout_seconds": args.timeout,
            "returncode": 0,
        }
        print(json.dumps(summary, ensure_ascii=False, indent=2))
        return 0

    try:
        result = subprocess.run(cmd, check=False, timeout=args.timeout)
        returncode = result.returncode
    except subprocess.TimeoutExpired:
        print(
            f"[ERROR] nano-banana 自动生图超时: design_file={design_file} timeout={args.timeout}s",
            file=sys.stderr,
        )
        returncode = 124
    summary = {
        "design_file": design_file.as_posix(),
        "project_name": project_name,
        "global_style": global_style_path.as_posix() if global_style_path else None,
        "request_path": request_path.as_posix(),
        "output_dir": request_doc["output_dir"],
        "output_stem": design_file.stem,
        "requested_output_filename": request_doc["output_filename"],
        "execution_mode": "foreground-batch-concurrent" if args.foreground else "dry-run",
        "max_concurrent": args.max_concurrent,
        "dry_run": args.dry_run,
        "timeout_seconds": args.timeout,
        "returncode": returncode,
    }
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    return returncode


if __name__ == "__main__":
    raise SystemExit(main())
