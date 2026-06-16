# Changelog: aigc 道具 3-生成

## 2026-06-16

- 将 `SKILL.md` 升级为 runtime-spine Skill 2.0 口径，补齐 Core Task、Business Requirement Analysis、Type Routing、Thinking-Action Node Map、Module Loading/Trigger、Convergence、Review Gate、Quantifiable Criteria、Attention、Checkpoint、Output 和 Learning 控制块。
- 新增 `test-prompts.json`，覆盖单道具生成、prompt-only、reference repair 和模板化 prompt 拒绝场景。
- 将 `SKILL.md 的 Thinking-Action Node Map` 明确降为 legacy read-only reference，运行时节点真源收回 `SKILL.md`。
- 强化默认 imagegen 执行器边界、`4. 解构` prompt 真源、主图 `view_image` 后作为多视图参照和 JSON/prompt 反模板伪差异门禁。

## 2026-05-01

- 将生成资产命名合同调整为 `<主体ID>-<主体名称>-主图/多视图`，并要求 JSON 记录 `subject_id` 与 `subject_id_source`。
- 强化主图到多视图的本地参照图规则：Step2 使用本地主图作为 reference image 时，必须先 `view_image` 进入对话上下文，并在 JSON / 报告记录 `reference_context_status`。

## 2026-04-30

- 调整主图与多视图 prompt 模板：导入给 gpt-image-2 的源引用统一改为上游设计文档 `4. 解构`，不再以旧英文整合 prompt 为主源。

## 2026-04-26

- 收紧默认图像执行入口：除非用户显式要求其他 provider / API / model，`道具/3-生成` 只能通过 `.agents/skills/cli/imagegen` 执行，不得直接路由到 nano-banana / Dreamina / AnyFast 子技能。
- 升级 `templates/prop-multiview-prompt.json` 到 v1.2，增加顶左主体身份牌与短 ASCII ID / 后期叠字 fallback 合同。
- 升级 `templates/prop-multiview-prompt.json` 到 v1.1，增加主体不变量、参考图策略、功能视图计划、漂移控制和审查焦点。
- 对照 `$skill-工作车间` 补齐根 `SKILL.md` 的 Mermaid Visual Maps、目录 owner、节点交接和失败路由表。
- 强化 `SKILL.md 的 Thinking-Action Node Map` 的 Business Requirement Analysis、混合拓扑图、sequence 图、节点 schema、分支与失败回路。
- 强化 `types/prop-generation-type-map.md` 的类型变量、路由图和 route-to-step 映射。
- 强化 `review/review-contract.md` 的默认 provider、外部 reviewer provider、本地 checklist、review flow 与 verdict schema。
- 补齐 `templates/output-template.md` 的 顾问与复核流程 降级记录和 review verdict 字段，并更新 README 质量入口。
- 将“结构校验通过但拓扑表达不足”的可复用经验沉淀到 `CONTEXT.md`。

## 2026-04-25

- 初始化 Skill 2.0 包结构。
- 建立 `SKILL.md + CONTEXT.md` 入口与经验层。
- 增加 references、steps、review、types、knowledge-base、templates、scripts、agents 分区。
- 将旧道具面板模板语义重构为当前道具生成阶段的多视图主体设计图 JSON 模板。
- 补齐 `knowledge-base/` 动态引用与 OpenAI 入口短描述长度门禁。
