---
name: aigc
description: Use when operating the repository's core multi-skill AIGC film workflow across project initialization, planning, inter-group directing, detail design, subject design, visuals, video, and post-production stages.
governance_tier: full
---

# aigc

## 概述

`aigc` 是本仓库的核心多子技能组合总合同。

它不是某一个阶段的生产技能，而是整棵 `aigc/` 技能树的总入口、总路由与总闭环，负责把创作项目稳定挂到仓库级 harness 真源上。

它首先回答五件事：

1. 创作项目应该落在哪里
2. 当前应进入哪个阶段
3. 哪些阶段已经具备可执行合同
4. 三省六部分别在这棵树上挂到哪里
5. 任务完成后如何验收、续跑与学习回流

## 使用场景

- 初始化一个新的 AIGC 创作项目
- 在 `projects/<项目名>/` 下推进影视创作主链
- 判断当前任务应该进入 `1-规划`、`2-组间`、`3-明细`、`4-主体`、`5-画面`、`6-视频`、`7-后期` 的哪一个阶段
- 续跑一个中断的创作项目
- 对齐阶段输出、项目状态与仓库级治理合同

## 项目工作区与工件落点

### Canonical Project Root

- 创作项目根目录：`projects/<项目名>/`
- 项目级团队真源：`projects/<项目名>/team.yaml`
- 项目运行时目录：`projects/<项目名>/`，并以此作为 AIGC 项目运行时唯一真源

### Canonical Stage Landing

- `projects/<项目名>/Init/`
- `projects/<项目名>/规划/`
- `projects/<项目名>/编导/`
- `projects/<项目名>/主体/`
- `projects/<项目名>/画面/`
- `projects/<项目名>/视频/`
- `projects/<项目名>/后期/`

说明：

- 技能阶段名仍沿用 `1-规划 / 4-主体 / 5-画面`。
- 项目 runtime 目录不再沿用这些阶段号，统一落为 `规划 / 主体 / 画面`。

### Canonical Runtime Artifacts

- `projects/<项目名>/project_state.yaml`
- `projects/<项目名>/mandate.yaml`
- `projects/<项目名>/mission-brief.yaml`
- `projects/<项目名>/route-plan.yaml`
- `projects/<项目名>/preflight-verdict.yaml`
- `projects/<项目名>/validation-report.md`
- `projects/<项目名>/learning-record.md`

### Shared Runtime Source

- `.agents/skills/aigc/_shared/council-runtime/module-spec.md`
- `.agents/skills/aigc/_shared/project-runtime-layout.md`

## 阶段路由

### 主阶段链

1. `0-Init`
   - 负责项目初始化、项目根目录建立、`north_star` 生成与基础运行时工件创建，并可预建统一 runtime 目录骨架
2. `1-规划`
   - 负责分集、格式、分组、节奏等规划合同，并在 `1-分集` 时首次创建 `编导/第N集.json`
3. `2-组间`
   - 负责全组一致的全局风格、半一致半动态的类型元素，以及按分镜组展开的导演意图，并围绕 `编导/第N集.json` 做组级字段补全
4. `3-明细`
   - 负责围绕分镜组内颗粒度的明细设计，包括分镜表现、角色表现、运镜、氛围、摄影美学与转场设计，并围绕同一份 `编导/第N集.json` 做镜级字段补全
5. `4-主体`
   - 负责主体清单、主体设计、主体审计与主体面板
6. `5-画面`
   - 负责围绕已有文件进行多类型画面提示词组合、一致性处理与图像生成
7. `6-视频`
   - 负责视频生成前的主体参照、分镜参照与视频执行入口
8. `7-后期`
   - 负责最终成片整理、后期收束与交付

### 当前合同覆盖状态

| 阶段 | 目录存在 | 阶段合同状态 | 调度策略 |
| --- | --- | --- | --- |
| `0-Init` | 是 | 已建合同，脚本待补 | 允许显式初始化任务进入，按 `north_star + init_handoff + project-root runtime` 合同执行 |
| `1-规划` | 是 | 已建阶段合同，父子路由已补齐 | 可路由到 `1-分集`、`2-格式`、`3-分组`、`4-节奏` |
| `2-组间` | 是 | 已建阶段合同，三个子路径可执行，并消费 `1-规划/4-节奏` handoff | 可路由到 `全局风格`、`类型元素`、`导演意图` |
| `3-明细` | 是 | 已建阶段合同，`2-角色表现`、`3-运镜手法`、`4-场景氛围`、`5-摄影美学` 与 `6-转场特效` 可执行，其余子路径持续补全 | 可路由到 `2-角色表现`、`3-运镜手法`、`4-场景氛围`、`5-摄影美学`、`6-转场特效`；其他子路径按状态检查 |
| `4-主体` | 是 | 已建阶段合同，四个子路径可路由 | 可路由到 `1-清单`、`2-设计`、`3-审计`、`4-面板` |
| `5-画面` | 是 | 已建阶段合同，支持围绕既有文件进行 `分镜故事板`、`分镜帧`、`漫画` 三类画面生成 | 可路由到 `分镜故事板`、`分镜帧`、`漫画`；整阶段模式默认先入 `分镜故事板` |
| `6-视频` | 是 | 已建阶段合同，`1-提示词蒸馏/全能参照` 与 `1-提示词蒸馏/首帧参照` 可执行，其余子路径待补 | 可路由到 `1-提示词蒸馏/全能参照`、`1-提示词蒸馏/首帧参照`；`首尾帧参照`、`多图参照` 仍按状态检查 |
| `7-后期` | 是 | 搁浅 | 当前不纳入执行链与严格审计失败项；仅保留目录槽位 |

