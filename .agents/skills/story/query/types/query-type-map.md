# Query Type Map

## 类型包加载边界

- 每次调用本技能时，必须依据本文件识别并加载同目录 `types/` 中选中的类型包（单选或多选）。
- `types/` 中命中的类型包作为固定上下文加载；`knowledge-base/` 只作为按需检索、切片或向量召回的知识库，不替代类型包。


本文件集中维护 `$story-query` 的查询类型变量、信号矩阵和真源映射。

## Type Variables

| variable | values |
| --- | --- |
| `truth_role` | `planned`、`current`、`history`、`validated_actual`、`quality`、`execution`、`manual_spec`、`conflict_diagnosis` |
| `source_scope` | `planning`、`cards`、`state`、`index`、`actualization`、`context_return`、`review_metrics`、`workflow_runtime`、`manual_tag_spec` |
| `answer_confidence` | `high`、`medium`、`low` |
| `evidence_level` | `path_only`、`field_hit`、`cross_checked`、`validation_backed` |

## Signal Matrix

| user signal | truth_role | canonical source | review gate |
| --- | --- | --- | --- |
| 原计划、哪章安排、落在哪章、章节编排 | `planned` | `2-卷章规划/整体规划.md`、`第V卷/卷规划.md`、`第N章.md` | 不能只读 `STATE.json` 或 compat MAP |
| 当前、现在、默认状态、持有、地点、境界 | `current` | `1-设定/**/*.json` 的 `current_state` | 不能把 `core` 当当前态 |
| 怎么变成、经历、成长、关系演化 | `history` | `experience_timeline`、`history`、`index.db state_changes / relationship_events` | 必须同时说明现在与形成过程 |
| 已经发生、实际兑现、最终推进到哪 | `validated_actual` | planning actualization sidecars + `context-return/*.context-return.json` + validation evidence | 无 PASS 证据时只能说未见 validated actual |
| 伏笔、紧急度、静默区、回收窗口 | `quality` | chapter planning foreshadowing + status reporter + `STATE.json.plot_threads.foreshadowing` | 不能只读老式伏笔列表 |
| 节奏、追读力、评分、风险 | `quality` | `index.db.review_metrics`、`reading_power`、`STATE.json.review_checkpoints` | 不能只凭主观总结 |
| run、执行态、卡住、断点、恢复点、task log | `execution` | `STATE.json.workflow_runtime.execution_state`、`task_log`、workflow CLI | `workflow_state` 只作兼容断点 |
| 关系图谱、最近出场、状态变化证据 | `history` | `index.db` + Cards / STATE 辅证 | 不能只扫 Markdown |
| XML、标签、手动补标 | `manual_spec` | `references/tag-specification.md` | 不进入普通剧情查询 |
| 计划和实际不一致、来源冲突 | `conflict_diagnosis` | 对应各 truth layer | 必须列出来源优先级 |

## Canonical Carrier Map

| truth_role | primary carrier | secondary carrier | fallback |
| --- | --- | --- | --- |
| `planned` | `2-卷章规划/整体规划.md`、`第V卷/卷规划.md`、`第N章.md` | Cards | `全息地图.json`、`卷分片/*.json` |
| `current` | `1-设定/**/*.json.current_state` | `STATE.json`、`index.db` | none |
| `history` | Cards `experience_timeline/history` | `index.db state_changes / relationship_events` | summaries |
| `validated_actual` | actualization sidecars + `context-return/*.context-return.json` | `validation_ref`、`review_metrics`、`review_checkpoints` | MAP actualization compat |
| `quality` | `index.db.review_metrics`、`reading_power` | `status_reporter.py`、`STATE.json.review_checkpoints` | none |
| `execution` | `workflow status/list-runs/detect` | `STATE.json.workflow_runtime` | `workflow_state` compat only |
| `manual_spec` | `references/tag-specification.md` | none | none |

## Source Priority Rules

- `planned` 和 `validated_actual` 冲突时，不合并为单一事实；分栏回答。
- `Cards.core` 只回答对象本体定义，`Cards.current_state` 才回答当前默认有效状态。
- `STATE.json` 是快照，`index.db` 是证据层；二者都不能改写 Cards 或 planning 真源。
- compat MAP / holomap 只在三层 planning 缺失或用户明确要求时读取，并必须标注兼容回退。
