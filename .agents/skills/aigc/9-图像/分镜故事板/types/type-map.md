# Type Map

## 类型包加载边界

- 每次调用本技能时，必须依据本文件识别并加载同目录 `types/` 中选中的类型包。
- `types/` 中命中的类型包作为固定上下文加载；`knowledge-base/` 只作为按需检索、切片或向量召回的知识库，不替代类型包。
- `分镜平面图` 产物若存在，只能作为可选 `spatial_handoff` 读取；不参与本技能完成门禁。

本文件定义 `分镜故事板` 的任务分型和 route。

## Package Index

| package_id | path | match_signals | load_mode | context_files | conflicts_with | inherits_from |
| --- | --- | --- | --- | --- | --- | --- |
| `storyboard_sheet_default` | `types/storyboard-sheet-default.md` | 分镜故事板所有组级 storyboard sheet 任务 | fallback | `types/storyboard-sheet-default.md` | none | none |

## Default Package Rule

默认加载 `types/storyboard-sheet-default.md`。生成、修复或审查时再按 mode 额外读取 `SKILL.md` 主节点、`review/review-contract.md` 或 imagegen handoff 合同。

## Loading Flow

1. 锁定 `target_scope`、`execution_intent`、`source_state`、`frame_unit_state`、`style_lock_state`、`prompt_atoms_state`、`layout_state`、`spatial_handoff_state` 与 `imagegen_route`。
2. 加载默认包 `types/storyboard-sheet-default.md`。
3. 将类型画像交给 `SKILL.md` 的 `Thinking-Action Node Map`。
4. 生成前检查主体参照、主体保真锚定、style lock、visual prompt atoms、layout 状态、可选空间侧车消费状态和 imagegen route；审查时加载 `review/review-contract.md`。

## Type Variables

| variable | values | meaning |
| --- | --- | --- |
| `target_scope` | `single_group / group_batch / episode_batch / review_existing` | 处理范围 |
| `execution_intent` | `generate / repair_and_regenerate / review_then_regenerate` | imagegen 执行意图；本技能不接受 prompt-only、review-only 或 imagegen-plan-only 作为完成态 |
| `source_state` | `group_source_ready / group_source_partial / group_source_missing` | `8-分组` 可用性 |
| `frame_unit_state` | `frame_units_ready / frame_units_partial / frame_units_missing` | storyboard panel 落点是否已基于视觉节拍识别 |
| `style_lock_state` | `style_lock_ready / style_lock_drift / style_lock_missing` | 是否已隔离完整组稿中的上游风格句，且最终绘制 atoms 不含彩色电影 still、写实渲染、场景氛围或全局画风词 |
| `prompt_atoms_state` | `atoms_ready / atoms_partial / atoms_missing` | 每个 panel 是否已有可执行 `visual_prompt_atoms`，而不是仅有 summary / panel_description / 完整组稿 |
| `reference_state` | `all_bound / partial_missing / no_assets / ambiguous` | 主体参照状态 |
| `subject_fidelity_state` | `identity_anchors_bound / identity_anchors_partial / no_reference_images` | 参照图是否承担角色身份、场景空间结构、道具外形保真 |
| `layout_state` | `layout_ready / layout_risk / layout_missing` | 是否具备 locked 16:9 panel image box、panel 下方 rich_brief 描述文字、每个可见角色头顶黑色角色名、受控彩色标注系统、`layout_aspect_decision` 和 `panel_geometry_blueprint` |
| `spatial_handoff_state` | `none / available / consumed / conflict / misused` | 可选 `分镜平面图` 侧车是否存在、是否被合理消费；缺失不阻断，冲突或误用必须返工 |
| `imagegen_route` | `built_in / blocked` | imagegen 路由；必须直接调用 `.agents/skills/cli/imagegen` 的内置 `image_gen` 生成图片，不能停在 plan |

## Mode Matrix

| type profile | mode | route |
| --- | --- | --- |
| `single_group + generate + group_source_ready` | `single_group_generate` | `SKILL.md` 的 `N1-N2-N3-N4-N5-N6-N7-N8-N9-N10` |
| `episode_batch + generate + group_source_ready` | `episode_batch_generate` | `N1-N2-N3-N4-N5-N6-N7-N8-N9-N10` with group-level sequential or controlled batch dispatch |
| `group_batch + generate + group_source_ready` | `group_batch_generate` | `N1-N2-N3-N4-N5-N6-N7-N8-N9-N10` for selected groups |
| `review_existing + review_then_regenerate` | `review_then_regenerate` | `review/review-contract.md` -> owning failed node -> `N7-N8-N9-N10` |
| `* + repair_and_regenerate` | `repair_and_regenerate` | route to owning failed node, then `N7-N8-N9-N10` |
| `* + group_source_missing` | block | ask user to provide/fix source |
| `* + frame_units_missing` | block | return to `references/group-source-extraction.md#storyboard-frame-unit-derivation` |

## Reroute Rules

- 单一四段式 `分镜ID` 或单帧画面请求：转 `分镜画面`。
- 顶视图、建筑平面图、角色站位平面图、动线/机位平面标注、空间连续性平面 sheet：转 `分镜平面图`。
- 漫画页、气泡文字、阅读顺序或漫画分镜页：转 repo-local `comic` workflow。
- 视频生成前故事板参照：转 `10-画布/分镜故事板参照`。
- 需要重写 `8-分组` 内容：转 `8-分组` 修复，不在本技能内改写。

## Gate

进入 `generate` 前必须同时满足：

1. `source_state != group_source_missing`。
2. `frame_unit_state == frame_units_ready`；若为 `frame_units_partial`，必须先回到 `N4-FRAME-LAYOUT` 自动返工到 ready；无法恢复时只可 failed 报告，不得作为 prompt-only 完成。
3. `style_lock_state == style_lock_ready`；若为 `style_lock_drift / style_lock_missing`，必须回到 `N6-FINAL-PAYLOAD` 重建 `style_lock_spec` 与负向原子。
4. `prompt_atoms_state == atoms_ready`；若为 `atoms_partial / atoms_missing`，必须回到 `N6-FINAL-PAYLOAD` 逐 panel 重写 `visual_prompt_atoms`。
5. `imagegen_route == built_in`；必须进入 `N7-IMAGEGEN` 并产生项目内图片路径，不得 plan-only 结束；CLI/API/provider 专属控制不属于本技能默认路线。
6. `reference_state != ambiguous`；若存在 ambiguous 条目，必须从 reference images 自动排除并记录为 missing/ambiguous evidence 后继续生图，不得等待用户确认。
7. `layout_state != layout_missing`，且 `panel_geometry_blueprint` 存在；若为 `layout_risk` 或 `panel_image_box_ratio_error > 0.06`，必须记录并采用分页或多 sheet 策略继续生成，不得等待人工确认。
8. `spatial_handoff_state != conflict` 且 `spatial_handoff_state != misused`；若存在冲突或误用，必须修复 source comprehension、visual prompt atoms 或移除错误侧车消费。`none` 与 `available` 不阻断。
9. 若存在主体参照图，`subject_fidelity_state != identity_anchors_partial`，除非缺失项已被记录为 `missing` 并从 reference images 移除。
10. 输出路径位于项目内 `9-图像/分镜故事板`。
