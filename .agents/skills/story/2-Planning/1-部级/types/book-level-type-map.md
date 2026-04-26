# Book-Level Type Map

本文件提供部级规划的轻量类型矩阵。它只决定执行分支，不替代 `steps/` 的节点网络。

## Type Profile

| variable | allowed values | meaning |
| --- | --- | --- |
| `request_type` | `create`、`revise`、`audit`、`repair` | 本轮用户意图 |
| `artifact_state` | `missing`、`partial`、`complete`、`drifted` | `整体规划.md` 当前状态 |
| `input_strength` | `seed_only`、`typed`、`card_rich`、`memory_rich` | 上游输入充分度 |
| `revision_scope` | `whole_file`、`field_patch`、`rhythm_only`、`handoff_only` | 修订范围 |
| `review_type` | `checklist`、`subagent_reviewer`、`parent_gate` | 审查方式 |

## Mapping Matrix

| type signal | step impact | reference impact | review impact |
| --- | --- | --- | --- |
| `request_type=create` | 从 `N1-INPUT-LOCK` 串行执行到 `N9-REVIEW` | 加载全部必需 references 与模板 | 完整 review gate |
| `request_type=revise` + `revision_scope=field_patch` | 先回读旧稿，只进入命中字段节点，再汇流 review | 只加载命中字段 reference | 检查 diff 是否越界 |
| `request_type=audit` | 不改写规划，只执行 review flow | 加载 output/rhythm contract | 输出 findings 和 verdict |
| `artifact_state=partial` | 从缺失字段对应节点补齐 | 加载对应字段 contract | 缺失字段必须转为 pass |
| `artifact_state=drifted` | 先定位漂移层，再回到节点修复 | 加载 `CONTEXT.md` 与 knowledge-base | 检查是否恢复 planning-only |

## Default Profile

```yaml
domain_type: story
artifact_type: markdown
execution_type: llm-first
topology_type: serial_with_field_patch_branch
review_type: checklist_or_subagent_reviewer
output_type: book_level_plan
```

## Anti-Patterns

- 不要因为用户只要求“补节奏”就跳过旧稿回读。
- 不要在 `audit` 模式下顺手改写正文，除非用户要求修复。
- 不要把 `input_strength=seed_only` 误当成可以生成精密卷职责；输入不足时应明确标注假设或追问。
