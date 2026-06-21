#!/usr/bin/env python3
"""Validate SRT structure for F1 outputs."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path


TIMING_RE = re.compile(r"^(\d\d:\d\d:\d\d,\d{3}) --> (\d\d:\d\d:\d\d,\d{3})$")


def parse_ts(value: str) -> float:
    h, m, rest = value.split(":")
    s, ms = rest.split(",")
    return int(h) * 3600 + int(m) * 60 + int(s) + int(ms) / 1000


def validate(path: Path) -> dict:
    text = path.read_text(encoding="utf-8").strip()
    blocks = re.split(r"\n\s*\n", text) if text else []
    previous_end = -1.0
    max_duration = 0.0
    errors: list[str] = []
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
        max_duration = max(max_duration, end - start)
        previous_end = end
    return {
        "path": str(path),
        "ok": not errors,
        "cue_count": len(blocks),
        "last_end": round(previous_end, 3) if blocks else 0,
        "max_duration": round(max_duration, 3),
        "errors": errors,
    }


def main(argv: list[str]) -> int:
    if len(argv) != 2:
        print("usage: validate_srt.py <master.srt>", file=sys.stderr)
        return 2
    report = validate(Path(argv[1]))
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0 if report["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))

