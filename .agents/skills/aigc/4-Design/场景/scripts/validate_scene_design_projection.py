#!/usr/bin/env python3
"""Validate scene Markdown cards against the structured v2 scene template."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any


REQUIRED_MARKDOWN_PATTERNS = {
    "story_heading": r"^\*\*物语\*\*$",
    "deconstruction_heading": r"^\*\*解构\*\*$",
    "reasoning_pivot": r"^Reasoning Pivot:\s*\S",
    "scene_design_heading": r"^## Scene Design ##$",
    "cinematography_heading": r"^## Cinematography ##$",
    "prompt_heading": r"^\*\*prompt整合\*\*$",
    "global_style_prefix": r"^Global style prefix:\s*\S",
    "integrated_prompt": r"^Integrated prompt:\s*\S",
}

FORBIDDEN_PATTERNS = {
    "legacy_full_generation_prompt_block": r"^\*\*full_generation_prompt\*\*$",
    "simplified_scene_id_bullet": r"^- scene_id:\s*",
}
CJK_RE = re.compile(r"[\u4e00-\u9fff]")
NON_ASCII_RE = re.compile(r"[^\x00-\x7F]")
INTEGRATED_PROMPT_MIN_BYTES = 1800
INTEGRATED_PROMPT_MAX_BYTES = 2200
REQUIRED_REFERENCE_GUARDRAILS = ("empty environmental shot", "no characters")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="校验场景 Markdown projection 是否绑定 structured v2 模板。")
    parser.add_argument("--output-dir", required=True, help="场景设计输出目录")
    parser.add_argument("--design-json", help="scene_design.json 路径；默认 output-dir/scene_design.json")
    parser.add_argument("--manifest", help="_manifest.json 路径；存在时同步写入 template_validation 状态")
    parser.add_argument("--no-manifest-update", action="store_true", help="只校验，不回写 manifest")
    return parser.parse_args()


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def integrated_prompt_byte_errors(path_label: str, prompt: str) -> list[str]:
    errors: list[str] = []
    if NON_ASCII_RE.search(prompt):
        errors.append(f"{path_label}: Integrated prompt contains non-ASCII text")
    byte_length = len(prompt.encode("utf-8"))
    if byte_length < INTEGRATED_PROMPT_MIN_BYTES:
        errors.append(
            f"{path_label}: Integrated prompt too short "
            f"({byte_length} bytes, expected {INTEGRATED_PROMPT_MIN_BYTES}-{INTEGRATED_PROMPT_MAX_BYTES})"
        )
    if byte_length > INTEGRATED_PROMPT_MAX_BYTES:
        errors.append(
            f"{path_label}: Integrated prompt too long "
            f"({byte_length} bytes, expected {INTEGRATED_PROMPT_MIN_BYTES}-{INTEGRATED_PROMPT_MAX_BYTES})"
        )
    lower_prompt = prompt.lower()
    for phrase in REQUIRED_REFERENCE_GUARDRAILS:
        if phrase not in lower_prompt:
            errors.append(f"{path_label}: Integrated prompt missing scene reference guardrail `{phrase}`")
    return errors


def validate_markdown(path: Path) -> list[str]:
    text = path.read_text(encoding="utf-8")
    errors: list[str] = []
    for label, pattern in REQUIRED_MARKDOWN_PATTERNS.items():
        if not re.search(pattern, text, re.MULTILINE):
            errors.append(f"{path.name}: missing {label}")
    for label, pattern in FORBIDDEN_PATTERNS.items():
        if re.search(pattern, text, re.MULTILINE):
            errors.append(f"{path.name}: forbidden {label}")
    integrated_match = re.search(r"^Integrated prompt:\s*(?P<prompt>.+)\Z", text, re.MULTILINE | re.DOTALL)
    if integrated_match:
        errors.extend(integrated_prompt_byte_errors(path.name, integrated_match.group("prompt").strip()))
    return errors


def validate_design_json(design_path: Path) -> list[str]:
    if not design_path.exists():
        return [f"design json missing: {design_path}"]
    payload = read_json(design_path)
    scenes = payload.get("scenes", [])
    errors: list[str] = []
    if not scenes:
        errors.append("scene_design.json has no scenes[]")
        return errors
    for scene in scenes:
        scene_name = scene.get("scene_name", "<unknown>")
        structured = scene.get("structured_fields") or {}
        for key in ("scene_design", "cinematography"):
            if not isinstance(structured.get(key), dict) or not structured[key]:
                errors.append(f"{scene_name}: structured_fields.{key} missing")
        if scene.get("design_prompt") != scene.get("prompt"):
            errors.append(f"{scene_name}: design_prompt != prompt")
        full_prompt = str(scene.get("full_generation_prompt", ""))
        if "Global style prefix:" not in full_prompt or "Integrated prompt:" not in full_prompt:
            errors.append(f"{scene_name}: full_generation_prompt missing required labels")
        if CJK_RE.search(str(scene.get("prompt_integration", ""))):
            errors.append(f"{scene_name}: prompt_integration contains Chinese characters")
        errors.extend(integrated_prompt_byte_errors(scene_name, str(scene.get("prompt_integration", ""))))
        if not scene.get("reasoning_pivot"):
            errors.append(f"{scene_name}: reasoning_pivot missing")
    return errors


def main() -> int:
    args = parse_args()
    output_dir = Path(args.output_dir)
    design_path = Path(args.design_json) if args.design_json else output_dir / "scene_design.json"
    manifest_path = Path(args.manifest) if args.manifest else output_dir / "_manifest.json"
    markdown_files = sorted(output_dir.glob("*.md"))
    errors: list[str] = []
    if not markdown_files:
        errors.append(f"no markdown files found: {output_dir}")
    for markdown_path in markdown_files:
        errors.extend(validate_markdown(markdown_path))
    errors.extend(validate_design_json(design_path))

    if manifest_path.exists() and not args.no_manifest_update:
        manifest = read_json(manifest_path)
        manifest["template_validation"] = {
            "status": "failed" if errors else "success",
            "checked_markdown_count": len(markdown_files),
            "design_json": design_path.as_posix(),
            "errors": errors,
        }
        write_json(manifest_path, manifest)

    if errors:
        for error in errors:
            print(f"[ERROR] {error}", file=sys.stderr)
        return 1
    print(f"[OK] validated {len(markdown_files)} scene Markdown files against structured v2 template")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
