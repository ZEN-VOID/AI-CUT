# Narration To Voice Adaptation Contract

## Purpose

本细则为 `2-编剧` script layer 增加一类受控能力：当小说来源中的客观视角叙事描写直接画面化会变成解释、死旁白或无戏的说明句时，可以把其改编为有上游锚点的对白、独白或内心独白，使信息更利于影视化表现。

该能力只处理**非引号内的客观叙事**，不授权改写上游已有对白。它是 `script-adaptation-contract.md` 的专项分支，也是 `script-adaptation-contract.md` 对“新增对白”禁区的唯一受控例外：允许的是 `source-grounded derived speech`，不是自由新增台词。

## Ownership

- 本文件拥有客观叙事转对白/独白的触发、说话者资格、字段选择、写法限制、证据结构和 review gate。
- `script-adaptation-contract.md` 继续拥有保真、对白冻结、字段标题和声音字段纯度；上游已有对白仍逐字冻结。
- `script-adaptation-contract.md` 负责先识别小说式表述类型，再按本文件判断是否进入语音化分支。
- `.agents/skills/aigc/5-表演/references/dialogue-subtext-contract.md` 可为派生对白补充戏剧动作，但不得借潜台词再改写派生行的信息。
- `review/review-contract.md` 负责把本文件的阻断项映射到阶段末 review。

## Terms

| term | definition |
| --- | --- |
| `source_dialogue` | 上游原文中已经存在的引号内对白，必须逐字冻结。 |
| `objective_narration` | 非引号内、由叙述者交代的客观事实、场景状态、公共信息、动作结果、关系压力、重复常态、剧情衔接或氛围判断。 |
| `derived_voice_line` | 从 `objective_narration` 提炼出的新对白、独白或内心独白；必须回指原文锚点，不得承担原文没有的信息。 |
| `voice_owner` | 合法说出或想到该行的角色、系统、群体或旁白主体。 |

## Trigger Gate

只有同时满足以下条件，才允许把客观叙事改编为对白或独白：

| trigger | must be true | fail if |
| --- | --- | --- |
| `source_is_non_dialogue` | 来源不是上游引号内对白，也不是已冻结对白的改写版本。 | 原文已有对白可直接使用，或派生行替换了原对白。 |
| `payload_is_source_grounded` | 派生行只承载原文已有事实、状态、规则、关系压力、情绪方向、剧情衔接或氛围功能。 | 行内出现新事实、新动机、新承诺、新威胁、新线索、新规则或新因果。 |
| `screen_need_exists` | 直接画面化会导致笨重解释、死旁白、信息不可感知，或当前场景缺少可演的语音节拍。 | 只是为了“更酷”“更有梗”“更像金句”。 |
| `voice_owner_is_eligible` | 说话者在场、可被当前叙事合理拥有该信息，并有当下说出/想到的压力或动机。 | 角色不知道这件事、没有说出口的空间，或说出后会改变信息差。 |
| `audience_disclosure_safe` | 派生行不提前泄露观众或角色此时不该知道的信息。 | 破坏悬念、提前解释谜底、让角色过早自白。 |
| `field_pairing_ready` | 派生行有就近 `对白画面`、`独白画面`、`内心独白画面` 或 `旁白画面` 承托。 | 只有一句话孤立输出，没有身体、空间、声音或对手反应。 |

## Continuity Bridge Trigger

当客观叙事段承担“剧情跨度衔接”时，应优先评估派生语音，而不是把整段硬塞进环境描写、角色动作或旁白。这里的跨度衔接指一段叙述同时压缩多个当前场景必须承接的信息簇：

| bridge payload | screen risk if literalized | voice adaptation target |
| --- | --- | --- |
| 上一轮动作结果 | 环境描写变成战报摘要 | 一句对白/独白交代“已经发生什么”，并由现场痕迹承托 |
| 场外行动状态 | 旁白解释路线、撤离、抵达、失败等信息 | 场内角色根据声号、信物、来人或远处声音作出判断 |
| 角色分工变化 | 动作字段解释谁负责什么 | 用命令、回应或确认式对白形成当前行动目标 |
| 外部威胁升级 | 作者说明后续风险 | 用角色可知信息压成判断句，并让声音/空间压力靠近 |
| 下一 beat 触发 | 硬写“紧接着发生” | 用音效、对手反应或门窗/道具变化切入下一拍 |

执行标准：

