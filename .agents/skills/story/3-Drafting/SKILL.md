---
name: story-write
description: Use when the user asks to write, continue, or revise a chapter inside an existing story2026 novel project.
governance_tier: lite
allowed-tools: Read Write Edit Grep Bash Task
---

# Chapter Writing (Structured Workflow)

> Canonical note: `3-Drafting` 已内含正式润色关口，Step 4 就是当前唯一的 polish 执行位；不再单设独立 `4-Polish` 技能包。

## Context Loading Contract

- 每次调用本技能时，必须同时加载同目录 `CONTEXT.md`。
- `CONTEXT.md` 只承载章节写作经验、返工线索与 craft 启发，不得覆盖本 `SKILL.md` 的 step 合同与写回门禁。
- 若 `CONTEXT.md` 与 `references/` 中的 step-playbook 冲突，以本 `SKILL.md` 与对应 `module-spec.md` 为准。

## 目标

- 以稳定流程产出可发布章节：优先使用 `正文/第{NNNN}章-{title_safe}.md`，无标题时回退 `正文/第{NNNN}章.md`。
- 默认章节字数目标：2000-2500（用户或章节规划节点明确覆盖时从其约定）。
- 保证审查、润色、数据回写完整闭环，避免“写完即丢上下文”。
- 润色职责固定收束在本 skill 的 Step 4，不再依赖额外 stage 包装。
- 输出直接可被后续章节消费的结构化数据：`review_metrics`、`summaries`、`chapter_meta`。

## 执行原则

1. 先校验输入完整性，再进入写作流程；缺关键输入时立即阻断。
2. 审查与数据回写是硬步骤，`--fast`/`--minimal` 只允许降级可选环节。
3. 参考资料严格按步骤按需加载，不一次性灌入全部文档。
4. Step 2B 与 Step 4 职责分离：2B 只做风格转译，4 只做问题修复与质控。
5. Step 4 是 canonical polish gate；若出现表达层修复需求，统一在这里闭环。
6. 任一步失败优先做最小回滚，不重跑全流程。

## Shadow Governance Artifact Chain (Mandatory)

当 `3-Drafting` 通过 tracked workflow 运行时，必须承认本轮 run 的三省 shadow 工件链：

- `<project_root>/.webnovel/tasks/<run_id>/mandate.yaml`
- `<project_root>/.webnovel/tasks/<run_id>/mission_brief.yaml`
- `<project_root>/.webnovel/tasks/<run_id>/artifact_manifest.json`
- `<project_root>/.webnovel/tasks/<run_id>/validation_report.md`
- `<project_root>/.webnovel/tasks/<run_id>/learning_record.md`

边界：

- 这些文件是证据层与闭环层，不替代 `.webnovel/state.json / workflow_state.json / execution_state.json`。
- Step 3-5 的正式结果必须能回填到 `artifact_manifest.json` 与最终 `validation_report.md`。
- 若发生失败，必须允许同一 `<run_id>/root_cause_trace.md` 承接失败闭环。

## TEAM 阶段治理（Mandatory）

- 执行 `3-Drafting` 前，必须读取项目根 `TEAM.toml`，并把 `["监制"]` 视为本阶段的唯一团队治理入口。
- 若满足以下任一条件，即视为监制专家组已激活：
  - `TEAM.toml["监制"].智能顾问团 = true`
  - `TEAM.toml["监制"].成员` 非空
- 监制专家组已激活时：
  - 必须创建后台多 subagents，围绕本章的推进策略、戏剧重心、镜头/场景调度、情绪波形、章节标题与 hook 落点形成结构化制作决议。
  - 这些决议必须进入 Step 1 的章节级创作执行包，并在 Step 4 / Step 5 的正式写回中留下可追溯的执行依据。
  - 监制专家组负责“怎么把这一章做得成立”，但**不替代** Step 3 的正式审查团队。
- `TEAM.toml["监制"].管辖` 是 stage-route sanity check；若未覆盖 `3-Drafting`，必须报告团队治理配置漂移。
- 若 `TEAM.toml["监制"]` 未激活，则维持当前默认单主流程模式，但仍要在执行说明中明确“本轮无监制专家组介入”。

## 模式定义

- `/story-write`：Step 1 → 2A → 2B → 3 → 4 → 5 → 6
- `/story-write --fast`：Step 1 → 2A → 3 → 4 → 5 → 6（跳过 2B）
- `/story-write --minimal`：Step 1 → 2A → 3（仅3个基础审查）→ 4 → 5 → 6

