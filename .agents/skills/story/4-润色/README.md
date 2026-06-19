# story-polishing

`story-polishing` is the root chapter polishing skill for `story2026`.

## Directory Tree

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
├── types/
│   ├── type-map.md
│   ├── polishing-type-map.md
│   ├── guardrail-setup.md
│   ├── character-reaction-repair.md
│   ├── prose-texture-repair.md
│   ├── visual-readability-repair.md
│   ├── genre-scene-repair.md
│   ├── action-choreography-repair.md
│   ├── interiority-repair.md
│   ├── atmosphere-pressure-repair.md
│   ├── sci-fi-tech-repair.md
│   ├── cyberpunk-texture-repair.md
│   ├── xuanhuan-power-repair.md
│   ├── romance-tension-repair.md
│   └── wuxia-blade-qi-repair.md
├── guardrails/guardrails-contract.md
└── knowledge-base/polishing-heuristics.md
```

The root package directly handles first polish, local repair, authorized rewrite, subagent review optimize, and dry-run context assembly. It does not use A/B/C subskill routes. Character reaction, prose texture, visual readability, genre-scene repair, action choreography, interiority, atmosphere pressure, sci-fi tech, cyberpunk texture, xuanhuan power, romance tension, and wuxia blade-qi repair are repair type packages owned by this root skill. Specific repair packages are selected through `types/type-map.md` and recorded in `repair_type_package_manifest`; detail-expansion tasks also require `detail_expansion_profile`.

## Canonical Output

`projects/story/<项目名>/4-润色/第N卷/第N章.md`
