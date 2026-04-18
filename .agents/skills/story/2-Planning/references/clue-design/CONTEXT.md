# CONTEXT.md

## Purpose & Loading Contract

- 本文件是 `clue-design` 子模块的局部经验层，只服务 `2-Planning` 的 Step 6。
- 加载顺序固定为：先读同目录 `module-spec.md`，再按需读取本文件。
- 跨模块的信息链与回照链经验仍回写到 `2-Planning/CONTEXT.md`。

## Context Health

- soft_limit_chars: 40000
- hard_limit_chars: 80000
- soft_limit_cases: 80
- hard_limit_cases: 140
- status: ok

## Type Map

| failure_or_outcome_type | root_cause_layer | immediate_fix | systemic_prevention | verification_point |
| --- | --- | --- | --- | --- |
| 线索只有结论没有发现路径 | step contract | 回到证据源与发现链设计 | 在 `module-spec.md` 固化五段线索链 | 角色获得信息的路径可追踪 |
| 误导只是遮蔽信息 | fairness design | 用可纠偏的证据误导替代作者硬骗 | 把公平误导三条件写成硬门禁 | 读者与角色都能在事后回看证据 |
| 线索与伏笔混写 | boundary control | 回划“当前可求证”与“未来再理解”的边界 | 固化 Step 7 必读本模块的边界说明 | Step 7 不再重复线索系统 |

## Repair Playbook

1. 先判定证据源和承载物，再设计发现路径。
2. 用任务链反查角色为何能接近这些证据。
3. 误导只允许建立在真实证据之上，并保留纠偏点。
4. 收尾把信息获得节点挂回 holomap 检查可消费性。

## Reusable Heuristics

- 线索设计最怕“作者知道，所以角色也突然知道”。
- 真正好用的误导不是藏信息，而是让错误解释暂时更像真相。
- 如果 holomap 里看不出角色这一章获得了什么信息，通常说明 Step 6 还没闭环。

