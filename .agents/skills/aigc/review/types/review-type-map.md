# Review Type Map

## Mode Matrix

| mode | required selector | primary question | selected dimensions |
| --- | --- | --- | --- |
| `checkpoint_inline` | `checkpoint_id` | 当前 handoff 点能不能过 | registry checkpoint mandatory dimensions |
| `stage_acceptance` | `stage` | 当前阶段能不能放行 | registry stage mandatory dimensions |
| `package_release` | `scope_ref` | 当前集/包能不能交付 | 全维度 release dimensions |

## Current Stage Language

新版 `.agents/skills/aigc` 的规范 stage 名称：

- `0-初始化`
- `1-分集`
- `2-编导`
- `3-摄影`
- `4-分组`
- `5-设计`
- `6-图像`
- `7-视频`

旧版 `_shared/` 中出现的 `1-Planning / 2-Global / 3-Detail / 4-Design / 5-Image / 6-Video` 只作为兼容 alias，不应成为新文档的业务真源。

## Dimension Fit

| dimension | current-stage focus |
| --- | --- |
| `规划与种子兑现` | `0-初始化 / 1-分集 / 2-编导` |
| `分镜执行连续性` | `3-摄影 / 4-分组` |
| `设计对位` | `5-设计` |
| `图像交付就绪` | `6-图像` |
| `视频交付就绪` | `7-视频` |
| `治理闭环` | 项目根治理 carrier 与所有阶段 validation carrier |

## Stage Owner And Runtime Root

| stage owner | canonical project runtime |
| --- | --- |
| `5-设计` | `projects/aigc/<项目名>/5-设计/` |

说明：`5-设计` 同时是技能阶段 owner 与当前项目资产根。旧 `4-设计/` 只作为 transition/compat 输入，review runner 的 required refs 默认读取 `5-设计/`。
