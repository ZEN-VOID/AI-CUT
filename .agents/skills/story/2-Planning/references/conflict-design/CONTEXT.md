# CONTEXT.md

## Purpose & Loading Contract

- 本文件是 `conflict-design` 子模块的局部经验层，只服务 `2-Planning` 的 Step 4。
- 加载顺序固定为：先读同目录 `module-spec.md`，再按需读取本文件。
- 跨模块的长线升级规律、holomap 状态流经验仍回写到 `2-Planning/CONTEXT.md`。

## Context Health

- soft_limit_chars: 40000
- hard_limit_chars: 80000
- soft_limit_cases: 80
- hard_limit_cases: 140
- status: ok

## Type Map

| failure_or_outcome_type | root_cause_layer | immediate_fix | systemic_prevention | verification_point |
| --- | --- | --- | --- | --- |
| 冲突只有情绪词没有 owner | step contract | 回到 owner / pressure source 判定 | 在 `module-spec.md` 固化冲突 owner 与状态流 | holomap 能追踪谁在施压 |
| 强冲突过早耗尽 | gradient control | 重排升级链与解决窗口 | 强制区分主压迫源与辅增压源 | 后续章节仍保有冲突梯度 |
| 冲突与任务脱节 | handoff contract | 用冲突网络重做任务触发逻辑 | 固化 Step 5 必读本模块输出 | 任务链能解释“为何必须行动” |

## Repair Playbook

1. 先判定主压迫源与辅增压源。
2. 再设计升级链与解决窗口。
3. 用任务系统反查冲突是否能逼出行动。
4. 最后用 holomap 检查状态流是否可挂章追踪。

## Reusable Heuristics

- 冲突是否成立，看的是压力如何持续，不是场面是否热闹。
- 同时存在多条冲突时，最重要的是谁在当主压迫源。
- 如果任务没有被冲突逼出来，通常说明 Step 4 还停留在“有矛盾”的描述层。

