#!/usr/bin/env python3
"""Validate F1 cue-to-audio/script dialogue alignment manifests."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path


def parse_srt_count(path: Path) -> int:
    text = path.read_text(encoding="utf-8").strip()
    if not text:
        return 0
    return len(re.split(r"\n\s*\n", text))


def span_values(value: object) -> tuple[float, float] | None:
    if isinstance(value, list) and len(value) == 2:
        return float(value[0]), float(value[1])
    if isinstance(value, dict) and "start" in value and "end" in value:
        return float(value["start"]), float(value["end"])
    return None


def validate(path: Path, srt_path: Path | None = None) -> dict:
    data = json.loads(path.read_text(encoding="utf-8"))
    cues = data.get("cues")
    errors: list[str] = []
    previous_audio_end = -1.0

    if not isinstance(cues, list) or not cues:
        return {"path": str(path), "ok": False, "errors": ["missing or empty cues"]}

    for expected, cue in enumerate(cues, 1):
        if not isinstance(cue, dict):
            errors.append(f"cue {expected}: not an object")
            continue
        if cue.get("index") != expected:
            errors.append(f"cue {expected}: bad index {cue.get('index')!r}")
        if not str(cue.get("text", "")).strip():
            errors.append(f"cue {expected}: missing text")
        audio_span = span_values(cue.get("audio_span"))
        if audio_span is None:
            errors.append(f"cue {expected}: missing audio_span")
        else:
            start, end = audio_span
            if end <= start:
                errors.append(f"cue {expected}: non-positive audio_span")
            if start < previous_audio_end - 0.02:
                errors.append(f"cue {expected}: audio_span overlaps or moves backward")
            previous_audio_end = max(previous_audio_end, end)
        if cue.get("script_span") is None:
            errors.append(f"cue {expected}: missing script_span")
        if not str(cue.get("source_method", "")).strip():
            errors.append(f"cue {expected}: missing source_method")
        if cue.get("verdict") != "pass":
            errors.append(f"cue {expected}: verdict is {cue.get('verdict')!r}")

    srt_count = None
    if srt_path is not None:
        srt_count = parse_srt_count(srt_path)
        if srt_count != len(cues):
            errors.append(f"srt cue count {srt_count} != alignment cue count {len(cues)}")

    return {
        "path": str(path),
        "srt_path": str(srt_path) if srt_path else None,
        "ok": not errors,
        "cue_count": len(cues),
        "srt_cue_count": srt_count,
        "errors": errors,
    }


def main(argv: list[str]) -> int:
    if len(argv) not in (2, 3):
        print("usage: validate_dialogue_alignment.py <dialogue_alignment.json> [master.srt]", file=sys.stderr)
        return 2
    report = validate(Path(argv[1]), Path(argv[2]) if len(argv) == 3 else None)
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0 if report["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
