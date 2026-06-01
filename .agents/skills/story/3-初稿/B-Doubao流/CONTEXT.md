# CONTEXT.md

## Context Health

- soft_limit_chars: 40000
- hard_limit_chars: 80000
- soft_limit_cases: 80
- hard_limit_cases: 140
- status: ok

## Type Map

| failure_or_outcome_type | root_cause_layer | immediate_fix | systemic_prevention | verification_point |
| --- | --- | --- | --- | --- |
| 明明是按章直写，却仍回写到平铺 `3-初稿/第N章.md` | runtime path contract | 改回 `projects/story/<项目名>/3-初稿/第N卷/第N章.md` | 在 `3-初稿/B-Doubao流/SKILL.md`、桥接脚本与 registry 路由同时固定 canonical 输出路径 | 正文不会再漂到平铺旧路径 |
| 只读三层 planning，没读north_star 全局/风格/类型契约 | context pack contract | 回补 `0-初始化/north_star.yaml` 的 `global_contract`、`style_contract` 与 `genre_contract` | 把完整上下文加载与 sidecar 证据链作为硬门槛，YAML 头只保留 `写作模型` 与 `字数` | sidecar 中三类上下文齐备，正文能读出吸收痕迹 |
| 合同要求全局卡/风格卡，但新项目没有实体卡目录，脚本因此空载 | global/style truth carrier mismatch | 从 `north_star.yaml.global_contract/style_contract/genre_contract` 抽取等价真源；若实体卡目录存在再额外并入 | 不把实体卡目录当唯一真源，初始化新项目默认以 north_star 承接全局/风格/题材合同 | messages pack 同时出现 north_star 三类契约；有实体卡时出现卡摘录 |
| `types/网文/<题材>/` 存在但没有进入 Doubao messages | type package injection gap | 按 `north_star.genre_contract`、章节 planning 和用户约束匹配题材包并注入 messages | dry-run summary 暴露 `type_package_refs`；正式调用无法识别题材包时阻断 | messages pack 中含题材类型包固定上下文 |
| 项目有 `CONTEXT/`，但 drafting 完全没加载 | project context loading | 补读相关 `CONTEXT` 文件并记录到 sidecar | 固定“存在则按相关性加载，不存在才留空” | sidecar 中 `project_context_refs` 与真实上下文一致 |
| 把同卷前文当成硬阻塞门，当前卷无前序章就停工 | continuity policy | 改成“同卷前文增强输入，planning 是兜底硬输入” | 在 skill 合同写死“same-volume priors optional, planning mandatory” | 当前卷无前序章时，本章仍可开写 |
| 只加载最近上一章，导致同卷早前事实、伏笔、线索、道具流向、卷目标完成度、任务连续性或悬疑节奏把控性断裂 | same-volume continuity underload | 加载当前卷内所有已存在且早于目标章的正文，并把最近前章末尾摘录单独置入 provider prompt | 将“上一章正文”升级为“同卷前文连续性桥”，并在 dry-run summary 暴露 `previous_chapter_refs` | messages pack 中能看到同卷前文逐章摘录；正文开章能读出同卷前文之后的下一步 |
| `3-初稿` 看起来命中正确，但实际创作仍由本地 GPT 会话直接写出 | provider route drift | 改成通过 `write_chapter_via_doubao.py` 调用 AnyFast 豆包，再写回业务根稿 | 在主合同里写死“actual creative step = Doubao provider”，并为脚本增加 dry-run / 校验 / writeback 路径 | provider 报告、messages pack 与写回文件能互相对上 |
| GPT 监制意见只停在口头，没有进入豆包 prompt | supervision packet drop | 把 subagents 汇流为 `supervision_packet`，通过 `--supervision-packet` 注入 messages pack | B lane 固定 GPT 为监制层、Doubao 为执行层；脚本记录 `supervision_packet_ref` | messages JSON 中含监制包；最终正文仍有 Doubao provider 证据 |
| 监制包未按项目 `team.yaml` 已指定监制组请教，只给泛泛创作建议 | project team consultation gap | 读取 `roles.production.members`，为每位相关大师提出具体问题并汇流可执行指导 | 监制包固定 `project_team_ref / consultations / executable_guidance` 字段 | Doubao messages 含可追溯的请教式监制包 |
| 豆包返回了正文，但缺 frontmatter / 标题行 / 必需字段，仍被直接写回 | provider output validation | 在写回前增加 frontmatter / heading / required marker 校验 | 将 provider output validation 固化到 bridge script，而不是靠人工肉眼兜底 | 非法输出会在写回前被阻断 |
| `north_star_chapter_brief` 直接复制 `north_star.yaml` 大段原文 | summary synthesis | 不再要求正文 YAML 重复 north-star 摘要，改由 provider 上下文消费 | 固定“上下文吸收在正文体现，证据在 sidecar 体现” | 正文对齐 north-star，但头部不复述 |
| frontmatter 变成大段资料转储，压过正文 | metadata density | 从正文 YAML 头移除重复上下文字段 | 固定正文 YAML 头只保留 `写作模型` 与 `字数`，引用和摘要留在 sidecar | YAML 头极简，正文 token 留给 prose |
| 正文主体仍沿用 planning 标题句法 | prose conversion | 把 `本章冲突 / 任务线 / 规避` 转译成人物行动、局势压力和章末牵引 | 在 skill 中固定“planning 只给蓝图，不得原样落成正文” | 正文读起来像小说，不像设计文档 |
| 正文出现 `第6章的二人组`、`上一章`、`本章` 等破次元标签 | narrative-perspective leak | 把章节/流程标签改成叙事内事件称呼，如“礁链那两个追杀手”“潮汊村寨那三人” | system prompt 与 validator 固定“叙事内视角完整性”，禁止章节编号和执行流程词进入正文 | 写回前阻断正文中的章节标签、流程标签和 evidence 层词 |
| 角色对白同质化，所有人物都用同一种冷静说明腔 | character voice under-specified | 从角色卡抽取 `voice_and_presence` 形成“角色对白声纹表”，并要求每句对白承担角色意图 | prompt 固定导入声纹表；对白必须按身份、关系、情绪和利益差异化 | messages pack 中存在声纹表；抽查同场对话能不看话标区分说话人 |
| `不是……是……` 句式高频重复，解释感生硬 | sentence-pattern loop | 在 system prompt 中把该句式降为偶发关键反转用法，并在 validator 中设置上限 | 生成前给替代表达路径：动作、感官、比喻、反问、停顿、误读修正或角色化口语 | validator 统计该句式不超过上限；正文不连续使用同一解释框架 |
| Skill 2.0 升级后 `SKILL.md` 又重新堆满执行细则 | skill package ownership drift | 把长细则下沉到 `references/steps/types/review/knowledge-base`，入口只留路由与门禁 | 在 `Reference Loading Guide` 中固定每个 owner 的读取时机 | 根 `SKILL.md` 能独立回答输入和输出，但不复制分区全文 |
| Skill 2.0 交付态 validator 报缺 guardrails、Output Contract 字段或 type-map 通配路径 | skill package delivery drift | 补 `guardrails/guardrails-contract.md`、`SKILL.md` Runtime Guardrails；将 Output Contract 改为五字段冒号列表；type-map 不把通配符/占位题材写成 literal path | 结构修复后必须重跑工作车间 `validate_skill_2_0.py --mode delivery` 与 `smoke_test_skill_2_0.py --mode delivery` | validator/smoke 均 accept，且 guardrail_compliant 为 true |
| 卷级 review 失败后 GPT 直接改正文，导致 B lane provider ownership 失真 | review loop ownership drift | GPT/subagents 只产出 repair brief，仍由 Doubao 执行 `local_repair` 或 `chapter_rewrite` | review aggregate 必须带 `original_drafting_lane=B-Doubao流` 与 repair mode | 返工 sidecar 有 Doubao messages/provider report |
| 用户授权 subagents 多路修复后，误把 worker 并行当成正文主创模型切换 | subagent repair overreach | worker 负责分章/分问题 brief，Doubao 按每个 brief 执行修复并落 provider sidecar | B lane 硬写“修复优化不是 GPT 直写许可”；最终报告列出 repair creative engine | 每个受影响章节有 Doubao repair messages/provider report，正文 `写作模型: Doubao` 与证据一致 |

