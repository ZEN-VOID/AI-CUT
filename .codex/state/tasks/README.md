# Task State Mirror

本目录是仓库级通用任务状态面与治理镜像，不是所有工作流的运行时第一真源。

## 角色定位

- 对通用非项目任务：
  - `.codex/state/tasks/<task_id>/` 是默认执行账本
- 对 `aigc` 项目工作流：
  - `projects/aigc/<项目名>/` 是运行时唯一真源
  - `.codex/state/tasks/<task_id>/` 只作跨项目治理镜像或非项目任务账本

## 与 HARNESS 的关系

- 宪章层：根 `AGENTS.md`
- 生命周期真源：`.codex/runbooks/task-lifecycle.md`
- 共享治理合同：`.codex/templates/harness/office-governance-contract.md`
- 注册与路由：`.codex/registry/skills.yaml`、`.codex/registry/routes.yaml`

本目录的职责是承接三省六部制里的“通用状态账本”能力，而不是反向覆盖项目内 canonical runtime。

## 推荐目录形态

```text
.codex/state/tasks/<task_id>/
├── mandate.yaml
├── mission-brief.yaml
├── route-plan.yaml
├── preflight-verdict.yaml
├── validation-report.md
├── learning-record.md
└── artifacts/
```

说明：

- `mandate / mission-brief / route-plan / preflight / validation / learning` 的字段真源仍在 `.codex/templates/harness/`
- 本目录只承接具体任务实例的镜像或通用任务落盘

## AIGC 特别规则

对 `.agents/skills/aigc/`：

- 若项目已绑定 `projects/aigc/<项目名>/`
  - 项目根 `STATE.json` 与可选 `governance-state.yaml` 优先
  - 阶段产物、review packet、validation carrier 也优先留在项目根
- 只有在以下场景，才建议额外在本目录落镜像：
  - 跨项目治理审计
  - 非项目型治理任务
  - 需要把多轮执行状态统一挂到仓库级任务账本

## 反漂移要求

1. 不得把 `.codex/state/tasks/` 当成 `aigc` 项目 runtime 的替代品。
2. 若工作流已声明项目内 canonical runtime，本目录中的镜像状态不得反向覆盖主真源。
3. 新增任务载体字段时，应同步更新：
   - `.codex/templates/harness/`
   - `.codex/runbooks/task-lifecycle.md`
   - `scripts/aigc_harness_audit.py`

