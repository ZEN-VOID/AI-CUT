---
name: aigc-detail
description: Use when the detail directing stage needs parent-skill orchestration plus 制作组 subagents to turn `2-Global` guidance, planning grouping outputs, and init presets into `projects/<项目名>/3-Detail/第N集.json` under the shared director episode schema.
governance_tier: full
---

# aigc 3-Detail

## 概述

`3-Detail` 是 `aigc` 技能树位于 `2-Global` 与 `4-Design / 5-Image / 6-Video` 之间的制作明细合同阶段。

它不再输出第二份导演主稿，也不让各角色各写一套平行 JSON。它的职责是消费：

- `projects/<项目名>/1-Planning/3-分组/第N集.*`
- `projects/<项目名>/2-Global/*.md`
- 初始化相关预设与 `source_profile`

并把这些上游真源收束为唯一 canonical episode 根文件：

- `projects/<项目名>/3-Detail/第N集.json`

当前阶段采用 `skill-subagents` 的父子治理结构：

- 父 skill 负责触发、路由、bootstrap、上下文装配、patch 聚合、质量门禁与最终写回
- `.codex/agents/aigc/制作组/` 下的 subagents 负责分镜级专门化思考
- subagents 默认返回 `agents_plan + patch / note / report`，不直接宣布阶段完成

## Skill / Subagent Execution Rule (Mandatory)

在 `3-Detail` 中，分工固定为：

- subagents 负责思考、`agents plan`、字段级候选路径、局部证据整理与 `patch / note / report`
- skill 本身负责总路由、上下文装配、bootstrap、patch 收束、canonical 写回、阶段验收与下游 handoff

subagents 可以决定“当前 shot/group 应该怎样拆、怎样补、哪些风险该上抛”，但不能替代 skill 完成阶段执行闭环。

## When to Use

- 已经存在 `projects/<项目名>/1-Planning/3-分组/第N集.md`，且 `2-Global` 三份导演前置文档已经可读。
- 需要把组级导演构思下钻为 shot-level 的结构化明细字段。
- 需要初始化或增量维护 `projects/<项目名>/3-Detail/第N集.json`。
- 需要通过 `.codex/agents/aigc/制作组/team.md` 做选择性调度，而不是把分镜表现、角色表现、运镜、氛围、摄影与转场混写在一个提示里。

## When Not to Use

- 当前连 `projects/<项目名>/1-Planning/3-分组/第N集.md` 都不存在。
- 当前 `2-Global/全局风格.md`、`类型指导.md`、`导演意图.md` 仍未稳定，应先回到 `2-Global`。
- 当前任务已经在生成主体、画面或视频请求，而不是补 `3-Detail/第N集.json`，应进入 `4-Design / 5-Image / 6-Video`。

## Canonical Anchors

| 载体 | 位置 | 作用 |
| --- | --- | --- |
| 当前集分组主稿 | `projects/<项目名>/1-Planning/3-分组/第N集.md` | 当前集 detail 的组级主输入 |
| 当前集分组侧车 | `projects/<项目名>/1-Planning/3-分组/第N集.grouping.json` | 组序、锁轴、handoff 的机读输入 |
| 初始化种子 | `projects/<项目名>/0-Init/north_star.yaml` | 项目目标、风格方向与高层约束 |
| 初始化 handoff | `projects/<项目名>/0-Init/init_handoff.yaml` | 初始化阶段传下来的项目基线 |
| 项目输入索引 | `projects/<项目名>/0-Init/story-source-manifest.yaml` | 预设、锁轴、保真模式等证据入口 |
| 全局风格真源 | `projects/<项目名>/2-Global/全局风格.md` | 项目级风格底座 |
| 类型指导真源 | `projects/<项目名>/2-Global/类型指导.md` | 项目级类型化导演协议 |
| 导演意图真源 | `projects/<项目名>/2-Global/导演意图.md` | 当前集按组的导演构思主稿 |
| shared runtime | `.agents/skills/aigc/_shared/project-runtime-layout.md` | 运行时目录和写回责任单一真源 |
| shared schema | `.agents/skills/aigc/_shared/director_episode_output.schema.json` | episode JSON 单一结构真源 |
| bootstrap template | `.agents/skills/aigc/_shared/director_episode_bootstrap.template.json` | 根文件首次创建模板 |
| shared I/O | `.agents/skills/aigc/3-Detail/_shared/IO_CONTRACT.md` | 本阶段输入/输出、命名和 field-slot 单一真源 |
| 制作组 team | `.codex/agents/aigc/制作组/team.md` | 执行投影与共享禁令 |
| 制作组质量手册 | `.codex/agents/aigc/制作组/_shared/CREATIVE_QUALITY_PLAYBOOK.md` | 共享创作方法、质量门禁与回退策略真源 |

