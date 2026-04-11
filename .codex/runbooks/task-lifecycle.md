# Task Lifecycle Runbook

## Purpose

定义当前仓库的标准任务生命周期，作为三省与六部共享的运行真源。

## Lifecycle

1. `受命`
   - 记录任务意图到 `mandate.yaml`
2. `起草`
   - 中书省生成 `mission-brief.yaml`
   - 同步生成 `route-plan.yaml`
3. `预审`
   - 门下省生成 `preflight-verdict.yaml`
   - 若 verdict 为 `reject` 或 `revise`，任务回流中书省
4. `执行`
   - 尚书省在已声明的 canonical runtime 中推进任务
   - 对 `aigc` 项目工作流，canonical runtime 为 `projects/<项目名>/`
   - 对通用非项目任务，默认使用 `.codex/state/tasks/<task_id>/`
5. `验收`
   - 门下省生成 `validation-report.md`
6. `沉淀`
   - 生成 `learning-record.md`
   - 把可复用经验回写对应 `CONTEXT.md`

## Required Paths

- `.codex/templates/harness/`
- `.codex/state/tasks/`
- `.codex/registry/`
- `.codex/evals/`

## Workflow-Specific Control Planes

- 默认通用控制面：`.codex/state/tasks/<task_id>/`
- `aigc` 项目型工作流：`projects/<项目名>/`，并以此作为运行时唯一真源
- 若工作流已声明项目内 canonical runtime，`.codex/state/tasks/` 仅作为可选治理镜像，不得覆盖主真源

## Hard Gates

- 没有 `mission-brief`，不得执行复杂任务
- 没有 `preflight-verdict`，不得执行高风险任务
- 没有 `validation-report`，不得宣布完成
- 失败若未做 upward trace，不得视为闭环

## Bootstrap Guidance

- 当前阶段允许最小人工驱动，但不允许绕开标准工件
- 业务 skill 尚未齐备时，先保持治理链完整，再逐步接入具体影视流程
- 对 `aigc` 项目技能树，阶段扩展、状态注册与审计覆盖必须同步进入 `.codex/registry/` 与 `scripts/aigc_skill_audit.py`
