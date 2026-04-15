# CONTEXT.md

## Purpose & Loading Contract

- 本文件是 `aigc/5-Image` 阶段父 skill 的经验层知识库，不是过程日志。
- 调用 `.agents/skills/aigc/5-Image/SKILL.md` 时，应自动预加载本文件。

## Context Health

- soft_limit_chars: 18000
- hard_limit_chars: 36000
- status: ok
- last_checked_at: 2026-04-14

## Type Map

| failure_or_outcome_type | root_cause_layer | immediate_fix | systemic_prevention | verification_point |
| --- | --- | --- | --- | --- |
| registry 已把 `5-Image` 注册成 active stage，但仓内没有阶段父级真源 | 阶段总合同层 | 补 `5-Image/SKILL.md + CONTEXT.md` | 把“active stage”定义为至少存在 stage parent，而不是只有子目录 | 根技能、registry 与磁盘结构一致 |
| `1-提示词蒸馏 / 2-参照引用 / 3-图像生成` 各自成立，但阶段级 discoverability 断层 | 阶段路由层 | 先补阶段父级路由，再保留子路径局部合同 | 让所有 active 图像子路径先回链 `5-Image/SKILL.md` | 模糊图像任务先命中阶段父级 |
| live 合同继续沿用旧 `5-画面` 路径或“`5-Image` 不存在阶段根”口径 | 真源同步层 | 把 live `SKILL.md / CONTEXT.md / routes / audit` 全部同步到 `5-Image` 新口径 | 把路径漂移视为阶段级问题，而不是 leaf 文案小瑕疵 | live 文档不再残留旧说法 |
| `1-提示词蒸馏` 只加载根 `aigc`，没把 `5-Image` 阶段父层纳入 preload | 上下文装配层 | 把 preload 顺序改成 `aigc -> 5-Image -> 具体子路径` | 阶段父层成为图像链路的统一 context bridge | 子路径能先获得阶段边界与路由约束 |
| routes 里没有图像阶段入口策略，外部编排只能靠根技能兜底 | 控制面路由层 | 在 `routes.yaml` 补 `aigc-image-stage-entry` | 把 active stage 的入口策略显式写进 route policies | 控制面可直接识别图像阶段入口 |
| 生成结果被写到 `Assets/` 或 provider cache，和 `submit-plan` 分离 | 输出治理层 | 把 canonical 输出图像回收到 `5-Image/3-图像生成/<provider>/<source_tranche>/<第N集>/` | 在阶段父层与 `3-图像生成` 局部合同共同声明“提交包与结果同目录” | 查询生成结果时能从 submit 包目录直接找到本地图像 |

## Repair Playbook

1. 先确认 `5-Image` 是否已有真实 stage parent。
2. 再确认根 `aigc/SKILL.md`、registry、routes 与磁盘结构是否同时指向该 stage parent。
3. 再检查三个子路径的 preload 与回溯链是否都先经过 `5-Image/SKILL.md`。
4. 再检查 live `CONTEXT.md` 是否还残留 `5-画面` 或“无阶段根合同”旧口径。
5. 最后才修具体子路径的局部合同。

## Reusable Heuristics

- 对 `5-Image` 这种多 tranche 图像阶段，最容易坏的不是某个 leaf，而是“阶段父层整层缺失”。
- 即使阶段内部是 tranche-first 结构，只要 registry 把它当 `active stage`，就应该落一个真实 stage parent，而不是长期靠根技能兜底。
- 图像阶段父层最稳的职责是路由、runtime 对齐和 handoff 边界，而不是再造 stage-level 总稿。
- 生成结果的 canonical 路径应跟着 `3-图像生成` 的 submit 包走；`Assets/` 可以留派生副本，但不能成为唯一业务真源。
- live 路径名、registry 路由和审计脚本必须一起升级；只改一个面，`5-Image` 很快又会退回逻辑桶状态。
