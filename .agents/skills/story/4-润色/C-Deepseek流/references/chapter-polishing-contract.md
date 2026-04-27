# Chapter Polishing Contract

本文件承载 `story-polishing-deepseek` 的章节润色稿细则。它不拥有入口路由权；调用时由 `SKILL.md` 决定何时加载。

## Stage Position

- 当前技能是 `story2026` 主链 `4-润色` 阶段的 `C-Deepseek流` provider 路径。
- 当 `4-润色` 路由选择 `C-Deepseek流` 时，当前技能拥有当前章润色稿根文件与 YAML 头的写权。
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

## Business Requirement Analysis

| analysis_slot | 当前结论 |
| --- | --- |
| `business_goal` | 让当前章在 3-初稿基础上形成可交付的二次润色稿；影响写作判断的 global/style/north-star/project-context 必须进入创作上下文与 sidecar，不再重复灌入正文 YAML 头。 |
| `business_object` | 当前章 3-初稿正文、当前章 planning、上游卷/整书规划、全局卡、风格卡、`north_star.yaml`、项目级 `MEMORY.md`、项目级 `CONTEXT/`、上一章正文。 |
| `constraint_profile` | planning 只给义务和约束，不能原样照抄进正文；DeepSeek 负责综合判断与小说化转译；脚本不得主创正文；若上一章存在，必须形成显式连续性桥。 |
| `success_criteria` | 目标文件成功落到 `projects/story/<项目名>/4-润色/第N卷/第N章.md`，YAML 头完整，正文具备章节级小说密度，并能读出承接、推进、章末牵引。 |
| `topology_fit` | `source lock -> context pack -> minimal frontmatter marker -> continuity bridge -> DeepSeek chapter generation -> final writeback` |

## Hard Rules

1. 当前技能的最小业务单元是“章”，不是“集”或“卷批次”。
2. 必须先锁定当前章 planning，再读取 global/style/north-star；不得反过来凭风格或世界观猜当前章该写什么。
3. YAML 头只保留 `润色模型: Deepseek` 与 `初稿来源`；禁止重复写入 planning 路径、cards 路径、项目上下文路径或 global/style/north-star 摘要。
4. `global_context`、`style_context`、`north_star_chapter_brief` 与各类引用路径由上下文包和 sidecar 承载，不再作为章节 frontmatter 必填项。
5. 若项目级 `CONTEXT/` 存在，必须在创作前真实加载并写入 sidecar 证据链；不得靠正文 YAML 空数组冒充加载。
6. 若上一章不存在，不得因此停止本章写作。
7. 若上一章存在，prompt 必须包含连续性桥：上一章末尾摘录、既成事实/人物位置/情绪余波/未完成动作/悬念压力，以及“本章不得重新开局”的开章约束。
8. 若上一章存在，`messages pack` / dry-run summary 必须能追溯实际加载的上一章路径；正文 frontmatter 仍不得写入 `previous_chapter_ref`。
9. 正文主体必须是小说 prose，不得把 `本章冲突 / 本章任务线 / 章末达成 / 规避` 原样复制成正文段落。
10. planning 中的“建议写法”只能转译成叙事动作、段落重心和章末牵引，不能原句粘贴。
11. 输出路径固定为 `projects/story/<项目名>/4-润色/第N卷/第N章.md`。
12. actual creative step 必须调用 `scripts/polish_chapter_via_deepseek.py`，并由它继续调用 `.agents/skills/api/deepseek/scripts/deepseek_chat.py`。
13. 正式写作默认启动 team supervision subagents；GPT/subagents 只做监制包与 prompt 约束，正文仍由 DeepSeek provider 执行。
14. DeepSeek 调用默认固定 `deepseek-v4-pro`、`thinking=enabled`、`reasoning_effort=high`。
15. 若 DeepSeek 返回内容不含完整 YAML frontmatter、`润色模型` 不等于 `Deepseek`、缺少 `# 第N章｜章标题` 标题行，必须判定为 provider output invalid，禁止直接写回业务真源。
16. provider 失败时只允许修 provider 输入、缩减 context、重试 provider、或向用户显式报告阻断；不允许静默回退到本地 GPT 直写。

## Frontmatter Contract

YAML 头至少包含：

- `润色模型`（固定为 `Deepseek`）
- `初稿来源`（固定为 `3-初稿/第N卷/第N章.md` 对应相对路径）

其余项目名、卷章号、章标题、规划引用、cards 引用、项目上下文引用、上一章引用与摘要字段均可由 canonical path、标题行、强上下文加载和 sidecar 追溯，不写入正文 YAML 头。

## Continuity Bridge Contract

- 上一章存在时，脚本必须把上一章末尾摘录作为优先承接材料，而不是只截取上一章开头。
- 连续性桥至少约束五件事：上一章既成事实、人物所在位置、情绪余波、未完成动作、悬念压力。
- 本章 planning 负责“要推进到哪里”，上一章末尾负责“从哪里入场”；两者冲突时，先保留上一章既成事实，再让本章事件完成推进。
- 开章可以跳时或换场，但必须补出因果过渡，不能让读者感觉这是另一条不相干的短篇。
- 章末必须继续留下对下一章的牵引，不得为了本章闭合而清空所有跨章压力。
- DeepSeek 流正文 frontmatter 保持极简；上一章路径、连续性桥和上下文引用由 messages pack、provider sidecar 与 dry-run summary 追溯。

## File Rules

- frontmatter 只记录 `润色模型`，不承载上下文引用或摘要。
- 正文主体不得保留“本章故事概要 / 本章冲突 / 规避”之类 planning 标题。
- 章末必须对齐当前章 planning 的 `exit_hook / 对下章的直接推动 / 章末达成` 中至少一项强义务。
- 当前技能默认不落盘 provider artifacts；业务真源只有 canonical 润色章节文件。
