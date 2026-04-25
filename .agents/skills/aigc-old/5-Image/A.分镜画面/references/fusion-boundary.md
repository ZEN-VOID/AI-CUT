# Fusion Boundary

## Role

`A.分镜画面` 是单帧画面链路的融合入口。它不删除原三包，也不创建新的 runtime 业务真源；它负责把原三包的能力面在一次调用中按需路由、跳过、汇流和审计。

## Source Packages Kept

| legacy package | retained role | new owner in this package |
| --- | --- | --- |
| `1-提示词蒸馏/分镜帧` | 旧入口、prompt 装配 spec、兼容 runner；蒸馏方法已完整消化进新包 | `references/request-distillation.md`、`steps/frame-image-workflow.md` |
| `2-参照引用` | 旧入口、参照绑定脚本、provider-neutral 引用合同 | `references/reference-binding.md`、`references/provider-modules.md` |
| `3-图像生成` | 旧入口、submit-plan runner、provider handoff 合同 | `references/generation-handoff.md`、`references/provider-modules.md` |

## Canonical Runtime Slots

- 单帧请求：`projects/aigc/<项目名>/5-Image/分镜帧/<第N集>/第N集.json`
- 参照绑定：`projects/aigc/<项目名>/5-Image/2-参照引用/<mode>/<source_tranche>/<第N集>/`
- 图像 handoff：`projects/aigc/<项目名>/5-Image/3-图像生成/<provider>/<source_tranche>/<第N集>/`

这些路径继续作为兼容 runtime 真源。本包可以调度这些写位，但不得把 `.agents/skills/aigc/5-Image/A.分镜画面/` 自身变成项目运行时输出目录。

## Skip Rules

- 若只需 prompt JSON，跳过参照绑定与 handoff，但必须说明下一入口。
- 若已有稳定 request JSON，跳过蒸馏，但必须审计 `meta / prompt_style / model / prompt / prompt_char_count`。
- 若显式 `prompt_only / no_reference`，可跳过绑定，但必须在 handoff 说明中记录覆盖原因。
- 若 provider 不唯一，不能写最终 submit-plan，只能给推荐主案、备选案和缺口。

## Non-Loss Rule

旧包语义不得静默丢失。任何从旧三包迁入、折叠、降级或保留为兼容源的内容，都应能在 `references/legacy-upgrade-migration-matrix.md` 中追溯。
