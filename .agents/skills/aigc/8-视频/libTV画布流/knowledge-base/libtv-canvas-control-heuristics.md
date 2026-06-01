# LibTV Canvas Control Heuristics

- `--left-add` 是画布连线动作，不足以证明 `{{Image N}}` 的最终语义；最终语义只看远端 `data.params.imageList[]`。
- `imageListOrder` 可作为顺序辅助字段，但单独写它不够；必须同步写 `imageList` 和 `mixedList`。
- 删除污染的视频节点后重建，比试图在旧节点上修复所有历史参数更容易审计。
- 同一 UUID 重复出现时，复用同一个 `图片N` 能避免把同一图重复传入模型。
- 默认视频规格为 `star-video2 / mixed2video / 16:9 / 720p`；用户显式指定模型、模式、画幅或分辨率时覆盖对应默认值。
