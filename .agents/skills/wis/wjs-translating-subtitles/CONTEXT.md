# Context: wjs-translating-subtitles

## Context Health
<!-- CONTEXT_HEALTH_START -->
```yaml
monitor_version: 1
soft_limit_chars: 40000
hard_limit_chars: 80000
soft_limit_cases: 80
hard_limit_cases: 140
current_chars: 2536
current_lines: 52
current_cases: 0
status: ok
recommended_action: none
last_checked_at: 2026-06-21T06:49:48Z
```
<!-- CONTEXT_HEALTH_END -->

本文件是 `wjs-translating-subtitles` 技能的经验层知识库，用于沉淀可复用的失败模式、修复策略和运行启发。它不重定义同目录 `SKILL.md` 的入口、路由、输出合同或完成门禁。

## Type Map

| failure_or_outcome_type | root_cause_layer | immediate_fix | systemic_prevention | verification_point |
| --- | --- | --- | --- | --- |
| 没有源语言 SRT 却要求翻译字幕 | 技能路由层 | 先走转写生成 SRT，或把用户粘贴的 transcript 转成可计时文本 | 本技能只处理 SRT / transcript → 目标字幕，不做转写、烧录或配音 | 输入存在源文本和可用时间轴 |
| 目标语言或输出形态不清 | 请求解析层 | 从用户措辞解析 `zh-CN`、`en`、bilingual 等；仍不清时沿用项目历史偏好 | 文件名使用 BCP-47 风格后缀，避免多语言输出混淆 | 输出文件名能看出语言和形态 |
| cue 翻译后仍在句中断开 | 重分段合同层 | 合并 / 拆分 cue，使每条结束于目标语言真实标点 | 重分段是强制步骤，即使后续只烧字幕不配音也执行 | 没有 cue 结束在名词、动词、连词或未完成短语上 |
| 中文字幕出现大量「这 / 那 / 这个」等填充指代 | 中文风格层 | 删除无语义负载的 demonstratives，只保留指代、对比或固定表达所需词 | 中文译文先按自然口语审一遍，不照搬源语言显性指代 | 字幕读起来像自然普通话 |
| 英文字幕僵硬、学术化或翻译腔 | 英文风格层 | 改为自然会话表达，尤其是灵性 / 冥想内容用 plain words | 英文目标优先可听可读，不追求逐词结构对应 | 每条英文能被 3-4 wps 节奏读完 |
| SRT 时间戳格式、编号或重叠错误 | SRT 格式层 | 重新编号，统一 `HH:MM:SS,mmm`，消除 overlap | 输出前固定做格式验证，不允许 period milliseconds | 播放器可加载且顺序正确 |
| 行长超限导致屏幕不可读 | 可读性层 | 拆行或拆成多 cue，按字符位置插值时间戳；不要删语义来硬压缩 | zh-CN 约 15 字 / 行，en 40-42 chars / 行，最多 2 行 | 关键长句在画面停留时间内可读 |
| proper noun / `[unclear]` 被错误改写或补编 | 保真边界层 | 恢复名称、品牌、技术词和 bracketed marker；不在字幕里加解释 | 未听清内容只标记，不发明；说明放在回复而非 SRT | 字幕无编造内容 |
| 双语字幕行序或长度混乱 | 双语输出层 | 源语言第一行、目标语言第二行，必要时拆 cue | 双语可见字幕比单语更占空间，优先短句和自然断点 | 两行均可读且时间轴保持一致 |

## Repair Playbook

1. 先确定输入类型、源语言、目标语言、输出形态：target-only、bilingual、transcript 或 side-by-side table。
2. 解析并规范源 SRT：编号、时间戳逗号毫秒、无重叠、每条文本可追踪。
3. 翻译时先保语义、语气、名称、数字、日期和 bracketed marker；不在字幕正文加入解释。
4. 翻译后强制按目标语言标点重分段；必要时合并相邻 cue 或把长 cue 拆成 2-4 条，并按文本位置插值时间。
5. 套用目标语言可读性限制：中文约 15 字 / 行，英文约 40-42 chars / 行，通常最多 2 行。
6. 面向配音下游时，每条 cue 必须是完整 utterance，避免 TTS 在句中制造假停顿。
7. 输出前检查 SRT 编号连续、时间不重叠、毫秒逗号、无句中断、无编造内容。
8. 不确定项写在最终回复或 side note，不写进 `.srt` 正文。

## Reusable Heuristics

- Whisper 的 silence/breath 边界不等于字幕边界；翻译后的目标语言必须重新找语法停顿。
- 配音质量从字幕阶段就开始决定；句中断开的 SRT 会让 TTS 每条都读成断句。
- 中文字幕要敢删源语言带来的显性指代；英文字幕要敢改掉直译结构。
- 行长超限时优先拆 cue，而不是丢信息或堆第三行。
- 文件名后缀比回复说明更可靠；多语言产物必须让下游一眼识别语言。
- `[unclear]` / `[inaudible]` 是保真边界，不是让模型补剧情的入口。
- 双语可见字幕天然更拥挤，宁可多拆 cue，也不要让两行都过长。

## Promotion Backlog

- 增加 SRT validator：检查编号、时间戳格式、overlap、period milliseconds、空 cue 和行长。
- 增加 punctuation-bound resegmentation helper：支持 split / merge 和按字符位置插值时间戳。
- 增加中文 demonstrative lint：提示无语义负载的「这 / 那 / 这个 / 那个 / 那份」。
- 增加 bilingual output checker：校验源行在前、目标行在后、行数和长度限制。
- 增加 glossary / proper noun sidecar：为项目内反复出现的人名、品牌、地名和术语提供一致译法。
- 增加 downstream handoff manifest：标明目标语言、是否已重分段、是否适合 dub、是否适合 burn-in。

## Case Log

暂无案例。后续只追加可复用、可验证、可晋升的案例。
