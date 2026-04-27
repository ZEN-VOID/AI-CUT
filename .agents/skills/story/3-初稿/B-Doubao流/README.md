# story-drafting-doubao

`story-drafting-doubao` 是 `story2026` 的 `3-初稿` 阶段 Doubao provider 技能，负责把章节 planning、全局卡、风格卡、`north_star`、项目记忆、项目上下文与上一章承接转成 canonical 章节正文。

## Directory Tree

```text
3-初稿/B-Doubao流/
├── references/
│   └── chapter-drafting-contract.md
├── scripts/
│   └── write_chapter_via_doubao.py
├── templates/
│   ├── chapter-root.template.md
│   ├── doubao-system-prompt.md
│   └── output-template.md
├── review/
│   └── review-contract.md
├── steps/
│   └── chapter-drafting-workflow.md
├── knowledge-base/
│   └── drafting-heuristics.md
├── types/
│   ├── type-map.md
│   └── 网文/
├── agents/
│   └── openai.yaml
├── CHANGELOG.md
├── CONTEXT.md
├── README.md
└── SKILL.md
```

## Quick Entry

```bash
python3 .agents/skills/story/3-初稿/B-Doubao流/scripts/write_chapter_via_doubao.py \
  --project-root "projects/story/<项目名>" \
  --chapter 12 \
  --mode chapter_draft
```

Dry run:

```bash
python3 .agents/skills/story/3-初稿/B-Doubao流/scripts/write_chapter_via_doubao.py \
  --project-root "projects/story/<项目名>" \
  --chapter 12 \
  --dry-run
```

When the target chapter already exists, formal writeback requires explicit `--mode chapter_rewrite / chapter_continue / local_repair` plus `--force`. The script injects the existing chapter into the provider context before overwriting and does not write extra sidecar files by default.

## Truth Boundary

- `SKILL.md` owns entry, routing, loading, provider boundary, root-cause and output contract.
- `references/` owns detailed chapter drafting rules.
- `steps/` owns the thinking-action workflow.
- `types/` owns mode classification.
- `review/` owns quality gates.
- `scripts/` only provides mechanical assistance and must not replace LLM creative authorship.
