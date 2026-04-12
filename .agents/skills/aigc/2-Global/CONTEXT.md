# CONTEXT.md

## Purpose & Loading Contract

- 本文件是 `aigc/2-Global` 的经验层知识库，不是过程日志。
- 调用 `.agents/skills/aigc/2-Global/SKILL.md` 时，应自动预加载本文件。
- 优先级遵循：用户显式请求 > `AGENTS.md` / 元规则 > `.agents/skills/aigc/SKILL.md` > 本 `SKILL.md` > 本 `CONTEXT.md`。

## Context Health

- soft_limit_chars: 20000
- hard_limit_chars: 40000
- soft_limit_cases: 16
- hard_limit_cases: 32
- status: ok
- last_checked_at: 2026-04-12

## Type Map

| failure_or_outcome_type | root_cause_layer | immediate_fix | systemic_prevention | verification_point |
| --- | --- | --- | --- | --- |
| `2-Global` 仍回指已退役的外置导演组 contracts | 能力真源层 | 将风格、类型、导演三类能力重新写回父 `SKILL.md` | 在 `SKILL.md` 固化 `Internal Capability Fusion Contract`，并让 audit 反向检查不得残留旧路径 | `2-Global` 当前合同与入口元数据不再引用导演组外置 contracts |
| 三条链只写“并发”，没有依赖汇流门 | 编排拓扑层 | 增加“导演意图预解构并发、最终定稿等待风格/类型稳定”的节点设计 | 在 `Thinking-Action Node Network` 固化 `N3A/N3B/N3C -> N4 -> N5` | 并发与依赖不再互相冲突 |
| 项目级风格/类型文档被 episode 内容污染 | 输出治理层 | 重新拆开项目级总则与组级增量 | 在模板与 `SKILL.md` 双重固化项目级/组级边界 | `全局风格.md`、`类型指导.md` 不再出现单集局部气氛杂糅 |
| `导演意图.md` 只剩导演口号 | 组级导演链层 | 回到 `第N集 -> 【x-x-x】 -> 剧情任务/关注焦点/情绪推进/空间压力` 粒度重写 | 在 `导演意图` 分支步骤和模板中固定最小可消费槽位 | `3-Detail` 可直接据此展开 |
| 只保留粗糙概述，没有把三链各自“从哪些方面着手”写细 | 思行细化层 | 为 `全局风格 / 类型指导 / 导演意图` 各写一套 branch-step 细表 | 在 `Capability Chain Detail` 中固化 GS/TG/DI 步骤表 | `SKILL.md` 读起来就能直接执行，而不是继续猜 |
| 风格、类型、导演意图只有抽象词，没有 `3-Detail` 可实现导向，也没有参考桥段与具像化表述 | 下游桥接层 | 在三条链的思行节点与模板中强制加入 `detail` 落地判断、参考作品桥段与具像化槽位 | 在 `Thinking-Action Node Network`、`Capability Chain Detail` 与三个模板同步固化 reference + bridge 审计位 | 输出能回答“参照哪段、借什么、如何落到 detail” |
| 旧的 `subagent_brief / agents_plan` 命名仍残留在 shared I/O | I/O 合同层 | 改写为内部 `global_style_plan / type_guidance_plan / director_intent_plan / convergence_report` 命名 | 将 `_shared/IO_CONTRACT.md` 作为唯一命名真源 | 不再出现外置导演组 handoff 语义 |
| 根技能与审计脚本还把 `2-Global` 当作导演组 subagent 阶段 | 仓级治理层 | 同步更新根 `aigc/SKILL.md` 与 `scripts/aigc_skill_audit.py` | 用 `audit_global_single_skill_contract` 固化“内收能力链”审计 | 根路由、阶段状态与审计口径保持一致 |

## Repair Playbook

1. 先看 `2-Global/SKILL.md` 是否仍把三条能力链和汇流门写在同一真源里。
2. 再看 `_shared/IO_CONTRACT.md` 与三个模板是否仍保持项目级/组级分层。
3. 再看三条能力链是否都能回答 `3-Detail` 可实现性、参考作品桥段与具像化表述，而不是只给抽象判断。
4. 再看根 `aigc/SKILL.md` 和 `scripts/aigc_skill_audit.py` 是否仍把 `2-Global` 误判成导演组 subagent 阶段。
5. 最后才看单次文案是否需要返工。

## Reusable Heuristics

- `2-Global` 最稳的形态不是“父 skill + 外置导演组 team”，而是“单技能锁前提、三链并发、统一汇流写回”。
- 对 `2-Global` 来说，并发不是三份文档同时乱写，而是风格链、类型链、导演意图预解构并行推进，最终导演意图必须等待项目级约束稳定后再定稿。
- `全局风格` 和 `类型指导` 是项目级硬约束；`导演意图` 是当前集按组的可消费增量。三者一旦混写，后续 `3-Detail` 就会失焦。
- `导演意图` 最忌讳空话；只要不能回答“本组最该看见什么、情绪怎么转弯、空间压力怎样服务任务”，就说明还没进入可消费状态。
- 对 `2-Global` 的高质量改造，不是改几个标题，而是把“从哪些方面着手”的专业步骤写成 branch-step 表，让 skill 自身成为执行真源。
- `2-Global` 的风格、类型、导演意图判断，必须再回答一层：“这句话怎么落到 `3-Detail` 的镜头/表演/调度/节奏上”；答不出来就说明还只是抽象口号。
- 参考作品不是只报片名，必须尽量下钻到具体桥段，并说明借鉴的是哪种处理逻辑；这样下游才知道是借镜头组织、气压控制还是信息揭示方式。
- 若一个阶段只有内部能力面而没有稳定的外置长期 specialist roster，优先做内收型父 skill，而不是维持一个空壳 subagent 体系。

