# CONTEXT.md

## Purpose & Loading Contract

- 本文件是该技能的经验上下文知识库（不是执行日志）。
- 技能每次被调用时，应自动预加载同目录 `CONTEXT.md`，用于策略选择、避坑与修复分支决策。
- 若 `SKILL.md` 与 `CONTEXT.md` 发生冲突，优先级遵循：用户显式请求 > AGENT.md / 元规则 > SKILL.md > CONTEXT.md。

## Context Health

- soft_limit_chars: 40000
- hard_limit_chars: 80000
- soft_limit_cases: 80
- hard_limit_cases: 140
- status: ok
- action_policy:
  - ok: 优先更新 Type Map / Repair Playbook / Reusable Heuristics。
  - warn: 对当前技能上下文做定向压缩与结构整理。
  - critical: 先归档旧案例，再继续大规模追加。

## Type Map

| failure_or_outcome_type | root_cause_layer | immediate_fix | systemic_prevention | verification_point |
|---|---|---|---|---|
| 滚动效果炫但不可用 | SKILL 合同层 | 回退到更轻量的动画与更清晰的内容层级 | 在设计前先确认 narrative beat 与交互目的，再选动画库 | 检查可读性、滚动控制权和 CTA 可达性 |
| 滚动驱动动画卡顿 | 规则应用层 | 减少主线程开销、缩减触发器和重绘范围 | 在实现前设定性能预算和移动端降级策略 | 复查 FPS、滚动流畅度和移动端发热 |
| 成功产出具有节奏感的叙事页面 | CONTEXT 经验层 | 提炼为 section cadence 和 reveal 节奏 heuristic | 在跨 2+ 页面验证后晋升到 `SKILL.md` | 检查不同内容密度下是否仍然自然 |

## Repair Playbook

1. 识别症状：确认是叙事节奏问题、性能问题还是交互控制问题。
2. 层层上溯：`Symptom -> Direct Cause -> 规则源 -> 规则源的规则源`。
3. 先修源层：优先修正技能中的动画选择规则、节奏建议和降级策略。
4. 再修局部：调整具体 section、trigger、sticky 区域和视觉层级。
5. 沉淀经验：把可复用的叙事节奏与性能预算规则写回知识库。
6. 验证闭环：桌面端和移动端都确认滚动顺畅、内容可读、交互可控。

## Reusable Heuristics

- 先定义“滚动要讲什么故事”，再决定用 GSAP、Framer Motion 还是原生 CSS，而不是先堆技术。
- 每个 scroll beat 最好只承担一个主要情绪或信息目标，能明显降低用户疲劳。
- 任何滚动特效都必须有移动端降级方案，否则很容易从“沉浸”变成“阻碍”。

## Case Log

> 仅记录里程碑案例（milestone-grade），避免过程流水账。

### Case-000 (placeholder)

- milestone_type: new_success_class
- outcome: 待补充
- root_cause_or_design_decision: 待补充
- final_fix_or_heuristic: 待补充
- prevention_or_replication_checklist: 待补充
- evidence_paths: 待补充
- user_feedback_or_constraint: 待补充
