# story-polishing-gpt-native

`story-polishing-gpt-native` 是 `story2026` 的 `4-润色` 阶段 GPT 原生技能，负责承接 `3-初稿` 章节，结合 planning、`north_star`、项目记忆与上下文，输出 canonical 章节润色稿。

## Directory Tree

```text
4-润色/A-GPT原生/
├── references/
│   └── chapter-polishing-contract.md
├── scripts/
│   └── polish_chapter_gpt_native.py
├── templates/
│   ├── chapter-root.template.md
│   ├── gpt-native-system-prompt.md
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

Dry run context pack:

```bash
python3 .agents/skills/story/4-润色/A-GPT原生/scripts/polish_chapter_gpt_native.py \
  --project-root "projects/story/<项目名>" \
  --chapter 12 \
  --dry-run
```

Validate and write a GPT-polished chapter:

```bash
python3 .agents/skills/story/4-润色/A-GPT原生/scripts/polish_chapter_gpt_native.py \
  --project-root "projects/story/<项目名>" \
  --chapter 12 \
  --draft-file /path/to/gpt-authored-chapter.md
```

When the target chapter already exists, the script auto-selects `polish_rewrite` and injects the existing chapter into the context pack. Use `--mode local_repair` or `--mode local_repair` when the user intent is narrower.

## Truth Boundary

- `SKILL.md` owns entry, routing, loading, GPT-native boundary, root-cause and output contract.
- `references/` owns detailed chapter polishing rules.
- `steps/` owns the thinking-action workflow.
- `types/` owns mode classification.
- `review/` owns quality gates.
- `scripts/` only provides mechanical assistance and must not replace LLM creative authorship.
