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
| GPT 原生流只读章级 planning，漏读north_star 全局/风格/类型契约 | context pack contract | 回补 `0-初始化/north_star.yaml` 的 `global_contract`、`style_contract` 与 `genre_contract` | 把完整上下文加载与 sidecar 证据链作为硬门槛，YAML 头只保留 `写作模型` 与 `字数` | sidecar 中三类上下文齐备，正文能读出吸收痕迹 |
| 项目有 `MEMORY.md` 或 `CONTEXT/`，但正文没有吸收项目长期偏好 | project context loading | 先读项目记忆，再按相关性选项目上下文 | 固定项目根上下文加载顺序与 sidecar refs | sidecar 中 `project_context_refs` 与真实上下文一致 |
| 把同卷前文当成硬阻塞门，当前卷无前序章就停工 | continuity policy | 改成“同卷前文增强输入，planning 是兜底硬输入” | 固定“same-volume priors optional, planning mandatory” | 当前卷无前序章时，本章仍可开写 |
| 只加载最近上一章，导致同卷早前事实、伏笔、线索、道具流向、卷目标完成度、任务连续性或悬疑节奏把控性断裂 | same-volume continuity underload | 加载当前卷内所有已存在且早于目标章的正文，并把最近前章末尾摘录置入 context pack | 将“上一章正文”升级为“同卷前文连续性桥”，dry-run summary 暴露 `previous_chapter_refs` | context pack 中能看到同卷前文逐章摘录；正文开章能读出同卷前文之后的下一步 |
| GPT 原生正文缺少可复核加载痕迹 | evidence chain gap | 运行 `write_chapter_gpt_native.py --dry-run` 检查 context pack 摘要，正式执行只写 canonical 章节 | Completion gate 固定加载计划、GPT-authored draft 与 writeback 状态 | 最终章节仍可追溯到加载计划与 stdout 摘要 |
| 脚本开始自动补写正文段落 | script boundary drift | 立即删除规则补写逻辑，改为只接受 `--draft-file` 或 stdin 的 LLM 已创作稿 | 在脚本和 review gate 中固定“脚本不主创” | 脚本没有任何模板灌字、启发式扩写或段落生成函数 |
| GPT 原生主写作者自评被当成独立监制 | supervision isolation gap | 启动后台隔离 subagents 产出 `supervision_packet`，主写作者只消费汇流后的约束 | A lane 固定“同模型也要隔离上下文”，脚本支持 `--supervision-packet` | messages JSON 中含监制包；报告能列出真实 subagent 或降级原因 |
| 监制包未按项目 `team.yaml` 已指定监制组请教，只给泛泛创作建议 | project team consultation gap | 读取 `roles.production.members`，为每位相关大师提出具体问题并汇流可执行指导 | 监制包固定 `project_team_ref / consultations / executable_guidance` 字段 | GPT-native messages 含可追溯的请教式监制包 |
| frontmatter 变成大段资料转储，压过正文 | metadata density | 从正文 YAML 头移除重复上下文字段 | 固定正文 YAML 头只保留 `写作模型` 与 `字数`，引用和摘要留在 sidecar | YAML 头极简，正文 token 留给 prose |
| `north_star_chapter_brief` 直接复制 `north_star.yaml` 大段原文 | summary synthesis | 不再要求正文 YAML 重复 north-star 摘要，改由创作上下文消费 | 固定“上下文吸收在正文体现，证据在 sidecar 体现” | 正文对齐 north-star，但头部不复述 |
| 正文主体仍沿用 planning 标题句法 | prose conversion | 把 `本章冲突 / 任务线 / 规避` 转译成人物行动、局势压力和章末牵引 | 固定“planning 只给蓝图，不得原样落成正文” | 正文读起来像小说，不像设计文档 |
| 正文出现 `第6章的二人组`、`上一章`、`本章` 等破次元标签 | narrative-perspective leak | 把章节/流程标签改成叙事内事件称呼，如“礁链那两个追杀手”“潮汊村寨那三人” | system prompt 与 validator 固定“叙事内视角完整性”，禁止章节编号和执行流程词进入正文 | 写回前阻断正文中的章节标签、流程标签和 evidence 层词 |
| 角色对白同质化，所有人物都用同一种冷静说明腔 | character voice under-specified | 从角色卡抽取 `voice_and_presence` 形成“角色对白声纹表”，并要求每句对白承担角色意图 | prompt 固定导入声纹表；对白必须按身份、关系、情绪和利益差异化 | context pack 中存在声纹表；抽查同场对话能不看话标区分说话人 |
| `不是……是……` 句式高频重复，解释感生硬 | sentence-pattern loop | 在 system prompt 中把该句式降为偶发关键反转用法，并在 validator 中设置上限 | 生成前给替代表达路径：动作、感官、比喻、反问、停顿、误读修正或角色化口语 | validator 统计该句式不超过上限；正文不连续使用同一解释框架 |
| 用户其实需要 provider 路径，却误走 GPT 原生 | route mismatch | 按用户意图改路由到对应 provider skill | 在 Actual Creative Engine 中保留简短路由说明 | A 的 artifacts 路径为 `gpt-native`，provider 路径使用自己的 artifacts |
| 卷级 review 失败后只做主观润色，没有回到原 finding | review loop weak repair | 按 `review` aggregate 生成 repair brief，再决定 `local_repair`、`chapter_rewrite` 或整卷重写 | A lane 的返工必须携带 `source_layer_owner / rework_target / supervision_packet` | 修后重新进入 `review` 能追溯原 finding |

