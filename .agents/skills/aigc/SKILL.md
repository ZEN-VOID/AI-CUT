---
name: aigc
description: Use when operating the repository's core multi-skill AIGC film workflow across project initialization, reinitialization, planning, inter-group directing, detail design, subject design, visuals, video, and post-production stages.
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

## 当前改造模式

- 当前 `aigc` 根技能已切换到 `bootstrap_compat` 改造窗口。
- 在这个窗口内，harness 对 `aigc` 根技能固定的真源只有四类：
  - `projects/aigc/<项目名>/` 项目 runtime 与根层治理工件
  - `.codex/registry/skills.yaml` / `.codex/registry/routes.yaml` 的根注册与路由入口
  - `query / resume / review` 三个根级卫星技能入口
  - 高风险任务的 `preflight-verdict` 与完成闭环的 `validation-report`
- 在这个窗口内，主阶段链、阶段状态表与子路径说明仍然可用，但它们默认视为“路由投影”，不是冻结的阶段内部 schema；后续重大改造可重写阶段内合同，只要不破坏上述根层真源。
- 若旧的阶段细节合同与当前重构目标冲突，优先保住项目 runtime、治理 carriers 与 review gate，再以目标阶段的当前显式本地合同为准。

## 使用场景

- 初始化一个新的 AIGC 创作项目
- 对已初始化项目执行“回到初始化态重来”的重置式重新初始化
- 在 `projects/aigc/<项目名>/` 下推进影视创作主链
- 判断当前任务应该进入 `1-Planning`、`2-Global`、`3-Detail`、`4-Design`、`5-Image`、`6-Video`、`7-Cut` 的哪一个阶段
- 查询某个 AIGC 项目的 runtime 真源、阶段产物、编导根文件、设计/画面/视频资产与治理工件
- 续跑一个中断的创作项目
- 对某个阶段或整个项目执行门下省侧预审、验收、`validation-report.md` 更新与学习桥接
- 对齐阶段输出、项目状态与仓库级治理合同

## 项目工作区与工件落点

### Canonical Project Root

- 创作项目根目录：`projects/aigc/<项目名>/`
- 项目级团队真源：`projects/aigc/<项目名>/team.yaml`
- 项目运行时目录：`projects/aigc/<项目名>/`，并以此作为 AIGC 项目运行时唯一真源

### Canonical Stage Landing

- `projects/aigc/<项目名>/0-Init/`
- `projects/aigc/<项目名>/Story/`
- `projects/aigc/<项目名>/1-Planning/`
- `projects/aigc/<项目名>/2-Global/`
- `projects/aigc/<项目名>/3-Detail/`
- `projects/aigc/<项目名>/4-Design/`
- `projects/aigc/<项目名>/5-Image/`
- `projects/aigc/<项目名>/6-Video/`
- `projects/aigc/<项目名>/7-Cut/`

说明：

- 技能阶段名仍沿用当前技能树口径，如 `1-Planning / 4-Design / 5-Image`。
- 项目 runtime 目录以 `.agents/skills/aigc/_shared/project-runtime-layout.md` 为唯一真源；当前 `4-Design` 不再回退到旧的 `主体/` 目录。

### Canonical Runtime Artifacts

- 核心运行时工件：
  - `projects/aigc/<项目名>/project_state.yaml`
- 惰性治理工件：
  - `projects/aigc/<项目名>/governance-state.yaml`
  - `projects/aigc/<项目名>/mandate.yaml`
  - `projects/aigc/<项目名>/mission-brief.yaml`
  - `projects/aigc/<项目名>/route-plan.yaml`
  - `projects/aigc/<项目名>/preflight-verdict.yaml`
  - `projects/aigc/<项目名>/validation-report.md`
  - `projects/aigc/<项目名>/learning-record.md`

### Shared Runtime Source

- `.agents/skills/aigc/_shared/council-runtime/module-spec.md`
- `.agents/skills/aigc/_shared/project-runtime-layout.md`

