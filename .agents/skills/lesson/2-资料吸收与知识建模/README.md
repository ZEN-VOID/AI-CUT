# lesson 2-资料吸收与知识建模

`$lesson-knowledge-modeling` researches source materials and turns a course positioning brief into evidence-backed knowledge context for downstream lesson stages.

## Directory Tree

```text
2-资料吸收与知识建模/
├── agents/
│   └── openai.yaml
├── CHANGELOG.md
├── CONTEXT.md
├── README.md
├── SKILL.md
└── test-prompts.json
```

## Quick Entry

Use `$lesson-knowledge-modeling` after `1-课程定位` has produced:

```text
projects/lesson/<项目名>/1-课程定位/course-positioning.md
```

The stage researches official sources, documentation, standards, papers, forums, community discussions, web materials, user-supplied files, and internal project context, then builds downstream-ready Markdown outputs.

Canonical project outputs:

```text
projects/lesson/<项目名>/2-资料吸收与知识建模/research-source-inventory.md
projects/lesson/<项目名>/2-资料吸收与知识建模/knowledge-model.md
projects/lesson/<项目名>/2-资料吸收与知识建模/evidence-and-case-library.md
projects/lesson/<项目名>/2-资料吸收与知识建模/downstream-handoff.md
```

Without a project root, return draft Markdown and mark it as not formally written back.

## Validation

```bash
python3 /Users/vincentlee/.codex/skills/meta/构建/技能/skill-2.0/scripts/validate_skill_2_0.py .agents/skills/lesson/2-资料吸收与知识建模 --mode delivery
python3 /Users/vincentlee/.codex/skills/meta/构建/技能/skill-2.0/scripts/smoke_test_skill_2_0.py .agents/skills/lesson/2-资料吸收与知识建模 --mode delivery
```