最小产物（所有模式）：
- `正文/第{NNNN}章-{title_safe}.md` 或 `正文/第{NNNN}章.md`
- `index.db.review_metrics` 新纪录（含 `overall_score`）
- `.webnovel/summaries/ch{NNNN}.md`
- `.webnovel/state.json` 的进度与 `chapter_meta` 更新

### 流程硬约束（禁止事项）

- **禁止并步**：不得将两个 Step 合并为一个动作执行（如同时做 2A 和 3）。
- **禁止跳步**：不得跳过未被模式定义标记为可跳过的 Step。
- **禁止临时改名**：不得将 Step 的输出产物改写为非标准文件名或格式。
- **禁止自创模式**：`--fast` / `--minimal` 只允许按上方定义裁剪步骤，不允许自创混合模式、"半步"或"简化版"。
- **禁止自审替代**：Step 3 审查必须由 Task 子代理执行，主流程不得内联伪造审查结论。
- **禁止源码探测**：脚本调用方式以本文档与 data-agent 文档中的命令示例为准，命令失败时查日志定位问题，不去翻源码学习调用方式。

## 引用加载等级（strict, lazy）

- L0：未进入对应步骤前，不加载任何参考文件。
- L1：每步仅加载该步“必读”文件。
- L2：仅在触发条件满足时加载“条件必读/可选”文件。

路径约定：
- `references/...` 相对当前 skill 目录。
- `../../references/...` 指向全局共享参考。

## Reference Loading Guide

- 默认判定顺序：`step 模块 -> 条件命中时进入 writing craft 模块 -> 必要时再读模块附属 appendix`
- 默认入口：Step 1 / 2B / 3 / 4 / 5 各自先进入对应 `references/<module>/module-spec.md`
- 互斥规则：`step-2-style-pass` 与 `step-4-polish-gate` 都能改正文，但前者只做表达层转译，后者只做问题修复与质控，二者不得互相替代
- 串行规则：`step-1-context-contract -> Step 2A`，`step-3-review-gate -> step-4-polish-gate -> step-5-data-writeback`
- 按需加载规则：`writing-craft-catalog` 只在题材命中、审查命中或写作症状命中时作为二级模块进入，不单独拥有路由权

| 模块 | 触发条件 | 进入信号 | 与其他模块关系 | 必读文件 |
| --- | --- | --- | --- | --- |
| `step-1-context-contract` | 进入 Step 1，或 Step 1 输出仍像“资料罗列”而不是“创作执行包” | Layer A-E 缺板块、Context Contract 缺字段、开头/钩子差异化需要裁决 | 起草前置模块；可按需串到 `writing-craft-catalog` | `references/step-1-context-contract/module-spec.md` |
| `step-2-style-pass` | 进入 Step 2B | 需要把 Step 2A 草稿转成更稳的网文表达，但不能改剧情事实 | 只服务 Step 2B；可按需串到 `writing-craft-catalog` | `references/step-2-style-pass/module-spec.md` |
| `step-3-review-gate` | 进入 Step 3 | 需要通过 `4-Validation` 生成隔离审查团队、聚合结果并落库 | Step 4 的上游硬闸门 | `references/step-3-review-gate/module-spec.md` |
| `step-4-polish-gate` | 进入 Step 4 | 已拿到审查问题包，需要修复问题并完成 Anti-AI / No-Poison / 排版终检 | Step 3 下游、Step 5 上游；可按需串到 `writing-craft-catalog` | `references/step-4-polish-gate/module-spec.md` |
| `step-5-data-writeback` | 进入 Step 5 | 需要把章节文件、审查分数和状态回写统一闭环，并判定债务利息是否开启 | 正式写回模块；不回流改写 Step 1-4 | `references/step-5-data-writeback/module-spec.md` |
| `writing-craft-catalog` | Step 1 / 2B / 4 命中题材或 craft 症状 | 需要对战斗、对白、情绪、节奏、氛围、排版、题材 hook 做局部强化 | 二级按需模块，不单独替代 step 模块 | `references/writing-craft-catalog/module-spec.md` |

### 全局共享参考

- `../../references/shared/core-constraints.md`
  - 用途：Step 2A 写作硬约束（规划真源即法律 / 设定即物理 / 发明需识别）。
  - 触发：Step 2A 必读。
