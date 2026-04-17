#!/usr/bin/env python3
"""Backward-compatible wrapper for the Grok video submit CLI."""

from __future__ import annotations

from grok_video_generate import main


if __name__ == "__main__":
    raise SystemExit(main())
