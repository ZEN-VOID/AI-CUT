# CONTEXT.md

## Purpose & Loading Contract

- 本文件是 `aigc/2-Global` 的经验层知识库，不是过程日志。
- 调用 `.agents/skills/aigc/2-Global/SKILL.md` 时，应自动预加载本文件。
- 优先级遵循：用户显式请求 > `AGENTS.md` / 元规则 > `.agents/skills/aigc/SKILL.md` > 本 `SKILL.md` > 本 `CONTEXT.md`。

## Context Health

- soft_limit_chars: 20000
- hard_limit_chars: 40000
- status: ok
- last_checked_at: 2026-04-15

## Type Map

| failure_or_outcome_type | root_cause_layer | immediate_fix | systemic_prevention | verification_point |
| --- | --- | --- | --- | --- |
| `2-Global` 仍回指已退役的外置导演组 contracts | 能力真源层 | 将风格、类型、导演三类能力重新写回父 `SKILL.md` | 在 `SKILL.md` 固化 `Internal Capability Fusion Contract`，并让 audit 反向检查不得残留旧路径 | `2-Global` 当前合同与入口元数据不再引用导演组外置 contracts |
| 内部能力链只写“并发”，没有拆开全集类型与分组类型的依赖汇流门 | 编排拓扑层 | 增加“全集类型先锁总则、分组类型继承总则、导演意图预解构并发但最终等待三层约束”的节点设计 | 在 `Thinking-Action Node Network` 固化 `N3A/N3B/N3D` 并发、`N3B -> N3C`、`N3A/N3B/N3C -> N4 -> N5` | 并发与依赖不再互相冲突，项目级类型和组级打法不再混写 |
| 项目级风格/类型文档被 episode 内容污染 | 输出治理层 | 重新拆开项目级总则与组级增量 | 在模板与 `SKILL.md` 双重固化项目级/组级边界 | `全局风格.md`、`分组类型元素.md` 不再出现单集局部气氛杂糅 |
| `导演意图.md` 里的 `导演意图` 只剩导演口号 | 组级导演链层 | 回到 `第N集 -> 【x-x-x】 -> 剧情任务/关注焦点/情绪推进/空间压力` 粒度重写 | 在 `导演意图` 分支步骤和模板中固定最小可消费槽位 | `3-Detail` 可直接据此展开 |
| 只保留粗糙概述，没有把四个输出面各自“从哪些方面着手”写细 | 思行细化层 | 为 `全局风格 / 全集类型元素 / 分组类型元素 / 导演意图` 各写一套 branch-step 细表 | 在 `Capability Chain Detail` 中固化 GS/TB/GT/DI 步骤表 | `SKILL.md` 读起来就能直接执行，而不是继续猜 |
| 风格、全集类型、分组类型、导演意图只有抽象词，没有 `3-Detail` 可实现导向，也没有参考桥段与具像化表述 | 下游桥接层 | 在四个输出面的思行节点与模板中强制加入 `detail` 落地判断、参考作品桥段与具像化槽位 | 在 `Thinking-Action Node Network`、`Capability Chain Detail` 与四个模板同步固化 reference + bridge 审计位 | 输出能回答“参照哪段、借什么、如何落到 detail” |
| `2-Global` 只写四份 Markdown，`3-Detail` 还要再次长文本抽取 `组间设计` | 跨阶段 handoff 层 | 在 `2-Global` 末段直接把 `组间设计` seed 写入 shared episode root | 新增 shared `group_design_seed_contract`，并让 `2-Global/3-Detail` 同步回指 | `3-Detail` 可直接继承 `组间设计`，不再把四份 Markdown 当第一结构化输入 |
| `3-Detail` 还在临场决定每组切几镜，导致 `水月/镜花` 顺序漂移 | 跨阶段切镜规划层 | 在 `2-Global` 末段直接写入固定 `分镜切换` 数字 | 在 shared schema、seed contract 与 `2-Global/3-Detail` 双侧合同固定组级镜数由 `2-Global` 先定 | `3-Detail` 只负责按既定镜数落真实切镜，不再重判组级镜数 |
| 漫画/恐怖漫画或短剧/竖屏短剧项目的 `分镜切换` 被按长剧/电影低密度裁定，导致分镜数太少、紧张感或爽感不足 | 媒介-平台-类型密度裁定层 | 按 `rhythm_density_profile` 重判固定镜数：漫画看面板密度，短剧看高信息递送密度，恐怖/悬疑允许慢停顿但不能低信息密度 | 在 `SKILL.md` 的 `N6-GROUP-DESIGN-DISTILL`、`IO_CONTRACT.md` 与 shared `group_design_seed_contract` 中加入 `medium_density_check / rhythm_density_profile`，让后续项目先判媒介、平台、类型任务再裁定镜数 | `switching_rationale_note` 能说明每组镜数如何承载声效格、停顿格、反应格、钩子格、冲突升级格和局部递进格 |
| former `镜花/1-切换` 仍作为下游独立叶子存在，导致固定镜数接受逻辑出现双真源 | 跨阶段真源治理层 | 将 fixed-shot-count 接受逻辑内化到 `2-Global` 的 `N6-GROUP-DESIGN-DISTILL`，下游只保留 `分镜构图` | 在 `2-Global/SKILL.md + group_design_seed_contract + 镜花` 双侧合同同步声明“upstream fixed count, downstream shot spine” | `镜花` 不再维护第二份切换真源 |
| JSON 写入阶段重新改写 `全局风格 / 类型元素 / 导演意图`，导致 Markdown 与 shared root 漂移 | 字段提取层 | 把三类字段都改成“先在 Markdown 用同名字段定稿，再由 JSON 直接提取” | 在 `SKILL.md`、模板、seed contract 与 schema 同步固化字段标题与提取位置 | shared root 与 Markdown 不再出现双重表述 |
| `全局风格` 最终字段混入具体景别、颜色、材质或摄影操作，导致下游被错误锁死 | 风格纯度层 | 将项目级统一前缀改回“媒介属性 + 渲染技术栈 + 美学范式 + 整体质感”的无污染底层协议 | 在 `SKILL.md`、模板、shared contract、schema 示例与项目产物中同步固化无污染过滤规则 | `全局风格` 可被 `3-Detail/4-Design/5-Image/6-Video` 继承而不预锁镜头规模 |
| `剧本正文` 写入 shared root 时被摘要化 | 组壳写回层 | 强制将命中组全文完整整理入 `分镜组列表[].剧本正文`，仅移除重复组号标题 | 在 `group_design_seed_contract`、schema 与 `N6/N7` 审计中固化“完整入壳”规则 | 下游图像/视频提示词能继承完整组级文本 |
| `全集类型元素.md` 与 `分组类型元素.md` 的思维节点混在一起，导致项目级总则和组级打法互相污染 | 类型组织层 | 将 `N3B` 固定为 `全集类型元素` 总则节点，将 `N3C` 固定为继承总则的 `分组类型元素` 节点，并为每组设置字段标题 `类型元素` | 在模板、节点网络、字段映射与 `N6` type inheritance check 中固定按组提取和继承规则；在 I/O 合同禁止新输出生成旧兼容投影 | `组间设计.类型元素` 与命中组一一对应，且可追溯到 `全集类型元素.md` 的项目级规则 |
| 旧的 `subagent_brief / agents_plan` 命名仍残留在 shared I/O | I/O 合同层 | 改写为内部 `global_style_plan / type_guidance_plan / director_intent_plan / convergence_report` 命名 | 将 `_shared/IO_CONTRACT.md` 作为唯一命名真源 | 不再出现外置导演组 handoff 语义 |
| `2-Global` 源层仍残留扁平输出命名或 `1-Planning/2-剧本` 旧路径 | canonical naming/path 层 | 把主合同、入口 prompt、模板和根 skill 投影统一收束到 `全局风格.md`、`全集类型元素.md + 分组类型元素.md`、`导演意图.md` 与 `1-Planning/2-格式/第N集.md` | runtime 路径或 canonical filename 发生变化时，必须按 `shared carrier -> stage skill -> root projection -> context` 四层同步，不允许 validation-report 提前宣称完成 | `2-Global` 不再同时维护旧扁平命名和新 runtime 命名两套口径 |
| `2-Global` 实际输出仍落到目录化旧结构，和根层四文件预期不符 | canonical output carrier 层 | 将 canonical 输出收束为 `全局风格.md / 导演意图.md / 全集类型元素.md / 分组类型元素.md`，并迁移示例项目旧文件 | 在 `IO_CONTRACT.md` 禁止新输出生成旧目录与 `类型元素.md` 兼容投影；同步 `SKILL.md`、模板、bootstrap skeleton、审计脚本和下游读取 fallback | 新项目只预建 `2-Global/` 阶段根；示例项目 `2-Global` 根层存在四个 Markdown，旧目录不再作为 canonical 输出 |
| 根技能与审计脚本还把 `2-Global` 当作导演组 subagent 阶段 | 仓级治理层 | 同步更新根 `aigc/SKILL.md` 与 `scripts/aigc_skill_audit.py` | 用 `audit_global_single_skill_contract` 固化“内收能力链”审计 | 根路由、阶段状态与审计口径保持一致 |

