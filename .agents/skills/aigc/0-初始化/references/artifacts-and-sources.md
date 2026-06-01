# Artifacts And Sources Contract

This file owns initialization artifacts, source readiness, north-star boundaries, stage-entry ownership, synthesis, and lazy governance.

## Core Artifacts

- `projects/aigc/<项目名>/0-初始化/north_star.yaml`
- `projects/aigc/<项目名>/0-初始化/init_handoff.yaml`
- `projects/aigc/<项目名>/0-初始化/story-source-manifest.yaml`
- `projects/aigc/<项目名>/team.yaml`
- `projects/aigc/<项目名>/STATE.json`

## North Star

Read:

- `templates/north-star.template.yaml`
- `templates/init-handoff.template.yaml`
- `templates/project-memory.template.md`
- `templates/project-changelog.template.md`
- `templates/project-context-readme.template.md`
- `templates/state.template.json`
- `templates/output-template-map.md`
- `.agents/skills/aigc/_shared/council-runtime/team.template.yaml`
- `.agents/skills/aigc/_shared/story-source-manifest.template.yaml`
- `.agents/skills/aigc/_shared/project-runtime-layout.md`

Rules:

1. `north_star.yaml` only carries long-lived project constraints.
2. `north_star.yaml` directly owns the exact global-design blocks `全局风格 / 细分风格 / 类型元素 / 世界观`.
3. `全局风格` owns the whole-work style contract. It is a union-style guidance field for the entire work collection, not the old cross-design intersection prefix. It may contain `媒介属性 / 时代属性 / 光影逻辑 / 画面质感 / 场景化风格策略 / 避免出现 / 全局风格提示词`.
4. `全局风格` must separate reusable style logic from one-off plot facts. It may include conditional scene-type rules for interiors/exteriors/action/night/day/crowd/dialogue/ritual/battle and similar reusable categories, including matching light, color, texture, atmosphere, camera, motion, material, and negative-style constraints; it must not include a single later-stage shot ID, one-off composition, character-only costume detail, prop-only design, or scene fact that belongs exclusively to a downstream asset file.
5. `全局风格` defaults to Chinese; the generated `全局风格提示词` is a natural paragraph, usually 300-500 Chinese characters, and must explicitly include the current `全局风格.媒介属性` value, preferably as the prompt prefix. It should explain which scene types use which matching lighting and color strategy, instead of deleting light/color detail for being scene-sensitive.
6. `类型元素` defaults to Chinese, and the generated `类型元素提示词` must stay within 30 Chinese characters.
7. `细分风格` owns domain-specific style guidance: `画面风格 / 服装风格 / 建筑风格 / 物品风格`. Ancient architecture guidance must not force-fit modern architects or modernist labels unless the project explicitly calls for it.
8. `画面风格` defaults to Chinese and describes the unified picture style; it may echo the whole-work light/color logic at a high level, but the fuller scene-type matrix belongs in `全局风格.全局风格提示词` or `全局风格.场景化风格策略`.
9. `服装风格 / 建筑风格 / 物品风格` default to Chinese and remain concise domain guidance; they can inherit the whole-work material/texture rules without becoming the owner of global style.
10. `创作阶段不变量` owns durable constraints for `2-编导 / 3-运动 / 4-摄影 / 5-分组 / 6-设计`; it may absorb initialization team synthesis, but it must not contain live route truth, stage status, single-shot facts, or post-init team persona dispatch rules.
11. Do not duplicate global-design fields in old umbrella slots such as `aesthetic_axes`, `genre_corridor`, `theme_promises`, or `tone_keywords`.
12. `init_handoff.yaml` carries stage-entry seeds, source layers, and unknowns.
13. Session-only information does not belong in `north_star.yaml`.
14. `north_star.yaml` must not contain route truth or `rebootstrap` process state.

## Stage Entry Ownership

1. Initialization-round stage seed: `init_handoff.yaml.project_contract.recommended_next_stage`.
2. Current live route truth: `STATE.json.recommended_next_stage`, `recommended_entry_path`, and `recommended_next_step`.
3. Creative-stage entry seed names are `episode_split_seed`, `writing_directing_seed`, `motion_seed`, `cinematography_seed`, `grouping_seed`, and `design_seed`; image/video/review hints belong under `post_creative_handoff`.
4. If present, `governance-state.yaml.resume_contract.*` is the structured resume truth for `query`, `resume`, and high-risk gates.
5. After the project leaves `0-初始化`, `init_handoff.yaml` remains historical handoff seed and no longer owns live current-stage truth.

