# Output Quality Contrast

用于分析好/坏示例在表达质量、结构完整度、细节密度、风格和任务完成度上的差异。

## Fixed Checks

- 好示例是否更完整覆盖任务要求，而不是单纯更长。
- 好示例是否有明确结构、层次、字段和收束。
- 坏示例是否存在空泛套话、未解释判断、跳过关键细节或风格错位。
- 差异是否应落到目标 `SKILL.md` Output Contract、`steps/` 执行节点、`templates/` 输出样板或目标 `CONTEXT.md` 经验层。

## Patch Bias

- 稳定输出形态问题优先修 `templates/` 和 Output Contract。
- 执行判断深度问题优先修 `steps/`。
- 口味和表达偏好优先写入目标 `CONTEXT.md` 或项目 `MEMORY.md`，不要直接写死为全局规则。
