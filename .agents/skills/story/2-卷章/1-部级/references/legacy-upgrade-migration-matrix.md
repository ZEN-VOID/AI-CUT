# Legacy Upgrade Migration Matrix

本文件记录 `story-plan-book-level` 从旧部级子技能骨架升级到 Skill 2.0 包时的语义去向。它只用于追溯，不作为运行时入口。

## Source Snapshot

升级前目标包包含：

- `SKILL.md`
- `CONTEXT.md`
- `references/book-rhythm-save-the-cat.md`
- `templates/overall-planning.template.md`

## Migration Matrix

| source_path | source_section | content_class | target_path | operation | semantic_risk | reference_updates | validation_gate |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `SKILL.md` | frontmatter | entry metadata | `SKILL.md` | keep + expand description | low | none | `validate_skill_2_0.py` |
| `SKILL.md` | `Context Loading Contract` | loading contract | `SKILL.md` | keep + expand project memory and dynamic loading | medium | add `Reference Loading Guide` | context audit |
| `SKILL.md` | `Parent Positioning` | scope boundary | `SKILL.md` | keep | low | none | manual semantic check |
| `SKILL.md` | `Canonical Sources` | dynamic references | `SKILL.md` `Reference Loading Guide` | rewrite | medium | add references to `steps/`, `review/`, `types/`, `knowledge-base/`, `agents/`, `scripts/` | `validate_skill_2_0.py` |
| `SKILL.md` | `Business Requirement Analysis Contract` | workflow analysis | `steps/book-level-planning-workflow.md` | move + expand | low | `SKILL.md` links steps file | manual semantic check |
| `SKILL.md` | `Output Contract` canonical output | output contract | `SKILL.md` `Output Contract` | rewrite into five fields | medium | add `templates/output-template.md` alignment | `validate_skill_2_0.py` |
| `SKILL.md` | `Required Headings` | output field rules | `references/book-level-output-contract.md` | move + expand | low | `SKILL.md` links reference | manual semantic check |
| `SKILL.md` | `Hard Rules` | output/review rules | `references/book-level-output-contract.md` and `review/review-contract.md` | split | medium | `SKILL.md` links both owners | review gate |
| `SKILL.md` | `Visual Map` | topology map | `SKILL.md` and `steps/book-level-planning-workflow.md` | keep summary + expand workflow | low | none | Mermaid presence check |
| `SKILL.md` | `Thinking-Action Network` | steps topology | `steps/book-level-planning-workflow.md` | move + expand evidence/gates | medium | `SKILL.md` links steps file | manual semantic check |
| `CONTEXT.md` | `Type Map` | experience layer | `CONTEXT.md` | keep + expand | low | none | context audit |
| `CONTEXT.md` | `Reusable Heuristics` | experience layer | `CONTEXT.md` and `knowledge-base/book-level-planning-heuristics.md` | keep + split stable heuristics | low | `SKILL.md` links knowledge-base file | context audit |
| `references/book-rhythm-save-the-cat.md` | all | rhythm reference | same path | keep | low | referenced from `SKILL.md` | manual semantic check |
| `templates/overall-planning.template.md` | all | business template | same path plus `templates/output-template.md` | keep + add aligned template | low | `SKILL.md` links both templates | `validate_skill_2_0.py` |

## Non-Loss Notes

- No legacy section was dropped silently.
- No target directory or existing file was renamed.
- Existing `overall-planning.template.md` remains available for consumers that already reference it.
- New files only add Skill 2.0 owners, metadata, review gates and traceability around the existing部级业务语义.
