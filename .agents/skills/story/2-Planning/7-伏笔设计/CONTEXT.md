# CONTEXT.md

## Purpose & Loading Contract

- 本文件是 `7-伏笔设计` 子技能包的局部经验层，只服务 `2-Planning` Step 7。
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
| 伏笔只有提醒，没有完整状态链 | child contract | 回到铺设/加深/静默/兑现四段 | 在子技能中固定 lifecycle gate | board 能回答未来如何回照 |
| 把线索换个名字继续写 | boundary control | 区分可求证线索与未来再理解伏笔 | 固化“线索偏当前、伏笔偏未来” | Step 6/7 边界清楚 |
| 伏笔没有挂回 chapter board | patch writeback | 补 `board.foreshadows` refs | 固化本 child 对 foreshadow refs 的 ownership | query 可追踪静默区与兑现窗口 |

## Repair Playbook

1. 先确认 Step 6 的线索链已稳定。
2. 再锁值得长期埋藏的对象。
3. 再写铺设/加深/静默/兑现四段状态链。
4. 收尾把伏笔 refs 挂回 board。

## Reusable Heuristics

- 伏笔 child 的高杠杆不是“埋得多”，而是“回收时能否重估前文意义”。
- 若静默区缺失，伏笔通常会像作者频繁提醒，而不是自然回照。
- board 没有 foreshadow refs 时，后续很难判断一条伏笔是还活着还是已经失效。
