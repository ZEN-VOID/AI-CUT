# Scope And Runtime Contract

This file owns the project scope, business object, canonical runtime layout, artifact ownership, and path boundaries for `$aigc-init`.

## Business Goal

- Lock the single `smart_advisor` initialization path.
- Require a user or explicit request signal to choose `auto` or `custom` lineup.
- Keep advisor selection inside `.agents/skills/team/`.
- Let planning-role advisors answer the fixed prompt packet before synthesis.
- Produce a stable `north_star` and a lightweight stage-entry handoff instead of an unfocused interview record.
- Support a safe reset back to `0-初始化` when a project direction is no longer valid.

## Business Objects

- `projects/aigc/<项目名>/0-初始化/north_star.yaml`
- `projects/aigc/<项目名>/0-初始化/init_handoff.yaml`
- `projects/aigc/<项目名>/0-初始化/story-source-manifest.yaml`
- `projects/aigc/<项目名>/team.yaml`
- `projects/aigc/<项目名>/MEMORY.md`
- `projects/aigc/<项目名>/CHANGELOG.md`
- `projects/aigc/<项目名>/附加预设/`
- `projects/aigc/<项目名>/STATE.json`
- Triggered sidecars such as `governance-state.yaml`, `mandate.yaml`, `mission-brief.yaml`, `route-plan.yaml`, `preflight-verdict.yaml`, `validation-report.md`, and `learning-record.md`.

## Canonical Project Root

The canonical runtime root is:

```text
projects/aigc/<项目名>/
```

Initialization creates or verifies:

- `0-初始化/`
- `1-分集/`
- `2-编导/`
- `3-摄影/`
- `4-设计/`
- `4-设计/场景/1-清单/`
- `4-设计/场景/2-设计/`
- `4-设计/场景/3-生成/`
- `4-设计/道具/1-清单/`
- `4-设计/道具/2-设计/`
- `4-设计/道具/3-生成/`
- `4-设计/角色/1-清单/`
- `4-设计/角色/2-设计/`
- `4-设计/角色/3-生成/`
- `5-分组/`
- `6-图像/`
- `7-视频/`
- `源/`
- `附加预设/`
- `MEMORY.md`
- `CHANGELOG.md`
- `STATE.json`
- `team.yaml`

## Bootstrap Runtime Skeleton

Initialization prebuilds the full user-facing stage skeleton requested for new AIGC projects. These directories are empty readiness containers until their owning stages write canonical files; empty directories never count as completed stage outputs.

```text
0-初始化/
1-分集/
2-编导/
3-摄影/
4-设计/
  场景/
    1-清单/
    2-设计/
    3-生成/
  道具/
    1-清单/
    2-设计/
    3-生成/
  角色/
    1-清单/
    2-设计/
    3-生成/
5-分组/
6-图像/
7-视频/
源/
附加预设/
CHANGELOG.md
MEMORY.md
STATE.json
team.yaml
```

Forbidden bootstrap paths include:

- `Original/`
- `Story/`
- `1-Planning/`
- `1-规划/`
- `2-Global/`
- `3-Detail/`
- `4-Design/`
- `5-Image/`
- `6-Video/`
- `7-Cut/`
- `2-全局/`
- `3-编导/`
- `4-摄影/`
- `5-设计/`
- `6-分组/`
- `7-图像/`
- `8-视频/`
- `CONTEXT/`

Legacy English runtime roots are compatibility inputs only; new initialization writes the Chinese runtime names above.

## Runtime Interpretation

- `源/` is the source landing root for new projects. Historical `Original/` and `Story/` may be read during migration but are not created for new initialization.
- `附加预设/` stores project-level preset packs and supplemental reference materials; it does not replace `MEMORY.md` and does not own live route truth.
- `1-分集/` is the episode-splitting stage root.
- `5-分组/` is the grouping stage root. Former nested `1-规划/2-分组/` and previous `6-分组/` roots are no longer created by initialization.
- `2-编导/` and `3-摄影/` separate script/directing work from cinematography/storyboard execution in the project runtime, even if the current skill tree still uses legacy package names internally.
- `4-设计/场景|道具|角色/1-清单/` owns list outputs, `2-设计/` owns design truth, and `3-生成/` owns generated design-image outputs.
- `6-图像/` and `7-视频/` are stage roots. Provider-specific request folders are created by image/video execution skills, not by initialization.

## Truth Ownership

`0-初始化` owns:

- project kickoff contract
- `north_star.yaml`
- `init_handoff.yaml`
- init source metadata
- next-stage seed
- unresolved-question routing
- initialization lineup lock, prompt-packet execution, sufficiency audit, and writeback rules

`0-初始化` first creates but does not monopolize:

- project `team.yaml`
- project `CHANGELOG.md`
- `0-初始化/story-source-manifest.yaml`

`0-初始化` does not own canonical truth for `1-分集`, `2-编导`, `3-摄影`, `4-设计`, `5-分组`, `6-图像`, or `7-视频`.

## Project Root Carrier Rules

1. `MEMORY.md` records only stable project preferences, tastes, special elements, exclusions, and long-term requirements.
2. `附加预设/` stores project presets and references; it does not replace any skill `CONTEXT.md`.
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
