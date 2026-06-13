# CHANGELOG

## 2026-06-13

- Added artifact writeback requirements for real HTML/PPT/courseware outputs: leaf handoffs must now require `artifact_paths`, `writeback_status`, and explicit blockers when no file can be written.
- Upgraded the `claude-design` handoff from executor presence to design-excellence evidence: selected modules, visual system, verification/export evidence, and quality verdict are now required for real HTML/PPT/courseware artifacts.
- Extended the parent-level design executor rule from HTML-only to HTML plus PPT/courseware artifact generation, redesign, polish, export, and browser verification.
- Added `visual_artifact_delivery` routing, `claude-design` module trigger coverage, and `FIELD-LESSON-DEL-09` gate evidence for automatic leaf handoff.
- Synced README, CONTEXT, agent metadata, and test prompts with the `.agents/skills/claude-design` executor and artifact writeback rule.

## 2026-06-07

- Added the parent-level HTML artifact handoff rule: HTML leaf packets must declare `.agents/skills/claude-design` as the design executor when real HTML/static-site output is requested.
- Clarified that the delivery parent keeps course truth and leaf routing, while HTML visual execution belongs to the HTML leaf plus `claude-design`.
- Synced `agents/openai.yaml` and test prompts with the HTML executor routing rule.

## 2026-06-05

- Created `lesson-delivery` as a Skill 2.0 runtime-spine stage package.
- Defined parent ownership for `delivery-plan.md`, `delivery-manifest.json`, and doc/ppt/html leaf routing.
- Declared LLM-first delivery authorship and limited scripts to format conversion, assembly, validation, and manifest writeback.
- Kept the package on core layout only, without `review/`, `steps/`, or optional modules.
