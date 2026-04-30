# CONTEXT.md

本文件是 `story2026 / 3-初稿` 阶段导引层的经验库。它记录父级路由、正文真源、防漂移与 lane 启用规则，不承载 `A-GPT原生`、`B-Doubao流` 或 `C-Deepseek流` 的具体主创细则。

## Context Health

```yaml
monitor_version: 1
soft_limit_chars: 40000
hard_limit_chars: 80000
soft_limit_cases: 80
hard_limit_cases: 140
status: ok
recommended_action: keep-router-level-only
last_checked_at: 2026-04-27
```

## Type Map

| failure_or_outcome_type | root_cause_layer | immediate_fix | systemic_prevention | verification_point |
| --- | --- | --- | --- | --- |
| 父级 `3-初稿/SKILL.md` 为空，registry 仍把它当 stage 入口 | stage router gap | 补成导引式入口，默认路由到可执行 lane | 父级只持有 lane selection、loading、truth path 与 close gate | `$story-drafting` 能先命中父级再进入子路径 |
| 子路径拆成 `A-GPT原生 / B-Doubao流 / C-Deepseek流` 后，父级仍写死旧 DeepSeek 默认 | provider split drift | 把具体执行细则留给子路径，父级只写默认路由和激活状态 | lane matrix 固定 `B` 默认、`A/C` 显式 | 父级不复制子路径 `references/steps/types/review` 全文 |
| 未点名 provider 时误走 GPT 原生、DeepSeek 或空 lane | lane default drift | 未明确 provider 时回到 `B-Doubao流` | `$story-drafting` 默认对齐 `B-Doubao流` | 普通“写一章”请求进入 B lane |
| 用户点名 GPT 原生，但父级误走默认或其它 lane | explicit lane override miss | 路由到 `A-GPT原生` | lane matrix 明确“用户显式 provider / native intent 优先于默认” | “GPT 原生/本地会话直写”进入 A lane |
| 用户点名豆包，但父级仍强制默认 DeepSeek | explicit lane override miss | 路由到 `B-Doubao流` | lane matrix 明确“豆包 / Doubao / `$story-drafting-doubao`”进入 B lane | 豆包写章请求进入 B lane |
| 用户点名 DeepSeek，但父级误判为其它 lane | explicit lane override miss | 路由到 `C-Deepseek流` | lane matrix 明确“DeepSeek / deepseek-v4-pro / api/deepseek”进入 C lane | DeepSeek 写章请求进入 C lane |
| 正文写回路径漂到平铺 `第N章.md`、`第N集.md`、`正文/` 或旧 `Drafting/chNNNN/chapter-root.md` | canonical path contract | 改回 `projects/story/<项目名>/3-初稿/第N卷/第N章.md` | 父级和所有子路径都把 canonical output 作为硬门禁 | writeback path 与 registry `canonical_output` 一致 |
| 父级导引层吞掉子路径经验，导致 `CONTEXT.md` 变成 provider 细则合集 | context ownership drift | 把 provider 经验迁回对应 lane `CONTEXT.md` | 父级只保留跨 lane 的防漂移经验 | 本文件不出现 provider prompt、脚本参数细则或章节正文规则长表 |
| 子路径执行前漏读 story 根层、项目 `MEMORY.md` 或项目 `CONTEXT/` | loading bridge gap | 在父级先列 loading plan，再交给 lane 继续加载 | 父级 Context Loading Contract 固定 shared + project + lane 三段式 | lane handoff 前已能列出必须读取的根层和项目层上下文 |
| 新章上下文只加载最近上一章，导致同卷早前伏笔、线索状态、关系推进、道具流向、卷目标完成度、任务连续性或悬疑节奏把控性断裂 | same-volume prior-chapter underload | 改为加载当前卷内所有已存在且早于目标章的前序正文；最近前章只作为开章承接重点 | 父级与 A/B/C lane 的 Input Contract、context pack 脚本和 dry-run summary 均记录 `previous_chapter_refs` 列表 | dry-run summary 出现本卷全部前序章路径，messages/context pack 含“同卷前文逐章摘录” |
| 正文只按角色声纹写互动，漏掉角色关系图谱的联系方式和传导边 | relationship graph context gap | context pack 加载 `1-设定/2-角色卡/角色关系图谱.md` 摘录 | 父级 Input Contract 与 A/B/C 脚本都固定 `relationship_graph_ref` | dry-run summary 出现 `relationship_graph_ref`，messages/context pack 出现“角色关系图谱”段落 |
| 正式写作没有启动 team supervision subagents，却把本地自评当监制 | supervision dispatch gap | 回读 `_shared/supervised-drafting-review-loop-contract.md`，补真实 subagent roster 或降级报告 | 父级 handoff 固定要求 `supervision_packet`，A/B/C scripts 消费 `--supervision-packet` | messages pack 中能追溯监制包或降级说明 |
| 启用了 subagents，但没有按项目 `team.yaml` 中的监制组成员请教，只临时从 team 根另选人或写泛泛意见 | project team consultation gap | 回读项目 `team.yaml -> roles.production.members`，向已指定监制组成员提出具体领域问题，重新汇流 `supervision_packet` | 共享合同固定 project team roster 优先级、请教题包和可执行指导字段 | `supervision_packet` 能追溯 team.yaml、consultation questions、answer_summary 与 executable_guidance |
| 卷级 review 失败后跨 lane 静默改正文 | review loop ownership drift | aggregate 必须指回原 A/B/C lane 与 repair mode | review rework target 固定 `original_drafting_lane`，BC 由 provider 执行，A 由隔离监制 + GPT 执行 | `第V卷.validation.json` 含原 lane 与返工入口 |
| 用户要求 subagents 多路修复时，执行者把“多路”误解为 GPT worker 直接主创 B/C provider 正文 | repair authorship drift | subagents 只拆分问题和写 repair brief，正文修复回原 lane provider 执行 | 父级 `Repair Lane Preservation` 固定 provider lane ownership；报告必须声明 repair creative engine | 修复后的 sidecar 有原 lane provider messages/report，正文 `写作模型` 与执行证据一致 |
| lane artifacts 被误认为正文真源 | evidence/truth confusion | 移除默认 artifacts 输出，只保留 `3-初稿/第N卷/第N章.md` | 父级 Output Contract 固定“本阶段正式产物只写入 3-初稿” | query/resume/review 默认读取 canonical draft |
| 章节被固定字数区间牵引，出现为凑字或压缩而损害节奏 | word-count overconstraint | 移除默认字数上下限、prompt 目标区间与脚本区间校验；`字数` 仅保留为结果记录 | 父级和 A/B/C lane 不再推导单章字数区间，脚本不再暴露 `--min-words/--max-words` | dry-run summary / messages pack 不再出现 `word_count_range`，最终正文只做结构、字段和正文非空校验 |
| 旧 step-after-write 即时审计合同又被当成当前主创拓扑 | compatibility contract overreach | 仅在恢复/兼容 runtime 时加载 `_shared/drafting-instant-validation-contract.md` | 父级写明它不是默认主创路径 | 新章节直写不再先展开旧八步 runtime |
| 正文出现 `第6章的二人组`、`上一章`、`本章` 等破次元标签 | narrative-perspective leak | 把章节/流程标签改成叙事内事件称呼，如“礁链那两个追杀手”“潮汊村寨那三人” | 父级 Core Gates、A/B/C prompt 和脚本 validator 固定叙事内视角完整性门禁 | 写回前 validator 阻断正文中的章节标签、流程标签和 provider 证据层词 |
| 惊吓、羞窘或愤怒反复写成“脸红了 / 脸白了 / 脸色惨白 / 脸色大变” | emotion shorthand loop | 改用角色动作、呼吸、手部细节、视线、步伐、物件误触、话语断裂或空间退让来呈现情绪 | 父级 Core Gates 与各 lane prompt 固定“脸部颜色变化不是默认情绪表达” | 抽查正文不再以脸色颜色词承载关键情绪变化 |