- `../../references/reading-power-taxonomy.md`
  - 用途：Step 1 中为钩子、爽点、微兑现建立 taxonomy。
  - 触发：当需要追读力设计时加载。
- `../../references/genre-profiles.md`
  - 用途：Step 1 中按题材配置节奏阈值与钩子偏好。
  - 触发：当 `state.project.genre` 已知时加载。

### 模块附属 Appendix 说明

- `references/` 根目录下保留的旧单文件现在只作为模块附属 appendix 或迁移入口，不再从根 `SKILL.md` 直接路由。
- 具体 leaf docs 的进入顺序由对应 `module-spec.md` 决定；根技能不再直连 `references/writing-craft-catalog/leaf-notes/*.md` 或旧 root appendix 单文件。

## 上游上下文加载矩阵（Mandatory）

`3-Drafting` 进入写作阶段后，默认目标不是“把 `0-Init / 1-Cards / 2-Planning` 全量重读一遍”，而是把上游真源压缩成一个**章节级创作执行包**。

固定原则：

1. `0-Init` 提供“用户承诺与禁飞区”，不再回灌整轮问卷原文。
   - 默认优先读取 `Init/north_star_contract.json.story_kernel / reader_promise / aesthetic_axes / ip_boundary`，必要时参考 `Init/初始化简报.json.planning_seed`。
2. `1-Cards` 提供“对象真源与长期约束”，但默认只做与本章相关的定向切片，不整库灌入。
3. `2-Planning` 提供“章节编排真源”，默认入口固定为 `Planning/8-全息地图.json`。
4. `3-Drafting` 只消费“本章需要发生什么 + 当前状态是什么 + 本章相关对象怎么约束 + 本章该怎么写”，不重新发明上游裁决。

### 五层加载结构

#### Layer A：必载硬约束层（Mandatory）

来源：
- `0-Init` 的最终确认项 / 项目承诺
- `Init/north_star_contract.json（cards 分区）`
- `.webnovel/state.json` 中的题材、项目信息与当前默认约束

默认加载内容：
- 题材走廊、平台承诺、规模目标
- 风格契约、叙事禁飞区、商业承诺
- 世界规则、力量边界、全局禁令

规则：
- 这层负责回答“这本书允许怎样写 / 不允许怎样写”。
- 禁止回读初始化问卷全文冒充约束层。

#### Layer B：本章编排真源层（Mandatory）

来源：
- `Planning/8-全息地图.json`
- 仅在 `MAP` 缺失时，允许回退到 legacy `Planning/legacy/`

默认加载内容：
- 当前章 `chapter_board`
- 时间锚点、卷篇定位、章节功能
- 本章事件 / 冲突 / 任务 / 线索 / 伏笔 / 角色 / 场景 / 物品 / 规则影响 / 状态变化

规则：
- 这层负责回答“本章必须发生什么、挂哪些对象、承担什么章节职责”。
- 默认禁止直接把 `Planning/1-7/*.json` 当作 Step 1 主输入；它们只作为追溯层存在。

#### Layer C：章节运行态层（Mandatory）

来源：
- `.webnovel/state.json`
- `.webnovel/summaries/ch{N-1}.md`
- `.webnovel/summaries/ch{N-2}.md`
- 最近章节 `chapter_meta / review_metrics / reading_power`

默认加载内容：
- 主角当前状态、当前位置、当前实力、关键压力位
- 最近两章摘要与承接钩子
- 最近章节节奏 / 审查 / 追读信号

规则：
- 这层负责回答“本章从哪里接上、当前人物和局势处于什么状态”。
- 不负责改写世界规则或章节规划。

#### Layer D：对象定向切片层（Targeted Slice）

来源：
- `Cards/2-角色卡/**/*.json`
- `Cards/3-场景卡/**/*.json`
- `Cards/4-物品卡/**/*.json`

默认加载方式：
- 以当前章 `chapter_board` 点名对象为第一优先
- 以 `state.json` 当前地点 / 当前持有 / 最近出场对象为第二优先
- 仅加载与当前章直接相关的角色卡、场景卡、物品卡切片

默认加载内容：
- 角色声口、关系边、欲望/缺陷、当前成长锚点
- 场景规则、可进入条件、危险与叙事功能
- 物品归属链、代价、触发条件、叙事作用

