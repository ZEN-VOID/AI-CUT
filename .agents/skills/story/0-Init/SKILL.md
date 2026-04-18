---
name: story-init
description: "Use when initializing a new story2026 novel project in Codex through one of three modes: advisor council, fast one-shot, or autonomous questionnaire."
governance_tier: lite
allowed-tools: Read Write Edit Grep Bash Task WebSearch WebFetch
---

# Project Initialization (Codex Multi-Mode)

## Context Loading Contract

- 每次调用本技能时，必须同时加载同目录 `CONTEXT.md`。
- `CONTEXT.md` 只负责初始化经验、返工顺序与兼容性启发，不得覆盖本 `SKILL.md` 的模式合同与 handoff 契约。
- 若初始化脚本、模板与 `CONTEXT.md` 口径冲突，先修脚本与本技能合同，再修经验层描述。

## Overview

这是 `story2026` 的初始化入口，目标不是“边问边猜”，而是在 Codex 内先锁定初始化模式，再用对应执行路径把创作前置条件一次收集到足够可落盘的程度。

核心原则：
- 初始化必须先确定“谁来回答、谁来补全、谁来拍板”。
- 初始化元选项只能出现一次；一旦选定模式，后续只沿该模式的合同执行。
- `智能顾问团模式` 与 `快速模式` 走一次性内部任务，不再退回完整问卷。
- `自主模式` 才进入普通对话问卷，并保持 Codex 兼容，不依赖 Claude Code 专属交互控件。
- 所有模式最终都必须沉淀为同一份可落盘 handoff，而不是三套不同 schema。

## When to Use

- 需要新建一个全新的 `story2026` 小说项目。
- 需要从 0 收集题材、主角、世界观、金手指、创意约束等初始化信息。
- 当前环境是 Codex，本轮交互不能依赖 `AskUserQuestion` 一类 CC 专属工具。

## When Not to Use

- 已有项目骨架，只是补写设定或修正少数字段。
- 用户不是要初始化新项目，而是继续 `2-Planning` / `3-Drafting` / `review`。
- 只需要查询、恢复、学习，不需要新建项目。

## 目标

- 把 `0-Init` 收束成“项目立项层 / 创作委托层 / 初始治理层 + north star 长期总规范层”，而不是越权替 `1-Cards`、`2-Planning` 做整套细化设计。
- 通过结构化交互收集足够信息，避免“先生成再返工”。
- 产出可落地项目骨架：`STATE.json`、`TEAM.toml`、`CHANGELOG.md`、`.webnovel/state.json`、`.webnovel/workflow_state.json`、`.webnovel/execution_state.json`、`.webnovel/task_log.jsonl`、`.webnovel/tasks/`、`Init/north_star_contract.json`、`Init/初始化简报.json`、`Init/访谈摘要.md`、`Init/确认卡.md`、`Cards/*` 预留目录、`Planning/8-全息地图/` 预留目录、`Planning/legacy/总纲.md`（legacy 兼容骨架）、`.webnovel/idea_bank.json`。
- 为 `1-Cards` 生成稳定的对象种子，并把原“全局卡/全局总览”长期对象约束并入 `north_star_contract.cards`；为 `2-Planning` 生成稳定的编排种子，而不是把两个阶段的裁决提前混成一份大问卷。
- 保证后续 `/story-plan` 与 `/story-write` 可直接运行。

## 执行原则

1. 先收集，再生成；未过充分性闸门，不执行 `init_project.py`。
2. `0-Init` 只负责回答“想写什么、给谁看、必须守什么承诺、共同长期约束是什么、哪些问题留给下游”，不越权替 `1-Cards` / `2-Planning` 做细部收敛。
3. 先锁定模式，再执行对应路径；只有 `自主模式` 使用分波次问卷。
4. 初始化交接物默认拆成四段：`project_contract + cards_seed + planning_seed + unknowns`。
5. `cards_seed` 只提供对象建卡种子；`planning_seed` 只提供叙事编排种子；两者都不是 canonical truth。
6. 允许调用 `Read/Grep/Bash/Task/WebSearch/WebFetch` 辅助收集；`智能顾问团模式 / 快速模式` 默认走一次性内部任务，`自主模式` 默认走普通对话问卷。
7. 用户已明确的信息不重复问；冲突信息优先让用户裁决。
8. 默认初始化模式是 `自主模式`；用户未指定时，只在单一入口发送一次“初始化元选项卡”。
9. `自主模式（兼容旧称 Deep/深度模式）` 优先完整性，允许慢一点，但禁止漏关键字段；其余两种模式优先一次收束。

## Governance Artifact Root (Mandatory)

`0-Init` 必须承认两层治理入口：

- repo 级规则真源：`.codex/schemas/`、`.codex/runbooks/`、`.codex/registry/`
- 项目级复杂任务工件根：`<project_root>/.webnovel/tasks/`

硬规则：

1. `init_project.py` 至少要创建 `.webnovel/tasks/` 根目录，并在 `STATE.json.paths.task_artifacts_root` 中登记。
2. `0-Init` 自身负责准备根目录与入口清单，不负责伪造某个 run 的 `mandate.yaml / mission_brief.yaml`；这些由 tracked workflow 在实际 run 中旁路写入。
3. 后续 `story-init` 若以 tracked workflow 启动，生成的 `<run_id>/` 工件目录必须与这里的根目录声明一致。

## Root-Cause Execution Contract (Mandatory)

当 `0-Init` 出现执行失败、产物漂移、模式路由错误、handoff 缺字段、状态文件与合同不一致等非平凡问题时，必须按以下层级向上追溯，而不是只改一处局部输出：

1. `Symptom / Failure`
   - 先明确是交互层、脚本落盘层、handoff 层、还是治理层出现偏差。
2. `Direct Technical Cause`
   - 确认是字段未写、模式元信息丢失、路径校验缺失、脚本入口错误、测试未覆盖，还是 reference 加载顺序错误。
3. `Rule Source`
   - 优先检查本文件中的 `Initialization Mode Contract / Handoff Contract / Sufficiency Gate / Execution Procedure`，以及对应 `references/*-mode/module-spec.md`。
4. `Meta Rule Source`
   - 若问题已超出 `0-Init` 局部合同，继续上溯到仓库 `AGENTS.md` 的 rollout / root-cause / context 治理规则。
5. `Fix Landing Points`
   - 优先修最高杠杆源层：`SKILL.md`、模式 `module-spec.md`、`init_project.py`、测试、再到可读投影文件。

执行顺序硬约束：
- 先修规则/脚本/测试的真源，再修本次具体输出。
- 修复完成后，必须同时给出：`root cause location + immediate fix + systemic prevention fix`。
- 若没有更高一层的治理合同，必须显式说明“trace stopped at Rule Source”，不能假装已经上溯完成。

## Init Truth Ownership Contract (Mandatory)

