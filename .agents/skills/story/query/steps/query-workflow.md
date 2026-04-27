# Query Workflow

`$story-query` 的步骤必须同时表达判断、动作、证据和失败回路。

## Node Network

| node_id | input | judgment | action | output | fail route |
| --- | --- | --- | --- | --- | --- |
| `N0-load-contract` | 用户查询 | 是否命中 `$story-query` | 加载 `SKILL.md + CONTEXT.md` | loaded contract | missing context -> report baseline gap |
| `N1-project-root` | cwd、用户路径、项目名 | 是否唯一定位项目根 | 运行 project root guard 与 preflight | `project_root_lock` | multiple candidates -> ask project name |
| `N2-truth-role` | 用户问题 | 主 truth role 是哪类 | 查 `types/query-type-map.md` | `type_profile` | ambiguous -> split primary/secondary |
| `N3-reference-load` | `type_profile` | 哪些 reference 必要 | 读取 L1 与条件 L2 | `reference_pack` | missing ref -> report contract gap |
| `N4-carrier-read` | `type_profile` | 哪些 carrier 有资格回答 | 读 canonical carrier | `evidence_pack` | carrier missing -> legacy fallback or gap |
| `N5-cross-check` | `evidence_pack` | 是否混淆计划/当前/实绩 | 拆分 truth layers | `truth_distinction` | conflict -> report each source |
| `N6-review-gate` | answer draft | 是否有证据和边界 | 执行 review checklist | `verdict` | fail -> return to missing node |
| `N7-answer` | all evidence | 输出是否覆盖四字段 | 按模板输出 | final answer | incomplete -> return to missing node |

## Project Root Guard

环境设置（bash 命令执行前）：

```bash
export WORKSPACE_ROOT="${CLAUDE_PROJECT_DIR:-$PWD}"
export REPO_ROOT="${CLAUDE_PROJECT_DIR:-$PWD}"
export SKILL_ROOT="${REPO_ROOT}/.agents/skills/story/query"
export SCRIPTS_DIR="${REPO_ROOT}/.agents/skills/story/scripts"

python3 "${SCRIPTS_DIR}/story.py" --project-root "${WORKSPACE_ROOT}" preflight --format json
export PROJECT_ROOT="$(python3 "${SCRIPTS_DIR}/story.py" --project-root "${WORKSPACE_ROOT}" where)"
```

硬门槛：

- `PROJECT_ROOT` 必须包含 `STATE.json`。
- 若当前目录位于 `.agents/skills/story` 下，不能把技能目录冒充项目根。
- 多候选时停止追问，不能把多个项目的证据混答。
- 若 `planning_source=legacy_fallback`，必须明确标注 degraded mode。

## Reference Loading Levels

- L0：未识别 truth role 前，不加载专题参考。
- L1：所有查询默认读取 `references/system-data-flow.md`。
- L2：仅按问题类型补加载专题参考。

L2 条件：

- 伏笔紧急度 / 静默区 / 回收窗口：`references/advanced/foreshadowing.md`
- Strand / 节奏结构 / 章节织线：`../_shared/strand-weave-pattern.md`
- 手动标签 / XML 兼容查询：`references/tag-specification.md`

## Carrier Read Rules

### Planning

优先读取：

```bash
cat "$PROJECT_ROOT/2-卷章/整体规划.md"
cat "$PROJECT_ROOT/2-卷章/第V卷/卷规划.md"
cat "$PROJECT_ROOT/2-卷章/第V卷/第N章.md"
```

兼容项目再补读 `2-卷章/全息地图.json` 与 `2-卷章/卷分片/*.json`。

### Cards / Current / History

先用 alias 或实体 ID 定位对象，再读取正式 card JSON：

```bash
python3 "${SCRIPTS_DIR}/story.py" --project-root "$PROJECT_ROOT" index get-by-alias --alias "{keyword}"
python3 "${SCRIPTS_DIR}/story.py" --project-root "$PROJECT_ROOT" index get-entity --id "{entity_id}"
python3 "${SCRIPTS_DIR}/story.py" --project-root "$PROJECT_ROOT" index get-state-changes --entity "{entity_id}" --limit 20
```

读取重点：

- `core`
- `current_state`
- `history`
- `experience_timeline`

### Validated Actual

必须检查：

1. `2-卷章/整体规划.actualization.json`
2. `2-卷章/第V卷/卷规划.actualization.json`
3. `2-卷章/第V卷/第N章.actualization.json`
4. `context-return/第V卷.context-return.json`
5. `validation_ref` / `review_metrics` / `STATE.json.review_checkpoints`

定位 context-return artifact：

```bash
rg --files "$PROJECT_ROOT/context-return" | rg '\\.context-return\\.json$'
```

若缺 actualization 或 context-return artifact，只能回答“尚无 validated actual evidence”。

### Quality / Risk

```bash
python3 "${SCRIPTS_DIR}/story.py" --project-root "$PROJECT_ROOT" status -- --focus urgency
python3 "${SCRIPTS_DIR}/story.py" --project-root "$PROJECT_ROOT" status -- --focus strand
python3 "${SCRIPTS_DIR}/story.py" --project-root "$PROJECT_ROOT" index get-recent-review-metrics --limit 5
python3 "${SCRIPTS_DIR}/story.py" --project-root "$PROJECT_ROOT" index get-review-trend-stats --last-n 5
python3 "${SCRIPTS_DIR}/story.py" --project-root "$PROJECT_ROOT" index get-recent-reading-power --limit 5
```

### Relationships / Evidence Windows

```bash
python3 "${SCRIPTS_DIR}/story.py" --project-root "$PROJECT_ROOT" index get-relationships --entity "{entity_id}"
python3 "${SCRIPTS_DIR}/story.py" --project-root "$PROJECT_ROOT" index get-relationship-graph --center "{entity_id}" --depth 2 --format mermaid
python3 "${SCRIPTS_DIR}/story.py" --project-root "$PROJECT_ROOT" index get-relationship-timeline --a "{entity_a}" --b "{entity_b}"
python3 "${SCRIPTS_DIR}/story.py" --project-root "$PROJECT_ROOT" index entity-appearances --entity "{entity_id}" --limit 20
```

### Execution / Run / Resume Point

```bash
python3 "${SCRIPTS_DIR}/story.py" --project-root "$PROJECT_ROOT" workflow status --format json
python3 "${SCRIPTS_DIR}/story.py" --project-root "$PROJECT_ROOT" workflow list-runs --limit 10 --format json
python3 "${SCRIPTS_DIR}/story.py" --project-root "$PROJECT_ROOT" workflow detect
```

解释规则：

- `execution_state` 回答“最近有哪些 run、各 stage 最新状态是什么、最新 resume point 在哪”。
- `task_log` 回答“最近发生了哪些心跳、失败、清理、重入事件”。
- `workflow_state` 只回答“当前兼容断点指针长什么样”。

## Cross-Check Rules

以下冲突必须显式拆开：

- `planned` 与 `validated_actual`
- `core` 与 `current_state`
- `事件时间` 与 `经历时间`
- `STATE.json` 快照与 `index.db` 证据
- `workflow_state` 与 `execution_state/task_log`

若多个来源冲突，输出必须写明：

- 哪个来源说了什么
- 哪个来源按当前合同优先
- 哪个来源可能过期或缺回写
