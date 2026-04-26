# Story Loopback

`story-loopback` performs PASS-gated volume actualization for `story2026`.

## Directory Tree

```text
5-Loopback/
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
- Confirm `PASS + handoff_to_review_and_loopback + review/ + 5-Loopback`.
- Run the node network in `steps/loopback-workflow.md`.
- Emit `projects/story/<项目名>/5-Loopback/第V卷.loopback.json`.

## Runtime Scripts

Shared mechanical helpers live in `../scripts/loopback_manager.py` and `../scripts/workflow_manager.py`.
