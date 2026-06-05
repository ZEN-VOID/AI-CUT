# lesson-learn

`$lesson-learn` absorbs external teaching methods, standards, reference courseware, documents, websites, videos, books, and lesson project experience into source-first learning packets and narrow improvement plans.

## Directory Tree

```text
learn/
├── agents/
│   └── openai.yaml
├── CHANGELOG.md
├── CONTEXT.md
├── README.md
├── SKILL.md
└── test-prompts.json
```

## Quick Entry

Use `$lesson-learn` when the request is about learning from external education materials or project experience, then mapping the result back to `.agents/skills/lesson/` without overwriting stage truth.

Typical outputs:

- `source_digest`
- `credibility/copyright/applicability decisions`
- `target_skill_map`
- `gap_matrix`
- `improvement_plan`
- `changed_files` and `audit_result` when writeback is authorized

The satellite does not directly write lesson positioning, knowledge models, learning objectives, course outlines, lesson scripts, assessments, visuals, DOC/PPT/HTML outputs, or `content-model/` bodies. Those remain owned by the corresponding lesson stages and leaves.

## Validation

```bash
python3 /Users/vincentlee/.codex/skills/meta/构建/技能/skill-2.0/scripts/validate_skill_2_0.py .agents/skills/lesson/learn --mode delivery
python3 /Users/vincentlee/.codex/skills/meta/构建/技能/skill-2.0/scripts/smoke_test_skill_2_0.py .agents/skills/lesson/learn --mode delivery
```
