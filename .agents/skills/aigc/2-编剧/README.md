# aigc 2-编剧

`2-编剧` 将 `1-分集` 的逐集原文忠实投影为保真、声画配对、字段格式化的剧本化结构。

## 目录树

```text
2-编剧/
├── references/
│   ├── script-adaptation-contract.md
│   ├── field-routing-and-audio-visual-contract.md
│   ├── novel-to-screen-language-contract.md
│   └── hollywood-quality-spec.md
├── scripts/
│   ├── validate_script_projection.py
│   └── README.md
├── templates/
│   ├── episode-script.template.md
│   └── output-template.md
├── review/
├── steps/
├── knowledge-base/
├── types/
│   ├── type-map.md
│   └── source-to-script-type-map.md
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
- 保真规则：`references/script-adaptation-contract.md`
- 字段与声画：`references/field-routing-and-audio-visual-contract.md`
- 小说表述二次画面化：`references/novel-to-screen-language-contract.md`
- 质量规范：`references/hollywood-quality-spec.md`
- 类型包：`types/source-to-script-type-map.md`

## 输出

- 输入：`projects/aigc/<项目名>/1-分集/第N集.md`
- 输出：`projects/aigc/<项目名>/2-编剧/第N集.md`
- 报告：`projects/aigc/<项目名>/2-编剧/执行报告.md`
