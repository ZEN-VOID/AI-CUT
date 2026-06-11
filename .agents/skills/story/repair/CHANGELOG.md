# CHANGELOG

## 2026-05-30

- Added `guardrails/guardrails-contract.md` and `SKILL.md#Runtime Guardrails` to match the latest `$skill-工作车间` Skill 2.0 runtime boundary requirements.
- Expanded `review/review-contract.md` with `security`、`runtime_behavior`、`integration`、`convergence` dimensions and parseable repair failure codes.
- Added `Review Gate Mapping` to `references/impact-scope-contract.md` and `references/source-truth-ledger.md`.
- Updated `README.md` directory tree and quick entry notes for the guardrails partition.

## 2026-06-10

- Updated authorship routing after `3-初稿` and `4-润色` collapsed old model-specific branches into root stage skill packages.
- Changed legacy `写作模型` / `润色模型` handling to read-only execution-environment evidence instead of repair routing truth.

## 2026-04-29

- Initialized `story-repair` as a full Skill 2.0 package.
- Added impact scope, source truth, repair workflow, type packages, review gate, output template, product metadata, and knowledge-base heuristics.
- Fixed the core contract that local story repairs must trace upstream owners, same-layer predecessors, downstream outputs, future constraints, review gates, and accepted actualization before claiming closure.
- Upgraded impact scope into a universal typed matrix: "when X, check X" now lives in the rule layer, with project-specific extensions limited to project CONTEXT/MEMORY.
- Historical note: this version previously treated `写作模型` as a repair routing hint; this was superseded on 2026-06-10 by root stage routing.
