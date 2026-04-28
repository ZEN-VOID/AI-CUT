# aigc 2-编导

`2-编导` 将 `projects/aigc/<项目名>/1-分集/第N集.md` 的逐集原文忠实投影为可拍、可分组、可表演的编导剧本稿。

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
├── agents/
│   └── openai.yaml
├── CHANGELOG.md
├── SKILL.md
├── CONTEXT.md
└── README.md
```

## 快速入口

- 技能入口：`SKILL.md`
- 运行上下文：`CONTEXT.md`
- 核心规则：`references/script-adaptation-contract.md`
- 字段与声画：`references/field-routing-and-audio-visual-contract.md`
- 高潮画面：`references/climax-visual-treatment-contract.md`
- 流程：`steps/directing-workflow.md`
- 验收：`review/review-contract.md`
- 输出模板：`templates/output-template.md`

## 输出

- 输入：`projects/aigc/<项目名>/1-分集/第N集.md`
- 输出：`projects/aigc/<项目名>/2-编导/第N集.md`
- 报告：`projects/aigc/<项目名>/2-编导/执行报告.md`
