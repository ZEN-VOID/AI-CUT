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
| 项目级风格/类型文档被 episode 内容污染 | 输出治理层 | 重新拆开项目级总则与组级增量 | 在模板与 `SKILL.md` 双重固化项目级/组级边界 | `全局风格.md`、`类型元素.md` 不再出现单集局部气氛杂糅 |
| `导演意图.md` 只剩导演口号 | 组级导演链层 | 回到 `第N集 -> 【x-x-x】 -> 剧情任务/关注焦点/情绪推进/空间压力` 粒度重写 | 在 `导演意图` 分支步骤和模板中固定最小可消费槽位 | `3-Detail` 可直接据此展开 |
| 只保留粗糙概述，没有把三链各自“从哪些方面着手”写细 | 思行细化层 | 为 `全局风格 / 类型元素 / 导演意图` 各写一套 branch-step 细表 | 在 `Capability Chain Detail` 中固化 GS/TG/DI 步骤表 | `SKILL.md` 读起来就能直接执行，而不是继续猜 |
| 风格、类型、导演意图只有抽象词，没有 `3-Detail` 可实现导向，也没有参考桥段与具像化表述 | 下游桥接层 | 在三条链的思行节点与模板中强制加入 `detail` 落地判断、参考作品桥段与具像化槽位 | 在 `Thinking-Action Node Network`、`Capability Chain Detail` 与三个模板同步固化 reference + bridge 审计位 | 输出能回答“参照哪段、借什么、如何落到 detail” |
| `2-Global` 只写三份 Markdown，`3-Detail` 还要再次长文本抽取 `组间设计` | 跨阶段 handoff 层 | 在 `2-Global` 末段直接把 `组间设计` seed 写入 shared episode root | 新增 shared `group_design_seed_contract`，并让 `2-Global/3-Detail` 同步回指 | `3-Detail` 可直接继承 `组间设计`，不再把三份 Markdown 当第一结构化输入 |
| JSON 写入阶段重新改写 `全局风格 / 类型元素 / 导演意图`，导致 Markdown 与 shared root 漂移 | 字段提取层 | 把三类字段都改成“先在 Markdown 用同名字段定稿，再由 JSON 直接提取” | 在 `SKILL.md`、模板、seed contract 与 schema 同步固化字段标题与提取位置 | shared root 与 Markdown 不再出现双重表述 |
| `全局风格` 最终字段混入具体景别、颜色、材质或摄影操作，导致下游被错误锁死 | 风格纯度层 | 将项目级统一前缀改回“媒介属性 + 渲染技术栈 + 美学范式 + 整体质感”的无污染底层协议 | 在 `SKILL.md`、模板、shared contract、schema 示例与项目产物中同步固化无污染过滤规则 | `全局风格` 可被 `3-Detail/4-Design/5-Image/6-Video` 继承而不预锁镜头规模 |
| `剧本正文` 写入 shared root 时被摘要化 | 组壳写回层 | 强制将命中组全文完整整理入 `分镜组列表[].剧本正文`，仅移除重复组号标题 | 在 `group_design_seed_contract`、schema 与 `N6/N7` 审计中固化“完整入壳”规则 | 下游图像/视频提示词能继承完整组级文本 |
| `类型元素.md` 仍按项目级总稿组织，导致 JSON 无法按组准确提取 | 类型组织层 | 将 `类型元素.md` 改成按 `第N集 -> 【x-x-x】` 组织，并为每组设置字段标题 `类型元素` | 在模板、节点网络与字段映射中固定按组提取规则 | `组间设计.类型元素` 与命中组一一对应 |
| 旧的 `subagent_brief / agents_plan` 命名仍残留在 shared I/O | I/O 合同层 | 改写为内部 `global_style_plan / type_guidance_plan / director_intent_plan / convergence_report` 命名 | 将 `_shared/IO_CONTRACT.md` 作为唯一命名真源 | 不再出现外置导演组 handoff 语义 |
| 根技能与审计脚本还把 `2-Global` 当作导演组 subagent 阶段 | 仓级治理层 | 同步更新根 `aigc/SKILL.md` 与 `scripts/aigc_skill_audit.py` | 用 `audit_global_single_skill_contract` 固化“内收能力链”审计 | 根路由、阶段状态与审计口径保持一致 |

## Repair Playbook

