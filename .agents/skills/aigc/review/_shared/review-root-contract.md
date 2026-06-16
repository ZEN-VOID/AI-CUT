# Review Root Contract

`aigc/review` 的正式 gate truth 固定为单一 aggregate review packet，不使用多份 dimension sidecar 并列裁决。

当前 registry 基线为六维审计：

- `规划与种子兑现`
- `分镜执行连续性`
- `设计对位`
- `图像交付就绪`
- `视频交付就绪`
- `治理闭环`

## Canonical Paths

- checkpoint aggregate packet：
  - `projects/aigc/<项目名>/review/checkpoints/<checkpoint_id>/<scope_ref>.review.json`
- stage aggregate packet：
  - `projects/aigc/<项目名>/review/stages/<stage>/<scope_ref>.review.json`
- release aggregate packet：
  - `projects/aigc/<项目名>/review/releases/<scope_ref>.review.json`
- fact pack sidecar：
  - 与 aggregate packet 同级
  - `<scope_ref>.review.fact-pack.json`
- repair sidecar：
  - 与 aggregate packet 同级
  - `<scope_ref>.review.repair.json`
- review summary sidecar：
  - 与 aggregate packet 同级
  - `<scope_ref>.review.review.md`
- dimension sidecars：
  - 落在 aggregate packet 同级目录
  - 文件名由 `review-dimension-registry.yaml -> report_filename` 单点定义
- provider artifacts：
  - 落在 aggregate packet 同级 `.code-reviewer/<scope_ref>.review/`

## Root Ownership

父层只拥有以下字段的唯一判定权：

- `review_status`
- `review_mode`
- `checkpoint_id`
- `stage`
- `scope_ref`
- `selected_agents`
- `overall_score`
- `dimension_scores`
- `issues`
- `severity_counts`
- `critical_issues`
- `routing_decision`
- `handoff_targets`
- `rework_targets`
- `review_ref`
- `review_fact_pack_ref`
- `repair_plan_ref`
- `review_report_ref`
- `source_trace`
- `evidence_refs`
- `external_review`

## Overwrite Rules

1. 每一轮 review 只能写一份 aggregate review packet。
2. 维度 reviewer 只允许覆盖自己的 MD sidecar，不得覆盖 aggregate packet。
3. 若 sidecar 与 aggregate packet 冲突，以 aggregate packet 为 gate 真源，但必须在下一轮 review 前修正 dimension output contract。
4. 各阶段或 provider handoff 只能消费 aggregate packet，不得直接消费某个 dimension sidecar 作为最终 gate。
5. `repair_plan_ref` 与 `review_report_ref` 属于 aggregate packet 的派生闭环载体；它们可被 `query / resume` 或治理工具消费，但不得反向夺取 gate authority。

## Source Trace Rule

- 若问题归属当前 `0-初始化` 到 `8-分组` 的 source layer，聚合结果必须显式保留 `source_layer_owner` 与 `back_to_source_contract`
- 若问题归属当前阶段节点，聚合结果必须显式保留 `rework_targets`

## Repair Bridge Rule

- `aigc/review` 的自动修复当前只拥有 repair routing 与治理桥接写回权：
  - 写 `*.review.repair.json`
  - 在 `governance-state.yaml` 已存在时更新 `review_bridge.latest_review_*`
  - 在 `governance-state.yaml.resume_contract.required_repairs` 中登记返工入口
- `aigc/review` 不拥有阶段业务 canonical truth 的直接自动改写权。
