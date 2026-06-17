# CHANGELOG

## 2026-06-17

- Strengthened the libTV canvas-to-project local canonical ensure contract: every scene subject image generated, reused, or uploaded on any episode canvas must have a same-stem local asset in `projects/aigc/<项目名>/3-主体/场景/3-生成/`; use `libtv download` only when the local asset is missing.
- Updated review, types, templates, references and CONTEXT with `local_sync_status`, `local_asset_path`, `download_command` evidence fields and the `FAIL-SCENE-GEN-LOCAL-SYNC` gate.
- Refined the local sync wording: when the local canonical same-stem asset already exists, skip download/copy and record `already_present`; run `libtv download` or copy only when the local asset is missing.

## 2026-06-16

- 升级 `$aigc-scene-generation` 到 runtime-spine Skill 2.0 口径，在旧正文末尾追加 `Skill 2.0 Runtime-Spine Upgrade` 控制块。
- 补齐 Type Routing、Thinking-Action Node Map、Module Loading/Trigger、Convergence、Review Gate、Quant、Attention、Checkpoint 与 Learning。
- 新增 `test-prompts.json`，覆盖完整生成、main_only 和缺 JSON repair。

## 2026-05-01

- 将生成资产命名合同调整为 `<主体ID>-<主体名称>-主图/多视图`，并要求 JSON 记录 `subject_id` 与 `subject_id_source`。
- 强化主图到多视图的本地参照图规则：Step2 使用本地主图作为 reference image 时，必须先 `同画布主图节点` 进入对话上下文，并在 JSON / 报告记录 `reference_context_status`。

## 2026-04-30

- Updated main-image and multi-view prompt templates so the source imported into Midjourney V8.1 is upstream `4. 解构`, not the former English integrated prompt.

## 2026-04-26

- Upgraded `templates/scene-multiview-prompt.json` to v1.2 with a required identity badge and lower-left panel view labels.
- Upgraded `templates/scene-multiview-prompt.json` to v1.1 as a spatial proof sheet template.
- Added `subject_invariant_lock`, domain view grammar, drift controls and review focus fields for scene continuity.

## 2026-04-25

- Initialized `$aigc-scene-generation` as a Skill 2.0 package.
- Added root `SKILL.md`, `CONTEXT.md`, `README.md`, and `CHANGELOG.md`.
- Added canonical Skill 2.0 partitions: `references/`, `SKILL.md` runtime spine, `review/`, `types/`, `knowledge-base/`, `templates/`, `scripts/`, and `agents/`.
- Added `templates/scene-main-image-prompt.json` for Step1 main-image prompt JSON alignment.
- Reworked the legacy scene panel prompt idea into `templates/scene-multiview-prompt.json` for Step2 multi-view scene generation.
- Completed workshop alignment pass: added Mermaid visual maps, steps topology, branch matrix, review dispatch matrix, local_checklist report fields, evidence-chain diagram, and README anchors.