1. 先看 `2-Global/SKILL.md` 是否仍把三条能力链和汇流门写在同一真源里。
2. 再看 `_shared/IO_CONTRACT.md` 与三个模板是否仍保持项目级/组级分层。
3. 再看三条能力链是否都能回答 `3-Detail` 可实现性、参考作品桥段与具像化表述，而不是只给抽象判断。
4. 再看根 `aigc/SKILL.md` 和 `scripts/aigc_skill_audit.py` 是否仍把 `2-Global` 误判成导演组 subagent 阶段。
5. 再查 shared root 的 `剧本正文` 是否完整来自命中组正文，以及 `全局风格 / 类型元素 / 导演意图` 是否都来自 Markdown 同名字段。
6. 最后才看单次文案是否需要返工。

## Reusable Heuristics

- `2-Global` 最稳的形态不是“父 skill + 外置导演组 team”，而是“单技能锁前提、三链并发、统一汇流写回”。
- 对 `2-Global` 来说，并发不是三份文档同时乱写，而是风格链、类型链、导演意图预解构并行推进，最终导演意图必须等待项目级约束稳定后再定稿。
- `全局风格` 和 `类型元素` 是项目级硬约束；`导演意图` 是当前集按组的可消费增量。三者一旦混写，后续 `3-Detail` 就会失焦。
- `导演意图` 最忌讳空话；只要不能回答“本组最该看见什么、情绪怎么转弯、空间压力怎样服务任务”，就说明还没进入可消费状态。
- 对 `2-Global` 的高质量改造，不是改几个标题，而是把“从哪些方面着手”的专业步骤写成 branch-step 表，让 skill 自身成为执行真源。
- `2-Global` 的风格、类型、导演意图判断，必须再回答一层：“这句话怎么落到 `3-Detail` 的镜头/表演/调度/节奏上”；答不出来就说明还只是抽象口号。
- 参考作品不是只报片名，必须尽量下钻到具体桥段，并说明借鉴的是哪种处理逻辑；这样下游才知道是借镜头组织、气压控制还是信息揭示方式。
- 对 `2-Global` 来说，最稳的跨阶段 handoff 不是再让 `3-Detail` 读三份长文，而是把三条判断压成 `组间设计.全局风格 / 类型元素 / 导演意图` 直接 seed 到 shared episode root。
- `组间设计` 的三条继承句必须先在 Markdown 用同名字段定稿，再写入 shared root；JSON 阶段若还在“临场改句子”，等于真源已经分裂。
- `剧本正文` 进入 shared root 时必须是命中组全文，而不是为了“更短更像摘要”去自行净化；下游图像和视频蒸馏都依赖这段原始组文本。
- `组间设计` 的三条继承句如果还和长文本一样长，等于 handoff 没有完成；最稳的做法是固定字符窗，把长文本解释留在 Markdown，把跨阶段第一结构化真源压到 episode root。
- 一旦 shared schema 已固定字段名 `类型元素`，`2-Global` 的模板名、Markdown 名和下游路径名也必须同名；如果上游还叫 `类型指导`，`3-Detail` 和 `4-Design` 就会被迫维护一层隐性映射。
- `类型元素.md` 一旦要写进 shared root，就必须按组组织；如果还停留在项目级总稿，JSON 写入就只能靠临时压缩，最终一定漂移。
- `全局风格` 的内部控制轴可以分析观演距离、主客观模式、炫技倾向、运镜/转场偏置、光影戏剧性、色彩振幅与母题密度，但最终提取字段不应直接写成景别、镜头距离、具体颜色、具体材质、构图术语或摄影操作。
- 若一个阶段只有内部能力面而没有稳定的外置长期 specialist roster，优先做内收型父 skill，而不是维持一个空壳 subagent 体系。

## Case Log

### Case-20260412-AIGC-GLOBAL-ZHI-XING-INTERNALIZATION

- milestone_type: source_contract_change
- outcome: 将 `2-Global` 从“父 skill + 外置导演组 contracts”重构为知行合一的单技能并发链。
- root_cause_or_design_decision: 用户明确要求“内容和机制上全量参照现有配置，但根据知行合一的规范进行编排”，并指出 `.codex/agents/aigc/导演组` 不再需要。现有 `2-Global` 的能力内容可复用，但真源分裂在父 skill、team、共享方法和三个角色文档之间，不适合继续维护。
- final_fix_or_heuristic: 保留三份 canonical Markdown、模板口径、项目级/组级分层与下游 handoff 不变，只把机制改成 `Business Requirement Analysis -> Internal Capability Fusion -> Parallel Three-Chain Topology -> Convergence Audit -> One-Shot Output` 的单技能网络，并为 `全局风格 / 类型元素 / 导演意图` 分别补齐细致 branch-step 表。
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
  - `.agents/skills/aigc/2-Global/templates/类型元素.template.md`
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
  - [x] `类型元素.template.md` 已补参考桥段与具像化槽位
  - [x] `导演意图.template.md` 已补组级 reference + detail 导向槽位
  - [x] `CONTEXT.md` 已沉淀“只给抽象词不够，必须给 reference + bridge”启发式
