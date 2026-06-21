#!/usr/bin/env python3
"""Mechanical environment preflight for F1."""

from __future__ import annotations

import json
import shutil
import subprocess
import sys


def has_ffmpeg_filter(name: str) -> bool:
    try:
        proc = subprocess.run(
            ["ffmpeg", "-hide_banner", "-filters"],
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            check=False,
        )
    except FileNotFoundError:
        return False
    return name in proc.stdout


def main() -> int:
    report = {
        "ffmpeg": bool(shutil.which("ffmpeg")),
        "ffprobe": bool(shutil.which("ffprobe")),
        "libass_subtitles_filter": has_ffmpeg_filter("subtitles") or has_ffmpeg_filter(" ass "),
        "python": sys.version.split()[0],
    }
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0 if report["ffmpeg"] and report["ffprobe"] else 1


if __name__ == "__main__":
    raise SystemExit(main())

