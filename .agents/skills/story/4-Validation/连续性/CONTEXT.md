# CONTEXT.md

## Purpose & Loading Contract

- 本文件是 `连续性` 子技能包的局部经验层，只服务连续性验收维度。
- 加载顺序固定为：先读同目录 `SKILL.md`，再按需读取本文件。
- 跨维度的 route 经验仍优先回写到父层 `CONTEXT.md`。

## Context Health

- soft_limit_chars: 40000
- hard_limit_chars: 80000
- soft_limit_cases: 80
- hard_limit_cases: 140
- status: ok

## Type Map

| failure_or_outcome_type | root_cause_layer | immediate_fix | systemic_prevention | verification_point |
| --- | --- | --- | --- | --- |
| 本集开篇像重启，不像承接 | carryover bridge | 回到上一集终稿抓真正停点 | 把上一集终稿固定成 `N > 1` 的硬输入 | 连续性报告能具体说出“从哪里接上” |
| 场景在切，但 reader debt 没跟着走 | thread continuity | 记录断掉的是哪条关系/任务/悬念线 | 在维度指标里固定 `thread_drop_count` | issue 不再只写“衔接一般” |
| 连续性问题被混成节奏评价，没有明确返工入口 | rework routing | 强制标 `1-起盘` 或 `2-节奏优化` | 子技能输出固定带 `rework_target_step` | drafting 能精确返工 |

## Repair Playbook

1. 先读上一集终稿最后一个真正改变局面的点。
2. 再看本集开篇是否回应了那个点，而不是只换了场景或天气。
3. 最后检查本集内部各条活跃线是否在推进时保持可追踪。

## Reusable Heuristics

- 连续性不是“人物名字和地点没写错”，而是读者上一章记着的压力，这一章有没有真的接住。
- 若问题只能被描述成“读着有点断”，通常说明还没把断在哪条线上找出来。
