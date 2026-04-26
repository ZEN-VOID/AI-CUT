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
| GPT 原生流只读章级 planning，漏读全局卡/风格卡/`north_star` | context pack contract | 回补 `1-Cards/0-全局卡`、`1-Cards/1-风格卡` 与 `0-Init/north_star.yaml` | 把 `写作模型 + global_context + style_context + north_star_chapter_brief` 写成 YAML 头硬门槛 | 生成稿头时写作模型与三类摘要都齐备 |
| 项目有 `MEMORY.md` 或 `CONTEXT/`，但正文没有吸收项目长期偏好 | project context loading | 先读项目记忆，再按相关性选项目上下文 | 固定项目根上下文加载顺序与 sidecar refs | frontmatter 中 `project_context_refs` 与真实上下文一致 |
| 把上一章当成硬阻塞门，上一章缺失就停工 | continuity policy | 改成“上一章增强输入，planning 是兜底硬输入” | 固定“previous optional, planning mandatory” | 上一章不存在时，本章仍可开写 |
| GPT 原生正文缺少 sidecar，无法证明读过哪些源 | evidence chain gap | 运行 `write_chapter_gpt_native.py --dry-run` 生成 context pack | 在 Completion gate 中固定 context pack / authored draft / writeback 证据链 | `reports/3-Drafting/gpt-native/...` 能追溯输入和输出 |
| 脚本开始自动补写正文段落 | script boundary drift | 立即删除规则补写逻辑，改为只接受 `--draft-file` 或 stdin 的 LLM 已创作稿 | 在脚本和 review gate 中固定“脚本不主创” | 脚本没有任何模板灌字、启发式扩写或段落生成函数 |
| frontmatter 变成大段资料转储，压过正文 | metadata density | 只保留当前章会直接用到的约束摘要 | 固定 `global/style` 摘要为约束性短段，而非 JSON dump | YAML 头短而有用 |
| `north_star_chapter_brief` 直接复制 `north_star.yaml` 大段原文 | summary synthesis | 回到“整书承诺 + 当前章义务”的压缩摘要 | 固定“必须二次综合，不得整段照抄” | YAML 头可读、短小、且明显对齐当前章 |
| 正文主体仍沿用 planning 标题句法 | prose conversion | 把 `本章冲突 / 任务线 / 规避` 转译成人物行动、局势压力和章末牵引 | 固定“planning 只给蓝图，不得原样落成正文” | 正文读起来像小说，不像设计文档 |
| 用户其实需要 provider 路径，却误走 GPT 原生 | route mismatch | 按用户意图改路由到对应 provider skill | 在 Actual Creative Engine 中保留简短路由说明 | A 的 artifacts 路径为 `gpt-native`，provider 路径使用自己的 artifacts |

## Repair Playbook

1. 先确认失败发生在路径、加载、frontmatter、承接、GPT 原生主创还是脚本边界层。
2. 若 YAML 头缺字段，先补 `global/style/north_star` 三件套，不先修句子。
3. 若正文像摘要稿，优先检查是不是把 planning 语言直接搬进正文。
4. 若开章发虚，先看上一章承接与 `第N章.md` 的开章义务是否真的被解码。
5. 若文件路径错了，先修 path contract，再谈内容质量。
6. 若执行记录里看不见 context pack、GPT-authored draft sidecar 或 writeback summary，优先补证据链。
7. 若脚本开始“自动生成正文”，直接回到 `scripts/write_chapter_gpt_native.py` 修边界；脚本只能校验和落盘。
8. 若 Skill 2.0 结构校验失败，先看是否缺 `agents/openai.yaml`、`README.md`、`CHANGELOG.md` 或 `templates/output-template.md`，再看内容语义。

## Reusable Heuristics

- GPT 原生路径的优势是当前会话能同时持有创作判断与项目约束；风险是容易忘记留下可复查 sidecar。
- 章级直写最容易漏的不是剧情，而是“作者此章为何这样写”的约束包；YAML 头就是把这层约束固定下来。
- `north_star` 对本技能最稳的用法不是全文引用，而是压成“这一章在整书承诺里承担什么”。
- 若上一章缺失，最可靠的替代承接永远是 `卷规划.md + 第N章.md`，不是临场脑补。
- frontmatter 的最佳长度是“足够约束当前章”，不是“展示我读了多少资料”。
- 只要正文还保留 planning 标题或条目句法，就说明小说化转换还没完成。
- A 路径保持 GPT 原生默认；需要外部模型时显式切到 B 或其他 provider skill。