## Repair Playbook

1. 先看 `2-Global/SKILL.md` 是否仍把全局风格、全集类型、分组类型、导演意图预解构/定稿和汇流门写在同一真源里。
2. 再看 `_shared/IO_CONTRACT.md` 与四个模板是否仍保持项目级/组级分层。
3. 再看四个输出面是否都能回答 `3-Detail` 可实现性、参考作品桥段与具像化表述，而不是只给抽象判断。
4. 再看根 `aigc/SKILL.md` 和 `scripts/aigc_skill_audit.py` 是否仍把 `2-Global` 误判成导演组 subagent 阶段。
5. 再查 shared root 的 `剧本正文` 是否完整来自命中组正文，以及 `全局风格 / 类型元素 / 导演意图` 是否都来自 Markdown 同名字段。
6. 最后才看单次文案是否需要返工。

## Reusable Heuristics

- `2-Global` 最稳的形态不是“父 skill + 外置导演组 team”，而是“单技能锁前提、项目级双链并行、分组级双链并行、统一汇流写回”。
- 对 `2-Global` 来说，并发不是四份文档同时乱写，而是风格链、全集类型链、导演意图预解构可并行推进；分组类型必须继承全集类型，最终导演意图必须等待项目级约束和组级类型稳定后再定稿。
- `全局风格` 和 `全集类型元素` 是项目级硬约束；`分组类型元素` 和 `导演意图` 是当前集按组的可消费增量。四者一旦混写，后续 `3-Detail` 就会失焦。
- `导演意图` 最忌讳空话；只要不能回答“本组最该看见什么、情绪怎么转弯、空间压力怎样服务任务”，就说明还没进入可消费状态。
- 对 `2-Global` 的高质量改造，不是改几个标题，而是把“从哪些方面着手”的专业步骤写成 branch-step 表，让 skill 自身成为执行真源。
- `2-Global` 的风格、类型、导演意图判断，必须再回答一层：“这句话怎么落到 `3-Detail` 的镜头/表演/调度/节奏上”；答不出来就说明还只是抽象口号。
- 参考作品不是只报片名，必须尽量下钻到具体桥段，并说明借鉴的是哪种处理逻辑；这样下游才知道是借镜头组织、气压控制还是信息揭示方式。
- 对 `2-Global` 来说，最稳的跨阶段 handoff 不是再让 `3-Detail` 读四份长文，而是把三条 seed 字段压成 `组间设计.全局风格 / 类型元素 / 导演意图` 直接写入 shared episode root。
- 当 `分镜切换` 已经被证明是 `水月 + 镜花` 的共同前置时，最稳的落点不是继续塞在 `镜花` 叶子里，而是由 `2-Global` 先写组级固定镜数。
- `分镜切换` 不是抽象预算数字，必须先按 `媒介形态 + 平台形态 + 类型任务` 解释：漫画项目按面板密度裁定，短剧/竖屏短剧按高信息递送密度裁定；恐怖/悬疑可以慢停顿，但停顿必须承担信息或情绪功能，否则固定镜数虽然稳定，仍会把紧张感或爽感压扁。
- 若 fixed-shot-count 接受逻辑已经稳定上收 `2-Global`，`3-Detail` 就不应再保留独立 `1-切换` 叶子；下游应直接把 inherited `分镜切换` 落成 `分镜构图` 的 shot spine。
- `组间设计` 的三条继承句必须先在 Markdown 用同名字段定稿，再写入 shared root；JSON 阶段若还在“临场改句子”，等于真源已经分裂。
- `剧本正文` 进入 shared root 时必须是命中组全文，而不是为了“更短更像摘要”去自行净化；下游图像和视频蒸馏都依赖这段原始组文本。
- `组间设计` 的三条继承句如果还和长文本一样长，等于 handoff 没有完成；最稳的做法是固定字符窗，把长文本解释留在 Markdown，把跨阶段第一结构化真源压到 episode root。
- 一旦 shared schema 已固定字段名 `类型元素`，`2-Global` 的模板名、Markdown 名和下游路径名也必须同名；如果上游还叫 `类型指导`，`3-Detail` 和 `4-Design` 就会被迫维护一层隐性映射。
- `分组类型元素.md` 一旦要写进 shared root，就必须按组组织；如果它没成为唯一组级真源，JSON 写入就只能靠临时压缩，最终一定漂移。
- `全局风格` 的内部控制轴可以分析观演距离、主客观模式、炫技倾向、运镜/转场偏置、光影戏剧性、色彩振幅与母题密度，但最终提取字段不应直接写成景别、镜头距离、具体颜色、具体材质、构图术语或摄影操作。
- 若一个阶段只有内部能力面而没有稳定的外置长期 specialist roster，优先做内收型父 skill，而不是维持一个空壳 subagent 体系。
- 一旦 runtime 真源在扁平根层文件和分目录输出之间切换，`SKILL.md`、`agents/openai.yaml`、模板、根 skill 投影、bootstrap skeleton、审计脚本和 `CONTEXT.md` 必须同轮改口径；否则 validation-report 会比源层真实状态更早“完成”。
