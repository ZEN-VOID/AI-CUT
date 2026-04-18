---
name: story-plan
governance_tier: full
description: |
  Use when story2026 needs whole-book planning passes, holomap rebuild, planning sequence repair, or source-layer fixes that must converge into `Planning/8-全息地图.json`.
tools: [Read, Write, Edit, Grep, Bash]
color: indigo
---

# 2-Planning

## Context Loading Contract

- 每次调用本技能时，必须同时加载同目录 `CONTEXT.md`。
- 根级 `CONTEXT.md` 只沉淀 planning 返工模式、模块触发经验与 holomap 收束启发，不得覆盖本 `SKILL.md` 的串行 step 合同。
- 模块级 `CONTEXT.md` 仅在命中局部异常时补充经验，不得替代 `module-spec.md`。

## 1. 功能描述

`2-Planning` 现在是 `story2026` 的单一 planning skill，不再是“父层 + 8 个子技能包”的目录总线。

它统一承担四件事：

1. 把 `0-Init` 的立项合同与 `1-Cards` 的对象真源，推进为 7 份可追溯的规划证据文件。
2. 通过 `references/` 模块按需加载每一类 planning pass 的执行细则，而不是分散到 8 个独立 skill。
3. 把 7 份并列 planning 文件再收束为唯一规划真源 `Planning/8-全息地图.json`。
4. 为 `3-Drafting / query / resume / loopback` 提供 holomap-first 的统一读取入口。

一句话裁决：

- `1-Cards` 负责对象真源。
- `2-Planning` 负责编排真源。
- `references/*/module-spec.md` 只提供模块细则；局部经验沉淀在同目录 `CONTEXT.md`，不再拥有独立 skill 身份。
- `Planning/8-全息地图.json` 是唯一默认规划入口。

## 2. 专业领域

| 层级 | 领域 |
| --- | --- |
| Primary | Long-form narrative planning, multi-pass orchestration, canonical holomap design |
| Secondary | Genre corridor design, chapter architecture, outline engineering, conflict/mission/clue/foreshadow systems |
| Standards | Codex CLI, repo-level `AGENTS.md` source governance, story2026 canonical truth contracts |

## 3. 风格语气

- 语气必须是系统架构式，而不是“写一篇更长的大纲”。
- 先解释规划真源的边界，再展开每个 planning module 的职责。
- 每个模块都要能回答“为什么由它裁决，而不是提前被上一层偷做”。
- 对 long-form 项目优先强调编排与收束，不迷恋一次性写满所有剧情细节。

## 4. 任务规则

### 核心任务

1. 识别当前任务是 `full-build / localized-rework / sequence-repair / holomap-rebuild / source-contract-fix` 的哪一种。
2. 固定先读取 `Init/north_star_contract.json + Init/初始化简报.json + Cards/**/*.json + TEAM.toml`，不从零散草稿倒推 planning。
3. 先判定 `TEAM.toml["策划"]` 是否已指派 AGENTS；若已激活，则本轮必须进入“策划专家组并行会诊 + 主流程串行收束”模式。
4. 读取 [`references/README.md`](/Volumes/AIGC/AIGC-DREAMER/.agents/skills/story/2-Planning/references/README.md)，按顺序选择本轮需要加载的 `module-spec.md`，并在局部异常时按需补读对应模块 `CONTEXT.md`。
5. 按固定顺序执行 8 个 planning step；允许局部返工，但不得跳过上游依赖。
6. 每个 module 都必须动态读取根级 `templates/*.json`，正式落盘为 `Planning/*.json` 并列文件。
7. 第 8 步必须把前 1-7 的裁决收束为唯一规划真源 `Planning/8-全息地图.json`。
8. 若发现多处漂移，优先回滚到“最早失稳模块”，而不是分别修 3 份下游文件。

### 单技能治理规则

- `references/genre-selection/module-spec.md`
  - 是题材选型模块，不是独立 skill。
- `references/chapter-planning/module-spec.md`
  - 是章节规划模块，不是独立 skill。
- `references/story-outline/module-spec.md`
  - 是故事大纲模块，不是独立 skill。
- `references/conflict-design/module-spec.md`
  - 是冲突设计模块，不是独立 skill。
- `references/mission-design/module-spec.md`
  - 是任务设计模块，不是独立 skill。
- `references/clue-design/module-spec.md`
  - 是线索设计模块，不是独立 skill。
