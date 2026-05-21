# Review Contract

## Review Purpose

`3-导演` 的 review gate 验证逐集编导稿是否在编剧基础上注入了真正的导演创作干货：高潮画面承托、顾问参谋沉淀、场景状态差、受控增强留证、视觉美学组织、创意证据链和终结画面尾钩，并能被下游摄影、设计与视频链路稳定消费。

## Default Provider

- 默认辅助 provider：`code-reviewer`
- 用途：检查 Skill 2.0 包结构、脚本边界、输出合同和导演门禁。
- 若本轮启动 subagents 模式，review 还必须检查 `../../_shared/team-advisor-consultation-contract.md` 与 `../SKILL.md#Subagents Execution Mechanism`：是否优先从项目 `team.yaml.roles.supervision.stage_profiles."3-导演"` 或共享合同回退路径解析导演监制 roster、是否把顾问任务同步到当前 `steps/directing-workflow.md` 节点、`Thought Pass Map` 与相关 review gate、是否要求顾问代入角色意识/创作风格/专业水准参与节点判断和执行取舍、是否形成带 `node_ref/pass_ref/gate_ref/role_lens` 的 `advisor_consultation_packet`，以及顾问指导是否沉淀为后续任务上下文而未改写上游真源。
- review 必须加载 `../references/directorial-authorship-contract.md`，检查关键场景是否有真正编导创作干货：戏剧问题、人物压力、观众位置、信息释放、表演/空间/道具/声音发动机和可拍执行策略，而不是只做结构规整或漂亮改写。
- review 必须加载 `../references/episode-visual-spine-contract.md`，检查整集是否有 `episode_visual_spine`，并确认视觉问题、母题链、材质/色彩弧、节奏曲线、呼应目标和克制规则没有越过上游保真。
- review 必须加载 `../references/visual-aesthetic-contract.md`，检查关键场景是否有核心画面、视觉气质、画面层级、母题变化、对比轴、景境氛围、节奏和留白取舍，并确认这些内容内嵌到既有字段而未新增剧情事实或摄影方案。
- review 必须加载 `../references/atmosphere-and-mood-contract.md`，检查关键情绪场、压迫场、离别场或类型氛围场是否执行了 `atmosphere_mood_pass`，正文中是否能看到至少两个感官通道和至少一种意境技法，且意境细节没有新增剧情事实或抽象审美词空转。
- review 必须加载 `../references/episode-final-image-contract.md` 与 `../types/episode-final-image-type-map.md`，检查每集终结画面是否形成迷你彩蛋尾钩：与下一集真实关联但不剧透，并从本集内容丝滑顺延，且已完成环境描写式、道具特写式、情绪酝酿式或高潮结尾式的类型化匹配。
- review 必须加载 `../references/controlled-enrichment-contract.md`，检查新增承托细节是否有上游锚点、是否只属于表现层、是否记录 `controlled_enrichment_ledger`。
- review 必须加载 `../steps/directing-workflow.md#Thinking-Action Node Contract`，检查本轮经过的关键节点是否形成 `thinking_action_node_ledger`；每条节点记录必须同时包含判断问题、执行动作、证据字段、出口路由、gate 状态和 source owner。节点只写 checklist、只写"已优化"结论或没有失败回路时，必须判为 `needs_rework`。
- 若本轮新增或显著修改学习型合同，review 必须检查 `learning_integration_review_evidence`：静态接入点、真实样例或等价 smoke 状态、未覆盖风险和后续生产观察点必须写清；没有真实项目样例时只能标注 `static_only`，不得写成 fully verified。
- 若上层策略阻断真实 subagent 或 provider 调度，允许降级为本地 review checklist，并在报告中说明阻断来源、原计划 provider、实际路径和未启动 reviewer。

## Stage-End Review-Repair Rule

- 除 `review_only` 外，review gate 是写回前的阻断门，不是交付后的附带报告。
- `needs_rework` 必须回到 `steps/directing-workflow.md` 的 `N10R-DIR-REPAIR`，由 `3-导演` 本阶段直接做最小修复并复审；复审未通过不得写入 canonical `3-导演/第N集.md`。
- 允许直接修复的范围：高潮承托、视觉美学组织、终结画面尾钩内嵌、controlled enrichment 留证、顾问证据、思维·执行节点、frontmatter/report 证据和格式。
- 禁止直接修复的范围：新增或删减剧情事实、改写对白、改变事件顺序、替上游 `2-编剧` 修剧情、把 B 路线扩展为新增对白/桥段/因果。遇到这类问题必须输出 source owner 和阻断报告。
- `pass_with_followups` 只允许非阻断质量建议；任何高潮承托、顾问参谋、场景状态差、受控增强、视觉美学、终结画面、创作证据或思维·执行节点问题不得降级为 followup。

