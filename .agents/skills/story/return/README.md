# Story Return

`story-return` performs PASS-gated volume actualization for `story2026`.

## Directory Tree

```text
return/
├── references/
├── scripts/
├── templates/
├── review/
├── steps/
├── knowledge-base/
├── types/
├── agents/
│   └── openai.yaml
├── CHANGELOG.md
├── CONTEXT.md
├── README.md
└── SKILL.md
```

## Quick Entry

- Load `SKILL.md + CONTEXT.md`.
- Confirm `PASS + handoff_to_review_and_context_return + review/ + return`, accepting legacy `return` targets when present.
- Run the node network in `steps/context-return-workflow.md`.
- Emit `projects/story/<项目名>/context-return/第V卷.context-return.json`.

## Runtime Scripts

Shared mechanical helpers live in `../scripts/context_return_manager.py` and `../scripts/workflow_manager.py`.
