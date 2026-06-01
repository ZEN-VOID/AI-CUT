# Cross-Episode Continuity Type Map

## Purpose

本类型包为 `2-编导` director layer 提供跨集连续性追踪能力。当处理第 N 集且第 N-1 集已完成导演稿时，可读取前集的关键证据作为延续参考，避免单集独立处理导致的视觉母题断裂、表演弧线丢失和叙事节奏脱节。

本类型包不授权新增剧情、对白或事件；它只在不改变保真前提下，让当前集的编导决策能参考前集已形成的创作轨迹。

## Type Profile Variables

| variable | values | detection cue | strategy |
| --- | --- | --- | --- |
| `previous_episode_available` | `true` / `false` | `projects/aigc/<项目名>/2-编导/第N-1集.md` 是否存在且可读 | 不可读时标注 `episode-local continuity`，不做跨集延续 |
| `motif_continuity_need` | `required` / `optional` / `not_applicable` | 前集 `episode_visual_spine` 是否包含可在本集延续的视觉母题 | `required` 时读取前集 `motif_chain` 和 `callback_targets` 作为延续参考 |
| `visual_arc_continuity` | `required` / `optional` / `not_applicable` | 前集的材质/色彩弧、节奏曲线是否形成本集应延续或呼应的视觉轨迹 | `required` 时参考前集 `material_and_color_arc` 和 `rhythm_curve` |
| `performance_arc_continuity` | `required` / `optional` / `not_applicable` | 前集关键角色的表演基调、情绪轨迹是否应在本集延续 | `required` 时优先读取前集 `director_substance_plan.character_pressure`；若前集已有 `2-编导` performance layer 产物，可额外读取外部阶段证据 `external_stage_refs.performance.actor_performance_control_evidence` 作为参考 |
| `prop_state_continuity` | `required` / `optional` / `not_applicable` | 前集末尾的道具状态、归属关系是否影响本集开场 | `required` 时读取前集 `episode_final_image_plan` 中的道具状态 |
| `spatial_continuity` | `required` / `optional` / `not_applicable` | 本集与前集是否使用相同或相连空间（同一建筑、同一城市、同一航线） | `required` 时参考前集 `environment描写` 的空间基调 |

## Continuity Strategy

### Motif Continuity

读取前集 `episode_visual_spine.motif_chain` 和 `callback_targets`：

- 若前集母题链中有物件、材质、自然景物或空间状态可在本集延续，纳入本集 `episode_visual_spine` 的 `motif_chain` 候选。
- 母题必须变化：同一物件在不同集应承担不同压力、距离、归属或情绪温度；不得机械复读前集用法。
- 若前集母题与本集剧情无关，不得强行延续；标注 `motif_continuity_not_applicable` 即可。

### Visual Arc Continuity

读取前集 `episode_visual_spine.material_and_color_arc` 和 `rhythm_curve`：

- 若前集建立的材质/色彩弧有延续空间，本集可选择呼应或反转。
- 节奏曲线的延续意味着本集开场节奏可参考前集结尾的节奏密度，避免突兀跳变。
- 不得为延续视觉弧线改变本集剧情条件或新增事实。

### Performance Arc Continuity

读取前集 `director_substance_plan.character_pressure`，并在存在时读取外部阶段证据 `external_stage_refs.performance.actor_performance_control_evidence`：

- 若某角色在前集建立了表演基调（例如压抑、试探、逐渐放松），本集开场可参考该基调。
- 表演弧线的延续意味着同一角色的微表情习惯、身体联动模式和声线特征可在本集保持一致。
- 不得为延续表演弧线改变角色在本集的真实情绪或行为选择。

### Prop State Continuity

读取前集 `episode_final_image_plan` 和末尾道具状态：

- 若前集结尾的道具状态影响本集开场（例如信未被收起、门未关上、伤痕未愈），本集 `环境描写` 或 `道具特写` 应承接。
- 道具状态的延续只处理可见物理状态，不新增道具功能或线索含义。

### Spatial Continuity

读取前集 `环境描写` 的空间基调：

- 若本集与前集使用相同空间，可参考前集的空间氛围但不得复制。
- 若本集与前集使用相连空间（同一建筑不同房间、同一城市不同地点），可参考前集的空间质感。

## Output Shape

```yaml
cross_episode_continuity_profile:
  previous_episode_available: true | false
  previous_episode_path: "projects/aigc/<项目名>/2-编导/第N-1集.md"
  motif_continuity: required | optional | not_applicable
  visual_arc_continuity: required | optional | not_applicable
  performance_arc_continuity: required | optional | not_applicable
  prop_state_continuity: required | optional | not_applicable
  spatial_continuity: required | optional | not_applicable
  external_stage_refs:
    performance:
      actor_performance_control_evidence: "optional; read-only evidence from previous 2-编导 performance layer output when it exists"
  continuity_notes: ""
```

## Boundary

允许：

- 读取前集 `episode_visual_spine`、`director_substance_plan.character_pressure`、可选外部阶段证据 `external_stage_refs.performance.actor_performance_control_evidence`、`episode_final_image_plan` 和 `环境描写` 作为延续参考。
- 在本集 `episode_visual_spine` 中标注前集母题的延续和变化方向。
- 在关键角色的表演规划中参考前集表演基调。

禁止：

- 为延续跨集母题新增本集没有的剧情事实、对白、事件、规则或线索。
- 为延续表演弧线改变角色在本集的真实情绪或行为选择。
- 机械复制前集的视觉母题、表演变量或环境描写。
- 把前集信息当成本集的上游真源；本集的上游真源始终是 `1-分集/第N集.md`。

## Review Checklist

- 跨集延续是否只参考前集创作证据，而不改变本集剧情条件？
- 母题延续是否有变化，而不是机械复读？
- 表演弧线延续是否尊重角色在本集的真实状态？
- 道具状态延续是否只处理可见物理状态？
- 是否没有把前集信息误当成上游真源？