`story2026` 重构后的真源分工已经固定，因此 `0-Init` 必须显式承认自己的边界：

- `0-Init`
  - 拥有：项目立项合同、创作承诺、`north_star_contract`、初始种子、未知项路由权
  - 不拥有：角色/场景/物品卡 canonical、规划 canonical、validated actualization
- `1-Cards`
  - 拥有：人物、场景、物品的对象真源
- `2-Planning`
  - 拥有：编排过程；最终收敛为 `MAP`
- `5-Loopback`
  - 拥有：`PASS` 后的 actualization 写回权

因此初始化默认产物必须按下列结构组织：

1. `project_contract`
   - 这本书的立项合同：题材、平台、规模、故事核、承诺、禁飞区、决策方式
2. `north_star_contract`
   - 初始化主文件：`story_kernel / reader_promise / aesthetic_axes / ip_boundary / cards`
   - 其中 `cards` 承担原“全局卡/全局总览”的长期对象总规范
3. `cards_seed`
   - 交给 `1-Cards` 的对象种子：角色、世界、金手指、关系、物品钩子
4. `planning_seed`
   - 交给 `2-Planning` 的编排种子：故事引擎、冲突方向、节奏规模、约束包
5. `unknowns`
   - 仍未决定、以及明确延后由 `1-Cards` / `2-Planning` 收敛的问题

旧式顶层 `project / protagonist / relationship / golden_finger / world / constraints` 可以保留作兼容镜像，但不再是首选思考模型。

## Initialization Mode Contract (Mandatory)

`0-Init` 必须先锁定且只锁定一次初始化元选项。三种模式的元选项、A/B/C 展示卡和选择规则只能在本节出现；其他章节只能引用本节，不得再次枚举或重写。

### 单一模式入口总表

| 模式 | 触发条件 | 执行形态 | 是否进入问卷 | 内部模板真源 | 默认拍板者 |
|---|---|---|---|---|---|
| 智能顾问团模式 | 用户点名要“顾问团/策划组/指定 agents 参与” | 顾问团并行会诊 + 协调助手一次性综合 | 否；只允许最终确认卡，必要时加 1 张裁决卡 | `references/advisor-council-mode/module-spec.md` | 用户 |
| 快速模式 | 用户明确想偷懒、让 LLM 直接补全 | 快速决策智能体一次性补全 + 协调助手复核 | 否；只允许最终确认卡，必要时加 1 张阻塞卡 | `references/fast-mode/module-spec.md` | 协调助手 |
| 自主模式 | 用户要自己一轮轮回答 | 用户问卷作答 + 助手结构化回填 | 是 | `references/autonomous-mode/module-spec.md` | 用户 |

### 单一元选项选择规则

1. 若用户明确指定 `.codex/agents` 下一个或多个 agent 文档作为顾问，则强制进入 `智能顾问团模式`。
2. 若用户表达“你直接帮我补完 / 我懒得答 / 你快速来一版”，则进入 `快速模式`。
3. 其余情况默认进入 `自主模式`。
4. 冲突优先级固定为：用户显式请求 > 模式合同 > 问卷默认策略。
5. 一旦模式锁定，必须立即加载该模式对应的 `references/*-mode/module-spec.md`，且只加载这一份模式细则作为执行真源。
6. 选择 `智能顾问团模式` 或 `快速模式` 后，禁止再回退为完整问卷流程；仅允许单张必要裁决/阻塞卡。
7. 无论哪种模式，最终都必须把 `用户确认项`、`顾问团意见`、`助手推断项` 分层记录。
8. `mode_source` 必须显式记录为 `user_selected / defaulted / inferred / switched_midway` 之一。

### 初始化元选项卡（唯一合法展示位）

若用户尚未明确模式，先发送：

```markdown
初始化元选项卡

1. 本次初始化方式
A. 智能顾问团模式
B. 快速模式
C. 自主模式（默认）

2. 如果选 A，顾问团布阵方式
A. 同一套班底，三阶段通用
B. 三个阶段分别指定

3. 若 2A，请给通用 agent 路径（可多个）
示例：`.codex/agents/小说家/金庸.md, .codex/agents/导演/徐克.md`

4. 若 2B，请分别给三阶段坐镇 agent 路径（可为空）
- 策划：`.codex/agents/小说家/金庸.md, .codex/agents/导演/徐克.md`
- 监制：`.codex/agents/制片/新藤兼人.md`
- 评审：`.codex/agents/评论家/博尔赫斯.md`

5. 如果选 B，是否允许我为特定概念联网补全
A. 允许，按需精准检索
B. 不联网，只靠本地知识和上下文

6. 最终拍板方式
A. 仍由我拍板
B. 你先综合给定稿，我只做最后确认
```

### 模式元数据记录 Contract

模式一旦确定，必须立刻记录以下元字段，供 handoff、状态文件和后续恢复使用：

- `init_mode`
- `team_setup.team_mode`
- `team_setup.shared_agents`
- `team_setup.roles.planning.members`
- `team_setup.roles.production.members`
- `team_setup.roles.review.members`
- `advisor_agents`（legacy mirror：默认映射策划阶段）
- `research_policy`
- `decision_owner`
- `mode_source`

若本轮已经完成字段来源裁决，还必须同步记录：

- `sources_breakdown.user_confirmed`
- `sources_breakdown.council_advised`
- `sources_breakdown.assistant_inferred`

## Advisor Council Contract (智能顾问团模式，Mandatory)

1. 顾问源默认来自 `.codex/agents/**/*.md`；可按 `策划 / 监制 / 评审` 三阶段分别指定，也可使用“同一套班底，三阶段通用”的快捷选项。
2. 调度前必须校验路径存在、可读，且确实是 agent 规则文档；失效路径要明确报告。
3. 锁定本模式后，禁止进入完整问卷；必须改为一次性内部初始化任务，并以 `references/advisor-council-mode/module-spec.md` 为唯一模板真源。
4. 必须先确定三阶段布阵：
   - `策划` 默认管辖 `0-Init / 1-Cards / 2-Planning`
   - `监制` 默认管辖 `3-Drafting / 5-Loopback`
   - `评审` 默认管辖 `4-Validation / review`
5. 必须并行启动后台 subagents；每位顾问 agent 单独一条线程，读取同一份初始化 brief 与当前已知字段；若使用“三阶段分别指定”，协调助手应先按阶段整理顾问名单。
6. 顾问 agent 负责从其专业立场、审美倾向、灵魂人格与知识库出发给建议，但不得越权改写最终 canonical。
7. 协调助手必须汇总一次性会诊结果，并输出：
   - `共识`
   - `关键分歧`
   - `建议采用方案`
   - `少数派高价值提醒`
