# Loopback Actualization Spec

## Purpose

本文件定义 `5-Loopback` 的 validated actualization 合同。

它回答两个问题：

1. 哪些 `PASS` 后的变化可以变成未来会继续被当真的 truth
2. 这些变化应该写进哪里，而不是互相覆盖

## PASS-only Gate

只有当 `4-Validation.validation_status = PASS` 时，才允许：

- 回写 `Cards.current_state/history`
- 更新 `story_map.actualization`
- 刷新 writer / planning / query projection

非 `PASS` 场景：

- 禁止 actualization 写回
- 只允许回到修复、恢复或卫星路由

## Truth Split

### 写入 `Cards`

适用：对象状态已经变化，且后续章节必须继续当真。

典型对象：

- 角色身份 / 伤势 / 立场 / knowledge state
- 关系信任 / 敌意 / 依赖 / 盟约
- 物品持有 / 激活 / 耗尽 / 损坏
- 场景封锁 / 损毁 / 常驻压力

### 写入 `story_map.actualization`

适用：规划节点已经被执行到某个状态。

典型对象：

- `episode_nodes`
- `clue_points`
- `foreshadow_points`
- `promise_threads`
- `suspense_threads`
- `tasklines`
- `threads`

硬规则：

- 只能新增 `actualization / actual_* / validated_*`
- 禁止覆盖 `planned_*`

### 写入 projection

适用：下游运行时需要立即看到的新默认视图。

例如：

- writer context projection
- 下一集 carryover context
- runtime marker / dirty flag

## Delta Shape

建议统一提纯为：

```json
{
  "card_deltas": [],
  "map_deltas": [],
  "projection_refresh": [],
  "evidence_refs": []
}
```

说明：

- `card_deltas` 只写 validated 的对象态变化
- `map_deltas` 只写 validated 的规划执行态变化
- `evidence_refs` 必须能回指 manuscript / validation / draft packet / map / card

## Artifact Contract

正式产物：

- `Loopback/第N集.loopback.json`

生成前必须读取：

- `5-Loopback/templates/loopback.json`

## Guardrails

- 不新造第二张“动态卡”
- 不把 suspense、高潮打法、局部文面处理回写进 Cards
- 不把单集临时裁决误写成长期对象属性
- 先提纯 delta，再写回 truth，不直接在原卡或原 MAP 上手工散改
