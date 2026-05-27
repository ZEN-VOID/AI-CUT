# Review Contract

## Review Purpose

`4-表演` 的 review gate 验证逐集编导稿中的表演层是否到位：心理反应可演可感知、演员演技控制精准、每段对白都有语气情绪和气口断句等台词表演锚点、主角内心独白人称正确、动作字段客观可拍、道具承托通过互动准入、表演提示和场面调度已拆入对应剧本句段而非末尾总结，并能被下游摄影和视频链路稳定消费。

## Default Provider

- 默认辅助 provider：`code-reviewer`
- 用途：检查 Skill 2.0 包结构、脚本边界、输出合同和表演字段门禁。
- review 必须加载 `../references/performance-and-scene-craft-contract.md`，检查场景状态差、台词表演、潜台词行为、演员任务、场面调度内嵌、沉默反应和摄影越权风险。
- review 必须加载 `../../_shared/action-first-continuity-contract.md`，检查人物动作链、空间可达性、情绪动作经济和道具/环境准入；任何因动作堆叠、空间不可达或无互动对象抢表演导致下游摄影/分组难以连续承接的问题必须阻断。
- review 必须加载 `../../_shared/lived-in-character-behavior-contract.md`，检查关键人物 beat 是否避免空闲摆拍：单人 beat 有场景内成立的当前小事、下意识反应和情绪落点；多人 beat 有行动者/反应者分工，且没有随机忙动作或人人同强度表演。
- review 必须加载 `../references/psychological-reaction-contract.md`，检查 `心理反应` 是否有主体、有上游触发点、有可见/可听/可演通道，主角内心想法和主角视角判断是否保留为 `独白/内心独白` 或可感知反应，且没有抽象想象、内心解释、因果论文、未授权新对白、无关回忆或场景末尾总结块。
- review 必须加载 `../references/actor-performance-control-contract.md`，检查关键情绪 beat 是否避免情绪标签和模板化表情，是否具备上游触发点、情绪动机、微表情、非面部生理联动、台词语气情绪、气口断句、环境声音或沉默余波、微动态限制，并已内嵌到既有字段而未新增剧情、对白或摄影方案。
- review 必须检查上游 `long_dialogue_beat_map` 是否被消费为 `long_dialogue_delivery_map`：每个长对白节拍都有气口/连续气息、停顿或无停顿依据、重音、尾音、身体联动和对手反应，且未改写或重切上游原文节拍。
- review 必须加载 `../../3-导演/references/performance-style-directive-contract.md`，检查 `performance_style_directive` 是否进入角色外放度、身体性、声线、面具/真实轴、风格转变触发和具体表演取舍。
- review 必须加载 `../../_shared/audience-psychology-model-contract.md`，检查 `audience_psychology_map` 与 `conflict_legacy_transfer` 是否进入知情层级、反应强度、沉默长度、潜台词行为和群戏注意力分配。
- review 必须加载 `../../_shared/emotional-rhythm-map-contract.md`，检查 `scene_emotional_register` 与 `genre_emotional_coloring` 是否进入表演强度预算，避免每场同强度演满。
- review 必须加载 `../references/character-arc-performance-contract.md`，检查关键角色是否有弧线阶段、变化方向、弧线锚点和跨场景表演演进。
- review 必须加载 `../references/ensemble-performance-contract.md`，检查群戏是否有前景行动者、前景反应者、中景知情者和背景环境参与者的层次分配。
- review 必须加载 `../references/physiological-realism-contract.md`，检查强情绪和强身体状态后的生理残留、过渡和因果链是否可信。
- review 必须加载 `../types/type-map.md` 与 `../types/performance-evidence-type-map.md`，检查 `performance_type_profile`、证据字段 owner、required shape 和 consumed_by 是否一致。
- review 必须加载 `../../_shared/concrete-visual-language-contract.md`，检查表演阶段自身的心理反应、演员控制、台词表演、潜台词行为、场面调度、顾问意见、执行报告和最终落盘是否使用具像表演语言；不得把 `2-编剧` / `3-导演` 已完成的画面化成果重新抽象成情绪标签、心理解释、关系概念、权力概念或表演意图总结。
- 若本轮执行顾问与复核流程，review 还必须加载 `../../_shared/team-advisor-consultation-contract.md` 与 `../SKILL.md#Advisor Consultation Mechanism`，检查是否优先从 `team.yaml.roles.supervision.stage_profiles."4-表演"` 解析表演监制 roster、是否基于当前 `PASS-PERF-*` / `N*-PERF-*` 思维·执行节点派生顾问问题、是否形成 `advisor_consultation_packet`，以及顾问指导是否沉淀为后续任务上下文而未改写 `3-导演` 原文。
- 若上层策略阻断顾问与复核流程 或 provider 调度，允许使用本地 review checklist，并使用本地 review checklist。

