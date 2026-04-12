# 分组执行报告

## 输入清单

- `projects/<项目名>/Init/north_star.yaml`
- `projects/<项目名>/Init/init_handoff.yaml`
- `projects/<项目名>/Init/episode-split-plan.json`
- `projects/<项目名>/规划/2-格式/第1集.md`

## 边界裁决摘要

- grouping_method: `multidimensional_quantized`
- 不可动约束：<集边界 / lock / 用户硬要求>
- 主要裁决依据：<结构锚点 / 依赖闭环 / 量化 / handoff>
- 终裁理由：<为什么采用当前边界集合>

## 量化摘要

- scene_unit_count: <整数>
- duration_policy: <<默认15秒>|<每组10秒>|<第3场每组8秒>|...>
- 默认组时长: <15秒|12秒|...>
- 分镜组时长映射: <{}|{"G03":"12秒"}|{"1-4-2":"10秒"}|...>
- 时长偏离证据: <[]|["north_star: ..."]|["user: ..."]|...>
- 分镜时间读取链: 分镜组时长映射 -> 默认组时长 -> 切分时长策略
- pace_tier: <<慢节奏>|<中节奏>|<快节奏>>
- base_text_window: <整数>
- warn_window: <<84-126>|<120-180>|...>
- hard_text_window: <整数>
- structure_unit_count: <整数>
- turning_point_count: <整数>
- hard_dependency_count: <整数>
- episode_load_score: <整数>
- recommended_group_band: <<1-2>|<2-3>|<3-4>|<4-5>|<5-6>>
- dependency_density: <小数>

## 集级边界继承检查

- 检查结果：PASS
- 说明：本轮未修改 `1-分集` 已锁定的集边界。

## 候选边界

- 候选边界 A：<描述>
- 候选边界 B：<描述>
- 排除理由：<为何未采用其他候选边界>

## 集内分组表

| episode | group_id | group_name | effective_text_chars | window_status | group_load_score | dependency | parallelism | note |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 第1集 | G01 | 潜入准备 | 136 | ok | 3 | none | 串行起点 | 开场任务触发 |
| 第1集 | G02 | 身份暴露 | 149 | ok | 3 | G01 | 需在 G01 后执行 | 依赖前组铺垫 |
| 第1集 | G03 | 脱身余波 | 120 | ok | 2 | G02 | 可与后续资产准备并行 | 依赖反转结果 |

## 依赖与并行性检查

- 可并行项：<哪些组或哪些下游动作可并行>
- 串行项：<哪些组或哪些下游动作必须串行>
- 原因：<依赖说明>

## 验收结论与返工项

- 结论：PASS
- 失败码：无
- 返工入口：无
