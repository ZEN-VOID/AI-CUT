# Review Contract

## Review Purpose

`2-编导` 的 review gate 验证逐集编导稿是否忠实承接 `1-分集`，并能被下游分组、摄影、设计与视频链路稳定消费。

## Default Provider

- 默认辅助 provider：`code-reviewer`
- 用途：检查 Skill 2.0 包结构、脚本边界、输出合同和剧本字段门禁。
- 若本轮启动 subagents 模式，review 还必须检查 `../../_shared/team-advisor-consultation-contract.md` 与 `../SKILL.md#Subagents Execution Mechanism`：是否从项目 `team.yaml` 解析监制组相关智能顾问团、是否把顾问任务同步到当前 `steps/directing-workflow.md` 节点、`Thought Pass Map` 与相关 review gate、是否要求顾问代入角色意识/创作风格/专业水准参与节点判断和执行取舍、是否形成带 `node_ref/pass_ref/gate_ref/role_lens` 的 `advisor_consultation_packet`，以及顾问指导是否沉淀为后续任务上下文而未改写上游真源。
- review 必须加载 `../references/performance-and-scene-craft-contract.md`，检查场景状态差、潜台词行为、演员任务、场面调度内嵌、沉默反应和摄影越权风险。
- review 必须加载 `../references/psychological-reaction-contract.md`，检查 `心理反应` 是否有主体、有上游触发点、有可见/可听/可演通道，主角内心想法和主角视角判断是否保留为 `独白/内心独白` 或可感知反应，且没有抽象想象、内心解释、因果论文、未授权新对白、无关回忆或场景末尾总结块。
- review 必须加载 `../references/actor-performance-control-contract.md`，检查关键情绪 beat 是否避免情绪标签和模板化表情，是否具备上游触发点、情绪动机、微表情、非面部生理联动、环境声音或沉默余波、微动态限制，并已内嵌到既有字段而未新增剧情、对白或摄影方案。
- review 必须加载 `../references/novel-to-screen-language-contract.md`，检查小说作者评论、主角视角判断、心理内视、直接情绪感受、比喻象征、抽象概括、往日常态句、背景说明、因果解释和关系结论是否完成二次画面化；同时确认引号内对白仍逐字冻结，小说叙述没有被改成新增对白，没有新增无关人物过往、物品来历或回忆性信息。
- review 必须加载 `../references/directorial-authorship-contract.md`，检查关键场景是否有真正编导创作干货：戏剧问题、人物压力、观众位置、信息释放、表演/空间/道具/声音发动机和可拍执行策略，而不是只做结构规整或漂亮改写。
- review 必须加载 `../references/episode-visual-spine-contract.md`，检查整集是否有 `episode_visual_spine`，并确认视觉问题、母题链、材质/色彩弧、节奏曲线、呼应目标和克制规则没有越过上游保真。
- review 必须加载 `../references/visual-aesthetic-contract.md`，检查关键场景是否有核心画面、视觉气质、画面层级、母题变化、对比轴、景境氛围、节奏和留白取舍，并确认这些内容内嵌到既有字段而未新增剧情事实或摄影方案。
- review 必须加载 `../references/episode-final-image-contract.md` 与 `../types/episode-final-image-type-map.md`，检查每集终结画面是否形成迷你彩蛋尾钩：与下一集真实关联但不剧透，并从本集内容丝滑顺延，且已完成环境描写式、道具特写式、情绪酝酿式或高潮结尾式的类型化匹配。
- review 必须加载 `../steps/directing-workflow.md#Thinking-Action Node Contract`，检查本轮经过的关键节点是否形成 `thinking_action_node_ledger`；每条节点记录必须同时包含判断问题、执行动作、证据字段、出口路由、gate 状态和 source owner。节点只写 checklist、只写“已优化”结论或没有失败回路时，必须判为 `needs_rework`。
- 若本轮新增或显著修改学习型合同，review 必须检查 `learning_integration_review_evidence`：静态接入点、真实样例或等价 smoke 状态、未覆盖风险和后续生产观察点必须写清；没有真实项目样例时只能标注 `static_only`，不得写成 fully verified。
- 若本轮启用 `controlled_enrichment`，review 必须加载 `../references/controlled-enrichment-contract.md`，检查新增承托细节是否有上游锚点、是否只属于表现层、是否记录 `controlled_enrichment_ledger`。
- 若上层策略阻断真实 subagent 或 provider 调度，允许降级为本地 review checklist，并在报告中说明阻断来源、原计划 provider、实际路径和未启动 reviewer。

