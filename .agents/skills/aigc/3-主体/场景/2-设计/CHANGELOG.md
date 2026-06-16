# CHANGELOG

## 2026-06-16

- 升级 `$aigc-scene-design` 到 runtime-spine Skill 2.0 口径，补齐必需控制块和可执行表格。
- 保留既有研究层、初始化综合、反抽象、纯空镜和 prompt evidence chain 语义，并将 workflow 节点迁入主 `SKILL.md`。
- 新增 `test-prompts.json`，覆盖单场景设计、增量补缺和纯空镜 prompt repair。
- 收束时间/地域/空间风格显式 token 规则：要求有来源姿态或保守推断，不得为了字段完整而编造具体年代、地点、族群、宗教、建筑流派或建筑大师名。
- 将 `space_style_token` 纳入模板、slot bundle、resolver、review gate 和入口提示；建筑/室内/街区可走建筑风格，自然、超现实、交通或抽象空间必须改用地理/生态/材质/变形/路径逻辑，避免非建筑场景被强行建筑化。

## 2026-06-11

- 同步 `2-美学` 输出 scope：场景设计继续读取 `画面基调` 全局 singleton；场景风格按目标场景的 `首次登场` / `episode_id` 优先读取 `2-美学/第N集/场景风格/`，缺失时回退项目级基线。
- 更新 `SKILL.md`、`CONTEXT.md`、模板、steps 与 reference 合同，要求记录 episode override / fallback。

## 2026-06-01

- 接入 `3-主体` 冻结初始化综合消费：只读 `team.yaml.init_synthesis.stage_seed_summary."3-主体"`、`init_handoff.design_seed` 与 `north_star.yaml.创作阶段不变量.设计`。
- `init_team_synthesis_context` 只承载场景设计节点可执行的约束、启发和风险，不再触发 team 成员身份、旧 stage profile、叶子 persona profile 或伪顾问问答。
- 同步 SKILL、steps、review、references、模板、README、入口元数据、经验层与知识库口径。

## 2026-05-01

- 将 `references/design-output-contract.md`、`references/design-slot-review-contract.md` 与 `references/workflow-supervision-contract.md` 接入 Reference Loading Guide、steps、review gate 和脚本 resolver，避免输出硬规则和 reviewer slot bundle 漂成旁路文档。
- 补全 `workflow-supervision-contract.md`，要求记录 dispatch / local_checklist / slot bundle findings / merge decision，并阻断空 slot bundle。

## 2026-04-30

- 强化英文整合 prompt 的覆盖范围：明确整合对象是 `## 4. 解构` 的全部有效 Scene Design 与 Cinematography 信息，而不是只拼接前缀、后缀、风格词、时间地域或纯空镜负向词。
- 强化提示词规则源层：最终英文整合 prompt 必须显式包含时间和地域锚点，并通过 `prompt_evidence_chain` 回指来源姿态、推断或保守化处理。
- 同步更新 `SKILL.md`、`references/scene-design-contract.md`、`templates/`、`review/`、`SKILL.md` runtime spine、`README.md`、`CONTEXT.md` 与入口元数据，避免只在单个项目输出中临时补词。
- 同步主体 ID 结构规则：`## 4. 解构` 下方必须新增 `主体ID号：<主体ID>`，并与 `## 5. 提示词设计` 主体 ID、英文 prompt 前缀保持一致。

## 2026-04-26

- 升级研究层合同：将“研究考据”扩展为 `research_brief -> source_posture -> uncertainty_register -> visual_translation -> prompt_evidence_chain` 的可追溯闭环。
- 更新 `templates/output-template.md`，增加研究简报 YAML、Prompt Evidence Chain 表格和 review verdict 中的研究层状态字段。
- 更新 `SKILL.md` runtime spine、`types/`、`review/`、`CONTEXT.md` 与 `scripts/README.md`，把来源姿态、不确定性、视觉翻译和 prompt 证据链纳入执行流、分型和验收门禁，同时保持 LLM-first 与纯空镜约束。
- 按 `$skill-工作车间` 精修 `$aigc-scene-design` Skill 2.0 包：在根 `SKILL.md` 补齐入口级 Mermaid 流程图、数据流图和状态图。
- 在 `review/review-contract.md` 增加 reviewer 汇流 Mermaid 图，明确外部顾问与复核 provider 调度 受 system / developer / tool / user 优先级约束，不可用时直接使用本地 checklist。
- 收束 `references/scene-design-contract.md` 与 `types/scene-design-type-map.md` 中可能误引入人物、人流或人物动线的措辞，保持纯空镜输出合同一致。

## 2026-04-25

- 初始化 `$aigc-scene-design` Skill 2.0 包结构。
- 补齐 `SKILL.md`、`CONTEXT.md`、`README.md`、`agents/openai.yaml` 与 canonical 分区。
- 建立上游场景清单消费合同、项目 `north_star.yaml` / `team.yaml` 读取合同、LLM-first 创作边界、顾问/reviewer 与本地 checklist 口径和单场景设计稿输出模板。
- 固定场景设计画面约束为纯空镜：不出现人物、人体局部、剪影、倒影或人群，并要求 prompt 明确包含 no people / no human figures。
