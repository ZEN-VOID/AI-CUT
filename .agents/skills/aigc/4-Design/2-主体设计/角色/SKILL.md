---
name: aigc-design-role-design
description: Use when the `4-Design` stage needs parent-skill orchestration plus 角色设计组 subagents to turn role list, global guidance, director detail evidence, and init presets into structured role design carriers under `projects/aigc/<项目名>/4-Design/角色/2-设计/`.
governance_tier: full
---

# 4-Design / 2-角色 / 2-设计

## 概述

`2-设计` 是 `4-Design/角色` 下的角色设计父 skill，负责把 `1-清单` 已锁定的角色对象池继续收束成：

1. `character_design.json`
2. `第N集/[角色名].md`
3. `_manifest.json`

本轮重排遵循知行合一，但保持现有业务边界与输出机制不变：

- 第一输入根仍是 `1-清单/角色清单.json`
- 原“角色设计组”已收敛为本技能内的能力镜面命名，不再强依赖缺失的外置 team 文档
- 能力镜面仍只返回 `agents_plan + patch / note / report`
- 父 skill 仍独占 canonical writeback
- `_shared/IO_CONTRACT.md`、`1-主体清单/角色` 合同、模板与 project runtime layout 仍是共享真源

本技能额外锁定：

- `复杂链路的骨架 / 细则分层 = false`
- 因此业务分析、类型策略、思行节点、并行 tranche、汇流门、失败码与一次性输出合同都必须直接写在本 `SKILL.md`
- `references/` 仅保留迁移 stub，不再承载平行执行真源

交付类型：`内容输出型 + capability-governed`

## Skill / Capability Execution Rule (Mandatory)

在 `2-角色/2-设计` 中，分工固定为：

- 能力镜面负责思考、`agents_plan`、局部证据整理、字段候选与 `patch / note / report`
- skill 本身负责命中角色裁决、上下文装配、patch 收束、canonical 写回、review/audit 闭环与下游 handoff

这些能力镜面可以决定“本轮哪些角色先做、哪些字段先补、哪些冲突该上抛”，但不能替代 skill 完成阶段执行闭环。若未来恢复外置 agent/team 文档，它们只能作为本合同的派生执行投影。

## When to Use

- 已有 `projects/aigc/<项目名>/4-Design/角色/1-清单/第N集/角色清单.json`，需要继续生成角色设计稿。
- 需要把 `2-Global` 的项目级风格/类型/导演意图，与 `3-Detail/第N集.json` 的镜头证据合并为逐角色设计卡。
- 需要为后续 `3-面板`、`5-Image` 或角色多视图生图提供稳定的结构化角色设计 carrier。

## When Not to Use

- 当前还没有 `1-清单` 的角色对象池，应先回到 `4-Design/角色/1-清单`。
- 当前任务是补 `3-Detail/第N集.json` 的镜头事实，应回到 `3-Detail`。
- 当前任务是直接出图、做面板或视频请求，应进入 `3-面板`、`5-Image` 或 `6-Video`。

## Business Requirement Analysis Contract (Mandatory)

| analysis_slot | 当前结论 |
| --- | --- |
| `business_goal` | 把角色对象池、全局风格和镜头证据压成可持续复用的角色结构化设计稿 |
| `business_object` | `角色清单.json` 中的角色 identity、`2-Global` 的风格/类型元素、`3-Detail` 的镜头证据、初始化项目约束 |
| `constraint_profile` | 不跳过对象池、不让 subagents 直接写 canonical 文件、不越权替代场景/道具或面板/生图阶段 |
| `success_criteria` | 命中角色范围清晰、视觉锚点稳定、specialist patch 可聚合、review/audit 可回溯、`character_design.json + Markdown + manifest` 同源 |
| `non_goals` | 不回写 `1-清单`、不直接出图、不直接写角色面板 packet、不把角色设计组扩张成跨模块常驻团队 |
| `complexity_source` | 角色批次裁决、上下文剪裁、视觉锚点先行、specialist 并行 patch 汇流、review/audit 返工、增量写回 |
| `topology_fit` | 前段串行锁角色范围与 context packet，中段 `形象建模 -> 三 specialist 并行`，后段统一 review、audit 与 writeback 汇流 |
| `step_strategy` | 采用“串行主干 + 并行 specialist tranche + 单写回汇流”的父 skill 思行网络 |

## Context Preload (Mandatory)

加载顺序固定为：

