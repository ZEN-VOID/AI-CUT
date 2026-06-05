# lesson 1-课程定位

`$lesson-positioning` turns course intent, audience, usage context, constraints, references, and delivery requirements into a course positioning Markdown document.

## Directory Tree

```text
1-课程定位/
├── agents/
│   └── openai.yaml
├── CHANGELOG.md
├── CONTEXT.md
├── README.md
├── SKILL.md
└── test-prompts.json
```

## Quick Entry

Use `$lesson-positioning` when a course, lesson, training, or courseware project needs a positioning brief before source intake, objectives, architecture, content, exercises, visual design, or DOC/PPT/HTML delivery.

Supported input modes:

- Quick mode: the user provides enough complete information, materials, links, images, videos, or benchmark courses; automatically check or route upstream project initialization/recovery, parse evidence, write the positioning MD, and return downstream handoff without generating downstream artifacts.
- Dialog mode: the user has a rough idea or asks for help clarifying; ask questionnaire-style questions over multiple turns, then generate the MD.

Canonical project output:

```text
projects/lesson/<项目名>/1-课程定位/course-positioning.md
```

Without a project root, return a draft MD in the response and mark it as not formally written back.

Quick mode workflow automation includes:

- upstream project root readiness check and non-destructive init/resume route;
- source and benchmark evidence status inventory;
- canonical `course-positioning.md` writeback when project-bound;
- downstream handoff for `2-资料吸收与知识建模`, `3-目标与评价蓝图`, and `4-教学策略与课程架构`.

## Validation

```bash
python3 /Users/vincentlee/.codex/skills/meta/构建/技能/skill-2.0/scripts/validate_skill_2_0.py .agents/skills/lesson/1-课程定位 --mode delivery
python3 /Users/vincentlee/.codex/skills/meta/构建/技能/skill-2.0/scripts/smoke_test_skill_2_0.py .agents/skills/lesson/1-课程定位 --mode delivery
```