### 子技能调度规则

- 主阶段目录带数字前缀，默认按升序串行
- 主阶段内的 `subtypes/` 若带数字前缀，默认按升序串行
- 无数字前缀的 `subtypes/` 默认并行候选，但仍以各阶段 `SKILL.md` 的显式合同为准
- 若目标阶段或子技能还没有实质合同，必须报告缺口，而不是编造下游步骤

## 三省六部挂载

### 三省

- 中书省
  - 总入口路由
  - 项目初始化起草
  - 阶段进入判定
  - `mandate / mission-brief / route-plan`
- 门下省
  - 阶段进入前预审
  - 审计与否决
  - `preflight-verdict / validation-report / root cause trace`
- 尚书省
  - 阶段执行调度
  - 项目状态与产物维护
  - `projects/<项目名>/` canonical runtime

### 六部

| 六部 | 在 `aigc` 根技能中的挂载 |
| --- | --- |
| 吏部 | `.codex/registry/skills.yaml`、`.codex/registry/routes.yaml` 对 `aigc` 的注册与路由 |
| 户部 | 根 `CONTEXT.md` 与 `projects/<项目名>/project_state.yaml`；必要时镜像到 `.codex/state/tasks/` |
| 礼部 | `.codex/templates/harness/` 与项目级工件合同 |
| 兵部 | 主阶段链与子技能调度 |
| 刑部 | 根验收闭环、主体审计、失败上溯 |
| 工部 | `scripts/`、`.codex/evals/`、后续阶段工具链接入 |

## 强制工作流

1. 确认或创建 `projects/<项目名>/`
2. 在 `projects/<项目名>/` 中建立或读取运行时工件，并检查项目根 `team.yaml` 是否存在。
3. 优先读取 `.agents/skills/aigc/_shared/project-runtime-layout.md`，锁定当前项目的 runtime 根目录映射。
4. 若后续进入 `1-规划 / 2-组间 / 3-明细 / 4-主体`，先加载 `.agents/skills/aigc/_shared/council-runtime/module-spec.md`。
5. 判断当前任务属于初始化、规划、组间、明细、主体、画面、视频或后期中的哪一类
6. 只推荐一个当前主入口阶段，不输出模糊候选列表
7. 若目标阶段合同缺失，停止向下伪造，返回缺口与补建落点
8. 若目标阶段被标记为 `搁浅`，显式返回搁浅状态与恢复前置，不向下生成伪执行链
9. 若目标阶段合同存在，则进入对应阶段或子技能
10. 阶段完成后，把结果写回项目工作区根层运行时工件
11. 输出验收结论与下一步唯一推荐入口

## 硬规则

1. `aigc` 根技能是总控面，不是替代各阶段产物的第二真源。
2. 创作项目的 canonical workspace 必须优先落在 `projects/<项目名>/`。
3. 没有 `mission-brief` 与 `route-plan`，复杂任务不得直接跳入阶段执行。
4. 高风险任务没有 `preflight-verdict`，不得宣布进入正式执行。
5. 对尚未补齐或已搁浅的阶段，必须报告“待补合同/搁浅”，不得伪造其工作流。
6. 子技能经验优先写入最窄作用域；跨阶段经验再晋升到根 `CONTEXT.md`。
7. 对 `1-规划 / 2-组间 / 3-明细 / 4-主体`，若项目根 `team.yaml.enabled == true`，必须先交给共享 `council-runtime` 判定是否启用顾问团运行时。

## 完成标准

当一次 `aigc` 根技能任务结束时，至少应满足以下条件：

- 已明确当前项目根目录
- 已明确当前唯一推荐阶段入口
- 已给出项目级工件落点
- 已说明目标阶段是否具备可执行合同
- 已返回三元闭环：
  - `root cause location`
  - `immediate fix`
  - `systemic prevention fix`

