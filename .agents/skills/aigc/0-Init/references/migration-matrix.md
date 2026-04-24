# Skill 2.0 Migration Matrix

This file records the 2026-04-24 upgrade from the former single-file `0-Init` contract into Skill 2.0 partitions.

## Section Matrix

| source section | target owner | operation | semantic risk | validation gate |
| --- | --- | --- | --- | --- |
| frontmatter, name, description, tier | `SKILL.md` | keep and update | low | validator |
| Context Loading Contract | `SKILL.md` | keep | high | context audit |
| single-source directory contract | `SKILL.md`, `CHANGELOG.md` | replace with dynamic-reference contract | high | semantic review |
| When to Use / When Not to Use | `SKILL.md` | keep compressed | low | semantic review |
| business_goal / business_object / constraints | `references/scope-and-runtime.md` | split and rewrite | medium | semantic review |
| visual maps | `SKILL.md`, `steps/init-workflow.md` | compress | low | manual review |
| Total Input Contract | `SKILL.md`, `steps/init-workflow.md` | split | high | semantic review |
| Internal Capability Fusion | `SKILL.md`, `references/mode-and-team-contract.md`, `steps/init-workflow.md` | split | high | semantic review |
| Thinking-Action Node Contract | `steps/init-workflow.md` | move and normalize | high | review gate |
| Topology Contract / Ordered Rules | `steps/init-workflow.md` | move | high | review gate |
| Canonical Landing | `references/scope-and-runtime.md` | move | high | AIGC audit |
| Init Truth Ownership | `references/scope-and-runtime.md` | move | medium | semantic review |
| Rebootstrap Contract | `references/rebootstrap-contract.md` | move | high | review gate |
| Initialization Mode Contract | `references/mode-and-team-contract.md` | move | high | review gate |
| initialization option card | `templates/init-option-card.template.md` | move | medium | template readback |
| Team Manifest Contract | `references/mode-and-team-contract.md` | move | high | semantic review |
| Prompt Packet Contract | `references/mode-and-team-contract.md` | move | high | semantic review |
| North Star / Stage Entry / Adaptation | `references/artifacts-and-sources.md` | move | high | template + review gate |
| Lazy Governance | `references/artifacts-and-sources.md` | move | medium | review gate |
| Story Source Manifest / Completeness / Reconciliation | `references/artifacts-and-sources.md` | move | high | semantic review |
| Synthesis Contract | `references/artifacts-and-sources.md` | move | high | review gate |
| Sufficiency Gate / Completion Standard | `review/init-review-gate.md` | move | high | review gate |
| Execution Procedure | `SKILL.md`, `steps/init-workflow.md` | split | high | semantic review |
| Root-Cause Execution Contract | `SKILL.md` | keep and retarget | high | validator marker |
| Field Master / Thought Pass / Pass Table | `SKILL.md`, `steps/init-workflow.md`, `review/init-review-gate.md` | split | high | review gate |
| Context Preload | `SKILL.md` | keep | high | context audit |

## Resource Matrix

| source path | target path | operation | validation |
| --- | --- | --- | --- |
| `CONTEXT.md` | `CONTEXT.md` | keep, patch obsolete single-source notes | context audit |
| `CHANGELOG.md` | `CHANGELOG.md` | keep, append migration | manual readback |
| `agents/openai.yaml` | `agents/openai.yaml` | keep, shorten description and update prompt | validator |
| `templates/north-star.template.yaml` | same | keep | template readback |
| `templates/init-handoff.template.yaml` | same | keep | template readback |
| `templates/project-memory.template.md` | same | keep | template readback |
| missing output-template binding | `templates/output-template-map.md` | create | Output Contract alignment |
| missing final response template | `templates/output-template.md` | create | Output Contract alignment |
| missing project changelog template | `templates/project-changelog.template.md` | create | Output Contract alignment |
| missing project context root helper | `templates/project-context-readme.template.md` | create | Output Contract alignment |
| missing project state template | `templates/state.template.json` | create | Output Contract alignment |
| missing `README.md` | `README.md` | create | validator |
| missing `TODO.md` | `TODO.md` | create | validator |
| missing Skill 2.0 partitions | `references/`, `steps/`, `review/`, `types/`, `knowledge-base/`, `scripts/` | create | validator |

## Reference Sync Plan

- Replace obsolete claims that `references/` must not exist.
- Keep shared template references pointing to `.agents/skills/aigc/_shared/` rather than duplicating schemas.
- Re-run Skill 2.0 validator after migration.
- Re-run AIGC and context audits where available.
