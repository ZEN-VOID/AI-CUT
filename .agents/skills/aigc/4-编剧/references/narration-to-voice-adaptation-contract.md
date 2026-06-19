# Narration To Voice Adaptation Contract

## Purpose

本细则为 `4-编剧` script layer 增加一类 mode-aware 受控能力：`正剧` 模式下，当小说来源中的客观视角叙事描写直接画面化会变成解释、死旁白或无戏的说明句时，可以把其改编为有上游锚点的对白、独白、内心独白或必要旁白，使信息更利于影视化表现；`解说剧` 模式下，陈述性 source 信息必须完整投影为 `旁白（主体）` + `旁白画面`，不得改写为派生对白、独白或内心独白。

该能力只处理**非引号内的客观叙事**，不授权改写上游已有对白。它是 `script-adaptation-contract.md` 的专项分支，也是 `script-adaptation-contract.md` 对“新增对白”禁区的唯一受控例外：允许的是 `source-grounded derived speech`，不是自由新增台词。`解说剧` 不启用该新增对白例外，只启用 source-grounded narrator projection。

## Ownership

- 本文件拥有客观叙事 mode-aware 语音化的触发、说话者资格、字段选择、写法限制、证据结构和 review gate。
- `script-adaptation-contract.md` 继续拥有保真、对白冻结、字段标题和声音字段纯度；上游已有对白仍逐字冻结。
- `script-adaptation-contract.md` 负责先识别小说式表述类型，再按本文件判断是否进入语音化分支。
- `.agents/skills/aigc/backup/5-表演/references/dialogue-subtext-contract.md` 可为派生对白补充戏剧动作，但不得借潜台词再改写派生行的信息。
- `review/review-contract.md` 负责把本文件的阻断项映射到阶段末 review。

## Terms

| term | definition |
| --- | --- |
| `source_dialogue` | 上游原文中已经存在的引号内对白，必须逐字冻结。 |
| `objective_narration` | 非引号内、由叙述者交代的客观事实、场景状态、公共信息、动作结果、关系压力、重复常态、剧情衔接或氛围判断。 |
| `derived_voice_line` | `正剧` 中从 `objective_narration` 提炼出的新对白、独白、内心独白或必要旁白；`解说剧` 中只能是源文本陈述信息的旁白化表达；必须回指原文锚点，不得承担原文没有的信息。 |
| `voice_owner` | 合法说出或想到该行的角色、系统、群体或旁白主体。 |
| `source_unit` | `解说剧` 中从 source 顺序拆出的最小可审计信息单元，用于判断落点，不是正文标题。 |
| `source_unit_type` | `source_unit` 的类型标签，例如 `source_dialogue`、`visible_action`、`declarative_fact`、`time_bridge`、`mixed_action_declaration`。 |
| `landing_policy` | 该 source 单元进入正式字段的策略，例如 `dialogue_freeze`、`narration_pair`、`visual_field_only`、`system_visual_plus_narration`、`split_visual_and_narration`。 |

## Mode Overlay

| screenplay_mode | policy | allowed_target_fields | hard_blocks |
| --- | --- | --- | --- |
| `zhengju` / `正剧` | 默认策略；只有通过本文件 trigger gate 的非引号客观叙事才可转为派生语音，旁白只在无合法场内角色或系统/公告/历史事实必须声音交代时使用 | `对白`、`独白`、`内心独白`、`旁白`、`不语音化` | 为了更有戏新增事实、替换上游对白、让旁白成为默认信息垃圾桶 |
| `jieshuoju` / `解说剧` | 显式策略；完全按照故事源内容，所有陈述性 source 信息都进入 `旁白（叙述者/指定主体）` + `旁白画面`；上游已有对白仍按对白冻结 | `旁白`、上游已有 `对白`、上游明确存在的独白/内心独白、`不语音化` 仅限非陈述性可见动作/环境 | 把陈述性 source 改写为派生对白/独白/内心独白；漏掉陈述信息；只写概要不做声画配对 |

`解说剧` 执行要求：

