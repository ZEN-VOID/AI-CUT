# Changelog

## 2026-05-30

- Aligned package with latest `skill-工作车间` Skill 2.0 delivery contract.
- Added `guardrails/guardrails-contract.md`, `types/type-map.md`, and `types/guardrail-setup.md`.
- Added `Input Contract`, `Multi-Subskill Continuous Workflow`, `Runtime Guardrails`, `Field Mapping`, and parser-friendly `Output Contract` fields to `SKILL.md`.
- Extended review gates with `security`, `runtime_behavior`, `integration`, `convergence`, fail-code registry, and convergence criteria.
- Added `Review Gate Mapping` to `references/chapter-polishing-contract.md`.

## 2026-04-29

- Added `subagent_review_optimize` mode for explicit subagents requests.
- Routed audit points through `.agents/skills/story/review` dimension child skills, then back into GPT-native direct optimization.
- Tightened review, workflow, type, and evidence gates so subagents mode cannot stop at reports without same-round prose repair.

## 2026-04-26

- Created `A-GPT原生` as a Skill 2.0 chapter polishing package aligned with `B-Doubao流`.
- Rewrote `SKILL.md` as an entry, routing, loading, root-cause and output contract for GPT-native creation.
- Split chapter polishing details into `references/`, workflow topology into `steps/`, type routing into `types/`, and quality gates into `review/`.
- Added GPT-native templates, `agents/openai.yaml`, `README.md`, and `templates/output-template.md`.
- Added `scripts/polish_chapter_gpt_native.py` for context pack assembly, LLM-authored draft validation and canonical writeback.
- Preserved the same canonical output path as `B-Doubao流`: `projects/story/<项目名>/4-润色/第N卷/第N章.md`.
