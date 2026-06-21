# CONTEXT.md

## Context Health
<!-- CONTEXT_HEALTH_START -->
```yaml
monitor_version: 1
soft_limit_chars: 40000
hard_limit_chars: 80000
soft_limit_cases: 80
hard_limit_cases: 140
current_chars: 2821
current_lines: 60
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
| 下载参数不清导致格式不符预期 | SKILL 合同层 | 明确 URL、输出格式、分辨率和保存位置 | 在执行前强制确认输入合同四元组 | 检查导出文件格式、清晰度和落盘路径 |
| 平台限制或版权边界不清 | 规则应用层 | 停止执行并明确权限前提与使用边界 | 在技能使用入口加入合规性提醒与拒绝分支 | 确认请求用途与权限声明 |
| YouTube 链接携带播放列表参数但用户只要单视频 | 执行参数层 | 使用 `--no-playlist` 并保留原始 watch URL | 将 `list=` / `start_radio=` 视为单视频下载的批量误触发风险 | yt-dlp 输出应显示 `Downloading just the video ... because of --no-playlist` |
| YouTube SABR / JS runtime 限制导致高分辨率格式不可见 | 平台兼容层 | 接受当前可用格式并用 `ffprobe` 验证实际分辨率 | 下载后必须报告实际 width/height，不把目标质量误报为成功质量 | 检查 yt-dlp format id 与 `ffprobe` 的 codec、duration、size、width、height |
| YouTube 下载中途 `HTTP 403` | 工具版本 / 平台兼容层 | 先升级 `yt-dlp` 后重试；必要时清理本轮 `.part` 临时文件 | 每次 YouTube 下载前检查 `yt-dlp --version`，遇到 403 优先排查版本滞后与 JS runtime 提示 | 重试后下载完整文件，并用 `ffprobe` 验证媒体参数 |
| 用户要音频但未说明格式 | 输入合同层 | 先确认 MP3、M4A、WAV 或保留原始音轨 | 把 audio-only 视为独立任务分支，不套用视频默认 MP4 输出 | 输出文件扩展名、codec、duration 与用户用途一致 |
| 批量或播放列表范围不清 | 任务路由层 | 明确是单条、多个 URL 还是整条 playlist | 执行前列出下载范围，避免把 playlist 参数误当批量授权 | 下载数量与用户确认的 URL/playlist 项数一致 |
| 下载后缺少标题、描述或缩略图 | 输出完整性层 | 补拉 metadata / thumbnail，或报告平台无法提供 | 对归档和研究用途默认保留最小 metadata sidecar | 目标目录存在媒体文件、缩略图和可读标题信息 |
| 成功形成可复用下载请求模板 | CONTEXT 经验层 | 提炼为下载参数收集 heuristic | 在跨平台复用验证后晋升到 `SKILL.md` | YouTube/playlist/audio-only 场景都能覆盖 |

## Repair Playbook

1. 识别症状：确认问题是链接无效、格式不符、质量不对还是权限边界不清。
2. 层层上溯：`Symptom -> Direct Cause -> 规则源 -> 规则源的规则源`。
3. 做权限判断：确认下载用途、版权边界和平台条款风险；边界不清时先澄清。
4. 先修源层：优先修正输入收集、格式选择、批量范围和合规提醒规则。
5. 再修局部：修正具体下载参数、命名策略、输出目录或临时文件处理。
6. 沉淀经验：把高频下载参数模板写回知识库。
7. 验证闭环：确认输出文件实际可播放、命名合理、位置明确，必要时用 `ffprobe` 核验。

## Reusable Heuristics

- 视频下载类任务先收齐“链接、格式、质量、保存位置”四个输入，再执行最稳。
- 只要版权或权限边界含糊，就先停下来澄清，不要把下载动作默认视为可执行。
- 音频提取、单视频下载、播放列表下载其实是三种不同任务，最好在技能调用时明确分流。
- YouTube URL 同时包含 `watch?v=` 与 `list=` 时，不应默认批量下载；用户确认单视频后必须加 `--no-playlist`。
- 下载完成后用 `ffprobe` 验证实际媒体参数；当平台只给低清格式时，最终报告以实际分辨率为准。
- YouTube 下载出现 `HTTP 403` 且本地 `yt-dlp` 版本落后时，先升级 `yt-dlp` 再重试；旧 `.part` 文件只保留本轮可恢复下载时使用，否则清理后重新拉取。
- 批量任务先生成待下载清单，再开始拉取；清单是防止误下整条 playlist 或漏掉 URL 的最小护栏。
- 归档、研究、后续剪辑类用途优先保存缩略图和标题信息；单纯离线观看则以媒体文件可播放为完成重点。
- 用户指定质量是目标值，不是成功声明；平台实际可用格式低于目标时，应报告实际下载质量和原因。

## Promotion Backlog

- 将“链接、格式、质量、保存位置、范围、metadata 是否保留”整理成执行前检查模板，重复稳定后晋升到 `SKILL.md`。
- 为 YouTube 单视频但 URL 含 `list=` 的场景补一个最小 smoke 检查，防止误下载播放列表。
- 若后续脚本化下载流程固定下来，补充 `ffprobe` 媒体参数校验输出作为完成门禁。
