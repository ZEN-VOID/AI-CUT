# lesson 8/ppt

`$lesson-delivery-ppt` generates PowerPoint/PPT delivery plans, slide deck structures, speaker notes, assembly manifests, and optional PPTX assembly targets from a parent delivery packet.

## Directory Tree

```text
ppt/
├── agents/
│   └── openai.yaml
├── CHANGELOG.md
├── CONTEXT.md
├── README.md
├── SKILL.md
└── test-prompts.json
```

## Quick Entry

Use `$lesson-delivery-ppt` when the target is PowerPoint, PPTX, slide deck, instructor presentation, workshop deck, or speaker notes under `projects/lesson/<项目名>/8-多端交付生成/ppt/`.

The active contract is in `SKILL.md`. Load `CONTEXT.md` with it. PPT writeback is limited to:

- `ppt-delivery-plan.md`
- `ppt-assembly-manifest.json`
- optional `.pptx`, HTML deck, or courseware artifacts generated, polished, exported, or verified through `.agents/skills/claude-design` from LLM-approved slide plans

When the request involves actual PPTX/courseware artifact generation, redesign, polish, export, or browser verification, this leaf must load `.agents/skills/claude-design/SKILL.md + .agents/skills/claude-design/CONTEXT.md`. Lesson owns the course truth, slide plan, speaker notes, and manifest; `claude-design` owns high-fidelity courseware/HTML deck visual execution, final artifact writeback, upstream design module selection, visual-system articulation, verification/export handoff, and quality verdict. Final artifact pass requires `artifact_paths` and `writeback_status`; if native PPTX export is unavailable, write the highest-fidelity source artifact and report the export blocker.

Scripts may only do PPT formatting, assembly, validation, export, and manifest writeback. They must not generate PPT 文案, replace the `claude-design` visual execution pass, or treat a generic deck without artifact writeback, visual-system, and quality-verdict evidence as complete.

## Validation

```bash
python3 /Users/vincentlee/.codex/skills/meta/构建/技能/skill-2.0/scripts/validate_skill_2_0.py .agents/skills/lesson/8-多端交付生成/ppt --mode delivery
python3 /Users/vincentlee/.codex/skills/meta/构建/技能/skill-2.0/scripts/smoke_test_skill_2_0.py .agents/skills/lesson/8-多端交付生成/ppt --mode delivery
```
