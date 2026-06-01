# Changelog

## 2026-05-30

- Aligned package with latest `skill-工作车间` Skill 2.0 delivery contract.
- Added `guardrails/guardrails-contract.md`, `types/type-map.md`, and `types/guardrail-setup.md`.
- Added `Input Contract`, `Multi-Subskill Continuous Workflow`, `Runtime Guardrails`, `Field Mapping`, and parser-friendly `Output Contract` fields to `SKILL.md`.
- Extended review gates with `security`, `runtime_behavior`, `integration`, `convergence`, fail-code registry, and convergence criteria.
- Added `Review Gate Mapping` to `references/chapter-polishing-contract.md`.

## 2026-04-29

- Added `subagent_review_optimize` mode for explicit subagents requests.
- Routed audit points through `.agents/skills/story/review` dimension child skills, then back into DeepSeek repair prompts.
- Tightened review, workflow, type, and evidence gates so subagents mode cannot stop at reports without same-round provider optimization.

## 2026-04-26

- Initialized `C-Deepseek流` as a Skill 2.0 chapter polishing provider path.
- Mirrored the intent of `B-Doubao流` while switching the actual creative engine to `.agents/skills/api/deepseek`.
- Added DeepSeek-specific context loading, provider evidence gates, system prompt, script bridge, and output contract.
- Fixed model/provider boundary to `deepseek-v4-pro` with default `thinking=enabled` and `reasoning_effort=high`.
