---
name: aigc-planning-format
description: Use when planning the formatting contract for episode documents in the AIGC planning stage, especially when choosing between standard drama and explainer drama before script execution.
governance_tier: full
---

# aigc 1-规划 / 2-格式

## 概述

`2-格式` 是 `1-规划` 阶段里负责“文稿格式化结果”的父技能。

它只负责三件事：

1. 识别当前项目需要哪一种文稿格式变体
2. 在不改动原文事实与原文措辞的前提下，为已确定集内容附加该变体下的字段标题与场景骨架
3. 把唯一主变体与格式化结果稿交接给后续 `3-分组`、`2-组间` 与 `3-明细`

它不新增故事事实，也不替下游阶段发明导演、镜头或主体细节。

## When to Use

- 需要先决定项目后续剧本文稿采用哪一种结构化格式。
- 需要在 `标准剧 / 解说剧` 两种文本组织方式之间做唯一裁决。
- 需要把场景标题、文本字段、画面字段、字数同步和验证门禁提前写成规划合同。
- 需要为后续 `3-明细`、`5-画面` 提供统一消费接口，而不是每一集临时发明格式。

## When Not to Use

- 当前任务是直接写某一集正文，而不是规划文稿格式。
- 只是做单次排版美化，不需要形成可复用的项目级格式合同。
- 项目还缺少 `0-Init` 的基本种子，无法判断叙事型态和下游消费方式。

## 父技能边界

### `2-格式` 拥有

- 变体判定
- 集级格式化结果稿
- 字段附加规则
- 向下游阶段的格式交接说明

### `2-格式` 不拥有

- 逐场景对白、独白、旁白正文创作
- 导演意图、视听风格或镜头语法真源
- 项目分组/批次规划
- `## G01 / G02 ...` 一类组容器或组级摘要投影

## Reference Modules (Mandatory)

`2-格式/SKILL.md` 只保留主合同、边界、路由、字段门禁与闭环；专项细则以下列模块为真源：

- `references/chain-of-thought.md`
- `references/execution-flow.md`
- `references/type-strategies.md`
- `references/output-template.md`

硬规则：

1. 详细执行链、回退链、VSM 四件套与模板骨架以下列 `references/` 文件为主。
2. 主 `SKILL.md` 只保留摘要、入口、硬门槛与回链，不再平行复制完整细则。
3. 子技能 `标准剧 / 解说剧` 必须各自继承同样的“主合同 + references”结构。

## Visual Maps

```mermaid
flowchart TD
    A["进入 2-格式"] --> B["读取 Init seeds + 1-分集结果 + 用户偏好"]
    B --> C["完成 VSM 判模"]
    C --> D{"唯一主变体裁决"}
    D -->|"未显式要求解说 / 默认表演优先"| E["进入 subtypes/标准剧"]
    D -->|"显式要求旁白主导 / 解说剧"| F["进入 subtypes/解说剧"]
    D -->|"用户要求双案对照"| G["并行生成两套合同并标推荐主案"]
    E --> H["产出 标准剧格式化结果稿"]
    F --> I["产出 解说剧格式化结果稿"]
    G --> J["汇总双案对照与推荐主案"]
    H --> K["汇总父级结果结论"]
    I --> K
    J --> K
```

```mermaid
flowchart LR
    A["projects/<项目名>/Init/north_star.yaml"] --> D["2-格式判模"]
    B["projects/<项目名>/Init/init_handoff.yaml"] --> D
    C["projects/<项目名>/Init/episode-split-plan.json 或 projects/<项目名>/规划/第N集.md"] --> D
    D --> E["标准剧"]
    D --> F["解说剧"]
    E --> G["projects/<项目名>/规划/2-格式/"]
    F --> G
    G --> H["下游 3-明细 / 5-画面"]
```

## Canonical Landing

- 父级根目录：`projects/<项目名>/规划/2-格式/`
- 父级结果稿：`projects/<项目名>/规划/2-格式/第N集.md`
- 父级总报告：默认降为按需 sidecar；父级全链模式下以 `projects/<项目名>/规划/第N集.md` 中的格式化正文为准

## 输入合同

