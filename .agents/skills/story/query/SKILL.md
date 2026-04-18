---
name: story-query
description: Use when story2026 needs factual retrieval about cards, MAP planning, runtime state, validated actualization, relationships, foreshadow urgency, or review metrics in an existing novel project.
governance_tier: lite
allowed-tools: Read Grep Bash
---

# story2026 Query

## Context Loading Contract

- 每次调用本技能时，必须同时加载同目录 `CONTEXT.md`。
- `CONTEXT.md` 只承载查询层的 truth-role 经验与避坑启发，不得覆盖本 `SKILL.md` 的主真源判定。
- 若查询经验与当前数据流合同冲突，以本 `SKILL.md` 与相关 shared reference 为准。

## Purpose

- `query/` 是 `story2026` 的运行时信息查询层，也是 `5-Loopback` 的卫星技能之一。
- 它的职责不是“看到关键词就 grep 一圈”，而是先判断用户问的是哪一种 truth，再去对应真源取证。
- 它默认服务已有项目，不负责改写规划、回写卡片、修正文稿或替代 `resume/`、`5-Loopback` 的 actualization 主流程。

一句话裁决：

- `MAP` 回答“原计划如何编排”。
- `Cards` 回答“对象长期是什么、当前怎样、经历如何演化”。
- `STATE/index` 回答“当前运行态和索引证据是什么”。
- `workflow_runtime` 回答“当前跑到哪、最近哪个 run 卡住、恢复点在哪里”。
- `actualization + loopback` 回答“哪些计划已经被 PASS 后正式兑现”。
- `review_metrics` 回答“质量与风险最近怎样”。

## Stage Position

`query/` 必须与 `0-Init -> 1-Cards -> 2-Planning -> 3-Drafting -> 4-Validation -> review -> 5-Loopback` 的最新链路对齐。

核心约束：

1. 不得把 `planned_state` 当成 `actualized truth`。
2. 不得把 `Cards.core` 当成“当前默认有效状态”。
3. 不得把 `STATE.json` 当成唯一真源。
4. 不得把 XML 标签规范当成普通故事查询的主入口。
5. 若用户问“已经发生了吗 / 现在怎样了 / 最终推进到哪”，必须显式区分：
   - `planned`
   - `current`
   - `validated_actual`

## Project Root Guard（必须先确认）

- 工作区根目录不一定等于真实书项目根目录。
- 必须先解析真实 `PROJECT_ROOT`；该目录必须包含 `STATE.json`。
- 禁止在 `.agents/skills/story` 技能包目录里冒充书项目查询业务数据。

环境设置（bash 命令执行前）：

```bash
export WORKSPACE_ROOT="${CLAUDE_PROJECT_DIR:-$PWD}"
export REPO_ROOT="${CLAUDE_PROJECT_DIR:-$PWD}"
export SKILL_ROOT="${REPO_ROOT}/.agents/skills/story/query"
export SCRIPTS_DIR="${REPO_ROOT}/.agents/skills/story/scripts"

if [ ! -d "${SKILL_ROOT}" ]; then
  echo "ERROR: 缺少目录: ${SKILL_ROOT}" >&2
  exit 1
fi

if [ ! -d "${SCRIPTS_DIR}" ]; then
  echo "ERROR: 缺少目录: ${SCRIPTS_DIR}" >&2
  exit 1
fi

export PROJECT_ROOT="$(python3 "${SCRIPTS_DIR}/story.py" --project-root "${WORKSPACE_ROOT}" where)"
python3 "${SCRIPTS_DIR}/story.py" --project-root "${WORKSPACE_ROOT}" preflight --format json
```

## Workflow Checklist

Copy and track progress:

```text
信息查询进度：
- [ ] Step 0: 解析 project_root 并完成 preflight
- [ ] Step 1: 识别查询属于哪种 truth role
- [ ] Step 2: 按需加载参考文件
- [ ] Step 3: 读取主真源与辅助证据
- [ ] Step 4: 如有现成 CLI，走快速查询
- [ ] Step 5: 做 planned/current/actual 交叉校验
- [ ] Step 6: 结构化输出结果、证据和冲突点
```

## Truth Role Decision（Mandatory）

先判定用户问的是哪一种 truth，而不是先猜文件。

