# story-plan-volume-level

`story-plan-volume-level` 是 `2-卷章规划` 的卷级规划子技能，负责把整部总纲下钻到单卷可执行规划。

## Directory Tree

```text
2-卷级/
├── references/
│   ├── legacy-upgrade-matrix.md
│   ├── volume-planning-contract.md
│   └── volume-rhythm-framework.md
├── scripts/
│   └── README.md
├── templates/
│   ├── output-template.md
│   └── volume-planning.template.md
├── review/
│   └── review-contract.md
├── steps/
│   └── volume-planning-workflow.md
├── knowledge-base/
│   └── volume-planning-heuristics.md
├── types/
│   └── volume-planning-type-map.md
├── agents/
│   └── openai.yaml
├── CHANGELOG.md
├── CONTEXT.md
└── SKILL.md
```

## Quick Entry

- 入口合同：`SKILL.md`
- 经验层：`CONTEXT.md`
- 业务细则：`references/volume-planning-contract.md`
- 六拍框架：`references/volume-rhythm-framework.md`
- 执行网络：`steps/volume-planning-workflow.md`
- 输出模板：`templates/output-template.md`

## Validation

```bash
python3 /Users/vincentlee/.codex/skills/meta/构建/技能/skill-工作车间/scripts/validate_skill_2_0.py .agents/skills/story/2-卷章规划/2-卷级
```
