# Performance Type Map

## Purpose

本类型包为 `4-表演` 建立 `performance_type_profile`。它只负责判型和路由，不直接生成表演正文；核心表演工艺仍由 LLM 在 workflow 节点中完成。

## Type Profile Variables

| variable | values | detection cue | routed node |
| --- | --- | --- | --- |
| `psychological_reaction_density` | `high` / `normal` / `low` | `心理反应`、抽象认知、主观情绪标签密集 | `N3-PERF-PSYCHOLOGICAL` |
| `actor_control_need` | `required` / `optional` / `not_applicable` | 关键情绪 beat、压抑/爆发/情绪切换、模板化表情风险 | `N4-PERF-ACTOR-CONTROL` |
| `subtext_behavior_need` | `required` / `optional` / `not_applicable` | 潜台词、信任变化、试探、未出口对白 | `N5-PERF-SCENE-CRAFT` |
| `scene_turn_need` | `required` / `optional` / `not_applicable` | 场景进入/转折/退出状态不清，关键场景平铺 | `N5-PERF-SCENE-CRAFT` |
| `blocking_power_need` | `required` / `optional` / `not_applicable` | 权力关系、空间压迫、站坐高低、道具归属可见化不足 | `N6-PERF-BLOCKING` |
| `silence_reaction_need` | `required` / `optional` / `not_applicable` | 沉默、反应空白、声音空缺、动作余波 | `N5-PERF-SCENE-CRAFT` |
| `advisor_need` | `required` / `optional` / `not_applicable` | 用户要求、项目 team 配置或 subagents 模式启动 | `N6.5-PERF-ADVISOR` |

## Output Shape

```yaml
performance_type_profile:
  psychological_reaction_density: high | normal | low
  actor_control_need: required | optional | not_applicable
  subtext_behavior_need: required | optional | not_applicable
  scene_turn_need: required | optional | not_applicable
  blocking_power_need: required | optional | not_applicable
  silence_reaction_need: required | optional | not_applicable
  advisor_need: required | optional | not_applicable
  routed_nodes:
    - N3-PERF-PSYCHOLOGICAL
    - N4-PERF-ACTOR-CONTROL
```

## Route Rules

- 任一 `required` 类型必须进入对应节点并在 `thinking_action_node_ledger` 留证。
- `advisor_need=required` 时必须进入 `N6.5-PERF-ADVISOR`，不得把顾问上下文并入 `N7-PERF-DRAFT` 后补。
- 类型画像只改变处理深度和 routeback，不授权新增剧情事实、对白、场景或摄影方案。
