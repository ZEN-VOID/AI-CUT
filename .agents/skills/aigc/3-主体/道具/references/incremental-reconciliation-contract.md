# Prop Incremental Reconciliation Contract

本文件是 `3-主体/道具` 域内的增量对账细则。它只展开组根和叶子 `SKILL.md` 已声明的 `domain_reconcile / incremental_merge / incremental_fill` 节点，不新增第二入口或第二完成门。

## Scope

- 对账对象：`subject-registry.yaml` 的 `subjects.props`、既有 `1-清单/道具清单.md`、`2-设计/*.md`、`3-生成/*-主图.*`、`3-生成/*-多视图.*` 与 `design-manifest.yaml`。
- 目标：保护既有清单、设计稿、生成资产和别名映射，只处理新增、变更或缺口主体。
- 禁止：静默全量覆盖、静默重命名、把状态词当新道具、用脚本自动裁决归并/设计/prompt。

## Reconcile Delta

`reconcile_delta` 至少记录：

| field | requirement |
| --- | --- |
| `new_registry_props` | 新增 registry prop id/name/source anchors |
| `changed_registry_props` | 名称、source anchor、首次登场或描述变更 |
| `alias_candidates` | 可能指向既有清单/设计稿的别名或状态称呼 |
| `protected_assets` | 不得覆盖的清单、设计稿、主图、多视图和 JSON |
| `list_gaps` | 需要回到 `1-清单` 的候选或错误 |
| `design_gaps` | 需要回到 `2-设计` 的缺设计稿主体 |
| `generation_gaps` | 需要回到 `3-生成` 的缺主图、多视图或 JSON |

## Review Gate Mapping

| Review Question | Review Gate | Fail Code | Rework Target | Report Evidence |
| --- | --- | --- | --- | --- |
| 新增/变更道具是否先与既有清单和设计稿对账？ | reconciliation | `FAIL-PROP-RECONCILE-SKIP` | 组根 `G5-RECONCILE` 或叶子增量节点 | `reconcile_delta` |
| 是否保护既有设计稿和生成资产？ | asset_protection | `FAIL-PROP-RECONCILE-OVERWRITE` | 对应叶子 worklist/scope 节点 | `protected_assets` |
| 是否把状态变化误判为新道具？ | alias_state_check | `FAIL-PROP-RECONCILE-STATE-DUP` | `1-清单` LLM 归并节点 | `alias_candidates` 与裁决理由 |
| 脚本是否只做对账枚举和格式检查？ | llm_first | `FAIL-PROP-RECONCILE-SCRIPT` | 命中叶子 LLM-first 节点 | 脚本职责与 LLM 裁决证据 |
