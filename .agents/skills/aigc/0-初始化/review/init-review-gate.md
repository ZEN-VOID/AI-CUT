# Init Review Gate

This file owns quality evaluation, sufficiency audit, pass table, and provider fallback for `$aigc-init`.

## Default Provider

- Preferred auxiliary provider for package maintenance review: `code-reviewer`.
- For actual initialization execution, planning direct-answer subagents are business-required by `steps/init-workflow.md`.
- If higher-level policy blocks real reviewer or subagent dispatch during package maintenance, use the local checklist below and report the downgrade source, planned path, actual path, and missing reviewers.

## Sufficiency Gate

Initialization is incomplete unless all applicable items pass:

- project name and root are clear
- `init_mode == smart_advisor`
- `team_lineup_mode` is locked
- `team.yaml` exists or is ready to write
- `team.yaml` records `.agents/skills/team/` as the only selector scope
- planning direct-answer packets ran with real subagents for actual initialization
- `north_star.yaml` has minimum long-term fields, safe `全局风格`, required `细分风格`, default Chinese style text, and configured character caps
- `init_handoff.yaml` has stage-entry seeds and `unknowns`
- `story-source-manifest.yaml` exists and marks readiness
- `STATE.json` points to primary init artifacts and one recommended next entry
- the requested runtime skeleton exists: `0-初始化/`, `1-分集/`, `2-编导/`, `3-摄影/`, `4-设计/<场景|道具|角色>/<1-清单|2-设计|3-生成>/`, `4-分组/`, `6-图像/`, `7-视频/`, `源/`, and `附加预设/`
- source-light story details are downgraded to `unknowns`, `deferred`, or `risk_notes`
- late source input triggers reconciliation before downstream work
- rebootstrap old-cycle artifacts are preserved, archived, purged, or marked stale according to reset mode
- `init_handoff.yaml.project_contract.recommended_next_stage` aligns with `STATE.json` during the init completion turn
- if governance carriers exist, they align with `STATE.json`
- final answer returns exactly one next-stage entry

## Pass Table

| field_id | pass standard | fail code | rework entry |
| --- | --- | --- | --- |
| `FIELD-INIT-01` | `north_star.yaml` contains only long-lived project constraints and valid adaptation policy | `FAIL-INIT-01` | `N4/N5` |
| `FIELD-INIT-01G` | `north_star.yaml` contains `全局风格 / 细分风格 / 类型元素 / 世界观`; `全局风格` is a cross-design safe prefix and contains no lens, character-material, scene-composition, costume-detail, or prop-detail payload; `全局风格提示词 <= 200 字`, `类型元素提示词 <= 30 字`, `画面风格 <= 70 字`, `服装风格 / 建筑风格 / 物品风格 <= 100 字` | `FAIL-INIT-01G` | `N4/N5` |
| `FIELD-INIT-02` | `init_handoff.yaml` contains seeds, `unknowns`, and source/provenance breakdown | `FAIL-INIT-02` | `N4/N5` |
| `FIELD-INIT-03` | mode, lineup, field provenance, `team_ref`, and decision source are traceable | `FAIL-INIT-03` | `N1/N3` |
| `FIELD-INIT-04` | `team.yaml` has roles, selector root, planning direct-answer provenance, and final gate semantics | `FAIL-INIT-04` | `N3/N4/N5` |
| `FIELD-INIT-05` | `0-初始化/` through `7-视频/`, `源/`, `附加预设/`, root carriers, project `MEMORY.md`, and `CHANGELOG.md` are complete; lazy carriers are trigger-based | `FAIL-INIT-05` | `N2/N5/N6` |
| `FIELD-INIT-06` | exactly one next active stage is returned | `FAIL-INIT-06` | `N7` |
| `FIELD-INIT-07` | route, mode, lineup, planning subagents, roster, and sufficiency audit are internally owned by this skill | `FAIL-INIT-07` | `N3/N4/N7` |
| `FIELD-INIT-08` | rebootstrap is identified, traced, and old-cycle truth exits active flow | `FAIL-INIT-08` | `N0/N6/N7` |

## Review Dimensions

| dimension | check |
| --- | --- |
| structure | Skill 2.0 directories and root files exist |
| dynamic reference | `SKILL.md` is entry/gate/navigation, not the long spec dump |
| runtime | paths match `references/scope-and-runtime.md` and shared layout |
| mode/team | `auto/custom` lock and advisor scope are explicit |
| source | source-light and source-grounded behavior are separated |
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
  dimension: structure | reference | runtime | mode | team | source | rebootstrap | review
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
