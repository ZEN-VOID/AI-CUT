# aigc 2-编导

`2-编导` 将 `projects/aigc/<项目名>/1-分集/第N集.md` 的逐集原文忠实投影为可拍、可分组、可表演的编导剧本稿。

## 目录树

```text
2-编导/
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
- 核心规则：`references/script-adaptation-contract.md`
- 字段与声画：`references/field-routing-and-audio-visual-contract.md`
- 小说表述二次画面化：`references/novel-to-screen-language-contract.md`
- 环境字段：`环境描写` 只写场景本身的写景画面；人物动作、对白承托、群体反应和道具信息分别进入对应字段。
- 心理反应细则：`references/psychological-reaction-contract.md`；主角内心想法和主角视角判断必须保留为 `独白/内心独白` 或可感知反应；`心理反应` 只写演员可表演、观众可从画面或声音 GET 到的反应，抽象内心解释必须转成可见/可听/可演承托，或改入 `独白/内心独白` 并配画面。
- 动作客观化：`角色动作` / `动作画面` 只写镜头可实拍的客观动作、神态、语气和生理反应，禁止“试图、想要、打算、意图”等主观预判词；直接情绪感受、往日常态总结和无关前史补充按 references 规则转译或删除。
- 高潮画面：`references/climax-visual-treatment-contract.md`
- 表演与场景工艺：`references/performance-and-scene-craft-contract.md`
- B 路线受控增强：`references/controlled-enrichment-contract.md`
- 整集视觉主轴：`references/episode-visual-spine-contract.md`
- 画面美学：`references/visual-aesthetic-contract.md`
- 终结画面尾钩：`references/episode-final-image-contract.md`
- 终结画面类型匹配：`types/episode-final-image-type-map.md`
- 流程：`steps/directing-workflow.md`
- 验收：`review/review-contract.md`
- 输出模板：`templates/output-template.md`

## 输出

- 输入：`projects/aigc/<项目名>/1-分集/第N集.md`
- 输出：`projects/aigc/<项目名>/2-编导/第N集.md`
- 报告：`projects/aigc/<项目名>/2-编导/执行报告.md`
