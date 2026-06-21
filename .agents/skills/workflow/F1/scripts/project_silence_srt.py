#!/usr/bin/env python3
"""Project LLM-approved subtitle chunks onto voiceover silence intervals.

This script is mechanical. It does not split or rewrite the user's script.
Input chunks must already be chosen by the LLM/operator.
"""

from __future__ import annotations

import json
import re
import subprocess
import sys
from pathlib import Path


def run_silencedetect(audio: Path, noise: str, duration: float) -> tuple[float, list[tuple[float, float, float]]]:
    voice_duration = float(
        subprocess.check_output(
            ["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "default=nw=1:nk=1", str(audio)],
            text=True,
        ).strip()
    )
    proc = subprocess.run(
        ["ffmpeg", "-hide_banner", "-i", str(audio), "-af", f"silencedetect=n={noise}:d={duration}", "-f", "null", "-"],
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    silences: list[tuple[float, float, float]] = []
    current = None
    for line in proc.stderr.splitlines():
        start_match = re.search(r"silence_start: ([0-9.]+)", line)
        if start_match:
            current = float(start_match.group(1))
        end_match = re.search(r"silence_end: ([0-9.]+) \| silence_duration: ([0-9.]+)", line)
        if end_match and current is not None:
            silences.append((current, float(end_match.group(1)), float(end_match.group(2))))
            current = None
    return voice_duration, silences


def timestamp(seconds: float) -> str:
    seconds = max(0.0, seconds)
    h = int(seconds // 3600)
    m = int((seconds % 3600) // 60)
    s = int(seconds % 60)
    ms = int(round((seconds - int(seconds)) * 1000))
    if ms == 1000:
        s += 1
        ms = 0
    if s == 60:
        m += 1
        s = 0
    if m == 60:
        h += 1
        m = 0
    return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"


def build_intervals(voice_duration: float, silences: list[tuple[float, float, float]], min_pause: float) -> list[tuple[float, float]]:
    start0 = 0.0
    for start, end, _ in silences:
        if start <= 0.001:
            start0 = end
            break
    real = [(s, e, d) for s, e, d in silences if d >= min_pause]
    intervals: list[tuple[float, float]] = []
    previous = start0
    for start, end, _ in real:
        if end <= start0 + 0.01:
            continue
        if start - previous >= 0.16:
            intervals.append((previous, start))
        previous = end
    if voice_duration - previous >= 0.16:
        intervals.append((previous, voice_duration))
    return intervals


def main(argv: list[str]) -> int:
    if len(argv) < 4:
        print(
            "usage: project_silence_srt.py <voiceover> <chunks.json> <out.srt> [out-timing.json]",
            file=sys.stderr,
        )
        return 2
    audio = Path(argv[1])
    chunks = json.loads(Path(argv[2]).read_text(encoding="utf-8"))
    out_srt = Path(argv[3])
    out_timing = Path(argv[4]) if len(argv) > 4 else out_srt.with_suffix(".timing.json")
    if not isinstance(chunks, list) or not all(isinstance(item, str) for item in chunks):
        print("chunks.json must be a JSON array of strings", file=sys.stderr)
        return 2
    voice_duration, silences = run_silencedetect(audio, "-35dB", 0.08)
    intervals = build_intervals(voice_duration, silences, 0.18)
    if len(intervals) != len(chunks):
        print(f"chunk/interval mismatch: {len(chunks)} chunks vs {len(intervals)} intervals", file=sys.stderr)
        return 1
    lines: list[str] = []
    records = []
    for index, ((start, end), text) in enumerate(zip(intervals, chunks), 1):
        cue_start = max(0.0, start - 0.045)
        cue_end = min(voice_duration, end + 0.07)
        if index < len(intervals):
            next_start = max(0.0, intervals[index][0] - 0.045)
            cue_end = min(cue_end, next_start - 0.01)
        lines.extend([str(index), f"{timestamp(cue_start)} --> {timestamp(cue_end)}", text, ""])
        records.append({"index": index, "start": round(cue_start, 3), "end": round(cue_end, 3), "text": text})
    out_srt.write_text("\n".join(lines), encoding="utf-8")
    out_timing.write_text(
        json.dumps(
            {
                "voice_duration": voice_duration,
                "cue_count": len(records),
                "method": "silencedetect n=-35dB d=0.08; min_pause=0.18",
                "cues": records,
            },
            ensure_ascii=False,
            indent=2,
        ),
        encoding="utf-8",
    )
    print(json.dumps({"srt": str(out_srt), "timing": str(out_timing), "cue_count": len(records)}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
