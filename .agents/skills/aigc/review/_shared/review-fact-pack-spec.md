# Review Fact Pack Spec

`review_fact_pack` 是 `aigc/review` 父层分发给全部维度 reviewer 的同一份事实包。

runner 正式落盘时，文件名固定为当前 aggregate packet 同级：

- `<scope_ref>.review.fact-pack.json`

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

## Required Slice Rules

### checkpoint_inline

- 必须包含当前 checkpoint 对应的 canonical output refs
- 必须包含当前 stage 的 `validation-report.md`
- 必须包含与该 checkpoint 直接相关的上游 truth refs

### stage_acceptance

- 必须包含当前 stage 的 canonical outputs
- 必须包含当前 stage 的 `validation-report.md`
- 必须包含该 stage 的直接上游 truth refs

### package_release

- 必须包含当前 package scope 涉及的 `0-初始化 ~ 9-审片` 关键 handoff refs
- 必须包含相关阶段 `validation-report.md`
- 必须包含项目根 `STATE.json` 与 `governance-state.yaml`（若存在）

## Hard Rules

1. 同一轮 dimension review 必须消费同一份 `review_fact_pack`。
2. 若缺 required slice，父层直接 `FAIL-COVENANT`，不得先跑维度 reviewer 再猜。
3. `review_fact_pack` 是 evidence pack，不是第二业务真源。
4. `review_fact_pack` 必须先于 `code-reviewer` 调度落盘，provider 只审这一份 pack，不直接越权读取零散阶段文件。
