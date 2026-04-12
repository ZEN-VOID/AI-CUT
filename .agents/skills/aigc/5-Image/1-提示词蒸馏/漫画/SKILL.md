---
name: aigc-storyboard-comic
description: Use when the `5-Image` stage needs to turn a storyboard group from `projects/<项目名>/3-Detail/第N集.json` into group-level image request JSON for a comic page, especially before downstream consistency or image-generation work.
governance_tier: full
---

# 5-Image / 1-提示词蒸馏 / 漫画

## Mode Selection

- 本技能已从“`SKILL.md + references/*` 并行合同”升格为“单一 `SKILL.md` 真源”。
- 原 `references/chain-of-thought.md`、`execution-flow.md`、`type-strategies.md`、`output-template.md` 的规范内容已全部内联到本文件。
- 当前不创建本地 `subagent team` 或 `team.md`：本技能是确定性的叶子蒸馏单元，不存在值得长期沉淀的多角色并发工作面。
- 若未来出现稳定的 `planner / reviewer / auditor` 分工，应优先在父级 `1-提示词蒸馏` 层治理，而不是在本叶子技能里重建第二总线。

## 概述

`漫画` 负责把一个已经进入共享编导根文件的分镜组，整理成漫画单页的图像生成请求 JSON。

本技能只负责 `分镜组 -> 漫画页图像请求对象` 的蒸馏，不负责真实出图，也不改写上游镜头事实。

交付重点固定为：

1. 共享模板兼容的 `meta`
2. 面向漫画单页的 `prompt_style`
3. 图像生成侧 `model` 参数骨架与参照图预留位
4. 由固定漫画前缀与 `comic_page_group` 内容块拼成的 `prompt`
5. 对应的 `prompt_char_count`

## When to Use

- 需要把一个分镜组整理成漫画页的图像生成请求 JSON。
- 用户明确要气泡文字、旁白框、漫画阅读节奏或 9:16 漫画页。
- 当前任务处于 `1-提示词蒸馏`，后续再进入一致性处理或图像生成。

## When Not to Use

- 只需要普通 storyboard sheet，应进入 `分镜故事板`。
- 只需要单一镜头的首帧或单帧图，应进入 `分镜帧`。
- 上游 `3-Detail/第N集.json` 尚未形成可唯一定位的分镜组与组内顺序。

## Truth Ownership

### `漫画` 拥有

- 分镜组 -> 漫画图像请求条目的一对一转换合同
- 固定漫画前缀 + `comic_page_group` 的 prompt 组织规则
- `1 shot = 1 panel` 与文字系统约束在 prompt 中的显式表达
- 对 `.agents/skills/aigc/5-Image/_shared/image-generation-input.template.json` 的局部填充规则
- `json_only / full_trace` 两种输出模式下的单集落盘合同

### `漫画` 不拥有

- 父级 `1-提示词蒸馏` 的对象裁决与互斥路由权
- 整组 storyboard sheet 合同
- 单帧关键帧合同
- 一致性二次处理与真实图片生成
- 上游文本与镜头事实改写

## Canonical Inputs

- `projects/<项目名>/3-Detail/第N集.json`
- `.agents/skills/aigc/_shared/director_episode_output.schema.json`
- `.agents/skills/aigc/5-Image/_shared/image-generation-input.template.json`

### 推荐补充输入

- `projects/<项目名>/3-Detail/evidence/` 下相关 sidecar：只在需要补充对白原文或人工上下文时读取
- `projects/<项目名>/4-Design/` 下角色、场景、道具参考：只登记到图像参照槽位，不改写镜头事实

## Canonical Landing

- 子路径根目录：`projects/<项目名>/5-Image/漫画/`
- 单集目录：`projects/<项目名>/5-Image/漫画/第N集/`
- 汇总 JSON：`projects/<项目名>/5-Image/漫画/第N集/第N集.json`
- 汇总清单：`projects/<项目名>/5-Image/漫画/第N集/_manifest.json`，仅在 `full_trace` 时输出

## Trigger Contract

