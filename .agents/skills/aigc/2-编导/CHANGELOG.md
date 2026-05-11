# CHANGELOG

## 2026-05-07

- 增补内心独白人称规则：`内心独白（主角）` 承接第三人称小说叙述时，主角自指必须转为第一人称心声；`内心独白画面` 保留第三人称可拍描述。同步更新 `SKILL.md`、`psychological-reaction-contract.md`、`novel-to-screen-language-contract.md`、`review-contract.md` 与 `CONTEXT.md`。
- 整合主角内心与动作客观化规则：主角内心想法、内心独白和主角视角下对他人行为的判断必须保留为 `内心独白（主角）` 或可感知反应；`角色动作` / `动作画面` 只写镜头可实拍的客观动作、神态、语气和生理反应，禁止“试图、想要、打算、意图”等主观预判词。
- 强化小说转影视边界：直接情绪感受必须转为微表情、肢体动作、生理反应或主角内心独白；抽象概括、往日常态总结和无关人物过往/物品来历/回忆性补充不得进入 canonical 编导稿。
- 同步更新 `SKILL.md`、`psychological-reaction`、`novel-to-screen`、`field-routing`、`performance craft`、workflow、review、模板、CONTEXT、脚本 README 与 validator，新增 `protagonist_inner_voice_evidence`、`objective_action_purity_evidence`、`protagonist_pov_judgment_map`、`habitual_summary_risk_map` 和 `backstory_expansion_risk_map`。
- 重定义 `心理反应` 字段：不再作为抽象内心解释容器，必须落实为演员可表演、观众可从画面或声音 GET 到的身体、表情、呼吸、停顿、声线、道具或空间反应。
- 同步更新 field-routing、workflow、review、模板、CONTEXT、README、类型图与 validator，新增 `psychological_reaction_getability_map`，并把 `心理反应` 纳入具像化/可感知化门禁。
- 新增 `references/psychological-reaction-contract.md`，将 `心理反应` 升格为独立细则：定义 source scope、GETability 标准、projection ladder、actor performance model、field selection matrix、`psychological_reaction_evidence` 和 review checklist；`field-routing` 只保留入口锚点，避免重复真源。
- 新增 `references/episode-final-image-contract.md`，将每集“终结画面”升格为 `2-编导` 的 references 细则：定位为迷你彩蛋尾钩，要求关联下一集但不剧透，并从本集最后的剧情、情绪、视觉母题、道具状态或高点余波丝滑顺延。
- 新增 `types/episode-final-image-type-map.md`，为终结画面提供类型化匹配：按下一集可读状态、结尾锚点表层、尾钩承诺、剧透风险、连续方式选择环境描写式、道具特写式、情绪酝酿式或高潮结尾式。
- 在 workflow 中新增 `N4.10-FINAL-IMAGE` 与 `episode_final_image_plan`，位于 `N4.9-AESTHETIC` 与 `N5-DRAFT` 之间；终结画面证据写入执行报告，正文只落入既有字段，不新增 `终结画面` 正文字段。
- review 新增 `GATE-DIRECT-26 / FAIL-EPISODE-FINAL-IMAGE`，阻断缺少尾钩、硬塞预告、剧透下一集、未类型化匹配或无法从本集内容自然顺延的编导稿。

## 2026-05-06

