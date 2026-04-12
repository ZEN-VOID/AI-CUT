---
name: aigc-design-role-design
description: Use when the `4-Design` stage needs parent-skill orchestration plus 角色设计组 subagents to turn role list, global guidance, director detail evidence, and init presets into structured role design carriers under `projects/<项目名>/4-Design/2-角色/2-设计/`.
governance_tier: full
---

# 4-Design / 2-角色 / 2-设计

## 概述

`2-设计` 是 `4-Design/2-角色` 下的角色设计父 skill。

它不让 `形象建模 / 服装设计 / 妆容设计 / 个性塑造` 四个专家各写一份平行定稿，也不把 `1-清单` 的角色对象池重新打散回 `3-Detail` 去重做事实抽取。它的职责是：

1. 先消费 `1-清单` 产出的角色 canonical list。
2. 再结合 `2-Global`、`3-Detail/第N集.json` 与初始化预设，把每个命中角色收束成稳定的结构化设计稿。
3. 由父 skill 聚合 subagent patch，统一写回 `character_design.json + 逐角色 Markdown + _manifest.json`。

当前阶段采用 `skill-subagents` 的父子治理结构：

- 父 skill 负责触发、路由、上下文装配、patch 聚合、质量门禁与最终写回。
- `.codex/agents/aigc/设计组/角色设计/` 下的 subagents 负责专门化思考。
- subagents 默认返回 `agents_plan + patch / note / report`，不直接落盘 canonical 产物。

## Skill / Subagent Execution Rule (Mandatory)

在 `2-角色/2-设计` 中，分工固定为：

- subagents 负责思考、`agents plan`、局部证据整理、角色批次判断与 `patch / note / report`
- skill 本身负责命中角色裁决、上下文装配、patch 收束、canonical 写回、review/audit 闭环与下游 handoff

subagents 可以决定“本轮角色怎么拆、哪些字段先补、哪些冲突该上抛”，但不能替代 skill 完成阶段执行闭环。

## When to Use

- 已有 `projects/<项目名>/4-Design/2-角色/1-清单/第N集/角色清单.json`，需要继续生成角色设计稿。
- 需要把 `2-Global` 的项目级风格/类型/导演意图，与 `3-Detail/第N集.json` 的镜头证据合并为逐角色设计卡。
- 需要为后续 `3-面板`、`5-Image` 或角色多视图生图提供稳定的结构化角色设计 carrier。
- 需要通过 `.codex/agents/aigc/设计组/角色设计/team.md` 做选择性调度，而不是把角色外形、服装、妆容、性格和校审混写在一个 prompt 里。

## When Not to Use

- 当前还没有 `1-清单` 的角色对象池，应先回到 `4-Design/2-角色/1-清单`。
- 当前任务是补 `3-Detail/第N集.json` 的镜头事实，应回到 `3-Detail`。
- 当前任务是直接出图、做面板或视频请求，应进入 `3-面板`、`5-Image` 或 `6-Video`。

## Canonical Anchors

| 载体 | 位置 | 作用 |
| --- | --- | --- |
| 角色清单真源 | `projects/<项目名>/4-Design/2-角色/1-清单/第N集/角色清单.json` | 本阶段逐角色设计的第一输入根 |
| 当前集导演真源 | `projects/<项目名>/3-Detail/第N集.json` | 镜头级角色表现、穿搭、场景与道具证据 |
| 兼容导演输入 | `projects/<项目名>/3-Detail/第N集.json` | 用户显式给旧路径时的兼容回退 |
| 初始化种子 | `projects/<项目名>/0-Init/north_star.yaml` | 项目级世界观、题材、风格与受众约束 |
| 初始化 handoff | `projects/<项目名>/0-Init/init_handoff.yaml` | 初始化阶段沉淀下来的角色侧边界 |
| 全局风格真源 | `projects/<项目名>/2-Global/全局风格.md` | 项目级审美底座 |
| 类型指导真源 | `projects/<项目名>/2-Global/类型指导.md` | 类型化导演协议与禁区 |
| 导演意图真源 | `projects/<项目名>/2-Global/导演意图.md` | 当前集、当前组的镜头与人物演法指导 |
| 角色设计输出根 | `projects/<项目名>/4-Design/2-角色/2-设计/第N集/` | 本阶段 canonical 输出根 |
| shared I/O | `.agents/skills/aigc/4-Design/2-角色/2-设计/_shared/IO_CONTRACT.md` | 输入、输出、命名与 patch 槽位真源 |
| 角色设计组 team | `.codex/agents/aigc/设计组/角色设计/team.md` | 角色设计 team 的执行投影与共享禁令 |

