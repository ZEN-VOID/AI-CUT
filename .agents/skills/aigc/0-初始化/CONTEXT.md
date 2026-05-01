# CONTEXT.md

## Purpose & Loading Contract

- 本文件是 `aigc/0-初始化` 的经验层知识库，不是进度日志。
- 调用 `.agents/skills/aigc/0-初始化/SKILL.md` 时，应自动预加载本文件。
- 详细时间线与迁移流水外置到 [`CHANGELOG.md`](./CHANGELOG.md)，本文件仅保留知识库与里程碑结论。
- 优先级遵循：用户显式请求 > `AGENTS.md` / 元规则 > `SKILL.md` > `CONTEXT.md`。

## Context Health

- soft_limit_chars: 20000
- hard_limit_chars: 40000
- status: ok

## Type Map

| failure_or_outcome_type | root_cause_layer | immediate_fix | systemic_prevention | verification_point |
| --- | --- | --- | --- | --- |
| “初始化小说”误入 AIGC 影片初始化，或“初始化影片/电影”被 story 初始化截走 | 媒介语义路由层 | 在 `aigc-init` 入口、registry routes 与 product metadata 中显式写入 film/movie/video 正向触发和 novel/book 负向排除 | 把自然语义触发词分成两组：`影片/电影/影视/视频 -> .agents/skills/aigc/0-初始化`，`小说/网文/书/长篇故事 -> .agents/skills/story/0-初始化` | 输入“初始化电影/影片”只落 `projects/aigc/<项目名>/`；输入“初始化小说/网文”只落 `projects/story/<项目名>/` |
| 初始化又长出旧三模式或平行问卷 | 模式合同层 | 把入口收口到 `智能顾问模式 -> 自动组队 / 自定义组队` 单一入口 | 模式锁定后只命中 1 个编组子路径，并由 planning 固定题包直答承接问题收束 | 全文只有一个合法模式展示位 |
| `north_star` 与 handoff 混成一个大杂烩 | 主文件分工层 | 将长期约束与全局设计块留在 `north_star.yaml`，阶段种子与 unknowns 放入 `init_handoff.yaml` | 用模板真源固定两份文件的字段边界，`全局风格 / 细分风格 / 类型元素 / 世界观` 原样归入 north star | 模板与最终落盘能看出清晰分工 |
| `全局风格` 混入镜头语言、角色材质、服装细节或道具细节，导致角色/场景/道具互相污染 | north-star 风格字段边界层 | 将 `全局风格` 收敛为通用安全前缀：`媒介属性 / 时代属性 / 光影逻辑 / 画面质感 / 避免出现 / 全局风格提示词`；把画面、服装、建筑、物品分流到 `细分风格` | 在 north-star 模板、artifact 规则、review gate 与 audit 脚本同步检查 `全局风格 / 细分风格` 字段 | 初始化生成的全局前缀能被所有设计类型复用，不会把单一设计类型口径污染到其他类型 |
| `画面风格` 写成场景别策略清单，例如姜家/陆家/巴黎/马场分别怎样拍 | north-star 细分风格边界层 | 将 `画面风格` 收敛为跨场景共同画面基调；场景别影像策略移入 `init_handoff`、摄影 seed、场景设计或后续阶段 | 初始化综合视觉建议时先区分“统一画面基调”与“场景别策略”，不得把后者塞入 `细分风格.画面风格` | `画面风格` 不含具体场景名或场景专属光色策略，仍能作为全片统一风格前缀 |
| `全局风格提示词` 没有显式包含 `媒介属性`，导致后续图像/视频提示词丢失媒介真源 | north-star prompt projection 层 | 将 `全局风格提示词` 改为显式包含 `全局风格.媒介属性` 的前缀，例如“真人感 AIGC 影视/短剧视觉，...” | 在 north-star 模板、artifact 合同、review gate 与项目记忆中同步要求 `全局风格提示词` 包含当前 `媒介属性` 字段值 | YAML 中 `全局风格提示词` 字符串包含 `媒介属性` 完整值，且仍在 200 字以内 |
| north-star 风格字段生成过长或混入英文默认口径 | 输出约束层 | 设定默认中文与字数上限：`全局风格提示词 <= 200 字`、`类型元素提示词 <= 30 字`、`画面风格 <= 70 字`、`服装风格 / 建筑风格 / 物品风格 <= 100 字` | 在模板注释、artifacts 规则、review gate 和 audit marker 同步声明 | 初始化产物可直接作为后续设计提示词前缀，不需要再压缩裁剪 |
| 顾问团只有共享名单，没有角色职责真源 | 团队治理层 | 生成项目根 `team.yaml`，把顾问写成 `策划 / 监制 / 评审` 三角色而非平铺列表 | 用 `.agents/skills/aigc/_shared/council-runtime/team.template.yaml` 固化角色、作用阶段与评审最终闸门 | 后续阶段能按角色读取顾问团队，而不是回猜 |
| 工件落盘漂向旧路径或外仓 | 路径合同层 | 固定到 `projects/aigc/<项目名>/0-初始化/` 与项目根 | 在根 `aigc` 与 `0-初始化` 双层合同中同时声明 canonical landing | 全部初始化工件都位于当前仓库项目路径 |
| 初始化目录骨架仍沿用旧英文、旧编号或最小骨架 | runtime skeleton 合同层 | 把初始化目录约定改为用户指定的扁平中文项目 runtime：以 `projects/aigc/<项目名>` 当前目录结构为准，`0-初始化/`、`1-分集/`、`2-编导/`、`3-摄影/`、`4-分组/`、`5-设计/`、`6-图像/`、`7-视频/`、`源/`、`CONTEXT/` 与根载体 | 让 `0-初始化`、scope/runtime 合同、模板与 `aigc_skill_audit.py` 共用同一套中文 skeleton | 初始化合同、模板、registry 与审计 marker 同步 |
| 初始化项目根漏建 `CHANGELOG.md`，导致后续项目级时间序记录没有统一入口 | project-root trace carrier 层 | 在 `N2-runtime-bootstrap` 同步创建项目根 `CHANGELOG.md` | 将 `CHANGELOG.md` 上收到 `_shared/project-runtime-layout.md`，并让 `0-初始化/SKILL.md` 与 `aigc_skill_audit.py` 同步检查 | 新项目初始化后项目根默认具备时间序记录入口，但 query/resume 仍不会把它误当治理真源 |
| `STATE.json`、`route-plan.yaml` 与 `init_handoff/governance-state` 给出不同下一步 | 阶段入口同步层 | 先以 `STATE.json` 的 live route truth 为主，初始化当轮再要求 `init_handoff.project_contract.recommended_next_stage` 对齐 | 在 `Stage Entry Ownership Contract` 与治理回填脚本中固定 authority order | 读取项目当前入口时，只会从 `project_state/governance-state` 得到一个主入口 |
| 项目进入规划前没有故事主源登记 | 共享输入真源层 | 固定生成 `story-source-manifest.yaml`，区分 `primary_story_source` 与 `development_briefs` | 将故事源落点与缺失提示上收到 `_shared/story-source-contract.md` | 初始化完成后，能立刻判断 `1-分集` 是否具备增量进入条件与整季完成条件 |
| 初始化合同声明 shared 模板，但声明路径下没有对应文件 | 模板真源落盘层 | 补齐 `.agents/skills/aigc/_shared/council-runtime/team.template.yaml` 与 `.agents/skills/aigc/_shared/story-source-manifest.template.yaml` | 将 required shared init templates 纳入 `scripts/aigc_skill_audit.py --strict` 缺失检查，避免只在执行时才暴露路径漂移 | `templates/output-template-map.md` 中 required shared 模板路径均可被 `test -f` 命中，审计缺失时失败 |
| 续跑与状态查询无法稳定重建断点 | 项目治理快照层 | 在需要时生成 `governance-state.yaml` | 用 shared template 固定 `last_stable_checkpoint + resume_contract + artifact_status` | `query / resume` 与根 `aigc` 的高风险治理 gate 能从同一份结构化快照读取断点与缺口 |
| 创作起盘被整套治理工件压得过重 | 初始化分层合同 | 把首次必出收敛到 `north_star / init_handoff / story-source-manifest / team / project_state` | 将 `governance-state + harness carriers` 改为惰性生成 | 首次初始化不再被非必要治理载体阻塞 |
| 路由、模式执行、充分性检查散落在旧外部 agent 或未声明分区 | 源层编排层 | 将入口门禁保留在父 `SKILL.md`，并把细则归入 `references/steps/review/types` 的显式 owner | 审计脚本反向约束 `0-初始化` 不得再引用 `.codex/agents/aigc/初始组/*.md`，且分区不得改写父入口路由 | `0-初始化` 能通过 `SKILL.md` 的 Reference Loading Guide 找到完整执行链 |
| `north_star` 混入下一阶段建议或 `rebootstrap` 状态 | 字段真源分层层 | 把 live route truth 收回 `STATE.json / governance-state.yaml`，把初始化当轮 handoff 收回 `init_handoff.yaml` | 在模板与审计脚本同时禁止 `north_star` 出现 `stage_entry_contract / rebootstrap_status` | `north_star` 只剩长期约束，续跑状态只从 `project_state/governance-state` 读取 |
| 初始化预建目录看起来与当前技能树“不匹配” | 真源口径混层 | 明确区分“技能树执行层”与“项目 runtime 落盘层”两套命名 | 在 `_shared/project-runtime-layout.md` 建立 `Skill Tree To Runtime Mapping`，并在 `0-初始化/SKILL.md` 同步注明 `5-Image / 6-Video` 的映射 | 读者不会再把 `1-提示词蒸馏/全能参照` 误读成必须预建 `projects/aigc/<项目名>/6-Video/1-提示词蒸馏/全能参照/` |
| 把“自动组队（推荐）”当成已锁定编组 | mode gate contract | 回到 `Initialization Mode Contract`，补发初始化元选项卡并等待用户确认 | 在 `SKILL.md` 明确“推荐项 != mode_lock_note”，并用审计脚本拦截歧义表述 | 仅有项目名或极简 brief 时，不再越权进入自动组队 |
| 自动组队把顾问选到 `.agents/skills/team/` 之外 | team scope contract | 立即裁掉越权成员，只保留 `team/` 树内 skill 并重写 `team.yaml` | 在 `team.yaml.init_contract.selector_scope_root` 固定 `.agents/skills/team/`，并在 `SKILL.md` 明确禁止外部候选 | `roles.*.members` 不再含 `.codex/agents/` 或仓外路径 |
| 自动组队直接全树扫描 `team/`，没有先走根层成员索引 | team root fast-path contract | 先读取 `.agents/skills/team/SKILL.md + CONTEXT.md` 的成员/场景索引，生成 shortlist 后再深读子技能 | 在 `0-初始化/SKILL.md` 固定“先根索引、后 shortlist deep-read”，并要求 team 根文档与成员树同步更新 | 自动选人理由可回溯到根层 `scenario_tags + candidate_shortlist` |
| 自动组队把治理角色和部门覆盖混成一层 | team governance contract | 先回到 `策划 / 监制 / 评审` 权属矩阵，再单独补 `导演组 / 设计组 / 摄影组` 必选覆盖 | 在 `SKILL.md` 与 `team.template.yaml` 同步固定“两层裁决”：治理角色先锁、部门选人后落 | `team.yaml` 同时能读出角色权属与部门覆盖，不再互相替代 |
| 把 `策划 / 监制 / 评审` 误判为必须三拨不同的人 | role allocation contract | 允许同人复用，也允许分人治理，并把实际选择写回 `team_setup.role_allocation_mode / role_overlap_notes` | 在 `SKILL.md` 与 `team.template.yaml` 固定“默认允许重叠，不默认强制互斥” | 后续读取 `team.yaml` 时，能看出是同人兼任还是分人治理 |
| 题材明显缺少更合适的大师，但初始化直接硬凑现有 roster 且无记录 | roster gap contract | 保留当前可执行 lineup，同时额外生成 `todos/*-team-recommendation.md` | 在 `SKILL.md` 固定“继续执行 + 输出推荐 todo + 写回 `team_setup.recommendation_todo_paths`”三联动作 | 题材缺口不会无痕消失，且本轮初始化不被阻塞 |
| planning 固定题包直答没有先于北极星综合执行 | direct-answer topology 层 | 回到 `N4-mode-engine`，先锁 `team.yaml` 再运行 `roles.planning.members` 的 subagents 固定题包直答 | 在 `Topology Contract` 与 `Execution Procedure` 固定 `team -> planning 固定题包直答 -> synthesis` 顺序 | `north_star / init_handoff` 可回溯到 planning 固定题包直答 provenance |
| planning 固定题包直答被降级成本地顺序扮演 | subagent gate 层 | 阻塞当前初始化并报告 subagents 不可用 | 在 `SKILL.md` 与 `team.template.yaml` 同时固定 `require_subagents_for_init_execution == true` | `0-初始化` 不再把本地模拟表述成正常主路径 |
| 上层模式合同已切到新口径，但 Thought Pass / Pass Table 仍是旧节点语义 | thought-action sync 层 | 把 `Thinking-Action Node Contract`、`Topology Contract`、`Thought Pass Map`、`Pass Table` 一起同步改写 | 每次模式/编组/subagent 语义变更，都强制补齐 `decision_lock / dispatch_contract / blocker_rule / reentry_rule` | 不再出现“主合同是新口径，节点检查还停在旧口径” |
| 缺故事源时先生成了剧情级预设，后补故事源也不回刷 | source completeness / reconciliation 层 | 将缺故事源初始化降级为 `source-light bootstrap`，并在故事源后补时强制回刷 `north_star / init_handoff / project_state` | 在 `references/artifacts-and-sources.md` 固化 `Story Source Completeness Gate + Story Source Reconciliation Contract`，并由 `review/init-review-gate.md` 消费 | 不再出现“题眼推断版剧情”覆盖真实故事源的情况 |
| 用户要求“回到初始化态重来”，却被误判成 `resume` 或局部补档 | 入口判型层 | 在 `N0-intake` 先锁 `rebootstrap_requested`，把主动回炉重起直接路由到 `0-初始化` | 在根 `aigc`、`0-初始化` 与 `resume` 三层同时固化“续跑 vs 重置式重新初始化”分工 | 明确要求回炉时，不再继续沿旧方向续跑 |
| 重置初始化时直接清空了 `Original/` 或原始素材 | reset preservation 层 | 默认改为 `archive_reset`，只归档派生产物与旧治理工件 | 在 `Rebootstrap Contract` 固定“故事主源、原始素材默认保留” | 回炉后仍能读取原始故事源与不可再生素材 |
| 预建阶段骨架被治理脚本误判成“已进入执行” | 轻量治理快照层 | 在治理回填脚本中只把真实文件产物视为阶段输出，不把空目录当执行证据 | 将“骨架目录 != 阶段产物”同步写入经验层，并在治理回填逻辑中固定 `is_file()` 判定 | `governance-state` 预演时，刚初始化的项目不会被误判到执行期 |
| Skill 2.0 升级后又把旧 mode stub 当成平行真源 | 技能目录结构层 | 只允许 `references/` 下的 owner 文件承载细则，不恢复 `references/*-mode/module-spec.md` 旧模式 stub | `SKILL.md` 固定动态引用表，`references/migration-matrix.md` 记录旧段落去向，review gate 检查分区不越权 | `find .agents/skills/aigc/0-初始化 -maxdepth 3` 可看到标准 Skill 2.0 分区，但没有旧三模式 stub |
| 初始化仍预建旧英文 runtime 根 | runtime naming drift | 将 `Original/`, `1-Planning/`, `2-Global/`, `3-Detail/`, `4-Design/`, `5-Image/`, `6-Video/`, `7-Cut/` 列为 legacy/forbidden bootstrap paths | 审计脚本检查中文 skeleton marker，同时允许现有历史项目保留旧目录作为兼容输入 | 新项目初始化只生成用户指定的中文目录，不再混用两套真源 |
| 初始化把项目级预设材料散落到 `CONTEXT/` 或 `Assets/` | project runtime preset layer | 将新项目预设入口固定为 `CONTEXT/`，故事源入口固定为 `源/` | 模板用 `project-context-readme.template.md` 初始化 `CONTEXT/README.md` | 项目偏好仍在 `MEMORY.md`，预设材料有独立落点，live route truth 仍在 `STATE.json` |
| 分镜脚本故事源登记时按语义自造 `preset_registry.lock_level` 值 | story-source contract / 枚举边界层 | 将 `high / critical` 等自然语言强度值改为合法枚举 `hard_lock / soft_lock / reference_only` | 起草 storyboard_script manifest 时先回读 `_shared/story-source-contract.md` 的 Source-Type Extension Fields，禁止自造 lock level | manifest YAML 解析后，所有 `preset_registry[].lock_level` 均属于合法枚举 |

