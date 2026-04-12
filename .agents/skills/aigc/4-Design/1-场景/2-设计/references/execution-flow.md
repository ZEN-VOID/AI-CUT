# 输入与上下文装配

## 必需输入

1. `projects/<项目名>/4-Design/1-场景/1-清单/第N集/第N集.json`
2. `projects/<项目名>/2-Global/全局风格.md`
3. `projects/<项目名>/2-Global/类型指导.md`
4. `projects/<项目名>/2-Global/导演意图.md`

## 补充输入

1. `projects/<项目名>/3-Detail/第N集.json`
2. `projects/<项目名>/3-Detail/第N集.json`
3. `projects/<项目名>/0-Init/north_star.yaml`
4. `projects/<项目名>/0-Init/init_handoff.yaml`

## 上下文裁剪规则

- `设计统筹`：拿到全量 scene catalog、全局风格和导演意图。
- `空间逻辑`：拿到目标场景的 `scene entry + group_scene_map + relevant shots`。
- `建筑设计师`：在 `空间逻辑` 输出后读取空间原型、时代约束、风格底座。
- `布景师`：在建筑骨架与功能定位稳定后读取空间骨架、镜头需求和道具氛围线索。
- `审景师`：读取聚合后的候选设计卡与原始 scene evidence，不读未采用的草稿。
- `真源审计`：读取最终 candidate、review note、output path 与 schema 合同。

# 默认执行流程

## Tranche 1. 父 skill 预处理

- 读取 scene catalog 与 `2-Global` 文档。
- 生成：
  - `mission_brief`
  - `context_packet_设计统筹`
  - `context_packet_审景师`
  - `context_packet_真源审计`

## Tranche 2. 设计统筹

- 输出：
  - `plan_patch_设计统筹`
  - `note_设计统筹`
  - `report_设计统筹`（如输入不足）
- 至少锁定：
  - 本轮命中场景列表
  - 每个场景的 `scene_key`
  - 是否需要补看 `3-Detail` 镜头证据

## Tranche 3. specialist 并行

- `空间逻辑`
  - 输出 `artifact_patch_空间逻辑`
- `建筑设计师`
  - 输出 `artifact_patch_建筑设计师`
- `布景师`
  - 输出 `artifact_patch_布景师`

本 tranche 默认并行，且默认后台 subagents 模式。

## Tranche 4. 父 skill 聚合

- 把三份 specialist patch 汇总为 `scene_design_candidate`。
- 严禁把任何单个 specialist 输出当成最终主稿。

## Tranche 5. review / audit

- `审景师` 返回 `review_note_审景师`
- `真源审计` 返回 `audit_report`
- 只要任一角色触发 veto，父 skill 必须停止写回并进入返工。

## Tranche 6. canonical writeback

- 父 skill 使用 `templates/scene-design-card.md` 渲染 `<scene_key>.md`
- 父 skill 将聚合结果写入 `场景设计.json`
- 仅在显式要求追溯时再写 `_manifest.json`

# 命名合同

- `mission_brief`
- `context_packet_<role>`
- `plan_patch_<role>`
- `artifact_patch_<role>`
- `review_note_<role>`
- `audit_report`
- `synthesis_report`

最终 canonical artifact 只能由父 skill 写回。
