# 角色 Workflow Supervision Contract

本合同监督 `角色/2-设计` 的初始化综合、worker、reviewer 汇流路径。它不替代 `SKILL.md` 或 `review/`，只记录外部 provider 调度、不可用、本地 review 和 slot bundle 结论，避免 初始化综合消费 路径变成口头声明。

Legacy audit marker only: `slot_bundles: []` 表示旧审计器的字面兼容标记；本合同的 canonical `slot_bundles` 见下方非空定义，不允许交付空 bundle。

## Required Supervision Packet

每个被设计或审查的角色主体必须形成以下监督记录：

```yaml
workflow_supervision:
  subject_id: ""
  base_subject_id: ""
  variant_id: "default"
  variant_label: "default"
  variant_type: "default"
  asset_id: ""
  dispatch_mode: external_provider | local_checklist | user_disabled
  blocking_layer: none | system | developer | tool | user
  init_synthesis_source: "projects/aigc/<项目名>/MEMORY.md"
  project_memory_init_context: present | blocked | not_applicable
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
      - base_subject_id
      - asset_id
      - variant_id
      - variant_label
      - variant_type
      - identity_invariants
      - variant_state_delta
      - deconstruction_subject_id
      - identity_evidence
      - visual_drivers
      - aesthetic_appeal
      - lead_beauty_handsomeness_floor
      - lead_presence_temperament_floor
      - charisma_floor
      - height_scale
      - body_build
      - hair_design
      - costume_color_palette
      - face_readability_lighting
      - corpus_usage_trace
      - costume_design
      - prompt_evidence_chain
      - deconstruction_coverage
```

## Gate

- `slot_bundles` 不得为空。
- 每个 `required_slots` 必须有证据位置；缺槽必须写入 `slot_bundle_findings`，并阻断交付。
- 项目记忆初始化上下文消费 被上层策略或工具不可用时，使用本地 checklist 并保留汇流裁决。
- 项目记忆初始化上下文存在时，`init_synthesis_node_coverage` 必须记录采纳内容绑定的当前思维·执行节点；不得只记录固定字段清单或成员名字。
- `merge_decision` 只能由主 agent 在读取 reviewer / 降级 checklist / slot bundle findings 后裁决。

## Review Gate Mapping

