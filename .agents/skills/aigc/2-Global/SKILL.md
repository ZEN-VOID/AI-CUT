---
name: aigc-global
description: Use when the global directing stage needs one root skill to write `projects/aigc/<项目名>/2-Global/episode_root.json` directly from planning grouping outputs and init presets, then hand off stable group-level seeds to `3-Detail`.
governance_tier: full
---

# aigc 2-Global

## Context Loading Contract

- 每次调用本技能时，必须同时加载同目录 `CONTEXT.md` 作为预加载上下文。
- 若同目录 `CONTEXT.md` 缺失，应先补齐最小知识库骨架，或向用户明确报告阻塞；不得在未检查该上下文的情况下执行技能。
- 冲突优先级：用户显式请求 > 仓库/全局 `AGENTS.md` > 本 `SKILL.md` > 同目录 `CONTEXT.md`。

## 概述

`2-Global` 是 `1-Planning` 与 `3-Detail` 之间的导演前置收束阶段。

从本轮开始，它默认采用与 `3-Detail` 一致的输出机制，并把“如何填好 `.agents/skills/aigc/2-Global/_shared/episode_root.json`”作为核心执行问题：

- 直接把结果写入单一 JSON 根文件 `projects/aigc/<项目名>/2-Global/episode_root.json`
- `episode_root.json` 是本阶段唯一业务真源
- `全局风格.md / 全集类型元素.md / 分组类型元素.md / 导演意图.md` 不再是默认 canonical 输出；若旧下游暂时仍依赖它们，只能作为由 JSON 派生的兼容投影

## Skill Execution Rule (Mandatory)

`2-Global` 采用“单技能内部生成 + 单一 JSON 直写 + 可选前置监制 advisory”模式：

- skill 自身负责输入读取、业务分析、约束裁决、字段生成、`episode_root.json` 直接写回、验收与下游回接
- `全局风格`、`全集类型元素`、`分组类型元素`、`导演意图` 的生成都内收在父 skill 内部，不再通过外置导演组 contracts 生成真源
- 若项目根 `team.yaml.enabled == true` 且当前阶段命中 `roles.supervision`，只允许在直写前消费 shared `council-runtime` 的前置 advisory；首次落盘后的收尾回到阶段审计/验收层，不再由 `监制` 执行
- 兼容投影若被生成，也只能由已确认 JSON 派生，不得反向夺取真源地位

## When to Use

- 已经有 `projects/aigc/<项目名>/1-Planning/3-分组/第N集.md`，需要进入导演前置全局合同阶段。
- 需要把初始化预设、规划分组结果与当前项目定位直接沉淀为组级 seed root，并交给 `3-Detail` 继续细化。
- 需要把项目级风格与类型总则、组级类型信号与导演意图一次性收进同一颗 JSON 树，而不是先写多份长文再二次抽取。

## When Not to Use

- 当前连 `projects/aigc/<项目名>/1-Planning/3-分组/第N集.md` 都不存在。
- 当前任务仍是分集、剧本或分组问题，应回到 `1-Planning`。
- 当前任务已经在补镜级字段、主体、设计、画面或视频产物，应进入 `3-Detail / 4-Design / 5-Image / 6-Video`。

## Business Requirement Analysis Contract (Mandatory)

| analysis_slot | 当前结论 |
| --- | --- |
| `business_goal` | 将规划分组结果与初始化预设直接收束为 `projects/aigc/<项目名>/2-Global/episode_root.json`，并把稳定组级 seed 交给 `3-Detail` |
| `business_object` | `0-Init` 的项目基线、`1-Planning` 的当前集分组正文、已有 `episode_root.json`、项目根 `team.yaml`（若存在） |
| `constraint_profile` | `episode_root.json` 必须同时承载 `meta`、项目级 `project_global`、以及 `groups[].global`；`global.剧本正文` 必须完整整理自命中组正文；不得在本阶段发明 shot-level 字段；兼容 Markdown 若被生成，只能由 JSON 派生 |
| `success_criteria` | `episode_root.json` 已稳定写入 `meta + project_global + groups[].global`，其中 `全局风格 / 类型元素 / 导演意图` 对下游可消费、可追溯、可增量 patch；`validation-report.md` 已记录验收与阻塞 |
| `non_goals` | 不生成 shot-level 明细；不把本阶段写成平行长文流水线；不再维护第二套导演组 agent 真源 |
| `complexity_source` | 项目级稳定项与当前集组级增量并存；类型总则与组级打法要分层；又要保证 JSON 结构能直接给 `3-Detail` 消费 |
| `topology_fit` | 串行锁输入与不变量，中段按“全局风格 + 全集类型 + 分组类型 + 导演意图”形成同一 JSON 根，后段统一审计与会审 |
| `step_strategy` | 采用“输入锁定 -> 项目级约束 -> 组级导演判断 -> JSON 直写 -> 验收”的固定主链；若有 `监制`，只以前置 advisory 方式介入 |

