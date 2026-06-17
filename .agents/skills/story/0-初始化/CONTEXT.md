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
| “初始化小说”误入 AIGC 影片初始化，或“初始化影片/电影”被 story 初始化截走 | 媒介语义路由层 | 在 `story-init` 入口、registry routes 与 product metadata 中显式写入 novel/book/story 正向触发和 film/movie/video 负向排除 | 把自然语义触发词分成两组：`小说/网文/书/长篇故事 -> .agents/skills/story/0-初始化`，`影片/电影/影视/视频 -> .agents/skills/aigc/0-初始化` | 输入“初始化小说/网文”只落 `projects/story/<项目名>/`；输入“初始化电影/影片”只落 `projects/aigc/<项目名>/` |
| 初始化技能路径仍指向旧插件目录 | skill contract | 改为 repo-local `story2026` 路径约定 | 在技能文档内固定 `REPO_ROOT/.agents/skills/story` | 预检命令可解析 `SCRIPTS_DIR` |
| 初始化仍沿用问卷调查或旧三模式入口 | mode contract | 把入口收口到单一 `team代入模式 -> 自动组队 / 自定义组队` | 在 `0-初始化/SKILL.md` 删除问卷/快速/顾问团平行模式，只保留 `team_lineup_mode` 分支 | 全文与脚本不再出现 active `快速模式 / 自主模式 / 顾问团模式` 执行真源 |
| 初始化完成后没有稳定交给 Cards 层 | stage handoff contract | 在 `0-初始化` 明确写入 `Cards Handoff Contract` | 固化 `固定题包直答 -> north_star.cards -> 角色卡 -> 场景卡 -> 物品卡 -> 技能卡` 的顺序与加载边界 | `1-设定` 能只凭初始化简报顺序建卡 |
| 题材资料出现 `templates/genres` 与 `story2026/genres` 双根并存 | genre asset governance | 将旧分片并入 `templates/genres/details/` 并删除平行根目录 | 在 `0-初始化` 固化 `templates/genres/` 为唯一 canonical 根，并用 README 记录入口模板与 detail pack 映射 | 全仓检索不存在 `.agents/skills/story/genres` 活跃路径 |
| `0-初始化/references/` 仍残留题材套路私有副本，和共享题材模板职责重叠 | genre asset governance | 将套路内容拆并进对应题材模板，并删除 `genre-tropes.md` | 在 `0-初始化` 固化 L1 只读共享题材模板 README，具体题材工法统一从共享根目录按需读取 | 全仓检索不再出现 `0-初始化/references/genre-tropes.md` 与其活跃引用 |
| `0-初始化/references/worldbuilding/` 继续承载跨阶段世界构建工法，和 `1-设定` 对象层职责混线 | worldbuilding asset governance | 将人物/势力/力量体系/世界规则/一致性检查迁入 `templates/worldbuilding/` 并删除旧私有副本 | 在 `0-初始化` 固化 worldbuilding 只从共享 `templates/worldbuilding/` 根目录按需读取 | 全仓检索不再出现活跃 `0-初始化/references/worldbuilding/*.md` 引用 |
| `0-初始化/references/creativity/` 仍以一组平级 leaf references 充当父技能的直接入口，导致创意路由散点化 | reference routing governance | 将其升格并更名为 `references/creative-seed-routing/`，新增 `module-spec.md + CONTEXT.md`，父技能只指向模块入口 | 在 `0-初始化` 固化“创意相关引用必须先经 `creative-seed-routing` 路由”的统一合同，并把 leaf reference 映射收口在模块内 | 全仓检索不再出现活跃 `references/creativity/` 直连路径 |
| 模块已写三轴三重，但没有形成 `think-think` 优化模式要求的事实/推断、验证矩阵和正式报告 | thought-chain governance | 回到真实基线，按 `chain-optimization` 补齐思维链强化，而不是只加漂亮轴名 | 对所有宣称执行了 `think-think` 的模块，强制检查“显式矩阵 + reports 正式报告”双门禁 | 目标模块与 `reports/` 同时出现可追溯产物 |
| 误把 legacy webnovel data module 当作初始化入口直接执行 | script entrypoint contract | 改用 `.agents/skills/story/scripts/story.py init` 或 `init_project.py` 正式入口 | 把 legacy data module 视为内部转发层，`story.py` 视为唯一用户侧 CLI 入口，不再直接暴露旧文件名 | 初始化命令不再触发 `ModuleNotFoundError: runtime_compat` |
| 新项目直到首个 drafting/review run 才出现执行态对象 | initialization state contract | 在 `init_project.py` 同步初始化 `STATE.json.workflow_runtime` | 把“状态管理期初对象”写进 `0-初始化` 成功标准，并用测试锁住初始化结果 | 新项目创建后即可被 `resume/status` 读取全阶段执行态 |
| workflow runtime 已内联到 `STATE.json`，但初始化合同仍提 `.webnovel/tasks/` | governance artifact root | 删除 `.webnovel/tasks/` 初始化逻辑与相关文档口径 | 把执行态证据链统一收口到 `STATE.json.workflow_runtime`，避免再长出第二套任务目录真源 | 新项目初始化后不再生成 `.webnovel/tasks/` |
| 新增 `STATE.json / team.yaml / CHANGELOG.md` 但未接入项目入口或初始化合同 | project entry governance | 在 `init_project.py` 统一生成 `STATE.json + team.yaml + CHANGELOG.md` | 将“项目入口状态、团队治理真源与变更记录入口”收口进 `0-初始化` 成功标准与测试 | 新项目初始化后，`STATE.json` 能直接承载运行态，`team.yaml` 成为唯一 team 真源 |
| `team.yaml` 被并行镜像或 fallback 路径稀释 | team governance contract | 将初始化元数据统一写入 `team.yaml` 单文件 | 在 `SKILL.md`、`init_project.py`、测试与下游 stage 合同中同步固化“只读 team.yaml” | 初始化后 `team.yaml` 能表达 `init_mode / team_lineup_mode / selector_scope_root / roles.*` |
| 初始化阶段被错误压缩成单主文件，导致故事源登记与阶段 handoff 丢边界 | stage handoff contract | 固化五件套：`team.yaml + STATE.json + 0-初始化/north_star.yaml + story-source-manifest.yaml + init_handoff.yaml` | 在 `0-初始化`、下游 stage 合同、脚本和测试中同时固定五文件分工 | `1-设定 / 2-卷章 / resume` 读取边界一致，不再互相挤占 |
| 初始化元信息未同步写入 `STATE.json / north_star.yaml / init_handoff.yaml / team.yaml` | handoff metadata contract | 在 `init_project.py` 与 `0-初始化` 合同中同步写入 `init_mode / team_lineup_mode / selector_scope_root / advisor_agents(legacy)` | 让 `north_star.yaml`、`init_handoff.yaml`、`STATE.json` 与 `team.yaml` 共用同一份初始化 provenance | 初始化完成后可追溯这本书是 `team代入模式` 下的 `auto/custom` 哪条子路径起盘 |
| `decision_owner=assistant` 时，`init_handoff.sources_breakdown` 仍把大量代填字段默认记成 `user_confirmed` | provenance attribution contract | 将 `init_project.py` 的默认归桶改为依据 `decision_owner` 选择 `assistant_inferred` 或 `user_confirmed`，并让内部 `confirmation` 明细跟随 `sources_breakdown` 分层 | 以后只要 assistant 代填初始化字段，未显式声明来源的剩余非空字段就默认落 `assistant_inferred`，不再污染 `user_confirmed` provenance | assistant 主导初始化时，`project.title` 等少数显式用户字段仍留在 `user_confirmed`，其余种子字段进入 `assistant_inferred` |
| `planning` 顾问团未成为初始化 kickoff owner | planning 固定题包直答 topology | 明确 `roles.planning.members` 必须先执行固定题包直答，再允许综合 `north_star` | 在 `0-初始化/SKILL.md` 固化 `team -> planning 固定题包直答 -> synthesis` 顺序 | 初始化不会再先写 handoff 再补直答说明 |
| 初始化元选项在多个章节重复出现，执行者容易在不同位置读到不同入口定义 | mode entry contract | 将入口收口到单一 `team代入模式 + 自动/自定义组队` 元选项卡 | 其他章节只允许引用该入口，不得再次枚举模式分支 | 全文检索只保留一个正式展示位 |
| `0-初始化` 合同升级后，脚本 stdout 与测试入口仍保留旧式默认认知，甚至把未生成的 `2-卷章/全息地图.json` 列成 primary file | init/script/test drift | 将 `init_project.py` 的终端输出限制为真实已生成文件，并显式提示 `2-卷章/全息地图.json` 应由 `/story-plan` 生成；同时在 tests 固化 stdout 断言 | 每次升级 `0-初始化` 合同时，同时审计 CLI 输出、测试入口与全量 pytest 执行路径，而不是只看 handoff JSON | 从仓库根执行 `pytest .agents/skills/story/scripts/data_modules/tests/test_init_project.py` 可验证 stdout 与真实落盘保持一致 |
| CLI 测试 fixture 只建目录不建 `STATE.json`，与严格 `project_root` 契约冲突 | project locator / test fixture drift | 统一用测试基座补写最小 `STATE.json`，让 `--project-root` 真正满足 `resolve_project_root()` 的合法条件 | 任何 CLI 测试若显式传 `--project-root`，都必须通过共享 helper 构造合法项目根，而不是各测例手搓半成品目录 | 全量 pytest 不再因 `Not a webnovel project root` 这类 fixture 失配而成片失败 |
| 用户已明确新项目不需要 `2-卷章/legacy/`，但初始化脚本仍默认生成 `总纲.md / 爽点规划.md` | init artifact scope drift | 从 `init_project.py` 移除 legacy planning 骨架默认生成，并把 stdout/test 断言切到阶段目录骨架 | 以后凡初始化交付清单未列出的 planning sidecar，一律不得默认落盘；legacy 只允许由旧项目迁移或显式补建产生 | 新项目初始化后不存在 `2-卷章/legacy/` |
| 用户级口径已改成五件套，但脚本或文档仍继续落旧 Init companion 文件 | init artifact contract drift | 删除旧 `Init/*` JSON/MD 默认落盘，并把测试改成断言五件套路径 | 以后升级 `0-初始化` 时，凡正式交付清单未列出的 Init 文件，一律在脚本与测试双层禁止默认生成 | 新项目只保留 `0-初始化/*.yaml` 三件套 |
| 初始化信息重新被压回“north_star 单主文件”，导致五件套边界失效 | init primary-artifact drift | 把长期约束、故事源登记、阶段入口种子重新分回 `north_star.yaml / story-source-manifest.yaml / init_handoff.yaml` | 以后调整 init handoff 时，必须同时审计脚本写入路径、测试断言、`0-初始化/1-设定/2-卷章/3-初稿` 契约 | 新项目五件套边界稳定，不再回退到单文件大杂烩 |
| 重跑初始化后 `STATE.json / north_star.yaml / init_handoff.yaml` 已更新，但 `team.yaml` 仍停在旧 skeleton | team manifest reinit drift | 将 `team.yaml` 从 `_write_text_if_missing(...)` 改为覆盖写入，并补一条 re-init 回归测试 | 以后凡初始化真源支持重跑，都必须把 `team.yaml` 纳入同一覆盖写回批次，避免项目级唯一 team 真源滞后于其余工件 | 对同一项目连跑两次初始化后，`team.yaml` 中的 `team_lineup_mode / roles.*.members / decision_owner` 与 `STATE.json`、`init_handoff.yaml` 保持一致 |
| 初始化项目骨架仍停留在旧 runtime：生成 `Drafting/`、`正文/`、无序号阶段目录、`.env.example`、`.webnovel`，还顺手建项目内 `.git` | runtime skeleton contract | 按根 `story/SKILL.md` 的 canonical runtime root 改写 `init_project.py`，只预建 `0-初始化 / 1-设定 / 2-卷章 / 3-初稿 / 4-润色 / review / context-return` 与当前对象卡子树，并补回归测试 | 以后凡阶段路径或 cards 子树发生 canonical 迁移，必须同步审计 `init_project.py` 的 `directories` 骨架、默认 sidecar 与“自动 git 初始化”副作用，防止新项目继续落旧版结构 | 新项目初始化后不再出现 `Drafting/`、`正文/`、`1-设定/其他设定/`、`.env.example`、`.webnovel/`、项目内 `.git/`，且存在 `1-设定/2-角色卡/主要角色/`、`2-卷章/`、`4-润色/`、`review/` 与 `context-return/` |
| `1-设定 / 2-卷章 / 3-初稿 / 4-润色 / review / context-return` 已更新，但初始化目录骨架与 `STATE.json` 仍停在旧阶段快照 | init project-state sync contract | 在 `init_project.py` 同步预建 `源/` 与阶段根，卡片子目录由 `1-设定` 按实际调度创建 | 以后凡阶段树或 workflow runtime schema 演进，必须同时审计 `PROJECT_SKELETON_DIRS + STATE.json.paths + workflow_runtime.execution_state.stage_progress + re-init task_log` 四处，而不是只改目录或只改文档 | 新项目初始化后，目录骨架、`STATE.json.paths`、`workflow_runtime` 与当前阶段链一致；重初始化也会追加 `project_reinitialized` 事件 |
| 用户级 registry 与全局 `.env` 仍停留在 `~/.claude/webnovel-writer/`，而用户层命令已切到 `story-*` | shared script compatibility layer | 改成 `~/.claude/story2026/` 新路径优先读写，旧路径双读兼容并自动迁移 | 在 `project_locator.py` 与 `data_modules/config.py` 固化“新路径优先、旧路径兼容、命中旧路径即 best-effort 迁移”的共享策略，并用测试锁住 | 旧用户目录不丢配置，新目录能自动接管后续写入 |
| `SKILL.md` 看似有执行顺序，但节点真源下沉在 `steps/`，Skill 2.0 delivery validator 直接拒绝 | runtime-spine source drift | 将业务画像、节点表、Mermaid、失败回路、模块矩阵、汇流门和 review binding 回收进 `SKILL.md`，删除 unsupported `steps/` | 升级或修复本技能时优先跑当前 `skill-2.0` validator/smoke，禁止恢复 `steps/` 作为第二执行链 | `validate_skill_2_0.py --mode delivery` 与 `smoke_test_skill_2_0.py --mode delivery` 不再报 unsupported steps 或缺 runtime spine 标记 |

