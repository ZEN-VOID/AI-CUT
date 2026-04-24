# Provider Handoff Contract

本文件承接旧 `3-视频生成` 的核心语义，负责 `generation-handoff/` 段。

## Ownership

`generation-handoff/` 拥有：

- provider 路由裁决或推荐主案。
- `submit-plan.json` 与 `submit-brief.md`。
- request readiness 检查。
- `reference_driven / prompt_only / unresolved` 引用模式判定。
- 唯一下一入口。

`generation-handoff/` 不拥有：

- 修改上游 distill 或 reference-binding 请求对象。
- 直接代替外部 provider skill 提交、轮询或下载。
- 把 provider 槽位目录冒充成本地已实现能力。

## Input Mode

| mode | 条件 | 行动 |
| --- | --- | --- |
| `reference_driven` | 引用字段已经绑定真实 `Assets/` 路径 | 写 provider-specific 解析策略和提交计划 |
| `prompt_only` | 用户或上游明确声明本轮不使用参照图 | 写纯 prompt handoff，并明确无参照 |
| `unresolved` | `Assets/` 有可用图、用户未声明 no-reference，或引用字段混有占位 | 停止，回 `reference-binding/` |

## Provider Slot Semantics

- `grok`、`kling`、`seedance`、`sora`、`veo`、`vidu` 等名称可作为 handoff target。
- 只有补齐独立 `SKILL.md + CONTEXT.md` 的 provider，才算本地 governed child skill。
- manual-only provider 必须保留完整 handoff 包，不得伪造自动执行链。

## Submit Plan Minimum Schema

- `source_request`
- `provider_selection`
- `input_mode`
- `provider_input_resolution`
- `output_dir`
- `handoff`
- `rework_entry`
- `risk_notes`

## Output

- `generation-handoff/<provider>/submit-plan.json`
- `generation-handoff/<provider>/submit-brief.md`

最低通过标准：

- 不得只说“去用某 provider”。
- `submit-plan.json` 必须回链 source request。
- `submit-brief.md` 必须说明边界、风险、返工入口与下一入口。
- provider 只有槽位时必须明确标注 manual-only 或 external-skill-required。
