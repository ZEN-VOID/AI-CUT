# lesson-benchmark

`$lesson-benchmark` compares a lesson project with reference courses, competitors, standards, rubrics, platform courses, or training exemplars. It returns benchmark evidence, gap matrices, tradeoff recommendations, and owning stage improvement routes.

It is a lesson satellite skill. It does not write stage canonical drafts, copy competitor course body, replace review gates, or generate DOC/PPT/HTML deliverables.

## Directory Tree

```text
benchmark/
├── agents/
│   └── openai.yaml
├── CHANGELOG.md
├── CONTEXT.md
├── README.md
├── SKILL.md
└── test-prompts.json
```

## Quick Entry

Use `$lesson-benchmark` when a user asks to benchmark a courseware project against excellent courses, competitors, industry standards, exam standards, teaching rubrics, platform courses, or enterprise training examples.

The active contract is in `SKILL.md`. Load `CONTEXT.md` with it, then load the lesson root router before touching any `projects/lesson/<项目名>/` context.

## Output Boundary

Default output is a structured benchmark packet in the current conversation. If the user asks to save a report, use:

```text
projects/lesson/<项目名>/benchmark/benchmark-report-YYYYMMDD.md
```

When no project is bound, use:

```text
reports/lesson-benchmark-YYYYMMDD.md
```

The report is evidence and route material only. Owning lesson stages remain responsible for canonical course outputs.

## Validation

```bash
python3 /Users/vincentlee/.codex/skills/meta/构建/技能/skill-2.0/scripts/validate_skill_2_0.py .agents/skills/lesson/benchmark --mode delivery
python3 /Users/vincentlee/.codex/skills/meta/构建/技能/skill-2.0/scripts/smoke_test_skill_2_0.py .agents/skills/lesson/benchmark --mode delivery
```