## Repair Playbook

1. 先确认失败发生在路径、加载、frontmatter、承接还是正文 prose 转写层。
2. 若 YAML 头缺字段，只检查并补正 `写作模型: Doubao` 与 `字数: XXX字`；上下文缺口回到 context pack / sidecar，而不是补进正文头。
3. 若正文像摘要稿，优先检查是不是把 planning 语言直接搬进正文。
4. 若开章发虚，先看同卷前文承接与 `第N章.md` 的开章义务是否真的被解码。
5. 若上下章像各写各的，优先检查 messages pack 是否覆盖当前卷内全部已存在前序章；最近前章末尾负责开章入场，其他前序章负责事实、伏笔、线索、关系、道具、卷目标完成度、任务连续性和悬疑节奏边界。
6. 若文件路径错了，先修 path contract，再谈内容质量。
7. 若执行记录里看不见 provider messages pack、豆包 sidecar 或 provider report，优先怀疑根本没走真实豆包。
8. 若 provider 输出缺字段，不要手工就地补正文冒充成功；先修 prompt / 校验 / provider 返回格式。
9. 若人工校阅指出对白同质化，先查 messages pack 是否含角色对白声纹表；若缺失，修脚本抽取角色卡，再用 `local_repair` 或 `chapter_rewrite` 让 Doubao 按声纹重写相关章节。
10. 若人工校阅指出句式循环，先查 system prompt 与 validator；修复后用同一 finding 回跑 provider，禁止用简单替换脚本机械改正文。
11. 若人工校阅指出正文出现 `第N章 / 上一章 / 本章 / 本轮生成` 等破次元标签，先修 system prompt 与 validator，再让 Doubao 按叙事内事件称呼执行局部修复；不要只做机械替换。
12. 若正式写作没有监制包，先查 subagent 是否被上层阻断；未阻断则补真实 subagents，已阻断则补降级报告。若监制包缺 `team.yaml` roster 来源、请教问题或可执行指导，重新按项目监制组执行请教汇流。
13. 若 dry-run 看见 `supervision_packet_ref` 为空，只能判定为上下文装配检查，不得据此执行正式 provider；正式调用必须补 `--supervision-packet` 或 `--supervision-degradation-report`。
14. 若 Skill 2.0 结构校验失败，先看是否缺 `agents/openai.yaml`、`README.md`、`CHANGELOG.md` 或 `templates/output-template.md`，再看内容语义。
15. 若 review 触发修复，先生成 repair brief，再调用 Doubao 执行正文修复；若环境暂时无法调用 Doubao，必须报告阻断，不能为了推进而用 GPT 直接改写 Doubao lane 正文。
16. 若 Skill 2.0 交付校验失败，优先处理 guardrails、Output Contract 五字段解析、type-map literal path，再看 README/CHANGELOG 等说明层；说明层不能替代交付态 validator。

