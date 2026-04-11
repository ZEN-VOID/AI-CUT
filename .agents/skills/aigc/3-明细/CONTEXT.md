# CONTEXT.md

## Purpose & Loading Contract

- 本文件是 `aigc/3-明细` 阶段的经验层知识库，不是执行日志。
- 调用 `.agents/skills/aigc/3-明细/SKILL.md` 时，应自动预加载本文件。
- 优先级遵循：用户显式请求 > `AGENTS.md` / 元规则 > `.agents/skills/aigc/SKILL.md` > 本 `SKILL.md` > 本 `CONTEXT.md`。

## Context Health

- soft_limit_chars: 40000
- hard_limit_chars: 80000
- soft_limit_cases: 80
- hard_limit_cases: 140
- status: ok

## Type Map

| failure_or_outcome_type | root_cause_layer | immediate_fix | systemic_prevention | verification_point |
| --- | --- | --- | --- | --- |
| `3-明细` 目录存在但没有阶段方法 | 阶段合同层 | 先补父级阶段合同与子路径矩阵 | 用“grouped source -> 组内明细精修 -> 单一主文件”收口 | 父级能解释唯一工作方式 |
| 子路径各自输出平行版本 | 真源治理层 | 收回到当前唯一主文件 `projects/<项目名>/编导/第N集.json` | 父级显式写 `patch-in-place` 总合同，并固定字段责任 | 不再出现多份正文真相 |
| 明细阶段退回泛化脚本改写 | 输入真源层 | 把 grouped source 与组内明细粒度重新锁为第一输入 | 在阶段合同固定“上游原文不改写，只做组内精修” | 任一增密都可回溯原文 |
| 后续加权层越过 `1-分镜表现` 直接堆细节 | tranche 层 | 明确 `1-分镜表现` 为默认首站 | 在父级路由矩阵写清 `T1 -> T6` | 顺序不再漂移 |
| `2-角色表现` 已补齐父子合同，但父级状态仍停留在“待补” | 阶段状态同步层 | 先同步父级 `3-明细/SKILL.md`，再同步根 `aigc` 状态 | 把阶段状态同步视为父子合同补建的收尾动作 | 父级与根入口状态一致 |
| `5-摄影美学` 空目录导致光影、色彩、参数无稳定写位 | 子路径合同层 | 先补 `5-摄影美学` 父级与三个 leaf | 把镜级 `摄影美学` 字段区块固化为该层唯一写位 | 摄影增强不再散落在终稿各处 |
| 摄影层回头重写 `焦距 / 光圈` 等静态字段 | 阶段边界层 | 回滚越界项并上溯到 `1-分镜表现` | 在 `5-摄影美学` 显式锁定“只补光影/色彩/捕捉参数” | 分镜骨架与摄影美学分层稳定 |
| `3-运镜手法` 没有合同，导致镜头运动层在明细阶段失语 | 子路径合同层 | 补 `3-运镜手法/SKILL.md + CONTEXT.md`，锁定 `运镜手法` 字段合同 | 把导演链高门槛适配为明细链镜级字段真源 | 终稿里有可执行的 `运镜手法` 字段与侧车波形 |
| `4-场景氛围` 已补齐合同，但父级状态仍停留在“待补” | 阶段状态同步层 | 同步更新 `3-明细/SKILL.md` 与根 `aigc` 的可路由描述 | 把新子路径补建视为父级/根级一起收尾的同步任务 | 父级矩阵与根入口状态一致 |
| `6-转场特效` 没有合同，导致段间衔接与收束层缺位 | 子路径合同层 | 补 `6-转场特效/SKILL.md + CONTEXT.md`，锁定 `转场特效` 字段合同 | 把导演链高门槛桥接逻辑适配为明细链镜级字段真源 | 终稿里有可执行的 `转场特效` 字段与侧车裁决 |
| 项目已启用顾问团，但明细阶段未读取 `team.yaml` | 共享运行时层 | 执行前先读项目根 `team.yaml` 与 `_shared/council-runtime/module-spec.md` | 在 `3-明细` 根技能固化 `监制前置 + 评审闸门` 合同 | 明细任务进入前能判断是否要启用顾问团 |
| 主 `SKILL.md` 长期同时承载主合同、长流程、长表格与写位合同 | 模块承载层 | 给根/父/叶技能补齐 `references/` 四件套，并把长细则从主 `SKILL.md` 下沉 | 固定“主合同留在 `SKILL.md`，长细则下沉 `references/*.md`”的单一拆分规范 | 主 `SKILL.md` 回到摘要+回链，细则集中在 `references/` |
| 父级 `chain-of-thought.md` 只剩字段表，无法承载阶段级路由与返工判断 | 思维链合同层 | 把父级思维链升级为 `模式判定 -> 启发式工作链 -> 三轴三重 -> 可见快照 -> Gate Summary` | 固定“父级思维链先服务唯一路由与单一主文件，而不是只做字段清单” | 从模块正文可直接读出为什么进这一层、如何回退与如何验收 |
| 结构化消费上游导演数据时，`3-明细` 自己推导了一套 group/shot 字段壳 | 真源治理层 | 明确共享字段壳只认 `.agents/skills/aigc/_shared/director_episode_output.schema.json` | `3-明细` 只维护 patch-in-place 语义与字段责任，不再另造 episode/group/shot 模板 | 上游导演 JSON 与明细消费字段壳一致 |
| `3-明细` 仍把主写位理解成阶段私有 `第N集.md`，而不是统一编导根文件 | 运行时真源层 | 将父级合同与输出模板统一改写为 `projects/<项目名>/编导/第N集.json` | 让 `_shared/project-runtime-layout.md` 承担目录真源，并固定“执行前完整读取 episode JSON，再做镜级 patch” | 各子路径都在同一 JSON 根文件上 patch 自己负责字段 |
| 子技能既想直写统一根文件，又把完整思维链一起堆进 episode JSON，导致根文件失控 | 输出治理层 | 固定“根文件只放最终镜级事实，完整思维链留在子技能 sidecar” | 在父级 `SKILL.md` 建立 `Unified Root File Output Governance`，要求子技能只交 `field patch`，父级统一聚合 | 根文件不再重复堆叠多份子技能三段式思维链 |
| 父级默认把所有子技能都纳入聚合，导致未命中层也被补空字段或伪状态 | 调度治理层 | 在父级 `SKILL.md` 建立 `Selective Dispatch And Aggregation Contract`，只聚合 `selected_subskills[]` | 固定“未调度子技能与总 json 无关，禁止为了结构完整补空聚合” | 本轮总 json 只受实际命中的子技能 patch 影响 |
| 上游其实来自 storyboard script，但 `3-明细` 仍按自由生成镜头处理 | 跨阶段 handoff 层 | 读取 `metadata.source_profile`，把 storyboard 预设当作保护性锚点 | 由 `1-规划` 把 `source_profile` 写进 bootstrap root，`3-明细` 固化 `preserve and extend` 合同 | 后续扩写围绕预设展开，不再推翻已锁定镜头轴 |

