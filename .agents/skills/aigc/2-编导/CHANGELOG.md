# CHANGELOG

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
