#!/usr/bin/env python3
"""Validate character Markdown projections against the structured v2 template."""

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
    "identity_story_pressure_heading": r"^## Identity & Story Pressure ##$",
    "visual_drivers_heading": r"^## Visual Drivers ##$",
    "detailed_character_design_heading": r"^## Detailed Character Design ##$",
    "face_heading": r"^### Face$",
    "hair_heading": r"^### Hair$",
    "body_heading": r"^### Body$",
    "personality_heading": r"^### Personality$",
    "detailed_costume_design_heading": r"^## Detailed Costume Design ##$",
    "cinematography_heading": r"^## Cinematography ##$",
    "prompt_heading": r"^\*\*prompt整合\*\*$",
    "global_style_prefix": r"^Global style prefix:\s*\S",
    "integrated_prompt": r"^Integrated prompt:\s*\S",
}

FORBIDDEN_MARKDOWN_PATTERNS = {
    "legacy_full_generation_prompt_block": r"^\*\*full_generation_prompt\*\*$",
    "simplified_role_id_bullet": r"^- role_id:\s*",
    "simplified_costume_bullet": r"^- costume:\s*",
}

REQUIRED_ROLE_FIELDS = (
    "role_id",
    "role_name",
    "role_tier",
    "costume_state",
    "story_premise",
    "identity_hook",
    "narrative_tension",
    "style_backbone",
    "character_style",
    "design_guardrails",
    "structured_fields",
    "prompt_integration",
    "global_style_prefix_en",
    "full_generation_prompt",
    "source_trace",
)

REQUIRED_STRUCTURED_GROUPS = ("face", "hair", "body", "costume", "camera")
NON_ASCII_RE = re.compile(r"[^\x00-\x7F]")
INTEGRATED_PROMPT_MIN_BYTES = 1800
INTEGRATED_PROMPT_MAX_BYTES = 2200
REQUIRED_REFERENCE_GUARDRAILS = ("solid color background", "no scene background elements")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="校验角色 Markdown projection 是否绑定 structured v2 模板。")
    parser.add_argument("--output-dir", required=True, help="角色设计输出目录")
    parser.add_argument("--design-json", help="character_design.json 路径；默认 output-dir/character_design.json")
    parser.add_argument("--manifest", help="_manifest.json 路径；存在时同步写入 template_validation 状态")
    parser.add_argument("--no-manifest-update", action="store_true", help="只校验，不回写 manifest")
    return parser.parse_args()


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def integrated_prompt_lines(text: str) -> list[str]:
    return [line for line in text.splitlines() if line.startswith("Integrated prompt:")]


def integrated_prompt_byte_errors(path_label: str, prompt: str) -> list[str]:
    errors: list[str] = []
    if NON_ASCII_RE.search(prompt):
        errors.append(f"{path_label}: integrated prompt contains non-ASCII text")
    byte_length = len(prompt.encode("utf-8"))
    if byte_length < INTEGRATED_PROMPT_MIN_BYTES:
        errors.append(
            f"{path_label}: integrated prompt too short "
            f"({byte_length} bytes, expected {INTEGRATED_PROMPT_MIN_BYTES}-{INTEGRATED_PROMPT_MAX_BYTES})"
        )
    if byte_length > INTEGRATED_PROMPT_MAX_BYTES:
        errors.append(
            f"{path_label}: integrated prompt too long "
            f"({byte_length} bytes, expected {INTEGRATED_PROMPT_MIN_BYTES}-{INTEGRATED_PROMPT_MAX_BYTES})"
        )
    lower_prompt = prompt.lower()
    for phrase in REQUIRED_REFERENCE_GUARDRAILS:
        if phrase not in lower_prompt:
            errors.append(f"{path_label}: integrated prompt missing character reference guardrail `{phrase}`")
    return errors


def validate_markdown(path: Path) -> list[str]:
    text = path.read_text(encoding="utf-8")
    errors: list[str] = []
    for label, pattern in REQUIRED_MARKDOWN_PATTERNS.items():
        if not re.search(pattern, text, re.MULTILINE):
            errors.append(f"{path.name}: missing {label}")
    for label, pattern in FORBIDDEN_MARKDOWN_PATTERNS.items():
        if re.search(pattern, text, re.MULTILINE):
            errors.append(f"{path.name}: forbidden {label}")
    for line in integrated_prompt_lines(text):
        prompt = line.split(":", 1)[1].strip()
        errors.extend(integrated_prompt_byte_errors(path.name, prompt))
    return errors


def has_structured_group(structured: dict[str, Any], group: str) -> bool:
    value = structured.get(group)
    if isinstance(value, dict) and value:
        return True
    prefix = f"{group}_"
    return any(key.startswith(prefix) and value for key, value in structured.items())


def validate_design_json(design_path: Path) -> list[str]:
    if not design_path.exists():
        return [f"design json missing: {design_path}"]
    payload = read_json(design_path)
    roles = payload.get("roles", [])
    errors: list[str] = []
    if not isinstance(roles, list) or not roles:
        errors.append("character_design.json has no roles[]")
        return errors

    for role in roles:
        role_name = role.get("role_name") or role.get("canonical_name") or "<unknown>"
        for field in REQUIRED_ROLE_FIELDS:
            if field not in role or role.get(field) in ("", None, [], {}):
                errors.append(f"{role_name}: missing or empty {field}")
        structured = role.get("structured_fields")
        if not isinstance(structured, dict) or not structured:
            errors.append(f"{role_name}: structured_fields missing")
            continue
        for group in REQUIRED_STRUCTURED_GROUPS:
            if not has_structured_group(structured, group):
                errors.append(f"{role_name}: structured_fields missing {group} group")
        full_prompt = str(role.get("full_generation_prompt", ""))
        if "Global style prefix:" not in full_prompt or "Integrated prompt:" not in full_prompt:
            errors.append(f"{role_name}: full_generation_prompt missing required labels")
        prompt_integration = str(role.get("prompt_integration", ""))
        errors.extend(integrated_prompt_byte_errors(role_name, prompt_integration))
    return errors


def main() -> int:
    args = parse_args()
    output_dir = Path(args.output_dir)
    design_path = Path(args.design_json) if args.design_json else output_dir / "character_design.json"
    manifest_path = Path(args.manifest) if args.manifest else output_dir / "_manifest.json"

    markdown_files = sorted(path for path in output_dir.glob("*.md") if path.is_file())
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
    print(f"[OK] validated {len(markdown_files)} character Markdown files against structured v2 template")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
