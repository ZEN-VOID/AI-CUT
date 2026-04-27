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
| GPT 原生流只读章级 planning，漏读north_star 全局/风格/类型契约 | context pack contract | 回补 `0-初始化/north_star.yaml` 的 `global_contract`、`style_contract` 与 `genre_contract` | 把完整上下文加载与 sidecar 证据链作为硬门槛，YAML 头只保留 `写作模型` | sidecar 中三类上下文齐备，正文能读出吸收痕迹 |
| 项目有 `MEMORY.md` 或 `CONTEXT/`，但正文没有吸收项目长期偏好 | project context loading | 先读项目记忆，再按相关性选项目上下文 | 固定项目根上下文加载顺序与 sidecar refs | sidecar 中 `project_context_refs` 与真实上下文一致 |
| 把上一章当成硬阻塞门，上一章缺失就停工 | continuity policy | 改成“上一章增强输入，planning 是兜底硬输入” | 固定“previous optional, planning mandatory” | 上一章不存在时，本章仍可开写 |
| 上一章虽然被读取，但新章仍像重新开局 | continuity bridge under-specified | 把上一章末尾摘录单独置入 context pack，并显式要求承接既成事实、位置、情绪余波、未完成动作和悬念压力 | 将“上一章正文”升级为 `continuity bridge`，并在 dry-run summary 暴露 `previous_chapter_ref` | context pack 中能看到连续性桥；正文开章能读出上一章之后的下一步 |
| GPT 原生正文缺少 sidecar，无法证明读过哪些源 | evidence chain gap | 运行 `write_chapter_gpt_native.py --dry-run` 生成 context pack | 在 Completion gate 中固定 context pack / authored draft / writeback 证据链 | `reports/3-初稿/gpt-native/...` 能追溯输入和输出 |
| 脚本开始自动补写正文段落 | script boundary drift | 立即删除规则补写逻辑，改为只接受 `--draft-file` 或 stdin 的 LLM 已创作稿 | 在脚本和 review gate 中固定“脚本不主创” | 脚本没有任何模板灌字、启发式扩写或段落生成函数 |
| GPT 原生主写作者自评被当成独立监制 | supervision isolation gap | 启动后台隔离 subagents 产出 `supervision_packet`，主写作者只消费汇流后的约束 | A lane 固定“同模型也要隔离上下文”，脚本支持 `--supervision-packet` | messages JSON 中含监制包；报告能列出真实 subagent 或降级原因 |
| frontmatter 变成大段资料转储，压过正文 | metadata density | 从正文 YAML 头移除重复上下文字段 | 固定正文 YAML 头只保留 `写作模型`，引用和摘要留在 sidecar | YAML 头极简，正文 token 留给 prose |
| `north_star_chapter_brief` 直接复制 `north_star.yaml` 大段原文 | summary synthesis | 不再要求正文 YAML 重复 north-star 摘要，改由创作上下文消费 | 固定“上下文吸收在正文体现，证据在 sidecar 体现” | 正文对齐 north-star，但头部不复述 |
| 正文主体仍沿用 planning 标题句法 | prose conversion | 把 `本章冲突 / 任务线 / 规避` 转译成人物行动、局势压力和章末牵引 | 固定“planning 只给蓝图，不得原样落成正文” | 正文读起来像小说，不像设计文档 |
| 用户其实需要 provider 路径，却误走 GPT 原生 | route mismatch | 按用户意图改路由到对应 provider skill | 在 Actual Creative Engine 中保留简短路由说明 | A 的 artifacts 路径为 `gpt-native`，provider 路径使用自己的 artifacts |
| 卷级 review 失败后只做主观润色，没有回到原 finding | review loop weak repair | 按 `review` aggregate 生成 repair brief，再决定 `local_repair`、`chapter_rewrite` 或整卷重写 | A lane 的返工必须携带 `source_layer_owner / rework_target / supervision_packet` | 修后重新进入 `review` 能追溯原 finding |

## Repair Playbook

1. 先确认失败发生在路径、加载、frontmatter、承接、GPT 原生主创还是脚本边界层。
2. 若 YAML 头缺字段，只检查并补正 `写作模型: GPT`；上下文缺口回到 context pack / sidecar，而不是补进正文头。
3. 若正文像摘要稿，优先检查是不是把 planning 语言直接搬进正文。
4. 若开章发虚，先看上一章承接与 `第N章.md` 的开章义务是否真的被解码。
5. 若上下章像各写各的，优先检查 context pack 是否只截取了上一章开头；承接判断应优先看上一章末尾，而不是章节开篇。
6. 若文件路径错了，先修 path contract，再谈内容质量。
7. 若执行记录里看不见 context pack、GPT-authored draft sidecar 或 writeback summary，优先补证据链。
8. 若脚本开始“自动生成正文”，直接回到 `scripts/write_chapter_gpt_native.py` 修边界；脚本只能校验和落盘。
9. 若正式写作没有监制包，先查 subagent 是否被上层阻断；未阻断则补真实 subagents，已阻断则补降级报告。
10. 若 Skill 2.0 结构校验失败，先看是否缺 `agents/openai.yaml`、`README.md`、`CHANGELOG.md` 或 `templates/output-template.md`，再看内容语义。

## Reusable Heuristics

- GPT 原生路径的优势是当前会话能同时持有创作判断与项目约束；风险是容易忘记留下可复查 sidecar。
- 章级直写最容易漏的不是剧情，而是“作者此章为何这样写”的约束包；这层约束应进创作上下文和 sidecar，不再塞进正文 YAML。
- `north_star` 对本技能最稳的用法不是在正文头复述，而是转成正文中的压力、选择和章末牵引。
- 若上一章缺失，最可靠的替代承接永远是 `卷规划.md + 第N章.md`，不是临场脑补。
- 若上一章存在，最可靠的承接材料通常是上一章末尾 3-6k 字，而不是上一章开头；章节开头负责调性，章节末尾负责因果入场。
- frontmatter 的最佳长度是“能标记写作模型即可”，不要展示已加载资料。
- 只要正文还保留 planning 标题或条目句法，就说明小说化转换还没完成。
- A 路径保持 GPT 原生默认；需要外部模型时显式切到 B 或其他 provider skill。
- A 路径不是“一个 GPT 同时写又同时审”的省事路径；隔离 subagents 的价值在于给主写作者一个有距离的监制包。
