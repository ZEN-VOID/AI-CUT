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
- `roles.planning.init_execution.*`
- `roles.supervision.stage_profiles` for at least `2-编剧 / 3-导演 / 4-表演 / 5-摄影 / 7-设计`

Hard rules:

1. `team.yaml` is both the phase advisor runtime and the initialization lineup truth.
2. Auto selection writes governance role ownership, required department coverage, optional department decisions, known gaps, and todo recommendation paths.
3. Custom selection writes user-specified lineup evidence and validation notes.
4. `roles.*.members` may only reference `.agents/skills/team/` skills.
5. `roles.planning.init_execution.kickoff_owner` and `requires_advisor_review` must be true.
6. `策划 / 监制 / 评审` may overlap or be separated; record the chosen allocation mode and overlap notes.
7. `roles.supervision.stage_profiles.<stage>` is the canonical later-stage advisor profile. Generic `roles.supervision.members`, old `roles.supervising.*`, old `roles.production.*`, `team_setup.shared_agents`, and `roles.planning.members` are only fallback compatibility paths.
8. Stage profiles must record `preferred_departments`, `focus_tags`, `question_binding`, and `dispatch_policy`, so later skills can ask node-derived questions without guessing what "监制" means for that stage.

## Governance Role Matrix

| role | owned phase | timing | core function | non-owner boundary |
| --- | --- | --- | --- | --- |
| `策划` | `0-初始化` | first direct-answer packet before synthesis | converge story core, emotional core, boundaries, and stage seeds | does not own later-stage canonical truth |
| `监制` | `2-编剧`, `3-导演`, `4-表演`, `5-摄影`, `6-分组`, `7-设计` | stage-front advisory, refined by `roles.supervision.stage_profiles.<stage>` | stage-specific style, type, director intent, performance craft, feasibility, design continuity | does not replace stage canonical writeback |
| `评审` | `8-图像`, `9-视频`, `10-审片` | around validation reports and generated footage review | image/video consistency, reference binding, provider risk, footage delivery gate | not a default early creative expansion role |

## Auto Lineup Selection

Auto lineup uses two-level selection:

1. Read `.agents/skills/team/SKILL.md + CONTEXT.md` first.
2. Build a root-index shortlist by department, member, and scenario tags.
3. Lock governance role ownership: `策划 -> 0-初始化`, `监制 -> 2-编剧/3-导演/4-表演/5-摄影/6-分组/7-设计`, `评审 -> 8-图像/9-视频/10-审片`.
4. Select members only from `.agents/skills/team/`, prioritizing the required departments.
5. Deep-read only shortlisted member skills.

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
- whether this is overlap or separated governance
- why optional departments were included or skipped
- current roster gaps
- root-index scenario tags and candidate shortlist evidence

If the current roster is adequate but visibly missing a better domain expert, continue with the available lineup and create `todos/<project-or-task-id>-team-recommendation.md`; record that path in `team_setup.recommendation_todo_paths`.

## Custom Lineup Selection

Custom lineup must:

- validate every requested member path under `.agents/skills/team/`
- map members into `策划 / 监制 / 评审`
- record user evidence and any coverage gaps
- warn when required departments are not covered
- refuse external advisor paths unless the user first adds them as proper team skills

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
| Does `team.yaml` record `init_contract`, selector scope, runtime policy, planning execution owner, role ownership, and required stage profiles for later supervision? | `FIELD-INIT-04` | `FAIL-INIT-04` | `steps/init-workflow.md` `N3-internal-router`, `N4-mode-engine`, and `N5-synthesis`; `.agents/skills/aigc/_shared/council-runtime/team.template.yaml`; this file's `Team Manifest` and `Governance Role Matrix` sections | Review report lists present or missing `team.yaml` keys, stage profiles, role allocation mode, overlap notes, and planning direct-answer provenance. |
| In auto lineup, did selection start from `.agents/skills/team/SKILL.md + CONTEXT.md`, build a shortlist, deep-read only shortlisted members, keep all member paths under `.agents/skills/team/`, cover required departments, and record roster gaps? | `FIELD-INIT-04` | `FAIL-INIT-04` | `steps/init-workflow.md` `N3-internal-router` and `N4-mode-engine`; this file's `Auto Lineup Selection` section; project `todos/*-team-recommendation.md` when needed | Review report cites root-index shortlist evidence, selected member paths, required department coverage, optional department rationale, and any created roster-gap todo path. |
| In custom lineup, are all requested members validated under `.agents/skills/team/`, mapped into `策划 / 监制 / 评审`, and refused or blocked if they point outside the team tree? | `FIELD-INIT-04` | `FAIL-INIT-04` | `steps/init-workflow.md` `N3-internal-router` and `N4-mode-engine`; this file's `Custom Lineup Selection` section | Review report lists each requested member path, validation result, assigned governance role, coverage gap warning, and any external advisor refusal. |
| Does the first prompt packet remain owned by the parent skill, answered by `roles.planning.members`, and limited to blockers that affect `north_star` or initial stage-entry seeds? | `FIELD-INIT-07` | `FAIL-INIT-07` | `steps/init-workflow.md` `N4-mode-engine`; this file's `Prompt Packet` section; `templates/output-template.md` blocked-output shape when advisor review is unavailable | Review report records prompt packet topics, planning member response provenance, blocked downstream-only questions moved to `unknowns`, and any local imitation attempt. |
| Does this reference itself keep every mandatory mode/team rule bound to a review gate, fail code, rework target, and report evidence row? | `FIELD-INIT-10` | `FAIL-INIT-10` | This `Review Gate Mapping` section; `review/init-review-gate.md`; `steps/init-workflow.md` | Maintenance report enumerates this file in the reference gate coverage list and confirms every mode, lineup, team, auto/custom, and prompt-packet rule above is represented. |
