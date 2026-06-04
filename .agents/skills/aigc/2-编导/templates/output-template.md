# 2-编导 Output Template

## Output Contract Alignment

### Required output

- `OUTPUT-BD-EPISODE`: `projects/aigc/<项目名>/2-编导/第N集.md`
- `OUTPUT-BD-REPORT`: `projects/aigc/<项目名>/2-编导/执行报告.md`

### Output format

- 逐集编导稿：Markdown，含 YAML frontmatter、`【剧本正文】`、场景标题和字段化正文；正文同时承载保真剧本、导演判断和表演工艺。
- 执行报告：Markdown，记录输入、目标集、类型画像、review verdict、直接修复项、复审结果、`thinking_action_node_ledger`、`scene_field_evidence_index`、`script_layer_evidence`、`narration_to_voice_adaptation_map`、`director_layer_evidence`、`performance_layer_evidence`、`concrete_visual_language_evidence`、`visual_unit_candidate_map`、初始化团队综合上下文、残余风险和 `motion_enrichment_handoff`。

### Output path

```text
projects/aigc/<项目名>/2-编导/
├── 第1集.md
├── 第2集.md
└── 执行报告.md
```

### Naming convention

- 逐集编导稿：`第N集.md`
- 报告：`执行报告.md`
- 不创建 `2-编剧/`、`3-导演/`、`4-表演/` 的新 canonical 主稿。

### Completion gate

- 上游 `1-分集/第N集.md` 已回指，输出 frontmatter 记录 `source_episode_path`。
- 事实、顺序和上游已有对白保真；对白引号内不混入动作、解释或未锚定新增台词。
- 场景 slugline、字段分流、声画配对、小说表述二次画面化、客观叙事派生语音裁决、信息差、观众心理和节奏画像已完成。
- 导演判断已内嵌为可见、可听、可执行的戏剧问题、人物压力、视觉主轴、高潮/反高潮、氛围声音、尾钩和终结画面。
- 表演工艺已内嵌为心理反应、演员五层控制、台词交付、长对白 delivery、潜台词行为、场面调度、沉默余波、角色弧线和群戏层次。
- 全稿最终语言可被摄影机处理：离开“高级感、电影感、压迫感、情绪复杂、内心崩塌、演员克制”等概念词，仍能看见人物动作、空间、道具、光线、声音、呼吸、声线、表情和对手反应。
- 终稿不写机位、景别、镜头运动、分镜编号、完整图像 prompt 或视频请求；运动细节交给 `3-运动`，摄影与后续执行交给 `4-摄影` 与后续阶段。
- 若 review 发现阻断项，已在 `2-编导` 阶段内直接最小修复并复审通过。
- 执行报告记录 `scene_field_evidence_index` 和结构化 `motion_enrichment_handoff`，明确是否允许进入 `3-运动`；如保留 `cinematography_handoff`，仅作为后续摄影参考。

## Report Evidence Blocks

执行报告必须包含或等价覆盖：

```yaml
input_lock:
  source_episode_path: projects/aigc/<项目名>/1-分集/第N集.md
  output_path: projects/aigc/<项目名>/2-编导/第N集.md
  type_profile: {}
thinking_action_node_ledger:
  - node_id: ""
    judgment_question: ""
    decision: "pass | needs_rework | blocked | routeback | not_applicable"
    actions_taken: []
    evidence_keys: []
    route_out: ""
    gate_status:
      passed: true
      fail_code: ""
    source_owner: ""
scene_field_evidence_index:
  - source_anchor: ""
    target_field: ""
    layer: "script | director | performance | visual_language"
    embedded_in_text: ""
    evidence_keys: []
    repair_owner: ""
script_layer_evidence:
  faithfulness: ""
  dialogue_lock: ""
  audio_visual_pairing: ""
  novel_expression_transform_evidence: []
  narration_to_voice_adaptation_map: []
  continuity_bridge_evidence:
    bridge_payload_units: []
    voiced_units: []
    visual_or_sound_units: []
    omitted_or_left_unsaid_units: []
  information_asymmetry_map: []
  scene_rhythm_profile: []
director_layer_evidence:
  dramatic_question: ""
  audience_position: ""
  episode_visual_spine: {}
  climax_or_anticlimax_treatment: []
  atmosphere_sound_and_final_image: []
  controlled_enrichment_ledger: []
performance_layer_evidence:
  psychological_reaction_evidence: []
  actor_performance_control_evidence: []
  dialogue_performance_evidence: []
  long_dialogue_delivery_map: []
  subtext_behavior_evidence: []
  blocking_power_map: []
  character_arc_performance_evidence: []
  ensemble_performance_evidence: []
concrete_visual_language_evidence:
  abstract_terms_removed: []
  visualized_replacements: []
  residual_risks: []
visual_unit_candidate_map:
  - source_anchor: ""
    target_field: ""
    visual_unit_text: ""
    why_visual: ""
    performance_or_action_anchor: ""
    non_camera_boundary: "no shot/camera/lens/movement/prompt"
init_team_synthesis_context:
  status: not_applicable | completed | blocked
  synthesis_sources: []
  node_anchors: []
  accepted_constraints: []
  useful_inspirations: []
  risks_to_watch: []
  execution_brief: ""
review:
  verdict: pass | pass_with_followups | needs_rework | blocked
  repair_actions: []
  re_review_verdict: pass
motion_enrichment_handoff:
  next_stage: 3-运动
  after_motion_stage: 4-摄影
  ready: true
  visual_unit_candidate_map_ref: visual_unit_candidate_map
  forbidden_payload: ["shot_number", "camera_angle", "lens", "camera_movement", "image_prompt", "video_prompt"]
  notes: []
```
