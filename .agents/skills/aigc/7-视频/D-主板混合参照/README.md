# D-主板混合参照

`D-主板混合参照` 是 `7-视频` 阶段的组级混合参照视频生成入口。它从 `4-分组` 读取完整分镜组内容，把 `6-图像/B-分镜故事板` 的组级故事板作为总参照，并把 `5-设计/角色|场景|道具/3-生成` 的主体图片绑定到对应主体后。

## Directory Tree

```text
D-主板混合参照/
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

## Quick Entry

- 技能目录：`.agents/skills/aigc/7-视频/D-主板混合参照/`
- 项目输出根：`projects/aigc/<项目名>/7-视频/D-主板混合参照/第N集/`
- 触发语义：同一分镜组 prompt 同时使用故事板总参照和主体后缀参照。

## Core Rule

故事板图写在 prompt 固定开头，说明它用于整组构图、镜头顺序和连续性；主体图写在对应角色、场景、道具后，形如 `主体名 @参照图`。