- `references/foreshadow-design/module-spec.md`
  - 是伏笔设计模块，不是独立 skill。
- `references/holomap/module-spec.md`
  - 是全息地图收束模块，不是独立 skill。
- 任何执行者若仍试图把上述模块当成独立 skill id 调度，视为 routing contract 失效，必须先修 `2-Planning/SKILL.md` 与相关入口。

## 5. 核心约束

### 工匠级约束（本仓库治理合同）

沿用仓库 `AGENTS.md` 中关于“成熟版 engine / 根因优先 / 真源治理 / 复合输出治理”的约束，不再依赖外部缺失的元技能文档。对本技能的具体化如下：

- 禁止把 2-Planning 退化为“8 篇散装说明文”。
- 禁止把模块细则重新拆回复数 skill 身份。
- 禁止让后序 module 偷偷重写前序裁决，只因它“看起来更会说话”。
- 禁止把 `holomap` 写成摘要总览；它必须是可导航、可回查、可 actualize 的真源。

### Root-Cause 执行契约

继承 `AGENTS.md § Root-Cause First`，并在本技能中固定为：

1. 先查主技能路由、module 触发、模板路径、planning 文件路径，再改产物内容。
2. 若多个 planning 文件同时失真，先锁定最早失稳模块，从那里串行回修。
3. 若 holomap 失真，优先检查：
   - `2-Planning/SKILL.md`
   - `references/holomap/module-spec.md`
   - 前 1-7 号 planning 文件
4. 收尾必须返回：`根因位置 + 立即修复 + 系统预防修复`。

### TEAM 阶段治理（Mandatory）

- 执行 `2-Planning` 前，必须读取项目根 `TEAM.toml`，并把 `["策划"]` 视为本阶段的唯一团队治理入口。
- 若满足以下任一条件，即视为策划专家组已激活：
  - `TEAM.toml["策划"].智能顾问团 = true`
  - `TEAM.toml["策划"].成员` 非空
- 专家组已激活时：
  - 不得只由主流程单点裁决 8 个 planning steps。
  - 必须创建后台多 subagents，对题材走廊、章节容器、故事脊柱、冲突/任务/线索/伏笔系统与 holomap 收束进行并行会诊。
  - 主流程必须把专家组决议收束为正式 `Planning/*.json` 写回；专家组结论不是聊天旁白，而是本轮规划落盘依据。
- `TEAM.toml["策划"].管辖` 是 stage-route sanity check；若未覆盖 `2-Planning`，必须报告团队治理配置漂移。
- 若 `TEAM.toml["策划"]` 未激活，则维持当前默认单主流程模式，但仍要在执行说明中明确“本轮无策划专家组介入”。

### 自评偏差声明

- LLM 容易把“文件很多”误判为“规划系统成立”；本技能必须优先验证单一真源与模块边界。
- LLM 容易让后序模块代替前序模块思考；本技能必须检查每份文件是否只裁决本层职责。
- LLM 容易把 holomap 写成总结页；本技能必须优先检查 chapter board 编组、三轴组织和跨线程索引。

### Planning Artifact Contract（Mandatory）

所有 planning 正式产物统一落在 `PROJECT_ROOT/Planning/` 下的并列文件：

- `Planning/1-题材选型.json`
- `Planning/2-章节规划.json`
- `Planning/3-故事大纲.json`
- `Planning/4-冲突设计.json`
- `Planning/5-任务设计.json`
- `Planning/6-线索设计.json`
- `Planning/7-伏笔设计.json`
- `Planning/8-全息地图.json`

执行原则：

- 1-7 是必须保留的 evidence layer，不再埋在各自目录下。
- 8 是唯一 canonical truth。
- 旧目录式路径仅作为 legacy read fallback，不再是 canonical write target。

### Shared Axes & Double-Time Contract（Mandatory）

- 规划层统一维护：
  - `timeline_axis`
  - `space_axis`
  - `episode_sequence_axis`
- 规划层统一生命周期词表：
  - `出现 / 激活 / 转移 / 解决 / 兑现 / 退场`
- `MAP` 负责“事件叙事中心”的规划时间。
- `1-Cards` 负责“角色经历中心”的成长时间。
- 两者可互相挂接，但不得互相复制。

## 6. 任务流程

1. 判断模式：
   - `full-build`
   - `localized-rework`
   - `sequence-repair`
   - `holomap-rebuild`
   - `source-contract-fix`
