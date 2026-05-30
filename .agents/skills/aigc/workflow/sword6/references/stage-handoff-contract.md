# Stage Handoff Contract

本文件定义 `sword6` 在 `2-编剧 -> 6-分组` 之间的 canonical 输入输出链。

## Stage Chain

| stage | consumes | produces | stage skill |
| --- | --- | --- | --- |
| `2-编剧` | `projects/aigc/<项目名>/1-分集/第N集.md` | `projects/aigc/<项目名>/2-编剧/第N集.md` | `.agents/skills/aigc/2-编剧/SKILL.md` |
| `3-导演` | `projects/aigc/<项目名>/2-编剧/第N集.md` | `projects/aigc/<项目名>/3-导演/第N集.md` | `.agents/skills/aigc/3-导演/SKILL.md` |
| `4-表演` | `projects/aigc/<项目名>/3-导演/第N集.md` | `projects/aigc/<项目名>/4-表演/第N集.md` | `.agents/skills/aigc/4-表演/SKILL.md` |
| `5-摄影` | `projects/aigc/<项目名>/4-表演/第N集.md` | `projects/aigc/<项目名>/5-摄影/第N集.md` | `.agents/skills/aigc/5-摄影/SKILL.md` |
| `6-分组` | `projects/aigc/<项目名>/5-摄影/第N集.md` + `projects/aigc/<项目名>/0-初始化/north_star.yaml` | `projects/aigc/<项目名>/6-分组/第N集.md` | `.agents/skills/aigc/6-分组/SKILL.md` |

## Handoff Rules

1. 下游阶段只消费上一阶段 canonical 产物，不消费 workflow ledger 或主窗口摘要。
2. 续跑时若 `start_stage` 不是 `2-编剧`，必须确认上一阶段产物存在且可信；否则回到缺失产物的 owning stage。
3. 每个阶段完成后只把路径、校验结果、失败码和必要统计交回主窗口。
4. `6-分组` 额外需要 `0-初始化/north_star.yaml`；缺失时阻断，不得用口头风格摘要替代。
5. 阶段产物不得写入 legacy 英文路径或旧中文漂移路径。

## Resume Matrix

| requested start | required prior input | if missing |
| --- | --- | --- |
| `2-编剧` | `1-分集/第N集.md` | stop with `FAIL-SWORD6-HANDOFF` |
| `3-导演` | `2-编剧/第N集.md` | route failed episode back to `2-编剧` |
| `4-表演` | `3-导演/第N集.md` | route failed episode back to `3-导演` |
| `5-摄影` | `4-表演/第N集.md` | route failed episode back to `4-表演` |
| `6-分组` | `5-摄影/第N集.md` and `north_star.yaml` | route failed episode back to `5-摄影` or `0-初始化` evidence repair |

## Review Gate Mapping

| Review Question | Review Gate | Fail Code | Rework Target | Report Evidence |
| --- | --- | --- | --- | --- |
| 每个阶段是否只消费上一阶段 canonical 产物？ | `GATE-SWORD6-04` | `FAIL-SWORD6-HANDOFF` | 本文件 `Stage Chain`、`steps/sword6-workflow.md#N4-STAGE-MERGE` | stage ledger 中的 input_path/output_path |
| 续跑是否先验证上一阶段产物存在且可信？ | `GATE-SWORD6-01` | `FAIL-SWORD6-HANDOFF` | 本文件 `Resume Matrix`、`types/retry-from-stage/retry-from-stage.md` | preflight evidence table |
| `6-分组` 是否读取 `north_star.yaml`，而不是使用口头摘要？ | `GATE-SWORD6-04` | `FAIL-SWORD6-HANDOFF` | `.agents/skills/aigc/6-分组/SKILL.md`、本文件 `Stage Chain` | dispatch packet 中的 extra_inputs |
