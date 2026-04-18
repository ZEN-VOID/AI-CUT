# CONTEXT.md

## Context Health

- soft_limit_chars: 40000
- hard_limit_chars: 80000
- soft_limit_cases: 80
- hard_limit_cases: 140
- status: ok

## Type Map

| failure_or_outcome_type | root_cause_layer | immediate_fix | systemic_prevention | verification_point |
|---|---|---|---|---|
| 初始化技能路径仍指向旧插件目录 | skill contract | 改为 repo-local `story2026` 路径约定 | 在技能文档内固定 `REPO_ROOT/.agents/skills/story` | 预检命令可解析 `SCRIPTS_DIR` |
| 初始化仍依赖 Claude Code 专属提问工具 | skill contract | 改成 Codex 可执行的普通文本问卷轮次 | 在 `0-Init` 中固化 Questionnaire Contract，并禁止依赖 `AskUserQuestion` | 每轮问题都可直接作为普通消息发送 |
| 初始化完成后没有稳定交给 Cards 层 | stage handoff contract | 在 `0-Init` 明确写入 `Cards Handoff Contract` | 固化 `访谈 -> north_star.cards -> 角色卡 -> 场景卡 -> 物品卡` 的顺序与加载边界 | `1-Cards` 能只凭初始化简报顺序建卡 |
| 题材资料出现 `templates/genres` 与 `story2026/genres` 双根并存 | genre asset governance | 将旧分片并入 `templates/genres/details/` 并删除平行根目录 | 在 `0-Init` 固化 `templates/genres/` 为唯一 canonical 根，并用 README 记录入口模板与 detail pack 映射 | 全仓检索不存在 `.agents/skills/story/genres` 活跃路径 |
| `0-Init/references/` 仍残留题材套路私有副本，和共享 `templates/genres/` 职责重叠 | genre asset governance | 将套路内容拆并进对应题材模板，并删除 `genre-tropes.md` | 在 `0-Init` 固化 L1 只读 `templates/genres/README.md`，具体题材工法统一从共享根目录按需读取 | 全仓检索不再出现 `0-Init/references/genre-tropes.md` 与其活跃引用 |
| `0-Init/references/worldbuilding/` 继续承载跨阶段世界构建工法，和 `1-Cards` 对象层职责混线 | worldbuilding asset governance | 将人物/势力/力量体系/世界规则/一致性检查迁入 `templates/worldbuilding/` 并删除旧私有副本 | 在 `0-Init` 固化 worldbuilding 只从共享 `templates/worldbuilding/` 根目录按需读取 | 全仓检索不再出现活跃 `0-Init/references/worldbuilding/*.md` 引用 |
| `0-Init/references/creativity/` 仍以一组平级 leaf references 充当父技能与 mode-playbook 的直接入口，导致创意路由散点化 | reference routing governance | 将其升格并更名为 `references/creative-seed-routing/`，新增 `module-spec.md + CONTEXT.md`，父技能与 mode-playbook 只指向模块入口 | 在 `0-Init` 固化“创意相关引用必须先经 `creative-seed-routing` 路由”的统一合同，并把 leaf reference 映射收口在模块内 | 全仓检索不再出现活跃 `references/creativity/` 直连路径 |
| 模块已写三轴三重，但没有形成 `think-think` 优化模式要求的事实/推断、验证矩阵和正式报告 | thought-chain governance | 回到真实基线，按 `chain-optimization` 补齐思维链强化，而不是只加漂亮轴名 | 对所有宣称执行了 `think-think` 的模块，强制检查“显式矩阵 + reports 正式报告”双门禁 | 目标模块与 `reports/` 同时出现可追溯产物 |
| 误把 `scripts/data_modules/webnovel.py` 当作初始化入口直接执行 | script entrypoint contract | 改用 `.agents/skills/story/scripts/story.py init` 或 `init_project.py` 正式入口 | 把 `data_modules/webnovel.py` 视为内部转发层，`story.py` 视为唯一用户侧 CLI 入口，不再直接暴露 legacy 文件名 | 初始化命令不再触发 `ModuleNotFoundError: runtime_compat` |
| 新项目直到首个 drafting/review run 才出现任务状态文件 | initialization state contract | 在 `init_project.py` 同步初始化 `workflow_state.json / execution_state.json / task_log.jsonl` | 把“状态管理期初文件”写进 `0-Init` 成功标准，并用测试锁住初始化结果 | 新项目创建后即可被 `resume/status` 读取全阶段执行态 |
| 初始化已生成项目入口文件，但没有预留 `.webnovel/tasks/` 治理工件根目录 | governance artifact root | 在 `init_project.py` 同步创建 `.webnovel/tasks/`，并把路径登记到 `STATE.json` | 把“项目入口清单”和“任务工件根目录”一并纳入初始化骨架与测试，避免后续 tracked workflow 各自猜目录 | 新项目创建后无需额外补骨架即可承接 shadow governance task 链 |
| 新增 `STATE.json / TEAM.toml / CHANGELOG.md` 但未接入项目入口或初始化合同 | project entry governance | 在 `init_project.py` 统一生成三份标准配置，并让 `project_locator.py` 认 `STATE.json` 的路径声明 | 将“项目入口状态、团队治理模板、变更记录入口”收口进 `0-Init` 成功标准与测试，避免再次退化成只写不认的装饰文件 | 新项目初始化后，`STATE.json` 能解析运行态路径，`TEAM.toml / CHANGELOG.md` 成为正式交付物 |
| 智能顾问团仍只有单一 `advisor_agents`，无法表达 `策划 / 监制 / 评审` 三阶段布阵 | team governance contract | 将初始化元数据升级为 `team_setup`，支持 `same_lineup / per_stage / legacy_planning_only` 三种布阵模式 | 在 `SKILL.md`、`advisor-council-mode/module-spec.md`、`init_project.py`、`TEAM.toml` 模板和测试中同步固化三阶段 team schema，并保留 `advisor_agents` 兼容镜像 | 初始化后 `TEAM.toml` 能正确区分三阶段成员，旧调用仍不会断裂 |
| `0-Init` 一边产出设定 Markdown，一边又宣称 `1-Cards` 是唯一上游，形成双真源错觉 | stage handoff contract | 固化 `Init/初始化简报.json + 访谈摘要.md + 确认卡.md` 为正式 handoff | 把历史 `Init/*.md` 明确降级为 seed / legacy-compat，并禁止后续持续维护 | `1-Cards` 可以不依赖散落 seed 文档完成首次建卡 |
| 初始化新增多模式后只改问卷文案，未把模式元信息写入 handoff/state | handoff metadata contract | 在 `init_project.py` 与 `0-Init` 合同中加入 `init_mode / advisor_agents / research_policy` | 让 `初始化简报.json`、`state.json`、`task_log` 同步记录本次初始化来源策略 | 初始化完成后可追溯这本书是顾问团、快速还是自主模式起盘 |
| 顾问团模式只点名 agents，却没有真实并发调度和意见汇总层 | advisor council orchestration | 明确“一顾问一 subagent”并要求输出共识/分歧/建议采用方案 | 在 `0-Init/SKILL.md` 固化顾问团调度合同与降级路径 | 每轮问卷都能看到顾问团的结构化纪要，而不是一句泛泛“综合建议” |
| `0-Init` 仍沿用固定 A-D 大问卷，和重构后的 truth layering 不匹配 | init scope contract | 将初始化改写为 `project_contract + cards_seed + planning_seed + unknowns` 四段式 | 在 `0-Init` 中固定 truth owner 判定：属于对象的交给 Cards，属于编排的交给 Planning，剩余进入 unknowns | 初始化不再越权替 `1-Cards / 2-Planning` 提前拍死细节 |
| 初始化元选项在多个章节重复出现，执行者容易在不同位置读到不同入口定义 | mode entry contract | 将三种模式的元选项卡、A/B/C 规则与模式选择表收口到 `Initialization Mode Contract` 单一入口 | 其他章节只允许引用该入口，不得再次枚举元选项；全文检索 `初始化元选项卡/模式选择卡` 应只保留一个正式展示位 | 执行者不会再把 Quick Reference、流程段落或附录误认成第二入口 |
| 选择智能顾问团或快速模式后仍被拖回问卷链，导致“换皮问卷” | mode execution routing | 为 `智能顾问团模式 / 快速模式` 固化 `Step 0.6` 一次性内部任务路径，并让 `自主模式` 独占 Questionnaire 合同 | 将模式执行细则模块化到 `references/{advisor-council-mode,fast-mode,autonomous-mode}/module-spec.md`，且模式锁定后只加载一份对应模块 | 顾问团/快速模式初始化时不再进入 Step 1-4 问卷轮次 |
| 合同声称会写 `.webnovel/idea_bank.json`，但实现未实际落盘 | init artifact drift | 在 `init_project.py` 中补写 `idea_bank.json` 并写入初始化约束 | 用测试锁住 `selected_idea / constraints_inherited / init_session` 的落盘结果 | 初始化产物清单与脚本实现重新对齐 |
| `0-Init` 合同升级后，脚本 stdout 与测试入口仍保留旧式默认认知 | init/script/test drift | 将 `init_project.py` 的终端输出分成 primary 与 optional seed/legacy-compat 两组，并在 tests 加统一 `conftest.py` 注入 scripts 路径 | 每次升级 `0-Init` 合同时，同时审计 CLI 输出、测试入口与全量 pytest 执行路径，而不是只看 handoff JSON | 从仓库根执行 `pytest .agents/skills/story/scripts/data_modules/tests` 可完成收集并进入真实断言阶段 |
| CLI 测试 fixture 只建目录不建 `.webnovel/state.json`，与严格 `project_root` 契约冲突 | project locator / test fixture drift | 统一用测试基座补写最小 `state.json`，让 `--project-root` 真正满足 `resolve_project_root()` 的合法条件 | 任何 CLI 测试若显式传 `--project-root`，都必须通过共享 helper 构造合法项目根，而不是各测例手搓半成品目录 | 全量 pytest 不再因 `Not a webnovel project root` 这类 fixture 失配而成片失败 |
| 初始化合同已经要求 legacy `总纲.md` 带初始化快照，但脚本生成的骨架缺字段或标签名漂移 | init artifact drift | 同步修正 `_build_master_outline()` 与快照注入逻辑 | 把 legacy 总纲快照纳入正式 contract regression test | 初始化后 `Planning/legacy/总纲.md` 与 handoff 合同字段保持一致 |
| 用户已要求移除的 Init seed brief 仍在新初始化里继续落盘 | init artifact contract drift | 删除 `init_project.py` 中旧 seed brief 生成逻辑，并把测试改成断言这些文件不存在 | 以后升级 `0-Init` 时，凡正式交付清单未列出的 Init 文件，一律在脚本与测试双层禁止默认生成 | 新项目 `Init/` 只保留初始化简报、访谈摘要、确认卡与 README |
| `north_star_contract` 已设计却没成为真正主入口，导致初始化简报继续背整套正文 | init primary-artifact drift | 把 `Init/north_star_contract.json` 变成实际落盘主文件，`初始化简报.json` 只保留 `north_star_ref + cards_seed + planning_seed + unknowns` | 以后调整 init handoff 时，必须同时审计脚本写入路径、测试断言、`0-Init/1-Cards/2-Planning/3-Drafting` 契约 | 新项目 `Init/` 出现 north star 主文件，Markdown 只剩导航与边界 |
| 用户级 registry 与全局 `.env` 仍停留在 `~/.claude/webnovel-writer/`，而用户层命令已切到 `story-*` | shared script compatibility layer | 改成 `~/.claude/story2026/` 新路径优先读写，旧路径双读兼容并自动迁移 | 在 `project_locator.py` 与 `data_modules/config.py` 固化“新路径优先、旧路径兼容、命中旧路径即 best-effort 迁移”的共享策略，并用测试锁住 | 旧用户目录不丢配置，新目录能自动接管后续写入 |

