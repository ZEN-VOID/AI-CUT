# story-drafting-deepseek

`story-drafting-deepseek` 是 `story2026` 的 `3-初稿` 阶段 DeepSeek provider 技能，负责把章节 planning、全局卡、风格卡、`north_star`、项目记忆、项目上下文与上一章承接转成 canonical 章节正文。

## Directory Tree

```text
3-初稿/C-Deepseek流/
├── references/
│   └── chapter-drafting-contract.md
├── scripts/
│   └── write_chapter_via_deepseek.py
├── templates/
│   ├── chapter-root.template.md
│   ├── deepseek-system-prompt.md
│   └── output-template.md
├── review/
│   └── review-contract.md
├── steps/
│   └── chapter-drafting-workflow.md
├── knowledge-base/
│   └── drafting-heuristics.md
├── types/
│   └── drafting-type-map.md
├── agents/
│   └── openai.yaml
├── CHANGELOG.md
├── CONTEXT.md
├── README.md
└── SKILL.md
```

## Quick Entry

```bash
python3 .agents/skills/story/3-初稿/C-Deepseek流/scripts/write_chapter_via_deepseek.py \
  --project-root "projects/story/<项目名>" \
  --chapter 12
```

Dry run:

```bash
python3 .agents/skills/story/3-初稿/C-Deepseek流/scripts/write_chapter_via_deepseek.py \
  --project-root "projects/story/<项目名>" \
  --chapter 12 \
  --dry-run
```

When the target chapter already exists, the script auto-selects `chapter_rewrite` and injects the existing chapter into the provider context. Use `--mode chapter_continue` or `--mode local_repair` when the user intent is narrower.

## Truth Boundary

- `SKILL.md` owns entry, routing, loading, provider boundary, root-cause and output contract.
- `references/` owns detailed chapter drafting rules.
- `steps/` owns the thinking-action workflow.
- `types/` owns mode classification.
- `review/` owns quality gates.
- `scripts/` only provides mechanical assistance and must not replace LLM creative authorship.