- evidence_paths:
  - `.agents/skills/aigc/2-Global/SKILL.md`
  - `.agents/skills/aigc/2-Global/templates/全局风格.template.md`
  - `.agents/skills/aigc/2-Global/templates/类型元素.template.md`
  - `.agents/skills/aigc/2-Global/templates/导演意图.template.md`
  - `.agents/skills/aigc/2-Global/CONTEXT.md`
- user_feedback_or_constraint: 用户要求对 `.agents/skills/aigc/2-Global` 的“思维·执行”节点加入两类判断细节：一是对后续 `detail` 是否具有可实现的指导意义，二是可参照哪部作品的哪个桥段，以及对应风格的具像化表述。

### Case-20260412-AIGC-GLOBAL-GROUP-DESIGN-SEED

- milestone_type: source_contract_change
- outcome: 将 `2-Global` 的阶段末段从“只写三份 Markdown”升级为“写三份 Markdown + seed shared episode root 的分镜组壳与 `组间设计`”。
- root_cause_or_design_decision: 用户明确指出，`3-Detail` 不应再从三份长文本里二次抽取 `全局风格 / 类型元素 / 导演意图`，而应直接继承与自己同模版的 episode JSON；这暴露出旧合同虽然能写长文，但缺少跨阶段第一结构化 handoff。
- final_fix_or_heuristic: 新增 shared `group_design_seed_contract`，并在 `2-Global` 中加入 `group_design_distill_engine`；固定 shared root 先写 `分镜组ID / 总时长 / 剧本正文 / 组间设计` 的分镜组壳，再把 `全局风格 <= 220`、`类型元素 <= 50`、`导演意图 <= 100` 的已确认字段直接提取进 shared episode root。
- prevention_or_replication_checklist:
  - [x] `_shared/group_design_seed_contract.md` 已建立
  - [x] shared schema 已允许 `2-Global` 阶段写入完整分镜组壳与 `组间设计`
  - [x] `2-Global/SKILL.md` 已加入 `group_design_distill_engine`
  - [x] `2-Global/_shared/IO_CONTRACT.md` 已固定字符窗与 shared root 写回边界
- evidence_paths:
  - `.agents/skills/aigc/_shared/group_design_seed_contract.md`
  - `.agents/skills/aigc/_shared/director_episode_output.schema.json`
  - `.agents/skills/aigc/2-Global/SKILL.md`
  - `.agents/skills/aigc/2-Global/_shared/IO_CONTRACT.md`
  - `.agents/skills/aigc/_shared/project-runtime-layout.md`
- user_feedback_or_constraint: 用户明确要求“2-Global 开始就应该有和 3-Detail 同模版的总输出，并在末段设定写入/蒸馏细则；3-Detail 直接继承 JSON，而不是再读三份 MD。”

### Case-20260412-AIGC-GLOBAL-MD-DIRECT-EXTRACTION

- milestone_type: source_contract_change
- outcome: 将 `2-Global` 的 JSON 写回逻辑改为“Markdown 先定稿，shared root 只对照字段标题直接提取”，并把 `类型元素.md` 调整为按分镜组组织。
- root_cause_or_design_decision: 用户明确要求三类字段不要在写 JSON 时再次改写，同时补充指出 `类型元素.md` 也应与 `导演意图.md` 一样按分镜组组织；这说明旧合同仍残留“Markdown 是长文解释、JSON 再次压写”的双真源风险。
- final_fix_or_heuristic: 在 `SKILL.md` 的 `N4/N6/N7`、三个模板、`group_design_seed_contract` 与 shared schema 中统一固化三类字段标题与提取位置；`全局风格.md` 负责项目级统一风格前缀，`类型元素.md` 与 `导演意图.md` 都按 `第N集 -> 【组ID】` 定稿，JSON 只提取同名字段；同时把 `剧本正文` 固定为命中组全文入壳。
- prevention_or_replication_checklist:
  - [x] `类型元素.template.md` 已改为按组组织并带 `- 类型元素：`
  - [x] `导演意图.template.md` 已固定 `- 导演意图：`
  - [x] `全局风格.template.md` 已固定 `- 全局风格：` 作为项目级统一风格前缀
  - [x] `group_design_seed_contract.md` 已写明 JSON 只直接提取字段内容
  - [x] `director_episode_output.schema.json` 已同步字段描述与全局风格字符窗
