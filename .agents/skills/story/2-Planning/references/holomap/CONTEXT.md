# CONTEXT.md

## Purpose & Loading Contract

- 本文件是 `holomap` 子模块的局部经验层，只服务 `2-Planning` 的 Step 8。
- 加载顺序固定为：先读同目录 `module-spec.md`，再按需读取本文件。
- 跨模块的最早失稳回溯经验、下游消费合同仍优先回写到 `2-Planning/CONTEXT.md`。

## Context Health

- soft_limit_chars: 40000
- hard_limit_chars: 80000
- soft_limit_cases: 80
- hard_limit_cases: 140
- status: ok

## Type Map

| failure_or_outcome_type | root_cause_layer | immediate_fix | systemic_prevention | verification_point |
| --- | --- | --- | --- | --- |
| holomap 退化成摘要页 | truth contract | 回修 chapter boards、cross_thread_indexes 与三轴组织 | 在 `module-spec.md` 固化六问底盘与三轴门禁 | 下游可默认 holomap-first |
| 三轴不全，只剩时间轴 | structure contract | 补齐空间轴与集序轴映射 | 把 three-axis gate 写成 Step 8 硬门禁 | 每章都有时间/空间/集序挂载 |
| actualization 覆盖 planned state | state contract | 改写到并存容器，不覆盖 `planned_*` | 把 actualization gate 固化到子模块合同 | loopback 写回后仍保留规划真源 |

## Repair Playbook

1. 先确认前 1-7 已稳定，再进入收束。
2. 先建三轴和 chapter boards，再挂跨线程索引。
3. 用六问底盘检查每章节点密度。
4. 最后检查下游是否能 holomap-first，以及 actualization 是否独立容纳。

## Reusable Heuristics

- holomap 的价值不在“信息最多”，而在“下游不需要重新拼导航层”。
- 如果 chapter board 不能回答六问，holomap 就还只是摘要页。
- Step 8 出问题时，最稳的修法通常不是继续补 holomap，而是回溯前 1-7 的最早失稳点。

