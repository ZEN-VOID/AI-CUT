# CONTEXT.md

## Purpose & Loading Contract

- 本文件是 `3-Detail/2-镜花` 的经验层知识库，不是过程日志。
- 命中 `.agents/skills/aigc/3-Detail/2-镜花/SKILL.md` 时，应自动预加载本文件。
- 优先级遵循：用户显式请求 > `AGENTS.md` / 元规则 > `aigc/3-Detail` 父合同 > 本 `SKILL.md` > 本 `CONTEXT.md`。

## Context Health

- soft_limit_chars: 18000
- hard_limit_chars: 36000
- status: ok
- last_checked_at: 2026-04-14

## Type Map

| failure_or_outcome_type | root_cause_layer | immediate_fix | systemic_prevention | verification_point |
| --- | --- | --- | --- | --- |
| 仍把 `镜花` 当成统一导演 prose 聚合器 | 输出合同层 | 回到四个 branch-owned cinematic 字段 | 在 `SKILL.md + template + validator` 固定 `assembly_only` bundle | 输出不再出现统一导演长句 |
| `镜花` branch 混入 `角色表现 / 运动表现 / 氛围表现 / 视觉强化` | 字段 ownership 层 | 删除越权字段，回到 cinematic owner | 用 validator 固定 target path | sidecar 无越权字段 |
| `分镜构图` 未先稳定，后三支就开始串并混跑 | 顺序门层 | 回到 `分镜构图 -> 摄影美学 -> 运镜手法 -> 转场特效` 的当前序号串行 | 在 `SKILL.md + module-index.md` 固定先行门与串行序号 | 后三支不再反向改骨架 |
| `分镜构图` 只有镜头名词，没有观看关系 | 构图骨架层 | 回到“谁在看谁、谁压谁、画面重心在哪里” | 在构图 branch 固定观看关系字段 | `分镜构图` 可指导后续三支 |
| `摄影美学` 堆审美词，缺少控制线 | 摄影汇流层 | 先锁 `visual_control_line` 再写光影/色彩/质感 | 在摄影 branch 固定控制线为前置 | `摄影美学` 能稳定指导 provider prompt |
| `运镜手法` 很花但没有收益 | 运镜层 | 回到变化、组合、速度的叙事动机 | 在运镜 branch 固定“无收益不动镜” | 运镜结论可解释 |
| `转场特效` 抢戏，导致镜间逻辑失真 | 转场层 | 先删无收益特效，再回看衔接问题类型 | 在转场 branch 固定默认克制原则 | 转场只做必要连续性 |
| owner bundle 仍沿用 `shot_patches[]` 作为 canonical | 模板/校验层 | 改成 `detail-branch-bundle-sidecar/v1` + `assembly_only` | 在 template + validator + runtime sample 同步切换 | `validate_jinghua_output.py` 直拦旧 bundle |
| compatibility projection 反向定义 `构图/摄影/运镜/转场` | 父子 handoff 层 | 先写四个 cinematic canonical，再保守派生旧字段 | 在父层 assembly 契约固定 projection 不反盖 canonical | root 四个 cinematic 字段始终是第一真相 |

## Repair Playbook

1. 先确认 shared root 中 `剧本正文 + 分镜切换` 是否稳定存在。
2. 再确认 `水月` 前置是否稳定，避免 `镜花` 代替上游补事实。
3. 若 `分镜构图` 不稳，立即回退到 `分镜构图`，不要直接补后三支。
4. 若摄影信息发虚，先补控制线，不要直接堆色彩形容词。
5. 若运镜抢戏，先删动作花样，再判断镜头是否本应静止。
6. 若转场喧宾夺主，先回退到直切优先。
7. 写 owner bundle 时优先检查 `assembly_only`；一旦出现统一导演 prose，就说明又回到旧路了。

## Reusable Heuristics

- `镜花` 的关键不是“写得更花”，而是让构图、摄影、运镜、转场四个结论可以独立评审、独立回写。
- `镜花` 最稳的顺序永远是 `分镜构图 -> 摄影/运镜/转场`，不是四支一起抢写。
- `分镜构图` 决定“镜头怎么站住”，`摄影美学` 决定“光和质感怎么压”，`运镜手法` 决定“镜头要不要动、怎么动”，`转场特效` 决定“镜间怎么接而不抢戏”。
- 旧的 `shot_patches[]` 现在只是 compatibility projection，不再是 `镜花` 的 canonical 真相。
- `镜花` 最稳的定位不是并发抢跑，而是在 `分镜切换 + 水月前置 + 分镜构图` 稳定后再展开后三支。
