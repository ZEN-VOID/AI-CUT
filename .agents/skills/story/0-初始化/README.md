# story-init

`story-init` 初始化或重初始化小说、网文、长篇故事和书项目，canonical runtime 为 `projects/story/<项目名>/`。

## Quick Entry

```bash
python3 .agents/skills/story/scripts/init_project.py \
  "./projects/story/示例小说" "示例小说" "悬疑" \
  --init-mode "team代入模式"
```

## Directory Tree

```text
0-初始化/
├── guardrails/
│   └── guardrails-contract.md
├── references/
│   ├── creative-seed-routing/
│   ├── legacy-upgrade-matrix.md
│   ├── mode-and-team-contract.md
│   ├── prompt-packet-contract.md
│   └── runtime-and-handoff-contract.md
├── scripts/
│   └── README.md
├── templates/
│   ├── init-handoff.template.yaml
│   ├── north-star.template.yaml
│   ├── output-template.md
│   ├── project-memory.template.md
│   └── story-source-manifest.template.yaml
├── review/
│   ├── review-contract.md
│   └── init-review-gate.md
├── knowledge-base/
│   └── init-heuristics.md
├── types/
│   ├── type-map.md
│   └── init-type-map.md
├── agents/
│   └── openai.yaml
├── CHANGELOG.md
├── CONTEXT.md
├── README.md
└── SKILL.md
```

## Owner Map

| owner | responsibility |
| --- | --- |
| `SKILL.md` | 入口、输入、类型路由、节点主链、模块授权、根因合同、输出门禁 |
| `CONTEXT.md` | 初始化经验层知识库 |
| `guardrails/` | 运行时权限、注入防护、self-modification 禁止与违规响应 |
| `references/` | 模式、team、runtime、handoff、prompt packet、创意路由和迁移细则 |
| `types/` | 媒介、运行类型、team 编组与证据类型分流 |
| `review/` | sufficiency gate、verdict 与 provider 降级口径 |
| `templates/` | 输出模板和项目工件样板 |
| `scripts/` | 机械脚本边界说明 |
| `knowledge-base/` | 可复用启发和修复打法 |
| `agents/` | 产品侧入口元数据 |
