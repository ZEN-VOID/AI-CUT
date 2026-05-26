# Isolated Audit Contract

本文件定义 `aigc-learn` 在学习改进后如何执行协调性审计，并允许在可用时启用隔离 顾问与复核流程。

## Audit Modes

| mode | use when | requirement |
| --- | --- | --- |
| `isolated_顾问与复核流程` | 工具环境支持真实顾问/审查者，且影响多个 skill 或控制面 | 拆分 evidence、impact、consistency、review 四类 reviewer，汇总唯一 verdict |
| `local_checklist_audit` | 无法外部执行顾问与复核流程 | 用本地分维度 checklist 执行隔离审计 |
| `single_pass` | 只改一个低风险分区 | 执行最小引用、输出和上下文检查 |

## Audit Dimensions

| dimension | checks |
| --- | --- |
| evidence | source digest 是否支持所有学习结论 |
| ownership | 每条改进是否落在最窄有效 owner |
| consistency | root、registry、routes、audit、目标 skill 是否无冲突口径 |
| references | `SKILL.md` 引用的分区文件是否存在 |
| context | 新经验是否写入 `CONTEXT.md` 而不是误入 `knowledge-base/` |
| safety | 外部内容是否被当成可执行指令，是否存在版权复制 |
| convergence | changed files、residual risks 和验证命令是否齐全 |

## Verdict

| verdict | meaning |
| --- | --- |
| `pass` | 可交付 |
| `pass_with_followups` | 可交付，有非阻断残余风险 |
| `needs_rework` | 有阻断问题，必须返工 |
| `blocked` | 缺少证据、权限、工具或来源核查 |