## Adaptation And Pacing Seed

1. `original_adherence` is boolean.
2. If the user does not request original adherence, preserve order, or structural fidelity, default `original_adherence: false`.
3. `reorder_authorization` must state the action stance.
4. Long-term adaptation policy belongs to `north_star.yaml`; executable pacing seeds belong to `init_handoff.yaml`.

## Story Source Manifest

Canonical source manifest:

```text
projects/aigc/<项目名>/0-初始化/story-source-manifest.yaml
```

Rules:

1. Always create `story-source-manifest.yaml`, even when no source text exists yet.
2. Only `primary_story_source` decides formal entry readiness.
3. Other materials are `development_briefs`.
4. If `primary_story_source.status != ready`, write `blocking_reason` and `required_user_action`.
5. Partial source coverage must distinguish incremental planning from formal full-season/whole-work completion.

## Story Source Completeness Gate

`source-light bootstrap`:

- condition: `primary_story_source.status != ready`
- allowed: runtime skeleton, `team.yaml`, source manifest, lightweight `STATE.json`, and genre/tone/audience/production/boundary constraints
- forbidden: invented plot events, character relations, conflict mechanics, episode beats, scene pools, object pools, or world rules as facts

`source-grounded bootstrap`:

- condition: source text or formal synopsis covers the target planning range
- allowed: source-backed story-facing seeds marked with coverage and provenance

Hard rules:

1. Missing source means story-facing sections become `unknowns`, `deferred_to_*`, or `risk_notes`.
2. Advisor or assistant guesses are never promoted to stable story truth in source-light mode.
3. If the user wants to start without source, the next action must explicitly include source/synopsis completion.

## Story Source Reconciliation

If a true source arrives after source-light initialization, first reconcile:

- `0-初始化/north_star.yaml`
- `0-初始化/init_handoff.yaml`
- `STATE.json`

Priority:

`story source user truth > user explicit confirmation > council_advised > assistant_inferred`

Conflicting assistant-inferred story fields must be rewritten before entering `1-分集`, `2-编导`, or later stages.

For `primary_story_source.source_type == storyboard_script`, `preset_registry[].lock_level` may only be `hard_lock`, `soft_lock`, or `reference_only`.

## Lazy Governance

Always required:

- `north_star.yaml`
- `init_handoff.yaml`
- `story-source-manifest.yaml`
- `team.yaml`
- `STATE.json`

Triggered only when needed:

- `governance-state.yaml`
- `mandate.yaml`
- `mission-brief.yaml`
- `route-plan.yaml`
- `preflight-verdict.yaml`
- `validation-report.md`
- `learning-record.md`

Triggers:

1. user requests governance, audit, resume, review, or retrospective
2. the task is about to enter complex multi-step execution
3. high-risk execution needs a preflight verdict
4. `query`, `resume`, or root `aigc` gates need a structured checkpoint
5. rebootstrap needs a reset trace

## Synthesis

1. The parent skill only absorbs patches from the selected path: route plan, team formation, planning direct-answer packets, and audit report.
2. Unselected paths must not receive placeholder fields.
3. Write provenance as `user_confirmed`, `council_advised`, or `assistant_inferred`.
4. Record `team_ref`, source breakdown, planning direct-answer provenance, and one next-stage entry.
5. Source-light story-level inferences stay provisional.
6. If source and old seed conflict, reconcile before final writeback.
7. In rebootstrap, consume reset scope, archive plan, and stale notes before reading old project artifacts as input.
8. `team.yaml` must be locked before `north_star.yaml` and `init_handoff.yaml`.

## Review Gate Mapping

