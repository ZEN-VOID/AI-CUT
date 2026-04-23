# 4-Design / 2-设计 Subagents 监制强化合同

## Module Identity

- `module_type`: `stage-local-shared-review-contract`
- `primary_consumers`: `4-Design/2-设计` tranche parent、`场景`、`角色`、`道具`
- `target_scope`: 当前轮刚写出的 `2-设计` canonical 输出、projection、slot bundle、`_manifest.json` 与按需阶段 `validation-report.md`

## Purpose

本合同把 `4-Design/2-设计` 的“输出后监制强化”收束为单一真源：

1. 读取项目根 `team.yaml`
2. 区分 `4-Design` 的 stage-end refine 与 final-stage review gate
3. 按显式成员、阶段 gate 与设计型补选规则匹配 `.agents/skills/team/` reviewer skill
4. 在 `runtime_policy.use_subagents_by_default == true` 时真实启动 reviewer subagents
5. 对当前轮业务输出文件及其 slot bundle 做定向评审、必要优化与主代理汇流

它参照但不复制：

- `.agents/skills/commands/subagetns/preview/SKILL.md`
- `.agents/skills/commands/subagetns/review/SKILL.md`

## Canonical Sources

- `projects/aigc/<项目名>/team.yaml`
- `.agents/skills/aigc/_shared/council-runtime/module-spec.md`
- `.agents/skills/aigc/_shared/council-runtime/team.template.yaml`
- `.agents/skills/aigc/4-Design/2-设计/_shared/design-slot-review-contract.md`
- `.agents/skills/aigc/4-Design/2-设计/_shared/scripts/resolve_design_slot_bundles.py`
- `.agents/skills/team/SKILL.md`
- `.agents/skills/commands/subagetns/preview/SKILL.md`
- `.agents/skills/commands/subagetns/review/SKILL.md`

## Trigger Gate

只有同时满足以下条件时，才进入监制强化：

1. 当前轮已写出 `2-设计` canonical 输出，至少包括 machine-first truth / Markdown projection / `_manifest.json`
2. 当前目标属于 `projects/aigc/<项目名>/4-Design/*/2-设计/` 或与之直接相关的当前轮业务输出文件
3. 当前项目未显式禁用顾问团，或用户已显式要求本轮启用 subagents 监制强化
4. 用户未显式禁止顾问团强化

若 `team.yaml.enabled == false`，但用户显式要求“启用 subagents 监制强化”，允许按 `manual override` 执行，并在结论中说明这次不是常驻运行时，而是人工触发复审。

图片状态只作为证据或 reviewer 输入，不是进入监制强化的 prerequisite。

## Slot Bundle Resolution

进入监制强化后，target bundle 必须先按 `.agents/skills/aigc/4-Design/2-设计/_shared/design-slot-review-contract.md` 解析为：

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
4. 默认执行载体是 `.agents/skills/aigc/4-Design/2-设计/_shared/scripts/resolve_design_slot_bundles.py`；若本轮无法把 target files 解析成 `slot_bundles`，必须先修 resolver 或 mapping，再进入 reviewer council。

## 4-Design Closeout Applicability

`2-设计` 的输出后监制强化，是 `4-Design` 阶段内的 stage-end refine，不等于整个 `4-Design` 的最终验收 gate。

当前轮 closeout 只要满足以下任一条件，即可视为允许进入：

1. `roles.supervision.operates_on` 包含 `4-Design`
2. 共享 `team.template.yaml` 明确把 `4-Design` 归于 `supervision`
3. 用户对当前轮输出显式要求执行 `subagents` 监制强化

若 `roles.review.operates_on_final_stage_of` 显式包含 `4-Design`，则它属于本阶段最终验收 gate 的 reviewer 来源，可并入当前轮 reviewer 池，但不取代 stage-end refine 的进入裁决。

`source_skill_refs` 只提供 provenance / 领域提示，不提供 runtime 授权。

## Reviewer Resolution

### 显式 reviewer

按以下优先级收集 reviewer，并只保留 `.agents/skills/team/**/SKILL.md`：

1. `roles.supervision.members`
2. `roles.review.members`（仅当 `roles.review.operates_on_final_stage_of` 显式包含 `4-Design`）
3. `team_setup.shared_agents`

### 非 reviewer 真源的处理

