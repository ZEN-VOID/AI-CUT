# story-plan-volume-level

`story-plan-volume-level` 是 `2-卷章` 的卷级规划子技能，负责把整部总纲下钻到单卷可执行规划，并把整书悬念总设计转成单卷悬念开关。

## Directory Tree

```text
2-卷级/
├── guardrails/
│   └── guardrails-contract.md
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
├── knowledge-base/
│   └── volume-planning-heuristics.md
├── types/
│   ├── type-map.md
│   └── volume-planning-type-map.md
├── agents/
│   └── openai.yaml
├── CHANGELOG.md
├── CONTEXT.md
├── README.md
├── SKILL.md
└── test-prompts.json
```

## Quick Entry

- 入口合同：`SKILL.md`
- 经验层：`CONTEXT.md`
- 业务细则：`references/volume-planning-contract.md`
- 悬念机制：`../_shared/suspense-design-contract.md`，含 `本卷悬念线程表` 与 `本卷悬念负载`
- 六拍框架：`references/volume-rhythm-framework.md`
- 执行网络：`SKILL.md` 的 `Thinking-Action Node Map`
- 输出模板：`templates/output-template.md`
- 运行时边界：`guardrails/guardrails-contract.md`

## Validation

```bash
python3 /Users/vincentlee/.codex/skills/meta/构建/技能/skill-2.0/scripts/validate_skill_2_0.py .agents/skills/story/2-卷章/2-卷级 --mode delivery
python3 /Users/vincentlee/.codex/skills/meta/构建/技能/skill-2.0/scripts/smoke_test_skill_2_0.py .agents/skills/story/2-卷章/2-卷级 --mode delivery
```
