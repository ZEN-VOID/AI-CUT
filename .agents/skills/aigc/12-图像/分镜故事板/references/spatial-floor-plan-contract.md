# Spatial Floor Plan Contract

本文件定义 `分镜故事板` 的前置空间站位图：每个分镜组在生成 storyboard sheet 前，必须先建立并验收一张顶视图 `spatial_floor_plan`，用于锁定角色、场景、道具、摄影机与运动方向的平面空间关系。

## Purpose

- `spatial_floor_plan` 是 storyboard sheet 的空间真源辅助图，不是概念图、气氛图或场景美术图。
- 它以顶视图方式展示当前分镜组的清晰平面布置：场景边界、出入口、主要家具/障碍物、角色站位、角色朝向、道具位置、摄影机位置、镜头方向、运动路径和关键空间关系。
- 下一个分镜组的 `spatial_floor_plan` 必须与上一个分镜组的通过版平面图建立空间连续性：保留未变化锚点，明确变化项，并解释角色/摄影机/道具如何从上一个位置移动到当前状态。
- storyboard sheet imagegen 只能消费 `accepted` 状态的 `spatial_floor_plan`；未验收、验收失败或空间关系不自洽时，必须在同轮自动返工到 accepted，无法恢复时 failed 报告，不得停成等待用户确认的断点。
- `accepted` 状态之后还必须生成 `floor_plan_to_panel_mapping`：把顶视图平面图逐 panel 转译为角色站位、朝向、道具位置、摄影机位置/方向和运动路径。没有逐 panel 映射时，平面图不得被视为已真正接入 storyboard sheet。

## Required Inputs

- 当前分镜组的 `group_full_source`、`source_comprehension`、`storyboard_frame_units` 和 `layout_aspect_decision`。
- 当前组底 YAML 的角色、场景、道具主体列表。
- 已绑定的主体参照图 manifest；有图时必须先 `view_image` 进入上下文，缺图时记录 missing，不得伪造。
- 同一集内前一个已验收分镜组的 `spatial_floor_plan`；第一组可记录 `previous_floor_plan_id: none`。

## Floor Plan Payload

每个组至少输出：

```yaml
spatial_floor_plan:
  group_id: "1-1-1"
  previous_floor_plan_id: "none | 1-1-0"
  top_view_diagram_prompt: ""
  top_view_diagram_path: "projects/aigc/<项目名>/12-图像/分镜故事板/第1集/floor-plans/1-1-1.png"
  scene_boundary:
    source: "group_yaml.场景 + group_body"
    layout_notes: ""
    fixed_anchors: []
    entrances_exits: []
  character_positions:
    - name: ""
      source: "group_yaml.角色"
      position_label: ""
      facing_direction: ""
      movement_path: ""
      relation_to_scene_anchors: ""
      relation_to_other_characters: ""
  prop_positions:
    - name: ""
      source: "group_yaml.道具"
      position_label: ""
      relation_to_character_or_scene: ""
  camera_plan:
    - panel_no: 1
      camera_position: ""
      camera_direction: ""
      framing_cone: ""
      movement_arrow: ""
      source_span: ""
  continuity_from_previous:
    unchanged_anchors: []
    changed_positions: []
    movement_logic: ""
    spatial_consistency_verdict: "initial | consistent | needs_rework"
  acceptance:
    verdict: "pending | accepted | needs_rework"
    checked_items: []
    failure_reasons: []
    rework_target: ""
  floor_plan_to_panel_mapping:
    - panel_no: 1
      floor_plan_zone: ""
      characters_position_and_facing: ""
      props_position: ""
      camera_position_and_direction: ""
      movement_path_used: ""
      unchanged_anchors_from_floor_plan: ""
      allowed_composition_variation: "framing_crop_perspective_only"
      forbidden_spatial_drift: ""
```

## Diagram Prompt Requirements

顶视图平面图 prompt 必须明确：

- top-down floor plan / overhead view / diagrammatic layout；
- 清晰场景边界和空间锚点，避免透视绘画、电影 still、气氛图或彩色场景美术；
- 用简单符号或轮廓表示角色站位，用黑色文本标注角色名；角色名必须与组底 YAML 一致；
- 用箭头表示角色运动、摄影机位置与视线方向；摄影机锥形视野必须能对应 `storyboard_frame_units`；
- 标注关键道具与场景锚点；缺图主体可标为 textual placeholder，但不得从外观猜测新主体；
- 若存在前一个通过版平面图，必须声明哪些锚点保持不变、哪些站位/镜头发生变化，以及变化路径；
- 图面应服务空间理解和下游 storyboard，不使用项目全局画风、光影、氛围或色彩渲染。

## Acceptance Gate

`spatial_floor_plan.acceptance.verdict` 为 `accepted` 前，不得进入 storyboard sheet imagegen；该验收是内部自动 gate，失败时立即回到平面图生成/连续性修复，直到 accepted 或确认存在不可恢复输入缺口。

必须检查：

