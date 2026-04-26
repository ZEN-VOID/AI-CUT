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

- 必须包含 `0-初始化` 到 `7-视频` 的关键 handoff refs。
- 必须包含相关阶段 validation carrier。
- 必须包含项目根 `STATE.json` 与 `governance-state.yaml`，若二者存在。

## Hard Rules

1. 同一轮 dimension review 必须消费同一份 `review_fact_pack`。
2. 若 required slice 缺失，父层直接 `FAIL-COVENANT`。
3. `review_fact_pack` 是 evidence pack，不是第二业务真源。
4. provider 只能审这份 pack，不应越权拼读零散阶段文件。
