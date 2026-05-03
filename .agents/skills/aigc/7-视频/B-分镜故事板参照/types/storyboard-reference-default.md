# Storyboard Reference Default Type

固定上下文：

- B 路线以 `4-分组` 的完整分镜组正文为视频 prompt 主体。
- 故事板图只作为整组视觉参照，不得被描述为唯一首帧。
- 有故事板图时先通过 `$libTV` 上传为 OSS URL，再把 URL 作为 `参照图1` 写入会话消息。
- 无故事板图时保持空引用，允许走纯文本 LibTV 会话。
