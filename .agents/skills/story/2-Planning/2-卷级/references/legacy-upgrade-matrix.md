# Legacy Upgrade Matrix

本文件记录 `2-卷级` 从旧轻量技能包升级为 Skill 2.0 包时的迁移矩阵。它只用于溯源，不替代 `SKILL.md` 的入口合同。

## Section Migration Matrix

| source_path | source_section | content_class | target_path | operation | semantic_risk | reference_updates | validation_gate |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `SKILL.md` | frontmatter | entry metadata | `SKILL.md` | keep and expand description | low | none | validator |
| `SKILL.md` | `Context Loading Contract` | mandatory loading | `SKILL.md` | keep and strengthen project context rules | high | parent/shared references retained | manual semantic check |
| `SKILL.md` | `Parent Positioning` | scope boundary | `SKILL.md` + `references/volume-planning-contract.md` | summarize in entry, expand in reference | medium | dynamic reference table updated | review gate |
| `SKILL.md` | `Canonical Sources` | dynamic reference | `SKILL.md` | rewrite as canonical sources and reference guide | low | all new sections referenced | validator |
| `SKILL.md` | `Business Requirement Analysis Contract` | business rules | `references/volume-planning-contract.md` | move | medium | `SKILL.md` points to reference owner | manual semantic check |
| `SKILL.md` | `Output Contract` | output anchor | `SKILL.md` + `templates/output-template.md` | rewrite into five-field contract | high | template alignment added | validator |
| `SKILL.md` | `Required Headings` | content rules | `references/volume-planning-contract.md` + `templates/output-template.md` | move and project into template | medium | template updated | review gate |
| `SKILL.md` | `Hard Rules` | content rules | `references/volume-planning-contract.md` | move | high | review checks reference owner | manual semantic check |
| `SKILL.md` | `Visual Map` | process topology | `SKILL.md` + `steps/volume-planning-workflow.md` | keep summary, expand workflow | low | Mermaid retained | review gate |
| `SKILL.md` | `Thinking-Action Network` | steps topology | `steps/volume-planning-workflow.md` | move and expand with evidence gates | medium | `SKILL.md` node handoff summary updated | review gate |
| `CONTEXT.md` | `Type Map` / `Reusable Heuristics` | experience | `CONTEXT.md` + `knowledge-base/volume-planning-heuristics.md` | keep and supplement | low | none | context baseline check |
| `references/volume-rhythm-framework.md` | entire file | detailed reference | `references/volume-rhythm-framework.md` | keep | low | referenced from guide | review gate |
| `templates/volume-planning.template.md` | entire file | output template | `templates/volume-planning.template.md` + `templates/output-template.md` | keep and add canonical output template | medium | `Output Contract Alignment` added | validator |

## Residual Risk

- Parent `1-部级` and sibling `3-章级` remain in their previous compact format; this upgrade only changes `2-卷级`.
- External reports may still mention older historical paths such as `2-章节规划`; those are archival references, not active route inputs.
