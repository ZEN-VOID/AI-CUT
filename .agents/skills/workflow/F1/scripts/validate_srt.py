#!/usr/bin/env python3
"""Validate SRT structure for F1 outputs."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path


TIMING_RE = re.compile(r"^(\d\d:\d\d:\d\d,\d{3}) --> (\d\d:\d\d:\d\d,\d{3})$")
HTML_BREAK_RE = re.compile(r"<br\s*/?>", re.IGNORECASE)
ASCII_FRAGMENT_RE = re.compile(r"[A-Za-z0-9]$")
ASCII_LEADING_RE = re.compile(r"^[A-Za-z0-9]")
BOUNDARY_BAD_STARTS = ("地现在", "了现在", "桶现在", "头现在")
BOUNDARY_BAD_ENDINGS = ("而", "已", "直", "膝盖", "从头", "调试与", "提")
BOUNDARY_BAD_PAIRS = (("提", "供"),)


def parse_ts(value: str) -> float:
    h, m, rest = value.split(":")
    s, ms = rest.split(",")
    return int(h) * 3600 + int(m) * 60 + int(s) + int(ms) / 1000


def validate(path: Path, strict_boundaries: bool = False, min_warn_duration: float = 0.5) -> dict:
    text = path.read_text(encoding="utf-8").strip()
    blocks = re.split(r"\n\s*\n", text) if text else []
    previous_end = -1.0
    previous_text = ""
    max_duration = 0.0
    errors: list[str] = []
    warnings: list[str] = []
    for expected, block in enumerate(blocks, 1):
        lines = block.splitlines()
        if len(lines) < 3:
            errors.append(f"block {expected}: too few lines")
            continue
        try:
            index = int(lines[0])
        except ValueError:
            errors.append(f"block {expected}: bad index")
            continue
        if index != expected:
            errors.append(f"block {expected}: index is {index}")
        match = TIMING_RE.match(lines[1])
        if not match:
            errors.append(f"block {expected}: bad timing")
            continue
        start = parse_ts(match.group(1))
        end = parse_ts(match.group(2))
        if start < previous_end:
            errors.append(f"block {expected}: overlaps previous")
        if end <= start:
            errors.append(f"block {expected}: non-positive duration")
        text_lines = lines[2:]
        text_line = ""
        if len(text_lines) != 1:
            errors.append(f"block {expected}: subtitle text must be exactly one line")
        else:
            text_line = text_lines[0].strip()
            if not text_line:
                errors.append(f"block {expected}: empty subtitle text")
            if r"\N" in text_line or HTML_BREAK_RE.search(text_line):
                errors.append(f"block {expected}: explicit line break marker is not allowed")
            duration = end - start
            if 0 < duration < min_warn_duration:
                warnings.append(f"block {expected}: short cue duration {duration:.3f}s")
            if strict_boundaries and previous_text and text_line:
                boundary_errors = []
                if ASCII_FRAGMENT_RE.search(previous_text) and ASCII_LEADING_RE.search(text_line):
                    boundary_errors.append("ASCII token appears split across adjacent cues")
                if text_line.startswith(BOUNDARY_BAD_STARTS):
                    boundary_errors.append("cue starts with likely sentence-tail + 现在 glue")
                if previous_text.endswith(BOUNDARY_BAD_ENDINGS):
                    boundary_errors.append("previous cue ends with likely incomplete word/phrase")
                for left, right in BOUNDARY_BAD_PAIRS:
                    if previous_text.endswith(left) and text_line.startswith(right):
                        boundary_errors.append(f"word appears split across cues: {left}/{right}")
                for reason in boundary_errors:
                    errors.append(f"block {expected}: {reason}")
        max_duration = max(max_duration, end - start)
        previous_end = end
        previous_text = text_line
    return {
        "path": str(path),
        "ok": not errors,
        "single_line_required": True,
        "strict_boundaries": strict_boundaries,
        "cue_count": len(blocks),
        "last_end": round(previous_end, 3) if blocks else 0,
        "max_duration": round(max_duration, 3),
        "warnings": warnings,
        "errors": errors,
    }


def main(argv: list[str]) -> int:
    args = argv[1:]
    strict_boundaries = False
    if "--strict-boundaries" in args:
        strict_boundaries = True
        args.remove("--strict-boundaries")
    min_warn_duration = 0.5
    if "--min-warn-duration" in args:
        index = args.index("--min-warn-duration")
        try:
            min_warn_duration = float(args[index + 1])
        except (IndexError, ValueError):
            print("error: --min-warn-duration requires a numeric value", file=sys.stderr)
            return 2
        del args[index:index + 2]
    if len(args) != 1:
        print(
            "usage: validate_srt.py [--strict-boundaries] "
            "[--min-warn-duration 0.5] <master.srt>",
            file=sys.stderr,
        )
        return 2
    report = validate(Path(args[0]), strict_boundaries=strict_boundaries, min_warn_duration=min_warn_duration)
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0 if report["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