2. 读取上游真源：
   - `Init/north_star_contract.json`
   - `Init/初始化简报.json`
   - 既有 `Cards/**/*.json`
   - `TEAM.toml`
   - 既有 `Planning/*.json`（若存在）
3. 判定 `TEAM.toml["策划"]` 是否激活；若激活，先创建后台策划专家组，并形成本轮 planning 决策简报。
4. 读取 [`references/README.md`](/Volumes/AIGC/AIGC-DREAMER/.agents/skills/story/2-Planning/references/README.md)，确定本轮 `module-spec`、局部 `CONTEXT` 与模板。
5. 固定执行顺序：
   - Step 1 `genre-selection`
   - Step 2 `chapter-planning`
   - Step 3 `story-outline`
   - Step 4 `conflict-design`
   - Step 5 `mission-design`
   - Step 6 `clue-design`
   - Step 7 `foreshadow-design`
   - Step 8 `holomap`
6. 按需加载对应 reference，并动态读取对应模板：
   - `templates/genre-selection.json`
   - `templates/chapter-planning.json`
   - `templates/story-outline.json`
   - `templates/conflict-design.json`
   - `templates/mission-design.json`
   - `templates/clue-design.json`
   - `templates/foreshadow-design.json`
   - `templates/holomap.json`
7. 每步正式落盘到并列文件：
   - `Planning/1-题材选型.json`
   - `Planning/2-章节规划.json`
   - `Planning/3-故事大纲.json`
   - `Planning/4-冲突设计.json`
   - `Planning/5-任务设计.json`
   - `Planning/6-线索设计.json`
   - `Planning/7-伏笔设计.json`
   - `Planning/8-全息地图.json`
8. 若本轮是局部返工：
   - 允许从最早失稳模块重新起链。
   - 禁止只修第 8 步而不回查其证据文件。
9. 第 8 步收尾后，必须确认：
   - holomap 已成为默认消费入口
   - 1-7 能作为追溯证据
   - legacy 路径只保留兼容读取，不再继续写入

## SKILL vs CONTEXT Placement Matrix

- 放在 `SKILL.md`
  - 单技能治理规则、module 路由、并列文件落盘契约、holomap 真源合同、模板清单、质量门禁。
- 放在 `CONTEXT.md`
  - 模块失稳信号、回滚顺序、跨模块漂移案例、holomap-first 经验、可复用 heuristic。
- 放在 `references/*/module-spec.md + CONTEXT.md`
  - `module-spec.md`：各 planning module 的专业细则、触发信号、设计焦点、常见误区与 handoff 钩子。
  - `CONTEXT.md`：各 planning module 的局部故障模式、返工顺序与可复用 heuristics。

## 7. 多线程并发模式

- 默认模式：串行。
  - 原因：8 个 planning steps 存在明确上游依赖。
- 允许并发：
  - 单一 module 内的候选比较、局部方案探索、同层替代解对照。
  - 当 `TEAM.toml["策划"]` 已激活时，允许后台策划 subagents 在单 step 内并行会诊，但正式 planning 文件仍必须按 Step 1-8 串行落盘。
- 禁止并发：
  - 同时落盘两个不同 step 的正式版本。
  - 在 `2-章节规划` 未稳定前并行推进 `故事大纲` 与 `全息地图`。
  - 在未确认最早失稳模块前，对多个下游文件各自打补丁。

## 8. 输入来源

### 必需输入

- `Init/north_star_contract.json`
- `Init/初始化简报.json`
- `Cards/2-角色卡/**/*.json`
- `Cards/3-场景卡/**/*.json`
- `Cards/4-物品卡/**/*.json`
- `TEAM.toml`

### 可选输入

- `.webnovel/state.json`
- `.webnovel/idea_bank.json`
- `Planning/*.json` 中既有稳定规划文件
- `Planning/legacy/总纲.md`
  - 仅作兼容回退，不是规划真源

### 禁止输入

- 把后序 planning 产物反向当作前序裁决依据
- 把旧子技能目录继续当作技能入口
- 在 `Planning/` 正式真源之外，再维护一套平行 Markdown 规划真源

## 9. References 模块与触发细则

### 固定入口

- 常驻加载：
  - [`references/README.md`](/Volumes/AIGC/AIGC-DREAMER/.agents/skills/story/2-Planning/references/README.md)

### 条件加载矩阵

