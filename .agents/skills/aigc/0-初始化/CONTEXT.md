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
| 初始化继续生成 `north_star / init_handoff / story-source-manifest / team / STATE` 等旧五件套或治理载体 | scaffold-plus-memory 合同漂移 | 回到 `0-初始化/SKILL.md`，只创建当前 `0-初始化` 到 `10-画布` 目录、项目根 `MEMORY.md` 和项目根 `CONTEXT/README.md`，并把初始化用户信息吸收进 `MEMORY.md` | 在 `scope-and-runtime.md`、`steps/init-workflow.md`、`review/init-review-gate.md` 与审计脚本同步 denylist 旧初始化产物，并把 `CONTEXT/` 保留为侧车允许项 | 新项目初始化后只有当前 0-10 目录、`MEMORY.md` 与 `CONTEXT/README.md` 是本轮写回产物；团队配置和资料摘要能从 `MEMORY.md` 读到 |
| 初始化目录仍按旧 `2-编导 / 3-运动 / 4-摄影` 骨架创建 | runtime skeleton 命名漂移 | 改用当前技能包名：`2-美学 / 3-主体 / 4-编剧 / 5-导演 / 6-分镜 / 7-摄影 / 8-分组` | 共享 runtime layout 与 `0-初始化` allowlist 同步维护当前 0-10 阶段链；`backup/5-表演`、`backup/6-氛围`、`backup/9-光影` 不参与新项目 scaffold | 初始化目录读回包含 `0-初始化` 到 `10-画布` 的最新包名，不包含旧别名或 backup 阶段 |
| 初始化用户要求、团队配置或补充资料没有进入项目记忆 | MEMORY.md 职责收窄不清 | 在 `MEMORY.md` 增加/更新“初始化时用户要求”“团队配置与协作偏好”“初始化资料吸收摘要”“阶段上下文读取指南”等段落 | 把初始化记忆写入设为 `N3-memory` 必过门禁；已有 memory 只能合并不能静默覆盖；大段资料可进 `CONTEXT/` 侧车但 `MEMORY.md` 必须有吸收摘要 | `projects/aigc/<项目名>/MEMORY.md` 能读到本轮长期要求、团队配置、资料吸收摘要或明确暂无 |
| “初始化小说”误入 AIGC 影片初始化，或“初始化影片/电影”被 story 初始化截走 | 媒介语义路由层 | 在 `aigc-init` 入口、registry routes 与 product metadata 中显式写入 film/movie/video 正向触发和 novel/book 负向排除 | 把自然语义触发词分成两组：`影片/电影/影视/视频 -> .agents/skills/aigc/0-初始化`，`小说/网文/书/长篇故事 -> .agents/skills/story/0-初始化` | 输入“初始化电影/影片”只落 `projects/aigc/<项目名>/`；输入“初始化小说/网文”只落 `projects/story/<项目名>/` |
| 初始化又长出旧三模式、平行问卷、自动组队或自定义组队入口 | 模式合同层 | 删除 active team mode；把用户明确给出的团队、顾问、评审、协作和创作视角偏好写入 `MEMORY.md` | `mode-and-team-contract.md` 固定“无自动组队、无 team.yaml、无顾问问答”；下游只消费 `project_memory_init_context` | 全文没有 active team mode；初始化不因缺 team/handoff/north-star 失败 |
| 下游需要风格、类型或 handoff，但初始化只生成 scaffold | 载体 owner 分层 | 不在 `0-初始化` 复活旧五件套；风格/类型需求路由到 `2-美学`，恢复/补档需求路由到明确 owning workflow、`resume` 或项目级补档任务 | 下游技能把 `2-美学` 输出作为美学真源，把 `MEMORY.md` 作为初始化用户信息真源；不得假定初始化已生成旧风格载体 | 新项目初始化后不会因为缺旧五件套被误判为初始化失败，且下游可从 `2-美学` 获取正式风格上下文 |
| `全局风格` 被继续当作跨设计交集安全前缀，导致场景化光影、色彩和质感被删掉 | `2-美学/画面基调` 风格概念层 | 将 `全局风格` 改为指导整个作品全集的并集式总风格：保留共享媒介/时代/质感底座，同时允许室内、室外、夜景、动作、群像、旷野等场景类型的光影、色彩、材质、氛围、摄影和禁区规则 | 在 `2-美学/画面基调` 合同、review gate 与 audit 脚本同步检查 `全局风格` 是 whole-work union style contract | `2-美学/画面基调/全局风格协议.md` 能被后续阶段按当前分镜组抽取相关片段，而不是被所有场景原样照抄 |
| `画面风格` 写成唯一承载场景别策略的清单 | `2-美学` 细分风格边界层 | `画面风格` 保持全片画面摘要；可复用的场景化光影/色彩矩阵回到 `画面基调.Global Style Prompt` 或对应风格协议 | `2-美学` 区分“总风格场景化规则”和“画面风格摘要” | `画面风格` 不替代全局风格矩阵，后续分组从 `2-美学` 输出中摘取当前组匹配部分 |
| `Global Style Prompt` 没有显式包含 `媒介属性`，导致后续图像/视频提示词丢失媒介真源 | `2-美学` prompt projection 层 | 将 `Global Style Prompt` 改为显式包含媒介属性，例如“真人版古装影视质感，...” | 在 `2-美学` 模板、review gate 与项目记忆中同步要求 `Global Style Prompt` 包含当前媒介属性 | `2-美学/画面基调/全局风格协议.md` 的 prompt 字符串包含媒介属性完整值，且按高密度自然段表达总风格 |
| 风格字段仍按旧短前缀压缩 | 输出约束层 | `Global Style Prompt` 保持可承接下游的高密度总风格母稿；类型元素提示词仍短；服装/建筑/物品保持简明域级摘要 | 在 `2-美学` 合同、模板、review gate 和 audit marker 同步声明 | `2-美学` 产物既能表达总风格全貌，又能被 `8-分组` 摘取为当前组风格语句 |
| 顾问团或 `team.yaml` 被当作初始化必出 | 团队治理层 | 不创建 `team.yaml`；把用户指定的团队、协作、reviewer、创作视角和禁用视角整理进项目 `MEMORY.md` | `project-memory.template.md` 固定团队配置与协作偏好段；下游优先读 `MEMORY.md`，不得把缺 `team.yaml` 记为初始化失败 | 新项目初始化不生成团队文件，但 `MEMORY.md` 能承载用户指定的团队上下文 |
| 工件落盘漂向旧路径或外仓 | 路径合同层 | 固定到 `projects/aigc/<项目名>/0-初始化/` 与项目根 | 在根 `aigc` 与 `0-初始化` 双层合同中同时声明 canonical landing | 全部初始化工件都位于当前仓库项目路径 |
| 初始化目录骨架仍沿用旧英文、旧编号或旧中文骨架 | runtime skeleton 合同层 | 把初始化目录约定改为当前 0-10 中文 runtime：`0-初始化/` 到 `10-画布/`，包含 `2-美学/3-主体/4-编剧/5-导演/6-分镜/7-摄影/8-分组`，并创建项目 `MEMORY.md` 与 `CONTEXT/README.md` | 让 `0-初始化`、scope/runtime 合同、模板与 `aigc_skill_audit.py` 共用同一套 skeleton；backup 阶段只作显式历史回读 | 初始化合同、模板、registry 与审计 marker 同步 |
| 初始化项目根漏建 `CONTEXT/`，导致根规则要求的项目上下文加载无稳定入口 | project-context carrier 层 | 在 `N2-scaffold` 创建 `CONTEXT/`，在 `N3-memory` 创建 `CONTEXT/README.md` | 将 `CONTEXT/` 上收到 `_shared/project-runtime-layout.md`，并让 `0-初始化/SKILL.md`、review gate 与审计脚本同步检查 | 新项目初始化后项目根默认具备项目上下文入口，但不会生成旧 north-star/team/state |
| `STATE.json`、`route-plan.yaml` 与 `init_handoff/governance-state` 给出不同下一步 | 阶段入口同步层 | 不由初始化创建 live route truth；已有项目冲突时交给 `resume` 或治理回填 owner 决定 authority order | 在 `resume` / review 治理合同中固定 state authority，不把初始化 scaffold 当阶段入口裁决源 | 新项目初始化后没有平行下一步真源；已有项目修复时只保留一个主入口 |
| 项目进入 `1-分集` 前没有故事主源登记 | 共享输入真源层 | 不在初始化阶段伪造 `story-source-manifest.yaml`；由 `1-分集`、source intake 或 `resume` 在需要时创建/报告缺口 | 将故事源落点与缺失提示放到 source-owning workflow，不把缺故事源判为初始化失败 | 初始化完成后可继续停在 source 缺口说明，而不是生成剧情级假 seed |
| 初始化合同声明 shared 模板，但声明路径下没有对应文件 | 模板真源落盘层 | 只补齐当前仍有 active/optional reader 的 shared 模板，例如 `governance-state.template.yaml`；不恢复已删除的 `story-source-manifest.template.yaml` 或把 `team.template.yaml` 重新变成初始化真源 | 将 current shared templates 纳入 `scripts/aigc_skill_audit.py --strict` 缺失检查，避免只在执行时才暴露路径漂移 | 当前 active shared 模板路径均可被 `test -f` 命中；团队配置以 `MEMORY.md` 为承载 |
| 续跑与状态查询无法稳定重建断点 | 项目治理快照层 | 在需要时生成 `governance-state.yaml` | 用 shared template 固定 `last_stable_checkpoint + resume_contract + artifact_status` | `query / resume` 与根 `aigc` 的高风险治理 gate 能从同一份结构化快照读取断点与缺口 |
| 创作起盘被整套治理工件压得过重 | 初始化分层合同 | 把首次必出收敛到 0-10 scaffold、`MEMORY.md` 和 `CONTEXT/README.md` | 将 `north_star/team/state/governance/source` 等 carriers 交给后续 owning workflow 惰性生成 | 首次初始化不再被非必要治理载体阻塞 |
| 路由、模式执行、充分性检查散落在旧外部 agent 或未声明分区 | 源层编排层 | 将入口门禁保留在父 `SKILL.md`，并把细则归入 `references/steps/review/types` 的显式 owner | 审计脚本反向约束 `0-初始化` 不得再引用 `.codex/agents/aigc/初始组/*.md`，且分区不得改写父入口路由 | `0-初始化` 能通过 `SKILL.md` 的 Reference Loading Guide 找到完整执行链 |
| 旧风格载体混入下一阶段建议或 `rebootstrap` 状态 | 字段真源分层层 | 把 live route truth 收回 `STATE.json / governance-state.yaml`；新初始化不创建旧风格或 handoff 载体 | 在模板与审计脚本同时禁止 legacy carrier 被当作 live route truth | 续跑状态只从 `STATE.json/governance-state` 读取；legacy carrier 只作历史证据 |
| 初始化预建目录看起来与当前技能树“不匹配” | 真源口径混层 | 明确区分“技能树执行层”与“项目 runtime 落盘层”两套命名 | 在 `_shared/project-runtime-layout.md` 建立 `Skill Tree To Runtime Mapping`，并在 `0-初始化/SKILL.md` 同步注明 `5-Image / 6-Video` 的映射 | 读者不会再把 `1-提示词蒸馏/全能参照` 误读成必须预建 `projects/aigc/<项目名>/6-Video/1-提示词蒸馏/全能参照/` |
| 把“自动组队（推荐）”当成现行入口 | legacy mode gate contract | 不再展示或锁定自动组队；只记录用户明确给出的团队/评审偏好 | 审计与经验层都把自动组队归为 legacy topology revival | 仅有项目名或极简 brief 时，只创建 scaffold 与记忆占位，不进入团队调度 |
| 自动组队、planning 固定题包或旧顾问链又被恢复 | legacy team topology 层 | 停止团队调度；把用户明确给出的团队/顾问/评审偏好压缩进 `MEMORY.md` | `SKILL.md` 与 `mode-and-team-contract.md` 固定“无自动组队、无 team.yaml、无顾问问答；团队信息属于 MEMORY 上下文” | 当前初始化不因缺 `team.yaml / north_star / init_handoff` 失败，且不把本地判断伪装成顾问输出 |
| 用户提供大量参考资料但只写入 `CONTEXT/` 没有进入可读记忆 | context hub drift | LLM 先吸收整理成 `MEMORY.md` 的资料摘要、使用边界、下游用途和待确认项；大段原文或索引再放 `CONTEXT/` | `project-context-readme.template.md` 固定 `CONTEXT/` 是侧车，`MEMORY.md` 是中枢 | 后续阶段先读 `MEMORY.md` 即可理解资料如何影响本阶段，必要时再追到 `CONTEXT/` |
| 上层模式合同已切到新口径，但 Thought Pass / Pass Table 仍是旧节点语义 | thought-action sync 层 | 把 `Thinking-Action Node Contract`、`Topology Contract`、`Thought Pass Map`、`Pass Table` 一起同步改写 | 每次模式/编组/顾问与复核流程 语义变更，都强制补齐 `decision_lock / dispatch_contract / blocker_rule / reentry_rule` | 不再出现“主合同是新口径，节点检查还停在旧口径” |
| 缺故事源时先生成了剧情级预设，后补故事源也不回刷 | source completeness / reconciliation 层 | 将缺故事源初始化降级为 `source-light bootstrap`，并在故事源后补时强制回看 `MEMORY.md`、`2-美学` 和已有下游派生产物中的 assistant-inferred 字段 | 在 `references/artifacts-and-sources.md` 固化 Story Source Completeness Gate，并由 owning stage 负责修正下游 | 不再出现“题眼推断版剧情”覆盖真实故事源的情况 |
| 用户要求“回到初始化态重来”，却被误判成 `resume` 或局部补档 | 入口判型层 | 在 `N0-intake` 先锁 `rebootstrap_requested`，把主动回炉重起直接路由到 `0-初始化` | 在根 `aigc`、`0-初始化` 与 `resume` 三层同时固化“续跑 vs 重置式重新初始化”分工 | 明确要求回炉时，不再继续沿旧方向续跑 |
| 重置初始化时直接清空了 `Original/` 或原始素材 | reset preservation 层 | 默认改为 `archive_reset`，只归档派生产物与旧治理工件 | 在 `Rebootstrap Contract` 固定“故事主源、原始素材默认保留” | 回炉后仍能读取原始故事源与不可再生素材 |
| 预建阶段骨架被治理脚本误判成“已进入执行” | 轻量治理快照层 | 在治理回填脚本中只把真实文件产物视为阶段输出，不把空目录当执行证据 | 将“骨架目录 != 阶段产物”同步写入经验层，并在治理回填逻辑中固定 `is_file()` 判定 | `governance-state` 预演时，刚初始化的项目不会被误判到执行期 |
| Skill 2.0 升级后又把旧 mode stub 当成平行真源 | 技能目录结构层 | 只允许 `references/` 下的 owner 文件承载细则，不恢复 `references/*-mode/module-spec.md` 旧模式 stub | `SKILL.md` 固定动态引用表，`references/migration-matrix.md` 记录旧段落去向，review gate 检查分区不越权 | `find .agents/skills/aigc/0-初始化 -maxdepth 3` 可看到标准 Skill 2.0 分区，但没有旧三模式 stub |
| 初始化仍预建旧英文 runtime 根 | runtime naming drift | 将 `Original/`, `1-Planning/`, `2-Global/`, `3-Detail/`, `4-Design/`, `5-Image/`, `6-Video/`, `7-Cut/` 列为 legacy/forbidden bootstrap paths | 审计脚本检查中文 skeleton marker，同时允许现有历史项目保留旧目录作为兼容输入 | 新项目初始化只生成用户指定的中文目录，不再混用两套真源 |
| 初始化把项目级预设材料散落到 `CONTEXT/` 或 `Assets/` | project runtime preset layer | 将新项目预设入口固定为 `CONTEXT/`，故事源入口固定为 `源/` | 模板用 `project-context-readme.template.md` 初始化 `CONTEXT/README.md` | 项目偏好仍在 `MEMORY.md`，预设材料有独立落点，live route truth 仍在 `STATE.json` |
| 分镜脚本故事源登记时按语义自造 `preset_registry.lock_level` 值 | story-source contract / 枚举边界层 | 将 `high / critical` 等自然语言强度值改为合法枚举 `hard_lock / soft_lock / reference_only` | 起草 storyboard_script manifest 时先回读 `_shared/story-source-contract.md` 的 Source-Type Extension Fields，禁止自造 lock level | manifest YAML 解析后，所有 `preset_registry[].lock_level` 均属于合法枚举 |

