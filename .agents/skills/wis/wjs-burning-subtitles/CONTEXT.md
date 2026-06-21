# Context: wjs-burning-subtitles

## Context Health
<!-- CONTEXT_HEALTH_START -->
```yaml
monitor_version: 1
soft_limit_chars: 40000
hard_limit_chars: 80000
soft_limit_cases: 80
hard_limit_cases: 140
current_chars: 2521
current_lines: 41
current_cases: 0
status: ok
recommended_action: none
last_checked_at: 2026-06-21T06:49:48Z
```
<!-- CONTEXT_HEALTH_END -->

本文件是 `wjs-burning-subtitles` 技能的经验层知识库，用于沉淀可复用的失败模式、修复策略和运行启发。它不重定义同目录 `SKILL.md` 的入口、路由、输出合同或完成门禁。

## Type Map

| failure_or_outcome_type | root_cause_layer | immediate_fix | systemic_prevention | verification_point |
|---|---|---|---|---|
| 用户只说“加字幕”但未说明硬字幕或软字幕 | 路由/模式选择层 | 先按目标平台判断：微信、抖音、朋友圈等默认 burn-in；可切换播放器才 soft-mux | 进入渲染前确认输出模式和平台，不把 `mov_text` 当通用方案 | 输出文件类型与目标平台匹配：`*_burned.mp4` 或 `*_softsub.mp4` |
| burn-in 报 `No such filter: subtitles` 或字幕滤镜不可用 | ffmpeg/libass 环境层 | 验证 `ffmpeg -filters`，缺 libass 时使用 evermeet static build 或 `render.py` 自动 fallback | 硬字幕前置 libass gate，不先承诺全片渲染 | `$FF -filters` 能看到 `subtitles` 或 `ass` |
| 全片跑完后字号过大、溢出或边距裁切 | 字幕样式/校准层 | 先渲染 30 秒预览，抽最长行 cue 的帧，调小 `Fontsize`、设置 `MarginL/R/V`、手动换行 | burn-in 全片前必须做 frame check；同视频同字体配置已确认才可跳过 | 最长字幕帧完整可读，无左右裁切 |
| `force_style` 样式被拆成多个滤镜导致失败 | ffmpeg filter graph 层 | 转义 `force_style` 内所有逗号为 `\,` | 样式字符串生成或手写时统一走逗号转义检查 | 渲染命令能通过 filter parse 并产出预览 |
| 本地化最终合成被拆成多次 re-encode | 输出合同层 | 改为单次 `filter_complex` 同时 burn subs、mix dub、保留 original bed | final cut 默认走 `render.py --video --srt --dub` 或等价单 pass | 输出只有一次视频重编码，音轨为 dub + 可选低音量原声 bed |
| 软字幕在移动中文平台不可见 | 平台兼容层 | 改成 burn-in，除非目标播放器明确支持 embedded subtitle track | soft-mux 只用于 YouTube、VLC、QuickTime、IINA 等支持场景 | 目标设备/播放器可看到字幕，或已改为硬字幕 |
| 配音合成听起来悬浮或原声压过配音 | 音频混合层 | 将 original bed 调到 `0.15`-`0.25`，dub 保持 `1.0`，必要时 `--no-original-audio` | full localized cut 统一显式设置 `bed-volume` 或说明不保留原声 | 抽听开头、中段、高潮处，配音清晰且原声只作氛围 bed |

## Repair Playbook

1. 先读取同目录 `SKILL.md`，确认本轮属于 subtitles only、dub only、full localized cut，还是 soft-mux。
2. 根据目标平台裁决硬字幕/软字幕；平台不可靠时优先硬字幕，但要说明会重编码。
3. 只有 burn-in 路径需要 libass；硬字幕前先跑滤镜可用性检查，缺失时切到 static ffmpeg fallback。
4. burn-in 全片前先做短预览和最长字幕帧检查，确认字号、字体、边距、描边、背景对比。
5. full localized cut 必须一次 ffmpeg encode 完成字幕烧录和音频混合，避免级联转码。
6. 失败时按层排查：输入 SRT 格式 -> 输出模式 -> libass -> `force_style` 转义 -> 字幕行长/边距 -> 音频混合。
7. 验证闭环至少包括：预览帧可读、最终文件有字幕、音轨符合预期、输出命名与模式一致。

## Reusable Heuristics

- 一个输出视频只选一种字幕系统：libass burn-in、soft-mux 或 HyperFrames/HTML captions，不要叠加。
- 中文硬字幕先以 `Fontsize=12` 作为竖屏保守起点，再按抽帧校准；不要把 libass 字号理解成输出像素。
- SRT 上游要控制行长：中文每行约 15 字以内，长句显式换行，别依赖播放器自动换行。
- `BorderStyle=1` 是默认干净选择；只有背景很乱时才考虑 `BorderStyle=3` 盒底。
- 原声 bed 的目标是保留现场感，不是和配音争主语义；默认 `0.15`-`0.25` 比完全静音更自然。
- soft-mux 的优点是快、可逆、不重编码；但面对微信、抖音、朋友圈这类不可控播放器，硬字幕更可靠。

## Promotion Backlog

- 如果多次手工校准同类竖屏视频，沉淀分辨率、字号、边距的推荐矩阵，但不得替代逐片 frame check。
- 可考虑新增 SRT 行长/逗号毫秒格式 dry-run 检查，提前发现 burn-in 溢出和下游兼容问题。
- 若 full localized cut 音频混合参数反复调整，沉淀一组按内容类型区分的 `bed-volume` 建议，并回接脚本默认值评估。
