# CHANGELOG

## 2026-06-13

- Added final PPT/courseware artifact writeback gates requiring `artifact_paths` and `writeback_status`; target-path-only handoff is no longer passable.
- Upgraded real PPT/courseware artifact delegation to require `claude-design` selected modules, a visible visual system, verification/export evidence, and quality verdict before pass.
- Added mandatory `.agents/skills/claude-design` delegation for real PPT/courseware artifact generation, redesign, polish, export, and browser verification.
- Extended the PPT schema with `PPT-08-design-executor` so the leaf preserves lesson truth while `claude-design` owns high-fidelity courseware/HTML deck execution.
- Synced README, CONTEXT, agent metadata, and test prompts with the `claude-design` artifact executor rule.

## 2026-06-05

- Created `lesson-delivery-ppt` as a Skill 2.0 runtime-spine leaf package.
- Defined PPT/PowerPoint ownership for slide delivery plans, speaker notes, assembly manifests, and optional PPTX conversion targets.
- Declared LLM-first PPT authorship and limited scripts to formatting, assembly, validation, export, and manifest writeback.
- Kept the package on core layout only, without `review/`, `steps/`, or optional modules.
