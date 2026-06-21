# CONTEXT.md

## Context Health
<!-- CONTEXT_HEALTH_START -->
```yaml
monitor_version: 1
soft_limit_chars: 40000
hard_limit_chars: 80000
soft_limit_cases: 80
hard_limit_cases: 140
current_chars: 2919
current_lines: 57
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
| 用 CSS 动画替代帧驱动导致渲染异常 | SKILL 合同层 | 改回 `useCurrentFrame()` + `interpolate()` 驱动 | 在实现检查单中加入“所有动画必须可被帧重放” gate | 预览和导出结果是否一致 |
| 片段时长或序列衔接错误 | 规则应用层 | 重新计算 fps、durationInFrames 与 sequence offset | 在开工前先画时间线，再落组件结构 | 检查 composition 总时长和转场边界 |
| 动态素材时长、尺寸或 props 未进入 composition 元数据 | Compositions & Metadata 层 | 用 `calculateMetadata` 或媒体探测结果回写 duration、dimensions、props | 凡时长依赖音频/视频/数据输入，先做 metadata preflight，再注册 composition | Studio 预览、最终 render 时长和首尾帧不截断 |
| 图片、视频、音频、GIF 等素材按假设直接使用后失帧或黑屏 | Assets & Media 层 | 先确认可解码、时长、尺寸和实际帧，再决定裁剪、循环或缩放 | 对外部素材建立导入前检查：decode、duration、dimensions、extract frame | 关键帧截图非空，音视频长度和 timeline 对齐 |
| 字幕或标题在竖屏/窄屏 composition 中溢出 | Text & Typography / Captions 层 | 测量最长文本，分页或缩小字号，必要时调整 caption page 与 word highlight 结构 | 所有字幕/标题组件必须以最长文案做 overflow gate | 最长文本帧在目标分辨率内完整可读 |
| Three.js、Lottie、Tailwind 等高级集成预览可见但 render 不稳定 | Advanced Features / Styling 层 | 收敛到 Remotion 支持的确定性渲染路径，避免依赖浏览器运行时副作用 | 高级集成先做最小 composition smoke，再接入主时间线 | Studio 与导出帧在相同 frame 上视觉一致 |
| 成功建立可复用的视频组件模式 | CONTEXT 经验层 | 提炼为 composition contract 和 props 设计 heuristic | 在跨 2+ 视频模板复用后晋升到 `SKILL.md` | 不同视频主题下仍能稳定复用 |

## Repair Playbook

1. 识别症状：确认问题出在动画驱动、时序、素材处理还是字幕/音频同步。
2. 层层上溯：`Symptom -> Direct Cause -> 规则源 -> 规则源的规则源`。
3. 先修源层：优先修正 composition 元数据、fps、durationInFrames、props 和素材 preflight，而不是只调局部样式。
4. 再修局部：按问题类型调整 `interpolate()`、`Sequence` offset、media trim、caption timing、font fitting 或高级集成配置。
5. 对动态输入视频，先确认素材时长/尺寸/可解码性，再决定 composition 总长和段落节拍。
6. 对字幕、标题、数据可视化等文字密集场景，用最长文本帧做截图检查，避免只看短样例。
7. 沉淀经验：把稳定有效的视频结构、时间线 heuristics 和 props contract 写回知识库。
8. 验证闭环：在 Remotion Studio 预览与导出结果间做一致性确认，至少抽查首帧、关键转场帧、字幕最长帧和尾帧。

## Reusable Heuristics

- 在 Remotion 里先定义 composition 的时长、fps 和内容节拍，再写视觉组件，返工会少很多。
- 把文字、媒体、音频、字幕分别抽成可组合层，比把所有逻辑塞进一个 composition 更稳定。
- 能在预览阶段暴露的问题，尽量不要等到最终 render 才发现，所以 sequence 边界和媒体时长要尽早核对。
- 所有动画都应该能由同一个 frame number 重放；如果依赖 CSS animation、wall-clock time 或随机副作用，导出稳定性会下降。
- 数据驱动视频优先让 props 和 metadata 表达业务事实，让组件只负责投影和动画。
- 字幕与文字动画要先解决可读性、换行和溢出，再叠加运动效果；动效不能掩盖信息不可读。
- 3D、Lottie、图表等复杂层应先做独立 composition smoke，再并入主片段，避免在完整 render 才暴露环境或资源问题。

## Promotion Backlog

- 将“动态素材 preflight -> `calculateMetadata` -> composition 注册”的流程沉淀为可复用检查单；跨多个 Remotion 项目稳定后再晋升到 `SKILL.md`。
- 补一个 caption/text overflow smoke 模式：用最长字幕或标题抽帧验证竖屏、横屏和窄屏 composition。
- 若多次出现素材黑屏或时长截断，考虑把 decode/duration/dimensions 检查固化为脚本或模板级门禁。
