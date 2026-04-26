# Shared Runtime Carrier

`4-Review` 在升级为 Skill 2.0 后保留 `_shared/` 作为运行时兼容载体。canonical 分区负责入口、引用、审计和维护说明；`_shared/` 继续承载当前 runner 与 sibling skills 已消费的结构化合同。

## Current Shared Sources

| source | role | canonical relationship |
| --- | --- | --- |
| `_shared/validation-root-contract.md` | aggregate 单一真源与父层字段边界 | 被 `references/root-runtime-contract.md` 展开引用 |
| `_shared/validation-child-output-contract.md` | child packet / issue 字段骨架 | 被子技能与 `review/review-gate.md` 消费 |
| `_shared/validation-dimension-registry.yaml` | mandatory 维度、权重、inline hook 与 report filename 真源 | 维度调度唯一 registry |
| `_shared/validation-aggregate.template.json` | aggregate JSON 投影模板 | 与 `templates/output-template.md` 对齐 |
| `_shared/validation-dimension-report.template.md` | 维度报告模板 | 子技能 sidecar 渲染参考 |
| `_shared/validation-fact-pack-spec.md` | 当前轮 fact pack required slices | `steps/review-workflow.md` 的 covenant gate |
| `_shared/validation-team-contract.md` | validator roster 共享规则 | 维护时仍回指 registry |
| `_shared/checker-output-schema.md` | 结构化 findings/schema | `review/review-gate.md` 的 provider 汇流依据 |

## Compatibility Rule

- 本轮不重命名 `_shared/`，避免破坏 `.agents/skills/story/scripts/review_runner.py`、`workflow_manager.py`、`3-Drafting` 即时校验合同与历史测试引用。
- 新增或调整维度时，仍先改 `_shared/validation-dimension-registry.yaml`，再改对应 child package。
- 若未来决定把 `_shared/` 内容拆入 `references/` 或 `templates/`，必须先更新所有脚本、子技能、registry、runbook、README 与测试引用，再删除旧路径。

## Maintenance Entry

维护者快速入口仍为 `扩维与调整指南.md`，但它不得覆盖本文件与根 `SKILL.md` 的 Skill 2.0 分区职责。
