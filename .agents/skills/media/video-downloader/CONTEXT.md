# CONTEXT.md

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
| 成功形成可复用下载请求模板 | CONTEXT 经验层 | 提炼为下载参数收集 heuristic | 在跨平台复用验证后晋升到 `SKILL.md` | YouTube/playlist/audio-only 场景都能覆盖 |

## Repair Playbook

1. 识别症状：确认问题是链接无效、格式不符、质量不对还是权限边界不清。
2. 层层上溯：`Symptom -> Direct Cause -> 规则源 -> 规则源的规则源`。
3. 先修源层：优先修正输入收集、格式选择和合规提醒规则。
4. 再修局部：修正具体下载参数、命名策略或输出目录。
5. 沉淀经验：把高频下载参数模板写回知识库。
6. 验证闭环：确认输出文件实际可播放、命名合理、位置明确。

## Reusable Heuristics

- 视频下载类任务先收齐“链接、格式、质量、保存位置”四个输入，再执行最稳。
- 只要版权或权限边界含糊，就先停下来澄清，不要把下载动作默认视为可执行。
- 音频提取、单视频下载、播放列表下载其实是三种不同任务，最好在技能调用时明确分流。
