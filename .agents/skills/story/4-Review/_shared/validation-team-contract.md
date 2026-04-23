# Validation Team Contract

`4-Review` 的 validator roster 不再在本文件手写维护。

唯一 roster 真源固定为：

- `validation-dimension-registry.yaml` 中 `final_acceptance.mandatory = true` 的维度集合

## Shared Rules

- 子技能只拥有维度 verdict 与 sidecar report 权。
- 父层独占 `validation_status / routing_decision / handoff_targets` 判定权。
- 当前阶段默认以卷为父单元并发执行；子技能看到的是同一卷 pack，而不是各自单章的独立快照。
- 本文件只保留团队共享规则，不再复制维度名单、文件名或权重。
- roster 调整时必须同步：
  - `validation-dimension-registry.yaml`
  - 对应 child `SKILL.md + CONTEXT.md`
  - `review_runner.py` 中的 `ROLE_RUNNERS` 与 handler（若该维度参与自动 runner）
  - 受影响的共享字段合同或示例
