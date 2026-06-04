# CHANGELOG

## 2026-06-04

- 按 `skill-2.0` runtime-spine 最新规范升级：在 `SKILL.md` 补齐 Runtime Spine、Business Requirement Analysis、Type Routing、Thinking-Action Node Map、Module Loading / Trigger、Convergence、Review Gate Binding、Quantifiable Criteria、Attention、Checkpoint、Evaluation Prompt 与 Learning Writeback 合同。
- 删除旧 workflow 第二执行链，将学习节点、Mermaid 拓扑和失败回路收束到 `SKILL.md`。
- 新增 `test-prompts.json`，覆盖 intake/gap analysis、execute improvement、conflict/audit 三类回归场景。
- 同步 README、类型图、全局改进引用与上下文中的旧 workflow 引用，并通过 delivery validator 与 smoke test。

## 2026-05-26

- 初始化 `aigc-learn` 为 `.agents/skills/aigc/` 的学习型卫星技能。
- 增加多媒介学习对象摄取、冲突核查、全局技能树映射、隔离审计、类型包和输出模板。
- 增加视频复杂对象与书籍/超长上下文学习的 `references/` 专属细则，并同步入口引用、类型指向、执行拓扑和审计门禁。

## 2026-05-26（下午）

**核心重新定位**：学习的终点是**改进落地**，不是输出报告。报告只是可选的执行副产物。

- `SKILL.md`：Output Contract 重新定位，强调核心产物是 changed_files + audit_result，报告降级为可选副产物；Reference Loading Guide 中 templates 降级为"按需加载"。
- `SKILL.md#Thinking-Action Node Map`：N8-AUDIT 通过 = 任务完成；N10-CLOSE 改为"仅当用户明确要求时"生成报告；更新 flowchart，强调完成标志。
- `review/review-contract.md`：Verdict Model 更新，pass/pass_with_followups = 任务完成；convergence 检查项改为 changed_files + audit_result。
- `CONTEXT.md`：recommended_action 改为 `execute-first-report-optional`；Reusable Heuristics 强化"报告是副产物，不是终点"。
- `templates/output-template.md`：重新定位为"可选副产物"，添加警告说明和简化模板。
- `README.md`：Quick Entry 更新，添加完成标志和报告副产物说明。
