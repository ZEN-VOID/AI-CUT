# Review Team Contract

`aigc/review` 的默认执行器不是 `team.yaml` 顾问团，而是 review registry + execution provider。

## Ownership Rule

- `team.yaml.roles.supervision`
  - 只负责 `2-编导 / 3-摄影 / 4-分组 / 5-设计` 的前置 advisory
- `team.yaml.roles.review`
  - 当前仍保留在 `6-图像 / 7-视频` 的阶段 gate 语义
- `aigc/review`
  - 负责 package-level / checkpoint-level / stage-level 结构化审计

## Hard Rules

1. 不得把 `team.yaml.roles.supervision` 重新升级成 review 父层的 post-write closeout owner。
2. `aigc/review` 默认通过 registry dimension specs + provider 执行，而不是复用 `council-runtime`。
3. 若未来需要人工 reviewer roster，应另建 review-specific runtime contract，不得偷渡回 `team.yaml` 顾问团。