### Quality Evidence Source

- `.agents/skills/aigc/benchmark-suite.yaml`

## 阶段路由

### 主阶段链

1. `0-Init`
   - 负责项目初始化、项目根目录建立、`north_star` 生成与基础运行时工件创建，并按 shared runtime layout 预建阶段根目录与 active child skeleton
2. `1-Planning`
   - 负责分集、格式、分组、节奏等规划合同，并在规划期登记 `bootstrap_output` 目标路径与 `source_profile` handoff
3. `2-Global`
   - 负责全项目共用的全局风格、类型元素、设计元素，以及按集按组展开的导演意图等全局设计真源；其中 `设计元素` 负责服装与建筑场景的时代化定调，阶段末段仍由可写入 shared root 的链路把 `组间设计` seed 写入 `第N集.json`，作为 `3-Detail` 的导演前置结构化合同
4. `3-Detail`
   - 负责围绕分镜组内颗粒度的明细设计，包括分镜表现、角色表现、运镜、氛围、摄影美学与转场设计；当前已改为单技能知行合一并发链，在父 `SKILL.md` 内部融合原制作组能力并继续补齐 shared `3-Detail/第N集.json`
5. `4-Design`
   - 负责场景、角色、服装、道具的清单、设计与面板阶段
6. `5-Image`
   - 负责围绕已有文件进行多类型画面提示词组合、一致性处理与图像生成
7. `6-Video`
   - 负责视频生成前的设计/画面参照、分镜参照与视频执行入口
8. `7-Cut`
   - 负责最终成片整理、后期收束与交付

### 根级卫星技能

- `query`
  - 根级事实查询卫星技能
  - 默认挂在尚书省执行侧，治理分域偏 `户部`
  - 负责围绕 `projects/aigc/<项目名>/` 读取项目状态、阶段产物、`3-Detail` 主文件、资产落点与治理工件，不改写业务真源
- `resume`
  - 根级续跑恢复卫星技能
  - 默认挂在尚书省执行侧，治理分域偏 `兵部`
  - 负责重建最后稳定入口、检查治理工件缺口、提出安全恢复方案，并把任务回接到根技能或目标阶段；不处理“主动回到初始化态重来”
- `review`
  - 根级复核承接卫星技能
  - 默认挂在门下省复核侧，治理分域偏 `刑部`
  - 负责 `preflight-verdict.yaml`、`validation-report.md` 与 `learning-record.md` 的 project/stage review bridge，不替代阶段执行

卫星技能默认关系：

- 三个卫星技能与根 `aigc` 同根同级，不并入主阶段串行链。
- `query` 只拥有检索与证据综合权，不拥有项目或阶段内容真源改写权。
- `resume` 只拥有恢复裁决与回接权，不拥有伪造断点或跳过治理 gate 的权力。
- `review` 只拥有门下省侧预审/验收/学习桥接权，不拥有阶段执行或内容生成权。

### 当前合同覆盖状态

