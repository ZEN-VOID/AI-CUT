# Type Package Map

`types/` 保存 `aigc-image-storyboard-frame` 的类型策略和子类型知识包。任务需要分型时，先选择命中的类型包，再形成 `type_profile` 供 `SKILL.md` 的 `Thinking-Action Node Map` 消费。

`knowledge-base/` 另走标准知识库模式：按需检索、切片、向量召回或关键词召回，不作为固定上下文全量加载。

## Package Index

| package_id | path | match_signals | load_mode | context_files | conflicts_with | inherits_from |
| --- | --- | --- | --- | --- | --- | --- |
| `group-multi-image` | `types/group-multi-image/group-multi-image.md` | 三段式 group_id、四段式 shot_id、imagegen 多图、生成多张单独分镜画面 | default | `types/group-multi-image/group-multi-image.md` | none | none |

## Default Package Rule

- 默认加载 `group-multi-image`，因为本技能的业务对象固定为 `8-分组` 普通分镜组。
- 用户给四段式 `shot_id` 时仍回溯到所属 `group_id`，继续使用 `group-multi-image`。
- `prompt_only`、`single_group_generate`、`episode_group_generate`、`group_batch_generate`、`repair` 与 `review_only` 都使用同一类型包，不拆出第二类型真源。

## Loading Flow

1. 收集用户输入、项目根、集号、`group_id` / `shot_id`、生成或审查意图。
2. 选择 `group-multi-image` 类型包。
3. 加载 `types/group-multi-image/group-multi-image.md` 作为固定上下文。
4. 回到 `SKILL.md` 的 `N1-INTAKE` 到 `N10-CLOSE` 节点消费 `type_profile`。
5. 如果 `SKILL.md` 授权 `knowledge-base/`，再按需检索外部资料；思行节点和 Mermaid 执行拓扑仍以主入口 `SKILL.md` 为准。

## Mode Matrix

| mode | trigger | required inputs | writes images | review focus |
| --- | --- | --- | --- | --- |
| `prompt_only` | 用户只要 prompt / manifest / plan | 项目名、集号、`group_id` 或范围 | no | 完整组稿、shot_count、非拼图前缀、主体参照 |
| `single_group_generate` | 指定一个 `group_id` 或组内 `shot_id` 出图 | 项目名、目标组 | yes | 一组一个 group imagegen package、`expected_image_count == shot_count`、输出映射 |
| `episode_group_generate` | 整集批量出图 | 项目名、集号 | yes | 每个普通组一个 group imagegen package，连接件跳过 |
| `group_batch_generate` | 多个指定分镜组出图 | 项目名、`group_id[]` | yes | 多组范围、逐组 task、失败汇流 |
| `repair` | 已有输出漂移或失败 | 目标文件或 group scope | maybe | 最小返工 |
| `review_only` | 只审查现有输出 | 目标目录或文件 | no | gate verdict |

## Input Type Variables

| variable | values | effect |
| --- | --- | --- |
| `scope_type` | `single_group` / `group_list` / `episode` / `shot_id_back_to_group` | 决定 group index 范围 |
| `execution_type` | `prompt_only` / `generate` / `review_only` | 决定是否进入 imagegen handoff |
| `group_source_state` | `complete_group_block` / `missing_group` / `connector_only` / `ambiguous_group` | 决定执行或阻断 |
| `shot_count_state` | `valid` / `zero` / `ambiguous` | 决定 `expected_image_count` 和是否阻断 |
| `aspect_ratio_state` | `default_16_9` / `explicit_9_16` / `explicit_other` | 决定 prompt 和 plan 的画面比例；未显式指定时固定 16:9 |
| `reference_state` | `full` / `partial` / `none` / `pending_view_image` | 决定生成是否可执行或 `pass_with_todo` |
| `multi_image_prompt_state` | `ready` / `missing_prefix` / `missing_image_section` / `collage_risk` | 决定是否允许进入 handoff |
| `consistency_state` | `ready` / `needs_spatial_axis` / `needs_character_lock` / `insufficient_evidence` | 决定是否返工 prompt |
| `handoff_route` | `imagegen_group_package` / `prompt_only` / `blocked_imagegen_batch` | 决定执行路径 |
| `result_mapping_state` | `matched` / `count_mismatch` / `collage_output` / `missing_file` | 决定结果是否 pass |

## Anti-Patterns

- 不要让四段式 `shot_id` 请求绕过 group 多图任务单位。
- 不要把 `types/` 变成 prompt 模板或 review gate 真源。
- 不要把 imagegen 并发、输出路径或 completion gate 只写在类型包里。