## Repair Playbook

1. 先检查 `3-明细/SKILL.md` 是否明确了新的阶段总前提。
2. 再检查父级是否固定了单一主文件与 `patch-in-place`。
3. 再检查当前命中的子路径是否真的有合同。
4. 若子路径已补齐，继续检查父级与根入口状态是否同步。
5. 最后才处理当前单次明细精修内容。

## Reusable Heuristics

- `3-明细` 阶段最容易失控的地方，不是写得不够多，而是没有单一主文件承接所有加权层。
- 只要上游已经完成分组，明细阶段就不该先“重写故事”，而应先“在组内锚点上增加可拍细节”。
- 只要任务的最高价值落在分镜组内的动作、视线、氛围、镜头调度与转场组织，而不是剧情结构推进，就应该进入 `3-明细` 而不是泛化写作路径。
- 数字前缀在本阶段不是装饰，它就是默认发酵顺序。
- 阶段内某个关键子路径补齐父子合同后，父级状态与根入口状态必须一起同步，不然总入口会继续误判。
- 摄影美学层最需要先锁的不是审美词，而是稳定写位；没有统一镜级 `摄影美学` 字段区块，就会重新长出多个平行摄影真相。
- 在 `3-明细` 里，光影、色彩、参数的最稳顺序通常是先定光，再定色，最后定捕捉参数。
- 导演链里的成熟方法论可以借，但 `3-明细` 子路径必须改写成“同一份 `第N集.json` 上的字段 patch”真源，而不是直接搬上游输出结构。
- `4-场景氛围` 最容易越权到 `5-摄影美学`；环境层应先补“场景为什么有压感”，而不是先补“画面看起来多漂亮”。
- `6-转场特效` 的价值不在于给每镜都加花活，而在于让真正命中的边界位有可感知、可续跑的桥接结果。
- 对 `3-明细` 来说，顾问团最稳的节奏是“监制先校可拍性与执行方向，评审最后只卡阶段验收”，不要让评审打断分层扩写主链。
- 当 `3-明细` 任一根/父/叶技能开始同时堆积路由矩阵、长流程、字段表和写位合同，优先补 `references/chain-of-thought.md + execution-flow.md + type-strategies.md + output-template.md`，而不是继续把主 `SKILL.md` 写成长文仓库。
- 阶段父级的 `chain-of-thought.md` 不能只保留字段主表；它必须先说明“为什么这轮进这一层、为什么不进其他层、写回哪里、失败回哪一层”。
- 当 `3-明细` 需要消费上游 `导演意图` 的结构化结果时，最稳的方式不是把叶子技能各自接一个私有 schema，而是让父级统一绑定 shared director schema，再由各子路径按责任字段继续 patch-in-place。
- 对 `3-明细` 来说，单一真源不只是“不要多份正文”，还包括“不要把 JSON 根文件重新投影回每个子路径各自的主文件”。
- 对复合型多子技能包来说，最稳的输出结构不是“每个子技能把完整三段式灌进根文件”，而是“根文件只收最终字段，三段式思维链留在 sidecar”。
- 对复合型多子技能包来说，最稳的聚合方式不是“每轮全量子技能都过一遍”，而是“只聚合本轮命中的子技能 patch”；未命中能力与总 json 无关。
- 当 `3-明细` 改为统一根文件后，叶子层最稳的合同不是“直接拥有 episode 主稿”，而是“只声明本字段 patch、自己的 evidence sidecar，以及只有被调度时才参与聚合”。
- 当 `3-明细` 已改为统一根文件后，leaf 深层细则不能只改路径；凡是 `[分镜N]`、`运镜：`、`转场：`、`[摄影美学]` 这类旧行式表头和示例，也要一起收平为 `分镜明细[]` 节点或镜级字段语义，否则执行者仍会把 JSON patch 理解成旧 `md` 主稿续写。
- 若上游源本身已经是分镜脚本，`3-明细` 的最佳动作不是“重做分镜”，而是“顺着预设点补质量层和细节层”。

