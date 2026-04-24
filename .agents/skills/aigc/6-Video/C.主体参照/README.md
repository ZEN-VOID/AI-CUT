# C.主体参照

`C.主体参照` 是 `6-Video` 阶段的主体识别向融合型 Skill 2.0 包。

## Directory Tree

```text
C.主体参照/
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
├── TODO.md
├── SKILL.md
├── CONTEXT.md
└── README.md
```

## Quick Entry

- 调用名：`$aigc-video-subject-reference`
- 技能目录：`.agents/skills/aigc/6-Video/C.主体参照/`
- 项目输出根：`projects/aigc/<项目名>/6-Video/C.主体参照/<第N集>/`

## Runtime Layout

```text
projects/aigc/<项目名>/6-Video/C.主体参照/<第N集>/
├── distill/
├── reference-binding/
└── generation-handoff/
```

## Source Compatibility

本包融合但不删除：

- `.agents/skills/aigc/6-Video/1-提示词蒸馏/全能参照/`
- `.agents/skills/aigc/6-Video/2-参照引用/`
- `.agents/skills/aigc/6-Video/3-视频生成/`
