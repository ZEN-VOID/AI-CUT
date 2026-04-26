# aigc-prop-list

从 `projects/aigc/<项目名>/4-分组/第N集.md` 的组底 YAML `道具` 字段生成项目级 `道具清单.md`。

## 快速入口

- 调用名：`$aigc-prop-list`
- 目标输出：`projects/aigc/<项目名>/4-设计/道具/1-清单/道具清单.md`
- 固定字段：`名称`、`首次登场`、`原文描述（关键词式）`

## Directory Tree

```text
1-清单/
├── references/
│   └── prop-list-contract.md
├── scripts/
│   └── README.md
├── templates/
│   └── output-template.md
├── review/
│   └── review-contract.md
├── steps/
│   └── prop-list-workflow.md
├── knowledge-base/
│   └── prop-list-heuristics.md
├── types/
│   └── prop-type-map.md
├── agents/
│   └── openai.yaml
├── CHANGELOG.md
├── SKILL.md
├── CONTEXT.md
└── README.md
```

## 运行边界

本技能只负责 `道具/1-清单`。角色、场景、道具设计稿和生成阶段由各自目录负责。