### Case-20260410-AIGC-DETAIL-REPOSITION

- milestone_type: source_contract_change
- outcome: 将 `.agents/skills/aigc/3-明细` 的阶段定位从泛化脚本扩写明确收束为“分镜组内分镜明细颗粒度的多子类型精致动态设计”。
- root_cause_or_design_decision: 用户明确要求将旧阶段更名为 `3-明细`，且要求根目录合同不只改名字，还要从领域语义上脱离泛化脚本任务，转向围绕组内分镜明细的精修设计。
- final_fix_or_heuristic: 重写根 `SKILL.md + CONTEXT.md` 的阶段口径，将默认工作粒度锁为“组内明细主文件上的多层 patch-in-place 精修”，并把总入口与 registry 一并同步到 `3-明细`。
- prevention_or_replication_checklist:
  - [x] 根目录已完成旧阶段目录到 `3-明细` 的重命名
  - [x] 根 `SKILL.md` 已改为明细阶段语义
  - [x] 根 `CONTEXT.md` 已记录新定位的判路 heuristic
  - [x] 根 `aigc` 入口与 registry 已同步新阶段名
- evidence_paths:
  - `.agents/skills/aigc/3-明细/SKILL.md`
  - `.agents/skills/aigc/3-明细/CONTEXT.md`
  - `.agents/skills/aigc/SKILL.md`
  - `.codex/registry/skills.yaml`
- user_feedback_or_constraint: 用户要求将该阶段重命名为 `明细`，并将其从“泛化的脚本任务领域”调整为“分镜组内分镜明细颗粒度、围绕多个细分类型的精致动态设计”。

### Case-20260410-AIGC-DETAIL-SHARED-DIRECTOR-SCHEMA-CONSUMPTION

- milestone_type: source_contract_change
- outcome: 为 `3-明细` 父级输出契约补入 `.agents/skills/aigc/_shared/director_episode_output.schema.json` 的共享消费合同，固定上游导演 JSON 的 group/shot 壳来源。
- root_cause_or_design_decision: 用户要求为后续 harness 工程化预先定义导演集级 schema；如果 `3-明细` 不同步声明共享壳，后续各子路径在接结构化输入时会继续发明自己的 group/shot 命名与顺序。
- final_fix_or_heuristic: 父级 `references/output-template.md` 只绑定 shared director schema 的组级/镜级字段顺序，并强调本阶段职责是将分层判断压回共享 `分镜明细[]`，而不是重写另一份 shot contract。
- prevention_or_replication_checklist:
  - [x] 父级输出契约已声明唯一 shared schema
  - [x] 组级固定顺序已声明
  - [x] 镜级固定顺序已声明
  - [x] `3-明细/SKILL.md` 已补 shared schema 摘要回链
- evidence_paths:
  - `.agents/skills/aigc/_shared/director_episode_output.schema.json`
  - `.agents/skills/aigc/3-明细/references/output-template.md`
  - `.agents/skills/aigc/3-明细/SKILL.md`
  - `.agents/skills/aigc/3-明细/CONTEXT.md`
