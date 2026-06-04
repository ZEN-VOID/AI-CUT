# aigc Query

`$aigc-query` answers factual questions about existing AIGC film projects under `projects/aigc/<项目名>/`.

## Directory Tree

```text
query/
├── references/
│   ├── legacy-migration-matrix.md
│   ├── project-runtime-layout.md
│   └── system-data-flow.md
├── scripts/
│   └── README.md
├── templates/
│   └── output-template.md
├── review/
│   └── review-contract.md
├── knowledge-base/
│   └── query-heuristics.md
├── types/
│   └── query-type-map.md
├── agents/
│   └── openai.yaml
├── CHANGELOG.md
├── CONTEXT.md
├── README.md
├── SKILL.md
└── test-prompts.json
```

## Quick Entry

Use `$aigc-query` for project status, stage output lookup, asset lookup, validation evidence, route evidence, and legacy/current path conflict diagnosis.

Load `SKILL.md + CONTEXT.md`, then read:

- `references/system-data-flow.md`
- `references/project-runtime-layout.md`
- `types/query-type-map.md`
- `SKILL.md#Thinking-Action Node Map`
- `review/review-contract.md`

## Validation

```bash
python3 /Users/vincentlee/.codex/skills/meta/构建/技能/skill-2.0/scripts/validate_skill_2_0.py .agents/skills/aigc/query --mode delivery
```
