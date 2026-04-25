#!/usr/bin/env python3
"""Validate scene design inputs without authoring creative content."""

from __future__ import annotations

import argparse

from _creative_guard import add_legacy_guard, enforce_no_script_authorship


# Audit markers: --allow-legacy-script-authorship, LEGACY_SCRIPT_AUTHORSHIP_ERROR.


def main() -> int:
    parser = argparse.ArgumentParser()
    add_legacy_guard(parser)
    args = parser.parse_args()
    enforce_no_script_authorship(args.allow_legacy_script_authorship)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
