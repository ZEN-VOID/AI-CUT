# Mode And Team Contract

This file owns initialization mode, lineup selection, team manifest requirements, advisor scope, and prompt-packet boundaries.

## Initialization Mode

| mode | trigger | execution shape | foreground interaction | team truth | execution owner | 顾问与复核流程 |
| --- | --- | --- | --- | --- | --- | --- |
| `smart_advisor` | All first initialization and rebootstrap runs | Lock `auto/custom`, form or validate team, run fixed direct-answer packet, synthesize | yes | project `team.yaml` | `roles.planning` | required |

Legacy `主创会诊模式 / 快速成案模式 / 自主问答模式` are not valid modes.

## Lineup Submodes

| submode | user action | source | allowed input | output |
| --- | --- | --- | --- | --- |
| `auto` | user chooses or explicitly requests auto lineup | `.agents/skills/team/` root index, then shortlisted deep reads | source material, goals, constraints, genre, references | `team_manifest_patch`, `selection_rationale`, optional roster-gap todo |
| `custom` | user specifies the lineup | user-selected members under `.agents/skills/team/` | names, paths, departments, role assignments | `team_manifest_patch`, `custom_lineup_validation_note` |

## Mode Lock Gate

1. If the user has not clearly chosen `auto` or `custom`, show `templates/init-option-card.template.md` and stop.
2. A project name, film title, logline, or short brief is not enough to infer `auto`.
3. A recommendation can be shown as `pending_recommendation`, but it is not a locked lineup.
4. Before mode lock, contract reading, template checking, and risk diagnosis are allowed; canonical artifact drafting is not.
5. If the session resumes before lock, the first action is to re-present the option card.

## Team Manifest

Project team truth is:

```text
projects/aigc/<项目名>/team.yaml
```

It must include:

- `init_contract.init_mode == smart_advisor`
- `init_contract.team_lineup_mode == auto|custom`
- `init_contract.selector_scope_root == ".agents/skills/team/"`
- `runtime_policy.require_advisor_review_for_init_execution == true`
- `runtime_policy.init_execution_owner_role == planning`
- `runtime_policy.team_identity_usage == init_only`
- `runtime_policy.creative_stage_persona_dispatch_allowed == false`
- `roles.planning.init_execution.*`
- `init_synthesis.stage_seed_summary` for `1-分集 / 2-编导 / 3-运动 / 4-摄影 / 5-分组 / 6-设计`

Hard rules:

1. `team.yaml` is the initialization lineup, role-skill Q&A provenance, and synthesis record only; it is not a creative-stage advisor runtime.
2. Team member role identity skills may be invoked only inside `0-初始化` to answer the fixed initialization packet and supply synthesis inputs.
3. `roles.*.members` may only reference `.agents/skills/team/` skills.
4. `roles.planning.init_execution.kickoff_owner` and `requires_advisor_review` must be true.
5. New writes must not create active `roles.supervision.stage_profiles`, `roles.supervising.*`, `roles.production.*`, `team_setup.shared_agents`, `dispatch_policy: stage-front-advisor`, or `dispatch_policy: leaf-advisor` as creative-stage runtime contracts.
6. If legacy projects already contain those fields, keep them read-only under `legacy_compat` or report them as deprecated evidence; do not use them to dispatch creative-stage persona work.
7. Later creative stages may read only frozen synthesis fields such as `init_synthesis.stage_seed_summary.<stage>` and `init_handoff.stage_entry_seeds.<stage>`; they must not re-open team role skills or imitate member identities locally.
8. Auto and custom selection still write department coverage, selected members, selection rationale, known gaps, and todo recommendation paths, but the downstream payload is stage guidance summary rather than stage advisor profiles.

## Initialization Role Matrix

| role | owned phase | timing | core function | non-owner boundary |
| --- | --- | --- | --- | --- |
| `策划` | `0-初始化` | first direct-answer packet before synthesis | converge story core, emotional core, boundaries, and stage seeds | does not own later-stage canonical truth |
| `初始化专业顾问` | `0-初始化` | selected by auto/custom lineup, before synthesis | answer role-specific initialization questions and expose useful risks or taste constraints | does not become a later-stage persona or advisor runtime |
| `初始化复核` | `0-初始化` | before artifact writeback | check whether Q&A synthesis supports `north_star`, `init_handoff`, `STATE`, and seed summaries | does not own image/video/review runtime gates |

## Auto Lineup Selection

Auto lineup uses two-level selection:

1. Read `.agents/skills/team/SKILL.md + CONTEXT.md` first.
2. Build a root-index shortlist by department, member, and scenario tags.
3. Lock initialization ownership only: `策划 / 初始化专业顾问 / 初始化复核 -> 0-初始化`.
4. Select members only from `.agents/skills/team/`, prioritizing the required departments.
5. Deep-read only shortlisted member skills.
6. Summarize every selected member's answer into `init_synthesis.stage_seed_summary` instead of writing creative-stage persona profiles.

Required departments:

| department | default | minimum | role |
| --- | --- | --- | --- |
| `导演组` | required | at least 1 | expression, staging, narrative stance |
| `设计组` | required | at least 1 | world, character, scene, prop, material systems |
| `摄影组` | required | at least 1 | light, distance, camera motion, photographic texture |

Optional departments are triggered by genre, medium, difficulty, or explicit user request: `小说组`, `演员组`, `武术组`, `美学组`, `动漫组`.

