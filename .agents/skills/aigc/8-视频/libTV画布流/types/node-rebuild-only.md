# Type: node_rebuild_only

用于 YAML 已经含 `图片N 主体名 UUID` 的情况，只删除或新建视频节点并连线。

## Fixed Context

- 不扫描本地图片作为主体真源；主体顺序完全来自 YAML `图片N`。
- 允许查询 active registry 或画布节点补 URL。
- 默认删除旧视频节点需要用户显式授权。
- 创建节点后必须写入 `imageList/mixedList/imageListOrder/mixedListOrder`。

## Completion Gate

- 非连接件分镜组数量等于新建视频节点数量。
- 每个节点的 `data.params.imageList[].nodeId` 顺序等于 YAML `图片N` 顺序。
