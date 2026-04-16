# CONTEXT.md

## Purpose & Loading Contract

- 本文件是 `aigc/3-Detail` 的经验层知识库，不是过程日志。
- 调用 `.agents/skills/aigc/3-Detail/SKILL.md` 时，应自动预加载本文件。
- 优先级遵循：用户显式请求 > `AGENTS.md` / 元规则 > `.agents/skills/aigc/SKILL.md` > 本 `SKILL.md` > 本 `CONTEXT.md`。

## Context Health

- soft_limit_chars: 22000
- hard_limit_chars: 44000
- status: ok
- last_checked_at: 2026-04-15

## Type Map

| failure_or_outcome_type | root_cause_layer | immediate_fix | systemic_prevention | verification_point |
| --- | --- | --- | --- | --- |
| `3-Detail` 仍沿用双次 markdown 扩写，导致 shared root 不收束 | 阶段总合同层 | 把父层切到 `JSON root + patch sidecar + parent merge` | 在父 `SKILL.md` 固化字段 ownership 与 sidecar merge 契约 | `剧本正文` 不再被二次重写 |
| `水月` 与 `镜花` 因目录序号被误判为关系不清 | 调度语义层 | 移除目录序号，并在父层显式写顺序门 | 把调度裁决固定到 `分镜切换 -> 水月 -> 镜花` | `3-Detail` 不再靠目录观感理解顺序 |
| `剧本正文` 在 detail 阶段被再次改写 | 真源边界层 | 回退到上游继承版本，只允许补字段 | 在父层与子层合同共同固定 `script_body_policy = inherit_only` | shared root 中 `剧本正文` 保持稳定 |
| `水月` 开始写 `分镜ID / 时间段 / 摄影美学` | 字段 ownership 层 | 回退到 factual patch，仅保留 `出场角色及穿搭 + beat factual fields` | 在 `director_episode_output.schema.json#/$defs/detail_patch_sidecar` 与 validator 中固化 owner 边界 | `水月` sidecar 无 cinematic 字段 |
| `镜花` 开始写 `出场角色及穿搭` 或 factual 字段 | 字段 ownership 层 | 回退到 cinematic patch，仅保留 shot skeleton 与导演/摄影字段 | 在 `director_episode_output.schema.json#/$defs/detail_patch_sidecar` 与 validator 中固化 owner 边界 | `镜花` sidecar 无 group/factual 字段 |
| sidecar 结构同时在两个 schema 文件维护，导致契约漂移 | canonical schema 治理层 | 将 sidecar 定义收束进 `director_episode_output.schema.json::$defs`，旧路径只保留兼容包装 | 在父子技能合同统一引用 canonical schema JSON Pointer，防止再出现双真源 | sidecar 与 canonical shot 契约只需维护一处 |
| 子技能 sidecar 很完整，但父层不会 merge | 父级聚合层 | 回到父 skill 做 `beat_refs[] -> shot merge` | 在父 `SKILL.md` 固化 `beat_id / beat_refs[]` 对齐规则 | `分镜明细[]` 不再停留为空数组 |
| `beat_id` 不稳定，导致 factual/cinematic sidecar 无法对齐 | patch 对齐层 | 回退到共享 `beat_id = <group_id>-bNN` 规则 | 在 shared schema 与父层 merge 契约固化 beat id 规则 | merge 不再靠临场猜测 |
| shared root 缺 `分镜切换`，却直接开始 `镜花` 落镜 | 上游 seed 层 | 先报告 `2-Global` seed 缺口，再决定是否兼容修复 | 在父层把 `分镜切换` 设为 `镜花` 前置门 | `镜花` 不再代替上游决定镜数 |
| 把 `水月 / 镜花` 的“允许并发”误读成 `镜花` 内部也能乱序展开 | 调度边界层 | 回到父层顺序 gate、子层阶段串行的双层规则 | 在父 `SKILL.md` 和 `镜花/SKILL.md` 同步固定“先 seed，再水月，再镜花；镜花内部先 `分镜构图`” | `镜花` 后续模块不再反向改镜数 |
| `3-Detail` 重构后共享 reference 真源断链 | 真源同步层 | 将共享节点包/创作引导合同上收 `_shared/` 并统一回指 | 在 validator 中固定共享 reference 存在性与新路径检查 | 子技能 preload 与 `module-index` 不再落死路径 |
| 校验脚本只验子目录内部，导致父子拓扑断裂仍给绿灯 | 防回归门层 | 把父层 `镜花` 路由、共享 reference 存在性、旧叶子残留纳入校验 | 在阶段 validator 中增加父层和共享真源检查 | 旧拓扑或死链再次出现时能直接报错 |
| 父层 `validation-report` 声称 merge/ready 已完成，但缺少等价 stage validator | 阶段验收门层 | 增加 `scripts/validate_stage_output.py`，统一校验 episode root、child sidecar、`document_phase` 与 `validation-report.md` | 把 `ready` 门槛收束成可复跑脚本，而不是 prose 自证 | 父层完成态可以直接复验 |
| `3-Detail` 质评若只看单样本或只读合同，容易误判稳定性 | 证据治理层 | 每轮评估至少同时抽取当前 shared root、child sidecar、stage validator 与一个代表性 episode 做交叉复验 | 将“即时样本 + validator + 合同对照”固定为默认动态评测组合，而不是依赖单独维护的固定 benchmark 文档 | 每轮质评都能直接从当前项目状态复验 `shared root / sidecar / report` 一致性 |
| `组间设计` 在 detail 阶段被无故改写 | 继承边界层 | 恢复上游 seed，只允许回填 `出场角色及穿搭` | 在 `group_design_seed_contract.md` 与父层合同共同固化“默认继承不重写” | `全局风格 / 类型元素` 保持稳定 |
| `出场角色及穿搭` 长期留空 | 组级回填层 | 从 `水月` group patch 回填，不再等下游猜 | 在父 `SKILL.md` 把该字段列为最低负责槽位 | 进入 `4-Design` 前已有基础角色穿搭摘要 |
| `document_phase` 被直接写成 `ready`，但 shot patch 仍不完整 | phase 管理层 | 回退到 `detail_in_progress`，先补完 `分镜明细[]` | 在父 skill 的 phase gate 固定 `ready` 必须有 merge 完成与 validation | `ready` 与实际完成度一致 |
| `场景` 下游只拿到 `角色背景面`，导致旧仓研究/bridge 迁移时证据过薄 | downstream handoff 层 | 把 `分镜表现 / 摄影美学 / 时间段 / 导演意图` 显式纳入 `场景` 的补证字段 | 在 `3-Detail/SKILL.md` 与 `4-Design/1-清单/_shared/detail-output-consumption-contract.md` 同步固定场景补证口径 | `场景清单.json.scenes[].design_context` 能直接回链到镜头表现与摄影证据 |
| `3-Detail` 已写出 canonical 输出，却没有按项目 `team.yaml` 执行 `监制` 强化 | 阶段收尾合同层 | 在父 skill 追加 `S8/S9` 监制强化节点，输出后先做 supervision runtime 判定，再决定真实 subagents / fallback / skip | 将 `master-check-team` 的 reviewer 解析与 subagents gate 收束进 `3-Detail/SKILL.md`，并把 `team.yaml` 纳入默认预加载与 evidence source | 阶段收尾能回读 `监制强化` 记录与 patched targets |
| 项目 `team.yaml` 已启用 `监制`，但阶段仍把本地顺序模拟表述成正常主路径 | subagent gate 层 | 把 `runtime_policy.use_subagents_by_default` 写成 `3-Detail` 的真实分发门，而不是可有可无提示 | 在 `FIELD-DETAIL-09` 与 `Subagents 监制强化合同` 固定“满足条件就必须真实启动 subagents；降级必须显式说明” | `validation-report.md` 能读到 `used_subagents` 与降级原因 |
| 监制强化为了快修，直接在父层改了 `水月/镜花` owner 字段 | ownership reentry 层 | 将 findings 按字段 ownership 回流到 `S4/S5`，而不是在 `S8/S9` 静默越权 patch | 在 `Optimization Routing` 与 `FIELD-DETAIL-10` 固定“root/report 可直修，child-owned findings 必须回流 owner step” | 监制强化后的 patch 不再破坏 owner 边界 |
| 监制强化只审最后一个 `validation-report.md`，忽略 `第N集.json` 主输出 | review target bundle 层 | 将 `第N集.json` 固定为主目标，report 仅作次目标 | 在 `3-Detail/SKILL.md` 写死 `Review Target Bundle`，不允许 report 抢占 episode root 的主评审地位 | reviewer 结论能直接指向业务真源字段 |
| `team.yaml` 没有显式 `监制 members` 时，阶段要么静默跳过，要么臆造整团 reviewer | reviewer 解析层 | 先按 `shared_agents -> roles.supervision.members -> roles.supervision.source_skill_refs` 解析，再做 `1-3` 位受限补选 | 把 `master-check-team` 的补选规则缩窄到 `3-Detail` 专用：导演必选，摄影/编剧按 issue 类型补入，并显式标记 `team-inferred` | reviewer roster 既不空转，也不无边界膨胀 |

