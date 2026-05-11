# Changelog

## 2026-05-08

- Clarified resolution precedence: the default remains 2K only when neither the user nor an upstream skill specifies a target.
- Added explicit upstream handoff handling so `resolution_target: 4K` from parent workflows is preserved in built-in prompts, CLI payloads, reports, and review gates instead of being downgraded to 2K.

## 2026-04-24

- Set the skill-level default resolution target to 2K.
- Updated CLI fallback defaults so omitted `--size` resolves to `2048x1152` for `gpt-image-2`, while non-`gpt-image-2` models keep model-supported defaults.
- Upgraded `imagegen` to a Skill 2.0 package structure.
- Added `CONTEXT.md`, `README.md`, `templates/`, `steps/`, `review/`, `types/`, and `knowledge-base/`.
- Rewrote `SKILL.md` as a dynamic reference entry with explicit Input Contract, Reference Loading Guide, Field Mapping, Root-Cause Execution Contract, and Output Contract.
- Split mode routing, output persistence, and transparent-background details into dedicated `references/` owners.
- Preserved existing CLI/API/prompting references, scripts, metadata, and assets.
