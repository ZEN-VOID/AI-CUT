# story-polishing-doubao

`story-polishing-doubao` 是 `story2026` 的 `4-润色` 阶段 Doubao provider 技能，负责承接 `3-初稿` 章节，结合 planning、`north_star`、项目记忆与上下文，输出 canonical 章节最小局部修补稿。Doubao 在当前三模型分工中默认承担 `3-初稿` 的中文气口与人话起稿；进入 `4-润色` 时只在用户显式点名 Doubao 或做对照实验时使用。

## Directory Tree

```text
4-润色/B-Doubao流/
├── guardrails/
│   └── guardrails-contract.md
├── references/
│   └── chapter-polishing-contract.md
├── scripts/
│   └── polish_chapter_via_doubao.py
├── templates/
│   ├── chapter-root.template.md
│   ├── doubao-system-prompt.md
│   └── output-template.md
├── review/
│   └── review-contract.md
├── steps/
│   └── chapter-polishing-workflow.md
├── knowledge-base/
│   └── polishing-heuristics.md
├── types/
│   ├── guardrail-setup.md
│   ├── polishing-type-map.md
│   └── type-map.md
├── agents/
│   └── openai.yaml
├── CHANGELOG.md
├── CONTEXT.md
├── README.md
└── SKILL.md
```

## Quick Entry

```bash
python3 .agents/skills/story/4-润色/B-Doubao流/scripts/polish_chapter_via_doubao.py \
  --project-root "projects/story/<项目名>" \
  --chapter 12 \
  --mode chapter_polish
```

Dry run:

```bash
python3 .agents/skills/story/4-润色/B-Doubao流/scripts/polish_chapter_via_doubao.py \
  --project-root "projects/story/<项目名>" \
  --chapter 12 \
  --dry-run
```

When the target chapter already exists, formal overwrite requires explicit `--mode polish_rewrite` plus `--force`. Use `--mode local_repair` for narrower fixes. The script injects the existing chapter into the provider context before overwriting and does not write extra sidecar files by default.

## Truth Boundary

- `SKILL.md` owns entry, routing, loading, provider boundary, root-cause and output contract.
- `references/` owns detailed chapter polishing rules.
- `steps/` owns the thinking-action workflow.
- `types/` owns mode classification.
- `review/` owns quality gates.
- `guardrails/` owns runtime permissions, provider identity boundaries, injection defense and violation response.
- `scripts/` only provides mechanical assistance and must not replace LLM creative authorship.
