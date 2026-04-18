# CONTEXT.md

## Purpose & Loading Contract

- 本文件是 `4-冲突设计` 子技能包的局部经验层，只服务 `2-Planning` Step 4。
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
| 冲突只剩情绪词，没有归属关系 | child contract | 回到 owner / pressure source | 在子技能中固定 owner gate | board 能说明谁压迫谁 |
| 强冲突过早耗尽，没有梯度 | escalation contract | 回修 escalation ladder | 在输出中保留 release window 与阶段压力 | 后续任务系统仍有驱动力 |
| 冲突没有挂回 chapter board | patch writeback | 补 `board.conflicts` refs | 固化本 child 的 board conflict ownership | 下游不再失去章节冲突入口 |

## Repair Playbook

1. 先看 story spine 是否稳定。
2. 再锁 owner 与 pressure source。
3. 再写升级链与解决窗口。
4. 收尾把冲突 refs 挂回 board。

## Reusable Heuristics

- 冲突 child 的价值不在“写多少打架”，而在“让对抗归属与梯度可追踪”。
- 如果 board 上看不到 conflict refs，后续任务链通常会漂成被动应对。
- 强冲突过早耗尽，往往不是内容太弱，而是 Step 4 提前把梯度用光了。
