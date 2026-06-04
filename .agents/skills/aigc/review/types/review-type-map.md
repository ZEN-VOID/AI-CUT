# Review Type Map

## 类型包加载边界

- 每次调用本技能时，必须依据本文件识别并加载同目录 `types/` 中选中的类型包（单选或多选）。
- `types/` 中命中的类型包作为固定上下文加载；`knowledge-base/` 只作为按需检索、切片或向量召回的知识库，不替代类型包。


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
- `2-编剧`
- `3-美学`
- `4-导演`
- `5-表演`
- `6-氛围`
- `7-分镜`
- `8-摄影`
- `9-光影`
- `10-分组`
- `11-主体`
- `12-图像`
- `13-画布`
- `14-审片`

旧版 `_shared/` 中出现的 `1-Planning / 2-Global / 3-Detail / 4-Design / 5-Image / 6-Video` 以及 `2-编导 / 3-运动 / 4-摄影` 只作为兼容 alias，不应成为新文档的业务真源。

## Dimension Fit

| dimension | current-stage focus |
| --- | --- |
| `规划与种子兑现` | `0-初始化 / 1-分集 / 2-编剧` |
| `分镜执行连续性` | `2-编剧 / 3-美学 / 4-导演 / 5-表演 / 6-氛围 / 7-分镜 / 8-摄影 / 9-光影 / 10-分组` |
| `设计对位` | `11-主体` |
| `图像交付就绪` | `12-图像` |
| `视频交付就绪` | `13-画布 / 14-审片` |
| `治理闭环` | 项目根治理 carrier 与所有阶段 validation carrier |

## Stage Owner And Runtime Root

| stage owner | canonical project runtime |
| --- | --- |
| `11-主体` | `projects/aigc/<项目名>/11-主体/` |

说明：`11-主体` 同时是技能阶段 owner 与当前项目资产根。旧 `4-设计/` 只作为 transition/compat 输入，review runner 的 required refs 默认读取 `11-主体/`。
