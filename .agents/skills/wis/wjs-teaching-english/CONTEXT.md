# Context: wjs-teaching-english

## Context Health
<!-- CONTEXT_HEALTH_START -->
```yaml
monitor_version: 1
soft_limit_chars: 40000
hard_limit_chars: 80000
soft_limit_cases: 80
hard_limit_cases: 140
current_chars: 2667
current_lines: 44
current_cases: 0
status: ok
recommended_action: none
last_checked_at: 2026-06-21T06:49:48Z
```
<!-- CONTEXT_HEALTH_END -->

本文件是 `wjs-teaching-english` 技能的经验层知识库，用于沉淀可复用的失败模式、修复策略和运行启发。它不重定义同目录 `SKILL.md` 的入口、路由、输出合同或完成门禁。

## Type Map

| failure_or_outcome_type | root_cause_layer | immediate_fix | systemic_prevention | verification_point |
| --- | --- | --- | --- | --- |
| 用户给的是句子而不是目标词 | input contract 层 | 从句子里选出目标英文单词或短语；不确定时请用户确认 | 入口先归一化为一个 word/short phrase | build 命令里的 `--word` 是明确目标 |
| 用户期待 MP4 成品 | output contract 层 | 说明本技能交付 HLS `.m3u8` 与同名 `.intro.ts` / `.cta.ts`，不烧录 MP4 | 任务开始时把 deliverable 说清楚，避免按视频渲染技能处理 | 输出路径为 `search-app/out/<word>.m3u8` |
| 没有匹配片段 | search-app 结果层 | 告知 no clips match，并建议更常见或形态更基础的词 | 选词时优先常见词、原形词，短语要预期匹配率更低 | 脚本未写出文件，最终回复包含替代词建议 |
| HLS 播放 `bufferAppendError` 或断点异常 | codec alignment 层 | 重新按第一段 supercut 的分辨率、codec、fps 编码 intro/CTA | 不手工拼接 codec 不一致的 `.ts`；交给 `build_lesson.py` 处理 | intro、supercut、cta 在 HLS player 中连续播放 |
| 依赖缺失导致构建中断 | prerequisites 层 | 检查 `ffmpeg`、`ffprobe`、`volcengine` SDK 与 search-app 可达性 | 首次运行或换机器时先做依赖预检 | 依赖检查通过，或阻塞项被明确报告 |
| intro 卡片文字太长、低分辨率难读 | lesson JSON 层 | 缩短 `usage`，`tts_text` 只保留词和短中文 gloss | mini-lesson 由 LLM 直接写，保持准确和克制，不调用词典 API 灌长解释 | `usage` 约 20 字以内，卡片可读 |
| Volcano TTS 混合文本读得拖沓 | TTS text 层 | 简化为 `<word>. <中文 gloss>.` 或更短表达 | `tts_text` 不承载完整教学内容，教学主要来自真实片段 | intro 音频短且不压过 supercut |
| 本地播放方式错误 | playback/reporting 层 | 用 `ffplay` 播放，或 HTTP serve `out/` 后在 HLS player/Safari 打开 | 报告交付物时同时说明 `.m3u8` 需要 sibling `.ts` 文件 | 用户拿到完整 out 目录即可播放 |

## Repair Playbook

1. 先确定目标词：单个英文单词或短语；如果用户给句子，提取最适合作为课程主题的词。
2. 检查运行条件：`ffmpeg` / `ffprobe`、Python `volcengine` SDK、search-app 地址；缺失时先报告阻塞。
3. 由 LLM 写 mini-lesson JSON：`word`、`ipa`、`pos`、`gloss`、短 `usage`、短 `tts_text`，不要调用词典 API 生成长解释。
4. 到 `/Users/jianshuo/code/mira/search-app` 运行 `scripts/build_lesson.py`，按需使用 `--speaker`、`--limit`、`--no-tts`、`--base`、`--out`。
5. 脚本返回 no clips match 时，不伪造片段、不写空 playlist，建议换更常见的词或原形词。
6. 构建完成后报告 `.m3u8` 路径和 clip count，并提醒 `.intro.ts`、`.cta.ts` 是同目录必要交付物。
7. 本地验证优先用 `ffplay` 或 HTTP serve `out/`；不要把该流程升级成 MP4 burn。

## Reusable Heuristics

- 本技能的交付真源是 HLS playlist，不是 MP4；只有 intro/CTA 两张卡片会被渲染成小 `.ts`。
- mini-lesson 卡片负责“给入口”，真实电影片段负责“教用法”；不要把 intro 写成完整词典页。
- `usage` 越短越稳，低分辨率下最好是一行中文提示。
- `tts_text` 只读词和短中文 gloss，避免长解释拖慢进入 supercut。
- 常见动词、名词和高频形容词更容易搜到足够 clips；冷僻词、变形词和长短语更容易 no match。
- intro/CTA 必须与第一段 supercut 的编码参数对齐；这是 HLS 稳定播放的关键，不是画质优化项。
- 报告输出时同时给 clip count；片段数本身是课程质量和可用性的关键指标。

## Promotion Backlog

- 增加 preflight helper：检查 `ffmpeg`、`ffprobe`、`volcengine`、search-app 可达性和 Python 环境。
- 增加 lesson JSON validator：字段齐全、`usage` 长度、`tts_text` 长度、word/slug 安全。
- 增加 no-match fallback 提示库：建议原形词、更常见同义词或去掉短语修饰词。
- 增加交付清单：`.m3u8`、`.intro.ts`、`.cta.ts`、clip count、播放方式说明。