1. 根 `AGENTS.md`
2. `.agents/skills/aigc/SKILL.md + CONTEXT.md`
3. `.agents/skills/aigc/4-Design/SKILL.md + CONTEXT.md`
4. `.agents/skills/aigc/4-Design/2-主体设计/SKILL.md + CONTEXT.md`
5. `.agents/skills/aigc/3-Detail/SKILL.md + CONTEXT.md`
6. `.agents/skills/aigc/4-Design/1-主体清单/_shared/detail-output-consumption-contract.md`
7. `.agents/skills/aigc/4-Design/1-主体清单/角色/SKILL.md + CONTEXT.md`
8. 本 `SKILL.md + CONTEXT.md`
9. `.agents/skills/aigc/_shared/project-runtime-layout.md`
10. `.agents/skills/aigc/4-Design/2-主体设计/角色/_shared/IO_CONTRACT.md`
11. `projects/aigc/<项目名>/0-Init/north_star.yaml`
12. `projects/aigc/<项目名>/0-Init/init_handoff.yaml`
13. `projects/aigc/<项目名>/2-Global/全局风格/全局风格设计.md`
14. `projects/aigc/<项目名>/2-Global/类型元素.md`
15. `projects/aigc/<项目名>/3-Detail/第N集.json` 中命中分组的 `组间设计.导演意图`
16. `projects/aigc/<项目名>/4-Design/角色/1-清单/第N集/角色清单.json`
17. `projects/aigc/<项目名>/3-Detail/第N集.json`
18. `projects/aigc/<项目名>/4-Design/场景/1-清单/第N集/场景清单.json`（若存在）
19. `projects/aigc/<项目名>/4-Design/道具/1-清单/第N集/prop_design_bridge.json`（若存在）
20. `projects/aigc/<项目名>/4-Design/角色/2-设计/第N集/*`（若存在）

## Shared Canonical Sources (Mandatory)

- 强制读取：`.agents/skills/aigc/4-Design/2-主体设计/角色/_shared/IO_CONTRACT.md`
- 强制读取：`.agents/skills/aigc/_shared/project-runtime-layout.md`
- 强制读取：`.agents/skills/aigc/4-Design/1-主体清单/_shared/detail-output-consumption-contract.md`
- 强制读取：`.agents/skills/aigc/4-Design/1-主体清单/角色/SKILL.md`
- 强制读取：`templates/角色设计卡.template.md`

硬规则：

1. 第一输入根固定为 `1-清单/角色清单.json`
2. `character_design.json` 是本阶段唯一 machine-first 真源
3. 能力镜面只能返回 `agents_plan + patch / note / report`
4. 场景/道具清单只作为只读上下文包，不得扩成角色设计组新常驻职责
5. 本阶段不得创建角色面板、图片或视频请求

## Total Input Contract

### 必需输入

- `projects/aigc/<项目名>/4-Design/角色/1-清单/第N集/角色清单.json`
- `projects/aigc/<项目名>/3-Detail/第N集.json`
- `projects/aigc/<项目名>/0-Init/north_star.yaml`
- `projects/aigc/<项目名>/0-Init/init_handoff.yaml`
- `projects/aigc/<项目名>/2-Global/全局风格/全局风格设计.md`
- `projects/aigc/<项目名>/2-Global/类型元素.md`

### 可选输入

- `projects/aigc/<项目名>/编导/第N集.json`
  - 用户显式给 legacy 路径时的兼容回退
- `projects/aigc/<项目名>/3-Detail/第N集.json` 中命中分组的 `组间设计.导演意图`
  - 当前项目没有单独平铺的 `2-Global/导演意图.md` 时，默认从 detail 根文件消费导演指导
- `projects/aigc/<项目名>/4-Design/场景/1-清单/第N集/场景清单.json`
- `projects/aigc/<项目名>/4-Design/道具/1-清单/第N集/prop_design_bridge.json`
- `projects/aigc/<项目名>/4-Design/角色/2-设计/第N集/*`
  - 已有角色设计稿，用于增量 patch
- 用户显式指定的 `selected_roles[]` 或局部设计维度

### 禁止输入

- 跳过 `角色清单.json` 直接从导演 JSON 发明角色设计结论
- 旧仓 `output/影片/.../3-设定/2-设计` 下的平行角色设计主稿
- 要求本阶段直接产出角色面板或直接出图的越权指令

## Visual Maps

```mermaid
flowchart TD
    A["读取 1-清单/角色清单.json"] --> B["装配 Init + 2-Global + 3-Detail 上下文"]
    B --> C["父 skill 锁定 selected_roles + selected_agents"]
    C --> D["设计统筹: 批次 / 优先级 / 返工入口"]
    D --> E["形象建模: visual_anchor"]
    E --> F["服装设计"]
    E --> G["妆容设计"]
    E --> H["个性塑造"]
    F --> I["角色一致性复核"]
    G --> I
    H --> I
    I --> J["真源审计"]
    J --> K["父 skill 聚合写回 JSON + Markdown + manifest"]
```

```mermaid
flowchart LR
    A["父 skill"] --> B{{"默认 mixed tranche"}}
    B --> C["T1: 设计统筹"]
    B --> D["T2: 形象建模"]
    B --> E["T3: 服装 / 妆容 / 个性 并行"]
    B --> F["T4: review -> audit -> writeback"]
    C --> G["agents_plan + patch / note / report"]
    D --> G
    E --> G
    F --> H["canonical outputs"]
```

```mermaid
stateDiagram-v2
    [*] --> IntakeLocked
    IntakeLocked --> Routed
    Routed --> ContextAssembled
    ContextAssembled --> Planned
    Planned --> Anchored
    Anchored --> SpecialistRunning
    SpecialistRunning --> Reviewed
    Reviewed --> Audited
    Audited --> Finalized
    Audited --> Blocked
    Blocked --> Planned
    Blocked --> Anchored
```

