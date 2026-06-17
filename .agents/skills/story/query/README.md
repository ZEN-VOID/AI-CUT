# story-query

`story-query` 是 `story2026` 的事实查询卫星技能，用于回答小说项目的规划态、当前态、已验证实绩、质量趋势和执行态问题。

## Directory Tree

```text
query/
├── references/
│   ├── advanced/foreshadowing.md
│   ├── legacy-migration-matrix.md
│   ├── query-command-catalog.md
│   ├── system-data-flow.md
│   └── tag-specification.md
├── scripts/
│   └── README.md
├── templates/
│   └── output-template.md
├── review/
│   └── review-contract.md
├── knowledge-base/
│   └── query-heuristics.md
├── types/
│   ├── type-map.md
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

1. Load `SKILL.md + CONTEXT.md`.
2. Resolve `PROJECT_ROOT` with `.agents/skills/story/scripts/story.py`.
3. Classify the request via `SKILL.md` `Type Routing Matrix` and `types/query-type-map.md`.
4. Execute the node network in `SKILL.md` `Thinking-Action Node Map`.
5. Use `references/query-command-catalog.md` only for read-only command details.
6. Check the answer with `review/review-contract.md`.
7. Render with `templates/output-template.md`.

## Non-Goals

- 不写正文。
- 不回写 Cards / planning / actualization。
- 不把 planned、current、validated_actual 混成一个事实。
