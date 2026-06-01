# story-drafting-gpt-native

`story-drafting-gpt-native` 是 `story2026` 的 `3-初稿` 阶段 GPT 原生技能，负责把章节 planning、全局卡、风格卡、`north_star`、项目记忆、项目上下文与当前卷全部前序章承接转成 canonical 章节正文。

## Directory Tree

```text
3-初稿/A-GPT原生/
├── guardrails/
│   └── guardrails-contract.md
├── references/
│   └── chapter-drafting-contract.md
├── scripts/
│   └── write_chapter_gpt_native.py
├── templates/
│   ├── chapter-root.template.md
│   ├── gpt-native-system-prompt.md
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
│       └── README.md
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
python3 .agents/skills/story/3-初稿/A-GPT原生/scripts/write_chapter_gpt_native.py \
  --project-root "projects/story/<项目名>" \
  --chapter 12 \
  --dry-run
```

Validate and write a GPT-authored chapter:

```bash
python3 .agents/skills/story/3-初稿/A-GPT原生/scripts/write_chapter_gpt_native.py \
  --project-root "projects/story/<项目名>" \
  --chapter 12 \
  --draft-file /path/to/gpt-authored-chapter.md
```

When the target chapter already exists, the script auto-selects `chapter_rewrite` and injects the existing chapter into the context pack. Use `--mode chapter_continue` or `--mode local_repair` when the user intent is narrower.

## Truth Boundary

- `SKILL.md` owns entry, routing, loading, GPT-native boundary, root-cause and output contract.
- `references/` owns detailed chapter drafting rules.
- `steps/` owns the thinking-action workflow.
- `types/` owns mode classification.
- `review/` owns quality gates.
- `guardrails/` owns runtime permission boundaries and anti-injection rules.
- `scripts/` only provides mechanical assistance and must not replace LLM creative authorship.