## Blocking Gates

| gate_id | check | fail_code |
| --- | --- | --- |
| `GATE-DIR-01` | 上游存在高潮/爽点/高光成分时，输出完成 `peak_visual_pass`，高点有可回指证据、可拍承托、状态差或余波，且没有新增事实、对白或因果 | `FAIL-PEAK-VISUAL` |
| `GATE-DIR-02` | 启动 subagents 模式时，已完成同步于当前思维·执行节点的 `team.yaml` 监制顾问请教，并沉淀为带节点锚点的后续上下文，或记录上层阻断降级 | `FAIL-ADVISOR-CONSULT` |
| `GATE-DIR-03` | 关键场景有可回指上游的进入状态、压力源、转折点和退出状态，或报告说明其过渡功能 | `FAIL-SCENE-TURN` |
| `GATE-DIR-04` | 启用 `controlled_enrichment` 时，每个新增承托细节都有上游锚点、目标字段、用途和风险检查，且没有新增对白/事件/因果/规则 | `FAIL-CONTROLLED-ENRICHMENT` |
| `GATE-DIR-05` | 已完成 `episode_visual_spine` 和 `visual_aesthetic_pass`：整集有视觉主轴，关键场景、强情绪场、压迫场、离别场、高潮场或类型氛围场有核心画面、视觉气质、画面层级、母题变化、对比轴、景境氛围、节奏和留白取舍；没有抽象审美词空转、细节堆砌、摄影越权或剧情新增 | `FAIL-VISUAL-AESTHETIC` |
| `GATE-DIR-06` | 执行报告包含 `director_substance_evidence`、`peak_visual_plan`、`advisor_consultation_packet`、`controlled_enrichment_ledger`、`visual_aesthetic_evidence`、`episode_final_image_evidence` 和 `atmosphere_mood_evidence`，能够证明编导判断、高潮画面、顾问参谋、受控增强、视觉美学、终结画面和氛围意境已经发生；非机械特例必须说明降级原因 | `FAIL-CREATIVE-EVIDENCE` |
| `GATE-DIR-07` | 每集已完成 `episode_final_image_pass`：终结画面作为迷你彩蛋尾钩，与下一集真实关联或明确为本集局部推断，不剧透下一集具体事件/结果/台词/新信息；已按类型化匹配选择环境描写式、道具特写式、情绪酝酿式或高潮结尾式，并从本集内容丝滑顺延到最后既有字段 | `FAIL-EPISODE-FINAL-IMAGE` |
| `GATE-DIR-08` | 关键情绪场、压迫场、离别场或类型氛围场已执行 `atmosphere_mood_pass`：正文中能看到至少两个感官通道（视觉、听觉、触觉、嗅觉、时间感）和至少一种意境技法（通感、微观放大、反衬、声景层次、延时承托、留白），且意境细节没有新增剧情事实、对白、事件、规则或抽象审美词空转 | `FAIL-ATMOSPHERE-MOOD` |

## Verdict Model

| verdict | meaning |
| --- | --- |
| `pass` | 可交付给下游阶段 |
| `pass_with_followups` | 可交付，但存在非阻断质量优化 |
| `needs_rework` | 存在高潮承托、顾问证据、受控增强、视觉美学、终结画面、氛围意境或创作证据阻断项 |
| `blocked` | 上游缺失、路径不可读、权限或策略阻断 |

## Report Shape