## Repair Playbook

1. 先检查 `projects/aigc/<项目名>/3-Detail/第N集.json` 是否存在、是否符合 shared schema、`document_phase` 当前处于什么状态。
2. 再检查 shared root 是否已经具备 `剧本正文 + 组间设计 + 分镜切换`；缺 `分镜切换` 时先报 seed 缺口。
3. 若需要 `组间设计.出场角色及穿搭` 或 factual 字段，先检查 `水月` sidecar 是否提供 beat-level evidence。
4. 若需要 shot skeleton 或导演/摄影字段，只有在既定 `分镜切换 + 水月 evidence` 稳定后才检查或重跑 `镜花` sidecar。
5. 做 shared root writeback 时，先保住 `剧本正文` 与 `分镜切换` 不变，再做 `beat_refs[]` merge 与 `镜头消费提示 -> 分镜表现` 投影。
6. 先用 `document_phase + validation-report.md + scripts/validate_stage_output.py` 形成可被审看的输出包，再决定是否进入 `监制强化`。
7. 若项目根 `team.yaml` 启用 `监制` 且命中 `3-Detail`，必须读取其 supervision 配置，先解 reviewer roster 与 mode，再决定真实 subagents 还是显式 fallback/skip。
8. 监制强化结束后要再次跑 validator；若 findings 命中 child owner 字段，则回流 `S4/S5`，而不是在收尾节点偷改。

