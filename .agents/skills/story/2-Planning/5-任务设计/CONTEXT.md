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
| 任务很多但没有主支关系 | topology design | 先做 `mainline/sideline` 判型，再删掉 filler 支线 | 在主合同固定四象限诊断节点 | 支线能明确改变主线资源、关系或时间差 |
| 暗线任务像作者私设 | reveal contract | 为每条暗线补 `surface_goal + true_intent + reveal_trigger` | 在模板固定明暗成对槽位 | 暗线都有明确 reveal / reversal 时机 |
| 每章只有事件没有目标 | board binding | 把任务 refs 回挂到 `bundled_elements.missions`，并说明单线收束例外 | 在子技能固定章节必答问题 | 任一章节都能回答“台面任务 + 里层任务” |
| 任务 thread 直接复制人物卡/关系图正文 | cross-stage bridge | 只保留 `owners / counterparts / relationship_edge_refs` | 共享桥固定任务 child 只写角色/关系引用与 hook | 任务线可追溯到角色与关系，但不会变成第二份人物设定 |

## Repair Playbook

1. 先确认 Step 4 的冲突网络已经稳定。
2. 先做 `主线/支线 + 明线/暗线` 四象限判型，不要先写任务名。
3. 再锁 `surface_goal / true_intent / reveal_trigger`。
4. 再把门槛、代价、收益和失败后果写实。
5. 收尾把任务 refs 挂回 board，并标注单线收束例外。

## Reusable Heuristics

- 任务 child 最怕“看起来很忙，但没人真的有明确目标”。
- 只要代价和失败后果是虚的，任务线程就很难驱动后续线索。
- 若 board 上没有 mission refs，query 和 drafting 很容易只看到事件，不知道角色动机。
- 主线任务负责决定读者为什么继续追，支线任务负责让主线付出更具体的代价。
- 暗线任务不是“保密信息”，而是“暂不公开的真实任务”；没有 reveal trigger 的暗线几乎必废。
- 当一章只保留单线时，必须是刻意聚焦，而不是因为设计者忘了检查四象限。
- 任务设计最稳的角色绑定方式是写 `owners / counterparts / relationship_edge_refs`，而不是把人物卡摘要直接塞进 thread。
- 十集分片模式下，`mission_threads` 留在 global root，章节目标挂载与 window 明细写入 slice；否则 drafting 会拿到两份不一致的任务债务。
