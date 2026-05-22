# CONTEXT.md

## Purpose & Loading Contract

- 本文件是 `aigc/3-导演` 的经验层知识库，不是过程日志。
- 调用本目录 `SKILL.md` 时必须同时加载本文件。
- 本文件不改写 `SKILL.md` 的输入、输出和门禁；只沉淀可复用判断经验、失败模式和修复打法。

## Context Health

- soft_limit_chars: 12000
- hard_limit_chars: 24000
- status: ok
- last_checked_at: 2026-05-13

## Type Map

| failure_or_outcome_type | root_cause_layer | immediate_fix | systemic_prevention | verification_point |
| --- | --- | --- | --- | --- |
| 编导稿只有结构正确没有戏剧干货 | 编导创作内核层 | 回到 `director_substance_pass`，为关键场景补戏剧问题、人物压力、观众位置、信息释放、表演/空间/道具/声音发动机 | 在 workflow 中固定 `N3-DIR-SUBSTANCE`，并在 review 中检查 `director_substance_evidence` | 正文能看到来自上游锚点的动作、声音、空间、道具、表演或沉默余波，而不是只有抽象评价 |
| 高潮画面被压平成普通叙述 | 高点识别层 | 回到上游锁定行动结果、认知翻转、关系暖点、规则显影、奇观或怪异落点，再用既有画面/声音/表演字段强化 | 在字段分流后固定 `peak_visual_pass`，但禁止新增事实、对白或事件结果 | 高点能回指上游，输出有可拍承托和状态差 |
| 画面有细节但没有美学组织 | 画面美学层 | 回到 `visual_aesthetic_pass`，为关键场景补核心画面、视觉气质、画面层级、母题变化、对比轴、节奏和留白取舍 | 在 workflow 固定 `N7-DIR-AESTHETIC`，让 `visual_aesthetic_plan` 成为 LLM 投影前证据 | 正文能看见主视觉和氛围层次；没有"电影感/高级感"等抽象审美词空转，也没有摄影越权 |
| 单场画面各自成立但整集缺少视觉记忆 | 整集美学主轴层 | 回到 `episode_visual_spine`，建立视觉问题、母题链、材质/色彩弧、节奏曲线、呼应目标和克制规则 | `N7-DIR-AESTHETIC` 先做整集视觉主轴，再做单场 `visual_aesthetic_pass`；review 固定 `GATE-DIR-05/06` | 执行报告能看到 `visual_aesthetic_evidence.episode_visual_spine`，正文中能感到核心物件、自然景物、材质和节奏的变化链 |
| 每集结尾没有追更欲，或尾钩变成硬塞预告 | 终结画面层 | 回到 `episode_final_image_pass`，先形成 `final_image_type_profile`，再选环境描写式、道具特写式、情绪酝酿式或高潮结尾式，把尾钩内嵌到最后既有字段 | `N8-DIR-FINAL-IMAGE` 固定迷你彩蛋尾钩：关联下一集但不剧透，从本集末场、视觉主轴、道具状态或高点余波丝滑顺延 | 执行报告有 `episode_final_image_evidence`；终稿最后一组字段能留下悬念/情绪/状态差，但没有下一集预告词或新增事实 |
| 终结画面写成小说式抽象或只有一两个薄镜头 | 终结画面画面纯度层 | 改为 3-6 个可拍 beat 的尾场小段落，用环境刷新、道具状态、人物停顿、群像位置、声音层次和空间方向承载意境 | 在 `episode-final-image-contract.md` 固定剧本画面纯度规则：不靠"像/仿佛/象征/意味着"等解释或比喻，不把尾钩压成单句预告 | 最后一组字段能被下游直接分解为画面/声音/表演，不需要读者解释抽象意义 |
| 氛围感停留在地点标签，缺少五感通感、微观质感和声景层次 | 意境密度层 | 回到 `atmosphere_mood_pass`，按五感氛围框架和意境技法清单为关键情绪场、压迫场、离别场和类型氛围场补意境密度；至少覆盖两个感官通道和一种意境技法 | 在 workflow 固定 `N7-DIR-AESTHETIC` 消费 `atmosphere-and-mood-contract.md`，review 固定 `GATE-DIR-08` | 正文关键氛围场能看到光线纹理、空气湿度、声音质感、气味或时间痕迹中的至少两类感官细节，以及通感、微观放大、反衬、声景层次、延时承托或留白中的至少一种技法 |
| B 路线被误用成自由新增 | 受控增强边界层 | 删除新增对白、事件、规则、线索、因果或人物动机；只保留有上游锚点的环境、反应、表演、调度、声音、道具和余波承托 | `controlled-enrichment-contract.md` 固定 B/C 分界与 `controlled_enrichment_ledger` | 每个新增项有 `source_anchor`、`target_field`、`purpose`、`risk_check` |
| 氛围/道具增强抢走人物动作链 | 人物动作链层 | 回到 `action_first_continuity_check`，先锁定人物 entry_state/action_vector/reachable_target/exit_state；删掉无法通过准入的环境或道具细节 | `../_shared/action-first-continuity-contract.md` 固定人物动作链优先，`controlled-enrichment-contract.md` 将 `action_chain_preserved` 纳入 risk_check | 删掉环境/道具细节后人物动作链不会更顺；保留项均有空间定位、互动、信息、规则/证据/危险源或必要交代理由 |
| 角色在导演稿里缺少活人感行为动机 | 行为动机种子层 | 回到 `director_substance_pass`，补 `lived_in_behavior_seed`：角色当前小事、生活压力/目标/阻碍、下意识反应方向、情绪落点；多人场面补行动者/反应者分工 | `../_shared/lived-in-character-behavior-contract.md` 与 `directorial-authorship-contract.md` 固定源层证据，review 增加 `GATE-DIR-10` | 下游 `4-表演` 不需要凭空给角色找事做；能从导演证据看出角色为什么动、谁行动、谁反应 |
| 场景只剩地点标签，缺少年代/功能/声光身份 | 场景身份种子层 | 回到 `director_substance_pass`，补 `scene_identity_seed`：年代/空间功能/社会语境/环境声底色/材质光影 | `../_shared/scene-shot-identity-contract.md` 与 `directorial-authorship-contract.md` 固定源层证据，review 增加 `GATE-DIR-11` | 下游 `5-摄影`、`8-图像`、`9-视频` 不需要把同一动作生成到泛化空间里 |
| subagents 启用时只本地模拟顾问 | 顾问请教层 | 回到 `team.yaml.roles.supervision.stage_profiles."3-导演"` 或共享合同回退路径，按共享团队顾问合同真实 dispatch 或写明上层阻断降级 | 把带 `node_ref/pass_ref/gate_ref/role_lens` 的 `advisor_consultation_packet` 固定为 LLM 投影前上下文，不让顾问替代上游真源 | 执行报告可看到 roster 来源、节点锚点、可执行指导或降级说明 |
| subagents 启用后只得到泛泛审美评价，没有节点级编导参谋 | 顾问问题质量层 | 回到当前 `steps/directing-workflow.md` 节点、`Thought Pass Map` 与 review gate，把 judgment/actions/evidence/route/gate 转化为顾问任务 | 顾问必须代入角色意识、创作风格和专业水准，输出可转成 `must_do / must_not_do / execution_brief` 的节点级参谋指导 | `advisor_consultation_packet` 中每条采纳意见都能回指节点，并改变节点判断、执行取舍、证据补强、风险禁区或后续投影上下文 |
| 创作规则很强但执行报告无法证明发生过 | 创作证据层 | 补 `director_substance_evidence`、`peak_visual_plan`、`visual_aesthetic_evidence.scene_items` 和 `episode_final_image_evidence`；特例降级必须说明原因 | review 固定 `GATE-DIR-06`，阻断"只有规则文档、没有创作证据"的交付 | 执行报告不仅有 mechanical pass，也能回指关键场景的戏剧问题、高潮画面、视觉主轴、美学组织和终结画面尾钩 |
| 思维·执行节点退化成 checklist | steps 拓扑层 | 回到 `steps/directing-workflow.md#Thinking-Action Node Contract`，为责任节点补 `judgment_question / decision / actions_taken / evidence_keys / route_out / gate_status / source_owner` | review 新增节点 ledger gate，执行报告必须写 `thinking_action_node_ledger`；顾问、review 和 writeback 都消费同一 ledger | 节点不只说明"做了什么"，还能证明"先判断了什么、据此做了什么、证据在哪里、失败回哪里" |
| 学习型合同只完成静态接入 | 验证闭环层 | 补 `learning_integration_review_evidence`，区分真实样例、等价 smoke、`static_only` 和残余风险 | workflow 固定 `Learning Integration Review Closure`，review 检查新增/显著修改合同是否留下静态接入点、样例或 smoke 状态与后续观察点 | 审查结果不再把"文档已引用"误判为"真实生成已稳定产出" |