- 本技能只能由父级 `.agents/skills/aigc/5-Image/1-提示词蒸馏/SKILL.md` 路由命中，或在用户明确指定“漫画页 / 漫画气泡 / 漫画阅读节奏”时直接命中。
- 默认消费单位是一个可唯一回链的 `分镜组`，不下沉为单帧，也不并行生成多个对象类型。
- 若当前请求同时混有 `分镜故事板`、`分镜帧`、`漫画` 多种对象，先回到父级拆成独立任务，不在本技能内强行聚合。
- 若 shared schema 不能确认组边界，或共享模板骨架被破坏，必须停止并报告上游缺口。

## Topology Contract

- 本技能是叶子执行单元，不在本地再派发 `subagents`。
- 运行拓扑固定为单线串行：`S1 组定位 -> S2 组内容提取 -> S3 prompt 拼接 -> S4 模板填充 -> S5 落盘与验收`。
- 本技能不拥有 sibling 并发权，也不把目录名当作顺序真源。
- 若未来引入独立 reviewer 或 auditor，只能返回 `review_note` 或 `audit_report`，最终写回权仍归本技能主合同。

## Handoff Contract

### 输入单位

- 一个能通过 shared schema 唯一定位的 `分镜组`
- 该组对应的有序 `分镜明细[]`

### 输出单位

- `第N集.json` 中每个分镜组 1 条漫画图像请求对象
- 按需输出 `_manifest.json`

### 本技能负责填充的 JSON 字段

1. `meta`
2. `prompt_style`
3. `model`
4. `prompt`
5. `prompt_char_count`

### 下游交接

- 本技能产物用于后续一致性处理或图像生成阶段消费。
- 本技能本身不生成图片，不额外输出 `.txt` 派生视图，不创建平行私有模板。

## Context Contract

### 强制加载顺序

1. `.agents/skills/aigc/SKILL.md`
2. `.agents/skills/aigc/5-Image/1-提示词蒸馏/SKILL.md + CONTEXT.md`
3. 本 `SKILL.md + CONTEXT.md`

### 说明

- 当前仓没有独立的 `.agents/skills/aigc/5-Image/SKILL.md` 阶段根合同；对本技能而言，直接父级就是 `1-提示词蒸馏`。
- `3-Detail/evidence/` 与 `4-Design/` 参考只作为补充证据或参照图来源，不能覆盖 `3-Detail/第N集.json` 的第一结构化真源地位。
- 缺失字段允许保守留空，不得为了凑完整度虚构新镜头、新对白或新导演意图。

## Type System

### 变量登记表

| var_id | 变量层级 | 观测信号 | 状态集合 | 检测方法 | 优先级 |
| --- | --- | --- | --- | --- | --- |
| V-SB-COMIC-01 | 输入 | 分镜组结构是否完整 | `ready/incomplete` | 检查 `分镜组ID/剧本正文/组间设计/分镜明细` | P0 |
| V-SB-COMIC-02 | prompt 内容块 | `comic_page_group` 是否完整 | `ready/partial` | 检查组级字段、镜级顺序与漫画硬门槛 | P1 |
| V-SB-COMIC-03 | 输出要求 | 本轮只要 JSON 还是 JSON+manifest | `json_only/full_trace` | 结合用户目标与父级要求 | P1 |

### 情况判定表

| case_id | 触发谓词 | 置信度阈值 | 互斥关系 | 可并发关系 |
| --- | --- | --- | --- | --- |
| C-SB-COMIC-01 | `V-SB-COMIC-01=incomplete` | 1.0 | 互斥全部生成路由 | 无 |
| C-SB-COMIC-02 | `V-SB-COMIC-02=ready` | 0.95 | 互斥 `C-SB-COMIC-03` | 可并发 `C-SB-COMIC-04` |
| C-SB-COMIC-03 | `V-SB-COMIC-02=partial` | 0.90 | 互斥 `C-SB-COMIC-02` | 可并发 `C-SB-COMIC-04` |
| C-SB-COMIC-04 | `V-SB-COMIC-03=full_trace` | 0.90 | 无 | 可并发 `C-SB-COMIC-02/C-SB-COMIC-03` |

### 策略映射矩阵

