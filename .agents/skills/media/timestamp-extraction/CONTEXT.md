# CONTEXT.md

## Purpose & Loading Contract

- 本文件是 `timestamp-extraction` 技能的经验层知识库，不是过程日志。
- 调用同目录 `SKILL.md` 时，必须同时加载本文件作为预加载上下文，用于阈值选择、边界判断与修复分支决策。
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
| 静音片段过多或过少 | 阈值配置层 | 根据素材响度重新调 `silence_thresh`、`min_silence_len` 与 padding | 按素材类型保留阈值预设，不把单个样本阈值泛化到所有视频 | 抽查输出 gaps 是否符合人工听感 |
| 帧号与时间秒数互转偏移 | fps / VFR 解析层 | 改用真实 `pts_time` 或 ffprobe 元数据校准 | 执行前检测 VFR，并在 metadata 中记录时间基来源 | 关键 timestamp 转帧后误差不超过约定帧数 |
| 场景切换误检密集 | scene detector 参数层 | 调高 threshold 或增加 `min_scene_len` | 为访谈、播客、Vlog 等素材分开维护 detector 配置 | 抽查 scene_changes 是否匹配实际镜头切换 |

## Repair Playbook

1. 先读取素材元数据：时长、fps、音轨、采样率、是否 VFR。
2. 静音检测异常时，先抽取一小段做阈值试跑，再运行全量。
3. 场景检测异常时，先调整 detector 类型和 threshold，再决定是否关闭场景检测。
4. 输出给剪辑技能前，检查 `timestamps.json`、`silence_gaps.json`、`scene_changes.json` 与 `metadata.json` 是否齐备。
5. 若某类素材形成稳定阈值经验，优先沉淀到 Reusable Heuristics 或模板预设。

## Reusable Heuristics

- 静音检测的阈值应跟素材噪声底绑定，不应直接复用另一个项目的默认值。
- VFR 素材优先相信 `pts_time`，不要用 `frame / fps` 做长期累计换算。
- 输出给后续剪辑的时间戳必须保留秒数、帧号和来源 metadata，便于下游复核。