## Character Design Team Contract (Mandatory)

唯一执行投影：

- team：`.codex/agents/aigc/设计组/角色设计/team.md`
- roles：
  - `.codex/agents/aigc/设计组/角色设计/设计统筹.md`
  - `.codex/agents/aigc/设计组/角色设计/形象建模.md`
  - `.codex/agents/aigc/设计组/角色设计/服装设计.md`
  - `.codex/agents/aigc/设计组/角色设计/妆容设计.md`
  - `.codex/agents/aigc/设计组/角色设计/个性塑造.md`
  - `.codex/agents/aigc/设计组/角色设计/角色一致性复核.md`
  - `.codex/agents/aigc/设计组/角色设计/真源审计.md`

### 父 skill 拥有

- `selected_roles[]`、`selected_agents[]` 与 tranche 决策。
- 全局上下文裁剪与 `context_packet_*` 装配。
- `character_design.json`、逐角色 Markdown、`_manifest.json` 的最终写回权。
- 对已有角色设计稿做增量 patch 而不是整稿覆盖的裁决权。
- `validation-report` 与下游 `3-面板 / 5-Image` 回接说明。

### 角色设计组 agents 拥有

- 专门化分析与角色化判断。
- `agents_plan + patch / note / report`。
- 当前角色范围内的局部证据与阻塞报告。

### 角色设计组 agents 不拥有

- 直接写回 `projects/<项目名>/4-Design/2-角色/2-设计/第N集/*`。
- 为未命中的角色补占位内容。
- 越权改写 `1-清单` 的角色 canonical identity。
- 越权创建角色面板、图片或视频请求。

## Route And Topology Contract (Mandatory)

### 默认 mixed tranche

`设计统筹 -> 形象建模 -> (服装设计 | 妆容设计 | 个性塑造 并行) -> 角色一致性复核 -> 真源审计`

### 路由规则

1. `设计统筹` 在以下任一条件满足时进入：
   - 本轮未明确 `selected_roles[]`
   - `角色清单.json` 已变更，需要重新切批
   - 用户显式要求只做主角、配角、某一角色或某一套服装状态
2. `形象建模` 对本轮所有命中角色默认进入：
   - 它负责建立 `visual_anchor / face_signature / body_signature / silhouette_signature`
   - 后续三位 specialist 的 patch 必须围绕该锚点收束
3. `服装设计 / 妆容设计 / 个性塑造` 在 `形象建模` patch 返回后默认并行：
   - `服装设计` 负责服装系统、材质、配色、穿搭状态与负面禁区
   - `妆容设计` 负责妆面、发型、皮肤质感、镜头可读性与近景稳定性
   - `个性塑造` 负责性格锚点、微动作、站姿、情绪气压与 prompt 中的人物气场
4. `角色一致性复核` 在以下任一条件满足时进入：
   - 同一角色命中了 2 个及以上 specialist
   - 同一角色有多套服装状态或多场景表现
   - 本轮做了跨角色批量设计
5. `真源审计` 在任何实际写回前默认进入：
   - 检查 evidence lineage、字段完整度、agents-plan-aware handoff 边界与输出路径
   - 只返回 `report` 或 veto，不写业务字段
6. 若用户显式只要求某个角色或某个设计维度，只命中对应角色与对应 specialist，不补空路径。

### 后台执行规则

