# CONTEXT.md

## Purpose & Loading Contract

- 本文件只服务 `step-2-style-pass`，用于记录风格转译阶段的局部经验。
- 加载顺序固定为：先读同目录 `module-spec.md`，再按需读取本文件。
- 若经验跨到 Step 4 的问题修复或 Step 1 的执行包设计，应回写根 `CONTEXT.md`。

## Context Health

- soft_limit_chars: 40000
- hard_limit_chars: 80000
- soft_limit_cases: 80
- hard_limit_cases: 140
- status: ok

## Type Map

| failure_or_outcome_type | root_cause_layer | immediate_fix | systemic_prevention | verification_point |
| --- | --- | --- | --- | --- |
| 风格改写误伤剧情事实 | boundary control | 先锁禁改项再改写 | 把事实边界前置到本模块 Phase 1 | 事件顺序与角色结果保持不变 |
| 改得更像润色，不像风格转译 | step boundary | 回收到表达层，只保留句式、口感、节奏修正 | 强化 Step 2B / Step 4 边界 | Step 3 仍有可检问题，不被提前吃掉 |
| 为了局部 craft 过度加读，改写成本失控 | load strategy | 只命中一个最必要 leaf note | 由本模块统一裁决 craft 加读入口 | 改写动作与症状一一对应 |

## Repair Playbook

1. 先锁禁改项。
2. 再处理长句、抽象句、说明腔。
3. 最后才按症状决定是否加读 craft note。
4. 若出现“像在修问题”，立即回收给 Step 4。

## Reusable Heuristics

- Step 2B 的最佳状态是“让文本更会说话”，而不是“把所有问题都提前修完”。
- 一次只引入一个 craft 专项，通常比同时叠多种风格技巧更稳。
- 如果改写日志说不清自己改了什么，通常说明这轮改写超出了表达层边界。