8. 若顾问团之间冲突明显，必须显式暴露冲突，而不是偷选其一。
9. 若用户本人和顾问团冲突，默认用户胜；若用户授权“顾问团先拟定”，也必须标成 `assistant_inferred / council_advised`。
10. 若存在无法自动裁决的高后果分歧，只允许追加 1 张用户裁决卡，不得退回完整问卷。
11. 若运行环境暂时无法使用后台 subagents，必须降级为顺序读取指定 agent 文档并模拟顾问纪要，同时明确说明是降级执行。

## Fast Mode Contract (快速模式，Mandatory)

1. 快速模式允许用户只给一句话梗概、题材词或情绪目标。
2. 锁定本模式后，禁止进入完整问卷；必须改为一次性内部初始化任务，并以 `references/fast-mode/module-spec.md` 为唯一模板真源。
3. 协调助手可以直接替用户补完核心合同卡和各条件模块卡的大部分字段，但必须把推断项单独标记为 `assistant_inferred`。
4. 若存在两条以上后果差异明显的高风险路径，仍要最小化追问，只问 1 张阻塞卡，不得退回完整长问卷。
5. 可使用后台 subagents 分工，但这些 subagents 只承担结构补全、风险校对、精准检索职责，禁止人格扮演式代入。
6. 联网只用于特定概念的专业校准、时间敏感信息核验、或用户明确要求的当前趋势参考。
7. 联网结果必须服务于字段补全，不得把网页摘要堆成外部资料墙。

## Autonomous Mode Contract (自主模式，Mandatory)

`自主模式` 即当前默认的一轮一轮问卷协作模式，兼容旧称 `Deep/深度模式`。

1. 锁定本模式后，必须加载 `references/autonomous-mode/module-spec.md` 作为问卷编排细则。
2. 每轮由用户本人直接回答，助手负责结构化回填与缺口追问。
3. 用户如果回答“你先给建议”，可以给候选，但关键字段仍以用户确认后再落盘为主。
4. 允许用户跳题、模糊回答或自由叙述；助手必须先吸收并结构化，不能机械要求重填格式。
5. 若用户在中途切换到“你直接补完”，可从 `自主模式` 升级到 `快速模式`；需在本轮摘要里记录模式切换。

## Autonomous Questionnaire Contract (自主模式专用，Mandatory)

只有 `自主模式` 才进入本节的“结构化问卷卡”流程；`智能顾问团模式` 与 `快速模式` 不得引用本节作为主执行路径。

### 问卷卡输出规则

1. 每轮输出一个问卷卡，建议 4-8 个问题，避免一次塞满全部字段。
2. 每题都尽量给出：
   - 简短标题
   - 可选项 `A/B/C`
   - 必要时的自由填写位
   - 一行示例
3. 允许用户用这三种方式回答：
   - 逐题作答
   - 自由叙述，由助手回填结构化字段
   - 简写答案，如 `1=A, 2=A+B, 3=100万字`
4. 若用户不知道，可接受：`未知`、`待定`、`你先给建议`。
5. 每轮结束后，必须返回：
   - 已确认字段
   - 助手推断字段
   - 仍缺失字段
   - 这些缺口是留给 `1-Cards` 还是 `2-Planning`
   - 下一轮是否继续问卷

### 关键裁决规则

- 需要用户做选择时，用普通文本 A/B/C 方案，不使用专属 UI 组件。
- 若用户回答自由文本，助手负责归一化，不允许因为格式不标准就整轮重问。
- 若出现冲突字段，必须显式列出冲突点，再让用户二选一或给第三方案。
- 未过充分性闸门前，不得提前执行 `init_project.py`。
- 默认不是“一次只问一个问题”；优先使用成组问卷卡，让体验更接近表单式采集。
- 默认不是“所有项目都走同一套固定问卷”；应先走核心合同卡，再按缺口加载条件模块卡。

### 核心合同卡（所有项目必问）

所有项目都必须先收这组最小立项信息：

```markdown
初始化核心合同卡

请直接按编号回答。你可以：
- 写完整答案
- 只写字母，如 `1=A, 2=B`
- 自由描述，我来帮你回填

1. 项目名 / 工作名
2. 题材走廊（可复合）
3. 规模带（字数或章数）
4. 一句话故事
5. 核心冲突
6. 目标读者 / 平台
7. 你最想守住的承诺（卖点 / 反套路 / 禁飞区）
```

### 条件模块卡（按缺口加载）

只在对应信息不足时追加，不默认全开：

- `角色模块卡`
  - 当主角欲望、缺陷、主反派镜像或主角结构不足以支撑 `cards_seed.character_seed`
- `世界模块卡`
  - 当世界规模、力量体系、势力格局或资源规则不足以支撑 `cards_seed.global_seed`
- `物件/金手指模块卡`
  - 当金手指代价、可见度、成长节奏或专属物钩子不足
- `规划模块卡`
  - 当故事引擎、冲突链、开篇钩子、约束包不足以支撑 `planning_seed`
- `商业与风格模块卡`
  - 当平台承诺、受众预期、风格走廊和禁飞区仍含混

### 回答解析规则

- 用户只回字母：按当前问卷卡的选项直接映射。
- 用户回字母加补充：优先保留补充文本。
- 用户只写一大段描述：助手先拆回结构化字段，再只追问缺口。
- 用户跳题：标记为缺失，不重发整张问卷卡。

## Cards Handoff Contract (Mandatory)

当核心合同卡与条件模块卡完成后，`0-Init` 必须把“已确认字段 + 助手推断补全 + 未决问题”固化为 `1-Cards` 的唯一上游双文件入口：`north_star_contract + 初始化简报`。

固定交接顺序：

1. `Init/north_star_contract.json.cards`
   - 承担原“全局卡/全局总览”的长期对象总规范
   - 默认收束 `文字风格 / 叙事风格 / 世界观 / 规则体系 / 年代约时 / 文化 / 艺术 / 科技武功 / 关系网总览`
2. `../1-Cards`
   - 角色卡请求加载 `references/character-card-module/module-spec.md`
   - 优先读取 `north_star_contract.story_kernel / reader_promise / aesthetic_axes / cards + cards_seed.character_seed + unknowns`
3. `../1-Cards`
   - 场景卡请求加载 `references/scene-card-module/module-spec.md`
   - 优先读取 `north_star_contract.story_kernel / reader_promise / aesthetic_axes / cards + cards_seed.global_seed + unknowns`
4. `../1-Cards`
   - 物品卡请求加载 `references/item-card-module/module-spec.md`
   - 优先读取 `north_star_contract.story_kernel / reader_promise / aesthetic_axes / cards + cards_seed.item_seed + 角色卡 + unknowns`

交接规则：

