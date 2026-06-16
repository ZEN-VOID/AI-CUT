# fine-tuning

`fine-tuning` 是 AIGC `2-美学` 到 `10-画布` 输出物的多轮迭代调优卫星技能。它匹配阶段方案、执行 LLM-first 多轮调优、完成比对验收，并把通过的候选以 owner-safe patch 形式回交对应阶段。

## Directory Tree

```text
fine-tuning/
├── agents/
│   └── openai.yaml
├── CHANGELOG.md
├── CONTEXT.md
├── README.md
├── SKILL.md
├── test-prompts.json
├── references/
│   └── stage-tuning-schemes.md
├── review/
│   └── review-contract.md
├── scripts/
│   ├── README.md
│   └── validate_fine_tuning_skill.py
├── templates/
│   └── output-template.md
└── types/
    ├── stage-output-types.md
    └── type-map.md
```

## Runtime Entry

- Main entry: `$fine-tuning`
- Skill contract: `SKILL.md`
- Experience layer: `CONTEXT.md`
- Detailed stage schemes: `references/stage-tuning-schemes.md`
- Report template: `templates/output-template.md`

## Validation

```bash
python3 .agents/skills/aigc/fine-tuning/scripts/validate_fine_tuning_skill.py .agents/skills/aigc/fine-tuning
python3 /Users/vincentlee/.codex/skills/meta/构建/技能/skill-2.0/scripts/validate_skill_2_0.py .agents/skills/aigc/fine-tuning --mode delivery
python3 /Users/vincentlee/.codex/skills/meta/构建/技能/skill-2.0/scripts/smoke_test_skill_2_0.py .agents/skills/aigc/fine-tuning --mode delivery
```