## Production Team Contract (Mandatory)

唯一执行投影：

- team：`.codex/agents/aigc/制作组/team.md`
- roles：
  - `分镜表现/分镜规划`
  - `分镜表现/分镜构图`
  - `角色表现/内心戏指导`
  - `角色表现/动作戏指导`
  - `角色表现/对手戏指导`
  - `运镜手法/叙事派`
  - `运镜手法/炫技派`
  - `场景氛围/景观设计`
  - `场景氛围/氛围设计`
  - `摄影美学/摄影师`
  - `摄影美学/光影美学大师`
  - `摄影美学/色彩美学大师`
  - `转场特效/转场设计`
  - `转场特效/特效设计`
  - `复核审计/连续性复核`
  - `复核审计/真源审计`

### 父 skill 拥有

- `selected_groups[]`、`selected_agents[]` 与 tranche 决策
- 根文件 bootstrap 与 `metadata / thinking_chain` 的父级写回权
- 多角色 patch 的字段级合成、冲突裁决与 patch-in-place
- `projects/<项目名>/3-Detail/validation-report.md` 的阶段闭环
- 对既有 episode 根文件做增量更新而不是整稿覆盖的裁决权

### 制作组 agents 拥有

- 专门化分析与角色化判断
- `agents_plan + patch / note / report`
- 当前角色范围内的局部证据、风险提示与阻塞报告

### 制作组 agents 不拥有

- 直接写回 `projects/<项目名>/3-Detail/第N集.json`
- 把自己的 patch 升格成最终真源
- 替未命中的角色补占位内容
- 越权改写 `2-Global/*.md` 或下游 `4-Design / 5-Image / 6-Video` 产物

## Route And Topology Contract (Mandatory)

### 默认 tranche

1. `分镜规划`
2. 并行：`分镜构图`、`景观设计`、`氛围设计`、`内心戏指导` / `动作戏指导` / `对手戏指导`
3. 并行：`叙事派`（默认）/ `炫技派`（对照或显式命中）、`摄影师`、`光影美学大师`、`色彩美学大师`、`转场设计`、`特效设计`
4. `连续性复核 -> 真源审计`

### 路由规则

1. `分镜规划` 在以下任一条件满足时强制进入：
   - `projects/<项目名>/3-Detail/第N集.json` 不存在
   - 当前集或命中组还没有稳定 `分镜ID / 时间段` 骨架
   - 用户显式要求重做镜头拆分、节奏分配或 shot 覆盖
2. `分镜构图` 在命中组需要新建或重写 shot-level staging 时默认进入。
3. `角色表现` 族群按命中组问题选择：
   - 内心驱动、压抑、心理波动 -> `内心戏指导`
   - 肢体动作、追逐、打斗、节奏推进 -> `动作戏指导`
   - 多角色关系、对峙、对话张力 -> `对手戏指导`
4. `运镜手法` 默认命中 `叙事派`；只有用户显式要求、题材允许或需要挑战方案时，才追加 `炫技派` 作为对照 patch。
5. `场景氛围` 族群按问题选择：
   - 空间结构、环境元素、景别支点 -> `景观设计`
   - 时间感、空气感、压迫/抒缓氛围 -> `氛围设计`
6. `摄影美学` 族群按问题选择：
   - 镜头语言总协调或 final look -> `摄影师`
   - 光源与明暗戏剧性 -> `光影美学大师`
   - 色板、色温、色彩情绪 -> `色彩美学大师`
7. `转场设计` 只在组内或组间镜头衔接需要被显式表达时进入；`特效设计` 只在存在必要特效桥接或幻想化效果时进入。
8. `连续性复核` 与 `真源审计` 在以下任一条件满足时强制进入：
   - 首次创建 episode 根文件
   - 本轮 patch 跨多个字段族
   - 用户要求“完整/精修/可直接下游消费”

### 后台执行规则