- user_feedback_or_constraint: 用户明确要求 schema 同时覆盖“组间设计 + 分镜明细”，以支撑后续 harness 工程化演化。

## Case Log

### Case-20260409-AIGC-SCRIPT-STAGE-CONTRACT

- milestone_type: source_contract_change
- outcome: 为 `.agents/skills/aigc/3-明细` 建立了新的阶段总前提，把明细阶段明确为“基于 grouped source 的层层精修式明细任务”。
- root_cause_or_design_decision: 用户明确要求整个 `3-明细` 系列改按新的前提预设运行；真正缺口不只是某个子目录，而是父级阶段完全空白，无法承接“单一主文件逐层发酵”的总合同。
- final_fix_or_heuristic: 先补父级 `3-明细/SKILL.md + CONTEXT.md`，把 `1-分镜表现` 定位为默认首站，并将后续子路径都改写为共享单一主文件的加权层；当前最新运行时已进一步统一到 `projects/<项目名>/编导/第N集.json`。
- prevention_or_replication_checklist:
  - [x] 已建立新的阶段总前提
  - [x] 已固定单一主文件
  - [x] 已显式声明 `1 -> 6` 默认顺序
  - [x] 已区分当前已建合同与待补合同的子路径
- evidence_paths:
  - `.agents/skills/aigc/3-明细/SKILL.md`
  - `.agents/skills/aigc/3-明细/CONTEXT.md`
  - `.agents/skills/aigc/3-明细/subtypes/1-分镜表现/SKILL.md`
  - `.agents/skills/aigc/3-明细/subtypes/1-分镜表现/CONTEXT.md`
- user_feedback_or_constraint: 用户明确要求“整个 `.agents/skills/aigc/3-明细` 系列按照新的前提预设：对于上游分集分组好的原文，根据不同的任务类型进行层层加权扩写式任务，以其最终发酵为完善的融合组间层全部智慧的最终文件”。

### Case-20260409-AIGC-SCRIPT-CHARACTER-STATUS-SYNC

- milestone_type: source_contract_change
- outcome: 将 `2-角色表现` 从父级状态中的“待补”同步升级为“已建父子合同”，并将该变化与根 `aigc` 状态联动同步。
- root_cause_or_design_decision: 本轮真正补齐的是 `2-角色表现` 与其 `动作戏 / 对手戏 / 内心戏`，若 `3-明细` 父级继续保留旧状态，就会形成新的真源漂移。
- final_fix_or_heuristic: 在 `2-角色表现` 父子合同落地后，同步更新 `3-明细` 父级状态描述，并把“状态同步”沉淀为阶段经验规则。
- prevention_or_replication_checklist:
  - [x] `2-角色表现` 状态已同步
  - [x] 根 `aigc` 状态已同步
  - [x] 阶段经验层已记录同类漂移模式
- evidence_paths:
  - `.agents/skills/aigc/3-明细/SKILL.md`
  - `.agents/skills/aigc/3-明细/subtypes/2-角色表现/SKILL.md`
  - `.agents/skills/aigc/SKILL.md`
- user_feedback_or_constraint: 用户要求先补齐 `动作戏 / 对手戏 / 内心戏`，再补根级 `2-角色表现` 与整个 `3-明细` 系列前提。

### Case-20260409-AIGC-SCRIPT-CINEMATOGRAPHY-CONTRACT

- milestone_type: source_contract_change
- outcome: 为 `.agents/skills/aigc/3-明细/subtypes/5-摄影美学` 建立了父级合同与三个 leaf，并将父级状态从“待补”同步更新为“已建父子合同”。
- root_cause_or_design_decision: 用户明确要求 `5-摄影美学` 包含 `光影·色彩·摄影参数`，且整个 `3-明细` 系列继续服从“基于上游分组原文的层层加权扩写”前提；真正缺口是该目录仍为空，导致摄影增强没有稳定写位与边界治理。
- final_fix_or_heuristic: 建立 `5-摄影美学` 父级合同，新增 `光影设计 / 色彩设计 / 摄影参数` 三个 leaf，并将摄影增强统一收口到共享终稿镜级 `摄影美学` 字段区块。
- prevention_or_replication_checklist:
  - [x] `5-摄影美学` 父级 `SKILL.md` 已建立
  - [x] `5-摄影美学` 父级 `CONTEXT.md` 已建立
  - [x] 三个 leaf 均已落地 `SKILL.md + CONTEXT.md`
  - [x] 父级状态已同步为“已建父子合同”
