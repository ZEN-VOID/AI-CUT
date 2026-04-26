# CHANGELOG

## 2026-04-26

- 补齐 `SKILL.md` 的 `Visual Maps`，覆盖入口流、来源到输出的数据流和状态机。
- 增强 `steps/scene-list-workflow.md`，加入业务需求分析、Mermaid hybrid topology、完整 node handoff schema 与 failure routes。
- 增强 `types/scene-type-map.md`，加入类型变量、Mermaid decision flow 与类型路由矩阵。
- 增强 `review/review-contract.md`，加入 review Mermaid 回路、finding schema 与 severity routing。
- 增强 `references/source-and-merge-contract.md` 的来源信任图，并在 `README.md` 标注关键拓扑入口。
- 将“结构合格但缺少可视拓扑”的批量生成风险沉淀到 `CONTEXT.md`。

## 2026-04-25

- 初始化 `$aigc-scene-list` Skill 2.0 包结构。
- 建立 `SKILL.md + CONTEXT.md` 入口与经验层。
- 补齐 `references/`、`steps/`、`review/`、`types/`、`knowledge-base/`、`templates/`、`scripts/`、`agents/` 分区。
- 固定上游真源为 `4-分组/第N集.md` 组底 YAML 的 `场景` 字段，输出真源为 `5-设计/场景/1-清单/场景清单.md`。