## Stage-End Review-Repair Rule

- 除 `review_only` 外，review gate 是写回前的阻断门，不是交付后的附带报告。
- `needs_rework` 必须回到 `steps/directing-workflow.md` 的 `N8R-PERF-REPAIR`，由 `4-表演` 本阶段直接做最小修复并复审；复审未通过不得写入 canonical `4-表演/第N集.md`。
- 允许直接修复的范围：心理反应可感知化、台词语气情绪与气口断句补足、表演提示内嵌、场面调度内嵌、沉默反应、人物动作链/空间可达性补足、情绪动作经济收敛、无互动道具冗余删除或降级、活人感小事/下意识反应/情绪落点补足、多人动作-反应分工收敛、主角内心独白回收、动作客观可拍化、直接情绪转译、具像表演语言回收、frontmatter/report 证据和格式。
- 禁止直接修复的范围：新增或删减剧情事实、改写对白、改变事件顺序、替上游 `2-编剧` 或 `3-导演` 修剧情。遇到这类问题必须输出 source owner 和不可用说明。
- `pass_with_followups` 只允许非阻断质量建议；任何心理反应、演员控制、主角内心、动作纯度或表演集成问题不得降级为 followup。

## Blocking Gates

| gate_id | check | fail_code |
| --- | --- | --- |
| `GATE-PERF-01` | 心理反应、演员控制、台词表演、主角内心独白和动作纯度全部达标：`心理反应` 有主体、触发点和可见/可听/可演通道；关键情绪 beat 避免情绪标签空转，有触发点、情绪动机、微表情、非面部身体联动或环境声音承托；每段 `对白（角色，...）` 第二项写清语气/情绪/状态，关键对白有气口、断句、停顿、声线、重音、尾音或对手反应承托且引号内对白未改写；`内心独白（主角）` 引号内指代主角自身时使用第一人称；`角色动作` / `动作画面` 只写客观可拍动作，不含主观预判或心理意图词 | `FAIL-PERFORMANCE-TASK` / `FAIL-PERF-03A` |
| `GATE-PERF-02` | 表演提示和场面调度已拆入对应画面、动作、对白画面、道具、群像、声音或反应字段，没有在场景末尾或分镜组末尾总结式列出；场面调度不写机位、景别、镜头运动、分镜编号或 `分镜明细预设` | `FAIL-PERFORMANCE-INTEGRATION` |
| `GATE-PERF-03` | 执行顾问与复核流程时，已完成 `team.yaml` 表演监制顾问请教；顾问问题同步于当前思维·执行节点，并沉淀为后续上下文，或使用本地流程 | `FAIL-PERF-13A` |
| `GATE-PERF-04` | 道具承托通过互动准入：道具只在角色明确互动、关键剧情/规则/证据/危险源或必要环境交代时进入表演；没有用无互动道具的倒影、涟漪、碰撞声、阴影压物等孤立细节替代表演 | `FAIL-PERF-15` |
| `GATE-PERF-05` | 人物动作链和空间可达性通过：关键 beat 可读出人物姿态、位置、朝向、动作向量、可达对象和退出状态；强情绪没有堆叠低信息动作，无互动环境/道具反应没有打断表演 | `FAIL-ACTION-FIRST-02` / `FAIL-ACTION-FIRST-03` / `FAIL-ACTION-FIRST-04` |
| `GATE-PERF-06` | 活人感行为通过：关键单人 beat 有当前小事、下意识反应和情绪落点；多人 beat 明确 `action_driver/reaction_receiver`，没有让所有角色同等强度表演，也没有随机忙动作或无互动道具伪装真实 | `FAIL-LIVED-IN-01` / `FAIL-LIVED-IN-02` / `FAIL-LIVED-IN-03` / `FAIL-LIVED-IN-04` |
| `GATE-PERF-07` | 角色弧线表演通过：关键角色有 `character_arc_profile`，表演强度、压抑/释放方向、本集起点、变化方向和弧线锚点可回指上游导演证据 | `FAIL-CHARACTER-ARC-PERFORMANCE` |
| `GATE-PERF-08` | 群戏表演层次通过：多人场面有 `ensemble_layers`，区分前景行动者、前景反应者、中景知情者和背景环境参与者；没有人人同强度抢戏 | `FAIL-ENSEMBLE-PERFORMANCE` |
| `GATE-PERF-09` | 生理真实性通过：强情绪、奔跑、恐惧、震惊、哭泣、冷热变化后有可见身体残留和过渡，未从极端状态瞬间无代价恢复 | `FAIL-PHYSIOLOGICAL-REALISM` |
| `GATE-PERF-10` | 导演表演风格消费通过：`performance_style_directive` 已进入关键角色外放度、身体性、声线、面具/真实轴、风格转变触发和具体表演取舍 | `FAIL-PERFORMANCE-STYLE-CONSUMPTION` |
| `GATE-PERF-11` | 观众心理消费通过：`audience_psychology_map` 与 `conflict_legacy_transfer` 已影响知情层级、反应强度、沉默长度、潜台词行为和群戏注意力分配 | `FAIL-AUDIENCE-PSYCHOLOGY-CONSUMPTION` |
| `GATE-PERF-12` | 情绪节奏消费通过：`scene_emotional_register` 与 `genre_emotional_coloring` 已进入表演强度预算，没有每场同强度演满或同强度压低 | `FAIL-EMOTIONAL-RHYTHM-CONSUMPTION` |
| `GATE-PERF-13` | 独白预算通过：内心独白、旁白和解释性心理文字未挤占影视呈现；可外显内容已转成表演、动作、沉默或可感知反应 | `FAIL-MONOLOGUE-BUDGET` |
| `GATE-PERF-14` | 长对白交付链通过：上游 `long_dialogue_beat_map` 已转为 `long_dialogue_delivery_map`，每个节拍有气口/连续气息、停顿、重音、尾音、身体联动和对手反应；没有改写、合并吞并或重新断开原文节拍 | `FAIL-LONG-DIALOGUE-DELIVERY` |
| `GATE-PERF-15` | 表演阶段自身的心理反应、演员控制、台词表演、潜台词行为、场面调度、顾问意见、执行报告和最终落盘均通过具像表演语言检查：心理、情绪、关系、权力和表演判断落到可见身体、可听声音、可演停顿、空间距离、道具互动或对手反应；没有重新抽象成情绪标签、心理解释、概念关系或表演意图总结；所有投影仍保持上游保真 | `FAIL-CONCRETE-PERFORMANCE-LANGUAGE` |