1. 先把客观叙事拆成 2-4 个 `bridge_payload_unit`，例如 `previous_result / offscreen_status / role_assignment / threat_escalation / next_beat_trigger`。
2. 只选择最影响当前行动的 1-2 个信息簇转成派生语音；其余信息转为现场痕迹、音效、动作或留白。
3. 每句派生语音必须改变当前场内动作的方向，例如“带谁走”“守哪里”“谁已经抵达”“危险从哪里来”。
4. 不允许一口气复述完整背景；若一句话需要逗号连续塞入三件以上事实，必须拆回画面/声音/动作。
5. 跨度信息必须就近显像：声号、尸体、湿衣、门闩、孩子反应、远处破风声、火光、信物、血迹、脚步或空间撤离痕迹至少承托一个。

## Field Choice Matrix

| target field | use when | required support | forbidden |
| --- | --- | --- | --- |
| `对白（角色，语态/状态短语）` | 客观叙事可由场内角色自然说出，且说出口会制造试探、施压、回应、遮掩、转移或揭示当下压力。 | `voice_owner_knowledge_basis`、对手反应、对白画面、`dialogue_subtext_map`。 | 让角色替作者总结主题；让未知情报从角色口中出现。 |
| `独白（角色）` | 角色可听见地自言、自嘲、立誓、压低声吐出判断，或项目风格允许角色外放式独白。 | 独白画面、声线状态、场景压力来源。 | 长篇解释设定；离开当前场景压力的旁观评论。 |
| `内心独白（角色）` | 客观叙事需要贴近焦点角色的判断、警觉、讽刺、恐惧或压住没说出口的信息。 | 第一人称或角色明确自指、内心独白画面、可见反应。 | 全知视角继续讲“他/她如何”；把未知事实写成角色已知结论。 |
| `旁白（主体）` | 信息没有合法角色可拥有，但必须以声音交代，例如系统规则、历史事实、公告或类型化叙述者。 | 旁白画面、信息载体或当下可见后果。 | 让旁白成为默认信息垃圾桶。 |
| `不语音化` | 画面、动作、道具、群像、声音或留白已能更好承托。 | `screen_strategy=visualize/leave_unsaid`。 | 为了热闹强行加话。 |

## Rewrite Rules

1. 先提炼 `objective_fact_payload`：只写原文已经给出的事实、状态、关系压力、剧情衔接或情绪方向。
2. 再选 `voice_owner`：角色必须在场、可知、可说；内心独白只给当前焦点角色或原文明确绑定视角的角色。
3. 派生行必须短：默认一行一意，避免连续解释；同一场景默认不超过 1-2 个 `derived_voice_line`，除非上游本身就是仪式、公告、审讯或独白型场景。
4. 语气要像角色，不像作者：可保留讽刺、冷感、口头禅或时代质感，但不得把作者的主题判断、章节标题或漂亮比喻原样塞进角色口中。
5. “有意思”必须来自冲突、反差、克制、误导、讽刺或人物立场，不来自脱口秀式抖机灵、现代梗或无锚点金句。
6. 派生对白必须能删除后仍不破坏剧情事实；它只改善表达和可演性，不承担新增剧情推进。
7. 派生行旁边必须有身体、停顿、空间、道具、声音或对手反应，证明它是场景行为，不是说明书。
8. 若派生行与上游已有对白表达同一信息，优先使用上游原对白；只允许用画面或表演提示加强，不再另写一句。

## Hard Blocks

出现以下任一情况，必须回到画面化、旁白或留白策略，不能转对白/独白：

- 改写、替换、润色或重排上游已有对白。
- 让角色说出他此时不可能知道的信息。
- 新增承诺、威胁、选择、拒绝、告白、因果、规则、线索、人物动机或关系结果。
- 把客观事实改成角色立场后导致观众误以为事实不可靠，除非原文允许这种主观化。
- 用派生对白解释潜台词、谜底或人物心理，破坏信息差。
- 为了“更有戏”制造上游没有的冲突回合或问答关系。
- 连续使用独白/旁白让成稿像有声小说。

## Evidence Structure

执行报告或节点证据必须保留等价结构：

```yaml
narration_to_voice_adaptation_map:
  - source_anchor: "原文锚点"
    source_text: "客观叙事原句或摘要"
    objective_fact_payload: "派生行允许承载的信息"
    trigger_reason: "为什么直接画面化/旁白不足"
    target_voice_field: "对白 | 独白 | 内心独白 | 旁白 | 不语音化"
    voice_owner: "角色/系统/旁白主体"
    voice_owner_knowledge_basis: "该主体为何知道/能说"
    derived_voice_line: "最终语音行；不语音化时为空"
    paired_visual_or_reaction_field: "对白画面/独白画面/内心独白画面/旁白画面或相邻动作"
    source_function: "信息交代 | 压力外化 | 节奏转折 | 讽刺反差 | 情绪外放 | 规则宣告"
    bridge_payload_units: []  # continuity_bridge 时必填，例如 previous_result/offscreen_status/role_assignment/threat_escalation/next_beat_trigger
    risk_check:
      rewrites_source_dialogue: false
      fact_drift: false
      new_event: false
      new_causality: false
      new_rule_or_clue: false
      new_character_motivation: false
      audience_disclosure_leak: false
      author_voice_leak: false
      over_voice_budget: false
```

