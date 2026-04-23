# CONTEXT.md

## Purpose & Loading Contract

- 本文件是 `aigc` 根技能的经验层知识库，不是过程日志。
- 调用 `.agents/skills/aigc/SKILL.md` 时，应自动预加载本文件。
- 详细 rollout 时间线与状态同步流水外置到 [`CHANGELOG.md`](./CHANGELOG.md)，本文件仅保留知识库与结论化里程碑。
- 优先级遵循：用户显式请求 > `AGENTS.md` / 元规则 > `SKILL.md` > `CONTEXT.md`。

## Context Health

- soft_limit_chars: 20000
- hard_limit_chars: 40000
- status: ok
- last_checked_at: 2026-04-14

## Type Map

| failure_or_outcome_type                                                                                                    | root_cause_layer       | immediate_fix                                                                                                                                 | systemic_prevention                                                                                                                                                                                       | verification_point                                                                                      |
| -------------------------------------------------------------------------------------------------------------------------- | ---------------------- | --------------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------- |
| 旧 harness 审计把 `aigc` 阶段细节绑定过深，导致重大改造一开始就被历史合同卡死                                            | harness / audit 控制层 | 将 `aigc` 控制面切到 `bootstrap_compat`，保留项目 runtime、治理 carriers 与卫星技能入口，放松深层阶段审计                                 | 对 suite 级重大改造优先保留骨架真源，并在 registry / routes / audit 中加入显式兼容模式开关，而不是整套清空 harness                                                                                        | `scripts/aigc_skill_audit.py --strict` 在兼容模式下通过，且允许阶段内部重构                           |
| 顾问团机制散落在多个阶段，无法共享消费                                                                                     | 真源治理层             | 将跨阶段规则上收至 `_shared/council-runtime/`，并把项目级团队真源固定为 `projects/aigc/<项目名>/team.yaml`                                     | 阶段根技能只保留角色适配，不再复制运行时合同                                                                                                                                                              | 进入 `2-Global / 3-Detail / 4-Design / 5-Image / 6-Video` 时都能先判断 `team.yaml`                |
| 创作输出未绑定到 `projects/aigc/<项目名>/`                                                                                    | 项目工作区合同层       | 在根技能中把 `projects/aigc/<项目名>/` 明确为 canonical landing                                                                                  | 把项目工作区写进根合同与阶段合同，不允许阶段各自发明落点                                                                                                                                                  | 项目输出与运行状态都能归到单个项目工作区                                                                |
| `2-Global` 已完成父子合同，但根技能状态表仍停留在旧口径                                                                  | 根技能状态同步层       | 同步更新 `.agents/skills/aigc/SKILL.md` 的阶段状态与调度说明                                                                                | 把阶段覆盖状态视为根入口投影，子阶段升级后必须回写                                                                                                                                                        | 根技能表格与 `2-Global` 实际状态一致                                                                  |
| 分组后节奏子技能迁到 `1-Planning`，但根技能仍把它写在 `2-Global`                                                       | 根技能状态同步层       | 同步更新根技能中 `1-Planning / 2-Global` 的阶段状态、调度策略与描述                                                                         | 把“阶段职责迁移”视为必须向上同步的元修复，而不是停留在局部技能文案                                                                                                                                      | 根技能能正确说明 `4-节奏` 归属与 `2-Global` 的消费关系                                              |
| `3-Detail` 父子合同已补齐，但根技能仍沿用旧阶段名或旧能力清单                                                           | 根技能状态同步层       | 用当前真实目录名 `3-Detail` 回写阶段状态与路由说明                                                                                         | 任何阶段改造完成后，都必须把根入口中的阶段名、能力清单与路径口径同步到当前目录真源                                                                                                                     | 根技能不再混用 `3-明细` 等旧名                                                                        |
| `4-Design` 父子合同已补齐，但 shared runtime 与根技能消费方仍沿用 `主体/` 旧目录，或遗漏已回迁 leaf                             | 根技能状态同步层       | 同步 `.agents/skills/aigc/SKILL.md` 与 `_shared/project-runtime-layout.md` 中的 design 阶段 runtime 口径，并把已回迁 leaf 回写根状态表      | 把“design 阶段 runtime / stage coverage 变更”视为必须向上同步到 query/review/council-runtime 的元修复                                                                                                   | 根技能与共享载体都指向 `projects/aigc/<项目名>/4-Design/`，且 stage row 不遗漏已落地 leaf                     |
| `2-设计/场景` 已迁回，但根技能 stage row 仍只列 `角色/道具` | 根技能状态同步层 | 同步根 `aigc/SKILL.md` 的 `4-Design` stage row 到 `场景/角色/道具` | 新增 active leaf 后必须向上检查根技能、阶段父级、tranche parent、registry 与 HARNESS 总览 | 根入口路由不会把场景设计误判为未迁回 |
| `1-Planning/2-Global/3-Detail` 的 episode 文件分工不清，导致阶段 seed root 与 detail root 混淆 | 真源治理层 | 在 shared runtime layout 中显式拆开 `2-Global/episode_root.json` 与 `3-Detail/第N集.json` 的 truth role | 让 `1-Planning` 只负责 handoff，`2-Global` 负责写组级 seed root，`3-Detail` 再围绕自己的 detail root 补齐 shot-level 明细，所有父级合同都回指 shared layout + stage-local template | 根技能、阶段技能与 shared carrier 对 seed root / detail root 的说法一致 |
| 根技能没有 `query / resume` 这类跨阶段旁路能力，导致事实查询与续跑被塞回阶段链或聊天口头说明              | 根 suite contract 层   | 在 `.agents/skills/aigc/` 根目录补 `query`、`resume` 两个卫星技能，并同步 registry / routes / audit                         | 对跨全阶段但不拥有阶段内容真源的能力，优先建根级卫星技能，不再把它们藏进 `references/` 或某个阶段私有流程                                                                                               | 根入口可直接路由到 `query / resume`，且 registry / audit 能识别                              |
| 已有 `query / resume`，但项目根没有结构化断点快照，导致二者仍只能围绕 `STATE.json` 自由文本猜恢复入口 | 根 runtime control 层  | 在 `0-Init` 新增 `governance-state.yaml` 并让卫星技能共读                                                                                 | 对跨阶段治理能力，优先补共享结构化状态真源，而不是新增 `CHANGELOGS.md`                                                                                                                                  | 查询、续跑都能从同一份 checkpoint 真源读取状态                                                    |
| `5-Image` 已在 registry 中作为 active stage 存在，但阶段父级真源缺失                                                   | 根阶段投影层           | 补建 `.agents/skills/aigc/5-Image/SKILL.md + CONTEXT.md`，再把根入口改回先进入阶段根                                                     | active stage 不再允许长期停留在“只有子入口、没有阶段父级”的状态；audit 与 routes 也要同步要求真实 stage parent                                                                                         | 根入口、registry、routes 与磁盘结构都先回链 `.agents/skills/aigc/5-Image/SKILL.md`                    |
| 根技能把 `7-Cut` 写成“目录存在”，但技能树中实际只有 runtime 槽位与 registry `shelved` 声明                              | 阶段生命周期层         | 在根 `SKILL.md` 把 `7-Cut` 改为“技能树目录不存在、仅保留 runtime 槽位”                                                                   | 对搁浅阶段同时核对 skill tree、registry 与 runtime layout，避免把 runtime 槽位误写成已建技能目录                                                                                                        | 根入口不会再把 `7-Cut` 当成可进入目录                                                                  |
| 根技能若把固定评测文档写成前置证据源，容易与真实运行样本和即时 validator 结果脱节                                         | 质量证据同步层         | 把根 `SKILL.md` 的 Quality Evidence Source 改成当前真实证据，优先回指样本项目、审计结果与阶段报告                                         | 对根级 evidence source 做“文件存在性 + live evidence relevance”双检查；默认只回链当前可复验的审计、validator 与样本运行结果                                                                             | 根入口的质评证据只引用当前存在且可复验的动态证据                                                       |
| 用户想“回到初始化态重来”，根路由却把它送进 `resume`                                                                      | 根路由判型层           | 将“主动重置式重新初始化”上收到根技能使用场景与硬规则，并回路由到 `0-Init`                                                               | 在根 `aigc`、`0-Init`、`resume` 三层同时固定“续跑 vs 回炉重起”边界                                                                                                                                        | 明确要求重起时，根入口只会推荐 `0-Init`                                                               |
| AIGC 项目 runtime 被平铺到 `projects/` 根层，导致技能合同、registry 与脚本发现口径不一致                                 | 项目命名空间治理层     | 统一回收到 `projects/aigc/<项目名>/` 并同步迁移 discovery / audit / registry / script carriers                                           | 把 `projects/aigc/` 写成根 `AGENTS.md`、根 `aigc/SKILL.md`、共享模板、registry、runbook 与脚本入口的单一命名空间真源                                                                                     | 路径发现、文档示例、审计规则与实际项目目录都指向同一层                                                 |
| `bootstrap_compat` 下的 strict audit 只审 stage parent，导致 active leaf 可能假绿 | 审计覆盖层 | 在兼容模式下把 review subtypes、5-Image / 6-Video active leaf 与 registry leaf 一并纳入严格审计 | 审计输出必须同时报告 discovered / checked / skipped 覆盖度，不再把“只审父层”包装成整树全绿 | `python3 scripts/aigc_skill_audit.py --strict` 能显式说明覆盖度，并在 leaf 漂移时报错 |
| `6-Video` shared runtime 真源仍残留 `2-视频生成` 旧口径 | canonical runtime mapping 层 | 同步修正 `_shared/project-runtime-layout.md`、`0-Init/SKILL.md` 与审计 marker 到 `2-参照引用 -> 3-视频生成` | 把 `6-Video` 技能树->runtime 映射纳入 bootstrap_compat 下的 targeted audit，而不是等全树 cutover 后再检查 | shared layout、init skeleton、6-Video parent 与审计脚本对当前链路说法一致 |