- 收紧字段纯度：`环境描写` 明确只写场景本身的写景画面，人物动作、对白引出、剧情结果、心理解释和关系结论必须拆入 `角色动作`、`对白画面`、`群像画面`、`道具特写` 或紧贴 beat 的调度字段。
- 新增占位泄露门禁：终稿字段正文不得出现“本场按上游原文顺序承接...”“说话者的视线...”“不新增事件结果”“引号内不加入动作”等内部任务说明、模板占位句或规则复述。
- 同步更新 `field-routing`、`script-adaptation`、`performance craft`、workflow、review gate、模板、CONTEXT、README 与 validator；新增 `GATE-DIRECT-20/21` 和 `placeholder_leak_risk_map / environment_purity_map`。
- 扩展 `validate_script_projection.py`，机械拦截占位句泄露和明显环境/动作混写，避免类似 `浪花传说之琉球篇/2-编导/第1集.md` 的错误进入下游。
- 将 `环境描写` 的定义从具体物件例子改为类型化维度：空间结构、自然条件、空气介质、光照状态、承载面、围护面、开口边界、静置物件和整体氛围。
- 强化 `角色动作` / `动作画面`：动作字段必要时必须体现速度感、节奏、停顿和力度，保留上游“一闪、缓缓、忽然、挣出、扑倒”等动作信号。
- 将 `道具特写` 从具体物件例子改为功能维度：信息载体、规则显影物、关键物件、线索痕迹、归属关系和状态变化；禁止写成心理解释、推理结论或新增功能。
- 新增 `环境氛围增强`：`环境描写` 可用飘雪、落叶、朝露、风沙、雨丝、雾气、日影等自然景物衬托心境和情绪；若上游未明写，按 B 路线留证，不得新增事件、线索、阻碍、因果或结果。
- 新增 `references/visual-aesthetic-contract.md`：把画面美学独立为核心画面、视觉气质、母题变化、对比轴、景境氛围、节奏和留白取舍；同步新增 `N4.9-AESTHETIC`、`PASS-DIRECT-08A`、`FIELD-DIRECT-15` 与 `GATE-DIRECT-23`。
- 收紧并放宽对白标签：终稿必须使用 `对白（真实角色名，语态/状态短语）`，例如 `对白（阿真，眼里带笑）`；第二项不强制一词或“地”字尾，重点呈现灵动、自然、鲜活的角色状态；`原文角色`、`角色名`、`某人` 等模板占位不得进入输出。
- 强化整集级画面创作力：新增 `references/episode-visual-spine-contract.md` 管理 `episode_visual_spine`，要求先建立整集视觉问题、母题链、材质/色彩弧、节奏曲线、呼应目标和克制规则，再进入单场 `visual-aesthetic`；review 新增 `GATE-DIRECT-24` 检查小说转译、`director_substance_evidence` 与视觉美学证据。
- 新增 `references/novel-to-screen-language-contract.md`：把小说作者评论、心理内视、比喻象征、概括叙述、背景说明、因果解释和关系结论统一纳入 `novel_expression_transform_pass`；同步新增 `N4.2-NOVEL-TRANSFORM`、`PASS-DIRECT-03A`、`FIELD-DIRECT-17` 与 `GATE-DIRECT-25`，并明确台词只冻结不润色，二次加工只发生在台词外的声画、表演和空间承托。
- 进一步明确 `环境描写` 可在同一 slugline 内重复出现：开篇环境建立场景，后续因室内外边界、角落、门廊、窗边、船舷、背景层次、光线、空气或材质焦点变化可追加环境刷新；同步更新 field-routing、visual-aesthetic、workflow、review、模板与 CONTEXT。

## 2026-05-03

- 调整 `2-编导` subagents 机制：监制顾问不再围绕固定问题字段发言，而是同步于当前 `steps/directing-workflow.md`、`Thought Pass Map` 与 review gate 的思维·执行节点。
- `advisor_consultation_packet` 现在要求保留 `node_ref / pass_ref / gate_ref / role_lens` 来源锚点，确保顾问参谋体现角色意识、创作风格和专业水准，并转化为节点级判断、执行取舍、证据补强与风险提示。
- 同步更新 workflow、review gate、CONTEXT 经验层与共享团队顾问合同，阻断脱离节点网络的固定题型清单和泛泛审美评价。
- 修复 review 反馈：共享顾问合同的 `2-编导` 行改为节点派生；`N4.6-ADVISOR` 增加 `advisor_routeback_targets`，允许回修 `N3-SCENE` / `N4-FIELD` / `N4.5-PEAK`；review 报告和输出模板补齐顾问 packet 的节点锚点、routeback 与降级证据。
- 新增 `references/directorial-authorship-contract.md` 与 `N4.4-DIRECTORIAL`，把“优秀编导”的要求落为 `director_substance_pass`：从上游原文提炼戏剧问题、人物选择压力、观众位置、信息释放和可拍执行策略，避免只交付结构正确或表达漂亮的稿件。
- 升级 `steps/directing-workflow.md`：新增 `Reference-To-Node Coverage`，把各 references 细则映射到具体节点证据和 blocking gate；扩展 `N4-FIELD / N4.4-DIRECTORIAL / N4.7-CRAFT / N4.8-ENRICH / N6-REVIEW` 的 evidence 与回退口径，并重绘主流程 Mermaid 与 reference coverage Mermaid。

## 2026-05-01

