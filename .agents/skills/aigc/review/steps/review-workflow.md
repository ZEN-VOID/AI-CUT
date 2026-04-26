# Review Workflow

## Thinking-Action Network

| node_id | objective | inputs | actions | evidence | route_out | gate |
| --- | --- | --- | --- | --- | --- | --- |
| `N1-REVIEW-INTAKE` | 锁定审计范围 | 用户请求、项目根、registry | 判定 mode、stage/checkpoint、scope_ref 与 aggregate 落点 | `review_scope_note` | `N2` | mode 与 scope 唯一 |
| `N2-FACT-PACK` | 建立事实契约 | 项目产物、validation carrier、source truth | 写 `*.review.fact-pack.json`；缺 required slice 时早停 | `fact_pack_ref` | `N3` 或 `FAIL-COVENANT` | required slice 完整 |
| `N3-DIMENSIONS` | 执行维度审计 | fact pack、dimension registry | 调度 mandatory dimensions，收集 packets | `dimension_packets` | `N4` | mandatory 维度不可缺 |
| `N4-AGGREGATE` | 写唯一 gate | dimension packets、aggregate template | 计算 status、score、issues、route | `aggregate_review_packet` | `N5` | 只有本节点写 gate |
| `N5-ROUTE` | 完成返工或放行 | aggregate packet、scope | 写 repair plan 或 handoff target | `repair_plan_ref` | done | route 可执行 |

## Branch Rules

- `checkpoint_inline` 优先阻断当前 checkpoint handoff。
- `stage_acceptance` 优先回答当前 stage 能否放行。
- `package_release` 优先回答 provider handoff 或 release 能否继续。

## Failure Loop

`FAIL-COVENANT` 回到 `N2`，且不得进入 provider 或 dimension loop；`FAIL-REVIEW-03` 回到 `N3`；aggregate 字段缺失回到 `N4`；route 不可执行回到 `N5`。
