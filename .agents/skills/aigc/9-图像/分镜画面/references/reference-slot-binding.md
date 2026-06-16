# Reference Slot Binding Contract

本文件定义 `N4-REF-BIND`：检查角色、场景、道具生成目录，把 `8-分组` 组底 YAML 和组内分镜点中对应主体绑定为 `.agents/skills/cli/imagegen` 组级 imagegen 任务包的参照图。

## Search Roots

固定检查以下目录：

```text
projects/aigc/<项目名>/3-主体/角色/3-生成
projects/aigc/<项目名>/3-主体/场景/3-生成
projects/aigc/<项目名>/3-主体/道具/3-生成
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

## Group Task Slot Output

推荐在 Markdown 中写为：

```markdown
Characters:
- 林寂: projects/aigc/<项目名>/3-主体/角色/3-生成/林寂-多视图.png

Scene:
- 永夜私立中学二年级A班教室: projects/aigc/<项目名>/3-主体/场景/3-生成/永夜私立中学二年级A班教室-多视图.png

Props:
- 红苹果: projects/aigc/<项目名>/3-主体/道具/3-生成/红苹果-多视图.png
```

## Manifest Requirements

`reference-manifest.json` 至少包含：

- `group_id`
- `shot_id`
- `source_yaml_subjects`
- `characters`
- `scene`
- `props`
- `bound`
- `missing`
- `ambiguous`
- `binding_policy`
- `visual_context_policy`

所有 `bound[].path` 必须是存在的本地图片路径；每个 `bound[]` 应记录 `selected_variant: multi_view | main`，且当同名多视图存在时只能为 `multi_view`。组级任务中同一 `group_id` 应有共享 `group_reference_images`，每个 `shot_id` 可记录自己的 `visible_subject_subset`，但不得为同一主体切换不同身份参照图。

## Visual Context Gate

- 对所有 `bound[].path`，执行 imagegen 生成任务前必须逐张调用 `view_image`，让本地参照图进入对话上下文。
- `bound[]` 必须记录 `context_role: character_reference | scene_reference | prop_reference`。
- 场景参照图除 `scene_reference` 外，还必须记录 `style_lock_role: scene_visual_style_reference`，用于锁定画面风格、光影、色调和氛围；若场景图存在但尚未 `view_image`，不得进入 prompt 组织或 imagegen 执行。
- 场景参照图的 `visual_style_lock` 至少记录 `style_notes`、`lighting_notes`、`color_palette_notes`、`atmosphere_notes`、`material_notes`，不得只写“同场景参考”。
- 检视完成后记录 `context_status: visible_in_conversation_context`；未检视时记录 `context_status: pending_view_image`，且不得进入 imagegen 执行。
- 若当前任务是 `prompt_only` 或 `review_only`，可以只记录 `pending_view_image`；一旦进入生成模式，必须补齐检视。

## Review Gate Mapping

| Review Question | Review Gate | Fail Code | Rework Target | Report Evidence |
| --- | --- | --- | --- | --- |
| 是否只从固定的角色、场景、道具 `3-主体/*/3-生成` 目录查找参照，而未从旧目录、JSON 或外部未知 URL 猜测绑定？ | `G4-SLOTS` | `FAIL-FRAME-REF` | `N5-REF-BIND` | `reference-manifest.json` 记录三个 search roots、每个主体的匹配来源和 missing / ambiguous 状态。 |
| 同一主体同时有多视图与主图时，prompt slot、manifest 和 imagegen plan 是否全部绑定多视图，未退回主图？ | `G4-SLOTS` | `FAIL-FRAME-REF` | `N5-REF-BIND` | `bound[].selected_variant: multi_view`；plan 中 `reference_images` 与 manifest 路径一致。 |
| 只有 JSON 或没有真实图片文件的主体是否保持空槽或 missing，而不是伪造可绑定图片？ | `G4-SLOTS` | `FAIL-FRAME-REF` | `N5-REF-BIND` | `missing[]` 记录主体名和原因；所有 `bound[].path` 文件存在且扩展名为图片格式。 |
| 匹配策略是否使用精确主体名或项目内已确认别名，并把泛词、类别词、子串匹配和同名多候选降级为 `ambiguous`？ | `G4-SLOTS` | `FAIL-FRAME-REF` | `N5-REF-BIND` | manifest 记录 `matched_by: exact / alias`；`ambiguous[]` 列出多候选；未出现自动绑定“学生/窗户/文具”等泛词。 |
| `reference-manifest.json` 是否包含 `group_id`、`shot_id`、`source_yaml_subjects`、`characters`、`scene`、`props`、`bound`、`missing`、`ambiguous`、`binding_policy` 和 `visual_context_policy`？ | `G4-REF` | `FAIL-FRAME-REF` | `N4-REF-BIND` | manifest 字段齐全；每个 `group_id` 有共享参照，每个 `shot_id` 可追踪 visible subset。 |
| 所有已绑定本地参照图在生成前是否逐张 `view_image`，并记录 `context_role` 与 `context_status: visible_in_conversation_context`？ | `G7-REF-INPUT` | `FAIL-FRAME-IMAGEGEN` | `N6-REVIEW` / `N7-IMAGEGEN` | manifest / plan / result 记录每张图的 `context_role`、`context_status` 和 `reference_input_status: visible_in_conversation_context`。 |
| 场景参照图是否同时作为 `scene_reference` 与 `scene_visual_style_reference`，并形成风格、光影、色调、氛围、材质五类视觉锁证据？ | `G3C-SCENE-VISUAL-STYLE-LOCK` | `FAIL-FRAME-SCENE-STYLE` | `N3A-SCENE-STYLE` / `N5-REF-BIND` | manifest 中场景图记录 `style_lock_role: scene_visual_style_reference` 与 `visual_style_lock` 五项 notes；prompt block 同步消费。 |
| `prompt_only` / `review_only` 的 `pending_view_image` 是否只停留在非生成模式；一旦进入生成模式是否补齐检视而不是继续执行？ | `G7-REF-INPUT` | `FAIL-FRAME-IMAGEGEN` | `N6-REVIEW` / `N7-IMAGEGEN` | plan/result 中生成任务不存在 `pending_view_image`；若未生成，报告明确 mode 为 `prompt_only` / `review_only`。 |