Auto selection rationale must explain:

- why required departments form the minimum closure
- why the chosen members fit or complement each other
- how each selected role contributes to the initialization direct-answer packet
- why optional departments were included or skipped
- current roster gaps
- root-index scenario tags and candidate shortlist evidence
- how member answers were compressed into `north_star` invariants and `init_handoff` stage-entry seeds

If the current roster is adequate but visibly missing a better domain expert, continue with the available lineup and create `todos/<project-or-task-id>-team-recommendation.md`; record that path in `team_setup.recommendation_todo_paths`.

## Custom Lineup Selection

Custom lineup must:

- validate every requested member path under `.agents/skills/team/`
- map members into `策划 / 初始化专业顾问 / 初始化复核`
- record user evidence and any coverage gaps
- warn when required departments are not covered
- refuse external advisor paths unless the user first adds them as proper team skills
- refuse requests that would keep the selected members active as creative-stage persona/subagent presets after initialization, unless the user explicitly changes the workflow contract.

## Prompt Packet

The first prompt packet belongs to the parent skill and is answered by `roles.planning.members`:

1. project name or working title
2. delivery form: short film, PV, trailer, concept film, feature, series fragment, etc.
3. story core or emotional core
4. target audience, platform, and use case
5. style references and aesthetic exclusions
6. production constraints: duration, resources, quality tier, toolchain, time
7. preferred next stage
8. IP, content, and adaptation boundaries

Only ask for blockers that affect `north_star` or initial stage-entry seeds. Anything better resolved downstream goes into `unknowns`.

## Review Gate Mapping

| Review Question | Review Gate | Fail Code | Rework Target | Report Evidence |
| --- | --- | --- | --- | --- |
| Is `smart_advisor` the only valid initialization mode, with legacy `主创会诊模式 / 快速成案模式 / 自主问答模式` rejected rather than revived as parallel modes? | `FIELD-INIT-03` | `FAIL-INIT-03` | `steps/init-workflow.md` `N1-mode-gate`; `SKILL.md` `Mode Selection`; this file's `Initialization Mode` section | Review report records the locked `init_mode`, any legacy mode wording found, and the file or artifact where the invalid mode appeared. |
| Is exactly one `team_lineup_mode` locked as `auto` or `custom` before any canonical initialization artifact is drafted, with recommendation text kept separate from lock evidence? | `FIELD-INIT-03` | `FAIL-INIT-03` | `steps/init-workflow.md` `N1-mode-gate`; `templates/init-option-card.template.md`; this file's `Mode Lock Gate` section | Review report cites `lineup_mode_decision` or option-card output and confirms whether `north_star`, `init_handoff`, `team.yaml`, and `STATE.json` drafting waited for the lock. |
| Does `team.yaml` record `init_contract`, selector scope, runtime policy, planning execution owner, initialization role ownership, Q&A provenance, stage seed summaries, and the explicit ban on creative-stage persona dispatch? | `FIELD-INIT-04` | `FAIL-INIT-04` | `steps/init-workflow.md` `N3-internal-router`, `N4-mode-engine`, and `N5-synthesis`; `.agents/skills/aigc/_shared/council-runtime/team.template.yaml`; this file's `Team Manifest` and `Initialization Role Matrix` sections | Review report lists present or missing `team.yaml` keys, deprecated stage-runtime fields, role allocation mode, init synthesis fields, and planning direct-answer provenance. |
| In auto lineup, did selection start from `.agents/skills/team/SKILL.md + CONTEXT.md`, build a shortlist, deep-read only shortlisted members, keep all member paths under `.agents/skills/team/`, cover required departments, and record roster gaps? | `FIELD-INIT-04` | `FAIL-INIT-04` | `steps/init-workflow.md` `N3-internal-router` and `N4-mode-engine`; this file's `Auto Lineup Selection` section; project `todos/*-team-recommendation.md` when needed | Review report cites root-index shortlist evidence, selected member paths, required department coverage, optional department rationale, and any created roster-gap todo path. |
| In custom lineup, are all requested members validated under `.agents/skills/team/`, mapped into initialization-only roles, and refused or blocked if they point outside the team tree or request post-init persona dispatch? | `FIELD-INIT-04` | `FAIL-INIT-04` | `steps/init-workflow.md` `N3-internal-router` and `N4-mode-engine`; this file's `Custom Lineup Selection` section | Review report lists each requested member path, validation result, assigned initialization role, coverage gap warning, external advisor refusal, and any post-init persona-dispatch refusal. |
| Does the first prompt packet remain owned by the parent skill, answered by `roles.planning.members`, and limited to blockers that affect `north_star` or initial stage-entry seeds? | `FIELD-INIT-07` | `FAIL-INIT-07` | `steps/init-workflow.md` `N4-mode-engine`; this file's `Prompt Packet` section; `templates/output-template.md` blocked-output shape when advisor review is unavailable | Review report records prompt packet topics, planning member response provenance, blocked downstream-only questions moved to `unknowns`, and any local imitation attempt. |
| Does this reference itself keep every mandatory mode/team rule bound to a review gate, fail code, rework target, and report evidence row? | `FIELD-INIT-10` | `FAIL-INIT-10` | This `Review Gate Mapping` section; `review/init-review-gate.md`; `steps/init-workflow.md` | Maintenance report enumerates this file in the reference gate coverage list and confirms every mode, lineup, team, auto/custom, and prompt-packet rule above is represented. |
