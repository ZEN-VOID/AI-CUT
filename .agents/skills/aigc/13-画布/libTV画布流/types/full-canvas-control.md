# Type: full_canvas_control

完整画布控制路线。

## Fixed Context

- 输入真源：`projects/aigc/<项目名>/10-分组/第N集.md`。
- 单集语义范围：`projects/aigc/<项目名>/第N集`，只用于跨系统映射，不替代输入真源或证据目录。
- 默认图片查找范围：
  - `projects/aigc/<项目名>/11-主体/角色/3-生成/`
  - `projects/aigc/<项目名>/11-主体/场景/3-生成/`
  - `projects/aigc/<项目名>/11-主体/道具/3-生成/`
- 默认 LibTV 项目空间：`项目名`；默认画布命名：`第N集`。本地 `projects/aigc/<项目名>` 映射到 LibTV 项目空间名，本地 `第N集` 映射到该项目空间下画布名。如目标项目空间下同名或同项目同集画布已存在，追加 `V2`、`V3`。无法唯一定位项目空间时，退回旧兼容画布名 `项目名-第N集`。
- 默认视频规格：`star-video2`、`mixed2video`、`16:9`、`720p`、`enableSound=on`；用户显式指定时覆盖对应默认值。
- 多分镜图视频节点：若用户提供一组分镜参照图并要求“多分镜参照 / 指明具体分镜段参照分镜图”，必须额外加载 `references/multi-storyboard-video-node-contract.md`，把分镜参照图和主体参照图写入同一个 `imageList/mixedList` 顺序证据，并在 prompt 中逐段绑定 `分镜段 XX -> 时间 -> 图名 -> {{Image N}}`。

## Required Evidence

- `projectUuid`（画布 UUID）
- `local_project_root` / `local_episode` / `local_episode_scope`
- `project_space_name`
- `projectSpaceId` / `folderId`（可得时）
- upload registry
- YAML backfill diff or summary
- video node list
- per-group runtime `imageList` verification
- multi-storyboard segment reference verification when applicable
