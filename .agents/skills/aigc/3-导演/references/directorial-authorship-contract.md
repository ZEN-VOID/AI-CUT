# Directorial Authorship Contract

本合同定义 `2-编导` 的“编导创作干货”。它要求输出不只结构严谨、字段正确或文字漂亮，而是能基于上游小说原文做专业剧本改编判断：抓住戏剧问题、人物选择压力、场景转折、观众体验和可拍执行。

## Core Principle

`2-编导` 的主创责任不是重写剧情，而是把小说原文中已经存在的事件、关系、心理和信息差，转化为导演、演员、声音和下游分组可以执行的戏剧动作。

高质量编导稿必须同时满足：

- 保真：不删减、不压缩、不改写上游事实、顺序和对白。
- 有戏：每场关键场景有明确的戏剧问题、冲突压力、人物主动目标、阻碍和状态变化。
- 可演：人物内心、潜台词和权力关系转成演员可执行的目标、策略、停顿、视线、身体距离、道具动作和反应。
- 可拍：观众能通过画面、声音、动作、空间、道具和沉默余波感知变化，而不是读到解释性结论。
- 有取舍：知道该强化什么、压住什么、延迟什么、让观众先知道还是角色先知道。
- 有回指：每个关键创作判断都能回到上游原文锚点。

## Director Substance Pass

在字段分流后、高潮画面和顾问汇流前，必须执行一次 `director_substance_pass`，形成内部规划证据：

```yaml
director_substance_plan:
  scene_id: ""
  source_anchor: ""
  dramatic_question: ""
  audience_position: "ahead_of_character | aligned_with_character | behind_character"
  character_pressure:
    active_want: ""
    obstacle: ""
    hidden_need_or_fear: ""
    choice_pressure: ""
  scene_turn:
    entry_state: ""
    turning_point: ""
    exit_state: ""
  directorial_strategy:
    reveal_or_withhold: ""
    performance_engine: ""
    spatial_or_prop_engine: ""
    sound_or_silence_engine: ""
    rhythm_choice: ""
  adaptation_payload:
    must_make_visible:
      - ""
    must_make_audible:
      - ""
    must_leave_unsaid:
      - ""
    downstream_hooks:
      - ""
  risk_check:
    fact_drift: false
    new_dialogue: false
    over_explaining: false
    cinematography_overreach: false
```

该计划是 LLM 剧本化投影前的创作判断，不是终稿可直接倾倒的总结块。终稿必须把计划拆进对应的环境、动作、对白画面、道具、群像、声音、停顿和反应字段。

## What Counts As Real Directing Substance

有效编导干货包括：

- 把“角色害怕/心虚/不信任”转成目标、阻碍、试探动作、避视、停顿、手部动作或空间距离。
- 把“气氛紧张”转成声音消失、群体反应迟滞、道具停在半空、座位距离、门口占位或视线压力。
- 把“爽点/高潮”转成兑现前的等待、兑现瞬间的可见动作、声音落点和余波。
- 把“信息差”转成观众位置：观众先知道、角色先知道、或观众与角色同步发现。
- 把“关系变化”转成谁靠近、谁退开、谁拿到道具、谁被迫沉默、谁掌控空间。
- 把“小说解释”转成场上可执行行为，不靠旁白解释人物状态。

无效编导干货包括：

- 只说“增强戏剧张力”“提升电影感”“节奏更紧凑”，但没有动作、声音、空间或表演承托。
- 只把上游原文改成更漂亮的句子。
- 只重排字段、补齐标签、调整 slugline，却没有场景目标、人物压力和状态差。
- 为了显得高级而新增对白、桥段、因果、规则、线索或事件结果。
- 在终稿末尾列“表演提示/场面调度总结”，而不是内嵌到具体剧本句段。

## Integration Rule

`director_substance_plan` 必须进入后续节点：

- `N4.5-PEAK` 使用它判断高点的观众欲望、兑现方式和余波。
- `N4.6-ADVISOR` 使用它向顾问提出节点级创作判断问题。
- `N4.7-CRAFT` 使用它生成 `scene_dramatic_map / performance_task_map / blocking_power_map`。
- `N4.8-ENRICH` 使用它判断哪些表现层承托可以安全新增。
- `N5-DRAFT` 必须把它内嵌进正文，而不是把它作为解释性规划段落输出。

若 `director_substance_plan` 无法回指上游原文，必须删除或降级为非 canonical 候选灵感。