| reference | 触发信号 | 解决问题 | 模板 | 正式输出 |
| --- | --- | --- | --- | --- |
| [`references/genre-selection/module-spec.md`](/Volumes/AIGC/AIGC-DREAMER/.agents/skills/story/2-Planning/references/genre-selection/module-spec.md) | 立题、题材、走廊、平台承诺、禁飞区 | 锁题材走廊与下游题材钩子 | `templates/genre-selection.json` | `Planning/1-题材选型.json` |
| [`references/chapter-planning/module-spec.md`](/Volumes/AIGC/AIGC-DREAMER/.agents/skills/story/2-Planning/references/chapter-planning/module-spec.md) | 体量、卷篇、节奏窗口、功能槽、密度合同 | 锁章节容器与元素密度 | `templates/chapter-planning.json` | `Planning/2-章节规划.json` |
| [`references/story-outline/module-spec.md`](/Volumes/AIGC/AIGC-DREAMER/.agents/skills/story/2-Planning/references/story-outline/module-spec.md) | 主干、转折、卷级推进、宏观节奏 | 锁叙事脊柱与推进波形 | `templates/story-outline.json` | `Planning/3-故事大纲.json` |
| [`references/conflict-design/module-spec.md`](/Volumes/AIGC/AIGC-DREAMER/.agents/skills/story/2-Planning/references/conflict-design/module-spec.md) | 对抗、升级链、归属、解决窗口 | 锁冲突系统与升级梯度 | `templates/conflict-design.json` | `Planning/4-冲突设计.json` |
| [`references/mission-design/module-spec.md`](/Volumes/AIGC/AIGC-DREAMER/.agents/skills/story/2-Planning/references/mission-design/module-spec.md) | 目标链、主线、支线、隐藏任务、收益代价 | 锁任务系统与门槛 | `templates/mission-design.json` | `Planning/5-任务设计.json` |
| [`references/clue-design/module-spec.md`](/Volumes/AIGC/AIGC-DREAMER/.agents/skills/story/2-Planning/references/clue-design/module-spec.md) | 线索网、发现路径、误导、揭晓 | 锁证据链与公平误导 | `templates/clue-design.json` | `Planning/6-线索设计.json` |
| [`references/foreshadow-design/module-spec.md`](/Volumes/AIGC/AIGC-DREAMER/.agents/skills/story/2-Planning/references/foreshadow-design/module-spec.md) | 伏笔、静默区、强化、兑现窗口 | 锁长期回照系统 | `templates/foreshadow-design.json` | `Planning/7-伏笔设计.json` |
| [`references/holomap/module-spec.md`](/Volumes/AIGC/AIGC-DREAMER/.agents/skills/story/2-Planning/references/holomap/module-spec.md) | 收束、三轴、章节编组、跨线程索引、actualization | 把 1-7 收束为 holomap 真源 | `templates/holomap.json` | `Planning/8-全息地图.json` |

### 触发细则

1. 先由主 `SKILL.md` 判定当前位于哪个 planning step。
2. 再加载对应 `module-spec.md`；不允许跳过主技能直接读 module 执行。
3. 局部返工时：
   - 若题材漂移，回到 `genre-selection/module-spec`
   - 若挂章失败，回到 `chapter-planning/module-spec`
   - 若长线断裂，先看 `story-outline / conflict / mission / clue / foreshadow`
   - 若 holomap 只剩摘要，回到 `holomap/module-spec`
4. 任一 module 若无法解释当前任务，必须返回主 `2-Planning/SKILL.md` 重做路由，不允许硬套。

## 10. 变量场景识别与策略映射（VSM）

**本技能 VSM 复杂度**: 复杂  
**判定依据**: 同时存在任务模式、规划尺度、对象密度、长线复杂度、模块稳定性、holomap 收束压力六类变量，并且它们会跨 8 个 step 联动。

### 10.1 变量登记表

| var_id | 变量层级 | 观测信号 | 状态集合 | 检测方法 | 优先级 |
| --- | --- | --- | --- | --- | --- |
| VAR-PL-01 | 结构 | 当前任务模式 | full-build / localized / sequence-repair / holomap-only / contract-fix | 看用户诉求与已有文件 | 高 |
| VAR-PL-02 | 叙事 | 项目体量与密度压力 | 短 / 中 / 长 | 读 `.webnovel/state.json` 与 `cards` 规模 | 高 |
| VAR-PL-03 | 结构 | 上游稳定度 | stable / partial / conflicted | 读取 `Planning/*.json` 与 Cards | 高 |
| VAR-PL-04 | 信息 | 长线负荷 | 低 / 中 / 高 | 看冲突/任务/线索/伏笔数量 | 中 |
| VAR-PL-05 | 收束 | holomap 编组压力 | 低 / 中 / 高 | 看 chapter_boards 需要承载的线程数 | 高 |
| VAR-PL-06 | 兼容 | 是否存在 legacy 项目路径 | yes / no | 检查旧目录式文件 | 中 |

