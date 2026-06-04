# Changelog

## 2026-06-04

- 强化角色审美吸引力合同：角色设计不得只做手术式关键词还原，必须让容貌、妆发、骨相、身形和服装具备美感与个性魅力。
- 新增 `Aesthetic Appeal Evidence`、`Beauty / Handsomeness Target`、`Face / Bone Aesthetic`、`Costume Appeal Strategy`、可选 `Celebrity Face Inspiration`，并要求明星脸灵感原创转译，不得精确复刻现实人物。
- 将 `GATE-CHAR-DESIGN-19` / `FAIL-CHAR-DESIGN-AESTHETIC-APPEAL` 接入 SKILL、references、steps、review、templates、slot bundle、workflow supervision、types、README、入口元数据和经验层。
- 新增 `knowledge-base/character-design-corpus.md` 作为高质量角色设计语料库，覆盖男主、女主、反派、书生、武将、少年、成熟角色、平民等角色类型，以及妆容化处理和服装时代语境护栏。
- 将语料库接入 `Module Trigger Matrix`、Reference Loading Guide、Execution Contract、review gate、steps、templates、slot bundle、workflow supervision、README 和入口元数据；新增 `GATE-CHAR-DESIGN-20` / `FAIL-CHAR-DESIGN-CORPUS-MISSING`。

## 2026-06-01

- 接入 `11-主体` 冻结初始化综合消费：只读 `team.yaml.init_synthesis.stage_seed_summary."11-主体"`、`init_handoff.design_seed` 与 `north_star.yaml.创作阶段不变量.设计`。
- `init_team_synthesis_context` 只承载角色设计节点可执行的约束、启发和风险，不再触发 team 成员身份、旧 stage profile、叶子 persona profile 或伪顾问问答。
- 同步 SKILL、steps、review、references、模板、README、入口元数据、经验层与知识库口径。

## 2026-05-01

- 将 `references/design-output-contract.md`、`references/design-slot-review-contract.md` 与 `references/workflow-supervision-contract.md` 接入 Reference Loading Guide、steps、review gate 和脚本 resolver，避免输出硬规则和 reviewer slot bundle 漂成旁路文档。
- 补全 `workflow-supervision-contract.md`，要求记录 dispatch / local_checklist / slot bundle findings / merge decision，并阻断空 slot bundle。

## 2026-04-30

- 标准化 Midjourney v8.1 prompt 合同：最终英文整合 prompt 必须覆盖 `## 4. 解构` 的全部有效身份、外观、服装、姿态和摄影信息，控制在 1300 characters 内，使用自然语言负向约束并禁止 `--no` 参数。
- 新增 `prompt_evidence_chain.deconstruction_coverage`，用于说明解构槽位如何进入、合并或被剔除。
- 同步主体 ID 结构规则：`## 4. 解构` 下方必须新增 `主体ID号：<主体ID>`。
- 将该 ID 与 `## 5. 提示词设计` 主体 ID、英文 prompt 前缀的一致性写入 `SKILL.md`、模板、references、steps、review、README、入口元数据与经验层。

## 2026-04-26

- 升级研究层合同：研究必须转化为基础研究镜头、禁区、不确定性和 prompt evidence chain。
- 同步更新 `references/`、`steps/`、`types/`、`review/` 与 `templates/`，把 `evidence -> design decision -> prompt phrase` 作为角色 prompt 的验收链路。
- 强化 LLM-first 与脚本边界：脚本只能检查研究层标题、字符数和空字段，不得生成研究或 prompt 证据链正文。
- 补强根 `SKILL.md` 的 Skill 2.0 Visual Maps：入口流程、汇流关系和状态流转。
- 为 `types/character-design-type-map.md` 增加类型分流 Mermaid 路由图。
- 为 `review/review-contract.md` 增加审查闭环 Mermaid 门禁图。
- 为 `README.md` 增加快速流程快照，便于入口层理解。
- 在 `CONTEXT.md` 沉淀批量定制后需人工检查关键图表的经验。

## 2026-04-25

- 初始化 `角色/2-设计` Skill 2.0 包。
- 补齐 canonical 分区：`references/`、`scripts/`、`templates/`、`review/`、`steps/`、`knowledge-base/`、`types/`、`agents/`。
- 建立从 `角色/1-清单` 到单角色细目设计稿的输入/输出合同。
- 声明 LLM-first 创作边界、默认 顾问与复核流程 调度合同和网络搜索允许条件。
- 固定角色设计画面约束为纯色背景全身定妆照，不置身剧情场景、建筑空间、街景、室内陈设或复杂环境。
