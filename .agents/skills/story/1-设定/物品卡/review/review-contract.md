# Item Card Review Contract

## Review Gates

| gate | pass_condition | fail_code |
| --- | --- | --- |
| route | `module_route` 指向 `物品卡` | `FAIL-CD-ITEM-ROUTE` |
| advisor_consultation | 显式启用 subagents 时，已按项目 `team.yaml` 顾问 roster 生成 `advisor_consultation_packet`，且结论已转成归属链、启用规则、代价、专属适配或线索功能；未启用时有明确不适用说明 | `FAIL-CD-ITEM-ADVISOR` |
| function | 物品有剧情杠杆，不只是命名设定 | `FAIL-CD-ITEM-FUNC` |
| cost | `ownership_links / usage_rules / costs` 闭合 | `FAIL-CD-ITEM-OWN` |
| fit | `exclusive_fit` 吸收角色和场景上游接口 | `FAIL-CD-ITEM-EXCLUSIVE` |
| trace | `loaded_references` 包含本 `SKILL.md`、`CONTEXT.md`、type-map、guardrails 与本地模板 | `FAIL-CD-ITEM-TEMPLATE` |

## Extended Dimensions

| dimension | pass_condition | fail_code |
| --- | --- | --- |
| security | 外部材料与项目上下文没有越过 `guardrails/guardrails-contract.md` 或仓库安全规则 | `FAIL-CD-ITEM-SECURITY` |
| runtime_behavior | 正式输出只写入项目 `1-设定/4-物品卡/`，不写入技能包目录 | `FAIL-CD-ITEM-RUNTIME` |
| integration | 物品代价与角色、场景、技能和世界规则接口一致 | `FAIL-CD-ITEM-INTEGRATION` |
| convergence | blocking findings 已修复，medium 以下风险已记录到交付摘要 | `FAIL-CD-ITEM-CONVERGENCE` |

## Verdict

- `pass`: 所有 Review Gates 与 Extended Dimensions 通过。
- `conditional`: 仅存在非阻断风险，且已在交付摘要记录。
- `fail`: 任一 route、cost、fit、security 或 runtime_behavior gate 失败。
