# CHANGELOG

## 2026-06-07

- Added the parent-level HTML artifact handoff rule: HTML leaf packets must declare `.agents/skills/claude-design` as the design executor when real HTML/static-site output is requested.
- Clarified that the delivery parent keeps course truth and leaf routing, while HTML visual execution belongs to the HTML leaf plus `claude-design`.
- Synced `agents/openai.yaml` and test prompts with the HTML executor routing rule.

## 2026-06-05

- Created `lesson-delivery` as a Skill 2.0 runtime-spine stage package.
- Defined parent ownership for `delivery-plan.md`, `delivery-manifest.json`, and doc/ppt/html leaf routing.
- Declared LLM-first delivery authorship and limited scripts to format conversion, assembly, validation, and manifest writeback.
- Kept the package on core layout only, without `review/`, `steps/`, or optional modules.
