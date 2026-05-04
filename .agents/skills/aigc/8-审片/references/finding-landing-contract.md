# Finding Landing Contract

## Landing Types

| landing | use when | write target |
| --- | --- | --- |
| `review_only` | 信息不足、低置信、或仅记录素材内容 | `projects/aigc/<项目名>/8-审片/第N集/` |
| `rerun_only` | 单次生成瑕疵，不需要改上游 | 审片报告 + `7-视频` rerun note |
| `group_repair` | 分镜组正文、节奏、焦点、首尾状态导致可复现偏差 | `projects/aigc/<项目名>/4-分组/第N集.md` |
| `source_escalation` | 多例复现且能定位阶段合同或技能模板 | owning skill / source document |

## Group Repair Boundary

允许修：

- 对应 `## group_id` 的正文、YAML 统计、出场/入场或新版组间连接件。
- 与该组直接相邻且必须同步的衔接画面。

禁止顺手修：

- 无关分镜组。
- 未经证据支持的剧情事实。
- 全集结构迁移。

## Report Required Fields

审片报告必须包含：

- `video_path`
- `group_id`
- `variant`
- `source_group_path`
- `observed_content`
- `expected_from_group`
- `findings`
- `landing_decision`
- `changed_files`
- `thinking_process`

## Patch Rule

`group_repair` 不是重写得更文学，而是让下一次视频生成更稳定：

- 降低同时出现的主体数量。
- 明确唯一焦点、镜头动作和停点。
- 把后续 beat 留给下一组。
- 减少可读文字、复杂近景手部和无必要角色近景。
