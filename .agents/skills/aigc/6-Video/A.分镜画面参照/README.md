# A.分镜画面参照

融合型 `6-Video` Skill 2.0 包：把首帧参照蒸馏、`Assets/` 参照绑定和 provider handoff 收束到一个入口内。

## Directory Tree

```text
A.分镜画面参照/
├── references/
│   ├── source-fusion-map.md
│   ├── prompt-distillation-contract.md
│   ├── reference-binding-contract.md
│   ├── provider-handoff-contract.md
│   └── shared-prompt-principles.md
├── steps/
│   └── frame-visual-reference-workflow.md
├── review/
│   └── review-contract.md
├── types/
│   └── type-map.md
├── knowledge-base/
│   └── video-reference-heuristics.md
├── templates/
│   ├── output-template.md
│   ├── request-packet.template.json
│   └── submit-plan.template.json
├── scripts/
│   └── README.md
├── agents/
│   └── openai.yaml
├── SKILL.md
├── CONTEXT.md
├── README.md
├── CHANGELOG.md
└── TODO.md
```

## Quick Entry

- 调用名：`$aigc-video-frame-visual-reference`
- 技能目录：`.agents/skills/aigc/6-Video/A.分镜画面参照/`
- 项目输出根：`projects/aigc/<项目名>/6-Video/A.分镜画面参照/<第N集>/`

原 `首帧参照`、`2-参照引用`、`3-视频生成` 目录保留，作为来源兼容和旧任务续跑入口。
