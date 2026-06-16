# Changelog

## 2026-06-16

- 将“主角和大反派一定要有魅力”升格为来源匹配审美硬门槛：新增 `charisma_floor` 槽位，要求主角、核心情感线角色、长期复用角色、大反派、主要对抗者、长线威胁和终局 Boss 必须具备 `charisma_floor=high` 的可见镜头魅力证据。
- 同步 `SKILL.md`、types、templates、references、review、slot bundle resolver、知识库、README 与入口元数据；普通配角/功能角色仍可按“个性化魅力或清晰可识别度”验收，避免把魅力门槛误写成默认美化、帅化、成人化或性化。
- 复查并修订同类默认误导：将“女性默认美丽、男性默认英俊、主角强化颜值”改为 `Source-Fit Aesthetic Target`，审美路线按清单证据、年龄、性别/性别表达、身份、物种/族群、项目调性和角色权重裁决。
- 将真实人物 / 明星脸灵感改为默认 `none/generic_only`；只有用户或项目明确允许且有必要时才可原创转译，禁止默认使用真实人物参考。
- 将服装 `磨损 / 使用痕迹 / Wear / Aging` 改为 `服装状态 / 维护状态 / 穿着状态` 下的条件子类，禁止无依据默认做旧、污损、补丁或破洞。

## 2026-06-11

- 同步 `2-美学` 输出 scope：角色设计继续读取 `画面基调` 全局 singleton；角色风格按目标角色的 `首次登场` / `episode_id` 优先读取 `2-美学/第N集/角色风格/`，缺失时回退项目级基线。
- 更新 `SKILL.md`、`CONTEXT.md`、模板、steps、review 与 reference 合同，要求记录 episode override / fallback。

## 2026-06-04

- 强化角色审美吸引力合同：角色设计不得只做手术式关键词还原，必须让容貌、妆发、骨相、身形和服装具备美感与个性魅力。
- 新增 `Aesthetic Appeal Evidence`、`Beauty / Handsomeness Target`、`Face / Bone Aesthetic`、`Costume Appeal Strategy`、可选 `Celebrity Face Inspiration`，并要求明星脸灵感原创转译，不得精确复刻现实人物。
- 将 `GATE-CHAR-DESIGN-19` / `FAIL-CHAR-DESIGN-AESTHETIC-APPEAL` 接入 SKILL、references、steps、review、templates、slot bundle、workflow supervision、types、README、入口元数据和经验层。
- 新增 `knowledge-base/character-design-corpus.md` 作为高质量角色设计语料库，覆盖男主、女主、反派、书生、武将、少年、成熟角色、平民等角色类型，以及妆容化处理和服装时代语境护栏。
- 将语料库接入 `Module Trigger Matrix`、Reference Loading Guide、Execution Contract、review gate、steps、templates、slot bundle、workflow supervision、README 和入口元数据；新增 `GATE-CHAR-DESIGN-20` / `FAIL-CHAR-DESIGN-CORPUS-MISSING`。

## 2026-06-16

- 升级为 runtime-spine Skill 2.0 口径，补齐业务分析、类型路由、思行节点、模块触发、汇流门、review gate、量化标准、注意力协议、检查点和测试 prompts。
- 将历史 workflow 文件迁移为 `references/legacy-character-design-workflow.md`，保留旧语义但不再作为第二执行主链。
- 强化创作作者性门禁：研究、物语、解构、服装、摄影和英文提示词必须由 LLM 逐角色理解后落盘，脚本和模板不得批量生成、批量插入、正则套句或映射投影正文。

## 2026-06-01

- 接入 `3-主体` 冻结初始化综合消费：只读 `team.yaml.init_synthesis.stage_seed_summary."3-主体"`、`init_handoff.design_seed` 与 `north_star.yaml.创作阶段不变量.设计`。
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
- 同步更新 `references/`、历史 workflow、`types/`、`review/` 与 `templates/`，把 `evidence -> design decision -> prompt phrase` 作为角色 prompt 的验收链路。
- 强化 LLM-first 与脚本边界：脚本只能检查研究层标题、字符数和空字段，不得生成研究或 prompt 证据链正文。
- 补强根 `SKILL.md` 的 Skill 2.0 Visual Maps：入口流程、汇流关系和状态流转。
- 为 `types/character-design-type-map.md` 增加类型分流 Mermaid 路由图。
- 为 `review/review-contract.md` 增加审查闭环 Mermaid 门禁图。
- 为 `README.md` 增加快速流程快照，便于入口层理解。
- 在 `CONTEXT.md` 沉淀批量定制后需人工检查关键图表的经验。

## 2026-04-25

- 初始化 `角色/2-设计` Skill 2.0 包。
- 补齐 canonical 分区：`references/`、`scripts/`、`templates/`、`review/`、历史 workflow、`knowledge-base/`、`types/`、`agents/`。
- 建立从 `角色/1-清单` 到单角色细目设计稿的输入/输出合同。
- 声明 LLM-first 创作边界、默认 顾问与复核流程 调度合同和网络搜索允许条件。
- 固定角色设计画面约束为纯色背景全身定妆照，不置身剧情场景、建筑空间、街景、室内陈设或复杂环境。
