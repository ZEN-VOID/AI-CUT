# Changelog

## 2026-06-13

- Completed Skill 2.0 runtime-spine upgrade coverage for `Core Task Contract`, `Context Processing Contract`, `LLM-First Creative Authorship Contract`, `Visual Maps`, and `Execution Contract`.
- Expanded module authorization from a broad `references/` row to explicit upstream reference files and the sibling imagegen bridge.
- Added review gates, field mappings, context heuristics, prompts, README notes, and agent metadata for `loaded_context_manifest`, LLM-first authorship evidence, and script/template boundary checks.
- Added an Artifact Writeback Contract requiring real artifact file creation/update or explicit `writeback_status=blocked` evidence for artifact tasks.
- Added a Design Excellence Contract requiring relevant upstream module selection, visible design systems, meaningful variants when direction is unlocked, and browser verification.
- Added a Lesson Handoff Contract so lesson HTML/PPT/courseware delivery uses `claude-design` as a high-fidelity design executor without changing lesson source truth.
- Added an Image Asset Generation Bridge so PPT/HTML/courseware artifact builds can call `.agents/skills/cli/imagegen` for needed bitmap assets, persist generated files in the workspace, and return asset-generation evidence.
- Added a style-adaptation gate for generated assets so imagegen handoffs derive `style_adaptation_profile` from the artifact visual system and reject mismatched image styles.
- Updated adapter context, README, agent metadata, and test prompts to treat generic functional output or target-path-only handoff as a design/writeback failure.

## 2026-06-06

- Installed upstream `jiji262/claude-design-skill` at commit `f1ac87c3decb175d99a269f23ca84860786a598b`.
- Added Codex Skill 2.0 adapter files: `SKILL.md`, `CONTEXT.md`, `README.md`, `agents/openai.yaml`, and `test-prompts.json`.
- Preserved upstream materials under `references/upstream/`.
