# Character Card Review Contract

## Review Gates

| gate | pass_condition | fail_code |
| --- | --- | --- |
| route | `module_route` 指向 `角色卡` | `FAIL-CD-CHAR-ROUTE` |
| advisor_consultation | 显式启用 subagents 时，已按项目 `team.yaml` 顾问 roster 生成 `advisor_consultation_packet`，且结论已转成角色职责、人物弧、关系载体或专属物接口指导；未启用时有明确不适用说明 | `FAIL-CD-CHAR-ADVISOR` |
| roster | 全剧集 roster 闭合，无单章临时卡 | `FAIL-CD-CHAR-ROSTER` |
| shaping | desire/flaw/wound/need/change 落到结构字段 | `FAIL-CD-CHAR-SHAPING` |
| growth | 主角成长合同与当前态成立 | `FAIL-CD-CHAR-GROWTH` |
| interface | `exclusive_item_hooks` 可被物品卡消费 | `FAIL-CD-CHAR-CLOSURE` |
| graph | `角色关系图谱.md` 有文字说明与 Mermaid 图，且只作为 side output | `FAIL-CD-CHAR-GRAPH` |
| trace | `loaded_references` 包含本 `SKILL.md`、`CONTEXT.md`、type-map、guardrails 与本地模板 | `FAIL-CD-CHAR-TEMPLATE` |

## Extended Dimensions

| dimension | pass_condition | fail_code |
| --- | --- | --- |
| security | 外部材料与项目上下文没有越过 `guardrails/guardrails-contract.md` 或仓库安全规则 | `FAIL-CD-CHAR-SECURITY` |
| runtime_behavior | 正式输出只写入项目 `1-设定/2-角色卡/`，不写入技能包目录 | `FAIL-CD-CHAR-RUNTIME` |
| integration | 角色最小投影能被场景、物品、技能、planning 和 drafting 消费，不复制完整角色真源 | `FAIL-CD-CHAR-INTEGRATION` |
| convergence | blocking findings 已修复，medium 以下风险已记录到交付摘要 | `FAIL-CD-CHAR-CONVERGENCE` |

## Verdict

- `pass`: 所有 Review Gates 与 Extended Dimensions 通过。
- `conditional`: 仅存在非阻断风险，且已在交付摘要记录。
- `fail`: 任一 route、roster、shaping、growth、security 或 runtime_behavior gate 失败。
