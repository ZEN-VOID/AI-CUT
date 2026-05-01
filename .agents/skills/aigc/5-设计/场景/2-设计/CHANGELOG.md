# CHANGELOG

## 2026-04-30

- 强化英文整合 prompt 的覆盖范围：明确整合对象是 `## 4. 解构` 的全部有效 Scene Design 与 Cinematography 信息，而不是只拼接前缀、后缀、风格词、时间地域或纯空镜负向词。
- 强化提示词规则源层：最终英文整合 prompt 必须显式包含时间和地域锚点，并通过 `prompt_evidence_chain` 回指来源姿态、推断或保守化处理。
- 同步更新 `SKILL.md`、`references/scene-design-contract.md`、`templates/`、`review/`、`steps/`、`README.md`、`CONTEXT.md` 与入口元数据，避免只在单个项目输出中临时补词。
- 同步主体 ID 结构规则：`## 4. 解构` 下方必须新增 `主体ID号：<主体ID>`，并与 `## 5. 提示词设计` 主体 ID、英文 prompt 前缀保持一致。

## 2026-04-26

- 升级研究层合同：将“研究考据”扩展为 `research_brief -> source_posture -> uncertainty_register -> visual_translation -> prompt_evidence_chain` 的可追溯闭环。
- 更新 `templates/output-template.md`，增加研究简报 YAML、Prompt Evidence Chain 表格和 review verdict 中的研究层状态字段。
- 更新 `steps/`、`types/`、`review/`、`CONTEXT.md` 与 `scripts/README.md`，把来源姿态、不确定性、视觉翻译和 prompt 证据链纳入执行流、分型和验收门禁，同时保持 LLM-first 与纯空镜约束。
- 按 `$skill-工作车间` 精修 `$aigc-scene-design` Skill 2.0 包：在根 `SKILL.md` 补齐入口级 Mermaid 流程图、数据流图和状态图。
- 在 `review/review-contract.md` 增加 reviewer 汇流 Mermaid 图，明确真实 subagent dispatch 受 system / developer / tool / user 优先级约束，阻断时降级为本地 checklist 并报告未启动 reviewer。
- 收束 `references/scene-design-contract.md` 与 `types/scene-design-type-map.md` 中可能误引入人物、人流或人物动线的措辞，保持纯空镜输出合同一致。

## 2026-04-25

- 初始化 `$aigc-scene-design` Skill 2.0 包结构。
- 补齐 `SKILL.md`、`CONTEXT.md`、`README.md`、`agents/openai.yaml` 与 canonical 分区。
- 建立上游场景清单消费合同、项目 `north_star.yaml` / `team.yaml` 读取合同、LLM-first 创作边界、subagents/reviewer 降级口径和单场景设计稿输出模板。
- 固定场景设计画面约束为纯空镜：不出现人物、人体局部、剪影、倒影或人群，并要求 prompt 明确包含 no people / no human figures。
