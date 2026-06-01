# Chapter Polishing Contract

本文件承载 `story-polishing-deepseek` 的章节修补稿细则。它不拥有入口路由权；调用时由 `SKILL.md` 决定何时加载。

## Stage Position

- 当前技能是 `story2026` 主链 `4-润色` 阶段的 `C-Deepseek流` provider 路径。
- 当 `4-润色` 路由选择 `C-Deepseek流` 时，当前技能拥有当前章修补稿根文件与 YAML 头的写权。
- `projects/story/<项目名>/3-初稿/第V卷.写作日志.yaml` 等批次/恢复工件如仍存在，只视为 runtime 兼容载体，不再定义本技能的主创拓扑。

## Canonical Sources

- `../../SKILL.md`
- `../../CONTEXT.md`
- `../SKILL.md`（若非空，作为 `4-润色` 阶段路由层）
- `../CONTEXT.md`（若非空，作为 `4-润色` 阶段经验层）
- `../../_shared/context-loading-contract.md`
- `../../_shared/core-constraints.md`
- `../SKILL.md`
- `review/review-contract.md`
- `./templates/chapter-root.template.md`
- `./templates/deepseek-system-prompt.md`
- `./scripts/polish_chapter_via_deepseek.py`
- `../../../api/deepseek/SKILL.md`
- `../../../api/deepseek/CONTEXT.md`

## Total Input Contract

### 必需输入

- `projects/story/<项目名>/0-初始化/north_star.yaml`
- `projects/story/<项目名>/0-初始化/north_star.yaml`（`global_contract`、`style_contract`、`genre_contract`）
- `projects/story/<项目名>/2-卷章/整体规划.md`
- `projects/story/<项目名>/2-卷章/第N卷/卷规划.md`
- `projects/story/<项目名>/2-卷章/第N卷/第N章.md`
- `projects/story/<项目名>/3-初稿/第N卷/第N章.md`：当前章润色主输入，缺失时必须阻断。
- `volume_num / chapter_num`
- 当前项目名与目标输出路径
- DeepSeek provider 可用：`.env: DEEPSEEK_API_KEY`

### 条件必需输入

- `projects/story/<项目名>/MEMORY.md`：项目存在时必须加载。
- `projects/story/<项目名>/CONTEXT/**/*.md`：若存在，必须按当前章主题与卷任务相关性加载。
- `projects/story/<项目名>/3-初稿/第N卷/第N-1章.md`：若存在，必须读取。
- 当前 `projects/story/<项目名>/4-润色/第N卷/第N章.md`：若已存在，必须先回读。
- `supervision_packet`：正式写作时必须由 team supervision subagents 产出并进入 DeepSeek messages；若上层策略阻断真实 subagents，必须有降级报告。
- `review_subagent_packets`：用户显式要求 subagents 模式时必须按 `.agents/skills/story/review` 维度子技能生成，并转成 DeepSeek provider 可执行的 repair brief。

## Business Requirement Analysis

| analysis_slot | 当前结论 |
| --- | --- |
| `business_goal` | 让当前章在 3-初稿基础上形成可交付的最小局部修补稿；影响写作判断的 global/style/north-star/project-context 必须进入创作上下文与 sidecar，不再重复灌入正文 YAML 头。 |
| `business_object` | 当前章 3-初稿正文、当前章 planning、上游卷/整书规划、全局卡、风格卡、`north_star.yaml`、项目级 `MEMORY.md`、项目级 `CONTEXT/`、上一章正文。 |
| `constraint_profile` | planning 只给义务和约束，不能原样照抄进正文；DeepSeek 负责综合判断与小说化转译；脚本不得主创正文；若上一章存在，必须形成显式连续性桥。 |
| `success_criteria` | 目标文件成功落到 `projects/story/<项目名>/4-润色/第N卷/第N章.md`，YAML 头完整，正文保留初稿骨架和文本分布，并能读出承接、推进、章末牵引。 |
| `topology_fit` | `source lock -> context pack -> minimal frontmatter marker -> continuity bridge -> DeepSeek minimal local repair generation -> final writeback` |

## Hard Rules

