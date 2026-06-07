# lesson 8/html

`$lesson-delivery-html` generates HTML/web course delivery plans, page structures, interaction states, site manifests, and optional static site assembly targets from a parent delivery packet.

## Directory Tree

```text
html/
├── agents/
│   └── openai.yaml
├── CHANGELOG.md
├── CONTEXT.md
├── README.md
├── SKILL.md
└── test-prompts.json
```

## Quick Entry

Use `$lesson-delivery-html` when the target is HTML, web courseware, static site, mobile lesson, LMS embed, or browser-based course delivery under `projects/lesson/<项目名>/8-多端交付生成/html/`.

The active contract is in `SKILL.md`. Load `CONTEXT.md` with it. HTML writeback is limited to:

- `html-delivery-plan.md`
- `html-site-manifest.json`
- optional `index.html` or static site artifacts generated or improved through `.agents/skills/claude-design` from LLM-approved page plans

When the request involves actual HTML generation, redesign, polish, or browser verification, this leaf must load `.agents/skills/claude-design/SKILL.md + .agents/skills/claude-design/CONTEXT.md`. Lesson owns the course truth, page plan, and manifest; `claude-design` owns high-fidelity HTML visual execution and browser verification.

Scripts may only do HTML/CSS/JS assembly, resource copying, validation, export, and manifest writeback. They must not generate web course正文 or replace the `claude-design` visual execution pass.

## Validation

```bash
python3 /Users/vincentlee/.codex/skills/meta/构建/技能/skill-2.0/scripts/validate_skill_2_0.py .agents/skills/lesson/8-多端交付生成/html --mode delivery
python3 /Users/vincentlee/.codex/skills/meta/构建/技能/skill-2.0/scripts/smoke_test_skill_2_0.py .agents/skills/lesson/8-多端交付生成/html --mode delivery
```
