# AIGC Review Modes

## Purpose

定义 `aigc/review` 的三种 review mode、carrier 与边界。

## Modes

| mode | trigger | carrier | subtype | boundary |
| --- | --- | --- | --- |
| `preflight-review` | 高风险执行前 | `projects/<项目名>/preflight-verdict.yaml` | `subtypes/preflight-review/` | 只给 verdict，不执行内容任务 |
| `acceptance-review` | 阶段或项目产物已写出 | scope 对应的 `validation-report.md` | `subtypes/acceptance-review/` | 只给验收与下一入口，不改业务真源 |
| `learning-bridge` | 某轮 review 已结束，需要沉淀经验 | `projects/<项目名>/learning-record.md` | `subtypes/learning-bridge/` | 只沉淀模式，不重写验收结论 |

## Governance-State Sync

每次 review mode 结束后，都应把以下摘要同步回 `projects/<项目名>/governance-state.yaml`：

- `review_bridge.latest_preflight_status`
- `review_bridge.latest_acceptance_status`
- `review_bridge.latest_learning_status`
- 如 verdict 改变了唯一下一入口，还要同步 `resume_contract`

父技能职责：

1. 只做 mode 判定与唯一路由。
2. 具体 carrier 写法、边界与局部 heuristics 统一下沉到对应 subtype。

## Scope Mapping

| scope | carrier |
| --- | --- |
| `project` | `projects/<项目名>/validation-report.md` |
| `1-Planning` | `projects/<项目名>/1-Planning/validation-report.md` |
| `2-Global` / `3-Detail` | `projects/<项目名>/3-Detail/validation-report.md` |
| `4-Design` | `projects/<项目名>/4-Design/validation-report.md` |
| `5-Image` | `projects/<项目名>/5-Image/validation-report.md` |
| `6-Video` | `projects/<项目名>/6-Video/validation-report.md` |

## Hard Guards

- `review/` 不代替阶段执行
- `review/` 不改业务真源
- 没有 `mission-brief / route-plan` 时，不得放行高风险执行
- scope 已搁浅时，只返回 blocker，不给 acceptance pass
- `governance-state.yaml` 只是 review 摘要同步位，不得替代 `preflight-verdict.yaml`、`validation-report.md`、`learning-record.md` 本体