| case_id | strategy_id | 执行步骤 | 质量门禁 | fallback_strategy_id | 升级条件 |
| --- | --- | --- | --- | --- | --- |
| C-SB-COMIC-01 | S-COMIC-BACKTRACK | 停止并报告上游缺口 | 不伪造缺失组或镜头事实 | S-COMIC-PAUSE | 上游缺口持续存在 |
| C-SB-COMIC-02 | S-COMIC-MAINLINE | 用完整 `comic_page_group` 填充共享模板 | 固定前缀、漫画硬门槛、组级字段和镜级顺序全部成立 | S-COMIC-PAUSE | 模板字段被局部删改 |
| C-SB-COMIC-03 | S-COMIC-PARTIAL | 保守填充已有内容，不虚构缺失字段 | 输出仍可回链真实上游内容 | S-COMIC-PAUSE | 缺口影响后续消费 |
| C-SB-COMIC-04 | S-COMIC-FULL-TRACE | 输出 JSON + manifest | 两文件互相可追溯 | S-COMIC-MAINLINE | 本轮只要求 `json_only` |

### 路由与回退卡

- 默认判定顺序：`shared group list -> comic_page_group 内容完整度 -> 输出模式`
- unknown 默认路由：按 `json_only` 执行，但必须显式说明哪些字段保守留空
- 停止条件：无法从 shared schema 确认分镜组结构，或共享模板字段骨架被破坏

## Mandatory Workflow

1. 读取 `.agents/skills/aigc/5-Image/1-提示词蒸馏/SKILL.md + CONTEXT.md`，确认本轮已明确命中 `漫画`。
2. 读取 `projects/<项目名>/3-Detail/第N集.json`，校验其可回链 `.agents/skills/aigc/_shared/director_episode_output.schema.json` 的共享字段壳。
3. 从 `final_output.main_content.分镜组列表[]` 中定位目标分镜组，提取：
   - `分镜组ID`
   - `剧本正文`
   - `组间设计.全局风格`
   - `组间设计.类型元素`
   - `组间设计.导演意图`
   - 全部按原顺序排列的 `分镜明细[]`
4. 将上述内容组织为 `comic_page_group` 内容块；内容允许直接使用，不做文字压缩。
5. 以共享模板为骨架填充 `meta + prompt_style + model + prompt + prompt_char_count`。
6. 如有 `4-Design` 参考资产，只把它们登记到 `model.reference_images / image_markers` 的预留位。
7. 写入单集 `第N集.json`；仅在任务要求 `full_trace` 时额外输出 `_manifest.json`。

## Prompt Assembly Rules

1. 固定前缀必须逐字保留：

   ```text
   Create a single comic page based on the following storyboard group.
   Keep exactly one panel per shot in the original sequence.
   Place dialogue, monologue, and narration only inside their corresponding panels.
   Auto-adapt the comic page layout based on the total number of shots.
   ```

2. `prompt` 必须严格等于“固定前缀 + `comic_page_group`”，中间不得插入额外模板说明。
3. `comic_page_group` 必须覆盖：
   - `分镜组ID`
   - `剧本正文`
   - `组间设计.全局风格`
   - `组间设计.类型元素`
   - `组间设计.导演意图`
   - 全部按原顺序排列的 `分镜明细[]`
4. `comic_page_group` 必须显式表达 `1 shot = 1 panel`，并要求对白、独白、旁白只能落在对应 panel 内。
5. 若上游内容存在空缺，允许保守留空，不得为凑完整度虚构镜头事实。

## Synthesis Contract

### 输出硬规则

1. `第N集.json` 是 canonical completeness carrier；结构完整性与下游消费能力一律以 JSON 为准。
2. 当前模式只输出 JSON，不输出 `.txt` 派生视图。
3. 每个分镜组只生成 1 条请求对象。
4. `meta.shot_level` 固定为 `storyboard_group`；`meta.group_id` 与 `meta.source_shot_ids` 必须能完整回链该组。
5. `prompt_style.type` 固定服务漫画单页；`prompt_style.language` 默认标记为 `mixed`。
6. `model` 必须保持图像侧参数骨架完整；`reference_images` 与 `image_markers` 在缺图时也必须保留空骨架。
7. `prompt_char_count` 必须与实际 `prompt` 内容一致。
8. 只有父级或用户明确要求时，才额外输出 `_manifest.json`；否则默认 `json_only`。

