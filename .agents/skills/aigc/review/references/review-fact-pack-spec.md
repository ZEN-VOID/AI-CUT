# Review Fact Pack Spec

`review_fact_pack` 是 `aigc-review` 父层分发给全部维度 reviewer 的同一份事实包。

## Minimum Fields

- `project_root`
- `review_mode`
- `checkpoint_id`
- `stage`
- `scope_ref`
- `team_yaml_ref`
- `state_ref`
- `governance_state_ref`
- `validation_refs`
- `source_truth_refs`
- `runtime_artifact_refs`
- `handoff_candidate_refs`
- `aggregate_review_ref`

## Required Slice Rules

### checkpoint_inline

- 必须包含当前 checkpoint 对应的 canonical output refs。
- 必须包含当前 stage 的 `validation-report.md` 或等价 validation carrier。
- 必须包含与该 checkpoint 直接相关的上游 truth refs。

### stage_acceptance

- 必须包含当前 stage 的 canonical outputs。
- 必须包含当前 stage 的 validation carrier。
- 必须包含该 stage 的直接上游 truth refs。

### package_release

- 必须包含 `0-初始化` 到 `9-审片` 的关键 handoff refs。
- 必须包含相关阶段 validation carrier。
- 必须包含项目根 `STATE.json` 与 `governance-state.yaml`，若二者存在。

## Hard Rules

1. 同一轮 dimension review 必须消费同一份 `review_fact_pack`。
2. 若 required slice 缺失，父层直接 `FAIL-COVENANT`。
3. `review_fact_pack` 是 evidence pack，不是第二业务真源。
4. provider 只能审这份 pack，不应越权拼读零散阶段文件。

## Review Gate Mapping

| Review Question | Review Gate | Fail Code | Rework Target | Report Evidence |
| --- | --- | --- | --- | --- |
| `review_fact_pack` 是否包含最小字段集，且 `project_root`、`review_mode`、`stage/checkpoint_id`、`scope_ref` 与 `aggregate_review_ref` 唯一对位？ | `GATE-REVIEW-FACT-01` | `FAIL-REVIEW-FACT-MINIMUM` | `N2-FACT-PACK` | fact pack 字段缺口、scope 对位结果、aggregate path 与缺失字段列表。 |
| `checkpoint_inline` 模式是否包含当前 checkpoint 的 canonical output refs、stage validation carrier 和直接上游 truth refs？ | `GATE-REVIEW-FACT-02` | `FAIL-REVIEW-FACT-SLICE` | `N2-FACT-PACK` | `required_refs` 中 checkpoint refs、validation refs、upstream truth refs 与缺失项。 |
| `stage_acceptance` 模式是否包含当前 stage 的 canonical outputs、validation carrier 和直接上游 truth refs，而不是只凭阶段目录或最终报告判断？ | `GATE-REVIEW-FACT-03` | `FAIL-REVIEW-FACT-SLICE` | `N2-FACT-PACK` | stage canonical refs、validation carrier、upstream truth refs、空目录/旧报告排除记录。 |
| `package_release` 模式是否覆盖 `0-初始化` 到 `9-审片` 的关键 handoff refs、相关 validation carrier、`STATE.json` 与 `governance-state.yaml` 存在状态？ | `GATE-REVIEW-FACT-04` | `FAIL-REVIEW-FACT-SLICE` | `N2-FACT-PACK` | release required slice coverage、阶段缺口、治理 carrier 状态和阻断范围。 |
| 同一轮 mandatory dimensions 是否消费同一份 fact pack，且 `scope_ref`、`review_mode`、`stage/checkpoint_id` 没有在维度间漂移？ | `GATE-REVIEW-FACT-05` | `FAIL-REVIEW-COVENANT` | `N3-DIMENSIONS` | `dimension_runtime.fact_pack_ref` 对比表、漂移维度、冲突字段和阻断结论。 |
| required slice 缺失时，父层是否直接写 `FAIL-COVENANT` aggregate、repair sidecar 和 summary，并停止 provider 与 dimension review？ | `GATE-REVIEW-FACT-06` | `FAIL-REVIEW-COVENANT` | `N2-FACT-PACK` | aggregate `review_status=FAIL-COVENANT`、missing_required_refs、未调度维度/provider 证据。 |
| fact pack 是否仅作为 evidence pack，不把摘要、推断或 runner 组装结果升级为第二业务真源？ | `GATE-REVIEW-FACT-07` | `FAIL-REVIEW-FACT-AUTHORITY` | `N2-FACT-PACK` | fact pack 中每个事实回指 canonical refs；推断字段标记为 evidence/summary 而非 truth。 |
| provider 或本地 checklist 是否只审这份 fact pack，没有越权散读未登记阶段文件、旧路径、缓存或 provider 历史任务？ | `GATE-REVIEW-FACT-08` | `FAIL-REVIEW-FACT-PROVIDER-SCOPE` | `N3-DIMENSIONS` | provider input manifest、本地 checklist 输入、额外读取路径和排除记录。 |
| fact pack、aggregate packet、dimension reports 与 repair sidecar 是否通过同一 `scope_ref` 和同级路径互相回指，避免产生孤立审计文件？ | `GATE-REVIEW-FACT-09` | `FAIL-REVIEW-FACT-LINKAGE` | `N4-AGGREGATE` | fact_pack_ref、aggregate_review_ref、dimension_report_refs、repair_plan_ref 的路径对位表。 |
