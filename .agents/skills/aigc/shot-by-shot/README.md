# aigc shot-by-shot

`shot-by-shot` 是 `.agents/skills/aigc` 的临摹型卫星技能，用于把参考影片或视频逐镜拆解成可供 `0-初始化`、`2-编导`、`3-摄影` 与 `5-设计` 消费的 AIGC 项目上下文解析。

## 目录树

```text
shot-by-shot/
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
- 基础解析维度：`references/analysis-method.md`
- AIGC 阶段输出融合：`references/adaptation-output-contract.md`
- 证据与版权边界：`references/evidence-and-rights-boundary.md`
- 流程：`steps/shot-by-shot-workflow.md`
- 验收：`review/review-contract.md`
- 输出模板：`templates/output-template.md`

## 输出

- 主报告：`projects/aigc/<项目名>/shot-by-shot/<reference_slug>/shot-by-shot.md`
- 画面风格解析：`projects/aigc/<项目名>/CONTEXT/shot-by-shot/<reference_slug>/画面风格解析.md`
- 编导解析：`projects/aigc/<项目名>/CONTEXT/shot-by-shot/<reference_slug>/编导解析.md`
- 摄影解析：`projects/aigc/<项目名>/CONTEXT/shot-by-shot/<reference_slug>/摄影解析.md`
- 设计解析：`projects/aigc/<项目名>/CONTEXT/shot-by-shot/<reference_slug>/设计解析.md`
- 执行报告：`projects/aigc/<项目名>/shot-by-shot/<reference_slug>/执行报告.md`