1. 先将 source 中的陈述性部分按原文顺序拆成最小可听信息单元。
2. 每个信息单元写为 `旁白（叙述者）` 或用户指定的旁白主体；可做轻量口语化，但不得新增、删减、重排事实。
3. 每条旁白必须配对 `旁白画面`，画面承托可来自信息载体、现场后果、空间状态、道具状态、群像反应、可见行动或留白画面。
4. 若 source 同句包含动作和陈述，动作可落入 `角色动作` / `动作画面`，陈述解释必须落入旁白，并在证据中记录拆分。
5. 不把上游已有对白改成旁白；上游对白仍由 `dialogue_lock_map` 冻结。
6. 正式写回时必须输出 `jieshuoju_source_unit_coverage_map`；不能只用 `narration_to_voice_adaptation_map` 证明覆盖。

## Jieshuoju Source Unit Typing Matrix

显式 `解说剧` 必须先做 source 单元类型化，再写正文。该矩阵只规定投影策略，不授权脚本或规则表自动生成正文。

| source_unit_type | identify_when | landing_policy | required_evidence | hard_block |
| --- | --- | --- | --- | --- |
| `source_dialogue` | 引号内对白、冒号后直接发声、source 明确某角色说出 | `dialogue_freeze`：逐字落为 `对白` + `对白画面` | `dialogue_lock_map`、source 原文拼回一致 | 改成旁白、润色、删词、换词、重排语序 |
| `explicit_inner_voice` | source 明确“心想/心里说/默念/心声/内心OS” | `inner_voice_freeze_or_light_projection`：落为 `内心独白` + `内心独白画面` | 原文主体、可见反应、信息差安全 | 新增角色未想过的信息或改成旁白概括 |
| `visible_action` | 身体动作、位移、表情、手部、道具操作、可见动作结果 | `visual_field_only`：落入 `角色动作`、`动作画面`、`表情特写`、`道具特写` 等 | `output_landing` 指向正式画面字段 | 为了“全旁白”把可见动作重复讲成旁白 |
| `environment_state` | 地点、空间结构、天气、光线、静置物件、环境声底色 | `environment_field`：落入 `环境描写` 或环境刷新 | 场景标题/环境字段落点 | 把环境写成剧情解释或作者判断 |
| `declarative_fact` | 客观事实、公共事实、人物已知状态、叙述者判断 | `narration_pair`：落为 `旁白（叙述者/指定主体）` + `旁白画面` | 旁白主体、画面承托、coverage_status | 转成派生对白/独白/内心独白，或压成概要 |
| `background_exposition` | 前史、设定由来、世界观、人物关系来源 | `narration_pair`：拆成最小可听信息单元逐条旁白化 | `fidelity_operation=sentence_split/light_oralization` | 一句概括多段背景、删关键条件 |
| `time_bridge` | 时间跨度、场外进展、上一轮结果、下一 beat 连接 | `narration_pair_with_transition`：旁白 + 转场/现场后果/信息载体 | `visual_support_type=transition_bridge/visible_consequence` | 重排时间顺序，或只写转场不交代 source 信息 |
| `relationship_state` | 群体共识、权力状态、信任/敌意变化、关系压力 | `narration_pair`，画面优先用站位、群像、沉默、道具归属承托 | `visual_support_type=group_reaction/blocking/prop_ownership` | 把关系状态改成角色新台词或新增冲突回合 |
| `result_summary` | 结果概括、事实结论、已发生后果 | `narration_pair`，画面承托用可见痕迹或现场后果 | `fidelity_operation=verbatim/sentence_split` | 改因果、提前解释未到信息 |
| `rule_or_system_info` | 系统文字、公告、通报、规则显影、外部信息面板 | `system_visual_plus_narration`：`系统画面/规则显影` + `旁白（系统提示/叙述者）` | 系统字段落点、旁白画面配对 | 只写系统画面不让可听信息落地，或新增规则 |
| `mixed_action_declaration` | 同一句含动作和解释、可见结果和作者说明、画面事实和背景补充 | `split_visual_and_narration`：动作/环境进画面字段，陈述解释进旁白 | 同一 `source_anchor` 下记录 split strategy | 整句只旁白导致画面丢失，或整句只动作导致陈述信息丢失 |

