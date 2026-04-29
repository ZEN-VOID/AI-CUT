# Changelog

## 2026-04-29

- Renamed skill package directory from `.agents/skills/story/context-return` to `.agents/skills/story/return`.
- Updated canonical skill id and product prompt from `story-context-return` to `story-return`.
- Kept `context-return/第V卷.context-return.json` as the runtime artifact path and retained legacy `context-return` / `story-context-return` handoff aliases for compatibility.

## 2026-04-26

- Upgraded `return` to Skill 2.0 layout.
- Added canonical `references/`, `steps/`, `review/`, `types/`, `knowledge-base/`, `scripts/`, and `agents/` sections.
- Rewrote `SKILL.md` as an input/output anchored dynamic reference entry.
- Migrated the context return actualization spec from `_shared/` into `references/`.
- Added `agents/openai.yaml`, `README.md`, and `templates/output-template.md`.
