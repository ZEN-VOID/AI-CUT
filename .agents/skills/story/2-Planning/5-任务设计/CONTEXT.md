# CONTEXT.md

## Purpose & Loading Contract

- 本文件是 `5-任务设计` 子技能包的局部经验层，只服务 `2-Planning` Step 5。
- 加载顺序固定为：先读同目录 `SKILL.md`，再按需读取本文件。

## Context Health

- soft_limit_chars: 40000
- hard_limit_chars: 80000
- soft_limit_cases: 80
- hard_limit_cases: 140
- status: ok

## Type Map

| failure_or_outcome_type | root_cause_layer | immediate_fix | systemic_prevention | verification_point |
| --- | --- | --- | --- | --- |
| 目标链模糊，只剩动作口号 | child contract | 回到主线/阶段/行动/隐藏任务四层 | 在子技能固定 goal chain gate | board 能回答本章角色要达成什么 |
| 没有门槛与代价，任务像旁白提示 | risk contract | 补 `entry_requirement/cost/reward/failure` | 把风险收益闭环写成硬门 | 后续线索链不再像作者分配任务 |
| 任务没有挂回 chapter board | patch writeback | 补 `board.missions` refs | 固化本 child 对 mission refs 的 ownership | 下游不再失去章节目标入口 |

## Repair Playbook

1. 先确认 Step 4 的冲突网络已经稳定。
2. 再锁目标链层次。
3. 再把门槛、代价、收益和失败后果写实。
4. 收尾把任务 refs 挂回 board。

## Reusable Heuristics

- 任务 child 最怕“看起来很忙，但没人真的有明确目标”。
- 只要代价和失败后果是虚的，任务线程就很难驱动后续线索。
- 若 board 上没有 mission refs，query 和 drafting 很容易只看到事件，不知道角色动机。
