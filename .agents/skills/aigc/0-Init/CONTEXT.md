# CONTEXT.md

## Purpose & Loading Contract

- 本文件是 `aigc/0-Init` 的经验层知识库，不是进度日志。
- 调用 `.agents/skills/aigc/0-Init/SKILL.md` 时，应自动预加载本文件。
- 详细时间线与迁移流水外置到 [`CHANGELOG.md`](./CHANGELOG.md)，本文件仅保留知识库与里程碑结论。
- 优先级遵循：用户显式请求 > `AGENTS.md` / 元规则 > `SKILL.md` > `CONTEXT.md`。

## Context Health

- soft_limit_chars: 20000
- hard_limit_chars: 40000
- status: ok

## Type Map

| failure_or_outcome_type | root_cause_layer | immediate_fix | systemic_prevention | verification_point |
| --- | --- | --- | --- | --- |
| 初始化又长出旧三模式或平行问卷 | 模式合同层 | 把入口收口到 `智能顾问模式 -> 自动组队 / 自定义组队` 单一入口 | 模式锁定后只命中 1 个编组子路径，并由 planning interview 承接问题收束 | 全文只有一个合法模式展示位 |
| `north_star` 与 handoff 混成一个大杂烩 | 主文件分工层 | 将长期约束留在 `north_star.yaml`，阶段种子与 unknowns 放入 `init_handoff.yaml` | 用模板真源固定两份文件的字段边界 | 模板与最终落盘能看出清晰分工 |
| 顾问团只有共享名单，没有角色职责真源 | 团队治理层 | 生成项目根 `team.yaml`，把顾问写成 `策划 / 监制 / 评审` 三角色而非平铺列表 | 用 `.agents/skills/aigc/_shared/council-runtime/team.template.yaml` 固化角色、作用阶段与评审最终闸门 | 后续阶段能按角色读取顾问团队，而不是回猜 |
| 工件落盘漂向旧路径或外仓 | 路径合同层 | 固定到 `projects/aigc/<项目名>/0-Init/` 与项目根 | 在根 `aigc` 与 `0-Init` 双层合同中同时声明 canonical landing | 全部初始化工件都位于当前仓库项目路径 |
| 初始化目录骨架未跟随当前 active 子路径 | runtime skeleton 合同层 | 把初始化目录约定升级为“阶段根目录 + active child skeleton” | 让 `0-Init`、`_shared/project-runtime-layout.md` 与 `aigc_skill_audit.py` 共用同一套 bootstrap skeleton | 初始化合同、shared layout 与审计 marker 同步 |
| `project_state.yaml`、`route-plan.yaml` 与 `init_handoff/governance-state` 给出不同下一步 | 阶段入口同步层 | 先以 `project_state.yaml` 的 live route truth 为主，初始化当轮再要求 `init_handoff.project_contract.recommended_next_stage` 对齐 | 在 `Stage Entry Ownership Contract` 与治理回填脚本中固定 authority order | 读取项目当前入口时，只会从 `project_state/governance-state` 得到一个主入口 |
| 项目进入规划前没有故事主源登记 | 共享输入真源层 | 固定生成 `story-source-manifest.yaml`，区分 `primary_story_source` 与 `development_briefs` | 将故事源落点与缺失提示上收到 `_shared/story-source-contract.md` | 初始化完成后，能立刻判断 `1-分集` 是否具备增量进入条件与整季完成条件 |
| 续跑与状态查询无法稳定重建断点 | 项目治理快照层 | 在需要时生成 `governance-state.yaml` | 用 shared template 固定 `last_stable_checkpoint + resume_contract + artifact_status` | `query / resume / review` 能从同一份结构化快照读取断点与缺口 |
| 创作起盘被整套治理工件压得过重 | 初始化分层合同 | 把首次必出收敛到 `north_star / init_handoff / story-source-manifest / team / project_state` | 将 `governance-state + harness carriers` 改为惰性生成 | 首次初始化不再被非必要治理载体阻塞 |
| 路由、模式执行、充分性检查散落在外部规则真源 | 源层编排层 | 将这些能力完全吸收到父 `SKILL.md` 的内部能力合同与节点网络 | 审计脚本反向约束 `0-Init` 不得再引用 `.codex/agents/aigc/初始组/*.md` | `0-Init` 能仅凭自身 `SKILL.md` 解释完整执行链 |
| `north_star` 混入下一阶段建议或 `rebootstrap` 状态 | 字段真源分层层 | 把 live route truth 收回 `project_state.yaml / governance-state.yaml`，把初始化当轮 handoff 收回 `init_handoff.yaml` | 在模板与审计脚本同时禁止 `north_star` 出现 `stage_entry_contract / rebootstrap_status` | `north_star` 只剩长期约束，续跑状态只从 `project_state/governance-state` 读取 |
| 初始化预建目录看起来与当前技能树“不匹配” | 真源口径混层 | 明确区分“技能树执行层”与“项目 runtime 落盘层”两套命名 | 在 `_shared/project-runtime-layout.md` 建立 `Skill Tree To Runtime Mapping`，并在 `0-Init/SKILL.md` 同步注明 `5-Image / 6-Video` 的映射 | 读者不会再把 `1-提示词蒸馏/全能参照` 误读成必须预建 `projects/aigc/<项目名>/6-Video/1-提示词蒸馏/全能参照/` |
| 把“自动组队（推荐）”当成已锁定编组 | mode gate contract | 回到 `Initialization Mode Contract`，补发初始化元选项卡并等待用户确认 | 在 `SKILL.md` 明确“推荐项 != mode_lock_note”，并用审计脚本拦截歧义表述 | 仅有项目名或极简 brief 时，不再越权进入自动组队 |
| 自动组队把顾问选到 `.agents/skills/team/` 之外 | team scope contract | 立即裁掉越权成员，只保留 `team/` 树内 skill 并重写 `team.yaml` | 在 `team.yaml.init_contract.selector_scope_root` 固定 `.agents/skills/team/`，并在 `SKILL.md` 明确禁止外部候选 | `roles.*.members` 不再含 `.codex/agents/` 或仓外路径 |
| 自动组队把治理角色和部门覆盖混成一层 | team governance contract | 先回到 `策划 / 监制 / 评审` 权属矩阵，再单独补 `导演组 / 设计组 / 摄影组` 必选覆盖 | 在 `SKILL.md` 与 `team.template.yaml` 同步固定“两层裁决”：治理角色先锁、部门选人后落 | `team.yaml` 同时能读出角色权属与部门覆盖，不再互相替代 |
| 把 `策划 / 监制 / 评审` 误判为必须三拨不同的人 | role allocation contract | 允许同人复用，也允许分人治理，并把实际选择写回 `team_setup.role_allocation_mode / role_overlap_notes` | 在 `SKILL.md` 与 `team.template.yaml` 固定“默认允许重叠，不默认强制互斥” | 后续读取 `team.yaml` 时，能看出是同人兼任还是分人治理 |
| 题材明显缺少更合适的大师，但初始化直接硬凑现有 roster 且无记录 | roster gap contract | 保留当前可执行 lineup，同时额外生成 `todos/*-team-recommendation.md` | 在 `SKILL.md` 固定“继续执行 + 输出推荐 todo + 写回 `team_setup.recommendation_todo_paths`”三联动作 | 题材缺口不会无痕消失，且本轮初始化不被阻塞 |
| planning interview 没有先于北极星综合执行 | interview topology 层 | 回到 `N4-mode-engine`，先锁 `team.yaml` 再运行 `roles.planning.members` 的 subagents interview | 在 `Topology Contract` 与 `Execution Procedure` 固定 `team -> planning interview -> synthesis` 顺序 | `north_star / init_handoff` 可回溯到 planning interview provenance |
| planning interview 被降级成本地顺序扮演 | subagent gate 层 | 阻塞当前初始化并报告 subagents 不可用 | 在 `SKILL.md` 与 `team.template.yaml` 同时固定 `require_subagents_for_init_interview == true` | `0-Init` 不再把本地模拟表述成正常主路径 |
| 上层模式合同已切到新口径，但 Thought Pass / Pass Table 仍是旧节点语义 | thought-action sync 层 | 把 `Thinking-Action Node Contract`、`Topology Contract`、`Thought Pass Map`、`Pass Table` 一起同步改写 | 每次模式/编组/subagent 语义变更，都强制补齐 `decision_lock / dispatch_contract / blocker_rule / reentry_rule` | 不再出现“主合同是新口径，节点检查还停在旧口径” |
| 缺故事源时先生成了剧情级预设，后补故事源也不回刷 | source completeness / reconciliation 层 | 将缺故事源初始化降级为 `source-light bootstrap`，并在故事源后补时强制回刷 `north_star / init_handoff / project_state` | 在 `SKILL.md` 固化 `Story Source Completeness Gate + Story Source Reconciliation Contract`，审计脚本同步检查 | 不再出现“题眼推断版剧情”覆盖真实故事源的情况 |
| 用户要求“回到初始化态重来”，却被误判成 `resume` 或局部补档 | 入口判型层 | 在 `N0-intake` 先锁 `rebootstrap_requested`，把主动回炉重起直接路由到 `0-Init` | 在根 `aigc`、`0-Init` 与 `resume` 三层同时固化“续跑 vs 重置式重新初始化”分工 | 明确要求回炉时，不再继续沿旧方向续跑 |
| 重置初始化时直接清空了 `Story/` 或原始素材 | reset preservation 层 | 默认改为 `archive_reset`，只归档派生产物与旧治理工件 | 在 `Rebootstrap Contract` 固定“故事主源、原始素材默认保留” | 回炉后仍能读取原始故事源与不可再生素材 |
| 预建阶段骨架被治理脚本误判成“已进入执行” | 轻量治理快照层 | 在治理回填脚本中只把真实文件产物视为阶段输出，不把空目录当执行证据 | 将“骨架目录 != 阶段产物”同步写入经验层，并在治理回填逻辑中固定 `is_file()` 判定 | `governance-state` 预演时，刚初始化的项目不会被误判到执行期 |
| `0-Init` 目录仍保留旧 mode reference stub，阅读路径与真源边界变得含混 | 技能目录结构层 | 删除 `references/*-mode/module-spec.md`，把目录合同写回 `SKILL.md` 并补建 `CHANGELOG.md` | 对单技能初始化层固定 `SKILL.md + CONTEXT.md + CHANGELOG.md + agents/openai.yaml + templates/` 结构，禁止重建平行 mode 目录真源 | `find .agents/skills/aigc/0-Init -maxdepth 3` 不再出现 `references/`，且目录边界可直接从根文件读清 |
| `2-Global` canonical 输出改为根层四文件后，初始化仍预建旧目录化输出骨架 | runtime skeleton 合同层 | 将 `2-Global/全局风格 + 类型元素 + 设计元素` 子目录从 bootstrap skeleton 移除，只预建 `2-Global/` 阶段根 | 让 `0-Init/SKILL.md`、`_shared/project-runtime-layout.md` 与 `aigc_skill_audit.py` 同步约束同一 runtime 真源：四个 Markdown 由 `2-Global` 阶段执行后落盘 | 新初始化项目不会再被空目录推回旧输出结构 |
| 初始化没有同步预建项目级 `Assets/` 资产库，导致参考图和画板素材只能临时散落在各阶段目录 | project runtime asset layer | 将 `Assets/角色 / 道具 / 场景 / 服装 / 分镜画板/*` 加入默认 bootstrap skeleton | 在 shared runtime layout、`0-Init/SKILL.md` 与审计脚本固定“Assets 是辅助资产库，不是阶段真源” | 新项目初始化后立即具备统一资产沉淀目录，且不与 `5-Image` 业务输出混淆 |
| `4-Design` source leaf 缩到 active 三类后，初始化仍预建 `4-Design/服装/*` | runtime skeleton / active leaf drift | 将初始化预建目录收敛为 `场景 / 角色 / 道具` 三类 active leaf，保留 `Assets/服装/` 作为资产库 | 以 `_shared/project-runtime-layout.md` 为单一 runtime 真源，并让 `0-Init/SKILL.md` 与 `aigc_skill_audit.py` 同步检查同一份 active skeleton | 新项目不再把 pending `服装` sibling 误判为已具备 4-Design active runtime |
| `5-Image` 已升格为三段 active 链路后，初始化仍只预建三类请求目录 | runtime skeleton / active chain drift | 将 `5-Image/2-参照引用/` 与 `5-Image/3-图像生成/` 加入默认 bootstrap skeleton | 以 `_shared/project-runtime-layout.md` 为单一真源，并让 `0-Init/SKILL.md` 与 `aigc_skill_audit.py` 同步检查五个图像阶段根 | 新项目初始化后能承接请求蒸馏、参照绑定与 provider handoff，不再残留旧 `2-图像生成` 口径 |
| 分镜脚本故事源登记时按语义自造 `preset_registry.lock_level` 值 | story-source contract / 枚举边界层 | 将 `high / critical` 等自然语言强度值改为合法枚举 `hard_lock / soft_lock / reference_only` | 起草 storyboard_script manifest 时先回读 `_shared/story-source-contract.md` 的 Source-Type Extension Fields，禁止自造 lock level | manifest YAML 解析后，所有 `preset_registry[].lock_level` 均属于合法枚举 |

