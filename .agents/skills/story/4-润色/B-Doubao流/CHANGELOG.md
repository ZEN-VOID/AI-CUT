# Changelog

## 2026-05-30

- Aligned package with latest `skill-工作车间` Skill 2.0 delivery contract.
- Added `guardrails/guardrails-contract.md`, `types/type-map.md`, and `types/guardrail-setup.md`.
- Added `Input Contract`, `Multi-Subskill Continuous Workflow`, `Runtime Guardrails`, `Field Mapping`, and parser-friendly `Output Contract` fields to `SKILL.md`.
- Extended review gates with `security`, `runtime_behavior`, `integration`, `convergence`, fail-code registry, and convergence criteria.
- Added `Review Gate Mapping` to `references/chapter-polishing-contract.md`.

## 2026-04-29

- Added `subagent_review_optimize` mode for explicit subagents requests.
- Routed audit points through `.agents/skills/story/review` dimension child skills, then back into Doubao repair prompts.
- Tightened review, workflow, type, and evidence gates so subagents mode cannot stop at reports without same-round provider optimization.

## 2026-04-26

- Upgraded `story-polishing` to Skill 2.0 layout.
- Rewrote `SKILL.md` as an entry, routing, loading, root-cause and output contract.
- Split chapter polishing details into `references/`, workflow topology into `steps/`, type routing into `types/`, and quality gates into `review/`.
- Added `knowledge-base/`, `agents/openai.yaml`, `README.md`, and `templates/output-template.md`.
- Preserved existing `scripts/polish_chapter_via_doubao.py`, `templates/chapter-root.template.md`, and `templates/doubao-system-prompt.md` as compatibility carriers while converting them to the 4-润色 contract.
- Updated the Doubao bridge to inject project `MEMORY.md`, include existing target chapter text before rewrite/continue/repair, and expose `--mode` for polishing branch selection.
- Synced internal references after moving the Doubao implementation under `3-初稿/B-Doubao流/`.
- Renamed the provider lane to `story-polishing-doubao`, added explicit overwrite safety (`--force` + backup sidecar), tightened provider output validation, and registered the lane separately from the parent router.
