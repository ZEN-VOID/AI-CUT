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
| 只读三层 planning，没读north_star 全局/风格/类型契约 | context pack contract | 回补 `0-初始化/north_star.yaml` 的 `global_contract`、`style_contract` 与 `genre_contract` | 把完整上下文加载与 sidecar 证据链作为硬门槛，YAML 头只保留 `写作模型` | sidecar 中三类上下文齐备，正文能读出吸收痕迹 |
| 项目有 `CONTEXT/`，但 drafting 完全没加载 | project context loading | 补读相关 `CONTEXT` 文件并记录到 sidecar | 固定“存在则按相关性加载，不存在才留空” | sidecar 中 `project_context_refs` 与真实上下文一致 |
| 把上一章当成硬阻塞门，上一章缺失就停工 | continuity policy | 改成“上一章增强输入，planning 是兜底硬输入” | 在 skill 合同写死“previous optional, planning mandatory” | 上一章不存在时，本章仍可开写 |
| 上一章虽然被读取，但新章仍像重新开局 | continuity bridge under-specified | 把上一章末尾摘录单独置入 provider prompt，并显式要求承接既成事实、位置、情绪余波、未完成动作和悬念压力 | 将“上一章正文”升级为 `continuity bridge`，并在有上一章时校验 `previous_chapter_ref` | messages pack 中能看到连续性桥；正文开章能读出上一章之后的下一步 |
| `3-初稿` 看起来命中正确，但实际创作仍由本地 GPT 会话直接写出 | provider route drift | 改成通过 `write_chapter_via_doubao.py` 调用 AnyFast 豆包，再写回业务根稿 | 在主合同里写死“actual creative step = Doubao provider”，并为脚本增加 dry-run / 校验 / writeback 路径 | provider 报告、messages pack 与写回文件能互相对上 |
| GPT 监制意见只停在口头，没有进入豆包 prompt | supervision packet drop | 把 subagents 汇流为 `supervision_packet`，通过 `--supervision-packet` 注入 messages pack | B lane 固定 GPT 为监制层、Doubao 为执行层；脚本记录 `supervision_packet_ref` | messages JSON 中含监制包；最终正文仍有 Doubao provider 证据 |
| 豆包返回了正文，但缺 frontmatter / 标题行 / 必需字段，仍被直接写回 | provider output validation | 在写回前增加 frontmatter / heading / required marker 校验 | 将 provider output validation 固化到 bridge script，而不是靠人工肉眼兜底 | 非法输出会在写回前被阻断 |
| `north_star_chapter_brief` 直接复制 `north_star.yaml` 大段原文 | summary synthesis | 不再要求正文 YAML 重复 north-star 摘要，改由 provider 上下文消费 | 固定“上下文吸收在正文体现，证据在 sidecar 体现” | 正文对齐 north-star，但头部不复述 |
| frontmatter 变成大段资料转储，压过正文 | metadata density | 从正文 YAML 头移除重复上下文字段 | 固定正文 YAML 头只保留 `写作模型`，引用和摘要留在 sidecar | YAML 头极简，正文 token 留给 prose |
| 正文主体仍沿用 planning 标题句法 | prose conversion | 把 `本章冲突 / 任务线 / 规避` 转译成人物行动、局势压力和章末牵引 | 在 skill 中固定“planning 只给蓝图，不得原样落成正文” | 正文读起来像小说，不像设计文档 |
| Skill 2.0 升级后 `SKILL.md` 又重新堆满执行细则 | skill package ownership drift | 把长细则下沉到 `references/steps/types/review/knowledge-base`，入口只留路由与门禁 | 在 `Reference Loading Guide` 中固定每个 owner 的读取时机 | 根 `SKILL.md` 能独立回答输入和输出，但不复制分区全文 |
| 卷级 review 失败后 GPT 直接改正文，导致 B lane provider ownership 失真 | review loop ownership drift | GPT/subagents 只产出 repair brief，仍由 Doubao 执行 `local_repair` 或 `chapter_rewrite` | review aggregate 必须带 `original_drafting_lane=B-Doubao流` 与 repair mode | 返工 sidecar 有 Doubao messages/provider report |

## Repair Playbook

1. 先确认失败发生在路径、加载、frontmatter、承接还是正文 prose 转写层。
2. 若 YAML 头缺字段，只检查并补正 `写作模型: Doubao`；上下文缺口回到 context pack / sidecar，而不是补进正文头。
3. 若正文像摘要稿，优先检查是不是把 planning 语言直接搬进正文。
4. 若开章发虚，先看上一章承接与 `第N章.md` 的开章义务是否真的被解码。
5. 若上下章像各写各的，优先检查 messages pack 是否只截取了上一章开头；承接判断应优先看上一章末尾，而不是章节开篇。
6. 若文件路径错了，先修 path contract，再谈内容质量。
7. 若执行记录里看不见 provider messages pack、豆包 sidecar 或 provider report，优先怀疑根本没走真实豆包。
8. 若 provider 输出缺字段，不要手工就地补正文冒充成功；先修 prompt / 校验 / provider 返回格式。
9. 若正式写作没有监制包，先查 subagent 是否被上层阻断；未阻断则补真实 subagents，已阻断则补降级报告。
10. 若 Skill 2.0 结构校验失败，先看是否缺 `agents/openai.yaml`、`README.md`、`CHANGELOG.md` 或 `templates/output-template.md`，再看内容语义。

## Reusable Heuristics

- 章级直写最容易漏的不是剧情，而是“作者此章为何这样写”的约束包；这层约束应进创作上下文和 sidecar，不再塞进正文 YAML。
- `north_star` 对本技能最稳的用法不是在正文头复述，而是转成正文中的压力、选择和章末牵引。
- 若上一章缺失，最可靠的替代承接永远是 `卷规划.md + 第N章.md`，不是临场脑补。
- 若上一章存在，最可靠的承接材料通常是上一章末尾 3-6k 字，而不是上一章开头；章节开头负责调性，章节末尾负责因果入场。
- frontmatter 的最佳长度是“能标记写作模型即可”，不要展示已加载资料。
- 只要正文还保留 planning 标题或条目句法，就说明小说化转换还没完成。
- 对当前技能来说，“真正命中豆包”不是口头说明，而是能落出 messages pack、provider report、raw model output 和最终 `第N卷/第N章.md` 的同轮证据链。
- Skill 2.0 化之后，`SKILL.md` 应像入口和裁决层；章节细则、分支、review 与类型策略各回各的 owner，后续维护才不会牵一发而动全身。
- B lane 的高级化关键是“GPT 监制不抢笔”：监制包越锋利，越要交给 Doubao 执行，而不是让 GPT 临场改稿。
