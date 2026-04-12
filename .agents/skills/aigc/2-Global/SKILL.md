---
name: aigc-global
description: Use when the global directing stage needs parent-skill orchestration plus 导演组 subagents to turn planning grouping outputs and init presets into project-level global style, type guidance, and episode-group director intent under `projects/<项目名>/2-Global/`.
governance_tier: full
---

# aigc 2-Global

## 概述

`2-Global` 是 `aigc` 技能树位于 `1-Planning` 与 `3-Detail` 之间的导演前置全局合同阶段。

它不负责把内容直接写成 `3-Detail/第N集.json`，也不让各角色各写一套平行主稿。它的职责是把规划阶段已经稳定的分组结果与初始化预设，收束成三份可被后续 `3-Detail` 稳定消费的导演组真源：

- `projects/<项目名>/2-Global/全局风格.md`
- `projects/<项目名>/2-Global/类型指导.md`
- `projects/<项目名>/2-Global/导演意图.md`

当前阶段采用 `skill-subagents` 的父子治理结构：

- 父 skill 负责触发、路由、上下文装配、patch 聚合、质量门禁与最终写回
- `.codex/agents/aigc/导演组/` 下的 subagents 负责专门化思考
- subagents 默认返回 `agents_plan + patch / note / report`，不直接宣告阶段完成

## Skill / Subagent Execution Rule (Mandatory)

在 `2-Global` 中，分工固定为：

- subagents 负责思考、`agents plan`、局部证据整理、候选路径比较与 `patch / note / report`
- skill 本身负责总路由、上下文装配、执行收束、canonical 写回、阶段验收与下游 handoff

subagents 可以决定“怎么想、为什么这么判、当前该补哪一块”，但不能替代 skill 完成阶段执行闭环。

## When to Use

- 已经有 `projects/<项目名>/1-Planning/3-分组/第N集.md`，需要进入导演前置全局合同阶段。
- 需要为整部项目沉淀稳定的全局风格与类型指导，再为当前集按分镜组生成导演意图。
- 需要让 `3-Detail` 在开写 `3-Detail/第N集.json` 之前先消费三份全局指导文档。
- 需要通过 `.codex/agents/aigc/导演组/team.md` 做选择性调度，而不是把风格、类型、导演构思混写在一个提示里。

## When Not to Use

- 当前连 `projects/<项目名>/1-Planning/3-分组/第N集.md` 都不存在。
- 当前任务其实是继续分集、剧本整形或分组，应回到 `1-Planning`。
- 当前任务已经在补镜级字段、主体、画面或视频产物，应进入 `3-Detail / 4-Design / 5-Image / 6-Video`。

## Canonical Anchors

| 载体 | 位置 | 作用 |
| --- | --- | --- |
| 当前集分组主稿 | `projects/<项目名>/1-Planning/3-分组/第N集.md` | 当前集导演前置工作的主输入 |
| 当前集分组总报告 | `projects/<项目名>/1-Planning/3-分组/执行报告.md` | 当前集分组决议、组序与 handoff 摘要 |
| 初始化种子 | `projects/<项目名>/0-Init/north_star.yaml` | 项目目标、风格方向与高层约束 |
| 初始化 handoff | `projects/<项目名>/0-Init/init_handoff.yaml` | 初始化阶段传下来的项目基线 |
| 项目输入索引 | `projects/<项目名>/0-Init/story-source-manifest.yaml` | 预设、锁轴、保真模式等证据入口 |
| 全局风格真源 | `projects/<项目名>/2-Global/全局风格.md` | 项目级风格底座 |
| 类型指导真源 | `projects/<项目名>/2-Global/类型指导.md` | 项目级类型化导演协议 |
| 导演意图真源 | `projects/<项目名>/2-Global/导演意图.md` | 按集、按组沉淀的导演构思主稿 |
| shared I/O | `.agents/skills/aigc/2-Global/_shared/IO_CONTRACT.md` | 本阶段输入/输出、命名和 handoff 单一真源 |
| 导演组创作方法真源 | `.codex/agents/aigc/导演组/_shared/CREATIVE_METHOD.md` | 导演组高质量创作方法与质量门禁单一真源 |
| 导演组 team | `.codex/agents/aigc/导演组/team.md` | 执行投影与共享禁令 |

## Director Team Contract (Mandatory)

唯一执行投影：

- team：`.codex/agents/aigc/导演组/team.md`
- roles：
  - `.codex/agents/aigc/导演组/全局风格设计师.md`
  - `.codex/agents/aigc/导演组/类型化指导.md`
  - `.codex/agents/aigc/导演组/导演.md`

### 父 skill 拥有

