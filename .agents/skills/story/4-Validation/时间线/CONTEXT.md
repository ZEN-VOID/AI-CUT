# CONTEXT.md

## Purpose & Loading Contract

- 本文件是 `时间线` 子技能包的局部经验层，只服务时间线维度。
- 加载顺序固定为：先读同目录 `SKILL.md`，再按需读取本文件。
- 聚合层的总 route 与 handoff 经验优先回写到父层。

## Context Health

- soft_limit_chars: 40000
- hard_limit_chars: 80000
- soft_limit_cases: 80
- hard_limit_cases: 140
- status: ok

## Type Map

| failure_or_outcome_type | root_cause_layer | immediate_fix | systemic_prevention | verification_point |
| --- | --- | --- | --- | --- |
| 时间顺序错，但报告没有证据锚点 | time anchor read | 回到 `chapter_planning_packet` 的时间锚重新比对 | 时间线 issue 必须回指锚点或时序句 | 返工不再停留在“感觉不对” |
| 伏笔提前揭晓，被漏判成普通逻辑问题 | silence window check | 单独标成 `spoiler_risk` | 在维度输出中固定保留 `spoiler_risk` | 父层可直接聚合剧透风险 |
| 时长不合理和节奏过快被混为一谈 | boundary split | 先区分时间物理矛盾与阅读速度问题 | 时间线维度只抓可回指的时序/时长冲突 | `时间线` 与 `连续性/节奏` 边界更清楚 |

## Repair Playbook

1. 先锁本章 planning 时间锚和伏笔静默窗口。
2. 再把正文事件按发生顺序排一遍，看是否有硬冲突。
3. 最后判断问题该回到起盘还是节奏优化，不要直接笼统打回整章。

## Reusable Heuristics

- 时间线维度最怕把“快”误当“乱”；只有回指到时间锚和事件顺序，问题才是可修的。
- 伏笔窗口一旦被提前揭开，往往不只是风格问题，而是直接影响闭环的验收问题。
