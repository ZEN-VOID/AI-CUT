# Type Package: adjacent-frame-state

适用于需要逐画面回顾上一最终位置或状态的连续运动。

## Fixed Context

- 每个 motion unit 消费上一 unit 的 `final_state`。
- 同一分镜组或连续动作段默认沿用 `primary_reference_frame`；场景切换、主体离开参照范围或动作重心转移时可重置 reference_frame，但必须记录重置原因。
- 如果上一状态和当前 source 明确矛盾，优先尊重 source，并报告连续性断点。

## State Priority

1. 角色位置。
2. 身体姿态和朝向。
3. 与他人或道具的接触关系。
4. 手中物或可见负载。
5. 注意力落点。
