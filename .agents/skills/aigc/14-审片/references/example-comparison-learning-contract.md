# Example Comparison Learning Contract

本合同用于处理用户显式提供的好示例、坏示例、参考片、反例、标杆视频或风格偏好。示例只在可观察维度上生效，不得把一次性偏好误写成永久硬规则。

## Accepted Examples

- 好示例：用户明确认可的目标片、同项目成功片段、参考风格片段。
- 坏示例：用户明确否定的废片、平庸片、错风格片、模型失败片。
- 成对示例：同一 prompt、同一分镜组或同一风格目标下的好/坏对照。
- 批量示例：多个视频或截图构成的偏好集合。

## Comparison Procedure

1. 锁定示例角色：`good_example`、`bad_example`、`mixed_reference` 或 `unknown_reference`。
2. 只提炼可观察维度：主体清晰度、动作可读性、节奏、构图、光影、材质、风格一致性、叙事推进、记忆点、AIGC 瑕疵。
3. 将目标视频分别与好示例和坏示例比较，输出“靠近好示例的点”和“落入坏示例的点”。
4. 判断差距来源：prompt 不足、模型执行失败、分镜组密度、审美目标不清或素材本身不可用。
5. 给出可执行修复：rerun、改 prompt、改分镜组、换路线、源层候选或只记录偏好。

## Learning Rule

可以沉淀到本技能 `CONTEXT.md` 的学习必须同时满足：

- 用户显式把示例标为好/坏，或在多轮中稳定表达同一偏好。
- 结论能转写为可观察的鉴赏 heuristic，而不是“喜欢/不喜欢”。
- 不与项目 `MEMORY.md`、根 `AGENTS.md`、`5-分组` 真源或用户当前指令冲突。
- 不会把单个项目口味误提升为所有项目的强制规则；项目专属偏好应写入项目 `MEMORY.md`，技能级鉴赏力只沉淀跨项目可复用判断。

## Learning Output Shape

写入 `CONTEXT.md` 时使用短条目，放入 `Aesthetic Calibration Heuristics`：

```text
- 从用户好/坏示例对比中学习：当 <可观察条件> 时，优先判定为 <质量判断>；修复建议是 <动作>。适用范围：<范围>。
```

不要写入原始视频长描述、用户隐私信息、临时文件路径或一次性任务过程。

## Review Gate Mapping

| Review Question | Review Gate | Fail Code | Rework Target | Report Evidence |
| --- | --- | --- | --- | --- |
| 用户提供的示例是否已被锁定为 `good_example`、`bad_example`、`mixed_reference` 或 `unknown_reference`，且角色来自用户标签或可说明的上下文？ | `GATE-REVIEW-07` | `FAIL-REVIEW-EXAMPLE-CALIBRATION` | `steps/video-review-workflow.md#N2 Source Lock`、本文件 `Accepted Examples` / `Comparison Procedure` | 报告中的 `example_refs`、示例角色、用户标签或不确定性说明 |
| 示例是否只被转写为主体、动作、节奏、构图、光影、材质、风格一致性、叙事推进、记忆点、AIGC 瑕疵等可观察维度，而不是“喜欢/不喜欢”口号？ | `GATE-REVIEW-07` / `GATE-REVIEW-06` | `FAIL-REVIEW-EXAMPLE-CALIBRATION` | `steps/video-review-workflow.md#N4 Method Palette Compare`、本文件 `Comparison Procedure` | 报告中的 `observable_example_dimensions` 或等价维度列表 |
| 目标视频是否分别写明“靠近好示例的点”和“落入坏示例的点”，并把差距归因到 prompt、模型、分组密度、审美目标或素材不可用？ | `GATE-REVIEW-07` / `GATE-REVIEW-09` | `FAIL-REVIEW-EXAMPLE-CALIBRATION` | `steps/video-review-workflow.md#N4 Method Palette Compare`、`references/review-dimensions-contract.md#Mismatch Attribution` | finding 中的 good/bad delta、`root_cause_guess`、示例对照证据 |
| 示例差距是否被转成可执行修复路线，而不是停留在泛泛审美评价？ | `GATE-REVIEW-10` | `FAIL-REVIEW-LANDING` | `steps/video-review-workflow.md#N5 Landing And Operation Design`、`references/finding-landing-contract.md` | 每条相关 finding 的 `landing`、`confidence`、rerun / group repair / source candidate 理由 |
| 学习写入是否同时满足稳定偏好、可观察 heuristic、无冲突、跨项目可复用；项目专属偏好是否回到项目 `MEMORY.md` 而非本技能经验层？ | `GATE-REVIEW-07` / `GATE-REVIEW-12` | `FAIL-REVIEW-EXAMPLE-CALIBRATION` | `steps/video-review-workflow.md#N6 Write And Verify`、本文件 `Learning Rule` / `Learning Output Shape`、同目录 `CONTEXT.md#Aesthetic Calibration Heuristics` | `CONTEXT.md` 变更摘要，或报告中的 `learning_not_written_reason` / `project_memory_target` |
