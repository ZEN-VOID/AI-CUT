# CONTEXT.md

## Context Health
<!-- CONTEXT_HEALTH_START -->
```yaml
monitor_version: 1
soft_limit_chars: 40000
hard_limit_chars: 80000
soft_limit_cases: 80
hard_limit_cases: 140
current_chars: 2989
current_lines: 61
current_cases: 0
status: ok
recommended_action: none
last_checked_at: 2026-06-21T06:49:48Z
```
<!-- CONTEXT_HEALTH_END -->

## Purpose & Loading Contract

- 本文件是 `video-editing` 技能的经验层知识库，不是过程日志。
- 调用同目录 `SKILL.md` 时，必须同时加载本文件作为预加载上下文，用于策略选择、风险识别与修复分支判断。
- 冲突优先级遵循：用户显式请求 > 仓库 `AGENTS.md` / 元规则 > 同目录 `SKILL.md` > 本 `CONTEXT.md`。

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
| --- | --- | --- | --- | --- |
| 时间戳剪辑后音画或切点偏移 | 素材时间基 / fps 合同层 | 重新核对源视频 fps、VFR 信息和 timestamp-extraction 输出格式 | 在执行前固定时间基，优先用同一份 timestamp JSON 驱动剪辑计划 | 抽查关键切点帧与音频边界是否对齐 |
| 静音删除误剪自然停顿 | timestamp 置信度 / 剪辑策略层 | 提高 `confidence_threshold`，恢复低置信度 gap 或设置更长 `min_gap_duration` | 静音删除默认保守；对访谈、冥想、演讲类素材保留自然停顿 | 对比删除前后语义停顿是否仍自然 |
| 批量渲染中途失败后产物混杂 | 执行目录 / 临时文件层 | 清理本轮临时目录并只重跑失败任务 | 每个任务使用独立 temp/output 路径，报告中记录输入、输出和失败原因 | 输出目录只包含本轮有效产物和可追踪报告 |
| MoviePy / ffmpeg 编解码参数不兼容 | 工具链配置层 | 降级 codec、preset 或音频参数后重跑最小样例 | 在模板中保留兼容参数，并记录平台特定 fallback | 最小片段能成功导出且可被播放器打开 |
| 输出文件体积过大或渲染过慢 | 编码配置 / 性能层 | 调整 bitrate、resolution、preset、threads 或硬件编码参数 | 按交付平台预设输出配置，避免每次从默认高码率开始 | 输出大小、清晰度和编码耗时符合任务目标 |
| 转场或拼接点出现跳帧、闪黑、伪影 | 转场参数 / 关键帧层 | 改用 crossfade/fade-to-black，延长转场，必要时 snap to keyframe | 剪辑计划中显式记录 transition type 与 duration，不把转场留给隐式默认 | 逐帧检查 2-3 个关键拼接点 |
| 字幕、标题或图形覆盖不可见 / 出框 | overlay 样式 / 画布适配层 | 调整 position、margin、fontsize、stroke/background 和字体路径 | 在模板中把 16:9、竖屏、字幕安全区分开配置 | 截取关键帧确认文字可读且不遮挡主体 |
| 多轨音频混合压过人声或响度不稳 | audio mixing / loudness 层 | 单独调整 background volume、ducking、normalize 与 target loudness | 音频处理先做短样本验证，再进入全片渲染 | 人声清晰，背景音乐只在非讲话处抬起 |

## Repair Playbook

1. 先确认输入素材、剪辑计划、timestamp JSON / scene JSON、素材资产与输出路径是否一一对应。
2. 与 `timestamp-extraction` 串联时，直接消费结构化 JSON；不要把时间点手工复制成临时文本再剪。
3. 对切点问题，先核对 fps / VFR / timecode，再用短片段复现，最后调整 segment、transition 或 gap handling。
4. 对渲染失败，先单任务、短片段、低分辨率复现；确认 codec、preset、audio_codec、temp_dir、磁盘空间和内存后再恢复批量。
5. 对音频问题，单独检查采样率、声道、loudness、ducking 和背景音乐起止点。
6. 对字幕 / 标题 / 图形覆盖问题，导出关键帧截图检查安全区、描边、背景和字体可用性。
7. 批量任务只重跑失败 task，并保留 execution report 中的失败原因、输入路径和输出路径。
8. 完成后至少打开输出文件，核对 duration、fps、resolution、audio stream 和若干关键切点。

## Reusable Heuristics

- 视频剪辑任务先固定时间基，再谈转场和特效；否则后续所有切点都会漂移。
- 静音删除不是越多越好；访谈、播客、冥想和叙事内容默认优先保留低置信度停顿。
- 批量渲染要把每个任务的 temp/output/report 隔离开，失败恢复会简单很多。
- 与 timestamp-extraction 串联时，最稳路径是直接消费结构化 JSON，而不是复制时间点到临时文本。
- 预览阶段优先用 proxy 或短片段，最终阶段再回到原素材和目标分辨率。
- 能一次合并的剪切、转场、混音和字幕叠加不要拆成多轮级联转码，除非用户明确要中间产物。
- 字幕和图形覆盖必须按目标画幅检查；横屏模板不能直接假设适配竖屏或裁切版。
- `plan_executor` 的 JSON plan 是可复跑真源；临时命令行参数只适合作为调试入口。

## Promotion Backlog

- 增加 plan preflight：检查输入文件、timestamp/scene JSON、asset、output_path、temp_dir 与 task_id 唯一性。
- 增加 ffmpeg/MoviePy 环境 smoke test：验证 codec、audio_codec、hardware_accel 和最小片段导出。
- 增加 `--smoke-render` 或等价短片段模式，用于全片渲染前验证切点、转场、字幕和音频混合。
- 增加输出 QA manifest：记录 duration drift、fps、resolution、音频流、文件大小和关键切点抽查结果。
- 把 VFR 转 CFR、硬件编码 fallback、字幕安全区模板沉淀为脚本级或模板级预检规则。
