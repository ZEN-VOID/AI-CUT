# Context: wjs-segmenting-video

## Context Health
<!-- CONTEXT_HEALTH_START -->
```yaml
monitor_version: 1
soft_limit_chars: 40000
hard_limit_chars: 80000
soft_limit_cases: 80
hard_limit_cases: 140
current_chars: 2617
current_lines: 48
current_cases: 0
status: ok
recommended_action: none
last_checked_at: 2026-06-21T06:49:48Z
```
<!-- CONTEXT_HEALTH_END -->

本文件是 `wjs-segmenting-video` 技能的经验层知识库，用于沉淀可复用的失败模式、修复策略和运行启发。它不重定义同目录 `SKILL.md` 的入口、路由、输出合同或完成门禁。

## Type Map

| symptom | root_cause_layer | immediate_fix | systemic_prevention | verification |
| --- | --- | --- | --- | --- |
| 没有 SRT 就开始按视频猜主题 | input routing | 先转 `wjs-transcribing-audio` 生成字幕 | 本技能入口固定为长视频 + SRT | 存在 source video、source SRT 和目标平台 |
| 用脚本/NLP 自动决定 topic boundaries | authorship boundary | Agent 通读 SRT 后重新人工判断语义边界 | `segment.py` 只负责切割，不负责选题 | `segments.json` 的每段有自洽标题、摘要、起止时间 |
| clip 开头多出前一句，字幕领先音频 | cut accuracy | 用 `--reencode` 重新 accurate-seek 切割 | stream-copy 只用于已强制关键帧的源视频 | 抽查 clip 起点与 per-clip SRT t=0 对齐 |
| 切在半句话或一个话题中途 | semantic boundary | snap 到 SRT cue 边界，调整到完整 hook/payoff | 选段必须自包含、单线程、不截断句子 | 冷观众能独立理解，且结尾不是半句 |
| 横屏素材直接交给竖屏平台 | orientation gate | probe 分辨率并询问是否调用 reframing | 每段切完后先做平台方向检查 | 用户确认后才 crop；匹配时明确跳过 |
| MediaPipe 零检测仍继续用中心裁剪 | crop fallback | 改用 deterministic fixed crop，并抽 midpoint frame 目检 | `0 face observations` 视为失败，低检测率不必然失败 | midpoint frame 里说话人居中，不是背景居中 |
| 在本技能里烧字幕、做封面、CTA 或最终包装 | handoff boundary | 停在 raw clips + per-clip SRT，转 `wjs-overlaying-video` | 后期包装归 overlay 技能，避免重复编码链 | 输出包只含 clip、SRT、frame、segments.json |
| 下游找不到 title / cover_prompt / frame | handoff artifact | 补齐 `segments.json` 元数据并重提取 frame | segmentation 阶段负责 downstream metadata，不负责渲染 | 每个 segment 有 slug/title/summary/cover_prompt 和对应 frame |

## Repair Playbook

1. 先确认输入是长视频、SRT 和目标平台；没有 SRT 时先转写，不进入 segmentation。
2. 通读 SRT，由 agent 判断 3-6 个强语义片段；每段检查自包含、单线程、长度、hook/payoff、SRT cue 边界。
3. 写 `segments.json`，确保 slug、title、summary、start/end、cover_prompt 都可供下游复用。
4. 默认用 `segment.py --reencode` accurate-seek 切割，并抽 midpoint frame。
5. probe 源/clip 方向；与平台不匹配时先问用户，再调用 reframing。
6. crop 后必须重提取 frame；遇到 0 face observations 时改 fixed crop 并目检。
7. 用 `burn_subs.py --no-burn` 切 per-clip SRT，确认时间戳从 0 开始。
8. 交付 exact handoff package 后转 `wjs-overlaying-video`，不要在本技能追加封面、字幕渲染或 CTA。

## Reusable Heuristics

- 3-6 段强片段比“尽量用满素材”更符合本技能目标；无聊中段应丢弃。
- `cover_prompt` 在 segmentation 阶段写，是为了让 overlay 不再反问，不代表本技能生成封面。
- 标题是传播判断，不是摘要字段；应人工压成 2 行以内，而不是直接复制 transcript 句子。
- 低 face-on-screen detection 不一定失败；零 landmark 才是必须切换方案的强信号。
- per-clip SRT 应对齐 clip 本地时间轴 t=0，下游 overlay 的 cover_duration 是另一层时间轴。
- 准确切割优先级高于省时；除非源视频已按边界强制关键帧，否则不要 stream-copy。

## Promotion Backlog

- 增加 `segments.json` validator，校验 schema、时间顺序、slug/title/cover_prompt 和段长区间。
- 增加 orientation preflight，自动输出源宽高、目标平台方向和是否需要用户确认。
- 增加 keyframe-drift smoke check，用于发现误用 stream-copy 导致的字幕提前。
- 增加 handoff manifest，列出每段 clip / SRT / frame / metadata 是否齐全。

## Case Log

暂无案例。后续只追加可复用、可验证、可晋升的案例。
