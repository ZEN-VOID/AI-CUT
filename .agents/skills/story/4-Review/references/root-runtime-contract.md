# Root Runtime Contract

本文件承载 `4-Review` 父层的卷级运行时边界。它展开根 `SKILL.md` 的父层职责，但不改写入口路由权。

## Parent Ownership

父层拥有：

- `volume scope / chapter_refs` 锁定
- 卷级 `validation_fact_pack` 组装与 covenant gate
- registry 当前 mandatory 子技能的并发调度与收束
- 卷级 `validation_status / routing_decision / handoff_targets` 唯一判定权
- `projects/story/<项目名>/4-Review/第V卷.validation.json` 正式落盘
- 章级 `rework_targets` 与 `source_trace` 汇总
- `candidate_volume_draft -> validated_volume_draft` 的最终放行裁决

父层不拥有：

- 直接修改任何 `第N章.md`
- 代替 `review/` 生成正式业务审查报告
- 代替 `5-Loopback` 回写 validated truth
- 把各维度 sidecar 变成第二份 parallel canonical truth

## Runtime Paths

| artifact | canonical path | owner |
| --- | --- | --- |
| aggregate gate packet | `projects/story/<项目名>/4-Review/第V卷.validation.json` | `4-Review` 父层 |
| dimension sidecars | `projects/story/<项目名>/4-Review/第V卷/` | 子技能维度证据层 |
| report handoff | `review/` | `review` 阶段 |
| actualization handoff | `5-Loopback/` | `5-Loopback` 阶段 |

## Routing Decision Contract

| routing_decision | 适用条件 | handoff_targets |
| --- | --- | --- |
| `back_to_drafting_nodes` | 问题主要落在卷内若干章节正文质量与工序执行 | `3-Drafting` 对应 workers / steps |
| `back_to_source_contract` | 上游 truth 缺失、冲突或 pack 失效 | `0-Init` / `1-Cards` / `2-Planning` |
| `handoff_to_review_and_loopback` | `PASS` 且允许进入完整闭环 | `review/`、`5-Loopback` |
| `handoff_to_review_only` | 只需要业务报告或历史复核，不进入 actualization | `review/` |

## Aggregate Gate Rules

- `validation_status` 不以均分独裁，必须额外经过 severity / source gate。
- 可用状态为 `FAIL-RUNTIME`、`FAIL-COVENANT`、`FAIL-QUALITY`、`PASS`。
- `PASS` 需要同时满足：无 `critical` 问题、无未解决 source-layer 冲突、无 `FAIL-COVENANT / FAIL-RUNTIME`。
- 卷级 `PASS` 不等于没有小问题，而是所有剩余问题均不构成 blocking issue。