## Repair Playbook

1. 先确认问题属于模式锁定、问题设计、主文件分工、团队治理、思行节点断裂还是落盘漂移。
2. 优先回到 `0-Init/SKILL.md` 的 `Initialization Mode Contract`、`Internal Capability Fusion Contract`、`Topology Contract`、`North Star Contract` 与 `Sufficiency Gate`。
3. 若是字段边界问题，先修模板真源。
4. 若是路径问题，先回查根 `aigc/SKILL.md` 与本阶段 `Canonical Landing`。
5. 若是能力外置或执行链断裂，先修父 `SKILL.md` 的节点网络，再修局部文字。
6. 只有源层合同稳定后，才修本次具体输出。
7. 若问题发生在 `N1-mode-gate`，先区分“推荐”“默认展示项”“已锁定模式”三层状态；只有最后一层允许进入 `N2` 之后的节点。
8. 若问题发生在故事源后补场景，先区分“概念级约束”和“剧情级 seed”；凡属剧情级 seed，先回刷再允许下游继续。

## Reusable Heuristics

- 对当前 `aigc` 技能树来说，`0-Init` 最重要的不是“问得多”，而是“把 north star 与阶段入口种子分干净”。
- 影视初始化最容易过度下潜到设计或分镜细节；凡是会在下游阶段形成 canonical 的内容，都只应在这里保留 seed。
- 当前仓库的初始化落点必须优先服从 `projects/aigc/<项目名>/`，而不是借用其他项目系的 state/layout。
- 初始化阶段如果已经知道后续 runtime 分区，就应优先同时预落“阶段根目录 + active child skeleton”。
- 只要某工件会被多个兄弟阶段长期共同消费，就不该继续挂在 `0-Init/` 名下；最稳的做法是提升到项目根。
- 对长期维护的可执行技能目录，除 `SKILL.md + CONTEXT.md` 外，还应补齐 `agents/openai.yaml`。
- 当自动组队只收到一个极简概念时，优先先组出最小 planning 顾问团，把高分叉问题压进 `unknowns`，不要伪造完整剧情 seed。
- 只要用户没有明确要求“贴原作/保原顺序/保留原作节奏”，`original_adherence` 就应显式落盘为 `false`。
- 如果项目后续要做 `1-分集`，最稳的初始化习惯不是先问“要不要分几集”，而是先把“故事主源在哪、是否完整、能否正式切分”写进 `story-source-manifest.yaml`。
- `north_star` 一旦开始承载“下一步去哪”或 `rebootstrap` 过程痕迹，就说明长期约束真源和运行时状态真源混层了；这类信息应回到 `project_state / governance-state / init_handoff`。
- 项目离开 `0-Init` 之后，`init_handoff` 仍可保留初始化时的 handoff seed，但 live current-stage truth 只能看 `project_state` 与 `governance-state`。
- 对创作起盘来说，最小闭环应先保证 `north_star / init_handoff / story-source-manifest / team / project_state`；其余治理载体只有在复杂执行或卫星技能真正需要时再补。
- 对 `知行合一` 编排的 `0-Init`，最稳的写法不是再造第二份思考文档，而是把路由、三种模式和充分性审计直接写进同一份父 `SKILL.md`。
- 对单技能父层初始化目录，若旧 `references/*-mode` 已无仓内回链价值，应直接删掉 stub，而不是继续让它们冒充“还在生效的模式子层”。
- 阶段质评若要做动态检查，优先直接回读当前样本项目、模板边界与 audit/validator 结果，不必为了评估再维护一份固定评测任务 YAML。
- 对项目初始化骨架，阶段根和阶段产物要分开；`2-Global` 这类根层文件输出只预建阶段根，四个 Markdown 等阶段执行时生成，避免空子目录反向制造旧 canonical 结构。
- 对跨阶段都会复用的图像/素材沉淀，单独放进项目根 `Assets/` 比散落在各阶段目录更稳；但必须明确它只是资产库，不是业务真源。
- `Assets/分镜画板/分镜帧|分镜故事板|漫画` 可以和 `5-Image/*` 同名，但语义必须拆开：前者存参考资产，后者存阶段输出。
- `5-Image` 初始化骨架要跟随当前 active 链路：请求对象目录、`2-参照引用/` 与 `3-图像生成/` 都是稳定 runtime 根；只有 provider/mode/source/episode 的下钻目录等执行时再创建。
- 对 `4-Design` 这类“技能树 tranche 父层 != runtime 落盘层”的阶段，初始化应继续预建 domain-first 业务目录，而不是把 `1-清单/2-设计/3-面板` 直接投影成项目目录；但 domain-first 只覆盖当前 active leaf，pending sibling 只能保留在说明中，不应预建成 runtime。
- 当技能树有中间 tranche，但项目 runtime 只接受业务语义落盘名时，必须优先相信 `_shared/project-runtime-layout.md`，并在阶段合同里把两套命名的映射写明；否则读者会把“技能目录现状”误当成“项目预建目录”。
- 在 `0-Init` 里，`智能顾问模式` 是固定主模式，真正需要用户拍板的是 `自动组队 / 自定义组队`；只要用户没拍板且不存在强制路由信号，就必须停在 `N1-mode-gate`。
- `team.yaml` 现在不仅是阶段顾问运行时，也是初始化编组真源；最少要看 `init_contract.*`、`roles.planning.init_interview.*` 和 `runtime_policy.require_subagents_for_init_interview`。
- 对当前 `0-Init`，`策划 / 监制 / 评审` 是治理角色，不等于具体选人部门；自动组队应先锁治理权属，再补部门覆盖。
- `策划 / 监制 / 评审` 可以是同一波人，也可以是不同的人；是否重叠是编组策略问题，不是角色定义问题。
- 自动组队的最小可靠闭环是 `导演组 + 设计组 + 摄影组`；其他组只有在题材或执行难点真正需要时再加。
- 题材缺口如果暂时无法靠仓内 roster 补齐，最稳的处理不是阻塞初始化，而是保留当前 lineup 并额外写一份 `todos/*-team-recommendation.md`。
- 初始化 interview 的第一发问权属于 `roles.planning.members`；如果一开始就是主代理自己直接问，通常说明 team topology 被绕过了。
- 只要 `0-Init` 改了模式、编组或 subagent 合同，就必须同步改 `Thinking-Action Node Contract / Topology Contract / Thought Pass Map / Pass Table`；节点层不同步，后续执行就会偷偷回到旧语义。
- `0-Init` 可以在缺故事源时初始化项目，但只能生成题材级、边界级、生产级约束；凡是剧情级、单集级、人物关系级推断，都应降级为 provisional unknowns。
- 一旦真实故事源后补进入 `Story/`，优先动作不是继续下游阶段，而是先回刷 `north_star / init_handoff / project_state` 中的 assistant-inferred 剧情字段。
- 对已跑出下游产物的项目，默认最稳的回炉方式是 `archive_reset`：保留故事源和原始素材，归档旧阶段派生产物，再重写 `north_star / init_handoff / project_state`。
- “继续当前方向但补断点”属于 `resume/`；“推翻当前方向重新起盘”属于 `0-Init`，两者不能混判。
- 对轻量初始化项目，`1-Planning / 2-Global / ...` 这些预建目录只负责锁定 runtime，不代表阶段已经开跑；治理脚本若把目录本身当产出，恢复入口就会被错误前推。
- 当 `primary_story_source.source_type == storyboard_script` 且需要登记 `preset_registry` 时，`lock_level` 只能使用 `_shared/story-source-contract.md` 的三档枚举：`hard_lock`、`soft_lock`、`reference_only`；不要用 `high`、`critical` 这类语义强度词。

## Archive Index

- 详细迁移线索已外置到 [`CHANGELOG.md`](./CHANGELOG.md)。
- 已归档的 subagent-era 迁移材料只保留在历史变更说明中，不再作为现行执行真源。
