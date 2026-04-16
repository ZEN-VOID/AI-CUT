# CONTEXT.md

## Purpose & Loading Contract

- 本文件是 `aigc/4-Design` 阶段父 skill 的经验层知识库，不是过程日志。
- 调用 `.agents/skills/aigc/4-Design/SKILL.md` 时，应自动预加载本文件。

## Context Health

- soft_limit_chars: 18000
- hard_limit_chars: 36000
- status: ok
- last_checked_at: 2026-04-15

## Type Map

| failure_or_outcome_type | root_cause_layer | immediate_fix | systemic_prevention | verification_point |
| --- | --- | --- | --- | --- |
| 根技能声称 `4-Design` 已建合同，但仓内没有阶段父级 | 阶段总合同层 | 补 `4-Design/SKILL.md + CONTEXT.md` | 把“阶段已建”定义为至少存在 stage parent 真源，而不是只有 leaf 目录 | 根技能状态与仓内实体一致 |
| leaf preload 直接引用不存在的 stage/substage parent | 上下文装配层 | 先补真实存在的 stage parent / tranche parent，再重挂 preload | 叶子只回链真实存在的父级真源 | preload 不再断链 |
| tranche parent 缺失，导致 leaf 各自发明父链 | tranche 治理层 | 先补当前轮真正要用的父级；当前最低闭环已提升到 `1-清单/{场景,角色,道具} -> 2-设计/{场景,角色,道具} -> 3-面板/{场景,角色,道具}` | 把 tranche parent 视为 leaf 共享 context bridge，并在迁移窗口显式标记 partial-active / pending-migration | source-layer status 不再虚报 |
| 场景 leaf 已迁回，但父层仍只宣称 `角色/道具` active | coverage 同步层 | 同步 `4-Design` 与 `2-设计` 父层 coverage 到 `场景/角色/道具` | 每次新增 active leaf 后同步检查阶段父级、tranche parent 与 shared input contract | 父层状态与 leaf 实体一致 |
| `4-Design` 父层越权发明第二业务真源 | 输出治理层 | 收回到“只路由、不写业务主稿” | 在 stage parent 固化“业务真源只由 leaf 写回” | 不再出现 `4-Design` 总稿 |
| `3-面板/场景` 已重建但父级仍显示 pending | 状态同步层 | 把 `3-面板` 更新为 `partial-active`，并明确 `场景 / 角色 / 道具` leaf active | 父级 Stage Coverage 必须随真实 source-layer 落点同步 | 父级路由可进入 `3-面板/{场景,角色,道具}` |
| 面板阶段默认未生图或直调误带参考图 | SMART 桥接层 | 引入 `3-面板/_shared` SMART 合同：批量连续执行扫 `2-设计` 图，单文件/自然语言默认 T2I | 把 SMART 判型放到 tranche shared contract，不在 leaf 复制 | request sidecar 记录 `smart_mode_resolved` |
| `3-面板/道具` 已重建但父级 coverage 仍只列场景 | coverage 同步层 | 同步 `4-Design` 父层、registry 与 HARNESS，把 `3-面板/{场景,道具}` 标为 partial-active | 新增 panel leaf 时同轮更新父层 active leaf 列表与路由策略 | 父级路由可进入 `3-面板/道具` |
| `3-面板/角色` 已重建但父级仍只列场景/道具 | coverage 同步层 | 同步 `4-Design` 父层、registry 与 nano-banana 回链，把 `3-面板/{场景,角色,道具}` 标为 partial-active | 新增 panel leaf 时同轮更新父层 active leaf 列表、SMART handoff 与入口元数据 | 父级路由可进入 `3-面板/角色` |
| pending `服装` leaf 被写成 active runtime 输出路径 | active leaf / runtime 投影层 | 将 `服装` 标成 `pending-migration`，不再声明 `4-Design/服装/*` active 输出根 | 初始化 skeleton 只从 `_shared/project-runtime-layout.md` 继承 active 三类 `场景/角色/道具`，pending sibling 不预建目录 | 新项目 `4-Design/` 下不再出现空的 `服装` runtime |
| `2-设计` 已新增单主体自动图，但阶段父层仍只把图片交给 `3-面板` 或 `5-Image` | 输出快路径同步层 | 在 `4-Design/SKILL.md` 回指 `2-设计/_shared/design-output-contract.md` | 把 `full_generation_prompt + same-stem auto image` 写进阶段拓扑、路由和 completion | 批量 panel 可直接扫描 `2-设计` 同 stem 图片 |
| 项目根 `team.yaml` 已启用顾问团，但 `4-Design` 父层没有在当前轮 leaf canonical 落盘后触发监制强化 | 阶段末端共享运行时层 | 在 `4-Design/SKILL.md` 追加 `S6/S7` 与 `Subagents 监制强化` 合同，围绕当前轮命中的 leaf canonical + stage report 做 refine | 将 `master-check-team` 的 reviewer 解析、mode 裁决与 subagents gate 收束进父层合同；并在 `validation-report.md` 固定 supervision 槽位 | `4-Design` 阶段收尾能回读 reviewer、mode、used_subagents 与 patched_targets |
| `4-Design` 把 stage-end refine、final-stage review gate 与 `source_skill_refs` 混成一条 reviewer 权限线 | council runtime layering | 把 `roles.supervision.members` 视为 stage-end refine 显式 reviewer；若 `roles.review.operates_on_final_stage_of` 显式覆盖 `4-Design`，再并入 `roles.review.members`；`source_skill_refs` 降为领域提示 | 在 `4-Design/SKILL.md`、`2-设计/_shared/subagent-supervision-contract.md` 与相关 leaf 中固定“分层裁定 + reviewer precedence + 不把 source refs 当授权” | closeout 结论能说明 refine / gate 分层，且 reviewer roster 不再漂移 |
| `4-Design` 的监制会审把 `_manifest.json`、派生 PNG 或 request sidecar 当成主评审对象，导致 reviewer 越过业务真源 | review target bundle 层 | 将 review 主目标固定为当前轮命中的 leaf canonical truth，manifest / image / request 只作为证据目标 | 在 `4-Design/SKILL.md` 固定 `Review Target Bundle` 与 `Optimization Boundary`，防止派生资产反向抢权 | 监制强化结论直接指向 leaf canonical，而不是派生文件 |
| `runtime_policy.use_subagents_by_default == true` 且 reviewer 已稳定命中时，`4-Design` 仍静默退回本地模拟 | dispatch gate 层 | 把 `Subagent Dispatch Gate` 明确写进 `4-Design` 父层，而不是只依赖 shared runtime 常识 | 在父层 `FIELD-4D-06` 与 completion 中固定 `used_subagents / fallback_reason` 记录位 | 阶段 summary 能明确说明是否真实启用了 subagents |

