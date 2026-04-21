# Validation Team Contract

`4-Validation` 的固定 validator roster：

- `结构兑现`
- `连续性`
- `逻辑自洽校验`
- `人物一致性`
- `时间线`
- `类型兑现`

## Shared Rules

- 子技能只拥有维度 verdict 与 sidecar report 权。
- 父层独占 `validation_status / routing_decision / handoff_targets` 判定权。
- 当前阶段默认以卷为父单元并发执行；子技能看到的是同一卷 pack，而不是各自单章的独立快照。
- roster 调整时必须同步：
  - `validation-dimension-registry.yaml`
  - 对应 child `SKILL.md + CONTEXT.md`
  - 聚合字段合同
  - 卷级 aggregate template