规则：
- 这层负责回答“本章涉及的人/地/物各自带着什么约束进场”。
- 禁止默认全量加载整库角色卡 / 场景卡 / 物品卡。

#### Layer E：自适应写作引导层（Adaptive Guidance）

来源：
- `reader_signal`
- `genre_profile`
- `writing_guidance`
- 可触发时的 `rag_assist`

默认加载内容：
- 最近低分区间、hook/pattern 使用趋势、审查均分
- 当前题材提示、复合题材提醒、方法论策略卡
- 针对本章的 guidance checklist 与执行建议

规则：
- 这层负责回答“这章怎样写得更稳、更贴题材、更不重复”。
- 它只优化写法，不替代 Layer B 的剧情真源。

### 追溯层与禁止项

可按需追溯：
- `Planning/1-题材选型.json`
- `Planning/2-章节规划.json`
- `Planning/3-故事大纲.json`
- `Planning/4-7/*.json`

追溯触发：
- 当前章 `chapter_board` 信息不足
- 需要回答“为什么排在这里 / 为什么由此对象承担”
- 需要排查冲突、任务、线索、伏笔的长线断裂

禁止项：
- 禁止把 `0-Init` 原始问卷、全量 Cards、全量 planning passes 一次性灌入 Step 1
- 禁止把写作参考文档当作上游真源替代 `MAP`
- 禁止让 RAG 命中片段反客为主覆盖 `chapter_board`

## 工具策略（按需）

- `Read/Grep`：读取 `state.json`、`Planning/8-全息地图.json`、章节正文与参考文件。
- `Bash`：运行 `extract_chapter_context.py`、`index_manager`、`workflow_manager`。
- `Task`：调用 `context-agent`、监制 subagents、审查 subagent、`data-agent` 并行执行。

## 交互流程

### Step 0：预检与上下文最小加载

必须做：
- 解析真实书项目根（book project_root）：必须包含 `.webnovel/state.json`。
- 校验核心输入：`Planning/8-全息地图.json`、`.agents/skills/story/scripts/extract_chapter_context.py` 存在。
- 读取 `TEAM.toml`，判定 `["监制"]` 是否激活；若激活，必须先生成本章监制专家组简报，再进入 Step 1。
- 兼容回退输入：若 `Planning/8-全息地图.json` 缺失，可临时回退到 `Planning/legacy/`，但必须报告“当前处于 legacy outline fallback”。
- 规范化变量：
  - `WORKSPACE_ROOT`：Claude Code 打开的工作区根目录（可能是书项目的父目录，例如 `D:\wk\xiaoshuo`）
  - `REPO_ROOT`：当前本地仓库根目录（默认同 `WORKSPACE_ROOT`）
  - `PROJECT_ROOT`：真实书项目根目录（必须包含 `.webnovel/state.json`，例如 `D:\wk\xiaoshuo\凡人资本论`）
  - `SKILL_ROOT`：skill 所在目录（固定 `${REPO_ROOT}/.agents/skills/story/3-Drafting`）
  - `SCRIPTS_DIR`：脚本目录（固定 `${REPO_ROOT}/.agents/skills/story/scripts`）
  - `chapter_num`：当前章号（整数）
  - `chapter_padded`：四位章号（如 `0001`、`0007`）

环境设置（bash 命令执行前）：
```bash
export WORKSPACE_ROOT="${CLAUDE_PROJECT_DIR:-$PWD}"
export REPO_ROOT="${CLAUDE_PROJECT_DIR:-$PWD}"
export SCRIPTS_DIR="${REPO_ROOT}/.agents/skills/story/scripts"
export SKILL_ROOT="${REPO_ROOT}/.agents/skills/story/3-Drafting"

python -X utf8 "${SCRIPTS_DIR}/story.py" --project-root "${WORKSPACE_ROOT}" preflight
export PROJECT_ROOT="$(python -X utf8 "${SCRIPTS_DIR}/story.py" --project-root "${WORKSPACE_ROOT}" where)"
```

**硬门槛**：`preflight` 必须成功。它统一校验当前仓库派生出的 `SKILL_ROOT` / `SCRIPTS_DIR`、`story.py`、`extract_chapter_context.py` 和解析出的 `PROJECT_ROOT`。任一失败都立即阻断。

