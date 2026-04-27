# Legacy Migration Matrix

本文件记录 `story-query` 从旧单文件入口升级到 Skill 2.0 分区结构时的语义去向。

| source_path | source_section | content_class | target_path | operation | semantic_risk | reference_updates | validation_gate |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `SKILL.md` | frontmatter / description / allowed tools | entry metadata | `SKILL.md` | keep + normalize | low | none | validator |
| `SKILL.md` | Context Loading Contract | entry contract | `SKILL.md` | keep + expand project MEMORY/CONTEXT rule | high | none | manual semantic check |
| `SKILL.md` | Purpose / Stage Position | entry and topology | `SKILL.md` | summarize | medium | story root route already points to query | manual semantic check |
| `SKILL.md` | Project Root Guard | workflow | `steps/query-workflow.md` | move + rewrite | high | command examples updated | review gate |
| `SKILL.md` | Workflow Checklist | workflow | `steps/query-workflow.md` | rewrite as node network | medium | none | review gate |
| `SKILL.md` | Truth Role Decision | type strategy | `types/query-type-map.md` | move + normalize | high | `SKILL.md` Reference Loading Guide | review gate |
| `SKILL.md` | Reference Loading Levels | dynamic reference | `SKILL.md` + `steps/query-workflow.md` | split | medium | links kept | validator |
| `SKILL.md` | Step 1 query type table | type strategy | `types/query-type-map.md` | move | medium | none | review gate |
| `SKILL.md` | Step 2 reference commands | workflow | `steps/query-workflow.md` | move | low | none | review gate |
| `SKILL.md` | Step 3 truth role reads | workflow | `steps/query-workflow.md` | move + preserve commands | high | none | manual semantic check |
| `SKILL.md` | Step 4 cross-check rules | workflow / review | `steps/query-workflow.md` + `review/review-contract.md` | split | high | none | review gate |
| `SKILL.md` | Step 5 output contract | output template | `SKILL.md` + `templates/output-template.md` | split | high | output template alignment added | validator |
| `SKILL.md` | Quick Reference | workflow command hints | `steps/query-workflow.md` | move | low | none | review gate |
| `SKILL.md` | Root-Cause 执行合同 | root-cause contract | `SKILL.md` | keep + align Skill 2.0 owners | high | owner paths added | manual semantic check |
| `SKILL.md` | Lite Tier Field Mapping | field map | `SKILL.md` | keep + compact | low | none | validator |
| `SKILL.md` | Completion Gate | output contract | `SKILL.md` + `review/review-contract.md` | split | medium | none | validator |
| `CONTEXT.md` | Type Map / Repair Playbook / Heuristics | experience layer | `CONTEXT.md` + `knowledge-base/query-heuristics.md` | keep + mirror stable heuristics | low | none | context audit |
| `references/system-data-flow.md` | data-flow spec | reference | `references/system-data-flow.md` | keep | medium | referenced by `SKILL.md` | semantic check |
| `references/tag-specification.md` | manual XML spec | reference | `references/tag-specification.md` | keep | low | referenced by `SKILL.md` | semantic check |
| `references/advanced/foreshadowing.md` | foreshadowing spec | reference | `references/advanced/foreshadowing.md` | keep | low | referenced by `SKILL.md` | semantic check |

## Unmigrated Or External References

- No file path was renamed in this upgrade.
- Existing registry and root story skill entries already point to `.agents/skills/story/query`; no automatic path reference rewrite was required.
