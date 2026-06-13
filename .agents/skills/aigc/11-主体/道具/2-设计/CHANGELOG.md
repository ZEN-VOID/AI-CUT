# Changelog: aigc 道具 2-设计

## 2026-06-11

- 同步 `3-美学` 输出 scope：道具设计继续读取 `画面基调` 全局 singleton；道具风格按目标道具的 `首次登场` / `episode_id` 优先读取 `3-美学/第N集/道具风格/`，缺失时回退项目级基线。
- 更新 `SKILL.md`、`CONTEXT.md`、README、模板、steps、review 与 reference 合同，要求记录 episode override / fallback。

## 2026-06-04

- 新增 `knowledge-base/prop-design-corpus.md`，作为道具审美、设计细节、文化元素、工艺装饰、使用痕迹、功能结构和 prompt 短语的高质量语料库。
- 强化道具设计吸引力合同：道具必须好看、有设计感、有文化元素和可见细节，不得只是简单功能还原或平凡物件；关键道具必须有可复现 signature detail。
- 新增 `GATE-PROP-DESIGN-13` / `FAIL-PROP-DESIGN-DETAIL-CULTURE` 与 `GATE-PROP-DESIGN-14` / `FAIL-PROP-DESIGN-CORPUS-MISSING`，并同步到 SKILL、templates、references、steps、review、types、slot bundle、workflow supervision、README、agents 入口、scripts 边界和 CONTEXT。
- 明确服饰/器物文化元素式的风格化必须符合项目时代、地域、阶层、职业、宗教/族群禁区与道具功能逻辑，禁止随机贴花或错置现代奢牌、战术、赛博、哥特奇幻等元素。

## 2026-06-01

- 接入 `11-主体` 冻结初始化综合消费：只读 `team.yaml.init_synthesis.stage_seed_summary."11-主体"`、`init_handoff.design_seed` 与 `north_star.yaml.创作阶段不变量.设计`。
- `init_team_synthesis_context` 只承载道具设计节点可执行的约束、启发和风险，不再触发 team 成员身份、旧 stage profile、叶子 persona profile 或伪顾问问答。
- 同步 SKILL、steps、review、references、模板、README、入口元数据、经验层、知识库和脚本边界口径。

## 2026-05-28

- 将固定画面约束从“近景特写”修正为“完整全貌展示”：默认要求 `full-view prop shot`、`full prop in view`、`entire prop fully visible`、`uncropped full silhouette`。
- 同步更新 `SKILL.md`、`CONTEXT.md`、`references/prop-design-contract.md`、`steps/prop-design-workflow.md`、`review/review-contract.md`、模板、README、structured masterprompt 与 `agents/openai.yaml`。
- 新增阻断口径：局部特写、裁切特写、半截道具画面不满足道具 2-设计固定画面要求。

## 2026-05-01

- 将 `references/design-output-contract.md`、`references/design-slot-review-contract.md` 与 `references/workflow-supervision-contract.md` 接入 Reference Loading Guide、steps、review gate 和脚本 resolver，避免输出硬规则和 reviewer slot bundle 漂成旁路文档。
- 补全 `workflow-supervision-contract.md`，要求记录 dispatch / local_checklist / slot bundle findings / merge decision，并阻断空 slot bundle。

## 2026-04-30

- 标准化 Midjourney v8.1 prompt 合同：最终英文整合 prompt 必须覆盖 `## 4. 解构` 的全部有效 Photography 与 Prop Design 信息，控制在 1300 characters 内，使用自然语言负向约束并禁止 `--no` 参数。
- 新增 `prompt_evidence_chain.deconstruction_coverage`，用于说明解构槽位如何进入、合并或被剔除。
- 同步主体 ID 结构规则：`## 4. 解构` 下方必须新增 `主体ID号：<主体ID>`，并与 `## 5. 提示词设计` 主体 ID、英文 prompt 前缀保持一致。
- 强化固定画面约束：`Photography` 必须完整展示道具全貌、仅展示道具本体，不出现人物或背景元素。
- 同步更新英文 prompt / prompt evidence / structured masterprompt，要求包含 `full prop in view`、`prop only`、`no people`、`no background elements`。
- 将上述约束同步到 `SKILL.md`、`references/`、`steps/`、`review/`、模板、README、入口元数据与经验层。

## 2026-04-26

- 升级研究层合同：研究必须形成 `source cue -> confidence -> visual translation -> design lock -> prompt evidence token` 链路。
- 在 `references/`、`steps/`、`types/`、`review/` 与模板中补齐形制、材料、工艺、年代、使用痕迹、功能逻辑、风险/不确定性和 prompt evidence chain 的规则与验收。
- 强化 LLM-first 边界：脚本只能检查研究链字段和 prompt 字符数，不得判断研究置信度或代写创作正文。
- 保持纯色背景单道具 45 度近景约束，并将该约束写入 prompt evidence chain 与 review gate。

## 2026-04-25

- 初始化 Skill 2.0 包结构，补齐 canonical 分区与根文件。
- 建立 `SKILL.md + CONTEXT.md` 成对加载合同、LLM-first 创作边界和 顾问与复核流程 默认执行合同。
- 定义上游 `道具/1-清单` 消费、`north_star.yaml` / `team.yaml` 监制上下文读取、单道具 Markdown 输出路径和 prompt 字符门禁；2026-04-30 已收束为 1300 characters。
- 新增 references、steps、types、review、templates、knowledge-base、scripts、agents 元数据。
- 固定道具设计画面约束为纯色背景单道具近景特写、45 度视角，不置身剧情场景、桌面环境、室内陈设、街景或人物手持情境。
- 补齐工作车间要求的关键 Mermaid 图谱：根执行拓扑、来源汇入、LLM-first 边界、类型分流、审查汇流与 README 可视化入口。