输出：
- “已就绪输入”与“缺失输入”清单；缺失则阻断并提示先补齐。
- 若 `TEAM.toml["监制"]` 已激活，还必须输出“监制专家组已加载 / 本轮坐镇 AGENTS / 是否覆盖 `3-Drafting` 管辖”的预检结论。

### Step 0.5：工作流断点记录（best-effort，不阻断）

```bash
python -X utf8 "${SCRIPTS_DIR}/story.py" --project-root "${PROJECT_ROOT}" workflow start-task --command story-write --chapter {chapter_num} || true
python -X utf8 "${SCRIPTS_DIR}/story.py" --project-root "${PROJECT_ROOT}" workflow start-step --step-id "Step 1" --step-name "Context Agent" || true
python -X utf8 "${SCRIPTS_DIR}/story.py" --project-root "${PROJECT_ROOT}" workflow complete-step --step-id "Step 1" --artifacts '{"ok":true}' || true
python -X utf8 "${SCRIPTS_DIR}/story.py" --project-root "${PROJECT_ROOT}" workflow complete-task --artifacts '{"ok":true}' || true
```

要求：
- `--step-id` 仅允许：`Step 1` / `Step 2A` / `Step 2B` / `Step 3` / `Step 4` / `Step 5` / `Step 6`。
- 任何记录失败只记警告，不阻断写作。
- 每个 Step 执行结束后，同样需要 `complete-step`（失败不阻断）。

### Step 1：Context Agent（内置 Context Contract，生成直写执行包）

执行前按需加载：
```bash
cat "${SKILL_ROOT}/references/step-1-context-contract/module-spec.md"
```

使用 Task 调用 `context-agent`，参数：
- `chapter`
- `project_root`
- `storage_path=.webnovel/`
- `state_file=.webnovel/state.json`

硬要求：
- 若 `state` 不可用，立即阻断并返回缺失项。
- 若 `全息地图` 缺失，先报告并确认当前只能使用 legacy outline fallback；不得把旧 `Planning/legacy/` 描述成默认真源。
- Step 1 必须按“Layer A-E”输出章节级执行包，不得退回“上游整包罗列”。
- 对 `1-Cards` 默认只输出与本章直接相关的角色 / 场景 / 物品切片，不输出整库 dump。
- 若需要为开头类型、钩子类型、情绪节奏、题材 hook 或 craft 症状做进一步裁决，先由 `step-1-context-contract` 模块决定，再按需进入 `writing-craft-catalog`。
- 输出必须同时包含：
  - Layer A：硬约束摘要（题材/风格/规则/禁飞区）；
  - Layer B：本章编排板块（目标/冲突/任务/线索/伏笔/角色/场景/物品/章节功能）；
  - Layer C：运行态承接（前文摘要、当前状态、当前压力位）；
  - Layer D：对象切片（相关角色/场景/物品的约束摘要）；
  - Layer E：写作引导（追读力、题材提示、执行建议、RAG 命中）；
  - 7 板块任务书（目标/冲突/承接/角色/场景约束/伏笔/追读力）；
  - Context Contract 全字段（目标/阻力/代价/本章变化/未闭合问题/开头类型/情绪节奏/信息密度/过渡章判定/追读力设计）；
  - Step 2A 可直接消费的“写作执行包”（章节节拍、不可变事实清单、禁止事项、终检清单）。
- 合同与任务书出现冲突时，以“全息地图章节节点与设定约束更严格者”为准。

输出：
- 单一“创作执行包”（Layer A-E + 任务书 + Context Contract + 直写提示词），供 Step 2A 直接消费，不再拆分额外中间步骤。

### Step 2A：正文起草

执行前必须加载：
```bash
cat "${SKILL_ROOT}/../../references/shared/core-constraints.md"
```

硬要求：
- 只输出纯正文到章节正文文件；若全息地图章节节点已有章节名，优先使用 `正文/第{chapter_padded}章-{title_safe}.md`，否则回退为 `正文/第{chapter_padded}章.md`。
- 默认按 2000-2500 字执行；若全息地图章节节点标明关键战斗章/高潮章/卷末章或用户明确指定，则按规划/用户优先。
- 禁止占位符正文（如 `[TODO]`、`[待补充]`）。
- 保留承接关系：若上章有明确钩子，本章必须回应（可部分兑现）。

