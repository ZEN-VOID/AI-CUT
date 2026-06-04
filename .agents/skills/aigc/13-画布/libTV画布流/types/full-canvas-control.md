# Type: full_canvas_control

完整画布控制路线。

## Fixed Context

- 输入真源：`projects/aigc/<项目名>/10-分组/第N集.md`。
- 默认图片查找范围：
  - `projects/aigc/<项目名>/11-主体/角色/3-生成/`
  - `projects/aigc/<项目名>/11-主体/场景/3-生成/`
  - `projects/aigc/<项目名>/11-主体/道具/3-生成/`
- 默认画布项目命名：`项目名-第N集`；如同名或同项目同集已存在，追加 `V2`、`V3`。
- 默认视频规格：`star-video2`、`mixed2video`、`16:9`、`720p`、`enableSound=on`；用户显式指定时覆盖对应默认值。

## Required Evidence

- `projectUuid`
- upload registry
- YAML backfill diff or summary
- video node list
- per-group runtime `imageList` verification