```mermaid
graph LR
    A["角色清单.json"] --> B["FIELD-ROLE-DESIGN-02 角色路由"]
    B --> C["FIELD-ROLE-DESIGN-03 视觉锚点"]
    C --> D["FIELD-ROLE-DESIGN-04 specialist patch"]
    D --> E["FIELD-ROLE-DESIGN-05 一致性复核"]
    E --> F["FIELD-ROLE-DESIGN-06 canonical carrier"]
    F --> G["FIELD-ROLE-DESIGN-07 聚合写回"]
    G --> H["FIELD-ROLE-DESIGN-08 审计闭环"]
```

## Internal Capability Recomposition (Mandatory)

当前唯一执行真源在本 `SKILL.md`，以下名称保留为能力镜面，而不是外置 team 文档依赖：

- `设计统筹`
- `形象建模`
- `服装设计`
- `妆容设计`
- `个性塑造`
- `角色一致性复核`
- `真源审计`

### 父 skill 拥有

- `selected_roles[]`、`selected_agents[]` 与 tranche 决策
- 全局上下文裁剪与 `context_packet_*` 装配
- `character_design.json`、逐角色 Markdown、`_manifest.json` 的最终写回权
- 对已有角色设计稿做增量 patch 的裁决权
- `validation-report` 与下游 `3-面板 / 5-Image` 回接说明

### 能力镜面拥有

- 专门化分析与角色化判断
- `agents_plan + patch / note / report`
- 当前角色范围内的局部证据与阻塞报告

### 能力镜面不拥有

- 直接写回 `projects/aigc/<项目名>/4-Design/角色/2-设计/第N集/*`
- 为未命中的角色补占位内容
- 越权改写 `1-清单` 的角色 canonical identity
- 越权创建角色面板、图片或视频请求

## Topology Contract (Mandatory)

### Topology Fit

本技能采用 `串行主干 + 并行 specialist tranche + 单写回汇流`：

1. 串行主干
   - 锁输入与角色范围
   - 组装 context packet
   - 运行 `设计统筹`
   - 运行 `形象建模`
2. 并行 tranche
   - `服装设计`
   - `妆容设计`
   - `个性塑造`
3. 汇流门
   - `角色一致性复核`
   - `真源审计`
   - 父 skill 聚合写回

### Route Priority (Mandatory)

`用户显式指定角色/维度 > 设计统筹批次裁决 > role_tier 默认策略`

解释：

1. 用户只要求某个角色、某个维度或某个服装状态时，优先命中该局部路径
2. 用户未指定时，由 `设计统筹` 先裁决 `selected_roles[]`、`selected_agents[]` 与返工入口
3. 若仍无强约束，再由 `role_tier` 和 `world_mode` 决定 specialist 深度

### Variable Register

| var_id | 观测信号 | 状态集合 | 检测方法 | 优先级 |
| --- | --- | --- | --- | --- |
| `V-ROLE-SCOPE` | 当前命中角色范围 | `single/batch/all/unknown` | 读取用户约束与 `角色清单.json` | P0 |
| `V-ROLE-TIER` | 角色层级 | `lead/support/featured-crowd/crowd` | 读取 `roles[].role_level` | P0 |
| `V-WORLD-MODE` | 世界观风格类型 | `historical/modern/fantasy/stylized/hybrid` | 读取 `north_star + 类型元素` | P1 |
| `V-STYLE-CONVERGENCE` | 项目级角色气质收敛状态 | `stable/drifting/blocked` | 对读 `north_star + 全局风格 + 类型元素 + 导演意图` | P0 |
| `V-PATCH-MODE` | 当前是新建还是增量更新 | `fresh/incremental` | 检查既有 `第N集/*` 输出 | P0 |
| `V-EVIDENCE-GAP` | 证据完整度 | `full/partial/blocked` | 检查 `group_id + shot_id + source_file` 与 style context | P0 |
| `V-ATTRIBUTE-CERTAINTY` | 角色基础属性确定度 | `explicit/inferred/conservative` | 汇总 `角色清单 + 3-Detail + 角色研究/bridge` | P0 |
| `V-PHOTO-CONTRACT` | 角色主体摄影合同 | `default-portrait/custom/blocked` | 检查用户显式要求与导演证据，否则走默认 portrait 合同 | P1 |

### Role Tier Strategy

| role_tier | 设计深度 | 默认 specialist | 说明 |
| --- | --- | --- | --- |
| `lead` | full | 全部 | 主角必须完整输出全部槽位 |
| `support` | high | 全部 | 配角可精简辅助字段，但视觉锚点与穿搭系统不能缺 |
| `featured-crowd` | medium | `形象建模 + 服装设计 + 个性塑造` | 有辨识要求的群像角色可弱化妆容颗粒度 |
| `crowd` | lite | `设计统筹 + 形象建模 + 服装设计` | 纯群演只保留识别锚点、阶层穿搭与禁区 |

### World Mode Strategy

