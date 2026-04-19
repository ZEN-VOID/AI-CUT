# CONTEXT.md

## Context Health
<!-- CONTEXT_HEALTH_START -->
```yaml
monitor_version: 1
soft_limit_chars: 40000
hard_limit_chars: 80000
soft_limit_cases: 80
hard_limit_cases: 140
current_chars: 2919
current_lines: 67
current_cases: 0
status: ok
recommended_action: none
last_checked_at: 2026-04-08T00:00:00Z
```
<!-- CONTEXT_HEALTH_END -->

## Type Map

| failure_or_outcome_type | root_cause_layer | immediate_fix | systemic_prevention | verification_point |
| --- | --- | --- | --- | --- |
| 根目录缺少总 `SKILL.md` / `CONTEXT.md`，导致执行者只能看到分阶段 skill | root source contract | 在 `.agents/skills/story/` 补齐根级入口与根级经验层 | 把跨阶段拓扑、总路由、共享 carrier 边界固定在根级真源，不再散落到各阶段自己解释 | 泛化 `story2026` 请求能先命中根入口，再转到唯一阶段 |
| 跨阶段共享 reference 被误下沉到某一阶段，后续产生第二真源 | canonical source governance | 回到根级 `_shared/` 与对应阶段 `_shared/` 重新确认共享归属 | 跨阶段共享合同只放根级 `_shared/`，阶段共享合同只放 owning stage `_shared/`，不再恢复历史根级 `references/` | 同一份 schema/contract 不再被多个阶段各自改写 |
| 用户问题同时触发多个阶段，执行者直接跳到“看起来最像”的下游阶段 | routing contract | 先判 truth role，再按总路由表选择最早 owner | 在根级 `SKILL.md` 固化 route matrix 与 owner 表 | 问题能稳定落到唯一默认入口 |
| 共享 helper 被多个阶段复制维护，导致路径或状态规则漂移 | shared script layer | 把共用 helper 收束到根级 `scripts/` | 对 2+ 阶段共用的路径/状态/CLI 逻辑，统一提升为共享入口 | 脚本调用路径与运行态规则只需修一处 |
| 根级 skill 变成“阶段细则合集”，反而制造第二层重复 | scope discipline | 收缩根级 skill，只保留总线职责 | 阶段细节留在各阶段 `SKILL.md`，根级只保留拓扑和边界 | 根级文件可快速说明系统，不需要复制阶段合同 |
| `story2026` 用户命令已切到 `/story-*`，但 skill frontmatter、workflow registry、模板 metadata 仍残留 `webnovel-*` / `story2026-*`，导致命名双真源 | canonical naming governance | 先对齐 `scripts/workflow_manager.py` 的 canonical alias，再同步改写 skill/frontmatter、模板与命令文档 | 将命名迁移固定为“workflow alias -> 文档/技能 -> 状态/测试”的单一升级顺序，旧名只留 alias 层 | 用户侧、状态层与模板层都只写 canonical `story-*`，旧名仅能被兼容读取 |
| workflow runtime 已改为内联写入 `STATE.json`，但根/阶段合同仍沿用 `.webnovel/tasks` 与旧独立状态文件口径 | governance artifact governance | 在根级与关键阶段 skill 中显式改成 `STATE.json.workflow_runtime` | 把 runtime artifact chain 固化成跨阶段共享证据层，并要求命令文档、阶段技能、CONTEXT 同步承认 | 运行脚本、技能合同、命令文档对执行态口径一致 |
| `3-Drafting` 已切换到 `projects/story/<项目名>/3-Drafting/第N集.md` 单根文件模式，但共享文档与 helper 还在讲 `Drafting/chNNNN/chapter-root.md` | drafting runtime governance | 把根 skill、query data-flow、path helper、旧 shared 合同统一切回新路径 | 将 `3-Drafting/_shared/episode-root-contract.md` 固定为唯一 drafting runtime 真源，旧 `chapter-root` 降级为迁移回指 | 相关文档与 helper 不再并行描述两套 drafting 路径 |
| 项目 runtime 仍把阶段目录写成无序号 `Cards / Planning / Validation / Loopback`，而 stage owner 已按 `1/2/4/5-*` 编排 | canonical runtime naming | 统一把项目级阶段目录收口为 `1-Cards / 2-Planning / 4-Validation / 5-Loopback`，并同步脚本、tests、stage contracts 与示例树 | 以后凡 stage 命名迁移，必须执行“root contract -> stage contract -> shared script -> tests/fixtures -> init skeleton”五层同步 | 新项目目录、脚本 relpath、stage 文档与回归测试对阶段命名保持一致 |
| 阶段 `SKILL.md` 已完成 0-5 重构，但 `workflow_manager` 步骤注册和统一 CLI 仍保留旧模式/旧脚本/旧对象名 | shared script registry drift | 先改 `scripts/workflow_manager.py` 与 `scripts/data_modules/webnovel.py`，再清理失效脚本与文档回指 | 每次阶段重构后都执行“skill contracts -> workflow registry -> CLI forwarding -> docs/tests”四层 parity 审计 | `resume`/workflow runtime 展示的步骤与最新阶段合同一致，仓内不再暴露 ghost scripts |
| 题材资料文件被当成通用基座必读，导致“类型化增强”误升格为“系统硬依赖” | base-vs-typed layering | 将 `genre-profiles.md`、`reading-power-taxonomy.md` 从根/阶段合同的必读列表中降级为可选增强材料 | 统一要求：通用基座只依赖共性合同，类型化知识只在启用 `type-pack` 时投影到相关阶段 | 缺少题材资料时，context pack 仍能正常生成，且阶段合同不再把类型化素材误写成必读 |
| 追读力 taxonomy 只有几条压缩摘要，Step 6、context builder、query 各自补充解释，形成隐性多真源 | shared reading-power taxonomy drift | 把完整 taxonomy 收束回根级 `_shared/reading-power-taxonomy.md`，兄弟阶段与脚本统一回读该文件 | 共享分类只放根级 `_shared/`，阶段子技能只写执行映射，不再各自复制 hook / payoff 词典 | Step 6、context builder、query / status 对钩子与爽点的叫法保持一致 |
| `cool-points-guide` 只剩 review 下的失效 deprecated 跳转，爽点工程知识没有 active 共享真源 | shared guide carrier missing | 在根级 `_shared/` 建立 `cool-points-guide.md`，并让 Step 6 / review redirect 都改指向它 | 固定“分类真源”和“工程 guide 真源”双载体边界：taxonomy 讲定义，guide 讲编排 | 兄弟模块不再引用一个不存在的 shared guide 路径 |
| `type-packs` 目录被重构为 `网文/<题材目录或family目录>/`，但合同和 loader 仍按旧平铺配置结构读取 | type-pack source contract drift | 先把 `_shared/type-pack-loading-contract.md`、根 `SKILL.md` 与扩维指南切到新目录真源，再让 loader 至少兼容当前目录形态 | 固定“目录知识真源 > 旧平铺配置假设”的优先级，任何结构迁移都要同步改合同与读取逻辑 | 文档、shared contract 与 loader 不再继续引用已废弃的平铺 contract 文件 |
| `1-题材选型` 锁题材时没有显式承认 `type-packs/网文/<题材>` 的默认入口关系，后续容易出现“题材已定，但知识入口仍靠人工猜” | planning-to-typepack routing drift | 在 `1-题材选型` 子技能、模板和 loading contract 中写死“题材同名目录默认命中” | 固定“题材名同名目录默认入口，family 按设定补读”的规则，避免后续再回到隐式人工猜目录 | 题材选型 artifact 能明确给出 `selected_type_refs / family_refs` |
| legacy 覆盖审计把 `.agents/skills/story_backup/...` 与 `story_backup/...` 直接比对，导致 72/72 假缺失 | path normalization in absorption audit | 在覆盖测试中先把 legacy 路径统一归一化到 `story_backup/...` 相对层再比较 | 以后凡是做技能根相对路径审计，都先锁定统一相对基准，避免 `.agents/skills/` 前缀差异制造假失败 | 覆盖测试返回真实 missing 列表，而不是全量假告警 |
| `type-pack` 已可加载，但 drafting 七工序仍共享同一套提示，导致 step hook 没有真正进入执行层 | step-specific projection gap | 把 `current_step_id` 透传到 context / extract / validation，并让 runtime 从 `drafting.step_hooks.Step X` 读取当前工序规则 | 固定“step hook 只在 pack 真源定义，runtime 统一按 `current_step_id` 消费”的链路，禁止 7 个 drafting 子技能各抄一份类型表 | `Step 2 / Step 5 / Step 7` 能收到不同 type-pack checklist 与 fail signal |
| 类型兑现只是结构兑现的附注，导致返工入口在“剧情没写成”和“题材没写像”之间漂移 | validation dimension boundary | 在 `4-Validation` 增加独立 `type-pack-fit-validator` 维度，并把 registry / runner / child skill 同轮接上 | pack.validation、registry、runner 与子技能共同承认“类型兑现”是独立维度，不再静默并入 `structure-validator` | aggregate JSON 与 sidecar 可单独追踪 type-pack fit 问题与返工节点 |
| `type-pack` 目录知识、alias pack、stage projection 分散在 consumer 硬编码里，导致同一 pack 在 resolver / planning / validation / cards 中语义不一致 | canonical pack semantics drift | 抽 `type-packs/pack-catalog.yaml` 为系统级 pack 真源，让 resolver 与各 consumer 共读 | pack 语义、别名、阶段投影、cards bias 都先落 catalog，再允许 consumer 消费 | pack 新增或别名迁移时，主要只需改 catalog 与少量 consumer tests |

