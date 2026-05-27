# Init Review Gate

This file owns quality evaluation, sufficiency audit, pass table, and provider fallback for `$aigc-init`.

## Default Provider

- Preferred auxiliary provider for package maintenance review: `code-reviewer`.
- For actual initialization execution, planning direct-answer 顾问与复核流程 are business-required by `steps/init-workflow.md`.
- If external reviewer/provider dispatch is unavailable during package maintenance, use the local checklist below.

## Sufficiency Gate

Initialization is incomplete unless all applicable items pass:

- project name and root are clear
- `init_mode == smart_advisor`
- `team_lineup_mode` is locked
- `team.yaml` exists or is ready to write
- `team.yaml` records `.agents/skills/team/` as the only selector scope
- planning direct-answer packets ran with real 顾问与复核流程 for actual initialization
- `north_star.yaml` has minimum long-term fields, whole-work union-style `全局风格`, required `细分风格`, default Chinese style text, and `全局风格提示词` explicitly contains `全局风格.媒介属性`
- `init_handoff.yaml` has stage-entry seeds and `unknowns`
- `story-source-manifest.yaml` exists and marks readiness
- `STATE.json` points to primary init artifacts and one recommended next entry
- the requested runtime skeleton exists: `0-初始化/`, `1-分集/`, `2-编剧/`, `3-导演/`, `4-表演/`, `5-摄影/`, `6-分组/`, `7-设计/<场景|道具|角色>/<1-清单|2-设计|3-生成>/`, `8-图像/`, `9-视频/`, `10-审片/`, `源/`, and `CONTEXT/`
- source-light story details are limited to `unknowns`, `deferred`, or `risk_notes`
- late source input triggers reconciliation before downstream work
- rebootstrap old-cycle artifacts are preserved, archived, purged, or marked stale according to reset mode
- `init_handoff.yaml.project_contract.recommended_next_stage` aligns with `STATE.json` during the init completion turn
- if governance carriers exist, they align with `STATE.json`
- final answer returns exactly one next-stage entry

## Pass Table

| field_id | pass standard | fail code | rework entry |
| --- | --- | --- | --- |
| `FIELD-INIT-01` | `north_star.yaml` contains only long-lived project constraints and valid adaptation policy | `FAIL-INIT-01` | `N4/N5` |
| `FIELD-INIT-01G` | `north_star.yaml` contains `全局风格 / 细分风格 / 类型元素 / 世界观`; `全局风格` is a whole-work union style contract, not a cross-design intersection prefix; `全局风格提示词` explicitly includes `全局风格.媒介属性`, is usually 300-500 Chinese characters, and describes reusable scene-type matching for light, color, texture, atmosphere, camera, motion, and negative-style rules; `类型元素提示词 <= 30 字`; `画面风格` is unified picture style and does not erase scene-sensitive light/color logic that belongs to the whole work style system | `FAIL-INIT-01G` | `N4/N5` |
| `FIELD-INIT-02` | `init_handoff.yaml` contains seeds, `unknowns`, and source/provenance breakdown | `FAIL-INIT-02` | `N4/N5` |
| `FIELD-INIT-02S` | `story-source-manifest.yaml` exists, `primary_story_source` alone decides formal readiness, source-light story facts stay in `unknowns/deferred/risk_notes`, late true source triggers reconciliation, and storyboard-script `preset_registry[].lock_level` uses only `hard_lock / soft_lock / reference_only` | `FAIL-INIT-02S` | `N3/N5/N7` |
| `FIELD-INIT-03` | mode, lineup, field provenance, `team_ref`, and decision source are traceable | `FAIL-INIT-03` | `N1/N3` |
| `FIELD-INIT-04` | `team.yaml` has roles, selector root, planning direct-answer provenance, and final gate semantics | `FAIL-INIT-04` | `N3/N4/N5` |
| `FIELD-INIT-05` | `0-初始化/` through `10-审片/`, `源/`, `CONTEXT/`, root carriers, project `MEMORY.md`, and `CHANGELOG.md` are complete; lazy carriers are trigger-based | `FAIL-INIT-05` | `N2/N5/N6` |
| `FIELD-INIT-06` | exactly one next active stage is returned | `FAIL-INIT-06` | `N7` |
| `FIELD-INIT-07` | route, mode, lineup, planning 顾问与复核流程, roster, and sufficiency audit are internally owned by this skill | `FAIL-INIT-07` | `N3/N4/N7` |
| `FIELD-INIT-08` | rebootstrap is identified, traced, and old-cycle truth exits active flow | `FAIL-INIT-08` | `N0/N6/N7` |
| `FIELD-INIT-09` | Skill 2.0 migration records map every carried section or resource to a current owner, operation, semantic risk, and validation gate; obsolete single-file or legacy-mode truth does not remain as a parallel source | `FAIL-INIT-09` | `references/migration-matrix.md` plus the affected owner partition |
| `FIELD-INIT-10` | Every modified initialization reference with mandatory rules has a tailored `Review Gate Mapping`; each mapping row resolves to this review gate table, a valid fail code, an executable rework target, and concrete report evidence | `FAIL-INIT-10` | `references/<file>.md` plus `review/init-review-gate.md` and `steps/init-workflow.md` when unresolved |

## Review Dimensions

| dimension | check |
| --- | --- |
| structure | Skill 2.0 directories and root files exist |
| dynamic reference | `SKILL.md` is entry/gate/navigation, not the long spec dump |
| runtime | paths match `references/scope-and-runtime.md` and shared layout |
| mode/team | `auto/custom` lock and advisor scope are explicit |
| source | source-light and source-grounded behavior are separated |
| reference | reference gate mappings resolve to pass table rows, fail codes, rework targets, and report evidence |
| migration | Skill 2.0 section/resource migration records remain complete and do not create a parallel truth source |
| rebootstrap | preserve/archive/purge boundaries are explicit |
| synthesis | only selected path deltas are aggregated |
| scripts | scripts remain mechanical helpers |
| context | `CONTEXT.md` remains heuristic knowledge, not a process log |

## Verdict Model

| verdict | meaning |
| --- | --- |
| `pass` | ready for use |
| `pass_with_todo` | usable with non-blocking follow-up |
| `needs_rework` | blocking issue exists |
| `blocked` | missing input, permission, or provider prevents execution |

## Finding Shape

```yaml
finding:
  severity: critical | high | medium | low
  dimension: structure | reference | migration | runtime | mode | team | source | rebootstrap | review
  symptom: ""
  direct_cause: ""
  source_contract: ""
  rework_target: ""
```

## Maintenance Review Flow

1. Run `python3 /Users/vincentlee/.codex/skills/meta/构建/技能/skill-工作车间/scripts/validate_skill_2_0.py .agents/skills/aigc/0-初始化`.
2. Run `python3 scripts/skill_context_audit.py --strict` when changing context-loading contracts.
3. Run `python3 scripts/aigc_skill_audit.py --strict` when changing AIGC registry, stage, or runtime contracts.
4. Use local semantic checklist or `code-reviewer` if allowed.
5. Update `CHANGELOG.md` after review; reusable findings belong in `CONTEXT.md`.