- 无论当前是 `分镜规划 -> 专业角色并行 -> 复核审计` 的 tranche 链，还是单点直达某一组/镜，制作组 subagents 默认都走后台派发，由父 skill 汇总 patch 后再做 patch-in-place 写回。
- 只有用户显式要求逐轮共创、某个命中组/镜必须前台确认，或证据缺口需要即时补料时，父 skill 才转前台阻塞。

## Shared I/O Contract (Mandatory)

- 强制读取：`.agents/skills/aigc/3-Detail/_shared/IO_CONTRACT.md`
- 强制读取：`.agents/skills/aigc/_shared/project-runtime-layout.md`
- 强制读取：`.agents/skills/aigc/_shared/director_episode_output.schema.json`
- 强制读取：`.codex/agents/aigc/制作组/team.md`
- 强制读取：`.codex/agents/aigc/制作组/_shared/CREATIVE_QUALITY_PLAYBOOK.md`

硬规则：

1. 本阶段的第一输入根固定为 `projects/<项目名>/1-Planning/3-分组/第N集.md` 与 `projects/<项目名>/2-Global/*.md`。
2. 首次进入且根文件不存在时，父 skill 必须基于 `.agents/skills/aigc/_shared/director_episode_bootstrap.template.json` 创建 `projects/<项目名>/3-Detail/第N集.json`。
3. `metadata.source_profile` 只能继承或保守扩写 `1-Planning` 与 `story-source-manifest` 的既有结论，不得在本阶段发明新预设模式。
4. 任何 subagent 只能返回 `agents_plan + patch / note / report`，不能直接落盘 canonical JSON。
5. 用户显式只要求某一组或某个 `分镜ID` 时，只更新命中切片，不补空其他组或镜。
6. 本阶段不得创建第二份 episode/group/shot 根文件；`thinking_chain` 只保留父级摘要，不堆叠全量子角色过程稿。
7. 制作组的创作方法与质量门禁统一以 `.codex/agents/aigc/制作组/_shared/CREATIVE_QUALITY_PLAYBOOK.md` 为真源；单角色 agent 只允许写局部 delta。

## Context Contract (Mandatory)

### 加载顺序

1. `.agents/skills/aigc/SKILL.md + CONTEXT.md`
2. 本 `SKILL.md + CONTEXT.md`
3. `.agents/skills/aigc/_shared/project-runtime-layout.md`
4. `.agents/skills/aigc/3-Detail/_shared/IO_CONTRACT.md`
5. `.agents/skills/aigc/_shared/director_episode_output.schema.json`
6. `projects/<项目名>/0-Init/north_star.yaml`
7. `projects/<项目名>/0-Init/init_handoff.yaml`
8. `projects/<项目名>/0-Init/story-source-manifest.yaml`（若存在）
9. `projects/<项目名>/1-Planning/3-分组/第N集.md`
10. `projects/<项目名>/1-Planning/3-分组/第N集.grouping.json`（若存在）
11. `projects/<项目名>/2-Global/全局风格.md`
12. `projects/<项目名>/2-Global/类型指导.md`
13. `projects/<项目名>/2-Global/导演意图.md`
14. `projects/<项目名>/3-Detail/第N集.json`（若已存在）
15. 仅加载命中的制作组 agent docs

### 四层上下文

1. `global charter context`
   - 根 `AGENTS.md`
   - `.agents/skills/aigc/SKILL.md`
2. `task context`
   - 用户目标、项目名、当前集数、显式约束、命中组/镜范围
3. `role context`
   - 每个 agent 所需的最小领域背景、字段槽位、共享质量门禁与禁止越权项
4. `evidence context`
   - `north_star / init_handoff / story-source-manifest / grouping.md / grouping.json / 2-Global 文档 / 现有 episode JSON`

## Execution Workflow

1. 读取当前 `第N集` 的分组主稿、2-Global 三份文档与初始化种子，锁定是否满足进入条件。
2. 判定 `selected_groups[]`、`selected_agents[]` 与是否需要 bootstrap：
   - 缺根文件或缺 shot skeleton -> 强制命中 `分镜规划`
   - 其余角色按问题类型和用户要求选择，不补空路径
3. 若 `projects/<项目名>/3-Detail/第N集.json` 不存在，先按 bootstrap template 创建空壳，并同步写入 `metadata.episode_id / source_profile / document_phase=detail_in_progress`。
4. 先生成父 skill 的 `mission_brief` 与各角色 `subagent_brief_<role>`，并把共享质量手册中的门禁、回退和 `note / report` 最小合同一并注入。
5. 按 tranche 收集命中角色的 `agents_plan + patch / note / report`：
   - `分镜规划` 先给出 `分镜ID / 时间段 / coverage` 骨架
   - 专业角色再围绕命中组/镜补字段