## Repair Playbook

1. 先确认 `4-Design` 是否存在真实 stage parent。
2. 再确认当前轮真正命中的 tranche parent 是否存在。
3. 若未全部迁回，不要假设全阶段 active；先把状态写清，再修命中的 leaf。
4. 最后才修具体 leaf 的业务合同。
5. 面板相关问题先查 `3-面板` 父合同和 `_shared` SMART 桥，再查具体 leaf。
6. 若项目根 `team.yaml` 启用顾问团，当前轮 leaf canonical 首次落盘后必须先按“stage-end refine / final-stage gate 分层”判定 reviewer roster 与 mode，再决定真实 subagents、fallback 还是 skip。
7. 监制强化只改当前轮命中的 canonical 文本/JSON 与阶段 `validation-report.md`；若 findings 命中 leaf 业务结构，回流对应 tranche/leaf，不在父层偷改派生资产。
8. 若 `team.yaml.enabled == false` 但用户显式要求执行本轮监制强化，按 `manual override` 进入 shared contract，并在 `validation-report.md` 标记人工触发而非常驻运行时。

## Reusable Heuristics

- 对 `4-Design` 这种多 tranche、多类目的阶段来说，最容易坏的不是某个 leaf，而是“中间父级整层缺失”，然后文档仍假装全量 active。
- 一旦某个 tranche parent 与 leaf 已回迁，就要同步回收父总线的 `pending-migration` 口径；否则 source-layer 会自相矛盾。
- 场景链迁回时要同时看 `1-清单` 三真源与 `2-设计` 场景 leaf；只补 leaf 不改父层 coverage，会让后续路由继续误判为 reserved。
- 当多个 leaf 都想加载同一个不存在的父级时，根因通常不在 leaf，而在 stage parent / tranche parent 没有真正落地。
- `4-Design` 父级最稳的职责是路由、边界和 runtime 对齐，而不是跨类目再造第二真源。
- `3-面板` 的业务真源应停在 layout JSON；自动生图应作为派生动作由 SMART bridge 管理，避免 request/PNG 反向抢真源。
- `2-设计` 的单主体自动图是面板连续性的上游参照，不替代 `3-面板` 的 layout JSON；两类图片要通过路径和 manifest 明确分层。
- 新增 panel leaf 时，不只补 leaf 文件；必须同步父层 coverage、registry leaf_index 与 HARNESS 总览，否则入口层仍会按 pending 处理。
- 角色面板重建时要优先兼容当前 `2-设计/角色` 的 `character_design.json + 逐角色 Markdown + 同 stem 单主体图` 组合；Markdown 只作人读投影，不能反向替代 machine-first 真源。
- `服装` 可继续作为类目宇宙和 `Assets/服装/` 资产库存在；但只要 source leaf 没迁回 active，阶段合同和初始化 skeleton 都不能给出 `4-Design/服装/*` active 落盘路径。
- `4-Design` 的监制强化默认主目标始终是当前轮命中的 leaf canonical truth；`validation-report.md` 只作阶段级次目标，派生 PNG、request sidecar 与 `_manifest.json` 只作证据。
- 对 `4-Design` 来说，最稳的阶段末监制口径不是“全阶段写完才总评”，而是“本轮命中的 leaf canonical 首次落盘后，立刻按 `team.yaml` 做一次受限 stage-end refine”。
- 只要 `runtime_policy.use_subagents_by_default == true` 且 reviewer 已稳定命中，`4-Design` 就不应把本地顺序模拟表述成正常主路径；降级必须显式记录。
- `4-Design` 当前轮 closeout 里，`roles.supervision.members` 是 stage-end refine 的显式 reviewer 池；若项目把 `roles.review` 显式挂到 `4-Design` final-stage gate，可并入 reviewer roster，但不替代 refine 入口。
- `source_skill_refs` 只适合做 reviewer 映射提示，不适合做 `4-Design` 监制强化的授权字段；一旦把它升格，reviewer roster 就会随 provenance 漂移。
