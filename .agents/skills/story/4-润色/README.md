# story-polishing

`story-polishing` is the root chapter polishing skill for `story2026`.

## Layout

```text
4-润色/
├── SKILL.md
├── CONTEXT.md
├── README.md
├── CHANGELOG.md
├── test-prompts.json
├── agents/openai.yaml
├── references/chapter-polishing-contract.md
├── review/review-contract.md
├── templates/
├── types/type-map.md
├── guardrails/guardrails-contract.md
└── knowledge-base/polishing-heuristics.md
```

The root package directly handles first polish, local repair, authorized rewrite, subagent review optimize, and dry-run context assembly. It does not use A/B/C subskill routes.

## Canonical Output

`projects/story/<项目名>/4-润色/第N卷/第N章.md`
