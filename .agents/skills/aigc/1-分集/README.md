# aigc 1-分集

将小说原文资料切分为逐集原文真源。

## Directory Tree / 目录树

```text
1-分集/
├── SKILL.md
├── CONTEXT.md
├── README.md
├── CHANGELOG.md
├── agents/openai.yaml
├── references/input-output-contract.md
├── steps/episode-split-workflow.md
├── review/review-contract.md
├── types/source-type-map.md
├── knowledge-base/episode-split-heuristics.md
├── templates/episode-output.template.md
├── templates/output-template.md
└── scripts/README.md
```

## 快速口径

- 默认输入：`projects/aigc/<项目名>/源/`
- 显式输入：用户指定的任意小说原文资料路径
- 原资料自带集数划分：以原划分为准
- 无集数划分：默认约 2500-3000 字一集
- 输出：`projects/aigc/<项目名>/1-分集/第N集.md`