## Context Preload (Mandatory)

加载顺序固定为：

1. 根 `AGENTS.md`
2. `.agents/skills/aigc/SKILL.md + CONTEXT.md`
3. 本 `SKILL.md + CONTEXT.md`
4. `.agents/skills/aigc/_shared/project-runtime-layout.md`
5. `.agents/skills/aigc/_shared/group_design_seed_contract.md`
6. `.agents/skills/aigc/2-Global/_shared/IO_CONTRACT.md`
7. `.agents/skills/aigc/2-Global/_shared/branch-output-contract.md`
8. `.agents/skills/aigc/2-Global/_shared/episode_root.json`
9. `.agents/skills/aigc/_shared/council-runtime/module-spec.md`
10. `.agents/skills/aigc/_shared/council-runtime/team.template.yaml`
11. `projects/aigc/<项目名>/team.yaml`（若存在）
12. `projects/aigc/<项目名>/0-Init/north_star.yaml`
13. `projects/aigc/<项目名>/0-Init/init_handoff.yaml`
14. `projects/aigc/<项目名>/0-Init/story-source-manifest.yaml`（若存在）
15. `projects/aigc/<项目名>/1-Planning/2-格式/第N集.md`（若存在）
16. `projects/aigc/<项目名>/1-Planning/3-分组/第N集.md`
17. `projects/aigc/<项目名>/1-Planning/3-分组/执行报告.md`（若存在）
18. `projects/aigc/<项目名>/2-Global/episode_root.json`（若存在）
19. `projects/aigc/<项目名>/2-Global/validation-report.md`（若存在）

## Shared Canonical Sources (Mandatory)

- 强制读取：`.agents/skills/aigc/2-Global/_shared/IO_CONTRACT.md`
- 强制读取：`.agents/skills/aigc/2-Global/_shared/branch-output-contract.md`
- 强制读取：`.agents/skills/aigc/_shared/project-runtime-layout.md`
- 强制读取：`.agents/skills/aigc/_shared/group_design_seed_contract.md`
- 强制读取：`.agents/skills/aigc/2-Global/_shared/episode_root.json`
- 强制读取：`.agents/skills/aigc/_shared/council-runtime/module-spec.md`
- 强制读取：`.agents/skills/aigc/_shared/council-runtime/team.template.yaml`

硬规则：

1. 本阶段的第一输入根固定为 `projects/aigc/<项目名>/1-Planning/3-分组/第N集.md`。
2. 项目级稳定约束优先来自 `0-Init/north_star.yaml`、`0-Init/init_handoff.yaml` 与 `story-source-manifest.yaml`。
3. `episode_root.json` 是本阶段唯一 canonical 业务载体。
4. 本阶段必须把完整组级 seed 写入 `episode_root.json`，并同步维护 `meta.剧名 / 集数 / 组数 / 总时长`、`project_global.*` 与 `groups[].分镜组ID / global.剧本正文 / global.*`。
5. `groups[].global.剧本正文` 必须完整整理自 `1-Planning/3-分组/第N集.md` 的命中组正文，除组号标题外不得二次摘要。
6. `groups[].global.全局风格 / 类型元素 / 导演意图` 必须由本阶段直接定稿写入 JSON，不允许先写 Markdown 再抽取。
7. 兼容投影若存在，只能由 JSON 派生；不得出现“Markdown 一套、JSON 一套”的双真源。

## Total Input Contract (Mandatory)

### 必需输入

- `projects/aigc/<项目名>/1-Planning/3-分组/第N集.md`
- `projects/aigc/<项目名>/0-Init/north_star.yaml`
- `projects/aigc/<项目名>/0-Init/init_handoff.yaml`

### 可选输入

- `projects/aigc/<项目名>/0-Init/story-source-manifest.yaml`
- `projects/aigc/<项目名>/1-Planning/2-格式/第N集.md`
- `projects/aigc/<项目名>/1-Planning/3-分组/执行报告.md`
- `projects/aigc/<项目名>/team.yaml`
- `projects/aigc/<项目名>/2-Global/episode_root.json`
- 用户显式指定的风格、类型或导演偏好

