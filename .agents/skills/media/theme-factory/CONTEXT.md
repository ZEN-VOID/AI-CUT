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
| 规则未命中导致输出偏离 | SKILL 合同层 | 修正触发条件与必填输入 | 在 SKILL 增加显式 gate 与失败分支 | 复跑同类输入，检查输出合同字段 |
| 运行成功但不可复用 | CONTEXT 经验层 | 提炼为 1-3 条 heuristic | 达到复现阈值后晋升到 SKILL/AGENT | 跨 2+ 场景复用一致生效 |

## Repair Playbook

1. 识别症状：记录失败现象或质量退化信号。
2. 层层上溯：`Symptom -> Direct Cause -> 规则源 -> 规则源的规则源`。
3. 先修源层：优先修复 SKILL / 模板 / 校验器 / 脚本中的高杠杆入口。
4. 再修局部：仅在必要时补充本次输出的局部修复。
5. 沉淀经验：把可复用策略写回 Type Map / Heuristics。
6. 验证闭环：提供证据路径与复验结果，确认可复现。

## Reusable Heuristics

- 先验证输入合同完整性，再执行生成或改写，避免下游返工。
- 优先修改可复用规则入口（模板/校验/脚本），而非仅修单次产物。
- 成功模式在跨场景复现达到阈值后再晋升到 SKILL/AGENT，避免过早固化。

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
