# CONTEXT.md

本文件是 `story-plan-chapter-level` 的经验层知识库，不承载核心执行合同，不记录流水日志。每次调用本技能时必须与同目录 `SKILL.md` 成对加载。

## Context Health

```yaml
monitor_version: 1
soft_limit_chars: 40000
hard_limit_chars: 80000
status: ok
recommended_action: keep-chapter-planning-heuristics-only
last_checked_at: 2026-04-26
```

## Type Map

| failure_or_outcome_type | root_cause_layer | immediate_fix | systemic_prevention | verification_point |
| --- | --- | --- | --- | --- |
| 章级只有梗概，没有节奏 | chapter-level rhythm gap | 补七步结构、规划义务和 Mermaid 图 | 在模板固定节奏段落，并在 review gate 检查 handoff slots | 节奏可供 drafting 直接读取 |
| 章级写了节奏，但 drafting 还得二次猜 pack/mode | rhythm handoff under-spec | 在 `本章节奏曲线` 中补齐 `selected_pack / selected_mode / mode_selection_reason / payoff_type / rhythm_intensity / previous_next_contrast / 规划义务 / 义务段位 / 建议写法` | 把共性 handoff 合同回指到 shared contract，并在模板固定槽位 | drafting 可直接读取 planning handoff |
| 章级只有 `payoff_type / micro_payoff`，没有独立爽点设计 | payoff design collapsed into rhythm | 补 `本章爽点设计`，锁 `reader_desire / promise_source / genre_payoff_profile / character_anchor / payoff_mode / build_up / delivery_action / satisfaction_delta / exaggeration_logic / cost_or_aftershock / aftertaste_hook` | 将爽点规则独立到 `references/chapter-payoff-rules.md`，再由节奏 handoff 消费 | 读者满足先被设计，再被节奏化移交 |
| 所有类型小说写成同一种爽法 | genre payoff flattening | 补 `genre_payoff_profile`，按 `types/payoff-genre-type-map.md` 校准类型口味、禁忌和兑现尺度 | 在 N4 爽点设计前先形成类型画像 | 同样的动能/势能/浪能在不同类型下呈现不同爽法 |
| 多章高潮点同质化 | payoff variation collapse | 补 `payoff_variation_axis`，至少改变对象、机制、尺度、时序、参与者、情绪或后果中的两项 | review gate 检查近邻章节高潮点差异 | 同类爽点保留熟悉感，但兑现方式不断变化 |
| 多章高超对决千篇一律 | duel variation collapse | 补 `duel_variation_axis`，至少改变对手类型、对决场域、胜法、代价或情绪色彩中的两项 | review gate 检查近邻章节对决差异 | 高超感来自不同博弈，不只是更大声量 |
| 爽点很刺激但不像这个角色会做的事 | character-payoff mismatch | 补 `character_anchor` 与 `exaggeration_logic`，回指角色个性、欲望、缺陷、惯常反应、关系姿态或成长压力 | 在 payoff review gate 固定角色一致性检查 | 爽点夸张但合情理，不靠剧情需要硬拽角色 |
| 章级没有本章时间推进 | chapter chronology gap | 补 `chapter_start_state / visible_time_span / event_order / parallel_hidden_events / chapter_end_state / handoff_to_next_chapter` | 在模板和 review gate 固定时间推进槽位 | drafting 能继承章内事件顺序和章末状态 |
| 本章时间推进漂离卷级时间线 | timeline inheritance drift | 回读目标卷 `本卷时间线 / chapter_chronology` 后重写本章时间推进 | steps 固定 `N3-CHAPTER-TIMELINE` | 章级不静默改变卷级事件顺序 |
| `selected_mode` 只有枚举值，没有选择依据 | mode arbitration gap | 补 `mode_selection_reason`，并让理由回指本章冲突、任务、信息压力、情绪调性、旅程/游玩状态、`micro_payoff` 或 `exit_hook` | 在 shared handoff、chapter rhythm rules、模板、review gate 和 validator 固定该槽位 | 势能/动能/浪能选择可复核，不靠直觉 |
| 章内七步完整但连续章感很平 | chapter wave flattening | 补 `previous_next_contrast`，写清承接上一章与预留下一章的波形变化 | 在模板与 review gate 固定前后章对比槽位 | 章节读感有起伏，不是每章同构 |
| `rhythm_intensity=高` 被滥用 | intensity inflation | 重判本章强度，只有强转折、强行动、强压迫、强情绪或阶段爆点才保留高强度 | 用 `rhythm_intensity` 控制连续高点密度 | 真正高点不被普通章节稀释 |
| `payoff_type` 与 `micro_payoff` 不一致 | payoff mismatch | 先裁定本章主导读者满足，再改写 `micro_payoff` 或 `payoff_type` 对齐 | review gate 检查 payoff 与兑现动作的一致性 | 读者读完能知道本章“爽点/暖点/信息点”是什么 |
| `浪能式` 被误写成无事发生 | soft-rhythm payoff gap | 补情绪、关系、世界感、软信息或状态修复层面的 `micro_payoff` | 在 rhythm rules 固定浪能式七步职责，避免把松弛等同于空转 | 松弛但不空，舒缓但有轻盈 payoff |
| 章级悬念被写成“吊胃口”口号或提前剧透 | chapter suspense switch gap | 补 `本章悬念开关`，明确读者可知、角色可知、隐藏、误导、揭秘、只埋不揭、章末压力和正文禁区 | 模板、steps、review 固定悬念开关并回指卷级 | drafting 能执行信息边界，不写上帝视角说明 |
| 一章同时动太多悬念导致读者疲劳 | chapter suspense overload | 补 `本章悬念线程动作` 与 `本章悬念负载`，标出主操作和副操作 | review gate 检查线程动作、负载理由和微兑现 | 本章知道主推哪条悬念、哪条只轻触 |
| 线索与伏笔混写 | chapter-level information drift | 拆开 `本章线索` 和 `本章伏笔` | 在模板固定两个标题，review gate 禁止合并 | 信息推进和长期回照可区分 |
| 伏笔只写铺设，不写兑现位判断 | foreshadow incompleteness | 即使无兑现也明确标 `本章无兑现` | 在模板保留 `铺设 / 兑现` 双槽位 | 伏笔段落完整 |
| 本章支流没有汇聚动作或去向 | task convergence gap | 补 `汇聚动作 / 未汇聚任务去向` | 在模板固定任务关系槽位，review gate 检查支流闭环 | validation 能判断支流是否回到主任务 |
| 章级局部补写漂离卷级职责 | upstream reread skipped | 重新回读目标卷 `卷规划.md` 与 `整体规划.md` 后再修订 | steps 固定 `N1-UPSTREAM-REREAD`，Input Contract 禁止缺上游落盘 | 章级 `上承卷级任务` 能回指卷级任务线 |
| 建议写法变成正文句段 | planning/drafting boundary drift | 删除对白、叙述段、正文桥段，只保留结构建议 | review gate 固定非正文化检查 | 章级文件仍是 planning，不是 drafting |
| 启用 subagents 后没有按项目顾问请教章级执行问题 | advisor consultation gap | 按 `team.yaml` 的 `roles.planning.members` 追问本章职责、时间推进、爽点变奏、悬念开关、任务汇聚和 drafting handoff | 显式启用 subagents 时先生成 `advisor_consultation_packet`，再进入章级规划创作 | `第N章.md` 能说明顾问建议如何转成时间、爽点、悬念、任务或节奏 handoff 指导 |

