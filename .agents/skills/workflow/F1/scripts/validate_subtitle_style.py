#!/usr/bin/env python3
"""Validate F1 subtitle style JSON before hard-subtitle rendering."""

from __future__ import annotations

import json
import re
import sys
import argparse
from pathlib import Path


ASS_COLOR_RE = re.compile(r"^&H[0-9A-Fa-f]{8}$")
ALLOWED_LINE_BREAK_POLICIES = {"single-line", "no-explicit-breaks"}
ALLOWED_FONT_SIZE_SCOPES = {"global", "whole_video", "global_fixed"}


def _format_number(value: float) -> str:
    if float(value).is_integer():
        return str(int(value))
    return str(value)


def _read_render_command(path: Path | None) -> str | None:
    if path is None:
        return None
    return path.read_text(encoding="utf-8")


def validate(
    path: Path,
    *,
    expected_font_size: float | None = None,
    render_command: Path | None = None,
    require_render_font_size: bool = False,
) -> dict:
    data = json.loads(path.read_text(encoding="utf-8"))
    errors: list[str] = []
    render_command_text = _read_render_command(render_command)

    def require_number(name: str, minimum: float, maximum: float) -> None:
        value = data.get(name)
        if not isinstance(value, (int, float)):
            errors.append(f"{name}: missing or not numeric")
        elif not minimum <= float(value) <= maximum:
            errors.append(f"{name}: {value} outside {minimum}-{maximum}")

    if not str(data.get("font_name", "")).strip():
        errors.append("font_name: missing")
    require_number("font_size", 6, 96)
    font_size = data.get("font_size")
    if expected_font_size is not None and isinstance(font_size, (int, float)):
        if float(font_size) != float(expected_font_size):
            errors.append(
                f"font_size: expected {_format_number(expected_font_size)} but got {_format_number(float(font_size))}"
            )
    if data.get("font_size_lock") is not True:
        errors.append("font_size_lock: must be true for F1 fixed-size subtitles")
    if data.get("font_size_scope") not in ALLOWED_FONT_SIZE_SCOPES:
        errors.append("font_size_scope: must be global, whole_video, or global_fixed")
    if data.get("auto_shrink") not in (None, False):
        errors.append("auto_shrink: must be false; split long dialogue into single-line cues instead")
    for name in ("font_size_overrides", "per_cue_font_size", "cue_font_sizes"):
        value = data.get(name)
        if value not in (None, {}, [], ""):
            errors.append(f"{name}: per-cue font-size overrides are not allowed")
    require_number("outline", 0, 10)
    require_number("shadow", 0, 10)
    require_number("margin_l", 0, 400)
    require_number("margin_r", 0, 400)
    require_number("margin_v", 0, 400)
    require_number("max_chars_per_line", 4, 60)
    require_number("max_lines", 1, 4)
    max_lines = data.get("max_lines")
    if isinstance(max_lines, (int, float)) and int(max_lines) != 1:
        errors.append("max_lines: must be 1 for F1 single-line subtitles")

    line_break_policy = data.get("line_break_policy")
    if line_break_policy not in ALLOWED_LINE_BREAK_POLICIES:
        errors.append("line_break_policy: must be single-line or no-explicit-breaks")

    alignment = data.get("alignment")
    if alignment is not None and alignment not in list(range(1, 10)):
        errors.append("alignment: must be 1-9")

    border_style = data.get("border_style")
    if border_style is not None and border_style not in (1, 3):
        errors.append("border_style: must be 1 or 3")

    for name in ("primary_color", "outline_color", "back_color"):
        value = data.get(name)
        if value is not None and not (isinstance(value, str) and ASS_COLOR_RE.match(value)):
            errors.append(f"{name}: must match &HAABBGGRR")

    if data.get("preview_required") is not None and not isinstance(data.get("preview_required"), bool):
        errors.append("preview_required: must be boolean")

    if require_render_font_size:
        if render_command_text is None:
            errors.append("render_command: required when --require-render-font-size is set")
        elif isinstance(font_size, (int, float)):
            expected = float(expected_font_size) if expected_font_size is not None else float(font_size)
            matches = re.findall(r"(?<![A-Za-z])Fontsize\s*=\s*([0-9]+(?:\.[0-9]+)?)", render_command_text)
            if not matches:
                errors.append("render_command: missing subtitle Fontsize projection")
            else:
                mismatches = [value for value in matches if float(value) != expected]
                if mismatches:
                    errors.append(
                        "render_command: subtitle Fontsize mismatch; "
                        f"expected {_format_number(expected)}, found {', '.join(mismatches)}"
                    )

    return {
        "path": str(path),
        "render_command": str(render_command) if render_command else None,
        "expected_font_size": expected_font_size,
        "render_font_size_required": require_render_font_size,
        "ok": not errors,
        "errors": errors,
    }


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("style", type=Path)
    parser.add_argument("--expected-font-size", type=float)
    parser.add_argument("--render-command", type=Path)
    parser.add_argument("--require-render-font-size", action="store_true")
    args = parser.parse_args(argv[1:])
    report = validate(
        args.style,
        expected_font_size=args.expected_font_size,
        render_command=args.render_command,
        require_render_font_size=args.require_render_font_size,
    )
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0 if report["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
