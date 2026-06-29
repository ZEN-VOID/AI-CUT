# Changelog: F2

## 2026-06-29

- Added platform deduplication controls for batch and semantic-equivalent F2 videos: `asset_usage_ledger.json`, `asset_diversity_audit.json`, reuse penalties, variation axes, and completion/report gates.
- Strengthened `N3-MEDIA-EVIDENCE` and `N5-STORYBOARD-PLAN` so F2 consumes deep manifest tags (`semantic_vector`, `trigger_profile`, `visual_signature`, `variation_profile`, `analysis_slice_id`, `reuse_profile`) instead of relying on coarse `semantic_tags`.
- Updated execution/output report templates, context heuristics, and test prompts for batch asset diversity and same-meaning copy variation.

## 2026-06-25

- Created F2 as a new HyperFrames-native workflow skill.
- Defined F2 as a successor/rebuild of F1 business goals, not an in-place replacement of F1 runtime.
- Added runtime-spine contract, HyperFrames module routing, review gates, output templates, migration matrix and registry-ready metadata.
