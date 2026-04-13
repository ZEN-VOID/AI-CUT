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
| 多模式初始化被写成重复问卷 | 模式合同层 | 把元选项收口到 `Initialization Mode Contract` 单一入口 | 模式锁定后只命中 1 条内部模式路径 | 全文只有一个合法模式展示位 |
| `north_star` 与 handoff 混成一个大杂烩 | 主文件分工层 | 将长期约束留在 `north_star.yaml`，阶段种子与 unknowns 放入 `init_handoff.yaml` | 用模板真源固定两份文件的字段边界 | 模板与最终落盘能看出清晰分工 |
| 顾问团只有共享名单，没有角色职责真源 | 团队治理层 | 生成项目根 `team.yaml`，把顾问写成 `策划 / 监制 / 评审` 三角色而非平铺列表 | 用 `.agents/skills/aigc/_shared/council-runtime/team.template.yaml` 固化角色、作用阶段与评审最终闸门 | 后续阶段能按角色读取顾问团队，而不是回猜 |
| 工件落盘漂向旧路径或外仓 | 路径合同层 | 固定到 `projects/<项目名>/0-Init/` 与项目根 | 在根 `aigc` 与 `0-Init` 双层合同中同时声明 canonical landing | 全部初始化工件都位于当前仓库项目路径 |
| 初始化目录骨架未跟随当前 active 子路径 | runtime skeleton 合同层 | 把初始化目录约定升级为“阶段根目录 + active child skeleton” | 让 `0-Init`、`_shared/project-runtime-layout.md` 与 `aigc_skill_audit.py` 共用同一套 bootstrap skeleton | 初始化合同、shared layout 与审计 marker 同步 |
| `project_state.yaml`、`route-plan.yaml` 与 `north_star` 给出不同下一步 | 阶段入口同步层 | 先以 `north_star.stage_entry_contract.stage_priority_order` 为主，回写项目状态与 handoff 到同一入口 | 在 `Sufficiency Gate` 中新增“下一步建议一致性”校验 | 读取三处工件时只能得到一个当前主入口 |
| 项目进入规划前没有故事主源登记 | 共享输入真源层 | 固定生成 `story-source-manifest.yaml`，区分 `primary_story_source` 与 `development_briefs` | 将故事源落点与缺失提示上收到 `_shared/story-source-contract.md` | 初始化完成后，能立刻判断 `1-分集` 是否具备增量进入条件与整季完成条件 |
| 续跑与状态查询无法稳定重建断点 | 项目治理快照层 | 在需要时生成 `governance-state.yaml` | 用 shared template 固定 `last_stable_checkpoint + resume_contract + artifact_status` | `query / resume / review` 能从同一份结构化快照读取断点与缺口 |
| 创作起盘被整套治理工件压得过重 | 初始化分层合同 | 把首次必出收敛到 `north_star / init_handoff / story-source-manifest / team / project_state` | 将 `governance-state + harness carriers` 改为惰性生成 | 首次初始化不再被非必要治理载体阻塞 |
| 路由、模式执行、充分性检查散落在外部规则真源 | 源层编排层 | 将这些能力完全吸收到父 `SKILL.md` 的内部能力合同与节点网络 | 审计脚本反向约束 `0-Init` 不得再引用 `.codex/agents/aigc/初始组/*.md` | `0-Init` 能仅凭自身 `SKILL.md` 解释完整执行链 |
| 初始化预建目录看起来与当前技能树“不匹配” | 真源口径混层 | 明确区分“技能树执行层”与“项目 runtime 落盘层”两套命名 | 在 `_shared/project-runtime-layout.md` 建立 `Skill Tree To Runtime Mapping`，并在 `0-Init/SKILL.md` 同步注明 `5-Image / 6-Video` 的映射 | 读者不会再把 `1-提示词蒸馏/全能参照` 误读成必须预建 `projects/<项目名>/6-Video/1-提示词蒸馏/全能参照/` |
| 把推荐模式当成已锁定模式 | mode gate contract | 回到 `Initialization Mode Contract`，补发初始化元选项卡并等待用户确认 | 在 `SKILL.md` 明确“默认展示项/推荐项 != mode_lock_note”，并用审计脚本拦截歧义表述 | 仅有项目名或极简 brief 时，不再越权进入 `fast_draft_engine` 或其他模式引擎 |
| 缺故事源时先生成了剧情级预设，后补故事源也不回刷 | source completeness / reconciliation 层 | 将缺故事源初始化降级为 `source-light bootstrap`，并在故事源后补时强制回刷 `north_star / init_handoff / project_state` | 在 `SKILL.md` 固化 `Story Source Completeness Gate + Story Source Reconciliation Contract`，审计脚本同步检查 | 不再出现“题眼推断版剧情”覆盖真实故事源的情况 |

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
- 当前仓库的初始化落点必须优先服从 `projects/<项目名>/`，而不是借用其他项目系的 state/layout。
- 初始化阶段如果已经知道后续 runtime 分区，就应优先同时预落“阶段根目录 + active child skeleton”。
- 只要某工件会被多个兄弟阶段长期共同消费，就不该继续挂在 `0-Init/` 名下；最稳的做法是提升到项目根。
- 对长期维护的可执行技能目录，除 `SKILL.md + CONTEXT.md` 外，还应补齐 `agents/openai.yaml`。
- 当快速模式只收到一个极简概念时，优先把项目先定为概念短片或概念预告级规模，并把高分叉问题放进 `unknowns`。
- 只要用户没有明确要求“贴原作/保原顺序/保留原作节奏”，`original_adherence` 就应显式落盘为 `false`。
- 如果项目后续要做 `1-分集`，最稳的初始化习惯不是先问“要不要分几集”，而是先把“故事主源在哪、是否完整、能否正式切分”写进 `story-source-manifest.yaml`。
- 只要 `north_star` 已经写出 `stage_priority_order`，就不要再让 `project_state` 或 `route-plan` 各自重写一版“下一步”。
- 对创作起盘来说，最小闭环应先保证 `north_star / init_handoff / story-source-manifest / team / project_state`；其余治理载体只有在复杂执行或卫星技能真正需要时再补。
- 对 `知行合一` 编排的 `0-Init`，最稳的写法不是再造第二份思考文档，而是把路由、三种模式和充分性审计直接写进同一份父 `SKILL.md`。
- 当技能树有中间 tranche，但项目 runtime 只接受业务语义落盘名时，必须优先相信 `_shared/project-runtime-layout.md`，并在阶段合同里把两套命名的映射写明；否则读者会把“技能目录现状”误当成“项目预建目录”。
- 在 `0-Init` 里，`自主问答模式（默认）` 是前台选项卡的默认建议，不是无确认自动锁模；只要用户没拍板且不存在强制路由信号，就必须停在 `N1-mode-gate`。
- `0-Init` 可以在缺故事源时初始化项目，但只能生成题材级、边界级、生产级约束；凡是剧情级、单集级、人物关系级推断，都应降级为 provisional unknowns。
- 一旦真实故事源后补进入 `Story/`，优先动作不是继续下游阶段，而是先回刷 `north_star / init_handoff / project_state` 中的 assistant-inferred 剧情字段。

## Archive Index

- 详细迁移线索已外置到 [`CHANGELOG.md`](./CHANGELOG.md)。
- 已归档的 subagent-era 迁移材料只保留在历史变更说明中，不再作为现行执行真源。
