# aigc 0-初始化

`$aigc-init` initializes or reinitializes AIGC film projects under `projects/aigc/<项目名>/`.

## Directory Tree

```text
0-初始化/
├── references/
│   ├── artifacts-and-sources.md
│   ├── migration-matrix.md
│   ├── mode-and-team-contract.md
│   ├── rebootstrap-contract.md
│   └── scope-and-runtime.md
├── scripts/
│   └── README.md
├── templates/
│   ├── init-handoff.template.yaml
│   ├── init-option-card.template.md
│   ├── north-star.template.yaml
│   ├── output-template.md
│   ├── output-template-map.md
│   ├── project-changelog.template.md
│   ├── project-context-readme.template.md
│   ├── project-memory.template.md
│   └── state.template.json
├── review/
│   └── init-review-gate.md
├── steps/
│   └── init-workflow.md
├── knowledge-base/
│   └── init-heuristics.md
├── types/
│   └── init-type-map.md
├── agents/
│   └── openai.yaml
├── CHANGELOG.md
├── CONTEXT.md
├── README.md
└── SKILL.md
```

## Quick Entry

Use `$aigc-init` when a project must enter or re-enter initialization.

The entry contract is in `SKILL.md`. Load `CONTEXT.md` with it, then read the referenced partition for the current node:

- runtime paths: `references/scope-and-runtime.md`
- mode and team: `references/mode-and-team-contract.md`
- artifacts and sources: `references/artifacts-and-sources.md`
- reset: `references/rebootstrap-contract.md`
- workflow: `steps/init-workflow.md`
- review: `review/init-review-gate.md`

## Validation

```bash
python3 /Users/vincentlee/.codex/skills/meta/构建/技能/skill-工作车间/scripts/validate_skill_2_0.py .agents/skills/aigc/0-初始化
python3 scripts/skill_context_audit.py --strict
python3 scripts/aigc_skill_audit.py --strict
```
