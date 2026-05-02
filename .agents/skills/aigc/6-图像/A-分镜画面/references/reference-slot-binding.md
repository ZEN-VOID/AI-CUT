# Reference Slot Binding Contract

本文件定义 step3：检查角色、场景、道具生成目录，给分镜 prompt 的空槽位绑定本地图片参照。

## Search Roots

固定检查以下目录：

```text
projects/aigc/<项目名>/5-设计/角色/3-生成
projects/aigc/<项目名>/5-设计/场景/3-生成
projects/aigc/<项目名>/5-设计/道具/3-生成
```

## Image Priority

对每个主体名称：

1. 进行图片参照时，如有 `<主体名称>-多视图.png`、`.jpg`、`.jpeg`、`.webp` 可选，必须优先绑定多视图。
2. 只有多视图图片不存在时，才选择 `<主体名称>-主图.png`、`.jpg`、`.jpeg`、`.webp`。
3. 若只有 JSON 而无真实图片文件，不视为可绑定图片。
4. 若多视图与主图都不存在，槽位保持空或从最终 prompt 块移除。
5. 同一主体同时存在多视图与主图时，manifest、prompt slot 与 imagegen plan 的 `reference_images` 必须全部使用多视图路径，不得退回主图。

## Matching Policy

- 默认使用精确主体名匹配。
- 可使用项目内已确认的规范别名，但必须在 manifest 中记录 `matched_by: alias`。
- 不得对子串、泛词、类别词或推测名进行自动绑定。例如“学生”不能自动绑定到“学生群像”，除非源 YAML 或用户显式确认。
- 同名多候选时进入 `ambiguous`，不得选择第一个凑数。

## Slot Output

推荐在 Markdown 中写为：

```markdown
Characters:
- 林寂: projects/aigc/<项目名>/5-设计/角色/3-生成/林寂-多视图.png

Scene:
- 永夜私立中学二年级A班教室: projects/aigc/<项目名>/5-设计/场景/3-生成/永夜私立中学二年级A班教室-多视图.png

Props:
- 红苹果: projects/aigc/<项目名>/5-设计/道具/3-生成/红苹果-多视图.png
```

## Manifest Requirements

`reference-manifest.json` 至少包含：

- `shot_id`
- `characters`
- `scene`
- `props`
- `bound`
- `missing`
- `ambiguous`
- `binding_policy`
- `visual_context_policy`

所有 `bound[].path` 必须是存在的本地图片路径；每个 `bound[]` 应记录 `selected_variant: multi_view | main`，且当同名多视图存在时只能为 `multi_view`。

## Visual Context Gate

- 对所有 `bound[].path`，执行 built-in `image_gen` 前必须逐张调用 `view_image`，让本地参照图进入对话上下文。
- `bound[]` 必须记录 `context_role: character_reference | scene_reference | prop_reference`。
- 场景参照图除 `scene_reference` 外，还必须记录 `style_lock_role: scene_visual_style_reference`，用于锁定画面风格、光影、色调和氛围；若场景图存在但尚未 `view_image`，不得进入 prompt 组织或 imagegen 执行。
- 场景参照图的 `visual_style_lock` 至少记录 `style_notes`、`lighting_notes`、`color_palette_notes`、`atmosphere_notes`、`material_notes`，不得只写“同场景参考”。
- 检视完成后记录 `context_status: visible_in_conversation_context`；未检视时记录 `context_status: pending_view_image`，且不得进入 imagegen 执行。
- 若当前任务是 `prompt_only` 或 `review_only`，可以只记录 `pending_view_image`；一旦进入生成模式，必须补齐检视。
