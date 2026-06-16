# aigc-prop-list

从 `projects/aigc/<项目名>/3-主体/subject-registry.yaml` 的 `subjects.props` 条目生成项目级 `道具清单.md`。

## 快速入口

- 调用名：`$aigc-prop-list`
- 目标输出：`projects/aigc/<项目名>/3-主体/道具/1-清单/道具清单.md`
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
├── knowledge-base/
│   └── prop-list-heuristics.md
├── types/
│   └── prop-type-map.md
├── agents/
│   └── openai.yaml
├── CHANGELOG.md
├── SKILL.md
├── CONTEXT.md
├── test-prompts.json
└── README.md
```

## 运行边界

本技能只负责 `道具/1-清单`。角色、场景、道具设计稿和生成阶段由各自目录负责。

`SKILL.md` 是 runtime-spine 真源；旧 workflow 语义已并入 `SKILL.md`，不再作为第二规则源。归并、过滤、canonical 名称和关键词式描述必须由 LLM 逐条裁决，脚本只能做机械读取、定位、格式检查和 dry-run。
