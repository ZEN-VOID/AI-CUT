# Output Template

## Output Contract Alignment

### Required output

- `OUTPUT-SCREENWRITING-EPISODE`: `projects/aigc/<项目名>/2-编剧/第N集.md`
- `OUTPUT-SCREENWRITING-REPORT`: `projects/aigc/<项目名>/2-编剧/执行报告.md`

### Output format

- 逐集编剧稿：Markdown，含 YAML frontmatter、`【剧本正文】`、场景标题和字段化剧本正文。
- 执行报告：Markdown，记录输入、目标集、review verdict、直接修复项、复审结果、`thinking_action_node_ledger`、`learning_integration_review_evidence`、`novel_expression_transform_evidence`、`psychological_reaction_evidence`、`actor_performance_control_evidence`、`director_substance_evidence`、`episode_visual_spine`、`visual_aesthetic_evidence`、`episode_final_image_evidence`、`advisor_consultation_packet` 节点锚点、遗留风险和下游 handoff。

### Output path

```text
projects/aigc/<项目名>/2-编剧/
├── 第1集.md
├── 第2集.md
└── 执行报告.md
```

### Naming convention

- 逐集编导稿：`第N集.md`
- 报告：`执行报告.md`

### Completion gate

- 上游 `1-分集/第N集.md` 已回指。
- 事实、顺序和对白保真。
- 对白字段标题为 `对白（真实角色名，语态/状态短语）`，第二项不强制一词或以“地”结尾；不得输出 `对白（原文角色）`、`对白（角色名）`、`对白（某人）` 或缺少语态/状态的旧格式。
- 声画配对、字段纯度和 slugline 稳定通过 review。
- 终稿没有内部任务说明、模板占位句或规则复述；`环境描写` 只写场景本身的写景画面，不混入人物动作、对白引出、剧情结果或心理解释；同一 slugline 下可在开篇之外因空间/背景/光线/空气/材质焦点变化再次出现环境描写。
- 小说原文中的作者评论、心理内视、比喻象征、概括叙述、背景说明、因果解释、关系结论、感官散文或武侠/玄幻抽象已按 `novel_expression_transform_pass` 二次画面化；引号内对白仍逐字冻结，小说叙述没有被改成新增台词。
- 主角内心想法、内心独白和主角视角下对他人行为的判断已保留为 `独白/内心独白` 或可感知反应；没有被改成客观第三方概括。`角色动作` / `动作画面` 只写镜头可实拍的客观动作、神态、语气和生理反应，没有“试图、想要、打算、意图”等主观预判词；直接情绪感受已按主落点转成 `表情特写`、微表情、肢体动作、生理反应、环境声音承托或主角内心独白。
- 关键面部表演 beat 可使用正式字段 `表情特写`；该字段只写眉、眼、嘴、鼻翼、咬肌、下颌、喉头、眨眼频率或皮肤状态等可见面部变化，必须能回指上游触发或当前声画压力，不写情绪标签、心理解释、摄影机位、景别或镜头运动。
- 终稿没有抽象概括、无法实拍的总结句、体现重复/熟悉/往日常态的无画面句；没有新增与当前主线无关的人物过往背景、物品来历或回忆性信息。
- 关键情绪场、压迫场、离别场或类型氛围场的 `环境描写` 有足够景境承托；新增自然景物只改变氛围密度，不改变剧情条件。
- 编剧稿没有提前承担 `3-导演` 的导演创作内核、终结画面、视觉主轴、氛围意境或 `4-表演` 的演员工艺控制；相关下游任务只保留可消费的声画基础。
- 终稿未写机位、景别、镜头运动、分镜编号或 `分镜明细预设`。
- 若执行顾问与复核流程，执行报告含 `advisor_consultation_packet` 摘要，至少记录 `node_ref/pass_ref/gate_ref/role_lens`、采纳指导、风险提示和 `routeback_targets`；否则直接使用本地 checklist。
- 执行报告含 `thinking_action_node_ledger`，覆盖本轮经过的关键思维·执行节点；每条节点记录必须包含判断问题、判断结果、执行动作、证据字段、出口路由、gate 状态和 source owner。
- 新增或显著修改学习型合同时，执行报告含 `learning_integration_review_evidence`；若没有真实项目样例，只能标注 `static_only`，并写出残余风险和下一次生产运行观察点。
- 若 review 发现阻断项，已在 `2-编剧` 阶段内直接最小修复并复审通过；若无法修复，已使用本地流程且不得推进下游。
- 执行报告记录 review verdict、repair actions、re-review verdict、残余风险和是否允许进入 `3-导演`。

## Report Evidence Blocks

执行报告必须包含或等价覆盖：

```yaml
advisor_consultation_packet:
  status: not_applicable | completed | blocked
  roster: []
  node_anchors: []
  routeback_targets: []
  execution_brief: ""
  local_checklist:
    findings: []
    repair_actions: []
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
  changed_contracts: []
  static_integration_points: []
  sample_or_smoke_check:
    source_anchor: ""
    output_anchor: ""
    evidence_anchor: ""
    result: ""
  residual_risks: []
  next_runtime_observation: []
director_substance_evidence:
  - scene_id: ""
    source_anchor: ""
    dramatic_question: ""
    audience_position: ""
    character_pressure: ""
    scene_turn: ""
    directorial_strategy: ""
    embedded_in_fields: []
    risk_check:
      fact_drift: false
      new_dialogue: false
      over_explaining: false
      cinematography_overreach: false
novel_expression_transform_evidence:
  - source_anchor: ""
    expression_type: ""
    source_function: ""
    screen_strategy: ""
    target_fields: []
    artistic_transform: ""
    risk_check:
      fact_drift: false
      new_event: false
      new_dialogue: false
      over_explaining: false
      cinematography_overreach: false
      subjective_intent_in_action: false
      unrelated_backstory: false
      third_person_pov_judgment: false
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
    embedded_in_fields: []
    risk_check:
      emotion_label_only: false
      template_expression: false
      overacting: false
      new_dialogue: false
      new_event: false
      cinematography_overreach: false
facial_expression_anchor_evidence:
  - scene_id: ""
    source_anchor: ""
    subject: ""
    trigger: ""
    target_field: "表情特写"
    facial_detail:
      brow: ""
      eyes: ""
      mouth: ""
      jaw_or_throat: ""
    moment_shape: "crack | suppression | held_smile | averted_gaze | blink_change | other"
    risk_check:
      emotion_label_only: false
      no_source_trigger: false
      overused_for_minor_beat: false
      cinematography_overreach: false
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
      embedded_in_fields: []
      risk_check:
        fact_drift: false
        new_dialogue: false
        cinematography_overreach: false
        detail_bloat: false
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
    embedded_in_fields: []
    risk_check:
      fact_drift: false
      new_event: false
      new_dialogue: false
      abstract_aesthetic: false
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
    final_field_projection: []
    risk_check:
      fact_drift: false
      new_dialogue: false
      next_episode_spoiler: false
      new_clue_or_rule: false
      cinematography_overreach: false
```

## Episode File Skeleton

See `templates/episode-script.template.md`.