- `projects/<项目名>/Init/north_star.yaml`
- `projects/<项目名>/Init/init_handoff.yaml`
- `projects/<项目名>/Init/episode-split-plan.json` 或 `projects/<项目名>/规划/第N集.md`
- 项目预设中的叙事类型、受众、平台时长、消费节奏说明
- 用户提供的参考文稿或既有项目格式样例

## VSM Complexity (Mandatory)

- complexity_level: `medium`
- 判定依据：存在 `叙事主通道`、`解说显式信号`、`下游消费方式`、`输入完整度` 四类变量，且存在互斥主变体与双案对照回退。
- 完整 VSM 四件套真源：`references/type-strategies.md`

## 核心约束（Mandatory）

1. 先判变体，再写格式化结果稿。
2. 没有显式“解说剧 / 旁白主导”信号时，默认进入 `标准剧`。
3. `标准剧` 与 `解说剧` 正式落盘时默认互斥，只能输出唯一主变体。
4. 若用户明确要求“两套格式都做对照”，允许并行生成，但必须显式标注推荐主变体。
5. 参考仓只继承能力结构，不继承旧路径；所有结果必须重写到当前 `projects/<项目名>/规划/2-格式/`。
6. `2-格式` 默认执行模式为“原文保真 + 字段标题附加”：允许补 `### 场景X`、`动作画面：`、`对白（角色）：`、`对白画面：` 等结构标题，但不得改写、压缩、润色、同义替换或重述原文正文。
7. 若 `source_type in {storyboard_script, hybrid_story_text}` 且 `locked_preset_axes` 包含 `scene_boundary`，`场景号` 只能按连续时空编号；`镜号 / 锚点 / 组号` 必须单独显式保留，不得把镜号直接升格为新场景号。
8. 若 `source_type in {storyboard_script, hybrid_story_text}`，`2-格式` 必须优先保留上游已明确写出的镜头语言；处理重点是把既有分镜表达规范化整理，而不是默认补齐第二套画面结构。
9. 若上游已提供可解析的场景标题、场次边界或镜头块标题，结果稿必须优先复用这些结构证据，不得先抹平再重概括。
10. `镜头语言预设` 仅允许整理上游已明确写出的运镜/镜头提示，且必须紧跟相关 `*画面` 条目；不得凭空新增、脑补补写或把导演层推断伪装成源文本证据。
11. `2-格式/第N集.md` 只能保持 scene-first draft，不得提前写入 `## G01 / G02 ...` 组容器；组级投影只属于 `3-分组` 子产物与父级 `规划/第N集.md` 聚合阶段。

## Mandatory Workflow

执行摘要如下；详细 phase、fallback 与局部验证顺序见 `references/execution-flow.md`：

1. 读取 `Init` 种子、`1-分集` 结果与用户要求，确认任务属于“格式化处理”。
2. 依据 `references/type-strategies.md` 完成变量识别、情况判定与唯一主变体裁决。
3. 路由到 `标准剧` 或 `解说剧` 子技能，按被选变体为当集原文附加字段标题与场景骨架，不改写原文正文。
4. 默认落盘 `projects/<项目名>/规划/2-格式/第N集.md`；说明性报告仅按需保留。
5. 返回唯一推荐入口；若双案对照，则返回“推荐主案 + 备选案”的明确关系。

## Council Runtime Inheritance (Mandatory)

`2-格式` 不单独定义顾问团运行时，而是强制继承上层 `1-规划` 的 `Council Runtime Contract`。

执行规则：

1. 进入本父技能或其变体子技能前，先遵守 `1-规划` 根技能对项目根 `team.yaml` 的读取规则。
2. 若顾问团启用，则由 `策划` 先对格式变体裁决与下游消费方式给建议。
3. 父级 `validation-report.md` 前后若命中 `评审`，仍按 `1-规划` 根技能的阶段级闸门执行。
4. 本父技能与其变体子技能都不夺取主代理的 canonical 写回权。

## 输出合同摘要

主模板真源位于 `references/output-template.md`。父技能至少应稳定产出：

- `第N集.md` 格式化结果稿
- 主变体选择结论
- 下游交接说明与返工入口

## Field Master

