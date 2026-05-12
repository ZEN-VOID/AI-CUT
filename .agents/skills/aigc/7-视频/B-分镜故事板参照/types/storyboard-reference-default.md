# Storyboard Reference Default Type

固定上下文：

- B 路线以 `4-分组` 的完整分镜组正文为视频 prompt 主体。
- 故事板图只作为整组视觉参照，不得被描述为唯一首帧。
- 有故事板图时先通过 `$libTV` 上传为 OSS URL，建立“故事板总参照”到 URL 的身份绑定；视频生成框加载完成后，再按 UI 图1/`Image 1` 槽位回刷最终提示词。
- 无故事板图时保持空引用，允许走纯文本 LibTV 会话。
- 视频时长不固定 15 秒；默认读取当前组 `时长估算`，按 4-15 秒范围 clamp 后写入 `duration_hint`。
