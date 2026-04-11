# aigc 1-规划 / Output Template

本文件承载 `aigc 1-规划` 根技能的输出写位与跨阶段 handoff 规则。

## Artifact Roles

| artifact | 默认落点 | 角色 |
| --- | --- | --- |
| 故事源清单 | `projects/<项目名>/Init/story-source-manifest.yaml` | 故事主源类型、覆盖范围与预设保护模式真源 |
| 阶段验收 | `projects/<项目名>/规划/validation-report.md` | 根技能级 route decision、source mode verdict、下一阶段入口 |
| 分集 bootstrap | `projects/<项目名>/编导/第N集.json` | 后续 `2-组间 -> 3-明细` 的单一 episode 真源 |

## Source Profile Handoff

若本轮已完成 `1-分集` bootstrap，则每个 `第N集.json` 都应带上：

```json
{
  "metadata": {
    "source_profile": {
      "source_type": "storyboard_script",
      "preset_retention_mode": "preserve_and_extend",
      "detail_expansion_mode": "respect_storyboard_presets",
      "locked_preset_axes": [
        "scene_boundary",
        "shot_order",
        "camera_motif"
      ],
      "preset_registry": [
        {
          "anchor_id": "A01",
          "source_span": "第1场 开场走廊调度",
          "lock_level": "soft_lock",
          "owned_axes": ["scene_boundary", "camera_motif"],
          "expandable_axes": ["shot_density", "composition", "micro_action"],
          "forbidden_changes": ["reverse_viewpoint"],
          "projected_group_ids": ["G01"],
          "projected_shot_mode": "single_anchor_multi_shot"
        }
      ]
    }
  }
}
```

## Output Checklist

1. `story-source-manifest.yaml` 是否明确当前主故事源类型。
2. 若是 `storyboard_script` 或 `hybrid_story_text`，是否明确 `preset_retention_mode` 与 `locked_preset_axes`。
3. 若存在外部分镜预设，是否已把可保留、可扩写、不可推翻的锚点写进 `preset_registry`。
4. `validation-report.md` 是否写清 `source_mode verdict` 与冲突解消理由。
5. 若已 bootstrap `第N集.json`，是否已写入 `metadata.source_profile`。
6. 下游建议是否明确指出 `3-明细` 是“自由扩写”还是“顺着预设扩写”。
