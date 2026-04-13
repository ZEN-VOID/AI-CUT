# CONTEXT.md

## Purpose & Loading Contract

- 本文件是 `resume/` 的经验层知识库，不是执行流水账。
- 每次调用 `resume/` 时，应自动预加载本文件，用于恢复范围判定、危险动作过滤与回接 heuristics。
- 冲突优先级固定为：用户显式请求 > `AGENTS.md` / 元规则 > `SKILL.md` > `CONTEXT.md`。

## Context Health

- soft_limit_chars: 20000
- hard_limit_chars: 40000
- status: ok

## Type Map

| failure_or_outcome_type | root_cause_layer | immediate_fix | systemic_prevention | verification_point |
| --- | --- | --- | --- | --- |
| 把仓库根目录误判为项目根目录 | project-root guard | 先锁定 `projects/<项目名>/` | 在 `SKILL.md` 固定 project-root 判定顺序 | 恢复建议基于真实项目目录 |
| 缺 `mission-brief / route-plan / preflight-verdict` 仍直接建议续跑 | governance gate | 先回根 `aigc` 或 `review/` 补 gate | 把高风险续跑写成门下省前置硬门槛 | 恢复建议不再跳过治理工件 |
| 只有 `project_state.yaml` 没有结构化治理快照，导致断点只能靠摘要猜 | governance snapshot contract | 先补 `governance-state.yaml` | 在 `0-Init` 固定初始化即生成治理快照 | 恢复模式能回读 `last_stable_checkpoint` 与 `resume_contract` |
| 把轻量初始化态一律判成 `governance_rebuild` | init layering contract | 先检查 `project_state.yaml + Init/* + team.yaml` 是否完整，再决定是否必须补治理快照 | 在 resume 合同中新增 `lightweight_init_continue` | 低风险续跑不会被不必要的治理补件阻塞 |
| 只凭最近修改文件猜阶段，忽略 `project_state.yaml` | runtime truth contract | 同时读 `project_state` 与阶段产物 | 在 reference 固定“状态 + 产物双证据” | 恢复模式会给出证据来源 |
| 默认给 destructive Git 建议 | safety contract | 改成 preview / inspect / reroute | 在技能与 reference 双层写死禁止项 | 恢复话术里不再出现危险默认动作 |
| 把 review 问题当成 resume 问题 | satellite boundary | 进入 `review/` 做 preflight 或 validation bridge | 在恢复模式表里单列 `review_reentry` | 恢复输出会给唯一下一入口 |

## Repair Playbook

1. 先确认 `PROJECT_ROOT`。
2. 再读 `project_state + mission-brief + route-plan + preflight + validation`。
3. 用“治理工件 + 阶段产物 + 工作区证据”三层交叉判定恢复模式。
4. 一旦涉及高风险继续执行，先回 `review/` 或根 `aigc`，不直接往下跑。
5. 优先输出唯一下一入口，不输出模糊候选列表。

## Reusable Heuristics

- `resume/` 恢复的不是“用户记忆里的上一步”，而是“系统还能证明的最后稳定入口”。
- 对 `aigc` 来说，治理工件缺口通常比内容产物缺口更先阻断续跑。
- 只要恢复结论需要用到“是否可以继续执行”，就应该先看 `preflight-verdict` 是否存在、是否仍有效。
- 若阶段已搁浅，恢复入口应该回到根 `aigc`，而不是硬闯阶段目录。
- `resume/` 最稳的输入不是聊天回忆，而是 `governance-state.yaml` 里的结构化 checkpoint，再用 `project_state.yaml` 做人类摘要校对。
- 若只是轻量初始化后的低风险续跑，`project_state.yaml + Init/*` 已足够决定下一入口；不要为了补齐全套治理工件而卡住创作起跑。
