# Changelog

## 2026-06-01

- 新建 `libTV画布流` Skill 2.0 包。
- 固化当前上下文验证出的最佳实践：本地 YAML 先显式 `图片N 主体名 UUID`，视频节点按该顺序逐张 `--left-add`，并同步写入 `imageList/mixedList/imageListOrder/mixedListOrder`。
- 默认视频规格调整为 `16:9 / 720p / star-video2 / mixed2video`，用户显式指定时覆盖对应默认值。