| world_mode | 重点 | 约束 |
| --- | --- | --- |
| `historical` | 制式、材质、阶层、文化痕迹 | 禁止现代时装语言偷渡 |
| `modern` | 职业、生活方式、现实可穿性 | 避免过度奇观化 |
| `fantasy` | 世界观符号、辨识度、视觉夸张度 | 仍需保留角色 identity 与 evidence anchor |
| `stylized` | 轮廓、色块、角色气场 | 避免只剩空泛风格词 |
| `hybrid` | 混合参考需显式说明主导风格 | 避免冲突风格无裁决 |

### Conflict Tie-Break

1. `角色清单.json` 的 canonical identity 优先
2. `2-Global` 的项目级风格与类型元素高于单次镜头修辞
3. `3-Detail/第N集.json` 的镜头证据高于设计组臆测
4. `casting_reference` 只作为具象化代理，不得压过 canonical identity 与镜头证据
5. 若两条证据冲突，优先保守设计，并在 `report` 说明

### Photography Default Contract

1. 角色主体画面默认写法固定为：`竖版 9:16 / 纯黑背景 / 自然站姿 / 单人 / 无多视图`。
2. 仅当用户显式要求，或 `3-Detail / 导演链` 对角色主体画面给出不可忽视的刚性约束时，才允许覆盖该默认合同。
3. 摄影字段只服务角色设计可执行性，不得越权扩写镜头调度、场面调度、运动设计或导演分镜判断。
4. 若景别与机位证据不足，使用保守默认，不得编造动态镜头语言。

## Thinking-Action Node Contract (Mandatory)

每个关键节点必须同时描述判断与动作，至少覆盖以下槽位：

| slot | 要求 |
| --- | --- |
| `node_id` | 稳定节点标识 |
| `objective` | 该节点要解决的判断/动作目标 |
| `inputs` | 进入该节点的输入与依赖 |
| `actions` | 该节点真正执行的动作 |
| `evidence` | 该节点留下的证据、产物或验证结果 |
| `route_out` | 成功、失败、分支时分别流向何处 |
| `gate` | 是否允许进入最终输出汇流 |

## Thinking-Action Node Network

