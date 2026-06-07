# lesson 8-多端交付生成

`$lesson-delivery` turns lesson content models into DOC/PPT/HTML delivery plans, leaf work packets, and a shared manifest.

## Directory Tree

```text
8-多端交付生成/
├── agents/
│   └── openai.yaml
├── doc/
│   ├── agents/
│   │   └── openai.yaml
│   ├── CHANGELOG.md
│   ├── CONTEXT.md
│   ├── README.md
│   ├── SKILL.md
│   └── test-prompts.json
├── html/
│   ├── agents/
│   │   └── openai.yaml
│   ├── CHANGELOG.md
│   ├── CONTEXT.md
│   ├── README.md
│   ├── SKILL.md
│   └── test-prompts.json
├── ppt/
│   ├── agents/
│   │   └── openai.yaml
│   ├── CHANGELOG.md
│   ├── CONTEXT.md
│   ├── README.md
│   ├── SKILL.md
│   └── test-prompts.json
├── CHANGELOG.md
├── CONTEXT.md
├── README.md
├── SKILL.md
└── test-prompts.json
```

## Quick Entry

Use `$lesson-delivery` when a project under `projects/lesson/<项目名>/` is ready to turn stages `3` through `7` and `content-model/` into a delivery plan and manifest.

Parent writeback is limited to:

- `projects/lesson/<项目名>/8-多端交付生成/delivery-plan.md`
- `projects/lesson/<项目名>/8-多端交付生成/delivery-manifest.json`

Concrete DOC, PPT, and HTML delivery belongs to the `doc/`, `ppt/`, and `html/` leaf packages. If the HTML target includes a real `.html` / static-site artifact, the HTML leaf packet must point to `8-多端交付生成/html -> .agents/skills/claude-design` for high-fidelity HTML design execution and browser verification. Scripts may only do format conversion, assembly, validation, and manifest writeback; they must not generate or project course正文.

## Validation

```bash
python3 /Users/vincentlee/.codex/skills/meta/构建/技能/skill-2.0/scripts/validate_skill_2_0.py .agents/skills/lesson/8-多端交付生成 --mode delivery
python3 /Users/vincentlee/.codex/skills/meta/构建/技能/skill-2.0/scripts/smoke_test_skill_2_0.py .agents/skills/lesson/8-多端交付生成 --mode delivery
```