## Root-Cause Execution Contract (Mandatory)

当 `aigc` 技能树出现以下症状时，必须优先修根层合同，而不是直接在单个阶段做局部补丁：

- 目录已建但阶段路由混乱
- 子技能很多，但没有统一入口
- 项目输出散落在 `projects/<项目名>/` 之外
- 阶段合同为空却仍被当作可执行链路
- 项目可以运行，但无法验收、续跑或回流

必经链路：

`Symptom -> Direct Technical Cause -> Rule Source -> Meta Rule Source -> Fix Landing Points`

优先检查：

- `Rule Source`
  - `.agents/skills/aigc/SKILL.md`
  - `.agents/skills/aigc/CONTEXT.md`
  - 各阶段 `SKILL.md` / `CONTEXT.md`
  - `.codex/registry/skills.yaml`
  - `.codex/registry/routes.yaml`
- `Meta Rule Source`
  - 根 `AGENTS.md`
  - 三省六部制元技能

## Field Master

| field_id | 输出位置/字段 | 内容要求 | 默认责任 Step | 质量维度 | 失败码 |
| --- | --- | --- | --- | --- | --- |
| FIELD-AIGC-ROOT-01 | 根技能.任务边界 | 明确 `aigc` 是总入口、总路由、总闭环，而非单阶段技能 | S1 | 根技能定位清晰度 | FAIL-AIGC-ROOT-01 |
| FIELD-AIGC-ROUTE-02 | 根技能.阶段路由 | 给出主阶段链、当前覆盖状态与子技能调度规则 | S2 | 路由完整性 | FAIL-AIGC-ROUTE-02 |
| FIELD-AIGC-LAND-03 | 根技能.工件落点 | 明确 `projects/<项目名>/` 即项目运行时真源，根层工件落点清晰 | S3 | 落点规范性 | FAIL-AIGC-LAND-03 |
| FIELD-AIGC-GOV-04 | 根技能.三省六部挂载 | 说明三省六部如何挂到 `aigc` 总合同 | S4 | 治理映射准确性 | FAIL-AIGC-GOV-04 |
| FIELD-AIGC-CLOSE-05 | 根技能.闭环合同 | 明确验收、续跑、失败上溯与学习回流 | S5 | 闭环完整性 | FAIL-AIGC-CLOSE-05 |

## Thought Pass Map

| step_id | 聚焦字段 | 核心问题 | 生成动作 | 未达标信号 |
| --- | --- | --- | --- | --- |
| S1 | FIELD-AIGC-ROOT-01 | `aigc` 根技能到底是什么 | 锁定总入口、总路由、总闭环定位 | 把根技能写成某个阶段说明 |
| S2 | FIELD-AIGC-ROUTE-02 | 阶段如何串起来 | 定义主阶段链、覆盖状态、调度规则 | 只有目录，没有路由合同 |
| S3 | FIELD-AIGC-LAND-03 | 项目工件落在哪里 | 明确 `projects/<项目名>/` 根层载体 | 输出与状态落点漂移 |
| S4 | FIELD-AIGC-GOV-04 | 治理如何挂到技能树 | 将三省六部映射到根技能 | 只有技能树，没有治理结构 |
| S5 | FIELD-AIGC-CLOSE-05 | 如何验收和回流 | 写闭环、续跑与失败上溯合同 | 能运行但无法结案 |

## Pass Table

| field_id | Pass Standard | Fail Code | Rework Entry |
| --- | --- | --- | --- |
| FIELD-AIGC-ROOT-01 | 根技能定位清楚，能区分总控面与阶段面 | FAIL-AIGC-ROOT-01 | S1 |
| FIELD-AIGC-ROUTE-02 | 主阶段链、阶段状态、子技能规则完整 | FAIL-AIGC-ROUTE-02 | S2 |
| FIELD-AIGC-LAND-03 | 项目工作区与运行时工件落点明确 | FAIL-AIGC-LAND-03 | S3 |
| FIELD-AIGC-GOV-04 | 三省六部挂载明确，无混层 | FAIL-AIGC-GOV-04 | S4 |
| FIELD-AIGC-CLOSE-05 | 有验收、续跑、失败上溯、学习回流合同 | FAIL-AIGC-CLOSE-05 | S5 |

## Context Preload (Mandatory)

- 每次调用本技能时，必须自动加载同目录 `CONTEXT.md`。
- 冲突优先级固定为：用户显式请求 > `AGENTS.md` / 元规则 > 本 `SKILL.md` > `CONTEXT.md`。
- 失败闭环必须回写 `CONTEXT.md`。
- 成功闭环必须回写 `CONTEXT.md`。
