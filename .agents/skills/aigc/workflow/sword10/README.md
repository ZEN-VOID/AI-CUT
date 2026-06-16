# aigc workflow sword10

`sword10` 编排 `projects/aigc/<项目名>/` 下指定分集，从 `2-美学` 经 `3-主体`、`4-编剧`、`5-导演`、`6-分镜`、`7-摄影` 连续推进到 `8-分组`。它只负责 subagent 派发、阶段汇流、失败路由和运行账本；阶段正文、主体注册表和风格协议仍由对应阶段技能拥有。

## Directory Tree

```text
sword10/
├── guardrails/
├── references/
├── scripts/
├── templates/
├── review/
├── knowledge-base/
├── types/
├── agents/
├── CHANGELOG.md
├── CONTEXT.md
├── README.md
├── SKILL.md
└── test-prompts.json
```

## Quick Entry

- 输入：项目根 + 分集选择 + 可用 subagent runtime。
- 默认链路：`2-美学 -> 3-主体 -> 4-编剧 -> 5-导演 -> 6-分镜 -> 7-摄影 -> 8-分组`。
- 默认输出：`projects/aigc/<项目名>/workflow/sword10/<run_id>/`。

## Key Files

- 入口合同：`SKILL.md`
- 执行拓扑：`SKILL.md#Thinking-Action Node Map`
- subagent 边界：`references/subagent-dispatch-contract.md`
- 阶段交接：`references/stage-handoff-contract.md`
- 质量门禁：`review/review-contract.md`
- 回归 prompts：`test-prompts.json`
