# CONTEXT.md

## Purpose & Loading Contract

- 本文件是 `3-Detail/1-水月` 的经验层知识库，不是过程日志。
- 命中 `.agents/skills/aigc/3-Detail/1-水月/SKILL.md` 时，应自动预加载本文件。
- 优先级遵循：用户显式请求 > `AGENTS.md` / 元规则 > `aigc/3-Detail` 父合同 > 本 `SKILL.md` > 本 `CONTEXT.md`。

## Context Health

- soft_limit_chars: 16000
- hard_limit_chars: 32000
- status: ok
- last_checked_at: 2026-04-14

## Type Map

| failure_or_outcome_type | root_cause_layer | immediate_fix | systemic_prevention | verification_point |
| --- | --- | --- | --- | --- |
| 仍把 `水月` 当成 factual prose 聚合器 | 输出合同层 | 回到 owner bundle，只保留 `角色表现 / 运动表现 / 氛围表现 / 视觉强化` | 在 `SKILL.md + template + validator` 固定 `assembly_only` | 输出不再出现第二份 prose |
| `水月` branch 混入 `分镜构图 / 摄影美学 / 运镜手法 / 转场特效` | 字段 ownership 层 | 删除越权内容，回到本 branch owner 字段 | 用 validator 固定 branch target path | branch sidecar 无越权字段 |
| `视觉强化` 写成空泛审美句，无法给下游消费 | 可消费性层 | 改成具体可见抓手、视线重点、视觉识别收益 | 在 branch review 固定“可拍、可见、可抽取”标准 | 下游能稳定提取视觉锚点 |
| `运动表现` 只有情绪没有路径 | 调度颗粒度层 | 回到站位、位移、节奏因果 | 在 `运动表现` branch 固定运动表现字段 | root 中动作关系可直接复用 |
| `氛围表现` 悬空抒情，脱离剧本承载 | 场域承载层 | 回到具体空间、材质、空气和压迫来源 | 在 `氛围表现` branch 固定“场域先于形容词” | `氛围表现` 可回指上游场景 |
| `角色表现` 和 `运动表现` 相互抢写 | branch 边界层 | 把意图/视线留给 `角色表现`，把路线/位移留给 `运动表现` | 在 owner matrix 固定边界 | 两字段不再内容重叠 |
| 同一 branch 内多个槽位复用同一句，只做轻微改词 | 细分字段合同层 | 回到该 branch 的槽位问题定义，按“一槽一问”重写 | 在 branch `SKILL.md + validator + rubric` 同步增加跨槽去重门 | 同一字段内部不再出现同句跨槽复写 |
| compatibility projection 机械拼接 canonical，放大重复感 | projection assembly 层 | 对 projection 做摘要化、去重和截断，而不是原句拼串 | 在 owner bundle validator 增加 projection-vs-canonical 去重检查 | projection 不再像 canonical 的复制粘贴 |
| reverse-build 产物出现 `…` 半截短语，把具体画面句压成模板残片 | 压缩回灌层 | 回到 `1-Planning/3-分组` 的 `动作画面 / 对白画面` 顺序句，重写当前镜的具像表达 | 在 stage / bundle validator 固定“禁止省略号硬截断”并优先使用上游具体句回灌 | `角色表现 / 分镜构图 / projection` 不再出现 `…` |
| owner bundle 仍是旧 `detail-patch-sidecar/v1` | 模板/校验层 | 改成 `detail-branch-bundle-sidecar/v1` + `assembly_only` | 在 template + validator + runtime sample 同步切换 | `validate_watermoon_output.py` 直拦旧 bundle |
| compatibility projection 反向决定 canonical 内容 | 父子 handoff 层 | 先写 canonical，再保守派生旧字段 | 在父层 assembly 契约固定“projection 不得反盖 canonical” | root 八字段始终是第一真相 |
| child 包名、leaf 模块名与 shared root 落盘字段名不一致，导致 `水月` 每次都要做二次翻译 | canonical field governance 层 | 让 shared root canonical 字段直接收束成 `角色表现 / 运动表现 / 氛围表现 / 视觉强化`，对象槽位直接收束成 leaf 模块名 | 在 schema、父 skill、branch validator、模板与首要 consumer script 同步回收同名字段合同 | `水月` 不再“输出一套、落盘另一套” |

## Repair Playbook

1. 先确认 shared root 与当前 group scope 是否唯一，避免 branch 在错误上下文里并发。
2. 再核对四个 branch 是否都只命中自己的 canonical target path。
3. 若 `角色表现` 成立但动作虚，优先回补 `运动表现`，不要继续堆表演词。
4. 若空间发虚，优先补 `氛围表现` 的承载来源，不要只加形容词。
5. 若 bundle 生成失败，先查 branch process sidecar 是否缺失或仍是 `pending review`。
6. 若同一 branch 内多个槽位几乎同句，先回到槽位问题定义，而不是继续局部润色。
7. 写 owner bundle 时优先检查 `assembly_only`；一旦出现 prose 压缩句或 projection 原句拼串，就说明又回到旧路了。

## Reusable Heuristics

- `水月` 的核心不是“先写一份更漂亮的 factual prose”，而是把表演、动作、氛围、视觉强化拆成四个可独立评审的 canonical 槽位。
- `水月` 最稳的落点是四个 branch-owned object + 一个 `assembly_only` owner bundle，而不是 beat 级综合句。
- `角色表现` 回答“人为什么这么演”；`运动表现` 回答“人怎么动”；`氛围表现` 回答“空气和压迫从哪里来”；`视觉强化` 回答“镜头先看什么”。
- 比起 `角色表现 / 运动表现 / 视觉强化` 这类混合旧名，更稳的 root 命名是直接写成 `角色表现 / 运动表现 / 氛围表现 / 视觉强化`；这样 parent、child、validator、consumer 都围绕同一组词汇工作。
- `水月` 的细分字段只有在“一槽只回答一个问题”时才成立；如果两个槽位能互相替换，说明源层合同还不够硬。
- `出场角色及穿搭` 仍应优先服务识别而不是文采；越短、越准、越可回填越好。
- compatibility projection 只能帮助旧下游过渡，不能反过来规定 `水月` 的 canonical 输出长什么样。
- 一旦看到 `…`、半截短语或“先抓/再把”模板句，优先怀疑 reverse-build 或压缩层偷懒，不要继续在坏句上局部润色。