## Repair Playbook

1. 先确认问题属于模式锁定、问题设计、主文件分工、团队治理、思行节点断裂还是落盘漂移。
2. 优先回到 `0-初始化/SKILL.md` 的 scaffold-plus-memory runtime spine、输入合同、目录 allowlist、former-output denylist 与 memory/context 写回门禁。
3. 若是字段边界问题，先修模板真源。
4. 若是路径问题，先回查根 `aigc/SKILL.md` 与本阶段 `Canonical Landing`。
5. 若是能力外置或执行链断裂，先修父 `SKILL.md` 的入口路由与 `steps/init-workflow.md` 的节点网络，再修局部文字。
6. 只有源层合同稳定后，才修本次具体输出。
7. 若问题发生在 `N1-mode-gate`，先区分“推荐”“默认展示项”“已锁定模式”三层状态；只有最后一层允许进入 `N2` 之后的节点。
8. 若问题发生在故事源后补场景，先区分“概念级约束”和“剧情级 seed”；凡属剧情级 seed，先回刷再允许下游继续。

## Reusable Heuristics

- 对当前 `aigc` 技能树来说，`0-初始化` 最重要的不是“问得多”，而是完成项目 runtime scaffold，并把初始化时用户指定的信息集中整理进 `MEMORY.md`；项目 `CONTEXT/` 只做补充资料侧车，不提前制造下游创作真源。
- 影视初始化最容易过度下潜到设计或分镜细节；凡是会在下游阶段形成 canonical 的内容，都只应在这里保留 seed。
- 当前仓库的初始化落点必须优先服从 `projects/aigc/<项目名>/`，而不是借用其他项目系的 state/layout。
- 初始化阶段会预建当前共享布局声明的阶段骨架容器；但只记录命名与 handoff，具体业务正文、任务子目录和 provider 子目录仍由 owning stage 执行时创建。
- 项目根 `CHANGELOG.md` 最稳的定位是“时间序记录入口”，但不属于当前初始化必出；需要时间线记录的 workflow 再创建，且不参与 `query / resume` 或根 `aigc` 高风险治理 gate 的 live governance 判型。
- 只要某工件会被多个兄弟阶段长期共同消费，就不该继续挂在 `0-初始化/` 名下；最稳的做法是提升到项目根。
- 对长期维护的可执行技能目录，除 `SKILL.md + CONTEXT.md` 外，还应补齐 `agents/openai.yaml`。
- 当初始化只收到一个极简概念时，只创建 scaffold 与 `MEMORY.md` 占位，把高分叉剧情、团队、资料问题压进待确认，不伪造顾问团或完整剧情 seed。
- 只要用户没有明确要求“贴原作/保原顺序/保留原作节奏”，`original_adherence` 就应显式落盘为 `false`。
- 如果项目后续要做 `1-分集`，最稳的初始化习惯不是生成 story-source manifest 占位，而是保留项目长期要求并让 `1-分集` 对真实故事源做完整性校验。
- 只要 `templates/output-template-map.md` 或 `references/artifacts-and-sources.md` 声明 shared 模板为初始化必需输入，模板文件本体必须同轮落在声明路径下；不能把“shared”当成未来会补的逻辑占位。
- 旧风格载体若在旧项目中存在，只能承载历史 context；一旦包含“下一步去哪”或 `rebootstrap` 过程痕迹，就说明长期约束真源和运行时状态真源混层了，这类信息应回到 `STATE.json / governance-state.yaml`。
- `2-美学/画面基调/全局风格协议.md` 是作品全集总风格的并集式真源；可以承载场景类型对应的光影、色彩、材质、空气、摄影和禁区逻辑，但不能承载单个镜号、一次性剧情事实或某个资产清单专属设计。
- `2-美学` 的画面摘要不是唯一的场景别摄影表；可复用场景化光色策略优先放在 `画面基调/全局风格协议.md`，下游 `8-分组` 再按当前分镜组摘取相关部分。
- `Global Style Prompt` 是供后续阶段按场景抽取的总风格母稿，必须显式带上 `媒介属性` 的完整值；不要只在旁侧字段写媒介属性却让提示词本体缺失。
- `2-美学` 风格字段默认使用中文；`Global Style Prompt` 通常 300-500 字，类型元素仍短，细分风格保留各设计链路需要的高密度口径。
- 项目离开 `0-初始化` 之后，legacy `init_handoff` 只可保留历史 handoff seed；live current-stage truth 只能看 `STATE.json` 与 `governance-state.yaml`。
- 对创作起盘来说，最小闭环应先保证当前 0-10 scaffold、强记忆版项目 `MEMORY.md` 和项目 `CONTEXT/README.md`；团队配置、资料吸收摘要、生产限制和阶段读取指南优先进入 `MEMORY.md`，其余治理载体只有在复杂执行或卫星技能真正需要时再补。
- 对 `知行合一` 编排的 `0-初始化`，最稳的写法不是再造第二份思考文档，而是把路由、三种模式和充分性审计直接写进同一份父 `SKILL.md`。
- Skill 2.0 化以后，`references/` 是细则 owner，但不得恢复旧 `references/*-mode/module-spec.md` 三模式 stub；新分区必须由 `SKILL.md` 的 Reference Loading Guide 明确引用。
- 阶段质评若要做动态检查，优先直接回读当前样本项目、模板边界与 audit/validator 结果，不必为了评估再维护一份固定评测任务 YAML。
- 对项目初始化骨架，新项目默认生成当前 0-10 扁平中文 runtime 容器：`1-分集`、`2-美学`、`3-主体`、`4-编剧`、`5-导演`、`6-分镜`、`7-摄影`、`8-分组`、`9-图像`、`10-画布`，并创建 `MEMORY.md` 与 `CONTEXT/README.md`。`backup/5-表演`、`backup/6-氛围`、`backup/9-光影` 不预建为空目录；空目录只是容器，不等于阶段已执行。
- 对跨阶段共享的预设和素材方向盘，优先放进 `CONTEXT/`；真实故事/剧本源落到 `源/`。
- 当前技能树仍可能使用英文包名，但项目 runtime 已切到中文目录；文档中必须区分 skill package path 与 project runtime path。
- 对 `3-主体` 这类“阶段父层 + 域级子包”的阶段，初始化只预建统一 runtime 容器与域级 readiness 目录；实际 domain-first 业务正文由设计阶段执行时创建。
- 当技能树有中间 tranche，但项目 runtime 只接受业务语义落盘名时，必须优先相信 `_shared/project-runtime-layout.md`，并在阶段合同里把两套命名的映射写明；否则读者会把“技能目录现状”误当成“项目预建目录”。
- 在 `0-初始化` 里，不再有 `智能顾问模式 -> 自动组队 / 自定义组队` 的 active 入口；用户提供的团队、顾问、评审或创作视角信息全部视为项目记忆输入，进入 `MEMORY.md`。
- `team.yaml` 只保留为历史兼容证据；新初始化不得生成它，也不得把缺失视为阻塞。后续阶段优先读取 `MEMORY.md` 的“团队配置与协作偏好”和“阶段上下文读取指南”。
- 团队信息进入 `MEMORY.md` 时，要区分“用户指定成员/角色”“希望借鉴的创作视角”“禁止采用的视角”“协作方式偏好”和“下游读取边界”，不要压成名单。
- 用户提供大量参考资料时，最稳的处理是 LLM 先写 `初始化资料吸收摘要`，说明 source、吸收后的长期记忆、下游用途和状态；大段原文、索引或模型参数再放 `CONTEXT/` 侧车。
- 只要 `0-初始化` 改了 memory/context 工程合同，就必须同步改 `Thinking-Action Node Contract / Topology Contract / Thought Pass Map / Pass Table`；节点层不同步，后续执行就会偷偷回到旧语义。
- `0-初始化` 可以在缺故事源时初始化项目，但只能生成题材级、边界级、生产级约束；凡是剧情级、单集级、人物关系级推断，都应降级为 provisional unknowns。
- 一旦真实故事源后补进入 `源/`，优先动作不是继续下游阶段，而是先回看 `MEMORY.md`、`STATE.json` 与已存在阶段产物中的 assistant-inferred 剧情字段，并由 owning stage 修正。
- 对已跑出下游产物的项目，默认最稳的回炉方式是 `archive_reset`：保留故事源和原始素材，归档旧阶段派生产物，再重建 current runtime scaffold、`MEMORY.md` 和必要治理状态。
- “继续当前方向但补断点”属于 `resume/`；“推翻当前方向重新起盘”属于 `0-初始化`，两者不能混判。
- 对新中文初始化骨架，`0-初始化 / 1-分集 / 2-美学 / 3-主体 / 4-编剧 / ... / 10-画布` 这些空目录只是预置容器；治理脚本仍应只把真实文件产物视为阶段输出，不能把空目录当作已执行证据。
- 当 `primary_story_source.source_type == storyboard_script` 且需要登记 `preset_registry` 时，`lock_level` 只能使用 `_shared/story-source-contract.md` 的三档枚举：`hard_lock`、`soft_lock`、`reference_only`；不要用 `high`、`critical` 这类语义强度词。

## Archive Index

- 详细迁移线索已外置到 [`CHANGELOG.md`](./CHANGELOG.md)。
- 已归档的 顾问与复核流程-era 迁移材料只保留在历史变更说明中，不再作为现行执行真源。