## Repair Playbook

1. 媒介路由混线时，先检查 `story-init` / `aigc-init` 的 frontmatter、`agents/openai.yaml` 与 `.codex/registry/routes.yaml`，再检查脚本入口。
2. 初始化模式漂移时，回到单一 `team代入模式 -> auto/custom`，不要用问卷或快速补全承接缺口。
3. `team.yaml` 与其他 team manifest 并存时，保留 `team.yaml` 为唯一真源，其他载体降级为 evidence 或删除活跃读取。
4. planning 固定题包直答缺失时，先修 `roles.planning.members` 与 subagent provenance，不用 synthesis 直接补空字段。
5. 项目骨架与 `STATE.json.paths` 不一致时，同时回修目录、paths、stage progress 与 task log。
6. 项目长期偏好写入项目根 `MEMORY.md`；技能复盘、失败模式和跨项目经验写回本 `CONTEXT.md` 或 `knowledge-base/`。
7. 旧路径、旧阶段名或旧 Init companion 文件回潮时，先跑全仓 `rg` 做引用同步，再修脚本和模板。
8. Skill 2.0 分区缺失时，先补 runtime spine、模块授权和动态引用，再运行当前 `skill-2.0` validator 与 smoke test。

## Reusable Heuristics

- 初始化阶段先保证路径、脚本入口和模板入口都在本仓库内闭合，再继续扩展交互深度。
- 用户一旦给出自由叙述，优先做信息归并和缺口标记，而不是要求对方重填整份表。
- 对当前 `0-初始化`，最稳的入口不是再造交互模式，而是固定 `team代入模式`，只让用户决定 `自动组队 / 自定义组队`。
- 初始化真正的下游不是“停在 Markdown 总结”，而是把结构化直答结果交给 `1-设定` 做整书卡片建模。
- 对当前 `0-初始化`，最稳的初始化骨架不是单一主文件，而是五件套：`team.yaml + STATE.json + north_star.yaml + story-source-manifest.yaml + init_handoff.yaml`。
- 初始化阶段最多只产出 legacy 兼容骨架，不产出规划真源；正式规划入口必须留给 `2-卷章` 收敛出的 `2-卷章/全息地图.json`。
- 题材资产允许“入口模板 + 细粒度分片”两层形态，但必须共存于 `templates/genres/` 一个根目录下，不能再拆成第二套平行路径。
- 如果某份题材知识同时服务初始化与规划，就应优先提升到 `templates/genres/`，不要在 stage 私有 `references/` 之间横向调拨。
- 如果某份人物/势力/力量/规则知识同时服务初始化与对象建卡，就应优先提升到 `templates/worldbuilding/`，不要继续挂在 `0-初始化` 私有目录。
- 如果一组创意资料会被父技能与 team 固定题包直答共享消费，就不该让多个入口散点点名 leaf docs，而应先升格成 `references/<module-name>/module-spec.md + CONTEXT.md` 统一路由。
- 当用户提供旧项目的 `preset`、`1-设定` 卡和 `2-卷章` 包时，初始化最稳的做法不是整包照搬，而是提炼“故事核 + 风格锚点 + 角色压力结构”后写回当前项目真源。
- `data_modules/webnovel.py` 适合被其他入口转发，不适合直接当命令入口执行；初始化脚本优先使用 `scripts/story.py init`。
- 单模式初始化最稳的落地顺序是：先锁 `team_lineup_mode`，再锁 `team.yaml`，随后先做 `planning 固定题包直答`，最后综合 `project_contract / cards_seed / planning_seed / unknowns`。
- 初始化元选项卡必须只有一个正式展示位；Quick Reference、执行流程和参考目录只能引用它，不能再复制第二入口。
- 对 `0-初始化` 这类 governed module，`think-think` 执行完成的最低证据是：目标模块内看得到优化模式矩阵，且同目录 `reports/` 下有正式思维链设计报告；两者缺一，都只能算“参考了方法”。
- team 代入模式的价值不在“顾问更像角色扮演”，而在把稳定立场转成 `planning 固定题包直答` 可吸收的 patch；因此必须保留来源分层，而不是只给一段混合结论。
- 当 `decision_owner=assistant` 且用户只明确给了少数字段时，初始化 provenance 的默认桶应切到 `assistant_inferred`；否则脚本只要收到了代填参数，就会把助手推断误记成用户确认。
- 当前结构下，初始化最重要的不是“问得多”，而是“路由对”：哪些东西现在就该定，哪些东西应该明确留给 `1-设定 / 2-卷章` 收敛。
- 如果 `1-设定` 子技能开始把 `planning_seed` 当对象真源读，说明 handoff slice 还没写清；应回修每张子卡的输入优先级，而不是继续扩大初始化问卷。
- 当用户不想再保留“全局卡/全局总览”这个中间层时，最稳的落点不是再造新卡，而是把长期对象总规范直接并入 `north_star.yaml.cards`。
- 涉及用户级路径升级时，最稳的策略不是一次性硬切，而是“新路径优先 + 旧路径兼容读取 + 命中旧路径即迁移到新路径”。
- 新项目若还没有任何具体 run，也应先创建 `STATE.json.workflow_runtime` 骨架；“先有内联执行态，再有具体 run”比让每个下游命令各自补状态更稳。
- 当阶段树已经升级而初始化还没跟上时，优先同步四件事：`源/ + stage roots`、`STATE.json.paths`、`workflow_runtime.execution_state.stage_progress`、`task_log` 的重初始化事件；缺一都会让下游脚本读到“目录存在但状态没跟上”或“状态更新了但目录没跟上”的半完成态。
- 对 runtime-spine Skill 2.0 包，节点真源必须在 `SKILL.md`；外部模块只能展开细则。若 validator 报 `steps/` unsupported，最小安全修复是先把节点、路由、gate 和 Mermaid 迁回主合同，再同步所有 active references。
