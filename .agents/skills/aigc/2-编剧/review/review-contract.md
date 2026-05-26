# Review Contract

## Review Purpose

`2-编剧` 的 review gate 验证逐集编剧稿是否忠实承接 `1-分集`，对白逐字冻结、声画字段纯净、画面具像化可拍、小说表述完成二次画面化，并能被下游导演、摄影、设计与视频链路稳定消费。

## Default Provider

- 默认辅助 provider：`code-reviewer`
- 用途：检查 Skill 2.0 包结构、脚本边界、输出合同和剧本字段门禁。
- review 必须加载 `../references/script-adaptation-contract.md`，检查上游逐集正文、输出路径、frontmatter、slugline 和保真边界。
- review 必须加载 `../references/field-routing-and-audio-visual-contract.md`，检查对白冻结、声画配对、字段纯度、声音本体、环境字段纯化、动作客观性、`表情特写` 字段落点和占位泄露。
- review 必须加载 `../references/novel-to-screen-language-contract.md`，检查小说作者评论、主角视角判断、心理内视、直接情绪感受、比喻象征、抽象概括、往日常态句、背景说明、因果解释和关系结论是否完成二次画面化；同时确认引号内对白仍逐字冻结，小说叙述没有被改成新增对白，没有新增无关人物过往、物品来历或回忆性信息。
- review 必须加载 `../references/information-asymmetry-contract.md`，检查关键场景是否建立观众/角色/隐藏信息状态、揭示与保留点和悬念机制。
- review 必须加载 `../../_shared/audience-psychology-model-contract.md`，检查关键场景是否建立观众知识基线、期待/恐惧/渴望种子和冲突遗产入口，且小说转译没有提前泄露观众应未知信息。
- review 必须加载 `../references/scene-rhythm-contract.md`，检查关键场景是否有时长体感、信息密度、beat 数量和转出方式。
- review 必须加载 `../references/dialogue-subtext-contract.md`，检查关键对白是否有戏剧动作和潜台词行为，而不只是语气状态。
- 若上层策略阻断顾问与复核流程 或 provider 调度，允许使用本地 review checklist，并使用本地 review checklist。

## Stage-End Review-Repair Rule

- 除 `review_only` 外，review gate 是写回前的阻断门，不是交付后的附带报告。
- `needs_rework` 必须回到 `steps/directing-workflow.md` 的 `N6R-SCRIPT-REPAIR`，由 `2-编剧` 本阶段直接做最小修复并复审；复审未通过不得写入 canonical `2-编剧/第N集.md`。
- 允许直接修复的范围：字段投影、声画配对、slugline 去重、画面具像化、主角内心独白回收、动作客观可拍化、直接情绪转译、声音本体、环境字段纯化、环境氛围承托、frontmatter/report 证据和格式。
- 禁止直接修复的范围：新增或删减剧情事实、改写对白、改变事件顺序、替上游 `1-分集` 修剧情。遇到这类问题必须输出 source owner 和不可用说明。
- `pass_with_followups` 只允许非阻断质量建议；任何保真、对白、声画、slugline、字段纯度、小说表述二次画面化、LLM-first 问题不得降级为 followup。

## Blocking Gates

