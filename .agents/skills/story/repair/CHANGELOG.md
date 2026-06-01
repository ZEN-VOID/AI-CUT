# CHANGELOG

## 2026-05-30

- Added `guardrails/guardrails-contract.md` and `SKILL.md#Runtime Guardrails` to match the latest `$skill-工作车间` Skill 2.0 runtime boundary requirements.
- Expanded `review/review-contract.md` with `security`、`runtime_behavior`、`integration`、`convergence` dimensions and parseable repair failure codes.
- Added `Review Gate Mapping` to `references/impact-scope-contract.md` and `references/source-truth-ledger.md`.
- Updated `README.md` directory tree and quick entry notes for the guardrails partition.

## 2026-04-29

- Initialized `story-repair` as a full Skill 2.0 package.
- Added impact scope, source truth, repair workflow, type packages, review gate, output template, product metadata, and knowledge-base heuristics.
- Fixed the core contract that local story repairs must trace upstream owners, same-layer predecessors, downstream outputs, future constraints, review gates, and accepted actualization before claiming closure.
- Upgraded impact scope into a universal typed matrix: "when X, check X" now lives in the rule layer, with project-specific extensions limited to project CONTEXT/MEMORY.
- Added the default that user-specified documents with a `写作模型` header must be adjusted through that model's lane unless the user explicitly asks to switch models.
