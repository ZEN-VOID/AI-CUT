---
name: story-plan
governance_tier: full
description: |
  Use when story2026 needs whole-book planning passes, story_map rebuild, planning sequence repair, or source-layer fixes that must converge into `Planning/全息地图.json`.
tools: [Read, Write, Edit, Grep, Bash]
color: indigo
---

# 2-Planning

## Context Loading Contract

- 每次调用本技能时，必须同时加载同目录 `CONTEXT.md`。
- 本技能已从“单技能 + references 模块”重构为“父 skill + 7 个受治理子技能包 + shared story_map root”。
- 所有 planning 写入必须优先回读当前 `Planning/全息地图.json`；若 root 不存在，先用 shared bootstrap template 建立。

## Overview

`2-Planning` 现在是 `story2026` 的 planning 阶段父 skill。

它不再把 `references/*/module-spec.md` 当作执行主体，而是显式治理 7 个直接子技能包：

1. `1-题材选型`
2. `2-章节规划`
3. `3-故事大纲`
4. `4-冲突设计`
5. `5-任务设计`
6. `6-线索设计`
7. `7-伏笔设计`
新的 canonical 路线是：

1. 每个子技能只产出自己的 `story_map_patch`。
2. 父层按固定顺序 `1 -> 7` 串行 progressive commit 到 `Planning/全息地图.json`。
3. `Planning/全息地图.json` 是唯一规划真源，不再独立落盘 `Planning/1-7*.json`。
4. 父层最后只做 normalize / validate，不再额外调度独立“第 8 份产物”。

## Parent Positioning

### 父层拥有

- root bootstrap / root lock
- mode routing
- 7 个子技能的固定顺序门
- progressive commit 与 ownership gate
- 统一 story_map 写回
- 最终 normalize / validate / close

### 父层不拥有

- 替任一子技能重写领域判断
- 把 1-7 的证据层再压缩成“更顺的一篇大纲 prose”
- 越权修改子技能拥有的 `story_map` 槽位
- 跳过上游 child 直接补下游 child 的正式写入
- 在 `.agents/skills/story/2-Planning/` 根层维护 stage 私有 `templates/`

## Governed Child Skills

| order | child skill | 正式落盘 | owned story_map slots |
| --- | --- | --- | --- |
| 1 | `1-题材选型` | `Planning/全息地图.json` | `story_promise`、`genre_corridor`、题材导航规则 |
| 2 | `2-章节规划` | `Planning/全息地图.json` | `volume_boards`、`chapter_boards` skeleton、`episode_sequence_axis` |
| 3 | `3-故事大纲` | `Planning/全息地图.json` | `story_spine`、章节主干事件挂载 |
| 4 | `4-冲突设计` | `Planning/全息地图.json` | `conflict_threads`、章节冲突挂载 |
| 5 | `5-任务设计` | `Planning/全息地图.json` | `mission_threads`、章节任务挂载 |
| 6 | `6-线索设计` | `Planning/全息地图.json` | `clue_threads`、章节线索挂载 |
| 7 | `7-伏笔设计` | `Planning/全息地图.json` | `foreshadow_threads`、章节伏笔挂载 |

## Shared Canonical Sources

- `.agents/skills/story/_shared/story_map.schema.json`
- `.agents/skills/story/_shared/story_map_bootstrap.template.json`
- `.agents/skills/story/2-Planning/_shared/planning-branch-output-contract.md`
- `.agents/skills/story/2-Planning/scripts/validate_story_map_output.py`
- `1-题材选型/SKILL.md`
- `2-章节规划/SKILL.md`
- `3-故事大纲/SKILL.md`
- `4-冲突设计/SKILL.md`
- `5-任务设计/SKILL.md`
- `6-线索设计/SKILL.md`
- `7-伏笔设计/SKILL.md`

## Canonical Output Root

- `2-Planning` 的正式业务落盘根目录固定为 `projects/story/<项目名>/Planning/`
- 唯一规划真源固定为：
  - `projects/story/<项目名>/Planning/全息地图.json`
- `1-7` 子技能虽按顺序生成 patch，但不得各自再起 sibling JSON 作为平行真源。

## Template Layering Contract

`2-Planning` 根层不再维护 stage 私有 `templates/` 目录。

规则固定为：

1. 各 planning child 的 artifact 模板必须跟随各自子技能包落在本地 `templates/`。
2. 父层只保留 shared schema、bootstrap template、branch output contract 与 validator。
3. 若某模板只服务某一个 planning child，不得再上提回 `2-Planning/templates/`。
4. 若未来出现真正跨多个 planning child 复用的模板，应优先评估是否进入 `.agents/skills/story/_shared/`，而不是重新建立根层 `templates/`。

## Business Requirement Analysis Contract