6. 父 skill 按 `_shared/IO_CONTRACT.md` 的字段合成规则，把 patch 聚合到 shared schema：
   - `metadata`
   - `thinking_chain`
   - `final_output.main_content.分镜组列表[]`
7. 对已存在的 episode 根文件只做命中切片 patch-in-place，不覆盖未命中的集、组、镜。
8. 运行 `连续性复核 -> 真源审计`，确认字段完整、上下游边界正确、无第二真源。
9. 写回 `projects/<项目名>/3-Detail/第N集.json`，并把阶段闭环写到 `projects/<项目名>/3-Detail/validation-report.md`。
10. 返回唯一默认下一入口：`4-Design`。

## Canonical Output Governance (Mandatory)

1. `projects/<项目名>/3-Detail/第N集.json` 是 `3-Detail` 的唯一 canonical 输出。
2. shared schema 固定为 `.agents/skills/aigc/_shared/director_episode_output.schema.json`，父 skill 不得私造第二套字段结构。
3. 本阶段只允许在同一份 `第N集.json` 上 patch-in-place；不得为每个组或每个角色输出平行主稿。
4. `metadata.document_phase` 至少要保持在 `detail_in_progress` 或 `ready`，不得回退为更早阶段。
5. `thinking_chain` 只承载父级收束摘要、证据与判断，不堆叠子角色原始长推理。
6. `4-Design / 5-Image / 6-Video / query / review` 默认只读取这份 root file，不读取并行 sidecar 作为第一真源。

## Field Master

| field_id | 输出位置/字段 | 内容要求 | 默认责任 Step | 质量维度 | 失败码 |
| --- | --- | --- | --- | --- | --- |
| FIELD-DETAIL-01 | 阶段定位 | 明确 `3-Detail` 是 `2-Global` 与下游资产阶段之间的制作明细父级阶段 | S1 | 边界清晰度 | FAIL-DETAIL-01 |
| FIELD-DETAIL-02 | 角色路由 | 明确 `selected_groups[]`、`selected_agents[]` 与 tranche | S2 | 路由完整性 | FAIL-DETAIL-02 |
| FIELD-DETAIL-03 | bootstrap 与 shared I/O | 锁定唯一 episode 根文件、bootstrap 模板与 patch 命名 | S3 | 交接清晰度 | FAIL-DETAIL-03 |
| FIELD-DETAIL-04 | 组级继承 | 组级 `剧本正文 / 组间设计 / source_profile` 正确继承进 episode root | S4 | 上游继承完整性 | FAIL-DETAIL-04 |
| FIELD-DETAIL-05 | 分镜骨架 | `分镜ID / 时间段 / coverage` 稳定、可被专业角色消费 | S5 | shot 骨架稳定性 | FAIL-DETAIL-05 |
| FIELD-DETAIL-06 | 专业字段补全 | `场景及方位 / 角色及站位和穿搭 / 道具及状态 / 分镜表现 / 角色表现 / 运镜手法 / 场景氛围 / 摄影美学 / 转场特效` 补全且不打架 | S6 | 字段可消费性 | FAIL-DETAIL-06 |
| FIELD-DETAIL-07 | 聚合写回 | 父 skill 聚合 patch 并只更新命中切片 | S7 | 聚合可执行性 | FAIL-DETAIL-07 |
| FIELD-DETAIL-08 | 验收闭环 | 返回通过/阻塞、返工入口与下一阶段回接 | S8 | 闭环完整性 | FAIL-DETAIL-08 |

## Thought Pass Map

