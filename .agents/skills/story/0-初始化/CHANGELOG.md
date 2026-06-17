# Changelog

## 2026-06-16

- Upgraded `story-init` to runtime-spine Skill 2.0 delivery standard.
- Moved the executable node network, business analysis, quant criteria, attention protocol, checkpoint contract, module matrices, convergence gates and review binding into `SKILL.md`.
- Retired unsupported `steps/` execution source after migrating its semantic content into the main runtime spine.
- Added `test-prompts.json` for regression prompts covering auto init, custom roster init, repair/review drift and film route blocking.
- Synced active references from the retired workflow file to `SKILL.md` node references and updated the validation command to the current `skill-2.0` meta scripts.
- Added Review Gate Mapping to `references/creative-seed-routing/CONTEXT.md`.

## 2026-05-30

- Added latest Skill 2.0 guardrails layer with `guardrails/guardrails-contract.md` and `SKILL.md` Runtime Guardrails.
- Added `types/type-map.md` as the required type package index while preserving `types/init-type-map.md` as the default fixed context package.
- Added `review/review-contract.md` as the review gate aggregate for structure, security, runtime behavior, integration and convergence.
- Added `Multi-Subskill Continuous Workflow` to `SKILL.md` and expanded dynamic references to remove wildcard or smoke-test-broken paths.
- Updated README and legacy migration references to reflect the current canonical package layout.

## 2026-04-26

- Upgraded `story-init` to Skill 2.0 workshop layout.
- Rewrote `SKILL.md` as input/output anchored dynamic reference entry with Mermaid topology maps.
- Added canonical owner partitions: `steps/`, `review/`, `types/`, `knowledge-base/`, `scripts/`, `README.md`, `CHANGELOG.md`, and `templates/output-template.md`.
- Split legacy long-form sections into:
  - `references/mode-and-team-contract.md`
  - `references/runtime-and-handoff-contract.md`
  - `references/prompt-packet-contract.md`
  - `steps/init-workflow.md`
  - `types/init-type-map.md`
  - `review/init-review-gate.md`
- Added `references/legacy-upgrade-matrix.md` to preserve old section ownership and validation gates.
- Removed empty retired mode directories after reference sync check: `references/advisor-council-mode/`, `references/fast-mode/`, `references/autonomous-mode/`.