## Case Log

### Case-20260412-AIGC-GLOBAL-ZHI-XING-INTERNALIZATION

- milestone_type: source_contract_change
- outcome: 将 `2-Global` 从“父 skill + 外置导演组 contracts”重构为知行合一的单技能并发链。
- root_cause_or_design_decision: 用户明确要求“内容和机制上全量参照现有配置，但根据知行合一的规范进行编排”，并指出 `.codex/agents/aigc/导演组` 不再需要。现有 `2-Global` 的能力内容可复用，但真源分裂在父 skill、team、共享方法和三个角色文档之间，不适合继续维护。
- final_fix_or_heuristic: 保留三份 canonical Markdown、模板口径、项目级/组级分层与下游 handoff 不变，只把机制改成 `Business Requirement Analysis -> Internal Capability Fusion -> Parallel Three-Chain Topology -> Convergence Audit -> One-Shot Output` 的单技能网络，并为 `全局风格 / 类型指导 / 导演意图` 分别补齐细致 branch-step 表。
- prevention_or_replication_checklist:
  - [x] `2-Global/SKILL.md` 已显式内收三条能力链
  - [x] `_shared/IO_CONTRACT.md` 已移除旧的导演组 handoff 命名
  - [x] `agents/openai.yaml` 已改为内部并发链入口摘要
  - [x] 根 `aigc/SKILL.md` 与审计脚本已同步改口
  - [x] 已退役的导演组外置 contracts 已退出当前执行真源
- evidence_paths:
  - `.agents/skills/aigc/2-Global/SKILL.md`
  - `.agents/skills/aigc/2-Global/CONTEXT.md`
  - `.agents/skills/aigc/2-Global/_shared/IO_CONTRACT.md`
  - `.agents/skills/aigc/2-Global/templates/全局风格.template.md`
  - `.agents/skills/aigc/2-Global/templates/类型指导.template.md`
  - `.agents/skills/aigc/2-Global/templates/导演意图.template.md`
  - `.agents/skills/aigc/2-Global/agents/openai.yaml`
  - `.agents/skills/aigc/SKILL.md`
  - `scripts/aigc_skill_audit.py`
- user_feedback_or_constraint: 用户明确要求将导演组外置智能体能力重新整理并融合回 `SKILL.md` 中，同时强调这是一个典型并发链，三条链都要写得足够细致和高品质。

### Case-20260412-AIGC-GLOBAL-DETAIL-BRIDGE

- milestone_type: source_contract_change
- outcome: 为 `2-Global` 三条能力链补入 `3-Detail` 可实现性、参考作品桥段与具像化表述的强制判断位。
- root_cause_or_design_decision: 用户指出现有“思维·执行”节点虽然有风格、类型、导演意图三条链，但还缺少一层关键导演判断：这些判断是否真的能指导后续 `3-Detail`，以及是否能用明确作品桥段和具像化语言把抽象风格钉住。
- final_fix_or_heuristic: 在 `Thinking-Action Node Network` 中给 `N3A/N3B/N3C/N4/N5/N6` 增加 reference + bridge 审计；在 `Capability Chain Detail` 中为三条链加入“参考桥段 / 具像化表述 / 对 `3-Detail` 的落地指导”；在三个模板里补固定槽位。
- prevention_or_replication_checklist:
  - [x] `SKILL.md` 已把 `detail` 落地判断写进思行节点和 pass gate
  - [x] `全局风格.template.md` 已补参考桥段与具像化槽位
  - [x] `类型指导.template.md` 已补参考桥段与具像化槽位
  - [x] `导演意图.template.md` 已补组级 reference + detail 导向槽位
  - [x] `CONTEXT.md` 已沉淀“只给抽象词不够，必须给 reference + bridge”启发式
- evidence_paths:
  - `.agents/skills/aigc/2-Global/SKILL.md`
  - `.agents/skills/aigc/2-Global/templates/全局风格.template.md`
  - `.agents/skills/aigc/2-Global/templates/类型指导.template.md`
  - `.agents/skills/aigc/2-Global/templates/导演意图.template.md`
  - `.agents/skills/aigc/2-Global/CONTEXT.md`
- user_feedback_or_constraint: 用户要求对 `.agents/skills/aigc/2-Global` 的“思维·执行”节点加入两类判断细节：一是对后续 `detail` 是否具有可实现的指导意义，二是可参照哪部作品的哪个桥段，以及对应风格的具像化表述。
