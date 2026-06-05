# lesson 0-初始化

`$lesson-init` initializes or repairs a courseware project scaffold under `projects/lesson/<项目名>/`.

## Directory Tree

```text
0-初始化/
├── agents/
│   └── openai.yaml
├── CHANGELOG.md
├── CONTEXT.md
├── README.md
├── SKILL.md
└── test-prompts.json
```

## Quick Entry

Use `$lesson-init` when a course, lesson, training, or courseware project must be created under `projects/lesson/`.

The active contract is in `SKILL.md`. Load `CONTEXT.md` with it. Current initialization writeback is limited to:

- `projects/lesson/<项目名>/0-初始化/` through `8-多端交付生成/`
- `projects/lesson/<项目名>/sources/`
- `projects/lesson/<项目名>/content-model/`
- `projects/lesson/<项目名>/assets/`
- `projects/lesson/<项目名>/MEMORY.md`
- `projects/lesson/<项目名>/CONTEXT/README.md`

Do not generate course briefs, source ledgers, objective maps, outlines, lesson text, question banks, visual systems, DOC/PPT/HTML files, or release folders during initialization.

## Validation

```bash
python3 /Users/vincentlee/.codex/skills/meta/构建/技能/skill-2.0/scripts/validate_skill_2_0.py .agents/skills/lesson/0-初始化 --mode delivery
python3 /Users/vincentlee/.codex/skills/meta/构建/技能/skill-2.0/scripts/smoke_test_skill_2_0.py .agents/skills/lesson/0-初始化 --mode delivery
```