- 新增 `references/performance-and-scene-craft-contract.md`，补齐场景状态差、潜台词行为、演员任务、场面调度、沉默反应和摄影越权边界。
- 在 workflow 中新增 `N4.7-CRAFT`，将高质量影视剧作与演员可执行表演技法前置为 LLM 草稿前的 `scene_dramatic_map / performance_task_map / blocking_power_map`。
- 同步更新 `SKILL.md`、review gate、模板、validator、CONTEXT 与知识库，要求心理、潜台词、权力关系和沉默反应必须转成可见/可听/可执行证据，不得新增对白或写摄影方案。
- 新增 `references/controlled-enrichment-contract.md`，将“新增式”限定为 B 路线 `controlled_enrichment`：只允许非剧情性承托新增，并要求 `controlled_enrichment_ledger` 留证；新增对白、桥段、因果、规则和线索仍需另行授权为候选稿。
- 在 workflow 中新增 `N4.8-ENRICH`，位于 `N4.7-CRAFT` 与 `N5-DRAFT` 之间，负责判断受控增强是否必要、是否有上游锚点、是否越过剧情边界。
- 新增“表演/调度内嵌”规则：`表演提示`、`场面调度` 不得在场景或分镜组末尾总结式列出，必须拆入对应剧本句段；review 新增 `FAIL-PERFORMANCE-SUMMARY-BLOCK`。

## 2026-04-30

- 明确 `2-编导` 启动 subagents 模式时的执行机制：以项目 `team.yaml` 中明确的监制组相关智能顾问团作为编导监制。
- 新增 `Subagents Execution Mechanism`，要求顾问代入专业视角和个人风格，对已知上下文提出编导方向参谋指导，并由主 agent 汇流为 `advisor_consultation_packet`。
- 在 workflow 中新增 `N4.6-ADVISOR`，将顾问参谋沉淀为 LLM 剧本化投影、阶段内修复和复审的后续上下文。
- 同步更新 review gate 与 CONTEXT 经验层，阻断“泛泛顾问意见”“本地模拟顾问”和“顾问意见越权改写上游真源”。

## 2026-04-29

- 新增阶段末 `Stage-End Review-Repair Contract`，将候选编导稿固定为 `candidate -> review -> direct repair -> re-review -> canonical writeback` 闭环。
- 在 workflow 中新增 `N6R-DIRECT-REPAIR` 与 `N6R-REVIEW-AGAIN`，要求 review 阻断项在 `2-编导` 阶段内最小修复并复审后才能交给下游。
- 更新 review gate、CONTEXT 和执行报告字段，明确保真、对白、声画、slugline、具像化和高点承托问题不得降级为交付后 followup。

## 2026-04-28

- 新增 `references/climax-visual-treatment-contract.md`，将 `story/2-卷章/3-章级` 的爽点设计思想投影为 `2-编导` 的高潮画面处理机制。
- 在 workflow 中新增 `N4.5-PEAK` / `peak_visual_pass`，要求从上游逐集正文识别 1-3 个高点或最强 `micro_payoff`，并落实为既有画面、声音、表演字段。
- 在 review gate 中新增 `FAIL-PEAK-VISUAL`，检查高点可回指、可拍承托、状态差/余波与不新增事实。
- 同步更新模板、README、CONTEXT 与 frontmatter policy，明确高潮强化不得新增剧情事实、对白或因果。

## 2026-04-25

- 初始化 `aigc/2-编导` Skill 2.0 包。
- 固定上游为 `projects/aigc/<项目名>/1-分集/第N集.md`，下游为 `projects/aigc/<项目名>/2-编导/第N集.md`。
- 新增忠实剧本化投影、对白冻结、声画配对、slugline 稳定和好莱坞级质量规范。
- 新增机械校验脚本 `scripts/validate_script_projection.py`；脚本只做结构与字段检查，不替代 LLM 主创。
- 强化“剧本化 = 可见 / 可听 / 可执行”源层定义，新增具像化、画面化、反抽象、反概念、反比喻门禁。
- 强化声音本体规则：`音效` 字段只写可听声音，不写时间说明、事件概括或描述性句子。
- 扩展 `validate_script_projection.py`，开始检查高频抽象画面词与描述性音效词。
- 移除 `分镜明细预设` 字段，避免 `2-编导` 越权到下游摄影/分镜；相关意图必须转化为可见画面、动作、表演或声音字段。
