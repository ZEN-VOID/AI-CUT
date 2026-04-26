# Type Map

## Mode Matrix

| mode | trigger | required inputs | writes images | review focus |
| --- | --- | --- | --- | --- |
| `prompt_only` | 用户只要 prompt / 配置 / 参照绑定 | 项目名、集号或分镜范围 | no | prompt 字数、north_star 直引、参照路径 |
| `single_shot_generate` | 单个四段式 `分镜ID` 出图 | 项目名、`shot_id` | yes | 单镜追溯、输出命名 |
| `episode_batch_generate` | 整集批量出图 | 项目名、集号 | yes | 批量计划、失败汇流 |
| `shot_batch_generate` | 多个指定分镜出图 | 项目名、`shot_id[]` | yes | 多镜范围与独立输出 |
| `repair` | 已有输出漂移或失败 | 目标文件或分镜范围 | maybe | 最小返工 |
| `review_only` | 只审查现有输出 | 目标目录 | no | gate verdict |

## Input Type Variables

| variable | values | effect |
| --- | --- | --- |
| `scope_type` | `single_shot` / `shot_list` / `episode` / `all_ready_episodes` | 决定 shot index 范围 |
| `execution_type` | `prompt_only` / `generate` | 决定是否进入 imagegen handoff |
| `reference_state` | `full` / `partial` / `none` | 决定槽位是否写路径或留空 |
| `source_state` | `complete_groups` / `missing_groups` / `ambiguous_shot` | 决定执行或阻断 |
| `handoff_route` | `built_in_image_gen` / `cli_confirmed` | 决定 imagegen 调用方式 |

## Routing Rules

1. 用户只说“生成提示词”时，默认 `prompt_only`。
2. 用户说“生成图片 / 生图 / 调用 imagegen”时，默认 `generate`，但仍先过 prompt 与参照审查。
3. 用户给 `第N集` 且无具体 `分镜ID` 时，默认整集批量。
4. 用户给多个四段式 ID 时，默认 `shot_batch_generate`。
5. 只有三段式 `1-1-1` 时，默认指向整个分镜组，需要拆出组内全部镜级 ID；若用户意图是单镜，需追问或从上下文唯一定位。