## Stage-End Review-Repair Rule

- 除 `review_only` 外，review gate 是写回前的阻断门，不是交付后的附带报告。
- `needs_rework` 必须回到 `steps/directing-workflow.md` 的 `N6R-DIRECT-REPAIR`，由 `2-编导` 本阶段直接做最小修复并复审；复审未通过不得写入 canonical `2-编导/第N集.md`。
- 允许直接修复的范围：字段投影、声画配对、slugline 去重、画面具像化、主角内心独白回收、动作客观可拍化、心理反应可感知化、直接情绪转译、声音本体、高潮承托、表演提示内嵌、场面调度内嵌、沉默反应、画面美学组织、终结画面尾钩内嵌、controlled enrichment 留证、frontmatter/report 证据和格式。
- 禁止直接修复的范围：新增或删减剧情事实、改写对白、改变事件顺序、替上游 `1-分集` 修剧情、把 B 路线扩展为新增对白/桥段/因果。遇到这类问题必须输出 source owner 和阻断报告。
- `pass_with_followups` 只允许非阻断质量建议；任何保真、对白、声画、slugline、字段纯度、高潮承托、表演任务、场面调度、画面美学、终结画面尾钩、controlled enrichment 或 LLM-first 问题不得降级为 followup。

## Blocking Gates

