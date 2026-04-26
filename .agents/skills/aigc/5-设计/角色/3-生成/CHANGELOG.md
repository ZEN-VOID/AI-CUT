# Changelog: aigc 5-设计/角色/3-生成

## 2026-04-26

- 补齐入口 `SKILL.md` 的 Mermaid Visual Maps，覆盖执行拓扑、证据链和状态流。
- 强化 `steps/character-generation-workflow.md` 的 subagent/本地降级汇流图、失败恢复图和 worker 返回形状。
- 补充 `review/review-contract.md` 的本地降级 checklist 与 review flow map，避免 reviewer subagent 被阻断时缺少可执行复核路径。
- 更新 `README.md`，显式标注 Visual Governance 的分区落点。

## 2026-04-25

- 初始化 Skill 2.0 包结构。
- 建立 `SKILL.md + CONTEXT.md` 入口与经验层。
- 新增角色生成业务合同、思行 workflow、类型矩阵、review gate、模板、脚本边界和 OpenAI 入口元数据。
- 将旧角色面板 prompt 模板重构为当前阶段的 `character-multiview-prompt-template.json`，明确设计文档 `提示词设计` 为主体真源。
