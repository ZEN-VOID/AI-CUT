# Changelog

## 2026-06-05

- 调整 LibTV 提交 prompt 的 YAML 主体行顺序：由 `图片N 主体名 UUID {{Image N}}` 改为 `图片N 主体名 {{Image N}} UUID`，并保留本地回刷 `图片N 主体名 UUID` 作为 UUID 匹配和顺序锁定格式。
- 完善同一画布内同一分镜组多批次与二次修改的视频节点命名规范：分离 `source_group_id` 与 `video_node_instance_id`，节点唯一名统一为 `vid__<source_group_id>__bNNN__rNN__vNNN`。
- 更新执行合同、审查门禁、输出模板和 registry 结构，要求重生成已存在分镜组时默认新增实例，不得覆盖旧节点，也不得因 `source_group_id` 已存在而跳过。

## 2026-06-01

- 新建 `libTV画布流` Skill 2.0 包。
- 固化当前上下文验证出的最佳实践：本地 YAML 先显式 `图片N 主体名 UUID`，视频节点按该顺序逐张 `--left-add`，并同步写入 `imageList/mixedList/imageListOrder/mixedListOrder`。
- 默认视频规格调整为 `16:9 / 720p / star-video2 / mixed2video`，用户显式指定时覆盖对应默认值。
