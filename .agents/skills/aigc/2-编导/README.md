# aigc 2-编导

`2-编导` 将 `1-分集` 的逐集原文一次性转成可拍、可演、可听的编导稿，整合旧 `2-编剧`、`3-导演`、`4-表演`。

## 目录树

```text
2-编导/
├── references/
├── scripts/
├── templates/
├── review/
├── steps/
├── knowledge-base/
├── types/
├── agents/openai.yaml
├── CHANGELOG.md
├── SKILL.md
├── CONTEXT.md
└── README.md
```

## 快速入口

- 技能入口：`SKILL.md`
- 运行上下文：`CONTEXT.md`
- 总流程：`steps/directing-workflow.md`
- 编剧内部层细则：`steps/script-layer-workflow.md`
- 客观叙事转对白/独白细则：`references/narration-to-voice-adaptation-contract.md`
- 导演内部层细则：`steps/director-layer-workflow.md`
- 表演内部层细则：`steps/performance-layer-workflow.md`
- 统一审查：`review/review-contract.md`

## 输出

- 输入：`projects/aigc/<项目名>/1-分集/第N集.md`
- 输出：`projects/aigc/<项目名>/2-编导/第N集.md`
- 报告：`projects/aigc/<项目名>/2-编导/执行报告.md`
- 下游：`3-运动` 默认读取 `2-编导/第N集.md`；`4-摄影` 默认读取 `3-运动/第N集.md`
