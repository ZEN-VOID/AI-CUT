# story-polishing-deepseek

`story-polishing-deepseek` 是 `story2026` 的 `4-润色` 阶段 DeepSeek provider 技能，负责承接 `3-初稿` 章节，结合 planning、`north_star`、项目记忆与上下文，输出 canonical 章节最小局部修补稿。DeepSeek 在当前三模型分工中是默认润色 lane，用于长思维链判断、问题定位与克制的二次调优，而不是默认整章洗稿。

## Directory Tree

```text
4-润色/C-Deepseek流/
├── references/
│   └── chapter-polishing-contract.md
├── scripts/
│   └── polish_chapter_via_deepseek.py
├── templates/
│   ├── chapter-root.template.md
│   ├── deepseek-system-prompt.md
│   └── output-template.md
├── review/
│   └── review-contract.md
├── steps/
│   └── chapter-polishing-workflow.md
├── knowledge-base/
│   └── polishing-heuristics.md
├── types/
│   └── polishing-type-map.md
├── agents/
│   └── openai.yaml
├── CHANGELOG.md
├── CONTEXT.md
├── README.md
└── SKILL.md
```

## Quick Entry

```bash
python3 .agents/skills/story/4-润色/C-Deepseek流/scripts/polish_chapter_via_deepseek.py \
  --project-root "projects/story/<项目名>" \
  --chapter 12
```

Dry run:

```bash
python3 .agents/skills/story/4-润色/C-Deepseek流/scripts/polish_chapter_via_deepseek.py \
  --project-root "projects/story/<项目名>" \
  --chapter 12 \
  --dry-run
```

When the target chapter already exists, formal overwrite requires explicit `--mode polish_rewrite` plus `--force`. Use `--mode local_repair` for narrower fixes; do not treat an existing target as permission for whole-chapter rewrite.

## Truth Boundary

- `SKILL.md` owns entry, routing, loading, provider boundary, root-cause and output contract.
- `references/` owns detailed chapter polishing rules.
- `steps/` owns the thinking-action workflow.
- `types/` owns mode classification.
- `review/` owns quality gates.
- `scripts/` only provides mechanical assistance and must not replace LLM creative authorship.
