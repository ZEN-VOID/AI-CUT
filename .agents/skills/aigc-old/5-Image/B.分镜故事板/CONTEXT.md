# CONTEXT.md

## Purpose & Loading Contract

- 本文件是 `B.分镜故事板` 的经验层知识库，不是过程日志。
- 调用 `.agents/skills/aigc/5-Image/B.分镜故事板/SKILL.md` 时，必须同时加载本文件。
- 新经验优先写入本文件；只有稳定、可重复、高置信的规则才晋升到 `SKILL.md` 或对应分区。

## Context Health

```yaml
monitor_version: 1
soft_limit_chars: 20000
hard_limit_chars: 40000
status: ok
last_checked_at: 2026-04-24
```

## Type Map

| failure_or_outcome_type | root_cause_layer | immediate_fix | systemic_prevention | verification_point |
| --- | --- | --- | --- | --- |
| 组级故事板被误路由成单帧画面 | 对象判定层 | 回到 `S0-S1`，要求唯一 `分镜组ID` 和多条或可组合的 `source_shot_ids` | 在 `Input Contract` 中固定单帧与故事板互斥 | request JSON 中 `meta.source_tranche=分镜故事板` 且 `source_shot_ids` 回链组内镜头 |
| prompt 仍由旧脚本主创 | LLM 主创层 | 改为 LLM 直出 canonical prompt，再让脚本仅做投影或校验 | 在 `LLM-First Creative Authorship Contract` 固化脚本边界 | prompt 生成过程能说明 LLM 裁决来源 |
| 多格 storyboard 退化成整组剧情摘要 | Prompt 结构层 | 回到 `S2-S4`，恢复固定前缀、组级设计块和组内多镜融写列 | `request-distillation.md` 固化多镜逐行覆盖 | prompt 能回链每个组内镜头 |
| 参照绑定过量 | 候选证据层 | 重跑保守绑定，只放行完整主体、主空间锚点或显式 marker | `reference-binding.md` 固化泛词、子串、多义候选阻断 | `match-report.md` 同时列 bound / ambiguous / rejected |
| provider 仍是 `dual_mode` 却写最终计划 | provider 路由层 | 回到 `S7` 锁唯一 provider 或只输出推荐主案 | 在 `generation-handoff.md` 固化 provider 不唯一不得落最终计划 | submit-plan 中 provider 唯一 |
| 真实图像路径漂到 `Assets/` 或 provider cache | 输出治理层 | 把 canonical 输出路径回到 submit 包同目录 | 在 handoff 合同固定 `output_dir == submit 包目录` | submit-plan 与 expected/result outputs 同目录 |
| 新包只转链旧三包，没有融合裁决 | 复合输出层 | 回到 `steps/storyboard-sheet-workflow.md` 补汇流与跳过规则 | 在 `fusion-boundary.md` 固化新包 owner 与旧包兼容角色 | 用户闭环能说明三段执行、跳过与返工入口 |

## Repair Playbook

1. 先判断本轮是 `storyboard_full`、`distill_only`、`bind_only`、`handoff_only` 还是 `repair`。
2. 再确认项目根、集号、`分镜组ID` 或 source request 是否唯一。
3. 若从 `3-Detail` 开始，先检查 canonical `groups[]` 和组内 `detail.分镜列表`，必要时只把旧 helper 当 compat projection。
4. prompt 漂移时，先修 LLM 主创、固定前缀与多镜融写列，不先修 provider。
5. 参照图漂移时，先查字段位证据，再查路径存在性；路径存在只是最低门槛。
6. handoff 漂移时，先查 provider 是否唯一，再查引用运输层和 `output_dir`。
7. 旧三包引用不一致时，保留旧包作为兼容源，在本包 `references/legacy-upgrade-migration-matrix.md` 中补迁移去向。

## Reusable Heuristics

- `B.分镜故事板` 的价值不是把三个旧入口串成清单，而是把组级 storyboard 从输入到 handoff 的所有写位和返工入口收束到一个裁决点。
- 故事板链路最容易坏在对象边界：只要请求只锁一个 `分镜ID`，就应怀疑已经从“分镜故事板”滑向“分镜画面”。
- 组级 prompt 必须保留组内镜头顺序；多格图像的叙事连贯性比单帧细节密度更重要。
- 参照绑定阶段宁可少绑也不要猜图；一个歧义图进入 canonical 引用后，会污染 provider plan 与后续视频参照。
- 默认 provider 是内置 Image Gen handoff；外部 CLI/API 只有在用户或上游显式要求时再切换。
- `3-图像生成` 的成功只表示 handoff 包准备好，不能等同于图片文件已经生成或复制回项目。
- 原三包暂不移除时，新包应写清旧包的兼容角色，避免未来执行者误以为有两套互相竞争的业务真源。
