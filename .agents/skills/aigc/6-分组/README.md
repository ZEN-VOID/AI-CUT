# aigc 6-分组

`6-分组` 将 `projects/aigc/<项目名>/5-摄影/第N集.md` 的逐集摄影稿切成完整分镜组，并为每组重复当前场景标题、补充定场镜头、拼接 north_star 风格字段和 YAML 统计；相邻分镜组之间额外生成 3-4 秒组间首尾帧连接件，连接件同样先标明同场景或跨场景标题关系，再继承三项 north_star 风格行，并把固定音频/字幕约束置顶于第 1 行风格行最前。

## 目录树

```text
6-分组/
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
- 项目级必读：`projects/aigc/<项目名>/MEMORY.md`
- 项目北极星：`projects/aigc/<项目名>/0-初始化/north_star.yaml`
- 边界规则：`references/group-boundary-contract.md`
- 定场镜头：`references/group-establishing-shot-contract.md`
- 组间连接件：`references/bridge-shot-contract.md`
- north_star 投影：`references/north-star-projection-contract.md`
- YAML 统计：`references/statistics-yaml-contract.md`
- 流程：`steps/grouping-workflow.md`
- 验收：`review/review-contract.md`
- 输出模板：`templates/output-template.md`
- 机械校验：`scripts/validate_storyboard_groups.py`

## 输出

- 输入：`projects/aigc/<项目名>/5-摄影/第N集.md`
- 风格真源：`projects/aigc/<项目名>/0-初始化/north_star.yaml`
- 输出：`projects/aigc/<项目名>/6-分组/第N集.md`
- 报告：`projects/aigc/<项目名>/6-分组/执行报告.md`
