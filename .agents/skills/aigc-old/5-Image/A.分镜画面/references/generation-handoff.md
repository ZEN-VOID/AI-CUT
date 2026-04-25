# Generation Handoff Contract

## Purpose

把稳定 request JSON 或 reference-bound JSON 组织为 provider-ready handoff 包。此处完成只表示提交准备就绪，不表示图片已生成成功。

## Provider Decision

1. 用户显式指定 provider 时，锁定对应 provider。
2. 输入 `meta.provider_mode` 已锁定时，优先消费该模式。
3. 未明确 provider 时，默认 `builtin_image_gen`。
4. `jimeng_cli` 与 `nano_banana` 是外部 fallback，不是默认路径。
5. `dual_mode / pending` 不得直接写最终 provider plan。

## Canonical Landing

- `projects/aigc/<项目名>/5-Image/3-图像生成/<provider>/<source_tranche>/<第N集>/submit-plan.json`
- `projects/aigc/<项目名>/5-Image/3-图像生成/<provider>/<source_tranche>/<第N集>/submit-brief.md`
- `projects/aigc/<项目名>/5-Image/3-图像生成/<provider>/<source_tranche>/<第N集>/<image_id>.<ext>`

## Handoff Rules

1. `submit-plan.json` 必须记录 source request、readiness verdict、provider、input_mode、provider_input_resolution、output_dir、expected_outputs、next_entry。
2. `output_dir` 必须等于 submit 包所在目录。
3. 远程 URL、task id、seed、原始 provider 响应只能作为 metadata 或 sidecar 证据。
4. `Assets/` 只能接收派生副本，不能替代 submit 包同目录 canonical 输出。
5. 若项目 `Assets/` 非空且没有显式 `prompt_only / no_reference`，空引用请求必须先回到参照绑定。

## Completion

完成口径固定为 `request_ready` 或 `handoff_ready`。只有执行层实际产图并复制回 `output_dir` 后，才可记录 `result_outputs[]`。
