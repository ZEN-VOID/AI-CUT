---
name: aigc-video-first-frame-reference
description: Use when the `6-Video` stage enters the `首帧参照` subtype to build frame-level video request JSON from `projects/<项目名>/3-Detail/第N集.json`, especially when a single `分镜ID` should become the first-frame anchor while still inheriting its storyboard-group context.
governance_tier: full
---

# 6-Video / 首帧参照

## 概述

`首帧参照` 是 `6-Video` 阶段位于 `1-提示词蒸馏` tranche 的帧级叶子技能，当前 canonical 路径固定为：

`/Volumes/AIGC/AIGC-DREAMER/.agents/skills/aigc/6-Video/1-提示词蒸馏/首帧参照/`

本技能负责把 `projects/<项目名>/3-Detail/第N集.json` 中 **分镜组维度下的上下文** 收束到 **单一 `分镜ID`**，并输出可供视频工具消费的 **帧级请求 JSON**、人工审阅 `TXT` 与 `_manifest.json`。

本次升格后，`SKILL.md` 是本技能唯一规范真源。稳定规则、字段表、执行流程、类型策略与输出契约全部内聚于此；`CONTEXT.md` 只承载经验层，`references/` 不再作为 live contract 载体。

## When to Use

- 需要把导演 JSON 中单一 `分镜ID` 蒸馏成帧级视频请求对象。
- 需要输出 `第N集.json + 第N集.txt + _manifest.json` 三件套。
- 需要保留 `组间设计.全局风格` 原文不变，并把 `剧本正文` 裁为目标分镜帧对应的剧情桥段。
- 需要生成 `meta + prompt_style + model + prompt + prompt_char_count` 结构化请求对象。
- 需要在 prompt 中隐藏字段标题，只保留 `分镜组 <ID>` 与 `分镜 <ID>` 的显式标签。

## When Not to Use

- 需要按整个分镜组全覆盖蒸馏视频请求，应进入 `6-Video/1-提示词蒸馏/全能参照`。
- 需要真正提交 `dreamina multimodal2video`、轮询任务结果或下载视频，应进入 `6-Video/2-视频生成` 或对应 provider 技能。
- 上游 `3-Detail/第N集.json` 尚未形成合法 `分镜组列表`，或目标 `分镜ID` 不存在。
- 任务一次要把多个 `分镜ID` 合并成一条请求；本技能只处理“一镜一条”。

## 真源边界

### `首帧参照` 拥有

- 单一 `分镜ID -> 1 条视频请求对象` 的转换合同
- `剧本正文 -> 对应分镜帧剧情桥段` 的提取与保守退化规则
- 帧级 prompt 的字数窗、压缩策略与标题隐藏规则
- 对 `6-Video/_shared` 共享 JSON/TXT 模板的局部填充规则
- `第N集.json / 第N集.txt / _manifest.json` 三件套的最低落盘合同

### `首帧参照` 不拥有

- 实际上传参照图
- 真实视频模型提交、轮询与下载
- 改写上游导演事实
- 把多个分镜拼成一条请求或伪造缺失输入

## Trigger And Topology Contract

- 本技能是单叶子本地收束合同，不额外调度长期 subagents。
- 每个命中的目标 `分镜ID` 只生成 1 条请求对象；若用户给出多个 `分镜ID`，必须逐个独立处理。
- 执行顺序固定为：锁定目标分镜 -> 提取剧情桥段 -> 保留固定块 -> 压缩非固定块 -> 组装请求 -> 写出三件套。
- 任何输入完整性门禁失败时，必须立即停止，不允许降级生成“尽量像”的结果。

## Canonical Inputs And Shared Sources

### Canonical Inputs

- `projects/<项目名>/3-Detail/第N集.json`
- `.agents/skills/aigc/_shared/director_episode_output.schema.json`

### Shared Sources

- `.agents/skills/aigc/6-Video/_shared/video-generation-input.template.json`
- `.agents/skills/aigc/6-Video/_shared/视频生成入参.template.txt`

### Input Integrity Gates

以下任一缺失都必须停机并报告上游缺口：

- `final_output.main_content.分镜组列表`
- 目标 `分镜ID`
- 目标分镜所属 `分镜组ID`
- 目标分镜所属组的 `剧本正文`
- `组间设计.全局风格`
- 目标分镜明细

## Context Preload (Mandatory)

