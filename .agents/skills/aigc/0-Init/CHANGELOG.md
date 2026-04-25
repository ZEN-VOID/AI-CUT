# CHANGELOG.md

本文件记录 `.agents/skills/aigc/0-Init/` 的结构迁移与目录治理说明，不参与默认技能预加载，也不与 `SKILL.md` / `CONTEXT.md` 竞争真源。

## 2026-04-24

- `Case-20260424-AIGC-INIT-MINIMAL-BOOTSTRAP-CORRECTION`
  - 以 `projects/aigc/校诡` 为样本，纠正 `0-Init` 把下游阶段目录和旧兼容链目录当成初始化骨架的问题。
  - 新初始化只创建 `0-Init/`、`Original/` 与项目根载体；`1-Planning`、`2-Global`、`3-Detail`、`4-Design`、`5-Image`、`6-Video` 均由对应阶段执行时创建。
  - `Story/` 统一更名为 `Original/`；画面阶段未来执行落点统一为 `5-Image/A-分镜帧/` 与 `5-Image/B-分镜故事板/`，不再使用无序号 `分镜帧/`、`分镜故事板/` 初始化目录。
  - 将 `1-Planning/1-分集`、`2-格式`、`3-分组`、`episode-split-plan.json`、`validation-report.md`、`5-Image/2-参照引用`、`5-Image/3-图像生成`、旧 `6-Video` 兼容目录与 `7-Cut/` 列入 `0-Init` forbidden bootstrap paths。
  - 本条 supersedes 同日早先的 `AIGC-INIT-RUNTIME-SKELETON-SUBSKILL-SYNC` 中关于初始化预建图像/视频兼容链目录的旧口径。
  - 证据路径：
    - `.agents/skills/aigc/0-Init/SKILL.md`
    - `.agents/skills/aigc/0-Init/CONTEXT.md`
    - `.agents/skills/aigc/0-Init/references/scope-and-runtime.md`
    - `.agents/skills/aigc/_shared/project-runtime-layout.md`
    - `.agents/skills/aigc/_shared/story-source-contract.md`
    - `scripts/aigc_skill_audit.py`

- `Case-20260424-AIGC-INIT-RUNTIME-SKELETON-SUBSKILL-SYNC`
  - 跟随 `5-Image` / `6-Video` 子技能包调整，同步初始化 bootstrap skeleton 的显式 marker。
  - 补齐 `5-Image/分镜故事板/`、`5-Image/分镜帧/`、`6-Video/A.分镜画面参照/` 与 `6-Video/2-参照引用/` 在 `0-Init` 入口和审计脚本中的检查。
  - 明确 `5-Image/A.分镜画面`、`5-Image/B.分镜故事板` 属于融合路由入口，不新增同名 runtime 目录；实际写位仍回到 `分镜帧/`、`分镜故事板/`、`2-参照引用/` 与 `3-图像生成/`。
  - 同步更新共享 runtime layout、根 `aigc` 阶段状态投影与 `scope-and-runtime` reference，避免初始化目录机械镜像技能树中间层。
  - 证据路径：
    - `.agents/skills/aigc/0-Init/SKILL.md`
    - `.agents/skills/aigc/0-Init/CONTEXT.md`
    - `.agents/skills/aigc/0-Init/references/scope-and-runtime.md`
    - `.agents/skills/aigc/_shared/project-runtime-layout.md`
    - `.agents/skills/aigc/SKILL.md`
    - `scripts/aigc_skill_audit.py`

- `Case-20260424-AIGC-INIT-TEMPLATE-OUTPUT-CONTRACT-ALIGNMENT`
  - 检查 `templates/` 与 `SKILL.md` 的 `Output Contract (Mandatory)` 是否匹配。
  - 将 `north-star.template.yaml` 收紧为长期约束模板，移除 `init_mode / mode_source` 这类初始化过程 provenance 字段。
  - 将 `init-handoff.template.yaml` 的旧阶段 seed 命名改为当前阶段链：`planning / global / detail / design / image / video / cut`。
  - 新增 `state.template.json`、`project-changelog.template.md`、`project-context-readme.template.md`、`output-template.md` 与 `output-template-map.md`，明确本地模板、shared 模板与惰性治理输出的对应关系。
  - 在 `Output Contract` 中补齐 `Required output / Output format / Output path / Naming convention / Completion gate` 五个显式锚点。
  - 证据路径：
    - `.agents/skills/aigc/0-Init/templates/output-template-map.md`
    - `.agents/skills/aigc/0-Init/templates/output-template.md`
    - `.agents/skills/aigc/0-Init/templates/north-star.template.yaml`
    - `.agents/skills/aigc/0-Init/templates/init-handoff.template.yaml`
    - `.agents/skills/aigc/0-Init/templates/state.template.json`

