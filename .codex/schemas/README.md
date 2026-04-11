# Schemas

本目录保留当前仓库共享 schema 的真源位置。

## Bootstrap Rule

初始化阶段先用 `.codex/templates/harness/` 作为可执行模板真源。

当具体影视 suite skill 稳定后，再把高复用字段沉淀为独立 schema 文件，例如：

- `mandate.schema.yaml`
- `mission-brief.schema.yaml`
- `route-plan.schema.yaml`
- `validation-report.schema.yaml`

## Why Not Now

- 当前仓库仍处在 bootstrap 阶段
- 先固定模板与流程，比过早拆 schema 更稳
- 一旦字段跨 2 个以上工作流稳定复用，再晋升为 schema
