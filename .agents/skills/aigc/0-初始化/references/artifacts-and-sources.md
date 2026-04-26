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
- `templates/project-preset-readme.template.md`
- `templates/state.template.json`
- `templates/output-template-map.md`
- `.agents/skills/aigc/_shared/council-runtime/team.template.yaml`
- `.agents/skills/aigc/_shared/story-source-manifest.template.yaml`
- `.agents/skills/aigc/_shared/project-runtime-layout.md`

Rules:

1. `north_star.yaml` only carries long-lived project constraints.
2. `north_star.yaml` directly owns the exact global-design blocks `全局风格 / 细分风格 / 类型元素 / 世界观`.
3. `全局风格` is a cross-design safe prompt prefix for image, character, scene, prop, and other design types. It may only contain `媒介属性 / 时代属性 / 光影逻辑 / 画面质感 / 避免出现 / 全局风格提示词`.
4. `全局风格` must not contain fields that pollute downstream design types, such as lens language, character material, scene composition, costume details, prop details, or any single-domain style payload.
5. `全局风格` defaults to Chinese, and the generated `全局风格提示词` must stay within 200 Chinese characters.
6. `类型元素` defaults to Chinese, and the generated `类型元素提示词` must stay within 30 Chinese characters.
7. `细分风格` owns domain-specific style guidance: `画面风格 / 服装风格 / 建筑风格 / 物品风格`. Ancient architecture guidance must not force-fit modern architects or modernist labels unless the project explicitly calls for it.
8. `画面风格` defaults to Chinese and must stay within 70 Chinese characters.
9. `服装风格 / 建筑风格 / 物品风格` default to Chinese, and each must stay within 100 Chinese characters.
10. Do not duplicate global-design fields in old umbrella slots such as `aesthetic_axes`, `genre_corridor`, `theme_promises`, or `tone_keywords`.
11. `init_handoff.yaml` carries stage-entry seeds, source layers, and unknowns.
12. Session-only information does not belong in `north_star.yaml`.
13. `north_star.yaml` must not contain route truth or `rebootstrap` process state.

## Stage Entry Ownership

1. Initialization-round stage seed: `init_handoff.yaml.project_contract.recommended_next_stage`.
2. Current live route truth: `STATE.json.recommended_next_stage`, `recommended_entry_path`, and `recommended_next_step`.
3. If present, `governance-state.yaml.resume_contract.*` is the structured resume truth for `query`, `resume`, and high-risk gates.
4. After the project leaves `0-初始化`, `init_handoff.yaml` remains historical handoff seed and no longer owns live current-stage truth.

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
