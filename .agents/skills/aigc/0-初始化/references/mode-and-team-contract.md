# Mode And Team Contract

This file owns initialization mode, lineup selection, team manifest requirements, advisor scope, and prompt-packet boundaries.

## Initialization Mode

| mode | trigger | execution shape | foreground interaction | team truth | execution owner | subagents |
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
- `runtime_policy.require_subagents_for_init_execution == true`
- `runtime_policy.init_execution_owner_role == planning`
- `roles.planning.init_execution.*`

Hard rules:

1. `team.yaml` is both the phase advisor runtime and the initialization lineup truth.
2. Auto selection writes governance role ownership, required department coverage, optional department decisions, known gaps, and todo recommendation paths.
3. Custom selection writes user-specified lineup evidence and validation notes.
4. `roles.*.members` may only reference `.agents/skills/team/` skills.
5. `roles.planning.init_execution.kickoff_owner` and `requires_subagents` must be true.
6. `策划 / 监制 / 评审` may overlap or be separated; record the chosen allocation mode and overlap notes.

## Governance Role Matrix

| role | owned phase | timing | core function | non-owner boundary |
| --- | --- | --- | --- | --- |
| `策划` | `0-初始化` | first direct-answer packet before synthesis | converge story core, emotional core, boundaries, and stage seeds | does not own later-stage canonical truth |
| `监制` | `2-编导`, `3-摄影`, `4-设计`, `5-分组` | stage-front advisory | style, type, director intent, feasibility, design continuity | does not replace stage canonical writeback |
| `评审` | `6-图像`, `7-视频` | around validation reports | image/video consistency, reference binding, provider risk, delivery gate | not a default early creative expansion role |

## Auto Lineup Selection

Auto lineup uses two-level selection:

1. Read `.agents/skills/team/SKILL.md + CONTEXT.md` first.
2. Build a root-index shortlist by department, member, and scenario tags.
3. Lock governance role ownership: `策划 -> 0-初始化`, `监制 -> 2-编导/3-摄影/4-设计/5-分组`, `评审 -> 6-图像/7-视频`.
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