- `Case-20260424-AIGC-INIT-INPUT-OUTPUT-ANCHOR`
  - 将 `0-Init/SKILL.md` 的入口重心进一步收束到 `Input Contract (Mandatory)` 与 `Output Contract (Mandatory)`。
  - 明确 accepted / rejected / rerouted input，核心 writeback 输出、blocked output shape 与最终用户答复字段。
  - 将 `Core Workflow` 与 `Execution Contract` 改为 index 口径，过程细节继续导向 `references/`、`steps/`、`types/` 与 `review/`。
  - 证据路径：
    - `.agents/skills/aigc/0-Init/SKILL.md`

- `Case-20260424-AIGC-INIT-SKILL-2-0-UPGRADE`
  - 使用 `$skill-工作车间` 将 `0-Init` 从旧的长 `SKILL.md` 入口升级为 Skill 2.0 动态引用包。
  - 新增标准分区：`references/`、`steps/`、`review/`、`types/`、`knowledge-base/`、`scripts/`、`README.md` 与 `TODO.md`。
  - 将运行时路径、模式与组队、源与工件、rebootstrap 分别拆到 `references/`；将节点网络拆到 `steps/init-workflow.md`；将充分性与 pass table 拆到 `review/init-review-gate.md`；将判型策略拆到 `types/init-type-map.md`。
  - 保留旧三模式 stub 删除口径：不恢复 `references/*-mode/module-spec.md`，新 `references/` 只作为 Skill 2.0 细则分区，由 `SKILL.md` 的 Reference Loading Guide 明确读取。
  - 同步修正 `agents/openai.yaml` 的产品描述与 `$aigc-init` 默认提示。
  - 证据路径：
    - `.agents/skills/aigc/0-Init/SKILL.md`
    - `.agents/skills/aigc/0-Init/references/migration-matrix.md`
    - `.agents/skills/aigc/0-Init/steps/init-workflow.md`
    - `.agents/skills/aigc/0-Init/review/init-review-gate.md`
    - `.agents/skills/aigc/0-Init/types/init-type-map.md`
    - `.agents/skills/aigc/0-Init/knowledge-base/init-heuristics.md`
    - `.agents/skills/aigc/0-Init/README.md`
    - `.agents/skills/aigc/0-Init/TODO.md`

## 2026-04-18

- `Case-20260418-AIGC-INIT-PROJECT-ROOT-CHANGELOG`
  - 将项目根 `projects/aigc/<项目名>/CHANGELOG.md` 补入 `0-Init` 的默认初始化合同。
  - 明确它是项目级时间序记录入口，由 `0-Init` 首次创建，但不承载 live route truth、断点治理或 review verdict。
  - 同步把这条规则上收到 shared runtime layout，并在 `scripts/aigc_skill_audit.py` 新增审计检查，防止后续 skeleton 再次漏建。
  - 证据路径：
    - `.agents/skills/aigc/0-Init/SKILL.md`
    - `.agents/skills/aigc/0-Init/CONTEXT.md`
    - `.agents/skills/aigc/_shared/project-runtime-layout.md`
    - `scripts/aigc_skill_audit.py`

## 2026-04-15

- `Case-20260415-AIGC-INIT-SMART-ADVISOR-SINGLE-MODE`
  - 将 `0-Init` 的初始化模式从旧的 `主创会诊 / 快速成案 / 自主问答` 三分结构，收口为单一 `智能顾问模式`。
  - 开场只保留 `自动组队 / 自定义组队` 两个编组子模式，并明确任何顾问候选都只能来自 `.agents/skills/team/`。
  - 同步把 `team.yaml` 模板升级为初始化编组真源，新增 `init_contract.*`、`roles.planning.init_interview.*` 与 `runtime_policy.require_subagents_for_init_interview`。
  - 将 `planning` 角色固定为初始化 interview 的首轮顾问 owner，并把“必须真实启用 subagents、不可降级成本地顺序扮演”写回父 `SKILL.md` 与审计脚本。
  - 证据路径：
    - `.agents/skills/aigc/0-Init/SKILL.md`
    - `.agents/skills/aigc/0-Init/CONTEXT.md`
    - `.agents/skills/aigc/0-Init/agents/openai.yaml`
    - `.agents/skills/aigc/_shared/council-runtime/team.template.yaml`
    - `.agents/skills/aigc/_shared/council-runtime/module-spec.md`
    - `scripts/aigc_skill_audit.py`

- `Case-20260415-AIGC-INIT-THOUGHT-ACTION-NODE-SYNC`
  - 将 `0-Init` 的思维·执行节点继续下沉到新口径：不仅改模式说明，还同步改 `Thinking-Action Node Contract`、`Topology Contract`、`Thought Pass Map` 与 `Pass Table`。
  - 新增节点级执行语义：`decision_lock / dispatch_contract / write_scope / blocker_rule / reentry_rule`。
  - 明确 `N4` 的 `planning_interview_engine` 必须真实起 subagents，且 `N7` 失败时按缺口层级回退到 `N1/N3/N4/N5`，而不是泛化回退。
  - 证据路径：
    - `.agents/skills/aigc/0-Init/SKILL.md`
    - `.agents/skills/aigc/0-Init/CONTEXT.md`

