# Legacy Migration Matrix

本文件记录 `story-query` 从旧单文件入口、旧版 Skill 2.0 分区结构升级到 runtime-spine Skill 2.0 的语义去向。

## 2026-04-27 Migration

| source_path | source_section | content_class | target_path | operation | semantic_risk | reference_updates | validation_gate |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `SKILL.md` | frontmatter / description / allowed tools | entry metadata | `SKILL.md` | keep + normalize | low | none | validator |
| `SKILL.md` | Context Loading Contract | entry contract | `SKILL.md` | keep + expand project MEMORY/CONTEXT rule | high | none | manual semantic check |
| `SKILL.md` | Purpose / Stage Position | entry and topology | `SKILL.md` | summarize | medium | story root route points to query | manual semantic check |
| `SKILL.md` | Project Root Guard | workflow command detail | `references/query-command-catalog.md` | move + rewrite as command catalog | high | README and SKILL module matrix updated | review gate |
| `SKILL.md` | Workflow Checklist | runtime node network | `SKILL.md` `Thinking-Action Node Map` | rewrite as nodes | high | Mermaid and smoke route simulation updated | smoke test |
| `SKILL.md` | Truth Role Decision | type strategy | `types/query-type-map.md` | move + normalize | high | `types/type-map.md` package index added | review gate |
| `SKILL.md` | Reference Loading Levels | module dispatch | `SKILL.md` Module Loading Matrix + Module Trigger Matrix | rewrite | high | references authorized with gate mapping | validator |
| `SKILL.md` | Step 1 query type table | type strategy | `types/query-type-map.md` | move | medium | none | review gate |
| `SKILL.md` | Step 2 reference commands | command catalog | `references/query-command-catalog.md` | move | low | README and Module Trigger Matrix updated | review gate |
| `SKILL.md` | Step 3 truth role reads | carrier read node | `SKILL.md` `N5-CARRIER-READ` + `references/system-data-flow.md` | split | high | data-flow Review Gate Mapping added | manual semantic check |
| `SKILL.md` | Step 4 cross-check rules | workflow / review | `SKILL.md` `N6-CROSS-CHECK` + `review/review-contract.md` | split | high | template split preserved | review gate |
| `SKILL.md` | Step 5 output contract | output template | `SKILL.md` + `templates/output-template.md` | split | high | output template alignment preserved | validator |
| `SKILL.md` | Quick Reference | command hints | `references/query-command-catalog.md` | move | low | unsupported `steps/` removed | smoke test |
| `SKILL.md` | Root-Cause 执行合同 | root-cause contract | `SKILL.md` | keep + align Skill 2.0 owners | high | owner paths updated | manual semantic check |
| `SKILL.md` | Lite Tier Field Mapping | field map | `SKILL.md` | keep + expand to runtime spine fields | medium | validator marker coverage updated | validator |
| `SKILL.md` | Completion Gate | output contract | `SKILL.md` + `review/review-contract.md` | split | medium | package delivery gate added | validator |
| `CONTEXT.md` | Type Map / Repair Playbook / Heuristics | experience layer | `CONTEXT.md` + `knowledge-base/query-heuristics.md` | keep + update runtime-spine heuristics | low | no `steps/`口径残留 | context audit |
| `references/system-data-flow.md` | data-flow spec | reference | `references/system-data-flow.md` | keep + add gate mapping | medium | referenced by `SKILL.md` | semantic check |
| `references/tag-specification.md` | manual XML spec | reference | `references/tag-specification.md` | keep + add gate mapping | low | manual_spec trigger retained | semantic check |
| `references/advanced/foreshadowing.md` | foreshadowing spec | reference | `references/advanced/foreshadowing.md` | keep + add gate mapping | low | quality trigger retained | semantic check |

## 2026-06-16 Runtime-Spine Upgrade

| source_path | source_section | content_class | target_path | operation | semantic_risk | module_authorization | reference_updates | validation_gate |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| old steps workflow file | Node Network | runtime node source | `SKILL.md` `Thinking-Action Node Map` | move + remove unsupported module | high | none; nodes owned by `SKILL.md` | README, CONTEXT, knowledge-base, legacy matrix | smoke route simulation |
| old steps workflow file | Project Root Guard | command detail | `references/query-command-catalog.md` | move | medium | `references/` row | SKILL Module Trigger Matrix | review gate |
| old steps workflow file | Carrier Read Rules | command detail | `references/query-command-catalog.md` + `references/system-data-flow.md` | split | high | `references/` row | no broken unsupported-module refs | validator + smoke |
| missing file | `types/type-map.md` | type package index | `types/type-map.md` | add | medium | `types/` row | SKILL Type Routing Matrix | validator |
| missing file | `test-prompts.json` | evaluation asset | `test-prompts.json` | add | medium | Evaluation Prompt Contract | README and CHANGELOG | validator |

## Unmigrated Or External References

- No skill directory path was renamed.
- The unsupported `steps/` file was removed after its node semantics moved to `SKILL.md` and its command details moved to `references/query-command-catalog.md`.
- Existing registry and root story skill entries still point to `.agents/skills/story/query`; no external path rewrite was required.

## Review Gate Mapping

| Review Question | Review Gate | Fail Code | Rework Target | Report Evidence |
| --- | --- | --- | --- | --- |
| 旧 section 和旧 `steps` 语义是否都有去向？ | 未迁移旧节点、命令或输出语义即失败 | `FAIL-QRY-MODULE-DRIFT` | 本文件 migration tables | migration matrix |
| 删除 `steps/` 后是否没有断链？ | 当前文件引用不再指向已删除路径，且目录扫描无 unsupported module 即失败 | `FAIL-QRY-MODULE-DRIFT` | README / CONTEXT / SKILL / references | reference scan |
| 新 runtime spine 是否能独立跑通查询路径？ | validator 或 smoke route simulation 失败即失败 | `FAIL-QRY-OUTPUT` | `SKILL.md` / `test-prompts.json` | validation and smoke output |
