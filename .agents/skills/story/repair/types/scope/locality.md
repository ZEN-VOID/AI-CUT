# Scope Package: Locality

## Selection Signals

- 用户指向某章、某段、某条线索、某个伏笔、某个角色状态、某个物件机制或某个 finding。

## Fixed Context

- 局部不是修复范围的上限，只是影响图的起点。
- 必须向上查 canonical owner，向左查同层前列，向下查已产物和后续消费者。
- 若目标是线索或伏笔，至少检查首次埋点、最近推进、当前改动点、后续兑现点。
- 本包只解决“目标局部在哪里”；具体“当 XX 时检查 XX”由同目录 typed scope 包和 `references/impact-scope-contract.md#Universal Type Matrix` 决定。

## Review Gate

- `impact_map.current_locality` 可定位。
- 至少列出一个 upstream 或说明 upstream unaffected 的证据。
- 至少检查一个 same-layer predecessor，若不存在需说明原因。