- 无论当前是默认 mixed tranche，还是只命中单个角色的单点直达，角色设计组 subagents 默认都走后台派发，由父 skill 汇总 patch 后统一写回 canonical 产物。
- 只有用户显式要求逐轮共创某个角色、风格候选需要人工拍板，或上游证据不足必须前台补料时，父 skill 才转前台阻塞。

## Shared I/O Contract (Mandatory)

- 强制读取：`.agents/skills/aigc/4-Design/2-角色/2-设计/_shared/IO_CONTRACT.md`
- 强制读取：`.agents/skills/aigc/_shared/project-runtime-layout.md`
- 强制读取：`.codex/agents/aigc/设计组/角色设计/team.md`
- 按需读取：
  - `references/output-template.md`
  - `references/execution-flow.md`
  - `references/type-strategies.md`
  - `templates/角色设计卡.template.md`

硬规则：

1. 本阶段第一输入根固定为 `1-清单/角色清单.json`，禁止跳过对象池直接发明角色设计结论。
2. `character_design.json` 是本阶段 machine-first canonical carrier；逐角色 Markdown 是与之同源的人读稿。
3. subagents 只能返回 `agents_plan + patch / note / report`，不能直接落盘 canonical 文件。
4. 当前阶段允许读取场景/道具清单作为只读上下文包，但不允许把角色设计组扩写成场景或道具设计组。
5. 本阶段不得创建角色面板、图片或视频请求；那是 `3-面板 / 5-Image / 6-Video` 的职责。

## Context Contract (Mandatory)

### 加载顺序

1. `.agents/skills/aigc/SKILL.md + CONTEXT.md`
2. `.agents/skills/aigc/4-Design/SKILL.md + CONTEXT.md`
3. `.agents/skills/aigc/4-Design/2-角色/SKILL.md + CONTEXT.md`
4. 本 `SKILL.md + CONTEXT.md`
5. `.agents/skills/aigc/_shared/project-runtime-layout.md`
6. `.agents/skills/aigc/4-Design/2-角色/2-设计/_shared/IO_CONTRACT.md`
7. `projects/<项目名>/0-Init/north_star.yaml`
8. `projects/<项目名>/0-Init/init_handoff.yaml`
9. `projects/<项目名>/2-Global/全局风格.md`
10. `projects/<项目名>/2-Global/类型指导.md`
11. `projects/<项目名>/2-Global/导演意图.md`
12. `projects/<项目名>/4-Design/2-角色/1-清单/第N集/角色清单.json`
13. `projects/<项目名>/3-Detail/第N集.json` 或兼容 `projects/<项目名>/3-Detail/第N集.json`
14. 仅加载命中的角色设计组 agent docs

### 四层上下文

1. `global charter context`
   - 根 `AGENTS.md`
   - `.agents/skills/aigc/SKILL.md`
2. `task context`
   - 用户目标、项目名、当前集数、显式角色范围、显式风格约束
3. `role context`
   - `角色清单.json` 中当前角色的 canonical identity、穿搭状态、证据镜头与出现组
4. `evidence context`
   - `north_star / init_handoff / 全局风格 / 类型指导 / 导演意图 / 编导第N集`

## Execution Workflow

1. 读取 `角色清单.json`，锁定当前集 `selected_roles[]`、`role_tier` 与 `costume_state`。
2. 判定 `selected_agents[]` 与执行 tranche。
3. 生成父 skill 的 `mission_brief_role_design` 与角色化 `subagent_brief_<role>`。
4. 先运行 `设计统筹`，决定角色批次、优先级、边界与回退。
5. 对命中角色先运行 `形象建模`，为每个角色建立统一视觉锚点。
6. 并行运行 `服装设计 / 妆容设计 / 个性塑造`，只收集局部 patch。
7. `角色一致性复核` 对跨字段冲突、跨角色辨识度、场景/道具兼容性做 review。
8. `真源审计` 对 evidence lineage、字段完整度、路径与越权项做 audit。
9. 父 skill 聚合 patch，并按模板写回：
   - `character_design.json`
   - `第N集/[角色名].md`
   - `_manifest.json`
