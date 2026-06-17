# 场景 Workflow Supervision Contract

本合同监督 `场景/2-设计` 的初始化综合、reviewer 汇流路径。它不替代 `SKILL.md`、`SKILL.md` runtime spine 或 `review/`，只记录外部 provider 调度、不可用、本地 review 和 slot bundle 结论，避免 初始化综合消费或 reviewer 路径变成口头声明。

Legacy audit marker only: `slot_bundles: []` 表示旧审计器的字面兼容标记；本合同的 canonical `slot_bundles` 见下方非空定义，不允许交付空 bundle。

## Required Supervision Packet

每个被设计或审查的场景主体必须形成以下监督记录：

```yaml
workflow_supervision:
  subject_id: ""
  dispatch_mode: external_provider | local_checklist | user_disabled
  blocking_layer: none | system | developer | tool | user
  project_memory_source: "projects/aigc/<项目名>/MEMORY.md"
  project_memory_init_context: present | blocked | not_applicable
  init_synthesis_node_coverage:
    - node_ref: ""
      pass_ref: ""
      gate_ref: ""
      synthesis_lens: ""
  reviewer_roster:
    - research-reviewer
    - scene-design-reviewer
    - cinematography-reviewer
    - prompt-reviewer
  unlaunched_reviewers: []
  local_checklist_note: ""
  slot_bundle_findings: []
  merge_decision: pass | pass_with_followups | needs_rework | blocked
```

## Slot Bundles

Review source: `design-slot-review-contract.md`

```yaml
slot_bundles:
  - id: SCENE-BUNDLE-01
    owner: scene-design-review
    required_slots:
      - scene_id
      - deconstruction_subject_id
      - period_region_anchor
      - space_style_token
      - research_brief
      - source_posture
      - visual_translation
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
| 每个被设计或审查的场景主体是否都有非空 `workflow_supervision` 记录，而不是只在口头报告中声明已 review？ | `GATE-SCENE-DESIGN-12` | `FAIL-SCENE-DESIGN-WORKFLOW` | `N7-REVIEW` | 报告记录 `subject_id`、`dispatch_mode`、完整 packet 路径或本地记录位置。 |
| `dispatch_mode`、`blocking_layer`、`project_memory_source` 是否能说明外部 provider 可用性、上层阻断层级和项目 `MEMORY.md` 来源？ | `GATE-SCENE-DESIGN-12` | `FAIL-SCENE-DESIGN-WORKFLOW` | `N7-REVIEW` | 留下 provider 状态、阻断层级、项目记忆来源和降级理由。 |
| 项目记忆存在时，`project_memory_init_context` 与 `init_synthesis_node_coverage` 是否绑定当前 `node_ref / pass_ref / gate_ref`，并包含项目初始化记忆对节点判断、执行取舍、局部 patch 或风险提示的影响？ | `GATE-SCENE-DESIGN-11` | `FAIL-SCENE-DESIGN-11` | `N5-RESEARCH` | 报告记录项目记忆采纳内容、节点引用、gate 引用、记忆约束和进入研究/设计草稿的采纳点。 |
| `reviewer_roster` 是否覆盖 `research-reviewer`、`scene-design-reviewer`、`cinematography-reviewer`、`prompt-reviewer`，并明确记录未启动 reviewer 或本地 checklist 替代路径？ | `GATE-SCENE-DESIGN-12` | `FAIL-SCENE-DESIGN-WORKFLOW` | `N7-REVIEW` | 留下 reviewer roster、`unlaunched_reviewers`、`local_checklist_note` 和替代审查范围。 |
| `slot_bundles` 是否使用 canonical 非空 `SCENE-BUNDLE-01` 定义，而不是把 legacy audit marker `slot_bundles: []` 当作交付通过证据？ | `GATE-SCENE-DESIGN-SLOT-01` | `FAIL-SCENE-DESIGN-SLOT-01` | `N7-REVIEW` | 报告记录 bundle id、owner、required slots、legacy marker 是否仅作为兼容标记。 |
| `SCENE-BUNDLE-01.required_slots` 中的 `scene_id`、`deconstruction_subject_id`、`period_region_anchor`、`space_style_token`、`research_brief`、`source_posture`、`visual_translation`、`prompt_evidence_chain`、`deconstruction_coverage` 是否都有证据位置？ | `GATE-SCENE-DESIGN-SLOT-01` | `FAIL-SCENE-DESIGN-SLOT-01` | `N7-REVIEW` | 留下 slot evidence 表、缺槽名、证据位置和对应返工节点；`space_style_token` 必须说明类型选择依据，非建筑场景不得以建筑流派充数。 |
| 缺槽或 reviewer 阻断项是否写入 `slot_bundle_findings`，并阻断交付，而不是被降级为 followup 或被 `merge_decision: pass` 覆盖？ | `GATE-SCENE-DESIGN-SLOT-01` | `FAIL-SCENE-DESIGN-SLOT-01` | `N7-REVIEW` | 报告记录 finding severity、source contract、缺槽原因、返工入口和复核结果。 |
| `merge_decision` 是否由主 agent 在读取 reviewer / 本地 checklist / slot bundle findings 后裁决，且只能取 `pass`、`pass_with_followups`、`needs_rework` 或 `blocked`？ | `GATE-SCENE-DESIGN-12` | `FAIL-SCENE-DESIGN-WORKFLOW` | `N7-REVIEW` | 留下汇流依据、最终 verdict、阻断项处理、裁决者说明。 |
