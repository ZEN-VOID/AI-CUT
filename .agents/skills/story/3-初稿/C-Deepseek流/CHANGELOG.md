# Changelog

## 2026-04-27

- Standardized repair authorship: `local_repair`, `chapter_rewrite`, review返工和卷级修复优化仍必须由 DeepSeek provider 执行正文创作性改写。
- Clarified that GPT/subagents in repair mode only own diagnosis, repair brief, prompt constraints, verification, and aggregation.
- Added gates requiring DeepSeek repair messages/provider reports before a repaired draft can still be claimed as `C-Deepseek流` output.

## 2026-04-26

- Initialized `C-Deepseek流` as a Skill 2.0 chapter drafting provider path.
- Mirrored the intent of `B-Doubao流` while switching the actual creative engine to `.agents/skills/api/deepseek`.
- Added DeepSeek-specific context loading, provider evidence gates, system prompt, script bridge, and output contract.
- Fixed model/provider boundary to `deepseek-v4-pro` with default `thinking=enabled` and `reasoning_effort=high`.