中文思维写作约束（硬规则）：
- **禁止"先英后中"**：不得先用英文工程化骨架（如 ABCDE 分段、Summary/Conclusion 框架）组织内容，再翻译成中文。
- **中文叙事单元优先**：以"动作、反应、代价、情绪、场景、关系位移"为基本叙事单元，不使用英文结构标签驱动正文生成。
- **禁止英文结论话术**：正文、审查说明、润色说明、变更摘要、最终报告中不得出现 Overall / PASS / FAIL / Summary / Conclusion 等英文结论标题。
- **英文仅限机器标识**：CLI flag（`--fast`）、checker id（`consistency-checker`）、DB 字段名（`anti_ai_force_check`）、JSON 键名等不可改的接口名保持英文，其余一律使用简体中文。

输出：
- 章节草稿（可进入 Step 2B 或 Step 3）。

### Step 2B：风格适配（`--fast` / `--minimal` 跳过）

执行前加载：
```bash
cat "${SKILL_ROOT}/references/step-2-style-pass/module-spec.md"
```

硬要求：
- 只做表达层转译，不改剧情事实、事件顺序、角色行为结果、设定规则。
- 对“模板腔、说明腔、机械腔”做定向改写，为 Step 4 留出问题修复空间。

输出：
- 风格化正文（覆盖原章节文件）。

### Step 3：审查（auto 路由，经 `4-Validation` 创建隔离评估团队）

执行前加载：
```bash
cat "${SKILL_ROOT}/references/step-3-review-gate/module-spec.md"
```

调用约束：
- 必须先进入 `4-Validation`，由其创建新的后台多智能体团队完成本轮检验。
- 禁止主流程直接复用旧 checker 线程或伪造审查结论。
- 禁止把 `TEAM.toml["监制"]` 的监制专家组冒充 Step 3 checker；监制只负责制作决议，正式质量裁决仍由 `4-Validation` 隔离团队给出。
- 团队内部可并行发起审查，统一汇总 `issues/severity/overall_score`。
- 默认使用 `auto` 路由：根据“本章执行合同 + 正文信号 + 章节规划标签”动态选择审查器。

核心审查器（始终执行）：
- `consistency-checker`
- `continuity-checker`
- `ooc-checker`

条件审查器（`auto` 命中时执行）：
- `reader-pull-checker`
- `high-point-checker`
- `pacing-checker`

模式说明：
- 标准/`--fast`：核心 3 个 + auto 命中的条件审查器
- `--minimal`：只跑核心 3 个（忽略条件审查器）

审查指标落库（必做）：
```bash
python -X utf8 "${SCRIPTS_DIR}/story.py" --project-root "${PROJECT_ROOT}" index save-review-metrics --data "@${PROJECT_ROOT}/.webnovel/tmp/review_metrics.json"
```

- `4-Validation` 负责产出聚合结果，`review/` 负责生成 `review_metrics.json` 并落库。

review_metrics 字段约束（当前工作流约定只传以下字段）：
```json
{
  "start_chapter": 100,
  "end_chapter": 100,
  "overall_score": 85.0,
  "dimension_scores": {"爽点密度": 8.5, "设定一致性": 8.0, "节奏控制": 7.8, "人物塑造": 8.2, "连贯性": 9.0, "追读力": 8.7},
  "anti_ai_force_check": "pending",
  "spoiler_risk": "low",
  "contrivance_risk": "medium",
  "cold_commentary_risk": "low",
  "severity_counts": {"critical": 0, "high": 1, "medium": 2, "low": 0},
  "critical_issues": ["问题描述"],
  "report_file": "Validation/第100-100章审查报告.md",
  "notes": "单个字符串；selected_agents / validation_mode / routing_decision / timeline_gate 等扩展信息压成单行文本写入此字段"
}
```
- `notes` 在当前执行契约中必须是单个字符串，不得传入对象或数组。
- `anti_ai_force_check / spoiler_risk / contrivance_risk / cold_commentary_risk` 必须作为正式字段传入，不得藏在 `notes`。
- 当前工作流不额外传入其它顶层字段；脚本侧未在此处做新增硬校验。

硬要求：
- `--minimal` 也必须产出 `overall_score`。
- 本轮 `overall_score` 必须来自新的隔离评估团队。
- 未落库 `review_metrics` 不得进入 Step 5。

### Step 4：润色（问题修复优先）

说明：
- 本步骤就是写作链中的正式润色阶段，不再额外路由到独立 `4-Polish` skill。
- 若问题属于事实层、规划层或设定层，应回退到更上游合同处理，不能把 Step 4 用成重写剧情入口。

