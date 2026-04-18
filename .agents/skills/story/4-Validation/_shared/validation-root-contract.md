# Validation Root Contract

`4-Validation` 的正式 gate truth 固定为单一聚合 JSON，不使用 6 份子报告并列裁决。

补充边界：

- 同一批 validator 可以被 `3-Drafting` 当作即时审计 hook 复用。
- 但只有 `4-Validation` 父层聚合结果，才拥有终验 `PASS` 与最终放行权。

## Canonical Paths

- 聚合验收包：
  - `projects/story/<项目名>/Validation/第N集.validation.json`
- 维度证据目录：
  - `projects/story/<项目名>/Validation/第N集/`
- 维度 sidecar：
  - `结构兑现.md`
  - `连续性.md`
  - `逻辑自洽校验.md`
- `人物一致性.md`
- `时间线.md`
- `类型兑现.md`

说明：

- schema 兼容字段仍使用 `chapter`，其语义等于当前 `第N集.md` 的集号。
- `review/` 的业务报告仍由其自身生成，不在本阶段产生。

## Root Ownership

父层只拥有以下字段的唯一判定权：

- `validation_status`
- `validation_mode`
- `selected_agents`
- `overall_score`
- `dimension_scores`
- `issues`
- `severity_counts`
- `critical_issues`
- `anti_ai_force_check`
- `spoiler_risk`
- `contrivance_risk`
- `cold_commentary_risk`
- `routing_decision`
- `handoff_targets`
- `rework_targets`
- `validation_ref`
- `type_pack_fit_summary`（若启用 pack）

## Overwrite Rules

1. 每一轮验收只能写一份 `第N集.validation.json`。
2. 子技能只允许覆盖自己的 MD sidecar，不得覆盖 aggregate JSON。
3. 若 MD sidecar 与 aggregate JSON 冲突，以 aggregate JSON 为 gate 真源，但必须在下一次验收前修正 child output contract。
4. `review/` 与 `5-Loopback` 只能消费 aggregate JSON，不得直接消费某个子技能 sidecar 作为最终 gate。

## Source Trace Rule

- 若问题归属 `0-Init / 1-Cards / 2-Planning`，聚合结果必须显式保留 `source_layer_owner` 与 `back_to_source_contract`。
- 若问题归属 `3-Drafting` 当前工序，聚合结果必须保留 step 级 `rework_targets`。

## Template Rule

- 聚合 JSON 模板真源：
  - `./validation-aggregate.template.json`
- 子技能 MD 模板真源：
  - `./validation-dimension-report.template.md`
- 维度注册表真源：
  - `./validation-dimension-registry.yaml`

## Quick Extension Rule

若未来要新增、删除或改名某个 validation 维度：

1. 先修改 `validation-dimension-registry.yaml`
2. 再补对应 child package
3. 若 machine-readable 字段变化，再同步 `checker-output-schema.md`
4. 操作顺序与最小触点说明，统一见：
   - `../扩维与调整指南.md`

不得先在 `3-Drafting` 或 `4-Validation` 父技能里各自手写第二份维度路由表。

子技能可加局部指标，但不得私自定义第二份总报告模板。

## Type-Pack Projection Rule

- 若项目未启用显式 `type-pack`，validation 只跑通用基座维度。
- 若项目启用了 `type-pack`，父层可在 aggregate JSON 中追加：
  - `type_pack_profile`
  - `type_pack_fit_summary`
  - `type_pack_fail_signals`
- 若 registry 已启用 `type-pack-fit-validator`，类型兑现问题应由独立维度出 packet；`type_pack_fit_summary` 只做父层摘要，不再把 issue 静默并入 `structure-validator`。
