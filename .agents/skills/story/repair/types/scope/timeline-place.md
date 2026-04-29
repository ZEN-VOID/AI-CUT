# Scope Package: Timeline Place

## Selection Signals

- 时间线、日期、年龄、历史年代、季节、行军耗时、地点、路线、空间动线、地理边界。

## When X Then Check X

| when | must check |
| --- | --- |
| 改历史年代或真实边界 | north_star、整体规划、项目 CONTEXT、历史边界说明 |
| 改日期/季节/年龄 | 前后章时间锚、角色年龄、旅程耗时、后续时间引用 |
| 改地点或路线 | 场景卡、地图/路线、上一次到达/离开、下一站 |
| 改空间动线 | 当前场景入口/出口、人物位置、追逃/战斗可达性 |

## Required Impact Additions

- `timeline_anchor_refs`
- `historical_boundary_refs`
- `route_refs`
- `location_state_refs`
- `downstream_time_place_refs`

## Review Gate

- 年代、地点、路线耗时和人物位置不穿帮。
- 历史边界不被主角行动静默改写。
