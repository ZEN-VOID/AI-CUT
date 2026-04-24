# Skill 2.0 Upgrade Migration Matrix

本文件记录 `北冥神功` 从单一主合同型包升级为 Skill 2.0 包时的语义去向。删除或收束旧段落前必须能追到新 owner。

## Section Migration Matrix

| source_path | source_section | content_class | target_path | operation | semantic_risk | reference_updates | validation_gate |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `SKILL.md` | frontmatter、触发描述 | 入口发现 | `SKILL.md`、`agents/openai.yaml` | rewrite | medium | registry/routes 保持路径不变 | validator + discovery check |
| `SKILL.md` | Context Loading Contract | 上下文合同 | `SKILL.md` | keep and tighten | high | 无路径变化 | manual semantic check |
| `SKILL.md` | 定位、何时使用、非目标 | 入口边界 | `SKILL.md` | summarize | medium | README 补概览 | manual semantic check |
| `SKILL.md` | 总输入合同 | 输入合同 | `SKILL.md` | rewrite as Input Contract | high | templates/output-template 对齐 | validator |
| `SKILL.md` | Visual Maps、思行节点 | steps 拓扑 | `steps/skills-update-absorption-workflow.md` | move and expand | medium | SKILL Reference Loading Guide 回链 | review gate |
| `SKILL.md` | Companion Contract、reviewer 触发 | 审计合同 | `review/review-contract.md` | move and normalize | high | SKILL Completion gate 回链 | local review |
| `SKILL.md` | 执行硬规则 | 主流程门禁 | `SKILL.md`、`steps/`、`review/` | split | high | README owner 摘要 | manual semantic check |
| `SKILL.md` | Skills-Update Self-Learning Contract | 学习闭环 | `steps/`、`CONTEXT.md`、`knowledge-base/` | split | medium | CHANGELOG 记录 | learning check |
| `SKILL.md` | 字段中心映射 | 字段合同 | `SKILL.md`、`types/upgrade-point-type-map.md` | split | medium | output template 对齐 | validator |
| `SKILL.md` | 输出合同 | 输出合同 | `SKILL.md`、`templates/output-template.md` | rewrite | high | templates 对齐 Output Contract 五字段 | validator |
| `SKILL.md` | Root-Cause 执行合同 | 根因合同 | `SKILL.md` | keep and normalize heading | medium | 无路径变化 | validator |
| `references/upgrade-point-absorption-map.md` | 全文 | 判型细则 | `references/upgrade-point-absorption-map.md` | keep | low | SKILL 引用保持 | link check |
| `CONTEXT.md` | Type Map、Repair Playbook、Reusable Heuristics | 经验层 | `CONTEXT.md` | keep and de-log | medium | Case Log 收束到 CHANGELOG/knowledge-base | context check |
| `CHANGELOG.md` | 变更史 | 时间序 | `CHANGELOG.md` | append | low | 无路径变化 | manual check |

## Resource Migration Matrix

| source_path | target_path | operation | validation_gate |
| --- | --- | --- | --- |
| `references/upgrade-point-absorption-map.md` | `references/upgrade-point-absorption-map.md` | keep | link check |
| missing `agents/openai.yaml` | `agents/openai.yaml` | create | validator |
| missing `README.md` | `README.md` | create | validator |
| missing `TODO.md` | `TODO.md` | create | validator |
| missing `steps/` | `steps/skills-update-absorption-workflow.md` | create | review gate |
| missing `types/` | `types/upgrade-point-type-map.md` | create | validator |
| missing `review/` | `review/review-contract.md` | create | review gate |
| missing `templates/` | `templates/output-template.md`、`templates/absorption-summary.template.md` | create | validator |
| missing `scripts/` | `scripts/README.md` | create placeholder | validator |
| missing `knowledge-base/` | `knowledge-base/skills-update-heuristics.md` | create | context check |

## Reference Sync Result

- `.codex/registry/skills.yaml`: canonical path unchanged; no update required.
- `.codex/registry/routes.yaml`: route path unchanged; no update required.
- Markdown links in `SKILL.md`: updated to Skill 2.0 owner paths.
- External or binary references: none detected in repository scan for `北冥` / `beiming`.
