# CONTEXT.md

## Purpose & Loading Contract

- 本文件是 `.agents/skills/aigc/5-Image/3-图像生成` 的经验层知识库，不是过程日志。
- provider-specific 规范真源在 `references/`，本文件只记录类型化失败、修复顺序和可复用 heuristic。

## Context Health

- soft_limit_chars: 20000
- hard_limit_chars: 40000
- status: ok

## Type Map

| failure_or_outcome_type | root_cause_layer | immediate_fix | systemic_prevention | verification_point |
| --- | --- | --- | --- | --- |
| provider 仍是 `dual_mode/pending` 却直接写最终计划 | 路由裁决层 | 先回到 `G2` 锁唯一 provider | 在主合同固化“provider 不唯一不得落最终计划” | submit-plan 不再指向模糊 provider |
| 即梦 CLI 计划里塞进 BASE64 或 URL | provider 输入层 | 回退到 `local_path` | 在 `references/jimeng-cli.md` 固化本地路径直传 | Dreamina handoff 始终可上传 |
| NANO-banana 计划没写 BASE64-compatible 说明 | provider 输入层 | 补 `pending_encode` 或 ready base64 说明 | 在 `references/nano-banana.md` 固化 BASE64-compatible handoff | nano plan 不再缺运输层说明 |
| 计划文件有了，但没有唯一下一入口 | handoff 层 | 回到 `G5` 补下一入口与返工入口 | 在输出合同固化唯一 next entry | 执行者不再自己猜下一步 |
| 本层试图重新绑定图片或重写 prompt | 边界层 | 回退到 `2-参照引用` 或 `1-提示词蒸馏` | 在主合同固化阶段边界 | `3-图像生成` 保持提交前组织职责 |

## Repair Playbook

1. 先查请求对象是否真的可提交。
2. 再查 provider 是否唯一。
3. 再查引用运输层是否与 provider 匹配：
   - 即梦 CLI -> 本地路径
   - NANO-banana -> BASE64-compatible
4. 再查 `submit-plan.json + submit-brief.md` 是否齐备。
5. 最后查下一入口是否唯一清楚。

## Reusable Heuristics

- `3-图像生成` 的核心不是“执行生成”，而是“把 provider 选择和输入运输层写清楚”。
- 对这条链来说，`dual_mode` 适合停留在 `2-参照引用`，不适合直接进入最终生成计划。
- 即梦 CLI 与 NANO-banana 的主要分水岭，在图片输入承载形态，而不是 prompt 文案。
- 只要 provider-specific 输入解析还没写清，submit-plan 就还不是合格的 handoff 包。