## Repair Playbook

1. 先判断故障属于上游回读、节奏 handoff、任务汇聚、信息层、模板对齐、review gate 还是正文化越界。
2. 若缺上游，暂停落盘并补读 `2-卷章/整体规划.md` 与目标卷 `2-卷章/第N卷/卷规划.md`。
3. 若时间推进不清，优先回到 `../_shared/timeline-design-contract.md` 与卷级 `本卷时间线`；先补事件顺序和章末状态，再改冲突、爽点或节奏。
4. 若节奏字段不足，优先回到 `../../_shared/chapter-rhythm-handoff-contract.md` 与 `references/chapter-rhythm-rules.md`；若只缺 mode 选择依据，补 `mode_selection_reason` 并检查其是否能回指本章 `micro_payoff`。
5. 若章感同构，优先补 `previous_next_contrast`；先判断上一章是升压、爆发、松弛还是余波，再决定本章是接力、反向变奏还是换气。
5. 若读者满足不清，先裁定 `payoff_type`，再让 `micro_payoff` 写成一个可验证的小兑现。
6. 若爽点只剩一个抽象分类，先回到 `reader_desire` 和 `promise_source`；读者想要什么不清楚时，不要急着选 `selected_mode`。
7. 若不同项目读起来同一种爽法，先形成 `genre_payoff_profile`；类型画像没有锁住前，不要直接套动能/势能/浪能清单。
8. 若近邻章节高潮点同质化，先补 `payoff_variation_axis`；至少换两项：满足对象、兑现机制、尺度、释放时序、参与者关系、情绪颜色、代价或余味。
9. 若高超对决连续重复，回读近邻章的爽点设计，补 `duel_variation_axis`；至少换两项：对手类型、对决场域、胜法、代价、情绪色彩。
10. 若爽点很夸张但角色依据不足，回读 `card_path` 或最小人物投影，补 `character_anchor` 与 `exaggeration_logic`。
11. 若 `micro_payoff` 与爽点设计脱节，先修 `delivery_action / satisfaction_delta`，再把它们压缩为节奏义务。
12. 若强度飘高，重判 `rhythm_intensity`；高强度必须有质变，不能只是“这一章也很重要”。
13. 若任务线悬空，优先补 `上承卷级任务 / 汇聚动作 / 未汇聚任务去向`，再看主线与支线。
14. 若信息推进混乱，先拆 `本章线索` 与 `本章伏笔`，再分别检查可见信息推进和长期回照。
15. 若输出模板或标题不齐，回到 `templates/chapter-planning.template.md` 与 `templates/output-template.md`。
16. 若审查意见指出正文化，删除句段级文本，只保留 planning 义务、建议写法和结构意图。
17. 修复技能包结构后运行工作车间 validator；修复业务章规划后运行父层 planning 输出校验或人工 review gate。
18. 如果显式启用 subagents，顾问问题要落到“这一章具体该承担什么变化”，例如本章只开线还是兑现、本章高潮如何和近邻章变奏、本章哪些信息正文不能说。