| node_id | 对应 Step | 聚焦字段 | objective | actions | evidence | route_out | gate |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `N1-INTAKE-LOCK` | S1 | `FIELD-ROLE-DESIGN-01` | 锁定当前确属 `2-设计` 问题而非前后游问题，并先判定本轮是主角聚焦、配角聚焦还是混合批次输出 | 读取 `角色清单.json`、检测前序真源是否齐备、确认 episode 目录，并回答“这次任务命中哪些角色层级、它们在剧情中承担什么职责” | 输入清单、phase verdict、role-scope verdict | 成功 -> `N2`；缺前序真源 -> 回 `1-清单` | 阶段边界与主体职责明确后方可继续 |
| `N2-ROLE-ROUTE` | S2 | `FIELD-ROLE-DESIGN-02` | 锁定本轮 `selected_roles[]`、`selected_agents[]`、输出顺序与角色层级是否稳定 | 结合用户约束、`设计统筹` 前置信号和 role_tier 做批次裁决，并先判定“本集到底哪些角色要输出” | role dispatch note、selected_roles、role_order draft | 成功 -> `N3`；角色范围不清或顺序漂移 -> 回 `S2` | 角色范围与输出顺序唯一后方可派发 |
| `N3-CONTEXT-PACKET` | S3 | `FIELD-ROLE-DESIGN-02` | 为父 skill 与能力镜面裁剪最小充分上下文，并读取全局风格源，锁定角色设计的视觉收敛方向 | 组装 `mission_brief_role_design`、`context_packet_*`、既有输出增量基线，判定项目级全局风格基调，并额外回答“该角色应朝哪里收敛、哪些泛化风格词不能直接拿来冒充设计实现” | context packets、patch mode 结论、style convergence note、role style note | 成功 -> `N4`；证据缺口或风格漂移 -> 回 `S1-S3` | 上下文、角色视觉收敛方向与禁用泛化风格词充分后方可进入设计 |
| `N4-DISPATCH-PLAN` | S4 | `FIELD-ROLE-DESIGN-02` | 用 `设计统筹` 锁角色批次、优先级、层级稳定性与返工入口 | 调度 `设计统筹`，收 `agents_plan + patch / note / report`，明确本轮输出顺序、角色层级与跳过原因 | `plan_patch_设计统筹` | 成功 -> `N5`；批次冲突或层级不稳 -> 回 `S2-S4` | 计划明确后方可建锚点 |
| `N5-VISUAL-ANCHOR` | S5 | `FIELD-ROLE-DESIGN-03` | 先为每个命中对象建立统一视觉锚点，并锁定最合适的作品参照而不是泛化风格词 | 调度 `形象建模`，生成 `visual_anchor / face_signature / body_signature / silhouette_signature / casting_reference / feature_markers / signature_elements`；其中 `casting_reference` 仅作第一联想演员代理，必须转译成可落盘的特征与元素，同时补出 `design_inspiration` 与“为什么是这个作品参照，而不是泛化风格词”的判断 | `artifact_patch_形象建模`、reference rationale note | 成功 -> `N5B`；锚点不稳、参照失焦或演员联想无法转译 -> 回 `S5` | specialist 必须围绕统一锚点、同一组 `feature_markers / signature_elements` 与唯一作品参照工作 |
| `N5B-STRUCTURED-LOCK` | S5 | `FIELD-ROLE-DESIGN-03` `FIELD-ROLE-DESIGN-04` | 把主锚点转成可建模、可复审、可返工的结构拆解、参照转译、误读剪枝与摄影合同 | 围绕 `物语` 主锚点锁定 `story_premise / reasoning_pivot / structured_fields`；概括时期、身份、景别、外部参照与禁忌误读；把基础属性区分为 `explicit / inferred / conservative`；把作品参照转译成当前项目的设计实现点而不是复述参照名；补出最该提前剪掉的误读；把结构字段压成可建模、可复审、可返工的参数表；在无更强证据时固定 `竖版 9:16 / 纯黑背景 / 自然站姿 / 单人 / 无多视图` | structured lock note、reference translation note、misread guardrail note、attribute certainty map、photo contract note | 成功 -> `N6A/N6B/N6C`；属性不稳、误读风险过高、参照未转译或摄影合同越界 -> 回 `S5` | 只有结构拆解、参照转译、误读剪枝、保守标记与摄影默认合同都锁定后才允许进入 specialist 并行 |
| `N6A-WARDROBE` | S6 | `FIELD-ROLE-DESIGN-04` | 生成服装系统、材质、配色、文化元素、穿着细节与状态变体，并让身形与服装共同定义角色轮廓与社会属性 | 调度 `服装设计`，基于 `visual_anchor + body_signature + signature_elements + structured_fields` 返回局部 wardrobe patch，显式概括制式、材质、文化元素、配色、细节与社会属性 | `artifact_patch_服装设计` | 成功 -> `N7`；服装冲突或轮廓失真 -> 回 `S6` | 只允许返回局部 patch，且不得背离既定标志性元素与社会属性 |
| `N6B-MAKEUP` | S6 | `FIELD-ROLE-DESIGN-04` | 生成妆面、发型、发饰、肤质和镜头可读性方案，并维护脸部辨识特征与时代/阶层/身份识别 | 调度 `妆容设计`，基于 `face_signature + feature_markers + structured_fields` 返回 makeup patch，细化五官/骨相、发型与发饰的执行字段 | `artifact_patch_妆容设计` | 成功 -> `N7`；年龄感、时代感或镜头冲突 -> 回 `S6` | 只允许返回局部 patch，且不得抹平关键辨识特征或把缺证据字段写成确定事实 |
| `N6C-PERSONA` | S6 | `FIELD-ROLE-DESIGN-04` | 生成人物气场、姿态、情绪锚点和行为特征，并把具象参照转写成可见表演感 | 调度 `个性塑造`，基于 `casting_reference + feature_markers + signature_elements` 返回 personality patch | `artifact_patch_个性塑造` | 成功 -> `N7`；人设冲突或表演感漂移 -> 回 `S6` | 只允许返回局部 patch，且不得把演员联想直接当成角色定稿 |
| `N7-CONSISTENCY-REVIEW` | S7 | `FIELD-ROLE-DESIGN-05` | 检查跨字段、跨角色、跨场景兼容性，并确认所有 specialist 仍收束在同一个具象方向上，且镜头服务主体而非悬空 | 调度 `角色一致性复核`，指出冲突字段、演员联想漂移、特征丢失、保守标记误写、参照转译失真、误读剪枝不足与摄影合同越界的返工入口；额外检查镜头字段是否真的服务主体展示，而不是把构图/摄影写成悬空装饰语 | `review_note_角色一致性` | pass -> `N8`；fail -> 回 `S5-S7` | review 不通过不得写回 |
| `N8-AUDIT-WRITEBACK` | S8 | `FIELD-ROLE-DESIGN-06` `FIELD-ROLE-DESIGN-07` `FIELD-ROLE-DESIGN-08` | 检查真源、路径、越权、证据并统一写回 canonical 产物 | 调度 `真源审计`，父 skill 聚合 patch，写回 JSON / Markdown / manifest，并给下游 handoff | canonical outputs、audit report、handoff note | pass -> Final；fail -> 回对应节点 | 仅父 skill 可写回，且通过 audit 后才允许结案 |

## Node Augmentation Coverage (Mandatory)