| Review Question | Review Gate | Fail Code | Rework Target | Report Evidence |
| --- | --- | --- | --- | --- |
| Does `north_star.yaml` contain only durable project constraints, including `创作阶段不变量`, and does it exclude live route truth, session-only notes, `rebootstrap` process state, and post-init team persona dispatch rules? | `FIELD-INIT-01` | `FAIL-INIT-01` | `steps/init-workflow.md` `N5-synthesis`; `templates/north-star.template.yaml`; this file's `North Star` and `Stage Entry Ownership` sections | Review report cites the inspected `north_star.yaml` path, stage invariant coverage, and any forbidden route/session/reset/persona-runtime fields found or confirms none were present. |
| Does `north_star.yaml` carry the exact `全局风格 / 细分风格 / 类型元素 / 世界观` blocks, with `全局风格` as a whole-work union-style contract and `全局风格提示词` explicitly containing `全局风格.媒介属性`? | `FIELD-INIT-01G` | `FAIL-INIT-01G` | `steps/init-workflow.md` `N4-mode-engine` and `N5-synthesis`; `templates/north-star.template.yaml`; this file's `North Star` section | Review report quotes or summarizes the four global design blocks, the medium-bearing prompt sentence, prompt length condition, and any missing or misplaced style logic. |
| Does `init_handoff.yaml` own the current seed set for `1-分集 / 2-编导 / 3-运动 / 4-摄影 / 5-分组 / 6-设计`, source layers, unknowns, post-creative handoff hints, and initialization-round next-stage seed without stealing live route truth from `STATE.json`? | `FIELD-INIT-02` | `FAIL-INIT-02` | `steps/init-workflow.md` `N5-synthesis`; `templates/init-handoff.template.yaml`; this file's `Stage Entry Ownership` section | Review report compares `init_handoff.yaml.project_contract.recommended_next_stage` with `STATE.json` for the init completion turn, lists present seed keys, and records any stale or duplicated route truth. |
| Does `story-source-manifest.yaml` always exist, use `primary_story_source` as the sole formal readiness owner, keep source-light story facts provisional, and reconcile late true source before downstream entry? | `FIELD-INIT-02S` | `FAIL-INIT-02S` | `steps/init-workflow.md` `N3-internal-router`, `N5-synthesis`, and `N7-internal-audit`; `.agents/skills/aigc/_shared/story-source-manifest.template.yaml`; this file's `Story Source Manifest`, `Story Source Completeness Gate`, and `Story Source Reconciliation` sections | Review report records manifest path, `primary_story_source.status`, blocking reason or coverage evidence, source-light unknown/deferred/risk fields, and any reconciliation diff required before downstream work. |
| If `primary_story_source.source_type == storyboard_script`, are all `preset_registry[].lock_level` values limited to `hard_lock`, `soft_lock`, or `reference_only`? | `FIELD-INIT-02S` | `FAIL-INIT-02S` | `steps/init-workflow.md` `N3-internal-router` and `N5-synthesis`; `.agents/skills/aigc/_shared/story-source-manifest.template.yaml`; this file's `Story Source Reconciliation` section | Review report lists the observed `preset_registry[].lock_level` values or states that no storyboard-script preset registry was present. |
| Are lazy governance carriers created only when triggered, while the core five-piece set remains the always-required initialization output? | `FIELD-INIT-05` | `FAIL-INIT-05` | `steps/init-workflow.md` `N6-lazy-governance`; `templates/output-template-map.md`; this file's `Lazy Governance` section | Review report lists created governance sidecars, their trigger reason, and confirms absent sidecars were not required for structural completeness alone. |
| Does synthesis absorb only the selected path's patches, preserve provenance as `user_confirmed / council_advised / assistant_inferred`, and lock `team.yaml` before `north_star.yaml` and `init_handoff.yaml`? | `FIELD-INIT-07` | `FAIL-INIT-07` | `steps/init-workflow.md` `N4-mode-engine`, `N5-synthesis`, and `N7-internal-audit`; this file's `Synthesis` section | Review report names selected lineup path, direct-answer provenance, `team_ref`, skipped unselected path fields, and any missing provenance or ordering conflict. |
| Does this reference itself keep every mandatory artifact/source rule bound to a review gate, fail code, rework target, and report evidence row? | `FIELD-INIT-10` | `FAIL-INIT-10` | This `Review Gate Mapping` section; `review/init-review-gate.md`; `steps/init-workflow.md` | Maintenance report enumerates this file in the reference gate coverage list and confirms every mandatory subsection above is represented or intentionally routed through another row. |