## Reusable Heuristics

- 章级是 planning 的最细层，但仍不是正文。
- `本章时间推进` 先回答世界内事件如何发生；`本章节奏曲线` 再回答这些事件如何被读者体验。
- 七步结构只要求职责完整，不要求七段等长。
- 章级最重要的节奏动作不是替 drafting 写句子，而是把 `pack / mode / obligation / suggestion` 移交清楚。
- `selected_mode` 不是口味标签；必须由本章主要 payoff 裁决：认知/压力兑现偏势能，行动/结果兑现偏动能，情绪/关系/旅途/游玩兑现偏浪能。
- `payoff_type` 是读者满足的主轴，不是分类装饰；一个章节最好只选一个主导满足，再允许副满足作为辅助。
- 爽点设计是读者满足的前置系统，`payoff_type` 和 `micro_payoff` 只是它在节奏 handoff 里的压缩结果。
- `genre_payoff_profile` 是防止同质化的关键：类型画像校准爽法口味，角色锚点保证爽点长在人物身上，节奏式决定兑现路径。
- `payoff_variation_axis` 是防止多章疲劳的关键：同类高潮点可以重复出现，但对象、机制、尺度、时序、情绪和后果必须换组合。
- 好爽点要像角色本人把事情推到了极致，而不是作者把刺激物塞进章节里；优先检查“这个人为什么会这样爽”。
- 夸张不是越界许可证；`exaggeration_logic` 要说明戏剧放大来自角色欲望、缺陷、关系压力、处境诱因或成长节点。
- 动能式的“高超对决”不只等于武斗；它可以是法则碰撞、谈判交锋、棋局互算、推理追捕、手艺比赛或商业博弈，取决于类型画像。
- 多章对决的差异优先从“对手不同”推导，而不是从“主角用更大的招”推导；好对手会逼出不同胜法。
- 动能式爽点通常交付外部化结果，势能式爽点通常交付认知、精神或压力变化，浪能式爽点通常交付体验、关系、生活质感和状态修复。
- `rhythm_intensity` 控制长篇波形，高强度越多越不值钱；连续高强度必须有递进质变。
- `previous_next_contrast` 是防机械七步的关键：章节可以内部七步完整，但外部波形必须有承接、换气或反向变奏。
- `浪能式` 可以轻松、愉快、欢乐、松弛、舒缓，但不能空转；它至少要交付关系升温、状态恢复、世界感打开、趣味体验或软线索之一。
- 章级如果不说清支流当章怎么汇、没汇后去哪，下游通常会把“悬念”写成“悬空”。
- 章级悬念的最低可执行标准是：正文作者能判断“这句解释现在能不能说”。如果不能判断，说明 `正文禁止上帝视角说明` 还不够具体。
- `本章悬念线程动作` 只记录本章实际操作的线程；没有动作的悬念不要塞进章级，避免信息噪音。
- `义务段位` 只锁必须出现或必须完成的结构义务；`建议写法` 只给推荐编排，不拥有正文法律效力。
- Mermaid 图不是装饰；它至少要让读者看见起势、转折、升级、高潮和尾钩。
- 局部修订也要完整回读上游，因为章级字段之间牵连很紧，改一处任务线常常会影响节奏和章末达成。
- 章级顾问请教的价值是把“灵感”压缩成可执行 handoff：本章变化、信息边界、爽点变奏、任务汇聚和 drafting 禁区必须比顾问原话更具体。
