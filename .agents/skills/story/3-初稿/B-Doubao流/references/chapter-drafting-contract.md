# Chapter Drafting Contract

本文件承载 `story-drafting-doubao` 的章节正文细则。它不拥有入口路由权；调用时由根 `SKILL.md` 决定何时加载。

## Stage Position

- 当前技能是 `story2026` 主链 `3-初稿` 阶段的 `B-Doubao流` provider 路径，不再通过 `正文/` child 承接。
- 当 `3-初稿` 路由选择 `B-Doubao流` 时，当前技能拥有当前章正文根文件与 YAML 头的写权。
- `projects/story/<项目名>/3-初稿/第V卷.写作日志.yaml` 等批次/恢复工件如仍存在，只视为 runtime 兼容载体，不再定义本技能的主创拓扑。

## Canonical Sources

- `../../SKILL.md`
- `../../CONTEXT.md`
- `../SKILL.md`（若非空，作为 `3-初稿` 阶段路由层）
- `../CONTEXT.md`（若非空，作为 `3-初稿` 阶段经验层）
- `../../_shared/context-loading-contract.md`
- `../../_shared/core-constraints.md`
- `../_shared/supervised-drafting-review-loop-contract.md`
- `../_shared/drafting-instant-validation-contract.md`
- `./templates/chapter-root.template.md`
- `./templates/doubao-system-prompt.md`
- `./scripts/write_chapter_via_doubao.py`
- `../../../api/anyfast/llm/doubao-seed-2.0-pro/SKILL.md`
- `../../../api/anyfast/llm/doubao-seed-2.0-pro/CONTEXT.md`

## Total Input Contract

### 必需输入

- `projects/story/<项目名>/0-初始化/north_star.yaml`
- `projects/story/<项目名>/0-初始化/north_star.yaml`（`global_contract`、`style_contract`、`genre_contract`）
- `projects/story/<项目名>/2-卷章/整体规划.md`
- `projects/story/<项目名>/2-卷章/第N卷/卷规划.md`
- `projects/story/<项目名>/2-卷章/第N卷/第N章.md`
- `projects/story/<项目名>/1-设定/2-角色卡/角色关系图谱.md`（存在时必须加载）
- `volume_num / chapter_num`
- 当前项目名与目标输出路径

### 条件必需输入

- `projects/story/<项目名>/MEMORY.md`：项目存在时必须加载。
- `projects/story/<项目名>/CONTEXT/**/*.md`：若存在，必须按当前章主题与卷任务相关性加载。
- `projects/story/<项目名>/3-初稿/第N卷/第N-1章.md`：若存在，必须读取。
- 当前 `projects/story/<项目名>/3-初稿/第N卷/第N章.md`：若已存在，必须先回读。
- `projects/story/<项目名>/team.yaml`：正式写作启用 subagents 监制时必须加载，优先使用 `roles.production.members` 作为本章监制组候选真源。
- `supervision_packet`：正式写作时必须由 team supervision subagents 产出并进入 Doubao messages；该包必须记录项目 `team.yaml` roster 来源、向各领域大师请教的问题、顾问回答摘要和最终可执行指导；若上层策略阻断真实 subagents，必须有降级报告。

## Business Requirement Analysis

| analysis_slot | 当前结论 |
| --- | --- |
| `business_goal` | 让当前章直接形成可交付的章节级小说正文；影响写作判断的 global/style/north-star/project-context 必须进入创作上下文与 sidecar，不再重复灌入正文 YAML 头。 |
| `business_object` | 当前章 planning、上游卷/整书规划、全局卡、风格卡、`north_star.yaml`、项目级 `MEMORY.md`、项目级 `CONTEXT/`、上一章正文。 |
| `constraint_profile` | planning 只给义务和约束，不能原样照抄进正文；global/style 摘要必须短而可用；`north_star` 只提炼本章相关摘要；上一章是增强输入不是阻塞门；若上一章存在，必须形成显式连续性桥。 |
| `success_criteria` | 目标文件成功落到 `projects/story/<项目名>/3-初稿/第N卷/第N章.md`，YAML 头完整，正文具备章节级小说密度，并能读出承接、推进、章末牵引。 |
| `topology_fit` | `source lock -> context pack -> minimal frontmatter markers -> continuity bridge -> doubao chapter generation -> final writeback` |

## Hard Rules

