# Changelog: 漫画生成

## 2026-06-15

- Migrated the active comic-generation runtime from legacy CLI imagegen to `.agents/skills/cli/imagegen` built-in `image_gen` mode.
- Replaced JSONL/`generate-batch` active artifacts with `imagegen_handoff_plan.json`, `imagegen_prompt_set.json`, per-page prompt files, and project-persisted PNG outputs.
- Added `prepare_builtin_imagegen_comic_generation.py` as the active mechanical planner and moved the old CLI runner to `run_legacy_imagegen_cli_comic_generation.py`.
- Updated runtime policy, types, steps, review, template, metadata, README, context, and heuristics so CLI/API paths are explicit legacy/external only.

## 2026-04-27

- Upgraded the package to the full Skill 2.0 layout required by `skill-工作车间`.
- Changed the default generation runtime from Codex built-in `image_gen` / legacy provider wording to `.agents/skills/cli/imagegen`.
- Added typed execution routing, thinking-action workflow, review gate, output template, knowledge-base notes, README, and CLI imagegen runner.
- Preserved Seedream and Dreamina as explicit legacy/fallback paths only.
