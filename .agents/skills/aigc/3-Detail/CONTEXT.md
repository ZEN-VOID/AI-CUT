# CONTEXT.md

## Purpose & Loading Contract

- 本文件是 `aigc/3-Detail` 的经验层知识库，不是过程日志。
- 调用 `.agents/skills/aigc/3-Detail/SKILL.md` 时，应自动预加载本文件。
- 优先级遵循：用户显式请求 > `AGENTS.md` / 元规则 > `.agents/skills/aigc/SKILL.md` > 本 `SKILL.md` > 本 `CONTEXT.md`。

## Context Health

- soft_limit_chars: 20000
- hard_limit_chars: 40000
- status: ok
- last_checked_at: 2026-04-14

## Type Map

| failure_or_outcome_type | root_cause_layer | immediate_fix | systemic_prevention | verification_point |
| --- | --- | --- | --- | --- |
| `3-Detail` 只有 `1-水月/2-镜花`，却没有父级阶段合同 | 阶段真源层 | 补父级 `SKILL.md + CONTEXT.md`，固定路由、shared root 写回和 validation | 把 `3-Detail` 视为 stage-local parent skill，而不是 sidecar 容器目录 | 根 `aigc`、阶段根与 shared layout 的说法一致 |
| child sidecar 写得很好，但 `第N集.json` 仍空或只有 seed | 父级聚合层 | 回到父 skill 做 sidecar -> shared JSON patch | 在父 `SKILL.md` 固化父层拥有 `分镜明细[]` 写回权 | `分镜明细[]` 不再停留为空数组 |
| shared root 缺失或只有 `bootstrapped` 空壳，却被静默继续下游 | seed 继承层 | 先报告 `2-Global` seed 缺口，再决定是否兼容 bootstrap | 在父 `SKILL.md` 固化 `seed check -> compat fallback` | 缺上游 seed 时不会被假装成 ready |
| 用户只要求局部 group 或单个 child skill，却被默认全量重跑 | 路由层 | 回到父层做 selective dispatch，只 patch 命中 scope | 在父 `SKILL.md` 固化 `selected_groups[] / selected_fields[] / selected_chains[]` 的路由语义 | validation 只登记本轮命中范围 |
| `组间设计` 在 detail 阶段被无故改写 | 继承边界层 | 恢复上游 seed，只允许回填 `出场角色及穿搭` 或显式返工项 | 在 `group_design_seed_contract.md` 与父层合同共同固化“默认继承不重写” | `全局风格 / 类型元素` 保持稳定继承 |
| `2-镜花` 很强，但 JSON 里角色走位、空间关系仍发虚 | 证据映射层 | 用 `1-水月` 补人物、动作、空间证据，再由 `2-镜花` 补镜头语法 | 在父层聚合规则固定“水月补事实，镜花补镜头组织” | `角色背景面 / 角色站位走位` 不再空泛 |
| `出场角色及穿搭` 长期留空 | 组级回填层 | 在 stage patch 时从 sidecar 与镜级事实回填，而不是等下游猜 | 在父 `SKILL.md` 把该字段列为 `3-Detail` 的最低负责槽位 | 进入 `4-Design` 前已有基础角色穿搭摘要 |
| `document_phase` 被直接写成 `ready`，但组内没有 shots | phase 管理层 | 回退到 `detail_in_progress`，先补 `分镜明细[]` | 在父 skill 的 phase gate 固定 `ready` 必须有 shot patch + validation | `ready` 与实际完成度一致 |
| 阶段产物存在，但没有 `validation-report.md` | 阶段闭环层 | 补写 `projects/<项目名>/3-Detail/validation-report.md` | 在父 `SKILL.md` Convergence Contract 固定 validation 必写 | 阶段完成时一定有验收结论 |
| `team.yaml` 已启用却绕过共享顾问团 gate | 共享运行时层 | 回到 `council-runtime` 做前置判断 | 在父层合同固定 council gate 是 `3-Detail` 的前置节点 | `validation-report.md` 中有 gate note |

## Repair Playbook

1. 先检查 `projects/<项目名>/3-Detail/第N集.json` 是否存在、是否符合 shared schema、`document_phase` 当前处于什么状态。
2. 若 root 不存在或 seed 不完整，先回溯 `2-Global -> group_design_seed_contract`，不要直接让 child sidecar 越权补根文件。
3. 再判断本轮是阶段级任务，还是单独的 `1-水月 / 2-镜花` 局部任务。
4. 若要写 JSON，优先复用已有 sidecar；只有证据不足时才重跑子技能。
5. 写 `分镜明细[]` 时，先用 `1-水月` 锁人物/动作/空间，再用 `2-镜花` 锁切镜/摄影/运镜/转场。
6. 最后用 `document_phase + validation-report.md` 一起表达完成度，不用单一文件存在与否代替验收。

## Reusable Heuristics

- `3-Detail` 父层的价值不是“再写一篇总稿”，而是让 shared JSON 与两个 sidecar 保持单线闭环。
- 当前最稳的阶段分工是：`1-水月` 负责 prose 级事实增密，`2-镜花` 负责镜头语法增密，父层负责结构化写回。
- `3-Detail` 一旦已经拿到 `2-Global` seed，就应优先继承而不是重抽；重抽通常意味着边界丢失。
- `组间设计` 在 `3-Detail` 的默认姿势是“继承 + 消费”，不是“重新定义”。
- `出场角色及穿搭` 最适合在 `3-Detail` 回填，因为这时镜级事实已经足够稳定，早填容易空泛，晚填会把负担转嫁给 `4-Design`。
- 若用户只要局部 group 或局部字段，就维持 `detail_in_progress`，不要为了追求看起来完整而假写 `ready`。
- `ready` 的真实含义不是 sidecar 都存在，而是 shared root 已可被下游稳定消费且 validation 已给出通过结论。
- 当 `1-水月` 与 `2-镜花` 出现冲突时，优先回看 `1-Planning/3-分组` 与 shared root 已继承的 seed，再决定是否返工子技能，而不是直接在 JSON 里折中臆写。
- 对 `3-Detail` 来说，最危险的退化模式是：child sidecar 越来越丰富，但父层 shared root 永远不收束；一旦出现这种迹象，应优先修父层聚合合同。
