# Review Team Contract

`aigc/review` 的默认执行器不是 `team.yaml` 顾问团，而是 review registry + execution provider。

## Ownership Rule

- legacy `team.yaml.roles.supervision`
  - 只作为旧项目只读迁移证据；不得恢复为当前 `2-编剧` 到 `11-主体` 的前置 advisory runtime
- legacy `team.yaml.roles.review`
  - 只作为旧项目只读迁移证据；当前 `12-图像 / 13-画布 / 14-审片` 的阶段 gate 由 review registry + execution provider 承担
- `aigc/review`
  - 负责 package-level / checkpoint-level / stage-level 结构化审计

## Hard Rules

1. 不得把 `team.yaml.roles.supervision` 重新升级成 review 父层的 post-write closeout owner。
2. `aigc/review` 默认通过 registry dimension specs + provider 执行，而不是复用 `council-runtime`。
3. 若未来需要人工 reviewer roster，应另建 review-specific runtime contract，不得偷渡回 `team.yaml` 顾问团。
