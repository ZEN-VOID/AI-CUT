# Query Review Contract

本文件定义 `$story-query` 的质量门禁。它不改写业务真源，只检查查询回答是否有证据、是否误判 truth layer、是否混淆计划、当前态、实绩与执行态。

## Verdict Model

| verdict | meaning |
| --- | --- |
| `pass` | 可以回答用户查询 |
| `pass_with_gaps` | 可回答，但需要明确缺失 carrier、legacy fallback 或 validation gap |
| `needs_clarification` | 无法唯一定位项目根或查询目标 |
| `blocked` | 必要 carrier 不可读，且没有安全 fallback |

## Gate Checklist

| gate_id | check | fail code |
| --- | --- | --- |
| `GATE-QRY-01` | 已加载 `SKILL.md + CONTEXT.md` | `FAIL-QRY-CONTEXT` |
| `GATE-QRY-02` | 已锁定或报告无法锁定 `PROJECT_ROOT` | `FAIL-QRY-PROJECT-ROOT` |
| `GATE-QRY-03` | 已判定 truth role | `FAIL-QRY-TRUTH-ROLE` |
| `GATE-QRY-04` | 每个结论有证据路径、字段或 CLI 输出 | `FAIL-QRY-EVIDENCE` |
| `GATE-QRY-05` | “已经发生 / 已兑现 / 已通过”带 actualization + PASS 证据，或明确说未见证据 | `FAIL-QRY-ACTUALIZATION` |
| `GATE-QRY-06` | `core/current_state`、`planned/actual`、`workflow_state/execution_state` 未混答 | `FAIL-QRY-LAYER-MIX` |
| `GATE-QRY-07` | legacy fallback 明确标注，不冒充 canonical | `FAIL-QRY-LEGACY` |

## Provider Note

`query/` 默认不需要真实 subagent reviewer。若上游任务把本查询包纳入 Skill 2.0 结构审计，可按 `skill-工作车间` 的 review provider 规则另行调度；若上层策略阻断真实 subagent，则降级为本地 checklist 并报告阻断来源。

本仓库的上层运行策略只允许在用户显式要求 subagents / delegation / parallel agent work 时启动真实 subagent；因此普通 `$story-query` 执行默认采用本地 gate checklist。
