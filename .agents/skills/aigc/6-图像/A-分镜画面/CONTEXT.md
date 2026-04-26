# Context: aigc 6-图像 / A-分镜画面

本文件是 `A-分镜画面` 的经验层知识库，不是执行日志。调用同目录 `SKILL.md` 时必须同时加载本文件。

## Context Health

```yaml
monitor_version: 1
soft_limit_chars: 24000
hard_limit_chars: 48000
status: ok
last_checked_at: 2026-04-26
```

## Type Map

| failure_or_outcome_type | root_cause_layer | immediate_fix | systemic_prevention | verification_point |
| --- | --- | --- | --- | --- |
| 四段式 `分镜ID` 断链 | `4-分组` 提取层 | 回到分镜组标题与组内 `分镜N` 重新建索引 | 先产出 shot index，再写 prompt | `x-y-z-N` 可回指源组和源文本 |
| prompt 变成组级摘要 | 镜级边界层 | 只保留当前 `分镜N` 的画面与必要桥段上下文 | 模板中固定 `source_group_id` 与 `source_shot_no` | prompt 只描述单镜画面 |
| 英文 prompt 超过 2000 字符 | prompt 压缩层 | 删除重复背景、保留核心动作与主体 | 审查时统计 `integrated_prompt` 字符数 | 每条 <= 2000 chars |
| north_star 被改写为摘要 | 风格直引层 | 重新从 `north_star.yaml` 原字段复制 | step2 固定三行直引，不翻译、不润色 | 三项与源 YAML 完全一致 |
| 主体引用猜测绑定 | 参照证据层 | 删除猜测路径，只保留存在的图片文件 | 多视图优先、主图次之、无图留空 | manifest 路径全部存在 |
| imagegen 批量任务混成一个 prompt | batch 分发层 | 每个 `分镜ID` 独立任务、独立输出名 | 计划文件按 shot_id 列任务数组 | 一镜一 prompt、一镜一输出 |
| 未传入本地参照图被误判为不能生成 | imagegen source semantics | 按 built-in `text_prompt_only` 生成并持久化，同时记录 `reference_input_status` | 在 handoff 与 review gate 固化 text prompt only 口径 | results/report 不把 reference path 描述为视觉输入 |

## Repair Playbook

1. 先判断本轮是 `prompt_only`、`single_shot_generate`、`episode_batch_generate`、`shot_batch_generate`、`repair` 还是 `review_only`。
2. 任何 prompt 问题先检查 `shot index`，确认是否真的锁定到单个 `分镜N`。
3. 若主体槽位缺图，先判断是设计生成阶段未产出图片，还是已有 JSON 但图片文件不存在；不得把 JSON 文件当作图片参照。
4. 对角色、场景、道具名称只做精确名与规范别名匹配；泛词如“学生”“窗户”“文具”必须谨慎，无法对应主体时留空。
5. 批量生成前先审查 prompt 包与 reference manifest，避免错误在批量任务中被放大。
6. imagegen 输出必须持久化到项目目录；不能只留下 `$CODEX_HOME/generated_images` 路径。
7. built-in `image_gen` 的 text-prompt-only 可以生成并持久化；这和真实 reference-image workflow 是两种状态。源层应记录 `reference_input_status`，不要把未传入视觉参照误判成生成阻断。

## Reusable Heuristics

- `4-分组` 的 `## 1-1-1` 是组，不是镜；组内的 `分镜1` 才对应 `1-1-1-1`。
- `入场画面` 与 `出场画面` 是桥段上下文，可帮助理解连续性，但不能吞掉当前镜头的主体动作。
- 生图 prompt 允许做画面表现增量，例如构图、焦段、光比、材质、遮挡、空间压力；不允许改变谁在做什么、在哪里、关键道具是什么。
- 多视图图像比主图更适合作为 imagegen 的主体连续性参照；但只有真实图片文件存在时才算可绑定。
- 对没有图片的主体，保留文字 prompt 通常比绑定错误图片更安全。
- 整集批量时最容易出错的是复用上一镜参照槽位；每个分镜都应独立从角色、场景、道具列表重算槽位。
