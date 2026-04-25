# Provider Handoff Contract

本文件承接旧 `3-视频生成` 的 provider handoff 语义，负责 `generation-handoff/` 段。

## Scope

- 输入是 `distill/` 或 `reference-binding/` 中已经稳定的请求对象。
- 输出是 provider-neutral 的 `submit-plan.json` 与人工可读 `submit-brief.md`。
- 本段不直接提交、轮询或下载 provider 结果。

## Reference Mode

| reference_state | handoff mode | rule |
| --- | --- | --- |
| `bound` | `reference_driven` | `reference_images / image_markers` 已解析为真实 `Assets/` 主体路径 |
| `empty` | `prompt_only` | 用户或上游明确声明本轮不使用参照图，或项目确无可用主体资产 |
| `unresolved` | blocked | 存在可用主体资产或主体候选，但引用字段尚未解析 |

## Handoff Rules

- `submit-plan.json` 必须回链 source request、subject index、reference-binding manifest 和 provider selection。
- 若 provider 已明确，写唯一 provider；若未明确，只能写推荐主案和等待用户裁决，不得并列多个无序入口。
- 若 provider 当前只有槽位没有本地 `SKILL.md + CONTEXT.md`，必须说明它是 manual-only 或外部 provider 入口。
- `reference_driven` 必须写清每张主体参照图如何被 provider 消费；例如 Dreamina 需要最终解析为本地可上传路径。
- `prompt_only` 必须说明本轮没有绑定主体参照图，禁止伪造空引用参数。

## Handoff Output

- `generation-handoff/<provider>/submit-plan.json`
- `generation-handoff/<provider>/submit-brief.md`

最终必须给出唯一下一入口：

- 外部 provider skill
- 人工提交
- 回 `reference-binding`
- 回 `3-Detail`
- 等待 provider 裁决
