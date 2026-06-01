# Changelog: aigc 6-设计/角色/3-生成

## 2026-05-01

- 将生成资产命名合同调整为 `<主体ID>-<主体名称>-主图/多视图`，并要求 JSON 记录 `subject_id` 与 `subject_id_source`。
- 强化主图到多视图的本地参照图规则：Step2 使用本地主图作为 reference image 时，必须先 `view_image` 进入对话上下文，并在 JSON / 报告记录 `reference_context_status`。

## 2026-04-30

- 调整主图与多视图 prompt 模板：导入给 gpt-image-2 的源引用统一改为上游设计文档 `4. 解构`，不再以旧英文整合 prompt 为主源。

## 2026-04-26

- 升级 `templates/character-multiview-prompt-template.json` 到 v1.2，增加顶左主体身份牌与短 ASCII ID / 后期叠字 fallback 合同。
- 升级 `templates/character-multiview-prompt-template.json` 到 v1.1，增加角色主体不变量、turnaround 视图计划、参考图策略、漂移控制和审查焦点。
- 补齐入口 `SKILL.md` 的 Mermaid Visual Maps，覆盖执行拓扑、证据链和状态流。
- 强化 `steps/character-generation-workflow.md` 的 顾问与复核流程/本地 checklist 汇流图、失败恢复图和 worker 返回形状。
- 补充 `review/review-contract.md` 的本地 checklist 与 review flow map，避免 reviewer provider 被不可用时缺少可执行复核路径。
- 更新 `README.md`，显式标注 Visual Governance 的分区落点。

## 2026-04-25

- 初始化 Skill 2.0 包结构。
- 建立 `SKILL.md + CONTEXT.md` 入口与经验层。
- 新增角色生成业务合同、思行 workflow、类型矩阵、review gate、模板、脚本边界和 OpenAI 入口元数据。
- 将旧角色面板 prompt 模板重构为当前阶段的 `character-multiview-prompt-template.json`，当时明确设计文档英文整合 prompt 为主体真源；该口径已由 2026-04-30 的 `4. 解构` 源引用规则取代。
