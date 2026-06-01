# Changelog

## 2026-05-30

- Added latest Skill 2.0 runtime guardrails with permission boundaries, self-modification prohibitions, anti-injection rules, and violation response protocol.
- Converted `SKILL.md` Output Contract to validator-readable five-field bullets and added guardrail/provider references.
- Added `Review Gate Mapping` to chapter drafting reference rules and expanded review dimensions for security, runtime behavior, integration, and convergence.
- Reworked `types/type-map.md` to remove placeholder/glob paths and use concrete validator anchors while preserving dynamic题材目录 selection.
- Corrected DeepSeek provider references to skill-relative paths for loading simulation and smoke validation.

## 2026-04-27

- Standardized repair authorship: `local_repair`, `chapter_rewrite`, review返工和卷级修复优化仍必须由 DeepSeek provider 执行正文创作性改写。
- Clarified that GPT/subagents in repair mode only own diagnosis, repair brief, prompt constraints, verification, and aggregation.
- Added gates requiring DeepSeek repair messages/provider reports before a repaired draft can still be claimed as `C-Deepseek流` output.

## 2026-04-26

- Initialized `C-Deepseek流` as a Skill 2.0 chapter drafting provider path.
- Mirrored the intent of `B-Doubao流` while switching the actual creative engine to `.agents/skills/api/deepseek`.
- Added DeepSeek-specific context loading, provider evidence gates, system prompt, script bridge, and output contract.
- Fixed model/provider boundary to `deepseek-v4-pro` with default `thinking=enabled` and `reasoning_effort=high`.
