# CONTEXT.md

## Purpose & Loading Contract

- 本文件是 `类型兑现` 子技能包的局部经验层，只服务 type-pack fit 维度。
- 加载顺序固定为：先读同目录 `SKILL.md`，再按需读取本文件。
- 跨维度聚合经验优先回写到 `4-Validation/CONTEXT.md`。

## Context Health

- soft_limit_chars: 40000
- hard_limit_chars: 80000
- soft_limit_cases: 80
- hard_limit_cases: 140
- status: ok

## Type Map

| failure_or_outcome_type | root_cause_layer | immediate_fix | systemic_prevention | verification_point |
| --- | --- | --- | --- | --- |
| 类型兑现问题被静默并入结构问题，导致返工入口不稳定 | dimension boundary | 独立输出 `type-pack-fit-validator` packet | registry 固定把类型兑现做成独立维度 | 聚合 JSON 里能看到独立维度结果 |
| 已声明 pack，但正文仍按通用文风写，缺少类型特征 | pack projection | 直接回指 active pack 的 required hooks | step hooks 与 validation hooks 共同进入 runtime | 当前章能被解释为“为什么不像当前类型” |
| drafting inline 看不到当前 step 的类型约束 | step projection | 透传 `current_step_id`，按 step hook 判定 | step-specific hook 统一从 pack 真源读取 | Step 2/5/7 等节点能看到不同提示与不同 fail |

## Repair Playbook

1. 先确认 `type_stack` 是否真的激活，而不是误把 `_base` 当成强类型包。
2. 再区分问题属于“pack 选错”“planning 没投影”“drafting 没兑现”中的哪一类。
3. 若当前是 drafting inline，优先看 step hook，再看整章类型承诺。

## Reusable Heuristics

- 类型兑现维度最常见的假通过，是“文本不差，但完全不像当前项目自称的那一类作品”。
- 若 pack 已声明 step hook，inline validation 就不该只检查通用质量，还要检查该 step 是否做了类型化动作。
