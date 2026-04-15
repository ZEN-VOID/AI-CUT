# CONTEXT.md

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
| 批量渲染中途失败后产物混杂 | 执行目录 / 临时文件层 | 清理本轮临时目录并只重跑失败任务 | 每个任务使用独立 temp/output 路径，报告中记录输入、输出和失败原因 | 输出目录只包含本轮有效产物和可追踪报告 |
| MoviePy / ffmpeg 编解码参数不兼容 | 工具链配置层 | 降级 codec、preset 或音频参数后重跑最小样例 | 在模板中保留兼容参数，并记录平台特定 fallback | 最小片段能成功导出且可被播放器打开 |

## Repair Playbook

1. 先确认输入素材、剪辑计划、timestamp JSON 与输出路径是否一一对应。
2. 对切点问题，优先核对 fps / VFR / timecode，再调整 segment 配置。
3. 对渲染失败，先用短片段和单任务复现，再扩大到批量计划。
4. 对音频问题，单独检查采样率、声道、loudness 与 ducking 参数。
5. 修复后保留可复跑的 plan 或最小命令，并把可复用经验沉淀回本文件。

## Reusable Heuristics

- 视频剪辑任务先固定时间基，再谈转场和特效；否则后续所有切点都会漂移。
- 批量渲染要把每个任务的 temp/output/report 隔离开，失败恢复会简单很多。
- 与 timestamp-extraction 串联时，最稳路径是直接消费结构化 JSON，而不是复制时间点到临时文本。
