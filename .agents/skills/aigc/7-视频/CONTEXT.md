# Context: 7-视频

本文件是 `7-视频` 阶段入口的经验层知识库，不是过程日志。

## Context Health

- soft_limit_chars: 20000
- hard_limit_chars: 40000
- status: ok

## Type Map

| failure_or_outcome_type | root_cause_layer | immediate_fix | systemic_prevention | verification_point |
| --- | --- | --- | --- | --- |
| 视频任务仍路由到 legacy `6-Video` | registry / route 层 | 改回 `.agents/skills/aigc/7-视频/<子技能>` | registry 把 `aigc-7-video` 作为当前 active stage | routes.yaml 指向中文路径 |
| 主体参照任务被当成故事板参照 | 判型层 | 按目标参照源重判：主体 YAML 走 C，storyboard 图走 B | `types/type-map.md` 固定互斥路由 | route note 只有一个 child |
| 子技能输出落到旧英文 runtime | runtime 层 | 迁回 `projects/aigc/<项目名>/7-视频/` | `video-stage-runtime.md` 固定 legacy 边界 | 输出路径可追溯 |

## Repair Playbook

1. 先确认任务目标是 `frame_reference`、`storyboard_reference`、`subject_reference`、`query_or_download`、`repair` 还是 `review_only`。
2. 再确认项目输出根是否为 `projects/aigc/<项目名>/7-视频/`。
3. 若任务命中 `C-主体参照`，检查是否保留 `4-分组` 主源、YAML 主体基准和 `@图片路径` 后缀。
4. 若发现旧 `6-Video` 路径，只允许作为 legacy 证据来源，不作为新产物落点。

## Reusable Heuristics

- `7-视频` 父级只做路由和汇流，不能吞并子技能的执行细则。
- 判型优先看参照对象：单帧画面走 A，故事板图走 B，角色/场景/道具主体走 C。
- legacy `6-Video` 最容易污染 registry 和 audit；最终落点必须回到中文 runtime。
