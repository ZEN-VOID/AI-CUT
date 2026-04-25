# $aigc-init Output Template

Use this template for the final user-facing response after `$aigc-init` completes, blocks, or returns to the option card. It mirrors `SKILL.md` `Output Contract (Mandatory)`.

## Output Contract Alignment

| marker | binding |
| --- | --- |
| Required output | initialized project state, core five-piece status, lazy governance status, one next-stage recommendation |
| Output format | Markdown final response; references YAML, JSON, and Markdown artifacts written by the run |
| Output path | artifact paths under `projects/aigc/<项目名>/`, plus chat response for this template |
| Naming convention | use canonical artifact names from `SKILL.md` Output Contract and `templates/output-template-map.md` |
| Completion gate | only use Completed shape after `review/init-review-gate.md` sufficiency gate passes |

## Completed

```markdown
已完成 `0-初始化` 初始化。

- init_mode: smart_advisor
- team_lineup_mode: <auto|custom>
- planning_direct_answer_subagents: <ran|blocked|not_applicable>
- core_five_piece:
  - north_star: <path>
  - init_handoff: <path>
  - story_source_manifest: <path>
  - team: <path>
  - STATE: <path>
- lazy_governance_artifacts: <none|paths>
- recommended_next_stage: <stage>
- recommended_entry_path: <path>
- recommended_next_step: <one concrete next action>
- root_cause_closeout:
  - root cause location: <where the decisive rule lived>
  - immediate fix: <what was fixed in this run>
  - systemic prevention fix: <which contract/template/gate prevents recurrence>
```

## Blocked

```markdown
`0-初始化` 暂停，尚未写入 canonical 初始化工件。

- block_reason: <missing auto/custom | subagents unavailable | unsafe reset scope | source conflict | other>
- current_safe_output: <option card | source-light skeleton | diagnostic only>
- missing_input_or_gate: <specific missing field/gate>
- next_required_user_action: <one concrete action>
```

## Option Card

When `team_lineup_mode` is not locked, return only `templates/init-option-card.template.md` plus the missing decision note.