| gate_id | check | fail_code |
| --- | --- | --- |
| `GATE-SCRIPT-01` | 输出路径为 `projects/aigc/<项目名>/2-编剧/第N集.md` | `FAIL-PATH` |
| `GATE-SCRIPT-02` | frontmatter 含 `source_episode_path` 且可回指上游 | `FAIL-SOURCE` |
| `GATE-SCRIPT-03` | 上游事实信息量与顺序完整承接 | `FAIL-FAITHFULNESS` |
| `GATE-SCRIPT-04` | 对白逐字保真，字段标题为 `对白（角色名，语态/状态短语）`，中文双引号，引号内无动作；第二项自然展示说话状态，不强制一词或"地"字尾；不得把 `原文角色`、`角色名`、`某人` 等占位词当角色名 | `FAIL-DIALOGUE` |
| `GATE-SCRIPT-05` | 声音字段就近配对对应 `*画面` 字段 | `FAIL-PAIRING` |
| `GATE-SCRIPT-06` | 每个场景至少一条正式画面字段 | `FAIL-SCENE-VISUAL` |
| `GATE-SCRIPT-07` | 场景标题是阿拉伯编号 + slugline，同 slugline 不重复开场 | `FAIL-SLUGLINE` |
| `GATE-SCRIPT-08` | `角色动作` / `动作画面` 只写镜头可实拍的客观动作、神态、语气、生理反应和空间运动；不含心理解释、抽象判断、小说章节名或"试图、想要、打算、意图"等主观预判/心理意图词 | `FAIL-ACTION-PURITY` |
| `GATE-SCRIPT-09` | 脚本没有替代 LLM 生成核心创作正文 | `FAIL-LLM-FIRST` |
| `GATE-SCRIPT-10` | 所有 `*画面`、`环境描写`、`道具特写`、`心理反应`、`表情特写`、`表演提示` 均具像化、画面化、可感知化、反抽象、反概念、反比喻；不含无法实拍的抽象概括、往日常态总结或直接主观情绪感受 | `FAIL-CONCRETE-VISUAL` |
| `GATE-SCRIPT-11` | `音效` 字段只写声音本体，不写时间说明、事件概括或描述性句子 | `FAIL-SOUND-LITERAL` |
| `GATE-SCRIPT-12` | 终稿字段正文没有内部任务说明、模板占位句或规则复述，例如"本场按上游原文顺序承接...""说话者的视线...""不新增事件结果""引号内不加入动作" | `FAIL-PLACEHOLDER-LEAK` |
| `GATE-SCRIPT-13` | `环境描写` 只写场景本身的写景画面，不承载人物动作、对白引出、剧情结果、背景概要、心理解释或关系结论；同一 slugline 内允许在开篇之外因室内外边界、角落、门廊、窗边、船舷、背景层次、光线、空气或材质焦点变化再次出现环境描写 | `FAIL-ENVIRONMENT-PURITY` |
| `GATE-SCRIPT-14` | 关键场景的 `环境描写` 有自然景物氛围承托，且承托不新增事件、线索或因果 | `FAIL-ATMOSPHERIC-ENVIRONMENT` |
| `GATE-SCRIPT-15` | 小说原文中的作者评论、主角视角判断、心理内视、直接情绪感受、比喻象征、抽象概括、往日常态句、背景说明、因果解释或关系结论已完成二次画面化；终稿没有把小说句式、抽象解释、作者判断原样塞入画面字段，也没有把小说叙述改成新增对白；没有新增与当前主线无关的人物过往、物品来历或回忆性信息 | `FAIL-NOVEL-TO-SCREEN-LANGUAGE` |
| `GATE-SCRIPT-16` | 主角视角下对他人行为的判断已进入 `内心独白（主角）` 或主角可感知反应，而非客观第三方概括；`内心独白（主角）` 引号内主角自指已从小说第三人称转成第一人称 | `FAIL-PROTAGONIST-INNER-VOICE` |
| `GATE-SCRIPT-17` | 执行报告包含 `novel_expression_transform_evidence`、`protagonist_inner_voice_evidence` 和 `objective_action_purity_evidence`，能够证明小说表述转译、主角内心独白保留和动作客观化已经发生；非机械特例必须说明处理依据 | `FAIL-CREATIVE-EVIDENCE` |
| `GATE-SCRIPT-18` | `表情特写` 为正式可选字段：若使用，必须只写眉、眼、眼睑、眨眼频率、鼻翼、嘴角、唇线、咬肌、下颌、喉头或皮肤状态等具体面部变化，并能回指上游触发或当前声画压力；不得只写情绪标签、心理解释、摄影机位、景别或镜头运动。若上游关键情绪明显集中在面部变化，不能只散落为无字段的泛化表情词 | `FAIL-FACIAL-EXPRESSION-FIELD` |
| `GATE-SCRIPT-19` | 关键场景完成 `information_asymmetry_map`：观众、角色、隐藏信息、揭示点、保留点和悬念机制明确；没有把信息释放策略全部留给下游导演 | `FAIL-INFORMATION-ASYMMETRY` |
| `GATE-SCRIPT-20` | 关键场景完成 `scene_rhythm_profile`：时长体感、信息密度、beat 数量、节奏类型、留白和转出方式明确；没有全稿同密度平铺 | `FAIL-SCENE-RHYTHM` |
| `GATE-SCRIPT-21` | 关键对白完成 `dialogue_subtext_map`：对白标题状态之外有戏剧动作；内心独白、旁白或解释性心理文字没有超过影视呈现预算 | `FAIL-DIALOGUE-SUBTEXT` |
| `GATE-SCRIPT-22` | 关键场景完成 `audience_knowledge_state`、`audience_psychology_seed` 与 `conflict_legacy_seed`：观众已知/未知、期待/恐惧/渴望种子和冲突继承状态明确；小说转译没有提前泄露观众应未知信息 | `FAIL-AUDIENCE-PSYCHOLOGY` |

## Recommended Mechanical Check

```bash
python3 .agents/skills/aigc/2-编剧/scripts/validate_script_projection.py projects/aigc/<项目名>/2-编剧/第N集.md
```

该脚本只检查结构、字段和基础配对，不能证明剧情事实完整承接；事实完整性和对白逐字保真仍需 LLM/人工对读上游。

## Verdict Model

| verdict | meaning |
| --- | --- |
| `pass` | 可交付给下游阶段 |
| `pass_with_followups` | 可交付，但存在非阻断质量优化 |
| `needs_rework` | 存在保真、对白、声画、场景标题、创作证据或其他 review gate 阻断项 |
| `blocked` | 上游缺失、路径不可读、权限或策略阻断 |

## Report Shape

```yaml
review:
  verdict: pass | pass_with_followups | needs_rework | blocked
  source_episode_path: projects/aigc/<项目名>/1-分集/第N集.md
  output_path: projects/aigc/<项目名>/2-编剧/第N集.md
  checks:
    faithfulness: pass
    dialogue_lock: pass
    audio_visual_pairing: pass
    slugline_stability: pass
    field_purity: pass
    facial_expression_closeup: pass
    concrete_visuals: pass
    sound_literal: pass
    placeholder_leak: pass
    environment_purity: pass
    atmospheric_environment: pass
    novel_to_screen_language: pass
    protagonist_inner_voice: pass
    creative_evidence: pass
    information_asymmetry: pass
    audience_psychology_baseline: pass
    scene_rhythm: pass
    dialogue_subtext: pass
    repair_loop: pass
  repair_actions: []
  re_review_verdict: pass
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
        subjective_intent_in_action: false
        unrelated_backstory: false
        third_person_pov_judgment: false
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
  findings: []
```
