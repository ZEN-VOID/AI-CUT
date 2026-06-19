# aigc 1-分集

将小说原文资料切分为逐集原文真源。

## Directory Tree / 目录树

```text
1-分集/
├── SKILL.md
├── CONTEXT.md
├── README.md
├── CHANGELOG.md
├── test-prompts.json
├── agents/openai.yaml
├── references/input-output-contract.md
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
- 无原生集标但有章节/回目结构：默认一章/一回一集
- 连续正文或用户要求重组：默认约 2500-3000 字一集
- 输出：`projects/aigc/<项目名>/1-分集/第N集.md`
- 执行主链：以 `SKILL.md` 的 `Thinking-Action Node Map` 为唯一节点真源；模块只做授权展开，不维护第二流程。
- 回归资产：`test-prompts.json` 覆盖 source scan、显式集标、章节型小说和 repair/review 场景。