- evidence_paths:
  - `.agents/skills/aigc/3-明细/SKILL.md`
  - `.agents/skills/aigc/3-明细/CONTEXT.md`
  - `.agents/skills/aigc/3-明细/subtypes/5-摄影美学/SKILL.md`
  - `.agents/skills/aigc/3-明细/subtypes/5-摄影美学/CONTEXT.md`
- user_feedback_or_constraint: 用户明确要求完善 `5-摄影美学`，并指定应包含 `光影·色彩·摄影参数`，同时要求整个 `3-明细` 系列统一服从新的阶段前提。

### Case-20260409-AIGC-SCRIPT-CAMERA-STATUS-SYNC

- milestone_type: source_contract_change
- outcome: 为 `.agents/skills/aigc/3-明细/subtypes/3-运镜手法` 建立了子路径合同，并将 `3-明细` 父级状态同步更新为“已建合同”。
- root_cause_or_design_decision: 用户要求参照导演链 `8-运镜手法` 完善明细链 `3-运镜手法`，但 `3-明细` 当前真源是同一份 `第N集.json` 的镜级字段集合，不能直接照搬导演阶段 JSON 组级字段合同。
- final_fix_or_heuristic: 吸收导演参考的高门槛运镜判断，改写为明细链的 `运镜手法` 字段合同，并同步父级状态与经验层。
- prevention_or_replication_checklist:
  - [x] `3-运镜手法` 已建立 `SKILL.md`
  - [x] `3-运镜手法` 已建立 `CONTEXT.md`
  - [x] 父级状态已同步
  - [x] 已记录“参考导演链但必须真源适配”的经验
- evidence_paths:
  - `.agents/skills/aigc/3-明细/SKILL.md`
  - `.agents/skills/aigc/3-明细/CONTEXT.md`
  - `.agents/skills/aigc/3-明细/subtypes/3-运镜手法/SKILL.md`
  - `/Volumes/AIGC/AIGC-ZEN-VOID/.agents/skills/aigc2026/2-导演/8-运镜手法/SKILL.md`
- user_feedback_or_constraint: 用户明确要求“完善一下 `.agents/skills/aigc/3-明细/subtypes/3-运镜手法`”，并强调整个 `3-明细` 系列应遵循新的“层层加权扩写式任务”前提。

### Case-20260409-AIGC-SCRIPT-ATMOSPHERE-STATUS-SYNC

- milestone_type: source_contract_change
- outcome: 将 `4-场景氛围` 从父级路由矩阵中的“目录存在，合同待补”同步升级为“已建合同”，并把其职责改写为环境压力、空间温度、空气质感与物件回声的氛围层补写。
- root_cause_or_design_decision: 用户明确要求参照 ZEN-VOID 的 `6-氛围感` 完善当前仓 `4-场景氛围`；如果只补子技能目录而不回写 `3-明细` 父级状态，就会立即产生新的父子真源漂移。
- final_fix_or_heuristic: 在 `4-场景氛围/SKILL.md + CONTEXT.md` 落地后，同步更新 `3-明细/SKILL.md` 的子路径矩阵，并把“氛围层不要越权到摄影层”沉淀为阶段经验。
- prevention_or_replication_checklist:
  - [x] `4-场景氛围` 状态已同步
  - [x] 父级经验层已记录同类同步规则
  - [x] 已沉淀氛围层与摄影层的边界启发
- evidence_paths:
  - `.agents/skills/aigc/3-明细/SKILL.md`
  - `.agents/skills/aigc/3-明细/CONTEXT.md`
  - `.agents/skills/aigc/3-明细/subtypes/4-场景氛围/SKILL.md`
  - `.agents/skills/aigc/3-明细/subtypes/4-场景氛围/CONTEXT.md`
- user_feedback_or_constraint: 用户要求参照 `/Volumes/AIGC/AIGC-ZEN-VOID/.agents/skills/aigc2026/1-编剧/6-氛围感` 完善当前 `4-场景氛围`，并强调整个 `3-明细` 系列都要遵守新的层层加权扩写前提。

### Case-20260409-AIGC-SCRIPT-TRANSITION-STATUS-SYNC

- milestone_type: source_contract_change
- outcome: 为 `.agents/skills/aigc/3-明细/subtypes/6-转场特效` 建立了子路径合同，并将 `3-明细` 父级状态同步更新为“已建合同”。
- root_cause_or_design_decision: 用户要求参照导演链 `9-转场特效` 完善明细链 `6-转场特效`，但 `3-明细` 当前真源是同一份 `第N集.json` 的镜级字段集合，不能直接照搬导演阶段 JSON 镜级字段合同。
- final_fix_or_heuristic: 吸收导演参考的高门槛桥接与包装层判断，改写为明细链的 `转场特效` 字段合同，并同步父级状态与经验层。
- prevention_or_replication_checklist:
  - [x] `6-转场特效` 已建立 `SKILL.md`
  - [x] `6-转场特效` 已建立 `CONTEXT.md`
  - [x] 父级状态已同步
  - [x] 已记录“参考导演链但必须真源适配”的经验
