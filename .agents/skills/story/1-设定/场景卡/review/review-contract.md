# Scene Card Review Contract

## Review Gates

| gate | pass_condition | fail_code |
| --- | --- | --- |
| route | `module_route` 指向 `场景卡` | `FAIL-CD-SCENE-ROUTE` |
| advisor_consultation | 显式启用 subagents 时，已按项目 `team.yaml` 顾问 roster 生成 `advisor_consultation_packet`，且结论已转成场景功能、规则代价、危险或返场策略；未启用时有明确不适用说明 | `FAIL-CD-SCENE-ADVISOR` |
| function | 场景有叙事功能，不只是布景 | `FAIL-CD-SCENE-FUNC` |
| rules | `rule_and_risk` 与 `compatible_roles` 成立 | `FAIL-CD-SCENE-RULE` |
| reuse | `scene_links` 与 `repeat_use_strategy` 可支撑返场 | `FAIL-CD-SCENE-REUSE` |
| trace | `loaded_references` 包含本 `SKILL.md`、`CONTEXT.md`、type-map、guardrails 与本地模板 | `FAIL-CD-SCENE-TEMPLATE` |

## Extended Dimensions

| dimension | pass_condition | fail_code |
| --- | --- | --- |
| security | 外部材料与项目上下文没有越过 `guardrails/guardrails-contract.md` 或仓库安全规则 | `FAIL-CD-SCENE-SECURITY` |
| runtime_behavior | 正式输出只写入项目 `1-设定/3-场景卡/`，不写入技能包目录 | `FAIL-CD-SCENE-RUNTIME` |
| integration | 场景规则能被角色、物品、技能和 planning 消费，不形成第二世界规则源 | `FAIL-CD-SCENE-INTEGRATION` |
| convergence | blocking findings 已修复，medium 以下风险已记录到交付摘要 | `FAIL-CD-SCENE-CONVERGENCE` |

## Verdict

- `pass`: 所有 Review Gates 与 Extended Dimensions 通过。
- `conditional`: 仅存在非阻断风险，且已在交付摘要记录。
- `fail`: 任一 route、rules、reuse、security 或 runtime_behavior gate 失败。