## Repair Playbook

1. 先确认问题属于模式锁定、问题设计、主文件分工、团队治理、思行节点断裂还是落盘漂移。
2. 优先回到 `0-初始化/SKILL.md` 的 `Initialization Mode Contract`、`Internal Capability Fusion Contract`、`Topology Contract`、`North Star Contract` 与 `Sufficiency Gate`。
3. 若是字段边界问题，先修模板真源。
4. 若是路径问题，先回查根 `aigc/SKILL.md` 与本阶段 `Canonical Landing`。
5. 若是能力外置或执行链断裂，先修父 `SKILL.md` 的入口路由与 `steps/init-workflow.md` 的节点网络，再修局部文字。
6. 只有源层合同稳定后，才修本次具体输出。
7. 若问题发生在 `N1-mode-gate`，先区分“推荐”“默认展示项”“已锁定模式”三层状态；只有最后一层允许进入 `N2` 之后的节点。
8. 若问题发生在故事源后补场景，先区分“概念级约束”和“剧情级 seed”；凡属剧情级 seed，先回刷再允许下游继续。

## Reusable Heuristics

- 对当前 `aigc` 技能树来说，`0-初始化` 最重要的不是“问得多”，而是“把 north star 与阶段入口种子分干净”。
- 影视初始化最容易过度下潜到设计或分镜细节；凡是会在下游阶段形成 canonical 的内容，都只应在这里保留 seed。
- 当前仓库的初始化落点必须优先服从 `projects/aigc/<项目名>/`，而不是借用其他项目系的 state/layout。
- 初始化阶段即使知道后续 runtime 分区，也只记录命名与 handoff；阶段根目录和 child skeleton 必须由对应阶段在执行时创建。
- 项目根 `CHANGELOG.md` 最稳的定位是“时间序记录入口”，初始化就创建，但不参与 `query / resume` 或根 `aigc` 高风险治理 gate 的 live governance 判型。
- 只要某工件会被多个兄弟阶段长期共同消费，就不该继续挂在 `0-初始化/` 名下；最稳的做法是提升到项目根。
- 对长期维护的可执行技能目录，除 `SKILL.md + CONTEXT.md` 外，还应补齐 `agents/openai.yaml`。
- 当自动组队只收到一个极简概念时，优先先组出最小 planning 顾问团，把高分叉问题压进 `unknowns`，不要伪造完整剧情 seed。
- 只要用户没有明确要求“贴原作/保原顺序/保留原作节奏”，`original_adherence` 就应显式落盘为 `false`。
- 如果项目后续要做 `1-分集`，最稳的初始化习惯不是先问“要不要分几集”，而是先把“故事主源在哪、是否完整、能否正式切分”写进 `story-source-manifest.yaml`。
- 只要 `templates/output-template-map.md` 或 `references/artifacts-and-sources.md` 声明 shared 模板为初始化必需输入，模板文件本体必须同轮落在声明路径下；不能把“shared”当成未来会补的逻辑占位。
- `north_star` 可以承载 `全局风格 / 细分风格 / 类型元素 / 世界观` 这类长期全局 context；但一旦开始承载“下一步去哪”或 `rebootstrap` 过程痕迹，就说明长期约束真源和运行时状态真源混层了，这类信息应回到 `project_state / governance-state / init_handoff`。
- `全局风格` 只适合写所有设计类型都能安全继承的前缀；凡是镜头语言、角色材质、服装、建筑、物品或场景专属语义，都应落入 `细分风格` 或后续阶段，而不是塞进全局前缀。
- `细分风格.画面风格` 是全片统一的画面基调，不是场景别摄影表；姜家、陆家、巴黎、马场等差异化光色/空间策略应放到 handoff 或后续摄影、场景设计阶段。
- `全局风格提示词` 是供后续提示词直接继承的投影字段，必须显式带上 `媒介属性` 的完整值；不要只在旁侧字段写媒介属性却让提示词本体缺失。
- north-star 风格字段默认使用中文；全局前缀要短而稳，类型元素更短，细分风格只保留各设计链路需要的高密度口径。
- 项目离开 `0-初始化` 之后，`init_handoff` 仍可保留初始化时的 handoff seed，但 live current-stage truth 只能看 `project_state` 与 `governance-state`。
- 对创作起盘来说，最小闭环应先保证 `north_star / init_handoff / story-source-manifest / team / project_state`；其余治理载体只有在复杂执行或卫星技能真正需要时再补。
- 对 `知行合一` 编排的 `0-初始化`，最稳的写法不是再造第二份思考文档，而是把路由、三种模式和充分性审计直接写进同一份父 `SKILL.md`。
- Skill 2.0 化以后，`references/` 是细则 owner，但不得恢复旧 `references/*-mode/module-spec.md` 三模式 stub；新分区必须由 `SKILL.md` 的 Reference Loading Guide 明确引用。
- 阶段质评若要做动态检查，优先直接回读当前样本项目、模板边界与 audit/validator 结果，不必为了评估再维护一份固定评测任务 YAML。
- 对项目初始化骨架，新项目默认生成扁平中文 runtime 容器：`1-分集`、`2-编导`、`3-摄影`、`4-分组`、`5-设计`、`6-图像`、`7-视频`。空目录只是容器，不等于阶段已执行。
- 对跨阶段共享的预设和素材方向盘，优先放进 `CONTEXT/`；真实故事/剧本源落到 `源/`。
- 当前技能树仍可能使用英文包名，但项目 runtime 已切到中文目录；文档中必须区分 skill package path 与 project runtime path。
- 对 `4-Design` 这类“技能树 tranche 父层 != runtime 落盘层”的阶段，初始化只记录 runtime 规则；实际 domain-first 业务目录由设计阶段执行时创建。
- 当技能树有中间 tranche，但项目 runtime 只接受业务语义落盘名时，必须优先相信 `_shared/project-runtime-layout.md`，并在阶段合同里把两套命名的映射写明；否则读者会把“技能目录现状”误当成“项目预建目录”。
- 在 `0-初始化` 里，`智能顾问模式` 是固定主模式，真正需要用户拍板的是 `自动组队 / 自定义组队`；只要用户没拍板且不存在强制路由信号，就必须停在 `N1-mode-gate`。
- `team.yaml` 现在不仅是阶段顾问运行时，也是初始化编组真源；最少要看 `init_contract.*`、`roles.planning.init_execution.*` 和 `runtime_policy.require_subagents_for_init_execution`。
- `0-初始化` 自动组队若想选得快又稳，关键不是直接遍历整个 `team/` 树，而是先读 team 根文档的成员/场景索引，把 deep read 限定在 shortlist 内。
- 对当前 `0-初始化`，`策划 / 监制 / 评审` 是治理角色，不等于具体选人部门；自动组队应先锁治理权属，再补部门覆盖。
- `策划 / 监制 / 评审` 可以是同一波人，也可以是不同的人；是否重叠是编组策略问题，不是角色定义问题。
- 自动组队的最小可靠闭环是 `导演组 + 设计组 + 摄影组`；其他组只有在题材或执行难点真正需要时再加。
- 题材缺口如果暂时无法靠仓内 roster 补齐，最稳的处理不是阻塞初始化，而是保留当前 lineup 并额外写一份 `todos/*-team-recommendation.md`。
- 初始化固定题包直答的第一发题权属于父技能；`roles.planning.members` 负责对既定题包并行直答。如果一开始就是主代理自己自由追问，通常说明 team topology 被绕过了。
- 只要 `0-初始化` 改了模式、编组或 subagent 合同，就必须同步改 `Thinking-Action Node Contract / Topology Contract / Thought Pass Map / Pass Table`；节点层不同步，后续执行就会偷偷回到旧语义。
- `0-初始化` 可以在缺故事源时初始化项目，但只能生成题材级、边界级、生产级约束；凡是剧情级、单集级、人物关系级推断，都应降级为 provisional unknowns。
- 一旦真实故事源后补进入 `源/`，优先动作不是继续下游阶段，而是先回刷 `north_star / init_handoff / project_state` 中的 assistant-inferred 剧情字段。
- 对已跑出下游产物的项目，默认最稳的回炉方式是 `archive_reset`：保留故事源和原始素材，归档旧阶段派生产物，再重写 `north_star / init_handoff / project_state`。
- “继续当前方向但补断点”属于 `resume/`；“推翻当前方向重新起盘”属于 `0-初始化`，两者不能混判。
- 对新中文初始化骨架，`1-分集 / 2-编导 / ...` 这些空目录只是预置容器；治理脚本仍应只把真实文件产物视为阶段输出，不能把空目录当作已执行证据。
- 当 `primary_story_source.source_type == storyboard_script` 且需要登记 `preset_registry` 时，`lock_level` 只能使用 `_shared/story-source-contract.md` 的三档枚举：`hard_lock`、`soft_lock`、`reference_only`；不要用 `high`、`critical` 这类语义强度词。

## Archive Index

- 详细迁移线索已外置到 [`CHANGELOG.md`](./CHANGELOG.md)。
- 已归档的 subagent-era 迁移材料只保留在历史变更说明中，不再作为现行执行真源。
