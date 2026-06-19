# Screenwriting Masters And Short-Drama Rhythm Contract

本合同为 `4-编剧` 提供新增细则：题材类型解析、叙事情节解析、编剧大师改编逻辑、爆款短剧节奏表现手法、匹配机制、套用逻辑、高潮强化和尾钩设计。它补充 copied references，不覆盖 `SKILL.md`、保真边界或输出路径。

## Evidence Sources

本合同综合以下资料形成规则，不在执行时强制联网：

- Sundance Collab 的剧本改编课程强调先识别原作核心、主题、人物欲望和故事引擎，再建立可独立成立的电影结构。
- Sundance Collab 的短片剧作课程将短片创作拆成故事结构、人物欲望、戏剧问题、场景 craft、行为/动作/对白、开场/结尾画面和视觉化页面表达。
- 黑泽明改编莎士比亚的公开电影案例显示：成功改编不是逐字搬运，而是把原作冲突转置到新的文化、视觉、身体和环境系统；BFI 对 `Ran` 的分析尤其提示“把语言挑战改成身体挑战”这一改编逻辑。
- Penguin Random House 对《Something Like An Autobiography》的书籍说明指出，黑泽明将好剧本、导演写作能力、演员指导、机位和广泛阅读视为导演基础；本技能只吸收“剧本是影视表达基底”和“文学输入转成可拍行动”的部分。
- 国家广电总局 2025 年“微短剧+”行动计划将微短剧概括为兼具影视剧基因与短视频特性，具有快节奏、高密度、题材丰富、低成本、短周期和传播触达优势。
- 国家广电总局 2026 年“微短剧精品创作传播计划”强调思想与艺术交融、网感与美感兼备、贴近时代/人民/生活以及全流程创作指导。
- 中国视协《精品微短剧创新发展趋势研究报告》发布信息强调强节奏不是快剪辑，而是适配拇指视听消费场景的叙事时间经济学；强冲突需要精准戏剧矛盾。
- Screenburn 的 microdrama structure 资料将单集结构概括为开场钩子、升级和 cliffhanger，强调竖屏短剧不是压缩长片。
- Morphic 的 AI microdrama 指南给出 75 秒左右单集的 hook、escalation、cliffhanger 时间分布，并提醒角色、地点和对白漂移是 AI 微短剧常见失败点。

## Genre Type Parsing

题材类型不是市场标签，而是决定观众期待、信息释放、节奏密度和高潮兑现方式的工作变量。每集至少建立以下字段：

```yaml
genre_narrative_profile:
  primary_genre: ""
  secondary_genre: ""
  audience_contract: ""
  pleasure_engine: ""
  risk_engine: ""
  emotional_promise: ""
  production_constraint: ""
```

### Genre Families

| genre_family | audience_contract | rhythm_bias | climax_bias | hook_bias |
| --- | --- | --- | --- | --- |
| 逆袭爽剧 | 观众期待弱者获得可见反制、身份翻盘或价值证明 | 高密度压迫 -> 证据反转 -> 公开兑现 | 让侮辱者、旁观者或权力结构发生可见位移 | 身份误认、证据露角、反派话未说完 |
| 甜宠/情感 | 观众期待关系误解、暧昧推进、保护与选择 | 小冲突密集、情绪延迟、亲密距离变化 | 关系选择被迫公开，身体距离或称呼改变 | 未完成触碰、误听一句话、礼物/旧物露出 |
| 复仇/权谋 | 观众期待信息差、布局、反杀和代价 | 暗线埋证 -> 表面失利 -> 背后翻盘 | 证据、证人、物件或盟友改变权力结构 | 反派以为赢了，镜头外证据进入场内 |
| 悬疑/惊悚 | 观众期待线索、误导、真相逼近 | 问题前置、信息节制、恐惧逐层具体化 | 已知安全空间变成危险空间 | 声音异常、物件位置改变、监控/短信异常 |
| 家庭伦理 | 观众期待亲情压力、身份义务、旧账爆发 | 日常细节承压、饭桌/门槛/病房等空间推进 | 家庭秩序被一句话或一个动作打破 | 长辈停顿、孩子听见、旧账物证出现 |
| 职场/行业 | 观众期待规则压迫、能力证明、专业反制 | 任务倒计时、公开场景、专业细节兑现 | 专业证据让局面反转 | 关键文件、会议投屏、客户一句质疑 |
| 古装/玄幻 | 观众期待身份等级、规则体系、奇观和命运选择 | 规则说明动作化、仪式压迫、身份揭露 | 规则代价或身份真相可视化 | 法器/令牌/称谓/天象触发未闭合问题 |
| 法治/现实议题 | 观众期待真实可信、规则温度、问题解决 | 案例压力、事实证据、人物选择 | 法律/制度/公共行动改变个人处境 | 一份材料、一句报警/起诉/举报后的后果 |

