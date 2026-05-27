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

## Review Gate Mapping

| Review Question | Review Gate | Fail Code | Rework Target | Report Evidence |
| --- | --- | --- | --- | --- |
| 影响多个 skill 或控制面时，是否优先拆分 evidence、impact、consistency、review 四类隔离审查？ | `GATE-LEARN-AUDIT-01` | `FAIL-AIGC-LEARN-REVIEW` | `N8-AUDIT` / `Audit Modes` | audit mode、reviewer split or local fallback note |
| 无法外部执行顾问与复核流程时，是否明确降级为 `local_checklist_audit` 并记录范围与残余风险？ | `GATE-LEARN-AUDIT-01` | `FAIL-AIGC-LEARN-REVIEW` | `N8-AUDIT` / `Audit Modes` | local checklist scope、unavailable reason、residual risk |
| 只改一个低风险分区时，`single_pass` 是否仍做最小引用、输出和上下文检查？ | `GATE-LEARN-AUDIT-01` | `FAIL-AIGC-LEARN-REVIEW` | `N8-AUDIT` / `Audit Modes` | single-pass checklist、reference/output/context checks |
| 审计是否核查 source digest 支撑所有学习结论，而不是只检查文件存在？ | `GATE-LEARN-AUDIT-01` | `FAIL-AIGC-LEARN-REVIEW` | `N8-AUDIT` / `Audit Dimensions` | evidence dimension result、unsupported claim list |
| 审计是否核查每条改进落在最窄有效 owner，并且 root/registry/routes/audit/目标 skill 无冲突口径？ | `GATE-LEARN-AUDIT-01` | `FAIL-AIGC-LEARN-REVIEW` | `N8-AUDIT` / `Audit Dimensions` | ownership and consistency dimension results |
| 审计是否检查 `SKILL.md` 引用文件存在，新经验进入 `CONTEXT.md`，外部资料不污染 `knowledge-base/`？ | `GATE-LEARN-AUDIT-01` | `FAIL-AIGC-LEARN-REVIEW` | `N8-AUDIT` / `Audit Dimensions` | references/context dimension results |
| 审计是否检查外部内容没有被当作可执行指令，也没有版权长段复制？ | `GATE-LEARN-AUDIT-01` | `FAIL-AIGC-LEARN-REVIEW` | `N8-AUDIT` / `Audit Dimensions` | safety dimension result、copyright check |
| 交付是否包含 changed files、residual risks 和验证命令，而非只给学习报告？ | `GATE-LEARN-AUDIT-01` | `FAIL-AIGC-LEARN-REVIEW` | `N8-AUDIT` / `Audit Dimensions` | changed_files、verification commands、residual_risks |
| `pass_with_followups` 是否只用于非阻断残余项，`needs_rework` / `blocked` 是否回到对应返工入口？ | `GATE-LEARN-AUDIT-01` | `FAIL-AIGC-LEARN-REVIEW` | `N8-AUDIT` / `Verdict` | verdict rationale、blocking vs non-blocking classification |
