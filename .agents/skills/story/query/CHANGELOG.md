# Changelog

## 2026-06-16

- Upgraded `story-query` to runtime-spine Skill 2.0 delivery shape.
- Moved execution nodes, routes, gates, convergence, module triggers, attention protocol and evaluation contract into `SKILL.md`.
- Removed unsupported `steps/` execution module; migrated read-only command details to `references/query-command-catalog.md`.
- Added `types/type-map.md` and `test-prompts.json` for type package loading and regression prompt coverage.
- Added reference gate mappings and synchronized README, CONTEXT and knowledge-base owner wording.

## 2026-04-27

- Upgraded `story-query` to Skill 2.0 layout.
- Added canonical partitions: `steps/`, `types/`, `review/`, `templates/`, `knowledge-base/`, `scripts/`, and `agents/`.
- Rewrote `SKILL.md` as an input/output anchored dynamic reference entry.
- Added `templates/output-template.md` aligned with the Output Contract five fields.
- Added `agents/openai.yaml` with UI metadata and explicit `$story-query` default prompt.
- Preserved existing data-flow references and moved legacy section ownership into `references/legacy-migration-matrix.md`.
