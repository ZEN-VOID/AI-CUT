# Character Generation Type Map

## 类型包加载边界

- 每次调用本技能时，必须依据本文件识别并加载同目录 `types/` 中选中的类型包（单选或多选）。
- `types/` 中命中的类型包作为固定上下文加载；`knowledge-base/` 只作为按需检索、切片或向量召回的知识库，不替代类型包。


本文件承载 `角色/3-生成` 的类型变量、模式矩阵和分型策略。

## Type Profile Fields

| field | values | meaning |
| --- | --- | --- |
| `scope` | `single_character` / `batch_from_designs` | 单角色或批量从设计文档执行 |
| `execution_mode` | `real_generation` / `prompt_only` / `review_only` | 是否真实调用 imagegen |
| `rerun_policy` | `skip_existing` / `version_existing` / `overwrite_allowed` | 已有产物处理策略 |
| `source_state` | `ready` / `missing_design` / `missing_prompt_section` | 上游设计文档状态 |
| `reference_state` | `none` / `main_image_ready` / `main_image_missing` | 多视图参照图状态 |
| `reference_context_status` | `pending_view_image` / `visible_in_conversation_context` / `no_reference_image` | 本地主图参照是否已通过 `view_image` 进入上下文 |

## Routing Matrix

| type_id | trigger | route | required references | review focus |
| --- | --- | --- | --- | --- |
| `CHAR-GEN-SINGLE` | 用户指定单个角色 | 只读取该角色设计文档并执行 Step1/Step2 | main template、multiview template | 单角色来源与命名 |
| `CHAR-GEN-BATCH` | 用户指定项目但未限制角色 | 遍历 `2-设计/*.md`，每个角色独立闭环 | workflow、review | 批量隔离和缺项报告 |
| `CHAR-GEN-PROMPT-ONLY` | imagegen 不可用或用户 dry-run | 只写 JSON prompt 和不可用说明 | templates | 不伪造图片路径 |
| `CHAR-GEN-REPAIR` | JSON 缺失、图片缺失、命名不符 | 最小范围重写 JSON 或重跑图片 | workflow、review | 不覆盖未授权产物 |
| `CHAR-GEN-REVIEW` | 用户只要求检查 | 不生图，只审查现有产物 | review | 路径、JSON、参照图、上游回链 |

## Strategy Notes

- `batch_from_designs` 只调度实际存在且被选中的设计文档；不得为了结构完整性补空角色。
- `prompt_only` 是阻断或 dry-run 模式，不是完成生图。
- `overwrite_allowed` 必须来自用户明确要求；否则默认 `skip_existing` 或 `version_existing`。
- 多视图永远消费对应角色主图，不跨角色复用参照图；真实生成模式下主图必须先 `view_image`，再进入 built-in `image_gen`。
