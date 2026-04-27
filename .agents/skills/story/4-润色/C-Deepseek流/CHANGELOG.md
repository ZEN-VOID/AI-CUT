# Changelog

## 2026-04-26

- Initialized `C-Deepseek流` as a Skill 2.0 chapter polishing provider path.
- Mirrored the intent of `B-Doubao流` while switching the actual creative engine to `.agents/skills/api/deepseek`.
- Added DeepSeek-specific context loading, provider evidence gates, system prompt, script bridge, and output contract.
- Fixed model/provider boundary to `deepseek-v4-pro` with default `thinking=enabled` and `reasoning_effort=high`.
