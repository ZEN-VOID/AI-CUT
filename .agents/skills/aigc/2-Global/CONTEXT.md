# CONTEXT.md

## Purpose & Loading Contract

- 本文件是 `aigc/2-Global` 的经验层知识库，不是过程日志。
- 调用 `.agents/skills/aigc/2-Global/SKILL.md` 时，应自动预加载本文件。
- 优先级遵循：用户显式请求 > `AGENTS.md` / 元规则 > `.agents/skills/aigc/SKILL.md` > 本 `SKILL.md` > 本 `CONTEXT.md`。

## Context Health

- soft_limit_chars: 20000
- hard_limit_chars: 40000
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
| `3-Detail` 还在临场决定每组切几镜，导致 `水月/镜花` 顺序漂移 | 跨阶段切镜规划层 | 在 `2-Global` 末段直接写入固定 `分镜切换` 数字 | 在 shared schema、seed contract 与 `2-Global/3-Detail` 双侧合同固定组级镜数由 `2-Global` 先定 | `3-Detail` 只负责按既定镜数落真实切镜，不再重判组级镜数 |
| former `镜花/1-切换` 仍作为下游独立叶子存在，导致固定镜数接受逻辑出现双真源 | 跨阶段真源治理层 | 将 fixed-shot-count 接受逻辑内化到 `2-Global` 的 `N6-GROUP-DESIGN-DISTILL`，下游只保留 `分镜构图` | 在 `2-Global/SKILL.md + group_design_seed_contract + 镜花` 双侧合同同步声明“upstream fixed count, downstream shot spine” | `镜花` 不再维护第二份切换真源 |
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
- 当 `分镜切换` 已经被证明是 `水月 + 镜花` 的共同前置时，最稳的落点不是继续塞在 `镜花` 叶子里，而是由 `2-Global` 先写组级固定镜数。
- 若 fixed-shot-count 接受逻辑已经稳定上收 `2-Global`，`3-Detail` 就不应再保留独立 `1-切换` 叶子；下游应直接把 inherited `分镜切换` 落成 `分镜构图` 的 shot spine。
- `组间设计` 的三条继承句必须先在 Markdown 用同名字段定稿，再写入 shared root；JSON 阶段若还在“临场改句子”，等于真源已经分裂。
- `剧本正文` 进入 shared root 时必须是命中组全文，而不是为了“更短更像摘要”去自行净化；下游图像和视频蒸馏都依赖这段原始组文本。
- `组间设计` 的三条继承句如果还和长文本一样长，等于 handoff 没有完成；最稳的做法是固定字符窗，把长文本解释留在 Markdown，把跨阶段第一结构化真源压到 episode root。
- 一旦 shared schema 已固定字段名 `类型元素`，`2-Global` 的模板名、Markdown 名和下游路径名也必须同名；如果上游还叫 `类型指导`，`3-Detail` 和 `4-Design` 就会被迫维护一层隐性映射。
- `类型元素.md` 一旦要写进 shared root，就必须按组组织；如果还停留在项目级总稿，JSON 写入就只能靠临时压缩，最终一定漂移。
- `全局风格` 的内部控制轴可以分析观演距离、主客观模式、炫技倾向、运镜/转场偏置、光影戏剧性、色彩振幅与母题密度，但最终提取字段不应直接写成景别、镜头距离、具体颜色、具体材质、构图术语或摄影操作。
- 若一个阶段只有内部能力面而没有稳定的外置长期 specialist roster，优先做内收型父 skill，而不是维持一个空壳 subagent 体系。
