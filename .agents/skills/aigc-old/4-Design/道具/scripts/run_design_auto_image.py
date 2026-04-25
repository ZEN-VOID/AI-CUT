#!/usr/bin/env python3
"""Prepare one built-in imagegen request for a 4-Design domain subject file."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any


def find_repo_root() -> Path:
    current = Path(__file__).resolve()
    for parent in current.parents:
        if (parent / ".agents").exists() and (parent / "AGENTS.md").exists():
            return parent
    return Path.cwd()


REPO_ROOT = find_repo_root()
SCRIPT_DIR = Path(__file__).resolve().parent
if SCRIPT_DIR.as_posix() not in sys.path:
    sys.path.insert(0, SCRIPT_DIR.as_posix())

from global_style_prefix import extract_global_style_prefix_from_path  # noqa: E402


def caller_skill_path() -> str:
    try:
        return (SCRIPT_DIR.parent).resolve().relative_to(REPO_ROOT.resolve()).as_posix()
    except ValueError:
        return ".agents/skills/aigc/4-Design"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="从单个主体设计文件准备内置 imagegen 请求侧车，prompt 自动加载全局风格前缀。"
    )
    parser.add_argument("--design-file", required=True, help="单一主体 Markdown 设计文件路径")
    parser.add_argument("--prompt", help="已包含全局风格前缀的完整 prompt；传入后不再从 Markdown 提取")
    parser.add_argument("--global-style", help="全局风格.md；默认按项目根自动推断")
    parser.add_argument("--project-name", help="项目名；默认按 projects/aigc/<项目名> 自动推断")
    parser.add_argument("--aspect-ratio", default="16:9", help="期望画幅；内置 imagegen 提示词和侧车记录使用")
    parser.add_argument("--image-size", default="auto", help="期望清晰度/尺寸；内置 imagegen 提示词和侧车记录使用")
    parser.add_argument("--max-concurrent", type=int, default=1, help="兼容旧参数；内置 imagegen 逐资产调用，不做脚本并发")
    parser.add_argument("--foreground", action="store_true", help="兼容旧参数；内置 imagegen 由 Codex 会话前台执行")
    parser.add_argument("--write-report", action="store_true", help="兼容旧参数；本 helper 始终写 request sidecar")
    parser.add_argument("--dry-run", action="store_true", help="只打印侧车摘要；不代表已经调用内置 imagegen")
    parser.add_argument(
        "--timeout",
        type=int,
        default=300,
        help="兼容旧参数；内置 imagegen 不由本脚本调用，因此不会在本脚本中等待 provider",
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
    """Build the built-in imagegen request sidecar for one design file."""
    return {
        "prompt": prompt,
        "project_name": project_name,
        "task_kind": "project",
        "request_id": f"design-auto-image-{design_file.stem}",
        "provider_skill": "imagegen",
        "provider_mode": "built-in image_gen",
        "default_model": "GPT-IMAGE-2",
        "caller_skill": caller_skill_path(),
        "aspect_ratio": aspect_ratio,
        "image_size": image_size,
        "output_dir": design_file.parent.as_posix(),
        "output_filename": f"{design_file.stem}.png",
        "save_policy": "Generate with built-in image_gen, then copy the selected output from $CODEX_HOME/generated_images into output_dir/output_filename. Leave the original generated image in place.",
    }


def write_request_sidecar(design_file: Path, request_doc: dict[str, Any]) -> Path:
    request_dir = design_file.parent / "generated" / "requests"
    request_dir.mkdir(parents=True, exist_ok=True)
    request_path = request_dir / f"{design_file.stem}-auto-image-request.json"
    request_path.write_text(json.dumps(request_doc, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return request_path


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
    summary = {
        "design_file": design_file.as_posix(),
        "project_name": project_name,
        "global_style": global_style_path.as_posix() if global_style_path else None,
        "request_path": request_path.as_posix(),
        "output_dir": request_doc["output_dir"],
        "output_stem": design_file.stem,
        "requested_output_filename": request_doc["output_filename"],
        "provider_skill": "imagegen",
        "provider_mode": "built-in image_gen",
        "default_model": "GPT-IMAGE-2",
        "execution_mode": "codex-builtin-imagegen",
        "status": "request_ready",
        "next_step": "Call the built-in image_gen tool with this prompt, then copy the selected generated image into output_dir/output_filename.",
        "dry_run": args.dry_run,
        "timeout_seconds": args.timeout,
        "returncode": 0,
    }
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
