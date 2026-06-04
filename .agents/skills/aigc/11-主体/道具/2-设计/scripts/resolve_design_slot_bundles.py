#!/usr/bin/env python3
"""Resolve prop design slot_bundles for review."""

from __future__ import annotations

import json


SLOT_REVIEW_CONTRACT = "design-slot-review-contract.md"
SLOT_MARKER_COVERAGE = ("SCENE-BUNDLE-01", "ROLE-BUNDLE-01", "PROP-BUNDLE-01")
PROP_REQUIRED_SLOTS = (
    "prop_id",
    "deconstruction_subject_id",
    "source_confidence",
    "material_logic",
    "function_logic",
    "prompt_evidence_chain",
    "deconstruction_coverage",
)


def main() -> int:
    slot_bundles = [
        {
            "id": "PROP-BUNDLE-01",
            "owner": "prop-design-review",
            "contract": SLOT_REVIEW_CONTRACT,
            "required_slots": list(PROP_REQUIRED_SLOTS),
        }
    ]
    print(json.dumps({"slot_bundles": slot_bundles}, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
