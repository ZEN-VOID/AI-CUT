#!/usr/bin/env python3
"""Backward-compatible wrapper for the Luma video CLI."""

from __future__ import annotations

from luma_video_generate import main


if __name__ == "__main__":
    raise SystemExit(main())