| 阶段 | 目录存在 | 阶段合同状态 | 调度策略 |
| --- | --- | --- | --- |
| `0-Init` | 是 | 已建合同，脚本待补 | 允许显式初始化任务进入，按 `north_star + init_handoff + project-root runtime` 合同执行 |
| `1-Planning` | 是 | 已建阶段合同，`1-分集` 直达 leaf 执行，`2-格式` 与 `3-分组` 已内化原规划组能力 | 可先执行 `1-分集`，再路由到 `2-格式`、`3-分组`，并按需触发节奏复核 gate |
| `2-Global` | 是 | 已建阶段合同，当前 active 子技能至少包含 `全局风格 / 类型元素 / 设计元素`，并继续消费 `1-Planning/3-分组` handoff；`导演意图` 仍保留为后续组级导演链路 | 写入 `全局风格/全局风格设计.md`、`类型元素/全集设计.md + 分组设计.md`、`设计元素/设计元素.md`，并由组级导演链路继续 seed shared `第N集.json` 的 `组间设计` |
| `3-Detail` | 是 | 已建阶段合同，采用单技能知行合一并发链，在父 skill 内部融合分镜表现、角色表现、运镜手法、场景氛围、摄影美学与转场特效能力 | 先进入 `.agents/skills/aigc/3-Detail/SKILL.md`，再按内部 capability route 判定 `selected_groups[] / selected_fields[] / selected_chains[]` |
| `4-Design` | 是 | 已建阶段合同，四个子路径可路由 | 可路由到 `1-清单`、`2-设计`、`3-审计`、`4-面板` |
| `5-Image` | 是 | 已建阶段合同，支持围绕既有文件进行 `分镜故事板`、`分镜帧`、`漫画` 三类画面生成 | 可路由到 `分镜故事板`、`分镜帧`、`漫画`；整阶段模式默认先入 `分镜故事板` |
| `6-Video` | 是 | 已建阶段合同，`1-提示词蒸馏/全能参照`、`1-提示词蒸馏/首帧参照` 与 `2-视频生成` 可执行，其余子路径待补 | 可路由到 `1-提示词蒸馏/全能参照`、`1-提示词蒸馏/首帧参照`、`2-视频生成`；`首尾帧参照`、`多图参照` 与未来一致性处理路径仍按状态检查 |
| `7-Cut` | 是 | 搁浅 | 当前不纳入执行链与严格审计失败项；仅保留目录槽位 |

### 卫星技能覆盖状态

| 卫星技能 | 目录存在 | owner_office | 治理分域 | 合同状态 | 默认职责 |
| --- | --- | --- | --- | --- | --- |
| `query` | 是 | `shangshu` | `户部` | active | runtime / project / artifact / governance truth retrieval |
| `resume` | 是 | `shangshu` | `兵部` | active | interruption recovery / safe re-entry / governance artifact repair |
| `review` | 是 | `menxia` | `刑部` | active | preflight / validation / learning bridge |

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
  - `projects/aigc/<项目名>/` canonical runtime

### 六部

| 六部 | 在 `aigc` 根技能中的挂载 |
| --- | --- |
| 吏部 | `.codex/registry/skills.yaml`、`.codex/registry/routes.yaml` 对 `aigc` 的注册与路由 |
| 户部 | 根 `CONTEXT.md`、`projects/aigc/<项目名>/project_state.yaml` 与 `projects/aigc/<项目名>/governance-state.yaml`；必要时镜像到 `.codex/state/tasks/`；`query` 负责读取与综合证据 |
| 礼部 | `.codex/templates/harness/` 与项目级工件合同 |
| 兵部 | 主阶段链与子技能调度；`resume` 负责续跑与恢复回接 |
| 刑部 | 根验收闭环、阶段审计、失败上溯；`review` 负责门下省侧 preflight / validation / learning bridge |
| 工部 | `scripts/`、`.codex/evals/`、后续阶段工具链接入 |

## 强制工作流

1. 确认或创建 `projects/aigc/<项目名>/`
2. 在 `projects/aigc/<项目名>/` 中建立或读取运行时工件，并检查项目根 `team.yaml`、`project_state.yaml`、`governance-state.yaml` 是否存在。
3. 优先读取 `.agents/skills/aigc/_shared/project-runtime-layout.md`，锁定当前项目的 runtime 根目录映射。
4. 若后续进入 `1-Planning / 2-Global / 3-Detail / 4-Design`，先加载 `.agents/skills/aigc/_shared/council-runtime/module-spec.md`。
5. 判断当前任务属于首次初始化、重置式重新初始化、规划、组间、明细、设计、画面、视频、后期，还是 `query / resume / review` 卫星诉求中的哪一类
6. 只推荐一个当前主入口阶段或卫星技能，不输出模糊候选列表
7. 若目标阶段合同缺失，停止向下伪造，返回缺口与补建落点
8. 若目标阶段被标记为 `搁浅`，显式返回搁浅状态与恢复前置，不向下生成伪执行链
9. 若命中卫星技能，则先进入对应卫星技能，再按其合同回接根技能或目标阶段
10. 若目标阶段合同存在，则进入对应阶段或子技能
11. 阶段或卫星动作完成后，把结果写回项目工作区根层运行时工件
12. 输出验收结论与下一步唯一推荐入口