- 默认尺度是“整部小说 / 全剧集”，不是单卷或单章。
- 当用户偷懒、字段缺失或只给一句话梗概时，允许助手基于题材、平台、商业定位、角色结构、反套路约束做保守补全，但必须把“推断项”和“用户确认项”分开。
- `1-Cards` 首选读取 `north_star_contract + cards_seed + unknowns`，其中长期共同约束优先来自 `north_star_contract.cards`，而不是把整个初始化简报当成无结构散文。
- `planning_seed` 只作为故事承诺、冲突方向和节奏预期的辅助背景，不得倒灌为对象 canonical。
- 交给 `1-Cards` 的卡片 schema 默认采用 `core/current_state/history` 一体式结构，不允许在初始化层另造“静态版 / 动态版”双真源。
- 若初始化信息存在重大冲突（如题材、主角结构、世界规则互斥），必须先阻断并澄清，不得把冲突原样传给下游卡技能。

## Init Handoff Artifact Contract (Mandatory)

`0-Init` 完成后，必须把交接物落到 `Init/` 下的固定文件：

- `Init/初始化简报.json`
  - companion handoff。
  - 供 `1-Cards / 2-Planning` 承接 `cards_seed + planning_seed + unknowns`。
  - 默认结构为：`north_star_ref + cards_seed + planning_seed + unknowns`。
- `Init/north_star_contract.json`
  - 初始化主文件。
  - 作为“总引领”承载 `story_kernel / reader_promise / aesthetic_axes / ip_boundary / cards / decision_policy`。
  - `cards` 分区默认承接原“全局卡/全局总览”的长期对象总规范。
  - 是 `0-Init` 面向 `1-Cards / 2-Planning` 的首要上游入口。
- `Init/访谈摘要.md`
  - 人工可读导航页。
  - 只保留文件角色、会话元信息与 unknowns，不重复正文设定。
- `Init/确认卡.md`
  - 冻结本轮初始化边界。
  - 用于标记“主次文件裁决 / 未决字段 / 交接规则”。

执行规则：

- `1-Cards` 的 canonical 上游默认是 `Init/north_star_contract.json + Init/初始化简报.json`，其中长期共同约束默认读取 `north_star_contract.json.cards`，不是散落在 `Init/*.md` 里的 seed 文档。
- `Init/访谈摘要.md` 与 `Init/确认卡.md` 只能作为可读投影，不得反向改写 `1-Cards` canonical。
- 如果 `Init/north_star_contract.json` 或 `Init/初始化简报.json` 缺失，必须先补齐，再允许进入 `1-Cards`。

## Init Seed Contract (Mandatory)

历史 `Init/*.md` 仅在旧项目中允许保留；新初始化默认不得再落这些 seed 文档。若旧项目存在，它们的角色已经降级：

- 它们只属于 seed / legacy-compat 层，不再是人物、世界、规则、物品的正式真源。
- 这些文件可以帮助 `1-Cards` 做一次性迁移读取，但不得成为后续阶段持续维护的对象。
- 一旦 `1-Cards` 已完成建卡，所有人物、世界、规则、物品的 canonical 都统一转入 `Cards/**/*.json`。
- 新的修订应优先落在 `Cards/**/*.json`；若仍去改 `Init/*.md`，视为越级写回。

## Quick Reference

| 执行路径 | 目标 | 主载体 | 用户交互 |
|---|---|---|---|
| 智能顾问团一次性初始化 | 顾问团并发给出初始化合稿 | `references/advisor-council-mode/module-spec.md` | 默认仅最终确认卡，必要时加 1 张裁决卡 |
| 快速模式一次性初始化 | 快速决策智能体直接补完落盘草案 | `references/fast-mode/module-spec.md` | 默认仅最终确认卡，必要时加 1 张阻塞卡 |
| 自主模式问卷初始化 | 分轮采集并结构化回填 | `references/autonomous-mode/module-spec.md` + `Autonomous Questionnaire Contract` | 问卷卡 + 确认卡 |

## 引用加载等级（strict, lazy）

采用分级加载，避免一次性灌入全部资料：

- L0：未确认任务前，不预加载参考。
- L1：每个阶段仅加载该阶段“必读”文件。
- L1.5：模式锁定后，只加载且只允许加载 1 份 `references/*-mode/module-spec.md` 模式细则。
- L2：仅在题材、金手指、创意约束触发条件满足时加载扩展参考。
- L3：市场趋势类、时效类资料仅在用户明确要求时加载。

路径约定：
- `references/...` 相对当前 skill 目录（`${REPO_ROOT}/.agents/skills/story/0-Init/references/...`）。
- `templates/...` 相对 `story2026` 共享模板目录（`${REPO_ROOT}/.agents/skills/story/templates/...`）。
- 题材资料唯一根目录固定为 `${REPO_ROOT}/.agents/skills/story/templates/genres/`：
  - 入口模板：`templates/genres/{genre}.md`
  - 细粒度分片：`templates/genres/details/{genre_slug}/`
  - 禁止再维护平行根目录（例如 `${REPO_ROOT}/.agents/skills/story/genres/`）

默认加载清单：
- L1（启动前）：`templates/genres/README.md`
- L1.5（模式锁定后，三选一）：
  - `references/advisor-council-mode/module-spec.md`
  - `references/fast-mode/module-spec.md`
  - `references/autonomous-mode/module-spec.md`
- L2（按需）：
  - 题材模板：`templates/genres/{genre}.md`
  - 金手指：`../../templates/golden-finger-templates.md`
  - 世界观：`templates/worldbuilding/*.md`
  - 创意路由：`references/creative-seed-routing/module-spec.md`
- L3（显式请求）：
  - 仅当 `references/creative-seed-routing/module-spec.md` 已判定需要趋势校准，且用户明确要求参考当下平台/市场趋势时，才进一步读取 `references/creative-seed-routing/market-trends-2026.md` 并配合 `WebSearch/WebFetch`

## Reference Loading Guide

- 默认判定顺序：`templates/genres/README.md` -> 三选一模式模块 -> `creative-seed-routing`（若创意/商业缺口成立） -> 题材/worldbuilding 叶子资料 -> 趋势校准
- 默认入口：先锁 `init_mode`，再决定是否进入 `creative-seed-routing`
- 互斥规则：`advisor-council-mode / fast-mode / autonomous-mode` 三者互斥
- 串行规则：任一模式模块在锁定后，都可以按需串行进入 `creative-seed-routing`
- 按需加载规则：`creative-seed-routing`、题材详情、worldbuilding、趋势校准都不是默认全开

