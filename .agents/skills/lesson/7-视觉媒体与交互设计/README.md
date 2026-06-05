# lesson 7-视觉媒体与交互设计

`$lesson-visual-media-interaction` turns lesson stages 3-6 into visual media and interaction design guidance for downstream DOC/PPT/HTML delivery.

## Directory Tree

```text
7-视觉媒体与交互设计/
├── agents/
│   └── openai.yaml
├── CHANGELOG.md
├── CONTEXT.md
├── README.md
├── SKILL.md
└── test-prompts.json
```

## Quick Entry

Use `$lesson-visual-media-interaction` after stages 3-6 have produced learning objectives, course architecture, lesson content, activities, exercises, assessments, or equivalent briefs.

Canonical project outputs:

```text
projects/lesson/<项目名>/7-视觉媒体与交互设计/visual-system.md
projects/lesson/<项目名>/7-视觉媒体与交互设计/media-asset-brief.md
projects/lesson/<项目名>/7-视觉媒体与交互设计/diagram-and-infographic-plan.md
projects/lesson/<项目名>/7-视觉媒体与交互设计/interaction-model.md
projects/lesson/<项目名>/7-视觉媒体与交互设计/accessibility-requirements.md
projects/lesson/<项目名>/7-视觉媒体与交互设计/delivery-visual-constraints.md
projects/lesson/<项目名>/7-视觉媒体与交互设计/downstream-handoff.md
```

This stage does not generate `.pptx`, `.html`, `.docx`, final slides, final web pages, lesson scripts, or question banks.

## Validation

```bash
python3 /Users/vincentlee/.codex/skills/meta/构建/技能/skill-2.0/scripts/validate_skill_2_0.py .agents/skills/lesson/7-视觉媒体与交互设计 --mode delivery
python3 /Users/vincentlee/.codex/skills/meta/构建/技能/skill-2.0/scripts/smoke_test_skill_2_0.py .agents/skills/lesson/7-视觉媒体与交互设计 --mode delivery
```