| analysis_slot | 当前结论 |
| --- | --- |
| `business_goal` | 把整书 planning 从“8 份并列说明”升级为“7 个受治理子技能串行写入同一个 story_map carrier”，并保持 `projects/story/<项目名>/Planning/全息地图.json` 为唯一规划真源。 |
| `business_object` | `projects/story/<项目名>/0-Init/north_star.yaml`、`projects/story/<项目名>/0-Init/init_handoff.yaml`、`projects/story/<项目名>/Cards/**/*.json`、`projects/story/<项目名>/Planning/全息地图.json`。 |
| `constraint_profile` | 1-7 固定串行；后一 child 必须读取当前 root；1-7 只写自己的 owned patch；父层只做 normalize 与收束；下游继续 holomap-first。 |
| `success_criteria` | 任一 child 都能回答“我拥有 story_map 哪一段”；父层能 progressive commit；`Planning/全息地图.json` 同时具备题材、容器、主干、四条长线与三轴导航；validator 通过。 |
| `non_goals` | 不制造第二份 `story_map.json` 平行真源；不要求每个 child 各自维护一套独立大纲；不把 `references/*` 保留为隐式执行入口。 |
| `complexity_source` | 复杂度来自顺序依赖、story_map 槽位 ownership、progressive commit 连续性，以及 downstream holomap-first 兼容。 |
| `topology_fit` | 固定为 `input lock -> root bootstrap -> serial child dispatch -> progressive commit -> normalize -> validate -> close`。 |
| `step_strategy` | 父层只保留顺序门、写回门和验收门；领域思考与执行节点下沉到 7 个 child skills。 |

## Context Preload

1. 根 `AGENTS.md`
2. `.agents/skills/story/SKILL.md + CONTEXT.md`
3. 本 `SKILL.md + CONTEXT.md`
4. `.agents/skills/story/_shared/story_map.schema.json`
5. `.agents/skills/story/_shared/story_map_bootstrap.template.json`
6. `.agents/skills/story/2-Planning/_shared/planning-branch-output-contract.md`
7. `0-Init/north_star.yaml`
8. `0-Init/init_handoff.yaml`
9. `Cards/**/*.json`
10. 当前 `Planning/全息地图.json`（若存在）
11. `1-题材选型/SKILL.md + CONTEXT.md`
12. `2-章节规划/SKILL.md + CONTEXT.md`
13. `3-故事大纲/SKILL.md + CONTEXT.md`
14. `4-冲突设计/SKILL.md + CONTEXT.md`
15. `5-任务设计/SKILL.md + CONTEXT.md`
16. `6-线索设计/SKILL.md + CONTEXT.md`
17. `7-伏笔设计/SKILL.md + CONTEXT.md`

## Total Input Contract

### 必需输入

- `0-Init/north_star.yaml`
- `0-Init/init_handoff.yaml`
- `Cards/**/*.json`

### 可选输入

- 当前 `Planning/全息地图.json`
- `STATE.json`
- `team.yaml`（若项目存在）

### 硬规则

1. `Planning/全息地图.json` 存在时，必须把它当当前 story_map root 回读。
2. 若 root 缺失，必须先建立 bootstrap root，再进入 Step 1。
3. 任一 child 开始前，都必须重新读取当前 root，而不是复用前一步缓存。
4. 任一 child 只允许写自己的 owned `story_map_patch`。
5. 只有父层允许补齐三轴、cross-thread index、lifecycle 和 normalize 结构。

## Dispatch Order Contract

### 固定顺序

`1-题材选型 -> 2-章节规划 -> 3-故事大纲 -> 4-冲突设计 -> 5-任务设计 -> 6-线索设计 -> 7-伏笔设计 -> 父层 normalize/validate`

### 当前 root 回读规则

1. 每个 child 开始前，必须重新读取当前 `Planning/全息地图.json`。
2. 该 root 必须已经包含前序 child 审核通过并写回的 patch。
3. 后序 child 可以把当前 root 当一致性上下文，但不得改写前序 owned slots。

### 并发规则

- 正式写回：禁止并发。
- 允许并发的只有单个 child 内部的候选比较、团队会诊或草案探索。
- 任意时刻只允许一个 child 对 story_map 执行正式 progressive commit。

## Output Contract

### canonical root

- `projects/story/<项目名>/Planning/全息地图.json`

### hard rules

1. 1-7 child 只返回 `story_map_patch`，不独立落盘 sibling JSON。
2. `Planning/全息地图.json` 必须保持 `content.holomap` 兼容入口。
3. 父层 normalize 后的 root 必须兼容 `query / 3-Drafting / 5-Loopback` 的 holomap-first 读取。

## Visual Maps

```mermaid
flowchart TD
    A["N1 Input Lock"] --> B["N2 Root Bootstrap"]
    B --> C["N3 Serial Child Dispatch"]
    C --> D["N4 Progressive Commit"]
    D --> E["N5 Normalize"]
    E --> F["N6 Validate"]
    F --> G["Close"]
```

```mermaid
flowchart TD
    A["Child n starts"] --> B["Read current story_map root"]
    B --> C["Run child skill and generate evidence artifact"]
    C --> D["Review owned slots"]
    D --> E{"target_json_paths overlap?"}
    E -- "Yes" --> F["Block and return fail code"]
    E -- "No" --> G["Commit patch to root"]
    G --> H["Next child rereads refreshed root"]
```

