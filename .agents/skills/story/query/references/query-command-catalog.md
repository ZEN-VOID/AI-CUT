---
name: query-command-catalog
purpose: `$story-query` 读取 story 项目事实载体时使用的只读命令目录
---

# Query Command Catalog

本文件只保存可复核的只读命令和 carrier 读取提示。执行节点、路由、gate 与完成标准以 `SKILL.md` 的 `Thinking-Action Node Map` 为唯一真源。

## Project Root Guard

```bash
export WORKSPACE_ROOT="${CLAUDE_PROJECT_DIR:-$PWD}"
export REPO_ROOT="${CLAUDE_PROJECT_DIR:-$PWD}"
export SCRIPTS_DIR="${REPO_ROOT}/.agents/skills/story/scripts"

python3 "${SCRIPTS_DIR}/story.py" --project-root "${WORKSPACE_ROOT}" preflight --format json
export PROJECT_ROOT="$(python3 "${SCRIPTS_DIR}/story.py" --project-root "${WORKSPACE_ROOT}" where)"
```

Hard gates:

- `PROJECT_ROOT` must be a `projects/story/<项目名>/` project root, not the repository root or a skill directory.
- `PROJECT_ROOT` must contain `STATE.json`.
- Multiple candidates require clarification before reading business evidence.
- `planning_source=legacy_fallback` must be reported as degraded mode.

## Planning

Prefer current planning truth:

```bash
cat "$PROJECT_ROOT/2-卷章/整体规划.md"
cat "$PROJECT_ROOT/2-卷章/第V卷/卷规划.md"
cat "$PROJECT_ROOT/2-卷章/第V卷/第N章.md"
```

Compatibility fallback:

- `2-卷章/全息地图.json`
- `2-卷章/卷分片/*.json`
- `2-卷章/legacy/`

Fallback evidence must never be presented as canonical planning truth.

## Cards / Current / History

```bash
python3 "${SCRIPTS_DIR}/story.py" --project-root "$PROJECT_ROOT" index get-by-alias --alias "{keyword}"
python3 "${SCRIPTS_DIR}/story.py" --project-root "$PROJECT_ROOT" index get-entity --id "{entity_id}"
python3 "${SCRIPTS_DIR}/story.py" --project-root "$PROJECT_ROOT" index get-state-changes --entity "{entity_id}" --limit 20
```

Read emphasis:

- `core`
- `current_state`
- `history`
- `experience_timeline`

`core` defines long-term identity; `current_state` answers the current default state.

## Validated Actual

Required evidence classes:

1. `2-卷章/整体规划.actualization.json`
2. `2-卷章/第V卷/卷规划.actualization.json`
3. `2-卷章/第V卷/第N章.actualization.json`
4. `context-return/第V卷.context-return.json`
5. `validation_ref` / `review_metrics` / `STATE.json.review_checkpoints`

Locate context-return artifacts:

```bash
rg --files "$PROJECT_ROOT/context-return" | rg '\.context-return\.json$'
```

If actualization or context-return evidence is missing, answer with an explicit validated-actual gap.

## Quality / Risk

```bash
python3 "${SCRIPTS_DIR}/story.py" --project-root "$PROJECT_ROOT" status -- --focus urgency
python3 "${SCRIPTS_DIR}/story.py" --project-root "$PROJECT_ROOT" status -- --focus strand
python3 "${SCRIPTS_DIR}/story.py" --project-root "$PROJECT_ROOT" index get-recent-review-metrics --limit 5
python3 "${SCRIPTS_DIR}/story.py" --project-root "$PROJECT_ROOT" index get-review-trend-stats --last-n 5
python3 "${SCRIPTS_DIR}/story.py" --project-root "$PROJECT_ROOT" index get-recent-reading-power --limit 5
```

## Relationships / Evidence Windows

```bash
python3 "${SCRIPTS_DIR}/story.py" --project-root "$PROJECT_ROOT" index get-relationships --entity "{entity_id}"
python3 "${SCRIPTS_DIR}/story.py" --project-root "$PROJECT_ROOT" index get-relationship-graph --center "{entity_id}" --depth 2 --format mermaid
python3 "${SCRIPTS_DIR}/story.py" --project-root "$PROJECT_ROOT" index get-relationship-timeline --a "{entity_a}" --b "{entity_b}"
python3 "${SCRIPTS_DIR}/story.py" --project-root "$PROJECT_ROOT" index entity-appearances --entity "{entity_id}" --limit 20
```

## Execution / Run / Resume Point

```bash
python3 "${SCRIPTS_DIR}/story.py" --project-root "$PROJECT_ROOT" workflow status --format json
python3 "${SCRIPTS_DIR}/story.py" --project-root "$PROJECT_ROOT" workflow list-runs --limit 10 --format json
python3 "${SCRIPTS_DIR}/story.py" --project-root "$PROJECT_ROOT" workflow detect
```

Interpretation:

- `execution_state` answers recent runs, stage state and latest resume point.
- `task_log` answers heartbeat, failure, cleanup and re-entry events.
- `workflow_state` only answers current run compatibility pointers.

## Cross-Check Rules

The final answer must split these conflicts instead of merging them:

- `planned` vs `validated_actual`
- `core` vs `current_state`
- event time vs experience time
- `STATE.json` snapshot vs `index.db` evidence
- `workflow_state` vs `execution_state/task_log`

## Review Gate Mapping

| Review Question | Review Gate | Fail Code | Rework Target | Report Evidence |
| --- | --- | --- | --- | --- |
| 只读命令是否服务 `SKILL.md` 节点，而不是定义第二执行链？ | 出现独立 node network、完成门或输出合同即失败 | `FAIL-QRY-MODULE-DRIFT` | `SKILL.md` Thinking-Action Node Map | command catalog audit |
| 命令是否只读且不写业务真源？ | 出现写入 STATE/Cards/planning/index 的命令即失败 | `FAIL-QRY-SOURCE` | `scripts/README.md` / 本文件 | command list |
| execution 查询是否区分 `workflow_state` 与 `execution_state/task_log`？ | 把兼容断点当全阶段执行真源即失败 | `FAIL-QRY-LAYER-MIX` | 本文件 Execution section | execution evidence split |
