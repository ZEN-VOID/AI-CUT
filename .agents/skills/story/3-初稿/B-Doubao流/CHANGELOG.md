# Changelog

## 2026-04-26

- Upgraded `story-drafting` to Skill 2.0 layout.
- Rewrote `SKILL.md` as an entry, routing, loading, root-cause and output contract.
- Split chapter drafting details into `references/`, workflow topology into `steps/`, type routing into `types/`, and quality gates into `review/`.
- Added `knowledge-base/`, `agents/openai.yaml`, `README.md`, and `templates/output-template.md`.
- Preserved existing `scripts/write_chapter_via_doubao.py`, `templates/chapter-root.template.md`, `templates/doubao-system-prompt.md`, and legacy `_shared/drafting-instant-validation-contract.md` compatibility carrier.
- Updated the Doubao bridge to inject project `MEMORY.md`, include existing target chapter text before rewrite/continue/repair, and expose `--mode` for drafting branch selection.
- Synced internal references after moving the Doubao implementation under `3-初稿/B-Doubao流/`.
- Renamed the provider lane to `story-drafting-doubao`, added explicit overwrite safety (`--force` + backup sidecar), tightened provider output validation, and registered the lane separately from the parent router.