执行前必须加载：
```bash
cat "${SKILL_ROOT}/references/step-4-polish-gate/module-spec.md"
```

执行顺序：
1. 修复 `critical`（必须）
2. 修复 `high`（不能修复则记录 deviation）
3. 处理 `medium/low`（按收益择优）
4. 执行 Anti-AI 与 No-Poison 全文终检（必须输出 `anti_ai_force_check: pass/fail`）

输出：
- 润色后正文（覆盖章节文件）
- 变更摘要（至少含：修复项、保留项、deviation、`anti_ai_force_check`）

### Step 5：Data Agent（状态与索引回写）

执行前加载：
```bash
cat "${SKILL_ROOT}/references/step-5-data-writeback/module-spec.md"
```

使用 Task 调用 `data-agent`，参数：
- `chapter`
- `chapter_file` 必须传入实际章节文件路径；若全息地图章节节点已有章节名，优先传 `正文/第{chapter_padded}章-{title_safe}.md`，否则传 `正文/第{chapter_padded}章.md`
- `review_score=Step 3 overall_score`
- `project_root`
- `storage_path=.webnovel/`
- `state_file=.webnovel/state.json`

Data Agent 默认子步骤（全部执行）：
- A. 加载上下文
- B. AI 实体提取
- C. 实体消歧
- D. 写入 state/index
- E. 写入章节摘要
- F. AI 场景切片
- G. RAG 向量索引（`rag index-chapter --scenes ...`）
- H. 风格样本评估（`style extract --scenes ...`，仅 `review_score >= 80` 时）
- I. 债务利息（默认跳过）

`--scenes` 来源优先级（G/H 步骤共用）：
1. 优先从 `index.db` 的 scenes 记录获取（Step F 写入的结果）
2. 其次按 `start_line` / `end_line` 从正文切片构造
3. 最后允许单场景退化（整章作为一个 scene）

Step 5 失败隔离规则：
- 若 G/H 失败原因是 `--scenes` 缺失、scene 为空、scene JSON 格式错误：只补跑 G/H 子步骤，不回滚或重跑 Step 1-4。
- 若 A-E 失败（state/index/summary 写入失败）：仅重跑 Step 5，不回滚已通过的 Step 1-4。
- 禁止因 RAG/style 子步骤失败而重跑整个写作链。

执行后检查（最小白名单）：
- `.webnovel/state.json`
- `.webnovel/index.db`
- `.webnovel/summaries/ch{chapter_padded}.md`
- `.webnovel/observability/data_agent_timing.jsonl`（观测日志）

性能要求：
- 读取 timing 日志最近一条；
- 当 `TOTAL > 30000ms` 时，输出最慢 2-3 个环节与原因说明。

观测日志说明：
- `call_trace.jsonl`：外层流程调用链（agent 启动、排队、环境探测等系统开销）。
- `data_agent_timing.jsonl`：Data Agent 内部各子步骤耗时。
- 当外层总耗时远大于内层 timing 之和时，默认先归因为 agent 启动与环境探测开销，不误判为正文或数据处理慢。

债务利息：
- 默认关闭，仅在用户明确要求或开启追踪时执行（见 `references/step-5-data-writeback/module-spec.md`）。

### Step 6：Git 备份（可失败但需说明）

```bash
git add .
git -c i18n.commitEncoding=UTF-8 commit -m "第{chapter_num}章: {title}"
```

规则：
- 提交时机：验证、回写、清理全部完成后最后执行。
- 提交信息默认中文，格式：`第{chapter_num}章: {title}`。
- 若 commit 失败，必须给出失败原因与未提交文件范围。

## 充分性闸门（必须通过）

未满足以下条件前，不得结束流程：

1. 章节正文文件存在且非空：`正文/第{chapter_padded}章-{title_safe}.md` 或 `正文/第{chapter_padded}章.md`
2. Step 3 已产出 `overall_score` 且 `review_metrics` 成功落库
3. Step 4 已处理全部 `critical`，`high` 未修项有 deviation 记录
4. Step 4 的 `anti_ai_force_check=pass`（基于全文检查；fail 时不得进入 Step 5）
5. Step 5 已回写 `state.json`、`index.db`、`summaries/ch{chapter_padded}.md`
6. 若开启性能观测，已读取最新 timing 记录并输出结论