| 增补判断点 | 当前落点 | 执行动作 |
| --- | --- | --- |
| 这次任务命中的是主角、配角还是混合批次，它们在剧情中承担什么职责 | `N1` | 先做角色职责判型，再决定后续模板如何收束 |
| 本集到底有哪些角色需要输出，顺序与层级是否稳定 | `N2 + N4` | 锁 `selected_roles[]`、输出顺序、role tier 与跳过原因 |
| 读取全局风格源，完成角色视觉收敛适配，并锁定该角色应朝哪里收敛 | `N3` | 在 `style convergence` 外，补出 `role style note` 与禁用泛化风格词 |
| 该角色最适合借哪一个作品参照，而不是泛化风格词 | `N5` | 为主锚点补 `design_inspiration` 与参照选择理由 |
| 参照如何转译成当前项目的设计实现，而不是复述参照名；同时最该提前剪掉什么误读 | `N5B` | 写入 `reference translation note + misread guardrail note` |
| 角色的时期、身份、景别、外部参照与禁忌误读应如何概括 | `N5B` | 写入 `story_premise / reasoning_pivot / design_guardrails` |
| 道具怎样写到可建模、可复审、可返工 | `N5B` | 把结构拆解压成参数表与返工友好字段，而不是停留在修辞描述 |
| 镜头如何服务道具，而不是让构图摄影悬空 | `N5B + N7` | 先锁 `photo_contract`，再由 reviewer 复核镜头字段是否真正服务主体 |
| 基础属性中哪些可确定，哪些必须保守标记 | `N5B` | 为基础属性打 `explicit / inferred / conservative` 标记 |
| 如何把面部摘要拆成可执行的五官与骨相字段 | `N5B + N6B` | 先锁字段骨架，再由妆容设计细化 |
| 发型与发饰如何服务时代感、阶层感与身份识别 | `N6B` | 在发型/发饰层写时代、阶层、身份识别作用 |
| 身形与服装如何共同定义角色轮廓与社会属性 | `N5 + N6A` | 用 body anchor + wardrobe patch 共同定轮廓与社会属性 |
| 角色主体画面应如何拍，既可执行又不越导演阶段边界 | `N5B` | 默认 `竖版 9:16 / 纯黑背景 / 自然站姿 / 单人 / 无多视图` |
| 种族 / 年龄 / 性别 / 肤色 是否证据明确、缺项处理规范 | `N5B` | 缺项只做保守标记，不伪造确定事实 |
| 体形 / 身高 / 体重 是否形成明确主体轮廓 | `N5B + N6A` | 先判主体轮廓是否稳定，再写服装放大点 |
| 制式、材质、文化元素、配色、细节是否形成当前项目实现点 | `N6A` | 服装节点必须给出当前项目可执行的实现点 |

## Convergence Contract (Mandatory)

只有同时满足以下条件，`2-设计` 才允许宣布完成：

1. `FIELD-ROLE-DESIGN-01` 到 `FIELD-ROLE-DESIGN-08` 全部已落位
2. `selected_roles[]`、`selected_agents[]` 与 tranche 路由清晰
3. 每个命中角色已有稳定 `visual_anchor`，且 `casting_reference / feature_markers / signature_elements` 已转成可消费锚点
4. `story_premise / reasoning_pivot / structured_fields.attribute_certainty / structured_fields.photo_contract` 已锁定，且缺项按保守标记处理
5. specialist patch 可被 review 汇流，不存在未裁决冲突
6. `character_design.json + [角色名].md + _manifest.json` 同源且只覆盖命中角色
7. `真源审计` 未给出 veto，且 evidence lineage 完整

若未满足：

- 角色范围问题 -> 回到 `N2-ROLE-ROUTE`
- 上下文缺口问题 -> 回到 `N3-CONTEXT-PACKET`
- 视觉锚点问题 -> 回到 `N5-VISUAL-ANCHOR`
- 结构拆解 / 保守标记 / 摄影合同问题 -> 回到 `N5B-STRUCTURED-LOCK`
- specialist 冲突问题 -> 回到 `N6A/N6B/N6C`
- review/audit 问题 -> 回到 `N7` 或 `N8`

## One-Shot Output Contract (Mandatory)

`2-设计` 的一次性输出不是多个 specialist 平行主稿，而是同一 bundle 内的四类 canonical 结果：

### A. `character_design.json`（Mandatory）

默认路径：

`projects/aigc/<项目名>/4-Design/角色/2-设计/第N集/character_design.json`

最低字段：

- `meta`
  - `project_name`
  - `episode_id`
  - `source_role_list`
  - `source_episode_detail`
  - `skill_id`
  - `generated_at`
- `roles[]`
  - `role_id`
  - `canonical_name`
  - `role_tier`
  - `biography`
  - `story_premise`
  - `reasoning_pivot`
  - `costume_state`
  - `visual_anchor`
  - `casting_reference`
  - `feature_markers`
  - `signature_elements`
  - `wardrobe_profile`
  - `makeup_profile`
  - `personality_profile`
  - `scene_compatibility`
  - `prop_compatibility`
  - `variation_rules`
  - `negative_constraints`
  - `structured_fields`
  - `prompt_integration`
  - `evidence`
  - `structured_markdown_path`

### B. 逐角色 Markdown（Mandatory）

默认路径：

`projects/aigc/<项目名>/4-Design/角色/2-设计/第N集/[角色名].md`

必须使用 `templates/角色设计卡.template.md`，最低包含：

1. `物语`
2. `解构`
3. `prompt整合`

补充边界：

- 逐角色 Markdown 当前按用户指定使用 `prop_*` 英文字段名作为展示投影。
- 该投影层不改 `character_design.json` 作为 machine-first 真源的字段命名；如需取值，应从 `roles[]` 及其 `structured_fields` 做映射，而不是反向重命名 canonical carrier。

生成硬规则：

