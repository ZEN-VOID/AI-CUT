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
| GIF 体积或尺寸不符合 Slack 场景 | SKILL 合同层 | 回到 Slack 约束，重新设置尺寸、帧率、色彩数和时长 | 在开始制作前先确认 emoji/message GIF 的目标类型 | 检查导出 GIF 尺寸、时长和文件大小 |
| 动画效果生硬或视觉质量差 | 规则应用层 | 使用 easing、分层构图和更厚实的图形描边重新设计帧 | 将“视觉精修”作为生成前检查项，而不只关注能动起来 | 预览 GIF 是否平滑、清晰、可辨识 |
| 成功形成可复用的 Slack GIF 模板 | CONTEXT 经验层 | 提炼为尺寸/FPS/配色/动作节奏 heuristic | 在跨 2+ GIF 主题复用后晋升到 `SKILL.md` | 不同主题下都能稳定输出 Slack 友好 GIF |

## Repair Playbook

1. 识别症状：确认问题出在 Slack 限制、视觉质量、动作节奏还是文件大小。
2. 层层上溯：`Symptom -> Direct Cause -> 规则源 -> 规则源的规则源`。
3. 先修源层：优先修正尺寸、FPS、颜色数和优化策略的默认判断。
4. 再修局部：调整具体帧内容、缓动、颜色搭配和图形细节。
5. 沉淀经验：把高频可复用的 GIF 参数组合和视觉套路写回知识库。
6. 验证闭环：确认 GIF 在 Slack 目标场景下清晰、流畅、体积合适。

## Reusable Heuristics

- 先确定是 Slack emoji 还是消息内 GIF，再决定尺寸、时长和文件大小预算。
- 好的 Slack GIF 通常先赢在辨识度和节奏，而不是细节复杂度。
- 如果目标是更小文件，优先减帧率、减时长、减颜色，而不是先牺牲主体清晰度。

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
