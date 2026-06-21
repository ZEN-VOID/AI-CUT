# Context: wjs-transcribing-audio

## Context Health
<!-- CONTEXT_HEALTH_START -->
```yaml
monitor_version: 1
soft_limit_chars: 40000
hard_limit_chars: 80000
soft_limit_cases: 80
hard_limit_cases: 140
current_chars: 3273
current_lines: 49
current_cases: 0
status: ok
recommended_action: none
last_checked_at: 2026-06-21T06:49:48Z
```
<!-- CONTEXT_HEALTH_END -->

本文件是 `wjs-transcribing-audio` 技能的经验层知识库，用于沉淀可复用的失败模式、修复策略和运行启发。它不重定义同目录 `SKILL.md` 的入口、路由、输出合同或完成门禁。

## Type Map

| failure_or_outcome_type | root_cause_layer | immediate_fix | systemic_prevention | verification_point |
|---|---|---|---|---|
| 中文音频误走 Whisper | 路由层 | 改走 Volcano streaming ASR，除非用户指定或 Volcano 不可用 | zh-CN/zh-HK/zh-TW 默认绑定 Volcano，Whisper 只作 fallback | ASR 输出来自 `volc_asr_stream.py`，含词级 ms 时间戳 |
| 使用飞书妙记做 SRT | 工具适配层 | 停止该路径，改用 Volcano 或 Whisper word-level | 飞书妙记只有 speaker-turn 时间戳，不作为字幕 ASR fallback | 生成 cue 的时间来自词级或可拆分 segment，而非 turn-level |
| Volcano 走需要公网 URL 的接口失败 | API 选择层 | 使用 WebSocket streaming 推 PCM 字节 | 文件识别、MediaKit、公网 URL 模式列为死路，不重复尝试 | 本地文件经 ffmpeg/PCM 直接推流成功 |
| Volcano 返回只保留最新句 | API 配置层 | 移除 `result_type:"single"`，用默认累积 utterances | 配置模板固定 `show_utterances:true` 且不设置 single | ASR JSON 中 `result.utterances[]` 覆盖全片 |
| OpenAI Whisper 直接 `response_format=srt` 出 30 秒 blob cue | 分段策略层 | 用 `verbose_json` + `timestamp_granularities[]=word` 重做 | 长内容禁止请求 Whisper SRT，统一自组 cue | cue 时长通常 3-8 秒，无 30 秒整块字幕 |
| 安静尾段出现循环幻觉 | 解码 / 质量层 | 使用 `temperature=0.2`，并在组装后跑重复短语检测 | Whisper 路径保留 loop guard，重复 3 次以上的短语不放行 | SRT 中无连续重复 phrase 残留 |
| 非中文语言被自动识别错 | 输入参数层 | 显式指定 `language=...` 后重新转写 | 禁止自动语言检测；路由时先确认源语言 | transcript 语言与源音频一致 |
| 分块合并后后半段时间戳整体偏移 | stitching 层 | 给每个 chunk 的 word/segment 加绝对 start offset | 合并前统一 offset stitching，不直接拼相对时间 | 后续 chunk cue 时间不从 00:00 重新开始 |
| Whisper 分块过大或代理断连 | 网络韧性层 | 改 10 分钟、64kbps mono MP3，重试并限制并发 | 默认 chunk 约 4.5MB，max_workers 优先 2 | API 调用在重试后完成，无超 25MB 请求 |
| `httpx` 走 SOCKS proxy 缺 `socksio` | 环境依赖层 | 用 `uvx --with httpx --with socksio python ...` | 代理环境下把 socksio 作为 Whisper API 路径前置依赖 | 不再报 `Using SOCKS proxy` ImportError |
| Volcano streaming ASR 缺 `websocket` 模块 | 环境依赖层 | 安装 `websocket-client` 或用 `uvx --with websocket-client python ...` | 在技能依赖文件和脚本错误提示中声明该包 | `python3 -c "import websocket"` 成功 |
| ASR 凭证缺失后字幕与音频不贴 | fallback 策略层 | 用音频 `silencedetect` 停顿边界重建 cue 时间，不用整段字数比例硬铺 | ASR 不可用时的最低可接受 fallback 是“文案分块 + 语音停顿边界”，比例分配只能作为临时草稿 | 最大 cue 时长、停顿间隔和抽帧检查通过，用户听感不再明显滞后/抢跑 |
| AI 润色改变时间戳或 cue 边界 | 后处理门禁层 | 回退重做，只改字幕文本行 | 润色 pass 明确禁止改编号、时间戳和 cue 数 | 润色前后 cue 数、编号、时间戳完全一致 |
| 专有名词被同音字误改 | 内容保真层 | 保留原文并列入不确定清单让用户确认 | 人名、品牌、产品名不凭上下文猜改 | 最终报告包含不确定专名列表 |

## Repair Playbook

1. 先确认目标只到源语言 SRT；如果用户要翻译、配音或烧字幕，先产出源语言 SRT 再交给下游技能。
2. 路由先看源语言：中文默认 Volcano streaming；非中文默认 OpenAI Whisper word-level；离线才用 local Whisper。
3. 中国语音排障先查 Volcano 凭据和 WebSocket streaming 配置，不回退到飞书妙记或公网 URL 文件接口。
4. Whisper 排障先查语言是否 pin、是否 word-level、chunk 是否过大、offset 是否叠加、loop guard 是否运行。
5. 组装 SRT 后检查编号、重叠、逗号毫秒、cue 时长、字符上限、重复短语和 mid-word break。
6. 中文必须做一次 AI 错别字润色，但只能改明确错字；专有名词和不确定项交给用户确认。
7. 下游交接前报告输出路径、引擎、关键参数、疑似专名和质量门禁结果。

## Reusable Heuristics

- 源语言 SRT 是后续翻译、切片、配音、烧字幕的主真源；不要在本技能里混入翻译或剪辑决策。
- 字幕质量的关键不是“全文识别出来”，而是 cue 可读、时间贴音频、边界自然；因此词级时间戳优先于模型自带 SRT。
- Volcano 的工作路径是“本地推 PCM 到 WebSocket”，不是让服务器下载文件；这条边界能避开公网 URL 和热点隧道问题。
- Whisper 的 `segments[]` 可参考呼吸边界，`words[]` 用于精确切分；两者都不能单独当最终字幕边界真源。
- 中文润色是纠错，不是改写；一旦改动了 cue 边界或时间戳，就破坏了 SRT 主真源。
- 专有名词宁可保留存疑，也不要猜成顺眼的错字；下游成文前再让用户确认。
- 10 分钟、64kbps、mono、并发 2 是非中文 Whisper API 的可靠性默认值；需要更快时先确认网络稳定性。
- 当 ASR 凭证缺失但用户已有确定文案和对应配音时，字幕 fallback 应先提取音频停顿边界，再把文案按语义短句映射到语音段；不要把全片时长按字数比例直接铺开到所有 cue。

## Promotion Backlog

- 为 SRT 输出补独立 validator：编号连续、时间不重叠、逗号毫秒、cue 长度、重复 phrase。
- 为 Volcano ASR JSON 补最小结构检查：`utterances[]`、`words[]`、ms 时间戳和 Latin token 0 时间回填。
- 为中文润色 pass 补 diff 报告模板，固定展示 `原词 -> 修正词 @ 时间` 和不确定专名列表。
- 为 Whisper chunk stitching 补回归样例，覆盖第二个 chunk 时间不归零、长 segment 拆分和 quiet tail loop guard。