1. `物语`
   - 标题固定为 `# [prop_name_en]`，按用户指定使用 prop-style 命名。
   - 必须先内化上游 `角色研究.json / role_design_bridge.json / 同集导演链` 的主体线索。
   - 优先直接继承 `biography`；仅在缺失时，才允许基于 bridge 与研究稿生成保守 fallback。
   - 默认输出中文文学正文，长度控制在 `150-300` 字，承担“主体线索内化成文学性物语”的职责。
   - 证据锚点保留在 `character_design.json.roles[].structured_fields` 的机器侧，不得把检索摘要直接铺在正文首段。
2. `解构`
   - 首行固定输出 `Reasoning Pivot: [reasoning_pivot_en]`。
   - 必须显式采用 `## Photography ##` 与 `## Prop Design ##` 两段参数表。
   - `Photography` 只能输出 `Type / Shot Size / Background`。
   - `Prop Design` 必须按以下顺序落位：`Style Backbone / Prop Type / Design Inspiration / Period Attribute / Functionality / Shape Sense / Line Sense / Dimensional Layering / Size / Material Detail / Texture Detail / Decoration Detail / Pattern Detail / Art Elements / Cultural Elements / Ergonomics`。
   - 必须围绕“已有线索资料 + 物语形成的主锚点”做理性拆解，不得退回旧的分散小节拼盘。
3. `prompt整合`
   - 必须输出可直接喂给生图模型的最终整合 prompt。
   - 默认英文；仅在用户显式指定时切换中文。
   - 必须显式消费 `story_narrative + reasoning_pivot_en + 解构参数表`，并与 `物语 + 解构` 联合蒸馏。
   - 输出应是自然衔接的短语串，使用 `,` 分隔，避免冗余。
   - 内容控制在 `<=1300` 英文单词内，并在尾段并入全局风格引用。

### C. `_manifest.json`（Mandatory）

默认路径：

`projects/aigc/<项目名>/4-Design/角色/2-设计/第N集/_manifest.json`

最低字段：

- `episode_id`
- `selected_roles`
- `source_inputs`
- `output_files`
- `selected_agents`
- `review_status`
- `audit_status`

### D. 父级 handoff note（Mandatory）

本技能返回给 `2-角色` 或下游阶段的最小闭环说明必须包含：

- `selected_roles`
- `patch_mode`
- `review_status`
- `audit_status`
- `next_recommended_entry`
- `blocking_notes`

## Field Master

| field_id | 输出位置/字段 | 内容要求 | 默认责任 Step | 质量维度 | 失败码 |
| --- | --- | --- | --- | --- | --- |
| `FIELD-ROLE-DESIGN-01` | 阶段定位 | 明确 `2-设计` 消费 `1-清单`，负责结构化角色设计，不越权做面板/出图 | S1 | 边界清晰度 | `FAIL-ROLE-DESIGN-01` |
| `FIELD-ROLE-DESIGN-02` | 角色路由 | 明确 `selected_roles[]`、`selected_agents[]` 与 mixed tranche | S2-S4 | 路由完整性 | `FAIL-ROLE-DESIGN-02` |
| `FIELD-ROLE-DESIGN-03` | 视觉锚点 | 每个命中角色都有稳定 `visual_anchor / face_signature / body_signature / casting_reference / feature_markers / signature_elements`，并已锁定 `story_premise / reasoning_pivot / structured_fields.attribute_certainty / structured_fields.photo_contract / design_guardrails` | S5 | 角色锚点稳定性 | `FAIL-ROLE-DESIGN-03` |
| `FIELD-ROLE-DESIGN-04` | specialist patch | `wardrobe_profile / makeup_profile / personality_profile / variation_rules` 完整可聚合，且能落到五官/骨相/发型/服装实现点 | S6 | 设计颗粒度 | `FAIL-ROLE-DESIGN-04` |
| `FIELD-ROLE-DESIGN-05` | 一致性复核 | 跨字段、跨角色、跨场景兼容性被 review，不互相打架 | S7 | 设计一致性 | `FAIL-ROLE-DESIGN-05` |
| `FIELD-ROLE-DESIGN-06` | canonical carrier | `character_design.json + 逐角色 Markdown + _manifest.json` 同源且命名稳定 | S8 | 输出完整性 | `FAIL-ROLE-DESIGN-06` |
| `FIELD-ROLE-DESIGN-07` | 聚合写回 | 父 skill 独占写回，未命中角色不被覆盖 | S8 | 聚合可执行性 | `FAIL-ROLE-DESIGN-07` |
| `FIELD-ROLE-DESIGN-08` | 审计闭环 | 返回 triad closure、阻塞说明与下游回接 | S8 | 闭环完整性 | `FAIL-ROLE-DESIGN-08` |

## Thought Pass Map

