# AIGC 3-主体

`aigc-design-subjects` 是 AIGC 主体资产阶段的父级路由技能。它负责建立主体注册表，向 `场景`、`角色`、`道具` 三个域级 subagents 分发同源任务包，并汇总三域状态、依赖缺口、跨域冲突和下游 handoff。

## Runtime Entry

- 主入口：`SKILL.md`
- 经验层：`CONTEXT.md`
- 父级注册表合同：`references/subject-registry-contract.md`
- Agent metadata：`agents/openai.yaml`
- 回归 prompts：`test-prompts.json`

## Boundary

父级只做路由、汇流、索引和报告，不代写场景、角色、道具的清单、设计稿、生成 prompt 或创作正文。整体调用时三域并发执行；域内 `1-清单 -> 2-设计 -> 3-生成` 顺序门由各自子技能包负责。
