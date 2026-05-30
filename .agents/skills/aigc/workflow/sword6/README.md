# aigc workflow sword6

`sword6` 编排 `projects/aigc/<项目名>/` 下指定分集，从 `2-编剧` 连续推进到 `6-分组`。它只负责 subagent 派发、阶段汇流、失败路由和运行账本；阶段正文仍由对应阶段技能拥有。

## Directory Tree

```text
sword6/
├── guardrails/
├── references/
├── scripts/
├── templates/
├── review/
├── steps/
├── knowledge-base/
├── types/
├── agents/
├── CHANGELOG.md
├── CONTEXT.md
├── README.md
└── SKILL.md
```

## Quick Entry

- 输入：项目根 + 分集选择 + 可用 subagent runtime。
- 默认链路：`2-编剧 -> 3-导演 -> 4-表演 -> 5-摄影 -> 6-分组`。
- 默认输出：`projects/aigc/<项目名>/workflow/sword6/<run_id>/`。

## Key Files

- 入口合同：`SKILL.md`
- 执行拓扑：`steps/sword6-workflow.md`
- subagent 边界：`references/subagent-dispatch-contract.md`
- 阶段交接：`references/stage-handoff-contract.md`
- 质量门禁：`review/review-contract.md`