## Verdict Model

| verdict | meaning |
| --- | --- |
| `pass` | 可交付给下游阶段 |
| `pass_with_followups` | 可交付，但存在非阻断质量优化 |
| `needs_rework` | 存在心理反应、演员控制、台词表演、主角内心、动作纯度、具像表演语言或表演集成阻断项 |
| `blocked` | 上游缺失、路径不可读、权限或策略阻断 |

## Report Shape

```yaml
review:
  verdict: pass | pass_with_followups | needs_rework | blocked
  source_script_path: projects/aigc/<项目名>/2-编剧/第N集.md
  output_path: projects/aigc/<项目名>/4-表演/第N集.md
  checks:
    psychological_reaction: pass
    actor_performance_control: pass
    dialogue_performance: pass
    long_dialogue_delivery: pass
    performance_style_consumption: pass
    audience_psychology_consumption: pass
    emotional_rhythm_consumption: pass
    monologue_budget: pass
    concrete_visual_language: pass
    protagonist_inner_voice: pass
    objective_action_purity: pass
    prop_interaction_economy: pass
    action_first_continuity: pass
    lived_in_behavior: pass
    action_reaction_focus: pass
    emotional_action_economy: pass
    performance_integration: pass
    advisor_consultation: pass
    repair_loop: pass
  repair_actions: []
  re_review_verdict: pass
  psychological_reaction_evidence:
    - scene_id: ""
      source_anchor: ""
      subject: ""
      reaction_function: "fear | recognition | suspicion | concealment | shame | trust_shift | power_pressure | withheld_speech | reasoning | memory"
      pov_owner: "protagonist | other_character | external"
      trigger: ""
      performance_task: ""
      getability_channels:
        visible: []
        audible: []
        performable: []
      target_fields:
        - "心理反应"
      risk_check:
        abstract_inner_life: false
        new_dialogue: false
        new_event: false
        over_explaining: false
        field_summary_block: false
        subjective_intent_in_action: false
        unrelated_backstory: false
        third_person_pov_judgment: false
  actor_performance_control_evidence:
    - scene_id: ""
      source_anchor: ""
      subject: ""
      trigger: ""
      surface_emotion: ""
      suppressed_emotion: ""
      hidden_motive: ""
      micro_expression:
        brow: ""
        eyes: ""
        mouth: ""
        facial_muscle: ""
      body_linkage:
        breath: ""
        hands: ""
        posture: ""
        object_action: ""
        voice: ""
      ambient_support:
        sound: ""
        silence_or_room_tone: ""
        environment: ""
      micro_dynamics: ""
      embedded_in_fields:
        - ""
      risk_check:
        emotion_label_only: false
        template_expression: false
        overacting: false
        new_dialogue: false
        new_event: false
        cinematography_overreach: false
  dialogue_performance_evidence:
    - scene_id: ""
      dialogue_anchor: ""
      speaker: ""
      tone_state: ""
      emotional_pressure: ""
      breath_point: ""
      pause_pattern: ""
      voice_control: ""
      paired_body_or_opponent_reaction: ""
      risk_check:
        missing_dialogue_state: false
        vague_emotion_label: false
        dialogue_text_changed: false
  long_dialogue_delivery_map:
    - scene_id: ""
      dialogue_anchor: ""
      speaker: ""
      source_beat_map_ref: ""
      delivery_beats:
        - beat_id: ""
          exact_text_segment_ref: ""
          tone_shift: ""
          breath_point: ""
          pause_pattern: ""
          stress_word_or_phrase: ""
          ending_control: ""
          body_linkage: ""
          opponent_reaction: ""
      risk_check:
        dialogue_text_changed: false
        beat_recut_without_source_owner: false
        same_delivery_for_all_beats: false
        missing_opponent_reaction_chain: false
  concrete_visual_language_evidence:
    - stage: "4-表演"
      node_id: ""
      source_anchor: ""
      abstract_or_conceptual_risk: ""
      concrete_projection: ""
      target_fields:
        - ""
      sensory_or_performable_channels:
        visible: []
        audible: []
        performable: []
        spatial_or_prop: []
      risk_check:
        abstract_language_residue: false
        concept_residue: false
        explanatory_residue: false
        upstream_visualization_regressed: false
        fact_drift: false
  lived_in_behavior_evidence:
    - scene_id: ""
      source_anchor: ""
      subject: ""
      micro_activity: ""
      subconscious_response: ""
      emotional_landing: ""
      action_reaction_pair:
        action_driver: ""
        reaction_receiver: ""
        ambient_participants: []
      embedded_in_fields:
        - ""
      risk_check:
        idle_pose_or_face_only: false
        random_busywork: false
        all_characters_performing: false
        prop_admission_bypassed: false
        missing_exit_state: false
  protagonist_inner_voice_evidence:
    - scene_id: ""
      source_anchor: ""
      protagonist: ""
      original_subjective_judgment: ""
      target_field: "内心独白（主角）"
      paired_visual_field: "内心独白画面"
      risk_check:
        third_person_pov_judgment: false
        new_dialogue: false
        unrelated_backstory: false
  objective_action_purity_evidence:
    - scene_id: ""
      field: "角色动作 | 动作画面"
      removed_subjective_wording: []
      objective_projection: ""
      risk_check:
        subjective_intent_in_action: false
        direct_emotion_label: false
  findings: []
  advisor_consultation_packet:
    status: "present | local_checklistd | not_applicable"
    roster_source_note: ""
    node_refs: []
    execution_brief: ""
    local_checklist:
      findings: []
      repair_actions: []
```