## Weak / Strong Examples

| source narration | weak adaptation | strong adaptation |
| --- | --- | --- |
| “院子里的人都知道，少一个名字就意味着少一条命。” | 对白（甲，严肃）：“少一个名字就意味着少一条命。” | 对白（点名人，压低声）：“少了一个。” 对白画面：名册边角被他按住，后排没人接话。 |
| “她早就习惯被这样审视。” | 内心独白（她）：“我早就习惯被这样审视。” | 不语音化：表情特写写眼睑不动、手指把袖口抚平；如必须贴近主观，可写内心独白（她）：“又来了。” |
| “这条规矩从来没有例外。” | 独白（主角）：“这条规矩从来没有例外。” | 旁白（系统提示）：“违规者，无例外。” 旁白画面：规则文字在屏幕底部停住，角色的呼吸声压低。 |
| “任盈盈护送老人孩子从村西后路往石井村暂避；令狐冲留在织坊，把黑蓑伏刃流火力引在自己身上；远处三短一长箫声后，石井村方向传来鞭梢破风。” | 旁白：任盈盈已经护送老人孩子去石井村，令狐冲留在织坊，敌人又追来了。 | 对白（陈阿叔，抱紧孩子压低声）：“三短一长，是任姑娘的号。西路那批人到石井了。” 对白画面：他摸到后门门闩，却没有立刻拉开。对白（令狐冲，盯着门外海雾）：“带阿真走。九鬼组下一刀，不会只落在织坊。” 对白画面：剑尖黑蓑断絮滴水，远处鞭梢破风声逼近。 |

## Review Gate Mapping

| Review Question | Review Gate | Fail Code | Rework Target | Report Evidence |
| --- | --- | --- | --- | --- |
| 客观叙事转对白/独白是否只来自非引号内叙事，没有改写或替换上游已有对白？ | `GATE-BD-04` / `GATE-BD-19` | `FAIL-BD-DIALOGUE` / `FAIL-BD-NARRATION-VOICE` | `steps/script-layer-workflow.md#N4.2-NOVEL-TRANSFORM` | `dialogue_lock_map` 与 `narration_to_voice_adaptation_map.risk_check.rewrites_source_dialogue=false` |
| 每条派生语音是否有 `source_anchor`、`objective_fact_payload`、合法 `voice_owner`、知识依据和触发理由？ | `GATE-BD-19` | `FAIL-BD-NARRATION-VOICE` | `steps/script-layer-workflow.md#N4.2-NOVEL-TRANSFORM` | `narration_to_voice_adaptation_map` 记录 source、payload、trigger、owner 和 knowledge_basis |
| 派生行是否没有新增事实、事件、因果、规则、线索、人物动机、关系结果或提前泄露信息差？ | `GATE-BD-03` / `GATE-BD-19` | `FAIL-BD-FAITHFULNESS` / `FAIL-BD-NARRATION-VOICE` | `steps/script-layer-workflow.md#N4.2-NOVEL-TRANSFORM` / `N6R-BD-REPAIR` | `risk_check.fact_drift/new_event/new_causality/new_rule_or_clue/new_character_motivation/audience_disclosure_leak=false` |
| 派生对白或独白是否有就近画面/动作/反应承托，并且没有变成作者口吻、金句堆砌或有声小说式解释？ | `GATE-BD-06` / `GATE-BD-13` / `GATE-BD-19` | `FAIL-BD-NOVEL-TO-SCREEN` / `FAIL-BD-VISUAL-LANGUAGE` / `FAIL-BD-NARRATION-VOICE` | `steps/script-layer-workflow.md#N4.2-NOVEL-TRANSFORM` / `N5-BD-VISUAL-LANGUAGE` | `paired_visual_or_reaction_field`、`author_voice_leak=false`、`over_voice_budget=false` |
| 跨度性剧情衔接叙事是否先拆成 `bridge_payload_units`，只把最影响当前行动的 1-2 个信息簇转成派生语音，其余交给画面、音效、动作或留白？ | `GATE-BD-19` | `FAIL-BD-NARRATION-VOICE` | `steps/script-layer-workflow.md#N4.2-NOVEL-TRANSFORM` | `narration_to_voice_adaptation_map.bridge_payload_units`、`derived_voice_line`、`paired_visual_or_reaction_field` |
