# Floor Plan Sheet Contract

本文件展开 `分镜平面图` 的图面 payload、平面图绘制要求和审查映射。它只展开 `SKILL.md` 已声明的节点与 gate，不新增入口、完成态或输出路径。

## Concept

- `floor_plan_sheet` 是组级多 panel 顶视图平面图，不是 storyboard picture panels。
- 每个 panel 都是建筑平面图标准的黑白线稿：墙体、边界、出入口、障碍物、固定锚点和区域关系必须清晰。
- 角色不用写实人物表现，必须用带颜色的几何图标表现：圆形、三角形、方形、菱形、五边形等。角色名用黑色文本标在图标旁或上方。
- 摄影机用蓝色 camera marker、方向箭头或视野锥表示；角色移动用红色箭头表示；绿色用于取景/构图，橙色用于灯光方向，紫色用于情绪/声音/叙事强调。
- 同一集的 `character_icon_legend` 必须保持一致；除非用户显式要求换图例，不得每组重新分配角色颜色或形状。

## Required Inputs

- 当前分镜组 `group_full_source`、`source_spatial_comprehension` 和底部 YAML。
- 当前组目标 `floor_plan_panels`。
- 同一集角色图例；若无则本组初始化 `character_icon_legend`。
- 可选主体参照图 manifest；有图时先 `view_image`，缺图时记录 missing。
- 同一集前一个 accepted `floor_plan_sheet`；首组记录 `previous_group_id: none`。

## Floor Plan Payload

每个组至少输出：

```yaml
floor_plan_sheet:
  group_id: "1-1-1"
  previous_group_id: "none | 1-1-0"
  prompt_block_path: "projects/aigc/<项目名>/9-图像/分镜平面图/第1集/第1集-分镜平面图-prompts.md"
  floor_plan_sheet_path: "projects/aigc/<项目名>/9-图像/分镜平面图/第1集/floor-plan-sheets/1-1-1.png"
  source_spatial_comprehension:
    narrative_function: ""
    action_chain: []
    spatial_anchors: []
    entrances_exits: []
    character_state_anchors: []
    prop_state_anchors: []
    forbidden_inventions: []
  character_icon_legend:
    - name: ""
      source: "group_yaml.角色"
      icon_shape: "circle | triangle | square | diamond | pentagon"
      icon_color: ""
      label_color: "black"
      consistency_scope: "episode"
  floor_plan_panels:
    - panel_no: 1
      source_shot_labels: []
      source_span: ""
      spatial_goal: ""
      scene_boundary:
        boundary_lines: ""
        entrances_exits: []
        fixed_anchors: []
        obstacles: []
      character_blocking:
        - name: ""
          icon_shape: ""
          icon_color: ""
          position_label: ""
          facing_direction: ""
          relation_to_scene_anchors: ""
          relation_to_other_characters: ""
      prop_positions:
        - name: ""
          position_label: ""
          relation_to_character_or_scene: ""
      camera_plan:
        camera_marker: ""
        camera_position: ""
        camera_direction: ""
        framing_cone: ""
        camera_movement: ""
      movement_paths:
        red_body_movement_arrows: ""
        blue_camera_movement_arrows: ""
      annotation_plan:
        green_framing_composition_marks: ""
        orange_lighting_direction_marks: ""
        purple_emotion_sound_narrative_marks: ""
        black_text_labels: ""
      negative_prompt_atoms:
        - "no perspective scene illustration"
        - "no realistic human figure rendering"
        - "no color rendering outside icons and annotations"
  continuity_from_previous:
    unchanged_anchors: []
    changed_positions: []
    movement_logic: ""
    camera_transition: ""
    narrative_spatial_rationale: ""
    spatial_consistency_verdict: "initial | consistent | needs_rework | failed"
  acceptance:
    verdict: "pending | accepted | needs_rework | failed"
    checked_items: []
    failure_reasons: []
    rework_target: ""
```

## Diagram Prompt Requirements

平面图 prompt 必须明确：