## Narrative Plot Parsing

每集至少拆出 3-7 个 `narrative_beats`。每个 beat 必须能回答“谁想要什么、被什么阻碍、观众知道什么、这一步改变了什么”。

```yaml
narrative_beat:
  beat_id: "E1-B1"
  source_anchor: ""
  character_want: ""
  obstacle: ""
  audience_knowledge: ""
  information_shift: ""
  emotional_shift: ""
  plot_function: "hook | setup | escalation | reversal | payoff | cliffhanger"
  screenplay_action: ""
```

## Adaptation Logic From Masters

| principle | usable rule in `4-编剧` | forbidden misuse |
| --- | --- | --- |
| 原作核心优先 | 先锁原作这一集最不可丢的关系、欲望、主题和事件结果，再决定删繁、压缩或转译 | 为了“更短剧”直接改结局或动机 |
| 结构独立成立 | 单集剧本必须有开场钩子、中段升级、当集落点和下一集问题，不依赖观众读过小说 | 用旁白解释“前情提要”替代当前场景冲突 |
| 人物欲望推动 | 每场至少有一个角色在争取、逃避、遮掩、确认或试探 | 让角色站着复述设定 |
| 陈述转行动 | `正剧` 中重要陈述优先转成对白、独白、喊出式台词、道具证据、动作结果或场内声音；显式 `解说剧` 中先做 source 单元覆盖，陈述性 source 按主合同转为 `旁白/旁白画面`，可见动作/环境仍走正式画面字段 | `正剧` 把信息全塞旁白或字幕；`解说剧` 漏掉旁白画面、摘要化丢失 source、把陈述改成派生对白，或把可见动作/环境过度旁白化 |
| 黑泽明式转置 | 找到原作戏剧功能，把文学段落转成身体挑战、空间压力、天气/声音/道具和集体反应 | 只把地点时代换掉，冲突仍靠解释 |
| 麦基式场景转折 | 场景进入和离开时价值状态必须变化：信任/怀疑、强/弱、知道/不知道、靠近/疏离 | 只换场不改变局面 |
| Syd Field 式段落目标 | 单集内部建立清晰起点、中点变化和尾端问题 | 用散点爽点替代单集推进 |
| Save-the-Cat 式可感同情 | 早段给主角一个可见选择或代价，让观众知道为何跟他/她走 | 用人设介绍替代选择 |

## Hit Short-Drama Rhythm Mechanisms

每集选择 1-2 个主机制、1 个辅助机制。机制必须匹配题材和情节，且落到具体承托。

