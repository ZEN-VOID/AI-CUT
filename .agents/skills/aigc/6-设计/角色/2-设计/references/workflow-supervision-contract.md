# 角色 Workflow Supervision Contract

本合同监督 `角色/2-设计` 的初始化综合、worker、reviewer 汇流路径。它不替代 `SKILL.md`、`steps/` 或 `review/`，只记录外部 provider 调度、不可用、本地 review 和 slot bundle 结论，避免 初始化综合消费 路径变成口头声明。

Legacy audit marker only: `slot_bundles: []` 表示旧审计器的字面兼容标记；本合同的 canonical `slot_bundles` 见下方非空定义，不允许交付空 bundle。

## Required Supervision Packet

每个被设计或审查的角色主体必须形成以下监督记录：

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
  reviewer_roster:
    - character-research-reviewer
    - visual-costume-reviewer
    - cinematography-reviewer
    - prompt-length-reviewer
  unlaunched_reviewers: []
  local_checklist_note: ""
  slot_bundle_findings: []
  merge_decision: pass | pass_with_followups | needs_rework | blocked
```

## Slot Bundles

Review source: `design-slot-review-contract.md`

```yaml
slot_bundles:
  - id: ROLE-BUNDLE-01
    owner: character-design-review
    required_slots:
      - character_id
      - deconstruction_subject_id
      - identity_evidence
      - visual_drivers
      - costume_design
      - prompt_evidence_chain
      - deconstruction_coverage
```

## Gate

- `slot_bundles` 不得为空。
- 每个 `required_slots` 必须有证据位置；缺槽必须写入 `slot_bundle_findings`，并阻断交付。
- 初始化综合消费 被上层策略或工具不可用时，使用本地 checklist 并保留汇流裁决。
- 初始化综合存在时，`init_synthesis_node_coverage` 必须记录初始化综合采纳内容绑定的当前思维·执行节点；不得只记录固定字段清单或成员名字。
- `merge_decision` 只能由主 agent 在读取 reviewer / 降级 checklist / slot bundle findings 后裁决。

## Review Gate Mapping

| Review Question | Review Gate | Fail Code | Rework Target | Report Evidence |
| --- | --- | --- | --- | --- |
| `slot_bundles: []` 是否仅被视为 legacy audit marker，canonical `slot_bundles` 是否按本合同下方非空定义交付？ | `GATE-CHAR-DESIGN-15` | `FAIL-SLOT-BUNDLE-MISSING` | `N8-REVIEW-GATE` | legacy marker 说明、canonical bundle 解析结果 |
| 每个角色主体是否形成完整 `workflow_supervision`，包含 `subject_id`、`dispatch_mode`、`blocking_layer`、`init_synthesis_source`、reviewer roster、local checklist、slot findings 与 `merge_decision`？ | `GATE-CHAR-DESIGN-16` | `FAIL-CHAR-DESIGN-SUPERVISION-PACKET` | `N6-INIT-SYNTHESIS-REVIEW` | `workflow_supervision_record` 完整字段检查 |
| `dispatch_mode` 为 `external_provider`、`local_checklist` 或 `user_disabled` 时，是否说明阻断层级/降级原因，且没有把不可用的外部 provider 伪报为已执行？ | `GATE-CHAR-DESIGN-16` | `FAIL-CHAR-DESIGN-SUPERVISION-PACKET` | `N6-INIT-SYNTHESIS-REVIEW` | dispatch mode、blocking layer、local checklist note |
| 初始化综合存在时，`init_team_synthesis_context` 与 `init_synthesis_node_coverage` 是否绑定当前 `node_ref / pass_ref / gate_ref`，并产生节点级判断、执行取舍、局部 patch 或风险提示？ | `GATE-CHAR-DESIGN-17` | `FAIL-INIT-SYNTHESIS-SKIPPED` | `N6-INIT-SYNTHESIS-REVIEW` | `init_synthesis_node_coverage`、初始化综合采纳内容与节点绑定记录 |
| 初始化综合记录是否避免退化为固定字段清单或成员名字堆砌，且初始化综合采纳内容被主 agent 转化为可执行 patch/risk 后才进入设计稿？ | `GATE-CHAR-DESIGN-17` | `FAIL-INIT-SYNTHESIS-SKIPPED` | `N6-INIT-SYNTHESIS-REVIEW` / `N7-MERGE-DRAFT` | init synthesis patch/risk 采纳记录、被拒绝建议说明 |
| `ROLE-BUNDLE-01` 的每个 required slot 是否有证据位置；缺槽是否写入 `slot_bundle_findings` 并阻断交付？ | `GATE-CHAR-DESIGN-15` | `FAIL-SLOT-BUNDLE-MISSING` | `N8-REVIEW-GATE` | required slot evidence map、blocking findings |
| `merge_decision` 是否由主 agent 在读取 reviewer、降级 checklist 与 slot bundle findings 后裁决，没有保留互相竞争的并列稿或让 reviewer 直接落盘 canonical 正文？ | `GATE-CHAR-DESIGN-18` | `FAIL-CHAR-DESIGN-MERGE-DECISION` | `N8-REVIEW-GATE` / `N7-MERGE-DRAFT` | `merge_decision`、采纳/拒绝 patch 记录、最终单稿声明 |