### 10.2 情况判定表

| case_id | 触发谓词 | 置信度阈值 | 互斥关系 | 可并发关系 |
| --- | --- | --- | --- | --- |
| CASE-PL-01 | `VAR-PL-01=full-build` 且 `VAR-PL-03=stable|partial` | 0.90 | 与 CASE-PL-02 互斥 | 可与 CASE-PL-04/05 并发 |
| CASE-PL-02 | `VAR-PL-01=localized` 且 `VAR-PL-03=stable` | 0.80 | 与 CASE-PL-01 互斥 | 可与 CASE-PL-03/04 并发 |
| CASE-PL-03 | `VAR-PL-03=conflicted` | 0.85 | 无 | 可与 CASE-PL-04/05 并发 |
| CASE-PL-04 | `VAR-PL-05=高` 或 `VAR-PL-04=高` | 0.75 | 无 | 可与所有 case 并发 |
| CASE-PL-05 | `VAR-PL-06=yes` | 0.70 | 无 | 可与所有 case 并发 |

### 10.3 策略映射矩阵

| case_id | strategy_id | 执行步骤 | 质量门禁 | fallback_strategy_id | 升级条件 |
| --- | --- | --- | --- | --- | --- |
| CASE-PL-01 | STR-PL-01 | 串行跑完 1-8，逐步落盘并列文件 | 8 份文件齐备且 holomap 可消费 | STR-PL-03 | 任一步缺正式产物 |
| CASE-PL-02 | STR-PL-02 | 仅从最早失稳模块重新起链 | 后序文件不得假装仍然有效 | STR-PL-03 | 局部返工仍出现跨模块失真 |
| CASE-PL-03 | STR-PL-03 | 暂停下游补丁，先修最早冲突文件与主技能合同 | 冲突点必须被显式定位 | 无 | 仍无法定位最早失稳点 |
| CASE-PL-04 | STR-PL-04 | 强化 chapter slot、cross-thread index 与 lifecycle 约束 | holomap 不能退化成摘要 | STR-PL-03 | 编组仍然发虚 |
| CASE-PL-05 | STR-PL-05 | 采用 canonical 写入 + legacy 读取兼容 | 不再继续写旧路径 | STR-PL-03 | 运行态仍硬编码旧路径 |

### 10.4 路由与回退卡

- 判定顺序：
  - 先判任务模式，再判上游稳定度，再判 holomap 压力与 legacy 兼容。
- 冲突解消规则：
  - 最早失稳模块优先于最显眼失败模块。
  - holomap 真源优先于任何派生大纲视图。
- unknown 默认路由：
  - 降级为“定位最早失稳模块 + 暂停继续落盘”。
- 失败重试上限：
  - 2 次。
- 停止条件：
  - 若无法判断最早失稳模块，禁止假装完成第 8 步。

## 11. 附加上下文加载

- 默认加载：
  - [`CONTEXT.md`](/Volumes/AIGC/AIGC-DREAMER/.agents/skills/story/2-Planning/CONTEXT.md)
- 条件加载：
  - 对应 planning module 的 `references/*/module-spec.md`
  - 仅在局部异常或返工时补读该模块的 `references/*/CONTEXT.md`
- 动态读取：
  - 对应 `templates/*.json`

上下文优先级固定为：

1. 用户显式请求
2. `AGENTS.md` / meta-SKILL
3. `2-Planning/SKILL.md`
4. `2-Planning/CONTEXT.md`
5. `references/*/module-spec.md`
6. `references/*/CONTEXT.md`

## 12. 输出内容模板

### 输出模式

- 默认：JSON-first
- 最终产物不是 1 个文件，而是 8 个 JSON artifact 的单链路收束系统。

### Canonical Artifact Ledger