- 执行前先加载 `.agents/skills/aigc/SKILL.md + CONTEXT.md`。
- 再加载 `.agents/skills/aigc/6-Video/SKILL.md + CONTEXT.md`。
- 最后加载本 `SKILL.md + CONTEXT.md`。
- 按需读取 `.agents/skills/aigc/6-Video/_shared/video-generation-input.template.json` 与 `.agents/skills/aigc/6-Video/_shared/视频生成入参.template.txt`。
- 本技能不再把 `references/*.md` 作为规范真源或必读入口。
- 优先级遵循：用户显式请求 > 根 `AGENTS.md` > `.agents/skills/aigc/SKILL.md` > `.agents/skills/aigc/6-Video/SKILL.md` > 本 `SKILL.md` > 各级 `CONTEXT.md`。

## Workflow Contract

1. 读取 episode JSON，锁定 `final_output.main_content.分镜组列表`。
2. 遍历分镜组，并按 `分镜明细[].分镜ID` 锁定目标分镜及其所属 `分镜组ID`。
3. 提取目标分镜所属组的：
   - `分镜组ID`
   - `剧本正文`
   - `组间设计.全局风格`
   - `组间设计.类型元素`
   - `组间设计.导演意图`
   - 目标 `分镜明细`
4. 从 `剧本正文` 中裁出对应目标分镜帧的剧情桥段：
   - 若该分镜组只有 1 个分镜，直接使用整段 `剧本正文`
   - 若该分镜组有多个分镜，结合目标分镜的 `时间段`、`角色表现`、`分镜表现` 与角色/空间状态，只保留与该帧直接对应的事件阶段、动作节点或状态变化
   - 若桥段边界不清晰，保守压缩到“该帧可见的最小剧情事实”，不得虚构过渡
5. 原文保留 `组间设计.全局风格`，不得改写、净化、重命名或压缩。
6. 把 `组间设计.类型元素`、`组间设计.导演意图` 与目标镜级字段压缩到剩余字数预算。
7. 组装为 `meta + prompt_style + model + prompt + prompt_char_count` 请求对象；`meta.source_shot_ids` 固定只放 1 个目标 `分镜ID`。
8. 按共享 TXT 模板整理 `提示词 + 字数统计` 阅读视图。
9. 写入单集 JSON、TXT 与 `_manifest.json`。

## Variable Register

| var_id | 变量层级 | 观测信号 | 状态集合 | 检测方法 | 优先级 |
| --- | --- | --- | --- | --- | --- |
| V-VID-FFR-01 | 输入 | 目标分镜结构是否完整 | `ready/incomplete` | 检查 `分镜组ID/剧本正文/组间设计/目标分镜明细` | P0 |
| V-VID-FFR-02 | 桥段判定 | `剧本正文` 与目标分镜的对应清晰度 | `single_shot/direct_match/ambiguous` | 结合组内分镜数、时间段与动作状态 | P0 |
| V-VID-FFR-03 | 字数预算 | 非固定字段压缩压力 | `normal/tight/underflow` | 估算剧情桥段 + 全局风格后剩余字数 | P1 |

## Case To Strategy Map

| case_id | 触发谓词 | 主策略 | 通过标准 | fallback |
| --- | --- | --- | --- | --- |
| C-VID-FFR-01 | `V-VID-FFR-01=incomplete` | 停止并报告上游缺口 | 不伪造缺失字段 | 回上游导演真源补齐 |
| C-VID-FFR-02 | `V-VID-FFR-02=single_shot` | 直接使用整段 `剧本正文` 作为剧情桥段 | 桥段与目标分镜天然一一对应 | 无 |
| C-VID-FFR-03 | `V-VID-FFR-02=direct_match` | 提取与目标分镜直接对应的剧情桥段 | 不引入无关分镜事实 | 无 |
| C-VID-FFR-04 | `V-VID-FFR-02=ambiguous` | 保守压缩到目标分镜可见的最小剧情事实 | 不虚构过渡；manifest 备注原因 | `single_shot` |
| C-VID-FFR-05 | `V-VID-FFR-03=normal` | 用自然语句压缩非固定字段 | `prompt_char_count` 落在目标窗附近 | 无 |
| C-VID-FFR-06 | `V-VID-FFR-03=tight` | 把非固定字段压成短语或关键词串 | 固定块不动，整体仍尽量靠近目标窗 | 无 |
| C-VID-FFR-07 | `V-VID-FFR-03=underflow` | 保守保真，不虚构扩写 | 允许低于下限，但 manifest 备注原因 | 无 |

## Prompt Assembly Rules

