# lesson Query

`$lesson-query` answers read-only factual questions about lesson projects under `projects/lesson/<项目名>/`.

## Directory Tree

```text
query/
├── agents/
│   └── openai.yaml
├── CHANGELOG.md
├── CONTEXT.md
├── README.md
├── SKILL.md
└── test-prompts.json
```

## Quick Entry

Use `$lesson-query` for project facts, stage output lookup, content-model indexes, DOC/PPT/HTML delivery paths, project status, route drift, and gap/conflict questions.

Load `SKILL.md + CONTEXT.md`, then follow the runtime spine:

1. Lock `PROJECT_ROOT` under `projects/lesson/<项目名>/`.
2. Classify the truth role: project fact, stage output, content model, delivery path, state route, or gap/conflict.
3. Read only existing carriers.
4. Distinguish file exists, stage complete, and validation passed.
5. Return one evidence-backed answer.

## Validation

```bash
python3 /Users/vincentlee/.codex/skills/meta/构建/技能/skill-2.0/scripts/validate_skill_2_0.py .agents/skills/lesson/query --mode delivery
python3 /Users/vincentlee/.codex/skills/meta/构建/技能/skill-2.0/scripts/smoke_test_skill_2_0.py .agents/skills/lesson/query --mode delivery
```
