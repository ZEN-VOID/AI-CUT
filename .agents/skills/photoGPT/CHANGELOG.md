# Changelog

## 2026-05-11

- Clarified character-preservation wording for `多视图/角色` and `元素替换/换装|换角色|换脸`: prompts and gates must preserve original character appearance and makeup unchanged, not only identity.
- Clarified costume-preservation wording for `多视图/服装` and `元素替换/换装`: prompts and gates must name `服装样式和版型`, not only clothing.
- Synced prompt enhancement, type review, local review gate, context heuristic, and the affected JSON/README templates.

## 2026-05-05

- Restricted `photoGPT` provider handoff to `gpt-image-2` only.
- Added provider boundary checks that block nano-banana, InsightFace, inswapper, Photoshop generative edit, and other non-`gpt-image-2` providers.
- Updated prompt plan, review, workflow, context, README, and product metadata to require `imagegen_handoff.model: gpt-image-2`.

## 2026-04-26

- Converted all fourteen subtype templates and the output prompt-plan template from legacy Markdown carriers to JSON files, and updated all photoGPT routing references to the JSON template truth.
- Synced `templates/多视图` with the upgraded AIGC multiview subject template v1.2 semantics.
- Added short ASCII identity badge requirements, full-name record fallback, subject invariant locks, and post-overlay badge fallback to `场景`, `道具`, `服装`, and `角色` multiview templates.
- Added lower-left scene-view panel label requirements to `templates/多视图/场景/TEMPLATE.json`.
- Updated multiview README, type gates, review gates, and context heuristics for identity badge and scene panel label governance.

## 2026-04-25

- Initialized `photoGPT` as a Skill 2.0 package in place.
- Added type-first routing for `多视图`, `多图融合`, `风格化`, `修图`, and `元素替换`.
- Added prompt templates derived from nano-banana 元素替换、修图和多视图 best practices, then normalized them into the Chinese subtype taxonomy.
- Added imagegen handoff contract, review gate, README, product metadata, and non-creative scripts boundary.
- Migrated root-level English template files into the user-provided Chinese template taxonomy: `多视图`, `多图融合`, `风格化`, `修图`, and `元素替换`.