### 禁止输入

- 与当前项目无关的外部参考文本
- 要求本阶段直接写 shot-level 字段或镜头 JSON 的额外指令
- 任何外置导演组 team、agent、creative method 文档作为业务真源

## Internal Capability Fusion Contract (Mandatory)

| 能力面 | 作用 | 典型输出 | 何时触发 |
| --- | --- | --- | --- |
| `global_style_engine` | 从项目级证据中提炼稳定的媒介属性、渲染底座、摄影级总体属性与禁区 | `project_global.全局风格` | 每次进入 `2-Global` 时 |
| `type_bible_engine` | 提炼项目级类型总则、观众合同与下游边界 | `project_global.全集类型元素` | 每次进入 `2-Global` 时 |
| `group_type_engine` | 将当前集各组转译为组级类型信号 | `groups[].global.类型元素` | 当前集分组稳定后 |
| `director_intent_engine` | 生成各组导演意图与 detail 放大方向 | `groups[].global.导演意图` | 当前集分组稳定后 |
| `json_writeback_engine` | 把项目级与组级结果、完整组正文与 meta 一次性写入 `episode_root.json` | `episode_seed_patch` | 上游字段稳定后 |
| `convergence_audit_engine` | 校验 JSON 结构、边界、长度窗与下游可消费性 | `convergence_report`、`writeback_patch_set` | 写回前必须触发 |
| `supervision_council_engine` | 对已落盘 JSON 与阶段验收报告做 stage-end 会审 | `supervision_report`、`supervision_patch_set` | `team.yaml` 启用时 |

硬规则：

1. 上述能力面全部内收在当前 `SKILL.md`，不是外置真源。
2. 任何能力面都不得绕过父 skill 直接写平行 canonical 文件。
3. 若后续仍需兼容 `全局风格.md` 等文件，它们只能从当前 JSON 派生，不得反向驱动 JSON。

## Field Master

| field_id | target_path | owner_pass | requirement |
| --- | --- | --- | --- |
| `FIELD-GLOBAL-01` | `meta.剧名 / 集数 / 组数 / 总时长` | `5-组正文入壳` | 必须与当前项目和当前集严格一致 |
| `FIELD-GLOBAL-02` | `project_global.全局风格` | `1-项目级风格` | 形成项目级统一风格前缀 |
| `FIELD-GLOBAL-03` | `project_global.全集类型元素` | `2-项目级类型` | 形成项目级类型总则 |
| `FIELD-GLOBAL-04` | `groups[].分镜组ID / global.剧本正文` | `5-组正文入壳` | 保留命中组原始正文与组标识 |
| `FIELD-GLOBAL-05` | `groups[].global.全局风格` | `1-项目级风格` | 默认继承项目级风格前缀 |
| `FIELD-GLOBAL-06` | `groups[].global.类型元素` | `3-组级类型` | 对齐当前组的类型信号 |
| `FIELD-GLOBAL-07` | `groups[].global.导演意图` | `4-导演意图` | 对齐当前组的导演执行导向 |
| `FIELD-GLOBAL-08` | `validation-report.md` | `6-验收` | 写回验收、阻塞与根因上溯 |

## Thought Pass Map

| pass_id | step_name | input | output |
| --- | --- | --- | --- |
| `P1` | `1-项目级风格` | `north_star / init_handoff / team.yaml` | `project_global.全局风格`、`groups[].global.全局风格` |
| `P2` | `2-项目级类型` | `north_star / init_handoff / 第N集分组正文` | `project_global.全集类型元素` |
| `P3` | `3-组级类型` | `project_global.全集类型元素`、`第N集分组正文` | `groups[].global.类型元素` |
| `P4` | `4-导演意图` | `第N集分组正文`、`project_global.*`、`groups[].global.类型元素` | `groups[].global.导演意图` |
| `P5` | `5-组正文入壳` | `第N集分组正文`、全部已定稿字段 | `episode_root.json` |
| `P6` | `6-验收` | `episode_root.json` | `validation-report.md` |

## Pass Table

