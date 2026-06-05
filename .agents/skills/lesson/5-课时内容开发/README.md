# lesson 5-课时内容开发

`$lesson-content-development` develops per-lesson teaching content, instructor scripts, learner materials, case explanations, key concept expansions, and media placeholders after lesson knowledge modeling, objectives, and course architecture are available.

## Directory Tree

```text
5-课时内容开发/
├── agents/
│   └── openai.yaml
├── CHANGELOG.md
├── CONTEXT.md
├── README.md
├── SKILL.md
└── test-prompts.json
```

## Quick Entry

Use `$lesson-content-development` after upstream stages have produced or supplied equivalents for:

- `2-资料吸收与知识建模`: evidence-backed facts, concepts, terms, cases, misconceptions, and dependencies.
- `3-目标与评价蓝图`: learning objectives, evaluation evidence, target depth, and success criteria.
- `4-教学策略与课程架构`: modules, lesson list, timing, strategy, and learning path.

Canonical project outputs:

```text
projects/lesson/<项目名>/5-课时内容开发/lesson-content-pack.md
projects/lesson/<项目名>/5-课时内容开发/instructor-script.md
projects/lesson/<项目名>/5-课时内容开发/learner-materials.md
projects/lesson/<项目名>/5-课时内容开发/case-and-concept-notes.md
projects/lesson/<项目名>/5-课时内容开发/media-placeholders.md
projects/lesson/<项目名>/5-课时内容开发/downstream-handoff.md
```

Without a project root, return draft Markdown and mark it as not formally written back.

This stage must not generate a complete activity question bank, visual system, DOC/PPT/HTML deliverables, or scripted/template-generated lesson prose. The active contract is in `SKILL.md`; load `CONTEXT.md` with it.

## Validation

```bash
python3 /Users/vincentlee/.codex/skills/meta/构建/技能/skill-2.0/scripts/validate_skill_2_0.py .agents/skills/lesson/5-课时内容开发 --mode delivery
python3 /Users/vincentlee/.codex/skills/meta/构建/技能/skill-2.0/scripts/smoke_test_skill_2_0.py .agents/skills/lesson/5-课时内容开发 --mode delivery
```
