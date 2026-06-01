#!/usr/bin/env python3
"""Render already-authored character fields into the canonical template."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


TEMPLATE_PATH = Path(__file__).resolve().parents[1] / "templates" / "character_masterprompt.structured.v2.md"
LEGACY_SCRIPT_FLAG = "--allow-legacy-script-authorship"
LEGACY_SCRIPT_AUTHORSHIP_ERROR = (
    "LEGACY_SCRIPT_AUTHORSHIP_ERROR: scripts may not author canonical creative text."
)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(LEGACY_SCRIPT_FLAG, action="store_true", dest="legacy_authorship")
    args = parser.parse_args()
    if args.legacy_authorship:
        raise SystemExit(LEGACY_SCRIPT_AUTHORSHIP_ERROR)
    print(json.dumps({"template": TEMPLATE_PATH.as_posix(), "template_name": "character_masterprompt.structured.v2.md"}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
