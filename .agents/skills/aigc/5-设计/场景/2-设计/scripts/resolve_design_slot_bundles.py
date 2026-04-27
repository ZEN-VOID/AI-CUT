#!/usr/bin/env python3
"""Resolve scene design slot_bundles for review."""

from __future__ import annotations

import json


SLOT_REVIEW_CONTRACT = "design-slot-review-contract.md"
SLOT_MARKER_COVERAGE = ("SCENE-BUNDLE-01", "ROLE-BUNDLE-01", "PROP-BUNDLE-01")


def main() -> int:
    slot_bundles = [{"id": "SCENE-BUNDLE-01", "contract": SLOT_REVIEW_CONTRACT}]
    print(json.dumps({"slot_bundles": slot_bundles}, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
