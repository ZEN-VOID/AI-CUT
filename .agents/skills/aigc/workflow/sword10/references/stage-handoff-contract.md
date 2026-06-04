# Stage Handoff Contract

本文件定义 `sword10` 在 `2-编剧 -> 3-美学 -> 4-导演 -> 5-表演 -> 6-氛围 -> 7-分镜 -> 8-摄影 -> 9-光影 -> 10-分组` 之间的 canonical 输入输出链。

## Stage Chain

| stage | consumes | produces | stage skill |
| --- | --- | --- | --- |
| `2-编剧` | `projects/aigc/<项目名>/1-分集/第N集.md` | `projects/aigc/<项目名>/2-编剧/第N集.md` | `.agents/skills/aigc/2-编剧/SKILL.md` |
| `3-美学` | `projects/aigc/<项目名>/2-编剧/` selected episodes or user-declared source packet | `projects/aigc/<项目名>/3-美学/美学总览.md` and six style protocol outputs | `.agents/skills/aigc/3-美学/SKILL.md` |
| `4-导演` | `projects/aigc/<项目名>/2-编剧/第N集.md` + `projects/aigc/<项目名>/3-美学/画面基调/全局风格协议.md` | `projects/aigc/<项目名>/4-导演/第N集.md` | `.agents/skills/aigc/4-导演/SKILL.md` |
| `5-表演` | `projects/aigc/<项目名>/4-导演/第N集.md` + declared `3-美学` style context | `projects/aigc/<项目名>/5-表演/第N集.md` | `.agents/skills/aigc/5-表演/SKILL.md` |
| `6-氛围` | `projects/aigc/<项目名>/5-表演/第N集.md` + declared `3-美学` style context | `projects/aigc/<项目名>/6-氛围/第N集.md` | `.agents/skills/aigc/6-氛围/SKILL.md` |
| `7-分镜` | `projects/aigc/<项目名>/6-氛围/第N集.md` + `3-美学/画面基调` and `3-美学/分镜风格` | `projects/aigc/<项目名>/7-分镜/第N集.md` | `.agents/skills/aigc/7-分镜/SKILL.md` |
| `8-摄影` | `projects/aigc/<项目名>/7-分镜/第N集.md` + `3-美学/画面基调` and `3-美学/摄影风格` | `projects/aigc/<项目名>/8-摄影/第N集.md` | `.agents/skills/aigc/8-摄影/SKILL.md` |
| `9-光影` | `projects/aigc/<项目名>/8-摄影/第N集.md` + declared `3-美学` style context | `projects/aigc/<项目名>/9-光影/第N集.md` | `.agents/skills/aigc/9-光影/SKILL.md` |
| `10-分组` | `projects/aigc/<项目名>/9-光影/第N集.md` + `projects/aigc/<项目名>/0-初始化/north_star.yaml` | `projects/aigc/<项目名>/10-分组/第N集.md` | `.agents/skills/aigc/10-分组/SKILL.md` |

## Handoff Rules

1. 下游阶段只消费上一阶段 canonical 产物，不消费 workflow ledger 或主窗口摘要。
2. 续跑时若 `start_stage` 不是 `2-编剧`，必须确认上一阶段产物和本表声明的额外输入存在且可信；否则回到缺失产物的 owning stage。
3. 每个阶段完成后只把路径、校验结果、失败码和必要统计交回主窗口。
4. `10-分组` 额外需要 `0-初始化/north_star.yaml`；缺失时阻断，不得用口头风格摘要替代。
5. 阶段产物不得写入 legacy 英文路径或旧中文漂移路径。

## Resume Matrix

| requested start | required prior input | if missing |
| --- | --- | --- |
| `2-编剧` | `1-分集/第N集.md` | stop with `FAIL-SWORD10-HANDOFF` |
| `3-美学` | selected `2-编剧` outputs or explicit source packet | route back to `2-编剧` or source packet repair |
| `4-导演` | `2-编剧/第N集.md` and `3-美学/画面基调/全局风格协议.md` | route back to `2-编剧` or `3-美学` |
| `5-表演` | `4-导演/第N集.md` and declared `3-美学` style context | route failed episode back to `4-导演` or `3-美学` |
| `6-氛围` | `5-表演/第N集.md` and declared `3-美学` style context | route failed episode back to `5-表演` or `3-美学` |
| `7-分镜` | `6-氛围/第N集.md` and required `3-美学` style protocols | route failed episode back to `6-氛围` or `3-美学` |
| `8-摄影` | `7-分镜/第N集.md` and required `3-美学` style protocols | route failed episode back to `7-分镜` or `3-美学` |
| `9-光影` | `8-摄影/第N集.md` and required `3-美学` style protocols | route failed episode back to `8-摄影` or `3-美学` |
| `10-分组` | `9-光影/第N集.md` and `north_star.yaml` | route failed episode back to `9-光影` or `0-初始化` evidence repair |

## Review Gate Mapping

| Review Question | Review Gate | Fail Code | Rework Target | Report Evidence |
| --- | --- | --- | --- | --- |
| 每个阶段是否只消费上一阶段 canonical 产物和本表声明的额外输入？ | `GATE-SWORD10-04` | `FAIL-SWORD10-HANDOFF` | 本文件 `Stage Chain`、`SKILL.md#Thinking-Action Node Map` | stage ledger 中的 input_path/output_path/extra_inputs |
| 续跑是否先验证上一阶段产物存在且可信？ | `GATE-SWORD10-01` | `FAIL-SWORD10-HANDOFF` | 本文件 `Resume Matrix`、`types/retry-from-stage/retry-from-stage.md` | preflight evidence table |
| `3-美学` 阶段是否产出父级总览和必要风格协议，供后续阶段继承？ | `GATE-SWORD10-04` | `FAIL-SWORD10-HANDOFF` | `.agents/skills/aigc/3-美学/SKILL.md`、本文件 `Stage Chain` | stage ledger 中的 style protocol paths |
| `10-分组` 是否读取 `north_star.yaml`，而不是使用口头摘要？ | `GATE-SWORD10-04` | `FAIL-SWORD10-HANDOFF` | `.agents/skills/aigc/10-分组/SKILL.md`、本文件 `Stage Chain` | dispatch packet 中的 extra_inputs |
