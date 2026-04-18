# Validation Fact Pack Spec

## Purpose

`validation_fact_pack` 是 `3-Drafting` 输出给 `4-Validation` 与 checker 团队的最小事实包。

目标：

- 让 checker 基于当前系统真源评估，而不是凭旧大纲或上下文残留粗审。
- 把“承诺 / 编排 / 对象状态 / 伏笔静默区 / 风格门禁”同时纳入验证。

## Required Slices

### 1. `promise_slice`

回答：这本书此时对读者承诺了什么。

最少应包含：

- 题材走廊
- 平台 / 读者承诺
- 当前卷或当前章不能违反的核心 promise

### 2. `chapter_board`

回答：这一章按 `MAP` 必须发生什么。

最少应包含：

- 章节功能
- 关键事件
- 冲突 / 任务 / 线索 / 伏笔挂载
- 时间锚与集序位置

### 3. `cards_state_history_slice`

回答：这章相关对象进场时带着什么当前态与历史包袱。

最少应包含：

- 相关角色 `current_state/history`
- 相关场景约束
- 相关物品归属与状态

### 4. `foreshadow_silence_slice`

回答：哪些伏笔当前处于静默窗口，哪些信息还不能提前揭穿。

最少应包含：

- `has_active_foreshadowing`
- 活跃伏笔列表
- 静默区与禁止提前揭晓项

### 5. `style_gate`

回答：表达层有哪些强制门禁。

最少应包含：

- `anti_ai_required`
- `no_poison_required`
- 当前风格禁飞区 / 反冷评要求

## Source Mapping

| slice | 默认来源 |
|---|---|
| `promise_slice` | `0-Init` 最终确认项 + `Init/north_star_contract.json.cards` |
| `chapter_board` | `Planning/8-全息地图.json` |
| `cards_state_history_slice` | 相关 `Cards.current_state/history` |
| `foreshadow_silence_slice` | `MAP` 伏笔层 + 当前回收窗口 |
| `style_gate` | 风格契约 + `core-constraints` + Step 4 终检要求 |

## Hard Gate

- 五个 slice 任一缺失，视为 `FAIL-COVENANT`。
- checker 不得自行补猜缺失 slice。
- `4-Validation` 只能消费本轮动态生成的事实包，不得复用旧轮次残包。

## Minimal Shape

```json
{
  "validation_fact_pack": {
    "promise_slice": {},
    "chapter_board": {},
    "cards_state_history_slice": {},
    "foreshadow_silence_slice": {
      "has_active_foreshadowing": true
    },
    "style_gate": {
      "anti_ai_required": true,
      "no_poison_required": true
    }
  }
}
```
