# 场景清单输出契约细则

## 单输出落点

- `projects/<项目名>/4-Design/1-场景/1-清单/第N集/第N集.json`
- `projects/<项目名>/4-Design/1-场景/1-清单/第N集/_manifest.json`（仅当本轮要求 `full_trace` 时）

## `第N集.json` 最低结构

1. `metadata`
2. `summary`
3. `scenes`
4. `group_scene_map`
5. `acceptance_notes`

## `scenes[]` 最低结构

1. `scene_id`
2. `scene_name`
3. `scene_key`
4. `first_appearance`
5. `coverage`
6. `variants`
7. `display_profile`

## `group_scene_map[]` 最低结构

1. `order`
2. `group_id`
3. `shot_id`
4. `scene_raw`
5. `scene_name`
6. `scene_variant`
7. `scene_key`
8. `time_range`

## 硬规则

1. `第N集.json` 是 canonical completeness carrier；结构完整性与下游消费能力都以此文件为准。
2. 当前模式只输出场景清单，不输出研究稿、设计稿或桥接稿。
3. `scene_name` 必须来自上游 `场景及方位` 的保守抽取，不得凭空研究补写。
4. `scene_variant` 只承接方位、门槛、边界、朝向等余量信息，不得改写主场景。
5. `group_scene_map[]` 必须能回链 `分镜组ID + 分镜ID`。
6. 同一 `scene_key` 的镜头必须聚合到同一 `scene_id`。
7. 当场景原句为空或无法成立时，允许写 `unknown`，但不得静默跳过该镜头。
8. 只有用户或父级显式要求时，才额外输出 `_manifest.json`。

## `_manifest.json` 最低要求

1. `episode_id`
2. `source_file`
3. `output_file`
4. `output_mode`
5. `scene_count`
6. `group_scene_count`
7. `scenes[].scene_id`
8. `scenes[].scene_name`
9. `scenes[].variant_count`
10. `scenes[].shot_count`
