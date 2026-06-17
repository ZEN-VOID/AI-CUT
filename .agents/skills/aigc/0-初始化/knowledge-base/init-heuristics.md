# Init Heuristics

This knowledge-base file keeps stable heuristics that are useful while reading or maintaining `$aigc-init`. New operational failures should first be recorded in same-directory `CONTEXT.md`; promote here only when stable and reusable.

## Stable Heuristics

- The hardest part of initialization is separating durable project memory from stage-entry artifacts and live route state.
- Project `MEMORY.md` is the initialization context hub: user requirements, team configuration, reference absorption summaries, constraints, exclusions, and downstream context guidance belong there.
- If a field affects live route state, it belongs in `STATE.json` or `governance-state.yaml`, not in project memory or aesthetic outputs.
- `team.yaml` is legacy-only evidence. New initialization writes user-specified team context into `MEMORY.md`, not into a separate lineup carrier.
- Team context in memory is a reading lens and constraint source, not permission to call team personas or fabricate advisor answers.
- Source-light initialization is allowed, but it must be humble: production and tone boundaries are safe; concrete story facts are not.
- Once a real source arrives, first reconcile initialization artifacts before running downstream stages.
- `Assets/` is an asset library, not a phase output owner.
- Empty phase directories are runtime readiness, not execution evidence.
- Rebootstrap should feel like business reset with preservation, not filesystem erasure.

## Common Failure Patterns

| symptom | likely cause | prevention |
| --- | --- | --- |
| style or project-memory files contain next-stage route fields | route/state truth mixed into long-term constraints | keep live route in `STATE.json` or `governance-state.yaml`; keep aesthetics in `2-美学` |
| initialization asks for `auto/custom` team choice | legacy team topology revived | write user team preferences directly into `MEMORY.md`; do not create `team.yaml` |
| user supplied references are only placed under `CONTEXT/` | context sidecar mistaken for memory hub | write a concise absorption summary and downstream use boundary into `MEMORY.md` |
| creative stage tries to call team member personas | old `roles.supervision.stage_profiles` runtime survived migration | consume project `MEMORY.md` team/context sections as read-only guidance and block persona dispatch |
| source-light project has detailed plot | assistant or advisor inference promoted too early | force story facts into `unknowns` until source is ready |
| resume request is treated as rebootstrap | task classification skipped | N0 must decide "continue current direction" vs "restart direction" |
| old downstream outputs influence a reset | archive/stale scope not enforced | write reset bridge before reading old outputs |

## Maintenance Heuristics

- If a rule changes node order, update `SKILL.md`, `steps/init-workflow.md`, and `review/init-review-gate.md` together.
- If a rule changes path layout, update `references/scope-and-runtime.md`, shared project runtime layout, and the AIGC audit script together.
- If a rule changes output field boundaries, update templates and pass table together.
- Keep `CONTEXT.md` experience-oriented. Do not turn it into a migration timeline; use `CHANGELOG.md` for that.