```mermaid
graph LR
    A["1-题材选型"] --> R["story_map root"]
    B["2-章节规划"] --> R
    C["3-故事大纲"] --> R
    D["4-冲突设计"] --> R
    E["5-任务设计"] --> R
    F["6-线索设计"] --> R
    G["7-伏笔设计"] --> R
    R --> X["3-Drafting / query / resume / 5-Loopback"]
```

## Thinking-Action Network

| node_id | field_id | objective | actions | evidence | route_out | gate |
| --- | --- | --- | --- | --- | --- | --- |
| `N1-INPUT-LOCK` | `FIELD-PL-01` | 锁定本轮输入真源与任务模式 | 读取 Init/Cards/Planning 现状 | `input_lock_note` | -> `N2` | 输入齐备 |
| `N2-ROOT-BOOTSTRAP` | `FIELD-PL-02` | 建立或回读唯一 story_map root | 读取或生成 bootstrap root | `root_bootstrap_note` | -> `N3` | root 唯一 |
| `N3-SERIAL-DISPATCH` | `FIELD-PL-03` | 按顺序运行 7 个 child skills | 每步先回读当前 root，再调度 child | `dispatch_log` | -> `N4` | 固定顺序成立 |
| `N4-PROGRESSIVE-COMMIT` | `FIELD-PL-04` | 把 child patch 写回 root | 校验 ownership、写回 patch、刷新 root | `commit_trace` | -> `N5` | 不越权、不冲突 |
| `N5-NORMALIZE` | `FIELD-PL-05` | 由父层收束三轴与导航结构 | 补齐 three-axis、cross-thread、lifecycle | `normalize_note` | -> `N6` | root 可消费 |
| `N6-VALIDATE` | `FIELD-PL-06` | 校验最终 root | 运行 validator，自检 fail codes | `validation_verdict` | pass -> done | validator 通过 |

## Field Master

| field_id | output_slot | 内容要求 | default_step | quality_dimension | fail_code |
| --- | --- | --- | --- | --- | --- |
| `FIELD-PL-01` | 输入锁定 | Init/Cards/Planning 真源齐备 | `S1` | 输入稳定性 | `FAIL-PL-01` |
| `FIELD-PL-02` | root bootstrap | story_map root 唯一且可回读 | `S1` | 真源唯一性 | `FAIL-PL-02` |
| `FIELD-PL-03` | serial dispatch | 7 个 child 串行顺序成立 | `S2` | 顺序完整性 | `FAIL-PL-03` |
| `FIELD-PL-04` | progressive commit | child 只写 owned slots | `S3-S7` | ownership 一致性 | `FAIL-PL-04` |
| `FIELD-PL-05` | normalized story_map | 三轴、chapter boards、threads 成立 | `S8` | 收束质量 | `FAIL-PL-05` |
| `FIELD-PL-06` | validation verdict | validator 通过且下游可消费 | `S8` | 可交付性 | `FAIL-PL-06` |

## Thought Pass Map

| step_id | 聚焦字段 | 核心问题 | 生成动作 | 未达标信号 |
| --- | --- | --- | --- | --- |
| `S1` | `FIELD-PL-01~02` | 本轮输入齐了吗，root 是否唯一 | 锁输入并 bootstrap root | root 缺失或多真源 |
| `S2` | `FIELD-PL-03` | child 顺序是否固定且可执行 | 生成 dispatch run list | 仍尝试并行正式写回 |
| `S3-S7` | `FIELD-PL-04` | 当前 child 是否只写自己的槽位 | 逐 child commit patch | overlap 或越权 |
| `S8` | `FIELD-PL-05~06` | 父层是否把 root 收束为可消费 story_map | normalize + validate | holomap 仍像摘要 |

## Pass Table

| field_id | pass_standard | fail_code | rework_entry |
| --- | --- | --- | --- |
| `FIELD-PL-01` | 输入真源齐备 | `FAIL-PL-01` | `S1` |
| `FIELD-PL-02` | root 唯一且可回读 | `FAIL-PL-02` | `S1` |
| `FIELD-PL-03` | child 串行顺序成立 | `FAIL-PL-03` | `S2` |
| `FIELD-PL-04` | progressive commit 无 overlap | `FAIL-PL-04` | 对应 child |
| `FIELD-PL-05` | root 收束完成 | `FAIL-PL-05` | `S8` |
| `FIELD-PL-06` | validator 通过 | `FAIL-PL-06` | `S8` |

## Root-Cause Execution Contract

出现以下任一情况，必须先修源层：

- 仍从 `references/*` 直调旧模块
- child 未回读当前 root 就继续写入
- 两个 child 命中同一路径
- 父层 normalize 越权重写 1-7 的领域判断
- story_map root 丢失 `content.holomap` 兼容入口

## Completion Contract

只有同时满足以下条件，`2-Planning` 才允许宣布完成：

1. 1-7 child patch 已完成 progressive commit。
2. `Planning/全息地图.json` 已完成父层 normalize。
3. validator 通过。
4. story_map 仍可被下游 holomap-first 消费。