| field_id | 输出位置/字段 | 内容要求 | 证据来源 | 默认责任 Step | 质量维度 | 失败码 |
| --- | --- | --- | --- | --- | --- | --- |
| FIELD-FMT-VARIANT-01 | `第N集.md / 文稿格式` | 唯一裁决为 `标准剧` 或 `解说剧`，并按其规则附加字段标题 | 用户要求、项目预设、`Init` 种子 | S1 | 判模准确性 | FAIL-FMT-VARIANT |
| FIELD-FMT-DRAFT-02 | `第N集.md / 正文场景块` | 在不改变原文措辞的前提下，把原文挂到场景与字段标题下 | 原文、被选变体规则 | S2 | 结果稿完整性 | FAIL-FMT-DRAFT |
| FIELD-FMT-HANDOFF-03 | `第N集.md / 结构边界` | 保留供 `3-分组` 可继续切组的场景边界、字段边界和锚点关系；不得提前写入组容器 | 父子技能结论 | S3 | 交接清晰度 | FAIL-FMT-HANDOFF |

## Thought Pass Map

| step_id | 聚焦字段 | 核心问题 | 生成动作 | 未达标信号 |
| --- | --- | --- | --- | --- |
| S1 | FIELD-FMT-VARIANT-01 | 现有信号支持哪一种主变体 | 锁定唯一主变体并说明原因 | 标准/解说边界模糊 |
| S2 | FIELD-FMT-DRAFT-02 | 如何在不改写原文的前提下附加该变体字段 | 产出可直接阅读的保真格式稿 | 改写了原文或只剩合同说明 |
| S3 | FIELD-FMT-HANDOFF-03 | 如何把结果交给 `3-分组` 与父级主稿 | 保留场景边界与锚点关系 | 下游不知道从哪里继续切组 |

## Pass Table

| field_id | Pass Standard | Fail Code | Rework Entry |
| --- | --- | --- | --- |
| FIELD-FMT-VARIANT-01 | 主变体唯一且理由清楚 | FAIL-FMT-VARIANT | S1 |
| FIELD-FMT-DRAFT-02 | 结果稿可直接阅读，且原文措辞未被改写 | FAIL-FMT-DRAFT | S2 |
| FIELD-FMT-HANDOFF-03 | 下游入口与边界清楚 | FAIL-FMT-HANDOFF | S3 |

## Root-Cause Execution Contract (Mandatory)

当出现以下症状时，必须先修 `2-格式` 父子合同，而不是只补某一份样例文稿：

- 标准剧与解说剧的边界说不清
- 子变体已经存在，但父级看不出何时进入哪个变体
- 参考仓的“正文改写技能”被直接照搬成规划技能
- 下游每一集都重新发明字段名和场景标题格式

必经链路：

`Symptom -> Direct Technical Cause -> Rule Source -> Meta Rule Source -> Fix Landing Points`

优先检查：

- `Rule Source`
  - `.agents/skills/aigc/1-规划/subtypes/2-格式/SKILL.md`
  - `.agents/skills/aigc/1-规划/subtypes/2-格式/CONTEXT.md`
  - `.agents/skills/aigc/1-规划/subtypes/2-格式/subtypes/*/SKILL.md`
  - `.agents/skills/aigc/1-规划/SKILL.md`
- `Meta Rule Source`
  - `.agents/skills/aigc/SKILL.md`
  - 根 `AGENTS.md`

## 完成标准

- 已锁定唯一主变体
- 已产出对应集的格式化结果稿 `第N集.md`
- 结果稿已可被 `3-分组` 继续消费
- 已给出下游唯一推荐入口

## Context Preload (Mandatory)

- 执行前先加载上层 `.agents/skills/aigc/1-规划/SKILL.md` 与 `CONTEXT.md`。
- 再加载本 `SKILL.md` 与本地 `CONTEXT.md`。
- 进入具体变体时，继续加载 `subtypes/<变体>/SKILL.md` 与 `CONTEXT.md`。
- 需要细化思维链、执行流、VSM 或模板时，继续加载本目录下对应 `references/*.md`。
- 若项目根 `team.yaml.enabled == true`，继承上层 `1-规划` 的顾问团运行时，不在本层重复定义第二套规则。
- 优先级遵循：用户显式请求 > 根 `AGENTS.md` > `.agents/skills/aigc/SKILL.md` > 上层 `1-规划/SKILL.md` > 本 `SKILL.md` > 各级 `CONTEXT.md`。
