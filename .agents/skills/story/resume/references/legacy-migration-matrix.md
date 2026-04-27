# Legacy Migration Matrix

本文件记录 `story-resume` 从旧长 `SKILL.md` 升级到 Skill 2.0 分区结构时的语义去向。升级原则：不静默丢语义；入口合同留在 `SKILL.md`，长细则下沉到明确 owner。

| source_path | source_section | content_class | target_path | operation | semantic_risk | reference_updates | validation_gate |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `SKILL.md` | frontmatter / Purpose / Stage Position | entry boundary | `SKILL.md` | keep + shrink | low | product metadata mirrors `agents/openai.yaml` | Skill 2.0 validator |
| `SKILL.md` | Context Loading Contract | loading contract | `SKILL.md` | keep | low | README mentions paired loading | context audit |
| `SKILL.md` | Supported Scope | command support matrix | `types/resume-type-map.md` | split | medium | `SKILL.md` Mode Selection links types | semantic check |
| `SKILL.md` | Project Root Guard | runtime guard | `steps/resume-workflow.md`, `scripts/README.md`, `review/resume-review-gate.md` | split | high | command examples use unified `story.py` | manual semantic check |
| `SKILL.md` | Reference Loading Levels | dynamic references | `SKILL.md` | rewrite | low | all section links point to canonical files | validator |
| `SKILL.md` | Workflow Checklist / Step 0-7 | execution topology | `steps/resume-workflow.md` | rewrite | high | `SKILL.md` keeps only topology index | steps review gate |
| `SKILL.md` | artifact_fallback interpretation | detailed recovery protocol | `references/workflow-resume.md`, `types/resume-type-map.md` | split | medium | fallback reasons preserved | semantic check |
| `SKILL.md` | `story-write` / `story-validate` / `story-review` / `story-query` step semantics | command strategy | `references/workflow-resume.md`, `types/resume-type-map.md` | split | medium | no cleanup for query | review gate |
| `SKILL.md` | safe cleanup commands | mechanical command boundary | `scripts/README.md`, `references/workflow-resume.md` | split | medium | destructive actions require preview/confirm | safety gate |
| `SKILL.md` | closure checklist / Completion Gate | quality gate | `review/resume-review-gate.md` | split | low | Output Contract references review gate | validator + manual check |
| `SKILL.md` | Lite Tier Field Mapping | owner matrix | `SKILL.md` Field Mapping | keep + update | low | expanded to all Skill 2.0 owners | validator |
| `CONTEXT.md` | Type Map / Repair Playbook / Reusable Heuristics | experience knowledge | `CONTEXT.md`, `knowledge-base/resume-heuristics.md` | keep + summarize | low | no process log added | context review |
| `references/workflow-resume.md` | recovery protocol | detailed reference | `references/workflow-resume.md` | keep | low | `SKILL.md` dynamic reference | reference review |
| `references/system-data-flow.md` | runtime data-flow redirect | detailed reference | `references/system-data-flow.md` | keep | low | README and SKILL link retained | reference review |

## Reference Sync Notes

- Registry entries for `story-resume` already point to `.agents/skills/story/resume`; no directory rename was performed.
- Existing links to `references/workflow-resume.md` and `references/system-data-flow.md` remain valid.
- New section files are additive; no external binary references were identified for this package.