| step | module_id | 模板 | 正式写入 |
| --- | --- | --- | --- |
| 1 | `genre-selection` | `templates/genre-selection.json` | `Planning/1-题材选型.json` |
| 2 | `chapter-planning` | `templates/chapter-planning.json` | `Planning/2-章节规划.json` |
| 3 | `story-outline` | `templates/story-outline.json` | `Planning/3-故事大纲.json` |
| 4 | `conflict-design` | `templates/conflict-design.json` | `Planning/4-冲突设计.json` |
| 5 | `mission-design` | `templates/mission-design.json` | `Planning/5-任务设计.json` |
| 6 | `clue-design` | `templates/clue-design.json` | `Planning/6-线索设计.json` |
| 7 | `foreshadow-design` | `templates/foreshadow-design.json` | `Planning/7-伏笔设计.json` |
| 8 | `holomap` | `templates/holomap.json` | `Planning/8-全息地图.json` |

### 构成主义类型分布

| type_prefix | 字段数 | 占比 | 代表字段 |
| --- | --- | --- | --- |
| IDN | 1 | 11% | FIELD-PL-IDN-01 |
| STR | 3 | 33% | FIELD-PL-STR-01, FIELD-PL-STR-02, FIELD-PL-STR-03 |
| MAT | 2 | 22% | FIELD-PL-MAT-01, FIELD-PL-MAT-02 |
| BHV | 1 | 11% | FIELD-PL-BHV-01 |
| CTX | 2 | 22% | FIELD-PL-CTX-01, FIELD-PL-CTX-02 |
| CST | 1 | 11% | FIELD-PL-CST-01 |

### 统一字段主表（Mandatory）

| field_id | 类型(type) | JSON路径 | 输出位置/字段 | 内容要求 | 证据来源 | 默认责任Step | 质量维度 | 失败码 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| FIELD-PL-IDN-01 | IDN | `Planning/8-全息地图.json :: meta.skill_id` | `meta.skill_id` | 单一 skill 身份固定为 `story-plan` | 主技能合同 | S1 | 结构正确性 | FAIL-PL-IDN-01 |
| FIELD-PL-STR-01 | STR | `Planning/1-题材选型.json :: content.genre_selection` | `1-题材选型.json` | 题材走廊、承诺、禁飞区与下游 hooks | Init + Cards | S1 | 路由清晰度 | FAIL-PL-STR-01 |
| FIELD-PL-STR-02 | STR | `Planning/2-章节规划.json :: content.chapter_planning` | `2-章节规划.json` | 章节容器、密度合同、功能槽和节奏窗口 | Step 1 + Cards | S2 | 容器稳定性 | FAIL-PL-STR-02 |
| FIELD-PL-STR-03 | STR | `Planning/8-全息地图.json :: content.holomap.timeline_axis/space_axis/episode_sequence_axis` | `8-全息地图.json` | 三轴组织与卷章板块 | Steps 1-7 | S8 | 真源收束力 | FAIL-PL-STR-03 |
| FIELD-PL-MAT-01 | MAT | `Planning/3-故事大纲.json :: content.story_outline` | `3-故事大纲.json` | 叙事脊柱、卷级推进、关键转折 | Steps 1-2 | S3 | 主干清晰度 | FAIL-PL-MAT-01 |
| FIELD-PL-MAT-02 | MAT | `Planning/4-7*.json :: core planning payloads` | `4-冲突/5-任务/6-线索/7-伏笔` | 对抗链、目标链、证据链、回照链 | Steps 1-3 + Cards | S4-S7 | 长线完整度 | FAIL-PL-MAT-02 |
| FIELD-PL-BHV-01 | BHV | `Planning/8-全息地图.json :: content.holomap.lifecycle_lexicon/state_transitions` | `holomap lifecycle` | 六态词表、状态流与 actualization 兼容容器 | 主技能合同 + Steps 4-7 | S8 | 生命周期一致性 | FAIL-PL-BHV-01 |
| FIELD-PL-CTX-01 | CTX | `Planning/8-全息地图.json :: content.holomap.cross_thread_indexes` | `cross_thread_indexes` | 长线跨章索引与反查入口 | Steps 4-7 | S8 | 下游可消费性 | FAIL-PL-CTX-01 |
| FIELD-PL-CTX-02 | CTX | `Planning/*.json :: meta.module_id/source_route` | `meta` | module 归属、template 版本、source route 清晰 | 模板 + 主技能合同 | S1-S8 | 模块自治度 | FAIL-PL-CTX-02 |
| FIELD-PL-CST-01 | CST | `Planning/8-全息地图.json :: gate_summary.status` | `gate_summary` | PASS/FAIL、失败码、返工入口与兼容说明 | 全链路自检 | S8 | 契约遵循 | FAIL-PL-CST-01 |