## Repair Playbook

1. 确认上游 `2-编剧/第N集.md` 已通过编剧门禁，输出路径可读。
2. 从上游正文抽取关键场景清单，逐个检查是否已完成 `director_substance_pass`：有戏剧问题、人物选择压力、观众位置、信息释放和可拍执行策略。
3. 检查上游是否存在高潮/爽点/高光成分；若有，确认 `peak_visual_pass` 已完成：高点有可回指证据、可拍承托、状态差或余波，且没有新增事实、对白或因果。
4. 若本轮启用 subagents，检查 `advisor_consultation_packet`：roster 来源、节点锚点、采纳指导摘要或降级说明。
5. 检查关键场景是否有可回指上游的进入状态、压力源、转折点和退出状态。
5.5. 检查关键人物 beat 是否有活人感行为动机种子：角色当前小事、生活压力/目标/阻碍、下意识反应方向和情绪落点；多人场面是否已说明谁行动、谁反应。
5.6. 检查关键场景是否有场景身份种子：年代/空间功能/社会语境/环境声底色/材质光影是否可回指上游；若只有“房间/街道/大厅”等地点标签，补 `scene_identity_seed`。
6. 若本轮启用 `controlled_enrichment`，检查 `controlled_enrichment_ledger`：每个新增项有上游锚点、目标字段、用途和风险检查。
7. 对所有景境、道具、声音和受控增强做人物动作链复核：人物起始姿态、行动方向、可达对象和结束状态是否清楚；若删掉某个细节后动作更顺，删除或降级该细节。
8. 检查 `episode_visual_spine` 和 `visual_aesthetic_evidence`：整集有视觉主轴，关键场景有核心画面、视觉气质、画面层级、母题变化、对比轴、景境氛围、节奏和留白取舍。
9. 检查 `atmosphere_mood_evidence`：关键氛围场至少两个感官通道和一种意境技法。
10. 检查 `episode_final_image_evidence`：终结画面有类型化匹配、尾钩表面、下一集关联方向和剧透边界。
11. 检查 `thinking_action_node_ledger`：每条记录包含判断问题、执行动作、证据字段、出口路由、gate 状态和 source owner。
12. 若本轮新增或显著修改学习型合同，检查 `learning_integration_review_evidence`。
13. 交付前把 review finding 当成修复输入；阻断项先在本阶段修复并复审，仍失败再阻断或回源层。

