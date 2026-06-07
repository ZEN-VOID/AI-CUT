# CHANGELOG

## 2026-06-07

- Added the HTML artifact handoff rule: stage 7 must not generate `.html` directly, and must route actual HTML generation through `8-多端交付生成/html -> .agents/skills/claude-design`.
- Updated the visual delivery and downstream handoff schemas to include the `claude-design` executor route for HTML artifacts.
- Synced `agents/openai.yaml` and test prompts to the same HTML handoff boundary.

## 2026-06-05

- Implemented `7-视觉媒体与交互设计` as `lesson-visual-media-interaction`, a Skill 2.0 runtime-spine stage package.
- Fixed upstream inputs as lesson stages 3-6 and defined the stage boundary before `8-多端交付生成`.
- Added LLM-first authorship rules that prohibit scripts, templates, regex patterns, batch insertion, and mapping projection from generating visual, media, interaction, or accessibility design text.
- Fixed canonical outputs as:
  - `visual-system.md`
  - `media-asset-brief.md`
  - `diagram-and-infographic-plan.md`
  - `interaction-model.md`
  - `accessibility-requirements.md`
  - `delivery-visual-constraints.md`
  - `downstream-handoff.md`
- Added `SKILL.md`, `CONTEXT.md`, `README.md`, `agents/openai.yaml`, and `test-prompts.json`.
