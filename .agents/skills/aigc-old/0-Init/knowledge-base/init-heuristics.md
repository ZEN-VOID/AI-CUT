# Init Heuristics

This knowledge-base file keeps stable heuristics that are useful while reading or maintaining `$aigc-init`. New operational failures should first be recorded in same-directory `CONTEXT.md`; promote here only when stable and reusable.

## Stable Heuristics

- The hardest part of initialization is separating long-lived north-star truth from stage-entry handoff seeds.
- If a field affects live route state, it belongs in `STATE.json` or `governance-state.yaml`, not `north_star.yaml`.
- `team.yaml` is both a lineup truth and a later-stage council runtime; role ownership and phase scope must be explicit.
- In auto lineup, read the team root index first. Directly deep-reading the full team tree is slow and tends to hide stale root-index drift.
- `策划 / 监制 / 评审` are governance roles, not necessarily three mutually exclusive human groups.
- Source-light initialization is allowed, but it must be humble: production and tone boundaries are safe; concrete story facts are not.
- Once a real source arrives, first reconcile initialization artifacts before running downstream stages.
- `Assets/` is an asset library, not a phase output owner.
- Empty phase directories are runtime readiness, not execution evidence.
- Rebootstrap should feel like business reset with preservation, not filesystem erasure.

## Common Failure Patterns

| symptom | likely cause | prevention |
| --- | --- | --- |
| `north_star.yaml` contains next-stage route fields | route/state truth mixed into long-term constraints | keep stage entry in `init_handoff`, live route in `STATE.json` |
| initialization starts without `auto/custom` | recommendation mistaken for lock | require mode lock note or option card |
| advisor selected from outside team tree | custom path or auto scan escaped selector root | validate every member path before `team.yaml` writeback |
| source-light project has detailed plot | assistant or advisor inference promoted too early | force story facts into `unknowns` until source is ready |
| resume request is treated as rebootstrap | task classification skipped | N0 must decide "continue current direction" vs "restart direction" |
| old downstream outputs influence a reset | archive/stale scope not enforced | write reset bridge before reading old outputs |

## Maintenance Heuristics

- If a rule changes node order, update `SKILL.md`, `steps/init-workflow.md`, and `review/init-review-gate.md` together.
- If a rule changes path layout, update `references/scope-and-runtime.md`, shared project runtime layout, and the AIGC audit script together.
- If a rule changes output field boundaries, update templates and pass table together.
- Keep `CONTEXT.md` experience-oriented. Do not turn it into a migration timeline; use `CHANGELOG.md` for that.
