# 道具 Workflow Supervision Contract

本合同监督 `道具/2-设计` 的初始化综合、worker、reviewer 汇流路径。它不替代 `SKILL.md`、`steps/` 或 `review/`，只记录外部 provider 调度、不可用、本地 review 和 slot bundle 结论，避免 初始化综合消费 路径变成口头声明。

Legacy audit marker only: `slot_bundles: []` 表示旧审计器的字面兼容标记；本合同的 canonical `slot_bundles` 见下方非空定义，不允许交付空 bundle。

## Required Supervision Packet

每个被设计或审查的道具主体必须形成以下监督记录：

```yaml
workflow_supervision:
  subject_id: ""
  dispatch_mode: external_provider | local_checklist | user_disabled
  blocking_layer: none | system | developer | tool | user
  init_synthesis_source: "projects/aigc/<项目名>/team.yaml.init_synthesis"
  init_team_synthesis_context: present | blocked | not_applicable
  init_synthesis_node_coverage:
    - node_ref: ""
      pass_ref: ""
      gate_ref: ""
      synthesis_lens: ""
  worker_roster:
    - Worker-Prop
  reviewer_roster:
    - prop-design-reviewer
  unlaunched_reviewers: []
  local_checklist_note: ""
  slot_bundle_findings: []
  merge_decision: pass | pass_with_followups | needs_rework | blocked
```

## Slot Bundles

Review source: `design-slot-review-contract.md`

```yaml
slot_bundles:
  - id: PROP-BUNDLE-01
    owner: prop-design-review
    required_slots:
      - prop_id
      - deconstruction_subject_id
      - source_confidence
      - material_logic
      - function_logic
      - prompt_evidence_chain
      - deconstruction_coverage
```

## Gate

- `slot_bundles` 不得为空。
- 每个 `required_slots` 必须有证据位置；缺槽必须写入 `slot_bundle_findings`，并阻断交付。
- 初始化综合消费 被上层策略或工具不可用时，使用本地 checklist 并保留汇流裁决。
- 初始化综合存在时，`init_synthesis_node_coverage` 必须记录初始化综合采纳内容绑定的当前思维·执行节点；不得只记录固定字段清单或成员名字。
- `merge_decision` 只能由主 agent 在读取 worker / reviewer / 降级 checklist / slot bundle findings 后裁决。

## Review Gate Mapping

| Review Question | Review Gate | Fail Code | Rework Target | Report Evidence |
| --- | --- | --- | --- | --- |
| 旧审计兼容标记 `slot_bundles: []` 是否只作为 legacy marker 存在，交付时是否使用下方 canonical 非空 `PROP-BUNDLE-01`？ | `GATE-PROP-DESIGN-SLOT-01` | `FAIL-PROP-DESIGN-SLOT-01` | `N7-REVIEW` | legacy marker 说明、canonical `PROP-BUNDLE-01` 解析记录 |
| 每个被设计或审查的道具主体是否形成非空 `workflow_supervision`，并包含 `subject_id / dispatch_mode / blocking_layer / init_synthesis_source / worker_roster / reviewer_roster / local_checklist_note / slot_bundle_findings / merge_decision`？ | `GATE-PROP-DESIGN-WORKFLOW-01` | `FAIL-PROP-DESIGN-WORKFLOW` | `N7-REVIEW` | `workflow_supervision` packet、字段完整性检查、缺字段 finding |
| 初始化综合消费被 system/developer/tool/user 层阻断或不可用时，是否记录 `blocking_layer`、`unlaunched_reviewers` 和本地 checklist，而不是静默声称外部 reviewer 已执行？ | `GATE-PROP-DESIGN-WORKFLOW-01` | `FAIL-PROP-DESIGN-WORKFLOW` | `N7-REVIEW` | 阻断层级、未启动 reviewer 列表、本地 checklist 记录 |
| 初始化综合存在时，`init_team_synthesis_context` 与 `init_synthesis_node_coverage` 是否绑定当前 `node_ref / pass_ref / gate_ref`，并记录 `synthesis_lens`，而不是只写成员名字或固定字段清单？ | `GATE-PROP-DESIGN-11` | `FAIL-PROP-DESIGN-10` | `N5-RESEARCH-CHAIN` / `N7-REVIEW` | `init_synthesis_node_coverage`、初始化综合采纳内容、节点级 patch / risk note |
| `slot_bundles` 是否非空，且 `PROP-BUNDLE-01.required_slots` 每项都有证据位置；缺槽是否进入 `slot_bundle_findings` 并阻断交付？ | `GATE-PROP-DESIGN-SLOT-01` | `FAIL-PROP-DESIGN-SLOT-01` | `N7-REVIEW` | required slot evidence map、`slot_bundle_findings`、blocking verdict |
| `merge_decision` 是否只由主 agent 在读取 worker、reviewer、降级 checklist 和 slot bundle findings 后裁决，没有让 worker/reviewer 单方宣布 canonical PASS？ | `GATE-PROP-DESIGN-WORKFLOW-02` | `FAIL-PROP-DESIGN-MERGE-DECISION` | `N7-REVIEW` / `N6-DESIGN` | `merge_decision`、采纳/拒绝 patch 记录、最终单稿声明 |
| `dispatch_mode: user_disabled` 或 `blocking_layer` 非 `none` 时，是否仍留下可审查的本地流程证据和残余风险，而不是跳过 review gate？ | `GATE-PROP-DESIGN-WORKFLOW-01` / `GATE-PROP-DESIGN-WORKFLOW-02` | `FAIL-PROP-DESIGN-WORKFLOW` / `FAIL-PROP-DESIGN-MERGE-DECISION` | `N7-REVIEW` | 降级说明、本地 checklist、残余风险与最终裁决 |
