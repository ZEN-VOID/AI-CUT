# Changelog

## 2026-06-15

- Upgraded `imagegen` to the current Skill 2.0 runtime-spine validator contract.
- Migrated the old `steps/execution-workflow.md` node truth into `SKILL.md` and removed the unsupported `steps/` directory.
- Added `test-prompts.json`, `types/request-profile.md`, `Module Trigger Matrix`, convergence gates, checkpoint/evaluation contracts, runtime guardrails, and reference `Review Gate Mapping` tables.
- Synced README, types, context heuristics, and output governance so modules remain support layers rather than second rule sources.
- Redefined `.agents/skills/cli/imagegen` as the built-in `image_gen` tool route only.
- Removed CLI/API fallback from the active mode, type, workflow, review, persistence, transparency, prompting, and README contracts.
- Kept `scripts/image_gen.py` and CLI references as historical/external workflow material, not as an execution path for this skill.
- Standardized batch/multiple image work as subagents parallel fan-out by default, capped at 10 concurrent workers, with main-thread serial execution allowed only by explicit user request.
- Promoted associated-project image transfer into the output persistence and review gates.

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
