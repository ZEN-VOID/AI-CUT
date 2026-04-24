# Provider Handoff Contract

本文件承接旧 `3-视频生成` 的核心语义，负责 `generation-handoff/` 段的提交前组织。

## Scope

- 输入是 `distill/` 或 `reference-binding/` 段产出的稳定 request JSON。
- 输出是 provider-neutral 到 provider-specific 的 handoff 包。
- 本段不直接提交、轮询或下载视频，也不越权回写上游 `3-Detail` 或 request JSON。

## Readiness Gates

1. `source_request` 存在且结构完整。
2. `reference_images / image_markers` 状态已经判定为：
   - `reference_driven`：引用字段已绑定真实资产。
   - `prompt_only`：本轮明确不使用参照图。
   - `unresolved`：项目存在候选资产或引用骨架未解析，但尚未完成绑定。
3. 若状态为 `unresolved`，必须回 `reference-binding/`，不得继续生成 provider plan。
4. 若 provider 只是 `3-视频生成/providers/` 中的槽位，没有 `SKILL.md + CONTEXT.md`，必须标记为 `manual_only` 或外部执行入口。

## Handoff Output

- `generation-handoff/<provider>/submit-plan.json`
- `generation-handoff/<provider>/submit-brief.md`

`submit-plan.json` 至少包含：

- `source_request.path`
- `provider.id`
- `input_mode`
- `provider_input_resolution`
- `output_dir`
- `handoff.next_entry`
- `rework_entry`

`submit-brief.md` 至少包含：

- 本轮边界
- provider 选择理由
- 引用解析策略
- 风险与暂停点
- 唯一下一入口
