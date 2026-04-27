# Output Template Map

This file binds `$aigc-init` output templates to the `Output Contract (Mandatory)` in `SKILL.md`.

| Output Contract item | Canonical path | Template source | Status |
| --- | --- | --- | --- |
| project `MEMORY.md` | `projects/aigc/<项目名>/MEMORY.md` | `templates/project-memory.template.md` | local |
| project `CHANGELOG.md` | `projects/aigc/<项目名>/CHANGELOG.md` | `templates/project-changelog.template.md` | local |
| project `CONTEXT/README.md` | `projects/aigc/<项目名>/CONTEXT/README.md` | `templates/project-context-readme.template.md` | local helper for non-empty context root |
| project `STATE.json` | `projects/aigc/<项目名>/STATE.json` | `templates/state.template.json` | local |
| north star | `projects/aigc/<项目名>/0-初始化/north_star.yaml` | `templates/north-star.template.yaml` | local |
| init handoff | `projects/aigc/<项目名>/0-初始化/init_handoff.yaml` | `templates/init-handoff.template.yaml` | local |
| final user-facing response | chat response | `templates/output-template.md` | local |
| story source manifest | `projects/aigc/<项目名>/0-初始化/story-source-manifest.yaml` | `.agents/skills/aigc/_shared/story-source-manifest.template.yaml` | shared |
| team manifest | `projects/aigc/<项目名>/team.yaml` | `.agents/skills/aigc/_shared/council-runtime/team.template.yaml` | shared |
| governance state | `projects/aigc/<项目名>/governance-state.yaml` | `.agents/skills/aigc/_shared/governance-state.template.yaml` | shared, lazy |
| other lazy governance carriers | `mandate.yaml`, `mission-brief.yaml`, `route-plan.yaml`, `preflight-verdict.yaml`, `validation-report.md`, `learning-record.md` | generated only when triggered by `references/artifacts-and-sources.md` and `review/init-review-gate.md` | lazy |

## Alignment Rules

- `north-star.template.yaml` must not contain live route fields such as `recommended_next_stage`, `recommended_entry_path`, `stage_entry_contract`, or `rebootstrap_status`.
- `init-handoff.template.yaml` may carry initialization-round handoff seeds and `recommended_next_stage`, but live route path belongs to `STATE.json`.
- `state.template.json` is the default live route carrier for the lightweight initialization state.
- Shared templates must not be copied locally unless the shared contract changes owner.