| 模块 | 触发条件 | 进入信号 | 与其他模块关系 | 必读文件 |
| --- | --- | --- | --- | --- |
| `advisor-council-mode` | 用户指定顾问团 agent 路径或明确要求顾问会诊 | `init_mode == 智能顾问团模式` | 与其余 mode-playbook 互斥；可串行调用 `creative-seed-routing` | `references/advisor-council-mode/module-spec.md` |
| `fast-mode` | 用户要求快速补完或偷懒式初始化 | `init_mode == 快速模式` | 与其余 mode-playbook 互斥；可串行调用 `creative-seed-routing` | `references/fast-mode/module-spec.md` |
| `autonomous-mode` | 用户选择自己逐轮作答，或未指定模式 | `init_mode == 自主模式` | 与其余 mode-playbook 互斥；可串行调用 `creative-seed-routing` | `references/autonomous-mode/module-spec.md` |
| `creative-seed-routing` | `planning_seed`、`creative_mandate`、商业定位、反套路或趋势校准存在缺口 | 规划模块卡 / 商业与风格模块卡 / 用户卡顿 / 复合题材 / 显式趋势请求 | 不是 mode-playbook；由任一模式按需串行加载 | `references/creative-seed-routing/module-spec.md` |

## References（逐文件引用清单）

### 根目录

- `../query/references/system-data-flow.md`
  - 用途：共享权威数据流文档；用于初始化产物与后续 `/plan`、`/write` 的数据流一致性检查。
  - 触发：Step 0 预检必读。

### shared templates

- `templates/genres/README.md`
  - 用途：题材资产唯一根目录、入口模板与 detail pack 映射、共享题材使用启发式。
  - 触发：所有项目必读。
- `templates/genres/{genre}.md`
  - 用途：已选题材的入口模板，承担题材归一化与基本爽点/结构提示。
  - 触发：用户明确主题材或需要对候选题材做比较时按需读取。
- `templates/genres/details/{genre_slug}/`
  - 用途：细粒度题材工法、套路变体、节奏与结构深化。
  - 触发：仅在入口模板不足以完成初始化判断时按需读取。
- `templates/worldbuilding/README.md`
  - 用途：共享 worldbuilding 根目录与跨阶段使用规则。
  - 触发：涉及人物、势力、力量体系或世界规则时按需读取。
- `templates/worldbuilding/*.md`
  - 用途：跨阶段共享的 worldbuilding 工法；供初始化补问与对象种子归一化使用。
  - 触发：对应对象或世界维度被提及且需要深化时按需读取。

### mode-playbook modules

- `references/advisor-council-mode/module-spec.md`
  - 用途：顾问团模式的一次性内部任务模板、顾问并发规则、综合裁决规则。
  - 触发：`init_mode == 智能顾问团模式` 时必读；加载后禁止进入完整问卷。
- `references/fast-mode/module-spec.md`
  - 用途：快速模式的一次性内部任务模板、推断补全规则、阻塞卡闸门。
  - 触发：`init_mode == 快速模式` 时必读；加载后禁止进入完整问卷。
- `references/autonomous-mode/module-spec.md`
  - 用途：自主模式的问卷编排、轮次裁剪、结构化回填规则。
  - 触发：`init_mode == 自主模式` 时必读；加载后方可进入 `Autonomous Questionnaire Contract`。

### worldbuilding

- `templates/worldbuilding/character-design.md`
  - 用途：角色模块卡中的角色维度补问（目标、缺陷、动机、反差）。
  - 触发：用户人物信息抽象或扁平时加载。
- `templates/worldbuilding/faction-systems.md`
  - 用途：世界模块卡中的势力格局与组织层级设计。
  - 触发：世界模块卡默认加载。
- `templates/worldbuilding/power-systems.md`
  - 用途：世界模块卡中的力量体系类型与边界定义。
  - 触发：涉及修仙/玄幻/高武/异能时加载。
- `templates/worldbuilding/setting-consistency.md`
  - 用途：确认卡前做设定冲突检查。
  - 触发：确认卡前默认加载。
- `templates/worldbuilding/world-rules.md`
  - 用途：世界模块卡中的世界规则与禁忌项收束。
  - 触发：世界模块卡默认加载。

### creativity

- `references/creative-seed-routing/module-spec.md`
  - 用途：`0-Init` 中所有创意约束、卖点、商业定位、复合题材、反套路和趋势校准的统一 governed route；内部负责把本地 leaf references 最小化加载并写回 `project_contract.creative_mandate / planning_seed / unknowns`。
  - 触发：规划模块卡、商业与风格模块卡、复合题材、用户在核心合同卡或规划模块卡卡住、或显式要求平台/趋势判断时按需读取。
  - 边界：父 `SKILL.md` 与各 mode-playbook 不再散点点名内部 leaf references；具体叶子文档、题材 -> 反套路映射与趋势 L3 闸门统一在该模块内维护。

## 工具策略（按需）

- `Read/Grep`：读取项目上下文与参考文件（`README.md`、`CLAUDE.md`、`templates/genres/*`、`templates/worldbuilding/*`、`references/*`）。
- 若需深挖题材工法，可继续读取 `templates/genres/details/*`，但 canonical 根目录仍是 `templates/genres/`。
- `Bash`：执行 `init_project.py`、文件存在性检查、最小验证命令。
- `Task`：拆分并行子任务（如题材映射、约束包候选生成、文件验证）。
- `普通对话问卷`：仅 `自主模式` 的默认交互方式；`智能顾问团模式 / 快速模式` 只允许使用单张必要裁决卡或阻塞卡。
- `WebSearch`：用于检索最新市场趋势、平台风向、题材数据（可带域名过滤）。
- `WebFetch`：用于抓取已确定来源页面内容并做事实核验。
- 外部检索触发条件：
  - 用户明确要求参考市场趋势或平台风向；
  - 创意约束需要“时间敏感依据”；
  - 对题材信息存在明显不确定。

## 交互与执行流程

### Step 0：预检与上下文加载

环境设置（bash 命令执行前）：
```bash
export WORKSPACE_ROOT="${CLAUDE_PROJECT_DIR:-$PWD}"
export REPO_ROOT="${CLAUDE_PROJECT_DIR:-$PWD}"

if [ ! -d "${REPO_ROOT}/.agents/skills/story/scripts" ]; then
  echo "ERROR: 缺少目录: ${REPO_ROOT}/.agents/skills/story/scripts" >&2
  exit 1
fi
export SCRIPTS_DIR="${REPO_ROOT}/.agents/skills/story/scripts"
```

必须做：
- 确认当前目录可写。
- 解析脚本目录并确认入口存在（仅支持当前仓库内的 `story2026` 本地技能包）：
  - 固定路径：`${REPO_ROOT}/.agents/skills/story/scripts`
  - 入口脚本：`${SCRIPTS_DIR}/story.py`
- 建议先打印解析结果，避免写到错误目录：
  - `python "${SCRIPTS_DIR}/story.py" --project-root "${WORKSPACE_ROOT}" where`
- 加载最小参考：
  - `../query/references/system-data-flow.md`（用于校对 init 产物与 plan/write 输入链路）
  - `templates/genres/README.md`
  - `templates/genres/`（用户选定题材后按需读取对应入口模板与 detail pack）

