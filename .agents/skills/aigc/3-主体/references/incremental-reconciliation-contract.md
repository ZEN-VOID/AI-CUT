# Incremental Reconciliation Contract

本文件定义 `3-主体` 场景、角色、道具三域在分批上游、既有产物和命名漂移之间做增量对账时的共享合同。它只展开对账细则，不替代父级或叶子 `SKILL.md` 的 runtime spine、输出合同或 LLM-first 主创门禁。

## Scope

- 适用对象：`subject-registry.yaml` 新增/更新、已有清单/设计/生成产物存在、`8-分组` 后置 reconciliation 发现别名或命名漂移。
- 输出性质：`reconcile_delta`、保护清单、返工目标和 sidecar manifest patch。
- 禁止用途：不得批量重写 canonical 清单、设计稿、prompt 或生成资产；不得把 `8-分组` 中的新名称直接晋升为主体真源。

## Reconciliation Rules

| rule_id | rule | evidence | fail_code |
| --- | --- | --- | --- |
| `IR-01` | 先读取当前 `subject-registry.yaml` 与对应域既有 canonical 输出，再判断新增、更新、别名或缺口。 | registry source anchors、existing output list | `FAIL-INCREMENTAL-SOURCE` |
| `IR-02` | 新主体只能追加到对应清单或待设计队列，不得重排既有编号或改写已验收主体名称。 | protected asset list、append-only delta | `FAIL-INCREMENTAL-OVERWRITE` |
| `IR-03` | 发现下游使用 alias 时归一到 registry canonical name，并记录 normalization；未登记主体必须返工到 `3-主体` 注册表或对应清单。 | normalization map、unregistered subject list | `FAIL-INCREMENTAL-UNREGISTERED` |
| `IR-04` | 若清单通过但设计或生成缺失，只返工最早缺口叶子，不回写父级总览正文。 | earliest-gap decision、leaf rework target | `FAIL-INCREMENTAL-GAP-ROUTE` |
| `IR-05` | 所有归并、边界裁决、主体重要性判断和创作型修复必须由 LLM 逐条判断；脚本只做机械对账和格式检查。 | LLM decision note、script boundary report | `FAIL-INCREMENTAL-SCRIPTED` |

## Review Gate Mapping

| review_question | review_gate | fail_code | rework_target | report_evidence |
| --- | --- | --- | --- | --- |
| 是否先保护既有 canonical 输出，再处理新增或漂移？ | `GATE-INCREMENTAL-PROTECT` | `FAIL-INCREMENTAL-OVERWRITE` | 对应域 `domain_reconcile` 节点 | protected asset list、append-only delta |
| 未登记主体是否返工到注册表或对应清单，而不是在下游临时补名？ | `GATE-INCREMENTAL-REGISTRY` | `FAIL-INCREMENTAL-UNREGISTERED` | 父级 `N2-PACKET` 或对应 `1-清单` | unregistered subject list |
| 对账是否只生成 delta 和返工目标，没有机械生成创作正文？ | `GATE-INCREMENTAL-LLM-FIRST` | `FAIL-INCREMENTAL-SCRIPTED` | 对应叶子 LLM-first 节点 | script boundary report、LLM decision note |
