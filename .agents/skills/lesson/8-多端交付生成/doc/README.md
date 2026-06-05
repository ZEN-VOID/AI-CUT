# lesson 8/doc

`$lesson-delivery-doc` generates Word/DOC delivery plans, document assembly manifests, and optional DOCX assembly targets from a parent delivery packet.

## Directory Tree

```text
doc/
├── agents/
│   └── openai.yaml
├── CHANGELOG.md
├── CONTEXT.md
├── README.md
├── SKILL.md
└── test-prompts.json
```

## Quick Entry

Use `$lesson-delivery-doc` when the target is a Word document, learner handout, instructor guide, course manual, or DOCX export under `projects/lesson/<项目名>/8-多端交付生成/doc/`.

The active contract is in `SKILL.md`. Load `CONTEXT.md` with it. DOC writeback is limited to:

- `doc-delivery-plan.md`
- `doc-assembly-manifest.json`
- optional `.docx` artifacts assembled from LLM-approved content

Scripts may only do Word formatting, assembly, validation, export, and manifest writeback. They must not generate course正文.

## Validation

```bash
python3 /Users/vincentlee/.codex/skills/meta/构建/技能/skill-2.0/scripts/validate_skill_2_0.py .agents/skills/lesson/8-多端交付生成/doc --mode delivery
python3 /Users/vincentlee/.codex/skills/meta/构建/技能/skill-2.0/scripts/smoke_test_skill_2_0.py .agents/skills/lesson/8-多端交付生成/doc --mode delivery
```
