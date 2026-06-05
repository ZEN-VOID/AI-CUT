# lesson 3-目标与评价蓝图

`$lesson-objective-assessment-blueprint` turns lesson positioning and knowledge-modeling outputs into measurable learning objectives, assessment evidence, rubrics, and an objective-activity-assessment alignment blueprint.

## Directory Tree

```text
3-目标与评价蓝图/
├── agents/
│   └── openai.yaml
├── CHANGELOG.md
├── CONTEXT.md
├── README.md
├── SKILL.md
└── test-prompts.json
```

## Quick Entry

Use `$lesson-objective-assessment-blueprint` after stages 1 and 2 have produced:

```text
projects/lesson/<项目名>/1-课程定位/course-positioning.md
projects/lesson/<项目名>/2-资料吸收与知识建模/research-source-inventory.md
projects/lesson/<项目名>/2-资料吸收与知识建模/knowledge-model.md
projects/lesson/<项目名>/2-资料吸收与知识建模/evidence-and-case-library.md
projects/lesson/<项目名>/2-资料吸收与知识建模/downstream-handoff.md
```

Canonical project outputs:

```text
projects/lesson/<项目名>/3-目标与评价蓝图/learning-objectives.md
projects/lesson/<项目名>/3-目标与评价蓝图/assessment-evidence-plan.md
projects/lesson/<项目名>/3-目标与评价蓝图/rubric-blueprint.md
projects/lesson/<项目名>/3-目标与评价蓝图/objective-activity-assessment-alignment.md
projects/lesson/<项目名>/3-目标与评价蓝图/downstream-handoff.md
```

This stage does not generate complete question banks, answers, lesson scripts, PPT copy, HTML pages, or DOC/PPT/HTML deliverables.

## Validation

```bash
python3 /Users/vincentlee/.codex/skills/meta/构建/技能/skill-2.0/scripts/validate_skill_2_0.py .agents/skills/lesson/3-目标与评价蓝图 --mode delivery
python3 /Users/vincentlee/.codex/skills/meta/构建/技能/skill-2.0/scripts/smoke_test_skill_2_0.py .agents/skills/lesson/3-目标与评价蓝图 --mode delivery
```