```yaml
review:
  verdict: pass | pass_with_followups | needs_rework | blocked
  source_script_path: projects/aigc/<项目名>/2-编剧/第N集.md
  output_path: projects/aigc/<项目名>/3-导演/第N集.md
  checks:
    peak_visual_treatment: pass
    advisor_consultation: pass
    scene_turn: pass
    controlled_enrichment: pass
    visual_aesthetic: pass
    atmosphere_mood: pass
    episode_final_image: pass
    creative_evidence: pass
    thinking_action_nodes: pass
    learning_integration_review: pass
    repair_loop: pass
  repair_actions: []
  re_review_verdict: pass
  director_substance_evidence:
    - scene_id: ""
      source_anchor: ""
      dramatic_question: ""
      audience_position: ""
      character_pressure: ""
      scene_turn: ""
      directorial_strategy: ""
      embedded_in_fields:
        - ""
      risk_check:
        fact_drift: false
        new_dialogue: false
        over_explaining: false
        cinematography_overreach: false
  peak_visual_plan:
    - scene_id: ""
      source_anchor: ""
      peak_type: "action_payoff | cognitive_flip | relationship_warmth | rule_revelation | spectacle | strange_landmark | micro_payoff"
      visual_target: ""
      sound_or_silence: ""
      performance_anchor: ""
      state_delta: ""
      embedded_in_fields:
        - ""
      risk_check:
        fact_drift: false
        new_dialogue: false
        new_event: false
  advisor_consultation_packet:
    status: not_applicable | completed | blocked
    roster_source_note: ""
    roster:
      - name: ""
        skill_path: ""
        selected_for: ""
    node_anchors:
      - node_ref: ""
        pass_ref: ""
        gate_ref: ""
        role_lens: ""
        accepted_guidance_summary: ""
        risk_flags: []
    routeback_targets:
      - node_ref: ""
        reason: ""
        resolution: "reworked | blocked"
    execution_brief: ""
    downgrade:
      blocked_by: "system | developer | tool | user | none"
      planned_path: ""
      actual_path: ""
      skipped_members: []
  controlled_enrichment_ledger:
    mode: none | controlled_supportive
    items:
      - source_anchor: ""
        target_field: ""
        purpose: ""
        risk_check:
          new_dialogue: false
          new_event: false
          new_rule: false
          new_clue: false
          new_causality: false
  visual_aesthetic_evidence:
    episode_visual_spine:
      visual_question: ""
      motif_chain: []
      material_and_color_arc: ""
      rhythm_curve: ""
      callback_targets: []
      episode_restraint_rule: ""
    scene_items:
      - scene_id: ""
        source_anchor: ""
        visual_tone: ""
        core_image: ""
        image_motif: ""
        contrast_axis: ""
        atmospheric_scenery: ""
        rhythm_and_negative_space: ""
        embedded_in_fields:
          - ""
        risk_check:
          fact_drift: false
          new_dialogue: false
          cinematography_overreach: false
        detail_bloat: false
  episode_final_image_evidence:
    final_image_type_profile:
      next_episode_context_status: next_episode_readable | episode_local_only
      final_anchor_surface: environment | prop | emotion | peak_aftershock | mixed
      hook_promise_type: suspense | danger | relationship_unfinished | information_gap | theme_stamp | emotional_aftertaste | state_reversal
      spoiler_risk_level: low | medium | high
      continuity_mode: smooth_extension | callback_variation | aftershock_hold | unresolved_action
      preferred_method: environmental_tag | prop_closeup_tag | emotional_brew_tag | climax_tail_tag
    plan:
      source_anchor: ""
      next_episode_relation: ""
      spoiler_boundary: ""
      continuity_bridge: ""
      hook_surface: ""
      final_image_method: environmental_tag | prop_closeup_tag | emotional_brew_tag | climax_tail_tag
      final_field_projection:
        - ""
      risk_check:
        fact_drift: false
        new_dialogue: false
        next_episode_spoiler: false
        new_clue_or_rule: false
        cinematography_overreach: false
  atmosphere_mood_evidence:
    - scene_id: ""
      source_anchor: ""
      target_mood: ""
      technique_used: "synesthesia | micro_zoom | contrast | soundscape_layering | delayed_perception | negative_space"
      sensory_channels:
        visual: ""
        auditory: ""
        tactile: ""
        olfactory: ""
        temporal: ""
      sound_atmosphere: ""
      embedded_in_fields:
        - ""
      risk_check:
        fact_drift: false
        new_event: false
        new_dialogue: false
        abstract_aesthetic: false
  thinking_action_node_ledger:
    - node_id: ""
      judgment_question: ""
      decision: "pass | needs_rework | blocked | routeback | not_applicable"
      actions_taken:
        - ""
      evidence_keys:
        - ""
      route_out: ""
      gate_status:
        passed: true
        fail_code: ""
      source_owner: ""
  learning_integration_review_evidence:
    status: "real_sample_verified | smoke_verified | static_only | blocked | not_applicable"
    changed_contracts:
      - ""
    static_integration_points:
      - ""
    sample_or_smoke_check:
      source_anchor: ""
      output_anchor: ""
      evidence_anchor: ""
      result: ""
    residual_risks:
      - ""
    next_runtime_observation:
      - ""
  findings: []
```

当 `advisor_consultation_packet.status == completed` 时，`node_anchors` 至少包含一个带 `node_ref/pass_ref/gate_ref/role_lens` 的采纳摘要；若顾问指出前置节点问题，`routeback_targets` 必须记录回修节点、原因和处理结果。若真实 subagent dispatch 被阻断，`downgrade` 必须完整记录阻断层级、原计划路径、实际路径和未启动成员。

`director_substance_evidence` 必须证明关键场景的编导判断来自上游原文，并已经进入正文具体字段；只写"戏剧张力更强""电影感更好""节奏更紧"但缺少动作、声音、空间、道具、表演或观众位置证据时，verdict 必须为 `needs_rework`。
