#!/usr/bin/env python3
"""Validate F1 subtitle style JSON before hard-subtitle rendering."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path


ASS_COLOR_RE = re.compile(r"^&H[0-9A-Fa-f]{8}$")


def validate(path: Path) -> dict:
    data = json.loads(path.read_text(encoding="utf-8"))
    errors: list[str] = []

    def require_number(name: str, minimum: float, maximum: float) -> None:
        value = data.get(name)
        if not isinstance(value, (int, float)):
            errors.append(f"{name}: missing or not numeric")
        elif not minimum <= float(value) <= maximum:
            errors.append(f"{name}: {value} outside {minimum}-{maximum}")

    if not str(data.get("font_name", "")).strip():
        errors.append("font_name: missing")
    require_number("font_size", 6, 96)
    require_number("outline", 0, 10)
    require_number("shadow", 0, 10)
    require_number("margin_l", 0, 400)
    require_number("margin_r", 0, 400)
    require_number("margin_v", 0, 400)
    require_number("max_chars_per_line", 4, 60)
    require_number("max_lines", 1, 4)

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

    return {
        "path": str(path),
        "ok": not errors,
        "errors": errors,
    }


def main(argv: list[str]) -> int:
    if len(argv) != 2:
        print("usage: validate_subtitle_style.py <subtitle_style.json>", file=sys.stderr)
        return 2
    report = validate(Path(argv[1]))
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0 if report["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
