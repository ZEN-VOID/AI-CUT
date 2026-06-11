# Scope Package: Tone Contract

## Selection Signals

- 题材、风格、语体、价值口径、叙述距离、AI 检测风险、表达分布、角色声口、读者承诺。

## When X Then Check X

| when | must check |
| --- | --- |
| 改题材承诺 | `0-初始化/north_star.yaml`、MEMORY、整体规划、卷规划 |
| 改价值口径或禁区 | MEMORY、项目 CONTEXT、north_star、已有敏感场景 |
| 改局部语体 | 同章前后句群、同卷文本分布、阶段根技能合同 |
| 改润色风格 | `4-润色` 根技能合同、执行报告、AI 检测风险上下文 |

## Required Impact Additions

- `tone_source_refs`
- `style_distribution_refs`
- `execution_context_refs`
- `memory_or_context_guardrail`
- `future_tone_constraints`

## Review Gate

- 风格修复不改事实。
- 局部润色没有扩大成未授权整章重写。
- 旧风格口径不会从 MEMORY、north_star 或阶段执行上下文回流。