## 13. 超级思维链规范

### 13.1 执行目标

- 让 2-Planning 成为“单技能治理 + 模块细则加载 + 并列文件落盘 + holomap 收束”的稳定系统。
- 让 1-7 不再是互相漂移的子技能，而是被同一主合同约束的证据层。
- 让 holomap 成为唯一默认入口，而不是“八份文件里最大的一份”。

### 13.2 三向三重自省流（Mandatory）

| 轴角色 | 当前技能轴名 | 核心问题 | 主导裁决层 | 说明 |
| --- | --- | --- | --- | --- |
| `方向轴` | 叙事 | 当前 step 应该裁决哪一层规划，而不替代谁？ | 粗裁决 | 先锁模块边界与顺序 |
| `成立轴` | 合理 | 当前 planning 文件是否建立在稳定上游之上？ | 细裁决 | 过滤掉越级裁决与无依据落盘 |
| `优选轴` | 编排审美 | 哪种组织方式最利于整书消费、追溯和写作？ | 离散裁决 | 在成立解中优选文件结构与 holomap 形态 |
| `硬门禁轴（可选）` | 真源性 | 下游能否默认只读 holomap 而不丢关键信息？ | 全层 veto | 不行则否决 |

- 第一层：粗裁决 / Base Range
  - 先锁模块顺序、模块边界与 artifact ledger，服务 `FIELD-PL-STR-01/02`。
- 第二层：细裁决 / Range Narrowing
  - 再验证每一步是否建立在前序稳定裁决之上，服务 `FIELD-PL-MAT-01/02`。
- 第三层：离散裁决 / Final Selection
  - 最后决定三轴组织、生命周期与 holomap 导航结构，服务 `FIELD-PL-STR-03`、`FIELD-PL-BHV-01`、`FIELD-PL-CTX-01`。

层内自问反思（Mandatory）：

- `为什么是这个结果？`
  - `方向轴判断（叙事）：当前 step 是否只解决本层该解决的问题？`
  - `成立轴判断（合理）：它是否真的继承了稳定上游？`
  - `优选轴判断（编排审美）：它是否比替代组织更便于长期消费？`
  - `硬门禁轴判断（真源性）：下游是否可默认只读 holomap？`
- `如果不是这个结果，会不会有更好的答案？`
  - 必须比较被排除方案为什么更易漂移、越级或失去可导航性。

字段落盘门禁（Mandatory）：

- 每层都必须回答：
  - 当前服务哪些 `field_id`
  - 当前收窄了什么候选空间
  - 下一层还能处理哪些候选
- 最终层必须明确：
  - `Planning/8-全息地图.json`
  - 为什么它是唯一真源
  - 为什么 1-7 只能作为证据层而不是并列入口

### 13.3 标准链路

| step_id | 聚焦字段(field_id) | 核心问题 | 生成动作 | 未达标信号 |
| --- | --- | --- | --- | --- |
| S1 | FIELD-PL-STR-01, FIELD-PL-CTX-02 | 题材走廊是否成立？ | 读 `genre-selection` module，写 `1-题材选型.json` | 仍像标签堆叠 |
| S2 | FIELD-PL-STR-02 | 章节容器和密度合同是否稳定？ | 读 `chapter-planning` module，写 `2-章节规划.json` | 后续无稳定挂点 |
| S3 | FIELD-PL-MAT-01 | 故事主干是否清楚？ | 读 `story-outline` module，写 `3-故事大纲.json` | 主干与题材脱节 |
| S4 | FIELD-PL-MAT-02 | 冲突链是否明确？ | 读 `conflict-design` module，写 `4-冲突设计.json` | 对抗关系发虚 |
| S5 | FIELD-PL-MAT-02 | 任务链是否明确？ | 读 `mission-design` module，写 `5-任务设计.json` | 推进只靠被动挨打 |
| S6 | FIELD-PL-MAT-02 | 线索链是否明确？ | 读 `clue-design` module，写 `6-线索设计.json` | 没有证据链 |
| S7 | FIELD-PL-MAT-02 | 伏笔链是否明确？ | 读 `foreshadow-design` module，写 `7-伏笔设计.json` | 只有提醒没有回照 |
| S8 | FIELD-PL-STR-03, FIELD-PL-BHV-01, FIELD-PL-CTX-01, FIELD-PL-CST-01 | holomap 是否成为唯一真源？ | 读 `holomap` module，写 `8-全息地图.json` | 仍像摘要或无法导航 |

