# Output Template

## Output Contract Alignment

- Required output: 逐集运动强化稿 `projects/aigc/<项目名>/3-运动/第N集.md` 与阶段 `执行报告.md`；任意来源模式写用户指定路径或 source 相邻 `3-运动/`。
- Output format: Markdown 运动强化稿 + Markdown 执行报告。
- Output path: 项目模式固定 `projects/aigc/<项目名>/3-运动/`；任意来源模式按 source 相邻目录或用户指定路径。
- Naming convention: `第N集.md`、`执行报告.md`；任意来源默认 `<source_stem>-运动强化.md`。
- Completion gate: 每个 motion unit 有 `motion_state_ledger`，已按同一场景或连续动作段建立 `group_reference_profile` 并尽量统一参照系；仅在输入源显式已有分镜组时继承源内组边界；每个被扩写的原有运动字段或动作句具备主体、起点、路径、终点和参照系，已回顾上一画面最终状态，未改写剧情事实，原字段名逐字保留，未新增、重命名、拆分字段，未新增独立 `运动强化：` 字段，未越权写摄影或 prompt。

## Episode Motion Draft

```markdown
---
stage: 3-运动
source_path: projects/aigc/<项目名>/2-编导/第N集.md
output_path: projects/aigc/<项目名>/3-运动/第N集.md
motion_policy: character_motion_five_elements
---

# 第N集

【剧本正文】

<!-- 保留 source 原字段名与顺序，只替换或扩写冒号后的字段值；示例中“动作”必须是 source 已存在字段名： -->
动作：在[参考系]处，[运动主体]面向[方向或对象]，从[起点]沿[路径][动词]到[终点]，最后在[参考系]处形成[最终状态]。
```

## Execution Report

```markdown
# 3-运动 执行报告

## Source Context

- source_path:
- source_kind:
- output_path:
- init_team_synthesis_context:
  - source: team.yaml.init_synthesis.stage_seed_summary."3-运动" / init_handoff.motion_seed / north_star.yaml.创作阶段不变量.运动
  - accepted_constraints:
  - risks_to_watch:

## Motion Unit Index

| unit_id | source_anchor | motion_subject | candidate_reason | skipped |
| --- | --- | --- | --- | --- |

## Scene / Segment Reference Profile

| reference_group_id | boundary_source | primary_reference_frame | candidate_basis | allowed_local_reference_frames | switch_rules |
| --- | --- | --- | --- | --- | --- |

## Motion State Ledger

| unit_id | reference_group_id | previous_final_state | current_start_inference | primary_reference_frame | reference_frame | reference_frame_basis | reference_switch_reason | start_point | path | end_point | final_state | continuity_status |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |

## Review

- verdict:
- findings:
- repair_actions:

## Handoff To 4-摄影

- ready_for_cinematography:
- source_for_next_stage:
- forbidden_overreach_checked:
- init_synthesis_consumed_without_persona_dispatch:
```
