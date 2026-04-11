---
name: aigc-detail-storyboard-density
description: Use when `1-分镜表现` must decide how many inline storyboard inserts a grouped script segment should receive, by mapping rhythm, scene type, duration, and information load to a single `panel_count`.
governance_tier: full
---

# aigc 3-明细 / 1-分镜表现 / 分镜密度

## 概述

`分镜密度` 只负责一件事：

为每个分组决定应插入多少个 `[分镜N]`，以及这些分镜分别挂到哪些句段之前。

它不负责构图字段，不负责运镜，不负责光影，只负责：

1. `panel_count`
2. 句段切分
3. 密度理由

交付类型：`内容输出型`
## When to Use

- 需要先判断某一组是一镜到底、两镜对切，还是多镜爆发。
- 需要把一个分组内部的句段分配到 `[分镜1..N]`。
- 需要为后续 `分镜构图` 提供稳定数量输入。
## When Not to Use

- 已经确定每组几镜，只是缺静态镜头字段。
- 当前任务重点是构图风格、景别、景深，而不是切镜数量。
- 输入分组边界还没稳定。
## 核心约束（Mandatory）

- 工匠级契约继承：遵循 `skill-内容输出型/SKILL.md` 的反模板化与深度思考要求，本层不按固定镜数模板切组，而是按节奏、场景类型、信息负载与锚点证据裁决唯一 `panel_count`。
- Root-Cause 执行契约继承：一旦出现镜数塌缩、锚点缺失、范围超界或把后续构图职责提前吞掉，先按根 `AGENTS.md` 与本技能 `Root-Cause Execution Contract` 上溯规则源，再决定是否改正文。
- 自评偏差与缓解：LLM 容易把 `1帧` 当偷懒默认值，或把高能段和低能段平均切镜；执行时必须先完成三层密度裁决，再写句段锚点与功能位。
- 镜数合法域固定为 `1-15`；其中 `1帧` 仅允许由 `single_panel_long_take` 特例触发，绝不能作为普通低配默认值。
- `panel_count` 只能按“节奏给基础区间 -> 场景/时长/负载收窄 -> 候选整数离散定值”的三级渐进链收敛；禁止多个量化规则并列抢答。
- `rhythm / scene_type / group_duration / info_load` 负责决定 `panel_count`；`director_intent` 只能在合法 `refined_range` 内做偏置，模板门槛、反平庸门禁与集级去重只负责验收，不得前置夺权。
- 本层只裁决 `panel_count`、句段锚点与密度理由；若镜数未锁或越界到静态字段，应立即回退父级链路。
## Reference Modules (Mandatory)

`aigc 3-明细 / 1-分镜表现 / 分镜密度/SKILL.md` 只保留主合同、边界、门禁、回指和 Mermaid 摘要；专项细则以下列模块为真源：

- `references/chain-of-thought.md`
- `references/execution-flow.md`
- `references/type-strategies.md`
- `.agents/skills/aigc/3-明细/references/output-template.md`

硬规则：

1. 根 `SKILL.md` 仍是唯一主合同；`references/` 是模块化细则承载层，不是并行第二真源。
2. 若字段、流程、路由或输出契约需要升级，优先回写对应 `references/*.md`。
3. 主 `SKILL.md` 只保留摘要与回链，不重复展开长表格、长流程与长写位合同。
## Route Summary

- 当前技能的 VSM 变量、情况判定、策略映射与回退规则已下沉到 `references/type-strategies.md`。
- `references/type-strategies.md` 现承载 `1-15` 镜数域、三级渐进裁决、`single_panel_long_take` 证据门槛、无交集回退与职责边界。
- 主 `SKILL.md` 只保留入口边界与判路摘要，不再重复长表。
## Execution Summary

- canonical landing、共享运行时继承与完整 workflow 已下沉到 `references/execution-flow.md`。
- 主 `SKILL.md` 只保留阶段边界与执行摘要，不重复整段流程细则。
## Output Summary

- 输出内容模板统一继承父级 `.agents/skills/aigc/3-明细/references/output-template.md`，本技能不再定义本地 output-template 真源；局部写位与侧车规则继续由 `references/execution-flow.md` 与 `references/type-strategies.md` 承载。
- 输出层新增 `base_range / refined_range / candidate_counts / template_id / template_gate_verdict / aesthetic_peak_plan` 等摘要写位，并对 `panel_count=1` 强制要求特例说明。
- 主 `SKILL.md` 只保留输出职责摘要，不再重复整段模板正文。
## Field System Summary

- 字段主表、thought pass 与 pass table 已下沉到 `references/chain-of-thought.md`。
- 第三层裁决的 `Aesthetic Pressure Test`、`FAIL-COMPOSITION-FLATLINE` 与模板级 `FAIL-SBD-TEMPLATE-GATE` 也以字段失败码方式落在该模块，不在主合同重复展开。
- 主 `SKILL.md` 只保留字段系统摘要，不再重复长表。
## Root-Cause Execution Contract (Mandatory)

当出现以下症状时，必须先修本子技能合同：

- 同类场景总是被平均切成同样镜数
- 只给出镜数，没有锚点计划
- `1帧` 被滥用成默认偷懒值
- 高爆发段被压成低密度，或低能段被切得过碎

必经链路：

`Symptom -> Direct Technical Cause -> Rule Source -> Meta Rule Source -> Fix Landing Points`

优先检查：

- `Rule Source`
  - `.agents/skills/aigc/3-明细/subtypes/1-分镜表现/subtypes/分镜密度/SKILL.md`
  - `.agents/skills/aigc/3-明细/subtypes/1-分镜表现/subtypes/分镜密度/CONTEXT.md`
- `Meta Rule Source`
  - `.agents/skills/aigc/3-明细/subtypes/1-分镜表现/SKILL.md`
  - `.agents/skills/aigc/3-明细/SKILL.md`
  - 根 `AGENTS.md`
## SKILL / CONTEXT 分工（Mandatory）

- `SKILL.md` 锁定本层触发条件、唯一真源、执行顺序、写位边界与验收门槛。
- `CONTEXT.md` 沉淀失败类型、修复策略、成功 heuristic 与复用证据，不重写本层主合同。
- 经多轮验证稳定成立的经验，才允许从 `CONTEXT.md` 晋升回本 `SKILL.md` 或上层技能合同。
## Context Preload (Mandatory)

- 依次加载：
  - `.agents/skills/aigc/3-明细/SKILL.md + CONTEXT.md`
  - `.agents/skills/aigc/3-明细/subtypes/1-分镜表现/SKILL.md + CONTEXT.md`
  - 本 `SKILL.md + CONTEXT.md`
- 需要细化局部思维链、执行流、类型策略与输出模板时，继续加载本目录 `references/*.md`。