- evidence_paths:
  - `.agents/skills/aigc/2-Global/SKILL.md`
  - `.agents/skills/aigc/2-Global/templates/全局风格.template.md`
  - `.agents/skills/aigc/2-Global/templates/类型元素.template.md`
  - `.agents/skills/aigc/2-Global/templates/导演意图.template.md`
  - `.agents/skills/aigc/_shared/group_design_seed_contract.md`
  - `.agents/skills/aigc/_shared/director_episode_output.schema.json`
- user_feedback_or_constraint: 用户要求“类型元素.md 也按分镜组为单位；再次检查 json 写入时的引用字段位置；对应的思维·执行节点及相关 mermaid 图标也更新一下”。

### Case-20260412-AIGC-GLOBAL-TYPE-ELEMENTS-RENAMING

- milestone_type: source_contract_change
- outcome: 将 `2-Global` 的类型文档 canonical 名从 `类型指导` 统一为 `类型元素`，并同步到模板、输出路径、共享 schema 与下游读取合同。
- root_cause_or_design_decision: 用户指出 shared schema 里的组级字段已经固定叫 `类型元素`，但 `2-Global` 长文档仍叫 `类型指导`；这会把本该显式的真源关系退化成隐性二次映射，增加 handoff 漂移风险。
- final_fix_or_heuristic: 把 `projects/<项目名>/2-Global/类型元素.md` 设为唯一 canonical 名，模板同步重命名为 `类型元素.template.md`，并将根 skill、`3-Detail`、`4-Design`、设计组 agent docs 与审计脚本的引用统一到同一名称。
- prevention_or_replication_checklist:
  - [x] `2-Global` 模板与输出路径已统一为 `类型元素`
  - [x] shared schema 与 shared contract 的字段/来源名已对齐
  - [x] `3-Detail` 与 `4-Design` 的输入合同已改读 `类型元素.md`
  - [x] 审计脚本已同步新的模板文件名
- evidence_paths:
  - `.agents/skills/aigc/2-Global/SKILL.md`
  - `.agents/skills/aigc/2-Global/_shared/IO_CONTRACT.md`
  - `.agents/skills/aigc/2-Global/templates/类型元素.template.md`
  - `.agents/skills/aigc/_shared/director_episode_output.schema.json`
  - `.agents/skills/aigc/_shared/project-runtime-layout.md`
  - `scripts/aigc_skill_audit.py`
- user_feedback_or_constraint: 用户明确要求“最大隐患是 schema 里叫 类型元素，但 2-Global 文档叫 类型指导，统一为类型元素”。

### Case-20260413-AIGC-GLOBAL-STYLE-PURITY

- milestone_type: source_contract_change
- outcome: 将 `全局风格` 从带景别/摄影偏置的导演说明，收束为项目级无污染底层风格协议；当前项目 `2049退休老头的快乐生活` 的统一前缀已同步去掉“中近景观察式摄影优先”。
- root_cause_or_design_decision: 用户指出当前 `全局风格` 把“中近景观察式摄影优先”写进了项目级统一前缀，这会把后续 `3-Detail` 锁死在特定景别与镜头规模上；根因是旧合同没有明确区分“控制轴内部判断”和“最终字段可见输出”。
- final_fix_or_heuristic: 把媒介属性、渲染技术栈、美学范式、控制轴与无污染过滤拆分进 `SKILL` 与模板；控制轴保留在思维·执行节点内部使用，最终 `- 全局风格：` 只保留可被各下游无污染继承的统一风格前缀。
- prevention_or_replication_checklist:
  - [x] `SKILL.md` 已明确全局风格最终字段默认禁止景别、具体颜色、材质、构图术语与摄影操作词
  - [x] `全局风格.template.md` 已拆出“项目级控制轴（内部分析）”与“无污染过滤规则”
  - [x] `_shared/IO_CONTRACT.md` 与 `group_design_seed_contract.md` 已同步无污染要求
  - [x] shared schema 示例与当前项目 root 已更新新的无污染前缀
- evidence_paths:
  - `.agents/skills/aigc/2-Global/SKILL.md`
  - `.agents/skills/aigc/2-Global/templates/全局风格.template.md`
  - `.agents/skills/aigc/2-Global/_shared/IO_CONTRACT.md`
  - `.agents/skills/aigc/_shared/group_design_seed_contract.md`
  - `.agents/skills/aigc/_shared/director_episode_output.schema.json`
  - `projects/2049退休老头的快乐生活/2-Global/全局风格.md`
  - `projects/2049退休老头的快乐生活/3-Detail/第1集.json`
- user_feedback_or_constraint: 用户明确要求“全局风格中不要固定中近景观察式摄影优先；要把旧版全局风格设计中的精华重新融合，并明确哪些进入 SKILL 整体规则面、哪些强化思维·执行节点，最终输出仍符合字数。”