## 验证与交付

执行检查：

```bash
test -f "${PROJECT_ROOT}/.webnovel/state.json"
chapter_file="$(find "${PROJECT_ROOT}/正文" -type f \( -name "第${chapter_padded}章.md" -o -name "第${chapter_padded}章-*.md" \) | head -n 1)"
test -n "${chapter_file}"
test -f "${PROJECT_ROOT}/.webnovel/summaries/ch${chapter_padded}.md"
python -X utf8 "${SCRIPTS_DIR}/story.py" --project-root "${PROJECT_ROOT}" index get-recent-review-metrics --limit 1
tail -n 1 "${PROJECT_ROOT}/.webnovel/observability/data_agent_timing.jsonl" || true
```

成功标准：
- 章节文件、摘要文件、状态文件齐全且内容可读。
- 审查分数可追溯，`overall_score` 与 Step 5 输入一致。
- 润色后未破坏全息地图章节节点与设定约束。

## 失败处理（最小回滚）

触发条件：
- 章节文件缺失或空文件；
- 审查结果未落库；
- Data Agent 关键产物缺失；
- 润色引入设定冲突。

恢复流程：
1. 仅重跑失败步骤，不回滚已通过步骤。
2. 常见最小修复：
   - 审查缺失：只重跑 Step 3 并落库；
   - 润色失真：恢复 Step 2A 输出并重做 Step 4；
   - 摘要/状态缺失：只重跑 Step 5；
3. 重新执行“验证与交付”全部检查，通过后结束。

## Root-Cause 执行合同

- 分层上溯路径固定为：
  - `症状/失败 -> 直接技术原因 -> Rule Source(3-Drafting/SKILL.md、step module、appendix、脚本入口) -> Meta Rule Source(仓库 AGENTS.md / 相关 meta skill) -> Fix Landing Points`
- 进入根因修复时，优先顺序固定为：
  - step 边界与路由
  - 上游上下文压缩合同
  - craft 症状到 leaf-note 的映射
  - polish / writeback gate
  - 最后才是单章正文局部返工
- 若问题来自共享引用漂移，必须同步检查：
  - `3-Drafting` 主 `SKILL.md`
  - 当前命中的 `references/<module>/module-spec.md`
  - 相关 appendix / leaf note
  - 与之共用的 shared references / system-data-flow
- 本技能收尾输出必须包含：
  - `根因位置 + 立即修复 + 系统预防修复`

## Lite Tier Field Mapping（Combined）

| field_id | step_id | intent | required_output | fail_code | rework_entry |
|---|---|---|---|---|---|
| FIELD-DRF-ROOT-01 | Step 0 | 解析真实项目根并完成 preflight / TEAM 治理判定 | `PROJECT_ROOT`、`planning_source`、监制团队结论 | FAIL-DRF-ROOT-01 | 回到 Step 0，修正 project root、规划源或 TEAM 漂移 |
| FIELD-DRF-CTX-02 | Step 1 | 把上游真源压成单一章节执行包 | Layer A-E、任务书、Context Contract、直写提示词 | FAIL-DRF-CTX-02 | 回到 Step 1，重做真源压缩与差异化路由 |
| FIELD-DRF-DRAFT-03 | Step 2A-2B | 生成可审正文，并在需要时完成不越权的表达转译 | 正文草稿 / 风格化正文、改写边界记录 | FAIL-DRF-DRAFT-03 | 回到 Step 2A/2B，先锁事实边界再重写表达 |
| FIELD-DRF-REVIEW-04 | Step 3 | 通过隔离审查团队生成问题包与 `overall_score` | 审查结果、问题分级、review gate | FAIL-DRF-REVIEW-04 | 回到 Step 3，重建隔离审查并重做聚合 |
| FIELD-DRF-POLISH-05 | Step 4 | 修复 critical/high 问题并完成症状优先的 Anti-AI / No-Poison 终检 | 润色后正文、deviation、`anti_ai_force_check` | FAIL-DRF-POLISH-05 | 回到 Step 4，先修问题包，再处理模板症状 |
| FIELD-DRF-WRITEBACK-06 | Step 5-6 | 完成 state/index/summary 回写与最终交付收口 | `state.json`、`index.db`、summary、观测结论、可选 git 备份 | FAIL-DRF-WRITEBACK-06 | 回到 Step 5/6，局部补跑写回或备份 |
