#!/usr/bin/env python3
"""Bind prop design packets to the canonical template."""

from __future__ import annotations

import argparse
from pathlib import Path

from _creative_guard import add_legacy_guard, enforce_no_script_authorship


TEMPLATE_PATH = Path(__file__).resolve().parents[1] / "templates" / "prop_masterprompt.structured.v2.md"
# Audit markers: --allow-legacy-script-authorship, LEGACY_SCRIPT_AUTHORSHIP_ERROR.


def main() -> int:
    parser = argparse.ArgumentParser()
    add_legacy_guard(parser)
    args = parser.parse_args()
    enforce_no_script_authorship(args.allow_legacy_script_authorship)
    if not TEMPLATE_PATH.exists():
        raise SystemExit(f"missing template: {TEMPLATE_PATH}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