## Repair Playbook

1. 先比对四个真源面：根 `SKILL.md`、根 `CONTEXT.md`、`.codex/registry/skills.yaml`、`_shared/project-runtime-layout.md`。
2. 再核对根入口写到的每个阶段或证据源，在磁盘上是否真的存在对应合同或文件。
3. 若某个 active stage 只有逻辑阶段桶、没有阶段根合同，优先补建 stage parent；只有在明确过渡窗口且 registry/routes 已显式降级声明时，才允许根层直达真实入口。
4. 若某阶段是 `shelved`，同时核对 skill tree、registry 与 runtime 槽位，避免把“保留路径”误写成“已建合同”。
5. 只有当根层投影、shared runtime 与 registry 说法一致后，才继续向子阶段解释细节。

## Reusable Heuristics

- 多子技能组合包最容易犯的错，是目录树长得很漂亮，但缺一个总控面；没有根合同时，阶段越多，漂移越快。
- 当 `2-Global` 与 `3-Detail` 的粒度明显不同，最稳的做法不是硬共用同一份 root，而是拆成“`2-Global` 组级 seed root + `3-Detail` detail root”两层真源，并明确谁只负责组级前置、谁负责 shot-level 细化。
- 当阶段目录已经明确是 runtime 分区时，父技能最该写清的是“字段责任”和“patch 顺序”，而不是各自再定义一套集文件壳。
- 在 AIGC 影视创作场景里，先固定 `projects/aigc/<项目名>/` 这种项目工作区，比先讨论每一阶段写多少提示词更重要。
- 对当前仓库，`projects/` 只是总容器，AIGC 正式 runtime 必须再落到 `projects/aigc/<项目名>/`；如果把项目直接平铺在 `projects/` 根层，后续 query / resume / audit 很容易各自推断出不同项目根。
- `aigc` 根技能应更像 suite router，而不是内容生成器本身。
- 当某个阶段已经从“骨架”升级为真实可执行入口时，必须把这次变化同步回根技能；否则根路由会继续把可执行阶段误判为待补。
- 对 `aigc` 项目工作流，`projects/aigc/<项目名>/` 不是普通内容目录，而是三省六部控制面认可的 canonical runtime；只有把它同步写进 runbook / registry / audit，技能树才算真正接上 harness。
- 对正在重大重构的 suite skill，不要先清空 harness；更稳的做法是保留 runtime / registry / review gate，再给审计增加显式 `bootstrap_compat` 模式开关。
- `bootstrap_compat` 不等于“刑部看不见叶子”；更稳的做法是让审计器只跳过未纳入当前 active contract 的深层路径，而继续严格检查真实可执行 leaf。
- 对跨兄弟阶段共同消费的治理工件，真源应优先放项目根；对跨兄弟阶段共同执行的运行规则，真源应优先放 `_shared/`。
- 当技能阶段名本身带序号时，不要默认把这个序号投影到项目 runtime 目录；项目目录应优先服从 `_shared/project-runtime-layout.md` 的映射。
- 一旦 `_shared/project-runtime-layout.md` 已明确采用技能树真实目录名，`0-Init`、共享模板、governance-state、query/resume 和 backfill 脚本都必须直接复用同一组阶段名：`0-Init / 1-Planning / 2-Global / 3-Detail / 4-Design / 5-Image / 6-Video / 7-Cut`。
- 只要 shared runtime 仍是 canonical source，就不能容忍它在 active 链路上保留旧叶子名；否则 query / resume / init 会继续围着旧口径打转。
- `4-Design` 新 leaf 回迁不能只改 leaf 自身；根技能 stage row、阶段父级、tranche parent、registry 与 HARNESS 总览都需要同轮同步，避免路由层继续认为该 leaf 未开放。
- 若某项能力横跨所有阶段，但它只负责读取、恢复、复核或桥接，而不拥有阶段内容真源，最稳的落点是根级卫星技能，而不是再加一个伪 stage。
- 在 `aigc` 里，`query / resume` 的最稳分工分别是：尚书省+户部读真源、尚书省+兵部续跑；高风险预审与验收则直接回根 `aigc` 走治理 gate。
- 当根级卫星技能开始承担项目治理职责时，`STATE.json` 已经不够；最稳的补强不是 `CHANGELOGS.md`，而是单独的 `governance-state.yaml` 结构化快照。
- 对 AIGC 项目来说，“继续跑下去”和“回到初始化态重来”是两种不同任务：前者交给 `resume/`，后者必须回 `0-Init` 重判北极星与阶段入口。
- 若根入口声称某个文件是 evidence source，它必须真正在磁盘上存在；不存在时，应该先降级为“待补证据”，而不是继续把它写成第一真源。
- 对像 `5-Image` 这种 tranche-first 阶段，最稳的落点不是长期停留在逻辑桶，而是补一个真实 stage parent，再由父层收束子入口路由。
- 对像 `7-Cut` 这种当前冻结阶段，最稳的写法是“runtime 槽位保留 + registry shelved + skill tree 未落地”三件事同时成立，缺一都容易让总入口继续漂移。
