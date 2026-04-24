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
- `Story/`
- `Assets/`
- `1-Planning/`
- `2-Global/`
- `3-Detail/`
- `4-Design/`
- `5-Image/`
- `6-Video/`
- `7-Cut/`
- `MEMORY.md`
- `CHANGELOG.md`
- `CONTEXT/`
- `STATE.json`

## Bootstrap Runtime Skeleton

Initialization prebuilds phase roots plus currently active child skeletons:

- `Assets/角色/`
- `Assets/道具/`
- `Assets/场景/`
- `Assets/服装/`
- `Assets/分镜画板/分镜帧/`
- `Assets/分镜画板/分镜故事板/`
- `Assets/分镜画板/漫画/`
- `1-Planning/1-分集/`
- `1-Planning/2-格式/`
- `1-Planning/3-分组/`
- `3-Detail/`
- `4-Design/`
- `4-Design/场景清单.md`
- `4-Design/角色清单.md`
- `4-Design/道具清单.md`
- `4-Design/[主体名].md`
- `4-Design/[主体名].json`
- `5-Image/分镜故事板/`
- `5-Image/分镜帧/`
- `5-Image/2-参照引用/`
- `5-Image/3-图像生成/`
- `6-Video/全能参照/`
- `6-Video/A.分镜画面参照/`
- `6-Video/B.分镜故事板参照/`
- `6-Video/C.主体参照/`
- `6-Video/首帧参照/`
- `6-Video/2-参照引用/`
- `6-Video/生成任务/`

The active child skeleton is runtime landing, not proof that a phase has executed.

## Runtime Interpretation

- `Assets/` is an auxiliary reusable asset library, not a phase truth owner.
- `2-Global/` is only prebuilt as a phase root. Its canonical outputs are later root-level files such as `全局风格.md`, `导演意图.md`, `全集类型元素.md`, and `分组类型元素.md`.
- `3-Detail/` is prebuilt as a phase root; historical `水月 / 镜花` compatibility paths are not runtime truth.
- `4-Design/` uses domain-first runtime directories for active leaves: `场景`, `角色`, and `道具`. Do not prebuild inactive `服装` design leaf paths.
- `5-Image/` maps prompt-distillation skill leaves to runtime `分镜故事板/` and `分镜帧/`, plus stable roots `2-参照引用/` and `3-图像生成/`.
- `6-Video/A.分镜画面参照/` is the fused Skill 2.0 landing for frame visual reference packages.
- `6-Video/B.分镜故事板参照/` is the fused Skill 2.0 landing for group-level storyboard reference packages.
- `6-Video/C.主体参照/` is the fused Skill 2.0 landing for subject-reference packages.
- `6-Video/生成任务/` is the business landing name for the `3-视频生成` skill stage.

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
