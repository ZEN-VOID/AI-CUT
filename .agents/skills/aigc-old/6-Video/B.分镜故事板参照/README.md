# B.分镜故事板参照

融合型 `6-Video` Skill 2.0 包：把 `全能参照` 组级蒸馏、`Assets/` 故事板参照绑定和 provider handoff 收束到一个入口内。

## Directory Tree

```text
B.分镜故事板参照/
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

- 技能目录：`.agents/skills/aigc/6-Video/B.分镜故事板参照/`
- 项目输出根：`projects/aigc/<项目名>/6-Video/B.分镜故事板参照/<第N集>/`
- 主要模式：`distill_only`、`bind_references`、`handoff_provider`、`full_chain`、`compat_migration`

原 `全能参照`、`2-参照引用`、`3-视频生成` 目录保留，作为来源兼容和旧任务续跑入口。