### `_manifest.json` 最低要求

1. `episode_id`
2. `source_file`
3. `output_mode`
4. `json_file`
5. `group_count`
6. `groups[].group_id`
7. `groups[].source_shot_ids`
8. `groups[].prompt_char_count`
9. `groups[].has_reference_slots`
10. `groups[].exception_note`

## Audit Contract

### 质量评估面

- `contract_compliance`：是否遵守分镜组输入、固定前缀、模板骨架与输出模式约束
- `input_coverage`：是否完整覆盖组级字段与镜级顺序
- `prompt_integrity`：是否满足“固定前缀 + comic_page_group + 1 shot = 1 panel”
- `template_compatibility`：是否与共享模板保持兼容
- `handoff_readiness`：下游是否可直接继续消费 `第N集.json`

### 失败闭环

- 若失败，必须返回：`root cause location + immediate fix + systemic prevention fix`
- 若发现共享规范漂移，优先修本 `SKILL.md` 或共享模板真源，而不是继续重建 `references/` 第二套合同
- 若本技能内再次出现 `references/*` 规范分拆，应视为源层回退

## Legacy Migration Mapping

| 旧载体 | 当前真源落点 | 处理方式 |
| --- | --- | --- |
| `references/chain-of-thought.md` | `Field Master / Thought Pass Map / Pass Table` | 已内联并废弃旧文件 |
| `references/execution-flow.md` | `Canonical Inputs / Canonical Landing / Mandatory Workflow / Prompt Assembly Rules` | 已内联并废弃旧文件 |
| `references/type-strategies.md` | `Type System` | 已内联并废弃旧文件 |
| `references/output-template.md` | `Handoff Contract / Synthesis Contract` | 已内联并废弃旧文件 |

## Field Master

| field_id | 输出位置/字段 | 内容要求 | 默认责任 Step | 质量维度 | 失败码 |
| --- | --- | --- | --- | --- | --- |
| FIELD-SB-COMIC-01 | `prompt_style.type / prompt_style.language / prompt_style.char_limit / meta.shot_level / meta.group_id / meta.source_shot_ids` | 以独立 `prompt_style` 声明漫画页提示词约束，并锁定组级来源与镜头顺序 | S1 | 输入覆盖完整度 | FAIL-SB-COMIC-01 |
| FIELD-SB-COMIC-02 | `prompt / prompt_char_count` | `prompt` 必须由固定漫画前缀与完整 `comic_page_group` 组成，且顶层字数统计一致 | S2-S3 | Prompt 蒸馏稳定性 | FAIL-SB-COMIC-02 |
| FIELD-SB-COMIC-03 | `model.model_version / model.ratio / model.image_size / model.output_format / model.num_images / model.reference_images / model.image_markers` | `model` 必须保持图像侧模板骨架完整；无图时也保留参照槽位 | S4 | 模板兼容性 | FAIL-SB-COMIC-03 |
| FIELD-SB-COMIC-04 | `第N集.json / _manifest.json` | 输出文件可追溯，可继续 handoff 给后续阶段消费 | S5 | 输出可消费性 | FAIL-SB-COMIC-04 |

## Thought Pass Map

| step_id | 聚焦字段 | 核心问题 | 生成动作 | 未达标信号 |
| --- | --- | --- | --- | --- |
| S1 | FIELD-SB-COMIC-01 | 当前目标分镜组是谁，组内镜头顺序是否稳定 | 锁定 `prompt_style + shot_level + group_id + source_shot_ids` | 组定位冲突或镜头顺序缺失 |
| S2 | FIELD-SB-COMIC-02 | `comic_page_group` 需要覆盖哪些上游字段和漫画约束 | 提取 `剧本正文 + 组间设计 + 全部分镜明细[]`，并加入 `1 shot = 1 panel` 与文字归属要求 | 漏掉组级字段、镜级字段或漫画硬门槛 |
| S3 | FIELD-SB-COMIC-02 | `prompt` 是否严格满足“固定前缀 + comic_page_group” | 逐字保留固定前缀并拼接内容块 | 前缀缺失、顺序错误或额外插入说明 |
| S4 | FIELD-SB-COMIC-03 | 图像请求模板字段是否完整且不虚构参照图 | 保留图像侧参数骨架与参照图槽位 | 删字段、乱序或擅自补图 |
| S5 | FIELD-SB-COMIC-04 | 输出是否已形成可 handoff 的单集 JSON | 写 `第N集.json`，按需补 `_manifest.json` | 仍把图片落盘当主产物或缺少 JSON |

