# CONTEXT.md

## Context Health
<!-- CONTEXT_HEALTH_START -->
```yaml
monitor_version: 1
soft_limit_chars: 40000
hard_limit_chars: 80000
soft_limit_cases: 80
hard_limit_cases: 140
current_chars: 2486
current_lines: 56
current_cases: 0
status: ok
recommended_action: none
last_checked_at: 2026-06-21T06:49:48Z
```
<!-- CONTEXT_HEALTH_END -->

## Purpose & Loading Contract

- 本文件是该技能的经验上下文知识库（不是执行日志）。
- 技能每次被调用时，应自动预加载同目录 `CONTEXT.md`，用于策略选择、避坑与修复分支决策。
- 若 `SKILL.md` 与 `CONTEXT.md` 发生冲突，优先级遵循：用户显式请求 > AGENT.md / 元规则 > SKILL.md > CONTEXT.md。

## Context Health

- soft_limit_chars: 40000
- hard_limit_chars: 80000
- status: ok
- action_policy:
  - ok: 优先更新 Type Map / Repair Playbook / Reusable Heuristics。
  - warn: 对当前技能上下文做定向压缩与结构整理。
  - critical: 先归档旧案例，再继续大规模追加。

## Type Map

| failure_or_outcome_type | root_cause_layer | immediate_fix | systemic_prevention | verification_point |
|---|---|---|---|---|
| emoji / message GIF 目标混淆 | 输入澄清层 | 先确认目标场景；emoji 默认 128x128，消息 GIF 默认 480x480 | 在动手生成帧前固定 `width`、`height`、`fps`、时长预算 | `validate_gif(..., is_emoji=...)` 与实际 Slack 场景一致 |
| GIF 体积或尺寸不符合 Slack 场景 | SKILL 合同层 | 回到 Slack 约束，重新设置尺寸、帧率、色彩数和时长 | 在开始制作前先确认 emoji/message GIF 的目标类型 | 检查导出 GIF 尺寸、时长、颜色数和文件大小 |
| 文件压缩后主体不可辨识 | 优化策略层 | 优先减帧率、时长、重复帧和颜色数；必要时再降尺寸 | 只有在用户要求缩小体积或验证失败时才做强压缩 | 小尺寸预览下主体、动作和文字仍清晰 |
| 动画效果生硬或视觉质量差 | 规则应用层 | 使用 easing、分层构图和更厚实的图形描边重新设计帧 | 将“视觉精修”作为生成前检查项，而不只关注能动起来 | 预览 GIF 是否平滑、清晰、可辨识 |
| 依赖 emoji 字体或预置素材导致跨平台不稳 | 素材实现层 | 改用 PIL primitives 或用户上传图像；不要假设技能内有素材库 | 绘制方案默认用几何图形、渐变、描边、图层和自定义组合 | 在目标机器上重新打开 GIF，确认没有缺字或替换字形 |
| 用户上传图像用途判断错误 | 输入解释层 | 明确区分“直接动画化/拆帧”和“仅参考风格/配色” | 处理上传图像前先建立用途判断，不把参考图自动当素材落入输出 | 输出是否符合用户对原图保真或灵感转译的预期 |
| 成功形成可复用的 Slack GIF 模板 | CONTEXT 经验层 | 提炼为尺寸/FPS/配色/动作节奏 heuristic | 在跨 2+ GIF 主题复用后晋升到 `SKILL.md` 或 helper 示例 | 不同主题下都能稳定输出 Slack 友好 GIF |

## Repair Playbook

1. 先定目标：判断是 Slack emoji、消息 GIF，还是用户上传图像的动画化/风格参考。
2. 固定约束：按目标设置画布、FPS、时长、颜色数和是否启用 `optimize_for_emoji`。
3. 修实现层：用 PIL primitives、渐变、厚描边、图层和 easing 生成帧；避免 emoji 字体和不存在的预置素材。
4. 修视觉层：若画面像占位图，优先增加层次、对比、轮廓和节奏变化，而不是只堆更多帧。
5. 修体积层：若验证或用户要求缩小体积，按“减时长/帧率 -> 减颜色 -> 去重复帧 -> 降尺寸”的顺序处理。
6. 验证闭环：用 validator 检查尺寸和 Slack readiness，再用实际预览确认小尺寸下仍清晰流畅。
7. 经验沉淀：只把跨主题可复用的参数组合、动作套路和失败修复写回本文件。

## Reusable Heuristics

- 先确定是 Slack emoji 还是消息内 GIF，再决定尺寸、时长和文件大小预算。
- emoji GIF 优先用 128x128、短时长、10-12 FPS、48 色左右起步；消息 GIF 可放宽到 480x480 和更丰富的帧数/色彩。
- 好的 Slack GIF 通常先赢在辨识度和节奏，而不是细节复杂度；小尺寸下轮廓要比细碎纹理更重要。
- 如果目标是更小文件，优先减帧率、减时长、减颜色和删除重复帧，而不是先牺牲主体清晰度。
- 视觉精修的默认抓手是厚线条、强对比、渐变背景、局部高光、内外层叠和缓动函数组合。
- 旋转、弹跳、脉冲、滑入、粒子等动作可以组合，但每个 GIF 应保留一个主动作焦点，避免 128x128 下信息拥挤。
- 用户上传图像如果是“直接使用”，先保持主体构图和色彩；如果是“作为灵感”，只提取风格，不把原图强行贴入。

## Promotion Backlog

- 若同一类 emoji 参数预设跨 2+ 主题稳定复用，可晋升为 `SKILL.md` 示例或 helper preset。
- 若多次出现同一类压缩失败，可补一个 validator wrapper，自动给出尺寸/FPS/颜色数调整建议。
- 若某类视觉套路反复成功（如 bounce+shine、pulse+ring），可沉淀为绘制片段，但不要把技能变成僵硬模板库。