## Reusable Heuristics

- 初始化阶段先保证路径、脚本入口和模板入口都在本仓库内闭合，再继续扩展交互深度。
- 对 Codex 来说，问卷式初始化最稳的做法不是“一问一答”，而是“每轮 4-8 题 + 助手负责结构化回填”。
- 用户一旦给出自由叙述，优先做信息归并和缺口标记，而不是要求对方重填整份表。
- 如果用户希望更“高级”的交互感，应升级成结构化问卷卡：每题带选项、示例和自由填写位，而不是退回一问一答。
- 初始化真正的下游不是“停在 Markdown 总结”，而是把结构化访谈结果交给 `1-Cards` 做整书卡片建模。
- 初始化如果还保留 `Init/*.md`，必须显式标注它们只是 seed / legacy-compat；真正的 handoff 应收束到一份固定简报。
- 初始化阶段最多只产出 legacy 兼容骨架，不产出规划真源；正式规划入口必须留给 `2-Planning` 收敛出的 `Planning/8-全息地图.json`。
- 题材资产允许“入口模板 + 细粒度分片”两层形态，但必须共存于 `templates/genres/` 一个根目录下，不能再拆成第二套平行路径。
- 如果某份题材知识同时服务初始化与规划，就应优先提升到 `templates/genres/`，不要在 stage 私有 `references/` 之间横向调拨。
- 如果某份人物/势力/力量/规则知识同时服务初始化与对象建卡，就应优先提升到 `templates/worldbuilding/`，不要继续挂在 `0-Init` 私有目录。
- 如果一组创意资料会被多个 mode-playbook 共享消费，就不该让各 mode 模块散点点名 leaf docs，而应先升格成 `references/<module-name>/module-spec.md + CONTEXT.md` 统一路由。
- 当用户提供旧项目的 `preset`、`1-设定` 卡和 `2-规划` 包时，初始化最稳的做法不是整包照搬，而是提炼“故事核 + 风格锚点 + 角色压力结构”后写回当前项目真源。
- `data_modules/webnovel.py` 适合被其他入口转发，不适合直接当命令入口执行；初始化脚本优先使用 `scripts/story.py init`。
- 多模式初始化最稳的落地顺序是：先记 `mode`，再决定“谁来答、是否联网、谁来拍板”，随后先收 `project_contract`，再按 truth owner 决定补 `cards_seed` 还是 `planning_seed`。
- 初始化模式的元选项卡必须只有一个正式展示位；Quick Reference、执行流程和参考目录只能引用它，不能再复制一份 A/B/C 入口。
- 一旦锁定 `智能顾问团模式` 或 `快速模式`，就要立刻切到一次性内部任务模板；若仍继续问卷，说明执行器没有真正命中模式细则。
- 当某份模式 reference 已进入治理范围，最稳的落点不是继续停留在“中间层目录 + 单文档”结构里，而是直接升格成 `references/<mode-name>/module-spec.md + CONTEXT.md` 独立子模块。
- 三种初始化模式完成目录级模块化后，还要继续把 `共享依赖边界 + 正式写回位点 + 子模块级验证门禁` 写进各自 `module-spec.md`；否则它们只是“搬了目录”，还不算真正可独立消费的 mode-playbook。
- 对 `0-Init` 这类 governed module，`think-think` 执行完成的最低证据是：目标模块内看得到优化模式矩阵，且同目录 `reports/` 下有正式思维链设计报告；两者缺一，都只能算“参考了方法”。
- 顾问团模式的价值不在“更像在演戏”，而在把不同 agent 的稳定立场转成策划会意见；因此必须保留共识与分歧，而不是只给一个混合结论。
- 快速模式可以大幅减少用户输入，但前提是把推断项写明，否则后续 `1-Cards` 会误把助手脑补当成用户承诺。
- 当前结构下，初始化最重要的不是“问得多”，而是“路由对”：哪些东西现在就该定，哪些东西应该明确留给 `1-Cards / 2-Planning` 收敛。
- 如果 `1-Cards` 子技能开始把 `planning_seed` 当对象真源读，说明 handoff slice 还没写清；应回修每张子卡的输入优先级，而不是继续扩大初始化问卷。
- 当初始化已经拆出 `north_star_contract` 时，`初始化简报.json` 应立刻降为伴生 handoff；否则第二入口会重新膨胀成主文件。
- 当用户不想再保留“全局卡/全局总览”这个中间层时，最稳的落点不是再造新卡，而是把长期对象总规范直接并入 `north_star_contract.json.cards`。
- 涉及用户级路径升级时，最稳的策略不是一次性硬切，而是“新路径优先 + 旧路径兼容读取 + 命中旧路径即迁移到新路径”。
- 新项目若还没有任何具体 run，也应先创建 `.webnovel/tasks/` 根目录；“先有任务工件根，再有 run 目录”比让每个下游命令各自补目录更稳。