## Repair Playbook

1. 先判断问题属于 lane selection、loading bridge、canonical path、子路径执行、还是兼容 runtime。
2. 若 `$story-drafting` 入口失效，先修父级 `SKILL.md`，不要直接让 registry 指到某个子路径。
3. 若普通章节创作没有点名 provider，默认进入 `B-Doubao流`；若用户显式要求 GPT 原生，进入 `A-GPT原生`；若用户显式要求豆包 / Doubao / `$story-drafting-doubao`，进入 `B-Doubao流`；若用户显式要求 DeepSeek / deepseek-v4-pro / `.agents/skills/api/deepseek`，进入 `C-Deepseek流`。
4. 若出现任一 provider lane，先检查是否已有非空 `SKILL.md + CONTEXT.md`、执行脚本、模板、review gate 和 `agents/openai.yaml`；缺任一关键合同都阻断执行。
5. 若路径错，优先修父级 canonical output gate，再同步检查子路径 Output Contract、脚本 writeback 和 registry。
6. 若正文内容像 planning 摘要、frontmatter 缺 `写作模型` / `字数` 或 provider 证据链缺失，转到具体 lane 的 `CONTEXT.md` 和分区细则，不在父级长篇补规则。
7. 若恢复链或即时审计仍需要旧 step gate，加载 `_shared/drafting-instant-validation-contract.md`；若是新章直写，不让该兼容合同反向改写 lane 选择。
8. 若本文件开始积累某个 provider 的提示词、脚本参数或正文审美细则，把该经验迁回对应 lane 的 `CONTEXT.md` 或 `knowledge-base/`。
9. 若 review 后需要正文修复，先读取正文 `写作模型`、provider sidecar 或 aggregate 中的 `original_drafting_lane`；B/C lane 不允许由 GPT worker 直接改写后继续冒充原 provider 修复。
10. 若旧流程或项目材料仍给出类似 `2500-4000` 的区间，只作为节奏参考，不再同步为 prompt 强目标、脚本参数或最终长度校验。
11. 若监制包缺项目 `team.yaml` roster 来源、请教问题或可执行指导，按共享合同重做请教汇流，不把泛泛顾问意见继续传给正文主创层。
12. 若人物互动变成“我知道你是谁”的说明腔，先查 context pack 是否加载 `角色关系图谱.md`；缺失时重建 context pack，让正文按物件、证据、通信和情感触发来写关系。
13. 若当前章忘记同卷早前事实、伏笔、线索、关系推进、道具流向、卷目标完成度、任务连续性或悬疑节奏把控性，先查 dry-run summary 的 `previous_chapter_refs` 是否覆盖当前卷内全部已存在前序章；若只出现最近上一章，优先修 context pack 脚本和 lane 输入合同。
14. 若人工校阅指出“脸红 / 脸白 / 脸色大变”等情绪捷径过多，先把它视为初稿表达规则缺口；修正时用动作链和角色身份反应替代，不做简单同义词替换。
15. 若人工校阅指出“第N章 / 上一章 / 本章 / 本轮生成”等破次元口径，优先视为 prose conversion 和 validator 缺口；修正文稿时只用叙事内时间、地点、事件、伤亡或物件称呼回指前事。

