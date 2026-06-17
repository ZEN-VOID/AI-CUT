#!/usr/bin/env python3
"""Resolve character design slot_bundles for review."""

from __future__ import annotations

import json


SLOT_REVIEW_CONTRACT = "design-slot-review-contract.md"
SLOT_MARKER_COVERAGE = ("SCENE-BUNDLE-01", "ROLE-BUNDLE-01", "PROP-BUNDLE-01")
ROLE_REQUIRED_SLOTS = (
    "character_id",
    "base_subject_id",
    "asset_id",
    "variant_id",
    "variant_label",
    "variant_type",
    "identity_invariants",
    "variant_state_delta",
    "deconstruction_subject_id",
    "identity_evidence",
    "visual_drivers",
    "aesthetic_appeal",
    "lead_beauty_handsomeness_floor",
    "lead_presence_temperament_floor",
    "charisma_floor",
    "height_scale",
    "body_build",
    "hair_design",
    "costume_color_palette",
    "face_readability_lighting",
    "corpus_usage_trace",
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
