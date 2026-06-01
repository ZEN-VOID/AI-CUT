# Changelog

## 2026-05-30

- Added latest Skill 2.0 runtime guardrails with permission boundaries, self-modification prohibitions, anti-injection rules, and violation response protocol.
- Converted `SKILL.md` Output Contract to validator-readable five-field bullets and added guardrail references.
- Added `Review Gate Mapping` to chapter drafting reference rules and expanded review dimensions for security, runtime behavior, integration, and convergence.
- Reworked `types/type-map.md` to remove placeholder/glob paths and use concrete validator anchors while preserving dynamic题材目录 selection.

## 2026-04-26

- Created `A-GPT原生` as a Skill 2.0 chapter drafting package aligned with `B-Doubao流`.
- Rewrote `SKILL.md` as an entry, routing, loading, root-cause and output contract for GPT-native creation.
- Split chapter drafting details into `references/`, workflow topology into `steps/`, type routing into `types/`, and quality gates into `review/`.
- Added GPT-native templates, `agents/openai.yaml`, `README.md`, and `templates/output-template.md`.
- Added `scripts/write_chapter_gpt_native.py` for context pack assembly, LLM-authored draft validation and canonical writeback.
- Preserved the same canonical output path as `B-Doubao流`: `projects/story/<项目名>/3-初稿/第N卷/第N章.md`.