- evidence_paths:
  - `.agents/skills/aigc/3-明细/SKILL.md`
  - `.agents/skills/aigc/3-明细/CONTEXT.md`
  - `.agents/skills/aigc/3-明细/subtypes/6-转场特效/SKILL.md`
  - `/Volumes/AIGC/AIGC-ZEN-VOID/.agents/skills/aigc2026/2-导演/9-转场特效/SKILL.md`
- user_feedback_or_constraint: 用户明确要求“完善一下 `.agents/skills/aigc/3-明细/subtypes/6-转场特效`”，并强调整个 `3-明细` 系列应遵循新的“层层加权扩写式任务”前提。

### Case-20260409-AIGC-SCRIPT-COUNCIL-RUNTIME

- milestone_type: source_contract_change
- outcome: 为 `3-明细` 根技能接入了基于项目根 `team.yaml` 的顾问团运行时，默认执行 `监制前置 -> 主代理草案 -> 评审闸门`，并由 `1-分镜表现 / 2-角色表现 / 5-摄影美学` 声明继承。
- root_cause_or_design_decision: 用户要求 `3-明细` 根技能或叶子技能进入时都先读取同一份 `team.yaml`，并落实 `监制 / 评审` 职责；如果只改根技能，不补中间父技能继承钩子，nested leaf 直达时仍可能断链。
- final_fix_or_heuristic: 对有中间父技能的阶段，应由根技能持有运行时合同，中间父技能只声明继承，不在每个父子层重复发明第二套顾问团规则。
- prevention_or_replication_checklist:
  - [x] `3-明细/SKILL.md` 已新增 `Council Runtime Contract`
  - [x] `1-分镜表现 / 2-角色表现 / 5-摄影美学` 已声明继承上层顾问团运行时
  - [x] 已固定 `监制前置 + 评审 validation gate`
- evidence_paths:
  - `.agents/skills/aigc/3-明细/SKILL.md`
  - `.agents/skills/aigc/3-明细/CONTEXT.md`
  - `.agents/skills/aigc/3-明细/subtypes/1-分镜表现/SKILL.md`
  - `.agents/skills/aigc/3-明细/subtypes/2-角色表现/SKILL.md`
  - `.agents/skills/aigc/3-明细/subtypes/5-摄影美学/SKILL.md`
- user_feedback_or_constraint: 用户明确要求 `3-明细` 及其叶子技能进入时都先读取 `projects/<项目名>/team.yaml`，并默认启用 `监制 / 评审` 职责。

### Case-20260409-AIGC-SCRIPT-REFERENCES-MODULARIZATION

- milestone_type: source_contract_change
- outcome: 为 `3-明细` 全树 15 个根/父/叶技能统一补齐 `references/` 四件套，并把长流程、长表格、路由/VSM、写位合同从主 `SKILL.md` 下沉为模块细则。
- root_cause_or_design_decision: 在前一轮统一合同外壳后，`3-明细` 树仍把主合同、执行流程、字段表、VSM 和输出写位长期堆在同一份 `SKILL.md` 中，已经不符合 `skill-内容输出型` 的最新 `references/` 模块承载规范。
- final_fix_or_heuristic: 以 `SKILL.md` 保留主合同、边界、门禁、Mermaid 摘要与回链为原则，为每个技能目录补 `references/chain-of-thought.md`、`execution-flow.md`、`type-strategies.md`、`output-template.md`，并把长细则按模块稳定下沉。
- prevention_or_replication_checklist:
  - [x] `3-明细` 根技能已补齐 `references/`
  - [x] `3-明细` 全树父级与 leaf 技能已补齐 `references/`
  - [x] 主 `SKILL.md` 已改成摘要 + 回链，不再重复长细则
  - [x] `Context Preload` 已显式声明按需继续加载 `references/*.md`
- evidence_paths:
  - `.agents/skills/aigc/3-明细/SKILL.md`
  - `.agents/skills/aigc/3-明细/references/chain-of-thought.md`
  - `.agents/skills/aigc/3-明细/references/execution-flow.md`
  - `.agents/skills/aigc/3-明细/references/type-strategies.md`
  - `.agents/skills/aigc/3-明细/references/output-template.md`
- user_feedback_or_constraint: 用户明确要求“把 `3-明细` 全树的父级/叶子技能都按最新 `references` 规范拆开，但保持语义不变”。

