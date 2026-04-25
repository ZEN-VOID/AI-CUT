# Init Type Map

This file owns type variables and route selection for `$aigc-init`.

## Type Profile

| variable | allowed values | meaning |
| --- | --- | --- |
| `task_type` | `first_init`, `rebootstrap`, `resume_or_query` | entry classification |
| `lineup_type` | `auto`, `custom`, `unlocked` | team formation route |
| `source_profile` | `source-light`, `source-grounded`, `source-reconcile` | source readiness behavior |
| `reset_profile` | `none`, `refresh_reset`, `archive_reset`, `purge_reset` | reset scope |
| `governance_profile` | `minimal`, `lazy_triggered`, `harness_extended` | sidecar scope |
| `execution_profile` | `subagent_required`, `local_diagnosis_only` | whether business execution may proceed |

## Routing Matrix

| signal | type output | step impact | reference impact | review impact |
| --- | --- | --- | --- | --- |
| no existing project root or user asks to create project | `task_type=first_init` | enter `N0 -> N1` | load `scope-and-runtime`, `mode-and-team` | full sufficiency gate |
| user asks to return to init, restart direction, rebuild north star | `task_type=rebootstrap` | enter `N0`, then reset planning before `N1` | load `rebootstrap-contract` | require `FIELD-INIT-08` |
| user asks to continue, query, repair checkpoint | `task_type=resume_or_query` | exit to `resume/` or root `aigc` | no init artifacts | do not run init gate |
| no `auto/custom` decision | `lineup_type=unlocked` | stop at `N1` | show option card template | no artifact drafting |
| explicit auto | `lineup_type=auto` | `N4` auto path | root team index first | required department coverage |
| explicit custom | `lineup_type=custom` | `N4` custom path | validate team skill paths | coverage/gap note |
| `primary_story_source.status != ready` | `source_profile=source-light` | synthesize only boundary constraints | load source completeness gate | fail story overclaims |
| source text or formal synopsis covers target | `source_profile=source-grounded` | story-facing seeds allowed with provenance | load source manifest contract | verify source coverage |
| true source arrives after source-light init | `source_profile=source-reconcile` | reconcile before downstream | load reconciliation contract | fail stale inferred plot |
| governance explicitly requested or high-risk execution | `governance_profile=lazy_triggered` | `N6` sidecars | load lazy governance | sidecar alignment check |

## Anti-Patterns

- Treating `auto` as locked because it is recommended.
- Letting `custom` members point outside `.agents/skills/team/`.
- Writing plot facts in source-light mode.
- Treating empty runtime directories as phase execution evidence.
- Using `archive_reset` to delete source or original assets.
- Running local direct-answer simulation when actual initialization requires planning subagents.

## Fusion With Steps

1. `N0` creates `task_type` and `reset_profile`.
2. `N1` resolves `lineup_type`.
3. `N3` resolves `source_profile` and context budget.
4. `N5` consumes `source_profile` to decide which fields may be stable truth.
5. `N6` consumes `governance_profile`.
6. `N7` maps failures to field IDs and reentry nodes.