## Pass Table

| field_id | Pass Standard | Fail Code | Rework Entry |
| --- | --- | --- | --- |
| FIELD-SB-COMIC-01 | `prompt_style.type / meta.shot_level` 合法，且 `group_id` 与有序 `source_shot_ids` 同时成立 | FAIL-SB-COMIC-01 | S1 |
| FIELD-SB-COMIC-02 | `prompt` 满足固定前缀、完整 `comic_page_group`、`1 shot = 1 panel` 与顶层字数统计 | FAIL-SB-COMIC-02 | S2-S3 |
| FIELD-SB-COMIC-03 | 图像侧 `model` 骨架完整，`reference_images` 与 `image_markers` 保持共享模板兼容 | FAIL-SB-COMIC-03 | S4 |
| FIELD-SB-COMIC-04 | `第N集.json` 可追溯可 handoff；若要求 `full_trace`，则 `_manifest.json` 同步成立 | FAIL-SB-COMIC-04 | S5 |

## Root-Cause Execution Contract (Mandatory)

当出现以下症状时，必须先修本子技能合同：

- 仍把图片落盘当主产物，而不是组级漫画图像请求 JSON
- `prompt` 没有以固定漫画前缀开头
- `comic_page_group` 没覆盖完整组级与镜级信息
- `1 shot = 1 panel` 或文字归属约束没有进入 `prompt`
- 共享模板字段被删改，尤其是 `reference_images` 或 `image_markers`
- 再次把规范内容拆回 `references/`，形成第二套真源

必经链路：

`Symptom -> Direct Technical Cause -> Rule Source -> Meta Rule Source -> Fix Landing Points`

优先检查：

- `Rule Source`
  - `.agents/skills/aigc/5-Image/1-提示词蒸馏/漫画/SKILL.md`
  - `.agents/skills/aigc/5-Image/1-提示词蒸馏/漫画/CONTEXT.md`
  - `.agents/skills/aigc/5-Image/1-提示词蒸馏/SKILL.md`
- `Meta Rule Source`
  - `.agents/skills/aigc/SKILL.md`
  - `/Users/vincentlee/.codex/skills/meta/构建/技能/skill-subagents/SKILL.md`
  - 根 `AGENTS.md`

若需要继续上溯，当前仓对本技能不存在独立 `5-Image/SKILL.md` 阶段根合同，应显式说明上溯在 `1-提示词蒸馏` 父级结束，而不是引用不存在的旧路径。

## SKILL / CONTEXT 分工（Mandatory）

- `SKILL.md` 锁定触发条件、输入输出、workflow、类型策略、字段表、质量门槛与闭环合同。
- `CONTEXT.md` 只保留失败模式、修复 playbook、复用 heuristic 与里程碑案例。
- 稳定经验可从 `CONTEXT.md` 晋升回本 `SKILL.md`；未经验证的经验不得重新拆成 `references/` 规范载体。

## Context Preload (Mandatory)

- 执行前先加载 `.agents/skills/aigc/SKILL.md`。
- 再加载 `.agents/skills/aigc/5-Image/1-提示词蒸馏/SKILL.md + CONTEXT.md`。
- 最后加载本 `SKILL.md + CONTEXT.md`。
- 优先级遵循：用户显式请求 > 根 `AGENTS.md` > `.agents/skills/aigc/SKILL.md` > `.agents/skills/aigc/5-Image/1-提示词蒸馏/SKILL.md` > 本 `SKILL.md` > 各级 `CONTEXT.md`。