## Reusable Heuristics

- `3-导演` 的价值不是"把剧本写得更像电影"，而是让每场关键戏有问题、有压力、有选择、有信息释放、有观众位置和可执行的动作/声音/空间发动机。
- 高潮画面强化的顺序是：先找上游已有满足兑现点，再找角色锚点和状态差，最后才强化画面、声音、表演和余波；不要为了"更炸"新增事实。
- 团队顾问的价值是"创作前照亮取舍"，不是接管剧本；最终执行口径必须同步于当前思维·执行节点，落成节点判断、执行取舍、证据补强、字段投影、表演任务、声画承托和风险禁区，并作为后续 LLM 投影、阶段内修复与复审的上下文继续使用。
- 画面美学不是多写形容词，而是先定核心画面和主次层级：观众记住什么、什么只做背景、哪里该重复成母题、哪里该留白。
- 视觉母题要变化，不要机械复读；同一扇门、同一盏灯、同一条雨线，每次出现都应改变压力、距离、归属或情绪温度。
- 整集视觉主轴不是统一滤镜，而是变化链：一个物件、一种材质、一片自然景物或一种动作节奏，在不同场景里承担不同压力，观众才会记住它。
- 终结画面不是"下一集预告"，而是迷你彩蛋尾钩：最后一个环境、道具、情绪或高点余波落点，应让观众感觉下一集已经在门外，但不能告诉观众下一集具体发生什么。
- 尾钩要先判型再写：环境描写式适合压力方向，道具特写式适合未解信息，情绪酝酿式适合关系和选择未尽，高潮结尾式适合代价与余波。
- 终结画面可以是一段尾场小段落，不必压成一两个镜头；意境来自可见物、可听声、可演停顿和空间方向，不来自小说式比喻或抽象评论。
- 下一集可读时只借"关联方向"，不可读时只做 `episode-local inference`；任何具体事件、台词、答案、新角色身份或结果都不该提前进入本集终结画面。
- 对比轴比空泛"高级感"更可靠：明暗、静动、冷暖、空满、近远、整洁与破败、喧闹与寂静，都能让画面有审美张力。
- 氛围不只来自宏观景物（飘雪、落叶），更来自微观感官细节——光线穿过材质后的纹理、空气湿度在皮肤上的触感、声音穿过不同材质的质感差异、时间在静物上留下的痕迹。关键氛围场至少覆盖两个感官通道，不要只写"地点+光线"。
- 声音在意境中的力量常常大于画面。声音的消失比出现更有压力，声音的距离感制造空间感，声音的材质感比类别更重要。写"嘶——沙——"比写"风吹过"更能让观众"听到"那个场景。
- 意境技法的核心是"少即是多"：微观放大用一个极小细节承托巨大情绪，留白用静物状态暗示事件，反衬用温暖承托离别。堆砌三个意象不如精准抓住一个。
- B 路线的价值是补"承托"，不是补"剧情"：环境微细节、群体反应、道具位置、停顿和余波可以新增；对白、桥段、因果、规则和线索不能新增。
- 判断受控新增是否安全，先问"删掉这项后剧情事实是否完全不变"；如果答案是否定的，它就不是 B 路线。
- 判断受控新增是否必要，再问"删掉这项后人物动作链是否更顺"；如果答案是肯定的，该细节不是承托，而是在抢行动线。
- 导演阶段不要把角色留成“等待表演的空人”。关键人物 beat 至少要知道他正在处理哪件场景内小事、被什么压力打断、身体可能先在哪里泄露，以及最后状态落在哪里。
- 多人戏的导演证据先分清行动者和反应者。下游表演需要的是因果焦点，不是每个人同等强度地做表情和小动作。
- 场景身份是导演阶段的源层判断，不是摄影阶段才补的参数。同一个“角色走进房间”，年代明确的审问空间、当代私人房间、旧式居民空间会有不同的规则、声音、材质和光线。
- 声音也有场景身份。用荧光灯嗡鸣、门外闷响、老楼水管声、衣料摩擦这类空间声音，比泛化“紧张 BGM/悲伤音乐”更能给下游稳定基底。
- 执行报告里的创作证据不是官样文章；它防止 skill 只在文档中有创作力，实际输出仍停留在字段整理。
- 思维·执行节点的价值在于"判断后执行、执行后留证、失败能回源层"；凡只列动作、不列判断问题、证据、路由和 gate 的节点，都还只是 checklist。
- 学习资料吸收不能只靠新增 reference；每次把学习成果晋升为合同，都要同时留下真实样例、等价 smoke 或 `static_only` 残余风险说明，避免把静态接入误判为运行稳定。
- references 细则不能只停在说明文档里；每条强制细则都应在 `steps/directing-workflow.md` 中找到 consumed_by 节点、planning evidence、blocking gate 和 route-back，否则执行时会退回泛泛 checklist。