| step_id | 聚焦字段 | 核心问题 | 生成动作 | 未达标信号 |
| --- | --- | --- | --- | --- |
| S1 | `FIELD-ROLE-DESIGN-01` | 当前是不是 `2-设计` 问题 | 锁定阶段边界与前后游停点 | 跳过 `1-清单` 直接设计 |
| S2 | `FIELD-ROLE-DESIGN-02` | 本轮要设计哪些角色 | 锁定 `selected_roles[]` 与角色范围 | 多角色并列但没有命中规则 |
| S3 | `FIELD-ROLE-DESIGN-02` | 当前上下文是否足够派发 | 生成 `mission_brief` 与 `context_packet_*` | 证据不足仍强行派发 |
| S4 | `FIELD-ROLE-DESIGN-02` | 设计统筹是否已给出批次和返工入口 | 收 `plan_patch_设计统筹` | 没有批次、优先级或返工说明 |
| S5 | `FIELD-ROLE-DESIGN-03` | 视觉锚点、结构拆解与摄影默认合同是否稳定且可具象化 | 生成 `visual_anchor / face_signature / body_signature / casting_reference / feature_markers / signature_elements / story_premise / reasoning_pivot / structured_fields` | specialist 没有统一锚点，或演员联想/基础属性/摄影合同没有被转成可执行字段 |
| S6 | `FIELD-ROLE-DESIGN-04` | 三条 specialist patch 是否各归其位 | 收服装、妆容、个性 patch，并检查五官/骨相、发型/发饰、轮廓/服装实现点 | patch 互相污染、缺字段或把保守项写成确定事实 |
| S7 | `FIELD-ROLE-DESIGN-05` | 设计是否一致可汇流 | 做 reviewer 复核与返工判断 | 强行拼成冲突人设 |
| S8 | `FIELD-ROLE-DESIGN-06` `FIELD-ROLE-DESIGN-07` `FIELD-ROLE-DESIGN-08` | canonical 输出与闭环是否稳定 | audit + writeback + handoff | 只有文采，没有 machine-first carrier 或审计闭环 |

## Pass Table

| field_id | Pass Standard | Fail Code | Rework Entry |
| --- | --- | --- | --- |
| `FIELD-ROLE-DESIGN-01` | 阶段边界、父子职责与输出真源明确 | `FAIL-ROLE-DESIGN-01` | S1 |
| `FIELD-ROLE-DESIGN-02` | 角色路由、顺序与单点直达规则明确 | `FAIL-ROLE-DESIGN-02` | S2-S4 |
| `FIELD-ROLE-DESIGN-03` | 每个命中角色有稳定视觉锚点，且具备可消费的具象参照 | `FAIL-ROLE-DESIGN-03` | S5 |
| `FIELD-ROLE-DESIGN-04` | specialist patch 颗粒度清晰且不越权 | `FAIL-ROLE-DESIGN-04` | S6 |
| `FIELD-ROLE-DESIGN-05` | reviewer 能指出跨字段冲突与返工入口 | `FAIL-ROLE-DESIGN-05` | S7 |
| `FIELD-ROLE-DESIGN-06` | JSON / Markdown / manifest 同源且字段完整 | `FAIL-ROLE-DESIGN-06` | S8 |
| `FIELD-ROLE-DESIGN-07` | 父 skill 独占写回，agents 只返 `agents_plan + patch / note / report` | `FAIL-ROLE-DESIGN-07` | S8 |
| `FIELD-ROLE-DESIGN-08` | 返回 triad closure、阻塞说明与下游回接 | `FAIL-ROLE-DESIGN-08` | S8 |

## Root-Cause Execution Contract (Mandatory)

当 `2-设计` 出现以下问题时，必须先修源层而不是补单次角色文案：

- `2-设计` 跳过 `1-清单`，直接从 `3-Detail/第N集.json` 发明人设
- 四个 specialist 各自输出一整套角色稿，父 skill 无法收束
- 角色设计看起来完整，但没有 `evidence[]`、`shot_id` 或 `group_id` 回链
- 设计内容吞掉场景或道具职责，出现跨模块越权
- canonical 输出只剩 Markdown，没有 machine-first JSON carrier
- 主 `SKILL.md` 已改成知行合一，但目录里仍让 `references/` 承载并列步骤真源

必经链路：

`Symptom -> Direct Technical Cause -> Rule Source -> Meta Rule Source -> Fix Landing Points`

优先检查：

- `Rule Source`
  - `.agents/skills/aigc/4-Design/2-主体设计/角色/SKILL.md`
  - `.agents/skills/aigc/4-Design/2-主体设计/角色/CONTEXT.md`
  - `.agents/skills/aigc/4-Design/2-主体设计/角色/_shared/IO_CONTRACT.md`
  - `.agents/skills/aigc/4-Design/1-主体清单/角色/SKILL.md`
  - `.agents/skills/aigc/4-Design/1-主体清单/_shared/detail-output-consumption-contract.md`
- `Meta Rule Source`
  - `.agents/skills/aigc/3-Detail/SKILL.md`
  - `.agents/skills/aigc/SKILL.md`
  - 根 `AGENTS.md`
  - `/Users/vincentlee/.codex/skills/meta/构建/技能/skill-知行合一/SKILL.md`
  - `/Users/vincentlee/.codex/skills/meta/构建/技能/skill-知行合一/SKILL.md`

面向用户的闭环固定返回：

1. root cause location
2. immediate fix
3. systemic prevention fix

## Completion Criteria

- 已锁定唯一输入根、唯一输出根和唯一 writeback owner
- 已完成 `设计统筹 -> 形象建模 -> specialist 并行 -> review -> audit -> writeback`
- 已生成 `character_design.json + [角色名].md + _manifest.json`
- 已给出 triad closure 与下游推荐入口
- 未命中角色未被覆盖或补空模板
