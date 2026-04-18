# CONTEXT.md

## Purpose & Loading Contract

- 本文件只服务 `step-5-data-writeback`，沉淀写回闭环与副作用开关的局部经验。
- 加载顺序固定为：先读同目录 `module-spec.md`，再按需读取本文件。
- 若经验涉及整条写作链的失败隔离策略，应回写根 `CONTEXT.md`。

## Context Health

- soft_limit_chars: 40000
- hard_limit_chars: 80000
- soft_limit_cases: 80
- hard_limit_cases: 140
- status: ok

## Type Map

| failure_or_outcome_type | root_cause_layer | immediate_fix | systemic_prevention | verification_point |
| --- | --- | --- | --- | --- |
| 把可选子步骤失败放大成整链失败 | failure isolation | 只重跑对应子步骤 | 固定 Step 5 最小失败隔离规则 | Step 1-4 不被误回滚 |
| 债务利息误开 | side-effect control | 按 appendix 回到默认关闭 | 在本模块中单点控制 debt switch | 无显式授权时 `debt_interest: skipped` |
| 白名单产物不全却结束流程 | acceptance gate | 回到核心写回重跑 | 把白名单检查写成结束前闸门 | state/index/summary 均存在 |

## Repair Playbook

1. 先查白名单产物。
2. 再查 scene / RAG / style extract 是否只是局部失败。
3. 再查 debt switch 是否被误开。
4. 最后看 timing 结论是否缺失。

## Reusable Heuristics

- Step 5 的首要任务是把“下一章会读到什么”写稳定，不是把所有附加处理都跑满。
- 只要核心白名单在，绝大多数 Step 5 问题都应局部补跑，不应回滚正文。
- 债务利息应被视为副作用开关，而不是默认流程的一部分。