| mechanism_id | mechanism | best_for | application_logic | required_support | fail_signal |
| --- | --- | --- | --- | --- | --- |
| `RHY-01` | 三秒误判钩子 | 逆袭、悬疑、权谋、甜宠 | 开场让观众先得到一个似是而非判断，10-20 秒内给出纠偏证据 | 一句台词、一个物件、一处空间关系或角色反应 | 只有惊讶表情，没有可验证信息 |
| `RHY-02` | 压迫阶梯 | 逆袭、家庭、职场 | 每 15-25 秒增加一种压力：身份、规则、经济、关系、时间 | 压迫者动作、旁观者反应、空间逼近、倒计时 | 压迫只是骂人重复 |
| `RHY-03` | 证据露角 | 悬疑、复仇、职场、法治 | 不直接揭真相，先让证据的一角进入场内，迫使角色改变策略 | 文件、短信、录音、伤痕、旧物、监控声 | 证据只在报告里，不在场景中 |
| `RHY-04` | 关系错位 | 甜宠、家庭、权谋 | 让角色 A 的行动被 B 误读，观众知道或半知道错位原因 | 视线遮挡、断句、未送达消息、错称呼 | 误会靠弱智不沟通 |
| `RHY-05` | 公开场合翻盘 | 逆袭、职场、家族 | 将私人压迫带到公开空间，让见证者成为反转的一部分 | 会议、宴席、直播、门口围观、族会 | 没有见证者变化 |
| `RHY-06` | 倒计时压缩 | 职场、悬疑、救援、复仇 | 给场景一个硬时限，删掉非必要解释 | 时间显示、来电、门外脚步、系统提示 | 倒计时不改变选择 |
| `RHY-07` | 沉默爆点 | 情感、家庭、复仇 | 关键处不加话，让环境声、动作停顿和对手反应承托爆点 | 杯子停住、门声、呼吸断拍、群体安静 | 只是写“沉默很久” |
| `RHY-08` | 低成本奇观 | 古装、玄幻、悬疑、AI 视频 | 用一个可生成的视觉状态变化承托奇观，不铺大场面 | 令牌发光、灯灭、影子错位、风铃无风响 | 奇观过大导致下游不可生成 |
| `RHY-09` | 台词炸点 | 爽剧、家庭、职场 | 把小说重要陈述压成角色必须说出口的一句台词 | source anchor、说话动机、现场听众、后果 | 金句脱离人物处境 |
| `RHY-10` | 反高潮留白 | 悬疑、复仇、情感 | 不在本集完全释放，让观众看到代价或更大问题 | 反派笑、主角收手、证据残缺、电话未接 | 留白变成没写完 |
| `RHY-11` | 迷你彩蛋尾钩 | 全题材 | 正片落点后补一个 1-3 秒可见/可听/可感的小异常 | 手机亮屏、背后脚步、门缝光、物件掉落 | 彩蛋与下一集无关 |
| `RHY-12` | 情绪过山车 | 甜宠、家庭、爽剧 | 同一集完成期待、失落、反弹或保护；每次转向有动作承托 | 靠近/撤离、礼物收回、称呼改变 | 情绪词堆叠无行为 |

## Matching Algorithm

1. 从 `genre_narrative_profile.primary_genre` 选 2-4 个候选机制。
2. 从 `narrative_beats.plot_function` 选能服务本集核心变化的机制。
3. 如果 source 中已有强冲突，优先“压实承托”，不新增更大事件。
4. 如果 source 是过渡集，使用 `证据露角`、`关系错位`、`反高潮留白` 或 `迷你彩蛋尾钩`，避免硬造大高潮。
5. 如果 AIGC 视频生成限制明显，优先低角色数、低地点数、强物件/声音承托的机制。
6. 每个机制输出时必须写：

```yaml
rhythm_strategy:
  mechanism_id: ""
  matched_reason: ""
  source_anchor: ""
  support_field: "dialogue | action | sound | prop_evidence | spatial_pressure | reaction"
  on_page_placement: ""
  downstream_note: ""
```

## Climax Treatment Rules

高潮强化不是把强度写满，而是让观众在一个明确落点上看见变化。

