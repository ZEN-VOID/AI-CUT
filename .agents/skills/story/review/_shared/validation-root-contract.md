# Validation Root Contract

`review` 的正式 gate truth 固定为单一卷级聚合 JSON，不使用多份子报告并列裁决。

当前 registry 基线为六维终验：`结构兑现 / 连续性 / 逻辑自洽校验 / 人物一致性 / 时间线 / 任务汇聚`。

## Canonical Paths

- 聚合验收包：
  - `projects/story/<项目名>/review/第V卷.validation.json`
- 维度证据目录：
  - `projects/story/<项目名>/review/第V卷/`
- 维度 sidecar 文件名：
  - 由 `validation-dimension-registry.yaml -> report_filename` 单点定义
  - sidecar 数量由 registry 中 `final_acceptance.mandatory = true` 的维度集合决定

说明：

- 卷级 aggregate JSON 是唯一 gate truth
- 章级问题通过 `issues.location / chapter_issue_index` 保留
- `review/` 的业务报告仍由其自身生成，不在本阶段产生

## Root Ownership

父层只拥有以下字段的唯一判定权：

- `validation_status`
- `validation_mode`
- `volume_ref`
- `chapter_refs`
- `selected_agents`
- `overall_score`
- `dimension_scores`
- `issues`
- `chapter_issue_index`
- `severity_counts`
- `critical_issues`
- `routing_decision`
- `handoff_targets`
- `rework_targets`
- `validation_ref`

## Overwrite Rules

1. 每一轮验收只能写一份 `第V卷.validation.json`。
2. 子技能只允许覆盖自己的 MD sidecar，不得覆盖 aggregate JSON。
3. 若 MD sidecar 与 aggregate JSON 冲突，以 aggregate JSON 为 gate 真源，但必须在下一次验收前修正 child output contract。
4. `review/` 与 `context-return` 只能消费 aggregate JSON，不得直接消费某个子技能 sidecar 作为最终 gate。

## Source Trace Rule

- 若问题归属 `0-初始化 / 1-设定 / 2-卷章规划`，聚合结果必须显式保留 `source_layer_owner` 与 `back_to_source_contract`
- 若问题归属 `3-初稿` 当前卷内的若干章节，聚合结果必须保留章级 `rework_targets`
