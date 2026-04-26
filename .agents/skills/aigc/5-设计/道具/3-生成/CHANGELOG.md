# Changelog: aigc 道具 3-生成

## 2026-04-26

- 升级 `templates/prop-multiview-prompt.json` 到 v1.2，增加顶左主体身份牌与短 ASCII ID / 后期叠字 fallback 合同。
- 升级 `templates/prop-multiview-prompt.json` 到 v1.1，增加主体不变量、参考图策略、功能视图计划、漂移控制和审查焦点。
- 对照 `$skill-工作车间` 补齐根 `SKILL.md` 的 Mermaid Visual Maps、目录 owner、节点交接和失败路由表。
- 强化 `steps/prop-generation-workflow.md` 的 Business Requirement Analysis、混合拓扑图、sequence 图、节点 schema、分支与失败回路。
- 强化 `types/prop-generation-type-map.md` 的类型变量、路由图和 route-to-step 映射。
- 强化 `review/review-contract.md` 的默认 provider、真实 reviewer subagent 降级矩阵、review flow 与 verdict schema。
- 补齐 `templates/output-template.md` 的 subagent 降级记录和 review verdict 字段，并更新 README 质量入口。
- 将“结构校验通过但拓扑表达不足”的可复用经验沉淀到 `CONTEXT.md`。

## 2026-04-25

- 初始化 Skill 2.0 包结构。
- 建立 `SKILL.md + CONTEXT.md` 入口与经验层。
- 增加 references、steps、review、types、knowledge-base、templates、scripts、agents 分区。
- 将旧道具面板模板语义重构为当前道具生成阶段的多视图主体设计图 JSON 模板。
- 补齐 `knowledge-base/` 动态引用与 OpenAI 入口短描述长度门禁。
