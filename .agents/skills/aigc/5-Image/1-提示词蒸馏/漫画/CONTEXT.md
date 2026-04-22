# CONTEXT.md

## Purpose & Loading Contract

- 本文件是 `5-Image/1-提示词蒸馏/漫画` 的经验层知识库，不是过程日志。
- 调用本叶子技能时，应在根 `.agents/skills/aigc/SKILL.md`、阶段父级 `.agents/skills/aigc/5-Image/SKILL.md` 与父级 `.agents/skills/aigc/5-Image/1-提示词蒸馏/SKILL.md` 之后加载本文件。
- 当前漫画页叶子以“单页请求 JSON” 为第一目标，不直接承担真实图片生成。

## Context Health

<!-- CONTEXT_HEALTH_START -->
```yaml
monitor_version: 1
soft_limit_chars: 20000
hard_limit_chars: 40000
status: ok
last_checked_at: 2026-04-22T00:00:00-07:00
```
<!-- CONTEXT_HEALTH_END -->

## Type Map

| failure_or_outcome_type | root_cause_layer | immediate_fix | systemic_prevention | verification_point |
| --- | --- | --- | --- | --- |
| 漫画页诉求被误路由到 `分镜故事板` | object route | 回父级 `1-提示词蒸馏` 重新锁对象 | 父级保持 `显式 shot_id > 明确漫画页诉求 > 默认组级 storyboard` | 当前对象唯一命中 `漫画` |
| prompt 只有气氛，没有页内阅读节奏 | page synthesis | 回 `N3` 补页面设计块与面板顺序列 | 在 `SKILL.md` 固化“页面设计块 + 面板顺序列” | prompt 能读出单页漫画节奏 |
| 把漫画页 JSON 当成直接出图产物 | output contract | 回到 `第N集.json` 作为主产物 | 固定“json 为主，生成后置” | 主产物指向 `第N集.json` |
| 共享模板骨架被删改 | template contract | 恢复 shared image template 骨架 | 在 `N5` 固化 `reference_images / image_markers` 保留 | 下游 `2-参照引用 / 3-图像生成` 可继续消费 |
| 上游 `3-Detail` 未就绪却直接蒸馏 | readiness gate | 回 `N1` 先查 `document_phase` | 固化 `detail_in_progress | ready` 为进入条件 | 不再从未完成 detail 结果取页 |

## Repair Playbook

1. 先查当前对象是不是明确的漫画页诉求。
2. 再查 `3-Detail/第N集.json` 的 `document_phase` 与目标分镜组是否可消费。
3. 再查页面设计块是否同时覆盖组级设计、镜头顺序和文字承载预留。
4. 再查 prompt 是否严格满足“固定前缀 + 页面设计块 + 面板顺序列”。
5. 最后查 `第N集.json` 是否仍是唯一主产物，并可继续 handoff。

## Reusable Heuristics

- 漫画页叶子最容易漂移的不是画风，而是把“单页阅读体验”退化成“普通故事板图”。
- 对漫画页来说，镜头顺序必须仍然来自上游分镜组，但表达要转成页面阅读节奏，而不是简单逐镜罗列。
- 只要下游还要做引用绑定或 provider 提交，`第N集.json` 就必须保持为唯一 canonical carrier。
- 父级已把 `漫画` 列为 active leaf；因此本叶子的第一责任是稳住对象边界，而不是抢父级路由权。