### 13.4 弹性裁剪（8-15 步）

- 基线采用 8 步，因为 8 个 module 本身就是强依赖主链。
- 若某一步内部复杂，可在该 module 内扩展候选探索步，但不得新增并行主 module。
- 若局部返工，只允许从最早失稳步起链，不允许跳过中间依赖。

### 13.5 禁止模式

- 保留“8 个子技能包”旧结构，却仅在父层文字上宣称已经单技能化。
- 继续把规划文件写进 `Planning/<子目录>/...json`，导致目录结构与 skill 架构继续耦合。
- 让 `全息地图` 成为摘要页，却仍要求下游默认只读它。
- 让后序 planning 文件比前序更像裁决真源，导致边界失守。

## 14. 质量评估与闭环验证

| 维度 | 评估项 | 关联步骤 | 得分 |
| --- | --- | --- | --- |
| 0 | Covenant Compliance（契约遵循）：是否真正完成单技能治理、module 触发与 holomap 单真源收束 | All | __/10 |
| 1 | Routing Clarity：主技能与 references 的边界是否清楚 | S1-S8 | __/10 |
| 2 | File Truth Contract：并列 planning 文件是否稳定落盘且职责清晰 | S1-S7 | __/10 |
| 3 | Sequence Integrity：是否严格遵守 1-8 顺序与最早失稳回滚原则 | S1-S8 | __/10 |
| 4 | Holomap Convergence：holomap 是否真正收束了 1-7 | S8 | __/10 |
| 5 | Downstream Utility：drafting/query/resume/loopback 是否能默认消费新真源 | S8 | __/10 |

### 思维链-质量评估回环映射

| field_id | 质量维度 | 通过标准 | 失败码 | 返工入口 |
| --- | --- | --- | --- | --- |
| FIELD-PL-STR-01 | Routing Clarity | 题材模块只裁题材，不偷做章节/剧情 | FAIL-PL-STR-01 | 回到 S1 |
| FIELD-PL-STR-02 | File Truth Contract | 章节规划能稳定承接 3-8 号模块 | FAIL-PL-STR-02 | 回到 S2 |
| FIELD-PL-MAT-01 | Sequence Integrity | 故事主干建立在 1-2 之上 | FAIL-PL-MAT-01 | 回到 S3 |
| FIELD-PL-MAT-02 | Sequence Integrity | 4-7 的四条长线均有明确职责与输入来源 | FAIL-PL-MAT-02 | 回到 S4-S7 最早失稳模块 |
| FIELD-PL-STR-03 | Holomap Convergence | holomap 可默认消费且可三轴导航 | FAIL-PL-STR-03 | 回到 S8 |
| FIELD-PL-BHV-01 | Holomap Convergence | lifecycle 与 actualization 合同成立 | FAIL-PL-BHV-01 | 回到 S8 |
| FIELD-PL-CTX-01 | Downstream Utility | query/write/resume 可用 holomap-first | FAIL-PL-CTX-01 | 回到 S8 + 下游合同 |
| FIELD-PL-CST-01 | Covenant Compliance | 维度 0 ≥ 8 且总分达标 | FAIL-PL-CST-01 | 回到最早失稳模块 |

### 验收机制

- 满分：60
- 维度 0 低于 8：`FAIL-COVENANT`
- 总分低于 49：`FAIL-QUALITY`
- 通过标准：
  - 8 份规划文件存在
  - 默认真源为 `Planning/8-全息地图.json`
  - legacy 路径仅保留读取兼容

## 15. Root-Cause 闭环契约

- 若问题涉及 module 路由错误，先修 `2-Planning/SKILL.md` 与 `references/README.md`。
- 若问题涉及落盘路径错误，先修模板、路径 helper 与下游消费合同。
- 若问题涉及 holomap 失真，先追溯最早失稳 planning 文件，再修 `references/holomap/module-spec.md`。
- 完成闭环时必须同时给出：
  - 根因位置
  - 立即修复
  - 系统预防修复
  - 分层 trace path（`symptom -> direct cause -> rule source -> meta rule source`）
