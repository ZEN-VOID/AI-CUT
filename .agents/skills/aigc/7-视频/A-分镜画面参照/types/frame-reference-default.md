# Frame Reference Default Type

固定上下文：

- A 路线以 `4-分组` 的完整分镜组正文为视频 prompt 主体。
- 四段式 `shot_id` 只用于绑定真实本地分镜画面图，不用于改写剧情。
- 有图时先通过 `$libTV` 上传为 OSS URL，再把 URL 编号写入会话消息。
- 无图时移除空参照槽位，保留缺图说明，允许走纯文本 LibTV 会话。
