# aigc-repair

`aigc-repair` 是 AIGC 影视工作流的修复卫星技能，用于跨阶段输出物的局部、批量或整体调整。

## Directory Tree

```text
repair/
├── references/
├── scripts/
├── templates/
├── review/
├── steps/
├── knowledge-base/
├── types/
├── agents/
│   └── openai.yaml
├── CHANGELOG.md
├── SKILL.md
├── CONTEXT.md
└── README.md
```

## Quick Entry

- 入口：`SKILL.md`
- 经验层：`CONTEXT.md`
- 影响范围：`references/impact-scope-contract.md`
- 源层真源：`references/source-truth-ledger.md`
- 豆包执行：`references/doubao-execution-contract.md`
- 工作流：`steps/repair-workflow.md`
- 验收：`review/review-contract.md`

## Output

默认对话交付 `repair_packet`。需要落盘时写入 `reports/aigc-repair-YYYYMMDD.md` 或 `projects/aigc/<项目名>/repair/repair-report-YYYYMMDD.md`。
