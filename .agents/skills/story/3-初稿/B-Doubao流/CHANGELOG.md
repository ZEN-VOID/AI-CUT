# Changelog

## 2026-05-30

- Added `guardrails/guardrails-contract.md` and `SKILL.md` Runtime Guardrails for permission boundaries, self-modification prohibitions, anti-injection rules, and escalation.
- Converted `SKILL.md` Output Contract from table-only form to validator-readable five-field contract.
- Updated `types/type-map.md` to avoid treating glob or placeholder topic paths as literal delivery references.
- Extended review gates with `security`, `runtime_behavior`, `integration`, and `convergence` dimensions.
- Added `Review Gate Mapping` to `references/chapter-drafting-contract.md` and synced README/CONTEXT notes.

## 2026-04-27

- Standardized repair authorship: `local_repair`, `chapter_rewrite`, review返工和卷级修复优化仍必须由 Doubao provider 执行正文创作性改写。
- Clarified that GPT/subagents in repair mode only own diagnosis, repair brief, prompt constraints, verification, and aggregation.
- Added gates requiring Doubao repair messages/provider reports before a repaired draft can still be claimed as `B-Doubao流` output.

## 2026-04-26

- Upgraded `story-drafting` to Skill 2.0 layout.
- Rewrote `SKILL.md` as an entry, routing, loading, root-cause and output contract.
- Split chapter drafting details into `references/`, workflow topology into `steps/`, type routing into `types/`, and quality gates into `review/`.
- Added `knowledge-base/`, `agents/openai.yaml`, `README.md`, and `templates/output-template.md`.
- Preserved existing `scripts/write_chapter_via_doubao.py`, `templates/chapter-root.template.md`, `templates/doubao-system-prompt.md`, and legacy `_shared/drafting-instant-validation-contract.md` compatibility carrier.
- Updated the Doubao bridge to inject project `MEMORY.md`, include existing target chapter text before rewrite/continue/repair, and expose `--mode` for drafting branch selection.
- Synced internal references after moving the Doubao implementation under `3-初稿/B-Doubao流/`.
- Renamed the provider lane to `story-drafting-doubao`, added explicit overwrite safety (`--force` + backup sidecar), tightened provider output validation, and registered the lane separately from the parent router.