### Narrator Profile

| narrator_profile | use_when | restriction |
| --- | --- | --- |
| `neutral_narrator` | 默认解说主体，用户未指定旁白主体时使用 | 语气中性，不替角色评价或新增态度 |
| `specified_subject` | 用户或项目记忆明确指定旁白主体 | 不得借主体口吻新增原文没有的信息 |
| `system_prompt` | 规则、系统、公告、通报等非角色信息 | 必须配 `系统画面`、`规则显影` 或可见信息载体 |
| `protagonist_attached` | source 明确贴近主角视角且用户允许贴身解说 | 只能承接主角已知信息，不得全知泄露 |

### Visual Support Types

| visual_support_type | valid_support |
| --- | --- |
| `synchronous_action` | 与旁白同时发生的角色动作、道具操作或身体反应 |
| `information_carrier` | 文字、名册、屏幕、通报、信物、地图、账本等信息载体 |
| `visible_consequence` | 旁白所述事实留下的痕迹、结果或空间状态 |
| `group_reaction` | 群像沉默、回避、站位、停顿、集体动作 |
| `spatial_empty_hold` | 留白画面、空场、门口、窗外、走廊等承托时间或关系压力 |
| `transition_bridge` | 转场动作、声音桥、物件串联或时间推进画面 |

### Fidelity Operations

| fidelity_operation | allowed_when | forbidden_variant |
| --- | --- | --- |
| `verbatim` | source 原句短且适合直接旁白 | 不得删改关键词 |
| `sentence_split` | source 长句或多信息簇需要拆成多个旁白 beat | 不得改变原顺序 |
| `light_oralization` | 书面句需轻量转为可听句 | 不得改事实、改语气立场或新增评价 |
| `pronoun_resolution` | “他/她/那件事”等指代会导致下游不清 | 不得引入注册表外新称谓 |
| `visual_split` | 混合句需要动作/环境与陈述双落点 | 不得漏掉任一侧信息 |

禁止操作：`summary`、`fact_drop`、`cause_reorder`、`new_exposition`、`tone_rewrite`。任一出现即触发 `FAIL-SCR-SCREENPLAY-MODE`。

## Trigger Gate

`正剧` 中，只有同时满足以下条件，才允许把客观叙事改编为对白或独白；`解说剧` 中，本 gate 只用于证明陈述性 source 已被旁白化，不授权转派生对白/独白/内心独白：

| trigger | must be true | fail if |
| --- | --- | --- |
| `source_is_non_dialogue` | 来源不是上游引号内对白，也不是已冻结对白的改写版本。 | 原文已有对白可直接使用，或派生行替换了原对白。 |
| `payload_is_source_grounded` | 派生行只承载原文已有事实、状态、规则、关系压力、情绪方向、剧情衔接或氛围功能。 | 行内出现新事实、新动机、新承诺、新威胁、新线索、新规则或新因果。 |
| `screen_need_exists` | 直接画面化会导致笨重解释、死旁白、信息不可感知，或当前场景缺少可演的语音节拍。 | 只是为了“更酷”“更有梗”“更像金句”。 |
| `voice_owner_is_eligible` | 说话者在场、可被当前叙事合理拥有该信息，并有当下说出/想到的压力或动机。 | 角色不知道这件事、没有说出口的空间，或说出后会改变信息差。 |
| `audience_disclosure_safe` | 派生行不提前泄露观众或角色此时不该知道的信息。 | 破坏悬念、提前解释谜底、让角色过早自白。 |
| `field_pairing_ready` | 派生行有就近 `对白画面`、`独白画面`、`内心独白画面` 或 `旁白画面` 承托；`解说剧` 中每条陈述性旁白必须有 `旁白画面`。 | 只有一句话孤立输出，没有身体、空间、声音、信息载体、现场后果或对手反应。 |

## Continuity Bridge Trigger

