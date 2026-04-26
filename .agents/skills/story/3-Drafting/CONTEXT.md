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
| 明明是按章直写，却仍回写到平铺 `3-Drafting/第N章.md` | runtime path contract | 改回 `projects/story/<项目名>/3-Drafting/第N卷/第N章.md` | 在 `3-Drafting/SKILL.md`、桥接脚本与 registry 路由同时固定 canonical 输出路径 | 正文不会再漂到平铺旧路径 |
| 只读三层 planning，没读全局卡/风格卡/`north_star` | context pack contract | 回补 `1-Cards/0-全局卡`、`1-Cards/1-风格卡` 与 `0-Init/north_star.yaml` | 把 `global_context + style_context + north_star_chapter_brief` 写成 YAML 头硬门槛 | 生成稿头时三类摘要都齐备 |
| 项目有 `CONTEXT/`，但 drafting 完全没加载 | project context loading | 补读相关 `CONTEXT` 文件并记录到 `project_context_refs` | 固定“存在则按相关性加载，不存在才留空” | frontmatter 中 `project_context_refs` 与真实上下文一致 |
| 把上一章当成硬阻塞门，上一章缺失就停工 | continuity policy | 改成“上一章增强输入，planning 是兜底硬输入” | 在 skill 合同写死“previous optional, planning mandatory” | 上一章不存在时，本章仍可开写 |
| `3-Drafting` 看起来命中正确，但实际创作仍由本地 GPT 会话直接写出 | provider route drift | 改成通过 `write_chapter_via_doubao.py` 调用 AnyFast 豆包，再写回业务根稿 | 在主合同里写死“actual creative step = Doubao provider”，并为脚本增加 dry-run / 校验 / writeback 路径 | provider 报告、messages pack 与写回文件能互相对上 |
| 豆包返回了正文，但缺 frontmatter / 标题行 / 必需字段，仍被直接写回 | provider output validation | 在写回前增加 frontmatter / heading / required marker 校验 | 将 provider output validation 固化到 bridge script，而不是靠人工肉眼兜底 | 非法输出会在写回前被阻断 |
| `north_star_chapter_brief` 直接复制 `north_star.yaml` 大段原文 | summary synthesis | 回到“整书承诺 + 当前章义务”的压缩摘要 | 在合同中固定“必须二次综合，不得整段照抄” | YAML 头可读、短小、且明显对齐当前章 |
| frontmatter 变成大段资料转储，压过正文 | metadata density | 只保留当前章会直接用到的约束摘要 | 固定 `global/style` 摘要为约束性短段，而非 JSON dump | YAML 头短而有用 |
| 正文主体仍沿用 planning 标题句法 | prose conversion | 把 `本章冲突 / 任务线 / 规避` 转译成人物行动、局势压力和章末牵引 | 在 skill 中固定“planning 只给蓝图，不得原样落成正文” | 正文读起来像小说，不像设计文档 |
| Skill 2.0 升级后 `SKILL.md` 又重新堆满执行细则 | skill package ownership drift | 把长细则下沉到 `references/steps/types/review/knowledge-base`，入口只留路由与门禁 | 在 `Reference Loading Guide` 中固定每个 owner 的读取时机 | 根 `SKILL.md` 能独立回答输入和输出，但不复制分区全文 |

## Repair Playbook

1. 先确认失败发生在路径、加载、frontmatter、承接还是正文 prose 转写层。
2. 若 YAML 头缺字段，先补 `global/style/north_star` 三件套，不先修句子。
3. 若正文像摘要稿，优先检查是不是把 planning 语言直接搬进正文。
4. 若开章发虚，先看上一章承接与 `第N章.md` 的开章义务是否真的被解码。
5. 若文件路径错了，先修 path contract，再谈内容质量。
6. 若执行记录里看不见 provider messages pack、豆包 sidecar 或 provider report，优先怀疑根本没走真实豆包。
7. 若 provider 输出缺字段，不要手工就地补正文冒充成功；先修 prompt / 校验 / provider 返回格式。
8. 若 Skill 2.0 结构校验失败，先看是否缺 `agents/openai.yaml`、`README.md`、`CHANGELOG.md` 或 `templates/output-template.md`，再看内容语义。

## Reusable Heuristics

- 章级直写最容易漏的不是剧情，而是“作者此章为何这样写”的约束包；YAML 头就是把这层约束固定下来。
- `north_star` 对本技能最稳的用法不是全文引用，而是压成“这一章在整书承诺里承担什么”。
- 若上一章缺失，最可靠的替代承接永远是 `卷规划.md + 第N章.md`，不是临场脑补。
- frontmatter 的最佳长度是“足够约束当前章”，不是“展示我读了多少资料”。
- 只要正文还保留 planning 标题或条目句法，就说明小说化转换还没完成。
- 对当前技能来说，“真正命中豆包”不是口头说明，而是能落出 messages pack、provider report、raw model output 和最终 `第N卷/第N章.md` 的同轮证据链。
- Skill 2.0 化之后，`SKILL.md` 应像入口和裁决层；章节细则、分支、review 与类型策略各回各的 owner，后续维护才不会牵一发而动全身。
