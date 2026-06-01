# Type: backfill_only

只处理参照图上传和 YAML UUID 回刷，不创建视频节点。

## Fixed Context

- 保持分镜组正文不变。
- 只修改 fenced YAML 中能唯一匹配图片的主体行。
- 回刷格式固定为：`- 图片N 主体名 图片UUID`。
- 同一分镜组内重复 UUID 复用同一个 `图片N`。
- 无匹配主体跳过，不写占位、不猜图。

## Completion Gate

- 每个已上传图片都有 node UUID 和 URL。
- 每个回刷主体都能追溯到上传节点或画布已有节点。
