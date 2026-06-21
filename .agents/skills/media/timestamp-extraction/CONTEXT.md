# CONTEXT.md

## Context Health
<!-- CONTEXT_HEALTH_START -->
```yaml
monitor_version: 1
soft_limit_chars: 40000
hard_limit_chars: 80000
soft_limit_cases: 80
hard_limit_cases: 140
current_chars: 3192
current_lines: 60
current_cases: 0
status: ok
recommended_action: none
last_checked_at: 2026-06-21T06:49:48Z
```
<!-- CONTEXT_HEALTH_END -->

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
| 静音片段过多或过少 | 阈值配置层 | 根据素材噪声底重新调 `silence_thresh`、`min_silence_len` 与 `padding` | 按录音棚、采访/播客、嘈杂环境维护阈值预设，不把单个样本阈值泛化到所有视频 | 抽查 `silence_gaps` 是否符合人工听感，且切点未吃掉语音边缘 |
| 低置信度切点被下游直接采用 | confidence scoring 层 | 只交付高置信度切点，或把中低置信度标记为需人工确认 | 在交付说明中保留 confidence 分级含义，避免下游把所有 gap 当作等价剪辑点 | `timestamps.json` 中低置信度 gap 有明确标签或过滤策略 |
| 帧号与时间秒数互转偏移 | fps / VFR 解析层 | 改用真实 `pts_time` 或 ffprobe 元数据校准 | 执行前检测 VFR，并在 `metadata.json` 中记录时间基来源 | 关键 timestamp 转帧后误差不超过约定帧数 |
| 场景切换误检密集 | scene detector 参数层 | 调高 threshold、增加 `min_scene_len`，或切换 detector 类型 | 为访谈、播客、Vlog 等素材分开维护 detector 配置 | 抽查 `scene_changes` 是否匹配实际镜头切换 |
| 播客/纯音频任务浪费在场景检测 | 任务类型路由层 | 使用 `audio_only` 或关闭 `detect_scenes` | 模板选择先判断素材媒介：播客用 podcast 模板，访谈/Vlog 才考虑场景检测 | 输出不包含无意义的 scene 文件，处理时间符合音频任务预期 |
| 无音轨、路径错误或格式不可读 | input validation 层 | 先用 ffprobe/路径检查中止并报告具体素材问题 | 批量任务执行前做统一预检，失败项不要进入检测主链 | 错误信息能指向具体 `video_path`、缺失音轨或解码失败原因 |
| 快速模式结果被当作最终精剪依据 | performance mode 层 | 对最终交付关闭会影响精度的跳过项，必要时重跑标准模式 | 把 `fast_mode`、`audio_only`、`skip_confidence_scoring` 标注为迭代/降级选项 | `metadata.json` 能看出是否启用快速或跳过项 |
| 输出文件缺项导致剪辑技能无法接手 | output contract 层 | 补齐 `timestamps.json`、`silence_gaps.json`、`scene_changes.json`、`metadata.json` 中适用文件 | 交付前做输出清单校验，场景检测关闭时也要说明 `scene_changes` 缺席原因 | 下游能从输出目录直接读取时间戳、静音、场景和执行元数据 |

## Repair Playbook

1. 先判定任务类型：静音剪点、语音边界、场景切换、帧/时间码转换、批量检测，避免把所有素材都套同一模板。
2. 读取素材元数据：时长、fps、是否 VFR、音轨、采样率、声道；路径或音轨异常时先报告，不进入主链。
3. 按素材类型选择模板或参数：录音棚更低阈值，标准采访/播客用中等阈值，户外/餐厅等嘈杂环境提高阈值并延长最小静音。
4. 静音检测异常时，先抽取代表片段试跑阈值，再全量执行；不要用一次全量失败反复猜参数。
5. 场景检测异常时，先调整 detector 类型、threshold 与 `min_scene_len`；纯音频或播客任务直接关闭场景检测。
6. 涉及 VFR 或非整数帧率时，优先使用 `pts_time` 与 ffprobe 元数据校准，不用 `frame / fps` 做长期累计换算。
7. 输出给剪辑技能前，检查适用的 `timestamps.json`、`silence_gaps.json`、`scene_changes.json` 与 `metadata.json` 是否齐备，并保留置信度与时间基来源。
8. 若某类素材形成稳定阈值经验，优先沉淀到 Reusable Heuristics；重复验证后再考虑晋升到模板预设或校验脚本。

## Reusable Heuristics

- 静音检测的阈值应跟素材噪声底绑定，不应直接复用另一个项目的默认值。
- 录音棚素材可从 `silence_thresh=-60dB`、`min_silence_len=300ms` 起步；标准采访/播客可从 `-50dB`、`500ms` 起步；嘈杂环境可从 `-40dB`、`800ms` 起步。
- `padding` 是保护句子边缘的剪辑安全垫；切掉字尾时先加 padding，不要只降低阈值。
- VFR 素材优先相信 `pts_time`，不要用 `frame / fps` 做长期累计换算。
- 高置信度 gap 可作为候选剪点；中置信度 gap 应标记为人工确认；低置信度 gap 默认不推荐给自动剪辑。
- 播客、有声书、纯音频访谈优先关闭场景检测；访谈视频和 Vlog 才把 scene changes 作为剪辑辅助信号。
- `fast_mode` 和 `audio_only` 适合迭代或音频任务；如果最终交付需要场景信息、完整置信度或波形，不应把快速模式结果当作最终真源。
- 输出给后续剪辑的时间戳必须保留秒数、帧号、SMPTE 时间码和来源 metadata，便于下游复核。

## Promotion Backlog

- 为输出目录补一个轻量 validator：检查适用 JSON 文件、时间基来源、confidence 字段和任务成功/失败计数。
- 为批量任务补 dry-run 预检：提前报告缺音轨、路径不存在、不可解码和 VFR 状态。
- 将稳定素材阈值沉淀为模板说明或模板参数，不把一次性项目参数直接写入 `SKILL.md`。
- 增加一条下游 handoff 清单：交给剪辑技能前必须说明模板、阈值、是否启用场景检测、是否为快速模式。