输出：
- 进入正式采集前的“已知信息清单”和“待收集清单”。

### Step 0.5：模式选择与分流

必须先确定本次初始化模式，再决定后续问卷路径。

执行规则：
- 若用户已在首条需求里明确模式，则直接记录，不重复发卡。
- 若用户未明确模式，只能发送一次“初始化元选项卡”。
- 记录以下元字段，供后续 handoff 与状态文件使用：
  - `init_mode`
  - `team_setup.team_mode`
  - `team_setup.shared_agents`
  - `team_setup.roles.planning.members`
  - `team_setup.roles.production.members`
  - `team_setup.roles.review.members`
  - `advisor_agents`（legacy mirror）
  - `research_policy`
  - `decision_owner`
  - `mode_source`（user_selected / defaulted / inferred / switched_midway）

分流规则：
- `智能顾问团模式`：
  - 立即加载 `references/advisor-council-mode/module-spec.md`。
  - 进入一次性内部任务路径，不再进入 Step 1-4 的问卷轮次。
- `快速模式`：
  - 立即加载 `references/fast-mode/module-spec.md`。
  - 进入一次性内部任务路径，不再进入 Step 1-4 的问卷轮次。
- `自主模式`：
  - 立即加载 `references/autonomous-mode/module-spec.md`。
  - 按“核心合同卡 -> 条件模块卡 -> unknowns -> 确认卡”的顺序走完整交互。

### Step 0.6：一次性初始化执行（仅智能顾问团模式 / 快速模式）

若当前模式是 `智能顾问团模式` 或 `快速模式`，必须在 Step 0.5 后直接执行本步：

- 基于当前用户输入、已知字段和题材触发参考，构造一次性初始化 brief。
- 调用对应 `references/*-mode/module-spec.md` 中的内部任务模板，让顾问团或快速决策智能体一次性产出：
  - `project_contract`
  - `cards_seed`
  - `planning_seed`
  - `unknowns`
  - `sources_breakdown`（`user_confirmed / council_advised / assistant_inferred`）
- 若存在无法自动裁决的关键分歧，只允许补发 1 张用户裁决/阻塞卡。
- 完成后直接跳到 Step 5 与 Step 6；不得回流到 Step 1-4 的完整问卷链。

### Step 1（仅自主模式）：核心合同卡

所有项目都先从这一步开始，目标是生成 `project_contract`。

必收字段：
- 书名
- 题材走廊（支持 A+B）
- 规模带（字数或章数至少一个）
- 一句话故事
- 核心冲突
- 目标读者 / 平台
- 核心承诺（卖点、反套路、禁飞区三选一或多选一）

产物：
- `project_contract.creative_mandate`
- `project_contract.promise_surface`

### Step 2（仅自主模式）：判断缺口属于 Cards 还是 Planning

在继续追问前，必须先判断每个缺口的 truth owner：

- 若问题属于“对象是什么、长期约束是什么”：
  - 路由到 `cards_seed`
- 若问题属于“故事如何推进、如何升级、如何兑现”：
  - 路由到 `planning_seed`
- 若当前无法决定：
  - 记入 `unknowns`

### Step 3（仅自主模式）：条件模块卡 - Cards Seed

只有在对象种子不足时才发这一轮。

典型字段：
- 主角姓名 / 欲望 / 缺陷 / 主角结构
- 女主与共主角骨架
- 反派分层与镜像关系
- 世界规模 / 势力格局 / 力量体系 / 资源逻辑
- 金手指类型 / 可见度 / 不可逆代价 / 成长节奏

本轮目标：
- 补齐 `cards_seed.global_seed`
- 补齐 `cards_seed.character_seed`
- 补齐 `cards_seed.item_seed`

### Step 4（仅自主模式）：条件模块卡 - Planning Seed

只有在叙事编排种子不足时才发这一轮。

典型字段：
- 开篇钩子
- 主角缺陷如何驱动剧情
- 反派镜像怎样形成长期压力
- 反套路规则
- 硬约束 2-3 条
- 金手指代价如何变成长期推进机制

本轮目标：
- 补齐 `planning_seed.story_engine`
- 补齐 `planning_seed.pacing_scale`
- 补齐 `planning_seed.constraint_seed`

备注：
- 若用户要求“贴近当下市场”，可触发外部检索并标注时间戳。
- 若用户卡住，可给 2-3 套候选约束包，按 `A / B / C` 编号。

### Step 5：Unknowns 与下游路由确认

必须把仍未解决的问题显式归档，而不是假装初始化已经全知。

至少输出：
- `unknowns.unresolved_questions`
- `unknowns.deferred_to_cards`
- `unknowns.deferred_to_planning`

规则：
- `deferred_to_cards` 里的问题，后续由 `1-Cards` 在建卡时继续收敛。
- `deferred_to_planning` 里的问题，后续由 `2-Planning` 在 1-7 pass 中继续收敛。

### Step 6：确认卡 - 一致性复述与最终确认

必须输出“初始化摘要草案”并让用户确认：
- 项目合同
- Cards Seed
- Planning Seed
- Unknowns 与下游路由
- 字段来源分层（`user_confirmed / council_advised / assistant_inferred`）

确认规则：
- 用户未明确确认，不执行生成。
- 若用户仅改局部，回到对应模块卡做最小重采集。

## 内部数据模型（初始化收集对象）

```json
{
  "init_session": {
    "mode": "自主模式",
    "mode_source": "user_selected",
    "advisor_agents": [],
    "team_setup": {
      "team_mode": "same_lineup",
      "shared_agents": [],
      "roles": {
        "planning": {"members": [], "governs": [".agents/skills/story/0-Init", ".agents/skills/story/1-Cards", ".agents/skills/story/2-Planning"]},
        "production": {"members": [], "governs": [".agents/skills/story/3-Drafting", ".agents/skills/story/5-Loopback"]},
        "review": {"members": [], "governs": [".agents/skills/story/4-Validation", ".agents/skills/story/review"]}
      }
    },
    "research_policy": "none",
    "decision_owner": "user"
  },
  "project_contract": {
    "creative_mandate": {
      "title": "",
      "genre": "",
      "target_words": 0,
      "target_chapters": 0,
      "one_liner": "",
      "core_conflict": "",
      "target_reader": "",
      "platform": ""
    },
    "promise_surface": {
      "core_selling_points": [],
      "anti_trope": "",
      "hard_constraints": [],
      "opening_hook": ""
    }
  },
  "cards_seed": {
    "global_seed": {
      "world_scale": "",
      "factions": "",
      "power_system_type": "",
      "social_class": "",
      "resource_distribution": ""
    },
    "character_seed": {
      "protagonist": {
        "name": "",
        "desire": "",
        "flaw": "",
        "archetype": "",
        "structure": "单主角"
      },
      "relationship": {
        "heroine_config": "",
        "heroine_names": [],
        "co_protagonists": [],
        "antagonist_tiers": {},
        "antagonist_mirror": ""
      }
    },
    "item_seed": {
      "golden_finger": {
        "type": "",
        "name": "",
        "style": "",
        "visibility": "",
        "irreversible_cost": "",
        "growth_rhythm": ""
      }
    }
  },
  "planning_seed": {
    "story_engine": {
      "one_liner": "",
      "core_conflict": "",
      "protagonist_desire": "",
      "protagonist_flaw": "",
      "antagonist_mirror": "",
      "golden_finger_cost": "",
      "golden_finger_growth_rhythm": "",
      "opening_hook": ""
    },
    "constraint_seed": {
      "anti_trope": "",
      "hard_constraints": [],
      "core_selling_points": []
    }
  },
  "unknowns": {
    "unresolved_questions": [],
    "deferred_to_cards": [],
    "deferred_to_planning": []
  },
  "sources_breakdown": {
    "user_confirmed": [],
    "council_advised": [],
    "assistant_inferred": []
  }
}
```

