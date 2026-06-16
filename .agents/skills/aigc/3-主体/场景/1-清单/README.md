# 场景 1-清单

`$aigc-scene-list` 从 `projects/aigc/<项目名>/3-主体/subject-registry.yaml` 的 `subjects.scenes` 条目生成场景清单。

## 快速入口

```text
使用 $aigc-scene-list，为 projects/aigc/<项目名>/ 生成场景清单。
```

## 关键拓扑

- 入口拓扑与状态图见 `SKILL.md` 的 `Visual Maps`。
- 执行节点、类型分支和返工回路见 `SKILL.md 的 Thinking-Action Node Map`。
- 来源信任图见 `references/source-and-merge-contract.md`。
- 类型判定图见 `types/scene-type-map.md`。
- review 回路见 `review/review-contract.md`。

## 目录树

```text
1-清单/
├── references/
│   └── source-and-merge-contract.md
├── scripts/
│   └── README.md
├── templates/
│   └── output-template.md
├── review/
│   └── review-contract.md
├── knowledge-base/
│   └── scene-list-heuristics.md
├── types/
│   └── scene-type-map.md
├── agents/
│   └── openai.yaml
├── CHANGELOG.md
├── CONTEXT.md
├── README.md
├── SKILL.md
└── test-prompts.json
```

`test-prompts.json` 用于 runtime-spine dry-run / regression prompts，覆盖单集清单、增量 merge 和反脚本伪差异 review。

## 输出

canonical 输出路径：

```text
projects/aigc/<项目名>/3-主体/场景/1-清单/场景清单.md
```

主体表格字段固定为：

| 名称 | 首次登场 | 原文描述（关键词式） |
| --- | --- | --- |

可选执行报告写入同目录 `执行报告.md`。
