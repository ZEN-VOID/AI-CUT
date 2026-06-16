#!/usr/bin/env python3
"""Build a mechanical character research manifest."""

from __future__ import annotations

import argparse
import json


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
    print(json.dumps({"owner": "角色", "mechanical_only": True}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