- `Case-20260415-AIGC-INIT-TEAM-OWNERSHIP-AND-AUTO-LINEUP`
  - 将 `策划 / 监制 / 评审` 从“阶段通用顾问”改写为明确权属：`策划 -> 0-Init`，`监制 -> 2-Global / 3-Detail / 4-Design`，`评审 -> 5-Image / 6-Video`。
  - 将自动组队重写为“两层裁决”：先锁治理角色，再按 `导演组 / 设计组 / 摄影组` 三个必选组补齐具体大师，允许每组多人，并把“黄金组合”改为显式排序准则而不是模糊口头推荐。
  - 明确 `策划 / 监制 / 评审` 可以是同一波人，也可以是不同的人；新增 `team_setup.role_allocation_mode / same_person_cross_role_allowed / role_overlap_notes`，避免后续把三类治理角色误读成强制互斥。
  - 增加题材缺口补救口：当现有 roster 明显不足但当前仍可执行时，继续按现有阵容执行，同时在 `todos/*-team-recommendation.md` 输出推荐文档并把路径写回团队真源。
  - 同步把 shared `council-runtime` 的消费范围从 `1-Planning / 2-Global / 3-Detail / 4-Design` 改为 `2-Global / 3-Detail / 4-Design / 5-Image / 6-Video`，避免根技能与共享模板继续传播旧阶段口径。
  - 证据路径：
    - `.agents/skills/aigc/0-Init/SKILL.md`
    - `.agents/skills/aigc/0-Init/CONTEXT.md`
    - `.agents/skills/aigc/_shared/council-runtime/team.template.yaml`
    - `.agents/skills/aigc/_shared/council-runtime/module-spec.md`
    - `.agents/skills/aigc/_shared/council-runtime/CONTEXT.md`
    - `.agents/skills/aigc/SKILL.md`
    - `.agents/skills/aigc/CONTEXT.md`

## 2026-04-14

- 目录结构按最新单技能 SKILLS 口径收束为：
  - `SKILL.md`
  - `CONTEXT.md`
  - `CHANGELOG.md`
  - `agents/openai.yaml`
  - `templates/*`
- 在 [`SKILL.md`](./SKILL.md) 新增“单一真源目录合同”，明确：
  - 父 `SKILL.md` 是唯一规范真源
  - `CONTEXT.md` 只保留知识库
  - `agents/openai.yaml` 只保留入口元数据
  - `CHANGELOG.md` 只保留迁移索引
- 删除旧的 `references/advisor-council-mode/module-spec.md`、`references/fast-mode/module-spec.md`、`references/autonomous-mode/module-spec.md`。
  - 根因：这些文件已降级为历史 stub，仓内不存在有效回链，继续保留只会制造“模式子层仍在生效”的错觉。
  - 预防：后续三种初始化模式的合同、节点与 gate 一律只写回父 `SKILL.md`。
- 同步更新 `CONTEXT.md` 与 `agents/openai.yaml`，让经验层和入口元数据与当前目录形态一致。
- 同步升级初始化 runtime bootstrap skeleton：
  - 新增默认预建 `projects/aigc/<项目名>/2-Global/` 阶段根；`2-Global` 阶段执行后在根层写入四个 Markdown
  - 新增默认预建 `projects/aigc/<项目名>/3-Detail/水月/`、`镜花/`
  - 明确 `4-Design` 仍坚持 domain-first runtime，不把 `1-清单 / 2-设计 / 3-面板` 误投影成项目目录
- 同步新增项目级辅助资产库 bootstrap：
  - `projects/aigc/<项目名>/Assets/角色/`
  - `projects/aigc/<项目名>/Assets/道具/`
  - `projects/aigc/<项目名>/Assets/场景/`
  - `projects/aigc/<项目名>/Assets/服装/`
  - `projects/aigc/<项目名>/Assets/分镜画板/分镜帧/`
  - `projects/aigc/<项目名>/Assets/分镜画板/分镜故事板/`
  - `projects/aigc/<项目名>/Assets/分镜画板/漫画/`
  - 根因：初始化缺少统一资产沉淀层，容易把参考素材散落到阶段输出目录里。
- 收紧 `north_star` 真源边界：
  - 删除 `templates/north-star.template.yaml` 中的 `stage_entry_contract`
  - 在 `SKILL.md` 新增 `Stage Entry Ownership Contract`
  - 明确当前 live route truth 只属于 `STATE.json / governance-state.yaml`，初始化当轮 handoff 只属于 `init_handoff.yaml`
  - 根因：`north_star` 混入阶段路由和 `rebootstrap` 状态后，会从长期方向主物退化为状态本
  - 预防：审计脚本新增模板级禁用字段检查，样本 `north_star.yaml` 同步归一
- 新增 `benchmark-suite.yaml`，补齐 `0-Init` 的 baseline / boundary / regression 基准任务。
- 在 `SKILL.md` 补加 `Quality Evidence Source` 回链，明确 `benchmark-suite.yaml` 属于动态评测真源，而不是 `CONTEXT.md` 经验层内容。
