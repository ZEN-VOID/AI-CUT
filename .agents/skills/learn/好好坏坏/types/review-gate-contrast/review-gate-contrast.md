# Review Gate Contrast

用于分析坏示例为什么没有被拦截，以及好示例体现了哪些可复用验收标准。

## Fixed Checks

- 坏示例是否违反了已有 `review/` gate，却未触发失败。
- 目标 skill 是否只有口号式 review，缺少 finding shape、verdict 或 fail condition。
- 好示例是否能转化为可执行验收维度，而不是仅作为风格偏好。
- 验收是否需要本地 checklist、结构 validator、脚本校验或用户显式授权的外部 reviewer。

## Patch Bias

- 漏检优先修 `review/review-contract.md`。
- 如果验收需要结构字段，必须同步 `templates/` 和 Output Contract。
- 若上层策略阻断真实 subagent/reviewer，必须报告降级路径并执行本地 checklist。
