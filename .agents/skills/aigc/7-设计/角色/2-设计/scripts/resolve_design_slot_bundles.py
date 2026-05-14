#!/usr/bin/env python3
"""Resolve character design slot_bundles for review."""

from __future__ import annotations

import json


SLOT_REVIEW_CONTRACT = "design-slot-review-contract.md"
SLOT_MARKER_COVERAGE = ("SCENE-BUNDLE-01", "ROLE-BUNDLE-01", "PROP-BUNDLE-01")
ROLE_REQUIRED_SLOTS = (
    "character_id",
    "deconstruction_subject_id",
    "identity_evidence",
    "visual_drivers",
    "costume_design",
    "prompt_evidence_chain",
    "deconstruction_coverage",
)


def main() -> int:
    slot_bundles = [
        {
            "id": "ROLE-BUNDLE-01",
            "owner": "character-design-review",
            "contract": SLOT_REVIEW_CONTRACT,
            "required_slots": list(ROLE_REQUIRED_SLOTS),
        }
    ]
    print(json.dumps({"slot_bundles": slot_bundles}, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
