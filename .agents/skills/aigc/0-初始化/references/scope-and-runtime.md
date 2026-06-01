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
- `projects/aigc/<项目名>/CONTEXT/`
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
- `3-运动/`
- `4-摄影/`
- `5-分组/`
- `6-设计/`
- `6-设计/场景/1-清单/`
- `6-设计/场景/2-设计/`
- `6-设计/场景/3-生成/`
- `6-设计/道具/1-清单/`
- `6-设计/道具/2-设计/`
- `6-设计/道具/3-生成/`
- `6-设计/角色/1-清单/`
- `6-设计/角色/2-设计/`
- `6-设计/角色/3-生成/`
- `7-图像/`
- `8-视频/`
- `9-审片/`
- `源/`
- `CONTEXT/`
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
3-运动/
4-摄影/
5-分组/
6-设计/
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
7-图像/
8-视频/
9-审片/
源/
CONTEXT/
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
- `3-摄影/`
- `4-表演/`
- `4-设计/`
- `4-分组/`
- `5-摄影/`
- `5-设计/`
- `6-分组/`
- `6-图像/`
- `7-设计/`
- `7-视频/`
- `8-图像/`
- `8-审片/`
- `9-视频/`
- `10-审片/`

Legacy English runtime roots are compatibility inputs only; new initialization writes the Chinese runtime names above.

## Runtime Interpretation

- `源/` is the source landing root for new projects. Historical `Original/` and `Story/` may be read during migration but are not created for new initialization.
- `CONTEXT/` stores project-level preset packs and supplemental reference materials; it does not replace `MEMORY.md` and does not own live route truth.
- `1-分集/` is the episode-splitting stage root.
- `2-编导/` integrates screenplay fidelity, directing intent, performance craft, and concrete visual language; `3-运动/` consumes it to strengthen character motion start, path, endpoint, and reference frame; `4-摄影/` consumes `3-运动/` for shot-detail injection.
- `5-分组/` is the grouping stage root. Former `4-分组/`, `6-分组/`, and legacy nested grouping roots are no longer created by initialization.
- `6-设计/场景|道具|角色/1-清单/` owns list outputs, `2-设计/` owns design truth, and `3-生成/` owns generated design-image outputs.
- `7-图像/`, `8-视频/` and `9-审片/` are stage roots. Provider-specific request folders and review report subdirectories are created by their owning stages, not by initialization.

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

`0-初始化` does not own canonical truth for `1-分集`, `2-编导`, `3-运动`, `4-摄影`, `5-分组`, `6-设计`, `7-图像`, `8-视频`, or `9-审片`.

## Project Root Carrier Rules

1. `MEMORY.md` records only stable project preferences, tastes, special elements, exclusions, and long-term requirements.
2. `CONTEXT/` stores project contexts and references; it does not replace any skill `CONTEXT.md`.
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

## Review Gate Mapping

| Review Question | Review Gate | Fail Code | Rework Target | Report Evidence |
| --- | --- | --- | --- | --- |
| Is the canonical project root `projects/aigc/<项目名>/`, and are all initialization business objects written under the project root or `0-初始化/` as specified? | `FIELD-INIT-05` | `FAIL-INIT-05` | `steps/init-workflow.md` `N2-runtime-bootstrap` and `N5-synthesis`; this file's `Canonical Project Root` and `Business Objects` sections | Review report lists the resolved project root, each required business object path, and any artifact found outside the canonical runtime. |
| Does initialization create or verify the full Chinese runtime skeleton from `0-初始化/` through `9-审片/`, including `3-运动/` between `2-编导/` and `4-摄影/`, `6-设计/场景/`, `6-设计/道具/`, `6-设计/角色/` each with `1-清单/`, `2-设计/`, and `3-生成/`, plus `源/`, `CONTEXT/`, `MEMORY.md`, `CHANGELOG.md`, `STATE.json`, and `team.yaml`? | `FIELD-INIT-05` | `FAIL-INIT-05` | `steps/init-workflow.md` `N2-runtime-bootstrap`; `.agents/skills/aigc/_shared/project-runtime-layout.md`; this file's `Canonical Project Root` and `Bootstrap Runtime Skeleton` sections | Review report records a directory/file readback or dry-run manifest showing each required runtime path as present or planned to write. |
| Are forbidden bootstrap paths such as `Original/`, `Story/`, legacy English stage roots, and stale Chinese numbering aliases not created for new initialization? | `FIELD-INIT-05` | `FAIL-INIT-05` | `steps/init-workflow.md` `N2-runtime-bootstrap`; this file's `Bootstrap Runtime Skeleton` and `Runtime Interpretation` sections | Review report lists any forbidden path found in a new initialization output, or confirms legacy aliases were only treated as compatibility inputs. |
| Are empty skeleton directories treated as readiness containers rather than completed stage outputs? | `FIELD-INIT-05` | `FAIL-INIT-05` | `steps/init-workflow.md` `N2-runtime-bootstrap` and `N7-internal-audit`; this file's `Bootstrap Runtime Skeleton` and `Project Root Carrier Rules` sections | Review report states whether phase completion was inferred from real files rather than empty directories, and cites any false-positive stage output. |
| Do `MEMORY.md`, `CONTEXT/`, `CHANGELOG.md`, `STATE.json`, and optional `governance-state.yaml` keep their distinct project-root responsibilities without `CONTEXT/` replacing memory or `CHANGELOG.md` replacing live route truth? | `FIELD-INIT-05` | `FAIL-INIT-05` | `steps/init-workflow.md` `N2-runtime-bootstrap`, `N5-synthesis`, and `N7-internal-audit`; this file's `Project Root Carrier Rules` section | Review report summarizes each carrier's role, current path, and any misplaced preference, context material, chronology, or live route field. |
| Does `0-初始化` claim only kickoff, north-star, handoff, source metadata, lineup, prompt-packet, audit, and writeback ownership, without taking canonical truth from downstream stages? | `FIELD-INIT-07` | `FAIL-INIT-07` | `SKILL.md` `Reference Loading Guide`; `steps/init-workflow.md` `N3-internal-router` and `N7-internal-audit`; this file's `Truth Ownership` section | Review report names any downstream-stage truth field incorrectly owned by initialization, or confirms downstream ownership remains with the later stage skill. |
| Does the review or delivery report cite concrete quality evidence from audit commands, current state files, representative project readback, or shared contracts rather than asserting runtime correctness without evidence? | `FIELD-INIT-10` | `FAIL-INIT-10` | This file's `Quality Evidence Sources`; `review/init-review-gate.md`; `steps/init-workflow.md` `N7-internal-audit` | Final report lists the commands, readback files, or shared contracts used as evidence, plus skipped checks and residual risk. |
| Does this reference itself keep every mandatory scope/runtime rule bound to a review gate, fail code, rework target, and report evidence row? | `FIELD-INIT-10` | `FAIL-INIT-10` | This `Review Gate Mapping` section; `review/init-review-gate.md`; `steps/init-workflow.md` | Maintenance report enumerates this file in the reference gate coverage list and confirms scope, skeleton, forbidden path, carrier, ownership, and evidence-source coverage. |