10. 对已存在的角色只更新命中角色或命中字段，不覆盖未命中的角色卡。
11. 返回默认下一入口：
   - 若需要排版/展示 -> `3-面板`
   - 若需要生图 -> `5-Image`

## Canonical Output Governance (Mandatory)

1. `projects/<项目名>/4-Design/2-角色/2-设计/第N集/character_design.json` 是本阶段 machine-first 唯一真源。
2. `projects/<项目名>/4-Design/2-角色/2-设计/第N集/[角色名].md` 是与 JSON 同源的人读稿，不是独立平行真相。
3. `projects/<项目名>/4-Design/2-角色/2-设计/第N集/_manifest.json` 只记录本轮命中角色、输入根、输出清单与审计摘要。
4. 所有 canonical 文件都由父 skill 聚合写回；角色设计组 agents 只提供局部 patch。
5. 未命中的角色不得被补空字段或空白模板。
6. 若现有输出已存在，只允许增量更新命中角色或命中字段，不得整稿抹平历史内容。

## Field Master

| field_id | 输出位置/字段 | 内容要求 | 默认责任 Step | 质量维度 | 失败码 |
| --- | --- | --- | --- | --- | --- |
| FIELD-ROLE-DESIGN-01 | 阶段定位 | 明确 `2-设计` 消费 `1-清单`，负责结构化角色设计，不越权做面板/出图 | S1 | 边界清晰度 | FAIL-ROLE-DESIGN-01 |
| FIELD-ROLE-DESIGN-02 | 角色路由 | 明确 `selected_roles[]`、`selected_agents[]` 与 mixed tranche | S2 | 路由完整性 | FAIL-ROLE-DESIGN-02 |
| FIELD-ROLE-DESIGN-03 | 视觉锚点 | 每个命中角色都有稳定 `visual_anchor / face_signature / body_signature` | S3 | 角色锚点稳定性 | FAIL-ROLE-DESIGN-03 |
| FIELD-ROLE-DESIGN-04 | specialist patch | `wardrobe_profile / makeup_profile / personality_profile / variation_rules` 完整可聚合 | S4 | 设计颗粒度 | FAIL-ROLE-DESIGN-04 |
| FIELD-ROLE-DESIGN-05 | 一致性复核 | 跨字段、跨角色、跨场景兼容性被 review，不互相打架 | S5 | 设计一致性 | FAIL-ROLE-DESIGN-05 |
| FIELD-ROLE-DESIGN-06 | canonical carrier | `character_design.json + 逐角色 Markdown + _manifest.json` 同源且命名稳定 | S6 | 输出完整性 | FAIL-ROLE-DESIGN-06 |
| FIELD-ROLE-DESIGN-07 | 聚合写回 | 父 skill 独占写回，未命中角色不被覆盖 | S7 | 聚合可执行性 | FAIL-ROLE-DESIGN-07 |
| FIELD-ROLE-DESIGN-08 | 审计闭环 | 返回 triad closure、阻塞说明与下游回接 | S8 | 闭环完整性 | FAIL-ROLE-DESIGN-08 |

## Thought Pass Map

| step_id | 聚焦字段 | 核心问题 | 生成动作 | 未达标信号 |
| --- | --- | --- | --- | --- |
| S1 | FIELD-ROLE-DESIGN-01 | 当前是不是 `2-设计` 问题 | 锁定阶段边界与上下游职责 | 跳过 `1-清单` 直接设计 |
| S2 | FIELD-ROLE-DESIGN-02 | 本轮该设计哪些角色、调哪些 agent | 写出 `selected_roles[]`、`selected_agents[]` 与 tranche | 多角色并列但没有进入条件 |
| S3 | FIELD-ROLE-DESIGN-03 | 角色视觉锚点是否已经稳定 | 生成 `visual_anchor / face_signature / body_signature` | specialist 没有统一锚点 |
| S4 | FIELD-ROLE-DESIGN-04 | 三个 specialist 的 patch 是否各归其位 | 写出服装、妆容、个性三类 patch | patch 互相污染或缺字段 |
| S5 | FIELD-ROLE-DESIGN-05 | 设计是否内在一致且可被场景/道具消费 | 做 reviewer 复核与返工判断 | 强行拼装成冲突人设 |
| S6 | FIELD-ROLE-DESIGN-06 | canonical 输出结构是否稳定 | 按模板生成 JSON / Markdown / manifest | 只有文采，没有机读 carrier |
| S7 | FIELD-ROLE-DESIGN-07 | 父 skill 如何安全写回 | 仅更新命中角色和命中字段 | 整稿覆盖或第二真源出现 |
| S8 | FIELD-ROLE-DESIGN-08 | 如何证明本轮完成或阻塞 | 输出 triad closure 与下一入口 | 没有审计或回接说明 |