1. 只允许显式保留 `分镜组 <ID>` 与 `分镜 <ID>` 两类标签。
2. `全局风格` 直接贴原文，不改写、不重命名。
3. `剧情桥段` 只允许对应目标分镜帧，不得直接整段复用全组 `剧本正文`，除非组内只有 1 个分镜。
4. `类型元素`、`导演意图` 与目标镜级字段一律不写字段标题，改写为自然句、高密度短语或关键词串。
5. 字数吃紧时，优先压缩非固定字段；固定块不得牺牲。
6. 源信息不足时，不为凑字数而虚构新事实；允许保守低于下限，但必须在 `_manifest.json` 备注。

## Prohibitions

- 禁止虚构 `reference_images`、`image_markers`、URL、主体图或未提供的参照图信息。
- 禁止改写、润色或净化上游事实，包括 `剧本正文` 与 `全局风格` 中的事实内容。
- 禁止把多个分镜拼成一条请求对象。
- 禁止暴露 `角色及站位和穿搭:`、`场景及方位:` 一类字段标题。
- 禁止在输入不完整时产出貌似完整的结果。

## Output Contract

### Canonical Landing

- `projects/<项目名>/6-Video/首帧参照/第N集/第N集.json`
- `projects/<项目名>/6-Video/首帧参照/第N集/第N集.txt`
- `projects/<项目名>/6-Video/首帧参照/第N集/_manifest.json`

### JSON Fill Scope

本技能负责填充：

1. `meta`
2. `prompt_style`
3. `model`
4. `prompt`
5. `prompt_char_count`

### Hard Rules

1. `第N集.json` 是 canonical completeness carrier；结构完整性、字段齐全性和下游消费能力都以 JSON 为准。
2. `第N集.txt` 只是 derived display view；它只展示 `prompt` 与 `prompt_char_count`，不承担结构完整性。
3. `_manifest.json` 是异常与追溯载体；低于目标字数、桥段保守退化、输入缺口或例外策略都必须记录。
4. 每个目标 `分镜ID` 在 `第N集.json` 中只生成 1 条请求对象。
5. `prompt` 必须覆盖目标分镜所属组的上下文与该目标分镜的全部镜级内容。
6. `全局风格` 必须原文保留，不得改写。
7. `剧本正文` 必须转换为对应分镜帧的剧情桥段；仅在组内只有 1 个分镜时允许整段直贴。
8. 默认目标字数为 `800-1200` 中文字符；若用户或父级显式给出其他范围，以显式约束覆盖。
9. `prompt_char_count` 必须与实际 `prompt` 内容一致，且 `第N集.txt` 中的字数统计必须与 JSON 同步。
10. `reference_images` 与 `image_markers` 仅保留共享模板骨架，不得擅自补入虚构图片信息。

### `_manifest.json` Minimum Fields

1. `episode_id`
2. `source_file`
3. `output_mode`
4. `json_file`
5. `txt_file`
6. `shot_count`
7. `shots[].group_id`
8. `shots[].shot_id`
9. `shots[].prompt_char_count`
10. `shots[].bridge_strategy`
11. `shots[].within_target_range`
12. `shots[].exception_note`

## Handoff Contract

- 若后续要正式生成视频，直接将本 JSON 交给 `.agents/skills/cli/dreamina-cli/SKILL.md` 或 `6-Video/2-视频生成` 继续消费。
- `TXT` 仅作为人工审阅副产物保留，不作为 canonical handoff 载体。
- `_manifest.json` 负责承载异常说明、桥段策略与验收证据。

## Field Master

| field_id | 输出位置/字段 | 内容要求 | 默认责任 Step | 质量维度 | 失败码 |
| --- | --- | --- | --- | --- | --- |
| FIELD-VID-FFR-01 | `prompt_style.type / prompt_style.language / prompt_style.char_limit / meta.shot_level / meta.group_id / meta.source_shot_ids` | 以独立 `prompt_style` 声明帧级提示词约束，并锁定组级归属与单一目标 `分镜ID` | S1 | 输入覆盖完整度 | FAIL-VID-FFR-01 |
| FIELD-VID-FFR-02 | `prompt / prompt_char_count` | prompt 必须覆盖目标分镜的剧情桥段、全局风格和压缩后的上下文，且隐藏字段标题 | S2-S4 | Prompt 蒸馏稳定性 | FAIL-VID-FFR-02 |
| FIELD-VID-FFR-03 | `model.reference_images / model.image_markers` | 当前按共享模板骨架保留，不擅自填入虚构图片信息 | S5 | 模板兼容性 | FAIL-VID-FFR-03 |
| FIELD-VID-FFR-04 | `第N集.json / 第N集.txt / _manifest.json` | 三件套可追溯、可继续 handoff，且例外说明完整 | S6 | 输出可消费性 | FAIL-VID-FFR-04 |