| 问题形状 | 主真源 | 辅助真源 | 禁止偷懒 |
|---|---|---|---|
| “原计划哪章发生 / 这条线原本怎么排” | `2-Planning/全息地图.json` 的 `chapter_boards / cross_thread_indexes / planned_state` | `2-Planning/1-7/*.json` 追溯 | 不能只读 `STATE.json` |
| “现在谁持有 / 当前关系 / 当前地点 / 当前默认状态” | `1-Cards/**/*.json` 的 `current_state` | `STATE.json`、`index.db` | 不能把 `core` 当当前态 |
| “这个人是怎么变成现在的 / 这段关系怎么演化的” | `角色卡.experience_timeline + history` | `index.db state_changes / relationship_events` | 不能只给当前快照 |
| “这件事实际上已经发生了吗 / 最终在哪集兑现了” | `全息地图.actualization` + `5-Loopback` artifact | `validation_ref / review_metrics / STATE.json.review_checkpoints` | 不能用 `planned_state` 冒充已发生 |
| “这条伏笔还活着吗 / 紧急度怎样 / 静默区是否过长” | `全息地图` + `7-伏笔设计` 结果 + `status_reporter` | `STATE.json.plot_threads.foreshadowing` | 不能只读老式伏笔列表 |
| “最近质量如何 / 哪些风险在抬头” | `index.db.review_metrics` / `reading_power` | `STATE.json.review_checkpoints` | 不能只凭主观总结 |
| “当前跑到哪 / 最近哪个 stage 卡住 / 最新 run / 恢复点在哪” | `STATE.json.workflow_runtime.execution_state / task_log` | `workflow_state`、`workflow status/list-runs` | 不能只看 `workflow_state.current_task` |
| “关系图谱 / 某角色最近出场 / 状态变化证据” | `index.db` | `Cards` / `STATE.json` | 不能只扫 Markdown |
| “XML 标签怎么写 / 手动补标规范” | `references/tag-specification.md` | 无 | 不能把它当普通剧情查询入口 |

固定裁决：

- `计划问题` 优先问 `MAP`。
- `对象问题` 优先问 `Cards`。
- `运行态问题` 优先问 `STATE.json + index.db`。
- `执行态问题` 优先问 `STATE.json.workflow_runtime.execution_state + task_log`。
- `是否已正式发生` 优先问 `actualization + loopback + validation PASS`。

## Reference Loading Levels（strict, lazy）

- L0：未识别 truth role 前，不加载参考。
- L1：所有查询默认只加载基础数据流规范。
- L2：仅按问题类型补加载专题参考。

### L1（minimum）

- [system-data-flow.md](references/system-data-flow.md)

### L2（conditional by query type）

- 伏笔紧急度 / 静默区 / 回收窗口：
  - [foreshadowing.md](references/advanced/foreshadowing.md)
- Strand / 节奏结构 / 章节织线：
  - [strand-weave-pattern.md](../_shared/strand-weave-pattern.md)
- 手动标签 / XML 兼容查询：
  - [tag-specification.md](references/tag-specification.md)

禁止默认一次性加载全部 L2 文件。

## Step 1：识别查询类型

| 查询信号 | 查询类型 | 主读取层 |
|---|---|---|
| 角色、人物、配角、别名、身份、关系 | 对象 / 关系查询 | `Cards + index.db` |
| 当前、现在、默认状态、持有、地点、境界 | 当前态查询 | `Cards.current_state + STATE.json` |
| 怎么变成、经历、成长、一路、时间线 | 历程查询 | `experience_timeline + history + state_changes` |
| 原计划、哪章安排、落在哪章、编排、章节板 | 规划查询 | `MAP planned_state` |
| 实际、已经发生、兑现了没、最后在哪集 | 实绩查询 | `MAP actualization + loopback artifact` |
| 伏笔、紧急度、静默区、回收、兑现窗口 | 伏笔查询 | `伏笔设计 + MAP + status_reporter` |
| 节奏、Strand、追读力、评分、风险 | 质量/节奏查询 | `status_reporter + index review_metrics` |
| run、执行态、卡住、断点、恢复点、最近任务、心跳、task log | 执行态查询 | `workflow_runtime.execution_state + task_log` |
| 标签、XML、手动标注 | 规范查询 | `tag-specification.md` |

若一句话同时命中多个类型，先回答主问题，再补次要问题；不要把多种 truth 混成一个来源。

## Step 2：加载参考文件

所有查询默认读取：

```bash
cat "${SKILL_ROOT}/references/system-data-flow.md"
```

伏笔类问题额外读取：

```bash
cat "${SKILL_ROOT}/references/advanced/foreshadowing.md"
```

Strand / 节奏类问题额外读取：

```bash
cat "${SKILL_ROOT}/../_shared/strand-weave-pattern.md"
```

仅当用户明确问标签/手动补标时读取：

```bash
cat "${SKILL_ROOT}/references/tag-specification.md"
```

## Step 3：按 truth role 读取主真源

### A. 规划查询

```bash
cat "$PROJECT_ROOT/2-Planning/全息地图.json"
```

如需追溯某条规划为何这样安排，再补读对应 `2-Planning/1-7/*.json`。