- `selected_agents[]` 与执行 tranche 决策
- 全局上下文裁剪与角色 context packet 装配
- 三份 canonical Markdown 的最终写回权
- `validation-report` 与下一阶段回接说明
- 对现有文件做增量更新而不是整稿覆盖的裁决权

### 导演组 agents 拥有

- 专门化分析与角色化判断
- `agents_plan + patch / note / report`
- 当前角色范围内的局部证据与阻塞报告

### 导演组 agents 不拥有

- 直接写回 `projects/<项目名>/2-Global/*.md`
- 把自己的 patch 升格成最终真源
- 替未命中的角色补占位内容
- 越权生成 `projects/<项目名>/3-Detail/第N集.json`

## Route And Topology Contract (Mandatory)

### 默认 tranche

`全局风格设计师 -> 类型化指导 -> 导演`

### 路由规则

1. `全局风格设计师` 在以下任一条件满足时进入：
   - `projects/<项目名>/2-Global/全局风格.md` 不存在
   - `north_star`、`init_handoff` 或用户显式风格要求发生重大变化
   - 当前项目需要首次建立稳定风格底座
2. `类型化指导` 在以下任一条件满足时进入：
   - `projects/<项目名>/2-Global/类型指导.md` 不存在
   - 项目题材裁决、主副类型、混合公式或风格底座发生变化
   - 用户显式要求重做类型化导演协议
3. `导演` 在当前集分组主稿已稳定时默认进入：
   - 读取当前 `第N集` 的分组结果
   - 只更新 `导演意图.md` 中对应集与组的区块
4. 若用户显式只要求某一份产物，只命中对应角色，不补空路径。
5. 若上游分组仍不稳定，停止进入 `导演`，先返回 `report` 说明阻塞点。

### 后台执行规则

- 无论当前是 `全局风格设计师 -> 类型化指导 -> 导演` 的有序 tranche，还是单点直达某一份产物，导演组 subagents 默认都走后台派发，由父 skill 汇总 patch 后统一写回三份 Markdown 真源。
- 只有用户显式要求逐轮共创、风格候选需要人工拍板，或上游证据不足必须前台补料时，父 skill 才转前台阻塞。

## Shared I/O Contract (Mandatory)

- 强制读取：`.agents/skills/aigc/2-Global/_shared/IO_CONTRACT.md`
- 强制读取：`.agents/skills/aigc/_shared/project-runtime-layout.md`
- 强制读取：`.codex/agents/aigc/导演组/_shared/CREATIVE_METHOD.md`
- 强制读取：`.codex/agents/aigc/导演组/team.md`

硬规则：

1. 本阶段的第一输入根固定为 `projects/<项目名>/1-Planning/3-分组/第N集.md`。
2. 项目级稳定约束优先来自 `0-Init/north_star.yaml`、`0-Init/init_handoff.yaml` 与 `story-source-manifest.yaml`。
3. `全局风格.md` 与 `类型指导.md` 是项目级真源，只允许按需刷新，不允许每个 episode 各写一份平行版本。
4. `导演意图.md` 是项目级主稿，但必须按 `## 第N集 -> ### 【x-x-x】` 的层次做增量写回。
5. `3-分组` 的组标题是三段式 `分镜组ID`；四段式 `分镜ID` 只属于下游 `3-Detail` 与制作阶段。
5. 本阶段不得创建或改写 `projects/<项目名>/3-Detail/第N集.json`；那是 `3-Detail` 的责任。
6. 导演组的高质量创作方法统一由 `.codex/agents/aigc/导演组/_shared/CREATIVE_METHOD.md` 提供；单角色文档只补 role delta，不再各自平行发明方法论。

## Context Contract (Mandatory)

### 加载顺序

1. `.agents/skills/aigc/SKILL.md + CONTEXT.md`
2. 本 `SKILL.md + CONTEXT.md`
3. `.agents/skills/aigc/_shared/project-runtime-layout.md`
4. `.agents/skills/aigc/2-Global/_shared/IO_CONTRACT.md`
5. `.codex/agents/aigc/导演组/_shared/CREATIVE_METHOD.md`
6. `projects/<项目名>/0-Init/north_star.yaml`
7. `projects/<项目名>/0-Init/init_handoff.yaml`
8. `projects/<项目名>/0-Init/story-source-manifest.yaml`（若存在）
9. `projects/<项目名>/1-Planning/2-剧本/第N集.md`（若存在）
10. `projects/<项目名>/1-Planning/3-分组/第N集.md`
11. `projects/<项目名>/1-Planning/3-分组/执行报告.md`（若存在）
12. 仅加载命中的导演组 agent docs