## Thought Pass Map

| step_id | 聚焦字段 | 核心问题 | 生成动作 | 未达标信号 |
| --- | --- | --- | --- | --- |
| S1 | FIELD-VID-FFR-01 | 当前目标 `分镜ID` 是谁，属于哪个 `分镜组` | 锁定 `prompt_style + shot_level + group_id + source_shot_ids` | 分镜定位冲突、缺失或多镜混入 |
| S2 | FIELD-VID-FFR-02 | `剧本正文` 中哪一段才对应目标分镜 | 提取对应分镜帧的剧情桥段 | 直接整段照搬组级剧本正文 |
| S3 | FIELD-VID-FFR-02 | 哪些内容必须原文保留，哪些内容应压缩 | 直贴 `全局风格`，压缩其余组级与目标镜级字段 | 固定块被改写或压缩失衡 |
| S4 | FIELD-VID-FFR-02 | 如何隐藏字段标题仍保住结构 | 仅保留组ID/镜ID显式标签 | 出现字段标题残留 |
| S5 | FIELD-VID-FFR-03 | 参照图字段当前如何处理 | 保持共享模板骨架，不填虚构信息 | 擅自补图或删字段 |
| S6 | FIELD-VID-FFR-04 | 输出是否能同时被视频工具与人工审阅消费 | 写 JSON、TXT、manifest 与统计字段 | 只产出单文件或缺少异常台账 |

## Pass Table

| field_id | Pass Standard | Fail Code | Rework Entry |
| --- | --- | --- | --- |
| FIELD-VID-FFR-01 | `prompt_style.type / meta.shot_level` 合法，且 `group_id` 与长度为 1 的 `source_shot_ids` 同时成立 | FAIL-VID-FFR-01 | S1 |
| FIELD-VID-FFR-02 | prompt 满足桥段提取、固定块保留、隐藏标题与字数窗 | FAIL-VID-FFR-02 | S2-S4 |
| FIELD-VID-FFR-03 | 图片字段保留共享模板骨架且无虚构内容 | FAIL-VID-FFR-03 | S5 |
| FIELD-VID-FFR-04 | JSON、TXT 与 manifest 可追溯、可 handoff，且例外信息完整 | FAIL-VID-FFR-04 | S6 |

## Quality And Audit Contract

至少验收以下项目：

- `group_id`、`shot_id`、`source_shot_ids` 是否能同时回链到目标分镜
- `prompt_char_count` 是否与实际 prompt 一致
- `bridge_strategy` 是否与剧情桥段提取策略一致
- `within_target_range` 是否如实反映字数窗命中情况
- `exception_note` 是否记录了 underflow、保守桥段或输入缺口
- `第N集.json / 第N集.txt / _manifest.json` 是否三件套齐全

## Root-Cause Execution Contract (Mandatory)

当出现以下症状时，必须先修本技能合同，而不是直接润色 prompt：

- prompt 明明是帧级任务，却直接复用了整组 `剧本正文`
- prompt 对应错了 `分镜ID`，或没能回链到所属 `分镜组ID`
- `全局风格` 被改写，或 `剧情桥段` 中新增了上游没有的事实
- prompt 里仍然残留 `角色及站位和穿搭:` 这类字段标题
- 参照图字段被擅自填入虚构 URL、主体或图片说明

必经链路：

`Symptom -> Direct Technical Cause -> Rule Source -> Meta Rule Source -> Fix Landing Points`

优先检查：

- `Rule Source`
  - `.agents/skills/aigc/6-Video/1-提示词蒸馏/首帧参照/SKILL.md`
  - `.agents/skills/aigc/6-Video/1-提示词蒸馏/首帧参照/CONTEXT.md`
- `Meta Rule Source`
  - `.agents/skills/aigc/6-Video/SKILL.md`
  - `.agents/skills/aigc/SKILL.md`
  - 根 `AGENTS.md`

对用户的闭环输出固定包含：

1. 根因位置
2. 立即修复
3. 系统预防修复

## Context Writeback Contract

- 稳定执行规则、字段表、输出契约与路径合同只能写回本 `SKILL.md`。
- 失败模式、保守桥段经验、字数压力 heuristics 与里程碑案例写回 `CONTEXT.md`。
- 若再次出现“把规范拆回 `references/`”或“路径口径再次漂移”的倾向，视为 source-layer regression，必须优先修回单一主合同。