| Review Question | Review Gate | Fail Code | Rework Target | Report Evidence |
| --- | --- | --- | --- | --- |
| `slot_bundles: []` 是否仅被视为 legacy audit marker，canonical `slot_bundles` 是否按本合同下方非空定义交付？ | `GATE-CHAR-DESIGN-15` | `FAIL-SLOT-BUNDLE-MISSING` | `N8-REVIEW-GATE` | legacy marker 说明、canonical bundle 解析结果 |
| 每个角色主体是否形成完整 `workflow_supervision`，包含 `subject_id`、`dispatch_mode`、`blocking_layer`、`init_synthesis_source`、reviewer roster、local checklist、slot findings 与 `merge_decision`？ | `GATE-CHAR-DESIGN-16` | `FAIL-CHAR-DESIGN-SUPERVISION-PACKET` | `N6-INIT-SYNTHESIS-REVIEW` | `workflow_supervision_record` 完整字段检查 |
| `dispatch_mode` 为 `external_provider`、`local_checklist` 或 `user_disabled` 时，是否说明阻断层级/降级原因，且没有把不可用的外部 provider 伪报为已执行？ | `GATE-CHAR-DESIGN-16` | `FAIL-CHAR-DESIGN-SUPERVISION-PACKET` | `N6-INIT-SYNTHESIS-REVIEW` | dispatch mode、blocking layer、local checklist note |
| 项目记忆初始化上下文存在时，`project_memory_init_context` 与 `init_synthesis_node_coverage` 是否绑定当前 `node_ref / pass_ref / gate_ref`，并产生节点级判断、执行取舍、局部 patch 或风险提示？ | `GATE-CHAR-DESIGN-17` | `FAIL-INIT-SYNTHESIS-SKIPPED` | `N6-INIT-SYNTHESIS-REVIEW` | `init_synthesis_node_coverage`、初始化上下文采纳内容与节点绑定记录 |
| 初始化综合记录是否避免退化为固定字段清单或成员名字堆砌，且初始化综合采纳内容被主 agent 转化为可执行 patch/risk 后才进入设计稿？ | `GATE-CHAR-DESIGN-17` | `FAIL-INIT-SYNTHESIS-SKIPPED` | `N6-INIT-SYNTHESIS-REVIEW` / `N7-MERGE-DRAFT` | init synthesis patch/risk 采纳记录、被拒绝建议说明 |
| `ROLE-BUNDLE-01` 的每个 required slot 是否有证据位置；缺槽是否写入 `slot_bundle_findings` 并阻断交付？ | `GATE-CHAR-DESIGN-15` | `FAIL-SLOT-BUNDLE-MISSING` | `N8-REVIEW-GATE` | required slot evidence map、blocking findings |
| `base_subject_id / asset_id / variant_id / identity_invariants / variant_state_delta` 是否有证据位置，并证明多状态稿没有变成新 base character？ | `GATE-CHAR-DESIGN-23` | `FAIL-CHAR-DESIGN-VARIANT-INVARIANT` | `N5-RESEARCH-PROFILE` / `N7-MERGE-DRAFT` | variant slot evidence map、base/variant/asset ID 对照、blocking findings |
| `aesthetic_appeal / lead_beauty_handsomeness_floor / lead_presence_temperament_floor / charisma_floor` slot 是否覆盖来源匹配审美路线、容貌、妆发、骨相、身形、服装吸引力、主角帅/美下限、主角整体气质下限、主角/大反派高魅力下限、普通正反派个性魅力和真实人物灵感许可/原创转译边界？ | `GATE-CHAR-DESIGN-19` | `FAIL-CHAR-DESIGN-AESTHETIC-APPEAL` | `N7-MERGE-DRAFT` | aesthetic/lead beauty/lead presence/charisma slot evidence map、blocking findings |
| `height_scale / body_build / hair_design / costume_color_palette` slot 是否覆盖身高档位/安全范围、身形结构、比例重心、发型长度/体量/轮廓/时代职业适配、服装主辅点缀色与配色逻辑？ | `GATE-CHAR-DESIGN-21` | `FAIL-CHAR-DESIGN-PHYSICAL-STYLING` | `N5-RESEARCH-PROFILE` / `N7-MERGE-DRAFT` | physical styling slot evidence map、blocking findings |
| `face_readability_lighting` slot 是否覆盖清晰眉眼、鼻梁、嘴部、骨相、肤色层次和表情意图，并避免重阴影、遮眼阴影、半脸阴影或低调剪影遮脸？ | `GATE-CHAR-DESIGN-22` | `FAIL-CHAR-DESIGN-FACE-READABILITY` | `N5-RESEARCH-PROFILE` / `N7-MERGE-DRAFT` | face readability slot evidence map、blocking findings |
| `corpus_usage_trace` slot 是否说明语料库触发、原创转译、服装时代语境和被剔除语料，且没有逐字套用或时代错配？ | `GATE-CHAR-DESIGN-20` | `FAIL-CHAR-DESIGN-CORPUS-MISSING` | `N5-RESEARCH-PROFILE` / `N7-MERGE-DRAFT` | corpus usage slot evidence map、blocking findings |
| `merge_decision` 是否由主 agent 在读取 reviewer、降级 checklist 与 slot bundle findings 后裁决，没有保留互相竞争的并列稿或让 reviewer 直接落盘 canonical 正文？ | `GATE-CHAR-DESIGN-18` | `FAIL-CHAR-DESIGN-MERGE-DECISION` | `N8-REVIEW-GATE` / `N7-MERGE-DRAFT` | `merge_decision`、采纳/拒绝 patch 记录、最终单稿声明 |
