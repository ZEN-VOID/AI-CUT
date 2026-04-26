# Legacy Upgrade Matrix

本文件记录 `4-Review` 从旧父技能长文档升级到 Skill 2.0 分区包的迁移去向。

## Section Migration Matrix

| source_path | source_section | content_class | target_path | operation | semantic_risk | validation_gate |
| --- | --- | --- | --- | --- | --- | --- |
| `SKILL.md` | `Context Loading Contract` | entry contract | `SKILL.md` | keep + tighten | high | manual semantic check |
| `SKILL.md` | `Overview` | workflow summary | `SKILL.md` + `steps/review-workflow.md` | split + rewrite | medium | dynamic reference check |
| `SKILL.md` | `Parent Positioning` | ownership | `references/root-runtime-contract.md` | move + summarize | low | ownership check |
| `SKILL.md` | `Governed Child Skills` | registry contract | `references/shared-runtime-carrier.md` | move + summarize | high | registry link check |
| `SKILL.md` | `Execution Provider Contract` | review provider | `review/review-gate.md` | move + expand | high | provider aggregation check |
| `SKILL.md` | `Shared Canonical Sources` | loading guide | `SKILL.md` + `references/shared-runtime-carrier.md` | rewrite | medium | reference existence check |
| `SKILL.md` | `Canonical Runtime` | output paths | `references/root-runtime-contract.md` + `Output Contract` | split | low | output path check |
| `SKILL.md` | `Total Input Contract` | input contract | `SKILL.md` + `steps/review-workflow.md` | keep anchors + move rules | medium | covenant gate |
| `SKILL.md` | `Dispatch Order Contract` | steps topology | `steps/review-workflow.md` | rewrite as node network | medium | workflow gate |
| `SKILL.md` | `Aggregate Gate Contract` | review gate | `review/review-gate.md` | move + expand | high | verdict model |
| `SKILL.md` | `Routing Decision Contract` | route matrix | `references/root-runtime-contract.md` | move | low | route value check |
| `SKILL.md` | `Output Contract` | output anchor | `SKILL.md` + `templates/output-template.md` | keep + align | high | output template alignment |
| `SKILL.md` | `Completion Contract` | completion gate | `SKILL.md` + `review/review-gate.md` | merge | low | validator |

## Resource Migration Matrix

| source_path | target_path | operation | reason |
| --- | --- | --- | --- |
| `CONTEXT.md` | `CONTEXT.md` | keep | 已是经验层知识库 |
| `_shared/*` | `_shared/*` + `references/shared-runtime-carrier.md` | keep + document | runner 与 sibling 引用仍消费 `_shared` |
| `扩维与调整指南.md` | `扩维与调整指南.md` + `references/shared-runtime-carrier.md` | keep + reference | 维护 runbook，不是入口合同 |
| child `*/SKILL.md` | child `*/SKILL.md` | keep | 已具备 lite frontmatter、上下文合同与维度字段 |
| child `*/CONTEXT.md` | child `*/CONTEXT.md` | keep | 已是局部经验层 |
| `逻辑自洽校验/references/*` | same path | keep | 子技能私有细则，不上提到父层 |

## Non-Loss Notes

- 本次没有删除旧语义；旧父层长细则已分别被根 `SKILL.md`、`references/`、`steps/`、`review/`、`templates/` 承接。
- 本次没有重命名 `_shared/`，因此不需要同步改 runner 的 `_shared` 路径。
- 后续若拆迁 `_shared/`，必须按仓库重命名引用同步规则全仓扫描并更新。