当客观叙事段承担“剧情跨度衔接”时，`正剧` 应优先评估派生语音，而不是把整段硬塞进环境描写、角色动作或旁白；`解说剧` 应拆为连续旁白节拍，并为每个节拍配 `旁白画面`。这里的跨度衔接指一段叙述同时压缩多个当前场景必须承接的信息簇：

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
| `旁白（主体）` | `正剧` 中信息没有合法角色可拥有但必须以声音交代，例如系统规则、历史事实、公告或类型化叙述者；`解说剧` 中所有陈述性 source 信息。 | 旁白画面、信息载体或当下可见后果。 | `正剧` 中让旁白成为默认信息垃圾桶；`解说剧` 中无画面承托、摘要化漏信息或改写 source。 |
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
- `正剧` 中连续使用独白/旁白让成稿像有声小说。
- `解说剧` 中旁白没有逐条对应 `旁白画面`，或把 source 陈述压成概要导致信息缺失。
- `解说剧` 中缺少 `jieshuoju_source_unit_coverage_map`，或 coverage map 中出现 `summary`、`fact_drop`、`cause_reorder`、`new_exposition`、`tone_rewrite`。

## Evidence Structure

执行报告或节点证据必须保留等价结构：

```yaml
jieshuoju_source_unit_coverage_map:
  - unit_id: "JSJ-001"
    source_anchor: "原文段落/句子锚点"
    source_text: "源文本单元"
    source_unit_type: "source_dialogue | explicit_inner_voice | visible_action | environment_state | declarative_fact | background_exposition | time_bridge | relationship_state | result_summary | rule_or_system_info | mixed_action_declaration"
    landing_policy: "dialogue_freeze | inner_voice_freeze_or_light_projection | visual_field_only | environment_field | narration_pair | narration_pair_with_transition | system_visual_plus_narration | split_visual_and_narration"
    narrator_profile: "neutral_narrator | specified_subject | system_prompt | protagonist_attached | n/a"
    visual_support_type: "synchronous_action | information_carrier | visible_consequence | group_reaction | spatial_empty_hold | transition_bridge | n/a"
    fidelity_operation: "verbatim | sentence_split | light_oralization | pronoun_resolution | visual_split"
    output_landing: "场景/字段"
    coverage_status: "covered | split_covered | dialogue_frozen | visual_only | n/a_for_zhengju"
    risk_check:
      summary: false
      fact_drop: false
      cause_reorder: false
      new_exposition: false
      tone_rewrite: false
      declarative_to_non_narration: false
      visual_over_narrated: false

narration_to_voice_adaptation_map:
  - source_anchor: "原文锚点"
    source_text: "客观叙事原句或摘要"
    screenplay_mode: "zhengju | jieshuoju"
    mode_policy: "zhengju_source_grounded_voice | jieshuoju_narration_only"
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
      jieshuoju_declarative_to_non_narration: false
```

## Weak / Strong Examples

| source narration | weak adaptation in `正剧` | strong adaptation in `正剧` |
| --- | --- | --- |
| “院子里的人都知道，少一个名字就意味着少一条命。” | 对白（甲，严肃）：“少一个名字就意味着少一条命。” | 对白（点名人，压低声）：“少了一个。” 对白画面：名册边角被他按住，后排没人接话。 |
| “她早就习惯被这样审视。” | 内心独白（她）：“我早就习惯被这样审视。” | 不语音化：表情特写写眼睑不动、手指把袖口抚平；如必须贴近主观，可写内心独白（她）：“又来了。” |
| “这条规矩从来没有例外。” | 独白（主角）：“这条规矩从来没有例外。” | 旁白（系统提示）：“违规者，无例外。” 旁白画面：规则文字在屏幕底部停住，角色的呼吸声压低。 |
| “任盈盈护送老人孩子从村西后路往石井村暂避；令狐冲留在织坊，把黑蓑伏刃流火力引在自己身上；远处三短一长箫声后，石井村方向传来鞭梢破风。” | 旁白：任盈盈已经护送老人孩子去石井村，令狐冲留在织坊，敌人又追来了。 | 对白（陈阿叔，抱紧孩子压低声）：“三短一长，是任姑娘的号。西路那批人到石井了。” 对白画面：他摸到后门门闩，却没有立刻拉开。对白（令狐冲，盯着门外海雾）：“带阿真走。九鬼组下一刀，不会只落在织坊。” 对白画面：剑尖黑蓑断絮滴水，远处鞭梢破风声逼近。 |