## Reusable Heuristics

- `3-Detail` 父层的价值不是“再写一篇总稿”，而是让 shared JSON 与两个 patch sidecar 保持单线闭环。
- `水月` 最适合持有事实层，`镜花` 最适合持有镜头层；这两者应通过字段 ownership 协作，而不是轮流改正文。
- `剧本正文` 一旦已经由 `2-Global` 正确 seed，就应优先继承而不是再扩写；重写正文通常意味着边界丢失。
- `组间设计` 在 `3-Detail` 的默认姿势是“继承 + 回填穿搭”，不是“重新定义设计”。
- `出场角色及穿搭` 最适合在 `3-Detail` 回填，因为这时镜级事实已经足够稳定，早填容易空泛，晚填会把负担转嫁给下游。
- `3-Detail` 最稳的顺序不是“谁先想到谁先跑”，而是 `2-Global` 先落固定 `分镜切换`，`水月` 先落 beat-level evidence，`镜花` 再按既定镜数落真实切镜和镜头语言。
- 父层真正要守的是 shared root 单线写回和顺序 gate，而不是追求表面上的 owner 并发。
- `镜花` 内部仍必须先锁 `分镜构图` 的实际切镜窗口，再让后续模块消费这个骨架。
- 子技能 `references/` 若共享同一套节点包或创作引导规则，真源应显式上收 `_shared/`；否则目录重构后最容易出现局部自洽、整体断链。
- `ready` 的真实含义不是 sidecar 都存在，而是 shared root 已可被下游稳定消费且 validation 已给出通过结论。
- 当 `4-Design/1-清单` 成为 detail 阶段的首个稳定下游时，应把它的字段消费矩阵显式回链到 `3-Detail` 父合同；否则上游 schema 虽然完整，下游 leaf 仍会各自演化一套“我以为该怎么读”的解释。
- `3-Detail` 的动态质评最稳的做法，是直接绑定当前真实 validator、样本项目和最小对抗场景即时取证；否则很容易退化成只解读固定文档。
- `场景` 链在当前仓已经不是“只抄背景句”的极简模式；只要要承接旧仓高密度配置，就该把 `分镜表现 / 摄影美学 / 时间段` 一起视作 design_context 的合法补证层。
- `3-Detail` 的监制强化默认主目标始终是 `第N集.json`；`validation-report.md` 只是次目标，不能因为“最后写的是 report”就抢走主评审对象。
- 对 `3-Detail` 来说，`team.yaml.enabled == false` 代表自动监制 runtime 不启用；这与用户显式调用 `master-check-team` 的人工 override 不是一回事，阶段自动路径不应偷用那个 override。
- `shared_agents -> supervision.members -> supervision.source_skill_refs -> stage-aware 补选` 是 `3-Detail` 最稳的 reviewer 解析顺序；没有稳定 reviewer 时，应显式 skip，而不是制造伪顾问团。
- 监制强化最容易越界的地方不是 review 本身，而是“图省事直接修 child-owned 字段”；一旦 findings 命中 `水月/镜花` ownership，就应回流 owner step，而不是在父层收尾节点偷改。