## Reusable Heuristics

- 章级直写最容易漏的不是剧情，而是“作者此章为何这样写”的约束包；这层约束应进创作上下文和 sidecar，不再塞进正文 YAML。
- `north_star` 对本技能最稳的用法不是在正文头复述，而是转成正文中的压力、选择和章末牵引。
- 若当前卷无前序章，最可靠的替代承接永远是 `卷规划.md + 第N章.md`，不是临场脑补。
- 若同卷前文存在，最可靠的承接组合是“最近前章末尾 3-6k 字 + 同卷全部前序章逐章摘录”；最近前章负责因果入场，早前章节负责事实、伏笔、线索、关系、道具、卷目标完成度、任务连续性和悬疑节奏边界。
- frontmatter 的最佳长度是“能标记写作模型与字数即可”，不要展示已加载资料。
- 只要正文还保留 planning 标题或条目句法，就说明小说化转换还没完成。
- 只要正文还用章节编号、lane/provider、sidecar、frontmatter 或 context pack 回指事实，就说明叙事内视角转换还没完成。
- 对当前技能来说，“真正命中豆包”不是口头说明，而是能落出 messages pack、provider report、raw model output 和最终 `第N卷/第N章.md` 的同轮证据链。
- Skill 2.0 化之后，`SKILL.md` 应像入口和裁决层；章节细则、分支、review 与类型策略各回各的 owner，后续维护才不会牵一发而动全身。
- B lane 的高级化关键是“GPT 监制不抢笔”：监制包越锋利，越要交给 Doubao 执行，而不是让 GPT 临场改稿。
- B lane 的监制包应像“向项目已选大师逐一请教后的写作备忘”，不是 GPT 对 Doubao prompt 的泛泛润色；最终只保留能直接影响正文的指导。
- 对新初始化项目，`north_star.yaml` 往往已经替代实体全局卡/风格卡成为全局、风格、题材方向盘；B lane messages 应优先消费这些契约，再按存在性追加实体卡摘录。
- 修复优化也是主创环节：只要写入 `3-初稿/第N卷/第N章.md` 的正文内容发生创作性改写，就必须遵守本 lane 的 Doubao 执行层边界。
- 人工反馈里出现“对白都像同一个人”“句式反复”时，优先视为 prompt/context pack 源层问题，而不是单章偶发瑕疵；先修声纹导入和句式门禁，再返工正文。
- 工作车间交付态校验器按冒号字段解析 `Output Contract`；表格可以用于模板 alignment，但 `SKILL.md` 的 Output Contract 应保留五个 `Field: value` 字段，避免结构正确却被解析为 0 字段。