`解说剧` 强模式示例：

```md
旁白（叙述者）：“任盈盈护送老人孩子从村西后路往石井村暂避。”
旁白画面：村西后路上，老人和孩子贴着石墙快步前行，任盈盈回头看了一眼织坊方向。
旁白（叙述者）：“令狐冲留在织坊，把黑蓑伏刃流火力引在自己身上。”
旁白画面：织坊门口的水迹被脚步踩乱，令狐冲站在门内，剑尖垂着黑蓑断絮。
```

## Review Gate Mapping

| Review Question | Review Gate | Fail Code | Rework Target | Report Evidence |
| --- | --- | --- | --- | --- |
| 客观叙事 mode-aware 语音化是否只来自非引号内叙事，没有改写或替换上游已有对白？ | `GATE-BD-04` / `GATE-BD-19` | `FAIL-BD-DIALOGUE` / `FAIL-BD-NARRATION-VOICE` | `steps/script-layer-workflow.md#N4.2-NOVEL-TRANSFORM` | `dialogue_lock_map` 与 `narration_to_voice_adaptation_map.risk_check.rewrites_source_dialogue=false` |
| 每条派生语音是否有 `source_anchor`、`objective_fact_payload`、合法 `voice_owner`、知识依据和触发理由？ | `GATE-BD-19` | `FAIL-BD-NARRATION-VOICE` | `steps/script-layer-workflow.md#N4.2-NOVEL-TRANSFORM` | `narration_to_voice_adaptation_map` 记录 source、payload、trigger、owner 和 knowledge_basis |
| 派生行是否没有新增事实、事件、因果、规则、线索、人物动机、关系结果或提前泄露信息差？ | `GATE-BD-03` / `GATE-BD-19` | `FAIL-BD-FAITHFULNESS` / `FAIL-BD-NARRATION-VOICE` | `steps/script-layer-workflow.md#N4.2-NOVEL-TRANSFORM` / `N6R-BD-REPAIR` | `risk_check.fact_drift/new_event/new_causality/new_rule_or_clue/new_character_motivation/audience_disclosure_leak=false` |
| 派生对白或独白是否有就近画面/动作/反应承托，并且没有变成作者口吻、金句堆砌或有声小说式解释？ | `GATE-BD-06` / `GATE-BD-13` / `GATE-BD-19` | `FAIL-BD-NOVEL-TO-SCREEN` / `FAIL-BD-VISUAL-LANGUAGE` / `FAIL-BD-NARRATION-VOICE` | `steps/script-layer-workflow.md#N4.2-NOVEL-TRANSFORM` / `N5-BD-VISUAL-LANGUAGE` | `paired_visual_or_reaction_field`、`author_voice_leak=false`、`over_voice_budget=false` |
| 跨度性剧情衔接叙事是否先拆成 `bridge_payload_units`，只把最影响当前行动的 1-2 个信息簇转成派生语音，其余交给画面、音效、动作或留白？ | `GATE-BD-19` | `FAIL-BD-NARRATION-VOICE` | `steps/script-layer-workflow.md#N4.2-NOVEL-TRANSFORM` | `narration_to_voice_adaptation_map.bridge_payload_units`、`derived_voice_line`、`paired_visual_or_reaction_field` |
| `screenplay_mode` 是否正确约束陈述性信息：默认 `正剧`，显式 `解说剧` 时 source 单元已类型化覆盖，所有陈述性 source 均为 `旁白/旁白画面`，未转派生对白/独白/内心独白，且无摘要/漏写/重排？ | `GATE-SCR-25` | `FAIL-SCR-SCREENPLAY-MODE` | `N1/N3/N6/N8` | `screenplay_mode_decision`、`jieshuoju_source_unit_coverage_map`、`narration_to_voice_adaptation_map.mode_policy`、`audio_visual_pairing_map` |
