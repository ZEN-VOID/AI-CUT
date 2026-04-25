# Generation Handoff Contract

## Scope

承接组级 storyboard request JSON 或参照绑定 JSON，生成 provider-ready `submit-plan.json + submit-brief.md`。

## Provider Route

默认 provider 为 `builtin_image_gen`，即内置 `$imagegen` / `GPT-IMAGE-2` handoff。外部 provider 只在用户或上游显式要求时使用：

- `jimeng_cli`
- `nano_banana`

若 `provider_mode=dual_mode | pending`，不得写最终 provider plan，只能输出推荐主案、备选案和缺口。

## Handoff Requirements

`submit-plan.json` 必须写清：

- source request 路径
- provider 唯一结论
- input mode: `reference_driven | prompt_only | unresolved`
- provider-specific 输入运输层
- `output_dir`
- `expected_outputs`
- `next_entry`

`submit-brief.md` 必须解释：

- 为什么选择该 provider。
- 参照图如何被 provider 消费。
- 输出图像应回填到哪里。
- 若执行失败，回到哪个节点返工。

## Output Path Rule

真实输出图像必须与 `submit-plan.json` 和 `submit-brief.md` 同目录：

`projects/aigc/<项目名>/5-Image/3-图像生成/<provider>/<source_tranche>/<第N集>/`

`Assets/分镜画板/分镜故事板/` 只能保存派生副本，不是唯一 canonical 输出真源。
