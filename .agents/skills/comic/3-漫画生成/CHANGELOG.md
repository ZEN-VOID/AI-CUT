# Changelog: 漫画生成

## 2026-04-27

- Upgraded the package to the full Skill 2.0 layout required by `skill-工作车间`.
- Changed the default generation runtime from Codex built-in `image_gen` / legacy provider wording to `.agents/skills/cli/imagegen`.
- Added typed execution routing, thinking-action workflow, review gate, output template, knowledge-base notes, README, and CLI imagegen runner.
- Preserved Seedream and Dreamina as explicit legacy/fallback paths only.
