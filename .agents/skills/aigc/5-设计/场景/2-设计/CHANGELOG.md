# CHANGELOG

## 2026-04-26

- 按 `$skill-工作车间` 精修 `$aigc-scene-design` Skill 2.0 包：在根 `SKILL.md` 补齐入口级 Mermaid 流程图、数据流图和状态图。
- 在 `review/review-contract.md` 增加 reviewer 汇流 Mermaid 图，明确真实 subagent dispatch 受 system / developer / tool / user 优先级约束，阻断时降级为本地 checklist 并报告未启动 reviewer。
- 收束 `references/scene-design-contract.md` 与 `types/scene-design-type-map.md` 中可能误引入人物、人流或人物动线的措辞，保持纯空镜输出合同一致。

## 2026-04-25

- 初始化 `$aigc-scene-design` Skill 2.0 包结构。
- 补齐 `SKILL.md`、`CONTEXT.md`、`README.md`、`agents/openai.yaml` 与 canonical 分区。
- 建立上游场景清单消费合同、项目 `north_star.yaml` / `team.yaml` 读取合同、LLM-first 创作边界、subagents/reviewer 降级口径和单场景设计稿输出模板。
- 固定场景设计画面约束为纯空镜：不出现人物、人体局部、剪影、倒影或人群，并要求 prompt 明确包含 no people / no human figures。