### B. 对象 / 当前态 / 历程查询

先按对象名称或别名定位相关 card：

```bash
python3 "${SCRIPTS_DIR}/story.py" --project-root "$PROJECT_ROOT" index get-by-alias --alias "{keyword}"
python3 "${SCRIPTS_DIR}/story.py" --project-root "$PROJECT_ROOT" index get-entity --id "{entity_id}"
python3 "${SCRIPTS_DIR}/story.py" --project-root "$PROJECT_ROOT" index get-state-changes --entity "{entity_id}" --limit 20
```

然后补读正式 card JSON，优先看：

- `core`
- `current_state`
- `history`
- `experience_timeline`（角色）

### C. 实绩 / validated actual 查询

必须同时检查：

1. `2-Planning/全息地图.json` 的 `content.holomap.actualization`
2. `5-Loopback/第N集.loopback.json`
3. `validation_ref` / `review_metrics` / `review_checkpoints`

可用下面的命令定位 loopback artifact：

```bash
rg --files "$PROJECT_ROOT/Loopback" | rg '\\.loopback\\.json$'
```

如缺 `actualization` 或缺 loopback artifact，只能回答“尚无 validated actual evidence”，不能擅自把计划当结果。

### D. 质量 / 节奏 / 风险查询

快速入口：

```bash
python3 "${SCRIPTS_DIR}/story.py" --project-root "$PROJECT_ROOT" status -- --focus urgency
python3 "${SCRIPTS_DIR}/story.py" --project-root "$PROJECT_ROOT" status -- --focus strand
python3 "${SCRIPTS_DIR}/story.py" --project-root "$PROJECT_ROOT" index get-recent-review-metrics --limit 5
python3 "${SCRIPTS_DIR}/story.py" --project-root "$PROJECT_ROOT" index get-review-trend-stats --last-n 5
python3 "${SCRIPTS_DIR}/story.py" --project-root "$PROJECT_ROOT" index get-recent-reading-power --limit 5
```

### E. 关系 / 图谱 / 时间窗查询

```bash
python3 "${SCRIPTS_DIR}/story.py" --project-root "$PROJECT_ROOT" index get-relationships --entity "{entity_id}"
python3 "${SCRIPTS_DIR}/story.py" --project-root "$PROJECT_ROOT" index get-relationship-graph --center "{entity_id}" --depth 2 --format mermaid
python3 "${SCRIPTS_DIR}/story.py" --project-root "$PROJECT_ROOT" index get-relationship-timeline --a "{entity_a}" --b "{entity_b}"
python3 "${SCRIPTS_DIR}/story.py" --project-root "$PROJECT_ROOT" index entity-appearances --entity "{entity_id}" --limit 20
```

### F. 执行态 / run / 恢复点查询

优先读取全阶段执行态，再用兼容断点补充：

```bash
python3 "${SCRIPTS_DIR}/story.py" --project-root "$PROJECT_ROOT" workflow status --format json
python3 "${SCRIPTS_DIR}/story.py" --project-root "$PROJECT_ROOT" workflow list-runs --limit 10 --format json
python3 "${SCRIPTS_DIR}/story.py" --project-root "$PROJECT_ROOT" workflow detect
```

解释规则：

- `execution_state`
  - 回答“最近有哪些 run、各 stage 最新状态是什么、最新 resume point 在哪”。
- `task_log`
  - 回答“最近发生了哪些心跳、失败、清理、重入事件”。
- `workflow_state`
  - 只回答“当前兼容断点指针长什么样”，不能单独冒充全阶段执行真源。

## Step 4：交叉校验规则（Mandatory）

以下冲突必须显式拆开，而不是混着回答：

1. `planned` 与 `validated_actual`
   - 计划写在 `planned_state`
   - 已验证实绩写在 `actualization / loopback`
2. `core` 与 `current_state`
   - 本体定义写在 `core`
   - 当前默认有效状态写在 `current_state`
3. `事件时间` 与 `经历时间`
   - `MAP` 是事件叙事中心
   - `experience_timeline` 是角色经历叙事中心
4. `STATE.json` 快照 与 `index.db` 证据
   - `STATE.json` 更像运行快照
   - `index.db` 更像细粒度索引与证据层
5. `workflow_state` 与 `execution_state/task_log`
   - `workflow_state` 更像当前 run 的兼容断点
   - `execution_state + task_log` 才是全阶段执行真源与事件链

若多个来源冲突，必须在输出中显式写：

- 哪个来源说了什么
- 哪个来源按当前合同优先
- 哪个来源可能过期或缺回写

## Step 5：输出合同

默认输出格式：

