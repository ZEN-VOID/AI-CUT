# Context: wjs-localizing-video

## Context Health
<!-- CONTEXT_HEALTH_START -->
```yaml
monitor_version: 1
soft_limit_chars: 40000
hard_limit_chars: 80000
soft_limit_cases: 80
hard_limit_cases: 140
current_chars: 1700
current_lines: 41
current_cases: 0
status: ok
recommended_action: none
last_checked_at: 2026-06-21T06:49:48Z
```
<!-- CONTEXT_HEALTH_END -->

本文件是 `wjs-localizing-video` 技能的经验层知识库，用于沉淀可复用的失败模式、修复策略和运行启发。它不重定义同目录 `SKILL.md` 的入口、路由、输出合同或完成门禁。

## Type Map

- 单步任务误走 orchestrator：用户只要转写、翻译、配音或烧字幕，却加载完整流水线。修复时直接路由到对应子技能，只有“一次做完整本地化”才进入本技能。
- 长流水线无进度反馈：多分钟任务如果没有 checklist，用户只看到沉默。修复时在第一个子技能前创建实际会运行的步骤清单，并保持同一时间只有一个 `in_progress`。
- 可选步骤被误创建：字幕-only、dub-only、已有 source SRT 或 target SRT 时仍保留无关任务，会让未勾选项像遗漏。修复时按输入和目标裁剪任务，不跑的步骤不出现在清单里。
- orchestrator 重实现子技能：在本层写 ASR、翻译、配音或烧录逻辑会制造第二执行入口。修复时回到四个 canonical 子技能；若看到本目录 stale scripts，只作为历史残留处理。
- 字幕系统混用：同一输出同时尝试 `/wjs-burning-subtitles` 和 `/wjs-overlaying-video`，容易产生重复字幕或风格冲突。修复时每个输出只选一个 caption system。
- 命名漂移：多语言产物没有 BCP-47 风格后缀时，后续烧录、配音和上传容易串文件。修复时按 `basename.lang.srt`、`basename_<lang>_dub.mp4`、`basename_<lang>_final.mp4` 收束。

## Repair Playbook

1. 先读取同目录 `SKILL.md`，判断用户要 full localization 还是单步操作；单步立即转交子技能，不在 orchestrator 里扩展。
2. 盘点已有输入：原视频、source SRT、target SRT、是否要配音、是否要烧字幕/soft-mux。
3. 创建只包含实际步骤的 checklist：转写、翻译、配音、烧字幕/混音；每步开始和完成都即时更新状态。
4. 按顺序委派子技能，并以子技能输出文件作为下一步输入；失败或需要澄清时保留当前步骤 `in_progress`。
5. 使用规范命名保存中间产物和最终产物，避免同一 basename 的多语言输出互相覆盖。
6. 完成时按模板列出实际执行步骤、输出文件和不确定片段；没有不确定片段就省略该段。

## Reusable Heuristics

- 本技能是薄编排层，不是媒体处理实现层；所有核心处理都应委派给四个子技能。
- Step 3 配音和 Step 4 烧字幕/混音是可选且相互独立的；用户目标决定是否运行，不按“完整四步”强推。
- 原声底层音量属于最终混音策略，默认 0.15-0.25；具体实现由 `/wjs-burning-subtitles` 承接。
- 微信视频号、抖音默认 burn-in；其他平台默认 soft-mux 更稳。
- 进度清单和最终摘要应使用同一套标签，用户看到的是一条连续流水线，而不是两套描述。

## Promotion Backlog

- 增加口语请求到步骤子集的 routing table，覆盖“只要字幕”“只配音”“已有 SRT”“双语字幕”等高频说法。
- 增加产物命名 smoke check，验证目标 SRT、dub MP4、final MP4 后缀和引用关系一致。
- 增加 stale script 扫描规则：发现本目录媒体处理脚本时提示 canonical 子技能位置，不从本层调用。
- 为 checklist 状态添加失败/重定向示例，避免中途变更需求时留下误导性的未完成项。

## Case Log

暂无案例。后续只追加可复用、可验证、可晋升的案例。
