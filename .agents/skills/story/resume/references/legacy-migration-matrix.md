# Legacy Migration Matrix

本文件记录 `story-resume` 从旧长 `SKILL.md` 升级到 Skill 2.0 分区结构时的语义去向。升级原则：不静默丢语义；入口合同留在 `SKILL.md`，长细则下沉到明确 owner。

| source_path | source_section | content_class | target_path | operation | semantic_risk | reference_updates | validation_gate |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `SKILL.md` | frontmatter / Purpose / Stage Position | entry boundary | `SKILL.md` | keep + shrink | low | product metadata mirrors `agents/openai.yaml` | Skill 2.0 validator |
| `SKILL.md` | Context Loading Contract | loading contract | `SKILL.md` | keep | low | README mentions paired loading | context audit |
| `SKILL.md` | Supported Scope | command support matrix | `types/resume-type-map.md` | split | medium | `SKILL.md` Mode Selection links types | semantic check |
| `SKILL.md` | Project Root Guard | runtime guard | `SKILL.md#Thinking-Action Node Map`, `scripts/README.md`, `review/resume-review-gate.md` | split + spine restore | high | command examples use unified `story.py` | manual semantic check |
| `SKILL.md` | Reference Loading Levels | dynamic references | `SKILL.md` | rewrite | low | all section links point to canonical files | validator |
| `SKILL.md` | Workflow Checklist / Step 0-7 | execution topology | `SKILL.md#Thinking-Action Node Map` | restore to runtime spine | high | `SKILL.md` owns node table and Mermaid topology | runtime spine smoke |
| `SKILL.md` | artifact_fallback interpretation | detailed recovery protocol | `references/workflow-resume.md`, `types/resume-type-map.md` | split | medium | fallback reasons preserved | semantic check |
| `SKILL.md` | `story-write` / `story-polishing` / `story-return` / `story-query` step semantics | command strategy | `references/workflow-resume.md`, `types/resume-type-map.md` | split | medium | no cleanup for query | acceptance gate |
| `SKILL.md` | safe cleanup commands | mechanical command boundary | `scripts/README.md`, `references/workflow-resume.md` | split | medium | destructive actions require preview/confirm | safety gate |
| `SKILL.md` | closure checklist / Completion Gate | quality gate | `review/resume-review-gate.md` | split | low | Output Contract references review gate | validator + manual check |
| `SKILL.md` | Lite Tier Field Mapping | owner matrix | `SKILL.md` Field Mapping | keep + update | low | expanded to all Skill 2.0 owners | validator |
| `CONTEXT.md` | Type Map / Repair Playbook / Reusable Heuristics | experience knowledge | `CONTEXT.md`, `knowledge-base/resume-heuristics.md` | keep + summarize | low | no process log added | context review |
| `references/workflow-resume.md` | recovery protocol | detailed reference | `references/workflow-resume.md` | keep | low | `SKILL.md` dynamic reference | reference review |
| `references/system-data-flow.md` | runtime data-flow redirect | detailed reference | `references/system-data-flow.md` | keep | low | README and SKILL link retained | reference review |

## Reference Sync Notes

- Registry entries for `story-resume` already point to `.agents/skills/story/resume`; no directory rename was performed.
- Existing links to `references/workflow-resume.md` and `references/system-data-flow.md` remain valid.
- `steps/` was retired during the 2026-06-16 runtime-spine upgrade; node references now point to `SKILL.md#Thinking-Action Node Map`.
- New section files are additive; no external binary references were identified for this package.

## Review Gate Mapping

| review_question | review_gate | fail_code | rework_target | report_evidence |
| --- | --- | --- | --- | --- |
| 每个旧 section / 资源是否都有迁移去向、风险和验证门禁？ | 迁移矩阵缺 source、target、operation、risk 或 validation 即失败 | `FAIL-RESUME-LEGACY-LOSS` | `references/legacy-migration-matrix.md` | migration matrix rows、drop/archive 理由 |
| `steps/` 旧节点是否已收回到 `SKILL.md` runtime spine？ | 节点、route、gate 或 Mermaid 仍依赖 steps 文件即失败 | `FAIL-RESUME-RUNTIME-SPINE` | `SKILL.md#Thinking-Action Node Map` | node map audit、smoke route simulation |
| 引用同步是否覆盖 README、CONTEXT、types、review 和模板？ | 包内仍引用退休节点文件或旧校验器路径即失败 | `FAIL-RESUME-REFERENCE-SYNC` | `README.md`、`CONTEXT.md`、相关模块 | `rg` 引用扫描结果 |
