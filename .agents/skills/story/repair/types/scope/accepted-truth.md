# Scope Package: Accepted Truth

## Selection Signals

- 已 PASS、终稿、accepted manuscript、return actualization、validated actual、review aggregate、上下文回流事实。

## When X Then Check X

| when | must check |
| --- | --- |
| 改已 PASS 终稿事实 | `review/第V卷.validation.json`、accepted manuscript refs、`4-润色/` 或 accepted `3-初稿/` |
| 改已 return 的实绩 | return artifact、Cards current_state/history、项目 CONTEXT carryover、STATE |
| 改下一卷已消费的事实 | 下一卷 planning、provider context、后续已产出章 |
| 只做局部说明不改 accepted truth | review aggregate 是否仍有效，是否需要 residual risk 标注 |

## Required Impact Additions

- `review_aggregate_ref`
- `accepted_manuscript_refs`
- `return_actualization_refs`
- `state_projection_refs`
- `consumer_refs`

## Review Gate

- 已验收事实被改变时必须重验、失效化或明确保留旧验收。
- 不得静默覆盖 accepted manuscript。
- 后续消费者必须指向新版事实或标注残余风险。
