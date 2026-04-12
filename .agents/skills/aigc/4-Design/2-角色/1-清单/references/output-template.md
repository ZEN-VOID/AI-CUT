# Output Template

## 文件列表

### `角色清单.json`

- `meta`
  - `schema_version`
  - `skill_id`
  - `source_schema`
  - `episode_id`
  - `project_name`
  - `source_file`
  - `generated_at`
- `statistics`
  - `group_count`
  - `shot_count`
  - `role_count`
  - `unknown_shot_count`
- `group_role_map[]`
  - `group_id`
  - `shot_id`
  - `shot_scene`
  - `role_text`
  - `roles[]`
  - `costume_mentions`
  - `source_file`
- `roles[]`
  - `role_id`
  - `name`
  - `role_level`
  - `group_ids[]`
  - `shot_ids[]`
  - `first_appearance`
  - `costume_profile`
  - `display_card`
  - `evidence[]`

### `_manifest.json`

- `status`
- `episode_id`
- `input_file`
- `output_dir`
- `output_files[]`
- `statistics`
- `notes[]`

## 验收面

- `角色清单.json.roles[]` 非空。
- `group_role_map[]` 的每项都带 `group_id + shot_id + source_file`。
- `unknown_shot_count` 可解释，且不会吞掉全部镜头。
- `_manifest.json.statistics.role_count` 与主清单一致。
