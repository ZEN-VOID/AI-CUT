# Scope And Runtime Contract

This file owns the project scope, business object, canonical runtime layout, artifact ownership, and path boundaries for `$aigc-init`.

## Business Goal

- Lock the single `smart_advisor` initialization path.
- Require a user or explicit request signal to choose `auto` or `custom` lineup.
- Keep advisor selection inside `.agents/skills/team/`.
- Let planning-role advisors answer the fixed prompt packet before synthesis.
- Produce a stable `north_star` and a lightweight stage-entry handoff instead of an unfocused interview record.
- Support a safe reset back to `0-Init` when a project direction is no longer valid.

## Business Objects

- `projects/aigc/<项目名>/0-Init/north_star.yaml`
- `projects/aigc/<项目名>/0-Init/init_handoff.yaml`
- `projects/aigc/<项目名>/0-Init/story-source-manifest.yaml`
- `projects/aigc/<项目名>/team.yaml`
- `projects/aigc/<项目名>/MEMORY.md`
- `projects/aigc/<项目名>/CHANGELOG.md`
- `projects/aigc/<项目名>/CONTEXT/`
- `projects/aigc/<项目名>/STATE.json`
- Triggered sidecars such as `governance-state.yaml`, `mandate.yaml`, `mission-brief.yaml`, `route-plan.yaml`, `preflight-verdict.yaml`, `validation-report.md`, and `learning-record.md`.

## Canonical Project Root

The canonical runtime root is:

```text
projects/aigc/<项目名>/
```

Initialization creates or verifies:

- `0-Init/`
- `Original/`
- `MEMORY.md`
- `CHANGELOG.md`
- `CONTEXT/`
- `STATE.json`
- `team.yaml`

## Bootstrap Runtime Skeleton

Initialization prebuilds only the `0-Init/` workspace, `Original/` source root, project memory/context carriers, `STATE.json`, and `team.yaml`. It does not prebuild downstream phase roots, downstream child skeletons, stage validation reports, or planning split plans.

Forbidden bootstrap paths include:

- `1-Planning/1-分集/`
- `1-Planning/2-格式/`
- `1-Planning/3-分组/`
- `1-Planning/episode-split-plan.json`
- `1-Planning/validation-report.md`
- `5-Image/2-参照引用/`
- `5-Image/3-图像生成/`
- `6-Video/2-参照引用/`
- `6-Video/全能参照/`
- `6-Video/生成任务/`
- `6-Video/首帧参照/`
- `7-Cut/`

Downstream active child skeletons are owned by their own stages and created on first execution. Empty downstream directories never count as readiness evidence.

## Runtime Interpretation

- `Assets/` is an auxiliary reusable asset library, not a phase truth owner. It may be created by asset-facing stages or explicit user request, but is not required by the minimal init bootstrap.
- `2-Global/` is created by the `2-Global` stage when it executes. Its canonical output is written as per-episode JSON such as `第N集.json`; old Markdown outputs are not new runtime skeleton truth.
- `3-Detail/` is created by the `3-Detail` stage when it executes; historical `水月 / 镜花` compatibility paths are not runtime truth.
- `4-Design/` uses domain-first runtime files for active leaves: `场景清单.md`, `角色清单.md`, `道具清单.md`, `[主体名].md`, and `[主体名].json`. Do not prebuild inactive `服装` design leaf paths.
- `5-Image/A.分镜画面` and `5-Image/B.分镜故事板` are fusion routing entries. When the image stage executes, their business runtime roots are `5-Image/A-分镜帧/` and `5-Image/B-分镜故事板/`; `0-Init` does not create them.
- `6-Video/A.分镜画面参照/` is the fused Skill 2.0 landing for frame visual reference packages.
- `6-Video/B.分镜故事板参照/` is the fused Skill 2.0 landing for group-level storyboard reference packages.
- `6-Video/C.主体参照/` is the fused Skill 2.0 landing for subject-reference packages.
- Legacy `6-Video/全能参照/`, `6-Video/首帧参照/`, `6-Video/2-参照引用/`, and `6-Video/生成任务/` are not init bootstrap paths.

## Truth Ownership

`0-Init` owns:

- project kickoff contract
- `north_star.yaml`
- `init_handoff.yaml`
- init source metadata
- next-stage seed
- unresolved-question routing
- initialization lineup lock, prompt-packet execution, sufficiency audit, and writeback rules

`0-Init` first creates but does not monopolize:

- project `team.yaml`
- project `CHANGELOG.md`
- `0-Init/story-source-manifest.yaml`

`0-Init` does not own canonical truth for `1-Planning`, `2-Global`, `3-Detail`, `4-Design`, `5-Image`, `6-Video`, or `7-Cut`.

## Project Root Carrier Rules

1. `MEMORY.md` records only stable project preferences, tastes, special elements, exclusions, and long-term requirements.
2. `CONTEXT/` is project shared context and does not replace any skill `CONTEXT.md`.
3. `CHANGELOG.md` is a project chronological record entry, not live route truth.
4. Live route truth belongs to `STATE.json` and, when present, `governance-state.yaml`.
5. Empty skeleton directories never count as executed phase outputs.

## Quality Evidence Sources

- `scripts/aigc_skill_audit.py --strict`
- `scripts/skill_context_audit.py --strict`
- current `STATE.json`
- current `governance-state.yaml`
- current `validation-report.md`
- representative initialized project readback
- shared contracts under `.agents/skills/aigc/_shared/`