## Field-Centric Mapping (Tier-Lite)

| step_id | field_id | quality_dimension | fail_code | rework_entry |
|---|---|---|---|---|
| `step-0.5-mode-lock` | `init_session.mode / mode_source / decision_owner` | 模式锁定后必须可追溯、可恢复、枚举值合法 | `INIT_MODE_METADATA_DRIFT` | 回到 `Initialization Mode Contract`、`Step 0.5` 与 `init_project.py`，补齐 state / handoff / task_log 三层写入 |
| `step-0.6-one-shot` | `sources_breakdown.*` | 顾问建议、用户确认、助手推断必须分层，不得混写 | `INIT_SOURCE_ATTRIBUTION_MISSING` | 回到对应模式 `module-spec.md` 与 `Step 0.6 / Step 6`，补 provenance 字段并补测试 |
| `step-1-project-contract` | `project_contract.creative_mandate / promise_surface` | 立项合同足够支撑后续 cards/planning 起跑 | `INIT_PROJECT_CONTRACT_THIN` | 回到核心合同卡，补最小阻塞字段或显式下沉到 `unknowns` |
| `step-3-cards-seed` | `cards_seed.*` | 对象种子够用但不越权抢 canonical | `INIT_CARDS_SEED_OVERREACH` | 回到 `Cards Handoff Contract`，把不该现在定死的字段退回 `unknowns` 或留给 `1-Cards` |
| `step-4-planning-seed` | `planning_seed.*` | 编排种子可供 `2-Planning` 起跑，但不替代 MAP | `INIT_PLANNING_SEED_OVERREACH` | 回到 `planning_seed` 路由规则，保留故事引擎与约束种子，撤销过度规划 |
| `step-5-unknowns` | `unknowns.unresolved_questions / deferred_to_*` | 未决项必须显式、路由清晰 | `INIT_UNKNOWNS_DROPPED` | 回到 `Unknowns` 归档步骤，禁止假装“已全部确定” |
| `step-6-confirmation` | `north_star_contract / 初始化简报 / 摘要 / 确认卡` | 主次文件关系清晰，伴生 handoff 不抢主文件 | `INIT_HANDOFF_ROLE_DRIFT` | 回到 `Init Handoff Artifact Contract` 与脚本落盘逻辑，统一主文件、伴生 handoff、可读投影的职责 |
| `step-7-path-safety` | `project_root` | 项目路径安全、不会写进 skill 包或隐藏非法目录 | `INIT_PROJECT_ROOT_UNSAFE` | 回到 `项目目录安全规则` 与 `init_project.py` 路径校验，拒绝危险目录并做安全化处理 |

## 充分性闸门（必须通过）

未满足以下条件前，禁止执行 `init_project.py`：

1. 初始化模式已确定，且模式来源已记录。
2. 书名、题材（可复合）已确定。
3. 目标规模可计算（字数或章数至少一个）。
4. `project_contract.creative_mandate.one_liner` 与 `core_conflict` 至少有一个可用；另一个可记入 `unknowns`。
5. 至少有一组可供 `1-Cards` 使用的对象种子：
   - 主角种子，或
   - 世界/规则种子，或
   - 金手指/物件种子
6. 至少有一组可供 `2-Planning` 使用的编排种子：
   - 开篇钩子，或
   - 反套路 / 硬约束，或
   - 主反派镜像 / 剧情驱动缺陷
7. 所有未补齐的关键项都已显式写入 `unknowns`，并标明由 `1-Cards` 还是 `2-Planning` 继续收敛。

## 项目目录安全规则（必须）

- `project_root` 必须由书名安全化生成（去非法字符，空格转 `-`）。
- 若安全化结果为空或以 `.` 开头，自动前缀 `proj-`。
- 禁止在 `story2026` 技能包目录下生成项目文件（`${REPO_ROOT}/.agents/skills/story`）。

## 执行生成

### 1) 运行初始化脚本

```bash
python "${SCRIPTS_DIR}/story.py" init \
  "{project_root}" \
  "{title}" \
  "{genre}" \
  --init-mode "{init_mode}" \
  --mode-source "{mode_source}" \
  --decision-owner "{decision_owner}" \
  --advisor-agents "{advisor_agents}" \
  --shared-council-agents "{shared_council_agents}" \
  --planning-agents "{planning_agents}" \
  --production-agents "{production_agents}" \
  --review-agents "{review_agents}" \
  --research-policy "{research_policy}" \
  --user-confirmed-fields "{user_confirmed_fields}" \
  --council-advised-fields "{council_advised_fields}" \
  --assistant-inferred-fields "{assistant_inferred_fields}" \
  --one-liner "{one_liner}" \
  --core-conflict "{core_conflict}" \
  --protagonist-name "{protagonist_name}" \
  --target-words {target_words} \
  --target-chapters {target_chapters} \
  --golden-finger-name "{gf_name}" \
  --golden-finger-type "{gf_type}" \
  --golden-finger-style "{gf_style}" \
  --golden-finger-growth-rhythm "{gf_growth_rhythm}" \
  --core-selling-points "{core_points}" \
  --protagonist-structure "{protagonist_structure}" \
  --heroine-config "{heroine_config}" \
  --heroine-names "{heroine_names}" \
  --heroine-role "{heroine_role}" \
  --co-protagonists "{co_protagonists}" \
  --co-protagonist-roles "{co_protagonist_roles}" \
  --antagonist-tiers "{antagonist_tiers}" \
  --antagonist-mirror "{antagonist_mirror}" \
  --world-scale "{world_scale}" \
  --factions "{factions}" \
  --power-system-type "{power_system_type}" \
  --social-class "{social_class}" \
  --resource-distribution "{resource_distribution}" \
  --gf-visibility "{gf_visibility}" \
  --gf-irreversible-cost "{gf_irreversible_cost}" \
  --currency-system "{currency_system}" \
  --currency-exchange "{currency_exchange}" \
  --sect-hierarchy "{sect_hierarchy}" \
  --cultivation-chain "{cultivation_chain}" \
  --cultivation-subtiers "{cultivation_subtiers}" \
  --protagonist-desire "{protagonist_desire}" \
  --protagonist-flaw "{protagonist_flaw}" \
  --protagonist-archetype "{protagonist_archetype}" \
  --antagonist-level "{antagonist_level}" \
  --target-reader "{target_reader}" \
  --platform "{platform}" \
  --anti-trope "{anti_trope}" \
  --hard-constraints "{hard_constraints}" \
  --opening-hook "{opening_hook}"
```