1. 当前技能的最小业务单元是“章”，不是“集”或“卷批次”。
2. 必须先锁定当前章 planning，再读取 global/style/north-star；不得反过来凭风格或世界观猜当前章该写什么。
3. 最小局部修补是默认策略：保留初稿段落顺序、句群骨架、长短不齐、局部粗粝和人物原声；无用户显式授权时不得整章重排、短句化清洗或通用顺滑化。
4. YAML 头只保留 `润色模型: Deepseek`、`初稿来源` 与 `字数`；`字数` 按正文去除 frontmatter 与章节标题后的非空白字符数统计，格式为 `XXX字`；禁止重复写入 planning 路径、cards 路径、项目上下文路径或 global/style/north-star 摘要。
5. `global_context`、`style_context`、`north_star_chapter_brief` 与各类引用路径由上下文包和 sidecar 承载，不再作为章节 frontmatter 必填项。
6. 若项目级 `CONTEXT/` 存在，必须在创作前真实加载并写入 sidecar 证据链；不得靠正文 YAML 空数组冒充加载。
7. 若上一章不存在，不得因此停止本章写作。
8. 若上一章存在，prompt 必须包含连续性桥：上一章末尾摘录、既成事实/人物位置/情绪余波/未完成动作/悬念压力，以及“本章不得重新开局”的开章约束。
9. 若上一章存在，`messages pack` / dry-run summary 必须能追溯实际加载的上一章路径；正文 frontmatter 仍不得写入 `previous_chapter_ref`。
10. 正文主体必须是小说 prose，不得把 `本章冲突 / 本章任务线 / 章末达成 / 规避` 原样复制成正文段落。
11. planning 中的“建议写法”只能转译成叙事动作、段落重心和章末牵引，不能原句粘贴。
12. 输出路径固定为 `projects/story/<项目名>/4-润色/第N卷/第N章.md`。
13. actual creative step 必须调用 `scripts/polish_chapter_via_deepseek.py`，并由它继续调用 `.agents/skills/api/deepseek/scripts/deepseek_chat.py`。
14. 正式写作默认启动 team supervision subagents；GPT/subagents 只做监制包与 prompt 约束，正文仍由 DeepSeek provider 执行。
15. 用户显式要求 subagents 模式时，必须按 `../SKILL.md` 的 `Subagent Review-Optimize Contract` 调度 `story/review` 维度子技能；不同审计点分别由结构兑现、连续性、逻辑自洽校验、人物一致性、时间线、任务汇聚、文体读感等子技能审计，并在同轮注入 DeepSeek messages 直接执行最小优化。
16. DeepSeek 调用默认固定 `deepseek-v4-pro`、`thinking=enabled`、`reasoning_effort=high`。
17. 若 DeepSeek 返回内容不含完整 YAML frontmatter、`润色模型` 不等于 `Deepseek`、缺少 `# 第N章｜章标题` 标题行，必须判定为 provider output invalid，禁止直接写回业务真源。
18. provider 失败时只允许修 provider 输入、缩减 context、重试 provider、或向用户显式报告阻断；不允许静默回退到本地 GPT 直写。
19. 处理 AI 腔时必须定位到具体文本特征：过量因果连接词、段落长度高度均匀、主谓句异常完整、情绪词直接贴标签、解释性插入语过多、流程化总结句或角色共用作者口吻；不得用泛化“去 AI 味”触发整章重写。
20. 润色不得把场景密度当作冗余清除；物件细节、身体反应、空间距离、关系压力和信息延迟只要承担叙事功能，就应保留或做最小修补。
21. 润色不得把初稿节奏意图清洗成均衡顺句；长复合句、意识流碎片、断裂句、省略句和有意长短不齐的句群只修明确语病、歧义或坏点。

## Frontmatter Contract

YAML 头至少包含：

- `润色模型`（固定为 `Deepseek`）
- `初稿来源`（固定为 `3-初稿/第N卷/第N章.md` 对应相对路径）
- `字数`（当前润色正文去除 frontmatter 与章节标题后的非空白字符数，格式为 `XXX字`）

其余项目名、卷章号、章标题、规划引用、cards 引用、项目上下文引用、上一章引用与摘要字段均可由 canonical path、标题行、强上下文加载和 sidecar 追溯，不写入正文 YAML 头。

## Continuity Bridge Contract

