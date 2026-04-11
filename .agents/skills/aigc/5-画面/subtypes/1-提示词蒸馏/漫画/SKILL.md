---
name: aigc-storyboard-comic
description: Use when the `5-画面` stage needs to turn a storyboard group from `projects/<项目名>/编导/第N集.json` into group-level image request JSON for a comic page, especially before downstream consistency or image-generation subtypes run.
governance_tier: full
---

# 5-画面 / 漫画

## 概述

`漫画` 负责把一个已经进入共享编导根文件的分镜组，整理成 **漫画单页的图像生成请求 JSON**。

交付类型：`内容输出型`

当前子技能名描述的是“漫画单页目标”，输出结构则与 `分镜故事板` 同步收口到 `5-画面/_shared` 的共享模板方式。

当前设计重点不是直接生成漫画页图片，而是先把每个分镜组整理成：

1. 共享模板兼容的 `meta`
2. 面向漫画单页的 `prompt_style`
3. 图像生成侧 `model` 参数骨架与参照图预留位
4. 由固定漫画前缀与 `comic_page_group` 内容块拼成的 `prompt`
5. 对应的 `prompt_char_count`

其中：

- 上游默认路径固定为 `projects/<项目名>/编导/第N集.json`
- shared schema 固定为 `.agents/skills/aigc/_shared/director_episode_output.schema.json`
- shared JSON 模板固定为 `.agents/skills/aigc/5-画面/_shared/image-generation-input.template.json`
- 当前只输出 `json`，不输出 `.txt`
- `comic_page_group` 内容可以直接使用上游信息，不做文字压缩

## When to Use

- 需要把一个分镜组整理成漫画页的图像生成请求 JSON。
- 用户明确要气泡文字、旁白框、漫画阅读节奏或 9:16 漫画页。
- 需要先完成 `1-提示词蒸馏`，后续再进入 `2-一致性处理` 或 `3-图像生成`。

## When Not to Use

- 只需要普通 storyboard sheet，应进入 `分镜故事板`。
- 只需要单一镜头的首帧或单帧图，应进入 `分镜帧`。
- 上游脚本没有稳定的组边界与分镜顺序。

## 子技能边界

### `漫画` 拥有

- 分镜组 -> 漫画图像请求条目的一对一转换合同
- 固定漫画前缀 + `comic_page_group` 的 prompt 组织规则
- `1 shot = 1 panel` 与文字系统约束在 prompt 中的显式表达
- 对 `5-画面/_shared` 图像入参模板的局部填充规则

### `漫画` 不拥有

- 整组 storyboard sheet 合同
- 单帧关键帧合同
- 一致性二次处理与真实图片生成
- 上游文本与镜头事实改写

## Visual Maps

```mermaid
flowchart TD
    A["读取 编导/第N集.json"] --> B["遍历 分镜组列表"]
    B --> C["抽取 comic_page_group 内容块"]
    C --> D["拼接固定漫画前缀"]
    D --> E["按组填充 image request JSON"]
    E --> F["写回 第N集.json"]
```

## Canonical Module References

| 模块 | 作用 | 真源文件 |
| --- | --- | --- |
| 思维链 | 承载字段主表、thought pass 与返工入口 | `references/chain-of-thought.md` |
| 执行流程 | 承载落点、输入合同、workflow 与 handoff | `references/execution-flow.md` |
| 类型策略 | 承载 VSM 变量、情况、策略映射与回退 | `references/type-strategies.md` |
| 输出契约 | 承载 JSON 骨架、最低要求与文件清单 | `references/output-template.md` |

## Execution Summary

- 每个 `分镜组` 只生成 1 条漫画图像请求对象。
- `prompt` 固定由漫画专属英文前缀与 `comic_page_group` 内容块组成。
- `comic_page_group` 必须覆盖该组的 `剧本正文`、`组间设计` 与全部 `分镜明细[]`，并显式强调 `1 shot = 1 panel` 与文字系统归属。
- 当前只输出 `第N集.json`；后续一致性处理与真实生成由其他子技能继续消费。
- `prompt_style` 独立承载类型、语言和可选字数限制。
- `prompt_char_count` 位于顶层，用于统计和验收。
- `model.reference_images` 保留上传顺序位。
- `model.image_markers` 承担图片 URL、关联主体和 `图1/图2/...` 顺序标记。
- 详细 canonical landing、输入合同、workflow 与 handoff 见 `references/execution-flow.md`。

## Output Summary

- canonical 主产物：`projects/<项目名>/5-画面/漫画/第N集/第N集.json`
- 可选追溯文件：`projects/<项目名>/5-画面/漫画/第N集/_manifest.json`
- 共享模板真源：`.agents/skills/aigc/5-画面/_shared/image-generation-input.template.json`
- 当前无 `.txt` 派生视图
- 详细 JSON 结构、prompt 规则与最小追溯要求见 `references/output-template.md`

## Strategy Summary

- 判定顺序仍为：`组边界是否稳定 -> comic_page_group 内容块是否完整 -> 是否只需 JSON -> 共享模板字段是否齐全`
- 变量登记、情况判定、策略映射与回退规则见 `references/type-strategies.md`

## Field System Summary

- 字段体系仍保持 `FIELD-SB-COMIC-01` 到 `FIELD-SB-COMIC-04`
- thought pass 与 pass table 见 `references/chain-of-thought.md`

## Root-Cause Execution Contract (Mandatory)

当出现以下症状时，必须先修本子技能合同：

- 仍把图片落盘当主产物，而不是组级漫画图像请求 JSON
- prompt 没有以固定漫画前缀开头
- `comic_page_group` 没覆盖完整组级与镜级信息
- `1 shot = 1 panel` 或文字归属约束没有进入 prompt
- 共享模板字段被删改，尤其是 `reference_images` 或 `image_markers`

必经链路：

`Symptom -> Direct Technical Cause -> Rule Source -> Meta Rule Source -> Fix Landing Points`

优先检查：

- `Rule Source`
  - `.agents/skills/aigc/5-画面/subtypes/1-提示词蒸馏/漫画/SKILL.md`
  - `.agents/skills/aigc/5-画面/subtypes/1-提示词蒸馏/漫画/CONTEXT.md`
- `Meta Rule Source`
  - `.agents/skills/aigc/5-画面/SKILL.md`
  - `.agents/skills/aigc/SKILL.md`
  - 根 `AGENTS.md`

## Context Preload (Mandatory)

- 执行前先加载 `.agents/skills/aigc/5-画面/SKILL.md + CONTEXT.md`。
- 再加载本 `SKILL.md + CONTEXT.md`。
- 建议同时读取 `references/*.md` 与 `.agents/skills/aigc/5-画面/_shared/image-generation-input.template.json`。
- 优先级遵循：用户显式请求 > 根 `AGENTS.md` > `.agents/skills/aigc/SKILL.md` > `.agents/skills/aigc/5-画面/SKILL.md` > 本 `SKILL.md` > 各级 `CONTEXT.md`。
