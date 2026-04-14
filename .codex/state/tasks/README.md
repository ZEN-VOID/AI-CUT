# Task State

本目录是当前仓库的通用任务账本与治理镜像载体。

## 推荐结构

```text
.codex/state/tasks/<task_id>/
  mandate.yaml
  mission-brief.yaml
  route-plan.yaml
  preflight-verdict.yaml
  artifacts/
  validation-report.md
  learning-record.md
```

## 规则

- `<task_id>` 应使用 ASCII-safe 命名
- 复杂任务必须使用独立任务目录
- 运行中产物可以放到 `artifacts/`
- 最终结论应汇总到 `validation-report.md` 与 `learning-record.md`
- 若工作流已声明项目内 canonical runtime，则本目录只作为镜像或跨项目治理账本，不反向覆盖主真源

## AIGC Workflow Override

- 对 `aigc` 项目型工作流，canonical runtime 为 `projects/aigc/<项目名>/`
- `mandate / mission-brief / route-plan / preflight-verdict / validation-report / learning-record` 以 `projects/aigc/<项目名>/` 为准
- 本目录仅在以下场景使用：
  - 非项目型通用治理任务
  - 跨项目协调任务
  - 需要额外保留仓库级治理镜像时

## 当前阶段约束

- 允许人工创建任务目录
- 不允许把状态只留在聊天记录或零散 markdown 中