1. 是否为顶视图性质，场景边界、出入口、主要锚点清晰。
2. 角色、道具、摄影机站位是否来自当前组源文本、YAML 和已绑定主体参照，没有新增事实。
3. 每个可见角色是否有与 YAML 一致的名称标签。
4. 摄影机位置、视线方向、运动路径是否能对应 `storyboard_frame_units`。
5. 与上一张已验收平面图相比，未变化锚点是否保持，变化项是否有清楚移动逻辑。
6. 平面图是否足以作为 storyboard sheet 生成的空间站位输入。
7. 是否存在会污染 storyboard 的透视图、气氛图、美术风格化、角色外观重设计或空间矛盾。

## Floor Plan To Panel Mapping Gate

`floor_plan_to_panel_mapping` 是 `accepted` 后的第二道空间门禁，必须在 imagegen 前通过。它不要求重新生成一张图，而是把平面图的顶视图信息转译成每个 storyboard panel 的可执行空间约束。

每个 panel 必须检查：

1. `floor_plan_zone` 是否能回指 accepted floor plan 中的场景区域、角色站位或摄影机视野锥。
2. `characters_position_and_facing` 是否保持角色名、左右/内外/前后关系、朝向和相互距离。
3. `props_position` 是否保持关键道具与角色/场景锚点的相对位置。
4. `camera_position_and_direction` 是否对应当前 frame unit 的景别、构图或运镜；源文本无明确运镜时不得补写不必要机位。
5. `movement_path_used` 是否来自平面图中的角色/道具/摄影机运动路径。
6. `allowed_composition_variation` 是否只允许景别、裁切和透视转换，不改变空间事实。
7. `forbidden_spatial_drift` 是否明确写出不得改变的关系，例如左内线/右外沿、上行/下行、老人孩子保护线、敌我距离、道具相对位置。

缺少该映射、映射空泛、或任何 panel 无法回指 accepted floor plan 时，必须标记 `FAIL-SHEET-FLOOR-PLAN-MAPPING` 并返工；不得只凭 `acceptance.verdict: accepted` 继续生图。

## Failure And Rework

| fail signal | fail code | rework |
| --- | --- | --- |
| 平面图不是顶视图，像场景插画或电影画面 | `FAIL-SHEET-FLOOR-PLAN` | 重写 top-view diagram prompt 并重生/重验 |
| 角色站位、道具位置或摄影机方向无法回指源文本 | `FAIL-SHEET-FLOOR-PLAN` | 回到 `source_comprehension`、frame units 和 YAML 主体重建 |
| 与上一组空间变化不连续 | `FAIL-SHEET-FLOOR-PLAN-CONTINUITY` | 标注 unchanged anchors、changed positions 和 movement logic 后重验 |
| 未验收就进入 storyboard sheet | `FAIL-SHEET-FLOOR-PLAN-GATE` | 阻断本次 storyboard imagegen，自动完成 floor plan acceptance 后继续生图 |
| 平面图缺主体参照状态或伪造缺失图片 | `FAIL-SHEET-REF` | 回到 reference manifest 和 `view_image` 前置门禁 |
| 平面图 accepted 但缺少逐 panel 映射，或故事板格子的站位无法回指平面图 | `FAIL-SHEET-FLOOR-PLAN-MAPPING` | 建立/修复 `floor_plan_to_panel_mapping` 后再进入 imagegen |

## Review Gate Mapping

| Review Question | Review Gate | Fail Code | Rework Target | Report Evidence |
| --- | --- | --- | --- | --- |
| 每个分镜组是否在 storyboard sheet 前生成或锁定了顶视图 `spatial_floor_plan`？ | `G8B-FLOOR-PLAN` | `FAIL-SHEET-FLOOR-PLAN` | `N5A-FLOOR-PLAN` / `references/spatial-floor-plan-contract.md` | `floor-plan-manifest.json`、floor plan image path、prompt block |
| 平面图是否清楚展示场景边界、角色站位、道具位置、摄影机位置/方向和运动路径，且能对应 frame units？ | `G8B-FLOOR-PLAN` | `FAIL-SHEET-FLOOR-PLAN` | `N5A-FLOOR-PLAN` | acceptance checklist、frame-unit mapping |
| 当前平面图与上一张已验收平面图的空间变化是否逻辑连续？ | `G8C-FLOOR-PLAN-CONTINUITY` | `FAIL-SHEET-FLOOR-PLAN-CONTINUITY` | `N5A-FLOOR-PLAN` | `continuity_from_previous` 记录 unchanged anchors、changed positions、movement logic |
| `spatial_floor_plan.acceptance.verdict` 是否为 `accepted` 后才进入 storyboard sheet 生成？ | `G8D-FLOOR-PLAN-ACCEPTANCE` | `FAIL-SHEET-FLOOR-PLAN-GATE` | `N6-REVIEW` / `N7-IMAGEGEN` | imagegen plan task 记录 accepted floor plan id/path/verdict |
| accepted floor plan 是否已逐 panel 转译为 `floor_plan_to_panel_mapping`？ | `G8E-FLOOR-PLAN-MAPPING` | `FAIL-SHEET-FLOOR-PLAN-MAPPING` | `N5A-FLOOR-PLAN` / `N5B-FINAL-PAYLOAD` | floor-plan manifest、prompt 和 imagegen plan 逐 panel 记录 floor_plan_zone、characters_position_and_facing、camera_position_and_direction、forbidden_spatial_drift |
