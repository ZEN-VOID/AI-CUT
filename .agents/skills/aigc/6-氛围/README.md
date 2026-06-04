# aigc 6-氛围

`6-氛围` 将 `projects/aigc/<项目名>/5-表演/第N集.md` 的逐集表演稿，结合 `3-美学` 的画面基调、角色风格和场景风格，选择性新增 `氛围画面：XXX` 字段。

## 目录树

```text
6-氛围/
├── agents/
│   └── openai.yaml
├── knowledge-base/
│   └── physical-atmosphere-index.md
├── references/
│   ├── atmosphere-and-mood-contract.md
│   └── scene-rhythm-contract.md
├── CHANGELOG.md
├── CONTEXT.md
├── README.md
├── SKILL.md
└── test-prompts.json
```

## 快速入口

- 技能入口：`SKILL.md`
- 运行上下文：`CONTEXT.md`
- 氛围与意境细则：`references/atmosphere-and-mood-contract.md`
- 视觉特效节奏细则：`references/scene-rhythm-contract.md`
- 物理氛围包索引：`knowledge-base/physical-atmosphere-index.md`

## 输入

- 默认 source：`projects/aigc/<项目名>/5-表演/第N集.md`
- 默认美学上下文：
  - `projects/aigc/<项目名>/3-美学/画面基调/全局风格协议.md`
  - `projects/aigc/<项目名>/3-美学/角色风格/角色风格协议.md`
  - `projects/aigc/<项目名>/3-美学/场景风格/场景风格协议.md`

## 输出

- 氛围稿：`projects/aigc/<项目名>/6-氛围/第N集.md`
- 执行报告：`projects/aigc/<项目名>/6-氛围/执行报告.md`

核心口径：保留原表演稿结构和正文，只在渲染、烘托、增强触发点之后新增 `氛围画面：XXX`，写入烟雾、打灯、鼓风机、自然元素、天气模拟、水火尘雪、投影影纹、温度/气味等现场物理/舞台特效层面的画面化细节。
