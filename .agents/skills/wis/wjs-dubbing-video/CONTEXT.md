# Context: wjs-dubbing-video

## Context Health
<!-- CONTEXT_HEALTH_START -->
```yaml
monitor_version: 1
soft_limit_chars: 40000
hard_limit_chars: 80000
soft_limit_cases: 80
hard_limit_cases: 140
current_chars: 3193
current_lines: 51
current_cases: 0
status: ok
recommended_action: none
last_checked_at: 2026-06-21T06:49:48Z
```
<!-- CONTEXT_HEALTH_END -->

本文件是 `wjs-dubbing-video` 技能的经验层知识库，用于沉淀可复用的失败模式、修复策略和运行启发。它不重定义同目录 `SKILL.md` 的入口、路由、输出合同或完成门禁。

## Type Map

| failure_or_outcome_type | root_cause_layer | immediate_fix | systemic_prevention | verification_point |
| --- | --- | --- | --- | --- |
| 用户没有目标语言 SRT 却要求配音 | 技能路由层 | 先转到转写 / 字幕翻译链路，拿到目标语言 SRT 后再配音 | 配音入口固定为 video + target-language SRT，不把翻译和 burn-in 混进本技能 | 输入中存在视频和目标语言 `.srt` |
| 单人视频被错误做成多人配音 | 说话人策略层 | 回到单 voice 方案，移除不必要的 `[A]` / `[B]` 标签 | 默认单说话人；只有用户明确说多人、访谈、对话、不同声音时才启用 diarization | 输出只使用一个 voice，听感不混乱 |
| Volcano voice 报 `55000000` / `401` / `403` | TTS 资源与账号授权层 | 换回已验证 voice / resource，或让用户开通对应资源；必要时 fallback 到 edge-tts | 新账号或新 speaker 必须先做 5 词 smoke test，不承诺未验证 voice | smoke test 生成非空 MP3 |
| Volcano 响应解析失败或空音频 | API 协议层 | 按 streaming NDJSON 逐行解析，拼接 `data` base64 音频块 | 把 `code=20000000` 视为成功终止码，不按单 JSON 或 raw bytes 处理 | 输出 MP3 可播放且 duration 可被 `ffprobe` 读取 |
| edge-tts 中途 RST / rate-limit | 执行方式层 | 使用 venv 中长驻 Python 进程和重试逻辑，避免每 cue 调一次 `uvx` | `dub.py` 统一驱动 edge_tts.Communicate，不在 shell 循环里生成片段 | 全片 cue 生成不中断，失败 cue 可重试 |
| 目标语言 TTS 明显短于 cue，留下长沉默 | 时间对齐 / 文本长度层 | 先降低原生 rate，再用 0.82-0.95 atempo 慢拉；极端 cue 经用户确认后扩写字幕 | 把 slack 作为 per-cue QA 指标，避免靠过度 stretch 解决 | cue 末尾无 2s 以上突兀空白 |
| voice 音色不匹配原说话人 | 采样确认层 | 先合成 3-4 个短样本，让用户明确选择 voice/rate/pitch | 除非用户已指定且听过样本，否则全片前必须 sample checkpoint | 用户确认样本后再跑全片 |
| 用户要求字幕烧录或原声垫底混音 | 技能边界层 | 只输出 dub-only mp4，并把 burn-in / audio bed 交给 `wjs-burning-subtitles` | 本技能不做最终混音和字幕烧录，避免多轮级联转码 | 下游收到 `*_<lang>_dub.mp4` 和 SRT |
| 多人配音标签不可靠 | diarization 层 | 对 on-camera 视频优先跑 visual diarization，低置信 cue 手修；短片或 off-camera 可手动标注 | 保留 clean SRT 给烧录，tagged SRT 只给配音 | JSON 报告中低置信 cue 已复核 |

## Repair Playbook

1. 先确认任务是 video + target-language SRT → dub track；无 SRT 先走转写 / 翻译，burn-in 或 audio bed 交给下游。
2. 决定说话人数：默认单 voice；只有用户明确多人或要求不同声音时才进入 visual diarization / manual tagging。
3. 按 voice ID 路由引擎：`zh_*_bigtts` 走 Volcano，`*-Neural` 走 edge-tts；Volcano 先加载 credentials 并 smoke test。
4. 全片前必须 sample：选最长 cue 和短 cue，合成 3-4 个 voice/rate/pitch 组合，等待用户明确选择。
5. 跑 `dub.py` 后检查 `dub_work/seg_NN.mp3`、per-cue duration、atempo 修正、最终音轨长度和 `*_<lang>_dub.mp4`。
6. 遇到长沉默，先调原生 `--rate`，再允许轻度 slow-stretch；只有少量最差 cue 才修改译文长度，并先告知会改变字幕。
7. 多说话人时保留两份 SRT：tagged SRT 给配音，clean SRT 给后续烧录；低置信 diarization cue 必须人工抽查。
8. 结束时把 dub-only 输出和推荐下游命令交给 `wjs-burning-subtitles`，不要在本技能里补做最终混音。

## Reusable Heuristics

- 单说话人是默认正确答案；多人配音是用户明确触发的增强路径。
- 中文配音优先 Volcano bigtts；没有凭据、未开通资源或 voice 未验证时，再 fallback 到 edge-tts。
- Volcano 的 bigtts 可用性由用户实例决定，文档列出不等于当前账号可用。
- 配音质量的最大风险通常不是 mux，而是 voice 选择和 cue 时长贴合；样本确认比全片返工便宜。
- Mandarin 通常比 Spanish 更短，原生慢速 + 轻度 atempo 比硬塞长静音自然。
- `dub_work/seg_NN.mp3` 是恢复和局部重生的工作缓存；不要在确认全片前随手清掉。
- 配音输出是下游输入，不是最终混音母版；最终字幕烧录和原声垫底应在一个下游 ffmpeg pass 完成。

## Promotion Backlog

- 增加 voice preflight：统一检查 voice ID、引擎路由、Volcano env、resource、speaker smoke test 与 edge-tts 依赖。
- 增加 sample manifest：记录候选 voice/rate/pitch、样本 cue、音频路径和用户选择。
- 增加 per-cue slack report：标出过长、过短、atempo 低于阈值和需要译文扩写的 cue。
- 增加 visual diarization review helper：突出 `confidence_ratio < 1.5` 的 cue 供人工复核。
- 增加下游 handoff manifest：明确 source video、dub mp4、clean SRT、tagged SRT、目标语言和推荐 burn-in 参数。

## Case Log

暂无案例。后续只追加可复用、可验证、可晋升的案例。
