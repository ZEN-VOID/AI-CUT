# lesson 4-教学策略与课程架构

`$lesson-course-architecture` turns upstream lesson positioning, knowledge modeling, and objectives into a teaching strategy and course architecture blueprint.

## Directory Tree

```text
4-教学策略与课程架构/
├── agents/
│   └── openai.yaml
├── CHANGELOG.md
├── CONTEXT.md
├── README.md
├── SKILL.md
└── test-prompts.json
```

## Quick Entry

Use `$lesson-course-architecture` after these upstream inputs exist or the user provides equivalent briefs:

```text
projects/lesson/<项目名>/1-课程定位/course-positioning.md
projects/lesson/<项目名>/2-资料吸收与知识建模/
projects/lesson/<项目名>/3-目标与评价蓝图/
```

The stage designs course modules, session sequence, teaching strategy, rhythm, and cognitive-load scaffolding. It does not generate complete lesson scripts, question banks, visual systems, PPT copy, HTML pages, or DOC/PPT/HTML deliverables.

Canonical project outputs:

```text
projects/lesson/<项目名>/4-教学策略与课程架构/course-outline.md
projects/lesson/<项目名>/4-教学策略与课程架构/teaching-strategy-and-load-plan.md
projects/lesson/<项目名>/4-教学策略与课程架构/downstream-handoff.md
```

Without a project root, return draft Markdown and mark it as not formally written back.

## Validation

```bash
python3 /Users/vincentlee/.codex/skills/meta/构建/技能/skill-2.0/scripts/validate_skill_2_0.py .agents/skills/lesson/4-教学策略与课程架构 --mode delivery
python3 /Users/vincentlee/.codex/skills/meta/构建/技能/skill-2.0/scripts/smoke_test_skill_2_0.py .agents/skills/lesson/4-教学策略与课程架构 --mode delivery
```