字段来源约定：

- 若上游已经完成字段来源裁决，调用脚本时应尽量传入：
  - `--user-confirmed-fields`
  - `--council-advised-fields`
  - `--assistant-inferred-fields`
- 若未显式传入，脚本会按当前模式做保守默认归类，但这只是兜底，不应替代上游真实 provenance。

### 2) 写入 `idea_bank.json`

写入 `.webnovel/idea_bank.json`：

```json
{
  "selected_idea": {
    "title": "",
    "one_liner": "",
    "anti_trope": "",
    "hard_constraints": []
  },
  "constraints_inherited": {
    "anti_trope": "",
    "hard_constraints": [],
    "protagonist_flaw": "",
    "antagonist_mirror": "",
    "opening_hook": ""
  },
  "init_session": {
    "mode": "",
    "advisor_agents": [],
    "team_setup": {
      "team_mode": "",
      "shared_agents": [],
      "roles": {
        "planning": {"members": []},
        "production": {"members": []},
        "review": {"members": []}
      }
    },
    "research_policy": ""
  }
}
```

### 3) Patch 总纲

必须补齐：
- 故事一句话
- 核心主线 / 核心暗线
- 创意约束（反套路、硬约束、主角缺陷、反派镜像）
- 反派分层
- 关键爽点里程碑（2-3 条）

## 验证与交付

执行检查：

```bash
test -f "{project_root}/STATE.json"
test -f "{project_root}/TEAM.toml"
test -f "{project_root}/CHANGELOG.md"
test -f "{project_root}/.webnovel/state.json"
test -f "{project_root}/.webnovel/workflow_state.json"
test -f "{project_root}/.webnovel/execution_state.json"
test -f "{project_root}/.webnovel/task_log.jsonl"
test -f "{project_root}/Init/north_star_contract.json"
test -f "{project_root}/Init/初始化简报.json"
test -f "{project_root}/Init/访谈摘要.md"
test -f "{project_root}/Init/确认卡.md"
test -d "{project_root}/Planning/8-全息地图"
test -f "{project_root}/Planning/legacy/总纲.md"
test -f "{project_root}/.webnovel/idea_bank.json"
```

成功标准：
- `STATE.json` 已写入，且能指向 `.webnovel/state.json` 与关键初始化工件路径。
- `TEAM.toml` 已写入，且 `策划 / 监制 / 评审` 三阶段都按初始化已知信息落盘；仍缺失信息的阶段保留空模板。
- `CHANGELOG.md` 已写入，且包含本次初始化的首条标准记录。
- `state.json` 存在且关键字段不为空（title/genre/target_words/target_chapters）。
- `workflow_state.json / execution_state.json / task_log.jsonl` 已初始化，且不要求等到首个 drafting run 才出现。
- `Init/north_star_contract.json` 已写入，并作为初始化主文件承载故事核与总引领。
- `Init/初始化简报.json` 已写入，并默认采用 `north_star_ref + cards_seed + planning_seed + unknowns` 伴生结构。
- `north_star_contract.json / 初始化简报.json / state.json` 中均能追踪本次初始化的 `init_mode / team_setup / advisor_agents(legacy) / research_policy`。
- `Init/访谈摘要.md / Init/确认卡.md` 已写入，并只保留导航、边界和 unknowns，不重复正文设定。
- 新初始化默认不生成额外 `Init/*.md`；旧项目中的历史 `Init/*.md` 若存在，仅视为 seed / legacy-compat 材料，不替代 `Cards/**/*.json`。
- `Planning/8-全息地图/` 目录已预留，供 `2-Planning` 收敛正式 MAP。
- `总纲.md` 已填核心主线与约束字段，但仅作为 legacy 兼容骨架，不替代后续 MAP。
- `idea_bank.json` 已写入且与最终选定方案一致。

## 失败处理（最小回滚）

触发条件：
- 关键文件缺失；
- 总纲兼容骨架关键字段缺失；
- 约束启用但 `idea_bank.json` 缺失或内容不一致。

恢复流程：
1. 仅补缺失字段，不全量重问。
2. 仅重跑最小步骤：
   - 文件缺失 -> 重跑 `init_project.py`；
   - 总纲缺字段 -> 只 patch 总纲；
   - idea_bank 不一致 -> 只重写该文件。
3. 重新验证，全部通过后结束。

## Common Mistakes

- 把 Codex 当成 `AskUserQuestion` UI 来写：
  - 修复：所有问题都必须能通过普通文本消息直接发送和回答。
- 把“Codex 兼容”误解成只能一题一题问：
  - 修复：优先使用结构化问卷卡，保留接近表单的观感与效率。
- 在多个章节重复放置初始化元选项卡或再写一份 A/B/C 入口：
  - 修复：模式元选项只能在 `Initialization Mode Contract` 出现一次；其他章节只允许引用。
- 一次把所有字段都抛给用户：
  - 修复：严格分轮，先问当前最阻塞的 4-8 项。
- 用户自由描述后仍要求“按格式重填”：
  - 修复：助手先负责结构化回填，只对真正缺失字段补问。
- 创意包只让用户选字母，不回写内容：
  - 修复：最终落盘前必须把 A/B/C 方案展开成结构化约束。
- 顾问团模式只把 agent 名字写进提示词，却没有真实并行调度：
  - 修复：必须一位顾问一条 subagent 线程，并输出共识/分歧汇总。
- 智能顾问团模式或快速模式选定后，又继续走完整问卷：
  - 修复：这两种模式必须在 Step 0.6 直接走一次性内部任务，只允许 1 张必要裁决/阻塞卡。
- 快速模式把“偷懒”理解成“可以不标记推断项”：
  - 修复：快速模式更需要清楚区分 `user_confirmed` 与 `assistant_inferred`。
- 仍把初始化理解成“必须一次性问完角色、世界、规划细节”：
  - 修复：先锁 `project_contract`，再按需补 `cards_seed / planning_seed`，剩余问题进入 `unknowns`。
- handoff 简报仍是散装字段，没有显式路由给下游：
  - 修复：固定四段式 handoff，并标明 `deferred_to_cards / deferred_to_planning`。
