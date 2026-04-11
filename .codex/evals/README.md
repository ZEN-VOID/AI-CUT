# Evals

本目录用于存放当前仓库的治理与流程评测入口。

## Bootstrap Scope

当前初始化阶段至少覆盖：

- harness 真源目录是否存在
- 三省角色合同是否存在
- 三省角色是否引用共享治理真源并暴露关键合同锚点
- 任务模板是否存在
- runbook / state / registry / evals 是否存在
- `aigc` 技能树是否已声明 `projects/<项目名>/` canonical runtime
- `aigc` 阶段状态是否已注册到 registry
- 搁浅阶段是否被显式排除出执行链与严格审计失败项

## Current Entry

- `python3 scripts/aigc_harness_audit.py`
- `python3 scripts/aigc_harness_audit.py --strict`
- `python3 scripts/aigc_skill_audit.py`
- `python3 scripts/aigc_skill_audit.py --strict`

## Future Expansion

- 影视阶段 skill smoke tests
- schema completeness checks
- self-host adoption checks
- context health checks
- creative skill package benchmark execution
- release-level recommendation checks