## Pass Table

| field_id | Pass Standard | Fail Code | Rework Entry |
| --- | --- | --- | --- |
| FIELD-ROLE-DESIGN-01 | 阶段边界、父子职责与输出真源明确 | FAIL-ROLE-DESIGN-01 | S1 |
| FIELD-ROLE-DESIGN-02 | 角色路由、顺序与单点直达规则明确 | FAIL-ROLE-DESIGN-02 | S2 |
| FIELD-ROLE-DESIGN-03 | 每个命中角色有稳定视觉锚点 | FAIL-ROLE-DESIGN-03 | S3 |
| FIELD-ROLE-DESIGN-04 | specialist patch 颗粒度清晰且不越权 | FAIL-ROLE-DESIGN-04 | S4 |
| FIELD-ROLE-DESIGN-05 | reviewer 能指出跨字段冲突与返工入口 | FAIL-ROLE-DESIGN-05 | S5 |
| FIELD-ROLE-DESIGN-06 | JSON / Markdown / manifest 同源且字段完整 | FAIL-ROLE-DESIGN-06 | S6 |
| FIELD-ROLE-DESIGN-07 | 父 skill 独占写回，agents 只返 `agents_plan + patch / note / report` | FAIL-ROLE-DESIGN-07 | S7 |
| FIELD-ROLE-DESIGN-08 | 返回 triad closure、阻塞说明与下游回接 | FAIL-ROLE-DESIGN-08 | S8 |

## Root-Cause Execution Contract (Mandatory)

当 `2-设计` 出现以下问题时，必须先修源层而不是补单次角色文案：

- `2-设计` 跳过 `1-清单`，直接从 `3-Detail/第N集.json` 发明人设。
- 四个 specialist 各自输出一整套角色稿，父 skill 无法收束。
- 角色设计看起来完整，但没有 `evidence[]`、`shot_id` 或 `group_id` 回链。
- 设计内容吞掉场景或道具职责，出现跨模块越权。
- canonical 输出只剩 Markdown，没有 machine-first JSON carrier。

必经链路：

`Symptom -> Direct Technical Cause -> Rule Source -> Meta Rule Source -> Fix Landing Points`

优先检查：

- `Rule Source`
  - `.agents/skills/aigc/4-Design/2-角色/2-设计/SKILL.md`
  - `.agents/skills/aigc/4-Design/2-角色/2-设计/_shared/IO_CONTRACT.md`
  - `.codex/agents/aigc/设计组/角色设计/team.md`
- `Meta Rule Source`
  - `.agents/skills/aigc/4-Design/2-角色/SKILL.md`
  - `.agents/skills/aigc/4-Design/SKILL.md`
  - `/Users/vincentlee/.codex/skills/meta/构建/技能/skill-subagents/SKILL.md`
  - 根 `AGENTS.md`

面向用户的闭环固定返回：

1. root cause location
2. immediate fix
3. systemic prevention fix

## Completion Criteria

- 已建立 `2-设计` 父级真源。
- 已锁定 `character_design.json + 逐角色 Markdown + _manifest.json` 的单一输出口径。
- 已落地角色设计组 team 与七个角色合同。
- 已明确 `2-设计` 只能消费 `1-清单` 与导演证据，不越权出图或做面板。
- 已给出 `3-面板 / 5-Image` 的默认回接闭环。