- 上一章存在时，脚本必须把上一章末尾摘录作为优先承接材料，而不是只截取上一章开头。
- 连续性桥至少约束五件事：上一章既成事实、人物所在位置、情绪余波、未完成动作、悬念压力。
- 本章 planning 负责“要推进到哪里”，上一章末尾负责“从哪里入场”；两者冲突时，先保留上一章既成事实，再让本章事件完成推进。
- 开章可以跳时或换场，但必须补出因果过渡，不能让读者感觉这是另一条不相干的短篇。
- 章末必须继续留下对下一章的牵引，不得为了本章闭合而清空所有跨章压力。
- DeepSeek 流正文 frontmatter 保持极简；上一章路径、连续性桥和上下文引用由 messages pack、provider sidecar 与 dry-run summary 追溯。

## File Rules

- frontmatter 只记录 `润色模型`、`初稿来源` 与 `字数`，不承载上下文引用或摘要。
- 正文主体不得保留“本章故事概要 / 本章冲突 / 规避”之类 planning 标题。
- 章末必须对齐当前章 planning 的 `exit_hook / 对下章的直接推动 / 章末达成` 中至少一项强义务。
- 当前技能默认不落盘 provider artifacts；业务真源只有 canonical 润色章节文件。

## Review Gate Mapping

| Review Question | Review Gate | Fail Code | Rework Target | Report Evidence |
| --- | --- | --- | --- | --- |
| 是否锁定唯一项目根、卷章、`3-初稿` 源章和 canonical `4-润色` 输出路径？ | `context_loading` / `path_contract` | `FAIL-DSD-SOURCE` | `N1-SOURCE-LOCK`、`Input Contract` | source lock note、源章路径、输出路径 |
| 是否真实加载 planning、global/style/north-star、项目 `MEMORY.md`、项目 `CONTEXT/` 与同目录 `CONTEXT.md`？ | `context_loading` / `source_alignment` | `FAIL-DSD-CONTEXT` | `N3-CONTEXT-PACK` | messages pack refs、north_star 摘要、项目上下文加载清单 |
| 上一章存在时是否形成连续性桥，且不存在时没有硬阻断？ | `continuity` | `FAIL-DSD-CONTINUITY` | `N3-CONTEXT-PACK`、`N5*` | previous chapter ref、continuity bridge 摘要 |
| 是否保留初稿骨架、文本分布、场景密度和节奏起伏，没有无授权整章重排或短句化清洗？ | `minimal_repair` / `density_rhythm_preservation` / `prose_quality` | `FAIL-DSD-PROMPT` | `N4-DRAFT-BRANCH`、`N5*` | diff 摘要、修补范围说明、节奏密度检查 |
| AI 腔修补是否定位到具体文本特征，而不是泛化“更自然”？ | `anti_ai_features` | `FAIL-DSD-PROMPT` | `N5D-REPAIR-PROMPT` | 具体坏点清单、修补前后样本 |
| DeepSeek provider 是否真实命中固定模型与高推理路径，且失败时没有静默回退到 GPT 直写？ | `provider_evidence` / `script_boundary` | `FAIL-DSD-PROVIDER` | `N6-DEEPSEEK-DRAFT`、`scripts/polish_chapter_via_deepseek.py` | messages pack、raw output、provider report |
| 显式 subagents 模式是否完成 review 维度审计并通过 DeepSeek 同轮直接优化正文？ | `review_subagent_packets` | `FAIL-DSD-REVIEW-SUBAGENTS` | `N3R-REVIEW-SUBAGENT-AUDIT`、`N5D-REPAIR-PROMPT` | dimension packets、repair brief、provider 优化证据 |
| 输出是否满足极简 frontmatter、标题、完整正文和写回路径？ | `frontmatter` / `path_contract` | `FAIL-DSD-WRITEBACK` | `N7-VALIDATE-WRITEBACK`、`templates/output-template.md` | final chapter path、frontmatter check、heading check |
| 是否加载并遵守 guardrails，且无注入、provider 身份漂移或越权写入？ | `security` / `runtime_behavior` | `FAIL-DSD-PROVIDER` | `guardrails/guardrails-contract.md`、`types/guardrail-setup.md` | guardrail loaded note、injection scan、provider evidence |
