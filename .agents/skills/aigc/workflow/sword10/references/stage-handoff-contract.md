# Stage Handoff Contract

本文件定义 `sword10` 在 `2-美学 -> 3-主体 -> 4-编剧 -> 5-导演 -> 6-分镜 -> 7-摄影 -> 8-分组` 之间的 canonical 输入输出链。

## Stage Chain

| stage | consumes | produces | stage skill |
| --- | --- | --- | --- |
| `2-美学` | `projects/aigc/<项目名>/1-分集/` all selected episode source or user-declared source packet | `projects/aigc/<项目名>/2-美学/类型风格.md`, `projects/aigc/<项目名>/2-美学/美学总览.md`, and six style protocol outputs | `.agents/skills/aigc/2-美学/SKILL.md` |
| `3-主体` | `projects/aigc/<项目名>/1-分集/` + `projects/aigc/<项目名>/2-美学/类型风格.md` + `2-美学` 角色/场景/道具风格协议 | `projects/aigc/<项目名>/3-主体/主体注册表.md`, `projects/aigc/<项目名>/3-主体/subject-registry.yaml`, and domain subject outputs | `.agents/skills/aigc/3-主体/SKILL.md` |
| `4-编剧` | `projects/aigc/<项目名>/1-分集/第N集.md` + `projects/aigc/<项目名>/2-美学/类型风格.md` + `projects/aigc/<项目名>/3-主体/主体注册表.md` | `projects/aigc/<项目名>/4-编剧/第N集.md` | `.agents/skills/aigc/4-编剧/SKILL.md` |
| `5-导演` | `projects/aigc/<项目名>/4-编剧/第N集.md` + `projects/aigc/<项目名>/2-美学/画面基调/全局风格协议.md` | `projects/aigc/<项目名>/5-导演/第N集.md` | `.agents/skills/aigc/5-导演/SKILL.md` |
| `6-分镜` | `projects/aigc/<项目名>/5-导演/第N集.md` + `2-美学/画面基调` and `2-美学/分镜风格` | `projects/aigc/<项目名>/6-分镜/第N集.md` | `.agents/skills/aigc/6-分镜/SKILL.md` |
| `7-摄影` | `projects/aigc/<项目名>/6-分镜/第N集.md` + `2-美学/画面基调` and `2-美学/摄影风格` | `projects/aigc/<项目名>/7-摄影/第N集.md` | `.agents/skills/aigc/7-摄影/SKILL.md` |
| `8-分组` | `projects/aigc/<项目名>/7-摄影/第N集.md` + `projects/aigc/<项目名>/3-主体/subject-registry.yaml` + optional `projects/aigc/<项目名>/0-初始化/north_star.yaml` | `projects/aigc/<项目名>/8-分组/第N集.md` | `.agents/skills/aigc/8-分组/SKILL.md` |

## Handoff Rules

1. 下游阶段只消费上一阶段 canonical 产物，不消费 workflow ledger 或主窗口摘要。
2. 续跑时若 `start_stage` 不是 `2-美学`，必须确认上一阶段产物和本表声明的额外输入存在且可信；否则回到缺失产物的 owning stage。
3. 每个阶段完成后只把路径、校验结果、失败码和必要统计交回主窗口。
4. `8-分组` 额外需要 `3-主体/subject-registry.yaml`；缺失时阻断正式 pass，不得在分组 YAML 中临时新增主体。旧项目存在 `0-初始化/north_star.yaml` 时可作为只读风格回读。
5. 阶段产物不得写入 legacy 英文路径或旧中文漂移路径。

## Resume Matrix

| requested start | required prior input | if missing |
| --- | --- | --- |
| `2-美学` | selected `1-分集` outputs or explicit source packet | stop with `FAIL-SWORD10-HANDOFF` |
| `3-主体` | selected `1-分集` outputs, `2-美学/类型风格.md`, and relevant style protocols | route back to `2-美学` or source packet repair |
| `4-编剧` | `1-分集/第N集.md`, `2-美学/类型风格.md`, and `3-主体/主体注册表.md` | route back to `3-主体`, `2-美学`, or source packet repair |
| `5-导演` | `4-编剧/第N集.md` and `2-美学/画面基调/全局风格协议.md` | route back to `4-编剧` or `2-美学` |
| `6-分镜` | `5-导演/第N集.md` and required `2-美学` style protocols | route failed episode back to `5-导演` or `2-美学` |
| `7-摄影` | `6-分镜/第N集.md` and required `2-美学` style protocols | route failed episode back to `6-分镜` or `2-美学` |
| `8-分组` | `7-摄影/第N集.md` and `3-主体/subject-registry.yaml` | route failed episode back to `7-摄影` or `3-主体` registry repair |

## Review Gate Mapping

| Review Question | Review Gate | Fail Code | Rework Target | Report Evidence |
| --- | --- | --- | --- | --- |
| 每个阶段是否只消费上一阶段 canonical 产物和本表声明的额外输入？ | `GATE-SWORD10-04` | `FAIL-SWORD10-HANDOFF` | 本文件 `Stage Chain`、`SKILL.md#Thinking-Action Node Map` | stage ledger 中的 input_path/output_path/extra_inputs |
| 续跑是否先验证上一阶段产物存在且可信？ | `GATE-SWORD10-01` | `FAIL-SWORD10-HANDOFF` | 本文件 `Resume Matrix`、`types/retry-from-stage/retry-from-stage.md` | preflight evidence table |
| `2-美学` 阶段是否产出 `类型风格.md`、父级总览和必要风格协议，供 `3-主体`、`4-编剧` 与后续阶段继承？ | `GATE-SWORD10-04` | `FAIL-SWORD10-HANDOFF` | `.agents/skills/aigc/2-美学/SKILL.md`、本文件 `Stage Chain` | stage ledger 中的 type/style protocol paths |
| `3-主体` 是否产出 `主体注册表.md` 与 `subject-registry.yaml`，供 `4-编剧` 和 `8-分组` 对齐命名？ | `GATE-SWORD10-04` | `FAIL-SWORD10-HANDOFF` | `.agents/skills/aigc/3-主体/SKILL.md`、本文件 `Stage Chain` | dispatch packet 中的 subject registry refs |
| `8-分组` 是否读取 `subject-registry.yaml`，而不是新增主体信息？ | `GATE-SWORD10-04` | `FAIL-SWORD10-HANDOFF` | `.agents/skills/aigc/8-分组/SKILL.md`、本文件 `Stage Chain` | dispatch packet 中的 extra_inputs |
