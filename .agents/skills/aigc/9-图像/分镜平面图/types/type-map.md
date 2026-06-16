# Type Map

## 类型包加载边界

- 每次调用本技能时，必须依据本文件识别并加载同目录 `types/` 中选中的类型包。
- `types/` 中命中的类型包作为固定上下文加载；`knowledge-base/` 只作为按需检索或人工维护知识库，不替代类型包。

本文件定义 `分镜平面图` 的任务分型和 route。

## Package Index

| package_id | path | match_signals | load_mode | context_files | conflicts_with | inherits_from |
| --- | --- | --- | --- | --- | --- | --- |
| `floor_plan_default` | `types/default/default.md` | 分镜平面图所有组级 floor plan sheet 任务 | fallback | `types/default/default.md` | none | none |

## Default Package Rule

默认加载 `types/default/default.md`。生成、修复或审查时再按 mode 额外读取 `references/floor-plan-sheet-contract.md`、`review/review-contract.md` 或 imagegen handoff 合同。

## Loading Flow

1. 锁定 `target_scope`、`execution_intent`、`source_state`、`panel_state`、`diagram_state`、`icon_legend_state`、`annotation_state`、`continuity_state` 与 `imagegen_route`。
2. 加载默认包 `types/default/default.md`。
3. 将类型画像交给 `SKILL.md` 的 `Thinking-Action Node Map`。
4. 生成前检查源追溯、panel 计划、角色图例、颜色标注、连续性、imagegen 计划和输出路径；审查时加载 `review/review-contract.md`。

## Type Variables

| variable | values | meaning |
| --- | --- | --- |
| `target_scope` | `single_group / group_batch / episode_batch / review_existing` | 处理范围 |
| `execution_intent` | `generate / repair_or_review / rerun` | 执行意图 |
| `source_state` | `group_source_ready / group_source_partial / group_source_missing` | `8-分组` 可用性 |
| `panel_state` | `panels_ready / panels_partial / panels_missing` | 平面图 panels 是否基于空间变化裁决 |
| `diagram_state` | `diagram_ready / diagram_drift / diagram_missing` | 是否满足黑白建筑平面图顶视图标准 |
| `icon_legend_state` | `legend_ready / legend_inconsistent / legend_missing` | 角色彩色几何图例是否同集一致 |
| `annotation_state` | `annotation_ready / annotation_drift / annotation_missing` | 颜色标注语义是否正确 |
| `continuity_state` | `initial / consistent / needs_rework / unavailable` | 与上一组空间关系是否连续 |
| `imagegen_route` | `built_in / blocked` | imagegen 路由；必须直接调用 `.agents/skills/cli/imagegen` 的内置 `image_gen` 生成图片，不能停在 plan |

## Mode Matrix

| type profile | mode | route |
| --- | --- | --- |
| `single_group + generate + group_source_ready` | `single_group_generate` | `N2-N3-N4-N5-N6-N7-N8-N9` |
| `episode_batch + generate + group_source_ready` | `episode_batch_generate` | `N2-N3-N4-N5-N6-N7-N8-N9` with ordered group processing |
| `group_batch + generate + group_source_ready` | `group_batch_generate` | `N2-N3-N4-N5-N6-N7-N8-N9` for selected groups |
| `review_existing + repair_or_review` | `repair_or_review` | `N8 -> owning failed node -> N7-N9` |
| `* + group_source_missing` | block | failed report or request source repair |
| `* + panels_missing` | repair | return to `N3-PANEL-PLAN` |
| `* + continuity_state needs_rework` | repair | return to `N5-CONTINUITY` |

## Reroute Rules

- 单一四段式 `分镜ID` 或单帧画面请求：转 `分镜画面`。
- 组级多格分镜画面：转 `分镜故事板`。
- 视频首帧、运动或连续性参照：转 `10-画布`。
- 需要重写 `8-分组` 内容：转 `8-分组` 修复，不在本技能内改写。

## Gate

进入 `generate` 前必须同时满足：

1. `source_state != group_source_missing`。
2. `panel_state == panels_ready`；若 partial/missing，回到 `N3-PANEL-PLAN`。
3. `diagram_state == diagram_ready`；若 drift/missing，回到 `N4-DIAGRAM-SPEC`。
4. `icon_legend_state == legend_ready`；若 inconsistent/missing，重建同集图例。
5. `annotation_state == annotation_ready`；若 drift/missing，重建颜色标注。
6. `continuity_state` 为 `initial` 或 `consistent`；若 `needs_rework`，回到 `N5-CONTINUITY`。
7. `imagegen_route == built_in`；必须进入 `N7-IMAGEGEN` 并产生项目内图片路径，不得 plan-only 结束；CLI/API/provider 专属控制不属于本技能默认路线。
8. 输出路径位于项目内 `9-图像/分镜平面图`。
