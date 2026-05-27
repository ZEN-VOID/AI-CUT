# Query Review Contract

本文件定义 `$aigc-query` 的质量门禁。它不改写业务真源，只检查查询回答是否有证据、是否误判真源、是否混淆验收状态。

## Verdict Model

| verdict | meaning |
| --- | --- |
| `pass` | 可以回答用户查询 |
| `pass_with_gaps` | 可回答，但需要明确缺失 carrier 或 legacy fallback |
| `needs_clarification` | 无法唯一定位项目根或查询目标 |
| `blocked` | 必要 carrier 不可读，且没有安全 fallback |

## Gate Checklist

| gate_id | check | fail code |
| --- | --- | --- |
| `GATE-QUERY-01` | 已加载 `SKILL.md + CONTEXT.md` | `FAIL-QUERY-CONTEXT` |
| `GATE-QUERY-02` | 已锁定或报告无法锁定 `PROJECT_ROOT` | `FAIL-QUERY-PROJECT-ROOT` |
| `GATE-QUERY-03` | 已判定 truth role | `FAIL-QUERY-TRUTH-ROLE` |
| `GATE-QUERY-04` | 每个结论有证据路径 | `FAIL-QUERY-EVIDENCE` |
| `GATE-QUERY-05` | 完成/通过类结论带验收证据或明确说未见验收 | `FAIL-QUERY-VALIDATION` |
| `GATE-QUERY-06` | legacy fallback 明确标注，不冒充 canonical | `FAIL-QUERY-LEGACY` |
| `GATE-QUERY-07` | 已按 truth role 读取 `system-data-flow.md` 声明的 canonical carrier，缺失时才降级到安全 fallback | `FAIL-QUERY-CARRIER` |
| `GATE-QUERY-08` | 路由制度、技能状态或治理系统类问题已读取 registry/routes 与相关阶段 `SKILL.md` | `FAIL-QUERY-GOVERNANCE` |

## Provider Note

`query/` 默认不需要顾问与复核流程 reviewer。若上游任务把本查询包纳入 Skill 2.0 结构审计，可按 `skill-工作车间` 的 review provider 规则另行调度；若顾问与复核流程不可用，则直接使用本地 checklist。