### Case-20260409-AIGC-SCRIPT-THINK-THINK-UPGRADE

- milestone_type: source_contract_change
- outcome: 将 `.agents/skills/aigc/3-明细/references/chain-of-thought.md` 从老式字段表升级为符合最新 `think-think` 规范的阶段级思维链合同。
- root_cause_or_design_decision: 父级思维链虽然已有字段表，但仍无法表达阶段级唯一路由、单一主文件、工具后反思和 Gate Summary，导致 `3-明细` 根技能难以承载“为什么先进哪一层”的真实裁决压力。
- final_fix_or_heuristic: 以 `模式判定 -> 启发式工作链 -> 三轴三重 -> 工具后反思 -> 字段落盘 -> Gate Summary` 为骨架重写父级 `chain-of-thought.md`，并补一份就近设计报告供后续回查。
- prevention_or_replication_checklist:
  - [x] 父级思维链已显式声明模式与消费者
  - [x] 已补启发式工作链与三轴三重
  - [x] 已补工具后反思与 Gate Summary
  - [x] 已把经验回写到 `CONTEXT.md`
- evidence_paths:
  - `.agents/skills/aigc/3-明细/references/chain-of-thought.md`
  - `.agents/skills/aigc/3-明细/reports/思维链设计报告-20260409.md`
  - `.agents/skills/aigc/3-明细/CONTEXT.md`
- user_feedback_or_constraint: 用户明确要求按最新 `think-think` 思维链设计规范优化 `.agents/skills/aigc/3-明细/references/chain-of-thought.md`。

### Case-20260410-AIGC-DETAIL-UNIFIED-DIRECTOR-ROOT

- milestone_type: source_contract_change
- outcome: 将 `3-明细` 的父级主写位从阶段私有 `projects/<项目名>/3-明细/第N集.md` 收敛为统一根文件 `projects/<项目名>/编导/第N集.json`，并把本阶段职责改写为镜级字段 patch。
- root_cause_or_design_decision: 用户明确要求 `2-组间` 与 `3-明细` 都围绕同一个 JSON 根文件工作，并且每次输出都要加载已落盘的整个 JSON 作为上下文；若 `3-明细` 继续保留自己的 `第N集.md` 主文件，shared schema 将只剩参考意义，无法成为真正的 harness 运行时真源。
- final_fix_or_heuristic: 由 `_shared/project-runtime-layout.md` 固定目录结构，`1-分集` 先 bootstrap 空 episode JSON，`2-组间` 先 patch 组级字段，`3-明细` 再按子路径 patch `分镜明细[]` 下的镜级字段。
- prevention_or_replication_checklist:
  - [x] `3-明细/SKILL.md` 已改写为统一 JSON 根文件口径
  - [x] `3-明细/references/output-template.md` 已改为镜级字段责任表
  - [x] evidence 路径已迁到 `projects/<项目名>/编导/evidence/`
  - [x] 已显式声明执行前加载完整 `第N集.json`
- evidence_paths:
  - `.agents/skills/aigc/_shared/project-runtime-layout.md`
  - `.agents/skills/aigc/3-明细/SKILL.md`
  - `.agents/skills/aigc/3-明细/references/output-template.md`
  - `.agents/skills/aigc/1-规划/subtypes/1-分集/SKILL.md`
  - `.agents/skills/aigc/2-组间/SKILL.md`
- user_feedback_or_constraint: 用户明确要求“之后 2 组和 3 组都将围绕一个统一根文件（确定为 json）进行不同字段分属下的定向输出”。

### Case-20260410-AIGC-DETAIL-OUTPUT-GOVERNANCE-PROMOTION

- milestone_type: source_contract_change
- outcome: 将“统一根文件只承载最终业务真相、子技能完整思维链留在 sidecar、父技能负责 field patch 聚合”的输出治理决议正式晋升到 `3-明细/SKILL.md`。
- root_cause_or_design_decision: 用户在统一根文件方案下进一步追问子技能是否应直接写字段，还是先各写完整三段式再由父级汇总；若不先升格为父级规范，后续 `3-明细` 全树重构会再次长出“根文件塞满思维链”或“父级二次汇总成第二真稿”的双真源风险。
- final_fix_or_heuristic: 在父级主合同新增 `Unified Root File Output Governance`，明确根文件只承载最终镜级字段，子技能只交 `field patch`，完整三段式思维链只允许落在 sidecar，shared schema 顶层 `thinking_chain` 仅保留父级精简摘要或 provenance 用途。
- prevention_or_replication_checklist:
  - [x] 父级 `SKILL.md` 已新增统一输出治理章节
  - [x] `CONTEXT.md` 已记录“根文件不堆叠子技能思维链”的经验
  - [x] 子技能输出模板已统一继承父级真源
  - [x] 后续整树重构可直接以该规范为准绳
