# Context Return Heuristics

This file stores stable reusable heuristics. Mandatory gates remain in `SKILL.md`, `references/`, `steps/`, and `review/`.

## Prevention Patterns

- Treat `PASS` as a green light only after the handoff target check also passes.
- Normalize `context_return_delta` before opening any truth file for writing.
- If a value describes what an entity is now, prefer `Cards.current_state/history`.
- If a value describes which plan promise has been fulfilled, prefer planning actualization sidecars and story_map actualization.
- Keep root `全息地图.json` light: root receives summary/index, slices receive details.
- When a recovery question appears, route to `resume/` even if the next recommendation is to rerun `story-return`.

## Common Failure Modes

| symptom | likely prevention |
| --- | --- |
| root story_map grows into a second detail store | force slice detail + root summary split |
| historical PASS gets actualized | check `acceptance_status`, `handoff_targets`, and `accepted_manuscript_refs` before delta |
| planning markdown becomes mixed truth | only write `.actualization.json` companions |
| half-written run is hard to diagnose | pending and committed manifests must be preserved |
| user asks a query and receives an artifact | classify request before loading writeback workflow |