- top-down floor plan sheet / overhead architectural plan / diagrammatic layout；
- black-and-white clean line art base for the floor plan, with walls, room boundaries, entrances, exits, fixed anchors, obstacles and key props;
- no perspective camera scene, no cinematic still, no storyboard illustration, no concept art, no atmosphere rendering;
- character icons are colored geometry symbols only, with black text labels using exact YAML character names;
- red arrows for body movement only;
- blue arrows for camera movement, camera direction or field-of-view cones only;
- green marks for framing/composition zones;
- orange marks for lighting direction only when source evidence exists;
- purple marks for emotion/sound/narrative emphasis only when source evidence exists;
- black text for role names, panel labels, anchor labels and short spatial notes;
- colors must not render clothes, faces, walls, backgrounds, lighting mood or atmosphere.

## Continuity Gate

同一集内从第二个目标组起必须审查：

1. 上一组 accepted sheet 中的固定锚点是否保持。
2. 角色从上一位置到当前位置的路径是否能由源文本、跳切、时间间隔或动作链解释。
3. 摄影机方向、视野锥和运镜变化是否能对应当前组 frame/panel 需求。
4. 道具与场景锚点的相对位置是否无矛盾。
5. 若连续性不可恢复，当前组必须 `failed` 或回到 `N3/N4` 返工，不得伪造 accepted。

## Failure And Rework

| fail signal | fail code | rework |
| --- | --- | --- |
| panel 没有 source span 或机械等同 `分镜N` | `FAIL-FLOOR-PLAN-PANELS` | 回到 `N3-PANEL-PLAN` 重建空间 panel |
| 成图不是顶视图建筑平面图 | `FAIL-FLOOR-DIAGRAM-STANDARD` | 回到 `N4-DIAGRAM-SPEC` 与 prompt 负向约束 |
| 角色未使用一致彩色几何图标或缺黑色角色名 | `FAIL-FLOOR-ICON-LEGEND` | 重建 `character_icon_legend` |
| 标注颜色语义混乱或颜色进入渲染层 | `FAIL-FLOOR-ANNOTATION-COLOR` | 重建 `annotation_plan` 和 negative atoms |
| 上下组空间变化无逻辑 | `FAIL-FLOOR-CONTINUITY` | 回到 `N5-CONTINUITY`，必要时返工 panel/spec |
| 生图未调用、未持久化、越权使用 CLI/API/provider 专属控制，或停在 imagegen plan | `FAIL-FLOOR-IMAGEGEN` | 回到 `N7-IMAGEGEN`，加载并调用 `.agents/skills/cli/imagegen/SKILL.md + CONTEXT.md` |
| 报告缺 generated/skipped/failed 或返工入口 | `FAIL-FLOOR-REPORT` | 回到 `N9-CLOSE` |

## Review Gate Mapping

| Review Question | Review Gate | Fail Code | Rework Target | Report Evidence |
| --- | --- | --- | --- | --- |
| floor plan panels 是否有 source span、spatial goal 和角色/摄影机/道具空间状态？ | `G2-PANEL-PLAN` | `FAIL-FLOOR-PLAN-PANELS` | `N3-PANEL-PLAN` | floor-plan-index.json 中每 panel 记录 |
| 图面是否为顶视图黑白建筑平面图，而非分镜画面或概念图？ | `G3-DIAGRAM-STANDARD` | `FAIL-FLOOR-DIAGRAM-STANDARD` | `N4-DIAGRAM-SPEC` | prompt negative atoms、生成图 review note |
| 角色是否用同集一致的彩色几何图标和黑色名称标签表示？ | `G4-ICON-LEGEND` | `FAIL-FLOOR-ICON-LEGEND` | `N4-DIAGRAM-SPEC` | character_icon_legend、panel labels |
| 标注颜色是否严格遵守红/蓝/绿/橙/紫/黑语义，且没有渲染污染？ | `G5-ANNOTATION-COLOR` | `FAIL-FLOOR-ANNOTATION-COLOR` | `N4-DIAGRAM-SPEC` / `N6-PROMPT-PAYLOAD` | annotation legend、review note |
| 当前组与上一组 accepted sheet 的空间变化是否连续且叙事扣合？ | `G6-CONTINUITY` | `FAIL-FLOOR-CONTINUITY` | `N5-CONTINUITY` | continuity_from_previous 字段 |
