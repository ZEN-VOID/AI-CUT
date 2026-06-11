# story-drafting

`story-drafting` is the root chapter drafting skill for `story2026`.

## Layout

```text
3-初稿/
├── SKILL.md
├── CONTEXT.md
├── README.md
├── CHANGELOG.md
├── test-prompts.json
├── agents/openai.yaml
├── references/chapter-drafting-contract.md
├── review/review-contract.md
├── templates/
├── types/type-map.md
├── guardrails/guardrails-contract.md
└── knowledge-base/drafting-heuristics.md
```

The root package directly handles chapter draft, continue, rewrite, local repair, and dry-run context assembly. It does not use A/B/C subskill routes.

## Canonical Output

`projects/story/<项目名>/3-初稿/第N卷/第N章.md`