## Repair Playbook

1. 先判断问题是“缺总入口”“路由错”“真源错认”“共享 carrier 误放置”中的哪一种。
2. 若问题跨两个以上阶段，先回根级 `story/SKILL.md` 做总线诊断，再进入阶段修复。
3. 若同一规则在多个阶段重复出现，优先找根级 canonical source，而不是逐个阶段补丁。
4. 若共享脚本或共享 reference 失配，先修共享层，再让阶段合同回指共享层。
5. 收尾验证固定检查：
   - 根级 `SKILL.md` 是否能解释主链与卫星关系
   - 根级 `CONTEXT.md` 是否记录跨阶段经验
   - 根级 `_shared/` 与阶段 `_shared/` 是否仍保持单一共享真源
   - `type-packs/` 是否能解释 active stack、resolver 与 stage projection
   - 泛化请求是否能稳定路由到唯一 owner

## Reusable Heuristics

- 根级 skill 最有价值的工作不是“替阶段再说一遍”，而是回答“该去哪一层、该信哪一层、哪些共享层先读”。
- 当一个体系已经有多个成熟阶段 skill 时，缺的往往不是更多子技能，而是一个总线级 canonical source。
- 跨阶段共享文档如果不能一句话说明“被哪些阶段共同消费”，就不该放在根级 `references/`。
- 遇到泛化 `story2026` 请求，先判 truth role，再判 stage，通常比先看动词更稳。
- 主链阶段默认串行，卫星技能默认侧挂；不要把 `query / resume` 写成新的主流程阶段，也不要让仅剩用户层入口的辅助命令伪装成正式卫星技能。
- 当用户命令、skill id、workflow command、模板 metadata 同时出现改名需求时，不要逐层碰运气替换；先建立一份根级命名合同，再让其他载体回指这份真源。
- 若某个命令只剩用户命令层入口、已不再对应 tracked workflow 或正式 skill，必须在命名合同与根级路由合同里显式标成“auxiliary command”，不要让它继续挂在卫星技能表里伪装成正式阶段。
- 当共享脚本已把治理工件内联到 `STATE.json.workflow_runtime`，而阶段合同还没承认这些对象时，优先补根 skill 与命令文档，再补关键阶段 skill，避免脚本能力再次沦为隐形层。
- 当某阶段的 canonical runtime 已从“技术根文件”升级到“业务根文件”后，shared docs 与 path helper 必须同轮同步，不然旧路径会很快长成第二真源。
- 当 canonical runtime 路径发生迁移时，除了主合同和脚本，还要同轮更新示例字符串、fixture、CLI 转发测试与目录树文档；这些“看起来只是例子”的载体最容易把旧路径重新固化成默认认知。
- 当阶段合同把旧脚本降级出正式流程后，不要只删文件本体；必须同步清掉 CLI 转发、workflow registry、调用矩阵和测试，否则 ghost entry 会继续制造“看似可用”的第二真源。
- 类型化知识默认属于增强层，不属于基座层；只有在项目显式启用 `type-pack` 后，才应把这些知识投影到 planning/drafting/validation。
- 最稳的类型化方案不是给每个题材重写一套 workflow，而是维持固定方法核，把题材/平台/受众差异压缩进可组合 `type-pack`。
- `type-packs` 若从旧平铺配置体系重构到目录知识体系，不能只改目录；根 `SKILL.md`、共享 loading contract、扩维指南和 loader 兼容层必须同轮同步，否则会出现“文档说旧结构、目录却是新结构”的双真源漂移。
- 若 pack 已定义 `drafting.step_hooks`，runtime 就必须同时拿到 `current_step_id`；否则只是把规则写进了真源，却没有真正变成执行约束。
- 类型兑现应当独立成 validator 维度，而不是继续借住在结构兑现里；否则最终只会得到一个模糊低分，拿不到稳定返工入口。
- 当共享 taxonomy 已经存在于根级 `_shared/` 时，阶段技能应该消费它，而不是在本地重复定义另一套分类解释；阶段只保留“怎么用”，共享层才保留“是什么”。
- 当一个 reference 更像“工程方法手册”而不是“定义字典”时，应单独成为 shared guide，而不是硬塞进 taxonomy；否则定义层和编排层会重新缠在一起。
- 当根级 `_shared/` 中某组前端资产已经形成“模板 + 样式 + 脚本”的稳定组件时，应收进独立子目录，而不是继续在 `_shared/` 根层平铺多个同名前缀文件。
- `type-packs` 若已重构为 `网文/<题材目录或family目录>/`，至少要保证三件事同时成立：`_shared/type-pack-loading-contract.md` 已更新、`infer_type_stack/init_project` 不再硬指向旧 `resolver.md`、`resolve()` 至少能回收当前目录下的 `knowledge_refs`；缺任一项都说明重构还停在目录层。
- 当题材命名已经与 `type-packs/网文/<题材>/` 对齐时，默认入口不该再靠人工临场猜；除非特别说明，`1-题材选型` 就应该先命中同名目录，再决定补读哪些 family。
- 做 legacy 覆盖审计时，路径比较必须先统一到同一相对根；`.agents/skills/story_backup/...` 和 `story_backup/...` 语义相同，但若不先归一化，测试会制造全量假告警。
- 当 pack 既有目录知识又有跨阶段执行语义时，目录只负责“写什么”，catalog 负责“系统怎么用”；不要再让 validation/cards/planning 各自维护另一套 pack 名判断。
