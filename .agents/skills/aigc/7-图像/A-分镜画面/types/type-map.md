# Type Map

## 类型包加载边界

- 每次调用本技能时，必须依据本文件识别并加载同目录 `types/` 中选中的类型包（单选或多选）。
- `types/` 中命中的类型包作为固定上下文加载；`knowledge-base/` 只作为按需检索、切片或向量召回的知识库，不替代类型包。


## Mode Matrix

| mode | trigger | required inputs | writes images | review focus |
| --- | --- | --- | --- | --- |
| `prompt_only` | 用户只要 prompt / 配置 / 参照绑定 | 项目名、集号或分镜范围 | no | prompt 字数、north_star 直引、场景视觉风格锁、参照路径 |
| `single_shot_generate` | 单个四段式 `分镜ID` 出图 | 项目名、`shot_id` | yes | 单镜追溯、输出命名 |
| `episode_batch_generate` | 整集批量出图 | 项目名、集号 | yes | 完整 prompts 文档前置、批量计划、失败汇流 |
| `shot_batch_generate` | 多个指定分镜出图 | 项目名、`shot_id[]` | yes | 指定范围完整 prompts 文档前置、多镜范围与独立输出 |
| `repair` | 已有输出漂移或失败 | 目标文件或分镜范围 | maybe | 最小返工 |
| `review_only` | 只审查现有输出 | 目标目录 | no | gate verdict |

## Input Type Variables

| variable | values | effect |
| --- | --- | --- |
| `scope_type` | `single_shot` / `shot_list` / `episode` / `all_ready_episodes` | 决定 shot index 范围 |
| `execution_type` | `prompt_only` / `generate` | 决定是否进入 imagegen handoff |
| `reference_state` | `full` / `partial` / `none` | 决定槽位是否写路径或留空 |
| `scene_visual_style_lock_state` | `visible_in_conversation_context` / `scene_reference_missing` / `pending_view_image` | 决定 prompt 组织是否已用场景参照图锁定画面风格、光影、色调和氛围 |
| `previous_frame_context_state` | `scene_first_shot` / `visible_in_conversation_context` / `not_same_scene` / `previous_image_missing` / `previous_shot_not_generated` | 决定 prompt 组织是否必须消费同场景上一生成图的空间站位和走位约束 |
| `spatial_continuity_state` | `space_model_ready` / `needs_reverse_shot_axis` / `insufficient_spatial_evidence` | 决定 prompt 组织是否已具备 3D 空间模型、正反打轴线和角色移动轨迹 |
| `prompt_package_state` | `complete_before_imagegen` / `incomplete` / `not_applicable` | 决定生成模式是否允许进入 imagegen；批量生成必须为 `complete_before_imagegen` |
| `batch_execution_state` | `serial_by_shot_id` | 批量生成第二阶段唯一合法执行形态；不得并发、后台并行、分片并跑、边生图边补 prompt 或跳过前镜结果 |
| `source_state` | `complete_groups` / `missing_groups` / `ambiguous_shot` | 决定执行或阻断 |
| `handoff_route` | `built_in_image_gen` / `cli_confirmed` | 决定 imagegen 调用方式 |

## Routing Rules

1. 用户只说“生成提示词”时，默认 `prompt_only`。
2. 用户说“生成图片 / 生图 / 调用 imagegen”时，默认 `generate`，但仍先为指定范围生成完整 prompts 文档、manifest、plan，并过 prompt 与参照审查。
3. 用户给 `第N集` 且无具体 `分镜ID` 时，默认整集批量。
4. 用户给多个四段式 ID 时，默认 `shot_batch_generate`。
5. 只有三段式 `1-1-1` 时，默认指向整个分镜组，需要拆出组内全部镜级 ID；若用户意图是单镜，需追问或从上下文唯一定位。