| layer | requirement | examples_of_support |
| --- | --- | --- |
| 视觉冲击 | 一个状态变化必须可见 | 人物位置变化、物件破损、灯光改变、血迹/泪痕/文件露出、群体退后 |
| 声音冲击 | 一个声音或沉默必须改变场景状态 | 门锁响、电话外放、录音播放、全场静音、雨声盖过一句话 |
| 情绪冲击 | 情绪必须经过身体或对手反应落地 | 呼吸断拍、手指松开、对方避视、旁观者停筷 |
| 行动落点 | 高潮结束后必须改变下一步行动 | 追、停、签字、报警、离开、公开、转身、收证据 |

## Episode Final Image / Mini-Easter-Egg Hook

集末尾钩优先使用“最后一个可见/可听/可感受落点”，不是一句解释。可选类型：

| hook_type | use_when | landing_rule |
| --- | --- | --- |
| `visible-object` | 证据、身份、旧物、玄幻规则 | 最后一帧让物件状态改变，但不解释完整含义 |
| `audible-interruption` | 悬疑、情感、复仇 | 最后一个声音打断当前稳定局面 |
| `felt-body-reaction` | 情感、家庭、惊悚 | 最后落在身体反应，观众知道角色意识到更大问题 |
| `public-witness-shift` | 逆袭、职场、家族 | 群体态度改变一瞬间，下一集承接公开后果 |
| `mini-easter-egg` | 过渡集或信息铺垫集 | 正片结束后 1-3 秒出现小异常，必须能接下一集 |

## Controlled Dramatized Supplement Rules

必要细节补充不是装饰性加戏，而是把 source 中已经存在但影视观看不足的戏剧功能落成可见、可听、可演、可连续消费的剧本材料。

允许服务以下目标：

- 补足人物行动的起因、对象、阻碍、触发点或结果承托。
- 让空间转换、时间跳跃、信息传递、因果承接更连贯。
- 把小说抽象心理转成可见、可听、可演的场内材料。
- 用群像、道具、声音、沉默、站位或转场承托压迫、误解、反击、确认和尾钩。
- 让 AIGC 下游知道角色、物件、地点、声音、天气、情绪和状态的当前变化。

每次补写必须能进入 `dramatic_intent_map`、`dramatization_gap_map`、`controlled_adaptation_plan`、`continuity_detail_map` 或 `rewrite_scope_check` 中的至少一个证据表。

不得使用细节补充新增 source 不支持的决定性人物动机、事实、关系、能力、线索、规则、因果或结局。

## Review Gate Mapping

| review_question | review_gate | fail_code | rework_target | report_evidence |
| --- | --- | --- | --- | --- |
| 题材画像是否输出 audience contract、pleasure engine 和 risk engine？ | `GATE-SCR-03` | `FAIL-SCR-GENRE-NARRATIVE` | `N2-SCR-GENRE-NARRATIVE` | `genre_narrative_profile` |
| 每个节奏机制是否匹配题材/情节，并有 source anchor 与承托字段？ | `GATE-SCR-08` | `FAIL-SCR-RHYTHM` | `N4-SCR-RHYTHM-ENGINE` | `rhythm_strategy_map` |
| 高潮是否同时有视觉、声音、情绪和行动落点？ | `GATE-SCR-09` | `FAIL-SCR-CLIMAX` | `N5-SCR-CLIMAX-HOOK` | `climax_treatment_map` |
| 尾钩是否为最后可见/可听/可感受落点，而不是抽象悬念句？ | `GATE-SCR-10` | `FAIL-SCR-HOOK` | `N5-SCR-CLIMAX-HOOK` | `episode_final_image_map` |
| 必要补写是否服务戏剧功能、连贯性、影视表现或下游理解，并有 source basis 和保真边界？ | `GATE-SCR-11` / `GATE-SCR-12` | `FAIL-SCR-DETAILS` / `FAIL-SCR-REWRITE-SCOPE` | `N2/N3/N6` | `dramatic_intent_map`、`dramatization_gap_map`、`controlled_adaptation_plan`、`rewrite_scope_check` |
