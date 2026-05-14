# 角色 Subagent Supervision Contract

本合同监督 `角色/2-设计` 的顾问、worker、reviewer 汇流路径。它不替代 `SKILL.md`、`steps/` 或 `review/`，只记录真实 dispatch、上层阻断、降级 review 和 slot bundle 结论，避免 subagent 路径变成口头声明。

Legacy audit marker only: `slot_bundles: []` 表示旧审计器的字面兼容标记；本合同的 canonical `slot_bundles` 见下方非空定义，不允许交付空 bundle。

## Required Supervision Packet

每个被设计或审查的角色主体必须形成以下监督记录：

```yaml
subagent_supervision:
  subject_id: ""
  dispatch_mode: real_subagents | local_downgrade | user_disabled
  blocking_layer: none | system | developer | tool | user
  advisor_roster_source: "projects/aigc/<项目名>/team.yaml"
  advisor_consultation_packet: present | blocked | not_applicable
  advisor_node_coverage:
    - node_ref: ""
      pass_ref: ""
      gate_ref: ""
      advisor_lens: ""
  reviewer_roster:
    - character-research-reviewer
    - visual-costume-reviewer
    - cinematography-reviewer
    - prompt-length-reviewer
  unlaunched_reviewers: []
  downgrade_report: ""
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
- 真实 subagents 被上层策略或工具阻断时，必须写明 `blocking_layer`、原计划 reviewer、实际降级路径和未启动 reviewer。
- 启用顾问路径时，`advisor_node_coverage` 必须记录顾问意见绑定的当前思维·执行节点；不得只记录固定字段清单或顾问名字。
- `merge_decision` 只能由主 agent 在读取 reviewer / 降级 checklist / slot bundle findings 后裁决。
