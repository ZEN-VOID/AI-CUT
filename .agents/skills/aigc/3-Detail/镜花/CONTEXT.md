# CONTEXT.md

## Purpose & Loading Contract

- 本文件是 `3-Detail/镜花` 的经验层知识库，不是过程日志。
- 命中 `.agents/skills/aigc/3-Detail/镜花/SKILL.md` 时，应自动预加载本文件。
- 优先级遵循：用户显式请求 > `AGENTS.md` / 元规则 > `aigc/3-Detail` 父合同 > 本 `SKILL.md` > 本 `CONTEXT.md`。

## Context Health

- soft_limit_chars: 18000
- hard_limit_chars: 36000
- status: ok
- last_checked_at: 2026-04-14

## Type Map

| failure_or_outcome_type | root_cause_layer | immediate_fix | systemic_prevention | verification_point |
| --- | --- | --- | --- | --- |
| 仍把镜花写成 `[分镜N ...]` prose 融写稿 | 输出合同层 | 回到 `shot_patches[]`，只保留 cinematic fields | 在 `SKILL.md + template + validator` 固定 patch sidecar 模式 | 输出不再出现 prose 成稿 |
| `镜花` sidecar 混入 `出场角色及穿搭` 或 factual 字段 | 字段 ownership 层 | 删除越权字段，回到 cinematic patch | 用 validator 固定 `镜花` 只拥有 cinematic 字段 | sidecar 无越权字段 |
| 有镜头感，但没有 `分镜ID / 时间段 / beat_refs[]` | shot skeleton 层 | 回到 `分镜构图` 先补 skeleton | 在 `FIELD-JH-04` 固定 shot spine 为先决门 | 父层能直接 merge |
| 把 `镜花` 误当成可在 `水月` 之前独立落镜 | 父子 handoff 层 | 回到 `分镜切换 -> 水月 -> 镜花` 的顺序门 | 在 `SKILL.md + module-index.md` 固定“先定镜数，再水月，再镜花实际落镜” | `镜花` 不再绕过 factual 前置 |
| shared root 缺 `分镜切换` 就直接开始切镜 | 上游 seed 层 | 先回报 seed 缺口，再停在切镜前 | 在 `SKILL.md + module-index.md` 固定 `分镜切换` 为前置 gate | `1-切换` 不再代替 `2-Global` 决定镜数 |
| 仍把 former `1-切换` 当作 `镜花` 独立叶子 | 源层拓扑层 | 从 `镜花` references 中移除独立叶子，改由 `2-Global` 内化固定镜数裁决逻辑 | 在 `2-Global` 与 `镜花` 双侧合同同步声明 “fixed shot count upstream, shot spine local” | `镜花` 不再维护第二份切换真源 |
| 把 `镜花可并发` 误解为可以跳过 `分镜构图` 直接写摄影/运镜/转场 | 阶段顺序层 | 回到 `分镜构图 -> (摄影/运镜/转场并行)` | 在 `SKILL.md + module-index.md` 固定“先成 shot spine，再放并行分支” | 后续模块不再反向改镜数 |
| `beat_refs[]` 漂移，导致无法和 `水月` 对齐 | patch 对齐层 | 回到组锚点与 beat hints，重建引用 | 在 `SKILL.md` 固定 `beat_refs[]` 为强要求 | 父层不再靠临场猜测 |
| 摄影信息堆形容词，但无法落字段 | 摄影汇流层 | 先补 `visual_control_line`，再压摄影 patch | 在 `S5` 固定“先收束后分发” | `摄影美学` 可直接落 JSON |
| 运镜很花，但没有叙事动机 | 运镜层 | 回到 `变化 / 组合 / 速度`，先锁动机，再写形式 | 在 `FIELD-JH-06` 固定“无收益不动镜” | `运镜手法` 有明确理由 |
| 转场和特效喧宾夺主 | 转场层 | 删掉没有叙事收益的项 | 在 `FIELD-JH-07` 固定默认克制原则 | sidecar 仍以 shot 组织为主 |
| 为了镜头语言反向发明剧情事实 | 事实边界层 | 回到固定 `剧本正文` 与上游 beat hints | 在 `Watermoon Relationship Contract` 固定 shared root 为第一事实层 | 镜头语言不越权 |

## Repair Playbook

1. 先确认 shared root 中 `剧本正文 + 分镜切换` 是否稳定存在，避免在错误真源上切镜。
2. 再确认 `水月` sidecar 是否已提供可用 factual evidence，避免 `镜花` 代替上游补事实。
3. 若还没有按既定镜数切出的镜窗与时间段，先回退到 `分镜构图`，不要直接补摄影词。
4. 若没有 `分镜ID / 时间段 / beat_refs[]`，再回退到 `分镜构图` 重建 shot spine，不要直接补摄影词。
5. 若摄影信息发虚，优先补 `visual_control_line`，不要直接堆色彩形容词。
6. 若转场抢戏，先回退 `转场特效`，不要继续叠效果。
7. 写 sidecar 时优先检查 ownership：只要出现 factual 或 group 字段，就说明越权了。

## Reusable Heuristics

- `镜花` 的关键不再是“写得更花”，而是“把镜头语言压成可 merge 的 cinematic patch”。
- `镜花` 最稳的顺序不是直接写摄影词，而是先锁 `shot skeleton -> 摄影 -> 运镜 -> 转场`。
- 对同一个 group，更细的第一门槛是先承接 shared root 的固定 `分镜切换`，再在 `分镜构图` 中把这几个镜窗、slot 和画面骨架一体锁清，最后才让并行分支消费它；否则后面越写越像补救。
- `beat_refs[]` 是镜花 sidecar 最关键的合并桥，不稳定的镜头设计对父层几乎不可用。
- `镜花` 最稳的定位不是并发抢跑，而是在既定 `分镜切换 + 水月 evidence` 稳定后再做实际落镜。
- `镜花` 的默认并行不等于“三条支线互相卡顺序”，而是都只能围绕同一条 stable shot spine 做增量 patch。
- `景别 / 镜头属性 / 镜头框架 / 镜头类型 / 镜头视角` 一起成组思考，会比单独补一个“景别”更稳定。
- `摄影美学` 真正有用时，通常能同时说明光感、空间剥离和观看压力，而不是只给审美词。
