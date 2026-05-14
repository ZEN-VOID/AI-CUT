# Review Contract

## Review Purpose

`2-编剧` 的 review gate 验证逐集编导稿是否忠实承接 `1-分集`，对白逐字冻结、声画字段纯净、画面具像化可拍、小说表述完成二次画面化，并能被下游导演、摄影、设计与视频链路稳定消费。

## Default Provider

- 默认辅助 provider：`code-reviewer`
- 用途：检查 Skill 2.0 包结构、脚本边界、输出合同和剧本字段门禁。
- review 必须加载 `../references/performance-and-scene-craft-contract.md`，检查场景状态差、潜台词行为、演员任务、场面调度内嵌、沉默反应和摄影越权风险。
- review 必须加载 `../references/psychological-reaction-contract.md`，检查 `心理反应` 是否有主体、有上游触发点、有可见/可听/可演通道，主角内心想法和主角视角判断是否保留为 `独白/内心独白` 或可感知反应，且没有抽象想象、内心解释、因果论文、未授权新对白、无关回忆或场景末尾总结块。
- review 必须加载 `../references/actor-performance-control-contract.md`，检查关键情绪 beat 是否避免情绪标签和模板化表情，是否具备上游触发点、情绪动机、微表情、非面部生理联动、环境声音或沉默余波、微动态限制，并已内嵌到既有字段而未新增剧情、对白或摄影方案。
- review 必须加载 `../references/novel-to-screen-language-contract.md`，检查小说作者评论、主角视角判断、心理内视、直接情绪感受、比喻象征、抽象概括、往日常态句、背景说明、因果解释和关系结论是否完成二次画面化；同时确认引号内对白仍逐字冻结，小说叙述没有被改成新增对白，没有新增无关人物过往、物品来历或回忆性信息。
- 若上层策略阻断真实 subagent 或 provider 调度，允许降级为本地 review checklist，并在报告中说明阻断来源、原计划 provider、实际路径和未启动 reviewer。

## Stage-End Review-Repair Rule

- 除 `review_only` 外，review gate 是写回前的阻断门，不是交付后的附带报告。
- `needs_rework` 必须回到 `steps/screenwriting-workflow.md` 的 `N6R-SCRIPT-REPAIR`，由 `2-编剧` 本阶段直接做最小修复并复审；复审未通过不得写入 canonical `2-编剧/第N集.md`。
- 允许直接修复的范围：字段投影、声画配对、slugline 去重、画面具像化、主角内心独白回收、动作客观可拍化、心理反应可感知化、直接情绪转译、声音本体、表演提示内嵌、场面调度内嵌、沉默反应、frontmatter/report 证据和格式。
- 禁止直接修复的范围：新增或删减剧情事实、改写对白、改变事件顺序、替上游 `1-分集` 修剧情。遇到这类问题必须输出 source owner 和阻断报告。
- `pass_with_followups` 只允许非阻断质量建议；任何保真、对白、声画、slugline、字段纯度、表演任务、场面调度、LLM-first 问题不得降级为 followup。

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
| `GATE-SCRIPT-10` | 所有 `*画面`、`环境描写`、`道具特写`、`心理反应`、`表演提示` 均具像化、画面化、可感知化、反抽象、反概念、反比喻；不含无法实拍的抽象概括、往日常态总结或直接主观情绪感受 | `FAIL-CONCRETE-VISUAL` |
| `GATE-SCRIPT-11` | `音效` 字段只写声音本体，不写时间说明、事件概括或描述性句子 | `FAIL-SOUND-LITERAL` |
| `GATE-SCRIPT-12` | 终稿没有在场景末尾或分镜组末尾总结式列出 `表演提示` / `场面调度`；规划结果已拆入对应画面、动作、对白画面、道具、群像、声音或反应字段 | `FAIL-PERFORMANCE-SUMMARY-BLOCK` |
| `GATE-SCRIPT-13` | 终稿字段正文没有内部任务说明、模板占位句或规则复述，例如"本场按上游原文顺序承接...""说话者的视线...""不新增事件结果""引号内不加入动作" | `FAIL-PLACEHOLDER-LEAK` |
| `GATE-SCRIPT-14` | `环境描写` 只写场景本身的写景画面，不承载人物动作、对白引出、剧情结果、背景概要、心理解释或关系结论；同一 slugline 内允许在开篇之外因室内外边界、角落、门廊、窗边、船舷、背景层次、光线、空气或材质焦点变化再次出现环境描写 | `FAIL-ENVIRONMENT-PURITY` |
| `GATE-SCRIPT-15` | 心理、潜台词、信任变化、权力关系和沉默反应被转成主角内心独白、可执行行为、表演任务、场面调度、可感知 `心理反应` 或反应余波，并内嵌到对应剧本句段；关键情绪 beat 已按 `actor-performance-control-contract.md` 避免情绪标签空转和模板化表情，至少能看到上游触发点、情绪动机、微表情、非面部身体联动或环境声音承托；主角视角下对他人行为的主观判断不得写成客观第三方概括；`内心独白（主角）` 引号内指代主角自身时必须使用第一人称心声，第三人称只可指向其他角色、引用文本或有留证的自我疏离；`心理反应` 必须符合 `psychological-reaction-contract.md` 的主体、触发点和 GETability 要求，不得写抽象想象、内心解释或离开文字无法感知的主角心理 | `FAIL-PERFORMANCE-TASK` |
| `GATE-SCRIPT-16` | 小说原文中的作者评论、主角视角判断、心理内视、直接情绪感受、比喻象征、抽象概括、往日常态句、背景说明、因果解释或关系结论已完成二次画面化；终稿没有把小说句式、抽象解释、作者判断原样塞入画面字段，也没有把小说叙述改成新增对白；没有新增与当前主线无关的人物过往、物品来历或回忆性信息 | `FAIL-NOVEL-TO-SCREEN-LANGUAGE` |
| `GATE-SCRIPT-17` | 执行报告包含 `novel_expression_transform_evidence`、`protagonist_inner_voice_evidence` 和 `objective_action_purity_evidence`，能够证明小说表述转译、主角内心独白保留和动作客观化已经发生；非机械特例必须说明降级原因 | `FAIL-CREATIVE-EVIDENCE` |

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
    concrete_visuals: pass
    sound_literal: pass
    performance_task: pass
    performance_integration: pass
    placeholder_leak: pass
    environment_purity: pass
    novel_to_screen_language: pass
    creative_evidence: pass
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
  findings: []
```
