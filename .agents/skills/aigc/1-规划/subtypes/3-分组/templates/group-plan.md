# 分组总览

## 分组目标

- 项目名：<项目名>
- 范围：<涉及集数或范围>
- 输出粒度：按集落盘，集内分组

## 边界裁决摘要

- grouping_method: `multidimensional_quantized`
- 不可动约束：<集边界 / hard lock / 用户硬要求>
- 主要裁决依据：<结构锚点 / 依赖闭环 / 量化 / handoff>
- 放弃相邻候选的原因：<为什么不是前一个或后一个切点>

## 量化摘要

- scene_unit_count: <整数>
- duration_policy: <<默认15秒>|<每组10秒>|<第3场每组8秒>|...>
- pace_tier: <<慢节奏>|<中节奏>|<快节奏>>
- base_text_window: <整数>
- warn_window: <<84-126>|<120-180>|...>
- hard_text_window: <整数>
- structure_unit_count: <整数>
- turning_point_count: <整数>
- hard_dependency_count: <整数>
- episode_load_score: <整数>
- recommended_group_band: <<1-2>|<2-3>|<3-4>|<4-5>|<5-6>>

## 集级总览表

| episode | grouping_method | duration_policy | pace_tier | episode_load_score | recommended_group_band | group_count | grouping_focus | downstream_entry | dependency_note |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 第1集 | multidimensional_quantized | 默认15秒 | 中节奏 | 7 | 3-4 | 3 | 潜入-暴露-脱身 | 1-规划/4-节奏 | G02 依赖 G01 的信息揭示 |