| gate_id | check | fail_code |
| --- | --- | --- |
| `GATE-DIRECT-01` | 输出路径为 `projects/aigc/<项目名>/2-编导/第N集.md` | `FAIL-PATH` |
| `GATE-DIRECT-02` | frontmatter 含 `source_episode_path` 且可回指上游 | `FAIL-SOURCE` |
| `GATE-DIRECT-03` | 上游事实信息量与顺序完整承接 | `FAIL-FAITHFULNESS` |
| `GATE-DIRECT-04` | 对白逐字保真，字段标题为 `对白（角色名，语态/状态短语）`，中文双引号，引号内无动作；第二项自然展示说话状态，不强制一词或“地”字尾；不得把 `原文角色`、`角色名`、`某人` 等占位词当角色名 | `FAIL-DIALOGUE` |
| `GATE-DIRECT-05` | 声音字段就近配对对应 `*画面` 字段 | `FAIL-PAIRING` |
| `GATE-DIRECT-06` | 每个场景至少一条正式画面字段 | `FAIL-SCENE-VISUAL` |
| `GATE-DIRECT-07` | 场景标题是阿拉伯编号 + slugline，同 slugline 不重复开场 | `FAIL-SLUGLINE` |
| `GATE-DIRECT-08` | `角色动作` / `动作画面` 只写镜头可实拍的客观动作、神态、语气、生理反应和空间运动；不含心理解释、抽象判断、小说章节名或“试图、想要、打算、意图”等主观预判/心理意图词 | `FAIL-ACTION-PURITY` |
| `GATE-DIRECT-09` | 脚本没有替代 LLM 生成核心创作正文 | `FAIL-LLM-FIRST` |
| `GATE-DIRECT-10` | 所有 `*画面`、`环境描写`、`道具特写`、`心理反应`、`表演提示` 均具像化、画面化、可感知化、反抽象、反概念、反比喻；不含无法实拍的抽象概括、往日常态总结或直接主观情绪感受 | `FAIL-CONCRETE-VISUAL` |
| `GATE-DIRECT-11` | `音效` 字段只写声音本体，不写时间说明、事件概括或描述性句子 | `FAIL-SOUND-LITERAL` |
| `GATE-DIRECT-12` | 上游存在高潮/爽点/高光成分时，输出完成 `peak_visual_pass`，高点有可回指证据、可拍承托、状态差或余波，且没有新增事实、对白或因果 | `FAIL-PEAK-VISUAL` |
| `GATE-DIRECT-13` | 启动 subagents 模式时，已完成同步于当前思维·执行节点的 `team.yaml` 监制顾问请教，并沉淀为带节点锚点的后续上下文，或记录上层阻断降级 | `FAIL-ADVISOR-CONSULT` |
| `GATE-DIRECT-14` | 关键场景完成 `director_substance_pass`：有上游锚点、戏剧问题、人物选择压力、观众位置、信息释放和可拍执行策略，并已内嵌进剧本句段 | `FAIL-DIRECTOR-SUBSTANCE` |
| `GATE-DIRECT-15` | 关键场景有可回指上游的进入状态、压力源、转折点和退出状态，或报告说明其过渡功能 | `FAIL-SCENE-TURN` |
| `GATE-DIRECT-16` | 心理、潜台词、信任变化、权力关系和沉默反应被转成主角内心独白、可执行行为、表演任务、场面调度、可感知 `心理反应` 或反应余波，并内嵌到对应剧本句段；关键情绪 beat 已按 `actor-performance-control-contract.md` 避免情绪标签空转和模板化表情，至少能看到上游触发点、情绪动机、微表情、非面部身体联动或环境声音承托；主角视角下对他人行为的主观判断不得写成客观第三方概括；`内心独白（主角）` 引号内指代主角自身时必须使用第一人称心声，第三人称只可指向其他角色、引用文本或有留证的自我疏离；`心理反应` 必须符合 `psychological-reaction-contract.md` 的主体、触发点和 GETability 要求，不得写抽象想象、内心解释或离开文字无法感知的主角心理 | `FAIL-PERFORMANCE-TASK` |
| `GATE-DIRECT-17` | `场面调度` 不写机位、景别、镜头运动、分镜编号或 `分镜明细预设` | `FAIL-CINEMATOGRAPHY-OVERREACH` |
| `GATE-DIRECT-18` | 启用 `controlled_enrichment` 时，每个新增承托细节都有上游锚点、目标字段、用途和风险检查，且没有新增对白/事件/因果/规则 | `FAIL-CONTROLLED-ENRICHMENT` |
| `GATE-DIRECT-19` | 终稿没有在场景末尾或分镜组末尾总结式列出 `表演提示` / `场面调度`；规划结果已拆入对应画面、动作、对白画面、道具、群像、声音或反应字段 | `FAIL-PERFORMANCE-SUMMARY-BLOCK` |
| `GATE-DIRECT-20` | 终稿字段正文没有内部任务说明、模板占位句或规则复述，例如“本场按上游原文顺序承接...”“说话者的视线...”“不新增事件结果”“引号内不加入动作” | `FAIL-PLACEHOLDER-LEAK` |
| `GATE-DIRECT-21` | `环境描写` 只写场景本身的写景画面，不承载人物动作、对白引出、剧情结果、背景概要、心理解释或关系结论；同一 slugline 内允许在开篇之外因室内外边界、角落、门廊、窗边、船舷、背景层次、光线、空气或材质焦点变化再次出现环境描写 | `FAIL-ENVIRONMENT-PURITY` |
| `GATE-DIRECT-22` | 关键情绪场、压迫场、离别场或类型氛围场的 `环境描写` 不应只是地点点缀；若新增自然景物或氛围细节，必须符合情境且不新增事件、线索、阻碍、因果或结果 | `FAIL-ATMOSPHERIC-ENVIRONMENT` |
| `GATE-DIRECT-23` | 已完成 `episode_visual_spine` 和 `visual_aesthetic_pass`：整集有视觉主轴，关键场景、强情绪场、压迫场、离别场、高潮场或类型氛围场有核心画面、视觉气质、画面层级、母题变化、对比轴、景境氛围、节奏和留白取舍；没有抽象审美词空转、细节堆砌、摄影越权或剧情新增 | `FAIL-VISUAL-AESTHETIC` |
| `GATE-DIRECT-24` | 执行报告包含 `thinking_action_node_ledger`、`novel_expression_transform_evidence`、`psychological_reaction_evidence`、`actor_performance_control_evidence`、`protagonist_inner_voice_evidence`、`objective_action_purity_evidence`、`director_substance_evidence`、`episode_visual_spine`、`visual_aesthetic_evidence` 和 `episode_final_image_evidence`，能够证明思维·执行节点、小说表述转译、主角内心独白保留、心理反应可感知化、角色演技控制、动作客观化、关键编导判断、整集视觉主轴、单场美学和终结画面尾钩已经发生；非机械特例必须说明降级原因 | `FAIL-CREATIVE-EVIDENCE` |
| `GATE-DIRECT-25` | 小说原文中的作者评论、主角视角判断、心理内视、直接情绪感受、比喻象征、抽象概括、往日常态句、背景说明、因果解释或关系结论已完成二次画面化；终稿没有把小说句式、抽象解释、作者判断原样塞入画面字段，也没有把小说叙述改成新增对白；没有新增与当前主线无关的人物过往、物品来历或回忆性信息 | `FAIL-NOVEL-TO-SCREEN-LANGUAGE` |
| `GATE-DIRECT-26` | 每集已完成 `episode_final_image_pass`：终结画面作为迷你彩蛋尾钩，与下一集真实关联或明确为本集局部推断，不剧透下一集具体事件/结果/台词/新信息；已按类型化匹配选择环境描写式、道具特写式、情绪酝酿式或高潮结尾式，并从本集内容丝滑顺延到最后既有字段 | `FAIL-EPISODE-FINAL-IMAGE` |
| `GATE-DIRECT-27` | 思维·执行节点没有退化为普通 checklist：`thinking_action_node_ledger` 覆盖本轮经过的关键节点，且每条记录包含 `judgment_question / decision / actions_taken / evidence_keys / route_out / gate_status / source_owner`；学习型新合同或大幅升级的合同有 `learning_integration_review_evidence`，能区分真实样例通过、等价 smoke、`static_only` 与残余风险 | `FAIL-THINKING-ACTION-NODE` |

