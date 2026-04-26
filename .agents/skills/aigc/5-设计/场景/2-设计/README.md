# aigc 5-设计 / 场景 / 2-设计

`$aigc-scene-design` 将上游 `场景/1-清单` 的汇总式场景清单扩展为单个场景主体的细目设计稿。它负责研究、物语、空间解构、摄影语汇和英文图像提示词，不负责重新生成场景清单，也不直接生成图片。

## 快速入口

```bash
# 结构检查
test -f .agents/skills/aigc/5-设计/场景/2-设计/SKILL.md
test -f .agents/skills/aigc/5-设计/场景/2-设计/CONTEXT.md
find .agents/skills/aigc/5-设计/场景/2-设计 -maxdepth 2 -type f | sort
```

## 目录树

```text
2-设计/
├── references/
│   └── scene-design-contract.md
├── scripts/
│   └── README.md
├── templates/
│   └── output-template.md
├── review/
│   └── review-contract.md
├── steps/
│   └── scene-design-workflow.md
├── knowledge-base/
│   └── scene-design-heuristics.md
├── types/
│   └── scene-design-type-map.md
├── agents/
│   └── openai.yaml
├── CHANGELOG.md
├── CONTEXT.md
├── README.md
└── SKILL.md
```

## 输出位置

- 单场景设计稿：`projects/aigc/<项目名>/4-设计/场景/2-设计/S###-<场景名>.md`
- 可选执行报告：`projects/aigc/<项目名>/4-设计/场景/2-设计/执行报告.md`

## 固定画面约束

- 场景设计固定为纯空镜。
- 不出现人物、人体局部、剪影、倒影或人群。
- 英文 prompt 必须包含 `empty shot, no people, no human figures` 等等价约束。
