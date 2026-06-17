# story-drafting

`story-drafting` is the root chapter drafting skill for `story2026`.

## Directory Tree

```text
3-初稿/
├── SKILL.md
├── CONTEXT.md
├── README.md
├── CHANGELOG.md
├── test-prompts.json
├── agents/openai.yaml
├── references/
│   ├── chapter-drafting-contract.md
│   ├── character-presence-contract.md
│   ├── scene-pressure-texture-contract.md
│   └── genre-scene-drafting-contract.md
├── review/review-contract.md
├── templates/
├── types/type-map.md
├── types/网文/武侠/白刃剑气流.md
├── guardrails/guardrails-contract.md
└── knowledge-base/drafting-heuristics.md
```

The root package directly handles chapter draft, continue, rewrite, local repair, and dry-run context assembly. It does not use A/B/C subskill routes. Character presence, scene pressure, and genre-scene drafting are authorized drafting references, not separate performance, atmosphere, or genre-strengthening stages. Genre and subtype packages are selected through `types/type-map.md` and recorded in `type_package_manifest`; wuxia blade-qi flow is a subtype package under `action_combat`, not an AIGC storyboard shortcut.

## Canonical Output

`projects/story/<项目名>/3-初稿/第N卷/第N章.md`
