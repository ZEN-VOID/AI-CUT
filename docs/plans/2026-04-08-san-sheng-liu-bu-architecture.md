# AIGC-FILM 三省六部制初始化架构包

## 1. 任务模式与目标边界

- 当前模式：`改造升级`
- 原因：当前仓库已经具备 `AGENTS.md`、`.codex/`、`.agents/`、`PRPs/`、`scripts/` 等治理骨架，但仍处于“制度真源刚开始收束、前代发源尚未完全显式继承”的初始化阶段。
- 前代发源仓库：`/Volumes/AIGC/AIGC-ZEN-VOID`
- 本轮目标：把当前仓库初始化为面向 AIGC 影视创作全流程的治理底座，而不是先堆业务技能或零散脚本。
- 本轮边界：
  - 建立三省治理层的最小角色合同
  - 建立六部能力层的最小挂载真源
  - 建立任务工件、状态、评测、审计的最小闭环
  - 明确从 `AIGC-ZEN-VOID` 迁移什么，不迁移什么

## 2. 现状诊断与 Layered Trace

### 2.1 现状症状

| 现状对象 | 观察到的症状 | 风险 |
| --- | --- | --- |
| 根层治理 | `AGENTS.md` 已较完整，但与之配套的三省角色、任务工件、运行状态与评测入口仍在初始化中 | 规则容易停留在宣言层 |
| `.codex/` | 已有 commands、templates、rules 基础骨架，但需要通过 registry、runbook、state、evals 才能形成治理真源 | 后续新增 skill / agent 容易漂移 |
| `.agents/skills/` | repo-local 影视技能体系仍未正式展开 | 容易退化为临时命令与人工记忆 |
| 发源承接 | 当前仓库需要接续 `AIGC-ZEN-VOID`，但必须避免无治理地整仓复制 | 继承可能失控 |

### 2.2 Layered Trace

| Symptom | Direct Technical Cause | Rule Source | Meta Rule Source | Fix Landing Points |
| --- | --- | --- | --- | --- |
| 仓库有治理说明，但还不能稳定支撑影视全流程编排 | 缺三省角色合同、工件模板、状态目录与审计脚本 | 当前 `.codex/` 仍是 starter 级骨架 | 根 `AGENTS.md` 与三省六部制元技能都要求“角色、工件、状态、验收”同落盘 | `.codex/agents/`、`.codex/registry/`、`.codex/runbooks/`、`.codex/state/`、`.codex/evals/`、`scripts/aigc_harness_audit.py` |
| 需要承接 `AIGC-ZEN-VOID`，但不能直接搬旧仓 | 前代结构仍主要存在于外部仓库 | 缺 legacy mapping 与迁移路由文档 | 元规则要求旧改必须先做现状诊断、目标态与迁移计划 | 本架构包与 `.codex/registry/routes.yaml` |

### 2.3 根因判断

- 根因位置：当前仓库的问题不是“没有规则”，而是“规则已有、真源刚建立、继承尚需制度化”。
- 立即修复：先补治理底座，再引入具体影视 skill / workflow。
- 系统预防修复：把后续扩展统一收敛到 `registry + runbooks + state + evals + agents + templates` 六类真源。

## 3. 宪章层设计

### 3.1 全局优先级

1. 用户显式请求
2. 根 `AGENTS.md`
3. 三省角色合同
4. 六部注册与路由合同
5. 任务工件与运行状态真源
6. 技能与经验层

### 3.2 任务进入条件

- 复杂影视任务不得直接进入执行，必须先形成 `mandate + mission-brief + route-plan`
- 需要跨阶段、跨技能、跨工具的任务，必须由中书省起草
- 涉及结构重构、批量迁移、长流程续跑、跨项目继承的任务，必须经过门下省预审

### 3.3 复核硬门槛

- 没有 `preflight-verdict`，不得进入高风险执行
- 没有 `validation-report`，不得宣布任务完成
- 出现非 trivial 失败，必须补 `root cause trace`

## 4. 三省治理层设计

### 4.1 中书省

- 负责接收目标、判断任务模式、起草 `mission-brief` 与 `route-plan`
- 负责明确验收标准、风险与回退条件

### 4.2 门下省

- 负责预审、复核、否决与上溯
- 负责检查是否绕过真源、模板、注册与状态面

### 4.3 尚书省

- 负责执行调度、状态维护、重试与产物落盘
- 对 `aigc` 项目工作流，负责把任务状态沉淀到 `projects/<项目名>/`
- `.codex/state/tasks/<task_id>/` 仅作为通用治理镜像或非项目任务账本