## 硬规则

1. `aigc` 根技能是总控面，不是替代各阶段产物的第二真源。
2. 创作项目的 canonical workspace 必须优先落在 `projects/aigc/<项目名>/`。
3. 当前 `bootstrap_compat` 模式下，不得把旧阶段细节合同当作冻结真源去阻断 `aigc` 系列重构；需要保留的是根 runtime、治理工件与 review gate。
4. 没有 `mission-brief` 与 `route-plan`，复杂任务不得直接跳入阶段执行。
5. 高风险任务没有 `preflight-verdict`，不得宣布进入正式执行。
6. 对尚未补齐或已搁浅的阶段，必须报告“待补合同/搁浅”，不得伪造其工作流。
7. 子技能经验优先写入最窄作用域；跨阶段经验再晋升到根 `CONTEXT.md`。
8. 对 `1-Planning / 2-Global / 3-Detail / 4-Design`，若项目根 `team.yaml.enabled == true`，必须先交给共享 `council-runtime` 判定是否启用顾问团运行时。
9. 根级卫星技能不得冒充新的主阶段；`query` 读真源、`resume` 接续跑、`review` 做门下省桥接，各自边界必须显式保持。
10. `review` 只承接 preflight / validation / learning 侧治理工件，不得替代尚书省执行或各阶段内容生成。
11. `resume` 不得伪造断点状态、不得跳过 `mission-brief / route-plan / preflight-verdict` 等硬 gate；缺治理工件时优先回到根技能补齐。
12. `project_state.yaml` 是轻量起盘的默认治理入口；`governance-state.yaml` 负责按需补上的结构化断点、治理缺口与 review/resume 同步。两者不得各自演化成平行真源。
13. 用户若明确要求“回到初始化态 / 重新起盘 / 推翻当前方向重来”，根路由必须回 `0-Init`；不得把这类诉求误判为 `resume` 的续跑恢复。

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
- 项目输出散落在 `projects/aigc/<项目名>/` 之外
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
| FIELD-AIGC-LAND-03 | 根技能.工件落点 | 明确 `projects/aigc/<项目名>/` 即项目运行时真源，根层工件落点清晰 | S3 | 落点规范性 | FAIL-AIGC-LAND-03 |
| FIELD-AIGC-GOV-04 | 根技能.三省六部挂载 | 说明三省六部如何挂到 `aigc` 总合同 | S4 | 治理映射准确性 | FAIL-AIGC-GOV-04 |
| FIELD-AIGC-CLOSE-05 | 根技能.闭环合同 | 明确验收、续跑、失败上溯与学习回流 | S5 | 闭环完整性 | FAIL-AIGC-CLOSE-05 |

## Thought Pass Map

| step_id | 聚焦字段 | 核心问题 | 生成动作 | 未达标信号 |
| --- | --- | --- | --- | --- |
| S1 | FIELD-AIGC-ROOT-01 | `aigc` 根技能到底是什么 | 锁定总入口、总路由、总闭环定位 | 把根技能写成某个阶段说明 |
| S2 | FIELD-AIGC-ROUTE-02 | 阶段如何串起来 | 定义主阶段链、覆盖状态、调度规则 | 只有目录，没有路由合同 |
| S3 | FIELD-AIGC-LAND-03 | 项目工件落在哪里 | 明确 `projects/aigc/<项目名>/` 根层载体 | 输出与状态落点漂移 |
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