## Recommended Mechanical Check

```bash
python3 .agents/skills/aigc/2-编导/scripts/validate_script_projection.py projects/aigc/<项目名>/2-编导/第N集.md
```

该脚本只检查结构、字段和基础配对，不能证明剧情事实完整承接；事实完整性和对白逐字保真仍需 LLM/人工对读上游。

## Verdict Model

| verdict | meaning |
| --- | --- |
| `pass` | 可交付给下游阶段 |
| `pass_with_followups` | 可交付，但存在非阻断质量优化 |
| `needs_rework` | 存在保真、对白、声画、场景标题、创作证据、思维·执行节点、学习集成验证或其他 review gate 阻断项 |
| `blocked` | 上游缺失、路径不可读、权限或策略阻断 |

## Report Shape

```yaml
review:
  verdict: pass | pass_with_followups | needs_rework | blocked
  source_episode_path: projects/aigc/<项目名>/1-分集/第N集.md
  output_path: projects/aigc/<项目名>/2-编导/第N集.md
  checks:
    faithfulness: pass
    dialogue_lock: pass
    audio_visual_pairing: pass
    slugline_stability: pass
    field_purity: pass
    concrete_visuals: pass
    sound_literal: pass
    peak_visual_treatment: pass
    advisor_consultation: pass
    director_substance: pass
    scene_turn: pass
    psychological_reaction: pass
    actor_performance_control: pass
    performance_task: pass
    blocking_power: pass
    performance_integration: pass
    controlled_enrichment: pass
    placeholder_leak: pass
    environment_purity: pass
    atmospheric_environment: pass
    novel_to_screen_language: pass
    visual_aesthetic: pass
    episode_final_image: pass
    thinking_action_nodes: pass
    learning_integration_review: pass
    creative_evidence: pass
    hollywood_quality: pass
    repair_loop: pass
  repair_actions: []
  re_review_verdict: pass
  controlled_enrichment_ledger:
    mode: none | controlled_supportive
    items: []
  thinking_action_node_ledger:
    - node_id: "N4.7-CRAFT"
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
  novel_expression_transform_evidence:
    - source_anchor: ""
      expression_type: "authorial_commentary | protagonist_pov_judgment | abstract_psychology | subjective_emotion | metaphor_symbol | summary_compression | habitual_summary | backstory_exposition | sensory_prose | causal_explanation | relationship_conclusion | time_compression | wuxia_abstraction | inner_monologue | rule_exposition"
      source_function: ""
      screen_strategy: ""
      target_fields:
        - ""
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
      embedded_in_fields:
        - ""
      risk_check:
        emotion_label_only: false
        template_expression: false
        overacting: false
        new_dialogue: false
        new_event: false
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
      - node_ref: "N3-SCENE | N4-FIELD | N4.2-NOVEL-TRANSFORM | N4.4-DIRECTORIAL | N4.5-PEAK"
        reason: ""
        resolution: "reworked | blocked"
    execution_brief: ""
    downgrade:
      blocked_by: "system | developer | tool | user | none"
      planned_path: ""
      actual_path: ""
      skipped_members: []
  findings: []
```

当 `advisor_consultation_packet.status == completed` 时，`node_anchors` 至少包含一个带 `node_ref/pass_ref/gate_ref/role_lens` 的采纳摘要；若顾问指出前置节点问题，`routeback_targets` 必须记录回修节点、原因和处理结果。若真实 subagent dispatch 被阻断，`downgrade` 必须完整记录阻断层级、原计划路径、实际路径和未启动成员。

`director_substance_evidence` 必须证明关键场景的编导判断来自上游原文，并已经进入正文具体字段；只写“戏剧张力更强”“电影感更好”“节奏更紧”但缺少动作、声音、空间、道具、表演或观众位置证据时，verdict 必须为 `needs_rework`。
