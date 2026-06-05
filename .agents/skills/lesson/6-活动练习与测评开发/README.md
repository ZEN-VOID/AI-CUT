# lesson 6-活动练习与测评开发

`$lesson-assessment-development` develops activities, exercises, question banks, answer explanations, scoring guides, rubrics, and formative/summative assessment packages for lesson projects.

## Directory Tree

```text
6-活动练习与测评开发/
├── agents/
│   └── openai.yaml
├── CHANGELOG.md
├── CONTEXT.md
├── README.md
├── SKILL.md
└── test-prompts.json
```

## Quick Entry

Use `$lesson-assessment-development` after the upstream stages have produced or supplied equivalent materials:

```text
projects/lesson/<项目名>/3-目标与评价蓝图/
projects/lesson/<项目名>/4-教学策略与课程架构/
projects/lesson/<项目名>/5-课时内容开发/
```

Canonical project outputs:

```text
projects/lesson/<项目名>/6-活动练习与测评开发/activity-exercise-package.md
projects/lesson/<项目名>/6-活动练习与测评开发/question-bank.yaml
projects/lesson/<项目名>/6-活动练习与测评开发/scoring-rubrics.md
projects/lesson/<项目名>/6-活动练习与测评开发/answer-explanations.md
projects/lesson/<项目名>/6-活动练习与测评开发/assessment-package.md
projects/lesson/<项目名>/6-活动练习与测评开发/downstream-handoff.md
```

The stage consumes course objectives, architecture, and lesson content. It does not rewrite course architecture, lesson scripts, visual plans, or final DOC/PPT/HTML deliverables.

## Validation

```bash
python3 /Users/vincentlee/.codex/skills/meta/构建/技能/skill-2.0/scripts/validate_skill_2_0.py .agents/skills/lesson/6-活动练习与测评开发 --mode delivery
python3 /Users/vincentlee/.codex/skills/meta/构建/技能/skill-2.0/scripts/smoke_test_skill_2_0.py .agents/skills/lesson/6-活动练习与测评开发 --mode delivery
```
