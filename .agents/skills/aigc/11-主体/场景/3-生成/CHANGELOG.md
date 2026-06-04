# CHANGELOG

## 2026-05-01

- 将生成资产命名合同调整为 `<主体ID>-<主体名称>-主图/多视图`，并要求 JSON 记录 `subject_id` 与 `subject_id_source`。
- 强化主图到多视图的本地参照图规则：Step2 使用本地主图作为 reference image 时，必须先 `view_image` 进入对话上下文，并在 JSON / 报告记录 `reference_context_status`。

## 2026-04-30

- Updated main-image and multi-view prompt templates so the source imported into gpt-image-2 is upstream `4. 解构`, not the former English integrated prompt.

## 2026-04-26

- Upgraded `templates/scene-multiview-prompt.json` to v1.2 with a required identity badge and lower-left panel view labels.
- Upgraded `templates/scene-multiview-prompt.json` to v1.1 as a spatial proof sheet template.
- Added `subject_invariant_lock`, domain view grammar, drift controls and review focus fields for scene continuity.

## 2026-04-25

- Initialized `$aigc-scene-generation` as a Skill 2.0 package.
- Added root `SKILL.md`, `CONTEXT.md`, `README.md`, and `CHANGELOG.md`.
- Added canonical Skill 2.0 partitions: `references/`, `steps/`, `review/`, `types/`, `knowledge-base/`, `templates/`, `scripts/`, and `agents/`.
- Added `templates/scene-main-image-prompt.json` for Step1 main-image prompt JSON alignment.
- Reworked the legacy scene panel prompt idea into `templates/scene-multiview-prompt.json` for Step2 multi-view scene generation.
- Completed workshop alignment pass: added Mermaid visual maps, steps topology, branch matrix, review dispatch matrix, local_checklist report fields, evidence-chain diagram, and README anchors.
