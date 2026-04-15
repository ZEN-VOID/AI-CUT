# CONTEXT.md

## Purpose & Loading Contract

- 本文件是 `.agents/skills/aigc/5-Image/3-图像生成` 的经验层知识库，不是过程日志。
- 调用本技能时，应先加载根 `aigc`、`5-Image` 阶段父级、`1-提示词蒸馏`、`2-参照引用` 与本技能主合同。
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
| 真实输出图像落到 provider cache、`Assets/` 或阶段根，和 `submit-plan` 不在同一目录 | 输出路径合同层 | 在 `submit-plan` 写入同目录 `output_dir / expected_outputs`，执行后把 `result_outputs` 回填到同目录 | 在主合同和 provider references 固化“提交包与结果同目录”，`Assets/` 只允许派生副本 | 打开 `5-Image/3-图像生成/<provider>/<source_tranche>/<第N集>/` 即可同时看到计划、简报与本地图像 |
| `Assets/` 中已有可用图片，但空引用请求仍被直接落成 provider 计划 | 引用模式分流层 | 停止生成计划，先回 `2-参照引用` 运行保守绑定和严格审计 | 在 Readiness Gate 固化“Assets 非空 + 未显式 prompt-only = unresolved” | submit-plan 只消费通过审计的绑定 JSON，或明确记录显式 prompt-only |
| submit-plan 只写 provider，却没写默认后台批量并发执行参数 | 执行 handoff 层 | 在计划中补 `execution_mode / max_concurrent / request_batch_path / foreground_override` | 共享 `image-generation-execution-contract.md` 成为 `3-图像生成` 与 provider references 的执行模式真源 | submit-plan 能区分 `background_submitted` 与真实 `result_outputs` |

## Repair Playbook

1. 先查请求对象是否真的可提交。
2. 再查 provider 是否唯一。
3. 再查项目 `Assets/` 是否非空；若非空且本轮没有显式 `prompt_only / no_reference`，空引用必须先回 `2-参照引用`。
4. 再查引用运输层是否与 provider 匹配：
   - 即梦 CLI -> 本地路径
   - NANO-banana -> BASE64-compatible
5. 再查 `submit-plan.json + submit-brief.md` 是否齐备。
6. 再查 `output_dir / expected_outputs` 是否指向 submit 包同目录。
7. 最后查下一入口是否唯一清楚。
8. 再查执行参数是否继承后台批量并发默认：`execution_mode=background-batch-concurrent`，`max_concurrent=100`，且有前台覆盖说明。

## Reusable Heuristics

- `3-图像生成` 的核心不是“执行生成”，而是“把 provider 选择和输入运输层写清楚”。
- 对这条链来说，`dual_mode` 适合停留在 `2-参照引用`，不适合直接进入最终生成计划。
- 即梦 CLI 与 NANO-banana 的主要分水岭，在图片输入承载形态，而不是 prompt 文案。
- 只要 provider-specific 输入解析还没写清，submit-plan 就还不是合格的 handoff 包。
- provider 执行结果不要只留在外部工具默认下载目录或 `Assets/`；最稳的 canonical 落点是 submit 包所在目录，后续资产库副本再从这里派生。
- `Assets` 非空时，空引用不能自动等同 prompt-only；除非用户或上游明确声明不用参照图，否则它代表绑定链路未完成。
- `3-图像生成` 的完成口径是稳定 handoff，不是 provider 结果；后台批量并发提交态必须写成 `background_submitted`，最终产图由 `result_outputs` 或本地文件复核。