## 5. 六部能力层设计

| 六部 | 初始化落点 | 核心职责 |
| --- | --- | --- |
| 吏部 | `.codex/registry/skills.yaml` / `.codex/registry/routes.yaml` | 能力注册、路由、heritage mapping |
| 户部 | `projects/<项目名>/` 为准，`.codex/state/tasks/` 为镜像 | 任务状态、上下文与续跑 |
| 礼部 | `.codex/templates/harness/` | 工件合同、模板、handoff |
| 兵部 | `.codex/runbooks/task-lifecycle.md` | 调度、派单、回退 |
| 刑部 | `scripts/aigc_harness_audit.py` 与门下省体系 | 审计、风控、回归检查 |
| 工部 | `scripts/`、`.codex/evals/` | 工程基础设施、验证与评测 |

## 6. 工件、状态与评测闭环

### 6.1 核心工件

- `mandate.yaml`
- `mission-brief.yaml`
- `route-plan.yaml`
- `preflight-verdict.yaml`
- `validation-report.md`
- `learning-record.md`

### 6.2 任务状态目录

- AIGC 项目真源目录：`projects/<项目名>/`
- 通用治理镜像：`.codex/state/tasks/<task_id>/`
- 最小内容：
  - 原始 mandate
  - 起草产物
  - 审计 verdict
  - 执行索引
  - 验收与学习记录

### 6.3 评测闭环

- 最小评测入口：`scripts/aigc_harness_audit.py`
- 当前阶段验证目标：
  - 检查治理真源目录是否存在
  - 检查三省角色是否存在
  - 检查任务模板是否存在
  - 检查 runbook / state / evals 是否存在

## 7. 风险、反官僚化约束与验收标准

### 7.1 风险

- 过早复制旧仓全部技能，导致当前仓库被历史包袱淹没
- 只补目录不补合同，形成新一轮空壳治理
- 三省与六部混层，重新退化为“一个大 orchestrator 全干”

### 7.2 反官僚化约束

- 三省默认串行，六部默认并行
- 高风险节点必须走门下省；稳定重复事务优先模板化和技能化
- 旧仓资产按“可继承、待验证、暂不迁移”三类管理，不做全量搬家

### 7.3 初始化验收标准

- 已生成正式架构包
- 已建立三省角色合同
- 已建立 registry / runbooks / state / evals / templates 真源
- 已建立最小审计脚本
- 审计脚本可通过当前初始化基线检查

## 8. 旧结构到新结构的映射表

| `AIGC-ZEN-VOID` 现有对象 | 当前价值 | 当前仓库目标归属 | 初始化迁移动作 |
| --- | --- | --- | --- |
| `.agents/skills/aigc2026/` | suite-level 控制面、状态聚合、统一入口 | 吏部 + 户部 + 兵部 的未来总控技能发源点 | 本轮不复制 skill 本体，先建立接入槽位 |
| `.codex/agents/story/*` | 专项 review 角色 | 门下省下属专项审计席位 | 先建立门下省总角色，后续再拆专项 reviewer |
| `.codex/hooks/*` | 自动化上下文守护与前置校验 | 兵部 / 工部 自动化能力 | 当前先不迁移 hooks，优先完成 runbook 与 audit 基线 |

## 9. 迁移阶段与防回归方案

### Phase 1. Inventory

- 建立治理真源与承接映射
- 验收：`python3 scripts/aigc_harness_audit.py --strict` 通过

### Phase 2. Shadow

- 新建第一个 repo-local 影视 suite skill
- 让 `aigc` 项目任务先写 `projects/<项目名>/`
- 新 skill 必须在 registry 注册

### Phase 3. Cutover

- 将剧本、设定、分镜、导演、后期等主流程正式映射到新 harness 真源
- 引入门下省专项 reviewer 与 eval / context health 自检

### Phase 4. Deprecation

- 移除临时入口与重复真源
- 停止使用未注册 skill / prompt / runbook

### 防回归硬规则

1. 新增 repo-local skill 若未注册到 `.codex/registry/skills.yaml`，视为治理缺口。
2. 复杂任务若未落 `mission-brief` 和 `route-plan`，视为绕过中书省。
3. 高风险任务若未产出 `preflight-verdict` 或 `validation-report`，视为绕过门下省。
4. 新增工作流若不写入已声明的 canonical control plane，视为绕过尚书省控制面；对 `aigc` 项目，以 `projects/<项目名>/` 为准。
5. 从 `AIGC-ZEN-VOID` 迁入资产但未登记映射，视为继承失控。
