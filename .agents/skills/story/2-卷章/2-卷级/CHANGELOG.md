# Changelog

## 2026-05-30

- Synced with latest `skill-工作车间` Skill 2.0 delivery contract.
- Added `guardrails/guardrails-contract.md` and `Runtime Guardrails` markers in `SKILL.md`.
- Rebuilt `types/type-map.md` as a loadable Package Index that points to `types/volume-planning-type-map.md`.
- Extended review dimensions with `security`, `runtime_behavior`, `integration`, and `convergence`.
- Updated README validation commands to include delivery-mode validator and smoke test.

## 2026-04-29

- Added explicit project `team.yaml` advisor consultation contract for subagents-enabled volume-level planning.
- Added advisor packet, review gate, context heuristic, and executable-guidance handoff before LLM-authored volume-level planning.
- Added volume-level suspense switch through shared `../_shared/suspense-design-contract.md`.
- Added `本卷悬念开关` to `SKILL.md`, volume output contract, templates, workflow nodes, review gate, type map, README, CONTEXT, and validator-facing fields.
- Locked volume-level suspense slots for inherited book suspense, new volume mystery, hidden information, visible surface information, misdirection, reveals, delayed pressure, and chapter-level constraints.
- Expanded volume suspense into `本卷悬念线程表` and `本卷悬念负载` for multi-thread state tracking.

## 2026-04-28

- Added volume-level timeline system via shared `../_shared/timeline-design-contract.md`.
- Added `本卷时间线` to `SKILL.md`, output contract, templates, workflow nodes, review gate, and validator-facing template fields.
- Fixed volume-to-chapter handoff so chapter planning inherits chapter chronology, parallel hidden events, time jumps/compression, and volume end-state changes.

## 2026-04-26

- Upgraded `2-卷级` to a Skill 2.0 package.
- Added canonical partitions: `steps/`, `review/`, `types/`, `knowledge-base/`, `scripts/`, and `agents/`.
- Rewrote `SKILL.md` as a dynamic reference entry with Input Contract, Reference Loading Guide, Root-Cause Execution Contract, Field Mapping, Mermaid maps, and five-field Output Contract.
- Added `templates/output-template.md` and aligned the legacy volume template with the Output Contract.
- Added `references/legacy-upgrade-matrix.md` to preserve old section ownership and migration traceability.