| pass | direct_write_target | hard_gate |
| --- | --- | --- |
| `1-项目级风格` | `project_global.全局风格`、`groups[].global.全局风格` | 不得写成具体镜头操作或工具参数 |
| `2-项目级类型` | `project_global.全集类型元素` | 不得混入某一组的临场打法 |
| `3-组级类型` | `groups[].global.类型元素` | 必须逐组对齐，不得跨组混写 |
| `4-导演意图` | `groups[].global.导演意图` | 必须可被 `3-Detail` 直接消费 |
| `5-组正文入壳` | `meta`、`groups[].分镜组ID`、`groups[].global.剧本正文` | 必须完整保留命中组正文 |
| `6-验收` | `validation-report.md` | 必须记录阻塞、根因上溯与下一阶段回接 |

## Direct JSON Writeback Contract (Mandatory)

`episode_root.json` 最低必须满足：

- `meta`
  - `剧名`
  - `集数`
  - `组数`
  - `总时长`
- `project_global`
  - `全局风格`
  - `全集类型元素`
- `groups[]`
  - `分镜组ID`
  - `global.剧本正文`
  - `global.全局风格`
  - `global.类型元素`
  - `global.导演意图`

字段规则：

1. `project_global.全局风格` 与 `groups[].global.全局风格` 默认保持同值，便于 `3-Detail` 与旧下游直接读取。
2. `project_global.全集类型元素` 只承载项目级类型总则。
3. `groups[].global.类型元素` 与 `groups[].global.导演意图` 必须严格对齐当前 `分镜组ID`。
4. `groups[].global.剧本正文` 必须完整整理命中组全文。
5. 当前阶段不得新增 `detail`、`分镜列表`、`分镜数` 或任何镜级字段。

## One-Shot Output Contract (Mandatory)

`2-Global` 的一次性输出固定为：

1. `projects/aigc/<项目名>/2-Global/episode_root.json`
   - 唯一业务真源
2. `projects/aigc/<项目名>/2-Global/validation-report.md`
   - 记录本轮验收、阻塞、根因上溯与 closure
3. `advisory note`
   - 若项目根 `team.yaml` 启用且当前阶段命中 `roles.supervision`，只需记录前置 advisory 是否被读取、其要点与是否采纳
4. `closure triad + handoff note`
   - 说明 `root cause location / immediate fix / systemic prevention fix`
   - 给出下一入口固定为 `3-Detail`
5. 可选兼容投影
   - 仅当旧下游明确需要时，允许从 JSON 派生 `全局风格.md / 全集类型元素.md / 分组类型元素.md / 导演意图.md`
   - 这些投影不拥有真源地位

## Canonical Output Governance (Mandatory)

1. `episode_root.json` 是本阶段唯一 canonical 业务载体。
2. `validation-report.md` 是本阶段唯一 stage 验收载体。
3. 若生成兼容 Markdown，它们只能由 JSON 派生，不得先写 Markdown 再回填 JSON。
4. `全局风格` 必须服务统一画面风格锚定，不得混入具体镜头操作、具体景别或工具参数。
5. `全集类型元素` 只写项目级类型总则，不得混入当前组临场打法。
6. `类型元素` 与 `导演意图` 都必须对齐当前 `分镜组ID`。
7. `episode_root.json` 的 `groups[].global.*` 由当前 skill 聚合写入，但本阶段不得发明 shot-level 字段。
8. 首次落盘后的审计与验收必须回到阶段自己的 `validation-report.md` / audit 机制；不得再把 `监制` 用作 stage-end refine 的 owner。

## Acceptance Checklist (Mandatory)

完成本技能前，必须确认：

1. `projects/aigc/<项目名>/2-Global/episode_root.json` 已落盘。
2. `meta + project_global + groups[].global` 结构完整。
3. `groups[].global.剧本正文` 是完整组正文，不是摘要。
4. `groups[].global.类型元素 / 导演意图` 与命中组严格对齐。
5. `projects/aigc/<项目名>/2-Global/validation-report.md` 已写回，或明确记录阻塞。
6. 下一阶段固定回接到 `projects/aigc/<项目名>/3-Detail/`。

## Root-Cause Execution Contract (Mandatory)

若本阶段失败，必须按以下格式上溯：

1. `Symptom`
2. `Direct Cause`
3. `Rule Source`
4. `Meta Rule Source`

最小上溯样式：

- `Symptom`: `episode_root.json` 字段缺失、跨组混写、或把组正文写成摘要
- `Direct Cause`: `json_writeback_engine` 未锁定字段边界，或把兼容投影误当真源
- `Rule Source`: 本 `SKILL.md` 的 `Direct JSON Writeback Contract / Canonical Output Governance`
- `Meta Rule Source`: 根 `AGENTS.md` 的 `LLM-first creative authorship`、`执行深度默认规则`、`复合型技能输出治理合同`
