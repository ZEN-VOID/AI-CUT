# 5-设计 / 2-设计 输出后审计占位合同

## Module Identity

- `module_type`: `stage-local-audit-placeholder`
- `primary_consumers`: `5-设计/2-设计` tranche parent、`场景`、`角色`、`道具`
- `target_scope`: 当前轮刚写出的 `2-设计` canonical 输出、projection、slot bundle、`_manifest.json` 与阶段 `validation-report.md` 的审计边界说明

## Purpose

本合同当前只承担停用说明，不再调度 `监制` closeout：

1. 明确 `2-4` 阶段首次落盘后的 refine 不再属于 `监制`
2. 保留 `slot bundle` 与 target bundle 的审计语义，供后续独立审计工作流复用
3. 防止旧 leaf 合同继续把 `roles.supervision` 当作输出后收尾 owner

它不再负责：

- 启动 reviewer subagents
- 对当前轮业务输出做 closeout patch
- 解析 `reviewer_source / used_subagents / patched_targets`

## Canonical Sources

- `projects/aigc/<项目名>/team.yaml`
- `.agents/skills/aigc/_shared/council-runtime/module-spec.md`
- `.agents/skills/aigc/_shared/council-runtime/team.template.yaml`
- `.agents/skills/aigc/5-设计/{场景,角色,道具}/references/design-slot-review-contract.md`
- `.agents/skills/aigc/5-设计/{场景,角色,道具}/scripts/resolve_design_slot_bundles.py`
- `.agents/skills/team/SKILL.md`

## Current Status

1. 当前文件保留为占位真源，但 `2-设计` 输出后不再进入 `监制强化`。
2. `team.yaml.roles.supervision` 在 `2-设计` 中只可作为前置 advisory 的来源，不得在本文件中升级成 post-write closeout。
3. 若当前轮存在落盘后的质量问题，只能写入阶段 `validation-report.md` 的 audit note，等待独立审计工作流接管。

## Slot Bundle Resolution

若未来独立审计工作流复用本文件，target bundle 仍应先按 `.agents/skills/aigc/5-设计/{场景,角色,道具}/references/design-slot-review-contract.md` 解析为：

1. `target files`
   - canonical truth
   - projection
   - `_manifest.json`
   - 按需阶段 `validation-report.md`
2. `slot bundles`
   - `场景`：`SCENE-BUNDLE-01~04`
   - `角色`：`ROLE-BUNDLE-01~04`
   - `道具`：`PROP-BUNDLE-01~04`

硬规则：

1. reviewer finding 应尽量回指 `bundle_id` 或对应 slot cluster，而不是只说“文件有问题”。
2. 若问题属于 `template_shape_drift`、renderer 漂移或 validator 失效，必须上报为 source-layer 问题，而不是只 patch 当前轮业务文件。
3. prompt 洁净与参照污染问题必须先 patch canonical prompt carrier，再同步 projection；不得靠裁切图片或 reviewer prose 兜底。
4. 默认执行载体是 `.agents/skills/aigc/5-设计/{场景,角色,道具}/scripts/resolve_design_slot_bundles.py`；若本轮无法把 target files 解析成 `slot_bundles`，必须先修 resolver 或 mapping，再进入 reviewer council。

## Boundary

1. `2-设计` 输出后的审计与验收，不再等同于 `5-设计` 阶段内的 `监制 refine`。
2. `roles.review.operates_on_final_stage_of` 若未来显式覆盖 `5-设计`，应归后续独立审计/验收设计处理；本占位合同不提前定义。
3. `source_skill_refs` 只提供 provenance / 领域提示，不提供 runtime 授权。

## Post-Write Rule

1. 不再解析 reviewer roster。
2. 不再定义 mode 与 dispatch。
3. 不再对当前轮 canonical truth、projection、`_manifest.json` 或 `validation-report.md` 做 `监制` 名义的 closeout patch。
4. 若发现源层治理问题，应直接报告为后续 task，而不是在本轮业务 closeout 中越权修规则。

## Target-Type Design Checks

- `场景`
  - `space_and_scale`
  - `material_and_texture`
  - `light_and_weather`
  - `blocking_and_wayfinding`
- `角色`
  - `silhouette_and_pose`
  - `costume_and_layering`
  - `face_hair_makeup`
  - `camera_readability`
- `道具`
  - `function_and_affordance`
  - `material_and_finish`
  - `state_trace`
  - `hand_relation_offscreen`
- `2-设计` 父层 / shared
  - `cross-leaf consistency`
  - `handoff readiness`
  - `design system coherence`

## Structured Audit Placeholder

```yaml
post_write_audit_note:
  team_yaml: "<path-or-null>"
  ownership: "audit-layer"
  supervision_status: "disabled-for-post-write-refine"
  slot_bundles: []
  slot_bundle_findings: []
  findings: []
  handoff_note: ""
```

## Verification Checklist

1. 当前轮已读取项目根 `team.yaml`
2. 已明确 `roles.supervision` 在 `2-设计` 中只作为前置 advisory
3. 未把 `source_skill_refs` 误当 runtime 授权或 post-write reviewer
4. 当前轮 target bundle 仍可从文件级解析到 slot bundle 级
5. 没有再从本合同触发 `监制` closeout patch 或 subagent dispatch
