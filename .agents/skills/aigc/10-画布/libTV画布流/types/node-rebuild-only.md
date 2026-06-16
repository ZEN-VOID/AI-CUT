# Type: node_rebuild_only

用于 YAML 已经含 `图片N 主体名 UUID` 的情况，只删除或新建视频节点并连线。

## Fixed Context

- 不扫描本地图片作为主体真源；主体顺序完全来自 YAML `图片N`。
- 允许查询 active registry 或画布节点补 URL。
- 默认删除旧视频节点需要用户显式授权。
- 默认重建已存在分镜组时不覆盖旧视频节点，而是创建新的 `video_node_instance_id`；只有用户明确要求“删除/替换旧节点”才对旧实例执行破坏性操作。
- 创建节点后必须写入 `imageList/mixedList/imageListOrder/mixedListOrder`。

## Completion Gate

- 非连接件分镜组数量等于新建视频节点数量。
- 每个新建节点名符合 `vid__<source_group_id>__bNNN__rNN__vNNN`，且 active registry 记录旧实例与新实例。
- 每个节点的 `data.params.imageList[].nodeId` 顺序等于 YAML `图片N` 顺序。
