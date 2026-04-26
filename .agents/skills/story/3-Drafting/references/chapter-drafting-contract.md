# Chapter Drafting Contract

本文件承载 `story-drafting` 的章节正文细则。它不拥有入口路由权；调用时由根 `SKILL.md` 决定何时加载。

## Stage Position

- 当前技能是 `story2026` 主链上的 `3-Drafting` 正式主技能，不再通过 `正文/` child 承接。
- 当前技能拥有当前章正文根文件与 YAML 头的写权。
- `projects/story/<项目名>/3-Drafting/第V卷.写作日志.yaml` 等批次/恢复工件如仍存在，只视为 runtime 兼容载体，不再定义本技能的主创拓扑。

## Canonical Sources

- `../SKILL.md`
- `../CONTEXT.md`
- `../_shared/context-loading-contract.md`
- `../_shared/core-constraints.md`
- `./templates/chapter-root.template.md`
- `./templates/doubao-system-prompt.md`
- `./scripts/write_chapter_via_doubao.py`
- `../../api/anyfast/llm/doubao-seed-2.0-pro/SKILL.md`
- `../../api/anyfast/llm/doubao-seed-2.0-pro/CONTEXT.md`

## Total Input Contract

### 必需输入

- `projects/story/<项目名>/0-Init/north_star.yaml`
- `projects/story/<项目名>/1-Cards/0-全局卡/**/*.json`
- `projects/story/<项目名>/1-Cards/1-风格卡/**/*.json`
- `projects/story/<项目名>/2-Planning/整体规划.md`
- `projects/story/<项目名>/2-Planning/第N卷/卷规划.md`
- `projects/story/<项目名>/2-Planning/第N卷/第N章.md`
- `volume_num / chapter_num`
- 当前项目名与目标输出路径

### 条件必需输入

- `projects/story/<项目名>/MEMORY.md`：项目存在时必须加载。
- `projects/story/<项目名>/CONTEXT/**/*.md`：若存在，必须按当前章主题与卷任务相关性加载。
- `projects/story/<项目名>/3-Drafting/第N卷/第N-1章.md`：若存在，必须读取。
- 当前 `projects/story/<项目名>/3-Drafting/第N卷/第N章.md`：若已存在，必须先回读。

## Business Requirement Analysis

| analysis_slot | 当前结论 |
| --- | --- |
| `business_goal` | 让当前章直接形成可交付的章节级小说正文，并把影响写作判断的 global/style/north-star/project-context 显式挂进 YAML 头。 |
| `business_object` | 当前章 planning、上游卷/整书规划、全局卡、风格卡、`north_star.yaml`、项目级 `MEMORY.md`、项目级 `CONTEXT/`、上一章正文。 |
| `constraint_profile` | planning 只给义务和约束，不能原样照抄进正文；global/style 摘要必须短而可用；`north_star` 只提炼本章相关摘要；上一章是增强输入不是阻塞门。 |
| `success_criteria` | 目标文件成功落到 `projects/story/<项目名>/3-Drafting/第N卷/第N章.md`，YAML 头完整，正文具备章节级小说密度，并能读出承接、推进、章末牵引。 |
| `topology_fit` | `source lock -> context pack -> frontmatter synthesis -> continuity bridge -> doubao chapter generation -> final writeback` |

## Hard Rules

1. 当前技能的最小业务单元是“章”，不是“集”或“卷批次”。
2. 必须先锁定当前章 planning，再读取 global/style/north-star；不得反过来凭风格或世界观猜当前章该写什么。
3. YAML 头必须显式包含 `global_context`、`style_context` 与 `north_star_chapter_brief`，三者缺一不可。
4. `global_context` 只保留会直接影响本章判断的世界规则、势力压力或舞台约束；禁止整份全局卡照抄。
5. `style_context` 只保留本章落笔需要的语体、气压、叙事/对白/画面抓手；禁止整份风格卡照抄。
6. `north_star_chapter_brief` 必须是“`north_star.yaml` + 当前章 planning”的压缩摘要，不得伪装成 `north_star.yaml` 原文摘录。
7. 若项目级 `CONTEXT/` 存在，不能只在 YAML 头里留空数组；必须留下真实命中的 `project_context_refs`，或显式写 `[]` 并说明无相关文件。
8. 若上一章不存在，`previous_chapter_ref` 可为空，但不得因此停止本章写作。
9. 正文主体必须是小说 prose，不得把 `本章冲突 / 本章任务线 / 章末达成 / 规避` 原样复制成正文段落。
10. planning 中的“建议写法”只能转译成叙事动作、段落重心和章末牵引，不能原句粘贴。
11. 输出路径固定为 `projects/story/<项目名>/3-Drafting/第N卷/第N章.md`。
12. actual creative step 必须调用 `scripts/write_chapter_via_doubao.py`，并由它继续调用 `doubao_seed_chat.py`。
13. 若豆包返回内容不含完整 YAML frontmatter、缺少必需字段、缺少 `# 第N章｜章标题` 标题行，必须判定为 provider output invalid，禁止直接写回业务真源。
14. provider 失败时只允许修 provider 输入、缩减 context、重试 provider、或向用户显式报告阻断；不允许静默回退到本地 GPT 直写。

## Frontmatter Contract

YAML 头至少包含：

- `story_name`
- `volume_num`
- `chapter_num`
- `chapter_title`
- `planning_global_ref`
- `planning_volume_ref`
- `planning_chapter_ref`
- `rhythm_type`
- `global_card_refs`
- `style_card_refs`
- `north_star_ref`
- `project_context_refs`
- `previous_chapter_ref`
- `global_context`
- `style_context`
- `north_star_chapter_brief`

其中关键槽位固定如下：

- `global_context`
  - `worldview_summary`
  - `rule_pressure`
  - `faction_or_system_pressure`
- `style_context`
  - `tone_summary`
  - `prose_summary`
  - `dialogue_summary`
- `north_star_chapter_brief`
  - 用一段 2-4 句中文，说明这一章在整书承诺里为什么成立、要把哪种压力从 planning 推进成戏内动作、章末应把什么牵到下一章。

## File Rules

- frontmatter 只记录写作约束与引用，不在正文段落中重复解释。
- 正文主体不得保留“本章故事概要 / 本章冲突 / 规避”之类 planning 标题。
- 章末必须对齐当前章 planning 的 `exit_hook / 对下章的直接推动 / 章末达成` 中至少一项强义务。
- 当前技能的 provider artifacts 不是业务真源。
