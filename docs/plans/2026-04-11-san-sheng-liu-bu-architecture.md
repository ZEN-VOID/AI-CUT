# AIGC-FILM `aigc` 根级卫星技能架构包

## 1. 任务模式与目标边界

- 当前模式：`改造升级`
- 目标：在现有 `aigc` 阶段链之上，补齐三个根级卫星技能：
  - `query`
  - `resume`
  - `review`
- 本轮边界：
  - 新增三个卫星技能及其 `SKILL.md + CONTEXT.md + references/`
  - 将卫星技能纳入根 `aigc` 路由、registry、routes、audit
  - 用三省六部制重新定义它们的 owner、carrier 与回接关系

## 2. 现状诊断与 Layered Trace

### 2.1 症状

| 症状 | 风险 |
| --- | --- |
| `aigc` 只有主阶段链，没有根级旁路能力层 | 查询、恢复、复核只能混进根路由或阶段私有流程 |
| query / resume / review 没有 skill 级显式合同 | 未来只能靠聊天口头说明，不可注册、不可审计 |
| registry / routes / audit 还不知道这些卫星技能 | 新增能力无法进入治理控制面 |

### 2.2 Layered Trace

| Symptom | Direct Technical Cause | Rule Source | Meta Rule Source | Fix Landing Points |
| --- | --- | --- | --- | --- |
| 根技能能路由阶段，不能路由查询/恢复/复核 | 根合同没有卫星层设计 | `.agents/skills/aigc/SKILL.md` | 根 `AGENTS.md` 的卫星技能放置矩阵 | 根技能 + 新卫星技能目录 |
| 新 skill 即使创建也不会进入治理控制面 | registry / routes 无注册 | `.codex/registry/skills.yaml`、`.codex/registry/routes.yaml` | 三省共享治理合同 | registry + routes + audit |
| 审计脚本仍沿用旧 runtime 口径 | 审计真源滞后于当前 `规划 / 主体 / 画面` runtime | `scripts/aigc_skill_audit.py` | 根 `AGENTS.md` 的 root-cause / canonical runtime 合同 | 审计脚本常量与 satellite 校验 |

## 3. 宪章层设计

### 3.1 全局优先级

1. 用户显式请求
2. 根 `AGENTS.md`
3. 根 `aigc/SKILL.md`
4. 卫星技能 `SKILL.md`
5. registry / routes / runbook / shared carrier
6. `CONTEXT.md`

### 3.2 进入条件

- `query`：需要事实查询与证据综合
- `resume`：需要恢复与安全回接
- `review`：需要门下省侧 preflight / acceptance / learning bridge

### 3.3 闭环硬门槛

- 卫星技能必须是 root sibling，而不是新主阶段
- 必须注册到 `.codex/registry/skills.yaml`
- 必须补 `.codex/registry/routes.yaml`
- 必须进入 `scripts/aigc_skill_audit.py`

## 4. 三省治理层设计

### 4.1 中书省

- 仍由根 `aigc` 拥有总入口与总路由
- 决定本轮请求应进阶段还是卫星技能

### 4.2 门下省

- `review/` 是门下省侧卫星技能
- 负责 `preflight-verdict.yaml`、`validation-report.md`、`learning-record.md` 的 bridge

### 4.3 尚书省

- `query/` 与 `resume/` 是尚书省侧卫星技能
- `query/` 负责 runtime 与证据读取
- `resume/` 负责恢复与回接

## 5. 六部能力层设计

| 六部 | 卫星技能挂载 | 说明 |
| --- | --- | --- |
| 吏部 | `skills.yaml` / `routes.yaml` | 记录 `satellite_index` 与 route policies |
| 户部 | `query/` | 读取项目状态、阶段产物与治理工件 |
| 礼部 | `review/` + harness templates | 承接 preflight / validation / learning carrier |
| 兵部 | `resume/` | 恢复最后稳定入口与续跑 |
| 刑部 | `review/` | 复核、否决、closure triad |
| 工部 | `scripts/aigc_skill_audit.py` | 将卫星技能纳入审计覆盖 |

## 6. 工件、状态与评测闭环

### 6.1 新增工件

- `.agents/skills/aigc/query/`
- `.agents/skills/aigc/resume/`
- `.agents/skills/aigc/review/`

### 6.2 状态与 carrier

- `query`：只读 `projects/<项目名>/` 与治理真源
- `resume`：读 `project_state + governance artifacts + stage outputs`
- `review`：写 `preflight-verdict.yaml / validation-report.md / learning-record.md`

### 6.3 评测与审计

- `.codex/registry/skills.yaml` 增加 `satellite_index`
- `.codex/registry/routes.yaml` 增加 3 条卫星路由
- `scripts/aigc_skill_audit.py` 增加 satellite 校验并修正 runtime 常量

## 7. 风险、反官僚化约束与验收标准

### 7.1 风险

- 把卫星技能注册成新的顶层 suite，造成第二总入口
- 把 query / resume / review 做成 stage，破坏主链
- 只建目录，不同步 registry / routes / audit

### 7.2 反官僚化约束

- 根 `aigc` 仍是唯一总入口
- 卫星技能默认不并入主阶段串行链
- 只有 `review` 能写 review carrier，`query` 与 `resume` 默认不写项目业务真源

### 7.3 验收标准

- 三个卫星技能目录存在且合同完整
- 根 `aigc/SKILL.md` 能正确路由到三个卫星技能
- registry / routes / audit 已知晓三个卫星技能
- `python3 scripts/aigc_skill_audit.py --strict` 可通过

## 8. 旧结构到新结构的映射表

| 参考对象 | 旧结构角色 | 新结构落点 |
| --- | --- | --- |
| `story2026/query` | 根级 query 卫星技能 | `aigc/query` |
| `story2026/resume` | 根级 resume 卫星技能 | `aigc/resume` |
| `story2026/review` | 根级 review 卫星技能 | `aigc/review`，但更偏门下省治理工件桥接 |

## 9. 迁移阶段与防回归方案

### Phase 1. Contract

- 建立三个卫星技能合同

### Phase 2. Control Plane

- 注册 `satellite_index`
- 补 route policies

### Phase 3. Audit

- 补 `aigc_skill_audit.py`
- 修当前 runtime 常量漂移

### 防回归规则

1. 以后新增根级卫星技能，必须走 `satellite_index`，不得另造顶层 suite。
2. 卫星技能只要改动 carrier 或路由边界，就必须同步 root `aigc/SKILL.md`、registry、routes、audit。
3. 任何 query / resume / review 能力若开始拥有阶段内容真源改写权，应重新评估是否仍适合作为卫星技能。
