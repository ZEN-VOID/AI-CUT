# CHANGELOG

## 2026-06-07

- Added mandatory `.agents/skills/claude-design` delegation for real HTML artifact generation, redesign, polish, and browser verification.
- Extended the HTML schema with `HTML-08-design-executor` so the leaf preserves lesson truth while `claude-design` owns high-fidelity HTML execution.
- Synced `agents/openai.yaml` and test prompts with the `claude-design` artifact executor rule.

## 2026-06-05

- Created `lesson-delivery-html` as a Skill 2.0 runtime-spine leaf package.
- Defined HTML/web ownership for web delivery plans, page structures, site manifests, and optional static site targets.
- Declared LLM-first HTML authorship and limited scripts to assembly, resource copying, validation, export, and manifest writeback.
- Kept the package on core layout only, without `review/`, `steps/`, or optional modules.
