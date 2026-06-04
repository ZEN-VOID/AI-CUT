# aigc 5-表演

`5-表演` 将 `projects/aigc/<项目名>/4-导演/第N集.md` 的导演批注稿，结合 `3-美学` 的画面基调、角色风格和场景风格，融合改写为无导演批注残留的演员可执行表演稿。

## 目录树

```text
5-表演/
├── agents/
│   └── openai.yaml
├── knowledge-base/
│   └── actor-style-index.md
├── references/
├── CHANGELOG.md
├── CONTEXT.md
├── README.md
├── SKILL.md
└── test-prompts.json
```

## 快速入口

- 技能入口：`SKILL.md`
- 运行上下文：`CONTEXT.md`
- 本地演员/流派资料索引：`knowledge-base/actor-style-index.md`
- 基础方法论：`references/stanislavski-method-reference.md`
- 表演控制：`references/actor-performance-control-contract.md`
- 受控增强：`references/controlled-enrichment-contract.md`

## 输入

- 默认 source：`projects/aigc/<项目名>/4-导演/第N集.md`
- 默认美学上下文：
  - `projects/aigc/<项目名>/3-美学/画面基调/全局风格协议.md`
  - `projects/aigc/<项目名>/3-美学/角色风格/角色风格协议.md`
  - `projects/aigc/<项目名>/3-美学/场景风格/场景风格协议.md`

## 输出

- 表演稿：`projects/aigc/<项目名>/5-表演/第N集.md`
- 执行报告：`projects/aigc/<项目名>/5-表演/执行报告.md`

核心口径：保留原字段标题和结构，删除 `（导演批注：...）`，把原画面点与批注意图融合成更具体的动作、微表情、台词语气、内心外显、自然反应和生理反应。