```markdown
# 查询结果：{用户问题}

## 类型判定
- truth_role: {planned/current/validated_actual/quality/manual-spec/...}
- truth_role: {planned/current/validated_actual/quality/execution/manual-spec/...}
- 主真源: {source}
- 辅助证据: {source}

## 结论
- {直接回答用户问题}

## 证据
- `{source_a}`: {命中的字段/对象/章节}
- `{source_b}`: {补充或校验信息}

## 边界与冲突
- {若计划与实绩不一致，必须写出}
- {若数据不足，也必须写出}
```

输出要求：

- 能直接回答用户问题。
- 能区分“计划 / 当前 / 已验证实绩”。
- 能指出主真源和辅助证据。
- 若证据不足，必须说清缺口，而不是补猜。

## Quick Reference

| 查询目标 | 快速入口 |
|---|---|
| 解析项目根 | `python3 "${SCRIPTS_DIR}/story.py" --project-root "${WORKSPACE_ROOT}" where` |
| 环境预检 | `python3 "${SCRIPTS_DIR}/story.py" --project-root "${WORKSPACE_ROOT}" preflight --format json` |
| 伏笔紧急度 | `python3 "${SCRIPTS_DIR}/story.py" --project-root "$PROJECT_ROOT" status -- --focus urgency` |
| Strand 节奏 | `python3 "${SCRIPTS_DIR}/story.py" --project-root "$PROJECT_ROOT" status -- --focus strand` |
| 别名找实体 | `python3 "${SCRIPTS_DIR}/story.py" --project-root "$PROJECT_ROOT" index get-by-alias --alias "{name}"` |
| 实体状态变化 | `python3 "${SCRIPTS_DIR}/story.py" --project-root "$PROJECT_ROOT" index get-state-changes --entity "{entity_id}" --limit 20` |
| 关系图谱 | `python3 "${SCRIPTS_DIR}/story.py" --project-root "$PROJECT_ROOT" index get-relationship-graph --center "{entity_id}" --depth 2 --format mermaid` |
| 最近评分趋势 | `python3 "${SCRIPTS_DIR}/story.py" --project-root "$PROJECT_ROOT" index get-review-trend-stats --last-n 5` |
| workflow 状态快照 | `python3 "${SCRIPTS_DIR}/story.py" --project-root "$PROJECT_ROOT" workflow status --format json` |
| 最近 run 列表 | `python3 "${SCRIPTS_DIR}/story.py" --project-root "$PROJECT_ROOT" workflow list-runs --limit 10 --format json` |

## Root-Cause 执行合同

- 若查询结果与下游事实冲突，必须按 `Symptom -> Direct Cause -> Rule Source -> Meta Rule Source` 上溯。
- `Rule Source` 默认优先检查：
  - 当前 `query/SKILL.md`
  - `query/references/system-data-flow.md`
  - `2-Planning/SKILL.md`
  - `2-Planning/_shared/planning-branch-output-contract.md`
  - `1-Cards/SKILL.md`
  - `5-Loopback/SKILL.md`
- `Meta Rule Source` 默认上溯到仓库 `AGENTS.md` 与相关 meta skill。
- 修复顺序必须是：先修 truth-role 判定或数据流合同，再修本次回答。

## Lite Tier Field Mapping（Combined）

| field_id | step_id | intent | required_output | fail_code | rework_entry |
|---|---|---|---|---|---|
| FIELD-QRY-ROOT-01 | Step 0 | 解析真实项目根并确认规划源状态 | `PROJECT_ROOT`、preflight 结果 | FAIL-QRY-ROOT-01 | 回到 root guard，重新解析项目根 |
| FIELD-QRY-ROLE-02 | Step 1 | 判断用户问的是哪一种 truth | `truth_role`、主真源判定 | FAIL-QRY-ROLE-02 | 回到 truth role 判定，拆开计划/当前/实绩 |
| FIELD-QRY-SOURCE-03 | Step 2-3 | 按需读取最小真源集合 | 主真源内容、辅助证据 | FAIL-QRY-SOURCE-03 | 回到最小读取层，补主真源或删错读文件 |
| FIELD-QRY-CHECK-04 | Step 4 | 明确 planned/current/actual 的关系 | 冲突说明、优先级说明 | FAIL-QRY-CHECK-04 | 回到交叉校验，禁止混答 |
| FIELD-QRY-ANSWER-05 | Step 5 | 产出可追溯答案 | 结论、证据、边界/缺口 | FAIL-QRY-ANSWER-05 | 重写输出，补 source 与不确定性 |

## Completion Gate

- 已确认真实 `PROJECT_ROOT`。
- 已明确本次问题属于哪一种 truth role。
- 已读取最小必要真源，而非盲目全量灌入。
- 已区分 `planned / current / validated_actual`。
- 输出中已写明主真源、辅助证据与边界说明。