- `roles.supervision.source_skill_refs` 与 `roles.review.source_skill_refs` 默认只证明“该角色关联哪些阶段或领域”，不直接等同 reviewer skill。
- 只有在显式 reviewer 仍不足，且某个 `source_skill_refs` 条目本身就位于 `.agents/skills/team/` 下时，才允许把它作为最后兜底 reviewer 候选。

### 设计型补选

若显式 reviewer 不足以形成稳定 council，则根据目标类型补到 `2-4` 位：

| target_type | 首选补选 |
| --- | --- |
| `2-设计` 父层 / `_shared` / 跨 leaf 技能真源 | `设计组/张叔平` -> `美学组/叶锦添` |
| `场景` 输出或 `场景` leaf 真源 | `设计组/隈研吾` -> `美学组/叶锦添` |
| `角色` 输出或 `角色` leaf 真源 | `设计组/张叔平` -> `美学组/叶锦添` |
| `道具` 输出或 `道具` leaf 真源 | `设计组/张叔平` -> `美学组/叶锦添` |

补选规则：

1. 若 `roles.supervision.members` 已有显式监制成员，则保留在 reviewer 列表前部
2. 若 `roles.review.members` 显式承担 `4-Design` final-stage gate，则保留在显式 reviewer 池中
3. 设计型补选只补足缺口，不挤掉显式监制成员或显式 gate reviewer
4. 最终 reviewer 总数固定在 `2-4`
5. 补选必须在结论中标记为 `team-inferred-design`

## Mode And Dispatch

默认模式如下：

1. `runtime_policy.use_subagents_by_default == true` 且 reviewer 数为 `2-4`
   - 使用 `parallel-council`
2. reviewer 数为 `1`
   - 使用 `single-reviewer`
3. 只有在上层策略强制要求链式 refine 时
   - 才改为 `serial-refine`

只要当前环境真实支持 subagents，且没有更高优先级策略阻断，就必须真实起 reviewer subagents，而不是把本地顺序模拟伪装成 council。

## Execution Contract

1. 锁定本轮 target files，并解析当前轮对应的 slot bundles；只审当前轮业务输出，不扩大到无关目录
2. 为每个 reviewer skill 启动一个 subagent
3. 每个 reviewer 至少返回：
   - `core_judgment`
   - `key_risk`
   - `direct_patch_suggestion`
   - `patch_recommendation`
   - `design_checks`
   - `slot_bundle_findings`
4. 主代理负责 synthesis、冲突裁决与最终 patch
5. patch 顺序固定为：
   - 先 canonical truth
   - 再 Markdown projection
   - 再 `_manifest.json` / audit sidecar
   - 最后按需补 `projects/aigc/<项目名>/4-Design/validation-report.md` 的监制强化记录
6. 普通监制收尾只允许 patch 当前轮 canonical 输出、其 projection、`_manifest.json` 与阶段 `validation-report.md`；不得顺手改 `SKILL.md`、`CONTEXT.md`、command runbook 或 team 真源。
7. 若 reviewer 发现的是源层治理问题，必须单独报告为后续 source-layer task，而不是在本轮业务 closeout 中越权修规则。
8. reviewer 不得各自生成平行总稿，也不得越权改写 team 真源

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

## Structured Review Summary

```yaml
subagent_supervision_result:
  team_yaml: "<path-or-null>"
  reviewer_source: "team-explicit|team-explicit+review-gate|team-explicit+team-inferred-design|team-explicit+review-gate+team-inferred-design|team-inferred-design|manual-override"
  reviewers: []
  slot_bundles: []
  mode: "parallel-council|serial-refine|single-reviewer|degraded-local-review"
  used_subagents: true
  patched_targets: []
  key_findings: []
  design_checks: {}
  synthesis: ""
```

## Verification Checklist

1. 当前轮已读取项目根 `team.yaml`
2. 已先按 stage-end refine / final-stage gate 的分层判断当前轮 closeout 是否允许进入
3. 未把 `source_skill_refs` 误当 runtime 授权或默认 reviewer
4. reviewer 顺序与共享运行时一致，且 `4-Design` final-stage gate reviewer 仅在配置存在时并入
5. 显式成员不足时，已按目标类型补入设计型 reviewer
6. `use_subagents_by_default == true` 且环境支持时，已真实启动 subagents
7. 当前轮 target bundle 已从文件级解析到 slot bundle 级
8. 最终 patch 只作用于当前轮业务目标文件，没有制造第二真源