## Reusable Heuristics

- 父级 `3-初稿` 最该像交通枢纽：能稳定指路、锁真源、设门禁，但不替每条 lane 写完整操作手册。
- 拆成多 provider 后，默认 lane 和显式 lane 必须同时存在；默认解决“普通请求往哪走”，显式解决“用户点名往哪走”，当前普通章节初稿默认进入 B lane，DeepSeek 只有点名或返工证据要求时进入 C lane。
- 初稿阶段的默认目标是“先写出有人话和中文网文气口的候选正文”，不要把长推理模型的规整化偏好提前引入初稿。
- 空骨架比坏执行更危险：目录存在不等于 skill 可用，尤其是 provider lane。
- `projects/story/<项目名>/3-初稿/第N卷/第N章.md` 是所有 lane 的共同锚点；artifacts 越多，越要反复声明它们只是证据链。
- 父级加载顺序的价值在于防漏读项目记忆和上下文；真正的章节写法、模型 prompt、review gate 应回到子路径。
- 如果同一条规则要在 `A`、`B` 和 `C` 多个 lane 同时重复维护，先判断它是否属于父级；如果只影响某个 provider，就不要上升。
- 旧即时审计合同可以服务 resume 和兼容 runtime，但不应重新把 `3-初稿` 拉回八步主创拓扑。
- 监制层最适合沉到共享合同：三条 lane 都需要它，但 execution layer 不同；A 是 GPT 隔离监制 + GPT 主写作，B/C 是 GPT 监制 + 外部 provider 执行。
- 返工闭环必须记住“谁写的就回到谁那里改”：review 可以裁决质量，但不应把 B/C 的 provider ownership 变成 GPT 直接改稿。
- “启用 subagents”只授权真实分工与真实 reviewer/worker runtime，不自动授权切换正文主创模型；正文主创模型仍由 lane contract 决定。
- 初稿阶段的 subagents 监制不是临时另组顾问团；若项目 `team.yaml` 已锁定 `roles.production.members`，应把这些成员当资深创作顾问按领域请教，再把灵感转成执行约束给正文主创层。
- 字数不再作为初稿硬门槛；`字数: XXX字` 只是结果记录，正文篇幅由章级任务、叙事完整度和用户本轮明确要求决定。
- 角色声纹表解决“谁怎么说话”，角色关系图谱解决“他们靠什么发生关系”；两者都应进入初稿上下文。
- 新章上下文的连续性基础是“本卷全部前序章”，不是“最近上一章”；最近前章负责开章姿态，同卷早前章节负责伏笔、事实、关系、线索、道具、卷目标完成度、任务连续性、悬疑节奏把控性和文气边界。
- 情绪变化不要默认落在脸色颜色词上；成熟小说里惊吓、羞窘、愤怒和震动更应该通过动作停顿、呼吸、手部细节、视线、退让距离、物件误触和话语断裂显影。
- 章节编号、lane/provider、sidecar、frontmatter 和 context pack 都是执行证据层，不是小说世界的一部分；正文回指前事必须转成角色能看见、听见、记住或拿在手里的叙事事实。
