# Character Generation Type Map

## 类型包加载边界

- 每次调用本技能时，必须依据本文件识别并加载同目录 `types/` 中选中的类型包（单选或多选）。
- `types/` 中命中的类型包作为固定上下文加载；`knowledge-base/` 只作为按需检索、切片或向量召回的知识库，不替代类型包。


本文件承载 `角色/3-生成` 的类型变量、模式矩阵和分型策略。

## Type Profile Fields

| field | values | meaning |
| --- | --- | --- |
| `scope` | `single_character` / `batch_from_designs` | 单角色或批量从设计文档执行 |
| `execution_mode` | `real_generation` / `prompt_only` / `review_only` | 是否真实调用 libTV |
| `canvas_resolution` | `resolved` / `ambiguous` / `missing` | 是否已按项目名-集数解析唯一 libTV 画布 UUID |
| `model_resolution` | `midjourney_v8_1_resolved` / `lib_image_resolved` / `missing` | 普通新主体解析 Midjourney V8.1；状态变体解析 Lib Image |
| `midjourney_suffix` | `--ar 9:16 --hd --style raw` plus optional style preset | 角色图固定后缀，风格预设来自 `../../_shared/midjourney风格参数.yaml` |
| `asset_reuse_decision` | `generate_new_subject` / `reuse_existing_asset` / `upload_existing_asset` / `generate_state_variant` | 生成前对项目 `3-主体` 既有主体图的判定 |
| `canvas_action` | `create_new_node` / `node_already_present` / `uploaded_existing_image_to_canvas` | 当前 libTV 画布中的节点处理动作 |
| `local_sync_status` | `already_present` / `synced` / `copied` / `pending` / `failed` | 项目 `角色/3-生成` 是否已有同 stem 本地资产；`already_present` 表示本地 canonical 已有并跳过下载/复制 |
| `local_asset_path` | canonical project image path / empty | 画布节点下载或本地复制后的项目侧最终资产路径 |
| `download_command` | `libtv download -p <canvas_uuid> -n <node> -o <dir>` / empty / `not_applicable` | 仅下载分支必填；本地 canonical 已有或复制分支可为空或 `not_applicable` |
| `generation_model_policy` | `new_subject_midjourney_default` / `lib_image_state_variant` | 普通新主体与状态变体的模型策略 |
| `state_variant_suffix` | empty / file-safe state suffix | 同主体新状态才填写，并加入输出 stem |
| `base_reference_node_name` | empty / same-subject libTV image node name | 状态变体使用的既有同主体参考节点 |
| `rerun_policy` | `skip_existing` / `version_existing` / `overwrite_allowed` | 已有产物处理策略 |
| `source_state` | `ready` / `missing_design` / `missing_prompt_section` | 上游设计文档状态 |
| `reference_state` | `none` / `main_image_ready` / `main_image_missing` | 历史参照图状态；默认不触发多视图 |
| `reference_context_status` | `disabled_multiview` / `no_reference_image` | 多视图已取消；reference 状态不再作为完成门 |

## Routing Matrix

| type_id | trigger | route | required references | review focus |
| --- | --- | --- | --- | --- |
| `CHAR-GEN-SINGLE` | 用户指定单个角色 | 只读取该角色设计文档并执行主图生成 | main template | 单角色来源与命名 |
| `CHAR-GEN-BATCH` | 用户指定项目但未限制角色 | 遍历 `2-设计/*.md`，每个角色独立主图闭环 | workflow、review | 批量隔离和缺项报告 |
| `CHAR-GEN-PROMPT-ONLY` | libTV 不可用或用户 dry-run | 只写 JSON prompt 和不可用说明 | templates | 不伪造图片路径 |
| `CHAR-GEN-REUSE` | 同主体同状态已有本地或画布主体图 | 跳过生成，必要时上传到当前画布 | shared reuse rule、review | 不重复生成 |
| `CHAR-GEN-STATE-VARIANT` | 同主体出现服装、年龄、受伤、战斗前后等新状态 | 使用 Lib Image 和参考图生成带状态后缀变体 | shared reuse rule、review | 不用 Midjourney 重生变体 |
| `CHAR-GEN-REPAIR` | JSON 缺失、图片缺失、命名不符 | 最小范围重写 JSON 或重跑图片 | workflow、review | 不覆盖未授权产物 |
| `CHAR-GEN-REVIEW` | 用户只要求检查 | 不生图，只审查现有产物 | review | 路径、主图 JSON、上游回链和多视图取消合同 |

## Strategy Notes

- `batch_from_designs` 只调度实际存在且被选中的设计文档；不得为了结构完整性补空角色。
- `prompt_only` 是阻断或 dry-run 模式，不是完成生图。
- `overwrite_allowed` 必须来自用户明确要求；否则默认 `skip_existing` 或 `version_existing`。
- 生成前必须扫描 `projects/aigc/<项目名>/3-主体`。同主体同状态已有图时优先复用或上传，不进入 Midjourney 新生成。
- 任一集 libTV 画布上的角色主体图生成、复用或上传成功后，都必须确保 `projects/aigc/<项目名>/3-主体/角色/3-生成/` 已有同 stem 本地资产；本地 canonical 已有则跳过下载/复制并记录 `already_present`，本地缺失才下载或复制补齐；真实生成分支的 `local_sync_status` 不能停留在 `pending` 或空值。
- 同主体新状态必须填写 `state_variant_suffix`、`base_reference_node_name`，并把 `generation_model_policy` 设为 `lib_image_state_variant`。
- 多视图默认取消；不得把 reference 缺失当作 generation gap 或 review failure。
- 真实生成前必须先解析 `canvas_uuid` 与 Midjourney V8.1 `model_key`；无法解析时只能进入 `prompt_only`，不得切换到其他 provider。
