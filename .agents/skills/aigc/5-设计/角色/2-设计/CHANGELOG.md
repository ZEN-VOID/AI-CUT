# Changelog

## 2026-04-26

- 升级研究层合同：研究必须转化为身份、职业、阶层、地域年代、服饰工艺、身体姿态、禁区、不确定性和 prompt evidence chain。
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
- 声明 LLM-first 创作边界、默认 subagents 调度合同和网络搜索允许条件。
- 固定角色设计画面约束为纯色背景全身定妆照，不置身剧情场景、建筑空间、街景、室内陈设或复杂环境。
