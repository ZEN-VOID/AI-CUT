# Story Resume

`story-resume` 是 story2026 的中断恢复卫星技能，负责检测真实断点、归一化安全恢复选项并回接唯一下一入口。它不拥有正文、规划、stage acceptance 或 context return 的业务真源。

## Directory Tree

```text
resume/
├── references/
│   ├── legacy-migration-matrix.md
│   ├── system-data-flow.md
│   └── workflow-resume.md
├── scripts/
│   └── README.md
├── templates/
│   └── output-template.md
├── review/
│   ├── review-contract.md
│   └── resume-review-gate.md
├── knowledge-base/
│   └── resume-heuristics.md
├── types/
│   └── resume-type-map.md
├── agents/
│   └── openai.yaml
├── CHANGELOG.md
├── CONTEXT.md
├── README.md
├── SKILL.md
└── test-prompts.json
```

## Quick Entry

1. Load `SKILL.md` and same-directory `CONTEXT.md`.
2. Resolve `PROJECT_ROOT` with the shared story CLI.
3. Run or consume `workflow detect`.
4. Apply the `SKILL.md` runtime spine, with `types/resume-type-map.md` and `review/resume-review-gate.md` only when authorized by the module trigger table.
5. Output a recovery decision package using `templates/output-template.md`.

## Validation

```bash
python3 /Users/vincentlee/.codex/skills/meta/构建/技能/skill-2.0/scripts/validate_skill_2_0.py .agents/skills/story/resume --mode delivery
python3 /Users/vincentlee/.codex/skills/meta/构建/技能/skill-2.0/scripts/smoke_test_skill_2_0.py .agents/skills/story/resume --mode delivery
```