### 四层上下文

1. `global charter context`
   - 根 `AGENTS.md`
   - `.agents/skills/aigc/SKILL.md`
2. `task context`
   - 用户目标、项目名、当前集数、显式约束
3. `role context`
   - 风格 / 类型 / 导演各自所需的最小证据切片
4. `evidence context`
   - `north_star / init_handoff / grouped-script.md / grouping-report.md / 现有 2-Global 文档`

## Execution Workflow

1. 读取当前 `第N集` 的分组主稿与初始化种子，锁定是否满足进入条件。
2. 判定 `selected_agents[]`：
   - 缺 `全局风格.md` 或风格约束变化 -> 命中 `全局风格设计师`
   - 缺 `类型指导.md` 或类型约束变化 -> 命中 `类型化指导`
   - 当前集分组已稳定 -> 命中 `导演`
3. 先生成父 skill 的 `mission_brief` 与角色化 `subagent_brief_<role>`，显式回指 `team.md + CREATIVE_METHOD.md`。
4. 依 tranche 顺序收集命中角色的 `agents_plan + patch / note / report`。
5. 父 skill 聚合 patch，并按模板写回：
   - `全局风格.md`
   - `类型指导.md`
   - `导演意图.md`
6. 对 `导演意图.md` 只更新当前 `第N集` 与命中的分镜组ID `【x-x-x】`，不覆盖其他集。
7. 运行自检，确认没有越权创建 `3-Detail/第N集.json`，也没有把 episode 内容写进项目级风格/类型总则。
8. 返回唯一默认下一入口：`3-Detail`。

## Canonical Output Governance (Mandatory)

1. `projects/<项目名>/2-Global/全局风格.md` 是项目级全局风格唯一真源。
2. `projects/<项目名>/2-Global/类型指导.md` 是项目级类型化导演协议唯一真源。
3. `projects/<项目名>/2-Global/导演意图.md` 是按集、按组组织的导演构思唯一真源。
4. 三份文档都由父 skill 聚合写回；导演组 agents 只提供 `agents_plan` 与局部 patch。
5. `2-Global` 不创建 `projects/<项目名>/3-Detail/第N集.json`，也不与 `3-Detail` 争夺 episode 根文件。
6. 若现有文档已存在，只允许增量更新被命中的章节，不得整稿抹平历史内容。

## Field Master

| field_id | 输出位置/字段 | 内容要求 | 默认责任 Step | 质量维度 | 失败码 |
| --- | --- | --- | --- | --- | --- |
| FIELD-GLOBAL-01 | 阶段定位 | 明确 `2-Global` 是 `1-Planning` 与 `3-Detail` 之间的导演前置全局合同阶段 | S1 | 边界清晰度 | FAIL-GLOBAL-01 |
| FIELD-GLOBAL-02 | 角色路由 | 明确 `selected_agents[]`、tranche 与进入条件 | S2 | 路由完整性 | FAIL-GLOBAL-02 |
| FIELD-GLOBAL-03 | shared I/O | 锁定分组输入根、三份 Markdown 输出与 patch 命名 | S3 | 交接清晰度 | FAIL-GLOBAL-03 |
| FIELD-GLOBAL-04 | 全局风格真源 | 项目级风格底座稳定、不过度 episode 化 | S4 | 项目级稳定性 | FAIL-GLOBAL-04 |
| FIELD-GLOBAL-05 | 类型指导真源 | 类型栈、导演打法与禁区清晰可消费 | S5 | 类型化有效性 | FAIL-GLOBAL-05 |
| FIELD-GLOBAL-06 | 导演意图真源 | 当前集按组的导演构思具像、可被 `3-Detail` 消费 | S6 | 组级可消费性 | FAIL-GLOBAL-06 |
| FIELD-GLOBAL-07 | 创作方法真源 | 导演组共享创作方法、质量门禁与退化规则有单一真源 | S7 | 方法稳定性 | FAIL-GLOBAL-07 |
| FIELD-GLOBAL-08 | 聚合写回 | 父 skill 聚合 patch 并仅更新命中章节 | S8 | 聚合可执行性 | FAIL-GLOBAL-08 |
| FIELD-GLOBAL-09 | 验收闭环 | 返回通过/阻塞、返工入口与下一阶段回接 | S9 | 闭环完整性 | FAIL-GLOBAL-09 |

## Thought Pass Map

