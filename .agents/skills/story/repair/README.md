# story-repair

`story-repair` 管理小说项目中“局部修改牵动整体”的判定、执行分流与验收。

## Directory Tree

```text
repair/
├── guardrails/
│   └── guardrails-contract.md
├── references/
│   ├── impact-scope-contract.md
│   └── source-truth-ledger.md
├── scripts/
│   └── README.md
├── templates/
│   └── output-template.md
├── review/
│   └── review-contract.md
├── knowledge-base/
│   └── repair-heuristics.md
├── types/
│   ├── type-map.md
│   ├── scope/locality.md
│   ├── scope/clue-thread.md
│   ├── scope/character-state.md
│   ├── scope/mechanism.md
│   ├── scope/chapter-event.md
│   ├── scope/timeline-place.md
│   ├── scope/tone-contract.md
│   ├── scope/structure-topology.md
│   ├── scope/accepted-truth.md
│   ├── operation/plan-only.md
│   ├── operation/execute.md
│   └── acceptance/review-gate.md
├── agents/
│   └── openai.yaml
├── CHANGELOG.md
├── SKILL.md
├── CONTEXT.md
├── test-prompts.json
└── README.md
```

## Quick Entry

Use `$story-repair` for story project repair requests that require typed impact mapping across settings, planning, drafts, polish, review, return, state, and future generation constraints.

The universal "when X, check X" matrix lives in `references/impact-scope-contract.md`; project-specific additions belong in `projects/story/<项目名>/CONTEXT/` or `MEMORY.md` only when they are stable project memory.

Runtime safety boundaries live in `guardrails/guardrails-contract.md`; the short execution copy is embedded in `SKILL.md#Runtime Guardrails`.

Runtime nodes, routes, gates, Mermaid topology, module authorization, and fail-code convergence now live in `SKILL.md`; `steps/` is intentionally absent in the runtime-spine layout.
