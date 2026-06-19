# CHANGELOG

## 2026-06-18

- Added `N0-PROBLEM-DISCOVERY` to convert vague reading symptoms and under-specified findings into a `problem_discovery_packet` before impact mapping or prose routing.
- Added `types/scope/problem-discovery.md` and synchronized `types/type-map.md`, review gates, output template, README, knowledge-base heuristics, and CONTEXT playbook.
- Fixed the report template field drift from `review_actualization` to `acceptance_actualization`.
- Expanded problem discovery for detail-expansion symptoms so action, interiority, atmosphere, sci-fi tech, cyberpunk texture, xuanhuan power, and romance tension findings can route to real `story-polishing` repair package ids before any prose rewrite.
- Clarified that those detail-expansion symptoms are candidate, genre/scene-dependent problem families; non-applicable foci now report as N/A instead of becoming universal diagnosis requirements.

## 2026-06-16

- Upgraded `story-repair` to the current Skill 2.0 runtime-spine contract.
- Moved the repair workflow topology, node table, fail-code routing, module authorization, convergence gates, business analysis, quantitative criteria, attention protocol, checkpoint contract, and evaluation contract into `SKILL.md`.
- Removed `steps/repair-workflow.md` as a second node truth and synchronized direct references to `SKILL.md` node IDs.
- Added `test-prompts.json` with repair/review regression prompts.
- Expanded the output template and scripts README with LLM-first authorship, module evidence, checkpoint evidence, fallback evidence, and residual-risk closure.

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