- evidence_paths:
  - `.agents/skills/aigc/3-明细/SKILL.md`
  - `.agents/skills/aigc/3-明细/CONTEXT.md`
  - `.agents/skills/aigc/3-明细/references/output-template.md`
  - `.agents/skills/aigc/2-组间/SKILL.md`
- user_feedback_or_constraint: 用户明确要求“先将以上决议升格为标准化规范，落盘到 `2组/3组` 的主 `SKILL.md`，再以其为指导执行完整重构”。

### Case-20260410-AIGC-DETAIL-LEAF-MD-SEMANTIC-FLATTENING

- milestone_type: source_contract_change
- outcome: 将 `1-分镜表现 / 3-运镜手法 / 4-场景氛围 / 5-摄影美学 / 6-转场特效` 的深层 `chain-of-thought.md + type-strategies.md` 从旧 `md` 行式示例统一收平为 JSON 字段 patch 语义。
- root_cause_or_design_decision: 统一根文件已切到 `projects/<项目名>/编导/第N集.json` 后，leaf 深层细则仍保留 `[分镜N]`、`运镜：`、`转场：`、`[摄影美学]` 等旧示例；如果只改路径、不改表头和例子，执行者仍会把根文件当旧 `md` 主稿来理解。
- final_fix_or_heuristic: 把深层细则统一改写为 `分镜明细[]` 节点、`运镜手法 / 转场特效 / 摄影美学` 字段、`第N集.json` 真源与 evidence sidecar 语义；sidecar 保留 `md` 仅作为过程载体，不再充当 episode 主稿暗示。
- prevention_or_replication_checklist:
  - [x] `1-分镜表现` 深层示例已改为 `分镜明细[]` 节点语义
  - [x] `3-运镜手法` 深层示例已改为 `运镜手法` 字段语义
  - [x] `4-场景氛围` 深层落盘表头已改回统一根文件字段 + evidence sidecar
  - [x] `5-摄影美学` 父子细则已改为 `摄影美学` 字段与子字段语义
  - [x] `6-转场特效` 深层示例已改为 `转场特效` 字段语义
- evidence_paths:
  - `.agents/skills/aigc/3-明细/subtypes/1-分镜表现/references/chain-of-thought.md`
  - `.agents/skills/aigc/3-明细/subtypes/3-运镜手法/references/chain-of-thought.md`
  - `.agents/skills/aigc/3-明细/subtypes/4-场景氛围/references/chain-of-thought.md`
  - `.agents/skills/aigc/3-明细/subtypes/5-摄影美学/references/chain-of-thought.md`
  - `.agents/skills/aigc/3-明细/subtypes/6-转场特效/references/chain-of-thought.md`
- user_feedback_or_constraint: 用户明确要求“把更深一层的 leaf chain-of-thought/type-strategies 全量再扫一轮，把还带旧 md 语义的表头和示例也彻底收平”。

### Case-20260411-AIGC-DETAIL-STORYBOARD-SOURCE-HANDOFF

- milestone_type: source_contract_change
- outcome: 为 `3-明细` 根技能补入了 `metadata.source_profile` 的消费合同，使 storyboard-script 上游能够以“preserve and extend”模式稳定进入后续明细层。
- root_cause_or_design_decision: 先前 `3-明细` 只假设上游是 grouped source + 空白可扩写位，没有来源画像就无法区分“可自由生成的镜头骨架”和“必须保留的 storyboard 预设”。
- final_fix_or_heuristic: 若 `1-规划` 已把 `source_type / preset_retention_mode / detail_expansion_mode / locked_preset_axes` 写入 bootstrap root，则 `3-明细` 必须先消费这组来源画像，再决定是否允许自由扩写；对 storyboard source 默认执行“preserve and extend”。
- prevention_or_replication_checklist:
  - [x] `3-明细/SKILL.md` 已加入来源画像读取门
  - [x] `3-明细/references/type-strategies.md` 已加入 source-profile 路由
  - [x] `3-明细/references/output-template.md` 已加入 source-profile 消费说明
- evidence_paths:
  - `.agents/skills/aigc/3-明细/SKILL.md`
  - `.agents/skills/aigc/3-明细/references/type-strategies.md`
  - `.agents/skills/aigc/3-明细/references/output-template.md`
  - `.agents/skills/aigc/_shared/director_episode_output.schema.json`
- user_feedback_or_constraint: 用户明确要求“如果保留分镜脚本中的预设点，后续 `3-明细` 需要能够不冲突地顺着这些预设点继续丰富和拓展”。