| step_id | 聚焦字段 | 核心问题 | 生成动作 | 未达标信号 |
| --- | --- | --- | --- | --- |
| S1 | FIELD-GLOBAL-01 | 当前是不是 `2-Global` 阶段问题 | 锁定阶段边界与上下游职责 | 把本阶段写成 `3-Detail` 或 `1-Planning` |
| S2 | FIELD-GLOBAL-02 | 本轮该调度哪些角色 | 写出 `selected_agents[]` 与 tranche | 多角色并列但没有进入条件 |
| S3 | FIELD-GLOBAL-03 | 输入输出真源是什么 | 回指 shared I/O 与模板 | stage 输入输出说不清 |
| S4 | FIELD-GLOBAL-04 | 项目级风格底座是否稳定 | 聚合风格 patch，避免写成某一集私有风格 | 风格文档被 episode 细节污染 |
| S5 | FIELD-GLOBAL-05 | 类型指导是否能约束后续导演链 | 聚合类型 patch 与禁区 | 只有题材词，没有导演打法 |
| S6 | FIELD-GLOBAL-06 | 当前集导演构思是否够具体 | 写入 `导演意图.md` 的 `第N集/【x-x-x】` 章节 | 只剩空泛口号 |
| S7 | FIELD-GLOBAL-07 | 方法论是否有共享真源 | 回指导演组共享创作方法合同 | 角色只剩边界，没有创作方法 |
| S8 | FIELD-GLOBAL-08 | 父 skill 如何安全写回 | 只更新命中章节并保留其余内容 | 整稿覆盖或越权创建新真源 |
| S9 | FIELD-GLOBAL-09 | 如何证明本轮完成或阻塞 | 输出 triad closure 与下一入口 | 没有返工入口或下一阶段 |

## Pass Table

| field_id | Pass Standard | Fail Code | Rework Entry |
| --- | --- | --- | --- |
| FIELD-GLOBAL-01 | 阶段边界、父子职责与输出真源明确 | FAIL-GLOBAL-01 | S1 |
| FIELD-GLOBAL-02 | 角色路由、顺序与单点直达规则明确 | FAIL-GLOBAL-02 | S2 |
| FIELD-GLOBAL-03 | 分组输入、三份输出与 patch 命名统一 | FAIL-GLOBAL-03 | S3 |
| FIELD-GLOBAL-04 | `全局风格.md` 维持项目级稳定，不写成 episode 杂糅稿 | FAIL-GLOBAL-04 | S4 |
| FIELD-GLOBAL-05 | `类型指导.md` 具备主副类型、导演打法与禁区 | FAIL-GLOBAL-05 | S5 |
| FIELD-GLOBAL-06 | `导演意图.md` 能按集、按三段式 `分镜组ID` 被 `3-Detail` 直接消费 | FAIL-GLOBAL-06 | S6 |
| FIELD-GLOBAL-07 | 导演组共享方法真源存在且被父 skill / team / 角色显式继承 | FAIL-GLOBAL-07 | S7 |
| FIELD-GLOBAL-08 | 父 skill 独占写回，agents 只返 `agents_plan + patch / note / report` | FAIL-GLOBAL-08 | S8 |
| FIELD-GLOBAL-09 | 返回 triad closure、阻塞说明与 `3-Detail` 回接 | FAIL-GLOBAL-09 | S9 |

## Root-Cause Execution Contract (Mandatory)

当 `2-Global` 出现以下问题时，必须先修源层而不是补单次文案：

- `2-Global` 仍只有概念引用，没有真实父 skill
- subagents 直接争夺三份 Markdown 的最终写回权
- 项目级风格/类型文档被当前集局部内容污染
- `导演意图.md` 被写成全局空话，无法回链到 `第N集/【x-x-x】`
- 阶段越权直接创建 `3-Detail/第N集.json`

必经链路：

`Symptom -> Direct Technical Cause -> Rule Source -> Meta Rule Source -> Fix Landing Points`

优先检查：

- `Rule Source`
  - `.agents/skills/aigc/2-Global/SKILL.md`
  - `.agents/skills/aigc/2-Global/_shared/IO_CONTRACT.md`
  - `.codex/agents/aigc/导演组/team.md`
- `Meta Rule Source`
  - `AGENTS.md`
  - `.agents/skills/aigc/SKILL.md`
  - `/Users/vincentlee/.codex/skills/meta/构建/技能/skill-subagents/SKILL.md`

面向用户的闭环固定返回：

1. root cause location
2. immediate fix
3. systemic prevention fix

## Completion Criteria

- 已建立 `2-Global` 阶段父级真源。
- 已锁定三份 Markdown 输出的单一口径。
- 已落地导演组 team 与三角色合同。
- 已明确 `2-Global` 不拥有 `3-Detail/第N集.json` 的写回权。
- 已给出 `3-Detail` 的唯一回接闭环。