1. 当前技能的最小业务单元是“章”，不是“集”或“卷批次”。
2. 必须先锁定当前章 planning，再读取 global/style/north-star；不得反过来凭风格或世界观猜当前章该写什么。
3. YAML 头只保留 `写作模型: Doubao` 与 `字数: XXX字`；禁止重复写入 planning 路径、cards 路径、项目上下文路径或 global/style/north-star 摘要。
4. 默认章节正文目标为 `2500-4000字`；若用户或上游 planning 明确给出其它区间，以显式区间为准，并由 `--min-words/--max-words` 传入脚本校验。
4. `global_context`、`style_context`、`north_star_chapter_brief` 与各类引用路径由上下文包和 sidecar 承载，不再作为章节 frontmatter 必填项。
5. 若项目级 `CONTEXT/` 存在，必须在创作前真实加载并写入 sidecar 证据链；不得靠正文 YAML 空数组冒充加载。
6. 若上一章不存在，不得因此停止本章写作。
7. 若上一章存在，prompt 必须包含连续性桥：上一章末尾摘录、既成事实/人物位置/情绪余波/未完成动作/悬念压力，以及“本章不得重新开局”的开章约束。
8. 若上一章存在，provider 上下文包与 sidecar 必须记录实际加载路径；正文 YAML 不再重复承载 `previous_chapter_ref`。
9. 正文主体必须是小说 prose，不得把 `本章冲突 / 本章任务线 / 章末达成 / 规避` 原样复制成正文段落。
10. planning 中的“建议写法”只能转译成叙事动作、段落重心和章末牵引，不能原句粘贴。
11. 输出路径固定为 `projects/story/<项目名>/3-初稿/第N卷/第N章.md`。
12. prompt 必须导入角色卡中的 `voice_and_presence`，形成可执行的角色对白声纹表；正文对白必须能体现人物身份、关系、情绪、利益和当前意图差异。
13. prompt 必须加载 `角色关系图谱.md` 摘录或等价关系投影，用于关系压力、联系方式、信息流、物件流和传导边判断；正文 frontmatter 不得写入该路径。
14. `不是……是……` 及其变体只允许偶尔用于关键反转，不得成为默认解释句式；同一场戏内不得连续使用。
15. actual creative step 必须调用 `scripts/write_chapter_via_doubao.py`，并由它继续调用 `doubao_seed_chat.py`。
16. 正式写作默认启动 team supervision subagents；具体模式为读取项目 `team.yaml -> roles.production.members`，把已指定监制组成员作为资深创作顾问逐一请教，并把其创意脑洞、个人风格判断和可执行指导汇流为写作前额外上下文。GPT/subagents 只做监制包与 prompt 约束，正文仍由 Doubao provider 执行。
17. 若目标章已存在，`auto` 不得静默转为正式覆写；必须由用户显式选择 `chapter_rewrite / chapter_continue / local_repair`，且正式写回必须传入 `--force`。
18. `chapter_continue` 必须提供续写边界或补充约束；`local_repair` 必须提供 review finding、局部问题描述或补充约束。
19. 若豆包返回内容不含完整可解析 YAML frontmatter、`写作模型` 不等于 `Doubao`、缺少 `字数: XXX字`、正文过短、仍含模板占位、缺少 `# 第N章｜章标题` 标题行，或句式重复门禁失败，必须判定为 provider output invalid，禁止直接写回业务真源。
20. provider 失败时只允许修 provider 输入、缩减 context、重试 provider、或向用户显式报告阻断；不允许静默回退到本地 GPT 直写。
21. 对现有章的 `local_repair`、`chapter_rewrite`、断尾补全、review 返工和卷级修复优化，正文创作性改写仍必须由 Doubao provider 执行；GPT/subagents 只能输出 repair brief、patch intent、风险清单和复核意见。
22. 若用户明确切换为 GPT 直接修复，必须退出本 lane 或改走 `A-GPT原生`，并同步调整 `写作模型` 与证据链；不得在 B lane 内静默切换主创模型。

## Frontmatter Contract

YAML 头至少包含：

- `写作模型`（固定为 `Doubao`）
- `字数`（格式为 `XXX字`，用于记录最终章节正文估算字数；默认应落在 `2500-4000字` 或本轮生效区间内）

其余项目名、卷章号、章标题、规划引用、cards 引用、项目上下文引用、上一章引用与摘要字段均可由 canonical path、标题行、强上下文加载和 sidecar 追溯，不写入正文 YAML 头。

## Continuity Bridge Contract

- 上一章存在时，脚本必须把上一章末尾摘录作为优先承接材料，而不是只截取上一章开头。
- 连续性桥至少约束五件事：上一章既成事实、人物所在位置、情绪余波、未完成动作、悬念压力。
- 本章 planning 负责“要推进到哪里”，上一章末尾负责“从哪里入场”；两者冲突时，先保留上一章既成事实，再让本章事件完成推进。
- 开章可以跳时或换场，但必须补出因果过渡，不能让读者感觉这是另一条不相干的短篇。
- 章末必须继续留下对下一章的牵引，不得为了本章闭合而清空所有跨章压力。

## File Rules

- frontmatter 只记录 `写作模型` 与 `字数`，不承载上下文引用或摘要。
- 正文主体不得保留“本章故事概要 / 本章冲突 / 规避”之类 planning 标题。
- 章末必须对齐当前章 planning 的 `exit_hook / 对下章的直接推动 / 章末达成` 中至少一项强义务。
- 当前技能默认不落盘 provider artifacts；业务真源只有 canonical 章节文件。