## Repair Playbook

1. 先确认失败发生在路径、加载、frontmatter、承接、GPT 原生主创还是脚本边界层。
2. 若 YAML 头缺字段，只检查并补正 `写作模型: GPT` 与 `字数: XXX字`；上下文缺口回到 context pack / sidecar，而不是补进正文头。
3. 若正文像摘要稿，优先检查是不是把 planning 语言直接搬进正文。
4. 若开章发虚，先看同卷前文承接与 `第N章.md` 的开章义务是否真的被解码。
5. 若上下章像各写各的，优先检查 context pack 是否覆盖当前卷内全部已存在前序章；最近前章末尾负责开章入场，其他前序章负责事实、伏笔、线索、关系、道具、卷目标完成度、任务连续性和悬疑节奏边界。
6. 若文件路径错了，先修 path contract，再谈内容质量。
7. 若执行记录里看不见 context pack、GPT-authored draft sidecar 或 writeback summary，优先补证据链。
8. 若脚本开始“自动生成正文”，直接回到 `scripts/write_chapter_gpt_native.py` 修边界；脚本只能校验和落盘。
9. 若人工校阅指出对白同质化，先查 context pack 是否含角色对白声纹表；若缺失，修脚本抽取角色卡，再让 GPT 原生按声纹执行 `local_repair` 或 `chapter_rewrite`。
10. 若人工校阅指出句式循环，先查 system prompt 与 validator；修复后用同一 finding 回跑 GPT 原生主创，禁止用简单替换脚本机械改正文。
11. 若人工校阅指出正文出现 `第N章 / 上一章 / 本章 / 本轮生成` 等破次元标签，先修 system prompt 与 validator，再让 GPT 原生按叙事内事件称呼执行局部修复；不要只做机械替换。
11. 若正式写作没有监制包，先查 subagent 是否被上层阻断；未阻断则补真实 subagents，已阻断则补降级报告。若监制包缺 `team.yaml` roster 来源、请教问题或可执行指导，重新按项目监制组执行请教汇流。
12. 若 Skill 2.0 结构校验失败，先看是否缺 `agents/openai.yaml`、`README.md`、`CHANGELOG.md` 或 `templates/output-template.md`，再看内容语义。

## Reusable Heuristics

- GPT 原生路径的优势是当前会话能同时持有创作判断与项目约束；风险是容易忘记留下可复查 sidecar。
- 章级直写最容易漏的不是剧情，而是“作者此章为何这样写”的约束包；这层约束应进创作上下文和 sidecar，不再塞进正文 YAML。
- `north_star` 对本技能最稳的用法不是在正文头复述，而是转成正文中的压力、选择和章末牵引。
- 若当前卷无前序章，最可靠的替代承接永远是 `卷规划.md + 第N章.md`，不是临场脑补。
- 若同卷前文存在，最可靠的承接组合是“最近前章末尾 3-6k 字 + 同卷全部前序章逐章摘录”；最近前章负责因果入场，早前章节负责事实、伏笔、线索、关系、道具、卷目标完成度、任务连续性和悬疑节奏边界。
- frontmatter 的最佳长度是“能标记写作模型与字数即可”，不要展示已加载资料。
- 只要正文还保留 planning 标题或条目句法，就说明小说化转换还没完成。
- 只要正文还用章节编号、lane/provider、sidecar、frontmatter 或 context pack 回指事实，就说明叙事内视角转换还没完成。
- A 路径保持 GPT 原生默认；需要外部模型时显式切到 B 或其他 provider skill。
- A 路径不是“一个 GPT 同时写又同时审”的省事路径；隔离 subagents 的价值在于给主写作者一个有距离的监制包。
- A 路径的监制包应像“向项目已选大师逐一请教后的写作备忘”，不是主写作者换个口吻自我点评；最终只保留能直接影响正文的指导。
- 人工反馈里出现“对白都像同一个人”“句式反复”时，优先视为 prompt/context pack 源层问题，而不是单章偶发瑕疵；先修声纹导入和句式门禁，再返工正文。