| step_id | 聚焦字段 | 核心问题 | 生成动作 | 未达标信号 |
| --- | --- | --- | --- | --- |
| S1 | FIELD-DETAIL-01 | 当前是不是 `3-Detail` 阶段问题 | 锁定阶段边界与上下游职责 | 把本阶段写成 `2-Global` 或下游资产阶段 |
| S2 | FIELD-DETAIL-02 | 本轮该调度哪些角色、覆盖哪些组/镜 | 写出 `selected_groups[] / selected_agents[] / tranche` | 多角色并列但没有进入条件 |
| S3 | FIELD-DETAIL-03 | episode 根文件与 bootstrap 规则是什么 | 回指 shared I/O、schema 与 bootstrap template | 又造出第二份主稿或无 bootstrap 规则 |
| S4 | FIELD-DETAIL-04 | 组级上游约束是否正确继承 | 写入组级 `剧本正文 / 组间设计 / source_profile` | 忘记继承 2-Global 或 planning handoff |
| S5 | FIELD-DETAIL-05 | shot skeleton 是否稳定可消费 | 生成 `分镜ID / 时间段 / coverage` 骨架 | 专业角色无从 patch 或镜序漂移 |
| S6 | FIELD-DETAIL-06 | 专业字段如何补全且不冲突 | 聚合多角色字段 patch | 多角色互相覆写、字段空洞或口径打架 |
| S7 | FIELD-DETAIL-07 | 父 skill 如何安全写回 | 只 patch 命中切片并保留其余内容 | 整稿覆盖或越权更新下游 |
| S8 | FIELD-DETAIL-08 | 如何证明本轮完成或阻塞 | 输出 triad closure 与默认下一入口 | 没有返工入口、没有审计结论 |

## Pass Table

| field_id | Pass Standard | Fail Code | Rework Entry |
| --- | --- | --- | --- |
| FIELD-DETAIL-01 | 阶段边界、父子职责与 canonical JSON 明确 | FAIL-DETAIL-01 | S1 |
| FIELD-DETAIL-02 | 角色路由、组/镜命中与 tranche 明确 | FAIL-DETAIL-02 | S2 |
| FIELD-DETAIL-03 | shared schema、bootstrap 与 patch 命名统一 | FAIL-DETAIL-03 | S3 |
| FIELD-DETAIL-04 | 组级信息与 `source_profile` 继承正确 | FAIL-DETAIL-04 | S4 |
| FIELD-DETAIL-05 | `分镜ID / 时间段 / coverage` 稳定且可回链 | FAIL-DETAIL-05 | S5 |
| FIELD-DETAIL-06 | 关键 shot 字段完整、可消费、无明显冲突 | FAIL-DETAIL-06 | S6 |
| FIELD-DETAIL-07 | 父 skill 独占写回，agents 只返 `agents_plan + patch / note / report` | FAIL-DETAIL-07 | S7 |
| FIELD-DETAIL-08 | 返回 triad closure、阻塞说明与 `4-Design` 回接 | FAIL-DETAIL-08 | S8 |

## Root-Cause Execution Contract (Mandatory)

当 `3-Detail` 出现以下问题时，必须先修源层而不是补单次内容：

- `3-Detail` 被当作 active stage，但阶段目录仍是空壳
- 制作组角色文件存在，却全是 0 字节占位
- 多个专业角色直接争夺 `第N集.json` 的最终写回权
- `2-Global` 的组级导演意图没有被稳定投影到 shot-level fields
- 下游又开始读取第二份 detail 主稿而不是 `3-Detail/第N集.json`
- 制作组角色只会做字段分工，却没有稳定的高质量创作方法与质量门禁

必经链路：

`Symptom -> Direct Technical Cause -> Rule Source -> Meta Rule Source -> Fix Landing Points`

优先检查：

- `Rule Source`
  - `.agents/skills/aigc/3-Detail/SKILL.md`
  - `.agents/skills/aigc/3-Detail/_shared/IO_CONTRACT.md`
  - `.codex/agents/aigc/制作组/team.md`
  - `.codex/agents/aigc/制作组/_shared/CREATIVE_QUALITY_PLAYBOOK.md`
  - `.agents/skills/aigc/_shared/director_episode_output.schema.json`
- `Meta Rule Source`
  - `AGENTS.md`
  - `.agents/skills/aigc/SKILL.md`
  - `/Users/vincentlee/.codex/skills/meta/构建/技能/skill-subagents/SKILL.md`

面向用户的闭环固定返回：

1. root cause location
2. immediate fix
3. systemic prevention fix

## Completion Criteria

- 已建立 `3-Detail` 阶段父级真源。
- 已锁定 `3-Detail/第N集.json` 的单一输出口径。
- 已落地制作组 team 与各角色合同。
- 已明确 `2-Global` 只供输入、`3-Detail` 才拥有 episode 根文件写回权。
- 已给出 `4-Design` 的唯一默认回接闭环。
