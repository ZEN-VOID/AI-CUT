# AIGC 3-主体

`aigc-design-subjects` 是 AIGC 主体资产阶段的父级路由技能。它负责建立主体注册表，向 `场景`、`角色`、`道具` 三个域级 subagents 分发同源任务包，并汇总三域状态、依赖缺口、跨域冲突和下游 handoff。

## Runtime Entry

- 主入口：`SKILL.md`
- 经验层：`CONTEXT.md`
- 父级注册表合同：`references/subject-registry-contract.md`
- 生成共享合同：`_shared/midjourney风格参数.yaml`、`_shared/主体图复用与状态变体规则.md`
- Agent metadata：`agents/openai.yaml`
- 回归 prompts：`test-prompts.json`

## Boundary

父级只做路由、汇流、索引和报告，不代写场景、角色、道具的清单、设计稿、生成 prompt 或创作正文。整体调用时三域并发执行；域内 `1-清单 -> 2-设计 -> 3-生成` 顺序门由各自子技能包负责。

进入任一 `3-生成` 叶子时，普通新主体图默认通过 libTV 画布 `image` 节点使用 Midjourney V8.1；跨集同主体同状态已有图应复用或上传到当前画布；同主体新状态变体使用 Lib Image 和既有参考图。
