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
| 用 CSS 动画替代帧驱动导致渲染异常 | SKILL 合同层 | 改回 `useCurrentFrame()` + `interpolate()` 驱动 | 在实现检查单中加入“所有动画必须可被帧重放” gate | 预览和导出结果是否一致 |
| 片段时长或序列衔接错误 | 规则应用层 | 重新计算 fps、durationInFrames 与 sequence offset | 在开工前先画时间线，再落组件结构 | 检查 composition 总时长和转场边界 |
| 成功建立可复用的视频组件模式 | CONTEXT 经验层 | 提炼为 composition contract 和 props 设计 heuristic | 在跨 2+ 视频模板复用后晋升到 `SKILL.md` | 不同视频主题下仍能稳定复用 |

## Repair Playbook

1. 识别症状：确认问题出在动画驱动、时序、素材处理还是字幕/音频同步。
2. 层层上溯：`Symptom -> Direct Cause -> 规则源 -> 规则源的规则源`。
3. 先修源层：优先修正时间线规划、composition 约束和素材使用规则。
4. 再修局部：调整具体插值、sequence、caption timing 或媒体处理代码。
5. 沉淀经验：把稳定有效的视频结构与时间线 heuristics 写回知识库。
6. 验证闭环：在 Remotion Studio 预览与导出结果间做一致性确认。

## Reusable Heuristics

- 在 Remotion 里先定义 composition 的时长、fps 和内容节拍，再写视觉组件，返工会少很多。
- 把文字、媒体、音频、字幕分别抽成可组合层，比把所有逻辑塞进一个 composition 更稳定。
- 能在预览阶段暴露的问题，尽量不要等到最终 render 才发现，所以 sequence 边界和媒体时长要尽早核对。

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
